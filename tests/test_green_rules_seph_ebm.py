"""REGRESSION (2026-06-29 codebase audit, 🟢 lower-impact rules nits — cluster rules-seph-ebm).

Two SECONDARY-line rules nits in the Sephiroth + Earthbend-the-Meta clock labs. Both were
investigated; both turned out to be NOT clock-neutral to actually fix, so per the sweep's
CLOCK-NEUTRAL-OR-ESCALATE rule they are DOCUMENTED-as-accepted (code comments) and the precise
fix is escalated to a coordinated clock re-derivation. This test pins the verified card facts
and guards the modeled/not-modeled state so the escalation can't silently rot.

  * sephiroth_clock_lab.py — Mikaeus, the Unhallowed (card_lookup 2026-06-29): "Other non-Human
    creatures you control get +1/+1 and have undying." Humans are EXPLICITLY EXCLUDED. The
    Mikaeus undying line (`_line_a`) uses a coarse `self.bodies >= 2` proxy that over-counts the
    deck's Human creatures (Yawgmoth itself, Zulaport Cutthroat, Syr Konrad, Ghoulcaller Gisa)
    as undying fodder. Tightening it to a non-Human count was MEASURED to move the PUBLISHED
    house-legal median T12 -> T13 (40k goldfish) -> ESCALATED, not applied. is_human() is kept
    correct so the deferred fix has a verified classifier; this test pins it.

  * ebm_clock_lab.py — Scute Swarm (card_lookup 2026-06-29): "Landfall — create a 1/1 Insect, or
    at 6+ lands a COPY of this creature instead" -> exponential. The lab models the LINEAR +1
    Insect/landfall but leaves the EXPONENTIAL self-copy INERT (self.scutes is never seeded, so
    the `>= 6 and self.scutes` branch is dead). Seeding it flips EBM's borderline PUBLISHED table
    median (T11<->T12 across trial counts) -> ESCALATED. This test guards the inert state.

All card text verified via scripts/card_lookup.py 2026-06-29. Hermetic: toy library + synthetic
records only (no Scryfall bulk).
"""
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import sephiroth_clock_lab as seph   # noqa: E402
import ebm_clock_lab as ebm          # noqa: E402
from helpers import rec, toy_library  # noqa: E402


# Verified type lines (scripts/card_lookup.py 2026-06-29). NOTE the em-dash (U+2014):
# is_human() splits the type line on it.
HUMANS = {
    "Yawgmoth, Thran Physician": "Legendary Creature — Human Cleric",
    "Zulaport Cutthroat": "Creature — Human Rogue Ally",
    "Syr Konrad, the Grim": "Legendary Creature — Human Knight",
    "Ghoulcaller Gisa": "Legendary Creature — Human Wizard",
}
NON_HUMANS = {
    "Mikaeus, the Unhallowed": "Legendary Creature — Zombie Cleric",
    "Blood Artist": "Creature — Vampire",
    "Geralf's Messenger": "Creature — Zombie",
    "Faerie Rogue token": "Creature — Faerie Rogue",     # Bitterblossom
    "Zombie Army token": "Creature — Zombie Army",        # Dreadhorde Invasion / amass
}


def gets_mikaeus_undying(record):
    """The predicate Mikaeus, the Unhallowed actually applies: a creature you control that
    is NOT Human (the corrected gate the escalated _line_a fix would wire in)."""
    return seph.is_creature(record) and not seph.is_human(record)


# --------------------------------------------------------------------------
# Sephiroth — Mikaeus does not pump / grant undying to Humans
# --------------------------------------------------------------------------

def test_is_human_flags_the_excluded_humans():
    for name, tl in HUMANS.items():
        assert seph.is_human(rec(type_line=tl)), name
    for name, tl in NON_HUMANS.items():
        assert not seph.is_human(rec(type_line=tl)), name


def test_mikaeus_grants_no_undying_to_humans():
    """A Human creature gets NO +1/+1 / undying from Mikaeus; non-Humans do."""
    for name, tl in HUMANS.items():
        assert not gets_mikaeus_undying(rec(type_line=tl)), f"{name} must be excluded"
    for name, tl in NON_HUMANS.items():
        assert gets_mikaeus_undying(rec(type_line=tl)), f"{name} should get undying"
    # a non-creature (e.g. Bastion of Remembrance enchantment) is never a Mikaeus target
    assert not gets_mikaeus_undying(rec(type_line="Enchantment"))


def test_seph_line_a_overcount_is_the_documented_escalated_state():
    """CHANGE-DETECTOR for the accepted over-count. With Yawgmoth (Human) + Mikaeus (the
    grant SOURCE, not undying itself) and ZERO real non-Human fodder, the coarse
    `self.bodies >= 2` proxy still fires line A. The precise non-Human model would NOT fire
    here -> applying it moves the published median T12->T13, so it stays escalated. If this
    assertion flips, the published Sephiroth clock must be re-derived (proposal + JSON)."""
    t = seph.Trial(toy_library(), random.Random(0))
    t.inplay = {"Yawgmoth, Thran Physician", "Mikaeus, the Unhallowed"}
    t.seph = True            # commander drain online
    t.undying = 0            # no printed-undying fodder
    t.bodies = 2             # Yawgmoth + Mikaeus — NEITHER is valid undying fodder
    assert t._line_a() is True
    # documents the corrected target: there are zero non-Human FODDER bodies here, so the
    # escalated fix (nonhuman-fodder gate) would make this False.


# --------------------------------------------------------------------------
# EBM — Scute Swarm exponential is intentionally INERT (linear path modeled)
# --------------------------------------------------------------------------

def _ebm_trial():
    return ebm.Trial(toy_library(), random.Random(0))


def test_scute_exponential_is_inert_linear_path_modeled():
    """Guard the modeled/not-modeled state. With Scute Swarm out and 6+ lands, the
    EXPONENTIAL copy branch is dead because self.scutes is never seeded (stays 0); only the
    LINEAR +1 Insect/landfall is modeled."""
    t = _ebm_trial()
    t.bf = {"Scute Swarm"}
    t.scutes = 0
    t.tokens = 0
    t.g.lands = 6                       # 6+ lands -> copy mode WOULD be active if seeded
    entered = t.landfall(8)
    assert t.scutes == 0               # exponential NEVER fired (engine inert)
    assert t.tokens == 1               # linear: one 1/1 Insect from the landfall
    assert entered == 1


def test_scute_exponential_capability_is_dormant_not_broken():
    """Documents that the engine is dormant by SEEDING, not structurally broken: once
    self.scutes >= 1 the copy branch WOULD compound (this is exactly the escalated wiring,
    asserted here only to show why it moves the clock — it is NOT done in the lab)."""
    t = _ebm_trial()
    t.bf = {"Scute Swarm"}
    t.scutes = 1                        # hypothetical seed (NOT what the lab does)
    t.tokens = 0
    t.g.lands = 6
    t.landfall(8)
    assert t.scutes == 2               # one copy per existing Scute -> exponential growth
