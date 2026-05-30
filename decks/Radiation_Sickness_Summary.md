# Radiation Sickness — The Wise Mothman

## Quick Reference

| Field | Value |
|---|---|
| **Commander** | The Wise Mothman (Sultai, BUG) |
| **Colors** | Sultai (BUG) |
| **Archetype** | Proliferate / +1/+1 Counters / Rad Counters |
| **Bracket** | 3 (3 Game Changers used; 1 two-card infinite combo — Mindcrank + Bloodchief Ascension; no MLD; no extra turns) |
| **Game Changers** | Seedborn Muse, Vampiric Tutor, Cyclonic Rift (3 of 3 slots used) |
| **Conversion Check** | **18/20** (5/5/4/4) — Phase A+B audit upgrade then Phase C consistency/Toxrill add, both 2026-05-13 |
| **Kill Window** | Goldfish: T6–9 · Through interaction: T8–12 |

-----

## Commander Rules Text

**The Wise Mothman** {1}{B}{G}{U}
Legendary Creature — Insect Mutant · 3/3 · Flying

- Whenever The Wise Mothman enters the battlefield or attacks, each player gets a rad counter.
- Whenever one or more nonland cards are milled, put a +1/+1 counter on each of up to X target creatures, where X is the number of nonland cards milled this way.

**Key rulings:**
- Rad counters are player counters. At the beginning of each player's precombat main phase, they mill cards equal to their rad counter count. For each nonland card milled, they lose 1 life and remove 1 rad counter.
- Rad counters only decay when nonland cards are milled — milling a land does NOT remove a rad counter, meaning the counter persists into the next turn.
- Mothman's second ability triggers once per mill event regardless of how many players milled simultaneously.
- Proliferate adds rad counters to opponents (increasing their next mill + life loss) AND +1/+1 counters to your creatures simultaneously. This is the deck's engine.

-----

## What the Deck Does

The deck exploits two interlocking counter systems. Mothman distributes rad counters to all players on ETB and attack. Those rad counters force opponents to mill and lose life each turn. Proliferate amplifies both the rad counters on opponents (increasing future mill depth and life drain) and the +1/+1 counters on your creatures (growing your board). Every mill event feeds Mothman's second ability, distributing more +1/+1 counters, which proliferate then doubles again.

Without proliferate, rad counters are self-correcting — they decay every turn when nonland cards are milled. The deck's identity is fighting that decay through 10+ proliferate sources, turning a temporary debuff into an escalating spiral. Opponents mill more each turn, lose more life, and your creatures grow faster than they can deal with.

### The Engine — Three Layers

**Layer 1 — Rad Counter Generation (4 cards):**
The Wise Mothman (ETB + attack), Agent Frank Horrigan (ETB + attack, proliferate twice), Vexing Radgull (whenever you proliferate, each opponent gets a rad counter), Glowing One (attack trigger). These ensure rad counters accumulate faster than they decay. **Vorinclex, Monstrous Raider** further doubles every rad counter you place on opponents — Mothman's ETB now distributes 2 rad counters to each player instead of 1.

**Layer 2 — Proliferate (9 cards):**
Tekuthal, Inquiry Dominus (doubles all proliferate — the key multiplier), Inexorable Tide (proliferate on every spell cast), Evolution Sage (landfall proliferate), Viral Drake (activated ability, repeatable), Contagion Engine (activated, also -1/-1 counters on opponents' boards), Sword of Truth and Justice (combat damage + protection), Tezzeret's Gambit (sorcery + draw), Karn's Bastion (land activation), Deepglow Skate (doubles all counters on a permanent on ETB).

With Tekuthal in play, each of these triggers proliferates twice. With Seedborn Muse, the activated abilities (Viral Drake, Contagion Engine, Karn's Bastion) fire on every opponent's turn. With **Vorinclex MR**, every counter placed (including from proliferate) is doubled again — Tekuthal × Vorinclex stacks multiplicatively. The Phase C cut of Flux Channeler and Thrummingbird trimmed two of the lowest-impact proliferate sources (low noncreature-spell density made Flux Channeler underperform; Thrummingbird died to any blocker before connecting).

**Layer 3 — Counter Amplification (8 cards):**
**Doubling Season** (replaces all counter placements on permanents you control with double — affects +1/+1 counters, growth counters on Simic Ascendancy, AND quest counters on Bloodchief Ascension, halving combo assembly time). Hardened Scales (+1 counter on every placement), Branching Evolution (doubles counters placed on creatures), Winding Constrictor (+1 counter on every placement), Corpsejack Menace (doubles counters placed on creatures), Kami of Whispered Hopes (+1 on every placement AND taps for mana equal to power), Ouroboroid (beginning of combat: X +1/+1 counters on EACH creature where X = its power — exponential scaling), The Ozolith (preserves counters through creature death).

**Supplemental Mill (4 cards):**
Altar of the Brood (each permanent ETB mills each opponent 1), Ruin Crab (landfall mill 3), Psychic Corrosion *(sideboard)* (draw trigger mills 2), Mindcrank (life loss triggers mill). These generate additional Mothman triggers beyond rad counters.

**Equipment (2 cards):**
Sword of Truth and Justice (already covered above — proliferate + protection from B/W on combat damage). **Sword of Feast and Famine** (3-mana equip 2; +2/+2, protection from black and from green; whenever equipped creature deals combat damage to a player, that player discards a card and *you untap all your lands*). The land untap enables a second main phase of activated proliferate (Viral Drake, Contagion Engine, Karn's Bastion) post-combat. **Morgul-Knife** *(Shadowspear, UB-reskinned)* (1-mana equip 2; +1/+1, trample, **lifelink** — directly offsets the deck's rad self-damage; activated ability strips hexproof and indestructible from opponents' permanents for {1}).

-----

## Kill Lines

**Line 1 — Counter Overload (primary, combat)**
Grow creatures through proliferate + Mothman distribution + counter doublers until they're lethal. Champion of Lambholt grows with every creature entering and makes your team unblockable once her power exceeds opponents' creature toughness. Kodama of the West Tree gives trample to any creature with a counter. Typical kill: 3-4 proliferate cycles with Tekuthal produce 15+ power creatures that swing through.

**Line 2 — Simic Ascendancy (alternate win)**
Enchantment: whenever counters are placed on a creature you control, put that many growth counters on Simic Ascendancy. At upkeep, if it has 20+ growth counters, you win. With counter doublers and proliferate (which also hits the growth counters directly), reaching 20 takes 2-3 turns from deployment. Telegraphed but fast with Tekuthal doubling proliferate on the Ascendancy itself.

**Line 3 — Mindcrank + Bloodchief Ascension (infinite combo)**
Once Bloodchief Ascension has 3 quest counters (proliferate accelerates this — 1-2 turns instead of 3), any life loss triggers Mindcrank → mill → triggers Ascension → more life loss → infinite. Kills all opponents simultaneously. Two-card combo requiring Ascension to be active. Earliest realistic assembly: turn 6-7 with proliferate help. Flag for pod Rule 0 discussion.

**Line 4 — Walking Ballista (counter sink)**
Enters with X +1/+1 counters, removes them to deal 1 damage. Mothman and proliferate refill the counters. With enough mana and proliferate, this becomes a repeatable removal engine that can also aim at faces. Not an infinite, but with Seedborn Muse + Tekuthal, each opponent's turn adds counters that can be spent.

**Line 5 — Herd Baloth + Counter Engine (token flood)**
Herd Baloth creates a 4/4 Beast token whenever a +1/+1 counter is placed on it. Basking Broodscale creates an Eldrazi Spawn when a counter is placed on it. With Mothman distributing counters from every mill trigger, these produce a wide board that Ouroboroid or proliferate then super-sizes.

**Line 6 — Iridescent Hornbeetle (insect army)**
Whenever one or more +1/+1 counters are placed on a creature you control, create that many 1/1 Insect tokens. Mothman distributes counters across multiple creatures per mill event → Hornbeetle creates an insect for each counter placed → wide board for Ouroboroid or Champion of Lambholt.

**Line 7 — Triumph of the Hordes (single-card kill swing)**
4-mana sorcery: until end of turn, your creatures get +1/+1, trample, and **infect**. With a wide board grown through Mothman, Hornbeetle tokens, and Herd Baloth Beasts, this poisons multiple opponents in one swing. 10 poison = lethal regardless of life total. Champion of Lambholt provides the evasion (creatures with power less than her power can't block). Doubling Season doubles the tokens from Hornbeetle/Herd Baloth/Broodscale, widening the kill range further.

**Line 8 — Toxrill, the Corrosive (attrition control finisher)**
7-mana 7/7 legendary creature. Each end step, slime counter each creature you don't control; creatures lose -1/-1 for each slime counter; opposing creatures that die become 1/1 Slugs you control; {U}{B} + sac a Slug: draw. **Vorinclex MR doubles your slime counter placements**, so 2 slime counters per end step = -2/-2 per cycle. Most opposing creatures (toughness 2-4) die within 1-2 cycles, each death feeding you a Slug for either Triumph board-width or sac-to-draw card flow. This is the deck's first non-combo non-combat kill line — pure attrition. Slow (Goldfish T9-10) but ignores most counterspell-stack interaction.

-----

## Conversion Check Breakdown

### Core Loop: 5/5

The loop is dense: 9 proliferate sources (post Phase C cuts), 8 counter amplifiers (with Doubling Season + Vorinclex MR), 4 supplemental mill effects, 4 rad counter generators (with Vorinclex doubling the rad output). Total engine density: ~28 cards directly serve the loop. Phase C's cut of Flux Channeler + Thrummingbird trimmed bloat without weakening the engine — both were the lowest-impact proliferate sources. Engine density is the same in *effective* terms because **Survival of the Fittest** acts as a virtual creature tutor every turn, raising every Mothman/payoff hit rate.

Doubling Season + Vorinclex MR + Tekuthal stack multiplicatively: a single Mothman ETB now distributes 2 rad counters to each player (Vorinclex), and any +1/+1 counter placement on your creatures is doubled by Doubling Season *before* counter-amplifier triggers fire. Bloodchief Ascension's quest counters are likewise doubled — combo activates in 2 life-loss triggers instead of 3.

Commander dependency is moderate. Mothman is the bridge that converts mill events into +1/+1 counters, but the proliferate engine and counter doublers function independently. Without Mothman, you still grow creatures through Ouroboroid, Walking Ballista's self-loading, and proliferating existing counters.

### Kill Reliability: 5/5

Eight closing lines, four of them deterministic or near-deterministic:
1. **Mindcrank + Bloodchief Ascension** — fastest deterministic kill. Vampiric Tutor *or* Survival of the Fittest now finds the missing piece on demand. With Doubling Season, Bloodchief's 3-quest-counter activation threshold is reached in 2 life-loss triggers. Realistic assembly T5–6.
2. **Triumph of the Hordes** — single-card win on a wide board. Doubling Season widens every token producer; Mothman distributes counters across multiple creatures. 5–8 creatures by T6 is normal; even half at +1/+1 with infect = 10+ poison.
3. **Simic Ascendancy** — Doubling Season + Vorinclex = ~4x growth counter accrual per proliferate cycle. 20 growth counters in 2 turns from deployment.
4. **Toxrill attrition** — Phase C addition. Once Toxrill stabilizes (T7 + 1 end step), opposing boards collapse in 1-2 cycles, your Slug board widens for Triumph/combat. Non-combo non-combat win ignores most interaction stacks.

Combat with big countered creatures remains the slowest path but is now genuinely lethal in 2 turns once the engine fires. The 5/5 here is the difference between "many kill lines on paper" (Phase A+B) and "multiple independent deterministic wins" (Phase C — Toxrill adds a non-combo line that cannot be answered by graveyard hate, Pithing Needle on Bloodchief, or wraths once it lands).

### Durability: 4/5

The Ozolith preserves counters through creature removal. Counter doublers are redundant. Proliferate sources are diverse. **Doubling Season is a high-value removal target** — taking it out is non-trivial (5-mana enchantment, no built-in protection) but losing it doesn't shut off the engine, just slows the doublings.

Vampiric Tutor at 1 mana means recovery from wraths is faster — Tutor → next turn deploy the missing piece. Seedborn Muse is still the irreplaceable engine piece. A turn-7 Cyclonic Rift hurts but the Vampiric → Ozolith / Doubling Season / Mindcrank sequence rebuilds quickly.

### Interaction Profile: 4/5

12 interaction pieces with Phase C's Force of Negation added back: An Offer You Can't Refuse, Counterspell, Swan Song, **Force of Negation (free off-turn)**, Cyclonic Rift, Beast Within, Assassin's Trophy, Pongify, Drown in the Loch, Toxic Deluge, Nuclear Fallout, plus Heroic Intervention for board protection.

Force of Negation restores the free-counter slot lost when Fierce Guardianship was cut for Vampiric Tutor. Same noncreature limitation as FG, but it works without commander on the field (a real advantage when Mothman is in the command zone or exiled). The deck still doesn't reach the 5/5 benchmark — Dark Lord's Army has 15 pieces with 3 free/mana-positive counters; this deck has 12 pieces with 1 free counter. To push to 5/5 would need a second free counter (Force of Will or Pact, both currently deployed) or substantial removal-suite expansion.

Toxrill provides asymmetric ongoing interaction by killing opponents' creatures every end step — not in the "11 pieces" count but materially reduces opposing pressure.

### Total: 18/20

The deck graduates from "17/20, multiple deterministic lines with cheap combo assembly" to "18/20, four-line kill plan with restored free interaction." The binding constraint sits at Interaction (12 pieces, 1 free counter) and Durability (no anti-wrath protection beyond Heroic Intervention + Ozolith). Pushing to 19+ would require either a 2nd free counter (Force of Will / Pact copies are all deployed) or Crucible-of-Worlds-style permanence.

**Upgrade history:**
- Original build: 13/20 (4/3/3/3)
- 2026-05-13 Phase A+B: corrected summary↔.txt mismatches; swapped Bloatfly Swarm / Contagion Clasp / Mesmeric Orb / Fierce Guardianship → Doubling Season / Vorinclex MR / Triumph of the Hordes / Vampiric Tutor. → 17/20 (5/4/4/4).
- 2026-05-13 Phase C: swapped Flux Channeler / Thrummingbird / Inspiring Call → Toxrill / Survival of the Fittest / Force of Negation. Kill Reliability 4→5 (Toxrill adds 8th, non-combo non-combat kill line); Interaction restored a free counter (still 4/5 vs 15-piece benchmark). → 18/20 (5/5/4/4).

-----

## Bracket 3 Compliance

**Game Changers (3/3):**
1. Seedborn Muse — untaps all permanents on each opponent's turn; enables Contagion Engine/Viral Drake/Karn's Bastion activation 3x per turn cycle
2. Vampiric Tutor — 1-mana instant tutor; finds combo pieces (Mindcrank, Bloodchief, Doubling Season) or interaction on demand. Replaced Fierce Guardianship 2026-05-13 to accelerate combo assembly
3. Cyclonic Rift — asymmetric board reset

**Infinite combo:** Mindcrank + Bloodchief Ascension is a 2-card infinite, but Ascension requires 3 quest counters before it functions. With Doubling Season the threshold is reached in 2 life-loss triggers. Earliest realistic activation: turn 5-6. This is comparable to Combat Celebrant + Satya in The Replication Crisis. Flag for pod Rule 0 discussion.

**Extra turns:** None. Sage of Hours deliberately excluded.

**Mass land denial:** None.

-----

## Pod Fit

1. **Incremental threat, not explosive.** The deck builds pressure over multiple turns rather than threatening a single combo turn. This makes it a secondary target while the archenemy draws fire — good for the current pod dynamic.
2. **Rad counters affect everyone.** Including you. Self-mill can be useful (feeding graveyard for Regrowth targets) but costs life. Accept this as a design cost.
3. **Weak to enchantment/artifact removal.** Hardened Scales, Branching Evolution, Doubling Season, Bloodchief Ascension, Simic Ascendancy are all vulnerable. The deck runs limited enchantment recovery (Regrowth only).
4. **Weak to graveyard hate.** Opponents' graveyards fill from rad counters and mill effects. Bojuka Bog and similar cards from opponents hurt incidental value. Your own Bojuka Bog is included to police opposing graveyards (especially relevant against Teval if both are in the pod).
5. **Commander is a moderate target.** 4 CMC, 3/3 flying. Not as threatening-looking as Teval or Azula, which helps it survive early. But experienced players will recognize the proliferate engine and prioritize removal.

-----

## Differentiation From Existing Decks

| | Teval (Loam Cycle) | Wise Mothman (Radiation Sickness) |
|---|---|---|
| Color identity | Sultai (BUG) | Sultai (BUG) |
| Engine | Graveyard as resource — dredge, recursion, land loops | Counters on players and creatures — proliferate, amplify, distribute |
| Graveyard role | Primary resource (Life from the Loam, Living Death, Muldrotha) | Incidental byproduct of milling; never accessed as a resource |
| Win condition | Craterhoof, Jarad + Lord of Extinction, Exsanguinate | Combat counters, Simic Ascendancy, Mindcrank combo |
| Commander dependency | Low (engine runs independently) | Moderate (mill-to-counter conversion requires commander) |
| Interaction | 4 counterspells + removal + recursion recovery | 4 counterspells + removal + Heroic Intervention |
| Key mechanic | Dredge, land recursion | Proliferate, rad counters |
| Card overlap | Sol Ring, basics, Farseek | Sol Ring, basics, Farseek |

**Zero engine overlap.** Different mechanical identity, different win conditions, different game feel. The shared color identity is cosmetic — these decks play nothing alike.

-----

## Acquisition Summary

> **Historical context:** This section reflects the *original* build's acquisition state. The 2026-05-13 upgrade swapped in Doubling Season (already owned, surplus from Earthbend), Vorinclex MR (buy needed — pricing not verified, may be ~€30+ on Cardmarket), Triumph of the Hordes (buy a 2nd copy or swap with Earthbend), and Vampiric Tutor (already owned, surplus). Mesmeric Orb's buy-list entry below is no longer relevant — it was cut.

### Already Available From Surplus (49 cards + commander)
All precon holdovers, generic staples, and cards with extra copies.

### Shared With Other Decks — Need 2nd Copy (18 cards)
These cards are allocated to other active decks. Options: buy duplicates or swap for alternatives.

**Buy duplicates (recommended):**
- Counterspell (~€0.50) — used in 4 decks, you own 4, just buy another
- Swan Song (~€3) — used in 2 decks
- Nature's Lore (~€0.50) — used in 3 decks
- Three Visits (~€3) — used in 2 decks
- Toxic Deluge (~€8) — used in 3 decks
- Assassin's Trophy (~€2) — used in 1 deck
- Pongify (~€0.50) — used in 2 decks
- Evolution Sage (~€0.50) — Toph also uses this
- Fathom Mage (~€0.50) — Bumbleflower uses this
- Generous Patron (~€0.50) — Bumbleflower uses this
- Incubation Druid (~€0.50) — Bumbleflower uses this
- Takenuma, Abandoned Mire (~€5) — Diminishing Returns uses this

**Swap for alternatives or accept swapping between decks:**
- Cyclonic Rift (~€25) — GC, Replication Crisis also uses it. Buy a 2nd if budget allows; otherwise swap between decks.
- Misty Rainforest (~€25) — Loam Cycle + Bumbleflower. Substitute: Prismatic Vista or another blue fetch.
- Polluted Delta (~€25) — 3 other decks use it. Substitute: Flooded Strand or another fetch.
- Verdant Catacombs (~€20) — Loam Cycle + Diminishing Returns. Substitute: Windswept Heath.
- Morphic Pool (~€5) — Loam Cycle + Golbez. Substitute: Shipwreck Marsh or Darkwater Catacombs.
- Rejuvenating Springs (~€5) — Loam Cycle. Substitute: Botanical Sanctum.

### Not In Collection — Buy List (29 cards)

| Card | Est. € (Cardmarket) | Role |
|---|---|---|
| Ouroboroid | ~€28 | Counter payoff (exponential growth) |
| Walking Ballista | ~€8 | Counter sink / removal |
| Sword of Truth and Justice | ~€6 | Proliferate on combat damage + protection |
| Bloom Tender | ~€8 | Mana dork (taps for 3 colors with Mothman) |
| Deepglow Skate | ~€5 | Doubles all counters on ETB |
| Mindcrank | ~€1 | Combo piece + supplemental mill |
| Mesmeric Orb | ~€5 | Mill engine (each untap → mill 1) |
| Contagion Engine | ~€3 | Repeatable proliferate + board control |
| Tekuthal, Inquiry Dominus | ~€1 | Doubles all proliferate |
| Psychic Corrosion | ~€0.50 | Draw-triggered mill |
| Kami of Whispered Hopes | ~€5 | Counter doubler + scaling mana dork |
| Bloodchief Ascension (if not precon) | — | Already owned (surplus) |
| Herd Baloth | ~€0.50 | Token generation from counters |
| Basking Broodscale | ~€2 | Token generation from counters |
| Champion of Lambholt | ~€1 | Evasion from counters |
| Iridescent Hornbeetle | ~€0.25 | Token generation from counters |
| Flux Channeler | ~€0.25 | Proliferate on noncreature spells |
| Thrummingbird | ~€0.25 | Proliferate on combat damage |
| Viral Drake | ~€1 | Repeatable proliferate (activated) |
| Ruin Crab | ~€0.50 | Landfall mill |
| Altar of the Brood | ~€2 | ETB mill |
| Drown in the Loch | ~€0.50 | Flexible counter/removal |
| Regrowth | ~€1 | Recursion |
| Hedge Maze | ~€1 | Dual land |
| Nurturing Peatland | ~€2 | Horizon land |
| Waterlogged Grove | ~€2 | Horizon land |
| Willowrush Verge | ~€1 | Dual land |
| Karn's Bastion | ~€1 | Proliferate land |
| Reflecting Pool | ~€3 | Fixing land |
| Zagoth Triome | ~€6 | Triome |

**Estimated total for not-owned cards: ~€95–105**
**Estimated total for duplicate staples: ~€25–30**
**Premium duplicates (fetches/Rift, if buying): ~€95–100**
**Grand total (all new cards): ~€120–135 without premium dupes, ~€215–235 with everything**

-----

## Maybeboard — Cards Considered But Cut

- **Sage of Hours** — Extra turns from +1/+1 counter removal. Cut per pod rules (no extra turn chains).
- **Willbreaker** — Steals creatures targeted by Mothman's ability. Clever but fragile (5 mana enchantment with no other synergy). Too cute.
- **Muldrotha, the Gravetide** — Powerful but pulls the deck toward graveyard recursion, which is Teval's identity. Excluded for distinctiveness.
- **Six** — Same issue. Graveyard value creature that belongs in Teval, not here.
- **The Gitrog Monster** — Land sacrifice/draw engine. Teval card. Excluded.
- **Conduit of Worlds** — Recursion permanent. Teval card. Excluded.
- **Fraying Sanity** — Doubles mill on one opponent. Too narrow in multiplayer (only hits one player).
- **Retribution of the Ancients** — Remove +1/+1 counters to kill creatures. Interesting but anti-synergy (you want counters to stay ON your creatures for proliferate and Simic Ascendancy).
- **Memory Erosion** — Mill 2 on each opponent spell. Slow and doesn't advance the counter plan.
- **Syr Konrad, the Grim** — Drain on mill/death. Good card but 5 mana, and the deck already has Bloodchief Ascension for this role plus Mindcrank combo.
- **Undead Alchemist** — Creates zombies from milling creatures. Already in Curse of the Scarab. Card demand conflict.
- **Herald of Secret Streams** — Creatures with +1/+1 counters are unblockable. Redundant with Champion of Lambholt and costs 4 mana.

-----

## Decklist (100 cards)

### Commander (1)
1 The Wise Mothman

### Game Changers (3)
1 Seedborn Muse
1 Vampiric Tutor
1 Cyclonic Rift

### Proliferate Sources (9)
1 Tekuthal, Inquiry Dominus
1 Inexorable Tide
1 Evolution Sage
1 Viral Drake
1 Contagion Engine
1 Sword of Truth and Justice
1 Tezzeret's Gambit
1 Deepglow Skate
1 Karn's Bastion

### Rad Counter / Mill Synergy (7)
1 Agent Frank Horrigan
1 Vexing Radgull
1 Glowing One
1 Altar of the Brood
1 Ruin Crab
1 Mindcrank
1 Vorinclex, Monstrous Raider

### Counter Amplifiers (8)
1 Doubling Season
1 Hardened Scales
1 Branching Evolution
1 Winding Constrictor
1 Corpsejack Menace
1 Kami of Whispered Hopes
1 Ouroboroid
1 The Ozolith

### Counter Payoffs / Closers (9)
1 Champion of Lambholt
1 Herd Baloth
1 Basking Broodscale
1 Iridescent Hornbeetle
1 Walking Ballista
1 Simic Ascendancy
1 Bloodchief Ascension
1 Triumph of the Hordes
1 Toxrill, the Corrosive

### Equipment (2)
1 Sword of Feast and Famine
1 Morgul-Knife *(Shadowspear)*

### Card Advantage (3)
1 Guardian Project
1 Fathom Mage
1 Generous Patron

### Tutors (1)
1 Survival of the Fittest

### Ramp (8)
1 Sol Ring
1 Arcane Signet
1 Birds of Paradise
1 Bloom Tender
1 Incubation Druid
1 Farseek
1 Nature's Lore
1 Three Visits

### Creatures — Utility (3)
1 Kodama of the West Tree
1 Rishkar, Peema Renegade
1 Tato Farmer

### Interaction (11)
1 An Offer You Can't Refuse
1 Counterspell
1 Swan Song
1 Force of Negation
1 Beast Within
1 Assassin's Trophy
1 Pongify
1 Drown in the Loch
1 Toxic Deluge
1 Nuclear Fallout
1 Heroic Intervention

### Recursion (1)
1 Regrowth

### Lands (34)
1 Breeding Pool
1 Overgrown Tomb
1 Watery Grave
1 Misty Rainforest
1 Polluted Delta
1 Verdant Catacombs
1 Zagoth Triome
1 Rejuvenating Springs
1 Morphic Pool
1 Undergrowth Stadium
1 Hinterland Harbor
1 Drowned Catacomb
1 Woodland Cemetery
1 Exotic Orchard
1 Reflecting Pool
1 Shifting Woodland
1 Nurturing Peatland
1 Waterlogged Grove
1 Hedge Maze
1 Willowrush Verge
1 Yavimaya, Cradle of Growth
1 Nesting Grounds
1 Mariposa Military Base
1 Takenuma, Abandoned Mire
1 Boseiju, Who Endures
1 Bojuka Bog
1 Command Tower
3 Forest
2 Island
2 Swamp

### Sideboard (2)
1 Psychic Corrosion
1 Swiftfoot Boots
