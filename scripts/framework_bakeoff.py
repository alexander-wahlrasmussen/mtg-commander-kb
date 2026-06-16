#!/usr/bin/env python3
"""framework_bakeoff.py — grade competing deck-evaluation FRAMEWORKS against the
lab-measured outcome oracle.

The question (2026-06-16, see memory project_framework_bakeoff): does The Conversion
Check actually predict RESULTS, and would a different framework rank our decks better?
We score all 16 active decks under several frameworks, then rank-correlate (Spearman)
each framework against the outcome oracle. The Conversion Check is one contestant.

Contestants (locked 2026-06-16):
    conversion_check   incumbent 4-axis judged score (from the Summaries)
    bdd_mana           Based Deck Dept "win-line mana vs bracket budget" (a clock in mana)
    disciple           Disciple of the Vault formula P = 2/A + (D/2+T+R/2)/2 + I/20
    wotc_bracket       official Commander brackets 1-5 (GC count + combo/MLD/extra-turns)
    bdd_consistency    BDD math video: function counts vs the "11 to guarantee by T2" rule
    pure_clock         null hypothesis: rank by lab decap turn (is it all just speed?)

Oracle = analysis/pod_gauntlet_clocks.json (lab decap/table medians + curves). Later we
add pod_gauntlet P(win) / self_meta P(win) and the real-game log (calibrate.py, Layer 2).

THIS FILE IS BUILT IN PHASES. Phase 1 (now) = shared infrastructure: decklist parsing,
the Scryfall card index, the per-card function tagger, and the Game-Changer loader, plus
debug views to eyeball them (`--tags`, `--gc`, `--decks`) before scoring is layered on.
Tag heuristics are oracle-text regex — noisy by nature, but a rank-correlation study is
robust to per-card tag noise. Refine the TAGGERS below and re-run `--tags` to validate.

Usage (Phase 1)
    python scripts/framework_bakeoff.py --decks            # registry + decklist resolution
    python scripts/framework_bakeoff.py --gc               # parsed Game-Changer set + per-deck counts
    python scripts/framework_bakeoff.py --tags genome_project   # tagged breakdown for one deck
    python scripts/framework_bakeoff.py --tags all              # one-line tag summary for all 16
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ORACLE_CARDS = ROOT / "collection" / "oracle-cards.json"
GC_LIST = ROOT / "reference" / "REF_Game_Changers_List.md"
ALIASES = ROOT / "reference" / "REF_Reskin_Aliases.md"
DECK_DIR = ROOT / "decks"

for _s in (sys.stdout, sys.stderr):
    if hasattr(_s, "reconfigure"):
        try:
            _s.reconfigure(encoding="utf-8", errors="replace")
        except (ValueError, OSError):
            pass

# slug -> (display name, decklist stem, CC total, CC axes). Slugs match pod_gauntlet /
# clock_check. CC scores read from the Summaries (grep'd 2026-06-16); Zero-Sum unaudited.
DECKS = {
    "genome_project":     ("The Genome Project",     "the-genome-project",   15, (4, 4, 3, 4)),
    "radiation_sickness": ("Radiation Sickness",      "radiation-sickness",   18, (5, 5, 4, 4)),
    "replication_crisis": ("The Replication Crisis",  "the-replication-crisis", 17, (5, 4, 4, 4)),
    "lorehold_spirits":   ("Lorehold Spirits",        "lorehold-spirit",      18, (5, 5, 4, 4)),
    "earthbend_the_meta": ("Earthbend the Meta",      "earthbend-the-meta",   17, (5, 4, 4, 4)),
    "exiles_return":      ("The Exile's Return",      "the-exiles-return",    17, (5, 4, 4, 4)),
    "zero_sum_game":      ("Zero-Sum Game",           "zero-sum-game",      None, None),
    "curse_of_the_scarab":("Curse of the Scarab",     "curse-of-the-scarab",  17, (5, 4, 4, 4)),
    "bumbleflower":       ("Ms. Bumbleflower",        "this-bunny-goes-to-market", 15, (4, 3, 3, 5)),
    "eldrazi_stampede":   ("Eldrazi Stampede Chaos",  "eldrazi-stampede-chaos", 14, (4, 4, 3, 3)),
    "dark_lords_army":    ("The Dark Lord's Army",    "the-dark-lords-army",  19, (5, 4, 5, 5)),
    "diminishing_returns":("Diminishing Returns",     "diminishing-returns",  17, (5, 4, 4, 4)),
    "lightning_war":      ("Lightning War",           "lightning-war",        19, (5, 5, 4, 5)),
    "grand_design":       ("The Grand Design",        "the-grand-design",     19, (5, 5, 5, 4)),
    "crystal_sickness":   ("Crystal Sickness",        "crystal-sickness",     17, (5, 4, 4, 4)),
    "calamity_tax":       ("The Calamity Tax",        "calamity-tax",         18, (5, 4, 4, 5)),
}

TAGS = ("ramp", "draw", "tutor", "interaction", "protection")


# ----------------------------------------------------------------- card index
def load_oracle():
    """name.lower() -> card dict, incl. individual face names for DFC/split/adventure."""
    if not ORACLE_CARDS.exists():
        sys.exit(f"ERROR: {ORACLE_CARDS} not found — run scripts/update_scryfall_data.py")
    cards = json.load(ORACLE_CARDS.open(encoding="utf-8"))
    idx = {}
    for c in cards:
        if c.get("layout") in ("art_series", "token", "double_faced_token"):
            continue
        idx.setdefault(c["name"].lower(), c)
        for face in c.get("card_faces", []):
            if face.get("name"):
                idx.setdefault(face["name"].lower(), c)
    return idx


def card_text(card):
    """Full oracle text incl. all faces, lowercased."""
    parts = [card.get("oracle_text", "")]
    parts += [f.get("oracle_text", "") for f in card.get("card_faces", [])]
    return "\n".join(p for p in parts if p).lower()


def card_type(card):
    parts = [card.get("type_line", "")]
    parts += [f.get("type_line", "") for f in card.get("card_faces", [])]
    return " ".join(p for p in parts if p).lower()


def card_cmc(card):
    return float(card.get("cmc", 0) or 0)


# ----------------------------------------------------------------- decklists
def resolve_deck(stem):
    hits = sorted(DECK_DIR.glob(f"{stem}-*.txt"))
    return hits[-1] if hits else None


CARD_LINE = re.compile(r"^(\d+)\s+(.+?)\s*$")


def parse_deck(path):
    """Return (main_cards, commander) as lists of (count, name).

    Convention: blocks separated by blank lines / 'SIDEBOARD:'. First block = the 99,
    last block = commander, any block after a SIDEBOARD marker is excluded.
    """
    blocks, cur, sideboard_seen = [], [], False
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line:
            if cur:
                blocks.append((cur, sideboard_seen)); cur = []
            continue
        if line.upper().startswith("SIDEBOARD"):
            if cur:
                blocks.append((cur, sideboard_seen)); cur = []
            sideboard_seen = True
            continue
        m = CARD_LINE.match(line)
        if m:
            cur.append((int(m.group(1)), m.group(2)))
    if cur:
        blocks.append((cur, sideboard_seen))
    card_blocks = [b for b, _ in blocks]
    if not card_blocks:
        return [], []
    main = card_blocks[0]
    commander = card_blocks[-1] if len(card_blocks) > 1 else []
    return main, commander


# ----------------------------------------------------------------- tagger
def is_land(card):
    return "land" in card_type(card)


_LAND_FETCH = re.compile(
    r"search your library for [^.]*?\b(lands?|forest|plains|island|swamp|mountain|wastes)\b")


def _classify_search(t):
    """A library search resolves to 'ramp' (land onto battlefield), 'tutor', or None.

    Land-ramp (Farseek, Cultivate) names land types, not always the word 'land', so we
    match basic-land-type names too. A land fetched to HAND is fixing, not acceleration
    or a wincon tutor -> None.
    """
    if "search your library" not in t:
        return None
    if _LAND_FETCH.search(t):
        return "ramp" if "onto the battlefield" in t else None
    if re.search(r"search your library for (a|an|up to|two|three|four|x|that|any)", t):
        return "tutor"
    return None


def tag_card(card):
    """Return set of function tags for one card (a card may carry several)."""
    if is_land(card):
        return set()                       # lands are handled separately
    t = card_text(card)
    tags = set()
    search = _classify_search(t)

    # ramp: mana production / treasure / land onto battlefield
    if re.search(r"add \{", t) or re.search(r"create .*treasure", t) or search == "ramp":
        tags.add("ramp")
    if search == "tutor":
        tags.add("tutor")
    if re.search(r"draw (a card|\w+ cards|that many cards|cards equal)", t):
        tags.add("draw")
    if (re.search(r"(destroy|exile) (target|all|each|up to)", t)
            or "counter target" in t
            or re.search(r"deals? \d+ damage to (target|any target|each)", t)
            or re.search(r"return target .*to (its|their) (owner|hand)", t)
            or "fight" in t
            or "each player sacrifices" in t
            or re.search(r"(doesn't|don't|can't) untap", t)
            or ("skip" in t and "step" in t)):
        tags.add("interaction")
    if (re.search(r"\b(hexproof|indestructible|shroud)\b", t)
            or "protection from" in t
            or "can't be countered" in t
            or "phase out" in t or "phases out" in t
            or re.search(r"prevent all (damage|combat damage)", t)):
        tags.add("protection")
    return tags


# ----------------------------------------------------------------- Game Changers
def load_gc():
    """Parse the numbered alphabetical Full List, stopping before the next section."""
    gc = set()
    in_list = False
    for line in GC_LIST.read_text(encoding="utf-8").splitlines():
        if line.startswith("## Full List"):
            in_list = True; continue
        if in_list:
            if line.startswith("---") or line.startswith("## "):
                break
            m = re.match(r"^\s*\d+\.\s+(.+?)\s*$", line)
            if m:
                gc.add(m.group(1).lower())
    return gc


def load_aliases():
    """Reskin / custom printed name -> canonical MTG card name (both lowercased).

    Parses every table row under '## Confirmed aliases' (col 0 = printed name,
    col 1 = canonical card), skipping headers and separator rows. Lets us resolve UB
    reskins (Aang's Shelter -> Teferi's Protection) for BOTH card lookup and GC count.
    """
    aliases = {}
    in_section = False
    for line in ALIASES.read_text(encoding="utf-8").splitlines():
        if line.startswith("## Confirmed aliases"):
            in_section = True; continue
        if in_section and line.startswith("## "):
            break
        if in_section and line.lstrip().startswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) < 2:
                continue
            src, dst = cells[0], cells[1]
            if not src or src.lower() in ("reskin name", "name") or set(src) <= set("-: "):
                continue
            aliases[src.lower()] = dst.lower()
    return aliases


# ----------------------------------------------------------------- deck model
def deck_cards(slug, idx, aliases):
    """Yield (count, printed_name, canonical, card-or-None, is_commander)."""
    path = resolve_deck(DECKS[slug][1])
    if path is None:
        sys.exit(f"no decklist found for {slug} (stem {DECKS[slug][1]})")
    main, commander = parse_deck(path)
    for cnt, name in main:
        canon = aliases.get(name.lower(), name.lower())
        yield cnt, name, canon, idx.get(canon), False
    for cnt, name in commander:
        canon = aliases.get(name.lower(), name.lower())
        yield cnt, name, canon, idx.get(canon), True


def profile(slug, idx, gc, aliases):
    """Aggregate one deck into counts/tags. Returns a dict."""
    total = lands = nonland = 0
    cmc_sum = 0.0
    tag_counts = {k: 0 for k in TAGS}
    tag_examples = {k: [] for k in TAGS}
    gc_hits, missing = [], []
    for cnt, name, canon, card, _is_cmd in deck_cards(slug, idx, aliases):
        total += cnt
        if card is None:
            missing.append(name); continue
        if canon in gc:
            gc_hits.append(name)
        if is_land(card):
            lands += cnt; continue
        nonland += cnt
        cmc_sum += card_cmc(card) * cnt
        for tg in tag_card(card):
            tag_counts[tg] += cnt
            if len(tag_examples[tg]) < 6:
                tag_examples[tg].append(name)
    return {
        "total": total, "lands": lands, "nonland": nonland,
        "avg_cmc": round(cmc_sum / nonland, 2) if nonland else 0.0,
        "tags": tag_counts, "examples": tag_examples,
        "gc": gc_hits, "missing": missing,
    }


# ----------------------------------------------------------------- commands
def cmd_decks(_a, idx, gc, aliases):
    print(f"{'slug':<22}{'CC':>4}  decklist")
    for slug, (name, stem, cc, _ax) in DECKS.items():
        path = resolve_deck(stem)
        print(f"{slug:<22}{str(cc):>4}  {path.name if path else '!! MISSING'}")


def cmd_gc(_a, idx, gc, aliases):
    print(f"Parsed {len(gc)} Game Changers from {GC_LIST.name}\n")
    print(f"{'slug':<22}{'GC#':>4}  cards")
    for slug in DECKS:
        p = profile(slug, idx, gc, aliases)
        print(f"{slug:<22}{len(p['gc']):>4}  {', '.join(p['gc']) or '—'}")


def cmd_tags(a, idx, gc, aliases):
    slugs = list(DECKS) if a.tags == "all" else [a.tags]
    if a.tags != "all" and a.tags not in DECKS:
        sys.exit(f"unknown slug {a.tags!r}; choose from {', '.join(DECKS)} or 'all'")
    if a.tags == "all":
        hdr = f"{'slug':<22}{'cards':>6}{'land':>5}{'nCMC':>6}" + "".join(f"{t[:4]:>6}" for t in TAGS) + f"{'miss':>6}"
        print(hdr); print("-" * len(hdr))
        for slug in slugs:
            p = profile(slug, idx, gc, aliases)
            row = f"{slug:<22}{p['total']:>6}{p['lands']:>5}{p['avg_cmc']:>6}"
            row += "".join(f"{p['tags'][t]:>6}" for t in TAGS)
            row += f"{len(p['missing']):>6}"
            print(row)
        return
    for slug in slugs:
        p = profile(slug, idx, gc, aliases)
        print(f"\n=== {DECKS[slug][0]} ({slug}) ===")
        print(f"  cards {p['total']}  (lands {p['lands']}, nonland {p['nonland']}, avg nonland CMC {p['avg_cmc']})")
        print(f"  Game Changers ({len(p['gc'])}): {', '.join(p['gc']) or '—'}")
        for t in TAGS:
            print(f"  {t:<12} {p['tags'][t]:>3}   e.g. {', '.join(p['examples'][t])}")
        if p["missing"]:
            print(f"  !! {len(p['missing'])} names not found in card data: {', '.join(p['missing'])}")


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0],
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--decks", action="store_true", help="show registry + resolved decklists")
    g.add_argument("--gc", action="store_true", help="show parsed GC set + per-deck counts")
    g.add_argument("--tags", metavar="SLUG|all", help="tagged breakdown for a deck (or 'all')")
    a = ap.parse_args()

    idx = load_oracle()
    gc = load_gc()
    aliases = load_aliases()
    if a.decks:
        cmd_decks(a, idx, gc, aliases)
    elif a.gc:
        cmd_gc(a, idx, gc, aliases)
    elif a.tags:
        cmd_tags(a, idx, gc, aliases)


if __name__ == "__main__":
    main()
