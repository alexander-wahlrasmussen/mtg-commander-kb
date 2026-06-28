"""Tests for validate.lint_summary_structure — the canonical Summary-schema guard.

Hermetic: writes synthetic Summary files to a tmp dir and lints them (no repo files, no bulk).
Pins the schema the 2026-06-28 harmonization established so the old heading variants can't drift
back in unflagged.
"""
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def _load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


val = _load("validate")

CANONICAL = """# Test Deck

## What the Deck Does
It does the thing.

## Kill Lines
**Line 1 — Win:** kill.

## Conversion Check — 17/20 (audited 2026-06-28)
axes.

## Don't-Miss Rulings
- **Card** — gotcha.

## Decklist (100 cards)
### Commander (1)
- X
"""


def _write(tmp_path, name, text):
    p = tmp_path / name
    p.write_text(text, encoding="utf-8")
    return p


def test_canonical_summary_passes(tmp_path):
    p = _write(tmp_path, "Good_Summary.md", CANONICAL)
    assert val.lint_summary_structure([p]) == []


def test_non_canonical_kill_lines_heading_flagged(tmp_path):
    p = _write(tmp_path, "Bad_Summary.md", CANONICAL.replace("## Kill Lines", "## Closing Lines"))
    issues = val.lint_summary_structure([p])[0][1]
    assert any("non-canonical '## Closing Lines'" in i and "Kill Lines" in i for i in issues)
    assert any("missing required '## Kill Lines'" in i for i in issues)


def test_core_loop_overview_variant_flagged(tmp_path):
    p = _write(tmp_path, "Bad_Summary.md",
               CANONICAL.replace("## What the Deck Does", "## Core Loop"))
    issues = val.lint_summary_structure([p])[0][1]
    assert any("Core Loop" in i and "What the Deck Does" in i for i in issues)


def test_conversion_check_breakdown_variant_flagged(tmp_path):
    p = _write(tmp_path, "Bad_Summary.md",
               CANONICAL.replace("## Conversion Check — 17/20 (audited 2026-06-28)",
                                 "## Conversion Check Breakdown"))
    issues = val.lint_summary_structure([p])[0][1]
    assert any("Conversion Check Breakdown" in i for i in issues)


def test_missing_rulings_flagged(tmp_path):
    text = CANONICAL.replace("## Don't-Miss Rulings\n- **Card** — gotcha.\n", "")
    p = _write(tmp_path, "Bad_Summary.md", text)
    issues = val.lint_summary_structure([p])[0][1]
    assert any("missing required '## Don't-Miss Rulings'" in i for i in issues)


def test_h3_kill_lines_flagged(tmp_path):
    text = CANONICAL.replace("## Kill Lines\n**Line 1 — Win:** kill.\n", "### Kill Lines\nstuff.\n")
    p = _write(tmp_path, "Bad_Summary.md", text)
    issues = val.lint_summary_structure([p])[0][1]
    assert any("### Kill Lines" in i and "top-level" in i for i in issues)


def test_non_summary_files_skipped(tmp_path):
    p = _write(tmp_path, "PROP_something.md", "# Proposal\n## Random Heading\n")
    assert val.lint_summary_structure([p]) == []   # only *_Summary.md is linted
