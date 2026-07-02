# The Measured Pod Profile — Backlog #13 Phase 3 (2026-07-02)

*The payoff of "measure the pod." Phase 0 asked whether the hand-assumed `pod_gauntlet.K_DIST`
("wins T6-7", mean T6.70) is load-bearing (yes, in the middle band + all absolute levels). Phases
1–2.5 reconstructed and clock-labbed the four decks his rotation actually fields. This folds those
MEASURED curves into `pod_gauntlet` as an OPT-IN profile and re-runs the tier list on it.*

Reproduce: `python scripts/pod_gauntlet.py --vs --measured` · `python scripts/pod_clock_sensitivity.py`
(prints the "AT THE MEASURED PROFILE" block) · toggle in code with `pg.set_profile(True)` or
`POD_MEASURED_PROFILE=1`. **Default OFF** — the legacy hand-assumed model is byte-identical until
turned on (`tests/test_pod_measured_profile.py` pins the null reduction).

---

## The model change

The legacy anti-pod model raced every deck against ONE hand-assumed `K_DIST` blended over a
generic three-slot opponent (Acererak / H&K / a "5C-tail" that could field Grand Abolisher). The
measured profile replaces it with the four decks he actually brings, each carrying **its own
lab-measured attempt/kill curve** instead of the shared assumption:

| Opponent | weight | measured K (decap median) | disruption_a / answer | source |
|---|---:|---|---|---|
| Acererak (mono-B combo-drain) | **0.40** | **>T14** (v2 all-lines; nv59%, T10 9% / T12 25%) | 0.05 / 0.10 | `opp_acererak_lab --mode bestline` |
| The Ur-Dragon (combat+burn) | **0.30** | **T8** (UNBLOCKED ceiling) | 0.08 / 0.12 | `opp_urdragon_lab` |
| Hidetsugu & Kairi (UB clone-drain) | **0.20** | **T8** (real T5-6 edge, nv 8%) | 0.30 / 0.30 | `opp_hk_lab` (real 2023 list + banfix) |
| Henzie (Rakdos blitz) | **0.10** | **T11** (grinder) | 0.05 / 0.08 | `opp_henzie_lab` |

Three things changed together, so this is a NEW model, not a single-parameter shift:
1. **Per-opponent K** — each `OPPONENTS` entry carries a measured `kdist` derived from its lab
   decap curve (`opp_kdist()`); the never-in-horizon mass lands on a `NEVER_K` sentinel (they
   never combo → we win by default). Sampled per-opponent in `simulate_vs`.
2. **Weights = the observed rotation** (user-confirmed 2026-07-02): Ur-Dragon + Acererak every
   meetup, H&K occasional-but-stomps, Henzie once. The legacy **5C-tail (Kenrith/Kinnan) is
   RETIRED** — unseen.
3. **Disruption re-derived DOWN** — no deck in the current stable can cast the **white** Grand
   Abolisher (Acererak mono-B, H&K UB, Henzie Rakdos, his Ur-Dragon list has none). Only H&K's UB
   counter wall keeps a real reactive tax (a=0.30); the rest are ~0. The legacy Abolisher-era
   `a≈0.15–0.30` sweep the whole disruption model was built around is obsolete vs this stable.

---

## The measured tier list vs the hand-assumed baseline (40k, seed 20260615)

| Deck | base tier | **meas tier** | base anti% | **meas anti%** | move |
|---|:--:|:--:|:--:|:--:|:--|
| The Genome Project | S | S | 61 | 91 | |
| Lightning War | S | S | 57 | 85 | |
| Radiation Sickness | A | A | 63 | 91 | |
| The Replication Crisis | A | A | 64 | 90 | |
| Zero-Sum Game | A | **B** | 33 | 61 | **A→B** |
| Croak and Dagger | A | A | 32 | 70 | |
| The Exile's Return | A | A | 49 | 86 | |
| Forced Liquidation | B | **A** | 38 | 75 | **B→A** |
| Lorehold Spirits | B | B | 39 | 81 | |
| Ms. Bumbleflower | C | **B** | 48 | 87 | **C→B** |
| Curse of the Scarab | C | **B** | 37 | 79 | **C→B** |
| Earthbend the Meta | C | **B** | 42 | 82 | **C→B** |
| The Dark Lord's Army | C | C | 26 | 70 | |
| The Grand Design | D | **C** | 36 | 77 | **D→C** |
| Eldrazi Stampede Chaos | D | **C** | 26 | 75 | **D→C** |
| Diminishing Returns | D | D | 17 | 70 | |
| Crystal Sickness | D | D | 9 | 49 | |

**Rank stability: Spearman ρ = 0.961 (n=17). 7 of 17 tiers move.** The apex (Genome/LW S;
Radiation/Replication/Croak/Exile A) and the D-floor (Diminishing/Crystal) are unchanged; every
move is in the middle band, and (bar one) UPWARD — exactly what the Phase-0 sweep predicted from
its `+1`/`slow` columns: **a slower measured pod lifts the fortresses and mid-clock grinders**
(FL B→A, Bumbleflower/CoS/Earthbend C→B, Grand Design/Eldrazi D→C), because a deck that couldn't
win a T6-7 race gets to close against a pod that doesn't actually kill until T8+. The lone
DOWN move is **Zero-Sum A→B**: its anti-pod gains LESS than the field (board-independent lifeloop
was already winning on durability, not the race), so under min-max renormalisation it slips a cut.

This ranking largely reproduces the assumed baseline — the whole reason Phase 0 rated the ranking
ROBUST (ρ≥0.975 across the sweep). What Backlog #13 buys is **the middle band and the absolute
levels**, which Phase 0 flagged as the load-bearing region.

## Per-opponent breakdown (`--vs --measured`, 40k) — where the blend hides the threat

| Deck | vs Acererak | vs Ur-Dragon | vs H&K | vs Henzie | BLEND | Δ(Acrk−H&K) |
|---|:--:|:--:|:--:|:--:|:--:|:--:|
| Radiation Sickness | 100 | 88 | 74 | 98 | **91** | +25 |
| The Genome Project | 99 | 89 | 72 | 98 | **90** | +27 |
| The Replication Crisis | 99 | 86 | 74 | 96 | **90** | +24 |
| Lightning War | 97 | 78 | 69 | 92 | **85** | +29 |
| The Exile's Return | 98 | 80 | 64 | 95 | **86** | +34 |
| … | | | | | | |
| Croak and Dagger | 87 | 57 | 48 | 78 | **69** | +38 |
| Crystal Sickness | 73 | 31 | 27 | 59 | **50** | +45 |

**The single most important read of the whole exercise: the blend hides H&K.** Every deck's vs-Acererak
column is inflated (his measured K is mostly "never," so we win by default), which drags the BLEND up —
but **H&K is the real stomp threat**, and the H&K column is 20–45 points lower. The huge Δ(Acrk−H&K)
means the matchup swings enormously on *which deck he brings*: against his favourite (slow Acererak)
almost everything wins; against the deck that stomped the table (H&K, median T8 with a real T5-6
god-draw edge) even our S-tier racers sit at 69–74%. **Play to beat H&K; the Acererak column is a
mirage.**

---

## Caveats (load-bearing — read before citing a number)

- **Both sides are UNBLOCKED goldfish ceilings.** Our decap curves race his kill ceilings; neither
  models the other's blockers/interaction. Ur-Dragon's T8 is his *unblocked* combat clock — the pod
  actually blocks dragons (`vs_dragon_lab` owns the defended matchup), so his real K is SLOWER and his
  columns are conservative-for-us (we chose to use it directly). The ABSOLUTE levels are optimistic;
  the ranking and the per-opponent SPREAD are the honest reads.
- **Acererak's slow K is MEMORY-BIAS-FLAGGED.** The v2 all-lines lab falsified the felt "wins T6-7"
  even with every axis on (front edge ~0-1% at T6-7); the residual gap to the felt clock is likely the
  H&K-stomp memory bleeding in, and/or the reconstruction underpowering his real (tighter) list. If his
  real Acererak is a turn or two faster, his 0.40-weight column drops and every BLEND with it.
- **PROXY clocks.** Acererak is a full reconstruction; Ur-Dragon/Henzie are Archidekt exports with
  land fills; H&K is his real 2023 list with a 2-slot banfix. Never citation-grade.
- **Opt-in, not the committed default.** Because of the above, the measured profile is a reality-check
  lens, not the ranking of record. `tier_list.py` still defaults to the (robust-ranking) assumed
  profile; run `--measured` / `pg.set_profile(True)` to see this view.

## Standing ask — the one thing that grades all of this

Log his **actual kill/attempt turn** at the next meetup (pocket scorecard beside `game_log.py quick`).
One real observation per opponent grades the PROXY curve directly — especially Acererak (does the felt
T6-7 hold, or was it the H&K memory?) and Ur-Dragon (how often does he actually close through the pod?).
