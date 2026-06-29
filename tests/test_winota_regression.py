"""REGRESSION (2026-06-29 codebase audit, the one 🔴 critical): winota_clock_lab
clocked a Winota deck WITHOUT Winota.

She is the COMMANDER — deck_sim loads only the 99-card library, so she is never in
g.hand — but the only code that set self.winota=True checked `nm == WINOTA` in hand.
Dead code (verified True in 0/3000 trials): the whole flood engine (non-Human attack
-> dig 6 -> flood a Human in attacking) never fired, so the headline clock read far
too SLOW (decap T8-9 / table T13-14 -> the real T6-7 decap / T9-10 table once the
engine is live). This pins the command-zone deploy: self.winota must flip True from
the command zone, never from a hand the card can't reach.
"""
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import winota_clock_lab as W
from helpers import land, rec


def _land_rich_library(n_land=60, n_bear=39):
    """parse_deck-shaped library: pure lands + non-Human attackers (Bears).
    Winota is NOT here — she's the commander; the whole point is she still deploys."""
    lib = [("Plains", land(produced=("W",), basic_type="Plains")) for _ in range(n_land)]
    lib += [(f"Bear{i}", rec(cmc=2, type_line="Creature — Bear", power="2"))
            for i in range(n_bear)]
    return lib


def test_commander_not_in_library():
    """Guards the premise: the engine must fire even though the card the old branch
    looked for is unreachable from hand/library."""
    assert not any(nm == W.WINOTA for nm, _ in _land_rich_library())


def test_winota_deploys_from_command_zone():
    """Across trials, self.winota flips True by the time 4 mana is online — even
    though WINOTA never enters the library/hand. Under the bug this was 0/N."""
    lib = _land_rich_library()
    trials = 60
    fired = 0
    for s in range(trials):
        tr = W.Trial(lib, random.Random(1000 + s), haste=False)
        for T in range(1, 9):
            tr.turn(T)
        if tr.winota:
            fired += 1
    # A 60/99-land deck reaches 4 mana well before T8 in every reasonable draw.
    assert fired == trials, f"command-zone deploy fired in only {fired}/{trials} trials"


def test_winota_engine_floods_humans():
    """With Humans in the library and non-Human attackers on board, the live engine
    must pull Humans out of the flood pool (humans_left decreases). Under the bug
    self.winota stayed False so _p_hit was never consulted and the pool never moved."""
    lib = [("Plains", land(produced=("W",), basic_type="Plains")) for _ in range(40)]
    lib += [(f"Bear{i}", rec(cmc=2, type_line="Creature — Bear", power="2")) for i in range(29)]
    lib += [(f"Soldier{i}", rec(cmc=1, type_line="Creature — Human Soldier", power="1"))
            for i in range(30)]
    moved = 0
    trials = 60
    for s in range(trials):
        tr = W.Trial(lib, random.Random(7000 + s), haste=False)
        start_humans = tr.humans_left
        for T in range(1, 11):
            tr.turn(T)
        if tr.winota and tr.humans_left < start_humans:
            moved += 1
    assert moved >= trials // 2, f"flood pool moved in only {moved}/{trials} trials"
