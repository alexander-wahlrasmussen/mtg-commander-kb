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
python -m pytest                          # from repo root; ~1–2s
```

Hermetic by design: synthetic card records (`helpers.py`), **no** 176 MB Scryfall
bulk, no network, no browser. It runs in CI as the `tests` job of
`.github/workflows/repo-health.yml`.

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

## The rule

**Every retraction earns a regression test.** When a sim bug is found and fixed,
add a `*_REGRESSION` test here before moving on — the code equivalent of what
`REF_Domain_Principles.md` does for card-text gotchas: make the lesson permanent.

## Roadmap

Tier 1 is this suite. Tier 2 (golden tests pinning the committed clock medians;
formalised null-reduction differentials) and Tier 3 (metamorphic suite; mutation
testing) are tracked in `../Backlog.md` #9. We do **not** chase coverage %, and we
do **not** unit-test the one-off `analysis/` scripts.
