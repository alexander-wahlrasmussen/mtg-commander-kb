#!/usr/bin/env python3
"""
update_scryfall_data.py — download the latest Scryfall oracle-cards and rulings bulk data.

Usage:
    python scripts/update_scryfall_data.py

Downloads to:
    collection/oracle-cards.json
    collection/rulings.json
Overwrites existing files in place.
"""

import json
import sys
import urllib.request
from pathlib import Path

BULK_DATA_API = "https://api.scryfall.com/bulk-data"
COLLECTION = Path(__file__).parent.parent / "collection"
HEADERS = {"User-Agent": "mtg-commander-kb/1.0", "Accept": "application/json"}

TARGETS = {
    "oracle_cards": COLLECTION / "oracle-cards.json",
    "rulings":      COLLECTION / "rulings.json",
}


def fetch_json(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())


def find_uris(bulk_data):
    uris = {}
    for entry in bulk_data.get("data", []):
        t = entry.get("type")
        if t in TARGETS:
            uris[t] = (entry["download_uri"], entry.get("size", 0))
    missing = set(TARGETS) - set(uris)
    if missing:
        sys.exit(f"ERROR: Could not find bulk data entries for: {missing}")
    return uris


def download_with_progress(url, dest):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req) as resp:
        total = int(resp.headers.get("Content-Length", 0))
        downloaded = 0
        chunk = 1024 * 1024
        with dest.open("wb") as f:
            while True:
                data = resp.read(chunk)
                if not data:
                    break
                f.write(data)
                downloaded += len(data)
                if total:
                    pct = downloaded / total * 100
                    mb = downloaded / 1024 / 1024
                    print(f"\r  {mb:.1f} MB / {total/1024/1024:.1f} MB ({pct:.0f}%)", end="", flush=True)
    print()


def main():
    print("Fetching Scryfall bulk data index...")
    bulk_data = fetch_json(BULK_DATA_API)
    uris = find_uris(bulk_data)

    COLLECTION.mkdir(parents=True, exist_ok=True)

    for bulk_type, dest in TARGETS.items():
        uri, size_bytes = uris[bulk_type]
        size_mb = size_bytes / 1024 / 1024
        print(f"Downloading {bulk_type} ({size_mb:.0f} MB) → {dest.name}")
        download_with_progress(uri, dest)

        print("Verifying...")
        with dest.open(encoding="utf-8") as f:
            data = json.load(f)
        print(f"OK — {len(data):,} entries in {dest.name}\n")


if __name__ == "__main__":
    main()
