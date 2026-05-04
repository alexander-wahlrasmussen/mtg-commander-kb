#!/usr/bin/env python3
"""
card_lookup.py — look up Scryfall oracle data and rulings for a card by name.

Usage:
    python scripts/card_lookup.py "Atraxa, Praetors' Voice"
    python scripts/card_lookup.py "Arlinn Kord"          # finds DFC by front face name
    python scripts/card_lookup.py "Fire // Ice"          # split card full name
    python scripts/card_lookup.py --fuzzy atraxa
    python scripts/card_lookup.py --name-only atraxa     # just list matching names

Data source: collection/oracle-cards.json + collection/rulings.json
Run update_scryfall_data.py to refresh both files.
"""

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

COLLECTION = Path(__file__).parent.parent / "collection"
DATA_FILE = COLLECTION / "oracle-cards.json"
RULINGS_FILE = COLLECTION / "rulings.json"

# Layouts where oracle_text lives in card_faces, not at top level
MULTI_FACE_LAYOUTS = {"transform", "modal_dfc", "split", "adventure", "flip",
                      "double_faced_token", "art_series", "prepare"}

# Layouts that are not real playable cards — sort to the back of results
JUNK_LAYOUTS = {"art_series", "double_faced_token", "token"}


def load_cards():
    if not DATA_FILE.exists():
        sys.exit(f"ERROR: {DATA_FILE} not found — run scripts/update_scryfall_data.py first")
    with DATA_FILE.open(encoding="utf-8") as f:
        return json.load(f)


def load_rulings_index():
    if not RULINGS_FILE.exists():
        return {}
    with RULINGS_FILE.open(encoding="utf-8") as f:
        rulings = json.load(f)
    index = defaultdict(list)
    for r in rulings:
        index[r["oracle_id"]].append(r["comment"])
    return index


def normalize_name(name):
    """Normalize // spacing so 'Fire//Ice' and 'Fire // Ice' both work."""
    return " // ".join(part.strip() for part in name.split("//"))


def face_names(card):
    """Return all searchable names for a card: full name + individual face names."""
    names = {card.get("name", "").lower()}
    for face in card.get("card_faces", []):
        face_name = face.get("name", "")
        if face_name:
            names.add(face_name.lower())
    return names


def format_face(face, separator=False):
    lines = []
    if separator:
        lines.append("- - - - - - - - - - - - - - - - - - - - - - - - - -")
    name = face.get("name", "?")
    mana = face.get("mana_cost", "")
    lines.append(f"  [{name}]  {mana}".rstrip())
    type_line = face.get("type_line", "")
    if type_line:
        lines.append(f"  {type_line}")
    oracle = face.get("oracle_text", "").strip()
    if oracle:
        lines.append(oracle)
    pt = face.get("power"), face.get("toughness")
    if pt[0] is not None:
        lines.append(f"P/T: {pt[0]}/{pt[1]}")
    return "\n".join(lines)


def format_card(card, rulings_index):
    lines = []
    name = card.get("name", "?")
    layout = card.get("layout", "normal")
    is_multi_face = layout in MULTI_FACE_LAYOUTS or not card.get("oracle_text")

    # Header
    if is_multi_face:
        mana = ""  # mana is per-face for multi-face cards
    else:
        mana = card.get("mana_cost", "")
    cmc = card.get("cmc", "")
    lines.append(f"{'=' * 60}")
    lines.append(f"  {name}  {mana}  (CMC {cmc})".rstrip())
    if not is_multi_face:
        lines.append(f"  {card.get('type_line', '')}")
    lines.append(f"{'=' * 60}")

    if is_multi_face:
        faces = card.get("card_faces", [])
        for i, face in enumerate(faces):
            lines.append(format_face(face, separator=(i > 0)))
    else:
        oracle = card.get("oracle_text", "").strip()
        if oracle:
            lines.append(oracle)
        pt = card.get("power"), card.get("toughness")
        if pt[0] is not None:
            lines.append(f"P/T: {pt[0]}/{pt[1]}")

    ci = card.get("color_identity", [])
    if ci:
        lines.append(f"\nColor identity: {''.join(ci)}")

    kw = card.get("keywords", [])
    if kw:
        lines.append(f"Keywords: {', '.join(kw)}")

    legalities = card.get("legalities", {})
    commander_status = legalities.get("commander", "unknown")
    lines.append(f"Commander legal: {commander_status}")

    rulings = rulings_index.get(card.get("oracle_id", ""), [])
    if rulings:
        lines.append(f"\n--- Rulings ({len(rulings)}) ---")
        for r in rulings:
            lines.append(f"* {r}")

    return "\n".join(lines)


def exact_match(cards, name):
    name_norm = normalize_name(name).lower()
    return [c for c in cards if name_norm in face_names(c)]


def fuzzy_match(cards, query):
    query_lower = query.lower()
    return [c for c in cards if any(query_lower in n for n in face_names(c))]


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser(
        description="Look up a Magic card's oracle text and rulings from local Scryfall data."
    )
    parser.add_argument("name", nargs="?", help="Exact card name (or one face of a DFC)")
    parser.add_argument("--fuzzy", metavar="QUERY", help="Partial name search")
    parser.add_argument("--name-only", metavar="QUERY", help="List matching names only (no card text)")
    args = parser.parse_args()

    if not any([args.name, args.fuzzy, args.name_only]):
        parser.print_help()
        sys.exit(1)

    print("Loading card data...", file=sys.stderr)
    cards = load_cards()
    rulings_index = load_rulings_index()

    if args.name_only:
        matches = fuzzy_match(cards, args.name_only)
        if not matches:
            print(f"No cards found matching '{args.name_only}'")
        else:
            for c in matches:
                print(c["name"])
        return

    if args.fuzzy:
        matches = fuzzy_match(cards, args.fuzzy)
    else:
        matches = exact_match(cards, args.name)
        if not matches:
            matches = fuzzy_match(cards, args.name)
            if matches:
                print(f"No exact match — showing fuzzy results for '{args.name}':\n", file=sys.stderr)

    if not matches:
        query = args.fuzzy or args.name
        sys.exit(f"No cards found matching '{query}'")

    # Suppress junk layouts (art series, tokens) when a real card is present
    real = [c for c in matches if c.get("layout", "") not in JUNK_LAYOUTS]
    if real:
        matches = real

    if len(matches) > 5 and (args.fuzzy or (args.name and len(args.name) < 6)):
        print(f"{len(matches)} matches — showing first 5. Use --name-only to list all.\n")
        matches = matches[:5]

    for card in matches:
        print(format_card(card, rulings_index))
        print()


if __name__ == "__main__":
    main()
