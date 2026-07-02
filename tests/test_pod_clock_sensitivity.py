"""Tier-1 tests for pod_clock_sensitivity — the K_DIST sweep's pure helpers.

Hermetic where possible (shift/composite/verdict are pure math; no bulk, no network). The
composite test guards the ONE thing that must never drift: this tool's recomposite is the
SAME math as tier_list.compute_rows (norm -> weighted mean with None redistribution -> tier
cut), because a sweep that recomposites differently would report tier flips that are just
implementation skew.
"""
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def _load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


pcs = _load("pod_clock_sensitivity")
tl = pcs.tl


# --- shift_kdist -------------------------------------------------------------
def test_shift_zero_is_identity():
    assert pcs.shift_kdist(pcs.pg.K_DIST, 0) == pcs.pg.K_DIST


def test_shift_preserves_mass_and_moves_mean():
    for d in (-2, -1, 1, 2):
        kd = pcs.shift_kdist(pcs.pg.K_DIST, d)
        assert abs(sum(kd.values()) - 1.0) < 1e-12
        assert abs(pcs.kdist_mean(kd) - (pcs.kdist_mean(pcs.pg.K_DIST) + d)) < 1e-12


def test_shift_clamps_at_turn_one():
    kd = pcs.shift_kdist({1: 0.5, 2: 0.5}, -1)
    assert kd == {1: 1.0}                       # clamp-merge, mass conserved
    assert abs(sum(kd.values()) - 1.0) < 1e-12


# --- composite parity with tier_list ------------------------------------------
def test_composite_matches_compute_rows_math():
    """Feed compute_rows' own raw axis values back through pcs.composite: COMP and tier
    must reproduce exactly. Small trial count — parity is deterministic given the rows."""
    base = tl.compute_rows(trials=400)
    rows = {r["slug"]: r for r in base["rows"]}
    raw = {"antipod": {s: rows[s]["anti"] for s in rows},
           "inter": {s: rows[s]["inter"] for s in rows},
           "self": {s: rows[s]["self"] for s in rows}}
    got = pcs.composite(raw)
    for s, r in rows.items():
        comp, tier = got[s]
        assert abs(comp - r["comp"]) < 1e-9, s
        assert tier == r["tier"], s


def test_composite_redistributes_none_weight():
    """One slug missing an axis (the compute_rows Zero-Sum/off-MEASURED case): its weight
    is redistributed over the axes it does have — same math as compute_rows lines 142-146."""
    raw = {"antipod": {"a": 100.0, "b": 0.0, "c": 50.0},
           "inter": {"a": 100.0, "b": 0.0, "c": None},   # c unmeasured on this axis
           "self": {"a": 100.0, "b": 0.0, "c": 50.0}}
    got = pcs.composite(raw)
    assert got["a"][0] == 100.0 and got["b"][0] == 0.0
    assert got["a"][1] == "S" and got["b"][1] == "D"
    assert abs(got["c"][0] - 50.0) < 1e-9       # redistributed mean of its two 50s


# --- verdict ------------------------------------------------------------------
def test_verdict_classification():
    dmap = {"-2": 2, "-1": 1, "base": 0, "+1": 1, "+2": 2, "fast": None, "slow": None}
    same = {k: "A" for k in dmap}
    assert pcs.verdict(same, "A", dmap) == "ROBUST"
    edge = dict(same, **{"+2": "B"})
    assert pcs.verdict(edge, "A", dmap) == "EDGE"
    near = dict(same, **{"+1": "B"})
    assert pcs.verdict(near, "A", dmap) == "SENSITIVE"
    preset = dict(same, **{"slow": "B"})        # preset shapes count as inside the band
    assert pcs.verdict(preset, "A", dmap) == "SENSITIVE"


def test_profiles_ordered_by_mean_and_include_presets():
    ps = pcs.profiles([-2, -1, 0, 1, 2])
    keys = [k for k, _, _ in ps]
    assert {"fast", "slow", "base"} <= set(keys)
    means = [pcs.kdist_mean(kd) for _, kd, _ in ps]
    assert means == sorted(means)
