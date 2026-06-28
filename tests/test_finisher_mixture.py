"""Tests for the per-line finisher mixture (Backlog #11 proper-version pilot).

Two layers, matching the rest of the suite:
  HERMETIC (fast gate)  — the disabler ENGINE on synthetic per-line samples: line_survives,
                          mixture_samples (null reduction + bounded-above), curve() shape.
                          No Scryfall bulk (finisher_mixture imports cleanly without it).
  GOLDEN (bulk-gated)   — the REAL Lightning War null reduction: mixture{} == bestline_kill
                          on the same games, per game. Needs the 168 MB oracle, so it is
                          `golden`-marked and auto-skips without it (same policy as
                          test_clock_golden).

The load-bearing invariant (and the reason this consumer is safe to add UNCALIBRATED): the
disabler vector only ever REMOVES lines, so the mixture is bounded ABOVE by the harvested
best-line curve — it can model degradation, never a faster fiction. test_bounded_above pins
that; test_null_reduction_* pins that empty conditions reproduce the harvested curve.
"""
import json
from pathlib import Path

import pytest

import finisher_mixture as fm

ROOT = Path(__file__).resolve().parent.parent
BULK = ROOT / "collection" / "oracle-cards.json"

# Synthetic per-line samples for Lightning War's two real lines. The ENGINE is deck-agnostic,
# so these stand in for lw_perline_samples without touching the oracle.
SAMPLES = [
    {"burn": (10, None), "combo": (9, 9)},      # combo wins both clocks
    {"burn": (6, 12), "combo": (None, None)},   # burn only; combo bricks this game
    {"burn": (None, None), "combo": (None, None)},  # both brick
    {"burn": (8, 8), "combo": (11, 11)},        # burn wins
]


def _inf(turn):
    return float("inf") if turn is None else turn


# --- hermetic: the disabler engine -------------------------------------------------------
def test_line_survives_rule_of_law_disables_both_lw_lines():
    assert not fm.line_survives("lightning_war", "burn", ["rule_of_law"])
    assert not fm.line_survives("lightning_war", "combo", ["rule_of_law"])


def test_line_survives_graveyard_hate_disables_neither():
    # both LW lines assemble from hand — graveyard hate must NOT switch them off
    assert fm.line_survives("lightning_war", "burn", ["graveyard_hate"])
    assert fm.line_survives("lightning_war", "combo", ["graveyard_hate"])


def test_null_reduction_synthetic():
    # mixture with no conditions == per-game min over all lines (the bestline)
    mix = fm.mixture_samples("lightning_war", SAMPLES, [])
    expect = [(9, 9), (6, 12), (None, None), (8, 8)]
    assert mix == expect


def test_graveyard_hate_is_a_noop_for_lw():
    assert fm.mixture_samples("lightning_war", SAMPLES, ["graveyard_hate"]) == \
        fm.mixture_samples("lightning_war", SAMPLES, [])


def test_rule_of_law_removes_every_lw_line():
    mix = fm.mixture_samples("lightning_war", SAMPLES, ["rule_of_law"])
    assert mix == [(None, None)] * len(SAMPLES)


def test_bounded_above():
    # disabling lines can only push a clock LATER (or to never) — never earlier. For every
    # game and every pod state, mixture(cond) >= mixture({}) on both clocks (None = inf).
    base = fm.mixture_samples("lightning_war", SAMPLES, [])
    for cond in ([], ["graveyard_hate"], ["rule_of_law"], ["graveyard_hate", "rule_of_law"]):
        got = fm.mixture_samples("lightning_war", SAMPLES, cond)
        for (bd, bt), (gd, gt) in zip(base, got):
            assert _inf(gd) >= _inf(bd)
            assert _inf(gt) >= _inf(bt)


def test_curve_shape_and_monotone():
    grid = [5, 6, 7, 8, 9, 10, 12, 14]
    dt = fm.mixture_samples("lightning_war", SAMPLES, [])   # curve() consumes (decap,table) tuples
    c = fm.curve(dt, grid, len(dt))
    assert c["grid"] == grid
    assert len(c["decap"]) == len(grid) == len(c["table"])
    assert len(c["med"]) == 2 and len(c["never"]) == 2
    # cumulative P(kill <= T) is non-decreasing in T
    assert c["decap"] == sorted(c["decap"])
    assert c["table"] == sorted(c["table"])
    # decap is never behind table (decap = first dead <= table = all dead), per game and so cum
    assert all(d >= t for d, t in zip(c["decap"], c["table"]))


# --- golden (bulk-gated): the REAL Lightning War null reduction ---------------------------
@pytest.mark.golden
@pytest.mark.skipif(not BULK.exists(), reason="needs Scryfall bulk")
def test_real_lw_null_reduction():
    # mixture{} reproduces bestline_kill on the same shared games, per game — the per-line
    # split did not perturb the harvested curve. Modest trials keep it quick.
    assert fm.null_reduction_ok(1500, fm.lw.SEED)


@pytest.mark.golden
@pytest.mark.skipif(not BULK.exists(), reason="needs Scryfall bulk")
def test_emitted_json_schema_and_lw_split():
    recs = fm.build_records(1200, fm.lw.SEED)
    assert recs["lightning_war"]["split"] is True
    lines = recs["lightning_war"]["lines"]
    assert {l["line_id"] for l in lines} == {"burn", "combo"}
    assert "bestline_check" in recs["lightning_war"]
    # an unsplit deck is a single pass-through line with no disablers
    assert recs["genome_project"]["split"] is False
    assert len(recs["genome_project"]["lines"]) == 1
    assert recs["genome_project"]["lines"][0]["disablers"] == []
