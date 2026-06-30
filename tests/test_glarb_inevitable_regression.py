"""Regression guards for the Glarb "inevitable" topdeck-combo build candidate.

Fast + hermetic: imports pod_gauntlet only (no 176 MB oracle load) and checks the
harvested clock wiring + the headline claim — that the T9 combo curve scores
materially better P(beat pod) than the T13 grind it replaces. The assembly-clock
lab itself (glarb_inevitable_lab.py) needs the oracle, so its output is exercised
by running the lab, not in this fast guard.
"""
import importlib.util
import random
from pathlib import Path

ROOT = Path(__file__).parent.parent


def _load(name, rel):
    spec = importlib.util.spec_from_file_location(name, ROOT / rel)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


pg = _load("pod_gauntlet", "scripts/pod_gauntlet.py")


def test_build_clock_registered_as_combo_t9():
    e = pg.BUILD_CLOCKS["glarb_inevitable"]
    assert e["decap"] == e["table"], "combo: decap == table by construction"
    assert e["med"] == ("T9", "T9")
    assert e["disrupt_class"] == "warn"      # keeps Croak's counter suite


def test_candidate_not_in_roster_but_in_pending():
    # it's a considering/ candidate — must NOT collide with the guarded roster CLOCKS,
    # but MUST be foldable via --pending (BUILD_CLOCKS).
    assert "glarb_inevitable" not in pg.CLOCKS
    assert "glarb_inevitable" in pg.BUILD_CLOCKS


def test_combo_clock_beats_the_grind_it_replaces():
    kd = pg.K_DIST
    e = pg.BUILD_CLOCKS["glarb_inevitable"]
    F_new = pg.build_cdf(e["grid"], e["decap"])
    old = pg.merged_clocks()["croak_and_dagger"]
    F_old = pg.build_cdf(old["grid"], old["decap"])
    w_new, _, _ = pg.simulate("glarb_inevitable", F_new, 0.5, kd, 20000, random.Random(1))
    w_old, _, _ = pg.simulate("croak_and_dagger", F_old, 0.5, kd, 20000, random.Random(1))
    assert w_new > 0.20, "rebuild should reach a fair-share band vs the pod"
    assert w_new > 2 * w_old, "must be materially better than the T13 grind"


def test_pure_race_lifts_above_grind():
    kd = pg.K_DIST
    e = pg.BUILD_CLOCKS["glarb_inevitable"]
    F_new = pg.build_cdf(e["grid"], e["decap"])
    assert pg.pure_race(F_new, kd) > 0.15     # was ~3% for the T13 grind
