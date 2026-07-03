"""Backlog #13 Phase 3 — the MEASURED per-opponent pod profile is OPT-IN and NULL-REDUCES.

The finisher_mixture / interaction-overlay discipline: a new modelling layer must default to
byte-identical output, so the switch is provably a switch. Here that means the anti-pod axis
(the tier list's largest weight) is unchanged with the profile OFF, and only moves when it's
explicitly turned on. Not bulk-gated: reads the committed pod_gauntlet_clocks.json + runs the
MC anti-pod oracle at a small trial count (~1s, no Scryfall bulk), same as test_tier_list.
"""
import importlib.util
import random
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent


def _load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


tl = _load("tier_list")
pg = tl.pg          # the SAME pod_gauntlet instance tier_list's antipod_blend reads (importlib
                    # spec_from_file_location makes fresh module objects, so a standalone
                    # _load("pod_gauntlet") would be a DIFFERENT instance set_profile wouldn't reach)


@pytest.fixture(autouse=True)
def _restore_profile():
    """The profile is a module global; always leave the default (legacy) restored so tests
    (and any later import consumers in the same session) never leak the measured state."""
    yield
    pg.set_profile(False)


def _anti(seed=7, trials=2000):
    """The tier list's anti-pod axis under the CURRENTLY active profile (attribute-read, so it
    follows set_profile). Fresh rng each call -> deterministic given (seed, profile)."""
    C = pg.merged_clocks()
    slugs = list(C)
    return tl.antipod_blend(slugs, C, trials, random.Random(seed))


def test_default_profile_is_legacy():
    pg.set_profile(False)
    assert pg.OPPONENTS is pg.OPPONENTS_LEGACY
    assert pg.MEASURED_PROFILE is False
    # legacy opponents carry NO per-opponent kdist -> simulate_vs falls back to the global K_DIST
    assert all("kdist" not in o for o in pg.OPPONENTS.values())


def test_null_reduction_antipod_bit_identical_off():
    """Profile OFF is byte-identical across a set_profile round-trip: the refactor did not touch
    the legacy code path."""
    pg.set_profile(False)
    a = _anti()
    pg.set_profile(True)
    pg.set_profile(False)                     # round-trip back to the default
    b = _anti()
    assert a == b                             # exact — same rng seed, same (legacy) path


def test_profile_on_changes_and_lifts_antipod():
    """The opt-in DOES something, and in the expected direction: the measured stable is a slower
    pod (Acererak nv59%, Henzie T11), so our anti-pod win-levels rise on average."""
    pg.set_profile(False)
    base = _anti()
    pg.set_profile(True)
    meas = _anti()
    assert pg.OPPONENTS is pg.OPPONENTS_MEASURED
    assert base != meas
    assert sum(meas.values()) / len(meas) > sum(base.values()) / len(base)


def test_measured_kdists_are_valid_pmfs():
    for s, o in pg.OPPONENTS_MEASURED.items():
        kd = o["kdist"]
        assert abs(sum(kd.values()) - 1.0) < 1e-6, s          # a proper pmf (incl. NEVER bucket)
        assert all(0.0 <= p <= 1.0 for p in kd.values()), s
        assert max(kd) <= pg.NEVER_K, s                       # never-in-horizon lands on the sentinel


def test_measured_weights_sum_to_one():
    assert abs(sum(o["weight"] for o in pg.OPPONENTS_MEASURED.values()) - 1.0) < 1e-9
    # the retired 5C-tail (Kenrith/Kinnan, unseen) is gone; Ur-Dragon + Henzie are now explicit
    assert set(pg.OPPONENTS_MEASURED) == {"acererak", "ur_dragon", "hidetsugu_kairi", "henzie"}
