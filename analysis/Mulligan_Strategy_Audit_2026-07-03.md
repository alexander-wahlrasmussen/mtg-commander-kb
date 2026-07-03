# Mulligan Strategy Audit — per-deck keep-specs + the mulligan script (2026-07-03)

**Trigger:** user push-back on the smoothness sweep's H1 conclusion — *"I am not convinced
that we have nailed the mulligan strategy which would allow us to conclude it has no
effect."* This audit checks, per deck: how the deck actually wins, what "engine online"
means, and whether the modeled mulligan (`deck_sim.opening_hand` + `keep_hand` +
`analysis/keep_specs.json`) expresses a real keep strategy for that plan.

**Verdict up front.** The push-back is justified on three counts, and the headline still
survives all three:

1. **The sweep's H1 lever had almost no contrast on 9 of 17 decks** — their "plan" keep
   degenerates to *land band + any ≤3-CMC nonland* (a generic smart-keep), so land-vs-plan
   disagree on only ~5% of hands. "No effect" there was guaranteed by construction, not
   discovered.
2. **One deck (Croak) ran the sweep on a stale spec** — mulling toward the superseded
   Torment-grind plan. Fixed (regenerated + a tier-1 freshness regression test); re-run
   changes nothing at the roster level.
3. **Dead-turns is the wrong outcome for the mulligan's job.** The mulligan optimises
   *plan assembly*, not smoothness — on the decks whose keeps are genuinely sharp, the plan
   keep *costs* smoothness (dMull −0.03…−0.08), exactly as it should. The right outcome
   (front-edge kill/assembly probability) was measured 2026-06-16 and again here on Croak:
   the effect is real but small (+1pp typical, +6pp best case, −9pp when the spec digs for
   the wrong plan).

So the corrected conclusion is **not** "the mulligan has no effect." It is: *within the
modeled mulligan (two free redraws, binary keep), the keep rule moves goldfish clocks by
roughly ±1pp except where the deck is genuinely finding-gated (up to +6pp) or the spec is
wrong (−9pp) — and the model cannot express the aggressive end of real mulligan strategy
at all (mull-to-5, London bottoming). Composition (H2) dominating smoothness stands.*

Instruments: `scripts/mulligan_audit.py` (new — keep operating-room diagnostics),
`scripts/smoothness_sweep.py` re-run, `scripts/glarb_inevitable_lab.py` A/B, plus a
Summary + clock-lab vs keep-spec fidelity read of all 17 decks.

---

## 1. The mulligan script as actually modeled

`deck_sim.opening_hand` (deck_sim.py:319): draw 7 → if `keep_hand` fails, reshuffle and
draw a **fresh 7**, at most **twice** → keep whatever the third hand is. Properties that
bound every mulligan result we have ever produced:

| # | Property | Consequence |
|---|---|---|
| M1 | Mulligans are **free** (always 7 cards back, no London bottoming) | digging has no modeled cost → positive keep effects are upper bounds |
| M2 | **Cap of 2** mulls, then the hand is kept even if it fails the predicate | aggressive strategy space (mull-to-5 for the combo) is unrepresentable; on sharp-keep decks 8–24% of games start on a hand the strategy itself says to ship ("stuck") |
| M3 | Keep is **binary** — any marginal pass keeps | no hand ranking, no "keep 7 vs positive redraw EV" decision, no bottoming choice |
| M4 | **No colour check** | a 3-land hand producing none of the deck's colours passes |
| M5 | The axes read only some buckets | `key_cards`/`tutors`/`selection` are consulted **only by a FINDING axis**; `ramp` only by MANA and BOARD-reach. On the 10 decks with no FINDING axis, the hand-picked kill pieces never influence a single keep decision |
| M6 | BOARD's commander-reach clause is `lands ≥ cmdr_cmc − 2 OR has_ramp` | with `min_lands = 2`, any commander of CMC ≤ 4 makes the clause **vacuously true** — BOARD collapses to "band + any ≤3-CMC nonland" |

M6 is the big one: it silently degrades the plan keep to the generic smart-keep (already
known to move 0/16 medians) on **9 decks** — Genome, Radiation, Replication, Lorehold,
Lightning War, Bumbleflower, Exile's (CMC 3), Crystal (CMC 2), and Diminishing's
`also:[BOARD]` fallback. Only Curse (CMC 5) and Dark Lord's (CMC 6) have a BOARD clause
that bites.

## 2. Operating room — how much the H1 lever could even measure

`python scripts/mulligan_audit.py` (10k first-7s/deck; ship>keep = land-keep keeps it,
plan-keep mulls — the plan lever's entire room; stuck = still failing after both free
mulls; why-kept = which clause admitted the kept hands):

```
deck                  axes              land%  plan%  ship>  mull2  stuck  why-kept
Croak and Dagger      FINDING+MANA       82.5   56.5   25.9   18.6    7.5  ramp:71 tutor:33 key:25
Crystal Sickness      BOARD              68.2   65.8    2.4   11.7    4.1  board(trivial):100
Curse of the Scarab   BOARD              78.2   62.0   16.2   13.8    5.0  board:100
Diminishing Returns   FINDING+BOARD      79.2   74.1    5.2    6.9    1.8  board(trivial):100 key:13
Earthbend the Meta    MANA               75.9   37.5   38.4   39.3   24.3  ramp:100
Eldrazi Stampede      MANA(hiC)          79.7   65.6   14.2   11.3    3.9  ramp:85 hiC-4land:15
Forced Liquidation    FINDING            79.2   39.4   39.8   38.6   23.2  2xsel:55 tutor:38 key:35
Lightning War         BOARD              78.8   73.8    5.0    6.8    1.8  board(trivial):100
Lorehold Spirits      BOARD+FINDING      80.1   73.8    6.3    7.2    1.8  board(trivial):99
Radiation Sickness    BOARD+FINDING      77.6   72.7    5.0    8.0    2.3  board(trivial):100
The Dark Lord's Army  BOARD              79.4   44.3   35.1   30.6   16.1  board:100
The Exile's Return    BOARD              80.5   74.0    6.5    7.0    1.9  board(trivial):100
The Genome Project    BOARD              80.2   73.7    6.5    6.9    1.8  board(trivial):100
The Grand Design      MANA(hiC)          82.9   55.4   27.5   19.2    8.3  ramp:71 hiC-4land:29
The Replication Cr.   BOARD+FINDING      78.5   73.6    4.9    7.3    2.0  board(trivial):100
Ms. Bumbleflower      BOARD              82.3   76.2    6.1    6.2    1.6  board(trivial):100
Zero-Sum Game         FINDING            78.8   40.5   38.3   35.4   20.8  tutor:80 key:24
```

Two regimes:

- **Degenerate (9 decks, `board(trivial)`):** ~5% disagreement room. The sweep's land→plan
  contrast was near-null by construction. Their dMull ≈ +0.06 in the sweep is the *generic
  early-play* smoothness bonus, not plan awareness.
- **Sharp (Earthbend, Forced Liquidation, Zero-Sum, Dark Lord's, Grand Design, Croak,
  Curse, Eldrazi):** 14–40% room, real mull pressure — and 4–24% of games start **stuck**
  on a hand the strategy says to ship. This is exactly where a real pilot would mull to
  5–6 with London bottoming, which the model cannot express (M1/M2).

## 3. The stale-spec incident (found + fixed)

`analysis/keep_specs.json` was last regenerated **2026-06-28**; the registry row for Croak
changed **2026-07-01** (combo promotion: MANA/Torment → FINDING+MANA / Top+Citadel+
Aetherflux). The 2026-07-03 sweep therefore ran Croak's "plan keep" against the
superseded grind plan. Fixes:

- Regenerated (`keep_spec.py --write`): Croak judgment + buckets now current; incidental
  drift picked up (Replication +imperial recruiter tutor; DLA −sensei's top).
- **Regression guard:** `tests/test_deck_registry.py::test_keep_specs_json_judgment_fields_current`
  (tier-1, no oracle data) — editing a registry judgment row without re-running
  `keep_spec.py --write` now fails the 3-second gate.

## 4. Sweep re-run (fresh specs) — headline unchanged, reading sharpened

8000 trials/cell, paced: **H1 +0.022 / H2 +0.302 dead turns removed; interaction +0.006**
(was +0.020 / +0.301 / +0.007). Croak's own dMull is +0.05. So the staleness did not
drive the H2-dominance result — that conclusion is robust.

The per-deck pattern is the informative part: every deck with a **sharp** keep shows
dMull ≤ 0 or ≈ 0 (DLA −0.08, GD −0.08, EBM −0.04, FL −0.04, ZS −0.03) while every
**degenerate**-keep deck shows dMull ≈ +0.06. Read: where the keep actually encodes a
plan, it *trades* smoothness for plan assembly; where it doesn't, it is a smoothness keep
and buys a smoothness crumb. **Mean dead turns cannot measure whether the mulligan does
its real job.** The sweep's conclusion should be stated as "the mulligan is not a
*smoothness* lever" — which is true and now twice-verified — not "the mulligan has no
effect."

## 5. The right metric, measured: assembly/front-edge A/Bs

- **2026-06-16** (Plan_Aware_Mulligan doc, P(decap ≤ T7), plan − default): Zero-Sum
  **+6pp**, DLA +3, Eldrazi +3, five decks +1, rest 0 — and Radiation **−9pp** when its
  FINDING spec dug toward the side-line combo (the mis-tag since fixed). The keep rule
  *can* matter; mostly it matters as a **diagnostic** of a mis-modeled plan.
- **New — Croak assembly A/B** (`glarb_inevitable_lab --mode clock`, 40k trials, default
  vs `DECK_SIM_PLAN_KEEP=1`): FULL-line cumulative T6 9→10, T7 24→25, **median T9→T9**,
  never 10%→9%. Even the roster's sharpest, freshest FINDING spec — with 43% of first-7s
  mulled — buys ~**+1pp** at the front edge. The deck's redundancy (4 enablers × 2
  payoffs, 12+ dig/tutors in the 92) does the work; the keep rule can only re-order the
  first 7.

Both measurements inherit M1/M2: free mulls overstate the benefit per mull, the 2-mull
cap + stuck hands understate what deeper aggression could buy. The net ceiling of *real*
mulligan strategy is therefore still unmeasured — see §8.

## 6. Per-deck fidelity audit

Full per-deck detail (plan, bottleneck evidence, bucket spot-checks, wrongly-kept /
wrongly-shipped example hands) reviewed against each Summary + clock lab. Verdicts:

| deck | axes (effective) | verdict | main gap |
|---|---|---|---|
| Genome Project | BOARD (degenerate) | MINOR DRIFT | keep = band + cheap card; buckets dead code; mitigating: lab showed clock un-upgradeable anyway |
| Radiation Sickness | BOARD(deg)+FINDING | MINOR DRIFT | union deliberately keeps combo upside (lab-backed re-tag); ramp bucket missing the any-colour dorks (§7) |
| Replication Crisis | BOARD(deg)+FINDING | MINOR DRIFT → buckets WRONG | key_cards = the ~1–3% Sword+AA **backup**; the **primary Satya+Lightning Runner line is absent** (registry `win_line` predates the 2026-06-22 swap); Ranger-Captain of Eos counted as tutor but fetches nothing relevant (lab says so itself) |
| Lorehold Spirits | BOARD(deg)+FINDING | MINOR DRIFT | key_cards = the side-line Reveillark loop; a lone Reveillark keeps as "advancing" |
| Earthbend the Meta | MANA | MINOR DRIFT | ramp-only is too narrow: false-rejects on-curve Toph+payoff hands with no ramp spell; the payoff axis its own `mixed` note names is not in `also` |
| Exile's Return | BOARD (worst deg., CMC 3) | MINOR DRIFT | keeps pure-removal piles; no `also:[FINDING]` for the exile/blink engine the lab calls the true gate |
| Zero-Sum Game | FINDING | **FAITHFUL** | sharpest correct spec; blemish: key_cards list 2 of ~8 loop pieces, so a complete Conqueror+Bloodlord pair gets **shipped** |
| Curse of the Scarab | BOARD (real, CMC 5) | near-FAITHFUL | reach clause genuinely bites; still keeps reactive counterspell piles ("early play" = any cheap nonland) |
| Ms. Bumbleflower | BOARD (degenerate) | MINOR DRIFT | cannot reject the all-interaction no-engine durdle its Summary says to toss |
| Eldrazi Stampede | MANA (hi_curve) | MINOR DRIFT | `hi_curve & lands≥4` clause keeps the all-bombs-zero-ramp hand the Summary explicitly tosses; 1 ramp piece vs Summary's "2+" |
| Dark Lord's Army | BOARD (real, CMC 6) | **FAITHFUL** | best-aligned BOARD spec — gates on deploying the 6-mana hub, matching lab + Summary mulligan advice |
| Diminishing Returns | FINDING+BOARD(deg) | **bordering WRONG** | mulls toward the ~3%-of-games Gravecrawler combo; the real clock (death volume: sac outlets + drain payoffs) is in **no bucket** — the textbook Viscera Seer + Zulaport keep passes only via the vacuous BOARD clause; Esper Sentinel+Mind Stone counts as "digging". Spec's own `mixed` note has flagged this since 06-16 |
| Lightning War | BOARD (degenerate) | MINOR DRIFT | the deck's **fastest documented line is the T9 Reiterate+Seething combo** (race-only table >T14) yet there is no FINDING axis — its 7 tutors are invisible to the keep; inverse of the Radiation/Lorehold pattern |
| Grand Design | MANA (hi_curve) | MINOR DRIFT | right class; `hi_curve` clause keeps all-bombs bricks; ramp bucket missing Birds/Bloom Tender/Arcane Signet/Coalition Relic → **false-rejects real accel hands** (§7) |
| Crystal Sickness | BOARD (degenerate, CMC 2) | MINOR DRIFT | dev-gated (8-artifact density) is inexpressible; CMC-1 Dreadnought games the "early play" clause (the Summary's example toss-hand keeps) |
| Croak and Dagger | FINDING+MANA (fresh) | **FAITHFUL** | one key card per combo category + real topdeck tutors; blemish: a lone Aetherflux (payoff, no engine/dig) keeps — the Summary's example toss |
| Forced Liquidation | FINDING | MINOR DRIFT | the deck-defining **lethal-or-bust ≥2-punisher rule is inexpressible** — a lone Windfall (the refuel-trap hand) keeps as a key card; selection bucket polluted by punisher payoffs (§7) |

Pattern: **no spec is backwards**, two are genuinely faithful (Zero-Sum, DLA — plus fresh
Croak), and the drift concentrates in three repeated causes: the M6 degeneracy, key_cards
pointing at a side/backup line instead of the measured primary, and generated-bucket
noise.

## 7. Generator bugs (verified against oracle text / lab docstrings)

1. **Ramp regex misses braceless producers** (`framework_bakeoff.tag_card`:254 requires
   `add \{`): "Add one mana of any color" cards — Birds of Paradise, Bloom Tender, Arcane
   Signet, Coalition Relic, Incubation Druid, Paradise Chocobo — are systematically absent
   from every `ramp` bucket. This **actively mis-mulls** the MANA decks (Grand Design /
   Earthbend reject a hand whose only accel is Birds or a Signet) and weakens BOARD-reach
   on Curse/DLA.
2. **Selection bucket counts draw *payoffs* as draw *sources***: the bucket inherits the
   raw `draw` tag ("draw a card" substring), so Sheoldred, Psychosis Crawler, Niv-Mizzet
   et al. read as selection. The flow model fixed exactly this class on 2026-07-03
   (`deck_sim._draw_profile` strips trigger-condition clauses) — **the fix never
   propagated to keep_spec's buckets.** Bites Forced Liquidation hardest: two punishers
   satisfy the "≥2 selection = digging" clause.
3. **Tutor-bridge mismatches** — a tutor counts as plan-advancing even when it cannot
   fetch any key card: Ranger-Captain of Eos (Replication — lab docstring: "no package
   piece qualifies"), Conduit of Ruin (Eldrazi — colourless-only, can't find Craterhoof),
   Recruiter of the Guard (Diminishing — can't fetch Phyrexian Altar), Enlightened Tutor
   (Exile's — misses Hellkite), Brightglass Gearhulk (Earthbend — MV≤1, misses Triumph).
   FINDING treats "holds a tutor" as "can find the win"; for these it can't.
4. Registry-level drift found on the way: Replication's `win_line` still names Sword+AA;
   the 2026-06-22 swap made **Satya+Lightning Runner** the primary (12% T6 vs 1%). This
   propagates beyond mulligans (WIN_LINE feeds the bake-off + key_cards) — flagged, not
   silently edited.

*Auditor humility note:* three additional "mis-tag" candidates flagged during review —
Toxrill (does have a real draw ability), Earthbender Ascension (genuinely ramps: fetches a
basic to battlefield), Professor Dellian Fel (0: draw a card) — were **checked against
oracle text and dismissed**. Read-the-card applies to auditors too.

## 8. What would actually answer "does mulligan strategy matter?"

The audited model can only answer for its own narrow strategy family (binary keep, ≤2
free redraws, keep-when-stuck). To bound the ceiling of *real* mulligan play:

1. **London mulligan experiment** (the direct answer): implement draw-7/bottom-N with a
   real card penalty and deeper mulls (env-gated, default off, golden untouched), plus a
   simple bottoming policy (bottom non-plan cards). A/B on the front-edge oracle
   (P(decap≤T7) / assembly curves) for the sharp-keep decks. This measures both the
   upside (deeper digs for FL/ZS/Croak) and the cost (card disadvantage) the current
   model structurally omits.
2. **Fix the generator first** (§7.1–.2 are cheap: extend the ramp regex to braceless
   "add one/two/… mana", strip payoff clauses before the draw tag), regenerate, re-run
   the GD/EBM front edge — the false-reject bug plausibly *understates* the MANA keeps
   today.
3. **Judgment edits worth testing** (each is one registry field + `--write` + an A/B):
   Lightning War `also:[FINDING]`; Earthbend `also:[BOARD]`; Exile's `also:[FINDING]`;
   Diminishing — encode the death-volume engine (needs a counted-bucket primitive, same
   as FL's ≥2-punisher rule — see next).
4. **A counted-bucket primitive** (`n_of{bucket} ≥ k`) would let FINDING express "2 of 3
   combo pieces", FL's ≥2 punishers, and Crystal's artifact density — the three places the
   audit found real plans that are *inexpressible* today.

Priority: (2) then (1). (3)/(4) only pay off if (1) shows the front edge responds to keep
sharpness at all once mulligans have real costs.

---

*Files: `scripts/mulligan_audit.py` (new), `analysis/keep_specs.json` (regenerated),
`tests/test_deck_registry.py` (freshness guard), this doc. Companion:
`analysis/Plan_Aware_Mulligan_2026-06-16.md`, `analysis/Smoothness_Sweep_2026-07-03.md`,
`analysis/Smoothness_Model_Handoff_2026-07-03.md`.*
