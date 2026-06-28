"""Hermetic tests for mulligan_trainer.py — the keep/mulligan DRILL.

The trainer's whole credibility rests on one invariant: its KEEP/MULL verdict is
the deck_sim plan-keep model's, verbatim — never a second, drifting heuristic. So
the load-bearing test is `verdict()[0] == ds.keep_hand()` over a battery of hands.
The rest pins the human-facing explanation (band reason, which axis fired, the
`also` second-line union). No Scryfall bulk, no decklist — synthetic spec + hands.
"""
import random
from pathlib import Path

import pytest

import mulligan_trainer as mt
from helpers import rec, land

BULK = Path(__file__).resolve().parent.parent / "collection" / "oracle-cards.json"


def _spec(**over):
    """A keep_specs.json-shaped entry; override any field."""
    s = {
        "deck_key": "toy", "name": "Toy Deck",
        "bottleneck": "FINDING", "also": [],
        "min_lands": 2, "max_lands": 4, "hi_curve": False,
        "cmdr": "Toy Commander", "cmdr_cmc": 4,
        "key_cards": ["combo piece"], "tutors": ["demonic tutor"],
        "ramp": ["sol ring"], "selection": ["ponder", "preordain"],
        "n_selection_needed": 2, "mixed": None,
    }
    s.update(over)
    return s


def _hand(n_land, spells):
    """n_land Islands + the named spells (each cmc 2 creature unless it's a known
    bucket card we just need by NAME — buckets match on name, not record)."""
    return [("Island", land()) for _ in range(n_land)] + \
           [(nm, rec(cmc=2)) for nm in spells]


# --------------------------------------------------------------------------- #
# THE invariant: the drill never disagrees with the sim it trains against.
# --------------------------------------------------------------------------- #
def test_verdict_matches_keep_hand_over_a_battery():
    spec = mt.install(_spec(also=["BOARD"]))
    pool = ["combo piece", "demonic tutor", "sol ring", "ponder", "preordain",
            "random bear", "another bear", "big dumb idiot"]
    rng = random.Random(0)
    for _ in range(400):
        n_land = rng.randint(0, 6)
        spells = [rng.choice(pool) for _ in range(7 - n_land)]
        hand = _hand(n_land, spells)
        keep, _ = mt.verdict(hand, spec)
        assert keep == mt.ds.keep_hand(hand)


# --------------------------------------------------------------------------- #
# Band gate
# --------------------------------------------------------------------------- #
def test_out_of_band_is_mull_and_says_so():
    spec = mt.install(_spec())
    keep, reasons = mt.verdict(_hand(1, ["combo piece", "x", "y", "z", "w", "v"]), spec)
    assert keep is False
    assert any("OUT OF BAND" in r for r in reasons)
    # band failing short-circuits — no per-axis lines are claimed satisfied
    assert any("ship regardless of plan" in r for r in reasons)


def test_too_many_lands_is_mull():
    spec = mt.install(_spec())
    keep, _ = mt.verdict(_hand(5, ["combo piece", "a"]), spec)
    assert keep is False


# --------------------------------------------------------------------------- #
# FINDING axis
# --------------------------------------------------------------------------- #
def test_finding_satisfied_by_a_key_piece():
    spec = mt.install(_spec())
    keep, reasons = mt.verdict(_hand(3, ["combo piece", "x", "y", "z"]), spec)
    assert keep is True
    assert any("FINDING" in r and "satisfied" in r for r in reasons)


def test_finding_needs_two_selection_not_one():
    spec = mt.install(_spec())
    # one dig card, in band, no key/tutor -> plan not advanced -> MULL
    one = mt.verdict(_hand(3, ["ponder", "x", "y", "z"]), spec)[0]
    assert one is False
    # two dig cards clears n_selection_needed=2
    two = mt.verdict(_hand(3, ["ponder", "preordain", "y", "z"]), spec)[0]
    assert two is True


# --------------------------------------------------------------------------- #
# `also` second line: a BOARD-strong hand keeps under a FINDING+BOARD deck
# (the Radiation -9pp lesson — don't ship a board hand chasing the side combo).
# --------------------------------------------------------------------------- #
def test_also_axis_can_carry_the_keep():
    spec = mt.install(_spec(bottleneck="FINDING", also=["BOARD"], cmdr_cmc=3))
    # in band, no FINDING card, but an early cmc<=3 play + lands reach the commander
    hand = _hand(3, ["random bear", "x", "y", "z"])
    keep, reasons = mt.verdict(hand, spec)
    assert keep is True
    assert any("BOARD" in r and "satisfied" in r for r in reasons)
    assert any("FINDING" in r and r.strip().endswith("no") for r in reasons)


# --------------------------------------------------------------------------- #
# card_tags: a card shows the buckets it belongs to (display correctness)
# --------------------------------------------------------------------------- #
def test_card_tags_label_buckets_and_lands():
    spec = mt.install(_spec())
    assert mt.card_tags("Island", land(), spec) == ["LAND"]
    assert "KEY" in mt.card_tags("Combo Piece", rec(cmc=3), spec)
    assert "DIG" in mt.card_tags("Ponder", rec(cmc=1), spec)
    assert mt.card_tags("Random Bear", rec(cmc=2), spec) == []


# --------------------------------------------------------------------------- #
# bake_hands — the dashboard payload. Bulk-gated (needs a real decklist + the
# Scryfall oracle); the verdict-equals-keep_hand invariant is already pinned
# hermetically above, so this guards SHAPE + land-count consistency + seed
# reproducibility on a real deck (catch an integration/schema break).
# --------------------------------------------------------------------------- #
@pytest.mark.golden
@pytest.mark.skipif(not BULK.exists(),
                    reason="Scryfall bulk (collection/oracle-cards.json) absent")
def test_bake_hands_shape_and_land_consistency():
    p = mt.bake_hands("genome_project", n=12, seed=0)
    assert p is not None and len(p["hands"]) == 12
    assert p["minLands"] <= p["maxLands"] and p["bottleneck"] in p["axisGloss"]
    for h in p["hands"]:
        assert len(h["cards"]) == 7
        assert h["lands"] == sum(c["land"] for c in h["cards"])
        assert isinstance(h["keep"], bool) and h["reasons"]
        assert "band" in h["reasons"][0]
        for c in h["cards"]:
            assert (c["cmc"] is None) == c["land"]   # lands carry no cmc, spells do


@pytest.mark.golden
@pytest.mark.skipif(not BULK.exists(), reason="Scryfall bulk absent")
def test_bake_hands_is_seed_reproducible_and_seed_matters():
    a = mt.bake_hands("genome_project", n=8, seed=0)
    b = mt.bake_hands("genome_project", n=8, seed=0)
    c = mt.bake_hands("genome_project", n=8, seed=1)
    assert a == b              # same seed -> identical payload (replayable bake)
    assert a != c              # the seed actually shuffles the hands


@pytest.mark.golden
@pytest.mark.skipif(not BULK.exists(), reason="Scryfall bulk absent")
def test_bake_hands_none_when_no_keep_spec():
    # a roster slug with no keep-spec (or no decklist) bakes to None, not a crash
    assert mt.bake_hands("not_a_real_slug", n=2, seed=0) is None
