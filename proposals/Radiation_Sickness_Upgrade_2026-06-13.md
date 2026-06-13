# Radiation Sickness — GC-Fix + Loam Synergy Upgrade (2026-06-13)

**The canonical Radiation Sickness upgrade proposal.** Two jobs: (1) **resolve a
standing Game-Changer-cap violation** (mandatory), and (2) spend the freed slot — plus
two more — on **non-GC Sultai synergy cards freed by the Loam Cycle teardown**, now that
Teval's dismantling removed the distinctiveness wall that benched them.

**Deck:** Radiation Sickness (`decks/radiation-sickness-20260513-phaseC.txt`), The Wise
Mothman — Sultai (BUG). Currently 18/20 (5/5/4/4).
**Lab:** `scripts/rs_clock_lab.py --mode upgrade` (40k, seed 20260613), built on
`speed_lab_core.py`. Baseline clock evidence: `analysis/Radiation_Sickness_Clock_Lab_2026-06-13.md`.

Card text verified via `card_lookup.py` (every add + cut + fork card); GC status checked
against `reference/REF_Game_Changers_List.md`; availability vs the Loam list +
`grep decks/*.txt`.

---

## ⚠️ The violation (why the first swap is mandatory, not optional)

The deployed maindeck runs **four** Game Changers, not three:

> **Seedborn Muse · Vampiric Tutor · Cyclonic Rift · Survival of the Fittest** (GC #45)

The Summary and the `REF_Game_Changers_List` Active-Decks table both report **3/3** and
file Survival under "non-GC tutor" — so the violation is invisible if you trust the docs.
It was first flagged 2026-06-12 (candidate-bake-off carry-out) and never carried into the
files. Bracket 3 caps Game Changers at 3, so **the deck is currently illegal** and the
first swap below is required regardless of the rest.

Recommended cut = **Survival of the Fittest** (the uncounted extra). Of the four it is the
most replaceable for *this* deck's win plan: the combo pieces it most wants to find
(Mindcrank, Bloodchief Ascension, Doubling Season) are **non-creatures** Survival can't
fetch — so **Vampiric Tutor** is the more important tutor — while Seedborn powers the
proliferate-on-opponents'-turns engine and Cyclonic Rift is the catch-all reset. (If you'd
rather keep repeatable creature-tutoring, cut Cyclonic Rift instead — but you lose your best
board reset, which matters more vs the pod than a 4th GC's worth of tutoring.)

---

## The swap — 3-for-3 (stays 100 cards, drops 4 GCs → legal 3/3)

| # | Out | In | Role |
|---|---|---|---|
| 1 | **Survival of the Fittest** (GC) | **Sylvan Library** | resolves the violation; {1}{G} non-GC raw selection/draw replaces the tutoring dig (watch the 4-life payments vs rad self-damage — Glowing One's lifegain offsets it) |
| 2 | **Generous Patron** | **Hedron Crab** | Patron's "draw when you counter a creature you *don't* control" rarely fires (you counter your own). Hedron Crab = a 2nd landfall **mill 3** → another Mothman counter-distribution trigger every land drop — pure engine fuel + self-mill |
| 3 | **Guardian Project** | **Sidisi, Brood Tyrant** | Guardian Project is anti-synergy in a go-wide deck (tokens from Hornbeetle/Herd Baloth/Broodscale don't trigger it). Sidisi mills 3 on ETB/attack (more Mothman triggers) **and** makes a Zombie per creature card milled — widening the board for Triumph of the Hordes |

**GC re-cert after the swap:** Seedborn Muse · Vampiric Tutor · Cyclonic Rift = **3/3, legal.**
**Count:** 99 − 3 + 3 = 99 (+ commander = 100). ✔

All three adds are Sultai, were in the Loam Cycle (or are cheap), and were previously
excluded only because Teval owned the graveyard/value identity — a constraint that is gone.

---

## Lab results (`rs_clock_lab.py --mode upgrade`, 40k, seed 20260613)

Two models, because the committed clock lab is the **coarsest in the sweep** and folds all
milling into the rad drain. The `+mills` model is **producer-faithful** — it scores the
discrete mill sources (Ruin Crab + Altar of the Brood baseline; + Hedron Crab + Sidisi
proposed) as the separate Mothman triggers they are, applying the 2026-06-13 producer-
inventory lesson.

| Build | T6 decap | T7 decap | T8 table | T9 table | T10 table | median decap / table |
|---|:--:|:--:|:--:|:--:|:--:|:--:|
| baseline (committed model) | 32 | 76 | 21 | 49 | 74 | T7 / **T10** |
| proposed (committed model) | 33 | 76 | 21 | 50 | 75 | T7 / **T10** |
| baseline + mills (producer-faithful) | 36 | 77 | 25 | 54 | 78 | T7 / **T9** |
| **proposed + mills (producer-faithful)** | **41** | **79** | **29** | **60** | **82** | T7 / **T9** |

**What the lab says, honestly:**

1. **The committed model can't see the upgrade** (proposed ≈ baseline, flat). Sylvan /
   Survival / Patron / Guardian Project are invisible to a goldfish, and Sidisi/Hedron Crab
   as vanilla bodies are negligible. This is *expected* and is the whole reason for the
   second model.
2. **Modeling the producers at all already lifts the *baseline* table T10 → T9** (T9
   49% → 54%) — i.e. the committed lab slightly under-rated the deployed deck by ignoring
   Ruin Crab + Altar mill. (A "learn-from-history" byproduct: the un-modelled-producer
   caveat the clock-lab writeup flagged was real, ~1 turn.)
3. **The proposed adds tighten the distribution without moving the median turn:** T6 decap
   **+5pp** (36 → 41), T9 table **+6pp** (54 → 60), T10 table **+4pp** (78 → 82); never-in-14
   stays 1%. The extra mill fuels Mothman → more +1/+1 placements → Simic growth and the
   wide-board Triumph fire a touch sooner across more games.

**Verdict: the upgrade buys reliability, not raw speed.** Median kill turn is unchanged
(decap T7 / table T9); the win comes from the **rad-drain `hit_all`, which is creature-count-
independent**, so no go-wide add can move the median — only the front edge and mid-curve, which
it does. This is the framework's recurring result (adds move the distribution, not the median).

**The biggest wins are OFF-clock — the goldfish cannot score them:** GC legality (non-
negotiable), Sylvan Library's selection (combo-find reliability, partly replacing the cut
tutor), and the Force-of-Will fork below (Interaction 4→5). Judged, not measured.

**Honest cost:** cutting Survival drops the deck from two tutors to one (Vampiric remains).
Sylvan's selection + the added mill fuel partially offset the lost combo-find, but on-demand
assembly of Mindcrank+Bloodchief is marginally less reliable. The fix is mandatory regardless.

---

## The 19/20 fork (and why I recommend *against* it for this pod)

The two soft axes are **Interaction (4/5)** and **Durability (4/5)**. The reality of the
color identity makes both hard to lift cleanly:

- **Durability 4→5 is nearly closed in Sultai.** The premier anti-wrath protection —
  **Teferi's Protection, Clever Concealment, Flawless Maneuver — are all white**, off-color
  here. The deck already runs the best in-color option (Heroic Intervention); Crucible of
  Worlds (the audit's "permanence" example) is in-color but marginal (RS isn't a lands deck).
- **Interaction 4→5 needs a 2nd free counter.** In blue that means **Force of Will** —
  but it's a **GC**, so it costs a GC trade: **+Force of Will / −Cyclonic Rift** (both blue,
  stays 3/3). That lifts Interaction to 5/5 → a 5/5/4/5 = **19/20**.

**But this fork is a rubric move, not a pod move — flag it as such.** Against the archenemy,
Grand Abolisher blanks your counters on their combo turn (`Pod_Matchup_Matrix.md`), so
**Force of Will is dead exactly when you need it**, while **Cyclonic Rift — castable on your
own turn — is one of your few Abolisher-proof answers.** Trading Rift for FoW *raises the
Conversion-Check score and weakens the actual matchup.* (The non-GC alternative, **Pact of
Negation**, avoids the GC trade but is also a counter — same Abolisher problem — and carries
the "pay {3}{U}{U} or lose" tax.)

**Recommendation: keep Cyclonic Rift and stay 18/20.** The score⊥pod gap is the whole
finding of the kill-window sweep; chasing the 20th point here trades a real answer for a
paper one. The GC-fix + Loam reliability adds are the genuine improvement.

---

## Availability (CLAUDE.md cross-deck check)

| Add | Status |
|---|---|
| Sylvan Library | **free from Loam teardown** (1 copy; unallocated — confirm against the parts-bin map) |
| Hedron Crab | **free from Loam teardown** (Loam ran it) |
| Sidisi, Brood Tyrant | **free from Loam teardown** (Loam ran it) |
| *(fork)* Force of Will | owned but **deployed in The Grand Design** — buy a 2nd (~€60+, premium; price unverified) or skip the fork |

With "a vast collection," none of the three core adds need a Loam pull if duplicates exist.
The fork's Force of Will is the one genuinely contested/expensive piece — another reason the
fork is optional.

---

## Maybeboard (considered, not in the 3-for-3)

- **Psychic Frog** ({U}{B}) — discard → +1/+1 (proliferate doubles it), draws on combat
  damage, self-evasion. A clean counters-theme 2-drop; cut for Sidisi only because Sidisi's
  mill+tokens feed two engine axes. Swap in if you want card advantage over go-wide.
- **Crucible of Worlds** ({3}) — the audit's "permanence" Durability example; recurs
  incidentally-milled lands. Marginal here (not a lands deck) — park it.
- **Tato Farmer / Glowing One** — *not* cut candidates despite looking like filler: both are
  rad generators (Tato landfall → 2 rad, doubled by Vorinclex; Glowing One combat → 4 rad +
  lifegain). They feed the **table win clock** — leave them in.

---

## Status

**Proposal only — not applied.** Deployed `.txt` unchanged; the GC violation is flagged in
the Summary but not yet fixed (per the house rule: flag the cap, let the user choose the cut).
To apply: bump the dated filename (`radiation-sickness-<today>.txt`), archive the old list to
`archive/old_decklists/`, make the 3 swaps, recount to 100, confirm **3/3 GCs**, and update the
Summary's Bracket-3 Compliance + decklist sections. Re-run `rs_clock_lab.py --mode upgrade` if
the list changes further.
