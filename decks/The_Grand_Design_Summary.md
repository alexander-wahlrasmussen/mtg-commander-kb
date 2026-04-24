# The Grand Design — Atraxa, Grand Unifier (Bracket 3, Final)

## Quick Reference

|Field               |Value                                            |
|--------------------|-------------------------------------------------|
|**Commander**       |Atraxa, Grand Unifier (WUBG)                     |
|**Archetype**       |Reanimator / Flicker / Creature Toolbox          |
|**Bracket**         |3 (strict — exactly 3 Game Changers)             |
|**Game Changers**   |Fierce Guardianship, Seedborn Muse, Cyclonic Rift|
|**Conversion Check**|**19/20** (5/5/5/4)                              |
|**Kill Window**     |Goldfish: T6–8 · Through interaction: T8–11      |

-----

## What the Deck Does

Atraxa is a 7-mana 7/7 with flying, vigilance, deathtouch, and lifelink. When she enters the battlefield, reveal the top 10 cards of your library and take one of each card type — typically netting 5–7 cards.

The deck abuses this ETB through three interlocking engines:

**Reanimation Engine (9 spells + Karmic Guide):** The deck’s primary reanimation targets in the early game are Razaketh (repeatable tutor), Vilis (massive draw), and Elesh Norn (ETB doubler) — dumped into the graveyard via Entomb, Buried Alive, or Fauna Shaman, then reanimated for 1–3 mana. Atraxa herself can only be reanimated after she has been cast from the command zone at least once and you choose to send her to the graveyard instead of back to the command zone when she dies. Early game: reanimate bombs. Mid-to-late game: reanimate Atraxa for cheap re-entry.

**Flicker Engine (7 pieces):** Ephemerate, Thassa Deep-Dwelling, Soulherder, Panharmonicon, Restoration Angel, Ghostly Flicker, and Displacer Kitten blink creatures to re-trigger ETBs. Panharmonicon and Elesh Norn Mother of Machines each add one additional ETB trigger — with both in play, each ETB fires 3 times total (base + 1 from Panharmonicon + 1 from Elesh Norn). Note: Elesh Norn also shuts off all opponents’ ETB triggers.

**Creature Toolbox (Birthing Pod + tutors):** Birthing Pod sacrifices a creature to find the next mana value up, directly to the battlefield. Activated at sorcery speed, once per turn. The deck has a complete creature chain from MV 1 through MV 8:

- MV 1: Birds of Paradise
- MV 2: Fauna Shaman, Grand Abolisher, Sakura-Tribe Elder
- MV 3: Ranger-Captain of Eos, Eternal Witness
- MV 4: Restoration Angel, Glen Elendra Archmage
- MV 5: Karmic Guide, Reveillark, Sidisi, Seedborn Muse, Soulherder
- MV 6: Sun Titan
- MV 7: Atraxa (from command zone first, then graveyard), Elesh Norn
- MV 8: Razaketh, Vilis

Chord of Calling (instant speed, convoke) and Eladamri’s Call (instant speed, to hand) supplement Pod as creature tutors.

-----

## How We End Games

### Kill Line 1: Finale of Devastation at X≥10 — Primary One-Card Win

**Cost:** 12 mana (GG + X where X=10). **Cards needed:** Just Finale.

Finale searches your library or graveyard for a creature with MV ≤X, puts it onto the battlefield, and if X≥10, ALL your creatures get +X/+X and haste until end of turn. At X=10, that’s +10/+10 and haste to everything. With even 3 creatures on board, that’s 30+ power with haste and trample (if any creature has it). Lethal to the table.

12 mana is achievable by turn 6–7 with Sol Ring, Arcane Signet, Carpet of Flowers (often adds 3–5 mana from opponents’ Islands), and Seedborn Muse untapping everything on opponents’ turns.

The haste clause also solves the Living Death timing problem — if you cast Living Death to rebuild your board (everything has summoning sickness), casting Finale the following turn gives everything haste, making summoning sickness irrelevant.

### Kill Line 2: Defense of the Heart — Automatic

**Cost:** 4 mana to cast, then free. **Condition:** Any opponent controls 3+ creatures at the beginning of your upkeep.

Sacrifice Defense of the Heart → search your library for two creatures, put them directly onto the battlefield. Standard targets: Razaketh + Elesh Norn. Razaketh immediately tutors for Finale (sac a creature, pay 2 life). Elesh Norn doubles all your future ETBs and shuts off opponents’. Cast Finale next turn to close.

Opponents must either remove Defense before your upkeep or keep their creature count under 3, which cripples most Commander strategies.

### Kill Line 3: Razaketh Reanimation → Tutor Chain

**Setup:** Entomb or Buried Alive dumps Razaketh into graveyard. Reanimate brings him back for 1 mana (pay 8 life).

Razaketh’s ability: pay 2 life, sacrifice another creature, search your library for any card. No tap required — activate as many times as you have life and creatures.

With 2–3 creatures on board after reanimating Razaketh:

1. Sac creature #1 → tutor Finale of Devastation (pay 2 life)
1. Sac creature #2 → tutor Grand Abolisher or Veil of Summer (pay 2 life)
1. Next turn: deploy protection → cast Finale → win

This is a 2-turn kill from a 1-mana Reanimate. The first turn establishes Razaketh and tutors the win; the second turn executes it.

### Kill Line 4: Chord of Calling → Razaketh

**Cost:** X=8 with convoke (tap non-attacking creatures to help pay). Cast on an opponent’s end step.

Razaketh enters at end of opponent’s turn. Sac a creature to tutor Finale. Your turn: cast Finale for the win.

Note: unlike the old Craterhoof line, this works on an opponent’s end step because Razaketh tutors to HAND (not a battlefield buff that expires). You cast Finale on your own turn when the +X/+X and haste matter.

### Kill Line 5: Protected Kill Turns

Four independent protection methods, all tutorable through the creature engine:

|Protector                |How it works                                                                                                                                                            |Limitation                                                                                                                                                     |How you find it                                        |
|-------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------|
|**Grand Abolisher**      |On your turn, opponents can’t cast spells or activate abilities of artifacts, creatures, or enchantments.                                                               |Doesn’t stop planeswalker abilities, land abilities, or triggered abilities.                                                                                   |Chord, Pod, Eladamri’s Call                            |
|**Ranger-Captain of Eos**|Sacrifice: opponents can’t cast **noncreature** spells this turn.                                                                                                       |Does NOT stop creature spells. Opponents could flash in a creature. Stops counterspells, removal, and wraths.                                                  |Chord, Pod, Eladamri’s Call                            |
|**Teferi, Time Raveler** |Static: opponents can only cast spells at sorcery speed.                                                                                                                |Must be on battlefield before the kill turn (loyalty abilities, not an ETB — flickering Teferi resets loyalty but doesn’t trigger anything with Panharmonicon).|Natural draws, Atraxa ETB                              |
|**Veil of Summer**       |1 mana: your spells can’t be countered this turn + you and your permanents get hexproof from blue and black. Draws a card if an opponent has cast a blue or black spell.|Only protects from BLUE and BLACK. White or green interaction is not stopped.                                                                                  |Natural draws, Atraxa ETB, Razaketh tutor, Sidisi tutor|

### Kill Line 6: Karmic Guide + Reveillark Value Loop

**Requires:** Karmic Guide + Reveillark + Razaketh (as a non-tapping sacrifice outlet) all on the battlefield.

1. Sacrifice Karmic Guide to Razaketh (tutor any card, pay 2 life)
1. Sacrifice Reveillark to Razaketh (tutor any card, pay 2 life)
1. Reveillark’s leave-the-battlefield trigger: return Karmic Guide + one other power ≤2 creature (Eternal Witness, Fauna Shaman, etc.) from graveyard
1. Karmic Guide ETB: return Reveillark from graveyard
1. Repeat from step 1

Each cycle: tutor 2 cards, return a utility creature, costs 4 life. Continue until you’ve tutored Finale + protection + anything else needed. This requires 3 specific creatures on the battlefield simultaneously, so it’s the most setup-intensive line but the most powerful once assembled.

Note: Phyrexian Tower does NOT enable this loop because it taps (one sacrifice per turn cycle). Razaketh’s sacrifice ability has no tap requirement, enabling multiple activations per turn.

Valid Reveillark targets in the deck (power ≤2): Karmic Guide (2/2), Eternal Witness (2/1), Fauna Shaman (2/2), Birds of Paradise (0/1), Sakura-Tribe Elder (1/1), Grand Abolisher (2/2), Glen Elendra Archmage (2/2). Note: Ranger-Captain of Eos is 3/3 and is NOT a valid Reveillark target.

### Kill Line 7: Birthing Pod Chain — Incremental Inevitability

Birthing Pod sacrifices a creature to find MV+1, directly to battlefield. **Sorcery speed only, one activation per turn.** This is a multi-turn chain:

- Turn A: Sac Birds (MV 1) → Fauna Shaman (MV 2, dumps reanimation targets)
- Turn B: Sac Fauna Shaman (MV 2) → Eternal Witness (MV 3, returns a spell)
- Turn C: Sac Eternal Witness (MV 3) → Restoration Angel (MV 4, flickers another creature)
- Turn D: Sac Restoration Angel (MV 4) → Karmic Guide (MV 5, reanimates from graveyard)
- Turn E: Sac Karmic Guide (MV 5) → Sun Titan (MV 6, returns MV ≤3 permanent)
- Turn F: Sac Sun Titan (MV 6) → Elesh Norn (MV 7, doubles ETBs)
- Turn G: Sac Elesh Norn (MV 7) → Razaketh (MV 8, tutors anything)

Each step generates value. The chain can’t be stopped by countering a single spell (Pod is an activated ability, not a spell). You don’t need to go all the way to MV 8 — stopping at Karmic Guide or Sidisi is often enough to close.

### Kill Line 8: Living Death — Board Recovery Into Kill

**Cost:** 5 mana. Living Death sacrifices all creatures on the battlefield, then returns all creature cards from all graveyards to the battlefield.

**Critical rules note:** All returned creatures have summoning sickness. They cannot attack the turn they enter. This is NOT a same-turn kill. Living Death rebuilds your board (Atraxa drawing 5–7 on ETB, Elesh Norn doubling triggers, Razaketh ready to tutor) and sets up a kill on the following turn via Finale (which grants haste, bypassing summoning sickness).

### Kill Line 9: Sidisi, Undead Vizier — Exploit Tutor

Sidisi’s exploit ETB sacrifices a creature to tutor any card. With Panharmonicon, the exploit ETB triggers twice — sacrifice two creatures, tutor two cards. With both Panharmonicon and Elesh Norn, it triggers three times. Each exploit that sacrifices a creature generates a separate tutor.

Sidisi can exploit herself (sacrificing herself for one tutor with no other creatures needed). Flickering Sidisi with Ephemerate or Thassa repeats the exploit.

### Kill Line 10: Atraxa Combat — Backup

Atraxa is a 7/7 with flying, vigilance, deathtouch, and lifelink. Three combat steps per player for commander damage lethal (21). Lightning Greaves provides haste for immediate connection. Not flashy, but always available from the command zone.

-----

## Conversion Check Breakdown

### Core Loop: 5/5

Three interlocking engines: 7 flicker pieces, 9 reanimation spells + Karmic Guide, and Birthing Pod with a complete MV 1–8 creature chain. 40+ cards directly serve the engine. Every creature is tutorable, reanimatable, and (mostly) flickerable.

Panharmonicon + Elesh Norn = 3x ETB triggers (not 4x — each adds one additional trigger to the base).

Known interaction restrictions: Restoration Angel cannot flicker Karmic Guide (both are Angels — Restoration Angel says “non-Angel”). All 5 other flicker pieces work on Karmic Guide normally.

Persist (the spell) cannot reanimate legendary creatures (Atraxa, Razaketh, Vilis, Elesh Norn, Sidisi are all legendary). It remains useful as a cheap way to reanimate Karmic Guide, who then reanimates any legendary creature — a 2-card chain rather than a direct reanimate.

### Kill Reliability: 5/5

Eight distinct kill paths plus Atraxa combat as a permanent backup. Finale of Devastation at X≥10 is a one-card win (12 mana). Defense of the Heart is an automatic win. Razaketh provides adaptable tutoring for the exact closer needed. The Karmic Guide + Reveillark + Razaketh loop tutors your entire deck. Birthing Pod provides incremental inevitability over multiple turns.

The deck draws 5–7 cards per Atraxa ETB, making it highly likely to find Finale naturally even without tutoring.

### Durability: 5/5

9 reanimation spells for the primary targets (all cleanly hit legendary creatures except Persist, which chains through Karmic Guide). Living Death and Dread Return work from the graveyard. Karmic Guide provides creature-based reanimation that works with the flicker engine. Fauna Shaman dumps targets into graveyard while finding replacements.

Atraxa can only be reanimated after dying from the battlefield at least once (she starts in the command zone, not the library — Entomb and Buried Alive cannot put her into the graveyard directly). The early reanimation targets are Razaketh, Vilis, and Elesh Norn, which are often better early targets anyway.

### Interaction: 4/5

**Counterspells (5 spells + 1 creature):**

- Fierce Guardianship (GC) — free with Atraxa in play, noncreature spells only
- Force of Negation — free on **opponents’ turns only** (pitch a blue card), noncreature spells only. On your own turn it costs 1UU.
- Counterspell — 2 mana, counters ANY spell
- Mana Drain — 2 mana, counters ANY spell, generates mana
- Swan Song — 1 mana, counters instant/sorcery/enchantment only
- Dovin’s Veto — 2 mana, uncounterable, noncreature spells only
- Glen Elendra Archmage — sacrifice to counter a noncreature spell. Persist returns her with a -1/-1 counter for one more use (2 total per cycle). Flickering removes the counter for 2 more. Not unlimited — 2 per flicker cycle.

**Only Counterspell and Mana Drain can counter creature spells.** Flash creatures and creature-based combos are a gap in the counter suite.

**On your own turn:** 2 free spells (Fierce Guardianship, Deadly Rollick). Force of Negation costs full price.
**On opponents’ turns:** 3 free spells (add Force of Negation).

**Removal (6):** Cyclonic Rift (GC, asymmetric bounce), Deadly Rollick (free with Atraxa), Swords to Plowshares, Path to Exile, Generous Gift, Beast Within, Toxic Deluge

**Proactive disruption (2):** Teferi Time Raveler (opponents can only cast at sorcery speed — note: Teferi’s abilities are loyalty abilities, not ETBs; flickering resets his loyalty but does not trigger Panharmonicon or Elesh Norn), Grand Abolisher (your-turn protection)

**Protection (4):** Heroic Intervention, Flawless Maneuver, Veil of Summer (blue/black only), Lightning Greaves

**Total: 20 interaction and protection pieces.** Excellent quantity and mostly tutorable through the creature engine. The 4/5 ceiling comes from the noncreature-only limitation on most counters and the inability to tutor for noncreature interaction (no Demonic Tutor or Vampiric Tutor — both Game Changers).

-----

## Bracket 3 Compliance

Exactly 3 Game Changers:

1. **Fierce Guardianship** — free counter with commander in play
1. **Seedborn Muse** — untap on every opponent’s turn
1. **Cyclonic Rift** — asymmetric board wipe

**Notable non-GC power cards:** Razaketh, Finale of Devastation, Defense of the Heart, Birthing Pod, Chord of Calling, Force of Negation, Teferi Time Raveler, Mana Drain, Deadly Rollick, Glen Elendra Archmage, Ranger-Captain of Eos, Elesh Norn Mother of Machines, Karmic Guide, Reveillark, Sidisi Undead Vizier, Panharmonicon, Veil of Summer, Carpet of Flowers, Sun Titan, Phyrexian Tower.

-----

## Decklist (100 cards)

### Commander (1)

1 Atraxa, Grand Unifier

### Game Changers (3)

1 Fierce Guardianship
1 Seedborn Muse
1 Cyclonic Rift

### Flicker Engine (7)

1 Ephemerate
1 Thassa, Deep-Dwelling
1 Panharmonicon
1 Soulherder
1 Restoration Angel
1 Ghostly Flicker
1 Displacer Kitten

### Reanimation (9)

1 Reanimate
1 Animate Dead
1 Necromancy
1 Victimize
1 Living Death
1 Dread Return
1 Persist
1 Buried Alive
1 Entomb

### Creatures — Value & Finishers (12)

1 Elesh Norn, Mother of Machines
1 Razaketh, the Foulblooded
1 Vilis, Broker of Blood
1 Sun Titan
1 Karmic Guide
1 Reveillark
1 Sidisi, Undead Vizier
1 Eternal Witness
1 Fauna Shaman
1 Sakura-Tribe Elder
1 Birds of Paradise
1 Grand Abolisher

### Creatures — Interactive (2)

1 Glen Elendra Archmage
1 Ranger-Captain of Eos

### Planeswalker (1)

1 Teferi, Time Raveler

### Tutors & Kill (4)

1 Eladamri’s Call
1 Chord of Calling
1 Birthing Pod
1 Finale of Devastation

### Enchantment — Kill Setup (1)

1 Defense of the Heart

### Counterspells (5)

1 Counterspell
1 Mana Drain
1 Force of Negation
1 Swan Song
1 Dovin’s Veto

### Removal (6)

1 Swords to Plowshares
1 Path to Exile
1 Generous Gift
1 Beast Within
1 Toxic Deluge
1 Deadly Rollick

### Protection (4)

1 Heroic Intervention
1 Flawless Maneuver
1 Veil of Summer
1 Lightning Greaves

### Ramp (6)

1 Sol Ring
1 Arcane Signet
1 Carpet of Flowers
1 Three Visits
1 Nature’s Lore
1 Farseek

### Lands (38)

1 Command Tower
1 Exotic Orchard
1 Breeding Pool
1 Hallowed Fountain
1 Overgrown Tomb
1 Watery Grave
1 Temple Garden
1 Godless Shrine
1 Polluted Delta
1 Windswept Heath
1 Verdant Catacombs
1 Misty Rainforest
1 Flooded Strand
1 Marsh Flats
1 Boseiju, Who Endures
1 Otawara, Soaring City
1 Eiganjo, Seat of the Empire
1 Yavimaya, Cradle of Growth
1 Indatha Triome
1 Zagoth Triome
1 Rejuvenating Springs
1 Undergrowth Stadium
1 Vault of Champions
1 Morphic Pool
1 Phyrexian Tower
1 Reflecting Pool
1 City of Brass
3 Forest
3 Island
4 Plains
2 Swamp

-----

## Shopping List

|Card                     |Role                                     |Est. Price|
|-------------------------|-----------------------------------------|----------|
|Force of Negation        |Free counter (opponents’ turns)          |~$35      |
|Razaketh, the Foulblooded|Repeatable creature tutor / sac outlet   |~$15      |
|Atraxa, Grand Unifier    |Commander                                |~$15      |
|Birthing Pod             |Repeatable creature chain                |~$12      |
|Defense of the Heart     |Automatic 2-creature tutor               |~$10      |
|Finale of Devastation    |One-card win at X≥10                     |~$20      |
|Indatha Triome           |Land                                     |~$8       |
|Zagoth Triome            |Land                                     |~$6       |
|Phyrexian Tower          |Sac outlet on a land                     |~$8       |
|Carpet of Flowers        |Premium ramp                             |~$6       |
|Displacer Kitten         |Flicker on noncreature casts             |~$5       |
|Chord of Calling         |Instant creature tutor with convoke      |~$5       |
|Teferi, Time Raveler     |Sorcery-speed lock                       |~$5       |
|Veil of Summer           |Blue/black protection                    |~$5       |
|Vilis, Broker of Blood   |Draw engine reanimation target           |~$4       |
|Ranger-Captain of Eos    |Tutorable noncreature Silence            |~$4       |
|Sun Titan                |MV 6 Pod bridge + recursion              |~$1       |
|Sidisi, Undead Vizier    |Exploit ETB tutor                        |~$2       |
|Karmic Guide             |Creature-based reanimation               |~$3       |
|Reveillark               |Returns power ≤2 creatures from graveyard|~$1       |
|Glen Elendra Archmage    |2 counters per flicker cycle             |~$2       |
|Fauna Shaman             |Creature tutor + graveyard enabler       |~$3       |
|Persist                  |Cheap reanimate (nonlegendary only)      |~$2       |
|Reflecting Pool          |4-color fixing                           |~$3       |
|City of Brass            |4-color fixing                           |~$5       |
|**Total**                |                                         |**~$210** |

### Conflict cards (need extra copies):

|Card              |Shared with               |Fix cost|
|------------------|--------------------------|--------|
|Reanimate         |Teysa, Sauron             |~$2     |
|Animate Dead      |Sauron                    |~$3     |
|Necromancy        |Sauron                    |~$4     |
|Buried Alive      |Sauron                    |~$2     |
|Swan Song         |Loam Cycle, Sauron        |~$3     |
|Temple Garden     |Bumbleflower, Toph, Sythis|~$10    |
|**Conflict total**|                          |**~$24**|