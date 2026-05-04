# The Loam Cycle — Teval, the Balanced Scale

**Status:** revised 2026-05-03 after a full card-text audit. The previous version contained material errors (wrong Game Changer count, wrong Ripples of Undeath text, mischaracterized Teval, phantom card references). All card text below verified against local Scryfall data.

## Quick Reference

| Field | Value |
|---|---|
| **Commander** | Teval, the Balanced Scale (Sultai, BUG) |
| **Colors** | Sultai (BUG) |
| **Archetype** | Self-mill / land recursion / graveyard value |
| **Bracket** | 3 (3 Game Changers — at hard cap; no infinite combos; no MLD; no extra turns) |
| **Game Changers** | Fierce Guardianship, Crop Rotation, Field of the Dead (**3/3 — full**) |
| **Conversion Check** | **19/20** (5/5/5/4) |
| **Kill Window** | Goldfish: T6–8 · Through interaction: T8–10 |

-----

## What the Deck Does

The deck fills its own graveyard via dredge, self-mill, and discard outlets, then treats the yard as a second hand. Land recursion (Life from the Loam + Crucible / Ramunap / Conduit) drives card velocity; creature recursion (Meren, Muldrotha, Phyrexian Reclamation, Oversold Cemetery) and mass reanimation (Living Death, Dread Return, Victimize) cash that velocity into board state. The engine is self-reinforcing — every card that enters the graveyard becomes future fuel.

Teval is an engine piece, not a passenger. His attack trigger mills 3 and recurs a land tapped, and his static "whenever one or more cards leave your graveyard, create a 2/2 black Zombie Druid token" fires off every Loam, every reanimation spell, every dredge, and every Scarab God activation. He converts the graveyard churn into bodies. He is not "balancing" or "political" — he is a token-generating self-mill engine.

The deck has redundant recursion past the commander: Muldrotha, Meren, Crucible, Conduit of Worlds, Ramunap Excavator, and Gitrog all provide independent engines. Cover Teval and you can still see the deck plan from the rest of the 99.

### The Engine — Two Interlocking Halves

**Half 1 — Fill the Graveyard:**

- **Self-mill creatures:** Hedron Crab (landfall mill 3 — fetchlands compound this), Stitcher's Supplier (mill 3 on enter and on death), Sidisi, Brood Tyrant (mill 3 on enter and on attack; creature cards milled from library make 2/2 zombies), World Shaper (optional mill 3 on attack; mass land reanimation on death).
- **Self-mill spells:** Life from the Loam (dredge 3, return up to 3 lands — the engine's backbone), Grapple with the Past (mill 3 + retrieve a creature or land), Frantic Search (draw 2, discard 2, untap up to 3 lands — effectively free filtering).
- **Discard outlets / selection:** Psychic Frog (discard pumps with +1/+1 counter, draws on combat damage to a player or planeswalker; flying costs exiling 3 from yard so use sparingly), Tortured Existence (discard a creature → return a creature from yard to hand, repeatable for {B}), Ripples of Undeath (first main phase mill 3; pay {1} and 3 life to put one of those into your hand).
- **Scry-ish dredge fuel from the manabase:** Cephalid Coliseum (threshold ability — 7+ in yard — sac for target player draws 3 / discards 3, useful as a self-discard outlet on demand), Fetid Pools (cycling), Drownyard Temple (free to cast, pay {3} to recur from graveyard — looping fuel for sac costs and Crop Rotation).
- **Fetchlands** (Misty Rainforest, Verdant Catacombs, Prismatic Vista, Terramorphic Expanse) trigger Hedron Crab and feed the loam loop directly.

**Half 2 — Exploit the Graveyard:**

- **Land recursion:** Life from the Loam (dredge + retrieve), Crucible of Worlds (play lands from graveyard), Ramunap Excavator (Crucible on a 2/3 body), Conduit of Worlds (play lands from graveyard *and* a sorcery-speed activated ability that lets you cast a single nonland permanent from your graveyard per turn), Splendid Reclamation (return all land cards from yard to battlefield tapped — game-warping with a stocked yard), Titania, Protector of Argoth (ETB returns a land from graveyard; whenever a land you control hits the graveyard, create a 5/3 Elemental).
- **Creature recursion:** Meren of Clan Nel Toth (end-step recursion scaling with experience counters), Muldrotha, the Gravetide (cast one of each permanent type from graveyard per your turn), Phyrexian Reclamation ({1}{B} + 2 life: return a creature from yard to hand, repeatable), Eternal Witness (ETB returns any card from yard to hand), Oversold Cemetery (upkeep recursion if you have 4+ creature cards in yard), The Scarab God ({2}{U}{B}: exile target creature card from any graveyard, create a 4/4 black Zombie copy; upkeep drain X / scry X per Zombie you control — drain matters), Wight of the Reliquary (vigilance, +1/+1 per creature in yard, tap+sac for any land).
- **Six** is its own engine: mills 3 on attack and lets you grab a land from among them, *plus* gives all your nonland permanent cards retrace during your turn (cast permanent cards from graveyard by discarding a land in addition to other costs). With recurring lands, retrace turns the deck into a permanent-loop machine.
- **Mass reanimation:** Living Death (each player exiles all creature cards from yard, sacs all creatures, then everyone puts the exiled cards onto the battlefield — your yard is stocked, opponents' usually aren't), Dread Return (flashback by sacrificing 3 creatures), Victimize (sac one, return two tapped), Afterlife from the Loam (8-mana **delve** sorcery — for each player, reanimate one of their creatures as a Zombie under your control; this is a payoff, not a mill enabler, and it exiles yard cards via delve so spend carefully).

### The Loam Loop

The signature play pattern. Life from the Loam returns 3 lands from graveyard to hand (typically fetchlands). Play one, crack it (the fetch hits the graveyard, Hedron Crab mills 3, Gitrog draws a card). Next draw step, dredge Life from the Loam back instead of drawing (mills 3 more). Each cycle:

- Mills 6 cards (3 from dredge + 3 from one Hedron Crab landfall trigger)
- Triggers Gitrog **once** if at least one land card hit your graveyard during the cycle (Gitrog draws once per simultaneous batch, not per land)
- Creates a Zombie Druid token from Teval's static whenever any card left your graveyard during the cycle
- Creates a 2/2 Zombie from Field of the Dead if you control 7+ uniquely-named lands and a new differently-named land entered
- Creates a 5/3 Elemental from Titania if a land of yours hit the graveyard
- Grows the yard for Living Death / Splendid Reclamation / Dread Return

With Azusa (2 extra land drops/turn) or Exploration (1 extra), the loop stretches to 2–3 land drops per turn, multiplying every trigger above.

-----

## Kill Lines

**Line 1 — Tooth and Nail entwined.** {5}{G}{G} entwined for {2} = 9 mana. Tutor any two creatures and put both onto the battlefield. Standard payoff: Craterhoof Behemoth + a fatty (Lord of Extinction, Muldrotha, Scarab God). Craterhoof gives all your creatures trample and +X/+X where X = creatures you control; with even 3–4 zombies/elementals from Teval, Sidisi, Field of the Dead, or Titania already in play, this is lethal.

**Line 2 — Jarad fling.** Jarad, Golgari Lich Lord activates for {1}{B}{G}, sacrifice another creature: each opponent loses life equal to its power. Lord of Extinction's P/T equals cards in all graveyards. Late game, that's typically 30–60. Sacrifice Lord of Extinction → each opponent eats 30–60 damage. Jarad himself recurs by sacrificing a Swamp and a Forest. Reanimating Lord of Extinction is trivial via Dread Return / Victimize / Living Death. The whole package is tutorable — Final Parting puts Lord of Extinction in yard and a reanimation spell or Jarad in hand.

**Line 3 — Living Death asymmetry.** The deck stocks creature cards in its yard far faster than opponents do. Cast Living Death after a few cycles of self-mill: your side returns a fistful of bombs, opponents' sides return whatever they happen to have (usually little). Combined with Wonder in the graveyard (gives all your creatures flying as long as you control an Island), the swing the next turn is usually game.

**Line 4 — Craterhoof from graveyard.** Mill or discard Craterhoof, reanimate via Dread Return (flashback, free from yard), Victimize, or Living Death. Wonder makes the alpha strike unblockable by anything without flying or reach. The deck naturally builds wide (Teval Druids, Sidisi Zombies, Field of the Dead Zombies, Titania Elementals), so Craterhoof's pump is large by default.

**Line 5 — Exsanguinate.** {X}{B}{B} sorcery: each opponent loses X, you gain life equal to total lost. The deck doesn't have Cabal Coffers or Urborg — this isn't a Sultai-mono-B mana engine — but Splendid Reclamation returning 8–12 lands at once, plus Sol Ring / signets / fetched bouncelands, gets X to 12–18 in the late game, which kills the table outright in three-opponent games.

**Line 6 — Unmarked Grave + reanimation.** Unmarked Grave is sorcery-speed and **nonlegendary only**, but it tutors Craterhoof (nonlegendary) directly into the graveyard. Cast Unmarked Grave for Craterhoof, then Dread Return / Victimize / Living Death the next turn. Two-card kill on T6–T7 with ramp.

-----

## Conversion Check Breakdown

### Core Loop: 5/5

25+ cards directly serve the fill-graveyard / exploit-graveyard cycle. The loop is self-reinforcing and has multiple redundant payoffs (Crucible, Ramunap, Conduit, Muldrotha, Meren, Six, Gitrog all provide independent recursion paths). Life from the Loam alone sustains the engine indefinitely once online. Cover Teval and the engine remains immediately recognizable. Textbook 5.

### Kill Reliability: 5/5

Six distinct closing lines, several of which are 1–2 card kills from a stocked yard. Tooth and Nail closes the turn it resolves. Jarad + Lord of Extinction is a tutorable 2-card combo for 30–60 damage. Living Death wins on raw asymmetry. The deck also threatens at instant speed (Jarad activation is an activated ability) which compresses the response window for opponents. Strong positions become decisive within 1–2 turns.

### Durability: 5/5

The defining axis. Board wipes feed the engine — anything that dies fuels Living Death, Splendid Reclamation, and the recursion package. Commander removal barely matters because the engine is distributed across Crucible, Ramunap, Conduit, Muldrotha, Meren, Gitrog, and Six. The deck recovers from a turn-7 wipe faster than any other in the collection — usually faster than the player who cast the wipe. Wipes often make the deck stronger.

The actual vulnerability is graveyard exile (Rest in Peace, Leyline of the Void, Bojuka Bog from an opponent, Soul-Guide Lantern). The deck answers with Tear Asunder (kicked exile of any nonland permanent — beats indestructible; bypasses Rest in Peace), Assassin's Trophy, Beast Within, Boseiju (channel destroys artifact/enchantment/nonbasic land of an opponent), and Dauthi Voidwalker as proactive hate that doubles as a free-cast threat. Even after a yard exile, normal self-mill rebuilds in 2–3 turns.

### Interaction: 4/5

Roughly 14–15 pieces depending on what you count:

- **Counterspells (4):** Fierce Guardianship (free with commander), Swan Song (enchantment/instant/sorcery only — does not counter creatures), An Offer You Can't Refuse ({U}, gives opponent 2 Treasures), Counterspell ({U}{U}).
- **Targeted removal (4):** Assassin's Trophy (any permanent, ramps opponent), Beast Within (any permanent, gives opponent a 3/3), Tear Asunder ({1}{G} exile artifact/enchantment; kick {1}{B} for any nonland permanent), Lethal Scheme ({2}{B}{B} instant convoke kill — destroy creature/planeswalker; each convoking creature **connives**, drawing+discarding and getting a +1/+1 counter on a nonland discard).
- **Channel lands as utility removal (2):** Boseiju Who Endures, Otawara Soaring City. These don't draw a card slot and double as colored mana, so they're effectively free interaction.
- **Board wipe (1):** Toxic Deluge (scalable, pay X life).
- **Mass recursion as functional wipe (1):** Living Death.
- **Protection (2):** Heroic Intervention (hexproof + indestructible for permanents), Lightning Greaves (shroud + haste, equip {0}).
- **Proactive yard hate (2):** Dauthi Voidwalker (replaces opponents' yard with exile-with-void-counter; sac to play one of those exiled cards for free), Bojuka Bog (ETB exile a player's yard).

Doesn't reach 5 because counterspells are thin (4 total, only 1 free), there are no unrestricted tutors to find specific answers, and Swan Song / An Offer You Can't Refuse both have downsides (no creature counter, opponent gets Treasures). Against pod combo decks the deck must draw answers naturally rather than tutor for them. A 5 would require 6+ counters or a free tutor for the answer slot.

### Total: 19/20 — near-ceiling. Grinds harder than anyone, closes faster than it looks.

-----

## Bracket 3 Compliance

**Game Changers (3 of 3 — at hard cap):**

1. **Fierce Guardianship** — free counter on a noncreature spell with commander in play.
2. **Crop Rotation** — instant sacrifice-a-land tutor for any land. Most often grabs Field of the Dead, Bojuka Bog, or Cephalid Coliseum.
3. **Field of the Dead** — colorless land that creates a 2/2 Zombie whenever a land enters and you control 7+ uniquely-named lands. The deck's manabase is built around this.

**No additional Game Changers may be added without cutting one of the above.** This invalidates a previous note suggesting open slots; the deck is at the cap.

**Infinite combos:** None. Gravecrawler is in the deck (recast from yard while you control a Zombie), but there is no Phyrexian Altar / Rooftop Storm / Diregraf Captain to enable a loop.

**Extra turns:** None.

**Mass land denial:** None. The deck recurs its own lands; it never destroys opponents'.

**Tooth and Nail:** Removed from the Game Changer list October 2025. No longer a Bracket 3 concern from a list-compliance standpoint, though it is a single-card win condition and may merit Rule 0 disclosure at unfamiliar tables.

-----

## Pod Fit

1. **Best long-game deck in the collection.** The graveyard engine outpaces any fair strategy in turn-by-turn value. In games that go past T8, the deck is favored against everything except resolved combo.
2. **Resilient to disruption.** Wipes feed the engine. Commander removal doesn't matter. The deck punishes interaction.
3. **Vulnerable to graveyard hate.** Rest in Peace, Leyline of the Void, opponent-controlled Dauthi Voidwalker, and yard-exile effects are the real threats. The deck has 4 answers (Tear Asunder, Assassin's Trophy, Beast Within, Boseiju) but must find one.
4. **Vulnerable to fast combo.** 4 counterspells in a 99-card deck is thin. A combo player who resolves their key piece on T4–5 wins before the grind matters.
5. **Threat perception management.** Tooth and Nail, Living Death, and Splendid Reclamation are all visible "I win now" buttons once seen. After the first deployment, opponents will prioritize keeping you off 9 mana / removing your Living Death turn. Don't telegraph the kill.

-----

## Differentiation From Other Decks

| | Teval (The Loam Cycle) | Scarab God (Curse of the Scarab) | Golbez (Crystal Sickness) |
|---|---|---|---|
| Engine | Self-mill + land recursion + value loops | Zombie tribal + graveyard exile + drain | Buried Alive → animate → big body |
| Graveyard role | Recur own creatures and lands; yard is fuel | Exile from any graveyard as 4/4 Zombies | Stage 2–3 reanimation targets |
| Kill speed | Fast (Tooth and Nail T6–8) | Moderate (incremental drain + tribal) | Moderate (animate Sheoldred / titan) |
| Colors | BUG | UB | UB |
| Durability | Extremely high (graveyard survives wipes) | High (zombies rebuild) | Medium (relies on yard targets) |

All three touch the graveyard but use entirely different resources: Teval recurs own yard and lands, Scarab God exiles from all yards, Golbez stages targeted reanimation. No shared engine pieces.

-----

## Decklist (100 cards)

### Commander (1)
1 Teval, the Balanced Scale

### Game Changers (3)
1 Fierce Guardianship
1 Crop Rotation
1 Field of the Dead

### Self-Mill Creatures (4)
1 Hedron Crab
1 Stitcher's Supplier
1 Sidisi, Brood Tyrant
1 World Shaper

### Self-Mill / Filter Spells (3)
1 Life from the Loam
1 Grapple with the Past
1 Frantic Search

### Discard / Selection Engines (3)
1 Psychic Frog
1 Tortured Existence
1 Ripples of Undeath

### Land Recursion (4)
1 Crucible of Worlds
1 Conduit of Worlds
1 Ramunap Excavator
1 Splendid Reclamation

### Extra Land Drops (2)
1 Azusa, Lost but Seeking
1 Exploration

### Creature Recursion (5)
1 Meren of Clan Nel Toth
1 Muldrotha, the Gravetide
1 Phyrexian Reclamation
1 Eternal Witness
1 Oversold Cemetery

### Mass Reanimation (4)
1 Living Death
1 Dread Return
1 Victimize
1 Afterlife from the Loam

### Graveyard Tutors (2)
1 Unmarked Grave
1 Final Parting

### Land Tutors (2)
1 Expedition Map
1 Wight of the Reliquary

### Kill Pieces (4)
1 Craterhoof Behemoth
1 Lord of Extinction
1 Jarad, Golgari Lich Lord
1 Exsanguinate

### Utility Closers (1)
1 Tooth and Nail

### Value Creatures (5)
1 The Gitrog Monster
1 The Scarab God
1 Titania, Protector of Argoth
1 Six
1 Gravecrawler

### Evasion Enabler (1)
1 Wonder

### Counterspells (3)
1 Counterspell
1 Swan Song
1 An Offer You Can't Refuse

### Targeted Removal (4)
1 Assassin's Trophy
1 Beast Within
1 Tear Asunder
1 Lethal Scheme

### Value Enchantment (1)
1 Teval's Judgment

### Board Wipe (1)
1 Toxic Deluge

### Protection (2)
1 Heroic Intervention
1 Lightning Greaves

### Proactive Yard Hate (2)
1 Dauthi Voidwalker
1 Bojuka Bog

### Card Draw (1)
1 Sylvan Library

### Ramp (6)
1 Sol Ring
1 Arcane Signet
1 Farseek
1 Three Visits
1 Harrow
1 Sakura-Tribe Elder

### Lands (38)
1 Command Tower
1 Command Beacon
1 Exotic Orchard
1 Breeding Pool
1 Overgrown Tomb
1 Watery Grave
1 Misty Rainforest
1 Verdant Catacombs
1 Prismatic Vista
1 Terramorphic Expanse
1 Cephalid Coliseum
1 Fetid Pools
1 Drownyard Temple
1 Golgari Rot Farm
1 Otawara, Soaring City
1 Boseiju, Who Endures
1 Hinterland Harbor
1 Woodland Cemetery
1 Darkwater Catacombs
1 Dreamroot Cascade
1 Sunken Hollow
1 Morphic Pool
1 Rejuvenating Springs
1 Undergrowth Stadium
1 Llanowar Wastes
1 Bojuka Bog
1 Field of the Dead
4 Forest
3 Island
4 Swamp

*Note: Field of the Dead is also listed under Game Changers above; Bojuka Bog is also listed under Proactive Yard Hate. Each card appears exactly once in the `.txt` decklist — descriptive section labels above can overlap. The authoritative card list is the `.txt` decklist (99 mainboard + 1 commander = 100).*

-----

## Changelog

- **2026-05-03:** Full card-text re-audit. Corrected Game Changer count (1/3 → 3/3); corrected Ripples of Undeath text; corrected Teval framing (added zombie token engine); reclassified Teval's Judgment as value (not removal) and Afterlife from the Loam as mass reanimation (not self-mill); fixed Sidisi text (mills on enter+attack, library-mill triggers tokens); fixed Psychic Frog (draws on combat damage, not mills); fixed Lethal Scheme (connive, not surveil); fixed Unmarked Grave (sorcery-speed, nonlegendary only); removed phantom references to Entomb, Cabal Coffers, and Urborg; added coverage for Six's retrace, Conduit's second ability, Dauthi's full power, Scarab God's drain, Gitrog's land tax, Wonder's evasion role, channel lands as interaction.
- **Pre-2026-05-03:** previous summary versions present in the original document; treat anything authored before this date with skepticism until re-verified.
