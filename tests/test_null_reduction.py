"""Tier-2 NULL-REDUCTION differential test (Backlog.md #9).

An overlay lab must, at its identity setting, reproduce the lab it overlays
*exactly* — otherwise its delta isn't measuring the overlay, it's measuring a
bug. We already check this by hand ("`interaction_meta_lab --tax 0` reproduces
`self_meta_lab` bit-for-bit" — Backlog #6). This makes it a CI test, so the next
overlay can't silently break the null.

This is a differential/metamorphic test: it asserts a *relationship between two
scripts*, not an absolute number, so it needs no golden snapshot and no Scryfall
bulk (both labs race table CDFs from analysis/pod_gauntlet_clocks.json). It runs
in the fast `tests` job.

The contract: at `--tax 0` the interaction overlay consumes NO rng on the
close (it short-circuits before the tax draw), so with the same seed + trials
its P(win) per deck is identical to self_meta's — and its own Δ (INTER - WIN(sm))
is +0 for every deck.
"""
import re
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"

# Determinism makes the equality hold at any (seed, trials); keep trials low for
# speed. Both labs default to self_meta's SEED; pass an explicit one so a future
# default change can't quietly desync the two halves of the test.
SEED = 4242
TRIALS = 3000

# A roster row: leading rank, deck name, then the table-clock token (Tn / >Tn).
_ROW = re.compile(r"^\s*\d+\s+(.+?)\s+>?T\d")
_PCT = re.compile(r"(\d+)%")


def _run(script, *args):
    out = subprocess.run(
        [sys.executable, str(SCRIPTS / script), "--trials", str(TRIALS),
         "--seed", str(SEED), *args],
        capture_output=True, text=True, timeout=120, cwd=str(SCRIPTS.parent))
    assert out.returncode == 0, f"{script} failed:\n{out.stderr}"
    return out.stdout


def _rows(text):
    """{deck name -> [percent ints on its row, left-to-right]}."""
    rows = {}
    for ln in text.splitlines():
        m = _ROW.match(ln)
        if not m:
            continue
        pcts = [int(x) for x in _PCT.findall(ln)]
        if pcts:
            rows[m.group(1).strip()] = pcts
    return rows


@pytest.fixture(scope="module")
def labs():
    sm = _rows(_run("self_meta_lab.py"))
    # --tax 0 is the identity setting; only the main table is needed, but the
    # script always prints the sweep too — _rows just reads the first table.
    inter = _rows(_run("interaction_meta_lab.py", "--tax", "0"))
    assert sm and inter, "parsed no rows from one of the labs"
    return sm, inter


def test_same_roster(labs):
    """Both labs cover the identical deck set (parity is part of the contract —
    self_meta filters to pods it can race; interaction must match)."""
    sm, inter = labs
    assert set(sm) == set(inter), (
        f"roster mismatch: only in self_meta={set(sm) - set(inter)}, "
        f"only in interaction={set(inter) - set(sm)}")


def test_interaction_delta_is_zero_at_tax0(labs):
    """REGRESSION (Backlog #6 null reduction): at TAX=0 every deck's
    WIN(sm) column == INTER column on its own row (Δ = +0)."""
    _, inter = labs
    for name, pcts in inter.items():
        assert len(pcts) >= 2, f"{name}: too few percents to read WIN(sm)/INTER"
        win_sm, inter_win = pcts[-2], pcts[-1]
        assert win_sm == inter_win, (
            f"{name}: TAX=0 not a null reduction — WIN(sm)={win_sm} != INTER={inter_win}")


def test_interaction_reproduces_self_meta(labs):
    """The cross-script bit-for-bit check: self_meta's WIN (last % on its row)
    == interaction's INTER at TAX=0 (last % on its row), per deck."""
    sm, inter = labs
    mismatches = {n: (sm[n][-1], inter[n][-1])
                  for n in sm if sm[n][-1] != inter[n][-1]}
    assert not mismatches, (
        "interaction --tax 0 diverged from self_meta (deck: self_meta_WIN vs "
        f"interaction_INTER): {mismatches}")
