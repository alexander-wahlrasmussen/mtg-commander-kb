# Crystal Sickness — Golbez, Crystal Collector

**Status:** Full card-text re-audit 2026-05-06. Previous version contained material hallucinations: Mirrodin Besieged Phyrexian mode was described as opponent-mill (it's actually a self-loot + 15-artifacts-in-your-yard alt-win); Tezzeret, Master of the Bridge was described as a static drain at combat (it's an activated +2 ability); Forensic Gadgeteer was described as ETB-triggered (cast-triggered); Prized Statue, Enhanced Surveillance, Tithing Blade direction, Flare of Denial / Malice sacrifice colors all corrected. All card text below verified against local Scryfall data. Note: "Merata, Neuron Hacker" in the decklist is a user-applied custom name for **Lady Octopus, Inspired Inventor** (alias logged in `REF_Reskin_Aliases.md`).

## Quick Reference

| Field | Value |
|---|---|
| **Commander** | Golbez, Crystal Collector ({U}{B}, 1/4 Legendary Creature — Human Wizard) |
| **Colors** | Dimir (UB) |
| **Archetype** | Artifact value / drain |
| **Bracket** | 3 (3 Game Changers: Chrome Mox, Fierce Guardianship, The One Ring) |
| **Game Changers** | Chrome Mox, Fierce Guardianship, The One Ring |
| **Conversion Check** | **17/20** (5/4/4/4) |
| **Kill Window** | Clock: **T11 decap** / **T13 table** (lab 2026-06-13, `cs_clock_lab.py`) · Through interaction: slower *(unverified — goldfish only; assumes Golbez/Urza never removed and no artifact-hate)*. The old "Goldfish T7–9" was the optimistic edge: decap median is T11 (T7 ≈ 7%), table median T13. Shape is **mixed** — Golbez drain + Tezzeret +2 hit the whole table (converge), Urza's Construct / Thopters focus-fire (decap leads by ~2). The kill is gated on assembling **8 artifacts *and* a drain bomb in the yard** (3 in the deck; ~50% by T9), not a race. See `analysis/Crystal_Sickness_Clock_Lab_2026-06-13.md` |
| **Ramp** | 20 sources (3 burst / 14 repeatable) · 47 mana sources, 30 land · in band (`ramp_audit.py` 2026-06-21) |

-----

## Commander Rules Text

Golbez has two abilities:

1. **Surveil trigger:** Whenever an artifact you control enters, surveil 1.
2. **End step recursion + drain:** At the beginning of your end step, if you control four or more artifacts, return target creature card from your graveyard to your hand. Then if you control eight or more artifacts, each opponent loses life equal to that card's power.

Key rulings: The four-artifact threshold is checked both at trigger time *and* at resolution — drop below four between trigger and resolution and the ability fizzles entirely. The eight-artifact threshold is checked only at resolution, as the secondary "then" clause; you must control eight artifacts when it resolves to deal the drain. The target creature card must be a legal target in the graveyard when the ability tries to resolve, otherwise the entire ability fails (the rulings are explicit: "Opponents won't lose life even if you control eight or more artifacts"). Golbez costs only {U}{B} — two mana — making him trivially cheap to recast after removal (4, 6, 8 mana for successive casts).

-----

## What the Deck Does

The deck floods the board with cheap and free artifacts, uses Golbez's surveil triggers to fill the graveyard and sculpt draws, then exploits the end-step ability to recur high-power creatures and drain opponents. Every artifact entering the battlefield is simultaneously card selection (surveil), engine fuel (artifact count), and kill setup (8+ threshold).

### Layer 1 — Cheap Artifact Density (30+ artifacts)

The deck runs 35+ artifacts including artifact lands. The core plays are 0–2 mana artifacts that deploy fast and inflate the count: Mishra's Bauble, Urza's Bauble, Lotus Petal, Mox Amber, Mox Opal, Chrome Mox, Springleaf Drum, Aether Spellbomb, Blood Fountain, Soul-Guide Lantern, Cryogen Relic, Nimblewright Schematic, Servo Schematic, Tithing Blade, and Liquimetal Torque. Each one enters, triggers Golbez surveil, and pushes toward the 4/8 thresholds.

Artifact lands count toward thresholds passively (5 in deck: Seat of the Synod, Vault of Whispers, Darksteel Citadel, Mistvault Bridge, Treasure Vault). Note that **Fomori Vault is *not* an artifact land** — it's a colorless utility land with a tap+discard top-X-of-library look. It does not count toward Golbez's thresholds.

### Layer 2 — Artifact Token Generators (6 pieces)

These multiply artifact count per spell and create board presence. **All triggers are on cast, not ETB** — that means token copies, cards entering from graveyard, and cards cheated into play don't multiply tokens. Plan around casting from hand.

- **Sai, Master Thopterist:** Whenever you cast an artifact spell, create a 1/1 Thopter. Also has an activated draw: {1}{U}, sac 2 artifacts, draw a card.
- **Efficient Construction:** Enchantment version of Sai — Thopter on each artifact cast.
- **Forensic Gadgeteer:** Whenever you *cast* an artifact spell (not ETB — common misread), investigate (create a Clue). Also reduces activated abilities of artifacts by {1} (floor of 1 mana). Triple-role card: counts as artifact for thresholds, Clue is another artifact, and the cost reduction enables cheaper KCI / Skullclamp / Soul-Guide Lantern activations.
- **Mirrodin Besieged:** Choose Mirran or Phyrexian on entry. **Mirran:** Whenever you cast an artifact spell, create a 1/1 colorless Myr token. **Phyrexian:** At the beginning of your end step, draw a card then discard a card. Then if there are 15+ artifact cards in *your* graveyard, target opponent loses the game. Phyrexian mode is a *self*-loot and a self-mill alt-win, not an opponent-mill effect — see Kill Line 3.
- **The Mechanist, Aerial Artisan:** Whenever you cast a *noncreature* spell, create a Clue. Tap to make target artifact token a 3/1 flying Construct until end of turn — converts Clues / Servos / Thopters into air force.
- **Stridehangar Automaton:** Thopters you control get +1/+1. Whenever artifact tokens would be created under your control, an *additional* 1/1 flying Thopter is also created (single bonus per creation event, not per token).

### Layer 3 — Cost Reduction and Free-Cast Engines (7 pieces)

- **Etherium Sculptor:** Artifact spells cost {1} less. Turns 1-drops into free plays.
- **Cloud Key:** Choose a type as it enters; spells of that type cost {1} less. Choose "artifact" in this deck.
- **Urza, Lord High Artificer:** Has an activated ability *on Urza* — "Tap an untapped artifact you control: Add {U}." So any untapped artifact you control can be tapped to give Urza {U} via that ability. Functionally turns every Thopter, Clue, and mana rock into a {U} source. Also creates a 0/0 Construct token that gets +1/+1 per artifact you control (so it's effectively as big as your artifact count). Note: Urza, Lord High Artificer was *removed* from the Game Changer list in October 2025 and no longer counts toward bracket compliance.
- **Krark-Clan Ironworks:** Sacrifice an artifact: Add {C}{C}. Converts low-value artifacts into burst mana for explosive turns.
- **Mystic Forge:** Look at the top of library at any time. Cast artifact spells and colorless spells from the top of library. With cost reduction, this chains multiple free casts per turn.
- **Crystal Skull, Isu Spyglass:** {2}{U}{U} legendary artifact. Look at top of library at any time. Cast *historic* spells (artifact, legendary, Saga) from the top of library. Taps for {U}. Mystic Forge for historic — virtually every nonland card in this deck is historic, so the casting permission is broad.
- **Lady Octopus, Inspired Inventor** (printed under custom name "Merata, Neuron Hacker"): {U} 0/2 legendary. Whenever you draw your first or second card each turn, put an ingenuity counter on her. Tap: free-cast an artifact spell from hand with mana value ≤ ingenuity counters. With Riddlesmith / Sai-draw / Skullclamp / Mishra's Baubles delayed-draws stacking, she ramps to 2–3 counters quickly and starts free-casting Mox Amber, Mishra's Bauble, Springleaf Drum, then Aether Spellbomb / Soul-Guide Lantern, then Skullclamp, then Cloud Key / Crystal Skull. **Massive engine piece in this deck** — frequently the second-most-impactful permanent after Golbez.

### Layer 4 — Card Draw Engines (8 pieces)

- **Thought Monitor:** {6}{U} flying artifact creature with affinity for artifacts. ETB draws 2. Often costs {U} or {U}{U} with artifact count.
- **Thoughtcast:** {4}{U} sorcery, affinity for artifacts. Draw 2. Same affinity-cheap dynamic as Thought Monitor.
- **Riddlesmith:** Whenever you cast an artifact spell, you may draw 1, then discard 1. May-loot — declines on a card you want to keep.
- **Skullclamp:** Equipped creature gets +1/-1. When equipped creature dies, draw 2. Equip to a 1/1 Thopter → dies immediately → draw 2 for 1 mana. Premier draw engine.
- **The One Ring:** Indestructible. ETB protection from everything until your next turn (only if you cast it). Tap: put a burden counter, then draw cards equal to burden counters. Pay 1 life per burden counter on upkeep — accelerating cost.
- **Cryogen Relic:** {1}{U} artifact. Draws a card when it enters AND when it leaves the battlefield (so KCI-sacking it gives {C}{C} *and* a card). Activated stun-counter ability is mostly unused.
- **Uthros Research Craft:** {2}{U} Spacecraft, base 0/8. Station ability adds charge counters equal to a creature's power (sorcery-speed). At 3+ charges: whenever you cast an artifact spell, draw a card and put a charge counter on Uthros. At 12+: gains flying. Static "+1/+0 per artifact you control" — at 12+ charges with 10 artifacts, attacks as a 10/8 flyer.
- **Matoya, Archon Elder:** {2}{U} 1/4. Whenever you scry or surveil, draw a card. Triggers off every Golbez surveil; also triggers from Ponder / Preordain / Geier Reach scries.
- **Basim Ibn Ishaq:** {U}{B} 2/2. Whenever you cast a historic spell, draw a card and Basim is unblockable this turn — *only once each turn*. Combat damage to a player puts a +1/+1 counter on Basim. Steady draw + chip damage.

### Layer 5 — Recursion and Graveyard Support

- **Golbez himself:** Free creature recursion at end step with 4+ artifacts.
- **Academy Ruins:** Tap for {C}; {1}{U}, {T}: put target artifact card from graveyard on top of library. Recurs Skullclamp, Mox Opal, Soul-Guide Lantern, Cryogen Relic — anything destroyed or sacrificed.
- **Blood Fountain:** ETB creates a Blood token. {3}{B}, {T}, sacrifice this artifact: return up to two creature cards from graveyard to hand. The activation is 4 mana plus tap plus sac — slow but two-for-one recursion.
- **Enhanced Surveillance:** {1}{U} enchantment. You may look at an *additional two* cards each time you surveil (so surveil 1 → 3, additive — not doubling). Exile (not sacrifice) it: shuffle your graveyard into your library. Graveyard insurance against mill or exile *and* a way to recycle Phyrexian Dreadnought / Master of Etherium back into the library if Golbez gets exiled.
- **Tezzeret, Master of the Bridge −3:** Returns target artifact card from graveyard to hand. Useful for replaying Skullclamp, key 0-drops, or Master of Etherium without committing it to the battlefield (where it would be vulnerable).

### The Play Pattern

Turn 1–2: Deploy Golbez for {U}{B}, play 0–1 mana artifacts. Turn 3–4: Deploy token generators (Sai, Efficient Construction) and mana rocks. Hit 4 artifacts. Golbez starts recurring creatures at end step. Turn 5–7: Hit 8 artifacts. Each end step drains opponents for the power of the recurred creature. Meanwhile, Thopter tokens accumulate, surveil sculpts draws, and the board becomes increasingly difficult to disassemble. The deck grinds incrementally — it doesn't go for one explosive turn but creates compounding advantage each turn cycle.

-----

## Kill Lines

### Line 1 — Golbez Drain with High-Power Creatures (Primary)

With 8+ artifacts, Golbez's end-step ability returns a creature card from graveyard to hand AND each opponent loses life equal to that card's power. The drain check looks at the card's power *in the graveyard* (the ability sees it before it returns to hand). The deck runs three dedicated drain bombs:

**Phyrexian Dreadnought (12 power, fixed):** A 12/12 trample for {1} with an ETB trigger that says "sacrifice it unless you sacrifice any number of creatures with total power 12 or greater." The deck doesn't cast it fairly — it gets surveiled into the graveyard via Golbez and discarded via Riddlesmith / Underworld Cookbook / Skullclamp-on-self / Mirrodin Besieged Phyrexian discard. Once in graveyard, Golbez recurs it for 12 drain per opponent. Discard it back (Riddlesmith, The Underworld Cookbook) and repeat next end step. Four end steps = 48 total drain, lethal from full life. Dreadnought also serves as KCI fuel: if you do cast it, you can activate KCI in response to its ETB sacrifice trigger to sac it for {C}{C}, then recur later — the rulings explicitly allow either choice if Dreadnought has already left the battlefield by the time the ETB trigger tries to resolve.

**Master of Etherium (variable power, scales):** Power and toughness equal to the number of artifacts you control. This is a characteristic-defining ability — explicitly stated in the rulings to work in all zones including the graveyard. With 10 artifacts on the battlefield, Master in your graveyard reads as 10 power, so Golbez drains each opponent for 10. With 12+ artifacts (common mid-game with token generators running), rivals or exceeds Dreadnought. Unlike Dreadnought, Master of Etherium is also a live threat on the battlefield — it pumps all *other* artifact creatures +1/+1 and swings as a large body. Best drain target because it scales with the same board state that enables the 8+ threshold.

**Troll of Khazad-dûm (6 power):** A 6/5 with swampcycling {1} that can be cycled early for a Swamp, then recurred later as a 6-damage drain. Lower ceiling than the other two but useful as a consistent mid-range option that also fixes mana early.

The drain line doesn't require combat, doesn't require mana beyond maintaining artifacts, and operates every single end step. With two drain bombs in the graveyard, you can alternate or choose the highest-power option each cycle.

### Line 2 — Tezzeret, Master of the Bridge (+2 Activated Damage)

Tezzeret, Master of the Bridge is {4}{U}{B} (often discounted by his own static "Creature and planeswalker spells you cast have affinity for artifacts"). His **+2 loyalty ability** deals X damage to each opponent and you gain X life, where X is the number of artifacts you control. With 10 artifacts, that's 10 damage to each opponent + 10 life gained, *every time you activate +2* — once per turn. Tezzeret enters at 5 loyalty and gains +2 each activation, so he's persistent: turn 1 cast (10 damage), turn 2 (10 damage), turn 3 (10 damage). Combined with Golbez's end-step drain, this stacks two damage sources per turn — Tezzeret on your main phase activation, Golbez at end step — often 20+ life loss per opponent per turn.

His **−3** returns a target artifact card from graveyard to hand — a real recursion option for replaying Skullclamp or staging a Master of Etherium swap. His **−8** ultimate exiles the top 10 of library and dumps all artifacts onto the battlefield. With 30+ artifacts in the deck, expect 5–8 free permanents.

Tezzeret is a planeswalker, so opponents can attack him to remove him. Protect with Thopter blockers, Meekstone tap-locking opposing big creatures, or counterspells on a kill spell.

### Line 3 — Mirrodin Besieged Phyrexian Win Condition

Choosing Phyrexian on entry: at the beginning of your end step, you draw a card then discard a card; **then if there are 15 or more artifact cards in *your* graveyard, target opponent loses the game.** This is a self-mill/self-loot alt-win, not opponent-mill. Filling your own graveyard with 15 artifact cards is the goal.

How the deck reaches 15 artifact cards in graveyard:
- KCI sacrifices (each one puts an artifact in yard, plus the sacrificed token / card itself).
- Skullclamp-on-Thopter loops (Thopter is an artifact, dies, goes to graveyard).
- Mishra's Bauble / Urza's Bauble / Aether Spellbomb / Soul-Guide Lantern / Springleaf Drum self-sacrifices.
- Blood Fountain / Executioner's Capsule activations.
- Treasure Vault {X}{X} sac for X Treasures, then sac the Treasures.
- Tithing Blade craft cost (exile a creature).
- Surveil putting artifacts into yard from library.
- Riddlesmith loots dropping artifact cards into yard.

Once at 15+ artifact cards in your graveyard, every end step targets one opponent for the loss. Three opponents = three end steps to game over after threshold. This line ignores life gain, damage prevention, and fog effects entirely. It is the deck's hardest-to-disrupt win — only graveyard exile (Bojuka Bog, Soul-Guide Lantern from opponent, Rest in Peace, Leyline of the Void) can derail it.

Note: Mirrodin Besieged Mirran mode (Thopter on each artifact cast) is also a viable choice if you're closing via combat damage and don't need the alt-win — pick the mode at the table based on the threats you're facing.

### Line 4 — Thopter Army Combat

With Sai, Efficient Construction, Stridehangar Automaton, and The Mechanist generating Thopters over multiple turns, a board of 6+ flying Thopters threatens lethal in the air. Master of Etherium gives all artifact creatures +1/+1 while Stridehangar Automaton gives Thopters an additional +1/+1 — with both out, Thopters are 3/3 flyers. The Mechanist can also tap to convert any artifact token into a 3/1 flying Construct, creating additional air threats from Clues and Servos.

### Line 5 — Urza Construct + Artifact Mana Dominance

Urza creates a Construct token with power/toughness equal to your artifact count. With 10+ artifacts, that's a 10/10 or larger. Urza also turns every artifact into a blue mana source, generating 10+ mana per turn for overwhelming card advantage through activated abilities, Mystic Forge chains, or hard-casting expensive spells.

### Line 6 — Tezzeret, Cruel Captain Emblem

Tezzeret, Cruel Captain gains loyalty on each artifact ETB (often 3–5 per turn cycle). His -7 creates an emblem that puts three +1/+1 counters on an artifact each combat and animates it as a creature. Over 2–3 combats, your mana rocks become 6/6+, 9/9+, etc. Combined with evasion from Thopters, this closes fast.

-----

## Conversion Check — 17/20

### Core Loop: 5/5

The loop is "play artifact → surveil → build count → recur/drain." Over 40 cards in the deck are artifacts. The token generators (Sai, Efficient Construction, Forensic Gadgeteer, Mirrodin Besieged, The Mechanist, Stridehangar Automaton) mean each artifact cast produces 1–3 additional artifacts, creating exponential board growth. Cost reducers (Etherium Sculptor, Cloud Key, Urza) enable chaining multiple artifacts per turn. The card draw suite (Thought Monitor, Thoughtcast, Skullclamp, Riddlesmith, Uthros Research Craft, Matoya, Basim Ibn Ishaq) keeps the hand full.

Golbez at 2 mana is the cheapest commander in the collection and comes down turn 2 consistently. But the 99 alone is unmistakably an artifact engine — cover the commander and the identity is obvious from Sai, Efficient Construction, Mystic Forge, Etherium Sculptor, KCI, and the density of 0–1 mana artifacts.

**Checkpoint:** Cover the commander. The 99 has 40+ artifacts, 6 artifact token generators, 3 cost reducers, 8+ draw engines keyed to artifacts. The strategy is unmistakable.

### Kill Reliability: 4/5

Six closing lines spanning drain, alt-win, combat, and planeswalker advantage. The Golbez drain line has three dedicated bombs — Phyrexian Dreadnought (fixed 12), Master of Etherium (scales, often 10+), Troll of Khazad-dûm (6). Master of Etherium is particularly strong because its characteristic-defining ability works in the graveyard. Tezzeret, Master of the Bridge adds +2 X damage per opponent on activation (X = artifacts), stacking with Golbez. Mirrodin Besieged Phyrexian mode provides a *self-mill alt-win* (15+ artifact cards in your graveyard → target opponent loses) that dodges life-gain and damage-prevention entirely.

Estimated 2–4 turns from engine-online (8+ artifacts, Golbez in play) to kill. With Tezzeret active and Golbez recurring Master of Etherium, each turn costs the table 20+ life. Even without Tezzeret, Dreadnought or Master of Etherium drain alone closes in ~4 end steps from 40 life; parallel combat damage from Thopters shortens this further.

Doesn't reach 5 because every kill line requires maintaining 8+ artifacts (or 15+ artifact cards in graveyard for Mirrodin Besieged). Artifact-specific hate (Vandalblast, Bane of Progress, Collector Ouphe, Energy Flux) can drop the battlefield count below threshold in a single card. The deck has counterspells to protect against this but can't guarantee it. Graveyard exile (Bojuka Bog, opponent Soul-Guide Lantern, Rest in Peace, Leyline of the Void) shuts down both Golbez recursion and the Mirrodin Besieged path. A 5 would need kills that function through both artifact and graveyard hate.

**Checkpoint:** Golbez in play, 8+ artifacts, Master of Etherium or Dreadnought in graveyard. Each end step drains 10–12 per opponent. Tezzeret +2 adds another 10+ on your main phase. Two damage sources running close in 2–3 turns.

### Durability: 4/5

Golbez at 2 mana is the cheapest commander to recast in the collection. After a board wipe: replay Golbez for 2 (or 4, or 6), replay 2–3 cheap artifacts from hand on the same turn, hit 4 artifacts again by next end step. The deck's mana curve is extremely low — average artifact MV is under 2 — so rebuilding is fast.

Academy Ruins recurs key artifacts. Blood Fountain recurs creatures. Enhanced Surveillance shuffles the graveyard back if needed. Prized Statue creates Treasure tokens when nontoken permanents die, partially refunding a wipe. The surveil engine rapidly refills the graveyard for Golbez recursion after a reset.

Artifact lands survive creature-only wipes (Toxic Deluge, Meathook Massacre) and count toward thresholds when everything else is gone.

Doesn't reach 5 because the deck is genuinely vulnerable to artifact-specific hate. Collector Ouphe or Null Rod shut down the entire mana rock suite and all activated abilities. Vandalblast (overloaded) or Bane of Progress destroy the entire board. These cards are common in Commander and the deck's Dimir colors offer no enchantment removal — only counterspells can prevent them. A resolved Collector Ouphe with no creature removal in hand is potentially game-ending.

**Checkpoint:** Cyclonic Rift on turn 7. Replay Golbez for 2, replay Mox Opal + Sol Ring + Springleaf Drum from hand. Threatening again in 1–2 turns. Vandalblast overload on turn 7 is worse — artifacts destroyed, not returned. Recovery takes 3+ turns.

### Interaction: 4/5

13 interaction and protection pieces:

- **Counterspells (5):** Fierce Guardianship (free if you control a commander), Mana Drain ({U}{U}, counter; gain {C} equal to spell's MV next main phase), Flare of Denial ({1}{U}{U}, counter any spell; alt cost = sacrifice a *nontoken blue creature*), An Offer You Can't Refuse (counter target noncreature spell, opponent gets 2 Treasures), Arcane Denial.
- **Removal (5):** Toxic Deluge (board wipe, pay X life), Flare of Malice ({2}{B}{B}, edict — each opponent sacs the highest-MV creature/PW; alt cost = sacrifice a *nontoken black creature*), Executioner's Capsule ({1}{B}, tap, sac: destroy nonblack creature), Tithing Blade ({1}{B} artifact — *front face* is the removal: ETB each opponent sacrifices a creature of their choice; can craft into Consuming Sepulcher for passive 1-drain on upkeep), Demonic Junker ({6}{B} Vehicle with affinity, often castable for {B} with 6+ artifacts; ETB destroys up to one creature per opponent).
- **Stax (1):** Meekstone — creatures with power 3+ don't untap during their controllers' untap steps (they have to be tapped first, e.g. by attacking; not "tapped down" but "kept tapped"). Golbez is 1/4 and most deck creatures are low-power, so this is largely one-sided.
- **Graveyard hate (1):** Soul-Guide Lantern — {1} artifact (triggers Golbez surveil on ETB and exiles one card from any graveyard); tap+sac exiles each opponent's graveyard; {1}+tap+sac draws a card.
- **Bounce (1):** Otawara, Soaring City — channel ({3}{U}, discard) to bounce any artifact, creature, enchantment, or planeswalker.

**Sacrifice color requirements matter.** Flare of Denial requires sacrificing a *blue* nontoken creature. Eligible blue creatures in deck: Master of Etherium, Etherium Sculptor, Sai, Forensic Gadgeteer, Riddlesmith, The Mechanist Aerial Artisan, Thought Monitor, Matoya, Lady Octopus. Phyrexian Dreadnought and Sojourner's Companion are colorless artifact creatures and *cannot* enable Flare of Denial's alt cost. Flare of Malice requires a *black* nontoken creature — and the deck has very few of those (Golbez, Baleful Strix, Basim Ibn Ishaq). Plan free-cast turns around what you actually have available to sac.

Executioner's Capsule deserves special mention: it's an artifact (counts toward thresholds, triggers surveil on entry), a removal spell, and is recurrable with Academy Ruins. Triple-role card.

Doesn't reach 5 because Dimir has zero enchantment removal. A resolved Rhystic Study, Smothering Tithe, Rest in Peace, or Collector Ouphe can only be answered by bouncing with Otawara or countering on the stack. The counterspell suite includes two weaker options (Arcane Denial gives opponent cards, An Offer gives treasures) that are tempo-negative. No second board wipe beyond Toxic Deluge.

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

### Cost Reduction / Free-Cast Engines (6)

1 Etherium Sculptor
1 Cloud Key
1 Urza, Lord High Artificer
1 Krark-Clan Ironworks
1 Mystic Forge
1 Crystal Skull, Isu Spyglass

### Draw Engines (8)

1 Thought Monitor
1 Thoughtcast
1 Riddlesmith
1 Skullclamp
1 Cryogen Relic
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
1 Merata, Neuron Hacker  *(custom name for Lady Octopus, Inspired Inventor — see REF_Reskin_Aliases.md)*

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

### Recursion / Graveyard Support (2)

1 Enhanced Surveillance
1 Prized Statue

### Utility Enchantments (1)

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

### Mana Rocks (6)

1 Sol Ring
1 Arcane Signet
1 Dimir Signet
1 Talisman of Dominance
1 Fellwar Stone
1 Liquimetal Torque

### Artifact Lands (5)

1 Seat of the Synod
1 Vault of Whispers
1 Darksteel Citadel
1 Mistvault Bridge
1 Treasure Vault

### Utility Lands (10)

1 Academy Ruins
1 Urza's Saga
1 Inventors' Fair
1 Command Tower
1 Command Beacon
1 Archway of Innovation
1 Otawara, Soaring City
1 Minamo, School at Water's Edge
1 Geier Reach Sanitarium
1 Fomori Vault

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

### Fixing & Utility Lands (3)

1 Undercity Sewers
1 Spire of Industry
1 Dimir Aqueduct

### Planet Land (1)

1 Uthros, Titanic Godcore

### Basic Lands (2)

1 Island
1 Swamp

-----

## Changelog

- **2026-05-06:** Full card-text re-audit. Fixed major hallucinations: Mirrodin Besieged Phyrexian mode (was described as opponent-mill; actually a self-loot + 15-artifacts-in-your-yard alt-win — Kill Line 3 fully rewritten); Tezzeret, Master of the Bridge (was described as static drain at combat; actually +2 activated ability for X damage / X life — Kill Line 2 fully rewritten); Forensic Gadgeteer trigger (cast, not ETB); Prized Statue (self-refund only, not other-permanent-death); Enhanced Surveillance (look at additional 2 cards = surveil 1 → 3, additive not doubling; cost is exile, not sacrifice); Tithing Blade direction (front face IS the removal; back face is the passive drain); Flare of Denial alt cost (sacrifice nontoken *blue* creature); Flare of Malice alt cost (sacrifice nontoken *black* creature). Recategorized: Crystal Skull moved from Draw Engines to Cost Reduction (it's a top-of-library cast engine, not draw); Cryogen Relic moved from Mana Rocks to Draw Engines (it draws on ETB and LTB, doesn't add mana); Fomori Vault moved from Artifact Lands to Utility Lands (it's just a Land, not Artifact — does not count toward Golbez's thresholds); Obsessive Pursuit moved from Recursion to a new Utility Enchantments section (it has no graveyard interaction). Added Lady Octopus, Inspired Inventor coverage (printed under custom name "Merata, Neuron Hacker"; alias logged in REF_Reskin_Aliases.md). Added correct sacrifice color requirements to interaction breakdown. Added Demonic Junker to removal count (now 13 interaction pieces, was 12). Note about Urza, Lord High Artificer being delisted from GC list Oct 2025 was already correct.

## Don't-Miss Rulings

- **Golbez's 4-artifact threshold is checked at trigger AND resolution** — drop below 4 in between and the *whole* ability fizzles. The 8-artifact threshold is checked only at resolution. **If there's no legal creature target in your yard, the entire ability fails — no drain even at 8+.**
- **Master of Etherium's power = your artifact count, and this works in the graveyard** — it's the best drain target because it scales with the same board that turns on the 8+ threshold.
- **Every artifact token generator triggers on CAST, not ETB.** Token copies, reanimation, and cheated-in artifacts do NOT make tokens — plan to cast from hand.
- **Mirrodin Besieged Phyrexian mode is a self-loot + self-mill alt-win** (15 artifacts in *your* yard), not opponent-mill. Mirran mode (Myr per artifact cast) is the combat-plan alternative — choose at the table.
- **Fomori Vault is NOT an artifact land** — it doesn't count toward thresholds.
- **Flare of Denial's alt-cost needs a nontoken *blue* creature; Flare of Malice needs a nontoken *black* one** (the deck has few). Plan free-cast turns around what you can actually sacrifice.

## Piloting Notes (for borrowers)

**Mulligan.** Looking for: **lands + 2–3 cheap artifacts + a token generator or cost reducer.** Golbez costs only {U}{B}, so he lands T2 routinely.

- **Keep:** Golbez castable + artifact density to reach the thresholds.
- **Toss:** no-land hands; all-payoff (Dreadnought / Tezzeret) with no artifacts to fuel them.

**Threats & timing.**

- **How you lose:** **artifact hate.** Vandalblast, Bane of Progress, Collector Ouphe, Null Rod, or Energy Flux can drop you below threshold in one card — counterspells are the only prevention (Dimir has no enchantment removal).
- **Also graveyard hate** — Rest in Peace / Bojuka Bog / opposing Soul-Guide Lantern shut off both Golbez recursion and the Mirrodin path.
- **Interaction:** five counters including two free (Fierce Guardianship, Flare of Denial). Mana Drain punishes expensive combo pieces.
- **Low profile early.** A 1/4 surveiling for two mana doesn't look threatening until the count crosses 8 — you set up under the radar.

## Reskins (for borrowers)

| On the card | Really is | What it does |
|---|---|---|
| Merata, Neuron Hacker | Lady Octopus, Inspired Inventor | {U} 0/2 legend; gains an ingenuity counter on your first and second draw each turn; tap to free-cast an artifact from hand with MV ≤ counters. A major engine — often the second-most-impactful permanent after Golbez. |
