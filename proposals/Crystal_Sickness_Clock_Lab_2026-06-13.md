# Crystal Sickness — Kill-Turn Clock Lab (2026-06-13)

**Deck 4 of 10** in the Kill-Window Lab Sweep (`proposals/Kill_Window_Lab_Sweep_2026-06-13.md`).
Lab: `scripts/cs_clock_lab.py` (40k trials, seed 20260613), built on `speed_lab_core.py`.
Procedure: `workflows/WF_Kill_Window_Lab.md`.

## Claim vs. measured

| | Claim (hand-estimate) | Measured (lab) |
|---|---|---|
| Goldfish | **T7–9** (single range) | decap median **T11** · table median **T13** |
| Front edge | T7 | T7 = 7% decap, 1% table |
| Never-in-14 | — | decap 21% / **table 34%** (upper bound — see caveats) |

```
  P(kill <= turn T) %                        5     6     7     8     9    10    12    14
  decap (one opponent, 40)                   0     1     7    19    34    48    68    79
  table (all three)                          0     0     1     6    15    27    50    66
```

## Direction: optimistic front edge + decap/table conflation (the recurring pattern)

"T7–9" is the **optimistic edge**, not the median. The decap median is **T11** —
two turns past the *back* of the claimed range — and the table median is **T13**.
T7 (the front edge) happens 7% of the time on decap and 1% on the table; it is a
fast-draw scenario, not the norm. As with the seven decks before it, the single
number silently meant "decap" and rounded a god-hand into the range. The Summary's
own body text is actually closer to the truth than its headline: it estimates
"2–4 turns from engine-online (8+ artifacts) to kill," and 8 artifacts is a ~T8
median here, so engine-online + 3 ≈ T11 decap — exactly what the lab measures. The
headline "T7–9" is faster than the Summary's own internal arithmetic.

## Why this shape

- **The engine is card draw, not the curve** (the Lightning-War-v1 lesson, again).
  The first model had no draw and flatlined at ~1 artifact/turn, killing essentially
  never — because the deck's drivers are *non-artifact* permanents the artifact-only
  deploy loop skipped: **Matoya** (draw on every surveil, i.e. every artifact ETB),
  **Sai / Efficient Construction / Mirrodin Besieged** (token-on-cast — Sai and
  Matoya are plain creatures, the other two are enchantments), **Forensic Gadgeteer /
  The Mechanist** (Clue-on-cast). Add the artifact-side draw (Thought Monitor +2,
  Thoughtcast +2, Cryogen Relic / Baubles, Skullclamp on a Thopter, The One Ring)
  and the engine snowballs: arts reach 8 by a ~T8 median, then climb steeply
  (≈12 by T9, ≈16 by T10) once a generator + Matoya are online.
- **The drain is gated on digging a *bomb*, and there are only three.** Golbez
  drains "that card's power," so the kill needs a high-power creature in the yard:
  **Phyrexian Dreadnought** (12, self-sac to yard for {1}, re-bin for {1} → the
  repeatable engine), **Master of Etherium** (= artifacts, CDA works in the yard),
  or **Troll of Khazad-dûm** (6, swampcycle to yard). With 3 such cards in 99 and
  no maindeck Entomb, a bomb is in the yard only ~38% by T7, ~46% by T9, ~58% by
  T12 — which tracks the raw hypergeometric odds of having seen one. So the
  drain — the deck's headline kill — is a roughly coin-flip line through the
  mid-game even with heavy surveil digging.
- **The table then needs 3–4 drain cycles.** Dreadnought drains 12/opponent/turn,
  so from 40 the *table* dies ~T(online)+3. Online ≈ T8–9 (8 arts AND a bomb), so
  table ≈ T11–13. Tezzeret, Master of the Bridge (+2 = arts to each opponent) is a
  real accelerant but lands late — 6 mana, online ~T9+ — so it shortens the back
  half rather than the front edge.

## Kill-shape prediction (pre-registered) — shape held, absolute prior was optimistic

The tracker's first-pass prior — *"reanimate a fatty → combat focus-fire →
diverge"* — was **half right and was corrected at Stage 0**: the deck's *named
primary* kills (Golbez drain, Tezzeret +2) are **all-table drains that converge**,
while only its *incidental* combat (Urza's Construct = arts, Master body, Thopters)
focus-fires and diverges. Corrected Stage-1 prior: **mixed — drain converges,
combat pulls decap ahead; decap ~T8, table ~T8–9.**

Measured: **mixed, decap T11 / table T13 (a ~2-turn gap)** — milder than a pure
combat deck's 3–4-turn divergence (the drain/Tezzeret converge component pulls them
together) and wider than a pure converge deck's zero gap. So the *shape* call held
(8 — now 9 — for-9 on the pattern: drain converges, combat leads decap). But the
*absolute* turns in my own corrected prior (decap ~T8) were themselves optimistic
by three turns. **Lesson reinforced: the kill-shape lens predicts the decap/table
*pattern* reliably; it does not protect the absolute turn estimate, which still
wants a lab — even an informed prior skewed fast here.**

## Card text

No new errors — the Summary's 2026-05-06 full re-audit (which fixed material
hallucinations: Mirrodin Phyrexian self-loot, Tezzeret +2 activated, Forensic
Gadgeteer cast-trigger, etc.) held under modeling. Reconfirmed against
`card_lookup.py` for the kill branches:

- **Golbez returns the creature to *hand*** then drains its power — so repeating the
  drain requires re-binning the bomb each turn. Dreadnought does this for itself
  (recast {1} → ETB self-sacrifice → back in yard); Master/Troll need a loot outlet
  (Riddlesmith / Underworld Cookbook) to repeat, modelled accordingly.
- **Master of Etherium's CDA works in all zones including the graveyard** (ruling) —
  so it drains for the live artifact count.
- **Tezzeret himself does *not* have affinity** (ruling) — flat {4}{U}{B} = 6 to
  cast, not discounted; that is why he comes online late.

## Modeling caveats (heuristic, not a rules engine)

- **Captures the primary drain + Tezzeret + combat; omits the redundant slower
  closers.** Not modelled: the **Mirrodin Besieged Phyrexian alt-win** (15 artifact
  *cards* in your yard → an opponent loses; a different axis that ignores life — the
  model picks Mirran mode for tokens instead), the **Tezzeret, Cruel Captain emblem**,
  and **Urza's tap-mana → hard-cast-anything** value. These are *closers for the
  long game*, so the **table never-in-14 of 34% is an upper bound** — the real tail
  is shorter. They do **not** touch the front edge, so the decap/table medians are
  the trustworthy headline.
- Mana = lands + rocks (+ Urza tap-mana capped at +8). Damage is **unblocked** and
  there is **no opposing interaction** — and crucially the goldfish assumes Golbez
  and Urza are **never removed**, when both are removal magnets and the deck folds
  to a single artifact-hate card (Vandalblast / Collector Ouphe / Null Rod). So the
  goldfish is an **upper bound**; the real clock against a pod is *slower*, which
  makes "T7–9" doubly optimistic.
- Fatty acquisition is a surveil/loot/self-sac dig proxy scaled by artifacts entered
  that turn; it reproduces the raw card-finding probability, so it is honest about
  the bomb bottleneck rather than papering over it.

## Verdict for the Summary

Replace `Goldfish: T7–9 (unverified)` with:
**`Clock: T11 decap / T13 table (lab 2026-06-13, cs_clock_lab.py) · Through interaction: slower (unverified — goldfish only; no removal of Golbez/Urza, no artifact-hate modelled)`**

Pod-bar read (decap T≤7): the deck clears T≤7 decap only **7%** of the time — it
**does not race** the T6–7 combo pod. This is consistent with the deck's actual pod
plan, which the Summary states correctly: it is **competitive *against* the combo
player through five counterspells (two free)**, i.e. it *interacts and grinds*, it
doesn't out-speed. No card swaps proposed (verification pass only); the clock
confirms the 17/20 grind-engine posture rather than challenging it. The headline
correction is that the kill is a mid-to-late drain gated on assembling 8 artifacts
*and* a bomb, not a T7–9 race.
