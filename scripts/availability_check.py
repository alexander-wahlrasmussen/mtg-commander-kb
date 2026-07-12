"""Check a candidate decklist against collection ownership and deployed decks.

For each card in the candidate list, reports:
  - owned count (Moxfield haves CSV; proxy copies count as owned — real-vs-proxy
    is display-only, never an availability distinction)
  - which active deck .txt files currently run it
  - whether every owned copy is locked inside a protected deck

Usage:
  python scripts/availability_check.py proposals/witherbloom-balancer-v2b-20260607.txt \
      --csv collection/moxfield_haves_2026-06-07-1031Z.csv \
      --protected lightning-war calamity-tax the-grand-design the-genome-project \
      --reserve "Exsanguinate" --reserve "Sheoldred, the Apocalypse" \
      --exclude-deck the-loam-cycle
"""
import argparse
import csv
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LINE_RE = re.compile(r"^\s*(\d+)\s+(.+?)\s*$")


def norm(name: str) -> str:
    # Match on front face for DFC/split names, case-insensitive
    return name.split("//")[0].strip().lower()


def read_decklist(path: Path) -> dict:
    cards = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        m = LINE_RE.match(line)
        if m:
            cards[norm(m.group(2))] = cards.get(norm(m.group(2)), 0) + int(m.group(1))
    return cards


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("candidate")
    ap.add_argument("--csv", required=True)
    ap.add_argument("--deck-dir", default="decks")
    ap.add_argument("--protected", nargs="*", default=[],
                    help="deck filename prefixes whose cards may not be taken")
    ap.add_argument("--reserve", action="append", default=[],
                    help="extra card names reserved (e.g. pending swap adds to a protected deck)")
    ap.add_argument("--exclude-deck", nargs="*", default=[],
                    help="deck prefixes to ignore as donors (e.g. dismantled decks)")
    args = ap.parse_args()

    candidate = read_decklist(ROOT / args.candidate)

    owned = defaultdict(int)
    proxy = defaultdict(int)
    with open(ROOT / args.csv, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            key = norm(row["Name"])
            n = int(row["Count"])
            if row.get("Proxy", "False") == "True":
                proxy[key] += n
            else:
                owned[key] += n

    deck_files = sorted((ROOT / args.deck_dir).glob("*.txt"))
    deployments = defaultdict(list)  # card -> [(deckname, count)]
    for df in deck_files:
        stem = df.stem
        if any(stem.startswith(p) for p in args.exclude_deck):
            continue
        dl = read_decklist(df)
        for card, n in dl.items():
            deployments[card].append((stem, n))

    reserved = {norm(r) for r in args.reserve}

    def is_protected(deckstem: str) -> bool:
        return any(deckstem.startswith(p) for p in args.protected)

    rows = []
    for card in candidate:
        own, prox = owned[card], proxy[card]
        # Proxy copies tagged in the collection ARE owned copies (user rule,
        # confirmed 2026-07-12) — one pool, no real-vs-proxy status distinction.
        total = own + prox
        deps = deployments.get(card, [])
        prot_used = sum(n for d, n in deps if is_protected(d))
        free_deps = [(d, n) for d, n in deps if not is_protected(d)]
        if card in reserved:
            prot_used += 1
        available = total - prot_used  # copies not locked in protected decks
        if total == 0:
            status = "UNOWNED"
        elif available <= 0:
            status = "LOCKED (protected)"
        elif free_deps:
            status = "DONOR PULL"
        else:
            status = "FREE"
        rows.append((status, card, own, prox,
                     "; ".join(f"{d} x{n}" for d, n in deps) or "-",
                     "RESERVED" if card in reserved else ""))

    order = {"UNOWNED": 0, "LOCKED (protected)": 1, "DONOR PULL": 2, "FREE": 3}
    rows.sort(key=lambda r: (order[r[0]], r[1]))
    counts = defaultdict(int)
    for r in rows:
        counts[r[0]] += 1
        print(f"{r[0]:<20} {r[1]:<32} own={r[2]} proxy={r[3]:<2} {r[5]:<9} decks: {r[4]}")
    print("\nSummary:", dict(counts), f"(of {len(candidate)} unique cards)")


if __name__ == "__main__":
    sys.exit(main())
