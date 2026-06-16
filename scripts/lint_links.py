#!/usr/bin/env python3
"""lint_links.py — flag broken intra-repo file references in the markdown corpus.

The repo is markdown-first and cross-links heavily (decklists, Summaries, proposals,
labs, analysis docs). When a `.txt` is re-dated, a candidate is consumed, a moxfield
CSV is rotated out, or a lab is renamed, the docs that named the old path go stale.
`validate.py` checks decks and `clock_check.py` checks clock citations; this checks
that the *paths* docs reference still resolve.

WHAT IT CHECKS (two passes over every *.md outside _sync_drop/):
  BROKEN path links   slash-bearing refs (`decks/foo.txt`, `scripts/bar.py`,
                      markdown `[x](analysis/y.md)`) that resolve to no file.
  MISSING bare refs   bare filenames (`foo_clock_lab.py`, `bar.txt`) whose basename
                      exists nowhere in the repo — catches references to a lab or
                      list that was never built / was deleted.

Findings are bucketed LIVE vs [arch] (archive/ is a frozen historical record, so
its dangling refs are expected and low-priority). Known non-repo references are
filtered out: memory files (`project_*.md` / `feedback_*.md` live in ~/.claude),
the external DeckSafe builder ($DECKSAFE_REPO), and glob/template fragments
(`*.txt`, `_Summary.md`, `[Deck_Name]_...`).

A LINT, NOT A GATE (same stance as clock_check): the path heuristics are fuzzy, so
bare-name misses are warnings. `--strict` exits non-zero on any LIVE broken
slash-path link (the high-confidence class) for CI.

Usage
    python scripts/lint_links.py            # report
    python scripts/lint_links.py --strict   # exit 1 on a LIVE broken path link
"""
import argparse
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXT = (".md", ".txt", ".py", ".json", ".xlsx", ".csv", ".jsonl")
# tokens that mark a glob/placeholder, not a real path
BAD = ("*", "<", ">", "[", "]", "...", "YYYY", "kebab", "$", "Deck_Name")
# bare filenames that legitimately live outside the repo
IGNORE_BARE = re.compile(r"^(project|feedback|reference)_.*\.md$"   # ~/.claude memory files
                         r"|^deck_safe_collection_builder\.py$")    # $DECKSAFE_REPO

for _s in (sys.stdout, sys.stderr):
    if hasattr(_s, "reconfigure"):
        try:
            _s.reconfigure(encoding="utf-8", errors="replace")
        except (ValueError, OSError):
            pass

MDLINK = re.compile(r"\]\(([^)]+)\)")
TICK = re.compile(r"`([^`]+)`")


def clean_token(s):
    parts = s.strip().strip("`").split()        # first whitespace token (drop command args)
    return parts[0].rstrip(").,;:'\"") if parts else ""


def as_path(s):                                 # slash-bearing real path ref
    s = clean_token(s)
    if not s or s.startswith(("http", "#", "mailto:")):
        return None
    if any(b in s for b in BAD):
        return None
    return s if ("/" in s and s.endswith(EXT)) else None


def as_bare(s):                                 # bare filename (no slash), basename-checkable
    s = clean_token(s)
    if not s or "/" in s or not s.endswith(EXT):
        return None
    if s.startswith((".", "_")):                # pure type/suffix fragment ('.txt', '_Summary.md')
        return None
    if any(b in s for b in BAD) or IGNORE_BARE.match(s):
        return None
    return s


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--strict", action="store_true",
                    help="exit 1 on any LIVE broken slash-path link")
    args = ap.parse_args()

    md_files = [p for p in ROOT.rglob("*.md") if "_sync_drop" not in p.parts]
    all_basenames = {p.name for p in ROOT.rglob("*")
                     if p.is_file() and "_sync_drop" not in p.parts}

    def resolves(ref, src):
        ref = ref.split("#")[0]
        if (ROOT / ref).exists() or (src.parent / ref).exists():
            return True
        return os.path.basename(ref) in all_basenames

    broken_path, missing_bare = [], []
    for f in md_files:
        rel = str(f.relative_to(ROOT))
        arc = rel.startswith("archive")
        txt = f.read_text(encoding="utf-8", errors="replace")
        toks = [m.group(1) for m in MDLINK.finditer(txt)] + \
               [m.group(1) for m in TICK.finditer(txt)]
        paths = {p for p in (as_path(t) for t in toks) if p}
        bares = {b for b in (as_bare(t) for t in toks) if b}
        for r in sorted(paths):
            if not resolves(r, f):
                broken_path.append((arc, rel, r))
        for b in sorted(bares):
            if os.path.basename(b) not in all_basenames:
                missing_bare.append((arc, rel, b))

    def show(title, rows):
        live = sorted(r for r in rows if not r[0])
        arch = sorted(r for r in rows if r[0])
        print(f"\n## {title}: {len(live)} live + {len(arch)} archive")
        for _, src, r in live:
            print(f"  [LIVE] {src}  ->  {r}")
        for _, src, r in arch:
            print(f"  [arch] {src}  ->  {r}")

    print(f"lint_links — scanned {len(md_files)} markdown files; "
          f"{len(all_basenames)} repo files")
    show("BROKEN path links", broken_path)
    show("MISSING bare-filename refs", missing_bare)

    live_broken = sum(1 for r in broken_path if not r[0])
    print(f"\n=== {live_broken} live broken path links · "
          f"{sum(1 for r in missing_bare if not r[0])} live missing bare refs "
          f"({len(broken_path)+len(missing_bare)} total incl. archive) ===")
    return 1 if (args.strict and live_broken) else 0


if __name__ == "__main__":
    sys.exit(main())
