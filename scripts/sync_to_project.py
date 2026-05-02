#!/usr/bin/env python3
"""
sync_to_project.py — Flatten the knowledge base for Claude Project upload.

Walks the repo, copies everything eligible into _sync_drop/ as a flat folder,
and detects filename collisions. Optionally filters to just what has changed
since a given git ref.

Usage:
    python scripts/sync_to_project.py --all
    python scripts/sync_to_project.py --since HEAD~10
    python scripts/sync_to_project.py --since main
    python scripts/sync_to_project.py --dry-run

Run from anywhere; the script locates the repo root via its own path.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = REPO_ROOT / "_sync_drop"

# Folders whose contents are recursively included.
INCLUDE_DIRS = ["decks", "collection"]

# Top-level files to include explicitly.
INCLUDE_TOP_LEVEL = [
    "Deck_Index.md",
    "Collection_Master_Status.md",
]

# File extensions that are eligible for sync.
INCLUDE_EXTENSIONS = {".md", ".txt", ".csv", ".xlsx"}

# Folders to skip entirely when walking.
SKIP_DIRS = {"_sync_drop", "archive", ".git", "__pycache__", "scripts"}


# -----------------------------------------------------------------------------
# File collection
# -----------------------------------------------------------------------------

def collect_candidate_files() -> list[Path]:
    """Return every file in the repo that is eligible for sync."""
    files: list[Path] = []

    for name in INCLUDE_TOP_LEVEL:
        p = REPO_ROOT / name
        if p.exists() and p.is_file():
            files.append(p)

    for dirname in INCLUDE_DIRS:
        d = REPO_ROOT / dirname
        if not d.is_dir():
            continue
        for p in d.rglob("*"):
            if not p.is_file():
                continue
            if any(part in SKIP_DIRS for part in p.parts):
                continue
            if p.suffix.lower() in INCLUDE_EXTENSIONS:
                files.append(p)

    return files


def filter_by_git_changes(files: list[Path], since: str) -> list[Path]:
    """Return only files changed between `since` and HEAD."""
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", since, "HEAD"],
            capture_output=True,
            text=True,
            cwd=REPO_ROOT,
            check=True,
        )
    except subprocess.CalledProcessError as e:
        print(f"git diff failed: {e.stderr.strip()}", file=sys.stderr)
        sys.exit(1)

    changed_rel = {line.strip() for line in result.stdout.splitlines() if line.strip()}
    changed_abs = {(REPO_ROOT / rel).resolve() for rel in changed_rel}
    return [f for f in files if f.resolve() in changed_abs]


# -----------------------------------------------------------------------------
# Collision detection
# -----------------------------------------------------------------------------

def detect_collisions(files: list[Path]) -> dict[str, list[Path]]:
    """Group files by basename; return any group with more than one member."""
    by_name: dict[str, list[Path]] = {}
    for f in files:
        by_name.setdefault(f.name, []).append(f)
    return {name: paths for name, paths in by_name.items() if len(paths) > 1}


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--all", action="store_true", help="Sync everything eligible (default).")
    group.add_argument("--since", metavar="GIT_REF", help="Sync only files changed since this git ref.")
    parser.add_argument("--dry-run", action="store_true", help="Print the file list without copying.")
    args = parser.parse_args()

    files = collect_candidate_files()
    if args.since:
        files = filter_by_git_changes(files, args.since)

    if not files:
        print("No files to sync.")
        return 0

    collisions = detect_collisions(files)
    if collisions:
        print("ERROR: filename collisions detected:", file=sys.stderr)
        for name, paths in collisions.items():
            print(f"  {name}", file=sys.stderr)
            for p in paths:
                print(f"    - {p.relative_to(REPO_ROOT)}", file=sys.stderr)
        print("\nFix naming before syncing. See README.md > Filename integrity.", file=sys.stderr)
        return 2

    if args.dry_run:
        print(f"Would copy {len(files)} files to {OUTPUT_DIR.relative_to(REPO_ROOT)}/:")
        for f in sorted(files, key=lambda p: p.name):
            print(f"  {f.relative_to(REPO_ROOT)} -> {f.name}")
        return 0

    # Clear and populate the drop folder.
    if OUTPUT_DIR.exists():
        for p in OUTPUT_DIR.iterdir():
            if p.is_file():
                p.unlink()
    else:
        OUTPUT_DIR.mkdir()

    for f in files:
        shutil.copy2(f, OUTPUT_DIR / f.name)

    print(f"Copied {len(files)} files to {OUTPUT_DIR.relative_to(REPO_ROOT)}/")
    print("Upload the contents of that folder to your Claude Project.")
    print("Reminder: delete existing same-named files from the Project before re-uploading.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
