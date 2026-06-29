# The Definitive Tier List, v2 — 2026-06-28

*Supersedes [`Definitive_Tier_List_2026-06-15.md`](Definitive_Tier_List_2026-06-15.md). One honest
ranking of the 17 active decks — but now a composite of the **three convergent OUTCOME oracles**,
not two-outcome-plus-build-quality. Reproduce: `python scripts/tier_list.py`
(legacy v1: `python scripts/tier_list.py --legacy-power`). Refreshed 2026-06-28: added Forced
Liquidation (Kefka) on its promotion to the active roster, then re-run after **Backlog #11's
all-finishers best-line clock**, which folds Lightning War's ~T9 Reiterate + Seething Song combo into
its harvested clock and **lifts Lightning War from D to S (#2 overall)**. The morning cut of this doc
had LW in D on a **race-only** clock that the combo's table kill was invisible to; #11 fixed the
**instrument**, not the deck — see "the one finding" below for why that matters.*

> **Refreshed 2026-06-29 (post codebase-audit).** Re-run on the corrected clocks from the
> 2026-06-29 bug audit. Four tier moves, all from sim fixes rather than deck changes:
> **Radiation Sickness S→A** — The Wise Mothman (the commander) was attacking the turn it was cast
> (no haste); fixing it slowed Radiation's race front edge (pod P(win) 69→60), so **Genome is now
> the sole apex and the top external racer**, and Radiation joins the pod-specialists. **Croak and
> Dagger C→D** — its `dig` knob was modelling Glarb's *selection* as raw card draw; the honest
> clock is a ~T13 grind, not ~T10. **The Exile's Return B→A** — Fire Lord Zuko is MV3 not MV4, so
> the deck comes online a turn earlier. **Lorehold Spirits C→B** on the renormalisation. Medians
> for every deck's *published Summary clock* were unchanged by these fixes (the moves are
> front-edge/normalisation effects); the narrative below is updated to match.*

---

## What changed from v1, and why it's a stronger read

v1 (2026-06-15) ranked on **ANTI-POD · SELF-META · POWER(Conversion Check /20)**. Two of those
three measure *winning*; the third (CC) measures *build quality* and is clock-blind — it rewards
fortresses that can't close. v1 had to use CC as its third axis because the third **outcome**
oracle didn't exist yet: `interaction_meta_lab.py` shipped 2026-06-16 (Backlog #6).

v2 closes that gap. All three axes now measure *winning*, against two different bars:

| Axis | Source | The bar it measures | Weight |
|---|---|---|---:|
| **ANTI-POD** | `pod_gauntlet` blended P(win) | Beating the recurring **external** T6–7 combo pod — *the meta that matters*. Rewards a fast **decap** + disruption. | 0.45 |
| **INTER** | `interaction_meta_lab` (TAX=0.6) | Winning a **mirror** pod of your own decks, **with** an interaction tax on the close. Rewards closing the **table** + durability + trading answers. | 0.35 |
| **SELF** | `self_meta_lab` P(win\|random pod) | The same mirror bar **without** the overlay (the pre-tax fidelity). | 0.20 |

**CC drops out of the composite entirely** — shown only as a `(cc)` context column. That is the
whole point of v2: *rank by what wins, then look at how badly the score sheet disagrees.*

A note on independence: ANTI-POD is a genuinely separate bar (external pod, decap clock). SELF and
INTER are the **same** mirror bar at two fidelities (INTER = SELF + a measured interaction tax), so
together they form a *mirror consensus* weighted slightly above the single external axis — but the
external pod stays the largest **single** axis. The weights are a stance (closing > building), not a
measurement; re-weight in `tier_list.py`.

---

## The list

| Tier | Deck | Anti% | Inter% | Self% | (cc) | Clock | COMP |
|:--:|---|:--:|:--:|:--:|:--:|:--:|:--:|
| **S** | **The Genome Project** | 61 | 65 | 71 | 15 | T8 | **98** |
| **S** | **Lightning War** | 57 | 52 | 48 | **19** | T9 | **80** |
| **A** | **Forced Liquidation** | 49 | 46 | 47 | 16 | T9 | **69** |
| **A** | **Radiation Sickness** | 63 | 33 | 31 | 18 | T10 | **69** |
| **A** | The Replication Crisis | 64 | 24 | 22 | 17 | T10 | 63 |
| **A** | The Exile's Return | 49 | 33 | 31 | 18 | T10 | 58 |
| **A** | Zero-Sum Game | 33 | 45 | 48 | — | T9 | 57 |
| **B** | Lorehold Spirits | 39 | 23 | 28 | 18 | T10 | 44 |
| **C** | Ms. Bumbleflower | 48 | 11 | 10 | 15 | T11 | 39 |
| **C** | Curse of the Scarab | 37 | 20 | 19 | 17 | T11 | 38 |
| **C** | Earthbend the Meta | 42 | 14 | 14 | 17 | T11 | 37 |
| **C** | The Dark Lord's Army | 26 | 26 | 20 | **19** | T12 | 32 |
| **D** | The Grand Design | 36 | 5 | 5 | 18 | >T12 | 24 |
| **D** | Eldrazi Stampede Chaos | 26 | 7 | 9 | 14 | T12 | 19 |
| **D** | Diminishing Returns | 17 | 3 | 3 | 17 | >T14 | 7 |
| **D** | Crystal Sickness | 9 | 9 | 11 | 17 | T13 | 7 |
| **D** | Croak and Dagger | 8 | 8 | 8 | 18 | >T14 | 4 |

*(Trials 40k, T_grind 10, TAX 0.6, seed from `self_meta_lab`. COMP = weighted mean of the three
min-max-normalised axes — re-normalised over 17 decks. Refreshed 2026-06-29 on the post-audit
clocks: Radiation's Mothman fix slowed its race front edge (S→A), the ct-dig fix slowed Croak to a
~T13 grind (C→D), and the Zuko fix sped Exile's Return (B→A); see the top-of-doc refresh note.)*

---

## The one finding that matters: score ⊥ winning — *but check the oracle too*

v1 noted the three 19/20-equivalent decks scattered S→A→C. v2, ranking **purely on outcomes**,
keeps it standing:

> **The Dark Lord's Army (19/20) ranks 12th of 17 — tier C.** Grand Design (18/20) is **13th, tier
> D.** Meanwhile the apex of the roster, The Genome Project, scores **15/20**, and the #3 deck
> overall, Forced Liquidation, scores **16/20.** The Conversion Check and finishing position
> disagree, mildly **negatively**, at the top.

The Conversion Check tells you a deck is *well-built for what it's trying to do.* It does **not**
tell you the deck wins. Trust the tiers, not the sheet.

**But Lightning War (also 19/20) is the cautionary flip side, and it's the more important lesson.**
The morning cut of this list put LW dead last in the mirror (3/3) and **14th overall, tier D** — and
the prose here called it "the roster's starkest over-rate." That was **wrong**, and not because CC
was right: it was the *outcome oracle* that lied. The harvested clock was a **race-only goldfish**
that flattened LW's fastest line — the ~T9 Reiterate + Seething Song infinite-mana combo — out before
the sim ever saw it, so LW was scored on the combat-race axis it's worst at. Backlog #11's
all-finishers best-line clock races the burn line **and** the combo on the same game and harvests the
earlier close; LW's table clock went **>T14 → T9**, its mirror axes **3/3 → 49/46**, and it jumped to
**S, #2 overall.** So the discipline is two-sided: *score ⊥ winning, and a winning-oracle is only as
honest as the kill lines it can see.* CC didn't save LW here — a better measurement did.

---

## The reconciliation — where the oracles DISAGREE, and what it means

This is what v1 couldn't show with only two outcome axes. The two bars — **external pod** (anti)
and **mirror** (inter/self) — pull different decks in different directions. Read the *gap*:

### Apex — strong on BOTH bars
- **Genome Project** is the top deck on all three oracles combined (anti 61 · inter 65 · self 71).
  Fastest table clock on the roster (T8), a hit-all ping kill (decap ≈ table), 1% never-close. It
  both closes first **and** survives any seeding. *The interaction overlay is the only thing that
  dings it: it's fast but answerable. It wins anyway.* The true #1, on 15/20.

### The instrument-corrected #2 — a combo-race hybrid that's strong on BOTH bars
- **Lightning War (19/20)** — anti **57** (4th external) **and** mirror **52/48** (2nd on the
  interaction bar, behind only Genome). Once the best-line clock credits the ~T9 Reiterate + Seething
  Song combo (Backlog #11), LW stops being a one-seat combat racer and becomes a deck that closes the
  **table** fast on its own turn — exactly the line Grand Abolisher can't tax. No weak axis, the
  highest CC on the roster, and an uncounterable Banefire button on the side. The catch is honesty
  about *why* it's here: this is the deck the morning oracle scored dead-last because it couldn't see
  the combo. Its S is real **given** the all-finishers clock; it's also the standing proof that the
  clock you harvest decides the deck you think you own. Verify against logged games (Layer C) before
  treating #2 as settled.

### The balanced contender — no weak axis (the #3 newcomer)
- **Forced Liquidation (Kefka)** — besides Genome and the corrected Lightning War, the deck with
  **no hole**: anti 49 · inter 46 · self 47, a near-flat profile that lands it **3rd overall** despite
  topping no single bar. A Grixis **forced-draw burn** engine (decap T8 / table T9) that's respectable
  racing the external
  pod *and* grinding the mirror. Its design purpose is the pod's specific weakness — forced draw +
  Notion Thief **punishes the Grand Abolisher combo turn** instead of trying to counter through it,
  so it doesn't fold to the lock the way pure counter-decks do. Leans a little on disruption (pure
  race ~30% vs P(win) 49%), but the mirror numbers are real. It earns its A on balance, not a
  spike — the opposite failure mode from the fortresses below.

### Specialists — strong on ONE bar
- **Replication Crisis** and **Radiation Sickness** are the two **external specialists** — top of the
  roster on the anti-pod bar (anti **64** / **63**, essentially tied for best external) but low in the
  mirror (Repl 22–24, Radiation 31–33). Both race the external T6–7 combo on a fast decap (T7) yet
  can't grind a four-way: their **table** clocks (T10) + double-digit never-close don't close a peer
  pod. Radiation is the new arrival to this group — it *used* to read as a top-3 apex deck (S, "best
  external ~71"), but that race edge was inflated by a sim bug: its commander, The Wise Mothman, was
  attacking the turn it was cast (no haste). With the 2026-06-29 fix its front edge drops (anti 71→63,
  pod P(win) 69→60) and it's an A-tier external specialist — still the **Ur-Dragon fair-deck
  nightmare**, just no longer a mirror threat or the apex racer. *Pod specialists, tuned to neutralise
  the archenemy, not to win a fair four-way.*
- **Zero-Sum Game** — the exact inverse: mirror **~45–48** (top-3) but anti **33**. The
  board-independent, **Abolisher-proof** lifeloop wins durability races, but its T9 decap is a beat
  too slow for the fast external pod. *A mirror grinder.* Still has **no formal CC score** — and v2
  scores it on outcomes alone, where it's clearly A. (Audit it; it may belong higher.) *Note Forced
  Liquidation reaches the same mirror tier from the opposite direction — it also races the external
  pod, which is why it clears Zero-Sum overall.*

### Over-rated fortresses — high CC, low on BOTH bars
*(Lightning War **used** to lead this list. It doesn't any more — the all-finishers clock showed its
"low on both bars" was a measurement artifact, not the deck. See "the instrument-corrected #2" above.
What's left are the genuine fortresses: high CC, slow clock, low on both bars even when every kill
line is counted.)*
- **The Dark Lord's Army (19/20)** — the subtle one, and now the roster's clearest over-rate by CC.
  CC's co-#1, the **most durable** deck on the roster (0.86), and the **only** deck the interaction
  overlay *lifts* meaningfully (Δ**+6** — it taxes opponents' closes while outlasting them). But a T12
  clock buries it: anti 26, and it needs a
  **grindy** meta to shine. Raise `--t-grind` and it climbs toward the Final Four (see the Pod
  Championship). A fortress, not a racer — over-rated by CC, *under-rated by pure race.*
- **The Grand Design (18/20)** — >T12 table, 5% on both mirror oracles. Ten kill lines all funnel
  through Finale, a *sorcery* the creature-tutors can't fetch; combat is the real, slow clock. A
  disruption-led value pile — now the roster's clearest cautionary tale, *because* Lightning War
  stopped being one: GD's only finisher really is un-tutorable, with no hidden fast line for a
  better clock to surface.

### The interaction overlay's net verdict (second-order, not a reversal)
The overlay **lifts** durable / answer-dense grinders (Dark Lord +6, Radiation +2, Exile's +2) and
**sinks** fast-but-answerable glass (Genome −6, Lorehold −5). But it does **not**
rescue a genuine fortress into contention — Grand Design and Dark Lord stay low in the mirror with or
without it. **The decap/table clock dominates; interaction is a real but secondary correction** —
which is exactly why getting the *clock* right (Backlog #11) moved Lightning War three tiers while
the overlay never could. (At TAX=0 the overlay is a verified null reduction — it reproduces self_meta
bit-for-bit; `tests/test_null_reduction.py`.)

---

## So: who should the pod fear, and what's over-rated?

**Fear these (bring them to a real pod):**
1. **Genome Project** — the apex. Fast and unkillable in the standings. Your default.
2. **Lightning War** — the corrected #2: a combo-race hybrid that closes the **table** ~T9 on its own
   turn (Abolisher-proof) with an uncounterable Banefire backstop. No weak axis. The one asterisk is
   that its rank rests on the best-line clock — verify it in real games before betting the night on it.
3. **Forced Liquidation** — the all-rounder (#3): no weak axis, and built to *punish* the pod's
   Abolisher-combo plan rather than race it. The safe pick when you don't know the table.
4. **Radiation Sickness** — the external pod's nightmare (anti 63, 2nd-best on the roster behind
   Replication): its kills are board states counterspells can't touch, and it's the best hedge vs the
   Ur-Dragon fair deck too. Weak in the mirror, so A not S — and its old apex standing was partly the
   Mothman summoning-sickness bug (now fixed).
5. **Replication Crisis** — when you *know* it's the T6–7 combo pod: it races them (anti 64, best
   external). Less so into a grind.
6. **Zero-Sum Game** — the quiet overperformer and Abolisher-proof. Bring it into a slow/grindy table.

**Stop over-rating these (the sheet lies about them):**
- **The Dark Lord's Army** (19/20) — a fortress that holds answers but can't close a table on a T12
  clock; earns only a grind-meta exception. (Lightning War, also 19/20, *used* to headline this
  list — until the all-finishers clock showed the sheet wasn't lying about it, the oracle was.)
- **The Grand Design** (18/20) — a value pile whose only finisher is un-tutorable.

**The rebuild pile (D):** Grand Design, Eldrazi Stampede (lowest CC *and* lowest outcomes — the
clearest next project), Crystal Sickness (worst external number, 9), Diminishing Returns (>T14,
death-volume-gated). **Croak and Dagger** dropped into D in the audit re-bake — but, like Lightning
War, that's a *measurement* note, not a verdict on the deck: its honest clock is a ~T13 grind (the
old `dig` knob was faking ~T10 by modelling Glarb's *selection* as raw draw), and it's the deliberate
anti-Ur-Dragon **grind fortress** (~87% heads-up vs the Dragon), built to grind + disrupt, never to
race the combo pod — D on the race oracles is its *role*, not a flaw. *(Lightning War left this pile
in the #11 re-bake — its ~T9 infinite-mana table kill is now modelled, so it's S, not a rebuild
target.)*

---

## Caveats (inherited, load-bearing)

- Clocks are **unblocked goldfish ceilings**; anti-pod folds in **measured disruption priors**;
  the mirror axes fold in a **soft durability overlay** + `T_grind`, and INTER adds a **swept**
  interaction tax. Trust the **tiers and the big gaps**, not single COMP points.
- SELF and INTER are the **same mirror bar twice** (correlated by construction) — they're a
  consensus, not two independent votes. ANTI-POD is the one truly independent axis.
- The composite **weights are a stance** (closing > building, external pod heaviest single axis),
  not a measurement. `--legacy-power` shows the v1 (CC-as-axis) list for contrast.
- This is a synthesis for orientation. Real deck decisions still go through the per-deck clock labs
  and `campaigns/Kill_Window_Lab_Sweep_2026-06-13.md`.
- **Layer C still open:** every number here predicts a *simulated* outcome. The grading instrument
  now exists end-to-end — `game_log.py` (capture) → `calibrate.py` (back-test: CLOCK MAE +
  WIN-RATE Spearman vs these same oracles) — but `analysis/game_results.jsonl` is still **empty**,
  so nothing has yet validated the tower against reality. The first logged pod games are where this
  list gets graded (`python scripts/calibrate.py`).
