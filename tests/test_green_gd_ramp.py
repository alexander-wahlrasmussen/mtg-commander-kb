"""Regression tests for the gd-family land-ramp mana-refund bug.

CODEBASE BUG AUDIT 2026-06-29 (🟢 lower-impact / latent):
  gd_ramp_lab.py:79 and gd_combo_lab.py:120 cast a one-shot land-ramp spell, then
  reset `g.avail = g.lands + g.rock_out`. Because Goldfish.cast() ALREADY pays the
  cost (`self.avail -= c`), that reset line REFUNDED the spell's cost (and, since
  g.lands was just bumped, also counted the freshly-fetched TAPPED land this turn)
  — so every land-ramp spell chained for free in one turn.

  Card text (card_lookup 2026-06-24 / Cultivate verified 2026-06-29): a {2}{G}
  Cultivate-style ramp costs 3 and puts the fetched basic onto the battlefield
  TAPPED — it must cost mana THIS turn and only add a land NEXT turn.

The fix dropped the reset line in both Goldfish-based labs. gd_speed_lab.py never
used Goldfish/land-ramp (the audit's gd_speed_lab.py:204 reference was inaccurate),
so it has nothing to fix — guarded below anyway so the copy-paste can't reappear.

Hermetic: synthetic Goldfish + a toy library (no 168 MB Scryfall bulk).
"""
from pathlib import Path

import gd_ramp_lab
import gd_combo_lab
from helpers import rec, toy_library

# The labs share the same Goldfish via speed_lab_core; use the exact class & config
# the lab runs so this test pins the real code path, not a copy.
Goldfish = gd_ramp_lab.core.Goldfish
SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"

CULTIVATE = ("Cultivate", rec(cmc=3.0, type_line="Sorcery", color_identity=("G",)))


def _fresh_goldfish():
    """A Goldfish in a controlled state: a land-ramp spell in hand, 3 lands of
    untapped mana available, no rocks. (We overwrite the random opening hand.)"""
    import random
    g = Goldfish(toy_library(), random.Random(0))
    g.hand = [CULTIVATE]
    g.lands = 3
    g.rock_out = 0
    g.avail = g.lands + g.rock_out      # 3 untapped mana this turn
    return g


def _run_landramp_step(g, land_ramp):
    """The labs' one-shot land-ramp loop body (post-fix): cast cheapest-first,
    each fetched land enters TAPPED (lands += 1), cast() pays the cost. No
    avail reset. Mirrors gd_ramp_lab.reach_turns / gd_combo_lab.assemble_turn."""
    moved = True
    while moved:
        moved = False
        for nm, cost in sorted(land_ramp.items(), key=lambda x: x[1]):
            if g.has(nm) and g.avail >= cost:
                g.cast(nm, cost)
                g.lands += 1
                moved = True
                break


# --------------------------------------------------------------------------- #
# the primitive the fix relies on: cast() spends mana
# --------------------------------------------------------------------------- #
def test_cast_decrements_avail():
    # The whole fix rests on this: cast() already pays, so the reset line was a
    # pure refund. If cast() ever stops decrementing, the reset would be needed.
    g = _fresh_goldfish()
    assert g.cast("Cultivate", 3) is True
    assert g.avail == 0          # 3 - 3, NOT refunded back to 3
    assert not g.has("Cultivate")


# --------------------------------------------------------------------------- #
# the headline assertion: a {2}{G} ramp at avail=3 spends ~all mana + +1 land
# --------------------------------------------------------------------------- #
def test_landramp_step_spends_mana_and_taps_the_land():
    g = _fresh_goldfish()
    _run_landramp_step(g, {"Cultivate": 3})
    assert g.avail == 0          # the spell COST mana this turn (was wrongly 3+1=4)
    assert g.lands == 4          # +1 land, but it entered TAPPED -> no same-turn mana
    assert not g.has("Cultivate")


def test_landramp_does_not_chain_for_free():
    # Two {2}{G} ramps with only 3 mana: the second is UNAFFORDABLE after the
    # first (avail hits 0). Under the bug both fired (each refunded its own cost).
    g = _fresh_goldfish()
    g.hand = [("Cultivate", CULTIVATE[1]), ("Kodama's Reach", rec(cmc=3.0, type_line="Sorcery"))]
    _run_landramp_step(g, {"Cultivate": 3, "Kodama's Reach": 3})
    assert g.lands == 4          # exactly ONE ramp resolved (not both)
    assert g.avail == 0
    # the unaffordable second spell stayed in hand
    assert g.has("Cultivate") ^ g.has("Kodama's Reach")


def test_old_refund_line_would_overcount():
    # Document the bug: the removed line `g.avail = g.lands + g.rock_out` (run
    # AFTER cast paid + lands bumped) leaves avail = 4 = the start 3 (cost refunded)
    # plus the tapped land — proving the reset both refunded and over-counted.
    g = _fresh_goldfish()
    g.cast("Cultivate", 3)
    g.lands += 1
    buggy_avail = g.lands + g.rock_out     # what the deleted line recomputed
    assert buggy_avail == 4                # vs the correct 0
    assert buggy_avail != g.avail          # the fix (g.avail) stays at 0


# --------------------------------------------------------------------------- #
# copy-paste guard: the refund line must not reappear in ANY gd-family lab
# --------------------------------------------------------------------------- #
def test_no_landramp_refund_in_gd_labs():
    refund = "g.avail = g.lands + g.rock_out"
    for fn in ("gd_ramp_lab.py", "gd_combo_lab.py", "gd_speed_lab.py"):
        src = (SCRIPTS / fn).read_text(encoding="utf-8")
        assert refund not in src, f"{fn} reintroduced the land-ramp mana refund"


def test_lab_landramp_costs_are_real():
    # Tie the test to the lab's actual config: every modelled land-ramp costs >=2
    # (Cultivate-class), so casting one always reduces a <=that-turn mana pool.
    for land_ramp in (gd_ramp_lab.LAND_RAMP, gd_combo_lab.LAND_RAMP):
        assert land_ramp, "land-ramp set should be non-empty"
        assert all(cost >= 2 for cost in land_ramp.values())
