"""Tier-1 tests for speed_lab_core.py — the shared clock-lab engine.

Every *_clock_lab.py imports this. The Table tracker and the median/cum/never
reporters turn a goldfish into the decap/table numbers the verification rule
mandates — so a bug here silently mis-states a clock in every Summary.
"""
import pytest
from hypothesis import given, strategies as st

import speed_lab_core as slc
from helpers import rec


# --------------------------------------------------------------------------- #
# Table — decap (first death) vs table (last death)
# --------------------------------------------------------------------------- #
def test_table_focus_then_all():
    t = slc.Table(n=3, life=40)
    t.hit_focus(40, T=5)            # kills opponent 0 only
    assert t.decap == 5 and t.table is None
    t.hit_focus(40, T=6)           # opponent 1
    t.hit_focus(40, T=7)           # opponent 2 -> table dead
    assert t.table == 7


def test_table_hit_all_decap_equals_table():
    t = slc.Table(n=3, life=40)
    t.hit_all(40, T=4)             # everyone dies at once
    assert t.decap == 4 and t.table == 4


def test_table_kill_all():
    t = slc.Table(n=3, life=40)
    t.kill_all(T=6)
    assert t.done and t.decap == 6 and t.table == 6


def test_table_partial_damage_no_death():
    t = slc.Table(n=3, life=40)
    t.hit_all(39, T=3)
    assert t.decap is None and t.table is None and not t.done


@given(st.lists(
    st.tuples(st.sampled_from(["all", "focus"]),
              st.integers(min_value=1, max_value=60),
              st.integers(min_value=1, max_value=15)),
    min_size=1, max_size=20))
def test_table_decap_never_after_table(events):
    # Property: under a monotonic turn clock (how labs drive it), the first death
    # cannot land later than the last. Sort by turn to model the real turn loop.
    t = slc.Table(n=3, life=40)
    for kind, x, T in sorted(events, key=lambda e: e[2]):
        (t.hit_all if kind == "all" else t.hit_focus)(x, T)
    if t.table is not None:
        assert t.decap is not None
        assert t.decap <= t.table


# --------------------------------------------------------------------------- #
# reporting — median / cum / never_pct
# --------------------------------------------------------------------------- #
def test_median_picks_middle():
    results = [(3, 5), (4, 6), (5, 7)]          # decap [3,4,5] -> T4
    assert slc.median(results, 0) == "T4"
    assert slc.median(results, 1) == "T6"


def test_median_never_in_horizon():
    assert "never" in slc.median([(None, None)] * 3, 0)


def test_median_even_length_is_lower_middle():
    # REGRESSION (2026-06-29 audit): even-N median read the UPPER-middle element
    # (vals[n//2]) -> ~1 turn slow at boundaries. The median is the lowest turn
    # with cumulative >= 50% = the lower-middle.
    results = [(3, 9), (4, 9), (5, 9), (6, 9)]   # decap [3,4,5,6]
    assert slc.median(results, 0) == "T4"        # lower-middle (was wrongly T5)
    results = [(7, 0), (8, 0)]                    # decap [7,8]
    assert slc.median(results, 0) == "T7"        # was wrongly T8


@given(st.lists(st.integers(min_value=1, max_value=12), min_size=1, max_size=40))
def test_median_agrees_with_curve_median(decaps):
    # The printed median() must use the SAME definition as the golden test's
    # curve_median (lowest turn whose cumulative P(kill) >= 50%), so the printed
    # line can't drift from the harvested clock. Pins both parities.
    results = [(d, d) for d in decaps]
    grid = list(range(1, 13))
    curve = [100.0 * sum(1 for d in decaps if d <= t) / len(decaps) for t in grid]
    cm = next((t for t, c in zip(grid, curve) if c >= 50), grid[-1] + 1)
    assert slc.median(results, 0) == f"T{cm}"


def test_cum_is_monotone_and_caps_at_100():
    results = [(2, 9), (4, 9), (6, 9)]
    show = [2, 3, 4, 5, 6, 7]
    c = slc.cum(results, 0, show)
    vals = [c[t] for t in show]
    assert vals == sorted(vals)
    assert c[6] == 100.0


def test_never_pct():
    results = [(2, 3), (None, None), (4, 5), (None, None)]
    assert slc.never_pct(results, 0, 4) == 50.0


@given(st.lists(st.integers(min_value=1, max_value=12), min_size=1, max_size=40))
def test_cum_curve_nondecreasing_property(decaps):
    results = [(d, d) for d in decaps]
    show = list(range(1, 13))
    c = slc.cum(results, 0, show)
    vals = [c[t] for t in show]
    assert vals == sorted(vals)
    assert 0.0 <= vals[0] and vals[-1] <= 100.0


# --------------------------------------------------------------------------- #
# build_lib — swap-variant construction
# --------------------------------------------------------------------------- #
def test_build_lib_swap():
    idx = {"sol ring": rec(cmc=1, type_line="Artifact")}
    base = [("A", rec()), ("B", rec()), ("A", rec())]
    lib = slc.build_lib(base, idx, removes=["A"], adds=["Sol Ring"])
    names = [n for n, _ in lib]
    assert names.count("A") == 1        # only ONE copy removed
    assert "B" in names and "Sol Ring" in names


def test_build_lib_remove_absent_raises():
    with pytest.raises(SystemExit):
        slc.build_lib([("A", rec())], {}, removes=["Zzz"], adds=[])


def test_build_lib_add_unknown_raises():
    with pytest.raises(SystemExit):
        slc.build_lib([("A", rec())], {}, removes=[], adds=["Not In Oracle"])


# --------------------------------------------------------------------------- #
# slot_complete — per-slot tutor (bipartite) assignment
# --------------------------------------------------------------------------- #
def test_slot_complete_member_seen():
    assert slc.slot_complete([({"a"}, set())], {"a"}) is True
    assert slc.slot_complete([({"a"}, set())], {"x"}) is False


def test_slot_complete_tutor_fills_slot():
    assert slc.slot_complete([({"a"}, {"tutor"})], {"tutor"}) is True


def test_slot_complete_two_slots_need_two_distinct_tutors():
    slots = [({"a"}, {"t1", "t2"}), ({"b"}, {"t2"})]
    assert slc.slot_complete(slots, {"t1", "t2"}) is True   # t2->b, t1->a
    assert slc.slot_complete(slots, {"t2"}) is False         # one tutor, two open slots
