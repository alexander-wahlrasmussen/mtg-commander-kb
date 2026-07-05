"""REGRESSION — vs_dragon_roster_lab's oracle index and toolkit classifier.

2026-07-05: otext("Infernal Grasp") returned whitespace — a textless "X // X"
double-faced printing was indexed via the face-name path BEFORE the real card,
poisoning the index and silently deflating every deck's spot-removal count
(the 2026-06-15 writeup called the counts "floors" without knowing this cause).
These tests pin the fix: textless printings may not shadow real oracle text,
and the canonical removal suite of the merged World Shapers list classifies.

`golden`-marked: needs the Scryfall bulk (collection/oracle-cards.json).
"""
import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
BULK = ROOT / "collection" / "oracle-cards.json"

pytestmark = [
    pytest.mark.golden,
    pytest.mark.skipif(not BULK.exists(),
                       reason="Scryfall bulk (collection/oracle-cards.json) absent"),
]


@pytest.fixture(scope="module")
def vd():
    spec = importlib.util.spec_from_file_location(
        "vs_dragon_roster_lab", ROOT / "scripts" / "vs_dragon_roster_lab.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.load_oracle()
    return mod


def test_textless_printing_does_not_poison_index(vd):
    # the 2026-07-05 regression card: a textless "Infernal Grasp // Infernal Grasp"
    # entry precedes the real card in the bulk
    assert "destroy target creature" in vd.otext("Infernal Grasp")


def test_no_indexed_entry_is_blank(vd):
    blank = [nm for nm, t in vd.ORACLE.items() if not t.strip()]
    assert not blank, f"blank oracle entries poison classify(): {blank[:5]}"


def test_spot_classifier_catches_the_merged_removal_suite(vd):
    tk = vd.classify(["Infernal Grasp", "Putrefy", "Beast Within",
                      "Tear Asunder", "Blasphemous Act"])
    assert set(tk["spot"]) >= {"Infernal Grasp", "Putrefy", "Beast Within",
                               "Tear Asunder"}
    assert tk["wraths"] == ["Blasphemous Act"]
