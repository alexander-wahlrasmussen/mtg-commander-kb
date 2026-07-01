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


# --- urza_clock_lab: Urza's +2 artifact mana was regranted on every spend() ---
def test_urza_artifact_mana_is_once_per_turn():
    """Urza's "Tap an untapped artifact: Add {U}" is once-per-artifact-per-turn, modelled
    as a +2 per-turn pool. The bug recomputed the +2 from the `self.urza` boolean on every
    spend(), so it refreshed per-spend (unbounded mana/turn) -> clock too fast. The pool
    must DEPLETE and not regrant within a turn."""
    u = _load("urza_clock_lab")
    from helpers import land, rec
    import random
    lib = [("Island", land()) for _ in range(20)] + [(f"S{i}", rec(cmc=2)) for i in range(10)]
    tr = u.Trial(lib, random.Random(0))
    tr.g.avail = 0
    tr.petal = 0
    tr.urza = True
    tr.urza_pool = 2
    assert tr.mana() == 2                  # the per-turn pool is available
    tr.spend(2)
    assert tr.urza_pool == 0               # ... and depletes
    assert tr.mana() == 0                  # NOT regranted from the urza boolean
    tr.spend(2)                            # a second spend can't draw a fresh +2 bonus
    assert tr.mana() == -2                 # it underflows (the buggy code would stay 0)


# --- lw_speed_lab: Crackle's X>=3 targeting floor (a 3-wipe never costs < 11 mana) ---
def test_crackle_lethal_mana_respects_targeting_floor():
    """Crackle with Power {X}{X}{X}{R}{R} hits up to X targets for 5X each; a 3-opponent
    wipe forces X>=3 => >=11 mana at ANY life. The sensitivity block offered 8/5-mana
    'wipes' (X=2/X=1, only 1-2 targets) -> @20/@30 kill odds inflated (clock too fast)."""
    lw = _load("lw_speed_lab")
    f = lw.crackle_lethal_mana
    assert (f(40, 2), f(40, 3)) == (14, 11)        # @40: no-amp X=4, amp X=3
    assert (f(30, 2), f(30, 3)) == (11, 11)        # floor kicks in
    assert (f(20, 2), f(20, 3)) == (11, 11)
    assert all(f(life, c) >= 11 for life in range(1, 46) for c in (2, 3))  # never below floor


# --- clock_check: a header-format clock line ("Score … · Clock: …") parsed as UNPARSED ---
def test_clock_check_parses_header_format_clock_line():
    """Forced Liquidation cites its clock on the header row: "Score: 16/20 (5 / 4 / 3 / 4) ·
    Clock: T8 decap / T9 table (lab …)". HEAD_CUT cut at the FIRST '·' (the Score|Clock
    separator), discarding the whole clock clause -> UNPARSED on a correct citation. The
    fallback re-cuts at the lab marker when the head lost every clock keyword. Pins decap/table
    AND that the "16/20" / "5 / 4 / 3 / 4" score numbers don't leak a false turn."""
    cc = _load("clock_check")
    line = ("**Score:** 16/20 (5 / 4 / 3 / 4) · Clock: T8 decap / T9 table (spell, sorcery) "
            "(lab `kfk_clock_lab.py` 2026-06-25). Audited 2026-06-27.")
    out = cc.cited_turns(line)
    assert out["decap"] == (8, False), out
    assert out["table"] == (9, False), out


# --- Croak PROMOTED 2026-07-01 to the "inevitable" topdeck combo (T9 assembly clock) ---
def test_croak_published_clock_is_the_promoted_combo():
    """The live Croak clock (merged_clocks -> analysis/pod_gauntlet_clocks.json) is the promoted
    "inevitable" topdeck-combo assembly clock: median T9, decap == table (the loop kills the table
    by construction, like a Thoracle line). This T9 is a LEGITIMATE combo clock from
    glarb_inevitable_lab (dig=SELECTION), NOT the historical dig=2 raw-draw bug that once inflated
    the GRIND shell to a fictional ~T10 — so the src must name glarb_inevitable_lab / dig=selection,
    never a raw-draw model."""
    import json
    c = json.loads((ROOT / "analysis" / "pod_gauntlet_clocks.json").read_text(encoding="utf-8"))["croak_and_dagger"]
    assert c["decap"] == c["table"], "combo: decap == table by construction"
    assert c["med"] == ["T9", "T9"], c["med"]
    assert "glarb_inevitable_lab" in c["src"] and "selection" in c["src"], c["src"]
    assert c["name"] == "Croak and Dagger"          # not the stale "The Calamity Tax"
