"""Regression guards for the Glarb "inevitable" topdeck-combo build.

PROMOTED to the active roster 2026-07-01 as Croak and Dagger
(decks/croak-and-dagger-20260701.txt). This guard was flipped from the
candidate-state checks (was: "glarb_inevitable in BUILD_CLOCKS, NOT in CLOCKS")
to the promoted-state checks below — the T9 combo curve now lives in
CLOCKS["croak_and_dagger"], and the pending BUILD_CLOCKS candidate was retired.

Fast + hermetic: imports pod_gauntlet only (no 176 MB oracle load) and checks the
harvested clock wiring + the headline claim — that the T9 combo curve scores
materially better P(beat pod) than the T13 grind it replaced. The assembly-clock
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


def test_croak_clock_is_now_the_combo_t9():
    e = pg.CLOCKS["croak_and_dagger"]
    assert e["decap"] == e["table"], "combo: decap == table by construction (loop kills the table)"
    assert e["med"] == ("T9", "T9")
    assert e["disrupt_class"] == "warn"      # keeps Croak's counter suite


def test_candidate_promoted_not_pending():
    # the "inevitable" build IS the roster deck now — its curve lives in CLOCKS under the
    # croak_and_dagger slug, and it must NOT linger as a pending BUILD_CLOCKS candidate.
    assert "croak_and_dagger" in pg.CLOCKS
    assert "glarb_inevitable" not in pg.BUILD_CLOCKS
    assert "glarb_inevitable" not in pg.PROTECT


def test_protect_reflects_counter_immune_kill():
    # Aetherflux "Pay 50: deal 50" is an ABILITY (counter-immune) + Tidal Barracuda soft-lock,
    # so our protect-own capability jumped from the old counterable-Torment 0.35 to 0.50.
    assert pg.PROTECT["croak_and_dagger"] == 0.50


def test_combo_clock_beats_the_grind_it_replaced():
    kd = pg.K_DIST
    e = pg.merged_clocks()["croak_and_dagger"]
    F_new = pg.build_cdf(e["grid"], e["decap"])
    # the old grind curve it replaced (decap T13 / table >T14)
    old_decap = [0, 0, 1, 3, 8, 30, 50, 58]
    old_grid = [5, 6, 7, 8, 9, 11, 13, 14]
    F_old = pg.build_cdf(old_grid, old_decap)
    w_new, _, _ = pg.simulate("croak_and_dagger", F_new, 0.5, kd, 20000, random.Random(1))
    w_old, _, _ = pg.simulate("croak_and_dagger", F_old, 0.5, kd, 20000, random.Random(1))
    assert w_new > 0.20, "rebuild should reach a fair-share band vs the pod"
    assert w_new > 2 * w_old, "must be materially better than the T13 grind"


def test_pure_race_lifts_above_grind():
    kd = pg.K_DIST
    e = pg.merged_clocks()["croak_and_dagger"]
    F_new = pg.build_cdf(e["grid"], e["decap"])
    assert pg.pure_race(F_new, kd) > 0.15     # was ~3% for the T13 grind
