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

### ⚠️ CHALLENGE (2026-07-02, user: "his version is stronger" — upheld; v1 is a FLOOR)

The v1 lab measures ONLY the tight net-0 infinite. That is the same single-line distortion
that mis-tiered Lightning War (Backlog #11: race-only clock, combo invisible) — mirrored.
Four kill axes are invisible in v1, and the "conservative" mana omissions are NOT
second-order for this deck:

1. **Big-mana drain turns** — Coffers/Urborg/Crypt Ghast/Dark Ritual were omitted; with
   Bontu's Monument (drains each opponent per cast), ~12 reduced casts off big mana is
   table −12/turn with NO Colossus/Altar/net-0 required. The infinite is the limit case,
   not the requirement.
2. **X-bursts** — Torment of Hailfire / Gray Merchant off the same mana: real T8-9 decap.
3. **Shepherd of Rot** — table −(zombie count) per tap once tokens accumulate.
4. **Gravecrawler lever** — excluded as unobserved, but Gravecrawler+Colossus+Phyrexian
   Altar is a 3-piece infinite needing zero reducers, and "repeat casting & saccing" is
   what that loop looks like from across the table. Ask / watch next meetup.

**Do not cite v1's nv70% as "Acererak is slow" — cite it as "the tight infinite alone is
slow."** Backlog #13 Phase 2.5 specs the v2 all-lines best-line lab (race attrition +
bursts + infinite on ONE correlated game, the #11 MVP rule). Expected: the front edge pulls
in toward the felt T6-7. The bottleneck census (Colossus > Altar > Plunderer) stays valid
as the kill-on-sight list for the infinite line specifically.

### v2 RESULT — all-lines best-line lab BUILT + RUN 2026-07-02 (challenge answered)

**Lab:** `opp_acererak_lab.py --mode bestline` (and `--mode lines` for the per-axis
decomposition) @40k, seed 20260702. `AllLines` inherits v1's infinite detection and adds the
four challenged axes, all raced on ONE correlated game (min over lines on the same draws —
the #11 MVP rule, never independent CDFs). Every card `card_lookup`-verified this session:
Bontu's Monument drains 1 per **creature** cast (Acererak recasts qualify; black creatures
−{1}); Cabal Coffers `{2}: +B/Swamp` × Urborg (all lands are Swamps) × Crypt Ghast (+B/Swamp
tapped) is the modelled big-mana engine (Dark Ritual burst; Black Market + combat token-makers
omitted conservative); Torment forces 3/iteration UNLESS the opponent sacs/discards (a
resource BUFFER they exhaust first); Shepherd of Rot taps for −(zombies) to each; Gray Merchant
ETB = devotion (tokens add 0 devotion — verified). Army of the Damned (+13 zombies) / Endless
Ranks / Bastion are now cast (v1's creature-only loop skipped them, understating Shepherd).

| line (kill = decap = table, cum %) | T7 | T8 | T9 | T10 | T12 | med | never-14 |
|---|---|---|---|---|---|---|---|
| infinite only (≈ v1) | 0 | 1 | 2 | 3 | 8 | >T14 | 84% |
| Shepherd only (strongest single axis) | 0 | 0 | 1 | 4 | 13 | >T14 | 77% |
| Monument only | 0 | 0 | 0 | 1 | 4 | >T14 | 89% |
| Gray Merchant only / Torment only | 0 | 0 | 0 | 0 | 0 | >T14 | 100 / 99% |
| attrition (Monument+Shepherd+Gary+venture) | 0 | 1 | 3 | 7 | 21 | >T14 | 65% |
| **ALL (best-line)** @40k | **0** | **1** | **4** | **9** | **25** | **>T14** | **59%** |
| ALL + Gravecrawler lever | 1 | 2 | 6 | 11 | 27 | >T14 | 56% |

**Finding — the challenge is UPHELD in DIRECTION but the felt T6-7 is STILL falsified as a
kill clock.** v2 confirms his deck is stronger than the tight infinite alone (never-in-14
70% → **59%**, +Gravecrawler lever → 56%; a real T10-12 mass appears, 9→25%). But the front
edge at T6-7 stays **~0-1%** even with every axis + the lever on — Acererak is a genuinely
SLOW combo-drain, not a T6-7 kill. Diagnostic (3k): by T12 the single-copy big-mana engines
are each ~25% present and zombies avg ~23, yet symmetric drains reach an opponent for only
~12.5 of the 40 needed — the deck needs the *infinite* (T12+/never) or a Shepherd/Army god-draw
to actually close. So the earlier §1 interpretations resolve: the felt "wins T6-7" is **memory
bias** (the H&K stomp bleeding into the Acererak memory) and/or the reconstruction underpowers
his real (tighter, more-redundant) list — **not** a live T6-7 kill. Shepherd of Rot is the
strongest single line (kill-on-sight #4 after the census trio); Gary/Torment are pure
chip/burst that only bite combined. **One real observation settles the residual gap** — log
his actual combo/kill turn next meetup.

**Consequence for K_DIST (Phase 3):** Acererak (weight 0.45, the largest) has a measured K far
SLOWER than the assumed T6-7. Per the sensitivity sweep's +1/+2 columns, a slower measured pod
LIFTS the roster's middle band. This v2 curve is the Acererak per-opponent kdist that feeds the
Phase-3 rebuild. Bottleneck census unchanged (Colossus 46% · Phyrexian Altar 29% · Plunderer
20% over the trials the infinite never assembled — the OTHER lines may still have closed).
Cite as `~ slow / infinite T12+/never (v2 all-lines PROXY lab 2026-07-02)`, memory-bias-flagged.

---

## 2. Hidetsugu & Kairi ("stomped us" last meetup) — LAB DONE 2026-07-02

**Lab:** `opp_hk_lab.py` @40k, seed 20260702. **List:**
`you-get-a-clone-BANFIX-PROXY-20260702.txt` — his REAL 2023 list (103 cards verbatim) with
the two banned cards substituted (Mana Crypt→Mana Vault, Jeweled Lotus→Coalition Relic, our
guess). Lowest-uncertainty opponent clock (2 guessed slots vs Acererak's 100).

**Kill shape:** CLONE LOOP — clone the commander → legend rule kills the copy → death
trigger drains the FOCUS player for the MV of a self-stacked bomb (his ETB draws 3 and puts
2 back on top; bombs MV 7-11) + free-casts it (Time Stretch/Trespass/Nexus/Beacon/
Expropriate = extra turns *inside the same wall-clock turn*). Drivnod doubles every trigger;
kicked Rite of Replication = five triggers at once; Saw in Half = two + commander survives.

### P(kill ≤ T), cum % @40k

| clock | T4 | T5 | T6 | T7 | T8 | T9 | T10 | T12 | med | never-14 |
|---|---|---|---|---|---|---|---|---|---|---|
| **decap** (one player, 40) | 4 | 11 | 27 | 46 | 60 | 70 | 78 | 87 | **T8** | 8% |
| table (all three) | 1 | 3 | 8 | 18 | 28 | 38 | 45 | 56 | T11 | 37% |

### Finding — the real racer of his stable, ~1 turn slower than assumed, real god-draw edge

The decap curve is the K that matters (his kill is target-one-player — exactly the user's
"a lot of damage to a player"). Median T8 vs the assumed T6-7 mean of 6.70, but with a
genuine T5-6 front edge (11→27%) — this deck CAN produce the assumed clock, it just isn't
the median. Table kill trails 3 turns (drains are single-target) — after the decap he needs
another ~2 stacked bombs per remaining player. OMITTED (conservative): Sensei's Top
top-control (he owns it — would lift the curve), Strionic Resonator, the big draw spells,
Reanimate rebuys. OPTIMISTIC: no interaction, Mana Vault untap tax ignored.

**Kill-on-sight / play-around:** the loop needs the ORIGINAL H&K on board — removal in
response to the clone's ETB (before the legend-rule death resolves the stack) still eats a
death trigger; the real leverage is killing H&K BEFORE a clone turn (he pays 5+tax to
return) and holding up graveyard-irrelevant, top-of-library-irrelevant interaction. His
whole engine is UB: no Grand Abolisher possible; a counter-war on the CLONE (2-4 mana
spells) is far cheaper than on the bombs.
## 3. The Ur-Dragon (seen every meetup) — LAB DONE 2026-07-02

**Lab:** `opp_urdragon_lab.py` @40k, seed 20260702. **List:**
`dragon-dragon-dragon-PROXY-20260702.txt` (his real 72 spells, 2025-06 + our 28-land fill).
**Kill shape:** go-tall dragon combat + a real ETB-burn sub-axis (Tempest/Scourge/Terror,
multiplied by Miirym/Lathliss tokens, DOUBLED by Twinflame Tyrant and Neriv — stack ×4) +
Dracogenesis free-casts + **Call the Spirit Dragons as a literal alternate wincon** (five
colours countered at upkeep = win; modelled as 5+ dragons surviving an upkeep).

| clock @40k | T5 | T6 | T7 | T8 | T9 | T10 | T12 | med | never-14 |
|---|---|---|---|---|---|---|---|---|---|
| **decap** | 1 | 9 | 28 | 53 | 73 | 85 | 96 | **T8** | 1% |
| table | 0 | 0 | 2 | 8 | 22 | 42 | 77 | T11 | 6% |

**Finding:** decap median T8 UNBLOCKED — same median as H&K but with a slower front edge
(T6 9% vs 27%) and far higher reliability (never 1% vs 8%). CAVEAT (biggest of the four):
this is the *unblocked* ceiling — the pod actually blocks dragons; `vs_dragon_lab` owns the
defended matchup. Read this curve as his pressure schedule, not P(win). The burn sub-axis
(Tempest/Scourge/Terror ×doublers) ignores blockers for real, though — with Twinflame or
Neriv out, dragon ETBs alone are lethal-adjacent. OMITTED (conservative): treasures, extra
combats, Dragonhawk, Betor, riot counters, Imoti cascade.

## 4. Henzie "Major tool" (seen once) — LAB DONE 2026-07-02

**Lab:** `opp_henzie_lab.py` @40k, seed 20260702. **List:**
`major-tool-PROXY-20260702.txt` (his complete 66-spell suite, 2023-02 + our 33-land fill).
**Kill shape:** blitz value — MV4+ fatties at mana cost with haste-die-draw, Warstorm/
Stalking Vengeance burn riders, Kokusho/Junji drains, Chainer/Victimize/Living Death
recursion. Lean model (lightest rotation weight); Etali/Ilharg/Pod/Skullclamp omitted.

| clock @40k | T7 | T8 | T9 | T10 | T12 | med | never-14 |
|---|---|---|---|---|---|---|---|
| **decap** | 3 | 13 | 25 | 38 | 61 | **T11** | 22% |
| table | 0 | 0 | 0 | 1 | 10 | >T14 | 71% |

**Finding:** a grinder, not a racer — decap T11 median even unblocked. The observed loss to
it was attrition, not a clock. Lowest-priority threat in K terms.

---

## The measured picture (all four labs, PROXY)

| Opponent | observed freq | assumed | measured decap (med · T6 · T7) | shape |
|---|---|---|---|---|
| Acererak | every meetup | "wins T6-7" | **all-lines >T14** · T7 ~0 · T10 9% (nv 59%; v1 infinite-only 70%) | combo-drain, SLOW |
| Ur-Dragon | every meetup | (fair deck) | **T8** · 9 · 28 (unblocked ceiling) | combat+burn, reliable |
| H&K | occasional, stomps | "wins T6-7" | **T8** · 27 · 46 | clone-drain racer, real T5-6 edge |
| Henzie | once | — | T11 · 0 · 3 | value grinder |

**The assumed K_DIST ({T5:10 T6:35 T7:35 T8:15 T9:5}, mean T6.70) is ~1-1.5 turns too
fast** as a description of his stable, and its Abolisher framing is wrong for BOTH current
combo decks (Acererak mono-B, H&K UB — neither can cast the white Grand Abolisher; only
the 5C shells could, and the Ur-Dragon list has none). The felt "wins T6-7 behind
Abolisher" appears to be an H&K-at-its-best memory generalized to the whole stable.

**Phase 2.5 DONE 2026-07-02** — Acererak v2 all-lines lab built + run (§1 v2 RESULT): the
challenge is upheld in direction (nv 70%→59%) but the felt T6-7 is still falsified as a kill
clock; the residual gap is memory bias / reconstruction underpower. The v2 curve is Acererak's
per-opponent kdist for Phase 3.

**Phase 3 DONE 2026-07-02** — the K_DIST rebuild shipped: all four measured curves + observed-
rotation weights (Acererak .40 / Ur-Dragon .30 / H&K .20 / Henzie .10, user-confirmed) + the
no-Abolisher disruption are folded into `pod_gauntlet` as the OPT-IN `set_profile(True)` /
`--measured` / `POD_MEASURED_PROFILE=1` profile (default byte-identical, null-reduction guarded by
`tests/test_pod_measured_profile.py`). Re-run at the measured profile: **ρ=0.961 vs the assumed
baseline, 7 of 17 tiers move** — the middle band lifts (FL B→A, Bumbleflower/CoS/Earthbend C→B,
Grand Design/Eldrazi D→C), Zero-Sum A→B, apex + D-floor unchanged. Writeup:
`analysis/Pod_Measured_Profile_2026-07-02.md`. **The blend hides H&K** — the real stomp threat sits
20–45pp below the Acererak column; play to beat H&K. Refinement standing ask: log his actual
kill/attempt turns at the next meetup (pocket scorecard) — real observations grade all four PROXY
clocks, especially Acererak (felt T6-7 vs the lab's slow K) and Ur-Dragon (closes through the pod?).
