"""Tier-1 tests for keep_spec.tutor_bridges — the tutor-bridge check from the
2026-07-03 keep-spec re-tune (Mulligan_Strategy_Audit §7.3).

RANGER_CAPTAIN_REGRESSION: Replication's FINDING keep counted Ranger-Captain of
Eos as a finder although it fetches only creatures with mana value <= 1 — nothing
in the combo package qualifies (the deck's own lab docstring says so). A tutor
that can fetch NO key card must be dropped from the tutors bucket; unparsable
search clauses fail OPEN (generic tutors like Demonic stay).

Hermetic: synthetic Scryfall-shaped card dicts, no oracle bulk.
"""
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def _load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ks = _load("keep_spec")


def _card(text="", type_line="Creature", cmc=0, colors=(), power=None, toughness=None):
    c = {"oracle_text": text, "type_line": type_line, "cmc": cmc, "colors": list(colors)}
    if power is not None:
        c["power"] = power
    if toughness is not None:
        c["toughness"] = toughness
    return c


RANGER_CAPTAIN = _card("When this creature enters, you may search your library for a "
                       "creature card with mana value 1 or less, reveal it, put it into "
                       "your hand, then shuffle.")
IMPERIAL = _card("When this creature enters, search your library for a creature card "
                 "with power 2 or less, reveal it, put it into your hand, then shuffle.")
DEMONIC = _card("Search your library for a card, put that card into your hand, then "
                "shuffle.", type_line="Sorcery")
ENLIGHTENED = _card("Search your library for an artifact or enchantment card, reveal "
                    "that card, and put it into your hand.", type_line="Instant")
GSZ = _card("Search your library for a green creature card with mana value X or less.",
            type_line="Sorcery")
CONDUIT = _card("When you cast this spell, you may search your library for a colorless "
                "creature card with mana value 7 or greater.")

LIGHTNING_RUNNER = _card(type_line="Creature — Human Warrior", cmc=5, colors="R",
                         power="2", toughness="2")
SWORD = _card(type_line="Artifact — Equipment", cmc=3)
CRATERHOOF = _card(type_line="Creature — Beast", cmc=8, colors="G",
                   power="5", toughness="5")
CELLARSPAWN = _card(type_line="Enchantment Creature — Horror", cmc=3, colors="B",
                    power="3", toughness="3")


def test_ranger_captain_bridges_to_nothing_REGRESSION():
    assert ks.tutor_bridges(RANGER_CAPTAIN, [SWORD, LIGHTNING_RUNNER]) is False


def test_imperial_recruiter_bridges_to_lightning_runner():
    # power 2 satisfies "power 2 or less" — the primary-line finder counts.
    assert ks.tutor_bridges(IMPERIAL, [SWORD, LIGHTNING_RUNNER]) is True
    assert ks.tutor_bridges(IMPERIAL, [SWORD, CRATERHOOF]) is False


def test_generic_tutor_fails_open():
    assert ks.tutor_bridges(DEMONIC, [SWORD]) is True


def test_type_restriction():
    assert ks.tutor_bridges(ENLIGHTENED, [SWORD]) is True          # artifact ok
    assert ks.tutor_bridges(ENLIGHTENED, [LIGHTNING_RUNNER]) is False   # creature only


def test_color_restriction_and_x_cost():
    # GSZ: "green creature, MV X or less" — X is unbounded (unparsed), colour bites.
    assert ks.tutor_bridges(GSZ, [CRATERHOOF]) is True
    assert ks.tutor_bridges(GSZ, [CELLARSPAWN]) is False           # black creature


def test_colorless_and_mv_greater():
    assert ks.tutor_bridges(CONDUIT, [CRATERHOOF]) is False        # green -> not colorless
    kozilek = _card(type_line="Legendary Creature — Eldrazi", cmc=10, colors=())
    assert ks.tutor_bridges(CONDUIT, [kozilek]) is True


def test_no_key_records_keeps_all_tutors():
    assert ks.tutor_bridges(RANGER_CAPTAIN, []) is True


def test_monocolored_is_not_the_color_red_REGRESSION():
    # "monocolored" contains the substring "red" — a plain substring test read a
    # phantom {R} constraint and dropped Emergent Ultimatum from Croak's tutors.
    emergent = _card("search your library for up to three monocolored cards with "
                     "different names and exile them.", type_line="Sorcery")
    citadel = _card(type_line="Legendary Artifact", cmc=6, colors="B")
    assert ks.tutor_bridges(emergent, [citadel]) is True
