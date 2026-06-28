# The Definitive Tier List, v2 — 2026-06-28

*Supersedes [`Definitive_Tier_List_2026-06-15.md`](Definitive_Tier_List_2026-06-15.md). One honest
ranking of the 16 active decks — but now a composite of the **three convergent OUTCOME oracles**,
not two-outcome-plus-build-quality. Reproduce: `python scripts/tier_list.py`
(legacy v1: `python scripts/tier_list.py --legacy-power`).*

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
| **S** | **The Genome Project** | 61 | 70 | 77 | 15 | T8 | **93** |
| **S** | **Radiation Sickness** | 70 | 44 | 41 | 18 | T10 | **76** |
| **A** | The Replication Crisis | 64 | 26 | 23 | 17 | T10 | 57 |
| **A** | Zero-Sum Game | 34 | 48 | 51 | — | T9 | 55 |
| **B** | The Exile's Return | 44 | 37 | 33 | 18 | T10 | 51 |
| **C** | Lorehold Spirits | 39 | 23 | 30 | 18 | T10 | 40 |
| **C** | Curse of the Scarab | 39 | 24 | 23 | 17 | T11 | 38 |
| **C** | Ms. Bumbleflower | 47 | 13 | 12 | 15 | T11 | 36 |
| **C** | The Calamity Tax (Croak & Dagger) | 22 | 37 | 35 | 18 | T10 | 36 |
| **C** | Earthbend the Meta | 42 | 16 | 16 | 17 | T11 | 35 |
| **C** | Lightning War | 49 | 6 | 5 | **19** | T14 | 32 |
| **C** | The Dark Lord's Army | 26 | 29 | 22 | **19** | T12 | 31 |
| **D** | The Grand Design | 38 | 5 | 5 | 18 | >T12 | 22 |
| **D** | Eldrazi Stampede Chaos | 26 | 8 | 11 | 14 | T12 | 17 |
| **D** | Crystal Sickness | 9 | 11 | 11 | 17 | T13 | 6 |
| **D** | Diminishing Returns | 17 | 3 | 4 | 17 | >T14 | 6 |

*(Trials 40k, T_grind 10, TAX 0.6, seed from `self_meta_lab`. COMP = weighted mean of the three
min-max-normalised axes.)*

---

## The one finding that matters, now even starker: score ⊥ winning

v1 noted the three 19/20-equivalent decks scattered S→A→C. v2, ranking **purely on outcomes**,
makes it undeniable:

> **The two highest-scored decks you own — Lightning War and The Dark Lord's Army, both 19/20 —
> rank 11th and 12th of 16.** Both land in **C tier.** The third-highest, Grand Design (18/20),
> is **D**. Meanwhile the apex of the roster, The Genome Project, scores **15/20.**

The Conversion Check tells you a deck is *well-built for what it's trying to do.* It does **not**
tell you the deck wins. Across three independent outcome oracles, the correlation between CC and
finishing position is, if anything, mildly **negative** at the top. Trust the tiers, not the sheet.

---

## The reconciliation — where the oracles DISAGREE, and what it means

This is what v1 couldn't show with only two outcome axes. The two bars — **external pod** (anti)
and **mirror** (inter/self) — pull different decks in different directions. Read the *gap*:

### Apex — strong on BOTH bars
- **Genome Project** is the only deck top-2 on all three oracles (anti 61 · inter 70 · self 77).
  Fastest table clock on the roster (T8), a hit-all ping kill (decap ≈ table), 1% never-close. It
  both closes first **and** survives any seeding. *The interaction overlay is the only thing that
  dings it (Δ−7): it's fast but answerable. It wins anyway.* The true #1, on 15/20.

### Specialists — strong on ONE bar, the mirror-image of each other
- **Replication Crisis** — anti **64** (4th-best external) but mirror **23–26** (low). Its decap
  clock (T7) races the external combo pod; its **table** clock (T10) + 20% never-close can't grind
  a mirror. A *pod specialist* — tuned to neutralise the archenemy, not to win a fair four-way.
- **Zero-Sum Game** — the exact inverse: mirror **48–51** (2nd) but anti **34**. The
  board-independent, **Abolisher-proof** lifeloop wins durability races, but its T9 decap is a beat
  too slow for the fast external pod. *A mirror grinder.* Still has **no formal CC score** — and v2
  scores it on outcomes alone, where it's clearly A. (Audit it; it may belong higher.)

### Over-rated fortresses — high CC, low on BOTH bars
- **Lightning War (19/20)** — the widest split on the roster: anti **49** (it survives the external
  pod — best disruption suite, holds answers 80%, Banefire uncounterable) but mirror **5–6**
  (*dead last*). A T14 table clock with 39% never-close: it decaps one seat and then cannot finish
  the other two. The canonical over-rate — the score sheet's favourite, the mirror's punching bag.
- **The Dark Lord's Army (19/20)** — the subtle one. CC's #1, the **most durable** deck on the
  roster (0.86), and the **only** deck the interaction overlay *lifts* meaningfully (Δ**+7** — it
  taxes opponents' closes while outlasting them). But a T12 clock buries it: anti 26, and it needs a
  **grindy** meta to shine. Raise `--t-grind` and it climbs toward the Final Four (see the Pod
  Championship). A fortress, not a racer — over-rated by CC, *under-rated by pure race.*
- **The Grand Design (18/20)** — >T12 table, 5% on both mirror oracles. Ten kill lines all funnel
  through Finale, a *sorcery* the creature-tutors can't fetch; combat is the real, slow clock. A
  disruption-led value pile. The clearest cautionary tale after Lightning War.

### The interaction overlay's net verdict (second-order, not a reversal)
The overlay **lifts** durable / answer-dense grinders (Dark Lord +7, Radiation +3, Exile's +3,
Croak +2) and **sinks** fast-but-answerable glass (Genome −7, Lorehold −6). But it does **not**
rescue any fortress into contention — Lightning War is still last in the mirror with or without it.
**The decap/table clock dominates; interaction is a real but secondary correction.** (At TAX=0 the
overlay is a verified null reduction — it reproduces self_meta bit-for-bit; `tests/test_null_reduction.py`.)

---

## So: who should the pod fear, and what's over-rated?

**Fear these (bring them to a real pod):**
1. **Genome Project** — the apex. Fast and unkillable in the standings. Your default.
2. **Radiation Sickness** — *specifically* the external pod's nightmare (anti 70, best on the
   roster): its kills are board states counterspells can't touch, and it's the best hedge vs the
   Ur-Dragon fair deck too.
3. **Replication Crisis** — when you *know* it's the T6–7 combo pod: it races them (anti 64). Less so
   into a grind.
4. **Zero-Sum Game** — the quiet overperformer and Abolisher-proof. Bring it into a slow/grindy table.

**Stop over-rating these (the sheet lies about them):**
- **Lightning War** and **The Dark Lord's Army** (both 19/20) — fortresses that hold answers but
  can't close a table. Dark Lord earns a grind-meta exception; Lightning War doesn't.
- **The Grand Design** (18/20) — a value pile whose only finisher is un-tutorable.

**The rebuild pile (D):** Grand Design, Eldrazi Stampede (lowest CC *and* lowest outcomes — the
clearest next project), Crystal Sickness (worst external number, 9), Diminishing Returns (>T14,
death-volume-gated).

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
- **Layer C still open:** every number here predicts a *simulated* outcome. Nothing yet validates
  the tower against real games (`game_log.py` is built; `analysis/game_results.jsonl` is empty;
  `calibrate.py` unbuilt). The first logged pod games are where this list gets graded.
