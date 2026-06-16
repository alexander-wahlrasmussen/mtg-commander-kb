# Plan-Aware Mulligan — what a "good hand" is, per deck

**2026-06-16 · Backlog #5 · spec for review BEFORE wiring into `deck_sim` + the 16-clock re-harvest**

This is the understanding step the build rests on. The 2026-06-16 robustness check
(`Framework_Bakeoff_2026-06-16.md`) added a *generic* smart-keep ("has a CMC≤3 play") and
**0/16 medians moved** — because "has a cheap play" is not "advances THIS deck's plan." Before
writing a per-deck keep predicate, we have to say, per deck, **what a keepable hand actually is.**

---

## The reframe: a good hand clears the deck's *bottleneck*

The bake-off's own near-miss told us the axis. BDD's mana-budget (cheaper win line ⇒ faster)
failed precisely on decks whose **kill is finding-gated, not mana-gated** — Crystal Sickness has
the *cheapest* line (3 mana) and is the *slowest* deck (T11) because it must **dig**, not pay.

That is the same axis a mulligan rides. A "good hand" is one that clears **the constraint that
actually gates this deck's kill** — and that constraint differs by deck. Three classes:

| Bottleneck | The keep is fishing for… | "Good hand" test | Decks |
|---|---|---|---|
| **FINDING** | a combo PIECE or a tutor/dig toward it | holds a key card, a tutor, OR ≥2 selection cards | combo / piece-assembly decks |
| **MANA** | **acceleration** toward an expensive X / bomb | ~3 lands **with ramp/rocks** — NOT a land flood | big-mana / X-bomb decks |
| **BOARD / COMMANDER** | commander on curve + a follow-up | can deploy the commander ~on time AND has an early play | engine / commander-gated decks |

**Land-band rule (user, 2026-06-16):** the keep ceiling is **4 lands**, not 5. >4 lands is "very
greedy" unless the deck has a genuinely high CMC curve — and **even then** the good hand wants
**ramp/rocks to speed it up**, not more lands. So MANA-gated ≠ "many lands": the ideal mana-gated
keep is **~3 lands + a rock/ramp piece**, and a flat 4-land no-acceleration hand is marginal. Band
defaults tighten to **2–4** across the board; only the high-curve decks (Eldrazi avg CMC 5.25;
Atraxa-7 in Grand Design) get a 5-land ceiling, and they still prefer ramp over the 5th land.

This is the same finding-gated ⊥ mana-gated distinction from
`feedback_selection_vs_mana_gated` — now applied to the opening hand instead of the kill turn.
The keep rule for a deck should target *its* bottleneck, not a generic "cheap play."

**Why this should show signal where the generic keep didn't.** A generic keep moves the
**median** ~0 (most hands already hold a 3-drop). A bottleneck-targeted keep moves the **front
edge** — P(piece assembled / mana online by T5–7) — which is exactly the bar the real pod sets
(`decap by T≤7`). So we measure it against a **front-edge oracle**, not the median (see §4).

---

## Per-deck "good hand" — the spec

Bottleneck + land band + the keep target, one row per active deck. **Seed cards** are the
already-verified pieces (from each Summary's kill line = `framework_bakeoff.WIN_LINE`, the
`*_clock_lab` KILL CHECKS, and `kill_tree.py`). The *authoritative* key/tutor/enabler card lists
get **generated** from those same verified sources + the bake-off tagger (§3) and reviewed — they
are **not** hand-typed from memory. "e.g." below = illustrative pending that generation.

| Deck | Commander | Bottleneck | Lands | Good hand = | Seed keep-cards |
|---|---|---|---|---|---|
| **Genome Project** | Kuja | BOARD (storm-engine) | 2–4 +ritual | cast Kuja ~T4 + a multiplier or a cheap cast-chain | Kuja online; e.g. Harmonic Prodigy, Coruscation Mage, City on Fire, a ritual/draw-2 |
| **Radiation Sickness** | Wise Mothman | FINDING (+counter board) | 2–4 | a combo piece, OR Mothman + a proliferate/counter engine | Mindcrank, Bloodchief Ascension, Simic Ascendancy |
| **Replication Crisis** | Satya | BOARD/**COMMANDER** (trigger on **attack**) +FINDING | 2–4 | Satya castable + protection so she can **attack** (token-copy fires on attack, not on connect — verified) | Sword of Feast and Famine, Aggravated Assault; protection (Greaves/Boots) |
| **Lorehold Spirits** | Quintorius | FINDING (3-card loop) | 2–4 | Quintorius + a recursion piece, OR a loop piece/tutor | Reveillark, Karmic Guide, Goblin Bombardment |
| **Earthbend the Meta** | Toph | MANA/BOARD (lands-matter) | 2–4 | ~3 lands + ramp/lands-matter + a payoff | Triumph of the Hordes + ramp |
| **Exile's Return** | Zuko | BOARD (aggro / extra-combat) | 2–4 | early aggressive bodies + a finisher / extra-combat | Hellkite Charger + early creatures |
| **Zero-Sum Game** | Witherbloom | FINDING (cmdr-indep combo) | 2–4 | a combo piece or tutor + a life-event source | Exquisite Blood, Sanguine Bond, Blood-Artist-class |
| **Curse of the Scarab** | Scarab God | BOARD (zombie-count / devotion) | 2–5 | Scarab + zombie producers, OR a devotion-drain payoff | Gray Merchant of Asphodel + zombie producers |
| **Ms. Bumbleflower** | Bumbleflower | BOARD (engine) | 2–4 | Bumbleflower + a spell engine / the steal package | Jolrael; Willbreaker; cheap spells |
| **Eldrazi Stampede** | Maelstrom Wanderer | MANA (ramp to bombs, hi-curve) | 2–5 + ramp | ~3 lands + **ramp/rocks** toward a bomb (ramp required, not a 5-land flood) | ramp; Craterhoof Behemoth / Eldrazi |
| **Dark Lord's Army** | Sauron | BOARD (grind drains) | 2–5 | Sauron + a drain enchantment or a sweeper | Sheoldred / Underworld Dreams / Wound Reflection; Gary |
| **Diminishing Returns** | Teysa | FINDING (combo) +aristocrats | 2–4 | a combo piece/tutor + a sac outlet, OR Teysa + death engine | Gravecrawler, Phyrexian Altar, Razaketh |
| **Lightning War** | Azula | **BOARD/COMMANDER** (deploy Azula → cheap-spell copy engine) | 2–4 | cast **Azula ~T4**, then a cheap value spell to copy/ramp (draw / ritual / burn) | Azula online; cheap spells (Banefire/Crackle, rituals, draw, pingers) |
| **Grand Design** | Atraxa | FINDING (Finale = single PoF) +MANA (Atraxa-7) | 2–5 + ramp | ~3 lands + **ramp** + a finisher (Finale or the combat backup) | Finale of Devastation, Craterhoof Behemoth |
| **Crystal Sickness** | Golbez | BOARD/MANA (**dev**-gated) + dig | 2–4 | Golbez + artifact-build/dig toward the drain cycle | Phyrexian Dreadnought; artifacts; dig (cycle the bracket) |
| **Calamity Tax** | Glarb | MANA (Torment X=12+) grind | 2–4 + ramp | ~3 lands + **ramp** + Glarb + an X-drain / grind engine | Torment of Hailfire; ramp |

Notes that bite (from the audits/memory, so the spec doesn't relearn them):
- **Crystal Sickness is NOT pure-finding.** It *looks* finding-gated (dig a bomb) but is
  **development-gated** — 8 artifacts + a high-power creature + drain cycles
  (`feedback_selection_vs_mana_gated`, `cs_clock_lab --mode digtest`). Its good hand wants
  *board/mana progress*, not just a dig spell. Tagged BOARD/MANA, not FINDING.
- **Radiation & Diminishing are FINDING with a BOARD fallback** — the combo is one line; the
  counter-board / death-volume grind is the other. Keep accepts *either* axis.
- **Replication is COMMANDER-gated, trigger on ATTACK** (verified `{1}{U}{R}{W}`, haste + menace):
  "Whenever Satya **attacks**, create a tapped+attacking copy… + {E}{E}." She doesn't need to
  *connect* — she needs to be cast and survive to **declare an attack**. So the keep values Satya
  (haste = same-turn swing) + protection to clear a removal window, as much as a combo piece.
  (kill_tree's "needs Satya to connect" is wrong — fix separately.)
- **Lightning War FLIPS at Azula** (verified `{1}{U}{B}{R}`, CMC 4): *Firebending 2* (attack → `{R}{R}`)
  + **copy every spell you cast while she's attacking.** It is mana-gated only until Azula lands;
  then it's a cheap-spell value/copy engine (draw / rituals / burn each get copied + RR refunds).
  So the opening-hand bottleneck is **deploy Azula on curve + hold cheap spells**, i.e.
  BOARD/COMMANDER — not "ramp to a 14-mana X." (Reclassified from MANA, 2026-06-16.)

---

## 3. Implementation — keep deck_sim text-free

`deck_sim` deliberately interprets **no card text** ("output is exactly as trustworthy as the
decklist + oracle fields"). To preserve that, the keep predicate must not run regexes in the hot
loop. Architecture:

1. **`scripts/keep_spec.py` (generator).** Reuses `framework_bakeoff`'s verified machinery — the
   `WIN_LINE` pieces, the function tagger (`tag_card` → ramp/draw/tutor/interaction/protection),
   the GC/alias loaders — plus the `*_clock_lab` KILL-CHECK card names and `kill_tree` lines, to
   emit **`analysis/keep_specs.json`**: per slug → `{bottleneck, min_lands, max_lands,
   key_cards[], tutors[], enabler_cards[], n_selection_needed}`. All card *names*, resolved once.
2. **`deck_sim.keep_hand` consults an installed spec.** A module hook (mirroring the existing
   `DECK_SIM_SMART_KEEP` env pattern) — `ds.set_keep_spec(spec_or_None)` — so each lab installs
   its deck's spec before its trials; with no spec installed, behaviour is **unchanged**
   (land-count keep). `keep_hand` only does set-membership + counts on names/cmc — still no text.
3. **The labs + `pod_gauntlet --refresh`** install the spec per deck and re-harvest the 16 clocks
   into a *separate* JSON (don't overwrite the committed `pod_gauntlet_clocks.json` until the
   verdict is in — same discipline as the `--clocks` smart-keep experiment).

Keep predicate (pseudocode):

```
keep_hand(hand, spec):
    lands = count_lands(hand)
    if not (spec.min_lands <= lands <= spec.max_lands): return False
    if spec.bottleneck == FINDING:
        return holds_any(hand, spec.key_cards | spec.tutors) \
            or count(hand, spec.enabler_cards[selection]) >= spec.n_selection_needed
    if spec.bottleneck == MANA:
        # acceleration, not a land flood: ~3 lands + a rock/ramp piece. A flat 4-land
        # no-ramp hand fails unless the deck is genuinely high-curve (spec.hi_curve).
        return holds_any(hand, spec.enabler_cards[ramp]) or (spec.hi_curve and lands >= 4)
    if spec.bottleneck == BOARD:        # commander-gated (incl. Lightning War: deploy Azula)
        return curve_ok_for(spec.cmdr_cmc, lands, hand) and has_early_play(hand)
```

---

## 4. Pair it with the front-edge oracle (or the test is blind)

The bake-off scored **medians**; two opening mulligans move the **front edge**, not the median
(measured: generic keep moved 0 medians). So a plan-aware keep tested against a median oracle is
**structurally insensitive** — we'd relearn "0/16 moved" and wrongly conclude it's worthless.

Add a **front-edge oracle**: `P(decap ≤ T7)` (and maybe `≤ T6`), read straight off the decap
curve already stored in `pod_gauntlet_clocks.json` (`grid`/`decap`), interpolated to T7. New
column in `framework_bakeoff --bakeoff`. **Hypothesis:** the consistency frameworks (BDD-
consistency, Disciple's draw/tutor terms) and finding-gated decks show signal here that the
median oracle hides — and the plan-aware keep *lifts the front edge for finding-gated decks*
specifically (a piece-dig is worth ~2 cards of selection, which matters at T5–7, not at the
median).

**Honest prior (unchanged):** a *fidelity* upgrade that lifts finding-gated decks + maybe
Disciple a little at the front edge — **not** a verdict reversal. It does not touch the deeper
leak (the oracle is a solitaire goldfish; Interaction/Durability score 0 with no opponents,
however you mulligan). That interaction overlay is a separate, bigger frontier.

---

## Build order

1. **Lock this spec** — bottleneck class + land band per deck (the rows above). ← review gate
2. `keep_spec.py` → `keep_specs.json` (generated from verified sources), eyeball with a `--show`.
3. `deck_sim.set_keep_spec` + bottleneck-aware `keep_hand`; default path unchanged.
4. Front-edge oracle column in `framework_bakeoff` (P(decap ≤ T7) off the clocks JSON).
5. Re-harvest 16 clocks WITH the spec into a scratch JSON; re-run `--bakeoff` median **and**
   front-edge; diff vs the committed snapshot.
6. Write the result up; only then decide whether the plan-aware keep replaces the default harvest.

## Results (built + harvested 2026-06-16)

**Built:** `keep_spec.py` → `analysis/keep_specs.json` (buckets generated from `WIN_LINE` + the
bake-off tagger; bottleneck/band hand-curated). `deck_sim.set_keep_spec`/`install_keep_spec` +
bottleneck-aware `keep_hand`, installed at parse when `DECK_SIM_PLAN_KEEP=1` (default path
byte-identical otherwise). Front-edge oracle `front_edge()` + `framework_bakeoff --frontedge` and a
`front7` column in `--bakeoff` (reads the decap CURVE, so it's sensitive to the mulligan; baked
`med` is not). `pod_gauntlet --refresh --out` for non-destructive scratch harvests. Verified the two
reclassified commanders' oracle text (Azula, Satya). A/B = two fresh 8k harvests, default vs
`DECK_SIM_PLAN_KEEP=1`, into scratch JSONs (committed snapshot untouched).

**The mulligan became a DIAGNOSTIC, not a speed-up.** P(decap ≤ T7), plan − default:

| helps (tag = fast line) | Δ front7 | hurts (tag = wrong line) | Δ front7 |
|---|---:|---|---:|
| Zero-Sum (FINDING, combo IS the clock) | **+6** | **Radiation (FINDING)** | **−9** |
| Dark Lord (BOARD) | +3 | **Lorehold (FINDING)** | **−4** |
| Eldrazi (MANA, ramp required) | +3 | | |
| Earthbend / Exiles / Bumble / Curse / Grand Design | +1 | (all others) | 0 |

The losers are the tell: a FINDING keep digs for a combo PIECE, so it keeps piece-rich /
development-poor hands. For **Radiation** that's actively wrong — its fast decap is the
**counter-grown board**, and the Mindcrank+Bloodchief combo is a *side* line; mulliganing toward
the combo slows the real clock by 9pp at T7. Same for **Lorehold** (the 3-card Reveillark loop is a
side line). This is exactly the "board-fallback not in predicate — watch" caveat, now measured. So
the tool's real payoff isn't speeding decks up — it's **flagging decks whose bottleneck we
mis-modelled.** Resolution: re-tagged Radiation + Lorehold FINDING → BOARD (their real fast line).

**Confirmation (re-tag harvest).** With Radiation + Lorehold tagged BOARD, the front-edge harm
vanishes exactly: **Radiation 76% (default) → 67% (FINDING) → 76% (BOARD)**; **Lorehold 47 → 43 →
46**. Every other deck moved 0pp between the two plan harvests (only those two tags changed) — so the
−9/−4 was provably the mis-tag, not the mulligan. A *union* keep (combo-piece OR board-curve) for
two-line decks was then explored — see below.

### Union keep — explored 2026-06-16

For genuinely two-line decks, a single axis is fragile: tag the wrong one and you over-dig (the −9).
The **union keep** accepts a hand strong on EITHER line — `keep = land-band AND (primary OR also)`,
an order-independent OR over axes (`deck_sim._axis_ok` + `spec["also"]`; `keep_spec.ALSO`). Applied
to the four two-line decks: Radiation (BOARD + FINDING), Lorehold (BOARD + FINDING), Replication
(BOARD + FINDING), Diminishing (FINDING + BOARD). Same-batch 8k A/B/C harvest, P(decap ≤ T7):

| deck | default | pure-primary | union |
|---|---:|---:|---:|
| Radiation | 76 | 76 | 76 |
| Replication | 59 | 59 | 59 |
| Lorehold | 47 | 46 | 46 |
| Diminishing | 11 | 11 | 11 |

**Union is clock-neutral** — +0 vs pure-primary on all four, ~0 vs default, and 0pp on every
single-line deck (the `also`-less ones are untouched). It doesn't move the front edge because (a)
the sim mulligan is free and (b) the primary BOARD axis already keeps the fast-line hands. **Its
value is robustness, not speed:** being an OR, it is *order-independent*, so it structurally cannot
reproduce the single-axis −9 over-dig — you no longer have to nail which axis is "primary," only
include the true fast axis somewhere in the union. It is also the more realistic keep (a player
keeps a bomb combo hand). **Adopt it as the safer formulation for two-line decks** (clock-free
hardening against future mis-tags), not for a number — exactly what a free-mulligan sim can and
can't see.

**Framework verdict held.** The `front7` Spearman ρ's barely moved default → plan-keep (CC
−0.406→−0.392, Disciple −0.352→−0.323, BDD-consistency +0.346→+0.319, all within ~0.03). No
quality framework predicts the front edge better under an aggressive plan-aware mulligan than under
the land-count keep. The honest prior was right: **a fidelity upgrade, not a verdict reversal.** The
deeper leak (solitaire goldfish: Interaction/Durability score 0) is untouched, as predicted.

**Caveat that bounds the whole result — the sim's London mulligan is FREE.** `deck_sim.opening_hand`
redraws a fresh 7 each mull without bottoming cards, so aggressive digging has *no modeled downside*.
The real London penalty (−1 card per mull) would shave every positive Δ above and would *worsen* the
over-digging losers further. So the +Δ's are an **upper bound** and the −Δ's are a **lower bound on
the harm** — which only sharpens the diagnostic reading. Decision: **do NOT** replace the committed
harvest with the plan-keep curves; keep plan-keep as an opt-in diagnostic (`DECK_SIM_PLAN_KEEP=1`).

## Open calls for review

- **Land bands — RESOLVED 2026-06-16.** Ceiling 4 lands; 5 only for high-curve decks (Eldrazi,
  Grand Design) and even they prefer ramp. MANA-gated keep **requires** a rock/ramp piece (≈3
  lands + acceleration), not a high land count.
- **Lightning War — RESOLVED 2026-06-16.** Reclassified MANA → BOARD/COMMANDER (deploy Azula,
  then cheap-spell copy engine).
- **Replication — RESOLVED 2026-06-16.** Commander-gated; trigger on attack, not connect.
- **Still open — combo keep strictness:** accept a *tutor or 2 selection cards* as "advancing"
  (proposed), or demand an actual piece in hand (stricter → more mulligans-to-3)?
- **Still open — the remaining mixed calls:** Radiation & Diminishing tagged FINDING-with-BOARD-
  fallback (keep accepts either axis); Grand Design FINDING+MANA. Confirm or split.
