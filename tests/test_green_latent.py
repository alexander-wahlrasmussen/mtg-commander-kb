"""REGRESSION (2026-06-29 codebase audit — 🟢 lower-impact / latent traps).

Guards the er_speed_lab / rc_speed_lab `build_lib` copies against the silent-no-op
bug: the shared speed_lab_core.build_lib raises when a remove-target isn't in the
library, but these two hand-rolled copies used to drop a missing target on the floor,
so a typo'd cut card silently produced the UNCHANGED list (a fake A/B comparison).

Hermetic: pure-function asserts on a tiny synthetic library — no Scryfall bulk
(runs in the `pytest -m "not golden"` fast gate). Loads each lab via importlib; the
labs only `import deck_sim` at module scope (no oracle bulk until main()).
"""
import importlib.util
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from helpers import land, rec  # noqa: E402


def _load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _base():
    """A parse_deck-shaped library: list of (name, record)."""
    return [("Island", land()), ("Bear", rec()), ("Bird", rec(cmc=1.0))]


@pytest.mark.parametrize("lab_name", ["er_speed_lab", "rc_speed_lab"])
def test_build_lib_raises_on_missing_remove_target(lab_name):
    """A cut that names a card NOT in the library is a typo, not a no-op: it must
    fail loud (SystemExit), mirroring speed_lab_core.build_lib — otherwise the
    variant silently equals the baseline and every A/B delta off it is fake."""
    lab = _load(lab_name)
    with pytest.raises(SystemExit) as exc:
        lab.build_lib(_base(), {}, ["Nonexistent Typo Card"], [])
    assert "remove not in library" in str(exc.value)


@pytest.mark.parametrize("lab_name", ["er_speed_lab", "rc_speed_lab"])
def test_build_lib_present_target_still_runs(lab_name):
    """The guard only fires on a genuinely-missing target: a real cut still works,
    removes exactly one copy, and leaves the rest of the library intact (so the real
    lab invocations are unchanged — clock-neutral)."""
    lab = _load(lab_name)
    out = lab.build_lib(_base(), {}, ["Bear"], [])
    names = [n for n, _ in out]
    assert names == ["Island", "Bird"]


@pytest.mark.parametrize("lab_name", ["er_speed_lab", "rc_speed_lab"])
def test_build_lib_missing_add_still_raises(lab_name):
    """The pre-existing add-side guard is untouched: an add absent from the oracle
    index still raises (the remove guard sits in front of it, not instead of it)."""
    lab = _load(lab_name)
    with pytest.raises(SystemExit) as exc:
        lab.build_lib(_base(), {}, ["Bear"], ["Card Not In Oracle"])
    assert "add not in oracle" in str(exc.value)
