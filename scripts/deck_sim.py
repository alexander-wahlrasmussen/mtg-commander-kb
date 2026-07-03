#!/usr/bin/env python3
"""
deck_sim.py — Monte Carlo consistency + combo-assembly simulator for the roster.

This is NOT a rules engine. It does not play games of Magic. It answers the
narrow, statistical questions that depend only on *decklist composition*:

  - Keepable-opening-hand rate (London mulligan, simple land-count heuristic)
  - Lands in play and mana available by turn T
  - Colour-screw: probability of a source of every colour in the deck's
    identity being in play by turn T
  - "Has a play": probability of a castable nonland in hand by turn T
  - Combo-assembly: probability all pieces of a named combo are together in hand
    by turn T (optional generic-tutor substitution), IGNORING mana cost — a
    card-availability ceiling, not a kill-turn guarantee.
  - Flow/smoothness (--flow): a light tempo pass that SPENDS mana and empties the
    hand, so it can see dead turns (starved vs flooded), hand-size depletion and
    hellbent — the things the availability pass above structurally cannot.

Everything is derived from the .txt decklist + collection/oracle-cards.json
(cmc, type_line, color_identity). No card *text* is interpreted, so output is
exactly as trustworthy as those two inputs. Unresolved card names are reported
explicitly — never silently dropped.

Usage:
    python scripts/deck_sim.py                      # all decks, consistency table
    python scripts/deck_sim.py --deck calamity      # one deck (fuzzy filename match)
    python scripts/deck_sim.py --combos             # also run combo assembly (sim_profiles.json)
    python scripts/deck_sim.py --deck rad --need ramp --by 3   # BDD count heuristic, measured:
                                                    #   P(>=1 ramp in hand/castable by T3) vs the ~12-source anchor
    python scripts/deck_sim.py --deck rad --flow    # smoothness: live vs dead (starved/flooded) turns,
                                                    #   hand-size + hellbent trajectory (tempo model)
    python scripts/deck_sim.py --trials 50000       # trial count (default 20000)
    python scripts/deck_sim.py --json out.json      # machine-readable dump (feeds the matrix)

Data source: collection/oracle-cards.json (refresh via update_scryfall_data.py)
Combo profiles: scripts/sim_profiles.json
"""

import argparse
import json
import os
import random
import re
import sys
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).parent.parent
DECKS_DIR = ROOT / "decks"
ORACLE = ROOT / "collection" / "oracle-cards.json"
PROFILES = Path(__file__).parent / "sim_profiles.json"
ALIASES_DOC = ROOT / "reference" / "REF_Reskin_Aliases.md"

# Per-deck identity (commander, display name) comes from the single source of truth.
# Loaded by file path (the repo's cross-module idiom — no package on sys.path).
import importlib.util as _il
_rspec = _il.spec_from_file_location("deck_registry", Path(__file__).parent / "deck_registry.py")
deck_registry = _il.module_from_spec(_rspec)
_rspec.loader.exec_module(deck_registry)

# Commander per decklist (filename stem prefix -> commander card name). Needed
# because some exports list the commander inline in the 100-card main block; it
# belongs in the command zone, not the shuffled library. The active roster is the
# single source of truth (deck_registry); EXTRA_COMMANDERS adds the dismantled +
# candidate/considering builds deck_sim must also parse. Order is load-bearing —
# parse_deck() prefix-matches the FIRST key a stem startswith — and actives (emitted
# first) are never a prefix of an extra stem, so every prefix match is preserved.
COMMANDERS = {**deck_registry.active_commanders(), **deck_registry.EXTRA_COMMANDERS}

DISPLAY = {**deck_registry.active_display(), **deck_registry.EXTRA_DISPLAY}


# ---------------------------------------------------------------------------
# Card data
# ---------------------------------------------------------------------------

@lru_cache(maxsize=1)
def load_oracle_index():
    # Cached: parses the 176 MB Scryfall bulk into a read-only name->record index.
    # Callers never mutate the records, so sharing one copy across every deck in a
    # batch run (deck_doctor --all, pod_gauntlet) turns N reads into one.
    if not ORACLE.exists():
        sys.exit(f"ERROR: {ORACLE} not found — run scripts/update_scryfall_data.py first")
    print("Loading card data (large file, a few seconds)...", file=sys.stderr)
    with ORACLE.open(encoding="utf-8") as f:
        cards = json.load(f)

    index = {}
    for c in cards:
        faces = c.get("card_faces", [])
        face_types = [f.get("type_line", "") for f in faces] or [c.get("type_line", "")]
        record = {
            "cmc": c.get("cmc", 0.0),
            "type_line": c.get("type_line", ""),
            "face_types": face_types,
            "color_identity": tuple(c.get("color_identity", [])),
            "produced_mana": tuple(c.get("produced_mana", [])),
        }
        names = [c.get("name", "")]
        for fc in faces:
            if fc.get("name"):
                names.append(fc["name"])
        junk = c.get("layout", "normal") in {"art_series", "double_faced_token", "token"}
        for n in names:
            key = n.lower()
            if key and (key not in index or not junk):
                index[key] = record
    return index


def load_reskin_aliases():
    """Parse REF_Reskin_Aliases.md into {reskin_name_lower: original_name}.

    Covers the two-column 'Confirmed aliases' tables (Reskin | Original) and the
    three-column 'Other / mechanical analogues' table (Name | Analogue | Notes).
    CLAUDE.md hard rule: never declare a card unresolved without checking this
    file first.
    """
    if not ALIASES_DOC.exists():
        print(f"WARNING: {ALIASES_DOC} not found; reskins will not resolve", file=sys.stderr)
        return {}
    aliases = {}
    for line in ALIASES_DOC.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 2:
            continue
        reskin, original = cells[0], cells[1]
        # Skip header and separator rows.
        if not reskin or reskin.lower() in {"reskin name", "name"} or set(reskin) <= {"-", ":"}:
            continue
        aliases[reskin.lower()] = original
    return aliases


def is_land(record):
    """True if the card can ever be played as a land (incl. MDFC land backs)."""
    if "land" in record["type_line"].lower():
        return True
    return any("land" in ft.lower() for ft in record["face_types"])


def is_pure_land(record):
    """True only if every face is a land (always enters as a land, no choice)."""
    fts = [ft.lower() for ft in record["face_types"] if ft]
    if not fts:
        return "land" in record["type_line"].lower()
    return all("land" in ft for ft in fts)


# ---------------------------------------------------------------------------
# Decklist parsing
# ---------------------------------------------------------------------------

def parse_deck(path, index, aliases=None):
    """Return (library, commander_name, diagnostics).

    library is a list of (name, record) tuples — the 99 shuffled cards, with the
    commander pulled to the command zone and sideboard cards excluded.
    """
    aliases = aliases or {}
    stem = path.stem
    deck_key = next((k for k in COMMANDERS if stem.startswith(k)), None)
    commander = COMMANDERS.get(deck_key)

    main_entries = []
    in_sideboard = False
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.upper().startswith("SIDEBOARD"):
            in_sideboard = True
            continue
        if in_sideboard:
            continue
        parts = line.split(" ", 1)
        if len(parts) != 2 or not parts[0].isdigit():
            continue
        main_entries.append((int(parts[0]), parts[1].strip()))

    library = []
    unresolved = []
    aliased = []
    commander_found = False
    UNKNOWN = {"cmc": 99, "type_line": "UNKNOWN", "face_types": [], "color_identity": ()}
    for qty, name in main_entries:
        if commander and name.lower() == commander.lower():
            commander_found = True
            continue
        rec = index.get(name.lower())
        if rec is None and "/" in name and " // " not in name:
            # Split cards exported as "Expansion/Explosion" -> "Expansion // Explosion".
            rec = index.get(name.lower().replace("/", " // "))
        if rec is None:
            # CLAUDE.md hard rule: resolve UB reskins via the alias table before
            # declaring a card unresolved.
            original = aliases.get(name.lower())
            if original and index.get(original.lower()):
                rec = index[original.lower()]
                aliased.append(f"{name} -> {original}")
            else:
                unresolved.append(name if not original else f"{name} -> {original} (alias target missing)")
                rec = UNKNOWN
        for _ in range(qty):
            library.append((name, rec))

    diag = {
        "deck_key": deck_key,
        "library_size": len(library),
        "commander": commander,
        "commander_in_main": commander_found,
        "unresolved": unresolved,
        "aliased": aliased,
    }
    if PLAN_KEEP:                       # install this deck's plan-aware keep-spec (else default)
        install_keep_spec(deck_key)
    return library, commander, diag


# ---------------------------------------------------------------------------
# Monte Carlo
# ---------------------------------------------------------------------------

# Smart-keep experiment (2026-06-16): the default keep rule is land-count-ONLY, so the
# 2 mulligans never dig toward a FUNCTIONAL hand — it keeps the first 2-5-land hand even
# if it has no early play. DECK_SIM_SMART_KEEP=1 additionally requires an early action
# (>=1 nonland with cmc<=3), i.e. mulligan a "lands + only expensive cards" hand. Tests
# whether aggressive, plan-aware mulliganing rewards the consistency frameworks. Read at
# import so each lab subprocess (which imports deck_sim) honours the parent env.
SMART_KEEP = os.environ.get("DECK_SIM_SMART_KEEP") == "1"
SMART_KEEP_MAX_CMC = 3

# Plan-aware keep (Backlog #5, 2026-06-16). The generic SMART_KEEP above ("has a CMC<=3
# play") moved 0/16 medians because it is not "does this hand advance THIS DECK'S plan."
# DECK_SIM_PLAN_KEEP=1 makes parse_deck install the deck's keep-spec (analysis/keep_specs.json,
# generated by keep_spec.py from the verified WIN_LINE + tagger) and keep_hand mulligan toward
# the deck's BOTTLENECK: FINDING (keep a piece/tutor/2-selection) / MANA (keep ramp at ~3 lands)
# / BOARD (commander on curve + an early play). With NO spec installed the behaviour is exactly
# the land-count [+SMART_KEEP] rule — so the default harvest is unchanged. Env read at import so
# each lab subprocess honours the parent (same pattern as SMART_KEEP / the --refresh re-harvest).
PLAN_KEEP = os.environ.get("DECK_SIM_PLAN_KEEP") == "1"
KEEP_SPECS_PATH = ROOT / "analysis" / "keep_specs.json"
EARLY_PLAY_MAX_CMC = 3
_KEEP_SPECS = None          # lazy dict[deck_key -> spec]
_KEEP_SPEC = None           # the spec currently installed (None = land-count default)


def _load_keep_specs():
    global _KEEP_SPECS
    if _KEEP_SPECS is None:
        _KEEP_SPECS = (json.loads(KEEP_SPECS_PATH.read_text(encoding="utf-8"))
                       if KEEP_SPECS_PATH.exists() else {})
    return _KEEP_SPECS


def set_keep_spec(spec):
    """Install (or clear, with None) the keep-spec keep_hand consults. Precomputes the
    bucket sets once so the hot keep loop only does membership tests."""
    global _KEEP_SPEC
    if spec is not None and "_sets" not in spec:
        spec = dict(spec)
        spec["_sets"] = {b: set(spec[b]) for b in ("key_cards", "tutors", "ramp", "selection")}
    _KEEP_SPEC = spec


def install_keep_spec(deck_key):
    """Install the spec for deck_key (clear if none). Called by parse_deck when PLAN_KEEP."""
    set_keep_spec(_load_keep_specs().get(deck_key) if deck_key else None)
    return _KEEP_SPEC


def _axis_ok(axis, hand, lands, spec, names, has_ramp):
    """Does the hand satisfy ONE bottleneck axis (FINDING / MANA / BOARD)?"""
    sets = spec["_sets"]
    if axis == "FINDING":
        if names & sets["key_cards"] or names & sets["tutors"]:
            return True
        return len(names & sets["selection"]) >= spec["n_selection_needed"]
    if axis == "MANA":                  # acceleration, not a land flood
        return has_ramp or (spec["hi_curve"] and lands >= 4)
    # BOARD: deploy the commander ~on curve + have an early play
    cmdr_reach = lands >= spec["cmdr_cmc"] - 2 or has_ramp
    early = any((not is_land(rec)) and rec["cmc"] <= EARLY_PLAY_MAX_CMC for _, rec in hand)
    return cmdr_reach and early


def _plan_progress(hand, lands, spec):
    """Does this (land-band-passing) hand advance the deck's plan? Union over the primary
    bottleneck + any secondary axes in spec['also'] (two-line decks): a hand strong on
    EITHER line keeps, so we don't ship a board hand to chase a side combo (the Radiation
    -9 lesson). 'also' absent/empty -> single-axis, identical to before."""
    names = {nm.lower() for nm, _ in hand}
    has_ramp = bool(names & spec["_sets"]["ramp"])
    for axis in (spec["bottleneck"], *spec.get("also", [])):
        if _axis_ok(axis, hand, lands, spec, names, has_ramp):
            return True
    return False


def keep_hand(hand):
    """Keepable? Plan-aware when a keep-spec is installed (set_keep_spec); otherwise the
    land-count rule (+ SMART_KEEP early-play). Default path is unchanged."""
    lands = sum(1 for _, rec in hand if is_land(rec))
    spec = _KEEP_SPEC
    if spec is not None:
        return spec["min_lands"] <= lands <= spec["max_lands"] and _plan_progress(hand, lands, spec)
    if not (2 <= lands <= 5):
        return False
    if SMART_KEEP and not any((not is_land(rec)) and rec["cmc"] <= SMART_KEEP_MAX_CMC
                              for _, rec in hand):
        return False
    return True


# London mulligan experiment (2026-07-03, Mulligan_Strategy_Audit §8.1). The default
# mulligan is FREE (fresh 7, max 2, keeps a failing 3rd hand) — it can neither price
# digging nor express real aggression (mull-to-5). DECK_SIM_LONDON_MULLS=N (>0) switches
# opening_hand to London rules: up to N mulligans, each a fresh 7; the final keep BOTTOMS
# one card per mulligan taken, so digging costs real cards. Bottomed cards stay in
# deck[0:7], which every consumer skips (ptr starts at 7) — bottomed == never drawn,
# exact for our <=14-turn goldfish horizons (the true bottom of a 92-card library is out
# of reach anyway). Env read at import so lab subprocesses inherit it (PLAN_KEEP pattern);
# with the env unset the default path is byte-identical, golden untouched.
LONDON_MULLS = int(os.environ.get("DECK_SIM_LONDON_MULLS", "0") or 0)
LONDON_LAND_KEEP = 3        # bottoming never touches the first 3 lands


def _bottom_hand(hand, n):
    """Drop n cards from a kept London hand. Bottoming priority: excess lands (4th+),
    then the most expensive NON-plan nonland, then the most expensive plan card. Plan
    cards = the installed keep-spec's buckets; with no spec every nonland ranks equally
    (most expensive goes first). The first LONDON_LAND_KEEP lands are protected so a
    kept hand can still operate."""
    if n <= 0:
        return hand
    spec = _KEEP_SPEC
    plan = set()
    if spec is not None:
        for b in ("key_cards", "tutors", "ramp", "selection"):
            plan |= spec["_sets"][b]
    scored = []
    lands_seen = 0
    for i, (nm, rec) in enumerate(hand):
        if is_land(rec):
            lands_seen += 1
            score = -1.0 if lands_seen <= LONDON_LAND_KEEP else 50.0 + lands_seen
        else:
            in_plan = (nm.lower() in plan) if spec is not None else True
            score = rec["cmc"] + (0.0 if in_plan else 20.0)
        scored.append((score, i))
    drop = {i for _, i in sorted(scored, key=lambda s: (-s[0], s[1]))[:n]}
    return [c for i, c in enumerate(hand) if i not in drop]


def opening_hand(deck, rng):
    """Shuffle, draw 7, mulligan up to twice on an unkeepable hand — FREE (fresh 7, no
    card penalty; the documented default). With DECK_SIM_LONDON_MULLS=N: London variant —
    up to N mulligans, and the final keep bottoms one card per mulligan taken
    (_bottom_hand), so the hand is 7−m cards. Both paths consume one rng.shuffle per
    mulligan, so a fixed seed pairs the arms."""
    rng.shuffle(deck)
    hand = deck[:7]
    mulls = 0
    max_mulls = LONDON_MULLS or 2
    while not keep_hand(hand) and mulls < max_mulls:
        rng.shuffle(deck)
        hand = deck[:7]
        mulls += 1
    kept = keep_hand(hand)
    if LONDON_MULLS:
        return _bottom_hand(list(hand), mulls), kept
    return list(hand), kept


# ---------------------------------------------------------------------------
# Land colour model (fixed 2026-06-09)
#
# A land's colour contribution was previously its Scryfall color_identity —
# which is EMPTY for sac-fetches (Polluted Delta) and rainbow lands (Command
# Tower, City of Brass, Exotic Orchard, Reflecting Pool). That scored a deck's
# best fixers as zero-colour sources and produced artificially low colour
# floors (Grand Design read 39% when its real floor is far higher). Fix:
#   - use produced_mana (structured Scryfall field, not text parsing) when
#     present, restricted to WUBRG;
#   - resolve sac-fetches to the union of colours of the deck's OWN lands of
#     the fetchable types (basic-only fetchers see basics only).
# Remaining (documented) optimism: enters-tapped, Exotic Orchard/Reflecting
# Pool board-dependence, and fetch-target depletion are ignored — still a
# floor on castability, but no longer a broken one.
# ---------------------------------------------------------------------------
WUBRG = set("WUBRG")
BASIC_TYPES = ("plains", "island", "swamp", "mountain", "forest")

# Sac-fetch -> basic land types it can fetch (nonbasics with the type count).
FETCH_TYPED = {
    "flooded strand": ("plains", "island"),
    "polluted delta": ("island", "swamp"),
    "bloodstained mire": ("swamp", "mountain"),
    "wooded foothills": ("mountain", "forest"),
    "windswept heath": ("forest", "plains"),
    "marsh flats": ("plains", "swamp"),
    "scalding tarn": ("island", "mountain"),
    "verdant catacombs": ("swamp", "forest"),
    "arid mesa": ("mountain", "plains"),
    "misty rainforest": ("forest", "island"),
    "krosan verge": ("forest", "plains"),
}
# Fetchers restricted to BASIC lands (Evolving Wilds class).
FETCH_BASIC = {"prismatic vista", "evolving wilds", "terramorphic expanse",
               "fabled passage", "myriad landscape"}


def printed_land_colors(record):
    """Colours a land itself produces: produced_mana when known, else identity."""
    prod = set(record["produced_mana"]) & WUBRG
    return prod if prod else set(record["color_identity"])


def land_color_map(library):
    """name(lower) -> effective colour set for each land in this library,
    resolving sac-fetches against the deck's own typed/basic lands."""
    typed = {bt: set() for bt in BASIC_TYPES}
    basics = set()
    for nm, r in library:
        if not is_land(r):
            continue
        cols = printed_land_colors(r)
        tl = r["type_line"].lower()
        for bt in BASIC_TYPES:
            if bt in tl:
                typed[bt].update(cols)
        if "basic" in tl:
            basics.update(cols)
    cmap = {}
    for nm, r in library:
        if not is_land(r):
            continue
        key = nm.lower()
        if key in FETCH_TYPED:
            cmap[key] = set().union(*(typed[bt] for bt in FETCH_TYPED[key]))
        elif key in FETCH_BASIC:
            cmap[key] = set(basics)
        else:
            cmap[key] = printed_land_colors(r)
    return cmap


def simulate(library, identity, turns, trials, rng):
    n = len(library)
    keepable = 0
    lands_play = [0.0] * (turns + 1)
    all_colors = [0] * (turns + 1)
    castable = [0] * (turns + 1)
    colors = list(identity)
    cmap = land_color_map(library)

    for _ in range(trials):
        deck = library[:]
        hand, kept = opening_hand(deck, rng)
        keepable += 1 if kept else 0
        ptr = 7
        in_play = []
        for t in range(1, turns + 1):
            if t > 1 and ptr < n:
                hand.append(deck[ptr])
                ptr += 1
            # Play a land, preferring pure lands so flex lands stay castable.
            li = next((i for i, (_, r) in enumerate(hand) if is_pure_land(r)), None)
            if li is None:
                li = next((i for i, (_, r) in enumerate(hand) if is_land(r)), None)
            if li is not None:
                in_play.append(hand.pop(li))

            lands_play[t] += len(in_play)
            if colors:
                avail = set()
                for nm, r in in_play:
                    avail.update(cmap.get(nm.lower(), r["color_identity"]))
                if all(c in avail for c in colors):
                    all_colors[t] += 1
            mana = len(in_play)
            if any((not is_land(r)) and r["cmc"] <= mana for _, r in hand):
                castable[t] += 1

    return {
        "keepable_pct": 100.0 * keepable / trials,
        "lands_by_turn": {t: lands_play[t] / trials for t in range(1, turns + 1)},
        "all_colors_by_turn": {t: 100.0 * all_colors[t] / trials for t in range(1, turns + 1)},
        "castable_by_turn": {t: 100.0 * castable[t] / trials for t in range(1, turns + 1)},
    }


# ---------------------------------------------------------------------------
# Flow / "smoothness" model (2026-07-03)
#
# simulate() asks only "does a castable card EXIST" — it never spends mana or
# removes a card from hand, so it cannot see a hand empty out or a turn pass with
# nothing to do. simulate_flow() adds a light TEMPO layer on the SAME draw + land
# model (it does not touch simulate(), so every golden consistency figure is
# unchanged): each turn, after the land drop, it greedily casts castable nonlands
# cheapest-first, spends the lands-only mana floor, and REMOVES them from hand.
# That makes three things observable the consistency pass can't:
#   - hand-size trajectory + hellbent rate — running out of gas / forced topdeck.
#   - dead turns split by CAUSE (the two feel-bads the user named):
#       * starved — a nonland is stuck in hand, no mana to cast it (mana screw).
#       * flooded — no nonland to cast at all (drew lands / ran dry).
#   - "live" turns split naive (cast ANY nonland) vs plan (cast a card the deck's
#     keep-spec tags as part of its win line). naive-high + plan-low = a deck that
#     always has *a* card to play but rarely advances its actual plan (durdle).
#
# CAVEATS — the same land-only floor as simulate(), plus two more; read the output
# as a RELATIVE smoothness rank across decks, never an absolute play pattern:
#   - mana = LANDS ONLY (rocks/dorks/rituals excluded) -> `starved` is an UPPER
#     bound and `live` a LOWER bound for ramp decks. A ramp-aware version belongs
#     on the Goldfish harness (speed_lab_core), which deploys rocks per deck.
#   - "deploy everything" greedy spend is a WORST CASE for hand-emptying: it never
#     holds a card for value or instant speed, so hellbent% is an upper bound.
#     Decks with real draw refill even under max deployment; decks without don't --
#     which is exactly the discriminator we want.
#   - GOLDFISH: no opponents, so it cannot credit reactive turns (holding up a
#     counter reads as dead). Trustworthy for PROACTIVE / development smoothness.
# ---------------------------------------------------------------------------

def plan_card_set(deck_key):
    """Union (lowercased) of the deck's keep-spec plan tags — key_cards | tutors |
    ramp | selection, i.e. the cards that ADVANCE this deck's win line. None when
    the deck has no keep-spec, in which case simulate_flow treats every nonland as
    plan-relevant (plan-live == naive-live)."""
    spec = _load_keep_specs().get(deck_key) if deck_key else None
    if not spec:
        return None
    names = set()
    for bucket in ("key_cards", "tutors", "ramp", "selection"):
        names.update(x.lower() for x in spec.get(bucket, []))
    return names


_DRAW_WORDS = {"a": 1, "an": 1, "one": 1, "two": 2, "three": 3, "four": 4,
               "five": 5, "six": 6, "seven": 7}

# A draw PAYOFF ("whenever you draw a card, <do something>") has "draw" in the
# TRIGGER CONDITION and yields no cards — Sheoldred, Psychosis Crawler. Strip these
# condition clauses before hunting for a real draw EFFECT so payoffs aren't miscounted
# as sources. Replacement effects ("if you would draw ...") go too. The subject must
# be a player and be followed by "draw(s)" — "whenever a player CASTS ... you draw a
# card" (Niv-Mizzet) is NOT matched, so its genuine draw effect survives.
_DRAW_PAYOFF_RE = re.compile(
    r"(whenever|if|when|each time) "
    r"(you|an opponent|a player|another player|that player|players)"
    r"( would)? draws?\b[^.,]*")
_RECURRING = ("at the beginning", "whenever", "each turn", "end step", "upkeep", "draw step")


def _draw_profile(text, type_line):
    """(gross_oneshot_draw, repeatable_engine) for a draw-tagged card. text and
    type_line lowercased. Floor heuristics (card advantage a proxy can defend):
      - (0, False) — the card has NO real draw effect (its only "draw" was a payoff
        trigger condition, stripped above). Contributes nothing.
      - (0, True) — repeatable permanent draw ENGINE: a genuine draw effect under a
        recurring trigger (upkeep / whenever / end step). Worth +1 card per later
        turn in play, not a burst on cast.
      - (gross, False) — one-shot. A cantrip (1, False) NETS zero (drew 1, spent the
        card) instead of the -1 the naive spend charged; 'draw two cards' is (2,
        False) = net +1. Look-then-put selection (Brainstorm/Ponder, "... on top")
        caps to (1, False) so card *selection* isn't miscredited as card *advantage*.

    Known residual over-credit (documented floor): a mana/discard LOOT engine
    (Glint-Horn, connive) reads as a repeatable engine though it only filters."""
    is_perm = any(k in type_line for k in
                  ("creature", "artifact", "enchantment", "planeswalker", "battle"))
    effect = _DRAW_PAYOFF_RE.sub(" ", text)   # keep only genuine draw EFFECTS
    if not re.search(r"\bdraw \w[^.,]*cards?", effect) and "that many cards" not in effect:
        return (0, False)
    if is_perm and any(k in effect for k in _RECURRING):
        return (0, True)
    m = re.search(r"draw (a|an|one|two|three|four|five|six|seven|\d+) cards?", effect)
    k = 1
    if m:
        w = m.group(1)
        k = _DRAW_WORDS.get(w, int(w) if w.isdigit() else 1)
    # Selection/rummage nets ~0 card advantage, not k: 'put ... on top' (Brainstorm)
    # or a paired discard (Faithless Looting, Frantic Search). Night's Whisper (draw
    # two, lose life — no discard) correctly stays +1.
    if k > 1 and ("on top" in text or "on the bottom" in text or "discard" in text):
        k = 1
    return (k, False)


def draw_map(library):
    """name(lower) -> (gross_oneshot_draw, repeatable_engine) for every draw-tagged
    card in the library. Detection uses the VERIFIED framework_bakeoff 'draw' tagger
    (so opponent/symmetric 'draws' and non-draw cards are excluded); only the AMOUNT
    and engine flag come from oracle text. simulate_flow uses this to REFILL the
    hand, so momentum decks aren't punished for casting their card advantage — the
    fix for the v1 flow model reading Ms. Bumbleflower (drawiest deck) as least
    smooth. Reskins resolve via the bake-off alias table."""
    idx, aliases = _fb_data()
    fb = _load_fb()
    out = {}
    for nm in {n.lower() for n, _ in library}:
        card = idx.get(nm) or idx.get(aliases.get(nm, nm))
        if not card or fb.is_land(card) or "draw" not in fb.tag_card(card):
            continue
        out[nm] = _draw_profile(fb.card_text(card), (card.get("type_line") or "").lower())
    return out


def simulate_flow(library, turns, trials, rng, plan_set=None, spend="greedy",
                  draw_profiles=None):
    """Tempo/smoothness pass over the lands-only mana floor, tracking per turn
    whether a (plan-)play happened, why a turn went dead, and the hand-size /
    hellbent trajectory. Consumes rng identically to simulate() (opening_hand
    only), so it is deterministic at a fixed seed.

    spend policy brackets the truth for hand-emptying:
      "greedy" — cast EVERY affordable nonland cheapest-first (max deployment).
                 An UPPER bound on emptying; hellbent% saturates the mid-pack.
      "one"    — cast a single marquee play/turn (the most expensive affordable
                 nonland), holding the rest. A LOWER bound on emptying; spreads
                 hellbent, so it discriminates paced decks. Real play sits between.

    draw_profiles (name.lower() -> (gross_oneshot_draw, repeatable_engine), from
    draw_map()) makes card draw REAL: casting a one-shot draw refills the hand by
    its gross count (a cantrip nets 0 instead of -1); a repeatable engine adds +1
    card per later turn while in play. None/{} = no draw execution (the pre-draw
    behaviour), so callers/tests without profiles are unchanged.
    """
    n = len(library)
    draws = draw_profiles or {}
    live = [0] * (turns + 1)        # cast >=1 nonland this turn
    plan_live = [0] * (turns + 1)   # cast >=1 plan-tagged nonland
    starved = [0] * (turns + 1)     # dead turn: a nonland stuck in hand, mana too low
    flooded = [0] * (turns + 1)     # dead turn: no nonland to cast (lands / empty)
    hand_sz = [0.0] * (turns + 1)
    hellbent = [0] * (turns + 1)    # hand <= 1 card at end of turn
    dead_total = 0                  # sum of dead turns (T1..turns) across all trials

    for _ in range(trials):
        deck = library[:]
        hand, _ = opening_hand(deck, rng)
        ptr = 7
        in_play = []
        engines = 0             # repeatable draw engines in play (each = +1 card/turn)
        for t in range(1, turns + 1):
            # Draw step: natural draw (not on T1, on the play) + one per engine online.
            for _ in range((1 if t > 1 else 0) + engines):
                if ptr < n:
                    hand.append(deck[ptr])
                    ptr += 1
            # Land drop, preferring pure lands so flex lands stay spendable.
            li = next((i for i, (_, r) in enumerate(hand) if is_pure_land(r)), None)
            if li is None:
                li = next((i for i, (_, r) in enumerate(hand) if is_land(r)), None)
            if li is not None:
                in_play.append(hand.pop(li))
            budget = len(in_play)   # lands-only mana floor

            # Spend the mana. "greedy" dumps every affordable nonland cheapest-first;
            # "one" makes a single marquee play (most expensive affordable) and holds
            # the rest. cheaper=greedy picks smallest cmc, else "one" picks largest.
            cast_any = cast_plan = False
            while True:
                best = None
                for i, (_, r) in enumerate(hand):
                    if is_land(r) or r["cmc"] > budget:
                        continue
                    if best is None or (r["cmc"] < hand[best][1]["cmc"] if spend == "greedy"
                                        else r["cmc"] > hand[best][1]["cmc"]):
                        best = i
                if best is None:
                    break
                nm, r = hand.pop(best)
                budget -= r["cmc"]
                cast_any = True
                if plan_set is None or nm.lower() in plan_set:
                    cast_plan = True
                prof = draws.get(nm.lower())
                if prof:
                    gross, repeatable = prof
                    if repeatable:
                        engines += 1        # refuels on future turns, not now
                    else:
                        for _ in range(gross):   # refill hand — cantrip nets 0, not -1
                            if ptr < n:
                                hand.append(deck[ptr])
                                ptr += 1
                if spend == "one":      # one marquee play per turn, hold the rest
                    break

            if cast_any:
                live[t] += 1
                if cast_plan:
                    plan_live[t] += 1
            else:
                dead_total += 1
                if any(not is_land(r) for _, r in hand):
                    starved[t] += 1     # a spell is stuck — mana too low
                else:
                    flooded[t] += 1     # nothing to cast — lands or empty hand
            hand_sz[t] += len(hand)
            if len(hand) <= 1:
                hellbent[t] += 1

    pct = lambda arr: {t: 100.0 * arr[t] / trials for t in range(1, turns + 1)}
    return {
        "live_by_turn": pct(live),
        "plan_live_by_turn": pct(plan_live),
        "starved_by_turn": pct(starved),
        "flooded_by_turn": pct(flooded),
        "hand_size_by_turn": {t: hand_sz[t] / trials for t in range(1, turns + 1)},
        "hellbent_by_turn": pct(hellbent),
        "mean_dead_turns": dead_total / trials,
        "has_plan_spec": plan_set is not None,
    }


def simulate_combos(library, profile, turns, trials, rng):
    """P(all pieces of a combo together in hand by turn T), ignoring mana.

    Generic tutors (profile['tutors']) are modelled as wildcards: each tutor in
    hand can stand in for one not-yet-drawn piece. This is optimistic — real
    tutors have colour/type limits and cost mana — so treat it as a card-flow
    ceiling, read alongside the mana curve from the consistency pass.
    """
    n = len(library)
    tutors = {t.lower() for t in profile.get("tutors", [])}
    results = {}

    for combo in profile.get("combos", []):
        pieces = {p.lower() for p in combo["pieces"]}
        drawn_only = [0] * (turns + 1)
        with_tutor = [0] * (turns + 1)

        for _ in range(trials):
            deck = library[:]
            hand, _ = opening_hand(deck, rng)
            ptr = 7
            seen_pieces = {nm.lower() for nm, _ in hand} & pieces
            tutors_seen = sum(1 for nm, _ in hand if nm.lower() in tutors)
            for t in range(1, turns + 1):
                if t > 1 and ptr < n:
                    nm = deck[ptr][0].lower()
                    ptr += 1
                    if nm in pieces:
                        seen_pieces.add(nm)
                    if nm in tutors:
                        tutors_seen += 1
                missing = len(pieces) - len(seen_pieces)
                if missing == 0:
                    drawn_only[t] += 1
                    with_tutor[t] += 1
                elif tutors_seen >= missing:
                    with_tutor[t] += 1

        results[combo["name"]] = {
            "pieces": combo["pieces"],
            "drawn_by_turn": {t: 100.0 * drawn_only[t] / trials for t in range(1, turns + 1)},
            "with_tutor_by_turn": {t: 100.0 * with_tutor[t] / trials for t in range(1, turns + 1)},
        }
    return results


# ---------------------------------------------------------------------------
# "Need N sources" query (--need): the BDD count-by-turn heuristic, measured.
#
# The rule of thumb (Based Deck Department, "How I'd Build Commander Decks If I
# Started Today"): to reliably see an effect by the opening/first few turns run
# ~12 sources; by ~T6 ~8; by ~T10 ~5-6. This query replaces the back-of-envelope
# with the real MC: P(>=1 source of a tagged class in hand by turn T). It reports
# IN-HAND and CASTABLE separately on purpose — a naive hypergeometric (and the
# bare rule of thumb) counts cards you can't cast yet, which is exactly how the
# video's V1 over-counted its early game. Castable conditions the source's own
# cmc on lands in play (same land-base-only floor as "has a play").
#
# Sources are tagged live via framework_bakeoff's verified function tagger, so
# this works on any parsed .txt — including a proposal deck not in the roster.
# ---------------------------------------------------------------------------
_FB = None


def _load_fb():
    """Lazy-load framework_bakeoff (the verified tagger + its oracle loader). Only
    pulled in for --need, so the default table path doesn't double-load oracle."""
    global _FB
    if _FB is None:
        _spec = _il.spec_from_file_location(
            "framework_bakeoff", Path(__file__).parent / "framework_bakeoff.py")
        _FB = _il.module_from_spec(_spec)
        _spec.loader.exec_module(_FB)
    return _FB


_FB_IDX = None
_FB_ALIASES = None


def _fb_data():
    """Memoised (fb oracle index, alias map). fb.load_oracle re-parses the 176 MB
    bulk on every call — caching it here lets draw_map() run per-deck across a whole
    batch (deck_doctor --all) without re-reading the file 17 times."""
    global _FB_IDX, _FB_ALIASES
    if _FB_IDX is None:
        fb = _load_fb()
        _FB_IDX = fb.load_oracle()
        _FB_ALIASES = fb.load_aliases()
    return _FB_IDX, _FB_ALIASES


def need_source_set(library, klass):
    """Set of printed-name(lower) in this library that the tagger marks as `klass`
    (ramp|draw|tutor|interaction|protection). Resolves reskins via the bake-off's
    alias table before tagging, so UB prints are not silently missed."""
    fb = _load_fb()
    fb_idx, fb_aliases = _fb_data()     # cached: no per-deck 176 MB re-read in a batch
    sources = set()
    for nm in {n.lower() for n, _ in library}:
        card = fb_idx.get(nm) or fb_idx.get(fb_aliases.get(nm, nm).lower())
        if card and klass in fb.tag_card(card):
            sources.add(nm)
    return sources


def simulate_need(library, source_names, turns, trials, rng):
    """P(>=1 source in hand) and P(>=1 *castable* source in hand) by turn T.
    Uses the same draw + land-play model as simulate(); castable = a source whose
    cmc <= lands in play (land-base only, a floor — rocks/dorks not counted)."""
    n = len(library)
    src = {s.lower() for s in source_names}
    in_hand = [0] * (turns + 1)
    castable = [0] * (turns + 1)
    for _ in range(trials):
        deck = library[:]
        hand, _ = opening_hand(deck, rng)
        ptr = 7
        in_play = []
        for t in range(1, turns + 1):
            if t > 1 and ptr < n:
                hand.append(deck[ptr])
                ptr += 1
            li = next((i for i, (_, r) in enumerate(hand) if is_pure_land(r)), None)
            if li is None:
                li = next((i for i, (_, r) in enumerate(hand) if is_land(r)), None)
            if li is not None:
                in_play.append(hand.pop(li))
            mana = len(in_play)
            srcs = [r for nm, r in hand if nm.lower() in src]
            if srcs:
                in_hand[t] += 1
                if any(r["cmc"] <= mana for r in srcs):
                    castable[t] += 1
    return {
        "n_sources": len(src),
        "in_hand_by_turn": {t: 100.0 * in_hand[t] / trials for t in range(1, turns + 1)},
        "castable_by_turn": {t: 100.0 * castable[t] / trials for t in range(1, turns + 1)},
    }


def rule_of_thumb(turn):
    """BDD's count anchor nearest to `turn`: (target_sources, label)."""
    if turn <= 3:
        return 12, "opening / first few turns"
    if turn <= 7:
        return 8, "~turn 6"
    return 6, "~turn 10"


def print_need_report(name, klass, need, turns, by):
    show = [t for t in (2, 3, 4, 5, 6, 8, 10) if t <= turns]
    print(f"\n  --need {klass}: {need['n_sources']} source(s) tagged in deck")
    if need["n_sources"] == 0:
        print(f"    (no card tagged '{klass}' — nothing to measure)")
        return
    print("  turn:           " + "".join(f"{t:>6}" for t in show))
    print("  in hand:        " + "".join(fmt_pct(need['in_hand_by_turn'][t]) for t in show))
    print("  castable:       " + "".join(fmt_pct(need['castable_by_turn'][t]) for t in show))
    if by:
        tgt, lbl = rule_of_thumb(by)
        ih = need["in_hand_by_turn"].get(by, 0.0)
        ca = need["castable_by_turn"].get(by, 0.0)
        verdict = "meets" if need["n_sources"] >= tgt else "below"
        print(f"    by T{by}: {ih:.0f}% in hand / {ca:.0f}% castable  |  "
              f"BDD anchor {lbl}: ~{tgt} sources ({need['n_sources']} run, {verdict})")


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

def fmt_pct(x):
    return f"{x:5.0f}%"


def print_deck_report(name, diag, stats, combo_res, turns):
    print(f"\n{'=' * 70}")
    print(f"  {name}")
    print(f"{'=' * 70}")
    print(f"  library: {diag['library_size']} cards | commander: {diag['commander'] or '??'}")
    if diag.get("aliased"):
        print(f"  reskins resolved ({len(diag['aliased'])}): {', '.join(diag['aliased'])}")
    if diag["unresolved"]:
        print(f"  WARNING unresolved ({len(diag['unresolved'])}): {', '.join(diag['unresolved'])}")
    print(f"  keepable opening hand: {stats['keepable_pct']:.1f}%")
    show = [t for t in (2, 3, 4, 5, 6, 8, 10) if t <= turns]
    hdr = "  turn:           " + "".join(f"{t:>6}" for t in show)
    print()
    print(hdr)
    print("  avg lands:      " + "".join(f"{stats['lands_by_turn'][t]:6.1f}" for t in show))
    print("  all colrs(land):" + "".join(fmt_pct(stats['all_colors_by_turn'][t]) for t in show))
    print("  has a play:     " + "".join(fmt_pct(stats['castable_by_turn'][t]) for t in show))
    print("  (mana/colour = LAND BASE ONLY; rocks & dorks excluded — figures are a floor)")
    if combo_res:
        for cname, r in combo_res.items():
            print(f"\n  combo: {cname}  [{' + '.join(r['pieces'])}]")
            print("    drawn:        " + "".join(fmt_pct(r['drawn_by_turn'][t]) for t in show))
            print("    +tutors:      " + "".join(fmt_pct(r['with_tutor_by_turn'][t]) for t in show))


def print_flow_report(name, flow, turns, spend="greedy"):
    show = [t for t in (2, 3, 4, 5, 6, 8, 10) if t <= turns]
    policy = "deploy-all (upper bound on emptying)" if spend == "greedy" else "one play/turn (lower bound)"
    print(f"\n  flow / smoothness  (tempo model: {policy}, LANDS-only mana)")
    print("  turn:           " + "".join(f"{t:>6}" for t in show))
    print("  live (any play):" + "".join(fmt_pct(flow['live_by_turn'][t]) for t in show))
    lbl = "  live (plan):    " if flow["has_plan_spec"] else "  live (plan=any):"
    print(lbl + "".join(fmt_pct(flow['plan_live_by_turn'][t]) for t in show))
    print("  dead-starved:   " + "".join(fmt_pct(flow['starved_by_turn'][t]) for t in show))
    print("  dead-flooded:   " + "".join(fmt_pct(flow['flooded_by_turn'][t]) for t in show))
    print("  avg hand size:  " + "".join(f"{flow['hand_size_by_turn'][t]:6.1f}" for t in show))
    print("  hellbent(<=1):  " + "".join(fmt_pct(flow['hellbent_by_turn'][t]) for t in show))
    print(f"  mean dead turns (T1-{turns}): {flow['mean_dead_turns']:.2f}"
          + ("" if flow["has_plan_spec"] else "   (no keep-spec: plan-live = any-live)"))
    print("  starved=spell stuck, no mana | flooded=no nonland to cast (lands/empty)."
          " Land-only floor: starved is an upper bound. Goldfish: no reactive turns.")


def deck_rng(base_seed, key):
    """Per-deck RNG seeded from the base seed + the deck's stable key.

    Each deck draws from its OWN stream, so a single-deck run (`--deck X`)
    consumes exactly the draws of X's row in a full batch. Previously one RNG was
    threaded across every deck in the sorted batch, so X's stream depended on
    which/how many sibling decks ran before it — `--deck X` did not match that
    deck's batch row. The string seed is PYTHONHASHSEED-independent: random.seed
    derives the Mersenne state from str/bytes via SHA-512, not the randomized
    builtin hash()."""
    return random.Random(f"{base_seed}:{key}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--deck", help="Fuzzy filename filter (e.g. 'calamity')")
    ap.add_argument("--combos", action="store_true", help="Run combo assembly from sim_profiles.json")
    ap.add_argument("--need", choices=["ramp", "draw", "tutor", "interaction", "protection"],
                    help="P(>=1 source of this tagged class in hand by turn T) — the BDD count heuristic, measured")
    ap.add_argument("--flow", action="store_true",
                    help="Smoothness/tempo pass: live vs dead turns (starved/flooded), hand-size + hellbent trajectory")
    ap.add_argument("--flow-spend", choices=["greedy", "one"], default="greedy",
                    help="With --flow: 'greedy' deploys every affordable spell (upper bound on emptying); "
                         "'one' makes a single marquee play/turn (lower bound). Truth sits between.")
    ap.add_argument("--by", type=int, metavar="T", help="With --need: headline a target turn against BDD's count anchor")
    ap.add_argument("--trials", type=int, default=20000)
    ap.add_argument("--turns", type=int, default=10)
    ap.add_argument("--seed", type=int, default=12345)
    ap.add_argument("--json", metavar="PATH", help="Write machine-readable results")
    args = ap.parse_args()

    index = load_oracle_index()
    aliases = load_reskin_aliases()

    profiles = {}
    if args.combos:
        if PROFILES.exists():
            profiles = json.loads(PROFILES.read_text(encoding="utf-8"))
        else:
            print(f"WARNING: {PROFILES} not found; skipping combo assembly", file=sys.stderr)

    txts = sorted(DECKS_DIR.glob("*.txt"))
    if args.deck:
        txts = [p for p in txts if args.deck.lower() in p.stem.lower()]
        if not txts:
            sys.exit(f"No decklist matches '{args.deck}'")

    out = {}
    for path in txts:
        library, commander, diag = parse_deck(path, index, aliases)
        # Per-deck RNG so `--deck X` reproduces X's full-batch row: seed each deck's
        # stream from (base seed, stable key) instead of sharing one batch RNG whose
        # state at deck X depends on the sibling decks drawn before it.
        rng = deck_rng(args.seed, diag["deck_key"] or path.stem)
        identity = set()
        for _, r in library:
            identity.update(r["color_identity"])
        if commander and index.get(commander.lower()):
            identity.update(index[commander.lower()]["color_identity"])
        stats = simulate(library, sorted(identity), args.turns, args.trials, rng)

        combo_res = None
        prof = profiles.get(diag["deck_key"]) if profiles else None
        if prof:
            combo_res = simulate_combos(library, prof, args.turns, args.trials, rng)

        name = DISPLAY.get(diag["deck_key"], path.stem)
        print_deck_report(name, diag, stats, combo_res, args.turns)

        need_res = None
        if args.need:
            sources = need_source_set(library, args.need)
            need_res = simulate_need(library, sources, args.turns, args.trials, rng)
            print_need_report(name, args.need, need_res, args.turns, args.by)

        flow_res = None
        if args.flow:
            # Own rng stream so `--flow` reproduces regardless of --combos/--need
            # (same per-deck-stream rationale as deck_rng).
            flow_rng = deck_rng(args.seed, (diag["deck_key"] or path.stem) + ":flow")
            plan_set = plan_card_set(diag["deck_key"])
            draw_profiles = draw_map(library)
            flow_res = simulate_flow(library, args.turns, args.trials, flow_rng, plan_set,
                                     spend=args.flow_spend, draw_profiles=draw_profiles)
            print_flow_report(name, flow_res, args.turns, args.flow_spend)

        out[name] = {
            "diag": {k: v for k, v in diag.items() if k != "deck_key"},
            "identity": sorted(identity),
            "stats": stats,
            "combos": combo_res,
            "need": {"class": args.need, **need_res} if need_res else None,
            "flow": flow_res,
        }

    if args.json:
        Path(args.json).write_text(json.dumps(out, indent=2), encoding="utf-8")
        print(f"\nWrote {args.json}", file=sys.stderr)


if __name__ == "__main__":
    main()
