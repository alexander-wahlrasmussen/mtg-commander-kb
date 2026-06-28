# Finisher Mixture Pilot — Backlog #11 "proper version", first increment

**Date:** 2026-06-28
**Builds on:** `analysis/Finisher_Coverage_Map_2026-06-28.md` (the coverage audit that retired
cost (a)). **Artifacts:** `scripts/finisher_mixture.py`, `analysis/finisher_lines.json`,
`scripts/lw_clock_lab.py` (`perline_kill` + `--mode perline`), `tests/test_finisher_mixture.py`.

## What the proper version still needed — and what this delivers

The coverage audit proved the per-line **MIN** ("race every kill line, not just the goldfish")
**already exists** for every deck: each clock lab is a multi-line best-line goldfish taking the
earliest decap/table over its lines on one correlated game. So the proper version's remaining
delta was never *adding* lines — it was making each line **first-class and switchable**, so pod
state can **disable** one:

> graveyard hate disables a storm/recursion line · a near-40 table disables chip · a one-spell
> lock disables a multi-spell burn/combo turn ([[feedback_interaction_role_protect_vs_disrupt]])

A single blended CDF (what the harvest emits) cannot be switched off component-wise. This
increment builds the consumer that can.

## The architecture

- **`lw_clock_lab.perline_kill`** — the per-line primitive. Runs Lightning War's two REAL labbed
  lines (burn race `goldfish_kill` + Reiterate/Seething Song combo `lw_combo_lab.assembly_turn`)
  on ONE shared pre-rolled game and returns `{"burn": (decap,table), "combo": (decap,table)}`.
  `bestline_kill` now just calls it and takes the min, so the harvested curve — and its golden
  snapshot — are **byte-identical** (verified: golden EXACT + tolerance both green).
- **`finisher_mixture.py`** — reads the lines separately, applies a pod-state **disabler vector**,
  and reports the earliest VIABLE close over the lines NOT disabled. `analysis/finisher_lines.json`
  is the schema artifact: per deck `{name, grid, split, lines:[{line_id, kind, decap, table, med,
  never, disablers, note}], bestline_check?}`.

## The load-bearing safety property: bounded above

The disabler vector **only ever removes lines**, so the mixture is **bounded ABOVE by the
harvested best-line curve** — it can model *degradation under hate*, never a faster fiction. This
is what makes it safe to ship UNCALIBRATED: the "every deck looks faster" worry was about *adding*
lines (already done, per the audit); *removing* lines can only push a clock later or to never.
Pinned by `test_bounded_above` + `test_null_reduction_*`.

**Null reduction (exact):** with no conditions active, the mixture reproduces the harvested curve
bit-for-bit. At 8k trials, LW's `bestline_check` decap `[11,28,41,55,70,83,96,99]` / table
`[11,27,38,45,52,59,71,83]` == `pod_gauntlet_clocks.json` LW exactly. Per-game equality
(`mixture{} == bestline_kill`) is a golden test.

## The LW demonstration (honest, card-grounded)

| pod state | live lines | mixture decap / table |
|---|---|---|
| `{}` | burn, combo | **T8 / T9** (== harvested) |
| `{graveyard_hate}` | burn, combo | **T8 / T9** — *unchanged* |
| `{rule_of_law}` | NONE | **never / never** |

- **`graveyard_hate` disables NEITHER LW line** — both assemble from hand (the combo's primary
  pieces are Reiterate + Seething Song, cast from hand; the burn is graveyard-independent). An
  honest "not every hate hits."
- **`rule_of_law` (Rule of Law / Eidolon of Rhetoric — one noncreature spell per turn) disables
  BOTH** — the burn race needs to chain several noncreature spells a turn (the pingers fire per
  cast), and the combo turn casts multiple noncreature spells. Under a one-spell lock LW does
  nothing. A real, card-text-grounded switch the single blended curve could not express.

## What is real vs UNCALIBRATED

- **Real:** the architecture, the per-line CDFs for LW (lab-backed), the bounded-above property,
  the null reduction, the disabler *mechanism*.
- **UNCALIBRATED:** whether a given disabler tag changes *real win-rate* by the modelled amount.
  The tags are grounded in oracle text, not back-tested against games. Per the honest prior, the
  mixture is **not** baked into the tier list / gauntlet — it is a separate consumer, exactly as
  the #11 MVP left the tournament untouched. It earns promotion only once Backlog #10 logs games
  and `calibrate.py` can grade the switched mixture.

## Roster-wide rollout (the rest, gated on #10)

Only LW is `split`; every other deck is a single pass-through line in `finisher_lines.json` (no
sub-lines to disable). Splitting a deck = teaching its clock lab to emit per-line turns (which
line fired), then tagging each line's disablers from card text. Priority candidates where a
disabler would actually bite (a gy-dependent line beside a non-gy one): **Genome** (Underworld
Breach / Mizzix's Mastery graveyard-storm vs the live Wizard ping), **Diminishing** (Gravecrawler
loop + Living Death reanimation vs the aristocrat board), **Radiation** (Mindcrank+Bloodchief vs
the counter-board). Each needs the read-the-card pass + a golden snapshot delta. Do them only as
#10 games arrive to validate that the switched mixture predicts results better than the single
curve — otherwise it is added complexity for an unproven model.

**Bottom line:** the proper version's switchable-line capability now exists and is proven on LW,
bounded above and null-reduced; its roster-wide value and calibration are the same gate as #10.
