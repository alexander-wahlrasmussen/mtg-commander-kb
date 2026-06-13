# Lorehold Spirits — Kill-Window Clock Lab (2026-06-13)

Deck 7 of the Kill-Window Lab Sweep (`Kill_Window_Lab_Sweep_2026-06-13.md`).
Lab: `scripts/lor_clock_lab.py` (40 000 trials, seed 20260613). Deck:
`decks/lorehold-spirit-20260503-154449.txt`. Commander: Quintorius, History Chaser
(Boros planeswalker). Score: **18/20** (unchanged).

---

## Claim vs measured

| | Claim (Summary) | Measured (lab) |
|---|---|---|
| Goldfish | T7–9 (fastest T6, avg T8) | **decap median T8** (T7 = 46%, T6 = 18%, T5 = 4%) / **table median T10** |
| never-in-14 | — | decap 1% / table 5% |

**Verdict: the claim is accurate as a DECAP window** — decap median T8 matches the
Summary's stated "avg T8" exactly, and the T7 front edge (46%) is a strong, smooth edge,
not a god-hand (the Summary's "fastest T6 … near-perfect" maps to T6 = 18%). This is the
**3rd deck in the sweep (after Curse of the Scarab and Earthbend) whose front edge did not
come back optimistic.** The single number's only error is the usual decap/table
conflation — but the gap here is just **2 turns** (T8 → T10), the tightest mixed-shape gap
measured so far.

## Kill shape — MIXED, decap leads table by ~2 (both predictions held)

Per the carried prior: predict decap off the focused/combo axis, table off the hit-all
ping. Measured exactly that:
- **decap (T8)** set by the focused axes — Quintorius −4 + anthem combat (focus-fire) and
  Balefire Liege chip.
- **table (T10)** set by the converge axes — Purphoros (`hit_all`, 2/opp per Spirit ETB)
  and the Goblin Bombardment combo (`kill_all`). These pull the table to only 2 turns
  behind decap, vs 4 for the pure-combat esc — the hit-all axis genuinely tightens the
  gap (the Earthbend over-correction lesson, the other way: here the converge axes ARE
  strong enough to matter, just not to fully converge).

The tracker's "combo converge / combat diverge" prediction held.

## Card-text correction (Stage 0 catch)

The Summary's **Line 6 combo description is wrong on one mechanic**: it says "Sac Karmic
Guide … Persist returns it with a −1/−1 counter." **Karmic Guide has Echo, not Persist**
(verified `card_lookup.py`). The combo still works and is still unbounded — it runs off
**Reveillark's leave-trigger** returning Karmic Guide + a power-≤2 creature, and **Karmic
Guide's ETB** returning Reveillark — not a persist counter. No model impact (the lab
treats the combo as `kill_all` on assembly), but the Summary text should be fixed.

## Engine modelled (oracle-verified, no other card-text errors)

- **Token engine:** recursion events/turn (repeatable engines online + one-shot pulses)
  → Quintorius static (1 Spirit per *event*, not per card; ×2 with Anointed Procession;
  ×2 statics with Field Historian) → each Spirit ETB pings Purphoros 2/opp (`hit_all`).
- **Quintorius +1 dig** (discard 1, draw 2, mill 1) modelled as draw-2/turn — the deck's
  central consistency engine (see model-correction below).
- **Combat** (focus): Spirit power 3 + anthems (Patchwork +1, Balefire +2 red&white,
  Hofri +1, Field Historian +1), doubled under −4 (loyalty-ready ~1 turn after landing)
  or Akroma's Will double strike; Moonshaker Cavalry +ncre/+ncre alpha.
- **Combo** (`kill_all`): Reveillark + Karmic Guide + Goblin Bombardment on bf + a body.

## Model correction (the +1 dig — a consistency omission, slow bias)

v1 (no +1 dig) gave decap T9 / table T12 with **12% never-decap / 35% never-table in 14** —
implausibly whiffy for an 18/20 engine deck. The miss was omitting Quintorius's **+1
(draw 2/turn)**, the deck's primary dig-and-fuel engine. Adding it: decap **T9 → T8**,
table **T12 → T10**, never-table **35% → 5%**. This is the same class as the Earthbend/cs/lw
under-modeling — omitting a deck's consistency/producer engine biases the clock slow and
under-rates it. The +1 is a verified ability, so modelling it is faithful, not tuning.

**Other omissions (conservative, same slow-bias direction):** Gamble tutoring a missing
combo piece, Hofri death-token copies, Venerable/Sun-Titan-attack/Teshar extra recursion
chains, Emeria/Mistveil. **Optimism (other direction):** rocks tap turn they land; no
interaction / static-40 table; recursion assumed yard-fuelled.

## Pod-bar read (decap T≤7)

decap T≤7 = **46%** — the highest pressure of the mixed decks measured so far (CoS 32%,
Earthbend 34%), and it nearly races: median T8 is one turn behind the T6–7 combo pod, and
46% of games threaten a kill by T7. The deck applies real early pressure, with the combo
(`kill_all`) and Teferi's Protection as the closing/insurance layer.

## Disposition

No card swaps (verification pass only). 18/20 stands. The clock confirms the deck's
mid-speed-but-resilient identity and tightens the Summary's single-number window into a
decap/table split. **Fix the Summary's Karmic-Guide-persist text** (echo, not persist).

### Summary Kill Window field → replace with

**`Clock: T8 decap (median; T7 ≈ 46%) / T10 table (lab 2026-06-13, lor_clock_lab.py) · Through interaction: slower (unverified — goldfish only; no graveyard-hate/Cyclonic Rift model)`**
