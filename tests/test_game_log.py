"""Tier-1 unit tests for game_log.py — the capture end of the Layer-C loop.

Hermetic: exercises the pure helpers (resolve_slug / parse_quick / grade_game / _parse_med /
problems / parse_seat / parse_event) on synthetic inputs, plus one light read of the committed
clocks JSON. No card bulk, no network, no interactive input().

Per the test discipline (tests/README.md): the instruments that emit decision numbers get tests.
game_log is the SOURCE of the real games calibrate.py grades the whole tower against — a malformed
record or a wrong-signed grade card is a silent leak into every Layer-C number. This file also
closes the pre-existing gap where game_log.py had no tests at all.
"""
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def _load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


gl = _load("game_log")
cal = _load("calibrate")


# ------------------------------------------------------------------- resolve_slug
def test_resolve_slug_exact_and_prefix():
    decks = {"genome_project", "grand_design", "grand_larceny"}
    assert gl.resolve_slug("genome_project", decks) == ("genome_project", ["genome_project"])
    slug, hits = gl.resolve_slug("genome", decks)       # unique prefix
    assert slug == "genome_project"


def test_resolve_slug_normalizes_dashes_and_spaces():
    decks = {"the_dark_lords_army"}
    assert gl.resolve_slug("The Dark Lords Army", decks)[0] == "the_dark_lords_army"


def test_resolve_slug_ambiguous_returns_none_with_hits():
    decks = {"grand_design", "grand_larceny"}
    slug, hits = gl.resolve_slug("grand", decks)
    assert slug is None and hits == ["grand_design", "grand_larceny"]  # sorted, both offered


def test_resolve_slug_miss():
    assert gl.resolve_slug("widget", {"genome_project"}) == (None, [])


# --------------------------------------------------------------------- parse_quick
def test_parse_quick_win_full():
    rec = gl.parse_quick("genome W T9 d8 combo | ur_dragon L | kinnan L")
    assert rec["mine"] == "genome_project"
    assert rec["winner"] == "genome_project"
    assert rec["win_turn"] == 9 and rec["first_decap_turn"] == 8
    assert rec["win_type"] == "combo"
    assert rec["pod"][0] == {"deck": "genome_project", "pilot": "me", "result": "win"}
    assert [s["deck"] for s in rec["pod"][1:]] == ["ur_dragon", "kinnan"]
    assert all(s["result"] == "loss" for s in rec["pod"][1:])


def test_parse_quick_loss_sets_winner_from_opponent():
    rec = gl.parse_quick("grand_design L T11 d9 | ur_dragon W")
    assert rec["mine"] == "grand_design" and rec["winner"] == "ur_dragon"
    assert rec["pod"][0]["result"] == "loss"
    assert rec["win_turn"] == 11 and rec["first_decap_turn"] == 9
    assert "win_type" not in rec                          # omitted, not empty


def test_parse_quick_notes_after_hash():
    rec = gl.parse_quick("genome W T7 combo | ur_dragon L # raced under abolisher")
    assert rec["notes"] == "raced under abolisher"


def test_parse_quick_hyphenated_wintype_survives_tokenizing():
    rec = gl.parse_quick("radiation_sickness W T10 table-drain | kinnan L")
    assert rec["win_type"] == "table-drain"


def _err(spec):
    try:
        gl.parse_quick(spec)
    except ValueError as e:
        return str(e)
    raise AssertionError(f"expected ValueError for {spec!r}")


def test_parse_quick_rejects_unknown_deck():
    assert "active decks" in _err("widget W T9")


def test_parse_quick_requires_result():
    assert "W or L" in _err("genome T9 | ur_dragon L")


def test_parse_quick_requires_end_turn():
    assert "T<n>" in _err("genome W | ur_dragon L")


def test_parse_quick_loss_without_winner_is_rejected():
    assert "who won" in _err("genome L T9 d8 | ur_dragon L")


def test_parse_quick_rejects_garbage_token():
    assert "didn't understand" in _err("genome W T9 zzz")


def test_parse_quick_output_passes_validation():
    """The whole point: a quick record must be clean by the same `problems()` gate as any other."""
    rec = gl.parse_quick("genome W T9 d8 combo | ur_dragon L")
    assert gl.problems(rec) == []


# ----------------------------------------------------------------------- _parse_med
def test_parse_med_matches_calibrate():
    """DRY-by-test: game_log's local median parser mirrors calibrate.parse_med exactly."""
    for s in ("T7", "T10", ">T14", "≥T12", None, "T6"):
        assert gl._parse_med(s) == cal.parse_med(s)


# ------------------------------------------------------------------------ grade_game
_MED = {
    "genome_project": {"name": "The Genome Project", "decap": (7.0, False), "table": (8.0, False)},
    "grand_design": {"name": "The Grand Design", "decap": (9.0, False), "table": (12.0, True)},
}


def test_grade_game_win_grades_both_clocks_signed():
    rec = {"mine": "genome_project", "winner": "genome_project",
           "win_turn": 9, "first_decap_turn": 8}
    g = gl.grade_game(rec, _MED)
    assert g["table"]["delta"] == 1.0 and g["table"]["lab"] == 8.0   # obs 9 - lab 8
    assert g["decap"]["delta"] == 1.0 and g["decap"]["lab"] == 7.0   # obs 8 - lab 7


def test_grade_game_loss_withholds_table_clock():
    rec = {"mine": "grand_design", "winner": "ur_dragon",
           "win_turn": 11, "first_decap_turn": 9}
    g = gl.grade_game(rec, _MED)
    assert g["table"] is None                       # I didn't close -> no observed table clock
    assert g["decap"]["delta"] == 0.0               # obs 9 - lab 9, matched exactly


def test_grade_game_unknown_deck_returns_none():
    assert gl.grade_game({"mine": "not_a_deck", "winner": "x"}, _MED) is None


def test_delta_phrase_sign_reads_right():
    assert "FAST" in gl._delta_phrase(1.0)          # obs slower than lab -> lab was optimistic
    assert "SLOW" in gl._delta_phrase(-2.0)         # obs faster than lab -> lab was pessimistic
    assert "exactly" in gl._delta_phrase(0)


# ------------------------------------------------------------------ load_clock_medians
def test_load_clock_medians_reads_committed_json():
    """Light integration: the harvested clocks JSON is committed, so the grade card can read it."""
    med = gl.load_clock_medians()
    assert "genome_project" in med
    decap, table = med["genome_project"]["decap"], med["genome_project"]["table"]
    assert decap[0] is not None and table[0] is not None
    assert isinstance(decap[1], bool)               # (turn, open) shape


def test_load_clock_medians_missing_file_is_empty():
    assert gl.load_clock_medians(ROOT / "tests" / "fixtures" / "nope.json") == {}


# ------------------------------------------------------------------------- problems
def test_problems_clean_record():
    rec = {"date": "2026-07-01", "mine": "genome_project", "winner": "genome_project",
           "win_turn": 9, "pod": [{"deck": "genome_project", "result": "win"}]}
    assert gl.problems(rec) == []


def test_problems_flags_offroster_mine():
    rec = {"date": "x", "mine": "some_opponent", "winner": "some_opponent",
           "win_turn": 9, "pod": [{"deck": "some_opponent", "result": "win"}]}
    assert any("active-roster slug" in p for p in gl.problems(rec))


def test_problems_flags_two_winners():
    rec = {"date": "x", "mine": "genome_project", "winner": "genome_project", "win_turn": 9,
           "pod": [{"deck": "genome_project", "result": "win"},
                   {"deck": "ur_dragon", "result": "win"}]}
    assert any("more than one" in p for p in gl.problems(rec))


# --------------------------------------------------------------- parse_seat / event
def test_parse_seat_and_event_round_trip():
    assert gl.parse_seat("ur_dragon,Sam,loss,9") == {
        "deck": "ur_dragon", "pilot": "Sam", "result": "loss", "ko_turn": 9}
    assert gl.parse_event("7,abolisher,Mia,") == {"turn": 7, "type": "abolisher", "by": "Mia"}
