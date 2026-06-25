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
  legality   every card legal in Commander                     [NEW — banlist scan]
  colour     every card's colour identity ⊆ the commander's    [NEW — CI scan]
  game ch.   ≤ 3 Game Changers, reskin-resolved   [validate.load_game_changers]
  names      no unresolved card names (oracle typos / missing data)
  clock      cached lab decap/table medians (analysis/pod_gauntlet_clocks.json)
             + does the Summary's Clock: line still match it?   [clock_check.py]
  framework  the deck's Conversion Check score (a datum from deck_registry — the CC
             is judged by hand, not computed; deck_doctor reports it, doesn't grade)
  --run-lab  ALSO run the deck's *_clock_lab.py live and echo the fresh clock grid

Read-only — changes nothing. Exit 1 on any ERROR (illegal / oversized / off-colour /
too many GCs), else 0. Safe to wire into a pre-commit hook for a deck under edit.

Usage
    python scripts/deck_doctor.py radiation-sickness      # active roster (slug or stem)
    python scripts/deck_doctor.py planned-obsolescence    # a decks/considering/ candidate
    python scripts/deck_doctor.py decks/considering/x.txt # any decklist file
    python scripts/deck_doctor.py grand-design --run-lab  # also run the clock lab live
    python scripts/deck_doctor.py planned-obsolescence --run-lab --lab urza_clock_lab:clock
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from deck_sim import (  # noqa: E402
    ROOT, ORACLE, parse_deck, load_oracle_index, load_reskin_aliases,
)
import deck_registry as reg          # noqa: E402
import clock_check as cc             # noqa: E402  (SUMMARY map + Clock-line parsers)
import card_lookup                   # noqa: E402  (full oracle records: legality + CI)
from validate import load_game_changers, MAX_GC, DECK_SIZE  # noqa: E402

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


def load_full_index():
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
# Report
# ---------------------------------------------------------------------------

class Report:
    def __init__(self):
        self.errors = self.warns = 0

    def line(self, sev, msg):
        if sev == ERROR:
            self.errors += 1
        elif sev == WARN:
            self.warns += 1
        print(f"  [{sev:5}] {msg}")

    def note(self, msg):
        print(f"          {msg}")


def doctor(arg, run_lab=False, lab_override=None, trials=LAB_TRIALS):
    path, slug = resolve_target(arg)
    if path is None or not path.exists():
        print(f"deck_doctor: could not resolve a decklist from '{arg}'.")
        print("  Try a registry slug (radiation_sickness), a stem (the-grand-design),")
        print("  a candidate name (planned-obsolescence), or a path to a .txt.")
        return 2

    rpt = Report()
    candidate = "considering" in path.parts or slug is None
    reg_row = reg.DECKS.get(slug) if slug else None
    title = (reg_row["name"] if reg_row else path.stem)
    print(f"=== Deck Doctor — {title} ===")
    print(f"file: {rel(path)}"
          + (f"   slug: {slug}" if slug else "   (candidate / non-roster)"))

    # --- load oracle data (degrade gracefully if absent) ---
    if not ORACLE.exists():
        print(f"\nNOTE: {ORACLE.relative_to(ROOT)} not present — legality, colour-identity")
        print("      and unresolved-name checks are SKIPPED. Run "
              "`python scripts/update_scryfall_data.py`.")
        oracle = False
        index = {}
    else:
        oracle = True
        index = load_oracle_index()
    aliases = load_reskin_aliases()
    library, commander, diag = parse_deck(path, index, aliases)
    pool = [n for n, _ in library] + ([commander] if commander else [])

    # --- 1. size ---------------------------------------------------------
    print("\n-- size --")
    total = len(library) + (1 if commander else 0)
    if commander is None:
        rpt.line(WARN, f"commander not recognised — size unverifiable "
                       f"(library={len(library)})")
    elif total != DECK_SIZE:
        rpt.line(ERROR, f"deck size {total} ({len(library)} library + commander), "
                        f"expected {DECK_SIZE}")
    else:
        rpt.line(OK, f"{total} cards (99 + {commander})")

    # --- 2. Commander legality (banlist) --------------------------------
    print("\n-- legality (Commander banlist) --")
    if not oracle:
        rpt.line(WARN, "skipped (no oracle data)")
    else:
        full = load_full_index()
        illegal, missing = [], []
        for nm in pool:
            rec = lookup(full, aliases, nm)
            if rec is None:
                missing.append(nm)
                continue
            status = rec.get("legalities", {}).get("commander", "unknown")
            if status != "legal":
                illegal.append((nm, status))
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

        # --- 3. colour identity ----------------------------------------
        print("\n-- colour identity --")
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
            ci_str = "".join(sorted(cmd_ci)) or "C"
            if offcolor:
                for nm, extra in offcolor:
                    rpt.line(ERROR, f"{nm} — adds {{{extra}}} outside the "
                                    f"commander's {{{ci_str}}} identity")
            else:
                rpt.line(OK, f"all cards within the commander's {{{ci_str}}} identity")
            rpt.note("(checked vs the single resolved commander; partners not modelled)")

    # --- 4. Game Changers ------------------------------------------------
    print("\n-- Game Changers --")
    gc_names = load_game_changers()
    gc_hits = {}
    for n in pool:
        canon = aliases.get(n.lower(), n).lower()
        if canon in gc_names:
            gc_hits[canon] = gc_names[canon]
    if len(gc_hits) > MAX_GC:
        rpt.line(ERROR, f"{len(gc_hits)} Game Changers (max {MAX_GC}): "
                        + ", ".join(sorted(gc_hits.values())))
    else:
        listed = ", ".join(sorted(gc_hits.values())) or "none"
        rpt.line(OK, f"{len(gc_hits)}/{MAX_GC} Game Changers: {listed}")

    # --- 5. unresolved names --------------------------------------------
    print("\n-- unresolved card names --")
    if not oracle:
        rpt.line(WARN, "skipped (no oracle data)")
    elif diag["unresolved"]:
        shown = ", ".join(diag["unresolved"][:6])
        more = f" (+{len(diag['unresolved']) - 6})" if len(diag["unresolved"]) > 6 else ""
        rpt.line(WARN, f"{len(diag['unresolved'])} unresolved (typo / reskin / missing): "
                       f"{shown}{more}")
    else:
        rpt.line(OK, "every card name resolves to oracle data")

    # --- 6. clock (cached medians + Summary drift) ----------------------
    print("\n-- clock --")
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

    # --- 7. framework datum (Conversion Check) --------------------------
    print("\n-- Conversion Check (reported, not computed) --")
    if reg_row and reg_row.get("cc") is not None:
        core, kill, dur, inter = reg_row["cc_axes"]
        rpt.line(INFO, f"CC {reg_row['cc']}/20  "
                       f"(core {core} · kill {kill} · durability {dur} · interaction {inter})")
    elif reg_row:
        rpt.line(INFO, "no Conversion Check score on file for this roster deck")
    else:
        rpt.line(INFO, "candidate deck — no Conversion Check score yet")

    # --- 8. optional: run the clock lab live ----------------------------
    if run_lab:
        print("\n-- live clock lab --")
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
                print(f"  $ {' '.join(cmd[1:])}")
                try:
                    out = subprocess.run(cmd, capture_output=True, text=True,
                                         timeout=600)
                    body = (out.stdout or "").rstrip()
                    for ln in body.splitlines():
                        print(f"  | {ln}")
                    if out.returncode != 0:
                        rpt.line(WARN, f"lab exited {out.returncode}; "
                                       f"stderr: {(out.stderr or '').strip()[:200]}")
                except subprocess.TimeoutExpired:
                    rpt.line(WARN, f"lab timed out at {trials} trials")

    # --- verdict ---------------------------------------------------------
    print("\n-- next steps --")
    if slug:
        print(f"  pod standing : python scripts/pod_gauntlet.py   "
              f"(P(beat the pod) for {slug})")
    print("  clock drift  : python scripts/clock_check.py")
    print("  full repo    : python scripts/validate.py")

    tag = "FAIL" if rpt.errors else ("WARN" if rpt.warns else "PASS")
    print(f"\n=== {tag}: {rpt.errors} error(s), {rpt.warns} warning(s) ===")
    return 1 if rpt.errors else 0


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("deck", help="registry slug, decklist stem, candidate name, or a .txt path")
    ap.add_argument("--run-lab", action="store_true",
                    help="also run the deck's *_clock_lab.py live and echo the grid")
    ap.add_argument("--lab", metavar="MODULE:MODE",
                    help="clock-lab override for candidates (e.g. urza_clock_lab:clock)")
    ap.add_argument("--trials", type=int, default=LAB_TRIALS,
                    help=f"trials for --run-lab (default {LAB_TRIALS})")
    args = ap.parse_args()
    return doctor(args.deck, run_lab=args.run_lab, lab_override=args.lab, trials=args.trials)


if __name__ == "__main__":
    sys.exit(main())
