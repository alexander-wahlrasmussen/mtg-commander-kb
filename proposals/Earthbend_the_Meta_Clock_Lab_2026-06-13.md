# Earthbend the Meta — Kill-Window Clock Lab (2026-06-13)

Deck 6 of the Kill-Window Lab Sweep (`Kill_Window_Lab_Sweep_2026-06-13.md`).
Lab: `scripts/ebm_clock_lab.py` (40 000 trials, seed 20260613). Deck:
`decks/earthbend-the-meta-20260404-075423.txt`. Commander: Toph, the First
Metalbender (Naya). Score: **17/20** (unchanged).

**First lab run under the producer-inventory step** added to `WF_Kill_Window_Lab.md`
after the 2026-06-13 esc/rs re-check — and the most producer-dense deck in the sweep.

---

## Claim vs measured

| | Claim (Summary) | Measured (lab) |
|---|---|---|
| Goldfish | T7–9 (fastest T6) | **decap median T8** (T7 = 34%, T6 = 11%, T5 = 2%) / **table median T12** |
| never-in-14 | — | decap 1% / table 8% |

**Verdict: the claimed window is essentially the DECAP window** — decap median T8 is
in-band and the T7 front edge (34%) is a healthy real edge, not a god-hand (the
Summary's own "fastest T6 … not typical" matches T6 = 11%). The single number's error
is the familiar **decap/table conflation**: the table is ~4 turns later (T12). This is
the 2nd deck in the sweep (after Curse of the Scarab) whose decap front edge did not
come back optimistic.

## Kill shape — DIVERGE (and a Stage-1 learning)

Stage 1 prediction history is itself the finding:
- The tracker predicted **"combat focus-fire → diverge."**
- At Stage 0 I *re-predicted* "MIXED, converge-dominant," reasoning that Purphoros +
  Impact Tremors (per-creature-ETB, `hit_all`) would converge decap and table.
- **Measured: DIVERGE — decap T8 / table T12, a 4-turn gap.** The original tracker
  prediction held; my re-prediction was wrong.

**Lesson:** the presence of a `hit_all` axis does **not** make the shape converge if a
*focused* axis kills one player much faster. Here the focused decap (All Will Be One
single-target counter-burn + combat focus-fire) outruns the `hit_all` Purphoros/Tremors
ping, which is too slow to take all three to 40 at once. Decap leads table by ~4 turns.
Kill-shape lens record: the *pattern* call (diverge) was right; trust the focused axis
to set the decap and the hit-all axis to set the (slower) table.

## Engine modelled (oracle-verified Stage 0, no card-text errors)

- **Per-creature-ETB ping** (`hit_all`, sets the table): Purphoros (2/opp) + Impact
  Tremors (1/opp) per creature entering + Tannuk (1/opp per landfall). Driven by the
  **Scute Swarm exponential** (copies at 6+ lands, doubled by Doubling Season).
- **AWBO counter-burn** (focus, sets the decap): each amplified earthbend/Cathars
  counter event → All Will Be One to ONE opponent. Amplifier stack additive-before-
  multiplicative: Hardened Scales (+1) → Earth Crystal (×2) → Doubling Season (×2);
  earthbend 2 → 12. Annie Joins Up doubles legendary-creature earthbend triggers
  (commander, Tannuk) — **not** Purphoros/Tremors (not legendary creatures at red
  devotion < 5) and **not** the replacement-effect amplifiers.
- **Landfall count/turn** = land drops (+1 with Dryad of the Ilysian Grove) + nontoken
  artifacts entered this turn **while Toph is out** (her static makes them lands) +
  Awaken/Entish/ramp lands.
- **Triumph of the Hordes** infect (go-wide poison alt-kill) and **combat** (earthbent
  lands, double strike via Greatest Earthbender, Moraug extra-combat multiplier) as
  secondary focused axes.

## Two model bugs caught & fixed (v1-class, the 4th and 5th of the sweep)

1. **Commander not in the library.** `parse_deck` pulls the commander to the command
   zone, so `g.cast("Toph…")` always failed and `self.toph` never flipped — which
   dead-ended the *entire* engine (artifact-landfall, end-step earthbend, and combat are
   all gated on Toph). v1 killed-never (decap 88% never-in-14). Fixed by gating the
   commander cast on mana (the rs/cos pattern), not `g.has`.
2. **End-step counters powering the same turn's combat.** The commander's earthbend is
   an *end-step* trigger (resolves after combat), so its counters can't attack until the
   next turn. v1.5 applied them to the same turn's swing (decap T7). Fixed by ordering
   begin-combat earthbend (Avatar Kyoshi) → combat → end-step earthbends (which still
   fire AWBO now but power *next* turn's combat). decap moved T7 → **T8**.

## Producer inventory (the new WF step) — applied

Modelled as producers: Scute Swarm (exponential), Felidar cats, Springheart insects,
Field of the Dead zombies, Awaken dryads, Tannuk ping, Cathars counters, Lotus
Cobra/Tireless mana. **Omitted, all slow-bias (conservative):** Evolution Sage
proliferate, Bristly Bill activated double, The Ozolith carryover, Bumi attack pumps,
Springheart copy mode, Earthbender Ascension quest, exhaust earthbends, Zuran Orb +
Amulet of Vigor recursion, fetchland double-landfall. So the true clock is, if anything,
slightly **faster** than decap T8 — consistent with the producer-omission direction, and
not a concern for the verdict (it would only sharpen the front edge, not slow it).
**Optimism risks (other direction):** counters never decay; coarse Cathars/Earthbending-
Master folding; no interaction / static-40 table. Net: trust the SHAPE and front edge.

## Pod-bar read (decap T≤7)

decap T≤7 = **34%** — pressures early (comparable to Curse of the Scarab's 32%) but does
**not** reliably race the T6–7 combo pod. The deck's pod plan is the snowball + its
interaction/protection suite (12 pieces, 3 stack answers), not out-speeding. The 4-turn
decap→table gap means it threatens one player well before it can actually close the
table.

## Disposition

No card swaps (verification pass only). 17/20 stands. The clock confirms the deck's
"snowball, decisive-from-developed-board" identity rather than challenging it — and
corrects the Summary's single-number window to a decap/table split.

### Summary Kill Window field → replace with

**`Clock: T8 decap (median; T7 ≈ 34%) / T12 table (lab 2026-06-13, ebm_clock_lab.py — coarse engine model) · Through interaction: slower (unverified — goldfish only; no disruption/Cyclonic Rift model)`**
