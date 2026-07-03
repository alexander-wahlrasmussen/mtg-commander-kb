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
             [chains unlock_optimizer.load_owned + Scryfall prices]
  bracket    estimated WotC bracket from GC + MLD + infinite + fast-mana signals,
             AND the pod house-rule gate: mass land denial = ERROR, extra-turn
             chains flagged  [NEW — REF_Bracket_3_House_Rules.md]
  --vitals   consistency: keepable opening-hand %% + ramp/draw count-by-turn vs the
             BDD anchors  [NEW — chains deck_sim.simulate / need-source MC]
  --combos   intended kill line present? + Commander Spellbook combo DB (complete /
             one-away / repeatable-extra-turn red line)  [NEW — chains find_combos]
  --interaction  resilience: can the deck answer an artifact / enchantment / creature
             / land, and get past indestructible + hexproof/shroud/ward? Heuristic
             over oracle text  [NEW — Trinket Mage "win any game" pillar 1]
  --footprint  hidden-commander rule 2: %% of nonland cards that go dead without the
             engine (the win_line build-around) — ramp/draw/tutor/removal/standalone
             body = a floor; the rest are low-floor synergy slots. Heuristic, INFO-
             only  [NEW — Cubrious "two rules for a hidden-commander deck"]
  --fragility  permanent-type removal/wipe exposure: %% of nonland permanents on the
             most-removable types (planeswalker/creature) + which win_line engine
             pieces sit on a fragile type, on the 7-tier durability ladder. Heuristic,
             INFO-only  [NEW — REF_Multiplayer_Card_Eval.md, "500 decks" lesson 2b]
  clock      cached lab decap/table medians (analysis/pod_gauntlet_clocks.json)
             + does the Summary's Clock: line still match it?   [clock_check.py]
  framework  the deck's Conversion Check score (a datum from deck_registry — the CC
             is judged by hand, not computed; deck_doctor reports it, doesn't grade)
  --run-lab  ALSO run the deck's *_clock_lab.py live and echo the fresh clock grid
  --deep     run everything, including --vitals, --combos, --interaction, --footprint,
             --fragility
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
    python scripts/deck_doctor.py zero-sum-game --deep    # + vitals + combos + bracket
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
import deck_sim as ds                # noqa: E402  (simulate / need-source MC for --vitals)
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
SIM_TRIALS = 8000        # --vitals Monte Carlo (deck_sim defaults to 20k; this is a quick read)


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
    """oracle_text for the card AND every face (DFC/split), lower-cased. None-safe:
    parse_deck KEEPS unresolved cards in the library (typo / missing oracle data /
    broken reskin alias), so the footprint/interaction scans can hand this an
    unresolved card; treat it as no text rather than crashing the whole report."""
    if rec is None:
        return ""
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


# --- bracket / house-rule signals (REF_Bracket_3_House_Rules.md) -------------
# Mass land denial is a HARD house-rule exclusion. Curated from the ref's named
# list + close kin; backstopped by an oracle-text scan so an un-listed MLD card
# still trips. Ruinous Ultimatum is deliberately absent (doesn't hit lands).
MLD_CARDS = {
    "armageddon", "ravages of war", "jokulhaups", "obliterate", "devastating dreams",
    "catastrophe", "boom // bust", "wildfire", "decree of annihilation", "cataclysm",
    "global ruin", "sunder", "impending disaster", "fall of the thran", "death cloud",
    "bend or break", "keldon firebombers", "epicenter", "mana vortex", "tectonic break",
}

# Fast mana density is a bracket SIGNAL (not a gate). Curated rocks/rituals.
FAST_MANA = {
    "sol ring", "mana crypt", "mana vault", "grim monolith", "basalt monolith",
    "chrome mox", "mox diamond", "mox opal", "mox amber", "mox ruby", "mox sapphire",
    "mox emerald", "mox jet", "mox pearl", "jeweled lotus", "lotus petal",
    "lion's eye diamond", "black lotus", "dark ritual", "cabal ritual", "rite of flame",
    "pyretic ritual", "desperate ritual", "simian spirit guide", "elvish spirit guide",
    "jeska's will", "seething song", "mana geyser", "culling the weak",
}


def is_mld(name_lower, rec):
    if name_lower in MLD_CARDS:
        return True
    return "destroy all lands" in _all_text(rec) if rec else False


def is_extra_turn(rec):
    # "take/takes an extra turn" (Time Warp uses "takes"); "extra combat" cards
    # (Aggravated Assault) don't say "extra turn", so the bare substring is safe.
    return rec is not None and "extra turn" in _all_text(rec)


def _ramp_floor(rec):
    """Generic mana floor the otag 'ramp' tag misses (Arbor Elf untaps a land,
    Birds/Gilded Goose add any colour, signets/medallions are rocks/cost-cutters).
    Ramp is the commonest standalone floor, so the footprint scan leans on oracle
    text here rather than trusting the (incomplete) otag class alone."""
    if rec is None:
        return False
    t = _all_text(rec)
    return (re.search(r"add (\{|[\w]+ mana)", t) is not None            # produces mana
            or (("untap target" in t or "untap up to" in t)            # Arbor Elf-type
                and re.search(r"\b(land|forest|island|swamp|mountain|plains)s?\b", t))
            or re.search(r"spells? (you cast )?cost \{?\d", t) is not None)  # cost cut


def _power_at_least(rec, n):
    """True if the card (or any face) is a creature with printed power >= n — a
    crude 'standalone body' floor for the footprint scan. '*'/'X'/empty power
    counts as 0 (no guaranteed body), so a Tarmogoyf-type reads as no floor; the
    scan flags candidates for human judgment, it doesn't adjudicate."""
    if rec is None:
        return False
    for f in (rec.get("card_faces") or [rec]):
        p = f.get("power", rec.get("power"))
        try:
            if p is not None and int(p) >= n:
                return True
        except (TypeError, ValueError):
            continue
    return False


# --- fragility (permanent-type removal/wipe exposure) ------------------------
# The "500 decks" video's resilience ladder (REF_Multiplayer_Card_Eval.md): the
# permanent types, ordered easiest -> hardest to remove. A deck whose ENGINE sits
# on the easy tiers (planeswalkers, creatures) gets dismantled by a board wipe; an
# engine on artifacts/enchantments/lands keeps rolling. As Commander speeds up,
# board wipes are more common, so this exposure matters more (video lesson 2b).
FRAG_TIERS = ["planeswalker", "creature", "artifact", "enchantment", "battle",
              "nonbasic land", "basic land"]


def _all_types(rec):
    """type_line for the card AND every face (DFC/split/MDFC), lower-cased — so a
    'Creature // Land' MDFC is judged on both halves."""
    parts = [rec.get("type_line", "") or ""]
    for f in rec.get("card_faces", []) or []:
        parts.append(f.get("type_line", "") or "")
    return " ".join(parts).lower()


def fragility_rank(rec):
    """Removal exposure by permanent type: 0 = easiest to remove (planeswalker) …
    6 = hardest (basic land), per FRAG_TIERS. A card is as fragile as its MOST
    removable type — an artifact creature dies to creature removal AND board wipes
    AND artifact removal — so we take the MIN rank across all its types (a Vehicle
    that isn't a creature stays an artifact, dodging creature wipes: the Ratchet
    point). Non-permanents (instant/sorcery) return None: never on the battlefield
    to be removed. HEURISTIC — type-only; it can't see OUR pod's actual answer
    availability (that's delay_lab / interaction_meta)."""
    if rec is None:
        return None
    t = _all_types(rec)
    ranks = [i for i, kw in enumerate(
        ("planeswalker", "creature", "artifact", "enchantment", "battle")) if kw in t]
    if "land" in t:
        ranks.append(6 if "basic" in t else 5)
    return min(ranks) if ranks else None


# --- interaction coverage (Trinket Mage "decks that can always win", pillar 1) -
# A resilience scan the legality checks don't do: can the deck ANSWER a threat of
# each kind? Buckets mirror the video — the four permanent types you might need to
# remove (artifact / enchantment / creature / land) plus the two ways a threat
# dodges ordinary removal (indestructible, and hexproof/shroud/ward = "protection").
# HEURISTIC over oracle text + type line, exactly like keepable% is a land-count
# heuristic: it flags coverage HOLES, it does NOT adjudicate an interaction. The
# lens is B2-3 grind; a pure racer may leave holes on purpose (memory:
# reference_trinketmage_win_any_game — "not a brake on race decks").
INTERACTION_BUCKETS = ["artifact", "enchantment", "creature", "land",
                       "indestructible", "protection"]


def _has(t, pat):
    return re.search(pat, t) is not None


def interaction_caps(rec):
    """Set of answer-bucket tags a card provides, from oracle text. HEURISTIC —
    pattern-matched, deliberately generous; meant to catch 'zero ways to touch an
    enchantment', not to rule edge cases."""
    if rec is None:
        return set()
    t = _all_text(rec)
    caps = set()

    bounce  = _has(t, r"return (target|all|each)[^.]*to (its|their) owner")
    # exile that removes a PERMANENT (not graveyard hate like Bojuka Bog) — this is
    # what actually answers an indestructible threat.
    exile_p = _has(t, r"exile (target|all|each)[^.]*\b(permanent|creature|artifact|"
                      r"enchantment|land|planeswalker|nonland|nontoken|token)s?\b")
    mass    = _has(t, r"(destroy|exile) all") or _has(t, r"(destroy|exile) each")
    edict   = _has(t, r"(player|opponent)s?[^.]{0,40}sacrific")
    minus   = _has(t, r"-[0-9xX]+/-[0-9xX]+")
    shuffle = _has(t, r"shuffles? (it|target permanent)") and "target permanent" in t
    # a GENERIC counter ("counter target spell") stops any threat before it resolves;
    # a narrow one (counter target creature/noncreature/artifact… spell) does not.
    counterG = (_has(t, r"counter target spell")
                and not _has(t, r"counter target (creature|noncreature|artifact|"
                                r"instant|sorcery|multicolored|monocolored) spell"))

    # catch-all that hits every permanent type: destroy/exile a "… permanent",
    # bounce a "… permanent" (Cyclonic Rift), or Chaos Warp's shuffle. A
    # "nonland permanent" effect doesn't answer lands.
    if (_has(t, r"(destroy|exile) (target|all|each)[^.]*permanent")
            or _has(t, r"return (target|all|each)[^.]*permanent[^.]*to (its|their) owner")
            or shuffle):
        caps |= {"artifact", "enchantment", "creature"}
        if "nonland permanent" not in t:
            caps.add("land")

    # targeted/mass removal naming a specific type (handles "artifact or enchantment",
    # "artifact, creature, or land", "destroy all creatures", bounce-that-type)
    for typ in ("artifact", "enchantment", "creature", "land"):
        if (_has(t, rf"(destroy|exile)[^.]*\b{typ}s?\b")
                or _has(t, rf"return[^.]*\b{typ}s?\b[^.]*to (its|their) owner")):
            caps.add(typ)
    # creature kill modes that never say "destroy"
    if minus or _has(t, r"damage to (target|any target|each)") or _has(t, r"\bfights?\b") or edict:
        caps.add("creature")
    # a generic counter answers any of the permanent spell types on the stack
    if counterG:
        caps |= {"artifact", "enchantment", "creature"}

    # past indestructible: exile / bounce / sacrifice / -X/-X / shuffle / counter
    if exile_p or bounce or edict or minus or shuffle or counterG:
        caps.add("indestructible")
    # past hexproof/shroud/ward: anything that doesn't target the permanent —
    # a mass effect, an edict (targets the player), damage-to-each, or a counter
    if mass or edict or counterG or _has(t, r"damage to each"):
        caps.add("protection")
    return caps


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
        self.log = []               # (severity, message) — kept even in quiet mode
        self._section = ""          # current section title, tags the log entries

    def line(self, sev, msg):
        if sev == ERROR:
            self.errors += 1
        elif sev == WARN:
            self.warns += 1
        self.log.append((sev, self._section, msg))
        if not self.quiet:
            print(f"  [{sev:5}] {msg}")

    def note(self, msg):
        if not self.quiet:
            print(f"          {msg}")

    def section(self, title):
        self._section = title
        if not self.quiet:
            print(f"\n-- {title} --")

    def say(self, msg=""):
        if not self.quiet:
            print(msg)


def doctor(arg, run_lab=False, lab_override=None, trials=LAB_TRIALS,
           quiet=False, check_build=True, csv_path=None,
           vitals=False, combos=False, trials_sim=SIM_TRIALS, interaction=False,
           footprint=False, fragility=False):
    path, slug = resolve_target(arg)
    if path is None or not path.exists():
        if not quiet:
            print(f"deck_doctor: could not resolve a decklist from '{arg}'.")
            print("  Try a registry slug (radiation_sickness), a stem (the-grand-design),")
            print("  a candidate name (planned-obsolescence), or a path to a .txt.")
        return {"code": 2, "tag": "ERR", "errors": 1, "warns": 0, "facts": {},
                "log": [], "title": arg, "slug": None, "candidate": True}

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

    # --- 8. consistency vitals (opt-in: chains deck_sim's Monte Carlo) ---
    if vitals:
        rpt.section("consistency vitals (MC sim)")
        if not oracle:
            rpt.line(WARN, "skipped (no oracle data)")
        else:
            import random as _random
            rng = _random.Random(12345)            # fixed seed = reproducible
            identity = set()
            for _, r in library:
                identity.update(r.get("color_identity", ()))
            cmd_idx = index.get(commander.lower()) if commander else None
            if cmd_idx:
                identity.update(cmd_idx.get("color_identity", ()))
            stats = ds.simulate(library, sorted(identity), 10, trials_sim, rng)
            kp = stats["keepable_pct"]
            sev = OK if kp >= 75 else (WARN if kp >= 65 else ERROR)
            rpt.line(sev, f"keepable opening hand: {kp:.0f}%  "
                          f"({trials_sim} trials; land-count heuristic)")
            rpt.facts["keepable"] = round(kp)
            # BDD count-by-turn for the two load-bearing classes
            try:
                for klass, by in (("ramp", 3), ("draw", 6)):
                    srcs = ds.need_source_set(library, klass)
                    need = ds.simulate_need(library, srcs, 10, trials_sim, rng)
                    tgt, lbl = ds.rule_of_thumb(by)
                    ih = need["in_hand_by_turn"].get(by, 0.0)
                    verdict = "meets" if need["n_sources"] >= tgt else "below"
                    rpt.line(INFO, f"{klass}: {need['n_sources']} sources "
                                   f"(BDD ~{tgt} by T{by}: {verdict}) — "
                                   f"{ih:.0f}% in hand by T{by}")
            except Exception as e:                  # tagger is best-effort
                rpt.line(WARN, f"ramp/draw tagging unavailable: "
                               f"{type(e).__name__}: {str(e)[:80]}")
            # smoothness / flow: unlike keepable% (which never spends a card), this
            # SPENDS mana + draws, so it sees the gas problem the consistency pass
            # hides — dead turns + hellbent (paced 'one' spend, draw-aware).
            try:
                plan = ds.plan_card_set(slug)
                flow = ds.simulate_flow(library, 10, trials_sim, _random.Random(999),
                                        plan_set=plan, spend="one",
                                        draw_profiles=ds.draw_map(library))
                md = flow["mean_dead_turns"]
                hb = flow["hellbent_by_turn"][8]
                lead = "starved" if flow["starved_by_turn"][4] >= flow["flooded_by_turn"][8] else "flooded"
                # INFO-only (like fp%/frg%): a goldfish can't tell a race deck that
                # empties BECAUSE it's winning from a grind deck that runs out of gas,
                # so this surfaces the number without flipping the verdict.
                rpt.line(INFO, f"smoothness: {md:.2f} mean dead turns, {hb:.0f}% hellbent by T8 "
                               f"(paced, draw-aware; lead dead-cause: {lead})")
                rpt.note("lower=smoother; a proactive/grind deck wants low hellbent, "
                         "but a RACE deck emptying by T8 is fine (goldfish can't see the win)")
                rpt.facts["mean_dead"] = round(md, 2)
                rpt.facts["hellbent8"] = round(hb)
            except Exception as e:                  # flow/tagger is best-effort
                rpt.line(WARN, f"smoothness unavailable: {type(e).__name__}: {str(e)[:80]}")
            rpt.note("consistency, not power: keepable% informs HOW to build "
                     "(redundancy/bottleneck), it doesn't grade the deck")

    # --- 9. combo audit (opt-in: intended kill line + CSB) --------------
    combo_infinite = None        # None = not checked; bracket reads it if set
    if combos:
        rpt.section("combos (kill line + accidental infinites)")
        pool_lower = {n.lower() for n in pool}
        # (a) intended kill line — network-free, from the registry win_line
        wl = reg_row.get("win_line") if reg_row else None
        if wl and wl.get("pieces"):
            fuzzy = wl.get("fuzzy")
            missing = [p for p in wl["pieces"]
                       if not (p.lower() in pool_lower
                               or (fuzzy and any(p.lower() in n for n in pool_lower)))]
            if missing:
                rpt.line(WARN, f"intended kill line incomplete — missing: "
                               f"{', '.join(missing)}")
            else:
                rpt.line(OK, f"intended kill line present: {', '.join(wl['pieces'])}")
        elif reg_row:
            rpt.line(INFO, "no win_line on file for this deck — CSB scan only")
        # (b) Commander Spellbook combo DB (network)
        try:
            import find_combos as fc
            q = fc.query_deck(path)
            inc = q["included"]

            def _is_extra_turn_combo(c):
                return any("extra turn" in f.lower() for f in fc._features(c))
            et_combos = [c for c in inc if _is_extra_turn_combo(c)]
            inf_combos = [c for c in inc
                          if any("infinite" in f.lower() for f in fc._features(c))]
            combo_infinite = len(inf_combos)
            if et_combos:
                rpt.line(ERROR, f"{len(et_combos)} repeatable extra-turn combo(s) "
                                f"— house-rule banned (REF_Bracket_3_House_Rules)")
                for c in et_combos[:3]:
                    rpt.note(f"[{c['id']}] {', '.join(fc._features(c))}")
            rpt.line(OK if not inc else INFO,
                     f"{len(inc)} complete combo(s) in deck; "
                     f"{len(inf_combos)} infinite (pod-accepted since 2026-06-19)")
            near = [c for c in q["almost"]
                    if sum(1 for n in fc._uses(c) if n.lower() not in q["deck_lower"]) <= 1]
            if near:
                rpt.line(INFO, f"{len(near)} combo(s) one card away — "
                               f"`find_combos.py {slug or path.stem}` for the buy list")
        except Exception as e:
            rpt.line(WARN, f"Commander Spellbook unreachable — combo DB skipped "
                           f"({type(e).__name__})")

    # --- 9b. interaction coverage (opt-in: resilience checklist) --------
    # Can the deck ANSWER each kind of threat? (Trinket Mage "win any game",
    # pillar 1 — see the interaction_caps() header.) Always computed under --all
    # so the batch table can show a gaps column; printed only on demand.
    if interaction:
        rpt.section("interaction coverage (resilience)")
        if not oracle:
            rpt.line(WARN, "skipped (no oracle data)")
        else:
            cover = {b: [] for b in INTERACTION_BUCKETS}
            for nm in pool:
                rec = lookup(full, aliases, nm)
                for b in interaction_caps(rec):
                    cover[b].append(rec.get("name", nm) if rec else nm)
            gaps = [b for b in INTERACTION_BUCKETS if not cover[b]]
            rpt.facts["intxn_gaps"] = len(gaps)
            for b in INTERACTION_BUCKETS:
                names = sorted(set(cover[b]))
                n = len(names)
                if n == 0:
                    # INFO, not WARN: a coverage hole is an advisory resilience
                    # signal (a pure racer may leave it open on purpose), NOT a
                    # legality/correctness failure — it must not flip the verdict.
                    rpt.line(INFO, f"{b:13} 0 answers — no way to deal with a "
                                   f"threat of this kind")
                elif n <= 2:
                    rpt.line(INFO, f"{b:13} thin ({n}): {', '.join(names)}")
                else:
                    rpt.line(OK, f"{b:13} {n} answers "
                                 f"(e.g. {', '.join(names[:3])})")
            if gaps:
                rpt.note(f"holes: {', '.join(gaps)} — a flexible catch-all closes "
                         f"several at once (Chaos Warp = any permanent + "
                         f"indestructible; a board wipe = hexproof/shroud/ward; "
                         f"Perilous Vault = both)")
            rpt.note("heuristic over oracle text (flags holes, doesn't adjudicate); "
                     "B2-3 grind lens — a pure racer may skip some on purpose "
                     "(memory: reference_trinketmage_win_any_game)")

    # --- 9c. engine footprint (opt-in: hidden-commander rule 2) ---------
    # Cubrious "two rules for a hidden-commander deck" (memory:
    # reference_hidden_commander_footprint). RULE 2: a synergy card earns its
    # slot only if it does SOMETHING without the engine (ramp / draw / tutor /
    # removal, or a standalone body). This counts the nonland cards that go DEAD
    # if the engine (the win_line pieces) is removed or never drawn. HEURISTIC
    # over the tagger + oracle text, like 9b — flags build-quality candidates,
    # never adjudicates, and is INFO-only (a tight combo deck may accept a high
    # footprint on purpose). RULE 1 (analogs for the key card) = second-kill-path
    # redundancy, which --combos already measures (complete + one-away lines), so
    # it's pointed to rather than re-derived with a weak text heuristic.
    if footprint:
        rpt.section("engine footprint (hidden-commander rule 2)")
        wl = reg_row.get("win_line") if reg_row else None
        engine = [p.lower() for p in (wl.get("pieces") or [])] if wl else []
        fuzzy = bool(wl.get("fuzzy")) if wl else False
        if not engine:
            rpt.line(INFO, "no win_line/engine on file — footprint needs a "
                           "build-around to scope against (roster decks only)")
        elif not oracle:
            rpt.line(WARN, "skipped (no oracle data)")
        else:
            # tagger source sets are lowercased printed names (deck_sim DRY)
            floor = (ds.need_source_set(library, "ramp")
                     | ds.need_source_set(library, "draw")
                     | ds.need_source_set(library, "tutor")
                     | ds.need_source_set(library, "interaction"))

            def _is_engine(low):
                return any(p == low or (fuzzy and p in low) for p in engine)

            low_floor, nonland = [], 0
            for nm, _ in library:
                rec = lookup(full, aliases, nm)
                tl = rec.get("type_line", "") if rec else ""
                if "Land" in tl:
                    continue
                nonland += 1
                low = nm.lower()
                if _is_engine(low):
                    continue
                has_floor = (low in floor
                             or _ramp_floor(rec)
                             or bool(interaction_caps(rec))
                             or "search your library" in _all_text(rec)   # any tutor
                             or ("Creature" in tl and _power_at_least(rec, 2)))
                if not has_floor:
                    low_floor.append(rec.get("name", nm) if rec else nm)
            pct = 100 * len(low_floor) / max(nonland, 1)
            rpt.facts["footprint_pct"] = round(pct)
            # INFO only: footprint is a build-quality signal, NOT a legality
            # failure — it must never flip the PASS/WARN/FAIL verdict.
            rpt.line(INFO, f"{len(low_floor)}/{nonland} nonland cards ({pct:.0f}%) "
                           f"do little without the engine "
                           f"({', '.join(sorted(set(engine)))})")
            if low_floor:
                shown = ", ".join(sorted(low_floor)[:15])
                more = f" … +{len(low_floor) - 15}" if len(low_floor) > 15 else ""
                rpt.note(f"low-floor (only good with the engine): {shown}{more}")
            rpt.note("rule 1 (analogs / second kill path): see --combos "
                     "(complete + one-card-away lines)")
            rpt.note("Cubrious hidden-commander rules; B2-3 build-quality lens — "
                     "a tight combo deck may accept high footprint on purpose "
                     "(memory: reference_hidden_commander_footprint)")

    # --- 9d. fragility (opt-in: permanent-type removal/wipe exposure) ----
    # The "500 decks" video's resilience lesson 2b: rank your permanents on the
    # durability ladder (FRAG_TIERS). An engine on planeswalkers/creatures folds
    # to a board wipe; one on artifacts/enchantments/lands keeps rolling. Like 9b
    # and 9c this is HEURISTIC and INFO-only — type-only exposure, blind to OUR
    # pod's real answer availability (delay_lab / interaction_meta), so it flags a
    # build-shape signal and must NEVER flip the PASS/WARN/FAIL verdict. A pure
    # go-wide/aggro deck accepts a fragile base on purpose (it wins before the wipe).
    if fragility:
        rpt.section("fragility (permanent-type removal/wipe exposure)")
        if not oracle:
            rpt.line(WARN, "skipped (no oracle data)")
        else:
            tally = Counter()
            vulnerable, nonland_perm = [], 0
            for nm, _ in library:
                rec = lookup(full, aliases, nm)
                rk = fragility_rank(rec)
                if rk is None:                       # instant/sorcery — not a permanent
                    continue
                tally[rk] += 1
                if rk <= 4:                          # a nonland permanent
                    nonland_perm += 1
                    if rk <= 1:                      # planeswalker / creature = fragile
                        vulnerable.append(rec.get("name", nm) if rec else nm)
            pct = 100 * len(vulnerable) / max(nonland_perm, 1)
            rpt.facts["fragility_pct"] = round(pct)
            rpt.line(INFO, f"{len(vulnerable)}/{nonland_perm} nonland permanents "
                           f"({pct:.0f}%) sit on the most-removable types "
                           f"(planeswalker/creature)")
            rpt.note("ladder easiest→hardest: "
                     + " · ".join(f"{FRAG_TIERS[i]} {tally.get(i, 0)}"
                                  for i in range(len(FRAG_TIERS))))
            # the load-bearing line: is your WIN ENGINE on a fragile type?
            wl = reg_row.get("win_line") if reg_row else None
            frag_engine = []
            for p in ((wl.get("pieces") or []) if wl else []):
                rk = fragility_rank(lookup(full, aliases, p))
                if rk is not None and rk <= 1:
                    frag_engine.append(p)
            if frag_engine:
                rpt.note(f"engine pieces on fragile types: "
                         f"{', '.join(sorted(set(frag_engine)))} — protect them or "
                         f"lean on recursion/rebuild (lesson 2c)")
            crk = fragility_rank(lookup(full, aliases, commander)) if commander else None
            if crk is not None and crk <= 1:
                rpt.note(f"commander {commander} is a {FRAG_TIERS[crk]} (fragile type) "
                         f"but recurs from the command zone")
            rpt.note("type-only exposure (board wipes are creature-centric; lands are "
                     "~never removed in our pod); OUR actual answer availability lives "
                     "in delay_lab / interaction_meta")

    # --- 10. bracket estimate + house-rule gate -------------------------
    rpt.section("bracket / house rules")
    if not oracle:
        rpt.line(WARN, "skipped (no oracle data)")
    else:
        mld_hits, et_hits, fast_hits = [], [], []
        for nm in pool:
            rec = lookup(full, aliases, nm)
            if is_mld(nm.lower(), rec):
                mld_hits.append(rec.get("name", nm) if rec else nm)
            if is_extra_turn(rec):
                et_hits.append(rec.get("name", nm) if rec else nm)
            if nm.lower() in FAST_MANA or aliases.get(nm.lower(), nm).lower() in FAST_MANA:
                fast_hits.append(nm)
        rpt.facts.update(mld=len(mld_hits), extra_turns=len(et_hits),
                         fast_mana=len(fast_hits))
        # house-rule hard gate: mass land denial
        if mld_hits:
            rpt.line(ERROR, f"mass land denial — house-rule banned: "
                            f"{', '.join(sorted(set(mld_hits)))}")
        # extra-turn allowance is 0-1; a repeatable loop is the real red line
        if len(et_hits) > 1:
            rpt.line(WARN, f"{len(et_hits)} extra-turn effects "
                           f"({', '.join(sorted(set(et_hits)))}) — house rule allows 0-1, "
                           f"no chains; verify with --combos")
        elif et_hits:
            rpt.note(f"1 extra-turn effect ({et_hits[0]}) — within the 0-1 allowance")
        # estimated WotC bracket
        gc_n = rpt.facts.get("gc", 0)
        two_card_inf = (combo_infinite or 0) > 0
        if gc_n > MAX_GC or mld_hits or two_card_inf:
            brk, why = 4, []
            if gc_n > MAX_GC:
                why.append(f"{gc_n} GC")
            if mld_hits:
                why.append("MLD")
            if two_card_inf:
                why.append("infinite combo")
        elif gc_n >= 1:
            brk, why = 3, [f"{gc_n} GC"]
        else:
            brk, why = 2, ["0 GC, no combo/MLD signal"]
        inf_note = ("" if combo_infinite is not None
                    else "  (run --combos to detect 2-card infinites)")
        rpt.facts["bracket"] = brk
        rpt.line(INFO, f"estimated WotC bracket ~{brk} ({', '.join(why)}; "
                       f"fast-mana {len(fast_hits)}, extra-turns {len(et_hits)})"
                       f"{inf_note}")
        rpt.note("pod runs B3-by-GC / B4-in-spirit; infinites OK, "
                 "MLD + repeatable extra-turns house-banned")

    # --- 11. clock (cached medians + Summary drift) ---------------------
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
                rpt.facts["drift"] = sum(v == "DRIFT" for v in (vd, vt))
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
            "warns": rpt.warns, "facts": rpt.facts, "log": rpt.log,
            "title": title, "slug": slug, "candidate": candidate}


# ---------------------------------------------------------------------------
# --all batch dashboard
# ---------------------------------------------------------------------------

def _flag(facts, key):
    """Render a count cell for the batch table: '·' for 0/None (all-clear), else
    the number — so any digit in the sing/ill/off columns reads as a problem."""
    v = facts.get(key)
    return "·" if v in (None, 0) else str(v)


def batch(include_candidates=False, csv_path=None, vitals=False):
    """Run the quiet doctor over the whole active roster (+ optionally the
    considering/ candidates) and print one PASS/WARN/FAIL row per deck. Same
    checks as the single-deck report — just rendered as a table. With vitals=True
    (`--all --vitals`) the MC sim runs per deck, adding the smoothness columns."""
    targets = [(slug, None) for slug in reg.DECKS]
    if include_candidates:
        for p in sorted((ROOT / "decks" / "considering").glob("*.txt")):
            targets.append((None, p))

    print(f"=== Deck Doctor — batch ({len(targets)} decks"
          f"{', incl. candidates' if include_candidates else ''}"
          f"{', +vitals' if vitals else ''}) ===\n")
    vcols = f"{'dead':>5} {'hlb%':>5} " if vitals else ""
    hdr = (f"{'verdict':7} {'deck':28} {'size':>4} {'sing':>4} {'ill':>3} "
           f"{'off':>3} {'MLD':>3} {'GC':>3} {'brk':>3} {'gap':>3} {'fp%':>4} "
           f"{'frg%':>4} {vcols}{'owned':>7} {'buy €':>8}")
    print(hdr)
    print("-" * len(hdr))

    worst = 0
    rows = []
    for slug, path in targets:
        res = doctor(path if path else slug, quiet=True, csv_path=csv_path,
                     interaction=True, footprint=True, fragility=True, vitals=vitals)
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
        fp = (f"{f['footprint_pct']}%" if "footprint_pct" in f else "·")
        frg = (f"{f['fragility_pct']}%" if "fragility_pct" in f else "·")
        vcells = ""
        if vitals:
            dead = (f"{f['mean_dead']:.1f}" if "mean_dead" in f else "·")
            hlb = (f"{f['hellbent8']}%" if "hellbent8" in f else "·")
            vcells = f"{dead:>5} {hlb:>5} "
        print(f"{res['tag']:7} {res['title'][:28]:28} {size_cell:>4} "
              f"{_flag(f,'singleton'):>4} {_flag(f,'illegal'):>3} "
              f"{_flag(f,'offcolor'):>3} {_flag(f,'mld'):>3} "
              f"{str(f.get('gc','?')):>3} {str(f.get('bracket','?')):>3} "
              f"{_flag(f,'intxn_gaps'):>3} {fp:>4} {frg:>4} {vcells}{own:>7} {buy:>8}")

    n_fail = sum(1 for r in rows if r[0]["tag"] == "FAIL")
    n_warn = sum(1 for r in rows if r[0]["tag"] == "WARN")
    print(f"\n=== {len(rows)} decks: {n_fail} FAIL, {n_warn} WARN, "
          f"{len(rows) - n_fail - n_warn} PASS ===")
    print("  columns: size(!=100 prefixed !) · sing(leton) · ill(egal) · off(-colour) "
          "· MLD(house-banned) · GC · brk(et est) · gap(interaction-coverage holes, 0-6) "
          "· fp%(nonland cards dead without the engine) "
          "· frg%(nonland permanents on wipe-vulnerable planeswalker/creature types) "
          + ("· dead(mean dead turns T1-10) · hlb%(hellbent by T8; lower=smoother) "
             if vitals else "· (--all --vitals adds dead/hlb% smoothness columns) ")
          + "· owned/100 · buy € (indicative; + unpriced)")
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
    ap.add_argument("--vitals", action="store_true",
                    help="consistency vitals: keepable%% + ramp/draw count-by-turn (MC sim)")
    ap.add_argument("--combos", action="store_true",
                    help="combo audit: intended kill line + Commander Spellbook DB (network)")
    ap.add_argument("--interaction", action="store_true",
                    help="resilience: can the deck answer artifact/ench/creature/land "
                         "+ indestructible + protection? (heuristic over oracle text)")
    ap.add_argument("--footprint", action="store_true",
                    help="hidden-commander rule 2: %% of nonland cards that do little "
                         "without the engine (win_line); flags low-floor synergy slots")
    ap.add_argument("--fragility", action="store_true",
                    help="permanent-type removal/wipe exposure: %% of nonland permanents "
                         "on the most-removable types (planeswalker/creature) + which "
                         "engine pieces sit on a fragile type")
    ap.add_argument("--deep", action="store_true",
                    help="run every check including --vitals, --combos, "
                         "--interaction, --footprint and --fragility")
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
        return batch(include_candidates=args.candidates, csv_path=args.csv,
                     vitals=args.vitals or args.deep)
    if not args.deck:
        ap.error("a deck is required (or pass --all / --diff)")
    return doctor(args.deck, run_lab=args.run_lab, lab_override=args.lab,
                  trials=args.trials, check_build=not args.no_build,
                  csv_path=args.csv, vitals=args.vitals or args.deep,
                  combos=args.combos or args.deep,
                  interaction=args.interaction or args.deep,
                  footprint=args.footprint or args.deep,
                  fragility=args.fragility or args.deep)["code"]


if __name__ == "__main__":
    sys.exit(main())
