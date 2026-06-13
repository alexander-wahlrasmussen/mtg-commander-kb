# Curse of the Scarab — Kill-Turn Clock Lab (2026-06-13)

**Deck 5 of 10** in the Kill-Window Lab Sweep (`campaigns/Kill_Window_Lab_Sweep_2026-06-13.md`).
Lab: `scripts/cos_clock_lab.py` (40k trials, seed 20260613), built on `speed_lab_core.py`.
Procedure: `workflows/WF_Kill_Window_Lab.md`.

## Claim vs. measured

| | Claim (hand-estimate) | Measured (lab) |
|---|---|---|
| Goldfish | **T7–9** (single range) | decap median **T8** (T7 = 32%) · table median **T11** |
| Front edge | T7 | T7 = 32% decap, 4% table |
| Never-in-14 | — | decap 1% / table 9% |

```
  P(kill <= turn T) %                        5     6     7     8     9    10    12    14
  decap (one opponent, 40)                   3    13    32    56    75    86    96    99
  table (all three)                          0     1     4    12    28    46    76    91
```

## Direction: the decap claim HOLDS — the miss is only the decap/table conflation

This is the **most accurate hand-estimate in the sweep so far.** "T7–9" is a good
description of the **decap** clock: the median is **T8**, squarely in-band, and the
T7 front edge is a healthy 32% (not a 1–10% god-hand like every prior deck). For the
first time in the campaign a front edge did **not** come back optimistic.

The one correction is the recurring single-number problem: "T7–9" silently meant
decap and never stated the table clock, which is **T11** — three turns slower. So
the deck *decaps* a player in the claimed window but does **not** win the game (table)
until ~T11.

## Why this shape — two different engines drive the two clocks

The deck reads as "drain → converge," but the lab shows a **3-turn decap/table gap**
because the decap and the table are powered by *different* engines:

- **Combat is the decap driver (focus-fire, diverge).** Lord-pumped Zombies
  (Death Baron / Undead Warchief / Lord of the Accursed / Cemetery Reaper / Narfi +
  Mikaeus) swing for `count × (2 + lord bonus)` — with ~5 Zombies and 2–3 lord power
  that is ~20 unblocked into one player, decapping ~T8.
- **The all-table drain is the table driver (converge, but modest per turn).** The
  Scarab God upkeep drains `X = your Zombies` to *each* opponent — but the median
  Zombie count is only ~4–5 through T7–9, so the symmetric drain is ~4–5/turn, and
  it takes until ~T11 to bring all three opponents to 0. Gray Merchant (devotion,
  ~6–8 to each, recurrable) and Shepherd of Rot accelerate it but don't collapse the
  gap. The combo (Warren Soultrader + Gravecrawler + Plague Belcher → kill_all) is a
  real table-kill but assembles in only ~1% of games by T12 — not the clock.

So the deck's *named primary* (Scarab upkeep drain) is the **table** clock, and its
*fastest* line (lord combat) is the **decap** clock — the opposite of how the Summary
frames it (drain primary, combat tertiary). The drain is inevitability, not speed.

## Kill-shape prediction (pre-registered) — held

Stage-1 prior: *"drain-led converge (Scarab/Gary/Shepherd hit all) with a combat
focus-fire decap accelerant; decap ≈ table, combat pulls decap ahead; table ~T8–9,
front edge T7 suspect."* Measured: combat decaps T8, all-table drain tables T11 — the
**pattern held** (combat leads decap, drain converges the table), now 10-for-10. The
absolute table prior (~T8–9) was optimistic by ~2 turns — same caveat as Crystal
Sickness: the shape lens predicts the decap/table *pattern*, not the absolute turn.
The decap front edge, unusually, was *not* optimistic.

## Card text

No errors — the Summary's thorough 2026-05-05 re-audit (~15 corrections) held under
modeling. Reconfirmed against `card_lookup.py` for the kill branches:

- **The Scarab God is a God, not a Zombie** — it does not count itself for X and
  lords do not pump it (modeled: Scarab excluded from the Zombie count).
- **Gray Merchant drains your devotion to black** (each {B} pip on your permanents,
  Gary's own {B}{B} included) — modeled by summing black pips from oracle mana cost.
- **Plague Belcher → each opponent loses 1 per *other* Zombie death**; the Warren
  Soultrader + Gravecrawler + Plague Belcher loop is mana-neutral and drains the
  whole table (self-limited by life) — a true `kill_all` when assembled.

## Modeling caveats (heuristic, not a rules engine — and conservative on Zombie count)

- The Zombie count is the master engine variable; token multipliers are flags
  (Diregraf Colossus, Necroduality, Grave Titan ETB+attack, Liliana DM +1,
  Cryptbreaker, Rot Hulk ETB, Living Death / Agadeem's mass dump). **The model still
  OMITS the deaths-based token engines** — Ghoulcaller Gisa, Wilhelt's death-replacement
  tokens + free sac outlets (Carrion Feeder), Crowded Crypt, Champion growth — because
  they need a death/sacrifice model the goldfish doesn't run. Those would *raise* the
  Zombie count and **speed the table clock toward (or past) T10**, so **T11 table is a
  conservative upper edge**, not a pessimistic one. The decap clock is unaffected.
- Mana = lands + rocks. Damage unblocked, no opposing interaction, and the Scarab God
  is never removed (its return-to-hand death trigger makes that realistic, but exile
  still answers it). So the goldfish is an upper bound on speed; the real table clock
  against interaction is slower (the Summary's own "through interaction T9–12").
- Devotion read from oracle mana cost because the parsed deck records carry no
  `mana_cost` field (a bug that initially zeroed Gary's drain — caught and fixed).

## Verdict for the Summary

Replace `Goldfish: T7–9 (unverified)` with:
**`Clock: T8 decap / T11 table (lab 2026-06-13, cos_clock_lab.py) · Through interaction: slower (unverified — goldfish only; conservative on Zombie count; no removal/gy-hate)`**

Pod-bar read (decap T≤7): **32%** — the highest decap front edge measured in the
sweep, so the deck genuinely *can* pressure a player early via lord combat. But
decapping one player does not stop a combo pod, and the *win* (table) clock is T11.
The deck's real pod plan, as the Summary states, is **interaction + inevitability**:
five counterspells (two free), Cyclonic Rift alpha-strike, and the passive Scarab
drain that wins if the game goes long — not a race. No card swaps proposed
(verification pass only); the clock confirms the 17/20 grind-tribal posture and is the
first deck whose hand-estimated *decap* window survives contact with a lab.
