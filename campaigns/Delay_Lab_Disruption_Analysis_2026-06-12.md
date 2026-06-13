# Delay Lab — Disruption Availability vs the Pod's Combo Turn (2026-06-12)

**What this is:** the first answer-availability ("counter-clock") lab — the axis the bake-off
verdict flagged as load-bearing-but-unmeasured. The Stage-3 clock labs measured how fast WE
kill; this measures how reliably we can DISRUPT the recurring pod combo deck's T6–7 win attempt
([[project_pod_combo_opponent]]). Lab: `scripts/delay_lab.py` (20 000 trials, seed 20260612).

**The design correction that shaped it (user, 2026-06-12):** Grand Abolisher is a drawn card,
not a constant. The lab therefore measures our answer availability as scenario *conditionals*
and composes them across a swept **P(Abolisher out) = a**, instead of assuming the lock is
always on.

---

## Model

Three scenarios on the opponent's key turn (verified rules fact: Abolisher stops **all** our
spells on their turn, not just counters):

- **A — no Abolisher:** counters + instant removal live if held with mana open; statics live if deployed.
- **B1 — Abolisher out, ≥1-turn window:** statics, OR own-turn removal (kill Abolisher / the
  visible piece) followed by a held reactive answer (both costs payable from one turn's lands).
- **B2 — Abolisher dropped the combo turn itself:** statics only.

`P(disrupt) = (1−a)·A + a·(w·B1 + (1−w)·B2)`, w = 0.5 default.

**Coverage weights (judgment, printed with results, NOT measured):** the pod rotates 4 shells;
Kinnan/Kenrith/Hidetsugu win through *activated abilities* — a counterspell cannot counter an
activation, statics like Cursed Totem/Revoker can — Kairi through spells/triggers. Static 0.75,
removal 0.90, counter 0.50.

**Ceiling conventions** (clock-lab philosophy — trust deltas): seen singleton = held; mana =
lands-only floor; holding open always possible; we act before them in turn order (half-turn
optimism, shared by all configs). **Main limitation:** this is *single-key-turn* availability —
a slow deck must disrupt *several* consecutive key turns and answers get consumed; multi-turn
campaigns compound below these numbers. And availability ≠ effectiveness (backup lines,
second protection pieces, recursion are not modelled).

Card classifications hand-verified via oracle text (see lab docstring for the exclusion list —
redirects, combat-conditioned pieces, protect-own, narrow tutors).

## Results — composed P(disrupt their key turn T6), drawn-only (with-tutors)

| Config | a=0% | a=25% | a=50% | a=75% | a=100% |
|---|---|---|---|---|---|
| **Yuriko** (the pick) | 52 (69) | 40 (54) | 29 (38) | 18 (22) | **7 (7)** |
| **Kefka-burn** (fallback) | 68 (74) | 56 (62) | 44 (51) | 32 (39) | 20 (28) |
| **Kefka-burn + 3-card port** | 70 (75) | 59 (65) | **48 (55)** | **37 (44)** | **27 (34)** |
| **Kefka-ext** (calibrator) | **77 (82)** | **64 (69)** | 51 (57) | 38 (44) | 26 (32) |

Key availability components at their T6 (drawn-only): Yuriko C 53 / R 37 / **S 0**;
Kefka-burn C 53 / R 58 / S 12 / B1-chain 33; port C 31 / R 64 / **S 22** / B1 29;
ext C 68 / R 68 / S 11 / **B1 50**. Their-T7 numbers run ~3pp higher across the board.

## Findings

1. **The user's correction has the biggest practical effect of anything in the model.**
   Realistic a is probably **~0.15–0.30** (a 1-of in 99 is ~12% raw by their T6; tutor support
   pushes it up, but their tutors compete with combo assembly). In that regime every suite is
   2–3× healthier than the worst-case reading: Abolisher is **tail risk, not baseline**. Note
   also the endogeneity: if they *wait* for Abolisher before going off, a rises but their key
   turn slips later — which feeds our racers. Either way the matchup is better than the
   always-locked reading the roster docs have been implicitly using.
2. **Yuriko: race-first is now quantified, not just argued.** Zero statics means its disruption
   collapses to 7% at a=1.0 and 29% at a=0.5. But at realistic a≈0.25 it holds 40% (54% with
   tutors — the largest tutor uplift of any config, because Mystical/Merchant Scroll/Solve
   fetch counters). Disruption is genuine race *support*, not a fallback plan. No list change
   recommended; if post-build pod games show high observed a, testing 1–2 statics is the lever —
   any candidate static needs a ruling check against the deck's own ninjutsu first (not done here).
3. **The 3-card port is lab-justified.** +4pp at a=0.5, +7pp at a=1.0, ~free at a=0. The
   robust driver is the second static (S doubles 12→22%, weight-independent in direction); the
   low-a gain partially reflects the counter-vs-removal weights and should be read as
   directional. Port plan stands, still fallback-conditional.
4. **The fallback's disruption thesis is a coin flip, not a wall.** Kefka-burn at a=0.5 holds
   44–51% on a single key turn — and its T8 decap means it may face *two* such turns. Honest
   matchup read vs the pod deck: lose the race, then ~50/50 per attempt to hold. The port and
   the wheel-recovery engine help, but Kefka-burn should be played as disrupt-*then*-race, not
   as a control deck.
5. **Calibrator surprise — the external's suite is the strongest raw suite, even under
   Abolisher-with-window.** 77% at a=0, and its cheap-removal density gives the best B1 chain
   (50%). Its collapse is the *largest* (−51pp to a=1.0) but the floor isn't zero. The Stage-4
   read sharpens: the external's problem was never the suite, it's that a T9/T9 clock asks it
   to win 2–3 consecutive coin flips while the internal builds ask for 0–1. Suite quality
   cannot rescue a slow clock — the two labs measure the same matchup from opposite ends.

## Roster comparison (same day, user request): candidates vs Lightning War / Calamity Tax / Grand Design

The three lab-verified roster decks were classified and run through the same model (suites
hand-verified; roster-specific conventions in the lab docstring — notably the free-spell suite
Forces/Fierce/Pact/Rollick modelled at 0 where the commander is cheap, and **CT understated**:
Seedborn+Glarb instant-speed top-casting blows past the lands-only mana floor and is not
modelled). Both axes side by side, **with the clock-measurement-class caveat**: only GD, Genome
and the bake-off candidates have *median decap/table clock labs*; LW's T6–7 and CT's T7–9 are
the older availability-corroborated goldfish windows (CT's summary itself notes "no kill-turn
goldfish run"), and that class trended optimistic 7-of-8 times historically.

| Deck | Clock decap/table | Clock class | CC | Disrupt T6: a=0 | a=25% | a=50% | a=100% |
|---|---|---|---|---|---|---|---|
| **LW** (roster) | "T6–7" goldfish | window est. | 19/20 | **77 (82)** | **64 (67)** | 50 (52) | 23 (23) |
| **GD** (roster) | T10 / >T12 | median lab | 19/20 | 67 (68) | 54 (55) | 42 (42) | 17 (17) |
| **CT** (roster) | "T7–9" goldfish | window est. | 18/20 | 52 (57) | 41 (45) | 30 (32) | 8 (8) |
| Genome (roster) | T7 / T8 | median lab | 15/20 | *not run* | | | |
| Yuriko (pick) | T7 / T8 | median lab | 17/20 | 52 (69) | 40 (54) | 29 (38) | 7 (7) |
| Kefka-burn (fallback) | T8 / T9 | median lab | 16/20 | 68 (74) | 56 (62) | 44 (51) | 20 (28) |
| — +3-card port | T8 / T9 | median lab | — | 70 (75) | 59 (65) | **48 (55)** | **27 (34)** |
| Godo (rank 3) | T6 / T6 | median lab | 13/20 | *not run* | | | |

**Findings:**

1. **No candidate outclasses Lightning War.** LW posts the best measured disruption profile
   (ties the expert external at a=0, beats the port at a=0.25) *while carrying the roster's
   fastest claimed clock and a 19/20*. The free-spell suite (Fierce/FoN/Rollick at cost 0 with
   Azula out) plus burn-as-removal is why: its kill-Abolisher-then-answer chain (48% at T6) is
   the best of any deck measured. The candidates add *coverage*, not a power upgrade.
2. **The honest caveat on #1:** LW's "T6–7" is the unverified-median class. Its own speed
   analysis showed 22% table-finisher availability by T6 — comparable to Yuriko's measured 26%
   table-by-T6 — so measured the same way, LW would plausibly read ~T7/T8 median too, i.e.
   **same speed as Yuriko, with far better interaction**. An `lw_clock_lab.py` (median
   convention) would settle it and is the cheapest way to sharpen this comparison.
3. **What each candidate adds that the roster lacks:** Yuriko — a *deterministic, on-cast,
   Abolisher-proof kill* (Thoracle at 3 mana wins outright; LW's kill needs big mana through a
   combat window) plus a verified decap median. Kefka-burn(+port) — the only damage axis that
   ignores Abolisher *and* the best high-a disruption floor measured (27–34% at a=1.0 vs LW 23,
   GD 17). Godo — nothing the roster lacks except raw speed, with the known glass.
4. **Calamity Tax is the roster's soft spot on this matchup axis** — weakest disruption of the
   three (0 statics, free counters only Pact/FoN/Fierce) on top of a mana-gated T7–9-claimed
   clock that its own analysis says can't race. The Seedborn understatement softens but doesn't
   reverse this: vs the pod combo deck specifically, both Yuriko (racing) and Kefka-burn
   (statics) are better-shaped. CT's grind/oppression strengths are simply off-axis here.
5. **Grand Design's matrix verdict ("Favoured — disruption-led, not a race") gets a number and
   a stress line:** 67% at a=0 is real, but it erodes to 42/17% as Abolisher enters, its only
   static (Elesh Norn, MV5) deploys late — and a T10-decap deck must win *several* consecutive
   key-turn rolls, which compounds. GD's true Abolisher tech is its own Grand Abolisher
   (protect-own, rightly uncounted here). Worth revisiting the matrix line vs this specific
   opponent.
6. **Portfolio read for the pick decision:** the bake-off brief presupposed building one deck.
   This comparison shows the *racer-with-interaction* niche is already occupied by LW; Yuriko's
   genuine marginal value is the deterministic combo kill and the verified clock, at ~€140–170.
   Whether that's worth building is a portfolio-diversity call, not a power upgrade — flagged
   for the user, verdict doc unchanged.

## Method caveats

- Single-key-turn ceiling; multi-turn defence compounds below it (answers consumed, wraths not
  modelled). Weights are judgment parameters — re-run with different weights before leaning on
  small low-a deltas. Mana is a lands-only floor; tutors pay tutor+target in one turn.
- a and w are opponent parameters the lab cannot know; the sweep is the result, not any single
  column. Observed pod frequency belongs to the user.

Related: `Candidate_Bakeoff_Verdict_2026-06-12.md` · [[project_candidate_bakeoff]] ·
[[project_kefka_proposal]] · [[feedback_grand_abolisher_blocks_counters]]
