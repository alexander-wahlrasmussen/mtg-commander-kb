# Lightning War — Fire Lord Azula (Combo-Race Build)

**Commander:** Fire Lord Azula ({1}{U}{B}{R}, 4/4, Legendary Creature — Human Noble)
**Colors:** Grixis (UBR)
**Archetype:** Spellslinger **combo-race** — Azula infinite combo (primary) + copy-amplified X-spell burn (backup)
**Role:** pulled to **race the combo pod** — out-tempo a Grand-Abolisher-protected combo rather than disrupt through it ([[bracket_4_in_spirit]], [[grand_abolisher_blocks_counters]])
**Bracket:** 3 (3 of 3 Game Changer slots used; **infinite combos present — pod-approved** [[infinites_ok_in_pod]]; no MLD; no extra turns)
**Game Changers (3/3):** Fierce Guardianship, Mystical Tutor, Gifts Ungiven
**Conversion Check:** 19/20 (5/5/4/5)
**Kill Window:** `Clock: T8 decap / T11 table (lw_clock_lab.py, chip 3/turn, 2026-06-21); combo assembly median T9 (lw_combo_lab.py, 2026-06-21); 14 catalogued infinite combos (commanderspellbook.com via find_combos.py, 2026-06-21).` Comet Storm and the infinite-mana lines kill at instant speed in Azula's combat; the sorcery X-spells (Crackle / Banefire / Torment of Hailfire) need a flash enabler to fire mid-combat. **pod_gauntlet P(WIN vs pod) ~64%** (race-led; `pod_gauntlet.py`).
**Current decklist:** `lightning-war-20260621.txt` — the `.txt` is ground truth, this is commentary. (Prior `20260619` build archived; the 2026-06-21 pass swapped two weak slots + three board-answer cards for stronger payoff/combo cards within the 3-GC cap.)

---

## Commander Rules Text

- **Firebending 2:** Whenever Azula attacks, add {R}{R}. **This mana lasts until end of combat** — it evaporates before main phase 2 unless spent in the combat.
- **Spell Copy:** Whenever you cast a spell while Azula is attacking, copy that spell (you may choose new targets). A copy of a permanent spell becomes a token.
- **Key rulings:** The copy resolves before the original. Copies are **not "cast"** (no re-trigger of cast-triggered abilities like Guttersnipe). X values are preserved. Additional costs paid on the original apply to the copy. **Azula only needs to be *declared as an attacker* to copy — she does not need to connect**, so blocking her doesn't stop the engine.

---

## What the Deck Is Trying to Do

Azula turns your combat into the most dangerous part of the turn: every instant/sorcery cast while she attacks is copied — instants natively, sorceries once a flash enabler is online — and Twinning Staff makes every copy event **+1**. The deck's primary plan is to **assemble an Azula infinite combo and kill the table on your own turn**, faster and more reliably than the pod's combo decks go off, with a copy-amplified X-spell burn race as the backup. You set the clock; they react.

This is a **race**, deliberately. The 2026-05-31 pod-loss review ([[pod_combo_opponent]], [[grand_abolisher_blocks_counters]]) showed that against Grand-Abolisher-protected combo, stacked counterspells are illusory — they're dead on the opponent's turn. The chosen answer is to **out-tempo and out-race**, not to build a static lock.

**Layer 1 — the copy engine.** Azula + **Twinning Staff** = every spell cast in her combat resolves 3×. Flash enablers (Leyline of Anticipation, Borne Upon a Wind) let sorceries join. Cunning Nightbonder makes your flash spells cost less and uncounterable.

**Layer 2 — the infinite combo (primary kill).** 14 catalogued infinite lines (CSB 2026-06-21). The workhorse trio: **Narset's Reversal + (Frantic Search *or* Turnabout)** → draw the deck; **Narset's Reversal + Storm-Kiln Artist** → infinite mana + Treasures; **Reiterate + Seething Song** (standalone or the Blazing Firesinger half) → infinite red mana. Each dumps into a table-finisher. **Bonus Round, Turnabout, and Expansion // Explosion** are the glue that multiplies the catalogued count (Bonus Round alone enables four lines).

**Layer 3 — X-spell finishers (combo payoff + backup race).** **Torment of Hailfire** is the premier infinite-mana sink — each opponent loses 3 per X, can't be prevented, forces sacrifice/discard: the cleanest "infinite mana = dead table" button. Crackle with Power (5×X to each of up to X targets) and multikicked Comet Storm fork to the whole table; Electrodominance and Banefire are single-target deletes (point them at one opponent or Grand Abolisher). Comet Storm/Electrodominance are instants (no enabler needed); **Banefire at X≥5 is uncounterable** — the button for the player behind a counter wall.

**Layer 4 — copy-doublers.** Galvanic Iteration, Increasing Vengeance, Bonus Round, Expansion // Explosion each multiply the finisher/loop on top of Azula.

**Layer 5 — execution ramp.** Storm-Kiln Artist (Treasure on every cast *and* copy), Goldspan Dragon (Treasures tap for 2), Blazing Firesinger (ritual on a body), Sanar (Treasure), Dark/Desperate Ritual, Seething Song, and Nightscape Familiar's cost reduction all spike on the kill turn. Lands + rocks (Sol Ring, Signet, Fellwar, both Talismans) carry the early game.

**Layer 6 — tutors (8).** Because Azula is always in the command zone, you only need **one** combo piece or finisher. Emeritus of Woe (→ Demonic Tutor, any card), Sanar (→ Wild Idea, any I/S), Mystical Teachings, Waterlogged Teachings, Mystical Tutor, Solve the Equation, Merchant Scroll, and Gifts Ungiven make the kill consistent.

The play pattern: T1–3 ramp and hold interaction; T4 cast Azula; T5+ attack, bank Treasure, tutor toward a combo or finisher, and close on your own turn while the pod is forced to go off into your open mana.

---

## Kill Lines

**Line 1 — Azula infinite combo (primary).** The workhorse trio (draw-deck / infinite mana / infinite red) → dump into **Torment of Hailfire**, Comet Storm, or Crackle for a table kill. 14 catalogued lines (`find_combos.py`, CSB 2026-06-21); Bonus Round and Turnabout each enable several.

**Line 2 — Copy-amplified X-spell (backup race, 2 cards).** Azula attacking + a finisher, doubled by Twinning Staff / Galvanic Iteration / Increasing Vengeance / Bonus Round / Expansion. Crackle X=3 with Twinning Staff = 3 × 15 = 45 to each opp (11 mana); Comet Storm forks at instant speed.

**Line 3 — Banefire through the wall.** X≥5 Banefire is uncounterable and can't be prevented; a one-player delete that ignores their countermagic. Doubled by Azula with a flash enabler for overkill.

**Line 4 — Graveyard storm (backup).** Flash enabler + Yawgmoth's Will / Past in Flames / Invoke Calamity mid-combat replays the yard, each spell copied. Non-infinite, 40+ damage; vulnerable to Rest in Peace.

---

## Conversion Check Assessment — 19/20 (5/5/4/5)

**Core Loop — 5/5.** Engine is unmistakable from the 99: Azula + Twinning Staff + cast volume; ~28 cards directly serve the combo/burn loop. Functions with or without a flash enabler (instants copy natively).

**Kill Reliability — 5/5.** **14 catalogued infinite combos** on top of multiple 2-card X-spell lethals (Crackle / Comet / Torment of Hailfire), copy-doublers, and an **eight-tutor package** (Emeritus of Woe, Sanar, Mystical Teachings, Waterlogged Teachings, Mystical Tutor, Solve the Equation, Merchant Scroll) + Gifts Ungiven. Combo assembly median **T9** (`lw_combo_lab.py`).

**Durability — 4/5.** Premium mana base, commander protection (Mithril Coat indestructible, Cavern of Souls, Command Beacon), and a Grixis **spell-recursion suite** (Snapcaster Mage, Yawgmoth's Will, Past in Flames, Invoke Calamity) that rebuys a countered/discarded combo piece and powers Gifts' binned pile. Graveyard-hate (Rest in Peace / Leyline of the Void) is the exposure, but the primary combos don't need the yard.

**Interaction — 4/5 (race-led).** 9 counters (3 free: Fierce Guardianship, Force of Negation, Deflecting Swat; + Spell Pierce / Swan Song / Stubborn Denial / Delay / Three Steps Ahead / Narset's Reversal) + Hullbreaker Horror, Vendilion Clique, Deadly Rollick, and burn-as-removal for Grand Abolisher. The 2026-06-21 strengthening swapped board-answer fat (Nowhere to Run, Redirect Lightning) for combo glue — interaction density is unchanged. Protect-own is strong: Banefire X≥5 is uncounterable under Fierce Guardianship, and the kill is on **our** turn (Abolisher-immune).

---

## Bracket 3 Compliance

**Game Changers (3/3):** Fierce Guardianship, Mystical Tutor, Gifts Ungiven. **Emeritus of Woe // Demonic Tutor is a distinct card not on the GC list** under its spell-half name ([[sos_prepared_cards_not_on_gc_list]]) — it costs no GC slot. The 2026-06-21 adds (Thunderdrum Soloist, Torment of Hailfire, Bonus Round, Expansion // Explosion, Turnabout) are all non-GC; the cap is unchanged.

**Infinite combo:** **Yes — 14 catalogued, pod-approved** [[infinites_ok_in_pod]] (verified vs commanderspellbook.com, 2026-06-21). The three workhorses: (1) **Narset's Reversal + Frantic Search** + Azula → draw the deck → cast a found payoff; (2) **Narset's Reversal + Storm-Kiln Artist** + Azula → infinite mana/Treasure; (3) **Reiterate + Seething Song** (standalone *or* the Blazing Firesinger half) + Azula → infinite red mana → Comet Storm / Crackle / Torment table kill. Glue: **Bonus Round** adds four lines (Reiterate+Seething Song, Reiterate+Desperate Ritual, Narset's+Storm-Kiln, Invoke Calamity+Narset's), **Turnabout** two, **Expansion // Explosion** one. The deck stays **Bracket 3 by the 3-GC cap**; the pod accepts infinites.

**Extra turns:** None. **Mass land denial:** None. Plays at Bracket-4 spirit via the combo + X-spell burn within the 3-GC cap.

---

## Pod Fit: Tempo Dictation

> **pod_gauntlet (race-led rebuild): P(WIN vs the pod) ~64%** (`pod_gauntlet.py`). The faster combined (combo ∪ race) clock buys the win even with Abolisher always out (~48%), because the kill is on **OUR** turn — Abolisher only acts on theirs. Most of the clock credit is the race speeding up (tutors + Sol Ring; the lab credits tutors generously) — trust the direction over the absolute.

1. **You set the clock.** Tutor toward a combo or finisher and kill on **your** turn — Abolisher can't stop a kill cast in your own combat.
2. **Burn doubles as removal.** Kill Grand Abolisher (a 2/2) on sight — Emeritus of Conflict's repeatable Bolt, Electrodominance, Guttersnipe, any X-spell — before it locks your turn.
3. **Banefire ignores counters** (X≥5), and the combo dumps into Torment of Hailfire / Comet Storm for the table — the answer to the counter-wall player.
4. **Gifts Ungiven + recursion** (Yawgmoth's Will / Past in Flames / Invoke Calamity) assembles a combo from the graveyard even when the pile is binned.
5. **Two kill axes** — a fast Azula combo (primary) backed by the X-spell burn race — so a single answer rarely stops both.

---

## Differentiation From Existing Decks

| | Kuja (Genome Project) | Azula (Lightning War) |
|---|---|---|
| Engine timing | Main-phase storm | Combat-phase copy |
| Win condition | Burn + storm count | Azula combo + copy-amplified X-spell |
| Color access | BR | UBR (adds counters) |
| Interaction density | Low | Moderate (9 counters); race-led |
| Play pattern | Explosive single turn | Tutor a combo, protect it, kill on your turn |

Azula is the only Grixis deck in the collection. No engine overlap.

---

## Engine Role Map (key cards; full 99 in the `.txt`)

- **Commander:** Fire Lord Azula
- **Combo pieces** (14 catalogued lines, verified vs commanderspellbook.com): Narset's Reversal · Frantic Search · Turnabout · Storm-Kiln Artist · Reiterate · Seething Song / Blazing Firesinger · Bonus Round · Expansion // Explosion · Twinning Staff · Hullbreaker Horror (+ Sol Ring)
- **Copy engine:** Twinning Staff · flash enablers (Leyline of Anticipation, Borne Upon a Wind) · Cunning Nightbonder (flash cost + uncounterable)
- **X-spell finishers / backup race:** Torment of Hailfire, Crackle with Power, Comet Storm, Electrodominance, Banefire, Expansion // Explosion · copy-doublers Galvanic Iteration, Increasing Vengeance, Bonus Round
- **Pingers / passive burn:** Guttersnipe (2/each), Vivi Ornitier (1/each + ramp), Thunderdrum Soloist (1/each; 3 on a 5+-mana spell) · Emeritus of Conflict // Lightning Bolt
- **Execution ramp:** Sol Ring, Storm-Kiln Artist, Goldspan Dragon, Dark/Desperate Ritual, Seething Song, Sanar's Treasure · cost reduction Nightscape Familiar
- **Tutors (8):** Emeritus of Woe // Demonic Tutor, Sanar // Wild Idea, Mystical Tutor, Gifts Ungiven, Solve the Equation, Merchant Scroll, Mystical Teachings, Waterlogged Teachings
- **Graveyard recursion:** Yawgmoth's Will, Past in Flames, Invoke Calamity, Snapcaster Mage
- **Counters (9):** Fierce Guardianship, Force of Negation, Deflecting Swat, Spell Pierce, Delay, Stubborn Denial, Swan Song, Three Steps Ahead, Narset's Reversal
- **Disruption / removal:** Vendilion Clique, Hullbreaker Horror, Deadly Rollick, Untimely Malfunction
- **Protection:** Mithril Coat, March of Swirling Mist
- **Ramp rocks:** Sol Ring, Arcane Signet, Fellwar Stone, Talisman of Dominance, Talisman of Indulgence
- **Lands (~30)** + selection (Ponder, Preordain, Brainstorm, Consider, Frantic Search, Faithless Looting, Valakut Awakening, Sink into Stupor) round out the 99.

---

## Clock & Evidence (2026-06-21)

Two clocks, stated separately (the CLAUDE.md verification rule):

- **Combo assembly (primary kill):** `lw_combo_lab.py`, 20k, seed 20260621 — median **T9** (by-T10 55%, by-T12 64%). The combo is tutor-gated, not dig-gated; the 2026-06-21 glue (Bonus Round / Turnabout / Expansion) lifted the median one turn and raised the CSB combo count 7 → 14.
- **Burn race (backup):** `lw_clock_lab.py`, chip 3/turn, 20k, seed 20260621 — **decap median T8 / table median T11**. The from-40 one-cast table sweep is the ceiling; cross-table chip collapses the *table* clock to the median (a real pod arrives below 40 from attacking each other). Finisher **availability** is the headroom axis, which the copy package + the eight tutors serve; the three pingers (Guttersnipe / Vivi / Thunderdrum Soloist) saturate the incremental-chip lever.

Scripts are the permanent provenance; the superseded 06-13/06-14 writeups and the 06-18 rebuild proposal are in `archive/`.

## Decklist (100 cards)

### Commander (1)
1 Fire Lord Azula

### Infinite Combo & Copy-Doublers (8)
1 Twinning Staff
1 Bonus Round
1 Galvanic Iteration
1 Increasing Vengeance
1 Narset's Reversal
1 Reiterate
1 Turnabout
1 Expansion // Explosion

### Flash Enablers (3)
1 Leyline of Anticipation
1 Borne Upon a Wind
1 Cunning Nightbonder

### X-Spell Finishers (5)
1 Banefire
1 Comet Storm
1 Crackle with Power
1 Electrodominance
1 Torment of Hailfire

### Pingers / Passive Burn (4)
1 Guttersnipe
1 Vivi Ornitier
1 Thunderdrum Soloist
1 Emeritus of Conflict

### Execution Ramp / Rituals (7)
1 Blazing Firesinger
1 Dark Ritual
1 Desperate Ritual
1 Seething Song
1 Storm-Kiln Artist
1 Goldspan Dragon
1 Nightscape Familiar

### Mana Rocks (5)
1 Sol Ring
1 Arcane Signet
1 Fellwar Stone
1 Talisman of Dominance
1 Talisman of Indulgence

### Tutors (8)
1 Emeritus of Woe
1 Sanar, Unfinished Genius
1 Mystical Tutor
1 Gifts Ungiven
1 Solve the Equation
1 Merchant Scroll
1 Mystical Teachings
1 Waterlogged Teachings

### Graveyard Recursion (5)
1 Yawgmoth's Will
1 Past in Flames
1 Invoke Calamity
1 Snapcaster Mage
1 Agadeem's Awakening

### Counterspells (8)
1 Fierce Guardianship
1 Force of Negation
1 Deflecting Swat
1 Spell Pierce
1 Delay
1 Stubborn Denial
1 Swan Song
1 Three Steps Ahead

### Disruption / Removal (5)
1 Deadly Rollick
1 Untimely Malfunction
1 Sink into Stupor
1 Hullbreaker Horror
1 Vendilion Clique

### Protection (3)
1 Mithril Coat
1 March of Swirling Mist
1 Malakir Rebirth

### Card Selection / Draw (7)
1 Brainstorm
1 Consider
1 Ponder
1 Preordain
1 Faithless Looting
1 Frantic Search
1 Valakut Awakening

### Lands (31)
1 Arena of Glory
1 Blood Crypt
1 Bojuka Bog
1 Cascade Bluffs
1 Cavern of Souls
1 Command Beacon
1 Command Tower
1 Fiery Islet
1 Gemstone Caverns
1 Haunted Ridge
1 Horizon of Progress
1 Island
1 Lindblum, Industrial Regency
1 Luxury Suite
1 Misty Rainforest
1 Morphic Pool
1 Mount Doom
1 Mountain
1 Otawara, Soaring City
1 Plaza of Heroes
1 Polluted Delta
1 Reflecting Pool
1 Scalding Tarn
1 Shipwreck Marsh
1 Starting Town
1 Steam Vents
1 Stormcarved Coast
1 Talon Gates of Madara
1 Training Center
1 Watery Grave
1 Xander's Lounge

## Don't-Miss Rulings

- **Copies aren't "cast"** — they don't re-trigger Azula or magecraft; X values carry; additional costs paid on the original apply to the copy.
- **Azula only copies while attacking.** Sorcery X-spells (Crackle, Banefire) need a flash enabler to be cast during combat; instant X-spells (Comet Storm, Electrodominance) don't.
- **Twinning Staff adds +1 to every copy event** — Azula makes 2 copies (3 total), and each copy-doubler likewise.
- **Prepared cards** (Sanar, Emeritus of Conflict, Emeritus of Woe, Blazing Firesinger): casting the prepared copy **is a cast** — Azula copies it, magecraft triggers (Storm-Kiln, Guttersnipe), and the creature **stays** afterward.
- **Ozai retains all unspent mana as red** to fund the X-spell mid-combat; firebending mana otherwise vanishes at end of combat.
- **Storm-Kiln Artist makes a Treasure on every cast AND every copy** — a 3-spell Azula combat nets a pile of Treasures.

## Piloting Notes (for borrowers)

**Mulligan.** Looking for **lands + early ramp + a route to Azula on T4**, ideally with one piece of interaction. A flash enabler or a finisher is gravy — you tutor for whatever's missing.

- **Keep:** ramp/rocks + a counter or two + a path to Azula.
- **Toss:** no-land hands; all-air hands with no early plays.

**Threats & timing.**

- **Interaction is still your backbone** — 8 counters (3 free: Fierce Guardianship, Force of Negation, Deflecting Swat) + removal that doubles as burn. Hold it up on opponents' turns; the deck develops in *your* combat.
- **Rest in Peace / Leyline of the Void** shut off the graveyard-storm backup line — but the primary X-spell kill doesn't need the yard. Fall back on Crackle/Comet/Banefire + copy-doublers.
- **Two ways to close, so hate splits** — the deck has 14 catalogued infinite lines (workhorse: Reiterate + Seething Song → infinite red mana; verified vs commanderspellbook.com 2026-06-21, pod-approved) *and* a finite copy-scaled X-spell that needs no combo. Graveyard/stack hate aimed at the combos still leaves the "just a big burn spell" kill — and vice versa.
