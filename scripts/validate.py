#!/usr/bin/env python3
"""
validate.py — read-only linter for the Commander KB hard rules.

Reports violations of the mechanically-checkable rules in CLAUDE.md and changes
nothing. Safe to wire into a pre-commit hook once the output is trusted.

Checks
  1. Deck size      — every decklist is exactly 100 (99 library + 1 commander).
  2. Game Changers  — no deck runs more than 3, cross-referenced to the
                      'Full List' section of reference/REF_Game_Changers_List.md
                      (the 'Cards Removed' section is deliberately excluded).
  3. Filename unique — no basename collisions in the sync set (the sync script
                      flattens decks/ + collection/ + two top-level files).
  4. Clock claims   — every 'Tx-y' kill-window in a Summary/proposal cites a
                      'lab YYYY-MM-DD' or carries an explicit '(unverified)' flag.

Reuses the canonical decklist parser (deck_sim.parse_deck), the reskin-alias
table, and the sync script's own collision detector, so the linter agrees with
the rest of the tooling rather than re-deriving any of it.

Usage
    python scripts/validate.py                # all checks, human report
    python scripts/validate.py --all-docs     # widen clock lint to analysis/ + campaigns/ + matrix
    python scripts/validate.py --no-oracle    # skip oracle load (size + GC still run; unresolved-name check skipped)

Exit code: 1 if any ERROR, else 0.
"""

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from deck_sim import (  # noqa: E402
    ROOT, ORACLE, parse_deck, load_reskin_aliases, load_oracle_index,
)
from sync_to_project import collect_candidate_files, detect_collisions  # noqa: E402

# Windows consoles default to cp1252; the docs we echo contain en-dashes and
# minus signs (turn ranges like "T7-9"). Force UTF-8 so echoing arbitrary lines
# never crashes the linter mid-report.
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        try:
            _stream.reconfigure(encoding="utf-8", errors="replace")
        except (ValueError, OSError):
            pass

GC_DOC = ROOT / "reference" / "REF_Game_Changers_List.md"
MAX_GC = 3
DECK_SIZE = 100

ERROR, WARN, OK = "ERROR", "WARN", "OK"


# ---------------------------------------------------------------------------
# Game Changer list
# ---------------------------------------------------------------------------

def load_game_changers(path=GC_DOC):
    """Return {lower_name: proper_name} parsed from the 'Full List (Alphabetical)'
    section only.

    The 'Cards Removed (No Longer GCs)' section is excluded on purpose: a grep
    hit there is not a current GC (REF_Domain_Principles — Tooth and Nail, etc.).
    """
    if not path.exists():
        sys.exit(f"ERROR: {path} not found")
    names = {}
    in_full_list = False
    entry = re.compile(r"^\s*\d+\.\s+(.+?)\s*$")
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.rstrip()
        if line.startswith("## "):
            in_full_list = line.lower().startswith("## full list")
            continue
        if in_full_list:
            m = entry.match(line)
            if m:
                proper = m.group(1).strip()
                names[proper.lower()] = proper
    return names


# ---------------------------------------------------------------------------
# Deck checks
# ---------------------------------------------------------------------------

def check_deck(path, index, aliases, gc_names, oracle_loaded):
    """Return (total_cards, commander, gc_hits, issues) for one decklist."""
    library, commander, diag = parse_deck(path, index, aliases)
    total = len(library) + (1 if commander else 0)
    issues = []

    # 1. deck size — library is the shuffled 99; commander pulled to the zone.
    if commander is None:
        issues.append((WARN, f"commander not in deck_sim.COMMANDERS registry — "
                              f"size unverifiable (library={len(library)})"))
    elif total != DECK_SIZE:
        issues.append((ERROR, f"deck size {total} ({len(library)} library + commander), "
                              f"expected {DECK_SIZE}"))

    # 2. Game Changers — resolve reskins to canonical names before matching.
    gc_hits = {}
    pool = [n for n, _ in library] + ([commander] if commander else [])
    for n in pool:
        canon = aliases.get(n.lower(), n).lower()
        if canon in gc_names:
            gc_hits[canon] = gc_names[canon]
    if len(gc_hits) > MAX_GC:
        issues.append((ERROR, f"{len(gc_hits)} Game Changers (max {MAX_GC}): "
                              + ", ".join(sorted(gc_hits.values()))))

    # 3. unresolved card names — only meaningful when oracle data is loaded.
    if oracle_loaded and diag["unresolved"]:
        shown = ", ".join(diag["unresolved"][:6])
        more = f" (+{len(diag['unresolved']) - 6} more)" if len(diag["unresolved"]) > 6 else ""
        issues.append((WARN, f"{len(diag['unresolved'])} unresolved card name(s): {shown}{more}"))

    return total, commander, gc_hits, issues


def report_deck(path, total, commander, gc_hits, issues):
    sev = (ERROR if any(s == ERROR for s, _ in issues)
           else WARN if any(s == WARN for s, _ in issues)
           else OK)
    print(f"  [{sev:5}] {path.name}  ({total} cards | GC {len(gc_hits)}/{MAX_GC} | {commander or '?'})")
    for s, m in issues:
        print(f"           {s}: {m}")


# ---------------------------------------------------------------------------
# Clock-claim citation lint
# ---------------------------------------------------------------------------

TURN_RE = re.compile(r"\bT\d{1,2}\b")
# A doc is "lab-backed" if it references a lab anywhere: the dated
# "(lab YYYY-MM-DD)" form, a *_clock_lab/*_speed_lab/deck_sim script, a trial
# count, or an explicit "unverified" flag.
CITE_RE = re.compile(
    r"lab\s+\d{4}-\d{2}-\d{2}|_(?:clock|speed)_lab|deck_sim|\b\d+k?\s+trials\b|unverified",
    re.I,
)
CTX_RE = re.compile(r"\b(decap|table|clock|lethal|goldfish|kill)\b", re.I)


def summary_and_proposal_docs(all_docs=False):
    docs = sorted((ROOT / "decks").glob("*_Summary.md"))
    docs += sorted((ROOT / "proposals").glob("*.md"))
    if all_docs:
        docs += sorted((ROOT / "analysis").glob("*.md"))
        docs += sorted((ROOT / "campaigns").glob("*.md"))
        docs += [ROOT / "Pod_Matchup_Matrix.md"]
    return [p for p in docs if p.exists() and p.name != "README.md"]


def lint_clock_claims(paths):
    """Flag docs that state a turn-window kill claim but carry NO lab citation
    anywhere in the doc.

    CLAUDE.md requires a kill-window claim to have 'a lab backing it' or an
    explicit '(unverified)' flag — the backing can sit in a clock-lab section
    elsewhere in the doc, so the check is doc-level, not line-level. That keeps
    the lint on the real risk (a Summary/proposal that hand-waves a clock with
    zero lab evidence) instead of every prose mention of a turn number.

    Returns [(path, [(lineno, text), ...]), ...] for flagged docs only.
    """
    flagged = []
    for p in paths:
        lines = p.read_text(encoding="utf-8").splitlines()
        if any(CITE_RE.search(ln) for ln in lines):
            continue  # doc is lab-backed somewhere
        claims = [(i + 1, ln.strip()) for i, ln in enumerate(lines)
                  if TURN_RE.search(ln) and CTX_RE.search(ln)]
        if claims:
            flagged.append((p, claims))
    return flagged


# Canonical Summary section schema (the harmonized format — see templates/TPL_Deck_Summary.md).
# REQUIRED H2 sections every active deck Summary must carry, with canonical names:
CANON_REQUIRED = ("What the Deck Does", "Kill Lines", "Conversion Check",
                  "Don't-Miss Rulings", "Decklist")
# Known NON-canonical H2 heading variants (lowercased base, before any — / : / () ) -> canonical.
NONCANON_H2 = {
    "core loop": "What the Deck Does", "what the deck is trying to do": "What the Deck Does",
    "overview": "What the Deck Does", "closing lines": "Kill Lines",
    "how we end games": "Kill Lines", "how we win": "Kill Lines",
    "clock & evidence": "Kill Window", "lab results": "Kill Window",
    "conversion check assessment": "Conversion Check — N/20",
    "conversion check breakdown": "Conversion Check — N/20",
}


def lint_summary_structure(paths):
    """Flag deck Summaries that deviate from the canonical section schema — the source-side
    guard that keeps the deck pages consistent (kb_content's parser tolerates the old variants,
    this stops new ones drifting back in). Reports, per Summary: missing required H2 sections and
    known non-canonical heading variants (incl. a '### Kill Lines' that should be top-level).
    Returns [(path, [issue, ...]), ...] for flagged Summaries only."""
    flagged = []
    for p in paths:
        if not p.name.endswith("_Summary.md"):
            continue
        lines = p.read_text(encoding="utf-8").splitlines()
        h2 = [re.sub(r"^##\s+", "", l).strip() for l in lines if re.match(r"^##\s", l)]
        h2low = [h.lower() for h in h2]
        issues = []
        for req in CANON_REQUIRED:
            rl = req.lower()
            if not any(hl == rl or hl.startswith(rl + " ") or hl.startswith(rl + " —")
                       or (req == "Conversion Check" and hl.startswith("conversion check"))
                       for hl in h2low):
                issues.append(f"missing required '## {req}'")
        for h, hl in zip(h2, h2low):
            base = re.split(r"\s*[—:(]", hl)[0].strip()
            if base in NONCANON_H2:
                issues.append(f"non-canonical '## {h}' → use '## {NONCANON_H2[base]}'")
        if (any(re.match(r"^###\s+Kill Lines\s*$", l) for l in lines)
                and "kill lines" not in h2low):
            issues.append("'### Kill Lines' should be a top-level '## Kill Lines'")
        if issues:
            flagged.append((p, issues))
    return flagged


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--all-docs", action="store_true",
                    help="widen clock-claim lint to analysis/ + campaigns/ + the matrix")
    ap.add_argument("--no-oracle", action="store_true",
                    help="skip loading oracle-cards.json (size + GC still run)")
    args = ap.parse_args()

    errors = warns = 0
    aliases = load_reskin_aliases()
    gc_names = load_game_changers()
    print(f"GC list: {len(gc_names)} cards (Full List section of {GC_DOC.relative_to(ROOT)})")

    oracle_loaded = False
    index = {}
    if args.no_oracle or not ORACLE.exists():
        if not ORACLE.exists():
            print(f"NOTE: {ORACLE.relative_to(ROOT)} not present — size + GC checks "
                  f"run on names only; unresolved-name check skipped.")
    else:
        index = load_oracle_index()
        oracle_loaded = True

    def run_decks(paths, candidate=False):
        nonlocal errors, warns
        for path in paths:
            total, commander, gc_hits, issues = check_deck(
                path, index, aliases, gc_names, oracle_loaded)
            if candidate:  # candidates are WIP — downgrade hard failures to advisory
                issues = [(WARN if s == ERROR else s, m) for s, m in issues]
            report_deck(path, total, commander, gc_hits, issues)
            errors += sum(1 for s, _ in issues if s == ERROR)
            warns += sum(1 for s, _ in issues if s == WARN)

    print("\n--- Active decklists ---")
    run_decks(sorted((ROOT / "decks").glob("*.txt")))

    considering = sorted((ROOT / "decks" / "considering").glob("*.txt"))
    if considering:
        print("\n--- Candidate decklists (decks/considering/) — advisory ---")
        run_decks(considering, candidate=True)

    print("\n--- Filename uniqueness (sync set) ---")
    synced = collect_candidate_files()
    collisions = detect_collisions(synced)
    if collisions:
        for name, paths in collisions.items():
            print(f"  [ERROR] {name}")
            for p in paths:
                print(f"            - {p.relative_to(ROOT)}")
            errors += 1
    else:
        print(f"  [OK] no basename collisions among {len(synced)} synced files")

    print("\n--- Clock-claim citations (Summaries + proposals) ---")
    docs = summary_and_proposal_docs(args.all_docs)
    flagged = lint_clock_claims(docs)
    if not flagged:
        print(f"  [OK] every clock claim in {len(docs)} docs is lab-cited or flagged")
    else:
        for p, claims in flagged:
            print(f"  [WARN] {p.relative_to(ROOT)} — turn-window claim(s), no lab citation in the doc:")
            for i, line in claims[:3]:
                print(f"            L{i}: {line[:90]}")
            if len(claims) > 3:
                print(f"            ... +{len(claims) - 3} more")
            warns += 1
    print("  NOTE: this checks a citation EXISTS; `scripts/clock_check.py` checks the cited "
          "decap/table\n        turns still MATCH the lab (run `pod_gauntlet.py --refresh` first).")

    print("\n--- Summary section schema (canonical headings) ---")
    summaries = sorted((ROOT / "decks").glob("*_Summary.md"))
    drift = lint_summary_structure(summaries)
    if not drift:
        print(f"  [OK] all {len(summaries)} deck Summaries match the canonical schema "
              f"(templates/TPL_Deck_Summary.md)")
    else:
        for p, issues in drift:
            print(f"  [WARN] {p.relative_to(ROOT)}:")
            for it in issues:
                print(f"            {it}")
            warns += 1

    print(f"\n=== {errors} error(s), {warns} warning(s) ===")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
