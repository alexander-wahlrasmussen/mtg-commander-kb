#!/usr/bin/env python3
"""free_pool.py — enumerate the OWNED-AND-UNALLOCATED ("free") card pool.

Surplus-aware: FREE(card) = owned_total(real+proxy) - deployed_total(active decks).
So if you own 26 Sol Ring and 17 are in decks/*.txt, 9 are free. This is the
"what can I build right now without buying anything OR cannibalising an existing
deck" pool — a stricter, more honest question than availability_check.py's
per-card FREE/DONOR label, which flags any deployed card regardless of surplus.

Active decks = decks/*.txt (non-recursive glob, so decks/considering/ candidates
are NOT counted as deployed — they aren't built).

Proxies count as owned (user rule, 2026-07-12). Reskin aliases (REF_Reskin_Aliases)
are NOT auto-merged here — spot-check unfamiliar UB names by hand.

Examples:
  python scripts/free_pool.py --colors B
  python scripts/free_pool.py --colors B --regex "sacrifice a creature" --text
  python scripts/free_pool.py --colors B --type creature --regex "when(ever)? .*dies"
"""
import argparse
import csv
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LINE_RE = re.compile(r"^\s*(\d+)\s+(.+?)\s*$")


def norm(name: str) -> str:
    return name.split("//")[0].strip().lower()


def owned_from_csv(csv_path: Path):
    total = defaultdict(int)
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            n = int(row["Count"]) if row.get("Count", "").isdigit() else 1
            total[norm(row["Name"])] += n  # real + proxy both count
    return total


def deployed_from_decks(deck_dir: Path, exclude: Path | None = None):
    dep = defaultdict(int)
    for df in sorted(deck_dir.glob("*.txt")):        # non-recursive: skips considering/
        if exclude is not None and df.resolve() == exclude:
            continue
        for line in df.read_text(encoding="utf-8").splitlines():
            m = LINE_RE.match(line)
            if m:
                dep[norm(m.group(2))] += int(m.group(1))
    return dep


def load_oracle(path: Path):
    idx = {}
    for c in json.loads(path.read_text(encoding="utf-8")):
        for key in {norm(c["name"]), c["name"].strip().lower()}:
            idx.setdefault(key, c)
    return idx


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--colors", default="B", help="color identity ceiling, e.g. B or WB (colorless always ok)")
    ap.add_argument("--csv", help="Moxfield haves CSV (default: newest in collection/)")
    ap.add_argument("--oracle", default=str(ROOT / "collection" / "oracle-cards.json"))
    ap.add_argument("--deck-dir", default=str(ROOT / "decks"))
    ap.add_argument("--regex", help="filter on oracle text (case-insensitive)")
    ap.add_argument("--type", help="filter on type line substring (e.g. creature, land, artifact)")
    ap.add_argument("--min-free", type=int, default=1)
    ap.add_argument("--text", action="store_true", help="print oracle text")
    ap.add_argument("--basics", action="store_true", help="include basic lands")
    ap.add_argument("--check", metavar="DECKLIST",
                    help="verify every card in a decklist is free (owned-deployed >= qty); "
                         "the checked list is NOT counted as deployed")
    args = ap.parse_args()

    csv_path = Path(args.csv) if args.csv else max((ROOT / "collection").glob("moxfield_haves_*.csv"))
    owned = owned_from_csv(csv_path)
    deployed = deployed_from_decks(Path(args.deck_dir),
                                   exclude=Path(args.check).resolve() if args.check else None)
    oracle = load_oracle(Path(args.oracle))

    if args.check:
        BASIC = {"swamp", "island", "plains", "mountain", "forest", "wastes",
                 "snow-covered swamp", "snow-covered island", "snow-covered plains",
                 "snow-covered mountain", "snow-covered forest"}
        problems = 0
        for line in Path(args.check).read_text(encoding="utf-8").splitlines():
            m = LINE_RE.match(line)
            if not m:
                continue
            qty, name = int(m.group(1)), m.group(2).strip()
            key = norm(name)
            if key in BASIC:
                continue
            free = owned.get(key, 0) - deployed.get(key, 0)
            tag = "ok" if free >= qty else ("NOT-FREE" if key in owned else "UNOWNED")
            if free < qty:
                problems += 1
                print(f"  [{tag:8}] {name}: free {free} < need {qty} "
                      f"(own {owned.get(key,0)}, deployed {deployed.get(key,0)})")
        print(f"\n{'ALL FREE' if problems == 0 else str(problems)+' NOT-FREE/UNOWNED'} "
              f"(basics exempt; deployed excludes the checked list)")
        return

    ceiling = set(args.colors.upper())
    rx = re.compile(args.regex, re.I) if args.regex else None
    rows = []
    unknown = []
    for name, own in owned.items():
        free = own - deployed.get(name, 0)
        if free < args.min_free:
            continue
        card = oracle.get(name)
        if card is None:
            unknown.append((name, free))
            continue
        if card.get("legalities", {}).get("commander") != "legal":
            continue
        tl = card.get("type_line", "")
        if not args.basics and "Basic" in tl:
            continue
        ci = set(card.get("color_identity", []))
        if not ci.issubset(ceiling):
            continue
        otext = card.get("oracle_text", "")
        if "card_faces" in card and not otext:
            otext = " // ".join(f.get("oracle_text", "") for f in card["card_faces"])
        if args.type and args.type.lower() not in tl.lower():
            continue
        if rx and not rx.search(otext):
            continue
        rows.append((tl, card["name"], free, "".join(sorted(ci)) or "C", otext))

    rows.sort(key=lambda r: (r[0], r[1]))
    for tl, name, free, ci, otext in rows:
        print(f"{free:>2}x  [{ci:<4}] {name}  ::  {tl}")
        if args.text:
            print(f"        {otext.replace(chr(10), ' / ')[:300]}")
    print(f"\n{len(rows)} free cards (CI subset of {{{args.colors}}}, legal){' + basics' if args.basics else ''}"
          f"; {len(unknown)} owned names not in oracle data (stale/typo/reskin): "
          + ", ".join(n for n, _ in sorted(unknown)[:12]) + (" ..." if len(unknown) > 12 else ""))


if __name__ == "__main__":
    main()
