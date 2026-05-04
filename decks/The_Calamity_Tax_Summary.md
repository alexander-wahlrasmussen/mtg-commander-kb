# The Calamity Tax — Glarb, Calamity's Augur

## Quick Reference

| Field | Value |
|---|---|
| **Commander** | Glarb, Calamity's Augur ({B}{G}{U}, 2/4 Frog Wizard Noble) |
| **Colors** | Sultai (BUG) |
| **Archetype** | Lands-matter / big mana / copy payoffs |
| **Bracket** | 3 (3 Game Changers; no infinite combos; no MLD; no extra turns) |
| **Game Changers** | Seedborn Muse, Fierce Guardianship, Demonic Tutor (3 of 3 slots used) |
| **Conversion Check** | **18/20** (5/4/4/5) |
| **Kill Window** | Goldfish: T7–9 · Through interaction: T9–12 |

-----

## Commander Rules Text

Glarb, Calamity's Augur {B}{G}{U}
Legendary Creature — Frog Wizard Noble (2/4)

- Deathtouch
- You may look at the top card of your library any time.
- You may play lands and cast spells with mana value 4 or greater from the top of your library.
- {T}: Surveil 2.

Key rulings: Normal timing rules apply — lands only during your main phase, sorceries at sorcery speed unless a flash enabler is in play. Instants with MV4+ can be cast from the top at instant speed naturally. The surveil 2 is a tap ability with no mana cost. Glarb costs only {B}{G}{U} (3 mana), making him trivially cheap to recast at 5, 7, 9.

-----

## What the Deck Does

The deck ramps aggressively into a massive land count, uses Glarb's top-of-library engine to convert that mana into free spells and card advantage, then kills the table with scaling X-spells or copy effects on high-impact creatures. Seedborn Muse transforms Glarb from a once-per-turn engine into a once-per-opponent's-turn engine, and flash enablers let the deck cast MV4+ sorceries on any player's turn.

### Layer 1 — Ramp / Lands Engine (20+ pieces)

The deck runs 39 lands plus 20+ ramp pieces that aggressively accelerate land count. Extra land drop creatures (Exploration, Azusa, Oracle of Mul Daya, Icetill Explorer) stack with Glarb's ability to play lands from the top, enabling 3–4 land drops per turn. Land tutors (Farseek, Nature's Lore, Three Visits, Skyshroud Claim, Hour of Promise, Open the Way, Tempt with Discovery, Pir's Whim, Sowing Mycospawn, Titania's Command, Omenpath Journey, Planar Genesis) ensure consistent ramp. Nissa Resurgent Animist and Lotus Cobra generate mana on landfall. Cabal Coffers + Urborg, Tomb of Yawgmoth produces 12–20+ black mana from a single land tap in the mid-to-late game.

### Layer 2 — Top-of-Library Value Engine

Glarb's {T}: Surveil 2 sculpts the top of the library, clearing sub-4 MV cards and positioning lands or big spells for free casting. **Seedborn Muse** (Game Changer) transforms this: Glarb untaps during each opponent's untap step, allowing surveil 2 on every player's turn — four activations per turn cycle in a 4-player game. With flash enablers (High Fae Trickster, Valley Floodcaller, Alchemist's Refuge), MV4+ sorceries can also be cast on opponents' turns.

Valley Floodcaller has two distinct roles. First, it is a full flash enabler — "You may cast noncreature spells as though they had flash" — allowing MV4+ sorceries from the top on any turn independently of High Fae Trickster. Second, every noncreature spell cast untaps all Birds, Frogs, Otters, and Rats you control (and gives them +1/+1). Since Glarb is a Frog, each noncreature spell untaps him for another surveil 2, enabling chains through the library on a single turn.

### Layer 3 — Copy / Multiplication Payoffs

Five copy effects multiply the impact of high-value creatures:

- **Rite of Replication** (kicked, 9 mana) — 5 copies of any creature
- **Doppelgang** ({X}{X}{X}{G}{U}) — X copies of X permanents, scaling with mana
- **Flash Photography** (4 mana, flashback 6 mana) — copy any permanent, castable twice
- **Mirrorform** (6 mana, instant) — ALL nonland permanents you control become copies of one target
- **Espers to Magicite** ({3}{B}, instant) — exiles all opponents' graveyards, then creates an artifact token copy of any exiled creature card; doubles as graveyard hate

**Starfield Vocalist** doubles all ETB triggers from permanents entering the battlefield (Panharmonicon on a 4-mana creature body with warp {1}{U}), amplifying every copy that enters.

### Layer 4 — The Coffers Engine

Cabal Coffers taps for {B} equal to the number of Swamps you control. Urborg, Tomb of Yawgmoth makes all lands Swamps in addition to their other types. Yavimaya, Cradle of Growth makes all lands Forests. With 12+ lands in play (typical by turn 6–7), Coffers produces 12+ mana from a single land. This directly fuels Torment of Hailfire kills and pays for kicked Rite of Replication or high-X Doppelgang in one tap.

-----

## How We End Games

### Kill Line 1 — Torment of Hailfire (Primary)

**Cost:** {X}{B}{B} (MV = X+2, castable from top via Glarb at X≥2). **Cards needed:** Just Torment + mana.

With Cabal Coffers + Urborg + 10 other lands = tap Coffers for 12+ mana. Torment at X=12 means each opponent faces 12 iterations of "lose 3 life, sacrifice a nonland permanent, or discard a card." Against a typical mid-game board (5 nonlands, 3 cards in hand, 30+ life), this forces: sacrifice 5 + discard 3 + lose 12 life from the remaining 4 iterations = lethal for most opponents. At X=15+ (very achievable), the table dies regardless of board state.

This is the primary kill because it converts the deck's core strength (massive mana production) directly into a win without requiring any other cards on board. Demonic Tutor finds it. Glarb can cast it from the top. One card, one turn, game over.

### Kill Line 2 — Kokusho + Rite of Replication (Kicked)

**Cost:** 10 mana total (Reanimate 1 mana + kicked Rite 9 mana), or Kokusho on board + 9 mana.

Five legendary token copies of Kokusho enter → all five immediately die to the legend rule → each triggers "each opponent loses 5 life, you gain 5 life per opponent" → 25 damage per opponent, 75 life gained. Lethal against any opponent below 26 life.

The cleanest version: Glarb's surveil naturally sends Kokusho to the graveyard. Reanimate him (1 mana), then cast kicked Rite (9 mana) = one-shot table kill for 10 mana total.

### Kill Line 3 — Doppelgang at High X

**Cost:** {X}{X}{X}{G}{U}. At X=3, costs 11 mana; at X=4, costs 14 mana.

At X=3 targeting Archon of Cruelty + 2 lands: 3 Archon copies enter (each opponent discards 3, loses 9, sacrifices 3; you draw 3, gain 9) plus 6 extra lands. With Starfield Vocalist doubling the ETBs, this doubles to 6 Archon triggers each. Devastating even if not immediately lethal — opponents are stripped of resources.

### Kill Line 4 — Mirrorform

**Cost:** {4}{U}{U}, instant speed.

All nonland permanents you control become copies of target non-Aura permanent. With 5+ nonland permanents and Archon of Cruelty as the target, 5+ Archon ETBs fire — each draining 3, forcing a discard, and forcing a sacrifice per opponent. Being an instant allows deployment at end of turn or in response to a board wipe (copy Kokusho → everything becomes Kokusho → they die to legend rule → massive drain).

### Kill Line 5 — Gray Merchant Drain

**Cost:** Gray Merchant (5 mana) + any copy effect.

Gray Merchant's ETB drains equal to black devotion. In a deck with Glarb ({B}{G}{U} = 2 black pips), plus incidental black permanents, devotion reaches 5–8 naturally. Kicked Rite on Gary = 5 copies, each counting all black pips including each other's = 30–50+ drain per opponent. The copies counting each other's pips creates a scaling feedback loop.

### Kill Line 6 — Value Grind

No single combo. Seedborn Muse untaps Glarb + all lands on every opponent's turn. With flash enablers, the deck casts 3–4 free MV4+ spells per turn cycle. The table cannot outpace this rate of advantage generation indefinitely. Archon of Cruelty, Massacre Wurm, and repeated land drops with Lumra, Nissa, and Icetill Explorer grind out wins through accumulated value.

-----

## Conversion Check Breakdown

### Core Loop: 5/5

The engine is the deck. 20+ ramp/lands cards directly serve the core loop. Seedborn Muse transforms Glarb from once-per-turn to once-per-opponent's-turn, creating 3–4 surveil cycles and potential free casts per turn rotation. With a flash enabler in play, every opponent's turn becomes: untap Glarb → surveil 2 → if MV4+ spell on top, cast it → check new top → potentially play a land or cast another spell.

Extra land drops (Exploration, Azusa, Oracle of Mul Daya, Icetill Explorer) + land tutors (10+ pieces) + top-of-library casting (Glarb) + Seedborn untaps = a coherent machine that's hard to fully disrupt. Even without Glarb, the ramp package independently produces 10+ lands by turn 7, and the big spells can be hardcast.

Valley Floodcaller provides the chain mechanic: each noncreature spell untaps Glarb (Frog type) → surveil 2 → new top → potentially another spell → untap again. On a good turn, this chains through 3–4 cards.

*Checkpoint: Cover the commander. The 99 has Exploration, Azusa, Oracle of Mul Daya, Icetill Explorer, 10+ land tutors, Seedborn Muse, copy effects, Torment of Hailfire, Cabal Coffers. The strategy is unmistakable: "produce massive mana, play threats from the top, copy the best ones, drain the table."*

### Kill Reliability: 4/5

Six distinct closing lines, at least two fast (1–2 turns from engine-online). Torment of Hailfire at X=12+ is a one-card kill that needs only mana — the deck's core product. Kokusho + Rite of Replication is a 25-damage-per-opponent kill from 2 cards (10 mana via Reanimate + kicked Rite). Doppelgang and Mirrorform provide alternative angles. Demonic Tutor ensures the right closer is found when needed.

From engine-online (10+ lands, approximately turn 6–7), the deck kills in 1–2 turns with either Torment (needs Coffers mana + the spell) or Kokusho + Rite (needs 2 specific cards). Three free counterspells protect the kill turn.

Docked from 5 because every kill line requires either massive mana accumulation (Torment needs X=12+ for reliability, requiring 14+ total mana) or assembling a specific 2-card combination. No deterministic infinite combo exists. A 5 would need a one-card guaranteed kill or a compact infinite loop.

*Checkpoint: Demonic Tutor → Torment of Hailfire with Coffers + Urborg + 10 lands = table kill. Kokusho in graveyard + Reanimate + kicked Rite = 25 per opponent. Both achievable 1–2 turns from engine-online.*

### Durability: 4/5

Strong structural resilience across multiple dimensions. Glarb costs 3 mana — recastable at 5, 7, 9 without meaningful tempo loss. Land advantage survives every board wipe (39 lands stay on the battlefield). Reanimate and Noxious Revival recover killed creatures. Lumra returns all lands from graveyard to battlefield on ETB. Icetill Explorer replays lands from graveyard with self-mill fueling it. The ramp density (20+ pieces) means the engine rebuilds fast.

Seedborn Muse is a key accelerant but not a hard dependency — without it, the deck functions at reduced speed but the core engine (ramp → Glarb top-casting) still works. The commander is important but trivially cheap to recast. The sheer mass of redundant ramp pieces means no single removal spell derails the plan.

Docked from 5 because the finisher creature pool is thin: Archon, Kokusho, Gray Merchant, Massacre Wurm = 4 cards. If multiple are exiled (Swords, Path, Farewell), the copy effects lose their best targets. Torment of Hailfire doesn't need creatures, which provides resilience — but the copy-based kills become significantly weaker. Graveyard hate (Rest in Peace, Dauthi Voidwalker) shuts off Reanimate, Noxious Revival, Lumra's land return, and Icetill Explorer simultaneously.

*Checkpoint: Cyclonic Rift on turn 7. Lands stay (39 of them). Recast Glarb for 5 mana. Surveil to find next threat. Noxious Revival puts best card on top for free casting. Threatening again in 1–2 turns.*

### Interaction Profile: 5/5

20 interaction pieces across diverse types and timings:

**Counterspells (5, including 3 free):** Fierce Guardianship (free with commander), Force of Negation (free with blue card), Pact of Negation (free, pay 5 on upkeep), Mana Drain ({U}{U}, generates mana), Swan Song ({U})

**Free/Cheap Removal (4):** Deadly Rollick (free with commander), Force of Vigor (free with green card), Submerge (free if opponent has Forest), V.A.T.S. (split second, destroys any number of creatures with equal toughness)

**Sweepers (3):** Toxic Deluge (scalable, ignores indestructible), Culling Ritual (destroys all MV2- nonlands, generates mana), The Meathook Massacre (scalable -X/-X + ongoing drain)

**Permanent Removal (4):** Druid of Purification (ETB, each player removes an artifact/enchantment), Boseiju Who Endures (channel, uncounterable), Otawara Soaring City (channel bounce), Venser Shaper Savant (flash bounce any spell or permanent)

**Utility Interaction (4):** Bojuka Bog (graveyard exile on ETB), Maze of Ith (neutralizes any attacker), Veil of Summer (protection + draw vs blue/black), Blasphemous Edict (edict removal)

Five counterspells including three that cost zero mana. Four free removal spells. Seedborn Muse untapping all lands on each opponent's turn resolves the develop-vs-hold-up tension completely — the deck holds counterspell mana while continuing to develop via Glarb's top-casting. This is the structural advantage that pushes to 5/5.

*Checkpoint: Opponent about to win with a spell on the stack. Fierce Guardianship (free), Force of Negation (free), Pact of Negation (free), Mana Drain (2 mana), Swan Song (1 mana). Five answers, three of which cost zero mana.*

### Total: 18/20 — Structurally excellent. Pilot skill is the main variable.

| Axis | Score | Key Strength | Limiting Factor |
|---|---|---|---|
| Core Loop | 5 | Seedborn + Glarb = 3–4 activations per turn cycle | — |
| Kill Reliability | 4 | Torment + Coffers = 1-turn kill from engine-online | No deterministic combo; X-kills need massive mana |
| Durability | 4 | 39 lands survive everything; 3-mana commander | Thin finisher creature pool; exile vulnerability |
| Interaction | 5 | 20 pieces including 3 free counters + 4 free removal | — |

-----

## The Path to 19

Push Kill Reliability from 4 to 5 by adding **Exsanguinate** ({X}{B}{B}) alongside Torment of Hailfire. With both in the deck, drawing either one closes the game from a strong mana position. Demonic Tutor can find whichever is better for the situation: Torment destroys boards and hands, Exsanguinate is pure life drain. Redundancy in the finisher slot moves toward deterministic kills — if one X-drain is in the deck, you find it about 10% of games; with two, that doubles. The most realistic candidate cut is Savvy Trader (value creature that doesn't directly serve a kill line). Exsanguinate is held in the maybeboard pending testing.

-----

## Bracket 3 Compliance

**Game Changers (3 of 3 used):**
1. Seedborn Muse — untap all permanents on every opponent's turn
2. Fierce Guardianship — free counterspell with commander in play
3. Demonic Tutor — unrestricted tutor for any card

**Notable non-GC power cards:** Force of Negation, Mana Drain, Pact of Negation, Deadly Rollick, Force of Vigor, Torment of Hailfire, Rite of Replication, Finale of Devastation, Chord of Calling, Green Sun's Zenith, Toxic Deluge, Reanimate, Sylvan Library, The Meathook Massacre, Cabal Coffers

**Infinite combos:** None. All kills are finite (X-spell scaling, copy-based ETB/death triggers, combat damage).

**Extra turns:** None.

**Mass land denial:** None.

-----

## Pod Fit

1. **Converts mana advantage into decisive kills.** Unlike ramp decks that build impressive boards but can't close, Torment of Hailfire and the Kokusho/Rite combo convert mana directly into lethal damage. Left alone past turn 8, this deck wins.
2. **Resilient to creature removal.** The primary kill (Torment) doesn't require any creatures on board. Board wipes help by clearing opponents' boards before a Torment turn.
3. **Punishes tap-out plays.** With Seedborn Muse, the deck holds counterspell mana while developing. Opponents who tap out to advance their plans walk into free counterspells on their combo turns.
4. **Vulnerable to graveyard hate.** Rest in Peace, Leyline of the Void, and Dauthi Voidwalker threaten Reanimate, Noxious Revival, Lumra, and Icetill Explorer. The deck has Force of Vigor, Druid of Purification, and Boseiju for answers, but a resolved Rest in Peace is painful.
5. **Draws archenemy attention.** A visible 12+ land count with Cabal Coffers and Urborg signals an imminent kill. Manage threat perception — Torment doesn't need to be announced until it's resolving.
6. **Strong against combo.** Five counterspells (3 free) mean the deck credibly threatens to stop any combo win attempt. This is the structural advantage over non-blue ramp strategies.

-----

## Reskin Reference

| Deck Card Name | Original MTG Name | Notes |
|---|---|---|
| Ba Sing Se | Ba Sing Se | ATLA original card — {T}: Add {G}; Earthbend 2 ability; not a reskin of an existing card |
| Espers to Magicite | Espers to Magicite | FF original card — {3}{B} instant; exiles opponents' graveyards + creates artifact-token creature copy; not a ramp spell |
| Flash Photography | Flash Photography | FF original (not a reskin) |

-----

## Decklist (100 cards)

### Commander (1)

1 Glarb, Calamity's Augur

### Game Changers (3)

1 Seedborn Muse
1 Fierce Guardianship
1 Demonic Tutor

### Extra Land Drops (4)

1 Exploration
1 Azusa, Lost but Seeking
1 Oracle of Mul Daya
1 Icetill Explorer

### Landfall Payoffs (2)

1 Lotus Cobra
1 Nissa, Resurgent Animist

### Land Recursion (2)

1 Lumra, Bellow of the Woods
1 Blossoming Tortoise

### Land Tutors / Ramp (12)

1 Farseek
1 Nature's Lore
1 Three Visits
1 Skyshroud Claim
1 Hour of Promise
1 Open the Way
1 Tempt with Discovery
1 Pir's Whim
1 Sowing Mycospawn
1 Titania's Command
1 Omenpath Journey
1 Planar Genesis

### Mana (1)

1 Sol Ring

### Creature Tutors (3)

1 Green Sun's Zenith
1 Chord of Calling
1 Finale of Devastation

### Top-of-Library Manipulation (1)

1 Sylvan Library

### Flash Enablers (2)

1 High Fae Trickster
1 Valley Floodcaller

### Copy Effects (5)

1 Rite of Replication
1 Doppelgang
1 Flash Photography
1 Mirrorform
1 Espers to Magicite

### ETB Doubler (1)

1 Starfield Vocalist

### Finisher Creatures (4)

1 Archon of Cruelty
1 Kokusho, the Evening Star
1 Gray Merchant of Asphodel
1 Massacre Wurm

### X-Spell Finisher (1)

1 Torment of Hailfire

### Counterspells (4)

1 Force of Negation
1 Mana Drain
1 Swan Song
1 Pact of Negation

### Removal (7)

1 Deadly Rollick
1 Force of Vigor
1 Submerge
1 V.A.T.S.
1 Toxic Deluge
1 Culling Ritual
1 The Meathook Massacre

### Utility Creatures (3)

1 Druid of Purification
1 Venser, Shaper Savant
1 Savvy Trader

### Recursion (3)

1 Timeless Witness
1 Reanimate
1 Noxious Revival

### Protection (2)

1 Veil of Summer
1 Blasphemous Edict

### Lands (39)

1 Bayou
1 Tropical Island
1 Underground Sea
1 Breeding Pool
1 Overgrown Tomb
1 Alchemist's Refuge
1 Cabal Coffers
1 Urborg, Tomb of Yawgmoth
1 Yavimaya, Cradle of Growth
1 Command Tower
1 Boseiju, Who Endures
1 Otawara, Soaring City
1 Bojuka Bog
1 Maze of Ith
1 Three Tree City
1 Shifting Woodland
1 Vesuva
1 Mistrise Village
1 Hedge Maze
1 Talon Gates of Madara
1 Dryad Arbor
1 Golgari Rot Farm
1 Undercity Sewers
1 Underground Mortuary
1 Minamo, School at Water's Edge
1 Ba Sing Se
1 Agadeem's Awakening
1 Polluted Delta
1 Flooded Strand
1 Misty Rainforest
1 Verdant Catacombs
1 Marsh Flats
1 Bloodstained Mire
1 Scalding Tarn
1 Wooded Foothills
1 Windswept Heath
1 Urza's Cave
1 Horizon of Progress
1 Forest

-----

## Maybeboard

| Card | Role | Notes |
|---|---|---|
| Exsanguinate | Finisher | Redundant X-drain alongside Torment. Path to Kill Reliability 5 — cut Savvy Trader. |
| Avenger of Zendikar | Finisher | Creates plant tokens equal to lands. Strong copy target, threatens lethal next combat. |
| Awaken the Woods | Ramp + landfall | Creates X Forest Dryad land creature tokens. Massive landfall burst. |
| Breach the Multiverse | Reanimation | 7 mana — mill everyone 10, reanimate a creature/PW from each graveyard. |
| The Gitrog Monster | Engine | Extra land drop + draw on land sacrifice. Strong with fetchlands. |
| Scapeshift | Land combo | Sacrifice X lands, search X lands. Enables Coffers/Urborg in one spell. |
| Sphinx of the Second Sun | Engine | Extra beginning phase = extra untap + draw. Redundant to Seedborn Muse. |
| Vein Ripper | Finisher + protection | Ward: sacrifice a permanent. Drains on any creature death. |
| Ertai Resurrected | Interaction | Flash creature — counters a spell/ability OR draws a card on ETB. |
| Titania, Protector of Argoth | Token producer | Creates 5/3 elementals when lands die. Pairs with fetchlands. |
| The Scarab God | Reanimation | Exile creatures from any graveyard as 4/4 zombie copies. |
| Faerie Artisans | Copy | Auto-copies opponents' creatures on ETB. |
| Nyxbloom Ancient | Mana | Triples mana production. Win-more but enormous with Coffers. |
| Consuming Tide | Bounce | Mass bounce with surveil synergy. |
| Coiling Rebirth | Recursion | ? |
| Aggressive Biomancy | Copy | ? |
| Lotuslight Dancers | Value | ? |
| Perfect Defense | Protection | ? |
| Reverent Silence | Enchantment removal | Free if opponent controls a Forest. Hits Rest in Peace. |
| Bala Ged Recovery | Recursion | MDFC — Regrowth on front, tapped land on back. |
| Villainous Wrath | Sweeper | ? |
