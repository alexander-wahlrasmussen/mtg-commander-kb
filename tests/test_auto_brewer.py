"""Hermetic tests for the auto_brewer pure core (no bulk, no CSV, no network).

The brew core is the load-bearing part: it must never emit an illegal deck
shape (size != 99, duplicate non-basics, >3 Game Changers, house-banned MLD
or extra-turn chains) no matter what pool it is handed. Everything here runs
on synthetic PoolCards in the tests/helpers.py spirit.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from auto_brewer import (  # noqa: E402
    Brew, PoolCard, brew_deck, can_be_commander, composite, curve_median,
    front, theme_profile, _owned_has, _the_variants,
)


# ---------------------------------------------------------------------------
# synthetic builders
# ---------------------------------------------------------------------------

def pc(disp, ci="B", cmc=2.0, tl="Creature — Human", text="",
       tags=(), produced=(), pips=None, land=False, cmdr=False,
       gc=False, mld=False, xturn=False):
    return PoolCard(
        disp=disp, oid="oid-" + disp, ci=frozenset(ci), cmc=float(cmc),
        type_line=tl, text=text.lower(), tags=tuple(tags),
        produced=tuple(produced), pips=pips or {}, is_land=land,
        is_cmdr=cmdr, is_gc=gc, is_mld=mld, is_xturn=xturn)


CMDR = pc("Gravelord, the Testcase", ci="B", cmc=4,
          tl="Legendary Creature — Zombie Wizard",
          text="Whenever you sacrifice a creature, each opponent loses 1 "
               "life. Other Zombies you control get +1/+1.",
          cmdr=True)


def big_pool(n_filler=70, n_gc=0, gc_kw=""):
    pool = []
    for i in range(15):
        pool.append(pc(f"Ramp {i}", cmc=2, tags=("ramp",)))
    for i in range(10):
        pool.append(pc(f"Draw {i}", cmc=3, tags=("draw",)))
    for i in range(6):
        pool.append(pc(f"Kill {i}", cmc=2, tags=("spot-removal",),
                       tl="Instant"))
    for i in range(3):
        pool.append(pc(f"Wipe {i}", cmc=4, tags=("mass-removal",),
                       tl="Sorcery"))
    for i in range(4):
        pool.append(pc(f"Tutor {i}", cmc=2, tags=("tutor",), tl="Sorcery"))
    for i in range(n_filler):
        tribal = i % 3 == 0
        pool.append(pc(f"Filler {i:03d}", cmc=2 + i % 5,
                       tl="Creature — Zombie" if tribal
                       else "Creature — Human",
                       text="sacrifice a creature: draw a card."
                       if i % 4 == 0 else "vanilla beater",
                       pips={"B": 1}))
    for i in range(n_gc):
        pool.append(pc(f"Changer {i}", cmc=2, tl="Creature — Zombie",
                       text=gc_kw, gc=True))
    for i in range(20):
        pool.append(pc(f"Land {i}", cmc=0, tl="Land", produced=("B",),
                       land=True))
    return pool


def deck_size(brew):
    return sum(n for _, n in brew.deck)


# ---------------------------------------------------------------------------
# commander predicate
# ---------------------------------------------------------------------------

def rec(type_line="Legendary Creature — Human", legal="legal",
        text="", faces=None):
    r = {"legalities": {"commander": legal}, "type_line": type_line,
         "oracle_text": text}
    if faces is not None:
        r["card_faces"] = faces
    return r


def test_legendary_creature_is_commander():
    assert can_be_commander(rec())


def test_banned_card_is_not():
    assert not can_be_commander(rec(legal="banned"))


def test_plain_creature_is_not():
    assert not can_be_commander(rec(type_line="Creature — Human"))


def test_can_be_your_commander_text():
    assert can_be_commander(
        rec(type_line="Legendary Planeswalker — Guff",
            text="Commodore Guff can be your commander."))


def test_dfc_front_face_governs():
    faces = [{"type_line": "Legendary Creature — Sphinx",
              "oracle_text": ""},
             {"type_line": "Land", "oracle_text": ""}]
    assert can_be_commander(
        rec(type_line="Legendary Creature — Sphinx // Land",
            faces=faces))
    faces_rev = [{"type_line": "Sorcery", "oracle_text": ""},
                 {"type_line": "Legendary Creature — Sphinx",
                  "oracle_text": ""}]
    assert not can_be_commander(
        rec(type_line="Sorcery // Legendary Creature — Sphinx",
            faces=faces_rev))


# ---------------------------------------------------------------------------
# theme profile
# ---------------------------------------------------------------------------

def test_theme_profile_detects_aristocrats_and_tribe():
    themes, tribes = theme_profile(CMDR)
    labels = {t.label for t in themes}
    assert "aristocrats" in labels
    assert "drain" in labels
    assert tribes == ["Zombie"]          # Wizard is NOT mentioned in the text


def test_tribe_needs_text_mention():
    quiet = pc("Quiet Legend", tl="Legendary Creature — Elf Druid",
               text="When this creature enters, draw a card.", cmdr=True)
    _, tribes = theme_profile(quiet)
    assert tribes == []


# ---------------------------------------------------------------------------
# brew invariants
# ---------------------------------------------------------------------------

def test_brew_is_exactly_99_and_singleton():
    brew = brew_deck(CMDR, big_pool(), [])
    assert deck_size(brew) == 99
    non_basic = [nm for nm, n in brew.deck if n == 1]
    assert len(non_basic) == len(set(non_basic))
    # basics are the only multi-count entries
    for nm, n in brew.deck:
        if n > 1:
            assert nm in {"Plains", "Island", "Swamp", "Mountain", "Forest",
                          "Wastes"}


def test_brew_meets_quotas_when_pool_allows():
    brew = brew_deck(CMDR, big_pool(), [])
    for label, (have, target) in brew.quota_report.items():
        assert have >= target, f"quota {label}: {have}/{target}"


def test_gc_cap_holds_even_when_gcs_score_high():
    # 5 high-synergy GCs (tribal zombies): only 3 may make the deck.
    pool = big_pool(n_gc=5, gc_kw="other zombies you control get +1/+1")
    brew = brew_deck(CMDR, pool, [])
    assert len(brew.gc_hits) <= 3
    assert deck_size(brew) == 99


def test_gc_commander_counts_toward_cap():
    gc_cmdr = CMDR._replace(is_gc=True)
    pool = big_pool(n_gc=5, gc_kw="other zombies you control get +1/+1")
    brew = brew_deck(gc_cmdr, pool, [])
    assert len(brew.gc_hits) <= 2   # commander occupies one GC slot


def test_mld_is_always_excluded():
    pool = big_pool() + [pc("Doomsday Quake", cmc=4, mld=True,
                            text="destroy all lands.",
                            tags=("mass-removal",))]
    brew = brew_deck(CMDR, pool, [])
    assert all(nm != "Doomsday Quake" for nm, _ in brew.deck)


def test_at_most_one_extra_turn_card():
    pool = big_pool() + [
        pc(f"Time Grab {i}", cmc=5, xturn=True,
           text="take an extra turn after this one.",
           tags=("extra-turn",)) for i in range(3)]
    brew = brew_deck(CMDR, pool, [])
    xt = [nm for nm, _ in brew.deck if nm.startswith("Time Grab")]
    assert len(xt) <= 1


def test_combo_pieces_are_seeded():
    pool = big_pool() + [pc("Piece A", cmc=3), pc("Piece B", cmc=2)]
    combos = [{"pieces": ["Piece A", "Piece B"],
               "produces": ["Infinite damage"], "popularity": 50}]
    brew = brew_deck(CMDR, pool, combos)
    names = {nm for nm, _ in brew.deck}
    assert {"Piece A", "Piece B"} <= names
    assert brew.combos_seeded == 1
    assert set(brew.combo_package) == {"Piece A", "Piece B"}


def test_extra_turn_combos_are_house_banned():
    pool = big_pool() + [pc("Loop X", cmc=3), pc("Loop Y", cmc=2)]
    combos = [{"pieces": ["Loop X", "Loop Y"],
               "produces": ["Infinite turns"], "popularity": 9999}]
    brew = brew_deck(CMDR, pool, combos)
    assert brew.combos_seeded == 0
    assert any("house-banned" in n for n in brew.notes)


def test_missing_combo_piece_skips_combo_without_crash():
    combos = [{"pieces": ["Not In Pool", "Ramp 0"],
               "produces": ["Infinite mana"], "popularity": 10}]
    brew = brew_deck(CMDR, big_pool(), combos)
    assert brew.combos_seeded == 0
    assert deck_size(brew) == 99


def test_brew_is_deterministic():
    pool = big_pool(n_gc=2, gc_kw="zombies")
    combos = [{"pieces": ["Ramp 0", "Draw 0"],
               "produces": ["Infinite value"], "popularity": 1}]
    a = brew_deck(CMDR, pool, combos)
    b = brew_deck(CMDR, list(reversed(pool)), combos)
    assert a.deck == b.deck
    assert a.combo_package == b.combo_package


def test_thin_pool_pads_basics_to_99():
    pool = big_pool(n_filler=0)[:12] + [pc("Land 0", tl="Land",
                                           produced=("B",), land=True)]
    brew = brew_deck(CMDR, pool, [])
    assert deck_size(brew) == 99
    assert any("pool thin" in n for n in brew.notes)
    assert brew.basics.get("Swamp", 0) > 40


# ---------------------------------------------------------------------------
# scoring plumbing
# ---------------------------------------------------------------------------

def _metrics(**over):
    m = {"keepable_pct": 90.0, "mean_dead_turns": 1.0, "colors_t4": 95.0,
         "ramp_n": 12, "draw_n": 8, "assembly_t10": 15.0,
         "combos_seeded": 1, "combos_owned": 3}
    m.update(over)
    return m


def test_composite_no_combo_zeroes_kill_axis():
    total, axes = composite(_metrics(combos_seeded=0, assembly_t10=None))
    assert axes["assembly"] == 0.0 and axes["combo_depth"] == 0.0
    assert total <= 65.0


def test_composite_rewards_likelier_assembly():
    likely, _ = composite(_metrics(assembly_t10=25.0))
    unlikely, _ = composite(_metrics(assembly_t10=3.0))
    assert likely > unlikely


def test_composite_bounded_0_100():
    total, _ = composite(_metrics(keepable_pct=100, mean_dead_turns=0,
                                  assembly_t10=100.0, combos_owned=99))
    assert 0 <= total <= 100


def test_curve_median():
    assert curve_median({1: 5.0, 2: 49.9, 3: 62.0}) == 3
    assert curve_median({1: 0.0, 2: 1.0}) is None


def test_owned_has_the_normalisation():
    owned = {"wise mothman"}
    assert _owned_has(owned, "The Wise Mothman")
    assert _owned_has(owned, "Wise Mothman")
    assert not _owned_has(owned, "Mothman of Yharnam")


def test_front_and_variants():
    assert front("Sephiroth, Fabled SOLDIER // Sephiroth, One-Winged Angel") \
        == "Sephiroth, Fabled SOLDIER"
    assert "the wise mothman" in _the_variants("Wise Mothman")
