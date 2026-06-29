"""REGRESSION (2026-06-29 codebase audit — per-lab sim-correctness cluster).

One hermetic guard per confirmed sim bug. Each pins a number/semantics the audit
found wrong so the regression can't return. No Scryfall bulk: synthetic objects and
pure-function asserts only (runs in the `pytest -m "not golden"` fast gate).
"""
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))


def _load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# --- er_speed_lab: Fire Lord Zuko MV was hardcoded 4; his cost is {R}{W}{B} = 3 ---
def test_er_zuko_mv_is_three():
    er = _load("er_speed_lab")
    assert er.ZUKO_MV == 3, (
        "Fire Lord Zuko is {R}{W}{B} = MV3 (card_lookup); MV4 made the commander "
        "(the deck's only +1/+1 source) come online a turn late -> clock too slow")


# --- pod_gauntlet.simulate_vs_lock: a PERSISTENT lock was re-rolled every turn ---
def test_simulate_vs_lock_is_persistent():
    """A live, effective hard-lock holds EVERY turn until removed; the bug re-rolled
    Bernoulli(e) per turn so P(hold n turns) ~= e^n (geometric leak), understating locks.
    Isolate persistence: we never kill (F=0), the lock is online from t1 with prob 1,
    e=0.5, r=0 (never removed). Persistent -> grind ~= P(lock effective) = e = 0.5; the
    e^n bug would collapse grind to ~0 (the lock leaks over the ~12 combo turns)."""
    pg = _load("pod_gauntlet")
    import random
    F_never = [0.0] * (pg.HORIZON + 1)
    lock_cdf = pg.build_cdf([1], [100])          # online turn 1, prob 1
    opp = {"disruption_a": 0.0, "answer": 0.0}
    _win, grind = pg.simulate_vs_lock("__synthetic_persistence_probe__", F_never, opp,
                                      {5: 1.0}, lock_cdf, e=0.5, r=0.0,
                                      trials=20000, rng=random.Random(0))
    assert 0.45 <= grind <= 0.55, (
        f"grind={grind:.3f}; a persistent lock should hold ~e=0.5 of the time, not e^n→0")


# --- pod_championship: the hardcoded 16-deck bracket dropped the 17th seed ---
import random  # noqa: E402

import pytest  # noqa: E402


@pytest.mark.parametrize("n", [15, 16, 17, 18, 19, 21])
def test_championship_brackets_place_every_seed(n):
    """draw_groups hardcoded `range(4)` × seeds[4p:4p+4], dealing only indices 0..15 —
    a 17-deck roster silently dropped seed #17. Both builders must place EVERY seed into
    one of 4 pods (so exactly 4 group winners advance) and stay balanced (±1)."""
    pc = _load("pod_championship")
    seeds = [f"d{i}" for i in range(n)]
    for groups in (pc.draw_groups(seeds, random.Random(0)), pc.snake_groups(seeds)):
        placed = [s for g in groups for s in g]
        assert sorted(placed) == sorted(seeds)              # no seed dropped or duplicated
        assert len(groups) == 4                             # still 4 pods -> Final Four = 4
        assert max(map(len, groups)) - min(map(len, groups)) <= 1   # balanced
