# Radiation Sickness — The Wise Mothman

## Quick Reference

| Field | Value |
|---|---|
| **Commander** | The Wise Mothman (Sultai, BUG) |
| **Colors** | Sultai (BUG) |
| **Archetype** | Proliferate / +1/+1 Counters / Rad Counters |
| **Bracket** | 3 (3 Game Changers used; 1 two-card infinite combo — Mindcrank + Bloodchief Ascension; no MLD; no extra turns) |
| **Game Changers** | Seedborn Muse, Fierce Guardianship, Cyclonic Rift (3 of 3 slots used) |
| **Conversion Check** | **13/20** (4/3/3/3) |
| **Kill Window** | Goldfish: T8–10 · Through interaction: T10–13 |

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

**Layer 1 — Rad Counter Generation (5 cards):**
The Wise Mothman (ETB + attack), Agent Frank Horrigan (ETB + attack, proliferate twice), Vexing Radgull (whenever you proliferate, each opponent gets a rad counter), Glowing One (attack trigger), Bloatfly Swarm (proliferate on creature death). These cards ensure rad counters accumulate faster than they decay.

**Layer 2 — Proliferate (12 cards):**
Tekuthal, Inquiry Dominus (doubles all proliferate — the key multiplier), Inexorable Tide (proliferate on every spell cast), Evolution Sage (landfall proliferate), Flux Channeler (noncreature spell trigger), Thrummingbird (combat damage), Viral Drake (activated ability, repeatable), Contagion Clasp (activated, also removes small creatures), Contagion Engine (activated, also -1/-1 counters on opponents' boards), Sword of Truth and Justice (combat damage + protection), Tezzeret's Gambit (sorcery + draw), Karn's Bastion (land activation), Deepglow Skate (doubles all counters on a permanent on ETB).

With Tekuthal in play, each of these triggers proliferates twice. With Seedborn Muse, the activated abilities (Viral Drake, Contagion Engine, Karn's Bastion) fire on every opponent's turn.

**Layer 3 — Counter Amplification (7 cards):**
Hardened Scales (+1 counter on every placement), Branching Evolution (doubles counters placed on creatures), Winding Constrictor (+1 counter on every placement), Corpsejack Menace (doubles counters placed on creatures), Kami of Whispered Hopes (+1 on every placement AND taps for mana equal to power), Ouroboroid (beginning of combat: X +1/+1 counters on EACH creature where X = its power — exponential scaling), The Ozolith (preserves counters through creature death).

**Supplemental Mill (5 cards):**
Mesmeric Orb (each untapped permanent mills 1 — absurd with Seedborn Muse untapping everything), Altar of the Brood (each permanent ETB mills each opponent 1), Ruin Crab (landfall mill 3), Psychic Corrosion (draw trigger mills 2), Mindcrank (life loss triggers mill). These generate additional Mothman triggers beyond rad counters.

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

-----

## Conversion Check Breakdown

### Core Loop: 4/5

The loop is dense: 12 proliferate sources, 7 counter amplifiers, 5 supplemental mill effects, 5 rad counter generators. Total engine density: ~29 cards directly serve the loop. The mechanical identity is immediately recognizable — fan out the 99 and the proliferate/counter theme jumps out.

Commander dependency is moderate. Mothman is the bridge that converts mill events into +1/+1 counters, but the proliferate engine and counter doublers function independently. Without Mothman, you still grow creatures through Ouroboroid, Walking Ballista's self-loading, and proliferating existing counters. The mill-to-counter conversion specifically requires the commander.

**Checkpoint:** Cover the commander — can you identify the core loop from the cards alone? Yes. Proliferate + counter doublers + counter payoffs. Clear identity.

### Kill Reliability: 3/5

Six closing lines exist on paper, but the primary path (combat with big countered creatures) is slow. Requires 3-4 proliferate cycles to reach lethal, meaning 2-3 full turn rotations minimum from engine-online. In a 4-player game, connecting with 3 opponents through combat takes additional turns even with evasion.

Simic Ascendancy is real but removable. Mindcrank + Bloodchief Ascension is the fastest deterministic kill but requires both pieces plus Ascension activation. The deck can generate impressive board states that don't convert into wins fast enough — "spectacle vs. lethality" is a real tension here.

**Checkpoint:** Two ways to end the game: (1) Combat with Lambholt/Kodama evasion, ~3-4 turns from engine-online. (2) Mindcrank combo, instant win once assembled. The gap between "threatening" and "winning" is wider than ideal.

### Durability: 3/5

The Ozolith preserves counters through creature removal, which is significant. Counter doublers are redundant (5 cards doing similar things). Proliferate sources are diverse enough that losing one doesn't cripple the engine.

However, a board wipe resets the entire counter investment except what The Ozolith saves. Rebuilding from zero takes 2-3 turns. The commander costs 4 mana and will be a target — repeated removal taxes tempo. Seedborn Muse is a key piece with no redundant replacement (losing it halves the engine's output).

**Checkpoint:** Cyclonic Rift on turn 7. Ozolith saves one creature's worth of counters. Recast Mothman on turn 8, replay a few creatures, start proliferating again turn 9. Threatening again turn 10. That's 3 turns — acceptable but not fast.

### Interaction Profile: 3/5

12 interaction pieces: An Offer You Can't Refuse, Counterspell, Swan Song, Fierce Guardianship (free), Cyclonic Rift, Beast Within, Assassin's Trophy, Pongify, Drown in the Loch, Toxic Deluge, Heroic Intervention (protection), Nuclear Fallout.

Count is adequate. 4 counterspells including a free one. Instant-speed removal covers creatures and permanents. Two board wipes. The weakness: using mana for interaction competes with proliferate activations (Viral Drake costs 4, Contagion Engine costs 4, Karn's Bastion costs 5). Seedborn Muse resolves this tension by untapping everything — but without it, the deck must choose between developing and interacting.

Heroic Intervention and Inspiring Call both protect the board through wraths, which matters for a deck that invests heavily in creature counters.

**Checkpoint:** Opponent about to win. You have Fierce Guardianship (free), Swan Song, or Counterspell. Realistic to have one in hand with Guardian Project and Fathom Mage drawing cards. Adequate but not dominant.

### Total: 13/20

Solid foundation. The core loop is well-designed with genuine mechanical identity distinct from every other deck in the collection. Kill reliability is the weakest axis — the deck threatens impressively but converts slowly. This is an honest 13, not a conservative one. The Mindcrank combo adds a deterministic kill that could push this toward 14 in practice, but the combo requires specific pieces and pod approval.

**Comparison to precon (9/20):** +4 points. Core Loop jumps from 2 to 4 (focused proliferate engine vs. scattered precon themes). Kill Reliability from 2 to 3 (actual closing lines vs. none). Durability from 3 to 3 (similar, Ozolith is a gain but commander dependency is the same). Interaction from 2 to 3 (real counterspells and targeted removal vs. precon's generic answers).

-----

## Bracket 3 Compliance

**Game Changers (3/3):**
1. Seedborn Muse — untaps all permanents on each opponent's turn; enables Contagion Engine/Viral Drake/Karn's Bastion activation 3x per turn cycle
2. Fierce Guardianship — free counterspell with commander in play
3. Cyclonic Rift — asymmetric board reset

**Infinite combo:** Mindcrank + Bloodchief Ascension is a 2-card infinite, but Ascension requires 3 quest counters before it functions. Earliest realistic activation with proliferate: turn 6-7. This is comparable to Combat Celebrant + Satya in The Replication Crisis. Flag for pod Rule 0 discussion.

**Extra turns:** None. Sage of Hours deliberately excluded.

**Mass land denial:** None.

-----

## Pod Fit

1. **Incremental threat, not explosive.** The deck builds pressure over multiple turns rather than threatening a single combo turn. This makes it a secondary target while the archenemy draws fire — good for the current pod dynamic.
2. **Rad counters affect everyone.** Including you. Self-mill can be useful (feeding graveyard for Regrowth targets) but costs life. Accept this as a design cost.
3. **Weak to enchantment/artifact removal.** Hardened Scales, Branching Evolution, Mesmeric Orb, Bloodchief Ascension, Simic Ascendancy are all vulnerable. The deck runs limited enchantment recovery.
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
1 Fierce Guardianship
1 Cyclonic Rift

### Proliferate Sources (12)
1 Tekuthal, Inquiry Dominus
1 Inexorable Tide
1 Evolution Sage
1 Flux Channeler
1 Thrummingbird
1 Viral Drake
1 Contagion Clasp
1 Contagion Engine
1 Sword of Truth and Justice
1 Tezzeret's Gambit
1 Deepglow Skate
1 Karn's Bastion

### Rad Counter / Mill Synergy (9)
1 Agent Frank Horrigan
1 Vexing Radgull
1 Glowing One
1 Bloatfly Swarm
1 Mesmeric Orb
1 Altar of the Brood
1 Ruin Crab
1 Psychic Corrosion
1 Mindcrank

### Counter Amplifiers (7)
1 Hardened Scales
1 Branching Evolution
1 Winding Constrictor
1 Corpsejack Menace
1 Kami of Whispered Hopes
1 Ouroboroid
1 The Ozolith

### Counter Payoffs / Closers (7)
1 Champion of Lambholt
1 Herd Baloth
1 Basking Broodscale
1 Iridescent Hornbeetle
1 Walking Ballista
1 Simic Ascendancy
1 Bloodchief Ascension

### Card Advantage (4)
1 Guardian Project
1 Fathom Mage
1 Generous Patron
1 Inspiring Call

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

### Interaction (12)
1 An Offer You Can't Refuse
1 Counterspell
1 Swan Song
1 Beast Within
1 Assassin's Trophy
1 Pongify
1 Drown in the Loch
1 Toxic Deluge
1 Nuclear Fallout
1 Heroic Intervention
1 Regrowth
1 Swiftfoot Boots

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
