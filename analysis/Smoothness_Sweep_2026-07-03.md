# Smoothness Sweep — Mulligan × Momentum (2026-07-03)

Joint test of the two "smoothness" hypotheses, using `deck_sim.simulate_flow` (the
draw-aware flow pass) as the single instrument. Reproduce: `python
scripts/smoothness_sweep.py --trials 8000`.

**The two hypotheses** (user, 2026-07-03):
- **H1 — mulligan primacy:** the opening hand is most crucial, so a sharper,
  deck-specific mulligan is the main lever for "always able to do something."
- **H2 — momentum:** the deck needs enough draw/selection to keep the hand stocked.

**Design.** Per deck, a 2×2 (paired shuffle stream), metric = mean dead turns T1–10
(lower = smoother):
- keep ∈ { **land** = land-count default mulligan, **plan** = the deck's plan-aware
  keep-spec } — the sharpest mulligan we have (H1 lever).
- draw ∈ { **on** = real card draw executed, **off** = draw spells draw nothing }
  (H2 lever).

## Result — H2 dominates H1 by ~15×

Roster averages (17 decks), dead turns *removed* by each lever:

| Lever | Effect |
|---|---|
| **H2** — add the draw suite (off→on), sharp mulligan | **+0.301** dead turns removed |
| **H1** — sharpen the mulligan (land→plan), gas on | **+0.020** dead turns removed |
| H1 — sharpen the mulligan, gas off | +0.027 |
| **Interaction** (H1 lever gas-off − gas-on) | **+0.007** |

**Read:** the draw suite is the overwhelming smoothness lever — turning it on
removes ~15× more dead turns than sharpening the mulligan to the plan. The
mulligan is nearly flat (≈0.02 turns). The user's **joint intuition** — that the
mulligan matters more when gas is low — is directionally **confirmed** (+0.027 gas-off
vs +0.020 gas-on) but the interaction is negligible in magnitude (+0.007).

## Nuances

- **Draw helps every deck** (dDraw +0.08…+0.53, all positive). Biggest beneficiaries:
  Eldrazi (0.53), Crystal Sickness (0.49), Ms. Bumbleflower (0.47), Curse (0.43) —
  draw suites doing heavy lifting.
- **Radiation is the tell (dDraw +0.08).** It barely benefits from its draw suite —
  because it *has* almost none (7 ramp / 3 selection). That is exactly why it reads
  99% keepable yet ~45% hellbent by T8: no gas to execute. The fix for its
  smoothness is to **add repeatable draw**, not to sharpen the mulligan.
- **The plan mulligan can slightly REDUCE smoothness** (dMull < 0 for Dark Lord's
  Army −0.08, Grand Design −0.08, Forced Liquidation −0.04). The plan-aware keep
  optimises for *finding the win line*, which sometimes keeps a clunkier curve than
  a pure land-count keep would. Sharpening the mulligan toward the plan trades a
  hair of smoothness for consistency of *finding* — a real, if tiny, tension.

## Takeaway for the two hypotheses

1. **H2 is the dominant smoothness lever** — draw/selection density. Confirmed and
   quantified. This is where to build for "always able to do something."
2. **H1 (mulligan) is a weak smoothness lever.** Consistent with the prior finding
   that the plan-aware mulligan moved opening-hand consistency only ~+1pp — the
   mulligan sets the opening *state*, not the depletion *slope*. Sharpen it to be a
   better **pilot**; change the **75** (add gas) to make the **deck** smoother.
3. The mulligan×gas interaction the user hypothesised is directionally right but
   too small to act on. Momentum first.

Inherits every `simulate_flow` caveat (goldfish, lands-only mana floor, paced
'one' spend) — read as a relative comparison of the two levers, not absolute turns.
