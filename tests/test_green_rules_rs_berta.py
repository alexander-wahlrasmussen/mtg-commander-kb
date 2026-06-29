"""REGRESSION (2026-06-29 codebase audit, 🟢 lower-impact rules nits — rs/berta cluster).

Two secondary-line summoning-sickness bugs, both about a creature acting the turn it
enters (no haste):

  * rs_clock_lab.goldfish_kill — The Wise Mothman (3/3, no haste) was added straight to
    `board`/`ncre` on its deploy turn, so a freshly-cast Mothman *swung* the same turn:
    its 3 combat power fed `hit_focus` and the per-turn ATTACK rad counter fired
    immediately (`if mothman and T > 1`). The ETB rad legitimately fires on entry; the
    ATTACK does not. Fixed: route Mothman through `new_board`/`new_cre` like every other
    creature here (combat online next turn) and gate the attack rad on `T > mothman_turn`.
    Published clock is unmoved (decap T7 / table T10 hold) — this only delays the front edge.

  * berta_clock_lab.Trial — the infinite-mana lines tap a creature with a {T}/{Q} mana
    ability (Bloom Tender's Vivid, Selvala's {G}{T}, Berta's {X}{T}). The gates keyed on
    `name in self.bf`, which is true the instant the dork is cast, so the combo CLOSED the
    turn the dork entered. Fixed: snapshot the board at the top of each turn (`self.unsick`)
    and gate every tapping line on the creature having been present since before this turn.
    The aura/untapper half may still be cast the same turn (no sickness on enchantments).

Hermetic: no Scryfall bulk — pure-function asserts on the lab internals using toy records.
"""
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import rs_clock_lab as RS          # noqa: E402
import berta_clock_lab as B        # noqa: E402
from helpers import land, rec, toy_library   # noqa: E402


# --------------------------------------------------------------------------- RS

def _pure_land_lib(n=60):
    """A library whose ONLY creature is the command-zone Mothman: 60 lands, no
    spells. Every hand is 7 lands, a land drops each turn, so Mothman (4 mana)
    deploys on T4 in every trial — a clean, rng-robust entry turn."""
    return [("Island", land()) for _ in range(n)]


def test_mothman_is_the_only_creature_and_comes_from_the_command_zone():
    """Premise guard: the kill-shape under test relies on Mothman being the sole
    attacker, deployed from the command zone (it is never in the library)."""
    lib = _pure_land_lib()
    assert not any("creature" in r["type_line"].lower() for _, r in lib)


def test_rs_mothman_does_not_attack_the_turn_it_enters():
    """A freshly-deployed Mothman must NOT swing on its entry turn (no haste).

    The ETB rad counter (a player counter) legitimately fires on entry -> the rad
    DRAIN (`hit_all`) starts the entry turn. Combat (`hit_focus`, board power) must
    wait at least one turn. So the first combat turn is strictly after the first
    drain turn. Under the bug both fired on the same (entry) turn."""
    captured = []

    class _Spy(RS.slc.Table):
        def __init__(self, *a, **k):
            super().__init__(*a, **k)
            self.focus, self.alls = [], []
            captured.append(self)

        def hit_focus(self, x, T):
            self.focus.append(T)
            super().hit_focus(x, T)

        def hit_all(self, x, T):
            self.alls.append(T)
            super().hit_all(x, T)

    orig = RS.slc.Table
    RS.slc.Table = _Spy
    try:
        RS.goldfish_kill(_pure_land_lib(), "The Wise Mothman", None, {},
                         random.Random(20260613))
    finally:
        RS.slc.Table = orig

    tbl = captured[-1]
    assert tbl.alls, "ETB rad drain (hit_all) should fire on Mothman's entry turn"
    assert tbl.focus, "Mothman should attack (hit_focus) on a later turn"
    assert min(tbl.focus) > min(tbl.alls), (
        f"combat began T{min(tbl.focus)} but Mothman entered ~T{min(tbl.alls)} "
        "— a summoning-sick Mothman swung the turn it entered")


# ------------------------------------------------------------------------- Berta

def _berta_trial():
    return B.Trial(toy_library(), random.Random(1), {})


def test_berta_infinite_requires_an_unsick_tapper():
    """Direct gate check: Bloom Tender + Freed from the Real + Walking Ballista all
    on the battlefield is NOT a combo while Bloom Tender is summoning sick (absent
    from `unsick`); it IS once Bloom Tender is unsick."""
    tr = _berta_trial()
    tr.bf = {"Bloom Tender", "Freed from the Real", "Walking Ballista"}
    tr.unsick = set()                       # Bloom Tender entered THIS turn -> sick
    assert tr.infinite(5) is False, "combo fired off a summoning-sick Bloom Tender"
    assert not tr.tbl.done
    tr.unsick = {"Bloom Tender"}            # survived to a later turn -> may tap
    assert tr.infinite(6) is True, "combo should fire once Bloom Tender can tap"


def test_berta_combo_cannot_close_the_turn_its_dork_enters():
    """End-to-end: with Bloom Tender + Freed + Ballista in hand and ample mana, the
    turn Bloom Tender is cast must NOT close (sick); the very next turn must."""
    tr = _berta_trial()
    tr.berta = True                         # Berta already online (not the gate here)
    g = tr.g
    g.lands = 12
    g.hand = [("Bloom Tender", rec(cmc=2, type_line="Creature — Elf Druid")),
              ("Freed from the Real", rec(cmc=3, type_line="Enchantment — Aura")),
              ("Walking Ballista", rec(cmc=2, type_line="Artifact Creature"))]

    tr.turn(1)
    assert "Bloom Tender" in tr.bf, "Bloom Tender should deploy on turn 1"
    assert not tr.tbl.done, "combo closed the turn Bloom Tender entered (sick tap)"

    tr.turn(2)
    assert tr.tbl.done, "combo should close the turn after Bloom Tender enters"
    assert tr.tbl.table == 2
