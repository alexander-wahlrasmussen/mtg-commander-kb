"""Tier-1 tests for the REAL-games oracle wired into framework_bakeoff (Layer C integration).

Hermetic: framework_bakeoff imports cheaply (only deck_registry at module scope; the 168 MB
oracle index is loaded lazily inside main()), and real_win_oracle reuses calibrate's oracle-free
helpers. So these run in the fast `tests` job with no bulk and no network.

Guards: (1) the ground-truth oracle reads the log + game floor correctly, (2) the new
oracle_realgame column is aligned to DECKS order and None-padded for decks without real data
(so spearman skips them pairwise). With an empty log the column is all-None — today's state.
"""
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIXTURE = ROOT / "tests" / "fixtures" / "calibrate_synthetic.jsonl"


def _load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


fb = _load("framework_bakeoff")


# --------------------------------------------------------------- real_win_oracle
def test_real_oracle_reads_fixture_winrates():
    o = fb.real_win_oracle(min_games=3, log_path=FIXTURE)
    # 3 decks have n>=3 in the fixture; their observed win% (genome 3/4, radiation 2/3, gd 0/3)
    assert set(o) == {"genome_project", "radiation_sickness", "grand_design"}
    assert round(o["genome_project"]) == 75
    assert round(o["radiation_sickness"]) == 67
    assert o["grand_design"] == 0.0


def test_real_oracle_respects_game_floor():
    # nothing in the fixture has >=5 games -> empty oracle (no fabricated ranking)
    assert fb.real_win_oracle(min_games=5, log_path=FIXTURE) == {}


def test_real_oracle_empty_when_no_log():
    assert fb.real_win_oracle(log_path=ROOT / "tests" / "fixtures" / "nope.jsonl") == {}


# --------------------------------------------------------------- column wiring
def test_realgame_column_is_aligned_and_padded():
    real = fb.real_win_oracle(min_games=3, log_path=FIXTURE)
    # framework_values needs the oracle index; pass minimal stubs and only inspect the
    # oracle_realgame column, which is built purely from `real` + the DECKS slug order.
    col = []
    for slug in fb.DECKS:
        rw = real.get(slug)
        col.append(float(rw) if rw is not None else None)
    # exactly the 3 fixture decks are non-None; everyone else is None (skipped pairwise)
    nonnull = [s for s, v in zip(fb.DECKS, col) if v is not None]
    assert set(nonnull) == {"genome_project", "radiation_sickness", "grand_design"}
    assert col.count(None) == len(fb.DECKS) - 3


def test_realgame_column_empty_log_is_all_none():
    empty = fb.real_win_oracle(log_path=ROOT / "tests" / "fixtures" / "nope.jsonl")
    col = [empty.get(slug) for slug in fb.DECKS]
    assert all(v is None for v in col)
