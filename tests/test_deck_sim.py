"""Tier-1 tests for deck_sim.py — the consistency/assembly simulator core.

Mix of plain unit, property-based (Hypothesis), and explicit REGRESSION tests.
A test tagged REGRESSION pins a bug that already shipped a wrong conclusion;
deleting it re-opens that hole. The discipline (Backlog #9): every retraction in
memory earns a test that turns the bug red forever.
"""
import random
import string

import pytest
from hypothesis import given, strategies as st

import deck_sim
from helpers import rec, land, toy_library


# --------------------------------------------------------------------------- #
# is_land / is_pure_land
# --------------------------------------------------------------------------- #
def test_pure_land():
    assert deck_sim.is_land(land()) is True
    assert deck_sim.is_pure_land(land()) is True


def test_mdfc_land_back_is_a_land_but_not_pure():
    # A creature // land MDFC can be PLAYED as a land but doesn't always enter as one.
    mdfc = rec(type_line="Creature — Elf", face_types=["Creature — Elf", "Land"])
    assert deck_sim.is_land(mdfc) is True
    assert deck_sim.is_pure_land(mdfc) is False


def test_nonland_is_not_a_land():
    assert deck_sim.is_land(rec(type_line="Instant")) is False


# --------------------------------------------------------------------------- #
# colour model — the Grand Design "39%" class of bug
# --------------------------------------------------------------------------- #
def test_printed_land_colors_prefers_produced_mana_REGRESSION():
    # REGRESSION (project_grand_design_mana_pass / colour-divide retraction):
    # fetches & rainbow lands have EMPTY color_identity but DO produce colours.
    # Reading color_identity scored them zero -> Grand Design read 39% vs 89%.
    rainbow = rec(type_line="Land", color_identity=(), produced_mana=tuple("WUBRG"))
    assert deck_sim.printed_land_colors(rainbow) == set("WUBRG")


def test_printed_land_colors_falls_back_to_identity_when_no_produced():
    dual = rec(type_line="Land", color_identity=("W", "U"), produced_mana=())
    assert deck_sim.printed_land_colors(dual) == {"W", "U"}


def test_printed_land_colors_filters_colorless():
    # {C} is not a WUBRG colour and must not count toward colour fixing.
    src = rec(type_line="Land", color_identity=(), produced_mana=("C", "U"))
    assert deck_sim.printed_land_colors(src) == {"U"}


def test_land_color_map_resolves_typed_fetch_REGRESSION():
    # REGRESSION: a sac-fetch (empty produced_mana/identity) must resolve to the
    # union of the deck's OWN fetchable basics, not to nothing.
    lib = [
        ("Polluted Delta", rec(type_line="Land")),          # fetches island/swamp
        ("Island", land(produced=("U",), basic_type="Island")),
        ("Swamp", land(produced=("B",), basic_type="Swamp")),
        ("Grizzly Bears", rec(type_line="Creature — Bear")),
    ]
    cmap = deck_sim.land_color_map(lib)
    assert cmap["polluted delta"] == {"U", "B"}


# --------------------------------------------------------------------------- #
# keep_hand — the default land-count band (2..5)
# --------------------------------------------------------------------------- #
def _hand(n_lands, n_spells):
    h = [("Land", land()) for _ in range(n_lands)]
    h += [("Spell", rec(cmc=2)) for _ in range(n_spells)]
    return h


@pytest.mark.parametrize("lands,keep", [
    (0, False), (1, False), (2, True), (3, True), (4, True), (5, True),
    (6, False), (7, False),
])
def test_keep_hand_land_band(lands, keep):
    assert deck_sim.keep_hand(_hand(lands, 7 - lands)) is keep


@given(st.integers(min_value=0, max_value=7))
def test_keep_hand_band_property(n_lands):
    deck_sim.set_keep_spec(None)   # @given runs the autouse fixture once, not per example
    assert deck_sim.keep_hand(_hand(n_lands, 7 - n_lands)) == (2 <= n_lands <= 5)


# --------------------------------------------------------------------------- #
# parse_deck — round-trip count, sideboard exclusion, commander to the zone
# --------------------------------------------------------------------------- #
def _write_deck(tmp_path, stem, lines):
    p = tmp_path / f"{stem}.txt"
    p.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return p


def test_parse_deck_excludes_sideboard_REGRESSION(tmp_path):
    # REGRESSION (Backlog #8.A.1 singleton over-count): cards after SIDEBOARD
    # must NOT enter the parsed main deck.
    path = _write_deck(tmp_path, "no-such-deck-stem", [
        "1 Alpha", "2 Beta", "SIDEBOARD:", "3 Gamma",
    ])
    index = {"alpha": rec(), "beta": rec(), "gamma": rec()}
    library, commander, diag = deck_sim.parse_deck(path, index)
    names = [n for n, _ in library]
    assert "Gamma" not in names
    assert sorted(names) == ["Alpha", "Beta", "Beta"]
    assert diag["library_size"] == 3


def test_parse_deck_pulls_commander_to_command_zone(tmp_path):
    # stem prefixes a real registry key -> its commander is pulled from the 99.
    path = _write_deck(tmp_path, "the-genome-project-20990101", [
        "1 Kuja, Genome Sorcerer", "1 Island", "1 Mountain",
    ])
    index = {"kuja, genome sorcerer": rec(), "island": land(), "mountain": land(("R",), "Mountain")}
    library, commander, diag = deck_sim.parse_deck(path, index)
    assert commander == "Kuja, Genome Sorcerer"
    assert diag["commander_in_main"] is True
    assert "Kuja, Genome Sorcerer" not in [n for n, _ in library]
    assert diag["library_size"] == 2


def test_parse_deck_resolves_reskin_alias(tmp_path, monkeypatch):
    path = _write_deck(tmp_path, "no-such-deck-stem", ["1 Morgul-Knife"])
    index = {"shadowspear": rec()}
    aliases = {"morgul-knife": "Shadowspear"}
    library, _, diag = deck_sim.parse_deck(path, index, aliases)
    assert diag["unresolved"] == []
    assert any("Morgul-Knife -> Shadowspear" in a for a in diag["aliased"])
    assert library[0][1] is index["shadowspear"]


_names = st.text(alphabet=string.ascii_letters, min_size=1, max_size=8)


@given(st.dictionaries(_names, st.integers(min_value=1, max_value=9), min_size=1, max_size=12))
def test_parse_deck_roundtrip_count(deck):
    # Property: every "N CardName" line expands to exactly N library entries
    # (no commander in this stem), regardless of oracle resolution.
    import tempfile
    from pathlib import Path
    lines = [f"{q} {nm}" for nm, q in deck.items()]
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "no-such-deck-stem.txt"
        p.write_text("\n".join(lines) + "\n", encoding="utf-8")
        library, commander, diag = deck_sim.parse_deck(p, {})
    assert commander is None
    assert diag["library_size"] == sum(deck.values())


# --------------------------------------------------------------------------- #
# simulate — deterministic simulation testing (same seed -> identical output)
# --------------------------------------------------------------------------- #
def test_simulate_is_deterministic_for_a_fixed_seed():
    lib = toy_library()
    a = deck_sim.simulate(lib, ["U"], turns=8, trials=400, rng=random.Random(42))
    b = deck_sim.simulate(lib, ["U"], turns=8, trials=400, rng=random.Random(42))
    assert a == b


def test_simulate_lands_curve_is_nondecreasing():
    lib = toy_library()
    stats = deck_sim.simulate(lib, ["U"], turns=8, trials=400, rng=random.Random(1))
    curve = [stats["lands_by_turn"][t] for t in range(1, 9)]
    assert curve == sorted(curve)   # you never have fewer lands in play next turn


# --------------------------------------------------------------------------- #
# load_reskin_aliases — table parsing
# --------------------------------------------------------------------------- #
def test_load_reskin_aliases_parses_table(tmp_path, monkeypatch):
    doc = tmp_path / "aliases.md"
    doc.write_text(
        "| Reskin Name | Original |\n"
        "|---|---|\n"
        "| Morgul-Knife | Shadowspear |\n"
        "| Wise Mothman | The Wise Mothman |\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(deck_sim, "ALIASES_DOC", doc)
    aliases = deck_sim.load_reskin_aliases()
    assert aliases["morgul-knife"] == "Shadowspear"
    assert aliases["wise mothman"] == "The Wise Mothman"
    assert "reskin name" not in aliases   # header row skipped
