# Lightning War

## Quick Reference

| Field | Value |
|---|---|
| **Commander** | Fire Lord Azula ({1}{U}{B}{R}, Legendary Creature — Human Noble, 4/4) |
| **Colors** | Grixis (UBR) |
| **Archetype** | Combo-Race spellslinger — Azula infinite combo (primary) + copy-amplified X-spell burn (backup) |
| **Bracket** | 3 by GC count (3/3). B4-in-spirit; infinites pod-approved ([[infinites_ok_in_pod]]); no MLD, no repeatable extra turns. |
| **Game Changers** | Fierce Guardianship, Gifts Ungiven, Mystical Tutor (3 of 3) |
| **Conversion Check** | **19/20 (A)** · audited 2026-06-28 |
| **Kill Window** | Clock: **T8 decap / T9 table** best-line goldfish · burn race ∪ Reiterate/Seething Song combo raced on ONE game (lw_clock_lab.py --mode bestline, 2026-06-28). Race-only was T10/>T14; the combo (CAST ~T9) is the fast table kill. Per-line clocks in Kill Window below. |
| **Status** | built — `lightning-war-20260621.txt` (ground truth) |

-----

## Commander Rules Text

Verified via `card_lookup.py` (2026-06-28).

- **Firebending 2** — *"Whenever this creature attacks, add {R}{R}. This mana lasts until end of combat."* Free red every combat, but it **evaporates at end of combat** — spend it on the kill, not main phase 2.
- **Spell Copy** — *"Whenever you cast a spell while Fire Lord Azula is attacking, copy that spell."* A copy of a permanent spell becomes a token. This is the engine: declare Azula as an attacker and every spell you cast that combat resolves twice (three times with Twinning Staff).
- **Key rulings:** the copy resolves **before** the original; the copy is **not "cast"** (no re-trigger of cast-triggered abilities such as Guttersnipe/Vivi); X values carry to the copy; additional costs paid on the original apply to the copy. Azula only needs to be **declared as an attacker** — she does not need to connect, so blocking her doesn't stop the engine.

Azula is the engine and a combo linchpin (combat is when the deck goes off), but the infinite lines are **commander-independent** once assembled — she accelerates and copies, she isn't a required combo piece.

-----

## What the Deck Does

Lightning War exploits **cast-and-copy volume in Azula's combat**: with Azula attacking (and Twinning Staff out, every spell resolves three times), the deck assembles an **infinite combo and kills the whole table on its own turn**, with a copy-amplified X-spell burn race as the backup. The primary win is a mana/draw loop (Narset's Reversal + Frantic Search/Turnabout, Reiterate + Seething Song, Narset's + Storm-Kiln) poured into a table-wide sink — **Torment of Hailfire** or multikicked **Comet Storm** — so infinite mana means a dead table in one cast. This is deliberately a **race**: the 2026-05-31 pod-loss review ([[pod_combo_opponent]], [[grand_abolisher_blocks_counters]]) showed stacked counters are dead against a Grand-Abolisher-protected combo, so the answer is to out-tempo and close on **your** turn, where Abolisher can't act. Eight tutors plus a Grixis recursion suite make the kill consistent and rebuy pieces lost to interaction; burn doubles as removal to delete Abolisher on sight.

-----

## Kill Lines

**Line 1 — Azula infinite combo (primary, combo):** Assemble a loop — Narset's Reversal + (Frantic Search *or* Turnabout) = draw the deck; Narset's Reversal + Storm-Kiln Artist = infinite mana/Treasure; **Reiterate + Seething Song** (standalone *or* the Blazing Firesinger // Seething Song prepare half) = infinite red mana — then dump into **Torment of Hailfire** / multikicked Comet Storm / Crackle for a table kill. 14 catalogued lines (`find_combos.py`, CSB 2026-06-21); Bonus Round and Turnabout each enable several. Tutor-gated: needs to *find* one loop piece + a sink.

**Line 2 — Copy-amplified X-spell (backup race, 2 cards):** Azula attacking + a finisher, doubled by Twinning Staff / Galvanic Iteration / Increasing Vengeance / Bonus Round. Crackle X=3 with Twinning Staff = 3 × 15 = 45 to each opponent (11 mana); Comet Storm forks at instant speed. No combo required.

**Line 3 — Banefire through the wall (single-target):** X≥5 Banefire is **uncounterable** and can't be prevented — a one-player delete that ignores countermagic. The button for the player behind a counter wall; doubled by Azula + a flash enabler for overkill.

**Line 4 — Graveyard storm (backup, fragile):** flash enabler + Yawgmoth's Will / Past in Flames / Invoke Calamity mid-combat replays the yard, each spell copied — 40+ damage, non-infinite. **Single point of failure:** dies to Rest in Peace / Leyline of the Void.

-----

## Kill Window

Clocks stated separately (the CLAUDE.md verification rule; decap ≠ table):

- **Best-line (the harvested clock — what `pod_gauntlet` now races):** decap **T8** / table **T9** (never-in-14: decap 1% / table 17%) — `lw_clock_lab.py --mode bestline` @8k, 2026-06-28. Backlog #11 (all-finishers MVP): the burn race **and** the combo are raced on the *same* simulated game and the earliest close by either line is reported, so the deck's fastest line (the combo) is no longer flattened out before the gauntlet sees it. The min is over correlated draws on one game, **not** over two labs' independent CDFs (that would be the optimistic-clock disease). This is the headline clock; the rows below are the per-line decomposition.
- **Goldfish (strict from 40, race only):** decap **T10** / table **>T14** (never-in-14: decap 2% / table 58%) — `lw_clock_lab.py --mode clock` @8k, 2026-06-28. The *race-only* ceiling; it slowed vs the prior list because the deck traded a pinger + race slots for combo pieces and tutors. This is the line the best-line clock *replaced* as the harvested curve.
- **Realistic cross-table chip (3/turn, @28 by T6):** decap **T8** / table **T11** — `lw_clock_lab.py --mode chipsweep/amp`. A real pod arrives below 40 from attacking each other, which collapses the *table* clock; this is the honest planning centre.
- **Combo assembly (the fastest table-wide route):** CAST median **T9** (50% by T9, 64% by T12) — `lw_combo_lab.py --mode bench`, current list. Infinite mana → Torment of Hailfire / multikicked Comet Storm kills the table in one cast, so for the *table* the combo (~T9) beats the race table sweep (~T11). The combo is **finding/tutor-gated, not mana-gated** (SEEN≈CAST; selection adds ~0pp).
- **Through interaction:** `pod_gauntlet.py` P(win vs pod) **51%** at Abolisher P(out)=0.3 (best-line clock; 61% at a=0, 42% at a=0.75 — the kill is on our turn, so Abolisher only taxes theirs); two-deck `--matrix` blend **57%** (vs Acererak 60% / H&K 55% / 5C-tail 54%). Folding the combo into the harvested clock lifted LW from a race-axis bottom-feeder to ~4th in the gauntlet (Backlog #11). Trust the direction over the absolute.

-----

## Conversion Check — 19/20 (audited 2026-06-28)

Scored from the list per `reference/REF_The_Conversion_Check.md`. Four judged axes; the clock is measured.

| Axis | Score | Rationale |
|---|---|---|
| **Core Loop** | **5/5** | Engine is unmistakable from the 99: Azula + Twinning Staff + cast volume; ~28 cards serve the combo/burn loop. Instants copy natively; sorceries need a flash enabler. |
| **Kill Reliability** | **5/5** | 14 catalogued infinite lines + multiple 2-card X-spell lethals (Crackle / Comet / Torment), copy-doublers, and an 8-tutor package + Gifts Ungiven. Combo assembly median T9. |
| **Durability** | **4/5** | Premium mana base, commander protection, and a Grixis spell-recursion suite that rebuys countered/discarded pieces. Graveyard hate is the exposure. |
| **Interaction** | **5/5** | 8 counters (3 free) + burn-as-removal + bounce; protect-own is excellent (uncounterable Banefire under Fierce Guardianship; kill is on our turn, Abolisher-immune). Race-led, not stax. |

**Reading:** A-band. The limiting axis is Durability (graveyard-hate exposure on the recursion/storm backup); the primary combos mostly don't need the yard.

-----

## Durability

Recovers well from disruption but not from graveyard exclusion. The mana base is premium (fast-mana + duals + utility lands), the commander has protection (Mithril Coat indestructible auto-attach, Cavern of Souls, Command Beacon to recast Azula), and a four-card Grixis recursion suite (Snapcaster Mage, Yawgmoth's Will, Past in Flames, Invoke Calamity) rebuys a countered or discarded combo piece and powers the Gifts Ungiven pile. After a turn-7 wipe the deck re-threatens in 1–2 turns because the kill needs only Azula (command zone) + one found piece. The hard stop is **Rest in Peace / Leyline of the Void**, which turns off the storm-recursion backup and Gifts — but the workhorse mana/draw combos don't rely on the yard, so it slows rather than stops the deck.

-----

## Interaction Package

**~13 dedicated pieces.** Counters: **8** — Fierce Guardianship (free), Force of Negation (free), Deflecting Swat (free), Spell Pierce, Delay, Stubborn Denial, Swan Song, Three Steps Ahead (+ Narset's Reversal as a soft counter/combo piece). Removal: **burn-as-removal** (Banefire, Electrodominance, Guttersnipe, Emeritus of Conflict) + Deadly Rollick + Hullbreaker Horror (bounce). Targeted disruption: Vendilion Clique, Untimely Malfunction. Instant speed: **most of it** — counters, Rollick, Hullbreaker, and (with a flash enabler) the burn all operate on opponents' turns; the deck itself develops in *its own* combat.

-----

## Known Weaknesses

- **Graveyard hate** (Rest in Peace / Leyline of the Void) shuts the storm-recursion backup and the Gifts pile. Primary combos survive it, but the safety net is gone.
- **Slow as a pure race now** — strict-goldfish table clock is never-in-14 from 40. The deck *needs* the combo (~T9) or a pre-chipped pod (table T11); a grindy, low-aggression table that stays near 40 and disrupts your tutors stretches the table clock badly.
- **Tutor/finding-gated combo** — assembly is bound by drawing/tutoring a loop piece (not mana). Stack interaction or removal aimed at your 8 tutors delays the kill.
- **Creature-light, few blockers** — go-wide aggro can pressure you or race; the plan is to answer/kill, not block.
- **Grand Abolisher / Drannith** must be killed on sight (burn doubles as removal); the on-your-turn kill dodges Abolisher's tax but you still have to deploy into it.

-----

## Don't-Miss Rulings

Verified via `card_lookup.py` (read the card + rulings).

- **Copies aren't "cast"** — Azula's copies (and Reiterate / Narset's Reversal copies) do **not** re-trigger cast-triggered abilities (Guttersnipe, Vivi, Aria-style pingers); X values carry; additional costs paid on the original apply to the copy. This is why the pingers can't be "looped" by the copy combos.
- **Azula's firebending mana vanishes at end of combat** — *"this mana lasts until end of combat."* Spend the {R}{R} on the kill spell during her attack; it does not carry to main phase 2.
- **Azula only copies while attacking** — sorcery X-spells (Crackle, Banefire, Torment of Hailfire) need a flash enabler to be cast during combat; instant X-spells (Comet Storm, Electrodominance) don't.
- **Twinning Staff adds +1 to every copy event** — Azula makes 2 copies (3 total), and each copy-doubler likewise; it also amplifies copied cantrips, rituals, and Storm-Kiln triggers.
- **Prepare cards** (Blazing Firesinger // Seething Song, Sanar, Emeritus of Woe, Emeritus of Conflict): a prepare card is a **creature in hand** and can only be cast with its base (creature) characteristics — the spell half (e.g. Seething Song) is castable only **after** the creature is in play and prepared. Casting that prepared copy **is a cast** (Azula copies it, cast-triggers fire), and the creature **stays** (just unprepared). The deck also runs a *standalone* Seething Song instant that any I/S tutor reaches directly.
- **Storm-Kiln Artist makes a Treasure on every cast AND every copy** — a 3-spell Azula combat banks a pile of Treasures.

-----

## Decklist (100 cards)

### Commander (1)
- Fire Lord Azula

### Infinite Combo & Copy-Doublers (8)
- Twinning Staff
- Bonus Round
- Galvanic Iteration
- Increasing Vengeance
- Narset's Reversal
- Reiterate
- Turnabout
- Expansion // Explosion

### Flash Enablers (3)
- Leyline of Anticipation
- Borne Upon a Wind
- Cunning Nightbonder

### X-Spell Finishers (5)
- Banefire
- Comet Storm
- Crackle with Power
- Electrodominance
- Torment of Hailfire

### Pingers / Passive Burn (4)
- Guttersnipe
- Vivi Ornitier
- Thunderdrum Soloist
- Emeritus of Conflict

### Execution Ramp / Rituals (7)
- Blazing Firesinger
- Dark Ritual
- Desperate Ritual
- Seething Song
- Storm-Kiln Artist
- Goldspan Dragon
- Nightscape Familiar

### Mana Rocks (5)
- Sol Ring
- Arcane Signet
- Fellwar Stone
- Talisman of Dominance
- Talisman of Indulgence

### Tutors (8)
- Emeritus of Woe
- Sanar, Unfinished Genius
- Mystical Tutor  *(GC)*
- Gifts Ungiven  *(GC)*
- Solve the Equation
- Merchant Scroll
- Mystical Teachings
- Waterlogged Teachings

### Graveyard Recursion (5)
- Yawgmoth's Will
- Past in Flames
- Invoke Calamity
- Snapcaster Mage
- Agadeem's Awakening

### Counterspells (8)
- Fierce Guardianship  *(GC)*
- Force of Negation
- Deflecting Swat
- Spell Pierce
- Delay
- Stubborn Denial
- Swan Song
- Three Steps Ahead

### Disruption / Removal (5)
- Deadly Rollick
- Untimely Malfunction
- Sink into Stupor
- Hullbreaker Horror
- Vendilion Clique

### Protection (3)
- Mithril Coat
- March of Swirling Mist
- Malakir Rebirth

### Card Selection / Draw (7)
- Brainstorm
- Consider
- Ponder
- Preordain
- Faithless Looting
- Frantic Search
- Valakut Awakening

### Lands (31)
- Arena of Glory
- Blood Crypt
- Bojuka Bog
- Cascade Bluffs
- Cavern of Souls
- Command Beacon
- Command Tower
- Fiery Islet
- Gemstone Caverns
- Haunted Ridge
- Horizon of Progress
- Island
- Lindblum, Industrial Regency
- Luxury Suite
- Misty Rainforest
- Morphic Pool
- Mount Doom
- Mountain
- Otawara, Soaring City
- Plaza of Heroes
- Polluted Delta
- Reflecting Pool
- Scalding Tarn
- Shipwreck Marsh
- Starting Town
- Steam Vents
- Stormcarved Coast
- Talon Gates of Madara
- Training Center
- Watery Grave
- Xander's Lounge

*(Functional buckets total 99 + commander = 100. The dated `.txt` is ground truth; this supplies labels only.)*

-----

## Piloting Notes (for borrowers)

**Mulligan.** Keep lands + early ramp + a route to Azula on T4, ideally with a piece of interaction. A flash enabler or finisher is gravy — you tutor for whatever's missing. Toss no-land hands and all-air hands with no early plays. A tutor (Mystical Tutor, Merchant Scroll, Gifts Ungiven, Solve the Equation) is the best card in an opener — the Reiterate + Seething Song combo (~T9) is the deck's real table clock, and finders outrank raw burn in the keep decision.

**Threat assessment & lines:**

- **You set the clock.** Tutor toward a loop piece + a sink and kill on **your** turn — Abolisher can't stop a kill cast in your own combat.
- **Burn doubles as removal** — kill Grand Abolisher (a 2/2) on sight (Emeritus of Conflict's Bolt, Electrodominance, Guttersnipe, any X-spell) before it locks your turn.
- **Banefire X≥5 ignores counters**, and the combo dumps into Torment of Hailfire / Comet Storm for the table — the answer to the counter-wall player.
- **Gifts Ungiven + recursion** (Yawgmoth's Will / Past in Flames / Invoke Calamity) assembles a combo from the graveyard even when the pile is binned.
- **Two kill axes split hate** — graveyard/stack hate aimed at the combos still leaves the finite copy-scaled X-spell, and vice versa.

-----

## Changelog

- **2026-06-28 (all-finishers MVP, Backlog #11):** The harvested clock `pod_gauntlet` races is now the **best-line** curve (`lw_clock_lab.py --mode bestline`): the burn race and the Reiterate/Seething Song combo run on the *same* simulated game and the earliest decap/table by either line is reported (correlated draws, not independent CDFs). Headline clock moved **T10/>T14 → T8/T9**; LW rose from a race-axis bottom-feeder to ~4th in the gauntlet (P(win) ~51% @a=0.3). The burn lab gained a `bestline` mode that injects a shared opening hand into both `goldfish_kill` and `lw_combo_lab.assembly_turn`; the combo lab's tutor picks were made hash-seed-deterministic so the golden snapshot is reproducible. Tournament/dashboard code unchanged — they still consume one curve; the curve just stopped hiding the combo.
- **2026-06-28:** Repointed `lw_clock_lab.py` to the current `lightning-war-20260621` list (was the archived 20260614); strict-goldfish clock is now decap T10 / table >T14 (the deck leaned combo, so the race-only clock slowed). Corrected the framing: the infinite-mana combo (~T9) is the **fastest table-wide kill**, not the race table sweep (~T11). Removed a wrong-card ("Ozai") ruling. Rebuilt the Summary onto the canonical template schema.
- **2026-06-21:** Combo-consistency pass — added a standalone Seething Song + tutor/selection density (combo assembly: never-in-horizon → median T9) and combo glue (Bonus Round / Turnabout / Expansion); swapped two weak slots + board-answer cards for payoff/combo within the 3-GC cap.
