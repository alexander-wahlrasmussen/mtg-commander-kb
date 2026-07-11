# The Exile's Return — Fire Lord Zuko

## Quick Reference

| Field | Value |
|---|---|
| **Commander** | Fire Lord Zuko ({R}{W}{B}, 2/4 Legendary Creature — Human Noble Ally) |
| **Colors** | Mardu (RWB) |
| **Archetype** | Exile-matters / blink-and-impulse value engine with firebending finisher |
| **Bracket** | 3 (3 Game Changers used; no early two-card infinites; no MLD; no extra turns) |
| **Game Changers** | Aang's Shelter (= Teferi's Protection), Enlightened Tutor, Jeska's Will (3 of 3 slots used). *Deflecting Swat is in the deck but no longer a GC after the Oct 2025 delisting.* |
| **Conversion Check** | **17/20** (5/4/4/4) |
| **Kill Window** | Goldfish: T7–8 (one player) / T10 (table) **(board)** · Through interaction: T8–11 — corrected 2026-06-09 by `scripts/er_speed_lab.py`; the old "T6–8" was ~1 turn optimistic at the front edge (T6 ≈ 9% even unblocked). **Re-run 2026-07-10 on the -20260710 list @40k — clock-neutral** (decap T8, 78% by T8; table T10). See `analysis/Exiles_Return_Speed_Curve_Analysis.md` |
| **Ramp** | 13 sources (2 burst / 11 repeatable) · 50 mana sources, 37 land · in band (`ramp_audit.py` 2026-06-21) |

-----

## Commander Rules Text

Fire Lord Zuko has two abilities:

1. **Firebending X**, where X is Zuko's power. *"Whenever this creature attacks, add X {R}. This mana lasts until end of combat."* Base 2/4 → attack adds {R}{R}; counters scale this up.
2. **Dual exile trigger:** *"Whenever you cast a spell from exile and whenever a permanent you control enters from exile, put a +1/+1 counter on each creature you control."*

Key reading: trigger #2 fires on **two distinct events**, and an airbended-then-recast permanent fires *both* — once on cast, once on ETB. The counter goes on **each creature you control**, not just one — every flicker compounds the whole board. Reanimation from the graveyard (Karmic Guide, Sun Titan returning a creature, Reanimate-style spells) does **not** trigger #2 — that's "from graveyard," not "from exile."

-----

## What the Deck Does

The deck converts exile-zone interactions into a board-wide +1/+1 counter engine that feeds firebending mana, then closes with combat damage. Engine pieces split across three sub-systems:

**Layer 1 — Cast-From-Exile Sources (8 in main 99):** These exile cards from your library and let you cast them later, firing trigger #1 each time the exiled card is cast.
- *Impulse draw:* Light Up the Stage (exile 2, spectacle for {R} after any opp loses life), Prosper, Tome-Bound (exile 1 at end step + Treasure on every play-from-exile), Laelia, the Blade Reforged (exile 1 on attack + grow herself), Zuko, Exiled Prince (pay {3}: exile 1 — note this is a **second Zuko** in the 99, not the commander), The Legend of Roku I (exile 3), Jeska's Will mode 2 (exile 3, both modes if commander out), Professional Face-Breaker (sac Treasure → exile 1).
- *Foretell:* Sozin's Comet (pay {2} to exile face-down, cast for its foretell cost {2}{R} later — counts as cast-from-exile and grants firebending 5 to all creatures that turn; hardcast is {3}{R}{R}. Costs corrected 2026-06-09 — a previous version had them inverted).
- *Sideboard alternate:* Outpost Siege (Khans mode = recurring impulse draw) is in the SB; Roku and Yangchen cover the recurring impulse-draw role in the main.

**Layer 2 — Airbend (4) — fires both triggers:** Airbend = exile a permanent; while exiled, owner may cast it for {2} instead of its mana cost. The recast fires trigger #1 (cast from exile) and the new ETB fires trigger #2 (permanent enters from exile). Airbend payers in this deck: Avatar's Wrath (mass airbend opponents' creatures + lock on non-hand casting), Monk Gyatso (airbend your creature when it's targeted — protection), The Legend of Yangchen II/III into Avatar Yangchen (airbend on second-spell-each-turn), Appa, Steadfast Guardian (airbend your nonland permanents on ETB + 1/1 token whenever you cast from exile). Airbending a 6-mana bomb to recast for {2} is mana-efficient; airbending an opponent's creature with Avatar's Wrath only fires Zuko if the opponent chooses to recast it (rare).

**Layer 3 — Flicker / Blink (11) — fires trigger #2:** Permanents leave to exile and return = ETB from exile.
- *Universal blink:* Felidar Guardian (any permanent), Flickerwisp (any permanent until next end step), Eldrazi Displacer ({2}{C}: any creature, repeatable), Charming Prince mode 3 (exile a creature you own — works on opponent-controlled creatures of your own).
- *Creature blink:* Restoration Angel (non-Angel), Ephemerate (with Rebound = two triggers), Eerie Interlude (any number, EOT return), Semester's End (any number + extra +1/+1 counter on each), Teleportation Circle (one artifact/creature each end step, recurring). *(Cloudshift cut 2026-07-10 — the 12th blink piece, one-shot with no rebound, traded for a payoff.)*
- *Doubler:* Panharmonicon — when the entering permanent is a creature or artifact, Zuko's trigger #2 fires twice. Norin returning under Panharmonicon = +2/+2 to each creature per cycle.
- *Enchantment engine:* Airbender Ascension (exile target creature on ETB; counts quest counters from creatures ETBing; at 4 counters, exile-and-return your own creature each end step).
- *Self-blink:* Norin the Wary (exiles itself when ANY player casts a spell or attacks — returns next end step; under Panharmonicon, doubles).

**Mass-cast-from-exile blowouts:** Sozin's Comet (firebending 5 on every creature for the turn) + Hellkite Charger + 4 attackers = 20 R floor, easily funding repeated extra combats. The Legend of Roku I (exile top 3) followed by Jeska's Will (exile top 3, both modes) often dumps 6 cards into exile in one turn; counters build sharply as each is cast.

**Tutors and selection:** Enlightened Tutor (artifact/enchantment to top — find Panharmonicon, Airbender Ascension, Teleportation Circle, Lightning Greaves; it **cannot** find Sozin's Comet, which is a sorcery — corrected 2026-06-09), Imperial Recruiter (creature with power 2 or less — Norin, Charming Prince, Karmic Guide, Skyclave Apparition, Laelia), Recruiter of the Guard (creature with toughness 2 or less — Skyclave Apparition, Laelia, Charming Prince, Norin, Solitude), Diabolic Intent (sac a creature for any tutor — Norin and tokens are fodder).

**The play pattern:** Land impulse-draw or blinker by T3. By T4–5, deploy a doubler (Panharmonicon) or repeating blink (Teleportation Circle, Airbender Ascension, Norin) and pile on counters. Drop Hellkite Charger or Sozin's Comet to convert counter-pumped firebending output into extra combats and lethal damage.

-----

## Kill Lines

**Line 1 — Hellkite Charger + Firebending Stack**
With Sozin's Comet up (firebending 5 on all your creatures for the turn) and Hellkite Charger out, attack with Hellkite + 3 other creatures: 5R from Hellkite firebending alone, +5R per supporting attacker = 20R floor. Pay Hellkite's {5}{R}{R} for an extra combat phase, untap, repeat. Each combat also fires Zuko's firebending. Reconnaissance can untap-and-remove-from-combat the supporting creatures, banking the firebending mana while protecting them. Lethal in 1–2 combat phases on a stocked board. **Requires:** Hellkite Charger + Sozin's Comet (or 4+ creatures with persistent firebending). Engine-online → kill: 1–2 turns.

**Line 2 — Counter-Stacked Commander Damage**
Cycle blink + cast-from-exile triggers to pile +1/+1 counters on Zuko. Zuko at 7+ power with Lightning Greaves for haste, attacking through Reconnaissance, threatens 21 commander damage in 3 connected swings. Panharmonicon doubles the rate of counter accumulation per ETB-from-exile. Engine-online → kill: 3–4 turns.

**Line 3 — Avatar Roku Dragons**
The Legend of Roku reaches III (turn 3 of the saga), exile-and-transforms into Avatar Roku (4/4 firebending 4). Avatar Roku attacks for 4R per attack, easily funding the {8}: create 4/4 firebending-4 dragon token activation. Slow, but a backup plan when the blink engine is down. Engine-online → kill: 4–5 turns.

**Line 4 — Sun Titan Loop**
Sun Titan attacks → return a CMC≤3 permanent from graveyard. The deck has many CMC≤3 engine targets (Norin, Charming Prince, Plaguecrafter, Skyclave Apparition, Laelia, Reconnaissance, Airbender Ascension). Each return rebuilds the engine post-wipe. Combined with a blink piece, Sun Titan flickers itself for repeat triggers (e.g., Felidar Guardian blinks Sun Titan, which on re-ETB returns a permanent from graveyard). Slower kill, but very durable.

*Note: Sun Titan and Karmic Guide return permanents from **graveyard**, not exile, so those returns do not trigger Zuko's #2 — they're resilience tools, not engine pieces.*

**Line 5 — Purphoros Passive Burn (added 2026-07-10)**
Purphoros, God of the Forge: whenever **another** creature you control enters, 2 damage to each opponent. Every blink cycle (Felidar, Restoration Angel, Teleportation Circle each end step), every Appa 1/1 token from a cast-from-exile, and every Norin return pings the table — and Panharmonicon doubles the Purphoros trigger on creature ETBs, so a Norin cycle under both is 4 damage to each opponent per spell anyone casts. Indestructible at low devotion (this deck's red devotion rarely reaches 5, so he's usually a non-creature enchantment — wipe-proof). This is the deck's first **non-combat reach axis**: it converts the engine's normal churn into table damage without attacking, and finishes low-life opponents the combat lines leave behind.

-----

## Kill Window

- **Goldfish (lab-verified 2026-06-09; re-run 2026-06-29 after the Zuko MV3 fix):** T7–8 to kill one focused player (median T8; 76% by T8, T6 ≈ 11% even with every attacker unblocked) · T10 to kill the table
- **Through Interaction:** T8–11 (one player)

The deck is mid-speed and its clock is the *broad* counter-stack, not the marquee combo: Hellkite Charger + Sozin's Comet is reachable only ~3% by T6 even with tutors (Diabolic Intent is the only tutor that finds either piece). `scripts/er_speed_lab.py` also tested ten single-card speed levers (extra-combat enablers, Sarkhan's Triumph, fast mana, impulse velocity, Cathars' Crusade) — none moved the median; the front edge is gated by engine assembly + mana before T5, which no 1-of fixes. Full numbers: `analysis/Exiles_Return_Speed_Curve_Analysis.md`.

-----

## Durability

After a Cyclonic Rift on T7: Karmic Guide (5 mana, flying, protection from black) returns a key creature from graveyard — most often Hellkite Charger, Avatar Roku side, or a recruiter. Sun Titan does the same on every attack for CMC≤3. Aang's Shelter (Teferi's Protection) phases out everything to dodge a wipe entirely and is a hard reset button when held in hand. Eerie Interlude and Semester's End preemptively save the team — Semester's End additionally grants every returning creature an extra +1/+1 counter, *and* the bulk return fires Zuko's trigger for each one.

Norin self-exiles continuously (on any spell cast or attack), so single-target removal rarely lands on him. Lightning Greaves grants haste and shroud to a target; Swiftfoot Boots in the SB does similar with hexproof. Recruiter of the Guard / Imperial Recruiter chain into specific resilience pieces. Diabolic Intent and Enlightened Tutor find missing engine cards.

Re-threatening after a full wipe: 1–2 turns once Karmic Guide or a recruiter resolves; immediate if Aang's Shelter saved the board.

The deck *is* commander-dependent in that Zuko is the +1/+1 source — without him, blink and impulse-draw still generate raw card advantage and firebending mana, but no global counter pump. Two-tax Zuko is recastable.

-----

## Interaction Package

**~21 pieces total.**

- **Targeted removal (10):** Path to Exile, Swords to Plowshares, Skyclave Apparition (4-or-less nonland nontoken), Solitude (free with evoke), Generous Gift, Feed the Swarm, Chaos Warp, Abrade, Deadly Rollick (free with commander out), Plaguecrafter (ETB edict — creature *or planeswalker*; blinked = repeatable, answers hexproof/shroud threats; added 2026-07-10).
- **Mass removal (3):** Toxic Deluge, Blasphemous Act, Avatar's Wrath (mass airbend on opponents' creatures + non-hand cast lock until next turn).
- **Stack redirection (3):** Imp's Mischief, Deflecting Swat (free), Redirect Lightning. *No counterspells — Mardu can't access them. Redirect partially substitutes by changing single-target spell/ability targets.*
- **Protection (4):** Aang's Shelter (= Teferi's Protection — phase out everything), Flawless Maneuver (free indestructible-team), Eerie Interlude (exile-and-return team), Semester's End (same with +1/+1 bonuses).
- **Soft locks (2):** Grand Abolisher (opps can't cast or activate on your turn), Reconnaissance (untap-and-remove attackers from combat).
- **Tap-out / repeat removal (1):** Eldrazi Displacer (any creature; combos with bounce-style effects, locks down a key threat per turn).

Instant speed: ~70% (most protection, redirects, and free spells). Sorcery speed: the targeted removal staples, board wipes, and Avatar's Wrath.

**The structural interaction gap is counterspells.** No Mardu deck has access. Redirect Lightning + Imp's Mischief + Deflecting Swat give three pieces of stack interaction, all targeting "spell or ability with a single target." Multi-target combo spells and uncounterable wins remain unanswerable.

-----

## Game Changer Slots

**3 / 3 used.**

1. **Aang's Shelter** *(reskin: Teferi's Protection)* — phase out everything, dodge wipes
2. **Enlightened Tutor** — top-decks Panharmonicon, Airbender Ascension, Teleportation Circle, Lightning Greaves (artifact/enchantment only — it cannot find Sozin's Comet, a sorcery)
3. **Jeska's Will** — both modes: ramp + impulse-draw 3, with commander out

*Verified against `REF_Game_Changers_List.md` on 2026-05-08. Deflecting Swat (in deck) was removed from the GC list 2025-10-21 and no longer counts toward the 3-slot cap.*

-----

## Bracket 3 Compliance

- **Game Changers:** 3 of 3 slots used. Adding any further GC requires a swap.
- **Infinite combos:** None. Hellkite Charger + firebending creates large mana but isn't infinite — it ends when blockers exhaust or you're out of attackers.
- **Extra turns:** None.
- **Mass land denial:** None.
- **Two-card infinites:** None on the engine side. Closest is Hellkite Charger + Aggravated Assault-style effects (not in deck).

-----

## Pod Fit

The exile-matters archetype has distinctive pod dynamics:

1. **Hard to disrupt at the engine level.** Triggers fire on cast and on ETB — there's no single permanent or spell that "is" the engine. Removing any one piece doesn't shut down the loop.
2. **Vulnerable to graveyard hate and exile hate.** Rest in Peace is mostly fine (the deck doesn't *need* the graveyard except for Sun Titan / Karmic Guide). Ashiok, Dream Render and Bojuka Bog are negligible. **Leyline of the Void is bad** for Sun Titan recursion. Conjurer's Closet flickers and the airbend zone *can* be cleared by Bojuka-flavored exile-zone effects (rare).
3. **Slower than control archetypes' clocks.** No T4 win — kills land T6+. Combo pods can outpace the deck if it stumbles on engine assembly.
4. **Strong against creature-aggro pods.** Avatar's Wrath + Toxic Deluge + Blasphemous Act + Skyclave + Solitude + Path/Swords = 6 board-resets-or-pinpoint tools that scale up against creature swarms.
5. **No counterspells.** Combo decks that resolve a stack-only win (Thoracle, Ad Naus chains) need to be answered before the spell, not during. Grand Abolisher is the only proactive lock.

-----

## Differentiation From Other Decks

| | The Exile's Return (Zuko) | Lightning War (Azula) | The Replication Crisis (Satya) |
|---|---|---|---|
| Engine | Cast/ETB-from-exile → +1/+1 stacking + firebending | Spellslinger / damage doubling | Token + clone copy |
| Counter source | Zuko global pump | Power-based burn | N/A |
| Win condition | Combat / commander damage | Direct damage | Wide tokens |
| Color overlap | RWB (Mardu) | UBR (Grixis) | URW (Jeskai) |
| Speed | T7–8 decap · T10 table (lab) | T6–7 table (lab) | T7–8 decap · T10+ table (lab) |
| Graveyard role | Light (Sun Titan, Karmic Guide) | Light | Light |
| Counterspell access | None | Yes | Yes |

No engine overlap with other Avatar decks (Lightning War, Earthbend the Meta) — Zuko cares about exile, Azula cares about damage, Toph cares about artifact-power. Generic staples are shared (Sol Ring, signets, Path, Swords, Toxic Deluge, Lightning Greaves) — the zero-surplus shared pool already accounts for these.

-----

## Known Weaknesses

- **No counterspells.** Mardu has no stack control; only redirect spells (Imp's Mischief, Deflecting Swat, Redirect Lightning) can intervene against single-target spells. Multi-target combo wins resolve unanswered.
- **Engine assembly is multi-piece.** No single card *is* the engine — you typically need a blinker + Zuko + something to blink, or an impulse-draw source + lots of mana. Mulligan decisions matter.
- **Slow-ish goldfish (T7–8 decap / T10 table, lab 2026-06-09).** The deck doesn't "go off" turn 4 — combo pods can pre-empt it. Rely on Aang's Shelter and the protection suite to buy turns, and on Grand Abolisher (+ pending Drannith) to disrupt theirs — the race alone doesn't beat a T6–7 combo clock.
- **Skyclave Apparition's drawback gives back a token.** When Skyclave dies, opponent gets an X/X token — usually fine, but stacked drains can be punishing in late-game.
- **Reanimation triggers don't help Zuko.** Sun Titan and Karmic Guide pull from graveyard, not exile, so they're resilience-only. The Conversion Check counts them as durability, not engine.
- **Aang's Shelter missing from local Scryfall data file.** Per `REF_Reskin_Aliases.md` it's confirmed as Teferi's Protection — but `card_lookup.py` returns no match. Recommend running `update_scryfall_data.py`. Functionally not a deck issue, only a tooling note.

-----

## Conversion Check — 17/20

### Core Loop: 5/5

The loop is "use exile-zone interactions (impulse-draw casts + flicker ETBs + airbend-then-recast) to compound +1/+1 counters across every creature you control, then convert that into firebending mana and combat damage." 25 cards directly serve this loop across three layers (8 cast-from-exile sources, 4 airbend payers that hit both triggers, 12 flicker pieces, 1 doubler in Panharmonicon). The loop is immediately recognizable from the 99 — even without the commander revealed, the density of exile-zone effects screams "exile matters." Highly redundant: any combination of one cast source + one blink piece keeps Zuko's triggers firing.

**Checkpoint:** Cover the commander. The 99 is loaded with exile triggers, blink effects, impulse-draw, and airbend payers. Unmistakable.

### Kill Reliability: 4/5

Four distinct closing lines, with Hellkite Charger + Sozin's Comet being the fastest (1–2 turns from setup once both pieces are out). Avatar Roku tokens and counter-stacked commander damage are slower backup plans. No deterministic infinite — Hellkite chains end naturally — but the firebending math compounds quickly enough that opponents must answer Hellkite or Sozin specifically. Estimated 2–3 turns from engine-online to kill.

Doesn't reach 5 because no single-card "I win" finisher exists, and the kill requires combat — board wipes can fully reset the clock if protection isn't held up.

**Checkpoint:** Hellkite + Sozin closes in 1–2 combat phases. Counter-stacked commander damage closes in 3–4 turns.

### Durability: 4/5

12 flicker pieces give massive engine redundancy. Karmic Guide and Sun Titan return key creatures from graveyard. Aang's Shelter is the hard reset (phase everything out, gain protection from everything). Eerie Interlude, Semester's End, and Flawless Maneuver are wipe-protection at instant speed. Norin auto-exiles (single-target removal rarely connects). Imperial Recruiter / Recruiter of the Guard / Diabolic Intent / Enlightened Tutor refill the engine after losses.

Doesn't reach 5 because Zuko himself is irreplaceable (he's the only +1/+1 source) — repeated commander removal slows the deck even with two-tax recast. Graveyard hate clamps Karmic Guide/Sun Titan recovery; no exile-zone hate is common but it would be brutal if it appeared (e.g., effects that exile from exile).

**Checkpoint:** Cyclonic Rift on T7. Karmic Guide for 5 mana returns Hellkite Charger or another bomb. Re-threatening in 2 turns.

### Interaction: 4/5

~20 interaction pieces across 6 categories. Strong instant-speed coverage (Aang's Shelter, Flawless Maneuver, Solitude, Deadly Rollick, Eerie Interlude, Semester's End — all free or alternative-cost). Spot removal is plentiful (9 pieces). Three pieces of stack redirection partially substitute for counters.

Doesn't reach 5 because Mardu has zero counterspells. Combo decks that win on the stack with multi-target spells can resolve unanswered. Grand Abolisher is the only proactive answer to a combo turn.

### Total: 17/20 — Structurally excellent. Pilot skill is the main variable.

-----

## Decklist (100 cards)

### Commander (1)

1 Fire Lord Zuko

### Cast-From-Exile Sources (8)

1 Light Up the Stage
1 Prosper, Tome-Bound
1 Laelia, the Blade Reforged
1 Zuko, Exiled Prince
1 Sozin's Comet
1 Jeska's Will
1 Professional Face-Breaker
1 The Legend of Roku

*Note: Outpost Siege is in the SB, not the main 99 — Khans-mode coverage in the main is via Roku and Yangchen.*

### Airbend Payers (4)

1 Avatar's Wrath
1 Monk Gyatso
1 The Legend of Yangchen
1 Appa, Steadfast Guardian

### Flicker / Blink Creatures (8)

1 Charming Prince
1 Eldrazi Displacer
1 Felidar Guardian
1 Flickerwisp
1 Restoration Angel
1 Norin the Wary
1 Karmic Guide
1 Sun Titan

### Flicker Spells / Enchantments (4)

1 Ephemerate
1 Eerie Interlude
1 Semester's End
1 Teleportation Circle

### Doubler (2)

1 Panharmonicon
1 Airbender Ascension

### Tutors (4)

1 Enlightened Tutor
1 Imperial Recruiter
1 Recruiter of the Guard
1 Diabolic Intent

### Removal — Spot (9)

1 Path to Exile
1 Swords to Plowshares
1 Solitude
1 Skyclave Apparition
1 Generous Gift
1 Feed the Swarm
1 Chaos Warp
1 Abrade
1 Plaguecrafter

### Removal — Mass (2)

1 Toxic Deluge
1 Blasphemous Act

### Stack Redirection (3)

1 Imp's Mischief
1 Deflecting Swat
1 Redirect Lightning

### Protection (4)

1 Aang's Shelter
1 Flawless Maneuver
1 Deadly Rollick
1 Grand Abolisher

### Combat / Closing (3)

1 Hellkite Charger
1 Reconnaissance
1 Purphoros, God of the Forge

### Equipment (1)

1 Lightning Greaves

### Card Draw (2)

1 Black Market Connections
1 Night's Whisper

### Ramp (8)

1 Sol Ring
1 Arcane Signet
1 Boros Signet
1 Rakdos Signet
1 Talisman of Conviction
1 Talisman of Indulgence
1 Fellwar Stone
1 Dark Ritual

### MDFC / Land-Spell (1)

1 Malakir Rebirth

### Lands (36)

1 Arid Mesa
1 Battlefield Forge
1 Blood Crypt
1 Bloodstained Mire
1 Caves of Koilos
1 Clifftop Retreat
1 Command Tower
1 Dragonskull Summit
1 Eiganjo, Seat of the Empire
1 Exotic Orchard
1 Fabled Passage
1 Fire Nation Palace
1 Godless Shrine
1 Haunted Ridge
1 Isolated Chapel
1 Luxury Suite
1 Marsh Flats
1 Phyrexian Tower
1 Rogue's Passage
1 Sacred Foundry
1 Savai Triome
1 Shattered Sanctum
1 Smoldering Marsh
1 Spectator Seating
1 Sulfurous Springs
1 Sundown Pass
1 Takenuma, Abandoned Mire
1 Vault of Champions
1 Windbrisk Heights
2 Mountain
3 Plains
2 Swamp

### Sideboard (4)

1 Cathars' Crusade — counter pile-on; held out for slot pressure
1 Gonti, Lord of Luxury — exile-cast-an-opp's-card; engine-aligned but slot-bound
1 Outpost Siege — Khans mode = recurring impulse draw; flex slot
1 Swiftfoot Boots — hexproof + haste; redundant with Lightning Greaves

-----

## Changelog

- **2026-07-10 (teardown-swap pass, 2 swaps, $0):** Cards freed by the Earthbend the Meta + Diminishing Returns dismantles. **Adds:** Purphoros, God of the Forge (2 owned; Earthbend copy freed, Lorehold keeps its own — non-combat reach axis, doubled by Panharmonicon on creature ETBs; new Kill Line 5), Plaguecrafter (freed from DR — blinkable edict, creature or planeswalker, answers hexproof; Appa tokens are the sac fodder). **Cuts (dominant-text reasoning):** Dualcaster Mage (ETB spell-copy — pure value, no combo partner in the 99), Cloudshift (the 12th blink piece, one-shot, strictly behind Ephemerate). Both adds verified non-GC — GC stays 3/3 (Aang's Shelter, Enlightened Tutor, Jeska's Will). `deck_doctor` PASS (100 cards, {BRW} identity, banlist, singleton). **Clock re-verified:** `er_speed_lab.py` retargeted to `-20260710` and re-run @40k — decap median T8 (78% by T8) / table T10, clock-neutral vs the 2026-06-09/06-29 baseline (adds are payoff-axis and unmodeled, so this is a floor). Bench (freed, no clean 3rd cut): Kokusho ×2, Solemn Simulacrum ×2 free copies, Giver of Runes — Redirect Lightning fills the scarce stack-interaction role, everything else is engine. CC held at 17/20. List `the-exiles-return-20260710.txt`; old list archived.
- **2026-06-09:** Kill-window verification + lever test (speed-curve analysis, **no card swaps**). `scripts/er_speed_lab.py` (40k trials): goldfish window corrected T6–8 → **T7–8 one player (med T8) / T10 table**; ten 1-card speed levers all within noise (no median moves) — the clock is broad counter compounding, gated by pre-T5 engine assembly, and no single add fixes that. Text fixes: Enlightened Tutor **cannot** find Sozin's Comet (sorcery — two listings corrected); Sozin foretell costs were inverted (pay {2} face-down, cast {2}{R}); Aggravated-Assault-style effects can never go infinite here (sorcery-speed activation vs firebending mana dying at end of combat) while Hellkite's in-combat trigger can. Pending Kiki swap measured: it *slows* the goldfish slightly (cuts Night's Whisper/Light Up the Stage velocity) — its case is resilience + Drannith disruption, not speed. Full analysis: `analysis/Exiles_Return_Speed_Curve_Analysis.md`.
- **2026-05-08:** Summary file created from scratch during deck audit. Decklist verified 100 cards (99 + commander); GC count 3/3 (Aang's Shelter = Teferi's Protection, Enlightened Tutor, Jeska's Will). Commander text verified against local Scryfall data; all UB cards verified except Aang's Shelter (missing from local data file — alias resolves to Teferi's Protection per `REF_Reskin_Aliases.md`). Conversion Check score 17/20 (5/4/4/4) confirms `Deck_Index.md` entry. No card swaps recommended at this time.

## Don't-Miss Rulings

- **Zuko's counter trigger fires on *two* events** — casting a spell from exile **and** a permanent entering from exile. An **airbended-then-recast permanent fires both** (once on cast, once on ETB).
- **The counter goes on *each* creature you control** — every flicker compounds the entire board, not just one creature.
- **Reanimation from the *graveyard* does NOT trigger Zuko.** Sun Titan, Karmic Guide, and Reanimate-style effects are "from graveyard," not "from exile" — they're resilience tools, not engine pieces.
- **Firebending mana lasts only until end of combat.**
- **Panharmonicon doubles trigger #2** when the entering permanent is a creature or artifact.
- **Norin self-exiles** whenever any player casts a spell or attacks (returns at end of turn), so single-target removal rarely lands on him — and under Panharmonicon his return double-pumps the board.
- **Airbending your *own* bomb to recast for {2} is efficient and fires both triggers.** Airbending an *opponent's* creature only triggers Zuko if *they* choose to recast it (rare).

## Piloting Notes (for borrowers)

**Mulligan.** Looking for: **ramp + at least one engine piece by T3–4** — an impulse-draw source *or* a blinker plus something to blink — and a route to casting Zuko. Ship pure interaction piles even on perfect lands — with no cast-from-exile or blink piece the counter-stack never starts, and removal alone doesn't win the grind this deck plays.

- **Keep:** ramp + a blinker + Zuko; or an impulse-draw source with mana behind it. A doubler (Panharmonicon) or recurring blink is a bonus.
- **Toss:** no-land hands; all-finisher (Hellkite/Sozin) with no engine; no way to cast Zuko.
- The engine is **multi-piece** — mulligan toward at least one cast-from-exile or blink piece rather than keeping on raw payoff.

**Threats & timing.**

- **No counterspells — Mardu has none.** Only redirects (Imp's Mischief, Deflecting Swat, Redirect Lightning) touch single-target spells. Multi-target combo wins resolve unanswered, so disrupt combo pieces *before* they go off, or lock with Grand Abolisher.
- **Mid-speed deck** — combo pods can outpace you. Lean on **Aang's Shelter (Teferi's Protection)** to phase out and buy turns.
- **Durability is good:** Aang's Shelter is a hard reset, Karmic Guide / Sun Titan rebuild from the yard, Norin dodges removal. Rest in Peace is mostly fine; Leyline of the Void hurts the Sun Titan recursion.
- **Zuko is the *only* +1/+1 source** — repeated commander removal slows you even though he recasts for two extra mana. Protect him on combo turns.

## Reskins (for borrowers)

| On the card | Really is | What it does |
|---|---|---|
| Aang's Shelter | Teferi's Protection | {2}{W} instant: until your next turn you phase out and gain protection from everything — dodges any wipe or kill. |
| *Airbend (keyword)* | — | Exile target permanent; while exiled its owner may cast it for {2}. The recast triggers Zuko twice (cast + ETB from exile). |
