# Crystal Sickness — Golbez, Crystal Collector

## Quick Reference

| Field | Value |
|---|---|
| **Commander** | Golbez, Crystal Collector ({U}{B}, 1/4 Legendary Creature — Human Wizard) |
| **Colors** | Dimir (UB) |
| **Archetype** | Artifact value / drain |
| **Bracket** | 3 (3 Game Changers: Chrome Mox, Fierce Guardianship, The One Ring) |
| **Game Changers** | Chrome Mox, Fierce Guardianship, The One Ring |
| **Conversion Check** | **17/20** (5/4/4/4) |
| **Kill Window** | Goldfish: T7–9 · Through interaction: T9–12 |

-----

## Commander Rules Text

Golbez has two abilities:

1. **Surveil trigger:** Whenever an artifact you control enters, surveil 1.
2. **End step recursion + drain:** At the beginning of your end step, if you control four or more artifacts, return target creature card from your graveyard to your hand. Then if you control eight or more artifacts, each opponent loses life equal to that card's power.

Key rulings: The four-artifact threshold is checked both at trigger time and at resolution — if you drop below four between trigger and resolution, the ability fizzles entirely. The eight-artifact check happens as a secondary "then" clause during the same resolution; you don't need to separately satisfy it. The creature card must be a legal target in the graveyard when the ability tries to resolve. Golbez costs only {U}{B} — two mana — making him trivially cheap to recast after removal (4, 6, 8 mana for successive casts).

-----

## What the Deck Does

The deck floods the board with cheap and free artifacts, uses Golbez's surveil triggers to fill the graveyard and sculpt draws, then exploits the end-step ability to recur high-power creatures and drain opponents. Every artifact entering the battlefield is simultaneously card selection (surveil), engine fuel (artifact count), and kill setup (8+ threshold).

### Layer 1 — Cheap Artifact Density (30+ artifacts)

The deck runs 40+ artifacts including lands. The core plays are 0–2 mana artifacts that deploy fast and inflate the count: Mishra's Bauble, Urza's Bauble, Lotus Petal, Mox Amber, Mox Opal, Chrome Mox, Springleaf Drum, Aether Spellbomb, Blood Fountain, Soul-Guide Lantern, Nimblewright Schematic, Servo Schematic, and Liquimetal Torque. Each one enters, triggers Golbez surveil, and pushes toward the 4/8 thresholds.

Artifact lands (Seat of the Synod, Vault of Whispers, Darksteel Citadel, Mistvault Bridge, Treasure Vault) count toward thresholds passively — they're artifacts that cost no card slots from the spell portion of the deck.

### Layer 2 — Artifact Token Generators (6 pieces)

These multiply artifact count per spell and create board presence:

- **Sai, Master Thopterist:** Creates a 1/1 Thopter whenever you cast an artifact spell. Each Thopter is another artifact for thresholds and another Golbez surveil trigger.
- **Efficient Construction:** Enchantment version of Sai — creates a Thopter on each artifact spell.
- **Forensic Gadgeteer:** Creates a Clue on each artifact ETB. Clues are artifacts (more thresholds) and can be cracked for cards.
- **Mirrodin Besieged:** In "Mirran" mode, creates a 1/1 Myr on each artifact cast. In "Phyrexian" mode, each opponent mills artifacts-you-control cards at end step and loses if they have no cards left (alternate win condition).
- **The Mechanist, Aerial Artisan:** Creates a Clue on each noncreature spell. Tap ability turns any artifact token into a 3/1 flying Construct — converts board width into air force.
- **Stridehangar Automaton:** Whenever artifact tokens would be created, an additional 1/1 flying Thopter is also created. Pumps all Thopters +1/+1. Stacks with every token generator above.

### Layer 3 — Cost Reduction and Mana Engines (5 pieces)

- **Etherium Sculptor:** Artifact spells cost {1} less. Turns 1-drops into free plays.
- **Cloud Key:** Naming "artifact" makes all artifacts {1} cheaper.
- **Urza, Lord High Artificer:** All artifacts tap for {U}. Turns every Thopter, Clue, and mana rock into a land. Also creates a Construct token with power/toughness equal to your artifact count.
- **Krark-Clan Ironworks:** Sacrifice artifacts for {C}{C}. Converts low-value artifacts into burst mana for explosive turns.
- **Mystic Forge:** Cast artifacts and colorless spells from the top of library. With cost reduction, this chains multiple free casts per turn.

### Layer 4 — Card Draw Engines (8+ pieces)

- **Thought Monitor / Thoughtcast:** Affinity draws — often cost {U} or {U}{U} with artifact count.
- **Riddlesmith:** Loots (draw + discard) on each artifact cast. Fills graveyard for Golbez recursion.
- **Skullclamp:** Equip to Thopter tokens (1/1 → dies → draw 2). One of the most powerful draw engines in the deck.
- **The One Ring:** Protection on ETB, draws increasing cards each turn.
- **Crystal Skull, Isu Spyglass:** Artifact-based card draw.
- **Uthros Research Craft:** At 3+ charge counters, draws a card on each artifact cast and auto-charges. At 12+, becomes a flying creature with power equal to artifact count.
- **Matoya, Archon Elder:** Converts Golbez's surveil triggers into card draw.
- **Basim Ibn Ishaq:** Draws a card on the first historic spell (artifact, legendary, or Saga) each turn, becomes unblockable, and grows with +1/+1 counters on combat damage.

### Layer 5 — Recursion and Graveyard Support

- **Golbez himself:** Free creature recursion at end step with 4+ artifacts.
- **Academy Ruins:** Puts an artifact from graveyard on top of library.
- **Blood Fountain:** Returns two creature cards from graveyard to hand when sacrificed.
- **Enhanced Surveillance:** Doubles surveil depth (surveil 1 → surveil 2). Also shuffles graveyard into library when sacrificed — graveyard insurance against mill or exile.

### The Play Pattern

Turn 1–2: Deploy Golbez for {U}{B}, play 0–1 mana artifacts. Turn 3–4: Deploy token generators (Sai, Efficient Construction) and mana rocks. Hit 4 artifacts. Golbez starts recurring creatures at end step. Turn 5–7: Hit 8 artifacts. Each end step drains opponents for the power of the recurred creature. Meanwhile, Thopter tokens accumulate, surveil sculpts draws, and the board becomes increasingly difficult to disassemble. The deck grinds incrementally — it doesn't go for one explosive turn but creates compounding advantage each turn cycle.

-----

## Kill Lines

### Line 1 — Golbez Drain with High-Power Creatures (Primary)

With 8+ artifacts, Golbez's end-step ability returns a creature from graveyard to hand AND drains each opponent for that creature's power. The deck runs three dedicated drain bombs:

**Phyrexian Dreadnought (12 power, fixed):** A 12/12 for {1} with an ETB sacrifice trigger that normally kills it. The deck doesn't cast it fairly — it gets milled or surveiled into the graveyard, then Golbez recurs it and drains 12 per opponent. Discard it back (Riddlesmith, The Underworld Cookbook) and repeat next end step. Four end steps = 48 total drain, lethal from full life. Dreadnought also serves as KCI fuel — cast it, sacrifice to KCI for {C}{C} before the ETB resolves, then recur later.

**Master of Etherium (variable power, scales):** Power and toughness equal to your artifact count. This is a characteristic-defining ability — it works in all zones, including the graveyard. With 10 artifacts, Master of Etherium has power 10 in the graveyard, so Golbez drains each opponent for 10. With 12+ artifacts (common in the mid-game with token generators running), it rivals or exceeds Dreadnought. Unlike Dreadnought, Master of Etherium is also a live threat on the battlefield — it pumps all artifact creatures +1/+1 and swings as a large body. It's arguably the best drain target because it scales with the same board state that enables the 8+ threshold.

**Troll of Khazad-dûm (6 power):** A 6/5 with swampcycling that can be cycled early for a Swamp, then recurred later as a 6-damage drain. Lower ceiling than the other two but useful as a consistent mid-range option that also fixes mana in the early game.

The drain line doesn't require combat, doesn't require mana beyond maintaining artifacts, and operates every single end step. With two drain bombs in the graveyard, you can alternate or choose the highest-power option each cycle.

### Line 2 — Tezzeret, Master of the Bridge (Passive Drain)

Tezzeret's static ability: each opponent loses X life at the beginning of combat on your turn, where X is the number of artifacts you control. With 10 artifacts, that's 10 damage per opponent per combat step — no attack required. His +2 draws cards, and he survives combat damage directed at him because he's not attacking. Combined with Golbez's end-step drain, this creates two drain triggers per turn cycle (Tezzeret at combat, Golbez at end step) — often 20+ total life loss per opponent per turn.

### Line 3 — Mirrodin Besieged (Mill Win)

In "Phyrexian" mode, at each end step, each opponent mills cards equal to your artifact count. If they have no cards in library, they lose. With 10+ artifacts, opponents mill 10 per turn cycle. Libraries are typically 70–80 cards by mid-game; this kills in 7–8 end steps. Faster if opponents are also drawing extra cards. This line operates on an entirely different axis from life drain — it ignores life gain, damage prevention, and fog effects.

### Line 4 — Thopter Army Combat

With Sai, Efficient Construction, Stridehangar Automaton, and The Mechanist generating Thopters over multiple turns, a board of 6+ flying Thopters threatens lethal in the air. Master of Etherium gives all artifact creatures +1/+1 while Stridehangar Automaton gives Thopters an additional +1/+1 — with both out, Thopters are 3/3 flyers. The Mechanist can also tap to convert any artifact token into a 3/1 flying Construct, creating additional air threats from Clues and Servos.

### Line 5 — Urza Construct + Artifact Mana Dominance

Urza creates a Construct token with power/toughness equal to your artifact count. With 10+ artifacts, that's a 10/10 or larger. Urza also turns every artifact into a blue mana source, generating 10+ mana per turn for overwhelming card advantage through activated abilities, Mystic Forge chains, or hard-casting expensive spells.

### Line 6 — Tezzeret, Cruel Captain Emblem

Tezzeret, Cruel Captain gains loyalty on each artifact ETB (often 3–5 per turn cycle). His -7 creates an emblem that puts three +1/+1 counters on an artifact each combat and animates it as a creature. Over 2–3 combats, your mana rocks become 6/6+, 9/9+, etc. Combined with evasion from Thopters, this closes fast.

-----

## Conversion Check Breakdown

### Core Loop: 5/5

The loop is "play artifact → surveil → build count → recur/drain." Over 40 cards in the deck are artifacts. The token generators (Sai, Efficient Construction, Forensic Gadgeteer, Mirrodin Besieged, The Mechanist, Stridehangar Automaton) mean each artifact cast produces 1–3 additional artifacts, creating exponential board growth. Cost reducers (Etherium Sculptor, Cloud Key, Urza) enable chaining multiple artifacts per turn. The card draw suite (Thought Monitor, Thoughtcast, Skullclamp, Riddlesmith, Uthros Research Craft, Matoya, Basim Ibn Ishaq) keeps the hand full.

Golbez at 2 mana is the cheapest commander in the collection and comes down turn 2 consistently. But the 99 alone is unmistakably an artifact engine — cover the commander and the identity is obvious from Sai, Efficient Construction, Mystic Forge, Etherium Sculptor, KCI, and the density of 0–1 mana artifacts.

**Checkpoint:** Cover the commander. The 99 has 40+ artifacts, 6 artifact token generators, 3 cost reducers, 8+ draw engines keyed to artifacts. The strategy is unmistakable.

### Kill Reliability: 4/5

Six closing lines spanning drain, mill, combat, and planeswalker advantage. The Golbez drain line has three dedicated bombs — Phyrexian Dreadnought (fixed 12), Master of Etherium (scales with artifact count, often 10+), and Troll of Khazad-dûm (6). Master of Etherium is particularly strong because its characteristic-defining ability works in the graveyard, so it scales with the same board state that enables the 8+ threshold. Tezzeret, Master of the Bridge adds passive drain that stacks. Mirrodin Besieged provides an entirely different axis (mill) that dodges life-gain strategies.

Estimated 2–4 turns from engine-online (8+ artifacts, Golbez in play) to kill. With Tezzeret and Golbez both active, the table takes 20+ life loss per turn. Even without Tezzeret, Dreadnought or Master of Etherium drain alone closes in ~4 end steps from 40 life, and parallel combat damage from Thopters shortens this further.

Doesn't reach 5 because every kill line requires maintaining 8+ artifacts on the battlefield. Artifact-specific hate (Vandalblast, Bane of Progress, Collector Ouphe, Energy Flux) can drop the deck below threshold in a single card. The deck has counterspells to protect against this but can't guarantee it. A 5 would need kills that function through artifact hate.

**Checkpoint:** Golbez in play, 8+ artifacts, Master of Etherium or Dreadnought in graveyard. Each end step drains 10–12 per opponent. Tezzeret adds another 10+ at combat. Two drain sources running simultaneously close in 2–3 turns.

### Durability: 4/5

Golbez at 2 mana is the cheapest commander to recast in the collection. After a board wipe: replay Golbez for 2 (or 4, or 6), replay 2–3 cheap artifacts from hand on the same turn, hit 4 artifacts again by next end step. The deck's mana curve is extremely low — average artifact MV is under 2 — so rebuilding is fast.

Academy Ruins recurs key artifacts. Blood Fountain recurs creatures. Enhanced Surveillance shuffles the graveyard back if needed. Prized Statue creates Treasure tokens when nontoken permanents die, partially refunding a wipe. The surveil engine rapidly refills the graveyard for Golbez recursion after a reset.

Artifact lands survive creature-only wipes (Toxic Deluge, Meathook Massacre) and count toward thresholds when everything else is gone.

Doesn't reach 5 because the deck is genuinely vulnerable to artifact-specific hate. Collector Ouphe or Null Rod shut down the entire mana rock suite and all activated abilities. Vandalblast (overloaded) or Bane of Progress destroy the entire board. These cards are common in Commander and the deck's Dimir colors offer no enchantment removal — only counterspells can prevent them. A resolved Collector Ouphe with no creature removal in hand is potentially game-ending.

**Checkpoint:** Cyclonic Rift on turn 7. Replay Golbez for 2, replay Mox Opal + Sol Ring + Springleaf Drum from hand. Threatening again in 1–2 turns. Vandalblast overload on turn 7 is worse — artifacts destroyed, not returned. Recovery takes 3+ turns.

### Interaction: 4/5

12 interaction and protection pieces:

- **Counterspells (5):** Fierce Guardianship (free with Golbez in play), Mana Drain, Flare of Denial (free — sacrifice an artifact creature), An Offer You Can't Refuse, Arcane Denial
- **Removal (4):** Toxic Deluge (board wipe), Flare of Malice (free — sacrifice a nontoken creature), Executioner's Capsule (artifact — triggers Golbez surveil, recurrable with Academy Ruins), Tithing Blade (artifact — transforms into removal)
- **Stax (1):** Meekstone — taps down creatures with power 3+. Golbez is 1/4, most deck creatures are low-power, so this is one-sided. Shuts down opposing commanders and beaters.
- **Graveyard hate (1):** Soul-Guide Lantern — artifact (triggers surveil), exiles a graveyard or draws a card.
- **Bounce (1):** Otawara, Soaring City — channel to bounce any artifact, creature, enchantment, or planeswalker.

Three free spells (Fierce Guardianship, Flare of Denial, Flare of Malice) mean the deck can protect its board or stop a win attempt while tapped out from deploying artifacts. Mana Drain converts an opponent's spell into artifact mana for your next turn — perfectly on-theme.

Executioner's Capsule deserves special mention: it's an artifact (counts toward thresholds, triggers surveil on entry), a removal spell, and is recurrable with Academy Ruins. Triple-role card.

Doesn't reach 5 because Dimir has zero enchantment removal. A resolved Rhystic Study, Smothering Tithe, Rest in Peace, or Collector Ouphe (enchantment-like effect on a creature, but the principle applies to enchantments proper) can only be answered by bouncing with Otawara or countering on the stack. The counterspell suite includes two weaker options (Arcane Denial gives opponent cards, An Offer gives treasures) that are tempo-negative. No second board wipe beyond Toxic Deluge.

### Total: 17/20 — Structurally excellent. Pilot skill is the main variable.

-----

## Bracket 3 Compliance

**Game Changers (3 of 3):**
1. **Chrome Mox** — fast mana (imprint a nonartifact, nonland card for a mana of its color)
2. **Fierce Guardianship** — free counterspell with commander in play
3. **The One Ring** — protection on ETB, escalating card draw engine

**Notable non-GC power cards:** Mana Drain, Urza Lord High Artificer (removed from GC list Oct 2025), Krark-Clan Ironworks, Mox Opal, Mox Amber, Mystic Forge, Phyrexian Dreadnought, Tezzeret Master of the Bridge, Flare of Denial, Flare of Malice, Skullclamp.

**Infinite combos:** None identified. The deck does not contain any two-card or three-card infinite loops. KCI enables large burst mana turns but does not go infinite without pieces not in the deck (Scrap Trawler, Myr Retriever). The drain lines require multiple end steps, not a single infinite loop.

**Extra turns:** None.

**Mass land denial:** None.

-----

## Pod Fit

The artifact engine has distinctive pod characteristics:

1. **Low profile early.** Golbez is a 1/4 for 2 mana that surveils. Deploying mana rocks and small artifacts doesn't look threatening until the board count crosses 8+ and drain starts. The deck flies under the radar while setting up.
2. **Difficult to attack profitably.** Meekstone taps down big creatures. Thopter tokens block flyers. The deck doesn't need to attack to win (drain lines are passive), so it doesn't expose itself to combat.
3. **Strong against creature strategies.** Toxic Deluge, Flare of Malice, Executioner's Capsule, Meekstone, and Demonic Junker all punish creature-heavy boards. The deck's own win conditions (drain, mill) don't rely on creatures surviving.
4. **Vulnerable to artifact hate.** Vandalblast, Bane of Progress, Collector Ouphe, Null Rod, and Energy Flux all devastate the deck. In pods with heavy green or white decks running these staples, the deck needs to hold counterspells more carefully.
5. **Vulnerable to graveyard hate.** Rest in Peace, Dauthi Voidwalker, and Bojuka Bog shut off Golbez's recursion. The drain requires recurring creatures, so no graveyard = no drain.
6. **Competitive against the pod's combo player.** Five counterspells including two free ones (Fierce Guardianship, Flare of Denial) give the deck reasonable odds of stopping a combo attempt. Mana Drain specifically punishes expensive combo pieces.

-----

## Differentiation From Other Decks

| | Golbez (Crystal Sickness) | Scarab God (Curse of the Scarab) |
|---|---|---|
| Engine | Artifact ETBs → surveil → threshold drain | Zombie tribal → death triggers → drain |
| Token type | Thopters, Clues, Servos (artifact) | Zombie tokens (creature) |
| Commander role | Active engine (surveil + recursion + drain) | Active engine (reanimation + scry) |
| Win axis | Drain (power-based), mill, artifact combat | Drain (count-based), zombie combat |
| Graveyard dependency | High (Golbez recurs from GY) | Moderate (Scarab God exiles from GY) |
| Vulnerability | Artifact hate | Graveyard hate |

Both are Dimir and use the graveyard, but the resource they exploit is completely different. Golbez cares about artifact count on the battlefield; Scarab God cares about creature density in graveyards. No shared engine pieces beyond generic Dimir staples (Polluted Delta, Morphic Pool, counters).

| | Golbez (Crystal Sickness) | Teysa (Diminishing Returns) |
|---|---|---|
| Engine | Artifact ETBs → surveil → threshold drain | Sacrifice → death triggers → drain |
| Drain source | Golbez end step (power-based) | Zulaport/Blood Artist effects (count-based) |
| Sacrifice role | KCI for mana, Skullclamp for draw (optional) | Core mechanic (required for engine) |
| Commander cost | 2 mana (trivial recast) | 4 mana (moderate recast) |
| Colors | UB (counterspells, no enchantment removal) | WB (removal suite, no counters) |

Different resources, different colors, different kill math. No overlap in engine pieces.

-----

## Maybeboard (Sideboard Cards)

The following cards are tracked as potential swaps or meta-dependent includes:

| Card | Role | Notes |
|---|---|---|
| Chromatic Star | Cantrip artifact | Draws on sacrifice, triggers Golbez on ETB |
| Crucible of Worlds | Land recursion | Replays Treasure Vault, fetchlands from graveyard |
| Entomb | Graveyard setup | Instant-speed tutor for Dreadnought or any creature into GY |
| Filigree Attendant | Artifact creature | Flying body with power = artifact count |
| Jeweled Amulet | 0-mana artifact | Stores mana, counts toward thresholds |
| Phyrexian Metamorph | Clone | Copies best artifact or creature on the board for {3} + 2 life |
| Repurposing Bay | Artifact recursion | Returns artifacts from graveyard |
| Requiem Monolith | Mana rock + drain | Drains opponents when creatures die |
| Souls of the Lost | Power = GY count | Massive power creature for Golbez drain line |
| The Regalia | Artifact ramp | Vehicle with strong artifact synergy |
| Thieving Skydiver | Theft | Steals opponent's low-MV artifacts (Sol Rings, signets) |
| Unshakable Tail | Surveil payoff | Draws cards from surveil triggers |

-----

## Decklist (100 cards)

### Commander (1)

1 Golbez, Crystal Collector

### Game Changers (3)

1 Chrome Mox
1 Fierce Guardianship
1 The One Ring

### Artifact Token Generators (6)

1 Sai, Master Thopterist
1 Efficient Construction
1 Forensic Gadgeteer
1 Mirrodin Besieged
1 The Mechanist, Aerial Artisan
1 Stridehangar Automaton

### Cost Reduction / Mana Engines (5)

1 Etherium Sculptor
1 Cloud Key
1 Urza, Lord High Artificer
1 Krark-Clan Ironworks
1 Mystic Forge

### Draw Engines (8)

1 Thought Monitor
1 Thoughtcast
1 Riddlesmith
1 Skullclamp
1 Crystal Skull, Isu Spyglass
1 Uthros Research Craft
1 Matoya, Archon Elder
1 Basim Ibn Ishaq

### Planeswalkers (2)

1 Tezzeret, Master of the Bridge
1 Tezzeret, Cruel Captain

### Kill Creatures (3)

1 Phyrexian Dreadnought
1 Master of Etherium
1 Troll of Khazad-dûm

### Utility Creatures (2)

1 Baleful Strix
1 Merata, Neuron Hacker

### Cheap / Free Artifacts (12)

1 Mishra's Bauble
1 Urza's Bauble
1 Lotus Petal
1 Mox Amber
1 Mox Opal
1 Aether Spellbomb
1 Blood Fountain
1 Soul-Guide Lantern
1 Springleaf Drum
1 Nimblewright Schematic
1 Servo Schematic
1 Tithing Blade

### Recursion / Graveyard Support (3)

1 Enhanced Surveillance
1 Prized Statue
1 Obsessive Pursuit

### Interaction (5)

1 Mana Drain
1 Flare of Denial
1 An Offer You Can't Refuse
1 Arcane Denial
1 Toxic Deluge

### Removal Artifacts (3)

1 Executioner's Capsule
1 Flare of Malice
1 Demonic Junker

### Stax (1)

1 Meekstone

### Card Selection (3)

1 Ponder
1 Preordain
1 Lórien Revealed

### Utility Artifacts (5)

1 Liberator, Urza's Battlethopter
1 Retrofitter Foundry
1 The Underworld Cookbook
1 The Mightstone and Weakstone
1 Sojourner's Companion

### Flash (1)

1 Street Wraith

### Mana Rocks (7)

1 Sol Ring
1 Arcane Signet
1 Dimir Signet
1 Talisman of Dominance
1 Fellwar Stone
1 Liquimetal Torque
1 Cryogen Relic

### Artifact Lands (6)

1 Seat of the Synod
1 Vault of Whispers
1 Darksteel Citadel
1 Mistvault Bridge
1 Treasure Vault
1 Fomori Vault

### Utility Lands (9)

1 Academy Ruins
1 Urza's Saga
1 Inventors' Fair
1 Command Tower
1 Command Beacon
1 Archway of Innovation
1 Otawara, Soaring City
1 Minamo, School at Water's Edge
1 Geier Reach Sanitarium

### Dual / Fetch Lands (9)

1 Underground Sea
1 Watery Grave
1 Morphic Pool
1 Sunken Ruins
1 Polluted Delta
1 Shipwreck Marsh
1 Gloomlake Verge
1 Darkwater Catacombs
1 Underground River

### Other Lands (3)

1 Undercity Sewers
1 Spire of Industry
1 Dimir Aqueduct

### Planet Land (1)

1 Uthros, Titanic Godcore

### Basic Lands (2)

1 Island
1 Swamp
