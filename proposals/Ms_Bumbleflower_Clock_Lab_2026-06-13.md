# Ms. Bumbleflower — Kill-Window Clock Lab (2026-06-13)

Deck 9 of the Kill-Window Lab Sweep (`Kill_Window_Lab_Sweep_2026-06-13.md`).
Lab: `scripts/bmf_clock_lab.py` (40 000 trials, seed 20260613). Deck:
`decks/this-bunny-goes-to-market-20260404-080311.txt`. Commander: Ms. Bumbleflower
(Bant). Score: **15/20** (unchanged).

---

## Claim vs measured

| | Claim (Summary) | Measured (lab) |
|---|---|---|
| Goldfish | T8–10 | **decap median T8** (T7 = 38%, T6 = 7%) / **table median T11** |
| never-in-14 | — | decap 0% / table 3% |

**Verdict: the claim's decap is corroborated — but as a CEILING.** decap median T8 sits in
the claimed band, and like CoS/Earthbend/Lorehold the front edge does not come back wildly
optimistic. The single number's error is the familiar decap/table conflation — **table is
T11, a 3-turn gap** that is exactly the deck's "out-values, under-closes" identity.

## Why decap T8 is a ceiling (the model over-credits a control deck)

Unlike most decks in the sweep, the goldfish is **generous** to this one: it dumps the deck's
~15 interaction pieces (7 counters + 8 removal) *proactively* to farm Bumbleflower triggers
(counters, Cats, draw-2 → Jolrael hand-size). In real games this is a tempo-**control** deck
that **holds that interaction up** — so true spell velocity, and therefore the Cats/counter/
hand-size that feed the Jolrael alpha, is lower and the real clock is slower (toward the
claimed T10 / the through-interaction T11–14). This is the inverse of Lightning War's strict-
goldfish penalty: here goldfish strictness *flatters* a control deck. Treat decap T8 as the
ceiling, not the median expectation in a real game.

## Kill shape — COMBAT focus-fire, diverge (prediction held)

- **decap (T8)** set by the **Jolrael alpha** ({4}{G}{G}: creatures become X/X, X = cards in
  hand; with Reliquary Tower the hand — and so X — gets large, and the board is Cats + payoffs).
  Focus-fires one player.
- **table (T11)** because the alpha kills one opponent at a time; tabling all three needs ~3
  swings. The 3-turn decap→table gap is the deck's signature "dominates the board, struggles
  to finish."

The tracker's "evasive/Jolrael alpha → combat diverge" prediction held.

## Goldfish-invisible (noted, like CT's oppression)

**Willbreaker theft (Line 2)** — steal opponents' creatures by aiming Bumbleflower's counter at
them — does nothing in a goldfish (dummies have no board). It's a real board-control/grind line
the clock cannot credit; it makes the deck stronger in a real pod than the goldfish shows
(against creature decks), without making it *faster*.

## Engine modelled (oracle-verified, no card-text errors)

Spell velocity → Bumbleflower trigger (counter + flying; 2nd cast/turn → draw 2) → Jolrael Cat
on the 2nd draw → board width + counters → Jolrael alpha (`ncre × hand + counters`) or counter-
beats. Cantrips/instants modelled as draw-1 selection; creatures stay as bodies; triggers capped
at 5/turn (free-spell loop guard). Mana = lands + rocks/dorks floor.

**Omitted (conservative):** Willbreaker theft, Sin counter-vacuum finisher, Smuggler's Share /
Tataru Treasure ramp, Snapcaster/flash rebuys. **Optimistic:** proactive spell-dumping (the
ceiling caveat above), rocks tap turn they land, static-40 table, no interaction.

## Pod-bar read (decap T≤7)

decap T≤7 = **38%** in the goldfish — but with the proactive-dump caveat, real early pressure is
lower, and the *win* (table) is T11+. The deck does not race; its pod plan is out-value + deep
interaction (5/5 axis) + a slow combat close, exactly as the Summary's Pod Fit states.

## Disposition

No card swaps (verification pass only). 15/20 stands. The clock confirms the deck's defining
weakness — Kill Reliability 3/5, "under-closes" — as a measured **decap T8 ceiling / table T11**
split, and flags that the deployed-deck reality is slower than the goldfish because its spells
are mostly reactive interaction. Upgrade path remains as the Summary notes (0 GCs used — room
for a faster/decisive closer).

### Summary Kill Window field → replace with

**`Clock: T8 decap (median; goldfish CEILING — see note) / T11 table (lab 2026-06-13, bmf_clock_lab.py) · Through interaction: slower, T11–14 (unverified — goldfish only). Ceiling caveat: the goldfish dumps interaction proactively for triggers; the real control deck holds it up and closes slower. Willbreaker theft is goldfish-invisible.`**
