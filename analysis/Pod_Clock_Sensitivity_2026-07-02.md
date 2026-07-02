# Pod-Clock Sensitivity — Is the Tier List Robust to the Hand-Assumed K_DIST? (2026-07-02)

**Tool:** `scripts/pod_clock_sensitivity.py` @ 40,000 trials, seed 20260615 (reproduce:
`python scripts/pod_clock_sensitivity.py`). **Phase 0 of "measure the pod."**

## The question

Every ANTI-POD number in the tower — `pod_gauntlet`, the matchup matrix, the v2 tier list's
largest axis (weight 0.45) — races the opponent profile `K_DIST` in `pod_gauntlet.py`:

```
K_DIST = {5: 0.10, 6: 0.35, 7: 0.35, 8: 0.15, 9: 0.05}   # "wins T6-7", mean T6.70
```

That distribution is **hand-assumed, never lab-measured**. The repo's deepest learning is
that hand-estimated kill windows were falsified 7-of-8 times when labbed, all optimistic
(`project_framework_clock_gap`) — we applied that discipline to all 17 of our own decks and
never to the four decks everything races against. Before paying for the fix (reconstruct +
clock-lab the pod's actual decks, Phases 1–2), this sweep measures whether the assumption
**matters**: shift the profile, watch the tier verdicts.

## Method (attribution by construction)

| | |
|---|---|
| **Swept** | `K_DIST` shifted by δ ∈ {−2…+2} whole turns (mean T4.70 → T8.70), plus the two preset *shapes* `pod_gauntlet` already carries (`--pod-fast` T6.34 / `--pod-slow` T7.24). |
| **Moves** | Only the ANTI-POD axis — `pg.simulate_vs` over the OPPONENTS blend, the exact model `tier_list.antipod_blend` runs, with the kdist injected. |
| **Fixed** | INTER / SELF raw values at the `compute_rows` baseline (they race the roster's own table clocks; the pod profile never enters them). CC is context-only in v2. |
| **Redone** | Min-max norm + COMP + tier cut per sweep point (tier_list math reused, not copied — parity pinned by `tests/test_pod_clock_sensitivity.py`). |

Min-max normalisation **cancels any uniform anti-pod shift** — only *differential* movement
(a fortress gaining more from a slower pod than a racer does) can move a tier. So a tier flip
here is real ranking sensitivity, not "everything got better against a slow pod."

**MC-noise yardstick:** the recomputed δ=0 column vs the live `compute_rows` baseline =
**0.4pp max abs gap** — tier letters are trustworthy at this trial count.

## Results

### ANTI-POD % by profile (raw axis)

| deck | −2 (T4.7) | −1 (T5.7) | fast (T6.3) | base (T6.7) | slow (T7.2) | +1 (T7.7) | +2 (T8.7) |
|---|---|---|---|---|---|---|---|
| The Genome Project | 15 | 35 | 51 | 61 | 73 | 83 | 94 |
| Lightning War | 31 | 44 | 53 | 57 | 64 | 69 | 79 |
| Radiation Sickness | 24 | 41 | 55 | 63 | 73 | 82 | 92 |
| The Replication Crisis | 29 | 45 | 58 | 64 | 73 | 80 | 89 |
| Zero-Sum Game | 12 | 22 | 29 | 33 | 39 | 44 | 53 |
| Croak and Dagger | 11 | 20 | 28 | 33 | 40 | 46 | 58 |
| The Exile's Return | 14 | 28 | 41 | 49 | 60 | 69 | 84 |
| Forced Liquidation | 16 | 26 | 33 | 38 | 46 | 53 | 66 |
| Lorehold Spirits | 9 | 21 | 32 | 39 | 50 | 58 | 74 |
| Ms. Bumbleflower | 13 | 27 | 39 | 47 | 60 | 71 | 88 |
| Curse of the Scarab | 11 | 22 | 31 | 37 | 47 | 55 | 71 |
| Earthbend the Meta | 13 | 25 | 35 | 42 | 53 | 62 | 78 |
| The Dark Lord's Army | 6 | 14 | 21 | 26 | 34 | 41 | 56 |
| The Grand Design | 14 | 23 | 31 | 36 | 45 | 52 | 68 |
| Eldrazi Stampede Chaos | 5 | 12 | 20 | 26 | 36 | 44 | 63 |
| Diminishing Returns | 2 | 7 | 12 | 17 | 26 | 35 | 55 |
| Crystal Sickness | 1 | 3 | 6 | 9 | 14 | 18 | 30 |

### TIER by profile (v2 composite, INTER/SELF fixed)

| deck | live | −2 | −1 | fast | base | slow | +1 | +2 | verdict |
|---|---|---|---|---|---|---|---|---|---|
| The Genome Project | S | S | S | S | S | S | S | S | ROBUST |
| Lightning War | S | S | S | S | S | S | S | S | ROBUST |
| Radiation Sickness | A | A | A | A | A | A | A | A | ROBUST |
| The Replication Crisis | A | A | A | A | A | A | A | A | ROBUST |
| Zero-Sum Game | A | A | A | A | A | A | A | A | ROBUST |
| Croak and Dagger | A | A | A | A | A | A | A | A | ROBUST |
| The Exile's Return | A | **B** | **B** | A | A | A | A | A | **SENSITIVE** |
| Forced Liquidation | B | B | B | B | B | B | B | B | ROBUST |
| Lorehold Spirits | B | **C** | **C** | **C** | B | B | B | B | **SENSITIVE** |
| Ms. Bumbleflower | C | **D** | C | C | C | C | **B** | **B** | **SENSITIVE** |
| Curse of the Scarab | C | C | C | C | C | C | C | **B** | EDGE |
| Earthbend the Meta | C | **D** | C | C | C | C | C | **B** | EDGE |
| The Dark Lord's Army | C | **D** | **D** | C | C | C | C | C | **SENSITIVE** |
| The Grand Design | D | D | D | D | D | D | D | D | ROBUST |
| Eldrazi Stampede Chaos | D | D | D | D | D | D | D | D | ROBUST |
| Diminishing Returns | D | D | D | D | D | D | D | D | ROBUST |
| Crystal Sickness | D | D | D | D | D | D | D | D | ROBUST |

**Rank stability** (Spearman ρ of swept COMP vs live baseline COMP): 0.975 at −2, ≥0.983
everywhere else. **11 ROBUST · 2 EDGE · 4 SENSITIVE of 17.**

## Findings

1. **The S-tier picks and the D floor survive the assumption.** Genome/Lightning War stay S
   and GD/Eldrazi/Diminishing/Crystal stay D across the entire T4.7→T8.7 band. "What do I
   bring to beat the pod" is robust at the top; nothing at the bottom is rescued by any
   plausible pod clock. The four A-core decks (Radiation, Replication, Zero-Sum, Croak) are
   robust too.

2. **The middle band is where the hand-assumed clock is load-bearing.**
   - **The Exile's Return's A-tier is conditional on the pod NOT being faster than assumed**
     — at −1 turn (mean T5.7, inside the plausible band) it drops to B. Asymmetric: a slower
     pod never demotes it.
   - **Lorehold's B is knife-edge**: it flips to C even under the alternative *fast shape* of
     "wins T6-7" (mean T6.34 — 0.36 turns faster than base). Its COMP sits almost exactly on
     the B/C cut.
   - **Ms. Bumbleflower is underrated if the pod is slower** (+1/+2 → B): its decap CDF is
     steep just past the assumed window (39% T7 → 82% T8), so one turn of pod slack converts
     directly into wins.
   - **Dark Lord's Army drops to D if the pod is faster** (−1/−2) — the MID-tempo
     opponent-driven engine needs the game to reach its window.

3. **Absolute P(beat pod) levels swing enormously even where ranking is stable.** Genome
   spans 15% → 94% across the sweep; the roster-median swing is ~±15pp per assumed turn.
   The *ranking* barely moves (ρ ≥ 0.975) because most decks shift together — but any
   statement of the form "deck X beats the pod ~60% of the time" inherits the full
   uncertainty of the unmeasured constant. The tier letters are robust; the **absolute
   numbers are not**.

4. **The PURE RACE closed form** (zero noise) shows the same shape: the sweep's differential
   signal comes from CDF steepness in the K-window, exactly as the normalisation argument
   predicts.

## Verdict → Phase 1/2

**Justified, and now targeted.** Reconstructing + clock-labbing the pod's actual decks
(Phase 1: elicit observed cards, build PROXY lists; Phase 2: lab them on the same harness)
would settle:

- whether Exile's Return is really an A deck (pod faster vs. as-assumed),
- the whole B/C band ordering (Lorehold / Bumbleflower / CoS / EBM / DLA),
- the absolute P(beat pod) levels that every "bring this deck" call quietly leans on,
- the *variance/tail shape* of the pod clock, which no point-sweep can supply.

What it would **not** change: the S-tier picks and the D floor — those verdicts are already
robust and stay citable under any plausible pod clock.

## Caveats

- Disruption rows are measured on K∈{6,7} and clamped outside (`pod_gauntlet.disruption`):
  the sweep is mildly **compressed** at both ends (measured sensitivity is a floor). MEASURED
  row deltas are ≤4pp — second-order vs the K shift itself.
- All clock curves remain **unblocked goldfish ceilings**; every caveat of the anti-pod
  oracle is inherited. This sweep varies the *opponent* assumption only.
- INTER/SELF were held fixed **by design** (the pod profile never enters them), so composite
  deltas are attributable to K_DIST by construction — but that also means this sweep cannot
  see second-order effects (e.g. a faster pod changing which of *our* decks survive to grind).
- Lorehold's flip at T6.34 shows some letters are knife-edge to *any* perturbation — tier
  boundaries are cuts on a continuous composite; read neighbouring letters as "same band"
  when the COMP gap is small.

## Side-observation (housekeeping, separate from this sweep)

The committed `analysis/Definitive_Tier_List_2026-06-28.md` table is **stale vs HEAD**: it
predates the Croak and Dagger promotion (2026-07-01: live A, doc still D/>T14) and the
2026-07-02 lab-audit fixes (live FL B, doc A). The live `tier_list.py` was used as this
sweep's baseline anchor. A doc + dashboard rebake is pending.
