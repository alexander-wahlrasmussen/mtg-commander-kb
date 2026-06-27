"""Tier-3 METAMORPHIC tests (Backlog.md #9).

The oracle problem: without real games we have no ground truth for "is this clock
RIGHT". Metamorphic testing sidesteps it — instead of asserting an output VALUE,
assert how the output must CHANGE (or not) under a transform of the input that
has a known-correct effect. A violated relation is a real bug even when we can't
say what the right number is.

All hermetic: synthetic card records (helpers.py), fixed seeds, no Scryfall bulk.
These complement Tier 1 (which tests functions' values) and Tier 2 (which pins the
labs' output) — here we pin the simulator's INVARIANTS. Relations are labelled MR-n.
"""
import random
import statistics

import pytest

import deck_sim
import speed_lab_core as slc
from helpers import rec, land, toy_library


def _write(tmp_path, stem, lines):
    p = tmp_path / f"{stem}.txt"
    p.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return p


# --------------------------------------------------------------------------- #
# MR-1  reorder the decklist -> identical deck
# Backlog: "reorder the decklist -> identical". Exact at the parser (the library
# is a multiset); only statistical at the simulator (the shuffle is position-based,
# so a permuted input draws differently per seed but converges in aggregate).
# --------------------------------------------------------------------------- #
def test_parse_is_order_invariant(tmp_path):
    lines = ["1 Alpha", "2 Beta", "1 Gamma", "3 Delta"]
    index = {"alpha": rec(), "beta": rec(), "gamma": rec(), "delta": rec()}
    base, _, dbase = deck_sim.parse_deck(_write(tmp_path, "no-such-a", lines), index)
    rev, _, drev = deck_sim.parse_deck(_write(tmp_path, "no-such-b", list(reversed(lines))), index)
    # same multiset of names, same size — order on disk is not load-bearing
    assert sorted(n for n, _ in base) == sorted(n for n, _ in rev)
    assert dbase["library_size"] == drev["library_size"]


def test_simulate_is_order_invariant_in_aggregate():
    lib = toy_library(n_land=24, n_spell=36)
    shuffled = lib[:]
    random.Random(0).shuffle(shuffled)            # permute the INPUT order
    a = deck_sim.simulate(lib, ["U"], turns=8, trials=3000, rng=random.Random(99))
    b = deck_sim.simulate(shuffled, ["U"], turns=8, trials=3000, rng=random.Random(99))
    # The estimator must not depend on input order beyond Monte-Carlo noise.
    assert abs(a["keepable_pct"] - b["keepable_pct"]) < 2.0
    for t in range(1, 9):
        assert abs(a["castable_by_turn"][t] - b["castable_by_turn"][t]) < 3.0


# --------------------------------------------------------------------------- #
# MR-2  swap a reskin alias -> identical result
# A decklist written with the UB reskin name must simulate identically to the same
# decklist written with the card's canonical name (same rec resolves; the name
# string is cosmetic for a nonland). Exact: identical recs in identical positions
# -> identical shuffles under one seed -> identical output.
# --------------------------------------------------------------------------- #
def test_reskin_alias_simulates_identically(tmp_path):
    spear = rec(cmc=2, type_line="Artifact — Equipment")
    index = {"shadowspear": spear, "island": land(), "grizzly bears": rec(type_line="Creature")}
    aliases = {"morgul-knife": "Shadowspear"}
    common = ["1 Island"] * 10 + ["1 Grizzly Bears"] * 6
    canon = deck_sim.parse_deck(_write(tmp_path, "no-such-c", ["1 Shadowspear", *common]), index, aliases)[0]
    ub = deck_sim.parse_deck(_write(tmp_path, "no-such-d", ["1 Morgul-Knife", *common]), index, aliases)[0]
    out_canon = deck_sim.simulate(canon, ["U"], turns=8, trials=3000, rng=random.Random(5))
    out_ub = deck_sim.simulate(ub, ["U"], turns=8, trials=3000, rng=random.Random(5))
    assert out_canon == out_ub


# --------------------------------------------------------------------------- #
# MR-3  more sources can only help — monotonicity under a superset
# A ⊆ B  =>  P(source in hand by T | B) >= P(... | A), pointwise. Exact: same
# library + same seed => identical hands each trial, so a larger source set can
# only turn more trials into hits, never fewer.
# --------------------------------------------------------------------------- #
def test_simulate_need_monotone_in_source_set():
    lib = toy_library(n_land=20, n_spell=40)            # spells: Spell0..Spell39
    small = {"spell0", "spell1"}
    big = small | {"spell2", "spell3", "spell4"}
    a = deck_sim.simulate_need(lib, small, turns=8, trials=3000, rng=random.Random(11))
    b = deck_sim.simulate_need(lib, big, turns=8, trials=3000, rng=random.Random(11))
    for t in range(1, 9):
        assert b["in_hand_by_turn"][t] >= a["in_hand_by_turn"][t]
        assert b["castable_by_turn"][t] >= a["castable_by_turn"][t]


# --------------------------------------------------------------------------- #
# MR-4  add copies of a source -> availability not slower
# The realistic "strictly better deck" transform: swap vanilla spells for more
# copies of a cheap ramp source (deck size fixed). Its availability curve must not
# drop at any turn. Statistical (composition changes the shuffle) but deterministic
# under a fixed seed, so the small tolerance only absorbs MC noise.
# --------------------------------------------------------------------------- #
def test_more_copies_of_a_source_not_slower():
    base = [("Island", land()) for _ in range(20)]
    base += [("Filler", rec(cmc=2, type_line="Creature")) for _ in range(40)]
    rock = ("Mind Stone", rec(cmc=2, type_line="Artifact"))
    few = base[:58] + [rock] * 2                        # 2 copies
    many = base[:54] + [rock] * 6                        # 6 copies (swap 4 fillers)
    src = {"mind stone"}
    a = deck_sim.simulate_need(few, src, turns=8, trials=6000, rng=random.Random(3))
    b = deck_sim.simulate_need(many, src, turns=8, trials=6000, rng=random.Random(3))
    for t in range(1, 9):
        assert b["in_hand_by_turn"][t] >= a["in_hand_by_turn"][t] - 1.0


# --------------------------------------------------------------------------- #
# MR-5  more trials -> the estimate concentrates (CI narrows)
# The Monte-Carlo estimator must be consistent: the spread of the keepable% across
# independent seeds shrinks as trials grow. Guards against a non-converging or
# biased loop. Deterministic (fixed seed list).
# --------------------------------------------------------------------------- #
def test_estimate_concentrates_with_more_trials():
    lib = toy_library()
    seeds = [1, 2, 3, 4, 5, 6]
    spread = {}
    for trials in (150, 4000):
        vals = [deck_sim.simulate(lib, ["U"], turns=6, trials=trials, rng=random.Random(s))["keepable_pct"]
                for s in seeds]
        spread[trials] = statistics.pstdev(vals)
    assert spread[4000] < spread[150], f"estimate did not concentrate: {spread}"


# --------------------------------------------------------------------------- #
# MR-6  add Sol Ring -> the clock is not slower
# Backlog: "Add a Sol Ring -> median decap not slower." Tested at the speed_lab_core
# goldfish (the layer that models rocks as MANA — deck_sim's core treats a rock as
# just a cheap spell, so this relation can only be checked here). A deck that swaps
# vanilla bodies for Sol Rings must reach a kill-cost mana threshold no later.
# Statistical over many seeds; the effect dwarfs the noise.
# --------------------------------------------------------------------------- #
def _first_turn_reaching(lib, rocks, seed, target=4, turns=10):
    g = slc.Goldfish(lib, random.Random(seed), rocks=rocks)
    for T in range(1, turns + 1):
        g.begin_turn(T)
        g.deploy_rocks()
        if g.avail >= target:
            return T
    return turns + 1


def test_sol_ring_does_not_slow_the_clock():
    lands = [("Island", land()) for _ in range(16)]
    filler = [("Bear", rec(cmc=2, type_line="Creature — Bear")) for _ in range(44)]
    with_rock = lands + [("Sol Ring", rec(cmc=1, type_line="Artifact"))] * 4 + filler[:40]
    no_rock = lands + filler                              # same size, no acceleration
    rocks = {"Sol Ring": (1, 2)}                          # pay 1, make 2
    seeds = range(300)
    med_with = statistics.median(_first_turn_reaching(with_rock, rocks, s) for s in seeds)
    med_without = statistics.median(_first_turn_reaching(no_rock, rocks, s) for s in seeds)
    assert med_with <= med_without, f"Sol Ring slowed the clock: {med_with} vs {med_without}"


# --------------------------------------------------------------------------- #
# DST — deterministic simulation testing
# The repo's replay guarantee: every component takes an injected rng, and every
# lab fixes its seed, so a failing number replays exactly (git-bisectable). We do
# NOT thread one global seed through all labs — they carry distinct fixed seeds
# whose outputs are already committed (golden snapshot, pod_gauntlet_clocks.json),
# and unifying them would churn every number for no replay benefit. Instead we pin
# the property that makes per-component seeds sufficient: same seed -> same run.
# (deck_sim's simulate determinism is pinned in test_deck_sim; this covers the
# speed_lab_core goldfish, the other half every clock lab is built on.)
# --------------------------------------------------------------------------- #
def _goldfish_trace(seed):
    # Rocks IN the deck so the mana trace depends on WHEN they're drawn — i.e. on
    # the shuffle, i.e. on the seed (a counts-only trace would be seed-blind).
    lib = ([("Island", land()) for _ in range(20)]
           + [("Sol Ring", rec(cmc=1, type_line="Artifact"))] * 8
           + [("Bear", rec(cmc=2, type_line="Creature — Bear")) for _ in range(32)])
    g = slc.Goldfish(lib, random.Random(seed), rocks={"Sol Ring": (1, 2)})
    trace = []
    for T in range(1, 11):
        g.begin_turn(T)
        g.deploy_rocks()
        g.draw(1)
        trace.append((g.lands, g.rock_out, g.avail, len(g.hand)))
    return trace


def test_goldfish_is_deterministic_for_a_fixed_seed():
    assert _goldfish_trace(2026) == _goldfish_trace(2026)
    assert _goldfish_trace(1) != _goldfish_trace(2)   # and the seed actually matters
