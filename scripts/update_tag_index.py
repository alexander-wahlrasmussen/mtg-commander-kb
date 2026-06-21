#!/usr/bin/env python3
"""
update_tag_index.py — build a local oracle-tag index from Scryfall Tagger data.

Scryfall's bulk `oracle-cards.json` does NOT carry tag data. The community
Tagger project (tagger.scryfall.com) does, and its tags are exposed through the
*official* search API via the `otag:` operator (e.g. `otag:ramp`). This script
queries one search per tag in a curated functional taxonomy, pages through the
results, and writes a compact card -> tags index keyed by oracle_id.

Usage:
    python scripts/update_tag_index.py                 # full taxonomy
    python scripts/update_tag_index.py --tags ramp,removal,tutor   # subset
    python scripts/update_tag_index.py --list          # print taxonomy and exit

Output:
    collection/oracle-tags.json   (gitignored, refreshable — like oracle-cards.json)

Consumed by card_lookup.py, which joins on each card's oracle_id.

Notes
-----
- Uses ONLY the documented search API. No auth, no scraping of the unofficial
  Tagger GraphQL endpoint.
- Tags are community-maintained: coverage is strong on staples, thinner on new
  and Universes Beyond cards. They categorize *function*, not exact wording —
  `removal` does not say destroy vs. exile. Still read the card text before
  recommending (see CLAUDE.md).
- Scryfall asks for 50-100ms between requests; we sleep 100ms.
"""

import argparse
import json
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError

COLLECTION = Path(__file__).parent.parent / "collection"
OUT_FILE = COLLECTION / "oracle-tags.json"
SEARCH_API = "https://api.scryfall.com/cards/search"
HEADERS = {"User-Agent": "mtg-commander-kb/1.0", "Accept": "application/json"}
REQUEST_DELAY = 0.1  # seconds between API calls (Scryfall asks 50-100ms)
MAX_RETRIES = 5      # on HTTP 429 (rate limited)

# Curated functional oracle-tag slugs. Every entry below was verified to return
# results from the live `otag:` search on 2026-06-21. Exact-duplicate aliases
# were dropped (board-wipe=mass-removal, blink=flicker, sac-outlet=sacrifice-outlet).
# Some tags are intentionally hierarchical (removal > spot-removal > mass-removal;
# card-advantage > draw) — keeping both lets you query broad or narrow.
TAXONOMY = [
    # interaction / removal
    "removal", "spot-removal", "mass-removal", "counterspell", "bounce",
    "protection", "fog", "graveyard-hate", "tax",
    # card flow
    "card-advantage", "draw", "cantrip", "scry", "wheel", "discard", "mill",
    # tutoring / recursion
    "tutor", "recursion", "reanimate",
    # mana
    "ramp", "mana-rock", "mana-dork", "mana-sink", "ritual",
    # tempo / engines / wins
    "sacrifice-outlet", "lifegain", "anthem", "pinger", "copy", "clone",
    "theft", "evasion", "flicker", "extra-turn", "extra-combat",
    "win-condition", "group-hug",
    # lands / counters themes
    "landfall", "lands-matter",
]


def get_json(url):
    """GET a Scryfall URL, backing off on HTTP 429. Returns parsed JSON or
    None if the search matched nothing (404)."""
    for attempt in range(MAX_RETRIES):
        req = urllib.request.Request(url, headers=HEADERS)
        try:
            with urllib.request.urlopen(req) as resp:
                return json.loads(resp.read())
        except HTTPError as e:
            if e.code == 404:  # search matched nothing
                return None
            if e.code == 429 and attempt < MAX_RETRIES - 1:
                wait = int(e.headers.get("Retry-After", 0)) or 2 ** (attempt + 1)
                print(f"\n  rate limited (429) — waiting {wait}s...", flush=True)
                time.sleep(wait)
                continue
            raise
    raise RuntimeError(f"giving up after {MAX_RETRIES} retries: {url}")


def fetch_tag(tag):
    """Return the set of oracle_ids carrying `otag:<tag>`, paging through results."""
    oracle_ids = set()
    params = urllib.parse.urlencode({
        "q": f"otag:{tag}",
        "unique": "cards",
        "order": "name",
    })
    url = f"{SEARCH_API}?{params}"
    pages = 0
    while url:
        data = get_json(url)
        if data is None:  # 404 — no results
            return oracle_ids, 0
        for card in data.get("data", []):
            oid = card.get("oracle_id")
            if oid:
                oracle_ids.add(oid)
        pages += 1
        url = data.get("next_page") if data.get("has_more") else None
        if url:
            time.sleep(REQUEST_DELAY)
    return oracle_ids, pages


def build(tags):
    by_oracle_id = {}
    tag_counts = {}
    for i, tag in enumerate(tags, 1):
        print(f"[{i}/{len(tags)}] otag:{tag} ...", end=" ", flush=True)
        oracle_ids, pages = fetch_tag(tag)
        tag_counts[tag] = len(oracle_ids)
        for oid in oracle_ids:
            by_oracle_id.setdefault(oid, []).append(tag)
        print(f"{len(oracle_ids):>5} cards ({pages} page{'s' if pages != 1 else ''})")
        time.sleep(REQUEST_DELAY)

    # Sort tags per card for stable, diff-friendly output.
    for oid in by_oracle_id:
        by_oracle_id[oid].sort()

    return {
        "fetched_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source": "https://api.scryfall.com/cards/search (otag: / Scryfall Tagger)",
        "tag_counts": dict(sorted(tag_counts.items())),
        "by_oracle_id": by_oracle_id,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--tags", help="Comma-separated subset of slugs to fetch "
                                       "(default: the full curated taxonomy)")
    parser.add_argument("--out", type=Path, default=OUT_FILE, help="Output path")
    parser.add_argument("--list", action="store_true",
                        help="Print the curated taxonomy and exit")
    args = parser.parse_args()

    if args.list:
        for t in TAXONOMY:
            print(t)
        return

    tags = [t.strip() for t in args.tags.split(",")] if args.tags else list(TAXONOMY)

    print(f"Building tag index for {len(tags)} tag(s) via Scryfall otag: search...\n")
    index = build(tags)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False)

    n_cards = len(index["by_oracle_id"])
    print(f"\nOK — {n_cards:,} cards carry >=1 tag. Wrote {args.out}")


if __name__ == "__main__":
    main()
