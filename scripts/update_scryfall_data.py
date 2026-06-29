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
    """Stream the download to a sibling .part file and return its path. The caller
    verifies it and atomically replaces `dest` only on success, so an interrupted or
    truncated download can never clobber the existing good copy — these bulk files are
    gitignored, so a corrupt overwrite has no checkout to recover from."""
    tmp = dest.with_name(dest.name + ".part")
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req) as resp:
            total = int(resp.headers.get("Content-Length", 0))
            downloaded = 0
            chunk = 1024 * 1024
            with tmp.open("wb") as f:
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
    except BaseException:
        tmp.unlink(missing_ok=True)           # don't leave a partial behind
        raise
    print()
    if total and downloaded != total:         # silent truncation (EOF before Content-Length)
        tmp.unlink(missing_ok=True)
        sys.exit(f"ERROR: truncated download ({downloaded:,} of {total:,} bytes) for {dest.name}; "
                 f"kept the existing file.")
    return tmp


def main():
    print("Fetching Scryfall bulk data index...")
    bulk_data = fetch_json(BULK_DATA_API)
    uris = find_uris(bulk_data)

    COLLECTION.mkdir(parents=True, exist_ok=True)

    for bulk_type, dest in TARGETS.items():
        uri, size_bytes = uris[bulk_type]
        size_mb = size_bytes / 1024 / 1024
        print(f"Downloading {bulk_type} ({size_mb:.0f} MB) → {dest.name}")
        tmp = download_with_progress(uri, dest)

        print("Verifying...")
        try:
            with tmp.open(encoding="utf-8") as f:
                data = json.load(f)
        except (OSError, ValueError) as e:        # ValueError covers json.JSONDecodeError
            tmp.unlink(missing_ok=True)
            sys.exit(f"ERROR: downloaded {dest.name} is not valid JSON ({e}); kept the existing file.")
        tmp.replace(dest)                          # atomic swap only after verification
        print(f"OK — {len(data):,} entries in {dest.name}\n")


if __name__ == "__main__":
    main()
