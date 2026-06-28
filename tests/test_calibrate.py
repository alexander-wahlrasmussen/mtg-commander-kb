"""Tier-1 unit tests for calibrate.py's pure helpers (the Layer-C back-test math).

Hermetic: exercises only the oracle-free helpers (load_log / observed_stats / parse_med /
clock_rows / mae) on synthetic records + a synthetic clocks dict. The prediction wiring
(tier_list axes) is integration-checked by running the script on the committed fixture, not
unit-tested here — these guard the arithmetic that turns a game log into calibration numbers.

Per the test discipline (tests/README.md): the instruments that emit decision numbers get
tests. calibrate grades every other lab, so its own aggregation must be pinned.
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


cal = _load("calibrate")


# --------------------------------------------------------------- parse_med
def test_parse_med_plain():
    assert cal.parse_med("T7") == (7.0, False)
    assert cal.parse_med("T10") == (10.0, False)


def test_parse_med_open_is_flagged():
    turn, opened = cal.parse_med(">T14")
    assert turn == 14.0 and opened is True


def test_parse_med_none():
    assert cal.parse_med(None) == (None, False)


# --------------------------------------------------------------- observed_stats
def _recs():
    return [
        {"mine": "a", "winner": "a", "win_turn": 8, "first_decap_turn": 7},
        {"mine": "a", "winner": "a", "win_turn": 10, "first_decap_turn": 7},
        {"mine": "a", "winner": "x", "win_turn": 9, "first_decap_turn": 9},
        {"mine": "b", "winner": "y", "win_turn": 11, "first_decap_turn": 10},
    ]


def test_observed_win_rate_and_clocks():
    o = cal.observed_stats(_recs())
    # a: 3 games, 2 wins -> 66.7%; table = mean(win_turn | won) = (8+10)/2 = 9.0
    assert o["a"]["n"] == 3 and o["a"]["w"] == 2
    assert round(o["a"]["win_rate"], 1) == 66.7
    assert o["a"]["table_mean"] == 9.0          # losing game's win_turn excluded
    # decap = mean(first_decap_turn) over ALL my games (pod-level), = (7+7+9)/3
    assert round(o["a"]["decap_mean"], 2) == 7.67


def test_observed_winless_deck_has_no_table_clock():
    o = cal.observed_stats(_recs())
    assert o["b"]["win_rate"] == 0.0
    assert o["b"]["table_mean"] is None         # never closed -> no observed table clock
    assert o["b"]["decap_mean"] == 10.0


def test_records_without_mine_are_skipped():
    o = cal.observed_stats(_recs() + [{"winner": "z", "win_turn": 5}])
    assert set(o) == {"a", "b"}


# --------------------------------------------------------------- clock_rows + mae
def _clocks():
    return {
        "a": {"name": "Deck A", "med": ["T7", "T8"]},     # decap T7, table T8
        "b": {"name": "Deck B", "med": ["T9", ">T12"]},   # table median is open
    }


def test_clock_rows_signed_error_and_eligibility():
    rows = {r["slug"]: r for r in cal.clock_rows(cal.observed_stats(_recs()), _clocks(), 3)}
    a = rows["a"]
    assert a["eligible"] is True                          # n=3 >= min 3
    assert a["lab_table"] == 8.0 and a["obs_table"] == 9.0
    assert a["d_table"] == 1.0                            # obs - lab = 9 - 8
    b = rows["b"]
    assert b["eligible"] is False                         # n=1 < 3
    assert b["obs_table"] is None and b["d_table"] is None  # winless -> no table delta


def test_mae_excludes_ineligible_and_missing():
    rows = cal.clock_rows(cal.observed_stats(_recs()), _clocks(), 3)
    # only deck 'a' is eligible AND has a table delta (|1.0|) -> MAE = 1.0
    assert cal.mae(rows, "d_table") == 1.0
    # deck 'b' (ineligible) must not pull the decap MAE; 'a' decap delta = |7.67 - 7| = 0.67
    assert round(cal.mae(rows, "d_decap"), 2) == 0.67


# --------------------------------------------------------------- load_log
def test_load_log_reads_fixture():
    recs = cal.load_log(FIXTURE)
    assert len(recs) == 10
    assert {r["mine"] for r in recs} == {"genome_project", "radiation_sickness", "grand_design"}


def test_load_log_missing_file_is_empty():
    assert cal.load_log(ROOT / "tests" / "fixtures" / "does_not_exist.jsonl") == []


# --------------------------------------------------------------- power_curve
def _toy_spearman(x, y):
    """Minimal exact Spearman on tie-free integer-rankable data — enough for the power test
    (keeps it independent of framework_bakeoff's import)."""
    n = len(x)
    if n < 3:
        return None, n
    rx = sorted(range(n), key=lambda i: x[i])
    ry = sorted(range(n), key=lambda i: y[i])
    rankx = {i: r for r, i in enumerate(rx)}
    ranky = {i: r for r, i in enumerate(ry)}
    d2 = sum((rankx[i] - ranky[i]) ** 2 for i in range(n))
    return 1 - 6 * d2 / (n * (n * n - 1)), n


def test_power_curve_shape_and_bounds():
    truth = {f"d{i}": p for i, p in enumerate([10, 25, 40, 55, 70, 85])}
    grid = [3, 30]
    rows = cal.power_curve(truth, grid, trials=400, seed=1, spearman=_toy_spearman, detect=0.5)
    assert [r[0] for r in rows] == grid
    for _N, med, p10, pdet in rows:
        assert -1.0 <= med <= 1.0 and -1.0 <= p10 <= 1.0 and 0.0 <= pdet <= 1.0


def test_power_curve_more_games_recovers_ranking():
    """The whole point: more games/deck -> the observed ranking matches truth better."""
    truth = {f"d{i}": p for i, p in enumerate([10, 25, 40, 55, 70, 85])}
    rows = cal.power_curve(truth, [3, 30], trials=400, seed=7, spearman=_toy_spearman)
    med3, med30 = rows[0][1], rows[1][1]
    pdet3, pdet30 = rows[0][3], rows[1][3]
    assert med30 > med3                 # median correlation rises with sample size
    assert pdet30 >= pdet3              # detection power is monotone non-decreasing


def test_power_curve_is_seed_deterministic():
    truth = {f"d{i}": p for i, p in enumerate([10, 30, 50, 70, 90])}
    a = cal.power_curve(truth, [5], trials=200, seed=42, spearman=_toy_spearman)
    b = cal.power_curve(truth, [5], trials=200, seed=42, spearman=_toy_spearman)
    assert a == b
