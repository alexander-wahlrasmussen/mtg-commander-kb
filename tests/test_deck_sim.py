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
# simulate_flow — the smoothness / tempo pass (2026-07-03)
# --------------------------------------------------------------------------- #
def test_simulate_flow_is_deterministic_for_a_fixed_seed():
    lib = toy_library()
    a = deck_sim.simulate_flow(lib, turns=8, trials=400, rng=random.Random(7))
    b = deck_sim.simulate_flow(lib, turns=8, trials=400, rng=random.Random(7))
    assert a == b


def test_simulate_flow_turn_partition_sums_to_100():
    # Every turn is exactly one of live / dead-starved / dead-flooded, so the three
    # rates must sum to 100% at each turn (the taxonomy has no gaps or overlaps).
    lib = toy_library()
    flow = deck_sim.simulate_flow(lib, turns=8, trials=800, rng=random.Random(3))
    for t in range(1, 9):
        total = (flow["live_by_turn"][t] + flow["starved_by_turn"][t]
                 + flow["flooded_by_turn"][t])
        assert total == pytest.approx(100.0)


def test_simulate_flow_all_lands_is_never_live():
    # A deck of pure lands can never cast a nonland: 0% live, and every dead turn is
    # 'flooded' (no nonland to cast), never 'starved' (which needs a stuck spell).
    lib = [("Island", land()) for _ in range(60)]
    flow = deck_sim.simulate_flow(lib, turns=6, trials=200, rng=random.Random(9))
    for t in range(1, 7):
        assert flow["live_by_turn"][t] == 0.0
        assert flow["plan_live_by_turn"][t] == 0.0
        assert flow["starved_by_turn"][t] == 0.0
        assert flow["flooded_by_turn"][t] == pytest.approx(100.0)


def test_simulate_flow_expensive_spells_read_as_starved_not_flooded():
    # Cheap lands but only 9-drops: early turns have a spell stuck in hand with too
    # little mana -> classified 'starved' (mana screw), not 'flooded'.
    lib = [("Island", land()) for _ in range(20)]
    lib += [(f"Bomb{i}", rec(cmc=9, type_line="Creature")) for i in range(40)]
    flow = deck_sim.simulate_flow(lib, turns=4, trials=300, rng=random.Random(11))
    # By T4 (<=4 lands) a 9-drop is uncastable; whenever a bomb is in hand it's starved.
    assert flow["starved_by_turn"][3] > flow["flooded_by_turn"][3]
    assert flow["live_by_turn"][3] == 0.0


def test_simulate_flow_plan_live_never_exceeds_any_live():
    # plan-live is a subset of live (a plan play is a play), so it can't be higher.
    lib = toy_library()
    plan = {"spell0", "spell1", "spell2"}   # only a few nonlands are plan-tagged
    flow = deck_sim.simulate_flow(lib, turns=8, trials=600, rng=random.Random(5), plan_set=plan)
    assert flow["has_plan_spec"] is True
    for t in range(1, 9):
        assert flow["plan_live_by_turn"][t] <= flow["live_by_turn"][t] + 1e-9


def test_simulate_flow_no_plan_set_makes_plan_equal_any():
    # Without a keep-spec, every nonland counts as plan-relevant -> the two curves match.
    lib = toy_library()
    flow = deck_sim.simulate_flow(lib, turns=8, trials=600, rng=random.Random(5), plan_set=None)
    assert flow["has_plan_spec"] is False
    for t in range(1, 9):
        assert flow["plan_live_by_turn"][t] == flow["live_by_turn"][t]


def test_simulate_flow_one_spend_empties_slower_than_greedy():
    # 'one' casts a single spell/turn; 'greedy' dumps everything affordable. With a
    # cheap castable curve, greedy must leave a SMALLER hand (it deploys more).
    lib = [("Island", land()) for _ in range(24)]
    lib += [(f"One{i}", rec(cmc=1, type_line="Creature")) for i in range(36)]
    greedy = deck_sim.simulate_flow(lib, turns=8, trials=500, rng=random.Random(4), spend="greedy")
    one = deck_sim.simulate_flow(lib, turns=8, trials=500, rng=random.Random(4), spend="one")
    assert one["hand_size_by_turn"][8] > greedy["hand_size_by_turn"][8]
    assert one["hellbent_by_turn"][8] <= greedy["hellbent_by_turn"][8]


def test_simulate_flow_one_spend_still_partitions_to_100():
    # The live/starved/flooded taxonomy must hold under the 'one' policy too.
    lib = toy_library()
    flow = deck_sim.simulate_flow(lib, turns=8, trials=600, rng=random.Random(6), spend="one")
    for t in range(1, 9):
        total = (flow["live_by_turn"][t] + flow["starved_by_turn"][t]
                 + flow["flooded_by_turn"][t])
        assert total == pytest.approx(100.0)


def test_simulate_flow_spending_empties_hand_faster_than_consistency_pass():
    # The tempo pass REMOVES cast cards; a hand of castable 1-drops should shrink,
    # unlike simulate() which never spends. Hand size must fall below the raw
    # draw-only ceiling (7 opening - 1 land drop + draws), proving cards left hand.
    lib = [("Island", land()) for _ in range(24)]
    lib += [(f"One{i}", rec(cmc=1, type_line="Creature")) for i in range(36)]
    flow = deck_sim.simulate_flow(lib, turns=8, trials=400, rng=random.Random(2))
    assert flow["hand_size_by_turn"][8] < 8.0   # would be ~13 if nothing were cast


# --------------------------------------------------------------------------- #
# _draw_profile — reading card-draw amount/repeatability from oracle text
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("text,type_line,expected", [
    ("draw a card.", "instant", (1, False)),                    # cantrip nets 0
    ("draw two cards.", "sorcery", (2, False)),                 # real advantage
    ("draw three cards, then put two cards from your hand on top of your library.",
     "instant", (1, False)),                                    # Brainstorm: selection, capped
    ("at the beginning of your upkeep, draw a card.", "enchantment", (0, True)),  # engine
    ("whenever a creature dies, you may draw a card.", "creature", (0, True)),    # engine
    ("draw x cards.", "sorcery", (1, False)),                   # X = floor 1
    ("draw two cards, then discard two cards.", "sorcery", (1, False)),   # rummage = net 0
    ("you draw two cards and you lose 2 life.", "sorcery", (2, False)),   # Night's Whisper = +1
])
def test_draw_profile_reads_text(text, type_line, expected):
    assert deck_sim._draw_profile(text, type_line) == expected


def test_draw_profile_engine_needs_a_permanent():
    # A triggered "draw" on an INSTANT is still a one-shot, not a repeatable engine.
    assert deck_sim._draw_profile("whenever a creature dies, draw a card.", "instant") == (1, False)


@pytest.mark.parametrize("text,type_line", [
    # REGRESSION: draw PAYOFFS have "draw" only in the trigger condition and yield no
    # cards — crediting them as +1/turn engines over-stated Forced Liquidation's
    # smoothness. They must read as (0, False), contributing nothing.
    ("whenever you draw a card, each opponent loses 1 life.", "creature"),   # Psychosis Crawler
    ("whenever you draw a card, you gain 2 life. whenever an opponent draws a card, they lose 2 life.",
     "creature"),                                                            # Sheoldred
    ("if you would draw a card, instead do something else.", "artifact"),    # replacement, not a source
])
def test_draw_profile_payoffs_yield_nothing_REGRESSION(text, type_line):
    assert deck_sim._draw_profile(text, type_line) == (0, False)


def test_draw_profile_real_effect_after_payoff_clause_survives_REGRESSION():
    # REGRESSION: Niv-Mizzet has a payoff clause AND a real draw effect ("whenever a
    # player casts an instant or sorcery spell, you draw a card"). Stripping the
    # payoff must not eat the genuine engine.
    niv = ("whenever you draw a card, niv-mizzet deals 1 damage to any target. "
           "whenever a player casts an instant or sorcery spell, you draw a card.")
    assert deck_sim._draw_profile(niv, "creature") == (0, True)


def test_draw_profile_etb_cantrip_is_oneshot_not_engine():
    # "When ~ enters, you draw two cards" (Cloudblazer) is a one-shot ETB, not a
    # recurring engine — the subject after 'when' is the card, not a player.
    assert deck_sim._draw_profile(
        "when this creature enters, you draw two cards and you gain 2 life.", "creature") == (2, False)


# --------------------------------------------------------------------------- #
# simulate_flow draw execution — the momentum fix (drawy decks stop being punished)
# --------------------------------------------------------------------------- #
def test_simulate_flow_oneshot_draw_refills_hand():
    # Same deck, with vs without a 'draw two' profile on the spells: executing the
    # draw must leave a LARGER hand and a LOWER hellbent rate (net card advantage).
    lib = [("Island", land()) for _ in range(24)]
    lib += [(f"Whisper{i}", rec(cmc=2, type_line="Sorcery")) for i in range(36)]
    profiles = {f"whisper{i}": (2, False) for i in range(36)}
    base = deck_sim.simulate_flow(lib, turns=8, trials=500, rng=random.Random(8))
    drawy = deck_sim.simulate_flow(lib, turns=8, trials=500, rng=random.Random(8),
                                   draw_profiles=profiles)
    assert drawy["hand_size_by_turn"][8] > base["hand_size_by_turn"][8]
    assert drawy["hellbent_by_turn"][8] < base["hellbent_by_turn"][8]


def test_simulate_flow_repeatable_engine_compounds_over_turns():
    # A cheap repeatable draw engine keeps the hand stocked: hellbent by T10 must be
    # far lower than the same deck with no engines.
    lib = [("Island", land()) for _ in range(24)]
    lib += [("Rhystic Study", rec(cmc=1, type_line="Enchantment"))] * 12
    lib += [(f"Filler{i}", rec(cmc=3, type_line="Creature")) for i in range(24)]
    profiles = {"rhystic study": (0, True)}
    base = deck_sim.simulate_flow(lib, turns=10, trials=500, rng=random.Random(1))
    engine = deck_sim.simulate_flow(lib, turns=10, trials=500, rng=random.Random(1),
                                    draw_profiles=profiles)
    assert engine["hellbent_by_turn"][10] < base["hellbent_by_turn"][10]
    assert engine["hand_size_by_turn"][10] > base["hand_size_by_turn"][10]


def test_simulate_flow_draw_execution_still_deterministic():
    lib = toy_library()
    profiles = {"spell0": (2, False), "spell1": (0, True)}
    a = deck_sim.simulate_flow(lib, turns=8, trials=300, rng=random.Random(2), draw_profiles=profiles)
    b = deck_sim.simulate_flow(lib, turns=8, trials=300, rng=random.Random(2), draw_profiles=profiles)
    assert a == b


def test_simulate_flow_empty_profiles_match_no_profiles_REGRESSION():
    # REGRESSION: adding the draw model must not change behaviour when no profiles
    # are supplied — the draw-step refactor stays byte-identical to the pre-draw sim.
    lib = toy_library()
    none = deck_sim.simulate_flow(lib, turns=8, trials=300, rng=random.Random(3))
    empty = deck_sim.simulate_flow(lib, turns=8, trials=300, rng=random.Random(3), draw_profiles={})
    assert none == empty


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
