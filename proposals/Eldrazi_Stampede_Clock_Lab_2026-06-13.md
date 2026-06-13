# Eldrazi Stampede Chaos — Kill-Turn Clock Lab (2026-06-13)

**Deck 1 of 10** in the Kill-Window Lab Sweep (`proposals/Kill_Window_Lab_Sweep_2026-06-13.md`).
Lab: `scripts/esc_clock_lab.py` (40k trials, seed 20260613), built on `speed_lab_core.py`.
Procedure: `workflows/WF_Kill_Window_Lab.md`.

## Claim vs. measured

| | Claim (hand-estimate) | Measured (lab) |
|---|---|---|
| Goldfish | **T6–8** (single range) | decap median **T8** (T6 ≈ 10%) · table median **T12** |
| Front edge | T6 | T6 = 10% decap (god-hand), 0% table |
| Never-in-14 | — | decap 1% / **table 11%** |

```
  P(kill <= turn T) %                        5     6     7     8     9    10    12    14
  decap (one opponent, 40)                   2    10    26    50    71    85    96    99
  table (all three)                          0     0     0     2     8    20    61    89
```

## Direction: optimistic front edge + decap/table conflation (the recurring pattern)

The "T6–8" claim is the **optimistic decap edge**. The decap median (T8) sits at the
*back* of the claimed range, not the middle — T6 is a 10% god-hand, not the norm.
And the single number silently meant decap: the **table clock is T12** (median),
four turns slower, and was never stated. This is the same failure the framework
documented seven times before — the hand-estimate rounds the god-hand into the
range and reports one clock for two.

The decap median isn't wildly off (T8 is in-band), so this is a milder miss than
Grand Design's two-turn gap — but the front edge is optimistic again (7-for-7 now)
and the table clock is genuinely slow.

## Why this shape

- **Wanderer is an 8-mana commander.** Even with 19 ramp pieces, the deck reaches
  the 8-mana threshold around T6–7, then needs ~2 swings to push one opponent to
  40. Decap median T8 is the honest consequence. The 10% T6 decaps are Sol-Ring /
  Mana-Vault / fast-ramp hands that land Wanderer T5–6 with a follow-up.
- **The table clock hangs on Craterhoof.** Focus-fire decaps one player fast but
  rolls slowly to the next two. The genuine table-kill is the Craterhoof alpha
  (trample + X/X distributed across the table) — but it needs Craterhoof in hand,
  8 mana, AND a wide board at once: 20% by T10, 61% by T12. Without it, the table
  dies to repeated swings (and 11% of games never table inside 14 turns).
- **Trample granters help the spread.** Garruk's Uprising / Goreclaw switch normal
  swings from focus to distributed in the model; drawing one accelerates the table
  clock, but they're singletons.

## Kill-shape prediction (pre-registered) — held

Stage-1 prior: *"combat focus-fire → decap fast / table slow; front edge suspect."*
Confirmed: decap T8 / table T12 (diverge ~4 turns), T6 front edge optimistic. The
kill-shape lens is now 8-for-8 at predicting the decap/table pattern.

## Card text

No new errors. The Summary's 2026-05-16 audit (~10 corrections) held under modeling.
One reinforcement worth noting: **Craterhoof Behemoth has haste itself**, and
Wanderer's static grants haste to the whole board, so the Craterhoof alpha is a
true same-turn swing (this-turn deploys included in the pump, per the ruling) — the
table-kill is real when the board is wide, just gated on assembling all three of
{Craterhoof in hand, 8 mana, width} simultaneously.

## Modeling caveats (heuristic, not a rules engine)

- Mana = lands + rocks/dorks + land-ramp spells, a floor. Ancient Tomb counted as 1
  (underclaim ~1 on Tomb turns); Nykthos and Selvala-tapping-into-a-titan upside
  capped (Selvala adds `max(1, greatest power)`, which floors at a dork early and
  realistically caps ~5–7 since the titans cost 10–12 to deploy first).
- Cascade resolved against the real library (scan top to first nonland MV<8; power
  added only if a creature) — faithful to the deck's ~50% creature density, so
  whiffs into ramp/removal cost the dump nothing.
- Damage unblocked (goldfish convention). The pod runs flying blockers, so the
  ground-token table clock is flattered here — the real table clock is *slower*
  than T12 against blockers (per the bake-off "conventions aren't deck-neutral" note).
- Normal swings focus-fire (rc/er/gd convention); only Craterhoof (and a trample
  board) distributes. Etali's free-cast value, Sunbird chains, and Annihilator
  board-stripping are not modeled — all push the real clock *faster on resource
  denial* but not on raw damage, which is what's measured.

## Verdict for the Summary

Replace `Goldfish: T6–8 (unverified)` with:
**`Clock: T8 decap (median; T6 ≈ 10% god-hand) / T12 table (lab 2026-06-13, esc_clock_lab.py) · Through interaction: slower (unverified — goldfish only; no blockers/disruption model)`**

Pod-bar read (decap T≤7): the deck clears T≤7 decap only **26%** of the time — it
does **not** race the T6–7 combo pod, consistent with the Summary's own "vulnerable
to combo / slow goldfish" and the Pod Matchup posture. No card swaps proposed here
(verification pass only); the clock confirms the 14/20 Solid posture rather than
challenging it.
