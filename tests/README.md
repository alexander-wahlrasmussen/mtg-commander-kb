# tests/ — testing the instruments, not the decks

The clock labs are test-first *deckbuilding*: state a hypothesis ("decap T6–7"),
run the lab, let red/green drive the build. But in real TDD you trust the test
runner because thousands of people tested it. Here the "test runner" is our own
simulator — `deck_sim.py`, `speed_lab_core.py` — and **nothing tested it**. Every
retraction in memory (the colour-divide artifact, Grand Design's "39%→89%" fetch
bug, the singleton sideboard over-count) was the same failure: a false red/green
from an uncalibrated instrument. This suite calibrates the instrument.

## Run

```bash
pip install -r ../requirements-dev.txt    # pytest + hypothesis only
python -m pytest -m "not golden"          # fast hermetic gate; ~1–2s
python -m pytest                          # + golden clock tier (needs the bulk; ~30s)
```

**Tier 1 + the hermetic Tier-2 tests** (null-reduction, CSB contract replay) are
hermetic by design: synthetic card records (`helpers.py`) or recorded fixtures,
**no** 168 MB Scryfall bulk, no network, no browser. They run in CI as the
`tests` job of `.github/workflows/repo-health.yml`.

**The golden clock tier** (`-m golden`) re-runs the real labs, so it needs the
gitignored Scryfall bulk and **auto-skips without it**. It runs in CI's
bulk-having `decks` job (pinned to the snapshot's interpreter) and on a local
full `pytest`. Markers are registered in `../pytest.ini`.

## What's covered (Tier 1)

| File | Core | Pins |
|---|---|---|
| `test_deck_sim.py` | `deck_sim` | colour model (produced_mana vs identity), fetch resolution, `keep_hand` band, `parse_deck` round-trip / sideboard exclusion / commander-to-zone / alias resolution, **determinism** (same seed → same output), alias-table parsing |
| `test_speed_lab_core.py` | `speed_lab_core` | `Table` decap-vs-table clock + the decap ≤ table invariant, `median`/`cum`/`never_pct`, `build_lib` swaps, `slot_complete` tutor assignment |
| `test_deck_registry.py` | `deck_registry` | every row well-formed, cc_axes sum to cc, stem uniqueness + no prefix-collision (the parse_deck routing hazard), kill-tree/accessor cross-refs |

Three kinds, by design:
- **unit** — a function, one input/output.
- **property** (`@given`, Hypothesis) — an invariant over generated inputs (the
  land band, the cum-curve monotonicity, parse round-trip count).
- **REGRESSION** — tagged in the test name. Pins a bug that already shipped a
  wrong conclusion. Deleting one re-opens that hole.

## What's covered (Tier 2)

Tier 1 tests the *cores*; Tier 2 pins the *labs' output* and the *relationships
between scripts*.

| File | Kind | Pins |
|---|---|---|
| `test_clock_golden.py` | golden / characterization | each clock lab re-run at its fixed seed + small trials. **EXACT** tier: curves bit-for-bit vs `golden/clock_snapshot.json` (same interpreter only — see the `_meta.python` guard). **TOLERANCE** tier: snapshot median within ±1 turn of the committed `analysis/pod_gauntlet_clocks.json` (cross-version robust). Reuses `pod_gauntlet.CLOCKS`/`parse_row` — the same machinery `--refresh` uses. `golden`-marked; needs the bulk. |
| `test_null_reduction.py` | differential / metamorphic | `interaction_meta_lab --tax 0` reproduces `self_meta_lab`'s per-deck WIN bit-for-bit (Backlog #6's null reduction, now a CI test). Hermetic. |
| `test_contract_csb.py` | contract (record/replay) | `find_combos.find_my_combos` parses + paginates + aggregates the Commander Spellbook response into `(identity, included, almost, changing)`. Replays `fixtures/csb_find_my_combos.json` offline; `--record` re-hits the live API to surface drift as a fixture diff. `contract`-marked; offline by default. |

Regenerate the golden snapshot after an **intended** lab change (review the diff):

```bash
python tests/test_clock_golden.py --update     # needs the bulk
python tests/test_contract_csb.py --record     # needs the network (CSB drift refresh)
```

## The rule

**Every retraction earns a regression test.** When a sim bug is found and fixed,
add a `*_REGRESSION` test here before moving on — the code equivalent of what
`REF_Domain_Principles.md` does for card-text gotchas: make the lesson permanent.

## Roadmap

Tier 1 + Tier 2 are this suite. Tier 2 shipped the golden clock snapshot, the
null-reduction differential, and the CSB contract test (Backlog #9). Tier 3
(broader metamorphic suite — Sol Ring shouldn't slow the clock, reskin-alias
invariance; deterministic-simulation seed threading; mutation testing) is tracked
in `../Backlog.md` #9. We do **not** chase coverage %, and we do **not**
unit-test the one-off `analysis/` scripts.
