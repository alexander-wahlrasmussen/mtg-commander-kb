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
