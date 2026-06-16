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
CLOCKS = ROOT / "analysis" / "pod_gauntlet_clocks.json"
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

# Cheapest documented win line per deck (Phase 3, BDD mana-budget). `pieces` = the
# non-commander cards that line needs (from each Summary's kill section + kill_tree +
# Kill_Window_Lab_Sweep, 2026-06-16). Commander MV is auto-added unless needs_cmdr=False
# (commander-independent combos). `override` = actual lethal mana for X / mana-gated lines
# whose printed MV lies (Torment/Banefire/Finale). `fuzzy` = combat/attrition line with no
# discrete piece set — an estimate. REVIEW + correct before trusting the bdd_mana column.
WIN_LINE = {
    "genome_project":      {"pieces": ["City on Fire"], "fuzzy": True,
                            "line": "Trance Kuja + City on Fire (x3 dmg) — 1-2 casts kill the table"},
    "radiation_sickness":  {"pieces": ["Mindcrank", "Bloodchief Ascension"], "needs_cmdr": False,
                            "line": "Mindcrank + Bloodchief Ascension infinite (commander-independent)"},
    "replication_crisis":  {"pieces": ["Sword of Feast and Famine", "Aggravated Assault"],
                            "line": "Satya + Sword of F&F + Aggravated Assault -> infinite combats"},
    "lorehold_spirits":    {"pieces": ["Reveillark", "Karmic Guide", "Goblin Bombardment"],
                            "line": "Reveillark + Karmic Guide + Goblin Bombardment loop (table)"},
    "earthbend_the_meta":  {"pieces": ["Triumph of the Hordes"], "fuzzy": True,
                            "line": "Triumph of the Hordes one-card closer from an earthbent board"},
    "exiles_return":       {"pieces": ["Hellkite Charger"], "fuzzy": True,
                            "line": "Hellkite Charger + firebending extra-combats"},
    "zero_sum_game":       {"pieces": ["Exquisite Blood", "Sanguine Bond"], "needs_cmdr": False,
                            "line": "Exquisite Blood + Sanguine Bond loop + any life event (cmdr-indep.)"},
    "curse_of_the_scarab": {"pieces": ["Gray Merchant of Asphodel"], "fuzzy": True,
                            "line": "Gray Merchant burst drain off black devotion"},
    "bumbleflower":        {"pieces": ["Jolrael, Mwonvuli Recluse"], "fuzzy": True,
                            "line": "Jolrael alpha strike (lands -> X/X, X = hand size)"},
    "eldrazi_stampede":    {"pieces": ["Craterhoof Behemoth"], "fuzzy": True,
                            "line": "Craterhoof alpha over an Eldrazi/ramp board"},
    "dark_lords_army":     {"pieces": ["Gray Merchant of Asphodel"], "fuzzy": True,
                            "line": "Sheoldred/Underworld Dreams/Wound Reflection drain + Gary close"},
    "diminishing_returns": {"pieces": ["Gravecrawler", "Phyrexian Altar"],
                            "line": "Gravecrawler + Phyrexian Altar + sac/drain loop (Teysa doubles)"},
    "lightning_war":       {"pieces": ["Banefire"], "override": 14, "fuzzy": True,
                            "line": "X-burn finisher (Banefire/Crackle); ~14 mana from-40 lethal"},
    "grand_design":        {"pieces": ["Finale of Devastation"], "override": 12, "fuzzy": True,
                            "line": "Finale of Devastation X>=10 (sorcery funnel); combat backup"},
    "crystal_sickness":    {"pieces": ["Phyrexian Dreadnought"], "fuzzy": True,
                            "line": "Golbez drain off a high-power creature (needs digging + cycles)"},
    "calamity_tax":        {"pieces": ["Torment of Hailfire"], "override": 14, "fuzzy": True,
                            "line": "Torment of Hailfire X=12+ (requires ~14 total mana)"},
}

# Richer outcome oracles = the project's results MODELS (P(win), higher=better). Harvested
# 2026-06-16: pod_gauntlet = `pod_gauntlet.py --trials 20000` P(WIN) col (a=0.3, vs the
# archenemy combo pod); self_meta = `self_meta_lab.py --trials 20000` WIN% col (random 4-seat
# roster pod, T_grind=10). Snapshot, like the CC scores — regenerate by rerunning those labs.
# CAVEAT: pod_gauntlet P(win) is partly DERIVED from the decap clock (+ disruption) and
# self_meta from the TABLE clock (+ durability), so pure_clock correlates with them partly by
# construction — flagged in --bakeoff. CC/Disciple/BDD are independent of both.
RICHER_ORACLE = {                       # slug: (pod_gauntlet P(win), self_meta P(win))
    "genome_project":      (66, 79),
    "radiation_sickness":  (69, 42),
    "replication_crisis":  (60, 18),
    "lorehold_spirits":    (42, 31),
    "earthbend_the_meta":  (42, 17),
    "exiles_return":       (44, 36),
    "zero_sum_game":       (36, 51),
    "curse_of_the_scarab": (38, 24),
    "bumbleflower":        (48, 12),
    "eldrazi_stampede":    (28, 11),
    "dark_lords_army":     (24, 24),
    "diminishing_returns": (18, 3),
    "lightning_war":       (38, 5),
    "grand_design":        (24, 1),
    "crystal_sickness":    (9, 12),
    "calamity_tax":        (20, 35),
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


# --- framework-specific counters (stricter than the generic substrate tags) ---
def disciple_is_draw(card):
    """DotV draw = sees 3+ cards in one shot, OR a permanent with repeatable draw.

    Deliberately stricter than the 'draw' tag: a one-shot draw-two (Night's Whisper) does
    NOT qualify, matching the rubric's 'see 3 cards, or a permanent that gives repeatable
    draw' (examples Brainstorm / Howling Mine / Phyrexian Arena).
    """
    t = card_text(card)
    if "draw" not in t:
        return False
    typ = card_type(card)
    permanent = (any(k in typ for k in ("artifact", "enchantment", "creature", "planeswalker", "battle"))
                 and "instant" not in typ and "sorcery" not in typ)
    repeatable = permanent and bool(re.search(r"draws? (a|\w+) cards?", t))
    sees3 = bool(re.search(r"draws? (three|four|five|six|seven|x|\d{2,}) cards", t)
                 or re.search(r"draws? that many cards", t)
                 or re.search(r"draws? cards equal", t)
                 or re.search(r"look at the top (three|four|five|six|\d+)", t))
    return repeatable or sees3


_MLD_NAMES = {"armageddon", "ravages of war", "catastrophe", "jokulhaups", "obliterate",
              "decree of annihilation", "impending disaster", "fall of the thran",
              "wildfire", "burning of xinye", "boom // bust"}


def is_mld(card):
    t = card_text(card)
    return (card.get("name", "").lower() in _MLD_NAMES
            or "destroy all lands" in t
            or ("each player" in t and re.search(r"sacrifices? .*lands", t)))


def is_extra_turn(card):
    return "take an extra turn" in card_text(card)


def clock_turn(s):
    """'T7' -> 7, '>T14' -> 14, 'T10' -> 10. Lower = faster."""
    m = re.search(r"(\d+)", s or "")
    return int(m.group(1)) if m else None


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
    """Aggregate one deck into counts/tags + framework-specific signals."""
    total = lands = nonland = 0
    cmc_sum = 0.0
    tag_counts = {k: 0 for k in TAGS}
    tag_examples = {k: [] for k in TAGS}
    gc_hits, missing = [], []
    dD = dT = dR = dI = 0                  # Disciple components (commander counts 2 for D, T)
    mld = extra_turns = 0
    for cnt, name, canon, card, is_cmd in deck_cards(slug, idx, aliases):
        total += cnt
        if card is None:
            missing.append(name); continue
        if canon in gc:
            gc_hits.append(name)
        if is_mld(card):
            mld += cnt
        if is_extra_turn(card):
            extra_turns += cnt
        if is_land(card):
            lands += cnt; continue
        nonland += cnt
        cmc = card_cmc(card)
        cmc_sum += cmc * cnt
        tags = tag_card(card)
        for tg in tags:
            tag_counts[tg] += cnt
            if len(tag_examples[tg]) < 6:
                tag_examples[tg].append(name)
        if disciple_is_draw(card):
            dD += 2 if is_cmd else cnt
        if "tutor" in tags and (cmc <= 4 or is_cmd):
            dT += 2 if is_cmd else cnt
        if "ramp" in tags and (cmc <= 2 or is_cmd):
            dR += cnt
        if "interaction" in tags:
            dI += cnt
    avg = cmc_sum / nonland if nonland else 0.0
    return {
        "total": total, "lands": lands, "nonland": nonland,
        "avg_cmc": round(avg, 2),
        "tags": tag_counts, "examples": tag_examples,
        "gc": gc_hits, "missing": missing,
        "disciple": {"A": max(avg, 1.0), "D": dD, "T": dT, "R": dR, "I": dI},
        "mld": mld, "extra_turns": extra_turns,
    }


# ----------------------------------------------------------------- scorers
_CLOCKS_PATH = None                       # set by --clocks (smart-mulligan experiment)


def load_clocks():
    path = _CLOCKS_PATH or CLOCKS
    return json.load(path.open(encoding="utf-8")) if path.exists() else {}


def score_conversion_check(slug, prof):
    """Incumbent: the stored 4-axis total (None if unaudited)."""
    return DECKS[slug][2]


def score_disciple(slug, prof):
    """DotV: P = 2/A + (D/2 + T + R/2)/2 + I/20."""
    d = prof["disciple"]
    return round(2 / d["A"] + (d["D"] / 2 + d["T"] + d["R"] / 2) / 2 + d["I"] / 20, 2)


def score_wotc(slug, prof):
    """Official bracket bucket from GC count + MLD + extra-turn signals.

    Cheap 2-card-combo detection (the other B4 trigger) is out of scope for a regex pass,
    so this LOWER-bounds the bracket; most of our >=1-GC roster lands at 3 (low resolution,
    which is itself the expected finding for the official framework)."""
    gc = len(prof["gc"])
    if prof["mld"] or gc > 3 or prof["extra_turns"] >= 2:
        return 4
    return 3 if gc >= 1 else 2


# BDD math-video targets (operationalized from the 11-to-guarantee-by-T2 / ~38-land guidance).
BDD_TARGETS = {"lands": 36, "ramp": 8, "draw": 8, "interaction": 6, "protection": 6}


def score_bdd_consistency(slug, prof):
    """How completely the deck fills BDD's functional bases (0-5; higher = better-built)."""
    counts = {"lands": prof["lands"], "ramp": prof["tags"]["ramp"], "draw": prof["tags"]["draw"],
              "interaction": prof["tags"]["interaction"], "protection": prof["tags"]["protection"]}
    return round(sum(min(counts[k] / t, 1.0) for k, t in BDD_TARGETS.items()), 2)


def score_pure_clock(slug, clocks):
    """Null hypothesis: lab decap median turn (lower = faster). Returns the turn number."""
    c = clocks.get(slug)
    return clock_turn(c["med"][0]) if c else None


def cumulative_mana(turn):
    """BDD total-mana-by-turn budget ≈ triangular sum (~1 land/turn). T7≈28 (+ramp≈35 = his B3)."""
    return turn * (turn + 1) // 2 if turn else None


def deck_card_set(slug, idx, aliases):
    return {canon for _c, _n, canon, card, _ic in deck_cards(slug, idx, aliases) if card}


def commander_mv(slug, idx, aliases):
    for _c, _n, canon, card, is_cmd in deck_cards(slug, idx, aliases):
        if is_cmd and card:
            return card_cmc(card), canon
    return 0.0, None


def score_bdd_mana(slug, idx, aliases):
    """BDD win-line mana: override if set, else commander(if needed) + the pieces' MVs.

    Returns (total, breakdown[(name, mv, in_deck)], missing). `in_deck=False` flags a piece
    I named that isn't actually in this decklist — a self-check on the hand-encoded lines.
    """
    wl = WIN_LINE[slug]
    if wl.get("override"):
        return float(wl["override"]), [("[override: X/mana-gated]", float(wl["override"]), True)], []
    deckset = deck_card_set(slug, idx, aliases)
    total, breakdown, missing = 0.0, [], []
    if wl.get("needs_cmdr", True):
        mv, cn = commander_mv(slug, idx, aliases)
        total += mv
        breakdown.append((cn or "?commander", mv, True))
    for name in wl["pieces"]:
        canon = aliases.get(name.lower(), name.lower())
        card = idx.get(canon)
        if not card:
            missing.append(name); continue
        total += card_cmc(card)
        breakdown.append((name, card_cmc(card), canon in deckset))
    return round(total, 1), breakdown, missing


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


# ----------------------------------------------------------------- correlation
def _avg_ranks(vals):
    """1-based average ranks, ascending (smallest value -> rank 1); ties share mean rank."""
    order = sorted(range(len(vals)), key=lambda i: vals[i])
    ranks = [0.0] * len(vals)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and vals[order[j + 1]] == vals[order[i]]:
            j += 1
        avg = (i + j) / 2 + 1
        for k in range(i, j + 1):
            ranks[order[k]] = avg
        i = j + 1
    return ranks


def spearman(x, y):
    """Tie-aware Spearman rho on pairwise-complete data. Returns (rho|None, n)."""
    pairs = [(a, b) for a, b in zip(x, y) if a is not None and b is not None]
    n = len(pairs)
    if n < 3:
        return None, n
    rx = _avg_ranks([p[0] for p in pairs])
    ry = _avg_ranks([p[1] for p in pairs])
    mx, my = sum(rx) / n, sum(ry) / n
    cov = sum((rx[i] - mx) * (ry[i] - my) for i in range(n))
    vx = sum((r - mx) ** 2 for r in rx)
    vy = sum((r - my) ** 2 for r in ry)
    if vx == 0 or vy == 0:           # a framework with no variance (e.g. WotC all 3)
        return None, n
    return round(cov / (vx * vy) ** 0.5, 3), n


def framework_values(idx, gc, aliases, clocks):
    """Per-deck value for every framework, ORIENTED so higher = 'should win',
    plus the oracle values (faster clock = higher). Returns dict[name] -> list[16]."""
    cols = {k: [] for k in ("conversion_check", "disciple", "wotc_bracket",
                            "bdd_consistency", "bdd_mana", "pure_clock",
                            "oracle_table", "oracle_decap", "oracle_gauntlet", "oracle_selfmeta")}
    for slug in DECKS:
        p = profile(slug, idx, gc, aliases)
        c = clocks.get(slug, {})
        decap = clock_turn(c.get("med", [None, None])[0])
        table = clock_turn(c.get("med", [None, None])[1])
        bm, _bd, _m = score_bdd_mana(slug, idx, aliases)
        cc = score_conversion_check(slug, p)
        gpw, smw = RICHER_ORACLE.get(slug, (None, None))
        cols["conversion_check"].append(float(cc) if cc is not None else None)
        cols["disciple"].append(score_disciple(slug, p))
        cols["wotc_bracket"].append(float(score_wotc(slug, p)))
        cols["bdd_consistency"].append(score_bdd_consistency(slug, p))
        cols["bdd_mana"].append(-bm if bm is not None else None)        # lower mana = better
        cols["pure_clock"].append(-decap if decap else None)            # faster decap = better
        cols["oracle_table"].append(-table if table else None)         # faster table = better
        cols["oracle_decap"].append(-decap if decap else None)
        cols["oracle_gauntlet"].append(float(gpw) if gpw is not None else None)   # P(win), higher=better
        cols["oracle_selfmeta"].append(float(smw) if smw is not None else None)
    return cols


def cmd_bakeoff(a, idx, gc, aliases):
    clocks = load_clocks()
    cols = framework_values(idx, gc, aliases, clocks)
    contestants = [("conversion_check", "Conversion Check (incumbent)"),
                   ("bdd_mana", "BDD mana-budget"),
                   ("disciple", "Disciple of the Vault"),
                   ("bdd_consistency", "BDD consistency"),
                   ("wotc_bracket", "WotC bracket 1-5"),
                   ("pure_clock", "Pure clock (null)")]
    print("FRAMEWORK BAKE-OFF — Spearman rho vs four outcome oracles")
    print("(every framework oriented so higher = 'should win'; clocks faster=better, P(win) higher=better)")
    print(f"\n{'framework':<28}{'gauntlet':>9}{'selfmeta':>9}{'TABLE':>8}{'decap':>8}{'N':>4}  note")
    print("-" * 78)

    def cell(key, oracle):
        r, _n = spearman(cols[key], cols[oracle])
        return "—" if r is None else f"{r:+.3f}"

    for key, label in contestants:
        _r, n = spearman(cols[key], cols["oracle_gauntlet"])
        note = ""
        if cell(key, "oracle_table") == "—":
            note = "no variance"
        elif key == "pure_clock":
            note = "semi-circular: oracles derive from the clock"
        print(f"{label:<28}{cell(key,'oracle_gauntlet'):>9}{cell(key,'oracle_selfmeta'):>9}"
              f"{cell(key,'oracle_table'):>8}{cell(key,'oracle_decap'):>8}{n:>4}  {note}")
    print("\nORACLES — gauntlet: P(beat the T6-7 combo pod) · selfmeta: P(win in a roster pod)")
    print("          TABLE/decap: lab kill clocks (faster=better). +1 agree · 0 unrelated · -1 backwards.")
    print("CC N=15 (Zero-Sum unaudited). bdd_mana rests on fuzzy win-lines. pure_clock vs the P(win)")
    print("oracles is semi-circular (they're built partly FROM the clock) — CC/Disciple/BDD are not.")


def cmd_scores(a, idx, gc, aliases):
    """Per-deck score under every framework."""
    clocks = load_clocks()
    hdr = (f"{'slug':<22}{'CC':>5}{'discip':>8}{'wotc':>6}{'bdd_c':>7}{'bddMana':>8}{'clock':>7}")
    print(hdr); print("-" * len(hdr))
    for slug in DECKS:
        p = profile(slug, idx, gc, aliases)
        cc = score_conversion_check(slug, p)
        pc = score_pure_clock(slug, clocks)
        bm, _bd, _miss = score_bdd_mana(slug, idx, aliases)
        print(f"{slug:<22}{str(cc):>5}{score_disciple(slug, p):>8}{score_wotc(slug, p):>6}"
              f"{score_bdd_consistency(slug, p):>7}{bm:>8}{('T' + str(pc)) if pc else '?':>7}")
    print("\nCC=Conversion Check (None=unaudited) · discip=Disciple of the Vault P · wotc=bracket"
          " 1-5 · bdd_c=BDD consistency 0-5 · bddMana=win-line mana (lower=faster) · clock=lab decap")


def cmd_winline(a, idx, gc, aliases):
    """BDD win-line mana per deck + the cumulative-mana-by-decap cross-check."""
    clocks = load_clocks()
    print("BDD win-line mana — cheapest documented kill line per deck.")
    print("  * = fuzzy combat/attrition estimate · (!) = piece NOT in this decklist (review)\n")
    for slug in DECKS:
        total, bd, missing = score_bdd_mana(slug, idx, aliases)
        wl = WIN_LINE[slug]
        decap = score_pure_clock(slug, clocks)
        budget = cumulative_mana(decap)
        star = "*" if wl.get("fuzzy") else " "
        pieces = ", ".join(f"{n} {mv:g}{'' if ind else ' (!)'}" for n, mv, ind in bd)
        print(f"{slug:<22}{star} win-mana {total:>5}   decap T{decap}   budget≈{budget}")
        print(f"     {wl['line']}")
        print(f"     = {pieces}" + (f"   MISSING: {missing}" if missing else ""))
    print("\nbudget = cumulative mana by decap turn (≈T(T+1)/2). Phase 4 tests whether win-mana"
          "\nrank-correlates with the lab clock (does cheaper win line => faster deck?).")


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0],
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--decks", action="store_true", help="show registry + resolved decklists")
    g.add_argument("--gc", action="store_true", help="show parsed GC set + per-deck counts")
    g.add_argument("--tags", metavar="SLUG|all", help="tagged breakdown for a deck (or 'all')")
    g.add_argument("--scores", action="store_true", help="per-deck score under each framework")
    g.add_argument("--winline", action="store_true", help="BDD win-line mana + decap cross-check")
    g.add_argument("--bakeoff", action="store_true", help="Spearman: each framework vs the oracle")
    ap.add_argument("--clocks", metavar="FILE",
                    help="alternate clocks JSON (smart-mulligan experiment); default = the committed one")
    a = ap.parse_args()

    global _CLOCKS_PATH
    if a.clocks:
        _CLOCKS_PATH = Path(a.clocks)
    idx = load_oracle()
    gc = load_gc()
    aliases = load_aliases()
    if a.decks:
        cmd_decks(a, idx, gc, aliases)
    elif a.gc:
        cmd_gc(a, idx, gc, aliases)
    elif a.tags:
        cmd_tags(a, idx, gc, aliases)
    elif a.scores:
        cmd_scores(a, idx, gc, aliases)
    elif a.winline:
        cmd_winline(a, idx, gc, aliases)
    elif a.bakeoff:
        cmd_bakeoff(a, idx, gc, aliases)


if __name__ == "__main__":
    main()
