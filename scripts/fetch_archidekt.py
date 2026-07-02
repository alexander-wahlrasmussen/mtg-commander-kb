#!/usr/bin/env python3
"""fetch_archidekt.py — pull the archenemy's PUBLIC Archidekt decks (Backlog #13 Phase 1).

The pod opponent's profile is public but PARTIAL: several key decks (current Acererak,
Hidetsugu&Kairi, Kenrith, Kinnan) are missing and the Ur-Dragon is half-assembled. What IS
there still constrains Phase 1 hard: his real card pool, build style, and the exact lists
for some decks we've lost to. This fetches the profile + individual decks into `opponents/`
(NEW folder — opponent lists must NEVER live in `decks/`, which the DeckSafe collection
builder reads as OUR demand).

Usage:
  python scripts/fetch_archidekt.py --owner nedor              # list his public decks
  python scripts/fetch_archidekt.py --deck 13758988            # print one deck
  python scripts/fetch_archidekt.py --deck 13758988 --save     # -> opponents/ (+ raw JSON)

Output format matches the repo's decklists ("1 Card Name" lines) with a comment header
(source URL, updatedAt, commander) so an opponent clock lab can pin the file the same way
the roster labs pin dated lists. Cards in maybeboard/sideboard-style categories
(includedInDeck=False) are EXCLUDED; commanders are flagged from the Commander category.

Honesty rules carried from the writeup: a fetched list is his REAL list as-of updatedAt
(cite it); anything we fill in ourselves later is PROXY and flagged in the filename.
"""
import argparse
import json
import re
import sys
import urllib.request
from datetime import date
from pathlib import Path

ROOT = Path(__file__).parent.parent
OUT = ROOT / "opponents"
API = "https://archidekt.com/api"
UA = {"User-Agent": "Mozilla/5.0 (compatible; mtg-commander-kb; personal pod analysis)"}

for _s in (sys.stdout, sys.stderr):
    if hasattr(_s, "reconfigure"):
        try:
            _s.reconfigure(encoding="utf-8", errors="replace")
        except (ValueError, OSError):
            pass


def get_json(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def list_owner(owner):
    """His public decks, newest-updated first. Tries the v3 search endpoint the site uses,
    falls back to the plain one — Archidekt's API is unversioned-in-practice, so probe."""
    for url in (f"{API}/decks/v3/?ownerUsername={owner}&orderBy=-updatedAt&pageSize=48",
                f"{API}/decks/?ownerUsername={owner}&orderBy=-updatedAt&pageSize=48"):
        try:
            j = get_json(url)
        except Exception as e:                                   # noqa: BLE001
            print(f"  probe {url.split('?')[0]} -> {e}")
            continue
        results = j.get("results", j if isinstance(j, list) else [])
        if results:
            return results
    return []


def fetch_deck(deck_id):
    return get_json(f"{API}/decks/{deck_id}/")


def normalise(j):
    """-> (meta, commanders, mainboard [(qty, name)]) with maybeboard categories excluded."""
    included = {c["name"]: c.get("includedInDeck", True) for c in j.get("categories", [])}
    commanders, main = [], []
    for c in j.get("cards", []):
        cats = c.get("categories") or []
        if any(included.get(cat) is False for cat in cats):
            continue                                            # maybeboard / considering
        name = c["card"]["oracleCard"]["name"]
        qty = c.get("quantity", 1)
        if "Commander" in cats:
            commanders.append(name)
        else:
            main.append((qty, name))
    main.sort(key=lambda t: t[1])
    meta = dict(id=j.get("id"), name=j.get("name"), updatedAt=(j.get("updatedAt") or "")[:10],
                fmt=j.get("format"), size=sum(q for q, _ in main) + len(commanders))
    return meta, sorted(commanders), main


def slugify(name):
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", name.lower())).strip("-")


def save_deck(j):
    meta, commanders, main = normalise(j)
    OUT.mkdir(exist_ok=True)
    (OUT / "raw").mkdir(exist_ok=True)
    raw = OUT / "raw" / f"archidekt-{meta['id']}.json"
    raw.write_text(json.dumps(j, indent=1), encoding="utf-8")
    stem = f"{slugify(meta['name'])}-archidekt-{meta['updatedAt'].replace('-', '')}"
    txt = OUT / f"{stem}.txt"
    lines = [f"# {meta['name']} — nedor, archidekt.com/decks/{meta['id']} "
             f"(updated {meta['updatedAt']}, fetched {date.today()})",
             f"# Commander: {' / '.join(commanders) or 'UNKNOWN'}",
             f"# {meta['size']} cards as listed — his REAL list as-of updatedAt, NOT a proxy"]
    lines += [f"{q} {n}" for q, n in [(1, c) for c in commanders] + main]
    txt.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  saved {txt.relative_to(ROOT)}  ({meta['size']} cards)  + raw JSON")
    return txt


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--owner", help="list this user's public decks")
    ap.add_argument("--deck", type=int, nargs="*", help="deck id(s) to fetch")
    ap.add_argument("--save", action="store_true", help="write opponents/<slug>.txt + raw JSON")
    args = ap.parse_args()

    if args.owner:
        decks = list_owner(args.owner)
        print(f"# {args.owner} — {len(decks)} public decks (newest first)\n")
        for d in decks:
            upd = (d.get("updatedAt") or "")[:10]
            fmt = d.get("format", "?")
            print(f"  {d['id']:>9}  {upd}  fmt={fmt:>2}  {d.get('name','?')}")
    for did in args.deck or []:
        j = fetch_deck(did)
        meta, commanders, main = normalise(j)
        print(f"\n# {meta['name']} (archidekt {meta['id']}, updated {meta['updatedAt']}) — "
              f"{meta['size']} cards\n# Commander: {' / '.join(commanders) or 'UNKNOWN'}")
        if args.save:
            save_deck(j)
        else:
            for q, n in main:
                print(f"{q} {n}")


if __name__ == "__main__":
    main()
