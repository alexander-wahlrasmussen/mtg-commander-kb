# Lightning War — Kill-Turn Clock Lab (2026-06-13)

**Deck 3 of 10** in the Kill-Window Lab Sweep (`proposals/Kill_Window_Lab_Sweep_2026-06-13.md`).
Lab: `scripts/lw_clock_lab.py` (40k trials, seed 20260613), on `speed_lab_core.py`.
**v2 — revised after user push-back** (the v1 model was too conservative; see "Model
correction" below). Lightning War was previously marked "lab-verified T6–7" off
`lw_speed_lab.py`, which measured finisher *availability* and the table wipe against
*pre-chipped* opponents, never an unconditional kill-turn goldfish. This is that goldfish.

## Claim vs. measured (v2)

| | Claim (Summary) | Measured (lab v2) |
|---|---|---|
| Goldfish | **T6–7** | **decap median T9** · table median ~T13 (40% never-in-14) |
| decap | — | T6 = 1%, T7 = 10%, T9 = 57%, T10 = 76% |
| table (one-cast win) | T6–7 | T8 = 2%, T10 = 12%, T12 = 33% |

```
  P(kill <= turn T) %                        5     6     7     8     9    10    12    14
  decap (one opponent, 40)                   0     1    10    32    57    76    93    99
  table (all three)                          0     0     0     2     5    12    33    60
```

## Model correction (what was wrong in v1, and why it matters)

v1 reported decap T11 / table "never," which was too slow. The user correctly flagged
that firebending + spell-copy is a tempo/race engine. Three real bugs were under-
crediting the deck, all now fixed:

1. **Combat swung only Azula's 4 power**, ignoring the actual creature board —
   Goldspan Dragon (4/4 haste-fly), Hullbreaker Horror (7/8), Leyline Tyrant (4/4 fly),
   Vendilion Clique, Opposition Agent, Storm-Kiln. v2 develops and swings the board.
2. **Vivi Ornitier was not modelled at all.** It's a *second pinger* (1 to each
   opponent per noncreature spell) AND a snowballing ramp source ({0}: add its power,
   which grows each noncreature cast). A material engine for both chip and mana.
3. **Fated Firepower was not modelled.** It amplifies *every* damage instance (ping,
   swing, finisher) by X — it boosts both clocks.

With these in, decap moved T11 → **T9** and table "never" → median ~T13 (never-in-14
54% → 40%). The deck is faster than v1 said. Lesson logged: inventory the full
creature board AND every pinger/amplifier before trusting a burn deck's clock.

## What still holds (model-independent)

The deck's *named* win — "kill the table from one cast" — is genuinely mana-expensive:
Crackle with Power is **`{X}{X}{X}{R}{R}`**, so a from-40 table fork is X=4 = **14 mana**
(X=3 + Twinning Staff = 11). The pre-existing `lw_speed_lab.py` one-cast-table-wipe-
from-40 baseline independently agrees: 20% by T12, **70% never**. So a literal turn-6
*table sweep from full life* is not the median for either model — it's the god-hand
ceiling.

## How to read "T6–7" honestly (it's not a clean falsification)

Unlike Grand Design (a genuine 2-turn optimistic miss), Lightning War's gap is partly
an **artifact of goldfish strictness against this particular deck**:

- **Goldfish models zero disruption.** The deck's edge is 8 counters (3 free) +
  removal that slow *opponents'* clocks while it sets up — exactly the Exile's Return
  lesson ("lost the race, Favoured because of interaction"). Its *match* clock beats
  its goldfish clock.
- **Goldfish holds all opponents at a static 40.** A real pod arrives at the finish
  already chipped from attacking *each other*; the deck picks the moment to fork a
  now-cheaper X-spell. From 30 life each, Crackle drops to X=3 (11 mana); from 20, the
  table wipe is 22% by T7 (lw_speed_lab @20). Cross-table chip is real and unmodelled.

So "T6–7" is best read as the deck's **real-pod** clock (disruption- and chip-assisted,
on a board it shaped), while the **strict unconditional goldfish is decap T9 / table
~T13**. The honest correction is not "the deck is slow" — it's "**the literal one-cast
table sweep from 40 is the ceiling, not the median; the deck's race is tempo +
disruption + a flexible finish, which goldfish understates.**"

## Card text

No errors. `card_lookup.py` confirmed: Crackle is `{X}{X}{X}{R}{R}` (triple X — the 14-
mana table kill); Comet Storm instant + multikick; Banefire/Electrodominance single-
target; Guttersnipe 2/each per I/S cast; **Vivi 1/each per noncreature cast + {0} tap
for its power**; **Fated Firepower +X to all your damage to opponents**; Emeritus of
Conflict is a 2/2 that copies Lightning Bolt only after your 3rd spell each turn (a
conditional bolt, not a free repeatable one — so I did NOT credit it as a per-turn pinger).

## Modeling caveats (heuristic)

- Mana = lands + rocks floor + Azula's +2 in combat + banked Storm-Kiln Treasures +
  Vivi's tap + rituals in hand (Jeska's Will counted flat at +4, likely an underclaim).
- Chip = (Guttersnipe 2 + Vivi 1)/noncreature-cast to all (+Fated X each), plus the
  creature board (focus). Finisher fires when its lethal X is affordable vs current life.
- No opposing interaction, no blockers, **no cross-table chip, none of the deck's own
  disruption** — all of which make the real-pod clock faster than this goldfish.

## Verdict for the Summary

Replace `Goldfish: T6–7 · Through interaction: T7–9` with:
**`Clock: T9 decap / ~T13 table (strict goldfish, lab 2026-06-13, lw_clock_lab.py). The from-40 one-cast table sweep is 14-mana Crackle (cf. lw_speed_lab: 20% by T12 / 70% never), so "T6–7" is the chip-/disruption-assisted real-pod clock, not a from-full goldfish median. Goldfish understates this deck — its race is tempo + 8-counter disruption + a flexible finish.`**

19/20 stands. Pod-matrix posture: **a tempo-race that wins on disruption + a finish,
not a from-40 burst.** Re-opens the standing pinger-add recommendation (the lever
lw_speed_lab found dominant). No card swaps (verification pass).
