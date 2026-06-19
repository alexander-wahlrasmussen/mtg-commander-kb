# Lightning War — Fire Lord Azula (Combo-Race Build)

**Commander:** Fire Lord Azula ({1}{U}{B}{R}, 4/4, Legendary Creature — Human Noble)
**Colors:** Grixis (UBR)
**Archetype:** Spellslinger **combo-race** — Azula infinite combo (primary) + copy-amplified X-spell burn (backup)
**Role:** the deck pulled to **race the combo pod** — out-tempo a Grand-Abolisher-protected combo rather than disrupt through it (see [[bracket_4_in_spirit]], [[grand_abolisher_blocks_counters]])
**Bracket:** 3 (3 of 3 Game Changer slots used; **infinite combo present — pod-approved** [[infinites_ok_in_pod]]; no MLD; no extra turns)
**Game Changers:** Fierce Guardianship, Mystical Tutor, Gifts Ungiven
**Conversion Check:** 19/20 (axes shifted 2026-06-19 — Kill/clock up, Interaction down; the build trades disruption density for an Abolisher-immune combo — see Pod Fit)
**Kill Window:** **combo decap=table ~T7–10** (`lw_combo_lab.py --mode recur`, 2026-06-19; ~52% by T10) · **race decap T7–8 / table T10** (`lw_clock_lab.py` chip, 2026-06-14). **pod_gauntlet P(WIN vs pod) 38%→64%** (race-led; clock gain ≫ static-disruption loss). Evidence: `proposals/Lightning_War_Consistency_Upgrade_2026-06-18.md` §10–13.
**Current decklist:** `lightning-war-20260619.txt` (combo-race rebuild 2026-06-19: 13 swaps + 2 land; the `.txt` is ground truth, this is commentary)

> **⚠ 2026-06-19 combo-race rebuild.** The header, Conversion Check, Bracket Compliance, Pod Fit, and Engine Role Map above/below are current. The lower narrative sections (*What the Deck Is Trying to Do*, *Kill Lines*, *Clock Note*, *Audit Note*) still describe the prior **race-only** build and are superseded by `proposals/Lightning_War_Consistency_Upgrade_2026-06-18.md` §10–13 (the canonical rebuild record) — refresh on a later pass.

---

## Commander Rules Text

- **Firebending 2:** Whenever Azula attacks, add {R}{R}. **This mana lasts until end of combat** — without a retention piece (Ozai, Leyline Tyrant) it evaporates before main phase 2.
- **Spell Copy:** Whenever you cast a spell while Azula is attacking, copy that spell (you may choose new targets). A copy of a permanent spell becomes a token.
- **Key rulings:** The copy resolves before the original. Copies are **not "cast"** (no re-trigger of cast-triggered abilities). X values are preserved. Additional costs paid on the original apply to the copy.

---

## What the Deck Is Trying to Do

Azula turns your combat into the most dangerous part of the turn. Every instant/sorcery you cast while she attacks is copied — instants natively, sorceries once a flash enabler is online — and Twinning Staff makes every copy event **+1**. The deck's job is to **assemble a large X-spell into that copy engine and kill the table from one cast**, faster and more reliably than the pod's combo decks go off. You set the clock; they react.

This is a **race**, deliberately. The 2026-05-31 pod-loss review ([[pod_combo_opponent]], [[grand_abolisher_blocks_counters]]) showed that against Grand-Abolisher-protected combo, stacked counterspells are illusory — they're dead on the opponent's turn. The chosen answer is to **out-tempo and out-race**, not to build a static lock. (Defensive/lock options were evaluated and explicitly declined — see Audit Note.)

**Layer 1 — the copy engine.** Azula + **Twinning Staff** = every spell cast in her combat resolves 3×. Flash enablers (Leyline of Anticipation, High Fae Trickster, Borne Upon a Wind) let sorceries join the party.

**Layer 2 — X-spell finishers.** Crackle with Power, Comet Storm, Electrodominance, Banefire. **Only Crackle (5×X to *each* of up to X targets) and multikicked Comet Storm fork damage to the whole table from one instance — the true table-kills.** Electrodominance and Banefire are **single-target**: copies either pile on one opponent (a single-player delete) or spread one each (X per opp). They earn their slots as cheap removal + reach, not as table-wipes. Comet Storm and Electrodominance are instants (no flash enabler needed); Banefire at X≥5 is **uncounterable** — the button for the player behind a counter wall.

**Layer 3 — copy-doublers.** Galvanic Iteration, Increasing Vengeance, Reiterate each multiply the X-spell on top of Azula. One finisher + one doubler in a combat is lethal spread.

**Layer 4 — execution ramp.** Storm-Kiln Artist (Treasure on every cast *and* copy), Goldspan Dragon (Treasures tap for 2), Blazing Firesinger (ritual on a body), Sanar (Treasure), Jeska's Will, and Dirgur Focusmage's cost reduction all spike on the kill turn. The 28-land base + rocks (Signet, Fellwar, both Talismans) + rituals carry the early game.

**Layer 5 — tutors.** Because Azula is always in the command zone, you only need to find **one** finisher. Emeritus of Woe (→ Demonic Tutor, any card), Sanar (→ Wild Idea, any instant/sorcery), and Mystical Teachings (instant-speed) make the kill consistent rather than draw-dependent.

The play pattern: T1–3 ramp and hold interaction; T4 cast Azula; T5+ attack, bank Treasure, tutor toward a finisher, and close on your own turn while the pod is forced to go off into your open mana.

---

## Kill Lines

**Line 1 — Copy-amplified X-spell (primary, 2 cards).** Azula attacking + an X-spell. Crackle is the clean table kill: **X=4 alone = 2 instances × 20 = 40 to each opp (exactly lethal at 14 mana); X=3 with Twinning Staff = 3 × 15 = 45 each (11 mana).** Comet Storm forks too but is mana-hungry (table kill ≈ 18–24 mana); its edge is instant speed. Electrodominance/Banefire are single-target deletes here — point them at one opponent (or Grand Abolisher). Mana from Jeska's Will (doubled mid-combat), Storm-Kiln Treasures, Goldspan, and Ozai's retained red. See `Lightning_War_Speed_Curve_Analysis.md` for the full mana-to-damage table.

**Line 2 — Doubler stack.** X-spell + Galvanic Iteration / Increasing Vengeance / Reiterate during Azula's combat pushes instance count to 4–5; even modest X is lethal. Reiterate buyback chains while Treasures fund it (finite — no infinite-mana enabler).

**Line 3 — Banefire through the wall.** X≥5 Banefire is uncounterable and can't be prevented; a one-player delete that ignores their countermagic. Doubled by Azula with a flash enabler for overkill.

**Line 4 — Graveyard storm (backup).** Flash enabler + Yawgmoth's Will / Past in Flames mid-combat replays the yard, each spell copied. Non-infinite, 40+ damage; vulnerable to Rest in Peace.

---

## Conversion Check Assessment — 19/20 (5/5/4/5)

**Core Loop — 5/5.** Engine is unmistakable from the 99: Azula + Twinning Staff + cast volume, ~28 cards directly serve the burn-finish loop. Functions with or without a flash enabler (instants copy natively).

**Kill Reliability — 5/5.** Two Azula infinite combos (draw-deck + infinite-mana) on top of multiple 2-card X-spell lethals (Crackle / Comet / Electrodominance), copy-doublers, and a **seven-tutor package** (Emeritus of Woe, Sanar, Mystical Teachings, Waterlogged Teachings, Mystical Tutor, Solve the Equation, Merchant Scroll) + Gifts Ungiven. Combo go-off ~52% by T10 (`lw_combo_lab.py`).

**Durability — 4/5.** Premium mana base, commander protection (Mithril Coat, Silver Shroud Costume, Cavern of Souls, Command Beacon), and a Grixis **spell-recursion suite** (Snapcaster Mage, Yawgmoth's Will, Past in Flames, Invoke Calamity) that rebuys a countered/discarded combo piece and powers Gifts' binned pile. Graveyard-hate (Rest in Peace / Leyline of the Void) is the exposure, but the primary combos don't need the yard.

**Interaction — 4/5 (race-led).** 9 counters (3 free: Fierce Guardianship, Force of Negation, Deflecting Swat; + Spell Pierce/Swan Song/Stubborn Denial/Delay/Three Steps Ahead/Narset's Reversal) + Hullbreaker Horror, Vendilion Clique, and burn-as-removal for Grand Abolisher. The 2026-06-19 rebuild **cut the broad removal and the only Abolisher-proof static** (Opposition Agent, V.A.T.S., Toxic Deluge, Snap, Vandalblast): delay_lab measures **−4 to −9pp disruption behind Abolisher**, deliberately traded for an Abolisher-immune combo (the kill is on our turn). Protect-own is strong: Banefire X≥5 is uncounterable under Fierce Guardianship.

---

## Bracket 3 Compliance

**Game Changers (3/3):** Fierce Guardianship, **Mystical Tutor, Gifts Ungiven** (2026-06-19 — the Opposition Agent + Jeska's Will GC slots were re-spent on tutors; see proposal §7–8). Note **Emeritus of Woe // Demonic Tutor is a distinct card not on the GC list** under its spell-half name (see [[sos_prepared_cards_not_on_gc_list]]) — it costs no GC slot.

**Infinite combo:** **Yes — three, pod-approved** [[infinites_ok_in_pod]] (corrected 2026-06-19; the prior "none" claim was wrong; verified vs commanderspellbook.com). (1) **Frantic Search + Narset's Reversal** + Azula attacking → draw the deck → cast a found payoff (CSB-confirmed). (2) **Storm-Kiln Artist + Narset's Reversal** + Azula → infinite mana (CSB-confirmed; needs a spare cheap instant/sorcery in hand). (3) **Seething Song (standalone *or* the Blazing Firesinger half) + Reiterate (buyback)** + Azula → infinite red mana → Comet Storm / Crackle table kill (the Azula instance of CSB's *Reiterate + Seething Song* family — Azula is the copy-enabler, like the listed Bonus Round; net +4 R/loop). All three are Azula-dependent (she copies the loop piece). The deck stays **Bracket 3 by the 3-GC cap**; the pod accepts infinites.

**Extra turns:** None. **Mass land denial:** None. Plays at Bracket-4 spirit via the combo + X-spell burn within the 3-GC cap.

---

## Pod Fit: Tempo Dictation

> **pod_gauntlet net (2026-06-19): the combo-race rebuild lifts P(WIN vs the pod) ~38% → ~64%.**
> Feeding the new combined (combo ∪ race) decap clock + the rebuild's measured disruption into
> `pod_gauntlet.simulate`: the **faster clock buys +30pp** while the lost static costs **−6pp** —
> net **+26pp**, and the deck wins even with Abolisher always out (17%→48%) because the kill is on
> OUR turn (Abolisher only acts on theirs). The build deliberately flips LW from **disruption-led**
> (the old 12% pure-race / 37% win) to **race-led**. Caveat: most of the clock gain is the race
> speeding up (7 tutors + Sol Ring; the lab credits tutors generously) — trust the direction +
> decomposition over the absolute. Full evidence: proposal §13.

1. **You set the clock.** Tutor toward a combo or finisher and kill on **your** turn — Abolisher can't stop a kill cast in your own combat.
2. **Burn doubles as removal.** Kill Grand Abolisher (a 2/2) on sight — Emeritus of Conflict's repeatable Bolt, Electrodominance, Guttersnipe, any X-spell — before it locks your turn.
3. **Banefire ignores counters** (X≥5), and the combo's Comet Storm kills the table from infinite mana — the answer to the counter-wall player.
4. **Gifts Ungiven + recursion** (Yawgmoth's Will / Past in Flames / Invoke Calamity) assembles a combo from the graveyard even when the pile is binned.
5. **Two kill axes** — a fast Azula combo (primary) backed by the X-spell burn race — so a single answer rarely stops both.

---

## Differentiation From Existing Decks

| | Kuja (Genome Project) | Azula (Lightning War) |
|---|---|---|
| Engine timing | Main-phase storm | Combat-phase copy |
| Win condition | Burn + storm count | Azula combo + copy-amplified X-spell |
| Color access | BR | UBR (adds counters) |
| Interaction density | Low | Moderate (9 counters); race-led since the 2026-06-19 rebuild |
| Play pattern | Explosive single turn | Tutor a combo, protect it, kill on your turn |

Azula is the only Grixis deck in the collection. No engine overlap.

---

## Engine Role Map (key cards; full 99 in the `.txt`)

- **Commander:** Fire Lord Azula
- **Combo pieces** (3 lines, verified vs commanderspellbook.com): Narset's Reversal + Frantic Search (draw-deck) · Narset's Reversal + Storm-Kiln Artist (infinite mana) · Reiterate + Seething Song / Blazing Firesinger (infinite red) → Comet Storm / Crackle payoff
- **Copy engine:** Twinning Staff · flash enablers (Leyline of Anticipation, Borne Upon a Wind)
- **X-spell finishers / backup race:** Crackle with Power, Comet Storm, Electrodominance, Banefire · copy-doublers Galvanic Iteration, Increasing Vengeance
- **Pingers / passive burn:** Guttersnipe (2/each), Vivi Ornitier (1/each + ramp), Electrostatic Field (1/each, 0/4 wall) · Emeritus of Conflict // Lightning Bolt
- **Execution ramp:** Sol Ring, Storm-Kiln Artist, Goldspan Dragon, Dark/Desperate Ritual, Seething Song, Sanar's Treasure · cost reduction Dirgur Focusmage // Braingeyser, Nightscape Familiar
- **Tutors (7):** Emeritus of Woe // Demonic Tutor, Mystical Tutor, Gifts Ungiven, Solve the Equation, Merchant Scroll, Mystical Teachings, Waterlogged Teachings, Sanar // Wild Idea
- **Graveyard recursion:** Yawgmoth's Will, Past in Flames, Invoke Calamity, Snapcaster Mage
- **Counters (9):** Fierce Guardianship, Force of Negation, Deflecting Swat, Spell Pierce, Delay, Stubborn Denial, Swan Song, Three Steps Ahead, Narset's Reversal
- **Disruption / removal:** Vendilion Clique, Hullbreaker Horror, Deadly Rollick, Nowhere to Run, Redirect Lightning, Untimely Malfunction
- **Protection:** Mithril Coat, Silver Shroud Costume, March of Swirling Mist
- **Ramp rocks:** Sol Ring, Arcane Signet, Fellwar Stone, Talisman of Dominance, Talisman of Indulgence
- **Lands (~30)** + selection (Ponder, Preordain, Brainstorm, Consider, Frantic Search, Faithless Looting, Valakut Awakening, Sink into Stupor) round out the 99.

---

## Clock Note (2026-06-13, v2)

Kill-turn goldfish (`scripts/lw_clock_lab.py`, 40k; sweep deck 3): **decap median T9** (10% T7, 57% T9, 76% T10), **table-win median ~T13** (33% by T12, 40% never-in-14). *(v1 reported T11/never; corrected after user push-back — v1 swung only Azula's 4 power and omitted Vivi Ornitier (2nd pinger + ramp) and Fated Firepower (damage amplifier). v2 develops the full board + both pingers + the amplifier.)*

This is **not a clean falsification** like Grand Design — it's partly goldfish strictness against a tempo/disruption deck. Two things the goldfish can't see make the real-pod clock faster: (1) the deck's **8-counter disruption** slows *opponents* (the Exile's Return lesson — Favoured on interaction, not the race); (2) goldfish holds a **static 40-life table**, but a real pod arrives at the finish chipped from attacking *each other*, dropping the fork's X (Crackle X=3 = 11 mana from 30; lw_speed_lab @20 = 22% by T7). What *is* model-independent: the from-40 one-cast sweep is 14-mana Crackle, so "T6–7" is the chip-/disruption-assisted clock, **not** a from-full burst. 19/20 stands. Full writeup: `analysis/Lightning_War_Clock_Lab_2026-06-13.md`.

**Update (2026-06-14 — `analysis/Lightning_War_Chip_Model_2026-06-14.md`):** cross-table chip is now modelled (`--mode chipsweep`). It collapses the *table* clock (median T14→T10, never-wipe 40%→1% at moderate 3/turn) while decap barely moves — the from-40 sweep is the ceiling, the chipped finish is the median. This also **retired the standing pinger-add recommendation**: it rested on an always-on abstraction, but a *real* drawn+cast pinger buys only +3pp (`--mode optimize`), and the deck's 3 pingers (Guttersnipe/Vivi/Electrostatic Field) already saturate the incremental-clock lever. The headroom axis is **finisher availability** (`--mode avail`: ceiling 33→73% by T9), which the copy package (Galvanic/Increasing Vengeance/Reiterate + **Twinning Staff**) serves by converting one finisher into a table kill. Applied **−Vedalken Orrery / +Electrostatic Field** — a free cut of the most-redundant enabler (the enabler axis is slack) for a sturdier 0/4 pinger body; ≈ clock-neutral.

## Audit Note (2026-06-07)

Rewritten from the prior "Hybrid Build" summary (CC 18/20) to match the applied **race / burn build** (`lightning-war-20260607-122049.txt`). The Aggravated Assault infinite-combat plan was removed from the deck across three passes (burn pivot → burn v2 → round 2); this summary no longer teaches it. See `Lightning_War_Burn_Pivot_2026-05-31.md` for the full swap history and buy list.

- **Race over lock — confirmed by user.** Restoring a 2nd board wipe (Day of Black Sun) and adding static disruption (Pithing Needle / Trickbind / Tormod's Crypt) were both evaluated and **declined**: the deck is meant to dictate tempo, not grind. (Aven Mindcensor was rejected as a candidate — it's white, illegal in Grixis.) See [[2026-05-31-pod-swaps]].
- **Ramp/tempo impact measured:** 28 lands untouched; mana/Treasure/cost-reduction sources 37→40 (execution-weighted, not earlier acceleration); nonland avg CMC 2.34→2.30; flash density 21→19; creatures 13→15.
- **CC moved 18→19** via Kill Reliability 4→5 (multiple 2-card kills + tutor package). Interaction held at 5/5 despite trimming situational removal (Hydroelectric Specimen, The Last Agni Kai, Observed Stasis, Day of Black Sun cut).
- **GC compliance:** 3/3 unchanged. Emeritus of Woe // Demonic Tutor is GC-free per list-by-name ([[sos_prepared_cards_not_on_gc_list]]).
- **Card count:** 99 main + 1 commander = 100 ✓ (Talisman of Creativity remains in sideboard).
