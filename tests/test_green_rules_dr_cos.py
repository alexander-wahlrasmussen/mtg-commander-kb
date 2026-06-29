"""REGRESSION (2026-06-29 codebase audit, 🟢 lower-impact rules nits).

Three SECONDARY-line rules misreads, fixed clock-neutrally (DR published decap T9 /
table >T14 and CoS decap T8 / table T11 all held on a full re-run):

  * dr_clock_lab.py — Zulaport-class lifegain over-credited. The per-death drain `d`
    (every each-opponent payoff: Zulaport, Elas, Syr Konrad, Meathook, Agent...) was
    re-credited WHOLESALE as life. But only Zulaport / Cruel Celebrant / Bastion read
    "each opponent loses 1 AND you gain 1" (gain 1 TOTAL, not per opponent). Elas gains
    on ETB not death; Meathook gains only off an OPPONENT's death; Syr Konrad/Agent
    gain nothing. The over-credit fed the Vito/Sanguine-Bond/Exquisite-Blood loop.

  * dr_clock_lab.py — Living Death OVER-RETURNED the board. It returns ONLY the creature
    cards already in the yard at resolution (exiled by its first instruction); the board
    sacrificed by its second instruction stays dead (oracle + ruling). The lab snapshotted
    the returnable set AFTER the board sacrifice dumped it into the yard -> whole board
    came back.

  * cos_clock_lab.py — Diregraf Colossus SELF-TRIGGERED. "Whenever you cast a Zombie
    spell, create a tapped 2/2" only fires when Colossus is ALREADY on the battlefield
    (ruling: "won't trigger when you cast it because it's not on the battlefield yet").
    The deploy loop set the colossus flag, THEN ran the cast trigger -> a self-token.

All card text verified via scripts/card_lookup.py 2026-06-29. Hermetic: toy library +
synthetic records only (no Scryfall bulk).
"""
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import dr_clock_lab as dr      # noqa: E402
import cos_clock_lab as cos    # noqa: E402
from helpers import rec, toy_library  # noqa: E402


def _dr_trial():
    return dr.Trial(toy_library(), random.Random(0))


def _cos_trial():
    return cos.Trial(toy_library(), random.Random(0), index={}, pips={})


# --------------------------------------------------------------------------
# DR — Zulaport-class lifegain counts only GAIN_PAYOFFS, not the full drain
# --------------------------------------------------------------------------

def test_dr_gain_payoffs_are_the_lifegain_subset():
    """Only the cards whose oracle reads '...and you gain 1 life' belong here."""
    assert dr.GAIN_PAYOFFS == {"Zulaport Cutthroat", "Cruel Celebrant",
                               "Bastion of Remembrance"}
    assert dr.GAIN_PAYOFFS < dr.PAYOFFS                 # strict subset
    # the drain-only payoffs must NOT gain you life
    for drain_only in ("Elas il-Kor, Sadistic Pilgrim", "Syr Konrad, the Grim",
                       "The Meathook Massacre"):
        assert drain_only in dr.PAYOFFS
        assert drain_only not in dr.GAIN_PAYOFFS


def test_dr_lifegain_is_not_the_drain_count():
    """The bug re-credited the per-opponent drain (d) as life. With four drain
    payoffs but one lifegain payoff, gain must be 1 while the drain is 4."""
    t = _dr_trial()
    t.teysa = False
    t.bf = {"Zulaport Cutthroat", "Elas il-Kor, Sadistic Pilgrim",
            "Syr Konrad, the Grim", "The Meathook Massacre"}
    assert t.per_death(False) == 4          # each opponent loses 4
    assert t.per_death_gain(False) == 1     # you gain 1, NOT 4


def test_dr_lifegain_doubles_with_teysa():
    t = _dr_trial()
    t.bf = {"Zulaport Cutthroat", "Cruel Celebrant", "Bastion of Remembrance",
            "Syr Konrad, the Grim"}
    t.teysa = False
    assert t.per_death_gain(False) == 3     # three lifegain payoffs
    t.teysa = True
    assert t.per_death_gain(False) == 6     # Teysa doubles the death triggers


def test_dr_token_lifegain_nadier_yes_mirkwood_no():
    """On a TOKEN death: Nadier ('a token you control leaves... you gain 1') adds
    lifegain; Mirkwood Bats ('each opponent loses 1' only) drains without gain."""
    t = _dr_trial()
    t.teysa = False
    t.bf = {"Mirkwood Bats", "Nadier's Nightblade"}
    assert t.per_death(True) == 2           # Mirkwood + Nadier both drain
    assert t.per_death_gain(True) == 1      # only Nadier gains you life
    # Mirkwood alone: a drain with zero lifegain
    t.bf = {"Mirkwood Bats"}
    assert t.per_death(True) == 1
    assert t.per_death_gain(True) == 0


# --------------------------------------------------------------------------
# DR — Living Death returns only the yard snapshot, never the sacrificed board
# --------------------------------------------------------------------------

def test_living_death_returns_only_the_yard_not_the_board():
    t = _dr_trial()
    t.teysa = True
    board = {"Zulaport Cutthroat", "Syr Konrad, the Grim"}
    yard = ["Grave Titan", "Kokusho, the Evening Star"]
    t.bf = set(board)
    t.dead = list(yard)
    returned = t.resolve_living_death(6)
    # ONLY the pre-existing yard creatures come back
    assert set(returned) == set(yard)
    assert len(returned) == len(yard)
    # the sacrificed board went to the yard and did NOT return to the battlefield
    for nm in board:
        assert nm not in t.bf
        assert nm in t.dead


def test_living_death_does_not_over_return():
    """The whole point: returnable count == yard-before, regardless of board size.
    Under the bug it was yard + board."""
    t = _dr_trial()
    t.teysa = False
    t.bf = {f"Body{i}" for i in range(5)}        # a big board (none are payoffs)
    yard = ["Grave Titan"]
    t.dead = list(yard)
    returned = t.resolve_living_death(7)
    assert len(returned) == 1                    # NOT 1 + 5


# --------------------------------------------------------------------------
# CoS — Diregraf Colossus does not trigger off its own casting
# --------------------------------------------------------------------------

def test_diregraf_does_not_self_trigger():
    """Casting Diregraf itself: colossus_active is the pre-cast state (False), so
    no 2/2 token even though the deploy loop has already set self.colossus=True."""
    t = _cos_trial()
    zombie = rec(cmc=3, type_line="Creature — Zombie Giant")
    t.new_z = 0
    t.colossus = True                                  # flag set for THIS card
    t.cast_zombie_spell(zombie, colossus_active=False)  # ...but it wasn't in play yet
    assert t.new_z == 1                                # just itself, no self-token


def test_diregraf_tokens_for_later_zombie_spells():
    """Once Colossus is on the battlefield, the NEXT zombie spell makes a token."""
    t = _cos_trial()
    zombie = rec(cmc=2, type_line="Creature — Zombie")
    t.new_z = 0
    t.cast_zombie_spell(zombie, colossus_active=True)
    assert t.new_z == 2                                # the zombie + the Colossus token
