# The Definitive Tier List — 2026-06-15

> **SUPERSEDED 2026-06-28 by [`Definitive_Tier_List_2026-06-28.md`](Definitive_Tier_List_2026-06-28.md)**
> (v2), which ranks on the **three convergent OUTCOME oracles** (pod_gauntlet · interaction_meta ·
> self_meta) instead of two-outcome-plus-Conversion-Check. The interaction-overlay oracle didn't
> exist when this v1 was written. Kept for the record; reproduce this exact list with
> `python scripts/tier_list.py --legacy-power`.

*One honest ranking of the 16 active decks, as a composite of the three things the lab stack
actually measures. The synthesis read — caveats baked in. Reproduce:
`python scripts/tier_list.py --legacy-power` (was `tier_list.py` before the v2 default).*

**Composite** = weighted mean of three min-max-normalised axes (`scripts/tier_list.py`):

| Axis | Source | "Measures" | Weight |
|---|---|---|---:|
| **ANTI-POD** | `pod_gauntlet --vs` blend | Wins vs the recurring T6-7 combo opponent (the meta that matters) | 0.40 |
| **SELF-META** | `self_meta_lab` P(win\|random pod) | Wins in a pod of your own decks | 0.35 |
| **POWER** | Conversion Check /20 | How good the build is (clock-blind) | 0.25 |

The two "does-it-actually-win" axes outweigh raw build quality 75/25 — the hard-won lesson of
the entire lab stack: **closing > building.** Each axis inherits its source's caveats (goldfish
ceilings, soft durability/disruption priors). This is a synthesis, not a new sim.

---

## The list

| Tier | Deck | Pwr/20 | Self% | Anti% | Table | COMP |
|:--:|---|:--:|:--:|:--:|:--:|:--:|
| **S** | **Radiation Sickness** | 18 | 42% | 70% | T10 | **78** |
| **S** | **The Genome Project** | 15 | 79% | 61% | T8 | **74** |
| **A** | The Replication Crisis | 17 | 17% | 63% | T10 | 58 |
| **A** | The Exile's Return | 18 | 35% | 44% | T10 | 58 |
| **A** | Lightning War | 19 | 6% | 49% | T14 | 54 |
| **A** | Lorehold Spirits | 18 | 31% | 39% | T10 | 53 |
| **A** | Zero-Sum Game | — | 52% | 34% | T9 | 53 |
| **B** | The Dark Lord's Army | 19 | 23% | 26% | T12 | 46 |
| **B** | Curse of the Scarab | 17 | 24% | 39% | T11 | 45 |
| **B** | The Calamity Tax | 18 | 36% | 22% | T10 | 44 |
| **B** | Earthbend the Meta | 17 | 17% | 42% | T11 | 44 |
| **C** | The Grand Design | 19 | 1% | 30% | >T14 | 39 |
| **C** | Ms. Bumbleflower | 15 | 13% | 47% | T11 | 36 |
| **D** | Diminishing Returns | 17 | 4% | 17% | >T14 | 22 |
| **D** | Crystal Sickness | 17 | 12% | 9% | T13 | 20 |
| **D** | Eldrazi Stampede Chaos | 14 | 11% | 26% | T12 | 16 |

---

## The one finding that matters: score ⊥ winning

**The three 19/20 decks land in A, B, and C.** The two best decks overall score **18 and 15.**
Raw Conversion score and actually closing games are nearly orthogonal at the top — exactly the
"score ⊥ clock" thesis the kill-window sweep found, now confirmed across the full composite.
A high score means the deck is *well-built for what it does*; it does not mean it wins.

---

## Tier verdicts

### S — wins on every axis that counts
- **Radiation Sickness (78)** — the most complete deck you own. Best anti-pod number on the
  roster (70%) because its kills are *board states* (Simic Ascendancy / Toxrill / rad counters)
  that counterspells can't touch, and it's the best **hedge vs the Ur-Dragon** fair deck too
  (board-independent sweeper-proof clock). 18/20, clean 3/3 GCs after the 2026-06-15 fix. No
  glaring weakness.
- **The Genome Project (74)** — *the championship winner.* Only 15/20, but it has the fastest
  table clock on the roster (T8) and a hit-all ping kill (decap ≈ table), so it both closes
  first and survives any seeding. Self-meta 79%. The clock is structurally maxed (every lever
  tested flat). Lower ceiling on paper, highest floor in practice.

### A — a real weapon, with one soft axis
- **The Replication Crisis (58)** — anti-pod 63% (3rd best) on counter-immune combat/Kiki
  kills; the gap is the **table** clock (T10) — it decaps the combo player fast but can't close
  three seats quickly. Pending Satya-free Kiki line adds resilience.
- **The Exile's Return (58)** — 18/20, durability 0.79, runs **its own** Grand Abolisher to
  protect its kill; pending Kiki+Felidar 2-card line. Balanced, no embarrassing axis.
- **Lightning War (54)** — the **highest raw score (19/20)** but self-meta 6% and a T14
  *goldfish* table clock: the burn plan chips the whole table, which the strict decap clock
  doesn't score (the cross-table chip model collapses it to ~T10 in a real pod). Banefire is an
  uncounterable finisher (PROTECT 0.65). It's better than its self-meta number; it's worse than
  its score.
- **Lorehold Spirits (53)** — 18/20, T10, but zero counters — it has to land its kill into open
  mana. Solid, exposed.
- **Zero-Sum Game (53)** — *the quiet overperformer.* No formal Conversion score yet (audit
  pending), but self-meta 52% (2nd on the roster) on a T9 board-independent, **Abolisher-proof**
  lifeloop. Re-roled as the anti-fair-deck answer (Glarb). Audit it — it may be S.

### B — good build, can't quite close
- **The Dark Lord's Army (46)** — the paradox deck. 19/20 and the **self-meta judgment #1**
  (durability 0.86, opponent-fed Sauron engine, 3 sweepers = best vs Ur-Dragon) — but a T12
  clock buries it in the composite. **It is the deck that most rewards a grindy meta:** drop
  `T_grind` and it rises to the Final Four (see the Pod Championship). A fortress, not a racer.
- **Curse of the Scarab (45)** — 17/20, zombie-army board kill, honest mid-speed (T11).
- **The Calamity Tax (44)** — 18/20; the grind-fortress rebuild dragged the table clock T13→T10
  (4%→29% ungated). Still the gauntlet's **least-supported "Favoured"** and the weakest anti-pod
  number (22%) — its X-drain kill is a counterable spell. Re-roled vs Ur-Dragon (Glarb anti-fair).
- **Earthbend the Meta (44)** — 17/20, T11; REB/Pyroblast give it extra bite specifically into
  the UB Hidetsugu & Kairi shell.

### C — over-rated by the score sheet
- **The Grand Design (39)** — the cautionary tale. **19/20, self-meta 1%, >T14 table, 82%
  never-closes.** Its ten kill lines all funnel through Finale, a *sorcery* the creature-tutors
  can't find; combat is the real (slow) clock. The single most over-rated deck on the roster by
  raw score. Disruption-led value pile, not a closer.
- **Ms. Bumbleflower (36)** — 15/20, slow combat-steal kill (Willbreaker), but **0 GCs = the
  most open upgrade path** on the roster.

### D — the rebuild pile
- **Diminishing Returns (22)** — 17/20 on paper, but >T14 / 70% never-close: the death-combo is
  gated on death *volume*, not the multipliers it's built around. Pending Nim Deathmantle + Grave
  Titan line is the fix.
- **Crystal Sickness (20)** — worst anti-pod on the roster (9%), low durability (0.37),
  dev-gated despite looking finding-gated (the dig brackets to ≤1 turn).
- **Eldrazi Stampede Chaos (16)** — lowest raw score (14/20) and bottom composite; chaos
  refinement long deferred. The clearest "next project" candidate.

---

## Caveats (inherited, load-bearing)
- Clocks are **unblocked goldfish ceilings**; anti-pod folds in **soft disruption priors**;
  self-meta folds in a **judgment durability overlay** and `T_grind`. Trust the **tiers and the
  big gaps**, not single COMP points.
- The composite **weights are a stance** (closing > building), not a measurement. Re-weight in
  `tier_list.py` to see a build-quality-first list (POWER up) reshuffle A/B.
- This is a synthesis for fun and orientation — real deck decisions go through the per-deck clock
  labs and `campaigns/Kill_Window_Lab_Sweep_2026-06-13.md`.
