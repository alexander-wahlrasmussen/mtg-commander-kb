# Framework Bake-Off — do deck-evaluation frameworks predict results?

**2026-06-16 · `scripts/framework_bakeoff.py` · lab `pod_gauntlet_clocks.json` oracle**

**Verdict.** Of six contestants, **only direct clock measurement positively predicts which
deck actually wins — and it holds across all four outcome oracles** (two lab clocks + the two
win-probability models, `pod_gauntlet` and `self_meta`). Every published "deck quality / power"
framework — the in-house **Conversion Check**, the community **Disciple of the Vault** power
formula, the official **WotC brackets**, **Based Deck Department's mana-budget**, and **BDD's
consistency** model — scores **≤ 0** against the win oracle, with no consistent positive sign on
any of the four. The two most serious quality frameworks run *negative*: **Disciple of the Vault
is negative on all four oracles** (−0.37 to −0.45 — robustly backwards), and the Conversion Check
is negative-to-zero on all four. The answer to "would another framework pick better decks?" is
**no — and Disciple would pick worse.** What works is what the repo already does: simulate the
clock.

---

## The question

Does The Conversion Check (the 20-point framework the KB is organized around) actually
predict *results*, and would a different, externally-published framework rank our decks
better? Asked by the user 2026-06-16; the empirical hook was the repo's own "score ⊥ clock at
the top" thesis (`Kill_Window_Lab_Sweep_2026-06-13`, `Self_Meta_Ranking`). This bake-off makes
it a measurement: score all 16 active decks under each framework, then rank-correlate each
framework against the outcome.

## Method

- **Contestants** (all from their *actual published rubrics*, not memory):
  - **Conversion Check** — the stored 4-axis total (Core Loop / Kill Reliability / Durability / Interaction), from the Summaries.
  - **BDD mana-budget** — Based Deck Dept (YouTube `7lJJPXGfFNs`): sum the mana of the cheapest **win line**; lower = faster. Win lines hand-encoded from each Summary + `kill_tree` + the Kill-Window sweep (`--winline`); X/mana-gated lines (Torment/Banefire/Finale) given a lethal-mana override.
  - **Disciple of the Vault** — the explicit formula `P = 2/A + (D/2 + T + R/2)/2 + I/20` (A=avg nonland CMC, D=draw sees-3+/repeatable, T=tutors CMC≤4, R=ramp CMC≤2, I=interaction; commander counts 2 for D/T).
  - **BDD consistency** — BDD's math video (`mwTCvRTunKQ`, "11 to guarantee by T2" / ~38 lands): how completely the deck fills its functional bases.
  - **WotC brackets 1–5** — the official criteria (GC count + mass-land-denial + extra-turn detection).
  - **Pure clock (null)** — rank by the lab decap median turn. "Is it all just speed?"
- **Oracles (four)** — two lab kill clocks from `pod_gauntlet_clocks.json` (**TABLE median** = closing *all* opponents = winning; **decap median** = first opponent dead; faster = better) plus the two project *results models* (**`pod_gauntlet` P(beat the T6-7 combo pod)** and **`self_meta` P(win in a random roster pod)**; higher = better). Running against all four tests whether the verdict is an artifact of the goldfish clock or robust to the actual win-probability models.
- **Statistic** — tie-aware Spearman ρ, every framework oriented so *higher = "this deck should win."* ρ = +1 perfect agreement, 0 unrelated, −1 backwards.

Reproduce: `python scripts/framework_bakeoff.py --bakeoff` (and `--scores`, `--winline`, `--tags all`).

## Result

Spearman ρ for each framework against each of the four oracles (every framework oriented so
higher = "should win"):

| Framework | gauntlet P(win) | self_meta P(win) | TABLE clock | decap clock | N |
|---|---:|---:|---:|---:|---:|
| **Pure clock (null)** | **+0.903**¹ | **+0.426** | **+0.561** | +1.000¹ | 16 |
| BDD mana-budget | +0.139 | +0.019 | −0.034 | +0.085 | 16 |
| BDD consistency | +0.258 | −0.200 | +0.008 | +0.408 | 16 |
| WotC bracket 1–5 | −0.253 | +0.168 | +0.029² | −0.116 | 16 |
| **Conversion Check** | −0.259 | −0.061 | **−0.264** | −0.448 | 15³ |
| **Disciple of the Vault** | **−0.448** | **−0.374** | **−0.419** | −0.376 | 16 |

¹ **semi-circular** — the P(win) models are built partly *from* the clock (gauntlet from decap +
disruption; self_meta from the table clock + durability), so pure_clock correlates with them by
construction. The honest read: even the *less*-circular self_meta number (which uses the table
clock, not the decap clock pure_clock is scored on) is +0.426 — clock measurement still leads.
² near-zero variance: 15/16 decks bucket to bracket 3, so WotC can't rank-order this roster.
³ Zero-Sum is unaudited (no CC score).

## What it means

1. **The quality frameworks don't predict winning.** All four land ≤ +0.03 against the
   win-clock. Treat them as a coin flip on "which deck closes the game faster."
2. **The Conversion Check and Disciple run *backwards*.** Both are negative against both
   oracles. They reward card advantage, durability, and interaction — real virtues — but on
   this roster those track *grind*, not *speed*: the slowest deck (Crystal Sickness, T11) is
   the **highest** Disciple score (8.8) and a solid 17/20; the fastest (Genome, T7) is the
   **lowest** Disciple (3.3) and only 15/20. This is the repo's "score ⊥ clock at the top"
   thesis, now measured — and it's not unique to the in-house framework: an external,
   widely-used community formula is *more* anti-correlated.
3. **Only measuring the clock predicts winning — on every oracle.** Pure-clock is the lone
   framework with a consistent positive sign across all four (+0.43 to +0.90). The gauntlet/decap
   figures are inflated by semi-circularity, but the clean number — self_meta P(win), which
   derives from the *table* clock, not the decap clock pure_clock is scored on — is still +0.426.
   The best "framework" for forecasting results is direct simulation, exactly the clock-lab
   methodology already in the repo. An off-the-shelf framework adds nothing, and a power-formula
   (Disciple) actively misleads — *robustly*, on all four oracles.
4. **BDD's mana-budget is the interesting near-miss** (ρ ≈ 0). Its hypothesis — cheaper win
   line ⇒ faster deck — fails on the decks whose kill is **finding-gated, not mana-gated**.
   Showcase: Crystal Sickness has the *cheapest* win line (3 mana: Golbez + a high-power
   creature) yet is the *slowest* deck (T11), because it must dig a drain bomb and run several
   cycles — effort BDD-mana can't see. Mana cost ≠ clock when consistency is the bottleneck.

## Mulligan robustness check — is an aggressive mulligan the missing payoff?

Challenge (user, 2026-06-16): a null across *every* framework should make us suspect the
**oracle**, not conclude quality is worthless. The pod allows **2 free mulligans** — does the sim
mulligan aggressively to a *functional* hand, or leave consistency unrewarded?

**Found:** `deck_sim.opening_hand` takes up to 2 mulligans (matches the pod) but its keep rule is
**land-count only** — `keep a 7 with 2–5 lands`, regardless of whether the hand can *do* anything.
It never digs toward a play. Added an opt-in **smart keep** (`DECK_SIM_SMART_KEEP=1`): also require
≥1 nonland with CMC ≤ 3 (mulligan a "lands + only expensive cards" hand). Re-harvested all 16
clocks under it (`pod_gauntlet.py --refresh`) and re-ran the bake-off (`--clocks`).

**Result: 0 of 16 decks changed their decap or table median, and the bake-off was byte-identical.**
The mulligan was not the leak. Two structural reasons: (1) most of the roster is low-curve (avg
nonland CMC 2.4–3.2), so a 2–5-land hand almost always already holds an early play — only the one
high-CMC deck (Eldrazi, 5.25) sped up, and only at the *front edge* (T6 10→12%), not the median.
(2) Kill-turn **medians** are gated by drawing/assembling pieces over 7–11 turns; two opening
mulligans move the god-hand front edge, not the median the verdict reads. A piece-*specific* dig
(model each deck's exact plan) would help finding-gated decks more, but is bounded by ~2 cards of
selection, is deck-specific to model, and would still move front edges, not medians.

**So the verdict is robust to the mulligan.** The remaining, deeper leak is the one this can't fix:
the oracle is a **solitaire goldfish** — Interaction and Durability (two of the Conversion Check's
four axes, and Disciple's `I` term) score zero with no opponents, *however* you mulligan. That is
the structural reason the quality frameworks can't correlate; the tell is that CC is least-negative
against self_meta, the one oracle with a durability overlay. Fixing it needs a real multiplayer
interaction model (the rules engine the project deliberately never built), not a better mulligan.

*N=16 fragility note:* re-harvesting at the same 8k trials shifted the **TABLE**-oracle ρ's by
~0.1–0.2 vs the committed snapshot (CC vs table −0.264 → −0.387; pure_clock +0.561 → +0.744) while
the decap and P(win) oracles stayed stable — the integer-turn table median is noise-sensitive at 16
points. One more reason to read the cross-oracle *pattern*, not any single ρ.

## The data (`--scores`)

| deck | clock | CC | Disciple | WotC | BDD-c | BDD-mana |
|---|---|---|---|---|---|---|
| genome | T7 | 15 | 3.31 | 3 | 4.33 | 12 |
| radiation | T7 | 18 | 3.46 | 3 | 4.22 | 3 |
| replication | T7 | 17 | 6.87 | 3 | 5.0 | 10 |
| lorehold | T8 | 18 | 4.37 | 3 | 4.88 | 16 |
| earthbend | T8 | 17 | 4.59 | 3 | 4.57 | 8 |
| exiles | T8 | 17 | 5.38 | 3 | 4.04 | 9 |
| curse | T8 | 17 | 7.03 | 3 | 4.17 | 10 |
| bumbleflower | T8 | 15 | 5.97 | 2 | 4.71 | 6 |
| eldrazi | T8 | 14 | 6.38 | 3 | 4.67 | 16 |
| dark_lords | T9 | 19 | 7.66 | 3 | 4.38 | 11 |
| diminishing | T9 | 17 | 5.19 | 3 | 4.88 | 8 |
| lightning | T9 | 19 | 5.06 | 3 | 4.62 | 14 |
| zero_sum | T9 | — | 6.64 | 3 | 4.29 | 10 |
| grand_design | T10 | 19 | 6.76 | 3 | 4.0 | 12 |
| calamity | T10 | 18 | 4.25 | 3 | 4.21 | 14 |
| crystal | T11 | 17 | 8.8 | 3 | 4.0 | 3 |

## Limitations — read before quoting a ρ

- **N = 16 (CC = 15).** Critical |ρ| ≈ 0.50 at p < .05, so only pure_clock clears significance
  on any single oracle; the quality frameworks' negatives are *suggestive, not significant in
  isolation*. The robust claim is **cross-oracle consistency, not any one ρ**: across the four
  oracles, **Disciple is negative on all four** (−0.37 to −0.45) and **pure_clock positive on all
  four**, while CC is negative-to-zero on all four and BDD-mana/consistency/WotC never hold a
  sign. A framework that genuinely predicted winning would show a stable positive ρ across
  independent oracles; only pure_clock does. That pattern is hard to dismiss as 16-point noise —
  but it is a verdict about *this roster*, not a proof about frameworks in general.
- **The oracle is a *goldfish* clock, not real games.** This measures prediction of the
  *simulated* outcome (Layer 1). Whether the sim itself matches reality is **Layer 2** —
  `scripts/game_log.py` is the capture end; a future `calibrate.py` closes it.
- **WotC has no variance here** (everything is bracket 3 by the 3-GC house cap), so its ρ is
  meaningless on this roster — not a verdict on the bracket system generally.
- **BDD-mana rests on 11 fuzzy win-lines** (combat/attrition/X). User reviewed and accepted the
  fuzziness 2026-06-16; ρ ≈ 0 is consistent with the finding either way.
- **Frameworks measure different objectives.** The Conversion Check *explicitly* holds the
  clock out ("not a fifth axis"); it optimizes structural quality, which is a legitimate goal —
  just not win-speed. This bake-off says the score is not a results proxy, not that the
  framework is "wrong" for what it set out to do. Read the score for *whether* a deck converts,
  the clock for *when*, and now this for *which to trust when you want to win.*

## Next

- **Richer oracle — DONE 2026-06-16.** Reran against `pod_gauntlet` P(beat the pod) and
  `self_meta_lab` P(win); the verdict held (table above). The goldfish-clock proxy was not
  driving it.
- **Layer 2 (the remaining gap):** accumulate real games via `game_log.py`, then `calibrate.py`
  to test the *oracles themselves* against reality — the only thing that can validate this whole
  tower. Until then this is prediction of the *simulated* outcome.

## Related

- `scripts/framework_bakeoff.py` — the tool (Phases 1–4).
- `campaigns/Kill_Window_Lab_Sweep_2026-06-13.md` · `campaigns/Self_Meta_Ranking.md` — the "score ⊥ clock" thesis this confirms.
- `reference/REF_The_Conversion_Check.md` — the incumbent, and its deliberate clock-exclusion.
- memory `project_framework_bakeoff` — project log.
