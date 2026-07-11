#!/usr/bin/env python3
"""Search the OWNED collection for cards matching a color identity + oracle-text regex.

Intersects a Moxfield haves CSV with collection/oracle-cards.json so you only see cards
you physically own that are legal in a given color identity. Built for deckbuilding a new
commander from the pool (e.g. "owned Naya token-makers").

Examples:
  python scripts/pool_search.py --csv collection/moxfield_haves_X.csv \
      --colors RGW --regex "create[s]? .*token"
  python scripts/pool_search.py --csv ... --colors RGW --regex "\\+1/\\+1 counter" --type creature

Color identity: a card is INCLUDED if its color identity is a subset of --colors
(colorless always qualifies). Legality: only Commander-legal cards are shown.
"""
import argparse
import csv
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
DATA = ROOT / "collection" / "oracle-cards.json"


def owned_names(csv_path):
    names = {}
    with open(csv_path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            n = row["Name"].strip()
            try:
                c = int(row["Count"])
            except (ValueError, KeyError):
                c = 1
            names[n] = names.get(n, 0) + c
            # index the front face of DFC/split names too
            if " // " in n:
                front = n.split(" // ")[0].strip()
                names.setdefault(front, 0)
                names[front] += c
    return names


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", required=True)
    ap.add_argument("--colors", default="WUBRG", help="allowed color identity letters, e.g. RGW")
    ap.add_argument("--regex", default="", help="case-insensitive regex over oracle text")
    ap.add_argument("--type", default="", help="substring that must appear in the type line (lowercased)")
    ap.add_argument("--max-cmc", type=float, default=99.0)
    ap.add_argument("--exclude", default="", help="regex; cards whose oracle matches are dropped")
    ap.add_argument("--names-only", action="store_true")
    args = ap.parse_args()

    allowed = set(args.colors.upper())
    pat = re.compile(args.regex, re.I) if args.regex else None
    expat = re.compile(args.exclude, re.I) if args.exclude else None

    owned = owned_names(args.csv)
    with open(DATA, encoding="utf-8") as f:
        cards = json.load(f)
    by_name = {}
    for c in cards:
        by_name.setdefault(c["name"], c)
        # also index each face name
        for face in c.get("card_faces", []) or []:
            by_name.setdefault(face["name"], c)

    seen = set()
    hits = []
    for name in owned:
        card = by_name.get(name)
        if not card:
            continue
        oid = card.get("oracle_id")
        if oid in seen:
            continue
        if card.get("legalities", {}).get("commander") != "legal":
            continue
        ci = set(card.get("color_identity", []))
        if not ci <= allowed:
            continue
        if card.get("cmc", 0) > args.max_cmc:
            continue
        # assemble oracle text (handle DFC)
        txt = card.get("oracle_text", "")
        if not txt and card.get("card_faces"):
            txt = "\n".join(fc.get("oracle_text", "") for fc in card["card_faces"])
        tl = card.get("type_line", "")
        if not tl and card.get("card_faces"):
            tl = " // ".join(fc.get("type_line", "") for fc in card["card_faces"])
        if args.type and args.type.lower() not in tl.lower():
            continue
        if pat and not pat.search(txt):
            continue
        if expat and expat.search(txt):
            continue
        seen.add(oid)
        hits.append((card.get("cmc", 0), card["name"], tl, txt, owned[name]))

    hits.sort(key=lambda h: (h[0], h[1]))
    print(f"# {len(hits)} owned cards | colors<={args.colors} | regex={args.regex!r} | type~{args.type!r}\n")
    for cmc, name, tl, txt, cnt in hits:
        if args.names_only:
            print(name)
            continue
        snippet = txt.replace("\n", " ")
        print(f"- {name}  [{cmc:g}] {tl}  (x{cnt})")
        print(f"    {snippet}")


if __name__ == "__main__":
    main()
