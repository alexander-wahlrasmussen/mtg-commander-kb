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

> **Correction (2026-07-02, user pushback "his Acererak is NOT slow"):** the Acererak curve below
> is the COMBO-TUNED **REV 3** reconstruction. The first cut used a deliberately mid-power list and
> measured Acererak as slow (>T14); `find_combos` showed that list was one card short of a dozen
> aristocrats infinites, so it was re-tuned to a real combo deck (18 complete CSB infinites) and
> re-labbed to **median T12, nv 28%, real T6-8 front edge** — a FLOOR. See
> `Opponent_Clock_Labs_2026-07-02.md` §1 "v3 CORRECTION". This shifted Acererak's column down but
> left every Phase-3 tier conclusion below UNCHANGED (ρ moved 0.961→0.973, same 7 moves).

| Opponent | weight | measured K (decap median) | disruption_a / answer | source |
|---|---:|---|---|---|
| Acererak (mono-B COMBO) | **0.40** | **T12** (REV3 aristocrats sac-loop + recast; nv28%, real T6-8 front edge; a FLOOR) | 0.05 / 0.10 | `opp_acererak_lab --mode bestline` |
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
| The Genome Project | S | S | 61 | 89 | |
| Lightning War | S | S | 57 | 83 | |
| Radiation Sickness | A | A | 63 | 89 | |
| The Replication Crisis | A | A | 64 | 88 | |
| Zero-Sum Game | A | **B** | 33 | 58 | **A→B** |
| Croak and Dagger | A | A | 32 | 66 | |
| The Exile's Return | A | A | 49 | 84 | |
| Forced Liquidation | B | **A** | 38 | 73 | **B→A** |
| Lorehold Spirits | B | B | 39 | 78 | |
| Ms. Bumbleflower | C | **B** | 48 | 85 | **C→B** |
| Curse of the Scarab | C | **B** | 37 | 76 | **C→B** |
| Earthbend the Meta | C | **B** | 42 | 80 | **C→B** |
| The Dark Lord's Army | C | C | 26 | 66 | |
| The Grand Design | D | **C** | 36 | 74 | **D→C** |
| Eldrazi Stampede Chaos | D | **C** | 26 | 71 | **D→C** |
| Diminishing Returns | D | D | 17 | 66 | |
| Crystal Sickness | D | D | 9 | 45 | |

**Rank stability: Spearman ρ = 0.973 (n=17). 7 of 17 tiers move.** The apex (Genome/LW S;
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
| Radiation Sickness | 96 | 88 | 74 | 98 | **89** | +22 |
| The Genome Project | 95 | 89 | 72 | 98 | **89** | +23 |
| The Replication Crisis | 95 | 86 | 74 | 96 | **88** | +20 |
| Lightning War | 92 | 78 | 69 | 92 | **83** | +23 |
| The Exile's Return | 93 | 80 | 64 | 95 | **84** | +29 |
| … | | | | | | |
| Croak and Dagger | 79 | 57 | 49 | 78 | **66** | +30 |
| Crystal Sickness | 61 | 31 | 28 | 59 | **45** | +33 |

**The single most important read of the whole exercise: the blend hides H&K.** Even with Acererak
corrected to a real combo deck (T12 median), our race decks still out-decap him (T7-9), so the
vs-Acererak column stays high (79–96) and drags the BLEND up — but **H&K is the real stomp threat**,
and the H&K column is 20–33 points lower. The Δ(Acrk−H&K) means the matchup swings enormously on
*which deck he brings*: against his favourite (Acererak, whom we usually out-race)
almost everything wins; against the deck that stomped the table (H&K, median T8 with a real T5-6
god-draw edge) even our S-tier racers sit at 69–74%. **Play to beat H&K** — and don't over-trust
the Acererak column either: it's high only because our *unblocked* decap beats his T12 *floor*;
his real, mulligan-aware, protected combo turn is faster (see the FLOOR caveat).

---

## Caveats (load-bearing — read before citing a number)

- **Both sides are UNBLOCKED goldfish ceilings.** Our decap curves race his kill ceilings; neither
  models the other's blockers/interaction. Ur-Dragon's T8 is his *unblocked* combat clock — the pod
  actually blocks dragons (`vs_dragon_lab` owns the defended matchup), so his real K is SLOWER and his
  columns are conservative-for-us (we chose to use it directly). The ABSOLUTE levels are optimistic;
  the ranking and the per-opponent SPREAD are the honest reads.
- **Acererak's T12 clock is a FLOOR (corrected 2026-07-02 on user pushback).** The first cut called
  him slow; that was the mid-power reconstruction, not his deck (CSB: one card short of a dozen
  infinites). The re-tuned REV3 combo list clocks median T12 / real T6-8 front edge — but the
  opponent goldfish keeps on land count, not combo pieces, and we deliberately proxy less fast mana
  than a real cEDH-adjacent list. So his true clock is FASTER than T12; his 0.40-weight Acererak
  column is optimistic-for-us and every BLEND with it. This is the residual the standing ask grades.
- **PROXY clocks.** Acererak is a full reconstruction; Ur-Dragon/Henzie are Archidekt exports with
  land fills; H&K is his real 2023 list with a 2-slot banfix. Never citation-grade.
- **Opt-in, not the committed default.** Because of the above, the measured profile is a reality-check
  lens, not the ranking of record. `tier_list.py` still defaults to the (robust-ranking) assumed
  profile; run `--measured` / `pg.set_profile(True)` to see this view.

## Standing ask — the one thing that grades all of this

Log his **actual kill/attempt turn** at the next meetup (pocket scorecard beside `game_log.py quick`).
One real observation per opponent grades the PROXY curve directly — especially Acererak (is his real
combo turn the ~T6-8 front edge or the T12 floor?) and Ur-Dragon (how often does he actually close
through the pod?). Also confirm his Acererak recursion package (Gravecrawler / Reassembling Skeleton /
Mikaeus?) — it decides how far below the T12 floor his real clock sits.
