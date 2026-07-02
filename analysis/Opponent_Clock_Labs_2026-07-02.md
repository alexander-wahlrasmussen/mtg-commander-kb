# Opponent Clock Labs — Backlog #13 Phase 2 (running doc, started 2026-07-02)

Measured clocks for the archenemy's decks (`opponents/*.txt`, `scripts/opponent_labs/`),
replacing the hand-assumed `pod_gauntlet.K_DIST` ("wins T6-7", mean T6.70). **All PROXY
clocks** — the input lists are Archidekt exports and evidence-tiered reconstructions, never
citation-grade. Cite as `~Tx (PROXY lab 2026-07-02)`.

Why this matters: `analysis/Pod_Clock_Sensitivity_2026-07-02.md` — the tier list's middle
band and ALL absolute P(beat pod) levels are load-bearing on the K_DIST assumption.

---

## 1. Acererak the Archlich (his favorite; seen every meetup) — LAB DONE 2026-07-02

**Lab:** `opp_acererak_lab.py` @40k (clock) / 8k (levers), seed 20260702.
**List:** `acererak-reconstruction-PROXY-20260702.txt` (full reconstruction; evidence tiers
in-file). **Kill shape:** COMBO ASSEMBLY (user-testified infinite: tax-free Acererak recasts
+ Diregraf Colossus token/cast + Altar-class sac-income; damage = Lost Mine Dark Pool laps
or Bontu's Monument per-cast drain).

### P(infinite assembled ≤ T), cum %

| variant | T6 | T7 | T8 | T9 | T10 | T12 | med | never-14 |
|---|---|---|---|---|---|---|---|---|
| LEAN (−Plunderer −Monument) | 0 | 0 | 0 | 1 | 1 | 3 | >T14 | 94% |
| **reconstruction as committed** | 0 | 1 | 2 | 4 | 7 | 17 | >T14 | **70%** |
| FAT (+Semblance Anvil +Cloud Key +2nd Altar) | 1 | 3 | 6 | 12 | 18 | 35 | T14 | 47% |

### Finding — the felt "wins T6-7" is FALSIFIED as an infinite-assembly clock

The 8th hand-estimated kill window this repo has falsified — and the first one that was
**too fast** rather than too optimistic-slow, and the first belonging to the OPPONENT. Under
any plausible enabler count (LEAN→FAT brackets the reconstruction uncertainty), the tight
infinite is a **T12+/never** assembly, not T6-7. The engine is gated on three 1-ofs
(bottleneck census at T14: Colossus 38% · Phyrexian Altar 27% · Plunderer 27%) that two
tutors can't reliably find by T7.

**Interpretations (not mutually exclusive):**
1. The felt T6-7 is the deck's **attrition half** — ToA symmetric drain opener, Dark
   Pool/Monument chips, zombie combat, Gray Merchant/Torment bursts — pressuring/killing a
   player well before the infinite is up. The lab models only the chip components of that
   axis (deliberately; assembly is the K-relevant line).
2. The reconstruction underestimates his mana (Coffers/Crypt Ghast/Dark Ritual omitted
   conservative) — some gap, not five turns of it.
3. Loss-memory bias: "felt T6-7" may partly be the H&K stomp bleeding into the Acererak
   memory.

**Consequence for K_DIST:** the Acererak slot (weight 0.45, the largest) appears
substantially SLOWER than the assumed T6-7 as a *combo* threat. Per the sensitivity sweep's
+1/+2 columns, a slower measured pod *lifts* the roster's middle band (Bumbleflower C→B,
CoS/EBM edge-up). Do NOT rebuild K_DIST from this one lab — H&K/Ur-Dragon/Henzie labs first.

**Kill-on-sight priorities confirmed (bottleneck census):** Diregraf Colossus > Phyrexian
Altar > Pitiless Plunderer. Single-point-of-failure engine — removal on the token source
hurts him disproportionately. ETB hate (Elesh Norn MoM / Torpor Orb class) still switches
off bounce + venture entirely.

**Next refinement:** observe his actual combo turn at the next meetup (pocket-scorecard
note alongside `game_log.py quick`) — one real observation grades the PROXY directly.

---

## 2. Hidetsugu & Kairi — PENDING (real 2023 list + 2-slot ban-fix variant)
## 3. The Ur-Dragon — PENDING (72/100 real + lands PROXY fill)
## 4. Henzie — PENDING (67/100 real + lands PROXY fill)

Then: harvest the measured per-opponent curves → rebuild `K_DIST` + the `OPPONENTS` blend
weights from the observed rotation (Ur-Dragon + Acererak every meetup ≫ H&K occasional ≫
Henzie rare) → re-run `pod_clock_sensitivity.py` with measured profiles.
