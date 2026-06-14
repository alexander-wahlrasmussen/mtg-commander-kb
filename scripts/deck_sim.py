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

Everything is derived from the .txt decklist + collection/oracle-cards.json
(cmc, type_line, color_identity). No card *text* is interpreted, so output is
exactly as trustworthy as those two inputs. Unresolved card names are reported
explicitly — never silently dropped.

Usage:
    python scripts/deck_sim.py                      # all decks, consistency table
    python scripts/deck_sim.py --deck calamity      # one deck (fuzzy filename match)
    python scripts/deck_sim.py --combos             # also run combo assembly (sim_profiles.json)
    python scripts/deck_sim.py --trials 50000       # trial count (default 20000)
    python scripts/deck_sim.py --json out.json      # machine-readable dump (feeds the matrix)

Data source: collection/oracle-cards.json (refresh via update_scryfall_data.py)
Combo profiles: scripts/sim_profiles.json
"""

import argparse
import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
DECKS_DIR = ROOT / "decks"
ORACLE = ROOT / "collection" / "oracle-cards.json"
PROFILES = Path(__file__).parent / "sim_profiles.json"
ALIASES_DOC = ROOT / "reference" / "REF_Reskin_Aliases.md"

# Commander per decklist (filename stem prefix -> commander card name). Needed
# because some exports list the commander inline in the 100-card main block; it
# belongs in the command zone, not the shuffled library.
COMMANDERS = {
    "calamity-tax": "Glarb, Calamity's Augur",
    "crystal-sickness": "Golbez, Crystal Collector",
    "curse-of-the-scarab": "The Scarab God",
    "diminishing-returns": "Teysa Karlov",
    "earthbend-the-meta": "Toph, the First Metalbender",
    "eldrazi-stampede-chaos": "Maelstrom Wanderer",
    "lightning-war": "Fire Lord Azula",
    "lorehold-spirit": "Quintorius, History Chaser",
    "peace-offering": None,
    "radiation-sickness": "Wise Mothman",
    "the-dark-lords-army": "Sauron, the Dark Lord",
    "the-exiles-return": "Fire Lord Zuko",
    "the-genome-project": "Kuja, Genome Sorcerer",
    "the-grand-design": "Atraxa, Grand Unifier",
    "the-loam-cycle": "Teval, the Balanced Scale",
    "the-replication-crisis": "Satya, Aetherflux Genius",
    "this-bunny-goes-to-market": "Ms. Bumbleflower",
    "zero-sum-game": "Witherbloom, the Balancer",
    # 2026-06-12 bake-off candidates (decks/considering/) + the two externals
    "insider-trading": "Yuriko, the Tiger's Shadow",
    "hostile-takeover": "Godo, Bandit Warlord",
    "quantitative-easing": "Kinnan, Bonder Prodigy",
    "asset-stripping": "Korvold, Fae-Cursed King",
    "forced-liquidation": "Kefka, Court Mage",
    "clive-external": "Clive, Ifrit's Dominant",
    "kefka-external": "Kefka, Court Mage",
    # 2026-06-14 Hashaton benchmark (decks/considering/) — Esper Thoracle variant
    "hashaton-thoracle": "Hashaton, Scarab's Fist",
    # 2026-06-13 external Glarb lists under evaluation (decks/considering/) — all Glarb
    "glarb-strong-ext": "Glarb, Calamity's Augur",
    "glarb-mastermind-ext": "Glarb, Calamity's Augur",
    "glarb-croak-dagger-ext": "Glarb, Calamity's Augur",
    "glarb-hybrid": "Glarb, Calamity's Augur",
    "glarb-hybrid-final": "Glarb, Calamity's Augur",
    "glarb-hybrid-b3": "Glarb, Calamity's Augur",
    # 2026-06-13 lab-run candidates (decks/considering/)
    "berta-wise-extrapolator": "Berta, Wise Extrapolator",
    "najeela-blade-blossom": "Najeela, the Blade-Blossom",
}

DISPLAY = {
    "calamity-tax": "The Calamity Tax",
    "crystal-sickness": "Crystal Sickness",
    "curse-of-the-scarab": "Curse of the Scarab",
    "diminishing-returns": "Diminishing Returns",
    "earthbend-the-meta": "Earthbend the Meta",
    "eldrazi-stampede-chaos": "Eldrazi Stampede Chaos",
    "lightning-war": "Lightning War",
    "lorehold-spirit": "Lorehold Spirits",
    "peace-offering": "Peace Offering",
    "radiation-sickness": "Radiation Sickness",
    "the-dark-lords-army": "The Dark Lord's Army",
    "the-exiles-return": "The Exile's Return",
    "the-genome-project": "The Genome Project",
    "the-grand-design": "The Grand Design",
    "the-loam-cycle": "The Loam Cycle",
    "the-replication-crisis": "The Replication Crisis",
    "this-bunny-goes-to-market": "Ms. Bumbleflower",
    "zero-sum-game": "Zero-Sum Game",
}


# ---------------------------------------------------------------------------
# Card data
# ---------------------------------------------------------------------------

def load_oracle_index():
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
    return library, commander, diag


# ---------------------------------------------------------------------------
# Monte Carlo
# ---------------------------------------------------------------------------

def keep_hand(hand):
    """London-mulligan keep rule: keep a 7 with 2-5 lands."""
    lands = sum(1 for _, rec in hand if is_land(rec))
    return 2 <= lands <= 5


def opening_hand(deck, rng):
    """Shuffle, draw 7, mulligan up to twice on an unkeepable hand."""
    rng.shuffle(deck)
    hand = deck[:7]
    mulls = 0
    while not keep_hand(hand) and mulls < 2:
        rng.shuffle(deck)
        hand = deck[:7]
        mulls += 1
    return list(hand), keep_hand(hand)


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


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--deck", help="Fuzzy filename filter (e.g. 'calamity')")
    ap.add_argument("--combos", action="store_true", help="Run combo assembly from sim_profiles.json")
    ap.add_argument("--trials", type=int, default=20000)
    ap.add_argument("--turns", type=int, default=10)
    ap.add_argument("--seed", type=int, default=12345)
    ap.add_argument("--json", metavar="PATH", help="Write machine-readable results")
    args = ap.parse_args()

    rng = random.Random(args.seed)
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
        out[name] = {
            "diag": {k: v for k, v in diag.items() if k != "deck_key"},
            "identity": sorted(identity),
            "stats": stats,
            "combos": combo_res,
        }

    if args.json:
        Path(args.json).write_text(json.dumps(out, indent=2), encoding="utf-8")
        print(f"\nWrote {args.json}", file=sys.stderr)


if __name__ == "__main__":
    main()
