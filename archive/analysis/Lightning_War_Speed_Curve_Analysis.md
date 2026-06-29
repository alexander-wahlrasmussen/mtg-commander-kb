# Lightning War — Speed-Curve Analysis: Pre-Pivot vs. Current Burn Build

**What this is:** the same rigor we applied to the Witherbloom builds (`Witherbloom_External_Build_Comparison.md`), turned on our own deck. A before/after measurement of whether the burn pivot actually made **Fire Lord Azula (Lightning War)** kill *sooner and more reliably* — not just "feel" faster.

**Date:** 2026-06-08
**Card text verified** against local Scryfall data (`card_lookup.py`) for every finisher, amplifier, mana source, and the old combo pieces — not pattern-matched.
**Decks measured:**
- **Pre-pivot:** `archive/old_decklists/lightning-war-20260413-153124.txt` (the "Combo Hunter" build — Azula + Ozai + Aggravated Assault infinite combats)
- **Current:** `decks/lightning-war-20260607-122049.txt` (race/burn — copy-amplified X-spell finish)

Both run through the canonical `scripts/deck_sim.py` engine (40k trials, seed 12345), plus a **grouped kill-enabler model** the stock fixed-piece sim can't express ("≥1 member of each named group available").

> **Bottom line up front:** Yes — the pivot is a genuine speed-curve improvement, but **not** through the mana curve (that is statistically identical before and after). The entire gain is in **kill-enabler availability**: the deck went from a ~1% two-specific-card combo that came online T8+ to a 1-of-N burn finisher behind an always-present commander that is **22–39% available by T6 (47–59% with tutors)** and lands the kill **T6–7**.

---

## The question

The pivot's thesis was "closes T6–7 from a single cast, faster and more reliable than the 3-card Aggravated Assault combo it replaces." This document tests that claim three ways:

1. **Did the mana/setup curve change?** (When can we cast the 4-mana commander and reach kill-turn mana?)
2. **Did the kill-enabler availability change?** (How often do we actually *have* a kill button by turn T?)
3. **What mana does the kill really cost?** (The part the sim ignores — does "finisher in hand" mean "lethal"?)

---

## 1. Setup curve — statistically unchanged

The mana base was deliberately left alone in the pivot, and the sim confirms it. These two columns are within Monte-Carlo noise of each other:

| metric (land base only) | Pre-pivot | Current |
|---|---|---|
| Keepable opening hand | 99.2% | 99.1% |
| Pure lands / flex-land backs | 30 / 7 | 30 / 6 |
| Avg nonland CMC | 2.65 | 2.64 |
| All colours from lands — T4 | 52% | 51% |
| All colours from lands — T6 | 67% | 66% |
| "Has a play" — T2 / T3+ | 96% / 100% | 96% / 100% |

**Read:** the deck is not faster because it curves out faster — it doesn't. Same lands, same colour reliability, same castability, ~same average cost. (Composition shifted *within* that flat curve: sorceries 8→12 and creatures 14→18, as X-spells and SOS bodies replaced control/value spells. The curve stayed flat because the X-spells are printed at low CMC — Crackle/Comet/Electrodominance all CMC 2, Banefire CMC 1.)

So if there's a speed gain, it has to be in the kill itself. There is.

---

## 2. Kill-enabler availability — the actual improvement

`deck_sim.py` grouped model. "Drawn" = pieces seen by natural draw; "+tutors" treats Mystical Teachings, Emeritus of Woe (→ Demonic Tutor), and Sanar (→ Wild Idea) as wildcards. Ignores mana — a **card-availability ceiling**, read next to §3.

| availability by turn | T4 | T5 | **T6** | T7 | T8 | T10 |
|---|---|---|---|---|---|---|
| **PRE-PIVOT** — its only assembled win (Aggravated Assault + Ozai), no tutors | 1% | 1% | **1%** | 2% | 2% | 2% |
| **PRE-PIVOT** — any dedicated X-finisher in hand | 0% | 0% | **0%** | 0% | 0% | 0% |
| **CURRENT** — ≥1 burn finisher drawn (of 4) | 33% | 36% | **39%** | 42% | 45% | 50% |
| **CURRENT** — ≥1 burn finisher, +tutors | 52% | 56% | **59%** | 62% | 65% | 71% |
| **CURRENT** — ≥1 *table*-finisher (Crackle/Comet) drawn | 18% | 20% | **22%** | 24% | 25% | 29% |
| **CURRENT** — ≥1 *table*-finisher, +tutors | 40% | 43% | **47%** | 50% | 53% | 58% |
| **CURRENT** — finisher **+** amplifier (overkill config), +tutors | 23% | 27% | **31%** | 35% | 39% | 46% |

**This is the speed curve.** Three things changed structurally:

1. **The old deck ran zero burn finishers** — its "finisher in hand" line is a flat 0% because the cards didn't exist in the 99. Its only assembled win was the Aggravated Assault + Ozai loop, which (a 2-card line with **no tutors to find it**) was ~1% by T6, ~2% by T10. That matches the known maths for an untutored fixed pair in a singleton deck (~2% by T10).

2. **The kill dropped from "two specific cards" to "one of N behind a free commander."** Azula is always in the command zone, so the new kill needs just *one* library card (a finisher). That is why the curve jumps from ~1% to 22–39% by T6 — redundancy (4 finishers) × a free combo half.

3. **Tutors now matter.** The old combo had no enabler that could find an enchantment. The new build's three tutors lift any-finisher availability to 59% by T6 / 71% by T10, and true table-finisher to 47% / 58%.

---

## 3. What the kill actually costs (the mana layer the sim ignores)

"Finisher in hand" ≠ "table is dead." All damage math below assumes **Azula is attacking** (so each spell cast in her combat is copied once; Twinning Staff adds one more copy) and a 4-player pod (3 opponents at 40 life). Casting a *sorcery* finisher in combat additionally needs a flash enabler (Leyline of Anticipation / Vedalken Orrery / Borne Upon a Wind / High Fae Trickster); the *instant* finishers (Comet, Electrodominance) need none.

**Crackle with Power** `{X}{X}{X}{R}{R}` (= 3X+2 mana) — *five times X to each of up to X targets*. The only finisher that forks full damage to the whole table from a single instance:

| X | mana | dmg/target/instance | Azula only (2 instances) → per opp | + Twinning (3 instances) → per opp |
|---|---|---|---|---|
| 3 | 11 | 15 | 30 | **45 ✔ lethal** |
| 4 | 14 | 20 | **40 ✔ lethal** | 60 |

→ **The clean table kill is Crackle X=3 with Twinning (11 mana) or X=4 without (14 mana).**

**Comet Storm** `{X}{R}{R}` + multikicker `{1}`/extra target — X to each target. Table kill needs to kick twice (+{2}) and stack enough X: 3 opps dead needs `2X≥40` (Azula only) → X=20 → **24 mana**, or `3X≥40` (+Twinning) → X=14 → **18 mana**. Real value is **instant speed** (cast on their turn / through a sorcery-counter wall), not cheap mass damage.

**Banefire** `{X}{R}` and **Electrodominance** `{X}{R}{R}` — **single target**. Copies can pile on one opponent (Banefire X=14 +Twinning = 3×14 = 42 → kills *one* player at 15 mana, **uncounterable** at X≥5) or spread one copy each (then each opp only takes X). They are **single-opponent deletes and removal** (kill Grand Abolisher, kill the combo player), *not* table kills at sane mana.

> **Correction to the deck Summary:** the Kill Lines list "Azula + Crackle / Comet / Electrodominance" as co-equal 2-card kills. Accurate for Crackle and (expensively) Comet; **Electrodominance and Banefire are single-target** and only wipe the table with a doubler stacking copies or a huge mana turn. They earn their slots as cheap removal + uncounterable reach, not as table-finishers.

**Can the deck reach 11–14 mana on T6–7?** The sim's land floor is ~5 at T6 — but that excludes the 4 rocks, the rituals (Dark/Desperate Ritual, **Jeska's Will**, Blazing Firesinger/Seething Song), and Treasures (Storm-Kiln on every cast *and* copy, Goldspan's tap-for-2, Sanar). **Jeska's Will** cast mid-combat is the spike: with a commander out you choose *both* modes, and Azula copies it — mode 1 alone is R per card in an opponent's hand, doubled. A T6–7 combat with one ritual/Treasure source online realistically clears 11–14. The kill turn is gated by the **joint** event "finisher in hand **and** a big-mana combat," which is why the honest window is T6–7, not T5.

---

## 4. Kill window — before vs after

| | Pre-pivot (combo) | Current (burn race) |
|---|---|---|
| Earliest realistic kill | **T8+** (needs Azula + 6-drop Ozai + Aggravated Assault all in play + ~13 mana to start the loop) | **T6–7** (Azula T4–5, then a finisher + big-mana combat) |
| Pieces required (beyond commander) | **2 specific** (Ozai + Aggravated Assault) | **1 of 4** finishers (+ amplifier for comfort) |
| Enabler availability by T6 | ~1% (no tutors) | 22% table / 39% any, → 47% / 59% with tutors |
| Failure mode | combo never assembles → grindy beatdown with no closer | finisher drawn but mana short → kill slips a turn |
| Counter-resilience of the kill | none special | Banefire uncounterable X≥5; instants castable through a sorcery-only Abolisher turn |

---

## Verdict

**The pivot improved the speed curve, and we can now say exactly how.** It did *not* lower the mana curve (identical) — it replaced a fragile, untutored, T8+ two-card combo (~1% by T6) with a **redundant, tutorable, T6–7 burn kill** that is one library card behind a free commander (22–39% by T6, up to 47–59% with tutors). The deck is both **earlier** (T6–7 vs T8+) and **far more consistent** (an order of magnitude more likely to have a closer in hand on the kill turn), at **zero cost** to opening-hand keepability, colour, or castability.

The remaining honest limiters:
- **Mana, not cards, is now the gate.** Availability outruns the mana to deploy it; the kill-turn join is the real constraint. A cheap front-loaded mana source (the kind already debated for Calamity Tax) would move the *realized* kill earlier more than any further finisher would.
- **Two of the four "finishers" are single-target.** True table-wipe availability is the 22%/47% line, not the 39%/59% line. Adding a second forking finisher (e.g., Fireball, Jaya's Immolating Inferno) would lift the table-kill curve; the current single-target pair is justified as removal/reach instead.

---

## Method caveats

- `deck_sim.py` is a **consistency** simulator, not a rules engine. Mana/colour are land-only floors; kill-enabler % ignores mana, the board, and whether Azula is attacking.
- The grouped model treats all three tutors as generic wildcards. Slightly optimistic: Mystical Teachings fetches instants only (it can grab Comet/Electrodominance and the instant doublers, but not the Crackle/Banefire sorceries) — it still satisfies "find *a* finisher," so the finisher curve is fair; the amplifier curve is marginally generous.
- "Lethal" math assumes a 3-opponent, 40-life pod with no prevention/fog and Azula connecting (unblocked / evasive enough to stay an attacker). Chip from Guttersnipe (2/opp/cast) and bodies lowers the X needed in practice.
- Conversion Check (19/20) and the kill-window turns are structural estimates, not playtest data.

---

## 5. Lever test — what actually pulls the kill earlier? (added 2026-06-08)

The §1–4 analysis said *mana is the gate*. This section tests that by measuring which upgrade most moves the kill turn, under the **3-GC cap** (no GC adds). Method: a **joint kill-turn Monte Carlo** (60k trials; reproduce with `python scripts/lw_speed_lab.py --mode levers`) that — unlike `deck_sim.py` — tracks *both* gates in one trial: a table-finisher castable in Azula's combat (sorcery finishers gated on a flash enabler) **and** enough kill-turn mana, where mana = lands + rocks + Azula's +2 + the Treasure-storm engine (Storm-Kiln/Goldspan if cast) + ritual bursts. Draw spells dig extra cards. Lethal thresholds assume a 3-opponent, 40-life table wiped from **one cast** (Azula gives one copy; an amplifier adds another). Each lever is a 1-for-1 swap.

> **Heavy-assumptions caveat.** This is a heuristic, not a rules engine, and outputs are **assumption-sensitive** (an earlier pass without the Treasure engine / enabler gate ranked fast mana first; this fuller pass ranks draw first — they are within ~1 point of each other either way). Trust the **robust** conclusions (which hold across both passes), not the second decimal.

**P(one-cast table wipe ≤ turn T), %:**

| lever (−1 flex slot) | T8 | T10 | T12 | never |
|---|---|---|---|---|
| **BASELINE (current 99)** | 5 | 11 | 20 | 70% |
| + draw spell, dig-3 (Night's Whisper class) | 6 | 13 | **23** | **66%** |
| + flash enabler | 6 | 13 | **23** | **66%** |
| + Sol Ring (fast mana) | 6 | 12 | 22 | 68% |
| + draw spell, dig-2 | 6 | 12 | 22 | 68% |
| + extra ramp rock / Lotus Petal | 5 | 12 | 21 | 69% |
| + amplifier (copy-doubler) | 5 | 12 | 21 | 69% |
| + **forking finisher** (Jaya/Exsanguinate class) | 5 | 11 | 20 | 69% |
| + Sol Ring & dig-3 (stacked) | 7 | 14 | 24 | 65% |

**Ranked answer to "which of these pulls the kill faster?"** — every single lever is *small* (+0 to +3 points by T12), because the one-cast table wipe is a **3–4 card conjunction** (finisher + flash-enabler-for-sorceries + amplifier + an 11–14 mana turn) and no single card fixes a conjunction:

1. **More draw (an efficient dig-3) — best of your four**, tied with adding a flash enabler. Card flow assembles the conjunction faster.
2. **Front-loaded fast mana (Sol Ring) — close second.** This metric *understates* it: Sol Ring also casts Azula on T3 instead of T4, starting the attack + ping clock a turn earlier (see §5b).
3. **Generic ramp (a 5th rock / Lotus Petal) and an extra amplifier — marginal.** The deck is already mana-rich (4 rocks + rituals + Treasure-storm); flooding more ramp barely helps.
4. **A forking finisher — the *worst* add for speed (≈0).** The finisher leg is already the best-covered part of the conjunction (Crackle + Comet + 3 tutors). A third one adds resilience to finisher removal, **not** speed. *Do not add Jaya/Exsanguinate to go faster.*

> **Fast-mana legality note:** **Mana Crypt is banned in Commander** (verified via card_lookup — it is not a GC because it is illegal), so it is *not* an option despite its absence from the GC list. **Sol Ring** is the clean legal non-GC fast-mana add. Lotus Petal / Jeweled Lotus are the only other non-GC fast mana, and both are one-shot.

### 5b. The lever that actually dominates: the incremental clock

The model above only scores a **simultaneous one-cast wipe of a full-health table** — i.e. ~120 damage (40×3) in a single cast. That is the hardest thing the deck can attempt. The deck's *real* clock is **incremental**: Guttersnipe (2 to each opp per cast), Azula + bodies attacking, and single-target burn (Banefire/Electrodominance) picking opponents off. Re-running the baseline with opponents **pre-chipped** shows how much that matters:

| baseline, opponents at… | T6 | T8 | T10 | T12 | never |
|---|---|---|---|---|---|
| 40 life (goldfish, no chip) | 1 | 5 | 11 | 20 | 70% |
| **30 life** (one round of chip) | 5 | 13 | **23** | 34 | 54% |
| **20 life** (sustained chip) | 15 | 29 | **42** | 53 | 37% |

**Pre-chipping 40→30 roughly *doubles* the kill odds (+12 points at T10); 40→20 *quadruples* them — 4–10× the impact of any single card lever above.** The conclusion: the highest-leverage way to pull the kill earlier is **not** more mana, draw, or finishers — it is **more incremental damage that softens the table before the finisher**, so Crackle only has to find ~30 instead of ~120.

> **CORRECTED 2026-06-29 (magnitude only; conclusion stands).** The 40/30/20 sensitivity above was inflated by a Crackle-with-Power targeting-floor bug in `lw_speed_lab`: a 3-opponent wipe forces X≥3 = **11 mana at any life ≤ 45**, but the pre-chip rows offered sub-floor 5/8-mana "wipes" (X=1/X=2, only 1–2 targets). Re-run with the floor enforced, the lift shrinks — 40→30 is **~+4 pts at T10** (not +12) and 40→20 lifts T10 ~4%→25% and never-in-14 86%→51%. Incremental chip is **still the dominant lever** (bigger than any single-card add) and Comet Storm's X genuinely scales down with life, but "Crackle only has to find ~30 not ~120" is wrong — a 3-wipe floors at 11 mana regardless. See `project_lightning_war_speed_analysis` memory for the corrected figures.

### 5c. Concrete recommendation (≤3 GC, all non-GC, Grixis-legal — *card text verified*)

1. **Lean into the incremental clock (highest leverage).** The deck already runs Guttersnipe + Emeritus of Conflict's repeatable Bolt. The cheapest force-multipliers, all `{1}{R}` 2-drops, all non-GC:
   - **Firebrand Archer** — 1 to each opp per *noncreature* spell (2/1 body).
   - **Thermo-Alchemist** — `{T}`: 1 to each opp; **untaps whenever you cast an instant/sorcery** (0/3 defender — repeatable each cast).
   - **Electrostatic Field** — 1 to each opp per instant/sorcery (0/4 wall — also a blocker that survives the pod).
   These convert the deck's high spell volume into a clock every turn, not just on the assembled finisher turn.
2. **One efficient draw spell** to assemble the conjunction faster: **Night's Whisper** (`{1}{B}` draw 2) or **Painful Truths** (`{2}{B}`, draw up to 3 in Grixis). Best of the four levers you asked about.
3. **Sol Ring** if you want the front-loaded "Azula on T3" tempo (starts the incremental clock a turn earlier). Legal, non-GC.
4. **Skip the forking finisher for speed.** Only add Jaya's Immolating Inferno / Exsanguinate if you want redundancy against having Crackle/Comet removed — it does not accelerate the kill.

### 5d. Cross-deck availability (checked 2026-06-08)

Ownership from `collection/moxfield_haves_2026-06-07-1031Z.csv`; deployment from `decks/*.txt`; reskin-alias check clean (none are UB reskins).

| Card | Owned | Deployed in | Free | Verdict |
|---|---|---|---|---|
| **Sol Ring** | ~25 | ~16 decks | ~9 | ✅ deep surplus — free |
| **Night's Whisper** | 4 | Dark Lord's, Exile's Return, Genome | 1 | ✅ 1 spare |
| **Young Pyromancer** | 2 | none | 2 | ✅ free (token bodies = chip + attackers) |
| **Firebrand Archer** | 0 | — | — | ❌ buy (cheap common) |
| **Thermo-Alchemist** | 0 | — | — | ❌ buy (cheap common) |
| **Electrostatic Field** | 0 | — | — | ❌ buy (cheap common) |
| **Painful Truths** | 0 | — | — | ❌ buy (cheap common) |

The three incremental pingers all need buying (all cheap commons). Night's Whisper has exactly one free copy; Sol Ring and Young Pyromancer are free from surplus. Prices not checked (per user). The verified-text + GC/legality + availability checks are done; only Cardmarket pricing remains before a buy.

---

Related: `Lightning_War_Summary.md` · `Lightning_War_Burn_Pivot_2026-05-31.md` · `Witherbloom_External_Build_Comparison.md` · [[project_deck_sim_and_matchup_matrix]] · [[2026-05-31-pod-swaps]]
