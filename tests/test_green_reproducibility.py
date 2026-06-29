"""Reproducibility / determinism regressions — the 🟢 "latent" cluster of the
2026-06-29 codebase audit (analysis/Codebase_Bug_Audit_2026-06-29.md).

Three independent nondeterminism traps, none of which moved a published clock
(they only fixed single-vs-batch parity and PYTHONHASHSEED dependence):

  1. deck_sim.py threaded ONE rng across the whole sorted batch, so `--deck X`
     consumed a different stream than X's row in a full run (X depended on the
     sibling decks drawn before it). Fixed by `deck_sim.deck_rng(base, key)`:
     a per-deck stream seeded from (base seed, stable key).
  2. esc_clock_lab.TRAMPLE_GRANTERS was a `set`, so the cast-the-first-affordable
     loop walked it in PYTHONHASHSEED-dependent order. Since the deck holds BOTH
     granters, the order is load-bearing. Fixed to a fixed-order tuple.
  3. deck_registry.resolve_deck's same-date tie-break sorted filenames as plain
     strings, where '.'(0x2E) > '-'(0x2D) ranked the bare-date file AFTER a
     same-date timestamped one — so the OLDER bare-date file won. Fixed to a
     chronological (date, time) int-tuple key; the timestamped re-cut wins.

All hermetic: no Scryfall bulk, pure-function / tmp-dir asserts.
"""
import json
import os
import subprocess
import sys
from pathlib import Path

import deck_sim
import deck_registry as reg
import esc_clock_lab as esc

SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"


# --------------------------------------------------------------------------- #
# Bug 1 — deck_sim per-deck RNG: single-deck run == that deck's batch row
# --------------------------------------------------------------------------- #
def test_deck_rng_stream_is_independent_of_sibling_decks():
    # A deck's stream must depend ONLY on (base seed, its key) — never on which or
    # how many sibling decks were drawn before it in a batch. So a "batch" that
    # first exhausts other decks' streams yields the same draws for X as X alone.
    base = 12345
    for sib in ("alpha", "beta", "gamma"):
        sib_rng = deck_sim.deck_rng(base, sib)
        [sib_rng.random() for _ in range(137)]   # sibling draws (the old batch leak)
    batch_x = [deck_sim.deck_rng(base, "x_deck").random() for _ in range(40)]
    single_x = [deck_sim.deck_rng(base, "x_deck").random() for _ in range(40)]
    assert batch_x == single_x


def test_deck_rng_distinct_keys_give_distinct_streams():
    # Per-deck means actually per-deck: two keys under the same base seed must not
    # collapse to one shared stream.
    a = [deck_sim.deck_rng(1, "a").random() for _ in range(20)]
    b = [deck_sim.deck_rng(1, "b").random() for _ in range(20)]
    assert a != b


def test_deck_rng_same_args_are_repeatable_in_process():
    assert ([deck_sim.deck_rng(7, "croak").random() for _ in range(30)]
            == [deck_sim.deck_rng(7, "croak").random() for _ in range(30)])


# --------------------------------------------------------------------------- #
# Bug 2 — esc set-iteration order is deterministic (not a set)
# --------------------------------------------------------------------------- #
def test_esc_trample_granters_is_not_a_set():
    # A set would walk in PYTHONHASHSEED-dependent order; the deck holds BOTH
    # granters and the loop casts the first affordable, so order is load-bearing.
    assert not isinstance(esc.TRAMPLE_GRANTERS, (set, frozenset))


def test_esc_trample_granters_order_is_fixed_and_stable():
    order = list(esc.TRAMPLE_GRANTERS)
    assert order == list(esc.TRAMPLE_GRANTERS)            # stable across iterations
    assert order == sorted(esc.TRAMPLE_GRANTERS)          # explicit, hash-independent
    assert order == ["Garruk's Uprising", "Goreclaw, Terror of Qal Sisma"]


# --------------------------------------------------------------------------- #
# Bug 3 — deck_registry same-date tie-break picks the newest (timestamped) file
# --------------------------------------------------------------------------- #
def _stub_deck_dir(tmp_path, monkeypatch, names):
    for n in names:
        (tmp_path / n).write_text("x", encoding="utf-8")
    monkeypatch.setattr(reg, "DECK_DIR", tmp_path)


def test_resolve_deck_same_date_tiebreak_picks_timestamped(tmp_path, monkeypatch):
    # Mirrors the real croak-and-dagger history: the bare-date file was archived,
    # the same-day 21:57:31 re-cut went live. Plain string sort wrongly returned
    # the bare-date (older) file because '.' > '-'.
    _stub_deck_dir(tmp_path, monkeypatch,
                   ["foo-20260623.txt", "foo-20260623-215731.txt"])
    assert reg.resolve_deck("foo").name == "foo-20260623-215731.txt"


def test_resolve_deck_picks_latest_date(tmp_path, monkeypatch):
    # A later DATE always beats an earlier one, even if the earlier carries a time.
    _stub_deck_dir(tmp_path, monkeypatch,
                   ["bar-20260601-235959.txt", "bar-20260629.txt"])
    assert reg.resolve_deck("bar").name == "bar-20260629.txt"


def test_resolve_deck_same_date_two_timestamps_picks_later(tmp_path, monkeypatch):
    _stub_deck_dir(tmp_path, monkeypatch,
                   ["baz-20260623-100000.txt", "baz-20260623-215731.txt"])
    assert reg.resolve_deck("baz").name == "baz-20260623-215731.txt"


def test_resolve_deck_single_file_unchanged(tmp_path, monkeypatch):
    # Clock-neutrality guard: with exactly one matching file (the live state of
    # every deck today) resolution is the identity — the fix can't move a clock.
    _stub_deck_dir(tmp_path, monkeypatch, ["qux-20260510.txt", "other-20260101.txt"])
    assert reg.resolve_deck("qux").name == "qux-20260510.txt"


def test_resolve_deck_returns_none_when_absent(tmp_path, monkeypatch):
    _stub_deck_dir(tmp_path, monkeypatch, ["qux-20260510.txt"])
    assert reg.resolve_deck("nope") is None


# --------------------------------------------------------------------------- #
# Cross-PYTHONHASHSEED reproducibility (the strongest determinism guarantee):
# the per-deck RNG stream AND the esc granter order are byte-identical regardless
# of the interpreter's string-hash randomization. One subprocess pair covers both.
# --------------------------------------------------------------------------- #
_PROBE = (
    "import json, deck_sim, esc_clock_lab as e;"
    "r = deck_sim.deck_rng(7, 'croak');"
    "print(json.dumps({"
    "'rng': [r.random() for _ in range(8)],"
    "'granters': list(e.TRAMPLE_GRANTERS)}))"
)


def _run_probe(hashseed):
    env = dict(os.environ, PYTHONHASHSEED=str(hashseed), PYTHONPATH=str(SCRIPTS))
    out = subprocess.run([sys.executable, "-c", _PROBE],
                         capture_output=True, text=True, env=env)
    assert out.returncode == 0, out.stderr
    return out.stdout.strip()


def test_rng_and_granter_order_are_pythonhashseed_independent():
    assert _run_probe(0) == _run_probe(1) == _run_probe(987654)
