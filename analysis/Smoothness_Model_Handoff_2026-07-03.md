# Smoothness Modeling — Discoveries & Learnings (handoff, 2026-07-03)

Session writeup so this can be picked up with fresh eyes. Companion docs:
`analysis/Smoothness_Sweep_2026-07-03.md` (the experiment), `scripts/deck_sim.py`
(`--flow`), `scripts/smoothness_sweep.py`, `scripts/deck_doctor.py` (`--vitals`).

## The question

Can we model deck "smoothness" — every deck should be able to *do something* every
turn? The two feel-bads named up front: (a) mana-starved with a hand you can't
cast, (b) hand empty, praying to the topdeck. Two hypotheses: **H1** the opening
hand / mulligan sharpness is the crucial lever; **H2** sufficient draw/selection/
ramp keeps momentum.

## What we built

`deck_sim.py --flow` (`simulate_flow`) — a tempo pass, isolated from `simulate()`
(golden figures untouched). Unlike the consistency pass, it **spends mana and
removes cast cards from hand**, then reports per turn: live% (naive AND plan-aware
via keep-spec tags), dead turns **split by cause** (starved = spell stuck, no mana
vs flooded = nothing to cast), hand-size trajectory, hellbent (≤1 card), mean dead
turns. `--flow-spend greedy|one` brackets hand-emptying (deploy-all upper bound vs
one-marquee-play lower bound). **Card draw is executed** (`draw_map`): one-shots
refill the hand (cantrip nets 0), permanent engines add +1/turn while in play.

Surfaced in `deck_doctor <deck> --vitals` (smoothness line) and `deck_doctor --all
--vitals` (`dead` / `hlb%` columns). INFO-only by design — a goldfish can't tell a
race deck emptying *because it's winning* from a grinder running dry, so it never
flips a verdict.

## Discoveries

1. **The consistency pass structurally hides the gas problem.** It never spends a
   card, so `castable_by_turn` says Radiation has a play 100% of turns — while the
   flow model shows its hand crashing to ~1 card, ~45% hellbent by T8 (paced).
   "Looks smooth, runs dry" was invisible to every prior tool.
2. **Smoothness is two axes, not one, with opposite fixes.** Gas-out / topdeck-lock
   (Radiation, Lightning War, Grand Design, Croak — dead turns are *flooded*,
   hellbent high) wants **repeatable draw**. Mana-clog (Eldrazi: only 6% hellbent
   but 3.2 mean dead turns, 33% *starved* @T4 — hand full, can't deploy) wants
   **cheaper ramp / lower curve**. Any single "smoothness score" would have blended
   these away.
3. **H2 beats H1 by ~15×** (`Smoothness_Sweep_2026-07-03.md`, 2×2 keep×draw,
   paired): the draw suite removes ~0.30 mean dead turns; sharpening the mulligan
   (land-count → plan-keep) removes ~0.02. The mulligan×gas interaction the user
   hypothesised is directionally real (+0.007) but negligible. **The mulligan sets
   the opening state; composition sets the depletion slope.** Consistent with the
   earlier +1pp plan-keep finding: change the 75, not the mulligan.
4. **Actionable:** Radiation gains almost nothing from draw-on (+0.08 vs roster
   +0.30) because it *has* almost no draw (3 selection tags). Its smoothness fix is
   adding repeatable draw — a concrete swap-lab candidate. Plan-keep can even cost
   a hair of smoothness (Dark Lord's −0.08): it optimises *finding the win*, not
   curve — a real but tiny tension.

## Learnings (methodological)

- **A model that spends but doesn't draw punishes card advantage.** v1 ranked
  Ms. Bumbleflower (drawiest deck) *least* smooth and Eldrazi (zero draw) smoothest
  — it was measuring curve, not gas. Executing draw inverted it to match intuition.
  Lesson: validate a new metric by rank-ordering against decks you know before
  trusting it — the wrongness was only visible in the roster run.
- **Fresh read-the-card instance:** draw *payoffs* ("whenever you draw a card,
  ...") are not draw *sources*. Sheoldred / Psychosis Crawler initially credited
  as +1/turn engines (inflating Forced Liquidation); fixed by stripping trigger-
  condition clauses before matching the effect, with REGRESSION tests. Niv-Mizzet
  (payoff clause AND real engine clause) pinned as the survivor case.
- Known residual over-credit: mana/discard loot (Glint-Horn class) still reads as
  an engine though it only filters. Documented floor, acceptable for ranking.

## Caveats (all documented in-code)

Goldfish (reactive turns read dead — trust it for proactive decks); lands-only
mana floor (starved = upper bound; a ramp-aware flow belongs on the
`speed_lab_core` Goldfish, which already deploys rocks); plan-live% is NOT
cross-deck comparable (confounded by keep-spec tag counts); calibration against
real games still blocked (0 logged).

## Open threads for a next session

1. **Radiation draw pass** — pick candidate repeatable-draw swaps, verify with
   `--flow` A/B (does `dead`/`hlb%` actually move?) + clock lab (does it cost speed?).
2. **Ramp-aware flow** on the Goldfish harness (rocks/dorks in the mana floor) —
   would firm up the starved axis, esp. Eldrazi.
3. Dashboard: bake flow curves into the deck pages (same pattern as `bake_hands`).
4. Tier-list interplay: does smoothness correlate with pod_gauntlet outcomes, or
   is it another orthogonal axis like CC score?
