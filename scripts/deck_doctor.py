#!/usr/bin/env python3
"""deck_doctor.py — one-command, end-to-end health check for a SINGLE decklist.

`validate.py` lints the WHOLE repo for the cheap mechanical rules (size, GC count,
filename collisions, clock-citation EXISTS). `deck_doctor.py` is its complement: it
goes DEEP on ONE deck you point it at and adds the two checks validate can't, both
real past misses this repo has made:

  * a Commander BANLIST scan          — the Griselbrand-banned miss (2026-06-24)
  * a COLOR-IDENTITY scan             — Smothering Tithe in Temur, Thopter Foundry
                                        in mono-U (off-colour cards that read fine)

It chains the repo's existing tools so its verdict agrees with the rest of the
tooling rather than re-deriving anything:

  identity   resolve the newest decklist + commander; confirm both load from oracle
  size       exactly 100 (99 library + 1 commander)            [mirrors validate.py]
  singleton  ≤ 1 copy of each non-basic, honouring "any number"/"up to N" cards
             (Relentless Rats, Nazgûl 9, Seven Dwarves 7)      [NEW — singleton rule]
  legality   every card legal in Commander                     [banlist scan]
  colour     every card's colour identity ⊆ the commander's    [CI scan]
  game ch.   ≤ 3 Game Changers, reskin-resolved   [validate.load_game_changers]
  names      no unresolved card names (oracle typos / missing data)
  build      own N of 100 (real + proxy), the buy list + indicative € to finish it
             [NEW — chains unlock_optimizer.load_owned + Scryfall prices]
  clock      cached lab decap/table medians (analysis/pod_gauntlet_clocks.json)
             + does the Summary's Clock: line still match it?   [clock_check.py]
  framework  the deck's Conversion Check score (a datum from deck_registry — the CC
             is judged by hand, not computed; deck_doctor reports it, doesn't grade)
  --run-lab  ALSO run the deck's *_clock_lab.py live and echo the fresh clock grid
  --all      batch dashboard: one PASS/WARN/FAIL row per deck for the whole roster
             (+ --candidates for decks/considering/), same checks, table-rendered
  --diff     swap inspector: cards in/out between two versions + whether the swap
             crossed a legality boundary (size / GC / off-colour / illegal)

Read-only — changes nothing. Exit 1 on any ERROR (illegal / oversized / off-colour /
duplicate / too many GCs), else 0. Safe to wire into a pre-commit hook for a deck
under edit. Buildability prices are INDICATIVE (Scryfall bulk, dated) — never treat
them as quotes (REF: verify-prices); 0-physical-copy = a buy-or-proxy decision, and
whether an OWNED copy is free or locked in another deck stays availability_check.py's
job (pointed to, not re-derived).

Usage
    python scripts/deck_doctor.py radiation-sickness      # active roster (slug or stem)
    python scripts/deck_doctor.py planned-obsolescence    # a decks/considering/ candidate
    python scripts/deck_doctor.py decks/considering/x.txt # any decklist file
    python scripts/deck_doctor.py grand-design --run-lab  # also run the clock lab live
    python scripts/deck_doctor.py planned-obsolescence --run-lab --lab urza_clock_lab:clock
    python scripts/deck_doctor.py --all                   # roster PASS/WARN/FAIL table
    python scripts/deck_doctor.py --all --candidates      # + the considering/ candidates
    python scripts/deck_doctor.py --diff OLD.txt NEW.txt  # swap inspector (did it stay legal?)
"""
import argparse
import json
import math
import re
import subprocess
import sys
from collections import Counter
from functools import lru_cache
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from deck_sim import (  # noqa: E402
    ROOT, ORACLE, parse_deck, load_oracle_index, load_reskin_aliases,
)
import deck_registry as reg          # noqa: E402
import clock_check as cc             # noqa: E402  (SUMMARY map + Clock-line parsers)
import card_lookup                   # noqa: E402  (full oracle records: legality + CI)
from validate import load_game_changers, MAX_GC, DECK_SIZE  # noqa: E402
from availability_check import norm                          # noqa: E402 (front-face normaliser)
from unlock_optimizer import load_owned                       # noqa: E402 (ownership, alias-resolved)

# Windows consoles default to cp1252; card names + en-dashes in echoed lab output
# would crash the report. Force UTF-8.
for _s in (sys.stdout, sys.stderr):
    if hasattr(_s, "reconfigure"):
        try:
            _s.reconfigure(encoding="utf-8", errors="replace")
        except (ValueError, OSError):
            pass

ERROR, WARN, OK, INFO = "ERROR", "WARN", "OK", "INFO"
LAB_TRIALS = 8000        # quick read; the labs default to 40k, pod_gauntlet harvests at 8k


def rel(p):
    """Path relative to the repo root for display, or the bare path if it's outside
    the repo (a decklist passed by an arbitrary absolute path)."""
    try:
        return p.relative_to(ROOT)
    except ValueError:
        return p


# ---------------------------------------------------------------------------
# Target resolution — accept a path, a registry slug, a stem, or a fuzzy name
# ---------------------------------------------------------------------------

def _newest(paths):
    return sorted(paths)[-1] if paths else None


def _stem_to_slug(path, stem2slug):
    """Map a decklist filename back to its active-roster slug (longest stem first,
    so a short stem can't shadow a longer one), or None for a candidate."""
    name = path.name.lower()
    for stem, slug in sorted(stem2slug.items(), key=lambda kv: -len(kv[0])):
        if name.startswith(stem + "-") or name == stem + ".txt":
            return slug
    return None


def resolve_target(arg):
    """Return (decklist_path, slug_or_None). slug ties the deck to its registry row
    (Conversion Check, clock lab, harvested medians); candidates resolve to None."""
    stem2slug = reg.deck_key_index()                       # active stem -> slug

    # 1. an explicit decklist file (resolve to absolute so display/rel() is safe)
    p = Path(arg)
    if p.suffix == ".txt" and p.exists():
        p = p.resolve()
        return p, _stem_to_slug(p, stem2slug)

    key = arg.strip().lower().replace(" ", "-")
    und, hyp = key.replace("-", "_"), key.replace("_", "-")

    # 2. exact registry slug (underscore form)
    if und in reg.DECKS:
        return reg.resolve_deck(reg.DECKS[und]["stem"]), und

    # 3. exact active stem (hyphen form)
    for stem, slug in stem2slug.items():
        if stem == hyp:
            return reg.resolve_deck(stem), slug

    # 4. substring over every decklist on disk (active + candidates)
    pool = (list((ROOT / "decks").glob("*.txt"))
            + list((ROOT / "decks" / "considering").glob("*.txt")))
    subs = [q for q in pool if hyp in q.name.lower()]
    if subs:
        path = _newest(subs)
        return path, _stem_to_slug(path, stem2slug)

    # 5. fuzzy over registry display names ("grand design" -> grand_design)
    needle = key.replace("-", " ")
    fz = [s for s, d in reg.DECKS.items() if needle in d["name"].lower()]
    if len(fz) == 1:
        return reg.resolve_deck(reg.DECKS[fz[0]]["stem"]), fz[0]

    return None, None


# ---------------------------------------------------------------------------
# Full-record oracle index (legality + colour identity, which the slim
# deck_sim index doesn't carry). Keyed by card name AND each face name.
#
# The Scryfall bulk holds one record PER ORACLE CARD plus non-playable extras
# (art series, tokens, emblems …). An "art_series" entry like "Farseek // Farseek"
# is `not_legal` and shares the face name "Farseek" — so it would shadow the real,
# legal Farseek. We skip those layouts and, on any residual same-name collision,
# keep the commander-legal record (a banned oracle card has no legal printing, so
# this never hides a real ban).
# ---------------------------------------------------------------------------

SKIP_LAYOUTS = {"art_series", "token", "double_faced_token", "emblem",
                "scheme", "planar", "vanguard", "augment", "host"}


def _commander_legal(rec):
    return rec.get("legalities", {}).get("commander") == "legal"


@lru_cache(maxsize=1)
def load_full_index():
    # Cached: it parses the 176 MB Scryfall bulk and is hit once per deck — without
    # the cache, --all (16 decks) re-read it 16×. Read-only consumers, safe to share.
    full = {}
    for c in card_lookup.load_cards():
        if c.get("layout") in SKIP_LAYOUTS:
            continue
        names = [c.get("name", "")]
        for f in c.get("card_faces", []) or []:
            names.append(f.get("name", ""))
        for nm in names:
            k = nm.lower()
            if not k:
                continue
            if k not in full or (_commander_legal(c) and not _commander_legal(full[k])):
                full[k] = c           # legality + colour identity are card-level
    return full


def lookup(full, aliases, nm):
    """Resolve a decklist name to its oracle record, trying the reskin alias
    (Morgul-Knife -> Shadowspear) and a leading-'The' normalisation (registry
    'Wise Mothman' vs Scryfall 'The Wise Mothman'). Returns the record or None."""
    low = nm.lower()
    cands = [low, aliases.get(low, nm).lower()]
    cands.append(low[4:] if low.startswith("the ") else "the " + low)
    for k in cands:
        if k in full:
            return full[k]
    return None


# ---------------------------------------------------------------------------
# Card-class helpers (singleton-rule + buildability)
# ---------------------------------------------------------------------------

def _all_text(rec):
    """oracle_text for the card AND every face (DFC/split), lower-cased."""
    parts = [rec.get("oracle_text", "") or ""]
    for f in rec.get("card_faces", []) or []:
        parts.append(f.get("oracle_text", "") or "")
    return " ".join(parts).lower()


def is_basic(rec):
    """Basic lands (incl. Snow basics + Wastes) may appear any number of times."""
    return rec is not None and "Basic" in (rec.get("type_line", "") or "")


_WORDNUM = {w: i for i, w in enumerate(
    "zero one two three four five six seven eight nine ten eleven twelve "
    "thirteen fourteen fifteen".split())}


def singleton_limit(rec):
    """Max copies of this non-basic a legal deck may run. The exemption text comes
    in two shapes, both granted by the card's own oracle text:
      * "A deck can have ANY NUMBER of cards named …"  (Relentless Rats, Dragon's
        Approach, Shadowborn Apostle, Persistent Petitioners, Rat Colony …) -> inf
      * "A deck can have UP TO <n> cards named …"       (Nazgûl 9, Seven Dwarves 7) -> n
    Everything else is the ordinary singleton -> 1."""
    if rec is None:
        return 1
    t = _all_text(rec)
    if "any number of cards named" in t:
        return math.inf
    m = re.search(r"a deck can have up to (\w+) cards named", t)
    if m:
        return _WORDNUM.get(m.group(1), math.inf)   # unknown word -> don't false-flag
    return 1


def eur_price(rec):
    """Indicative non-foil EUR price from the Scryfall bulk, or None. Prices go
    stale (REF: verify-prices) — callers must label this as indicative + dated."""
    if rec is None:
        return None
    p = (rec.get("prices") or {}).get("eur")
    try:
        return float(p) if p is not None else None
    except (TypeError, ValueError):
        return None


def canon_quantities(library, commander, aliases):
    """Per-card counts for the MAIN deck only, keyed the same way ownership is
    (front-face normalised + reskin-aliased), so singleton + buildability agree
    with parse_deck (which excludes the SIDEBOARD) and with load_owned. Re-reading
    the raw .txt would wrongly fold in sideboard/maybeboard lines."""
    q = Counter()
    for nm, _ in library:
        k = norm(nm)
        q[aliases.get(k, k)] += 1
    if commander:
        k = norm(commander)
        q[aliases.get(k, k)] += 1
    return dict(q)


def _data_date():
    """Date of the local Scryfall bulk, for labelling indicative prices."""
    try:
        import datetime
        ts = card_lookup.DATA_FILE.stat().st_mtime
        return datetime.date.fromtimestamp(ts).isoformat()
    except (OSError, AttributeError):
        return "unknown"


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------

class Report:
    """Tallies errors/warns and routes all output. In quiet mode (used by --all)
    nothing prints but the tally + the facts dict still fill, so the batch table is
    driven by the EXACT same checks as the single-deck report — no second code path."""

    def __init__(self, quiet=False):
        self.errors = self.warns = 0
        self.quiet = quiet
        self.facts = {}             # compact per-check data for the --all table

    def line(self, sev, msg):
        if sev == ERROR:
            self.errors += 1
        elif sev == WARN:
            self.warns += 1
        if not self.quiet:
            print(f"  [{sev:5}] {msg}")

    def note(self, msg):
        if not self.quiet:
            print(f"          {msg}")

    def section(self, title):
        if not self.quiet:
            print(f"\n-- {title} --")

    def say(self, msg=""):
        if not self.quiet:
            print(msg)


def doctor(arg, run_lab=False, lab_override=None, trials=LAB_TRIALS,
           quiet=False, check_build=True, csv_path=None):
    path, slug = resolve_target(arg)
    if path is None or not path.exists():
        if not quiet:
            print(f"deck_doctor: could not resolve a decklist from '{arg}'.")
            print("  Try a registry slug (radiation_sickness), a stem (the-grand-design),")
            print("  a candidate name (planned-obsolescence), or a path to a .txt.")
        return {"code": 2, "tag": "ERR", "errors": 1, "warns": 0, "facts": {},
                "title": arg, "slug": None, "candidate": True}

    rpt = Report(quiet=quiet)
    candidate = "considering" in path.parts or slug is None
    reg_row = reg.DECKS.get(slug) if slug else None
    title = (reg_row["name"] if reg_row else path.stem)
    rpt.say(f"=== Deck Doctor — {title} ===")
    rpt.say(f"file: {rel(path)}"
            + (f"   slug: {slug}" if slug else "   (candidate / non-roster)"))

    # --- load oracle data (degrade gracefully if absent) ---
    if not ORACLE.exists():
        rpt.say(f"\nNOTE: {ORACLE.relative_to(ROOT)} not present — legality, colour-identity")
        rpt.say("      and unresolved-name checks are SKIPPED. Run "
                "`python scripts/update_scryfall_data.py`.")
        oracle = False
        index = {}
    else:
        oracle = True
        index = load_oracle_index()
    aliases = load_reskin_aliases()
    full = load_full_index() if oracle else {}     # legality + CI + prices + classes
    library, commander, diag = parse_deck(path, index, aliases)
    pool = [n for n, _ in library] + ([commander] if commander else [])
    quantities = canon_quantities(library, commander, aliases)  # main deck only

    # --- 1. size ---------------------------------------------------------
    rpt.section("size")
    total = len(library) + (1 if commander else 0)
    rpt.facts["size"] = total
    if commander is None:
        rpt.line(WARN, f"commander not recognised — size unverifiable "
                       f"(library={len(library)})")
    elif total != DECK_SIZE:
        rpt.line(ERROR, f"deck size {total} ({len(library)} library + commander), "
                        f"expected {DECK_SIZE}")
    else:
        rpt.line(OK, f"{total} cards (99 + {commander})")

    # --- 2. singleton rule (max 1 per non-basic) ------------------------
    # A genuine legality gap validate.py doesn't cover. parse_deck EXPANDS
    # quantities (it doesn't collapse dupes), so a >1 count is real, not an
    # artifact. Basics + "any number" cards (Relentless Rats, Dragon's
    # Approach, Shadowborn Apostle …) are exempt — read from oracle text, DRY.
    rpt.section("singleton rule")
    if not oracle:
        rpt.line(WARN, "skipped (no oracle data)")
    else:
        dupes = []
        for card, n in quantities.items():
            if n <= 1:
                continue
            rec = lookup(full, aliases, card)
            if is_basic(rec):
                continue
            lim = singleton_limit(rec)
            if n <= lim:
                continue
            dupes.append((rec.get("name", card) if rec else card, n, lim))
        rpt.facts["singleton"] = len(dupes)
        if dupes:
            for nm, n, lim in sorted(dupes):
                why = ("singleton violation (max 1 per non-basic)" if lim == 1
                       else f"exceeds this card's {lim}-copy limit")
                rpt.line(ERROR, f"{nm} x{n} — {why}")
        else:
            rpt.line(OK, "no illegal duplicates (singleton rule holds)")

    # --- 3. Commander legality (banlist) --------------------------------
    rpt.section("legality (Commander banlist)")
    if not oracle:
        rpt.line(WARN, "skipped (no oracle data)")
    else:
        illegal, missing = [], []
        for nm in pool:
            rec = lookup(full, aliases, nm)
            if rec is None:
                missing.append(nm)
                continue
            status = rec.get("legalities", {}).get("commander", "unknown")
            if status != "legal":
                illegal.append((nm, status))
        rpt.facts["illegal"] = len(illegal)
        rpt.facts["missing"] = len(missing)
        if illegal:
            for nm, st in illegal:
                rpt.line(ERROR, f"{nm} — {st} in Commander")
        else:
            rpt.line(OK, f"all {len(pool)} cards legal in Commander")
        if missing:
            shown = ", ".join(missing[:6])
            more = f" (+{len(missing) - 6})" if len(missing) > 6 else ""
            rpt.line(WARN, f"{len(missing)} card(s) not found in oracle data "
                           f"(can't check legality/colour): {shown}{more}")

        # --- 4. colour identity ----------------------------------------
        rpt.section("colour identity")
        cmd_rec = lookup(full, aliases, commander) if commander else None
        if cmd_rec is None:
            rpt.line(WARN, "commander not found in oracle data — CI check skipped")
        else:
            cmd_ci = set(cmd_rec.get("color_identity", []))
            offcolor = []
            for nm in pool:
                rec = lookup(full, aliases, nm)
                if rec is None:
                    continue
                ci = set(rec.get("color_identity", []))
                if not ci <= cmd_ci:
                    offcolor.append((nm, "".join(sorted(ci - cmd_ci))))
            rpt.facts["offcolor"] = len(offcolor)
            ci_str = "".join(sorted(cmd_ci)) or "C"
            if offcolor:
                for nm, extra in offcolor:
                    rpt.line(ERROR, f"{nm} — adds {{{extra}}} outside the "
                                    f"commander's {{{ci_str}}} identity")
            else:
                rpt.line(OK, f"all cards within the commander's {{{ci_str}}} identity")
            rpt.note("(checked vs the single resolved commander; partners not modelled)")

    # --- 5. Game Changers ------------------------------------------------
    rpt.section("Game Changers")
    gc_names = load_game_changers()
    gc_hits = {}
    for n in pool:
        canon = aliases.get(n.lower(), n).lower()
        if canon in gc_names:
            gc_hits[canon] = gc_names[canon]
    rpt.facts["gc"] = len(gc_hits)
    if len(gc_hits) > MAX_GC:
        rpt.line(ERROR, f"{len(gc_hits)} Game Changers (max {MAX_GC}): "
                        + ", ".join(sorted(gc_hits.values())))
    else:
        listed = ", ".join(sorted(gc_hits.values())) or "none"
        rpt.line(OK, f"{len(gc_hits)}/{MAX_GC} Game Changers: {listed}")

    # --- 6. unresolved names --------------------------------------------
    rpt.section("unresolved card names")
    if not oracle:
        rpt.line(WARN, "skipped (no oracle data)")
    elif diag["unresolved"]:
        shown = ", ".join(diag["unresolved"][:6])
        more = f" (+{len(diag['unresolved']) - 6})" if len(diag["unresolved"]) > 6 else ""
        rpt.line(WARN, f"{len(diag['unresolved'])} unresolved (typo / reskin / missing): "
                       f"{shown}{more}")
    else:
        rpt.line(OK, "every card name resolves to oracle data")

    # --- 7. buildability (ownership + buy cost) -------------------------
    # The doctor proves a deck is LEGAL; this proves it's BUILDABLE. Chains the
    # ownership logic (unlock_optimizer.load_owned, alias-resolved
    # both sides) + indicative Scryfall EUR prices. Basics are assumed owned
    # (unlimited). Contention (is an owned copy free or locked in another deck?)
    # stays availability_check.py's job — pointed to below, not re-derived here.
    if check_build:
        rpt.section("buildability (ownership + buy cost)")
        csvs = sorted((ROOT / "collection").glob("moxfield_haves_*.csv"))
        cpath = Path(csv_path) if csv_path else (csvs[-1] if csvs else None)
        if cpath is None or not cpath.exists():
            rpt.line(WARN, "skipped (no collection/moxfield_haves_*.csv found)")
        elif not oracle:
            rpt.line(WARN, "skipped (no oracle data — can't class basics / price)")
        else:
            owned, proxy = load_owned(cpath, aliases)
            total_need = sum(quantities.values())
            have = 0
            buys = []                              # (name, shortfall, eur_or_None)
            for card, qty in quantities.items():
                rec = lookup(full, aliases, card)
                if is_basic(rec):
                    have += qty                    # unlimited basics
                    continue
                # Join ownership on BOTH name forms, because neither alone is
                # sufficient: the deck key (handles "Exsanguinate" owned under its
                # own name while its oracle record's front face is "Stensian
                # Sanguinist // Exsanguinate") AND the oracle canonical front-face
                # (handles the registry's "Wise Mothman" -> CSV "The Wise Mothman",
                # and UB reskins). The CSV holds a card under one of these, so summing
                # the distinct keys finds it without double-counting.
                keys = {card}
                if rec:
                    ok = norm(rec.get("name", card))
                    keys.add(aliases.get(ok, ok))
                phys = sum(owned.get(k, 0) + proxy.get(k, 0) for k in keys)
                have += min(phys, qty)
                if qty - phys > 0:
                    buys.append((rec.get("name", card) if rec else card,
                                 qty - phys, eur_price(rec)))
            priced = [b for b in buys if b[2] is not None]
            unpriced = [b for b in buys if b[2] is None]
            buy_eur = sum(b[2] * b[1] for b in priced)
            rpt.facts.update(owned=have, need=total_need, buy_n=len(buys),
                             buy_eur=buy_eur, buy_unpriced=len(unpriced))
            rpt.line(OK if not buys else INFO,
                     f"own {have}/{total_need} cards "
                     f"(real + proxy; {cpath.name}; basics assumed owned)")
            if buys:
                est = f"≈ €{buy_eur:,.0f}" if priced else "€?"
                tail = f" ({len(unpriced)} unpriced)" if unpriced else ""
                rpt.line(INFO, f"buy list: {len(buys)} card(s) not physically owned, "
                               f"{est}{tail}  [indicative, Scryfall {_data_date()}]")
                for nm, short, eur in sorted(buys, key=lambda b: -(b[2] or 0))[:15]:
                    price = f"€{eur:,.2f}" if eur is not None else "€?"
                    qtag = f" x{short}" if short > 1 else ""
                    rpt.note(f"{price:>9}  {nm}{qtag}")
                if len(buys) > 15:
                    rpt.note(f"… +{len(buys) - 15} more")
            rpt.note("contention (is an owned copy free or locked elsewhere?): "
                     "availability_check.py / unlock_optimizer.py")

    # --- 8. clock (cached medians + Summary drift) ----------------------
    rpt.section("clock")
    clocks = (json.loads(cc.CLOCKS_JSON.read_text(encoding="utf-8"))
              if cc.CLOCKS_JSON.exists() else {})
    rec = clocks.get(slug) if slug else None
    if rec:
        rpt.line(OK, f"lab medians — decap {rec['med'][0]} / table {rec['med'][1]} "
                     f"(never {rec['never'][0]}%/{rec['never'][1]}%, {rec['src']})")
        # Summary clock-line drift (reuses clock_check's parsers)
        fname = cc.SUMMARY.get(slug)
        spath = (ROOT / "decks" / fname) if fname else None
        if spath and spath.exists():
            line = cc.find_clock_line(spath.read_text(encoding="utf-8"))
            if line is None:
                rpt.line(WARN, f"{fname}: no canonical Clock: line found")
            else:
                cites = cc.cited_turns(line)
                vd, nd = cc.classify(cites["decap"], cc.parse_med(rec["med"][0]))
                vt, nt = cc.classify(cites["table"], cc.parse_med(rec["med"][1]))
                sev = ERROR if "DRIFT" in (vd, vt) else (
                    WARN if "UNPARSED" in (vd, vt) else OK)
                # DRIFT is a real correctness problem for a deck under audit -> ERROR
                rpt.line(sev if sev != ERROR else WARN,
                         f"Summary Clock: decap {vd} ({nd}) / table {vt} ({nt})")
                if sev != OK:
                    rpt.note(f"cite: {line.strip()[:110]}")
    elif slug:
        rpt.line(WARN, "no harvested clock — run "
                       "`python scripts/pod_gauntlet.py --refresh` to populate it")
    else:
        rpt.line(INFO, "candidate deck — not in the harvested clock set; "
                       "run its bespoke *_clock_lab.py (see --run-lab --lab)")

    # --- 9. framework datum (Conversion Check) --------------------------
    rpt.section("Conversion Check (reported, not computed)")
    if reg_row and reg_row.get("cc") is not None:
        core, kill, dur, inter = reg_row["cc_axes"]
        rpt.line(INFO, f"CC {reg_row['cc']}/20  "
                       f"(core {core} · kill {kill} · durability {dur} · interaction {inter})")
    elif reg_row:
        rpt.line(INFO, "no Conversion Check score on file for this roster deck")
    else:
        rpt.line(INFO, "candidate deck — no Conversion Check score yet")

    # --- 10. optional: run the clock lab live ---------------------------
    if run_lab:
        rpt.section("live clock lab")
        lab = None
        if lab_override:
            mod, _, mode = lab_override.partition(":")
            lab = (mod, mode or "clock")
        elif reg_row and reg_row.get("lab"):
            lab = reg_row["lab"]
        if lab is None:
            rpt.line(WARN, "no clock lab known for this deck — pass --lab module:mode "
                           "(e.g. --lab urza_clock_lab:clock)")
        else:
            mod, mode = lab
            script = ROOT / "scripts" / f"{mod}.py"
            if not script.exists():
                rpt.line(ERROR, f"lab script {script.name} not found")
            else:
                cmd = [sys.executable, str(script), "--mode", mode,
                       "--trials", str(trials)]
                rpt.say(f"  $ {' '.join(cmd[1:])}")
                try:
                    out = subprocess.run(cmd, capture_output=True, text=True,
                                         timeout=600)
                    body = (out.stdout or "").rstrip()
                    for ln in body.splitlines():
                        rpt.say(f"  | {ln}")
                    if out.returncode != 0:
                        rpt.line(WARN, f"lab exited {out.returncode}; "
                                       f"stderr: {(out.stderr or '').strip()[:200]}")
                except subprocess.TimeoutExpired:
                    rpt.line(WARN, f"lab timed out at {trials} trials")

    # --- verdict ---------------------------------------------------------
    rpt.section("next steps")
    if slug:
        rpt.say(f"  pod standing : python scripts/pod_gauntlet.py   "
                f"(P(beat the pod) for {slug})")
    rpt.say("  clock drift  : python scripts/clock_check.py")
    rpt.say("  buildability : python scripts/unlock_optimizer.py | availability_check.py")
    rpt.say("  full repo    : python scripts/validate.py")

    tag = "FAIL" if rpt.errors else ("WARN" if rpt.warns else "PASS")
    rpt.say(f"\n=== {tag}: {rpt.errors} error(s), {rpt.warns} warning(s) ===")
    return {"code": 1 if rpt.errors else 0, "tag": tag, "errors": rpt.errors,
            "warns": rpt.warns, "facts": rpt.facts, "title": title, "slug": slug,
            "candidate": candidate}


# ---------------------------------------------------------------------------
# --all batch dashboard
# ---------------------------------------------------------------------------

def _flag(facts, key):
    """Render a count cell for the batch table: '·' for 0/None (all-clear), else
    the number — so any digit in the sing/ill/off columns reads as a problem."""
    v = facts.get(key)
    return "·" if v in (None, 0) else str(v)


def batch(include_candidates=False, csv_path=None):
    """Run the quiet doctor over the whole active roster (+ optionally the
    considering/ candidates) and print one PASS/WARN/FAIL row per deck. Same
    checks as the single-deck report — just rendered as a table."""
    targets = [(slug, None) for slug in reg.DECKS]
    if include_candidates:
        for p in sorted((ROOT / "decks" / "considering").glob("*.txt")):
            targets.append((None, p))

    print(f"=== Deck Doctor — batch ({len(targets)} decks"
          f"{', incl. candidates' if include_candidates else ''}) ===\n")
    hdr = (f"{'verdict':7} {'deck':28} {'size':>4} {'sing':>4} {'ill':>3} "
           f"{'off':>3} {'GC':>3} {'owned':>7} {'buy €':>8}")
    print(hdr)
    print("-" * len(hdr))

    worst = 0
    rows = []
    for slug, path in targets:
        res = doctor(path if path else slug, quiet=True, csv_path=csv_path)
        f = res["facts"]
        own = (f"{f['owned']}/{f['need']}" if "owned" in f else "—")
        if f.get("buy_n"):
            buy = f"€{f['buy_eur']:,.0f}" + ("+" if f.get("buy_unpriced") else "")
        elif "owned" in f:
            buy = "—"
        else:
            buy = "?"
        rows.append((res, f, own, buy))
        worst = max(worst, res["code"])

    # active first (registry order), then candidates, FAIL/WARN floated up within
    rows.sort(key=lambda r: (r[0]["candidate"], {"FAIL": 0, "WARN": 1}.get(r[0]["tag"], 2)))
    for res, f, own, buy in rows:
        size = f.get("size", "?")
        size_cell = str(size) if size == DECK_SIZE else f"!{size}"
        print(f"{res['tag']:7} {res['title'][:28]:28} {size_cell:>4} "
              f"{_flag(f,'singleton'):>4} {_flag(f,'illegal'):>3} "
              f"{_flag(f,'offcolor'):>3} {str(f.get('gc','?')):>3} "
              f"{own:>7} {buy:>8}")

    n_fail = sum(1 for r in rows if r[0]["tag"] == "FAIL")
    n_warn = sum(1 for r in rows if r[0]["tag"] == "WARN")
    print(f"\n=== {len(rows)} decks: {n_fail} FAIL, {n_warn} WARN, "
          f"{len(rows) - n_fail - n_warn} PASS ===")
    print("  columns: size(!=100 prefixed !) · sing(leton) · ill(egal) · off(-colour) "
          "· GC · owned/100 · buy € (indicative; + = unpriced cards)")
    print("  drill into any deck: python scripts/deck_doctor.py <slug>")
    return 1 if worst else 0


# ---------------------------------------------------------------------------
# --diff swap inspector
# ---------------------------------------------------------------------------

def diff(old_arg, new_arg, csv_path=None):
    """Compare two decklist versions: cards in/out, plus whether the swap CROSSED a
    boundary (size off 100, GC over cap, a newly illegal / off-colour / duplicate
    card). The legality verdicts come from the SAME quiet doctor that grades a single
    deck, so a diff that says 'still PASS' means exactly that. Clock impact is NOT
    inferable from two static lists — flagged for a re-lab, never guessed."""
    old_path, _ = resolve_target(old_arg)
    new_path, new_slug = resolve_target(new_arg)
    for arg, p in ((old_arg, old_path), (new_arg, new_path)):
        if p is None or not p.exists():
            print(f"deck_doctor --diff: could not resolve '{arg}'.")
            return 2

    print(f"=== Deck Doctor — diff ===")
    print(f"old: {rel(old_path)}")
    print(f"new: {rel(new_path)}")

    # Grade both with the identical checks (build off — ownership isn't a swap concern)
    old_res = doctor(old_path, quiet=True, check_build=False, csv_path=csv_path)
    new_res = doctor(new_path, quiet=True, check_build=False, csv_path=csv_path)
    of, nf = old_res["facts"], new_res["facts"]

    # Card-level delta — parse both with one shared (cached) index, canon-keyed so a
    # reskin printed differently across versions doesn't read as a swap.
    aliases = load_reskin_aliases()
    index = load_oracle_index() if ORACLE.exists() else {}
    full = load_full_index() if ORACLE.exists() else {}
    libO, cmdO, _ = parse_deck(old_path, index, aliases)
    libN, cmdN, _ = parse_deck(new_path, index, aliases)
    qO = canon_quantities(libO, cmdO, aliases)
    qN = canon_quantities(libN, cmdN, aliases)
    added = {c: qN[c] - qO.get(c, 0) for c in qN if qN[c] > qO.get(c, 0)}
    removed = {c: qO[c] - qN.get(c, 0) for c in qO if qO[c] > qN.get(c, 0)}

    gc_names = load_game_changers()
    cmd_rec = lookup(full, aliases, cmdN) if cmdN else None
    cmd_ci = set(cmd_rec.get("color_identity", [])) if cmd_rec else None

    def disp(c):
        rec = lookup(full, aliases, c)
        return rec.get("name", c) if rec else c.title()

    def annotate(c):
        """Why this added card might matter: GC, off-colour, or banned."""
        rec = lookup(full, aliases, c)
        tags = []
        if c in gc_names:
            tags.append("GC")
        if rec and cmd_ci is not None:
            extra = set(rec.get("color_identity", [])) - cmd_ci
            if extra:
                tags.append("off-colour {" + "".join(sorted(extra)) + "}")
        if rec and rec.get("legalities", {}).get("commander") != "legal":
            tags.append("BANNED")
        return ("  [" + ", ".join(tags) + "]") if tags else ""

    if cmdO and cmdN and cmdO.lower() != cmdN.lower():
        print(f"\nNOTE: commander changed {cmdO} -> {cmdN} (this is more than a swap).")

    print(f"\n-- cards out ({sum(removed.values())}) --")
    for c in sorted(removed):
        n = removed[c]
        print(f"  - {('x' + str(n) + ' ') if n > 1 else ''}{disp(c)}")
    if not removed:
        print("  (none)")
    print(f"\n-- cards in ({sum(added.values())}) --")
    for c in sorted(added):
        n = added[c]
        print(f"  + {('x' + str(n) + ' ') if n > 1 else ''}{disp(c)}{annotate(c)}")
    if not added:
        print("  (none)")

    # Boundary crossings — read straight off the two facts dicts.
    print("\n-- boundary checks (old -> new) --")
    crossed = []

    def show(label, key, is_bad, fmt=str):
        o, n = of.get(key), nf.get(key)
        if o is None and n is None:
            return
        mark = ""
        if is_bad(n):
            mark = "  <-- NEWLY over limit" if not is_bad(o) else "  <-- still over limit"
            crossed.append(label)
        elif is_bad(o) and not is_bad(n):
            mark = "  <-- fixed"
        print(f"  {label:14} {fmt(o)} -> {fmt(n)}{mark}")

    show("size", "size", lambda v: v not in (None, DECK_SIZE))
    show("Game Changers", "gc", lambda v: v is not None and v > MAX_GC)
    show("singleton", "singleton", lambda v: bool(v))
    show("illegal", "illegal", lambda v: bool(v))
    show("off-colour", "offcolor", lambda v: bool(v))

    print(f"\n-- clock --")
    clocks = (json.loads(cc.CLOCKS_JSON.read_text(encoding="utf-8"))
              if cc.CLOCKS_JSON.exists() else {})
    crec = clocks.get(new_slug) if new_slug else None
    if crec:
        print(f"  cached lab medians (per slug, NOT per file): decap {crec['med'][0]} "
              f"/ table {crec['med'][1]} ({crec['src']})")
    print("  a static diff can't measure clock movement — re-run the lab on the new "
          "list to confirm:")
    print(f"  python scripts/deck_doctor.py {rel(new_path)} --run-lab")

    print(f"\n-- verdict --")
    print(f"  {old_res['tag']} -> {new_res['tag']}")
    if crossed:
        print(f"  swap CROSSED a boundary: {', '.join(crossed)}")
        return 1
    print("  swap stayed within every legality boundary "
          "(clock unverified — see above)")
    return 0


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("deck", nargs="?",
                    help="registry slug, decklist stem, candidate name, or a .txt path")
    ap.add_argument("--all", action="store_true",
                    help="batch dashboard: PASS/WARN/FAIL table for the whole roster")
    ap.add_argument("--candidates", action="store_true",
                    help="with --all, also include decks/considering/ candidates")
    ap.add_argument("--diff", nargs=2, metavar=("OLD", "NEW"),
                    help="swap inspector: cards in/out + boundary crossings between two versions")
    ap.add_argument("--csv", help="Moxfield haves CSV for buildability (default: newest)")
    ap.add_argument("--no-build", action="store_true",
                    help="skip the ownership/buy-cost check (single-deck mode)")
    ap.add_argument("--run-lab", action="store_true",
                    help="also run the deck's *_clock_lab.py live and echo the grid")
    ap.add_argument("--lab", metavar="MODULE:MODE",
                    help="clock-lab override for candidates (e.g. urza_clock_lab:clock)")
    ap.add_argument("--trials", type=int, default=LAB_TRIALS,
                    help=f"trials for --run-lab (default {LAB_TRIALS})")
    args = ap.parse_args()

    if args.diff:
        return diff(args.diff[0], args.diff[1], csv_path=args.csv)
    if args.all:
        return batch(include_candidates=args.candidates, csv_path=args.csv)
    if not args.deck:
        ap.error("a deck is required (or pass --all / --diff)")
    return doctor(args.deck, run_lab=args.run_lab, lab_override=args.lab,
                  trials=args.trials, check_build=not args.no_build,
                  csv_path=args.csv)["code"]


if __name__ == "__main__":
    sys.exit(main())
