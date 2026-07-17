"""Unit tests for deck_doctor pure heuristics.

Currently covers fragility_rank — the permanent-type durability ladder from the
"500 decks" video (REF_Multiplayer_Card_Eval.md). The rule that's easy to get
wrong: a card is as fragile as its MOST removable type (min rank across types),
so an artifact creature reads as a creature, not as the more durable artifact.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import deck_doctor as dd  # noqa: E402


def rec(type_line, faces=None):
    r = {"type_line": type_line}
    if faces:
        r["card_faces"] = [{"type_line": t} for t in faces]
    return r


def test_fragility_ladder_order():
    # easiest (0) -> hardest (6), one representative per tier
    assert dd.fragility_rank(rec("Legendary Planeswalker — Teferi")) == 0
    assert dd.fragility_rank(rec("Creature — Human Wizard")) == 1
    assert dd.fragility_rank(rec("Artifact")) == 2
    assert dd.fragility_rank(rec("Enchantment — Aura")) == 3
    assert dd.fragility_rank(rec("Battle — Siege")) == 4
    assert dd.fragility_rank(rec("Land")) == 5
    assert dd.fragility_rank(rec("Basic Land — Forest")) == 6
    assert dd.fragility_rank(rec("Basic Snow Land — Island")) == 6


def test_multi_type_takes_most_removable():
    # an artifact creature dies to creature removal AND board wipes -> as fragile
    # as a creature (rank 1), not the more durable artifact (rank 2)
    assert dd.fragility_rank(rec("Artifact Creature — Golem")) == 1
    # a man-land / Dryad Arbor: land + creature -> creature exposure wins
    assert dd.fragility_rank(rec("Land Creature — Forest Dryad")) == 1
    # the Ratchet point: a Vehicle that is NOT a creature stays an artifact (2),
    # dodging creature wipes
    assert dd.fragility_rank(rec("Artifact — Vehicle")) == 2


def test_nonpermanents_return_none():
    assert dd.fragility_rank(rec("Instant")) is None
    assert dd.fragility_rank(rec("Sorcery — Arcane")) is None
    assert dd.fragility_rank(None) is None


def test_mdfc_judged_on_both_faces():
    # "Creature // Land" MDFC -> most removable face (creature) wins
    r = rec("", faces=["Creature — Elemental", "Land"])
    assert dd.fragility_rank(r) == 1


def test_gc_match_splits_dfc_front_face():
    # REGRESSION: a double-faced Game Changer is on the GC list under its FRONT
    # face only. The full printed name "Tergrid, God of Fright // Tergrid's
    # Lantern" must still register as a GC, or a DFC GC silently evades the hard
    # 3-cap (found 2026-07-17 building the owned Yahenni list).
    gc = {"tergrid, god of fright": "Tergrid, God of Fright",
          "demonic tutor": "Demonic Tutor"}
    hits = dd.match_game_changers(
        ["Tergrid, God of Fright // Tergrid's Lantern", "Sol Ring"], gc)
    assert hits == {"tergrid, god of fright": "Tergrid, God of Fright"}
    # plain front-face name and a non-GC both behave
    assert dd.match_game_changers(["Demonic Tutor"], gc)
    assert dd.match_game_changers(["Reassembling Skeleton"], gc) == {}


def test_gc_match_resolves_reskin_alias():
    # a reskin of a GC is still a GC (REF_Reskin_Aliases); alias maps printed
    # name -> canonical GC name (both lowercased keys).
    gc = {"jeska's will": "Jeska's Will"}
    aliases = {"storm's will": "jeska's will"}
    assert dd.match_game_changers(["Storm's Will"], gc, aliases) == {
        "jeska's will": "Jeska's Will"}


def test_all_text_none_safe():
    # REGRESSION: parse_deck KEEPS unresolved cards in the library, so the
    # footprint/interaction scans can hand _all_text a None record. It must return
    # "" rather than AttributeError (which crashed --footprint and the whole --all
    # batch on any deck with a typo'd / unresolved card). See 2026-06-29 audit.
    assert dd._all_text(None) == ""
    assert dd._all_text({"oracle_text": "Draw a card."}) == "draw a card."
    assert dd._all_text({}) == ""
