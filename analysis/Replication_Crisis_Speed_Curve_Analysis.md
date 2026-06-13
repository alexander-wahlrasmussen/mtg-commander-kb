# Replication Crisis — Speed-Curve Analysis: Can It Race the Combo Pod?

**What this is:** the same rigor applied to Lightning War (`Lightning_War_Speed_Curve_Analysis.md`), Calamity Tax, and Grand Design, turned on **Satya (The Replication Crisis)** — this time to answer one question: **can this deck beat the pod combo opponent (kill T6–7 behind Grand Abolisher) on the clock?** The Pod Matchup Matrix already flagged the deck as "overrated as a race" on structural grounds; this measures it.

**Date:** 2026-06-09
**Card text verified** against local Scryfall data (`card_lookup.py`) for Satya, Sword of Feast and Famine, Aggravated Assault, Adeline, Anointed Procession, Brudiclad, Inferno Titan, Strionic Resonator, and the pending-swap trio (Kiki-Jiki, Zealous Conscripts, Restoration Angel) — not pattern-matched.
**Deck measured:** `decks/the-replication-crisis-20260504-202914.txt` (current 99) plus the pending-Kiki variant (−Bident +Kiki, `The_Replication_Crisis_Swaps_2026-06-01.md`, not yet applied).
**Lab:** `scripts/rc_speed_lab.py` (40k trials, seed 12345), built on `deck_sim.py`'s engine. Unlike the prior labs it includes a **goldfish combat clock**: Satya attack tokens (copy value = power + Inferno Titan's enters/attacks 3), Anointed Procession doubling, Panharmonicon/Elesh Norn ETB-doubling, the energy bank paying to keep tokens, Brudiclad's begin-of-combat conversion, Aggravated Assault extra combats, the Sword+AA infinite, and Akroma's Will as a one-shot damage doubler.

> **Bottom line up front: No — the deck cannot race a T6–7 combo clock, and the Summary's "Goldfish T5–7" window was a god-draw artifact.** At the *zero-blocker ceiling* (every creature unblocked, no interaction, Satya never dies), the deck has killed **one** focused opponent by T6 only **16%** of the time (median **T7**); under a defended-board proxy that drops to **6%** (median **T8**). The **table** kill — what "winning the race" actually requires if the combo player isn't decapitated first — is **T10–11 median even unblocked** (4% by T8). The Sword+AA infinite decides ~1–3% of games; the pending Kiki swap moves the clock by ~0 (it's a resilience fix, as its own proposal says). Bring Lightning War or Grand Design to that table instead.

---

## The question

The matchup matrix gives the pod combo opponent a **T6–7 kill behind Grand Abolisher**. Counterspells are dead on their combo turn, so a deck beats them by (a) **static disruption in play**, or (b) **killing first** — either the whole table or the combo player specifically (decapitation). Replication Crisis has no static hate, so its row lives or dies on (b). The Summary's Quick Reference claims "Goldfish: T5–7," while the matrix reassessment note argued that's a god-draw floor. Who's right, and by how much?

---

## 1. Kill-package availability — every fast line is a low-percentage draw

`rc_speed_lab.py --mode avail`. The deck has **zero tutors that find any package piece** (Ranger-Captain of Eos fetches MV≤1 creatures only), so there is no "+tutors" column — these *are* the numbers.

| P(package complete ≤ T), % | T4 | T5 | **T6** | T7 | T8 | T10 | T12 |
|---|---|---|---|---|---|---|---|
| **INF** — Sword of F&F + Aggravated Assault | 1 | 1 | **1** | 2 | 2 | 2 | 3 |
| **ALPHA** — Adeline + Anointed Procession | 1 | 1 | **1** | 1 | 2 | 2 | 3 |
| **BRUD** — Brudiclad (1 card, but see §3) | 10 | 11 | **12** | 13 | 14 | 16 | 18 |
| **ANY of the three** | 11 | 13 | **14** | 15 | 17 | 20 | 23 |
| *pending-Kiki variant:* Kiki + Conscripts/Resto | 2 | 2 | **2** | 3 | 3 | 4 | 6 |

The two named 2-card packages sit at the familiar ~1–2% untutored-pair floor (same maths that doomed Lightning War's old AA+Ozai combo). The only package that shows up reliably is Brudiclad — a single card — but Brudiclad isn't a kill by itself (§3). Compare Lightning War today: **≥1 table-finisher 22% drawn / 47% with tutors by T6**, because its kill is *one of four* cards behind a free commander, with three tutors pointing at them.

---

## 2. The clock — what the goldfish actually kills, and when

`rc_speed_lab.py --mode clock`. Mana-aware (lands + all 10 rocks), greedy board development, 3 opponents at 40, **all damage focused on one opponent (the combo player) until dead**. Two attack policies bracket reality:

- **ALL-IN** — every summoning-sick-free creature attacks, *nothing is ever blocked*. A pure ceiling: only Satya has menace; against an Ur-Dragon shell with large flying blockers this is fantasy.
- **SQUAD** — only Satya + her tokens (+ kept tokens/Myr) attack; Adeline still triggers (her tokens enter attacking without being declared). A rough proxy for a defended board.

| P(dead ≤ T), % | T5 | **T6** | **T7** | T8 | T10 | T12 |
|---|---|---|---|---|---|---|
| ALL-IN: **combo player** dead | 2 | **16** | **59** | 80 | 94 | 99 |
| ALL-IN: **table** dead | 0 | **1** | **1** | 4 | 35 | 79 |
| — of which via Sword+AA infinite | 0 | 1 | 1 | 1 | 2 | 3 |
| SQUAD: **combo player** dead | 1 | **6** | **28** | 65 | 92 | 98 |
| SQUAD: **table** dead | 0 | **1** | **1** | 2 | 16 | 48 |
| *pending-Kiki:* Kiki line online (mana-aware) | 1 | **2** | **2** | 3 | 4 | 5 |

**Read:**

1. **The honest goldfish window is T7–8 for one player and T10+ for the table** — not the Summary's T5–7. "T5" exists (2%) but is a god-draw, exactly as the matrix note suspected.
2. **Against a T6–7 combo win, the decapitation race is 16% at the unblockable ceiling, 6% defended.** And decapitation only works if you correctly focus the combo player from turn ~4 and they never block, remove Satya, or chump. The pod's actual deck — an Ur-Dragon ramp shell — is the *worst possible* opponent to race with combat: it presents big flying blockers without trying.
3. **The infinite is a rounding error** (≤3% by T12). It's a nice line to keep, not a plan.
4. **The Summary's "2–3 turns from engine-online to kill" is right — and that's the problem.** Satya lands T4 at the earliest, the engine compounds T5–6, lethal-on-one arrives T7–8. A combat-sequenced kill pays a per-turn tax a one-cast kill doesn't.

---

## 3. Why the lines are structurally slow (text-verified)

- **Every line is sequenced across combat steps.** Satya's trigger fires *per attack*; tokens are sacrificed at end step unless energy (2/attack) covers their MV — an Inferno Titan token costs 6{E}, i.e. **three attacks of banked energy to keep one**. Early turns the board doesn't compound; it resets.
- **Adeline's tokens are spread, not focused.** Her printed text creates 1/1s "for each opponent... attacking **that player**" — with Procession that's 2 damage/turn to the racing target, not 6. The ALPHA package reads much better in the Summary than it measures.
- **Brudiclad is a +1-combat tax.** His conversion happens at *the beginning of combat*, so the token you want to copy (e.g. a Satya-made Titan) must already exist from a **previous** combat, and the converted swarm connects one combat later still. A 6-mana card that needs T+1 and T+2 to pay off is not a racing card.
- **The deck's interaction can't protect a race against this pod anyway.** Its shield is counterspell-shaped (FG, Swan Song, An Offer, Swat) — dead under the opponent's Grand Abolisher on the only turn that matters if you *haven't* already killed them.

---

## 4. The pending Kiki swap doesn't change this verdict (and wasn't supposed to)

The −Bident +Kiki proposal adds Kiki + Conscripts and Kiki + Resto — Satya-free, combat-free *assembly* wins. Mana-aware, the line is online **2% by T6–7, 5% by T12**: it raises the deck's **resilience and ceiling** (no longer folds to Satya removal), exactly as `The_Replication_Crisis_Swaps_2026-06-01.md` claims — and it does **not** make the deck a racer, exactly as the matrix note warned. Both documents survive this analysis unchanged; the *Summary's* kill window does not (corrected, see below).

---

## 5. Verdict vs the pod — and the matrix row

| | Replication Crisis | Lightning War (for contrast) |
|---|---|---|
| Kill delivery | combat, sequenced over 2–4 turns, blockable | one cast in Azula's combat, ignores blockers |
| Closer availability T6 | 14% (any package, drawn; no tutors) | 22% table / 39% any drawn → 47/59% +tutors |
| Realistic kill | T7–8 one player / T10+ table | T6–7 table |
| Vs their Abolisher | counters dead; no static hate | races; Banefire uncounterable |
| Vs their blockers | bad (Ur-Dragon bodies blank the swarm) | irrelevant |

**Matrix consequence:** the row's verdict (*Even — overrated as a race*) is confirmed and now quantified; the clock cell tightens from "T6–8 (T5 god-draw)" to **"T7–8 decap / T10+ table (lab)"**. The deck's real pod value remains what the Summary's Pod Fit section says: a flexible, incremental value engine that recovers well — a fine *second threat*, not the deck you bring to out-race this opponent.

**Recommendation: don't try to turn Satya into a racer.** Making this deck beat a T6–7 clock would mean grafting on a tutor package + a combat-independent kill — that's a different deck wearing Satya's clothes (the matrix's rec #3 anti-pattern). The right moves are already on file: apply the Kiki swap for resilience (pending purchase + pod approval), and bring **Lightning War** or **The Grand Design** (post finisher/ETB merge) to the combo table.

---

## Method caveats

- `rc_speed_lab.py` is a **heuristic goldfish**, not a rules engine. Nothing blocks, nobody interacts, Satya never dies, focus-fire is perfect from turn 1. Every one of those favours the deck — the real numbers are *worse* than the table above.
- Not modelled (all small, mostly conservative): Strionic Resonator's second trigger, Phelia/Resto flicker value, Goldspan Treasures, The One Ring draw, Snapcaster/Knight ETBs. Ponder/Preordain modelled as dig-2; Cloudblazer/Wall of Omens draw counted on cast.
- Adeline's dynamic power and the energy-keep economics are modelled per printed text (verified 2026-06-09).
- Reproduce: `python scripts/rc_speed_lab.py --trials 40000` (seed fixed at 12345).

---

Related: `The_Replication_Crisis_Summary.md` · `The_Replication_Crisis_Swaps_2026-06-01.md` · `Pod_Matchup_Matrix.md` · `Lightning_War_Speed_Curve_Analysis.md` · [[project_replication_crisis_b4_swap]] · [[project_pod_combo_opponent]]
