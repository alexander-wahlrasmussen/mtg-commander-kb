# Diminishing Returns — Teysa Karlov

## Quick Reference

| Field | Value |
|---|---|
| **Commander** | Teysa Karlov ({2}{W}{B}, 2/4 Legendary Creature — Human Advisor) |
| **Colors** | Orzhov (WB) |
| **Archetype** | Aristocrats / Sacrifice-Drain |
| **Bracket** | 3 (3 Game Changers used; no early two-card infinites; no MLD; no extra turns) |
| **Game Changers** | Farewell, Smothering Tithe, Teferi's Protection (3 of 3 slots used) |
| **Conversion Check** | **17/20** (5/4/4/4) |
| **Kill Window** | Goldfish: T7–9 · Through interaction: T9–12 |

-----

## Commander Rules Text

Teysa Karlov has two abilities:

1. **Death trigger doubling:** If a creature dying causes a triggered ability of a permanent you control to trigger, that ability triggers an additional time.
2. **Token keyword granting:** Creature tokens you control have vigilance and lifelink.

Key rulings: Teysa doubles the number of triggers, not the effect of each trigger. She doubles triggers from any permanent you control, not just your own creatures dying. Tokens with lifelink and vigilance are relevant for stabilizing after drain chains or blocking while attacking with an aristocrats board.

-----

## What the Deck Does

The deck converts creatures into damage through a three-part engine:

**Layer 1 — Sacrifice Outlets (8 permanents + 1 land):** Viscera Seer (free, scry), Carrion Feeder (free, grows), Yahenni (free, indestructible), Woe Strider (free, scry), Ashnod's Altar (free, {C}{C}), Phyrexian Altar (free, any color), Altar of Dementia (free, mill), Priest of Forgotten Gods ({T} + sac 2, draws + mana + edict), Phyrexian Tower (land, sac for {B}{B}). Skullclamp and Soldevi Adnate also function as pseudo-sac outlets. Razaketh sacrifices creatures to tutor.

**Layer 2 — Death Trigger Payoffs (8 pieces):** Zulaport Cutthroat (drain 1 per death), Nadier's Nightblade (drain 1 per token death), Mirkwood Bats (drain 1 per token ETB/death), Agent of the Iron Throne (drain 1 per death), Syr Konrad (damage 1 per creature entering or leaving graveyard), Midnight Reaper (draw per nontoken death), Morbid Opportunist (draw per opponent's-turn death), Desecrated Tomb (bat token per creature leaving graveyard). All of these are doubled by Teysa.

**Layer 3 — Recursive Creatures and Reanimation:** Gravecrawler recasts from graveyard for {B} if you control a Zombie (Gray Merchant, Midnight Reaper, Fleshbag Marauder are Zombies). Reanimate, Animate Dead, Necromancy, Victimize, and Living Death recycle high-value creatures. K'rrik reduces the mana cost of all black spells by converting {B} to 2 life, accelerating the entire engine by 1–2 turns.

**The play pattern:** Deploy a sac outlet and a drain payoff in the early game. Land Teysa to double all death triggers. Sacrifice creatures, drain the table, draw cards off the deaths, replay creatures from graveyard or via reanimation. Each cycle generates more resources than it costs. Razaketh tutors any missing piece. K'rrik lets you pay life instead of black mana, and the drain triggers pay the life back with interest.

-----

## Kill Lines

**Line 1 — Gravecrawler Loop**
Gravecrawler + Phyrexian Altar + any Zombie on the battlefield + any drain payoff. Sacrifice Gravecrawler to Phyrexian Altar for {B}. Recast Gravecrawler for {B}. Each cycle triggers drain payoffs, doubled by Teysa. Repeat until all opponents are dead. This is mana-neutral and deterministic once assembled. Requires 4 pieces (Gravecrawler, Phyrexian Altar, a Zombie, a drain piece), but Razaketh can tutor all of them.

**Line 2 — Gray Merchant Recursion**
Gray Merchant of Asphodel drains each opponent for your devotion to black. Teysa doubles the trigger. With K'rrik ({B/P}{B/P}{B/P} = 3 devotion), Teysa ({W}{B} = 1), and Gary himself ({B}{B} = 2), devotion is 6 minimum. Doubled by Teysa: each opponent loses 12, you gain 36. Sacrifice Gary, reanimate him with Animate Dead / Necromancy / Victimize, drain again. Each cycle gains more life than you spend.

**Line 3 — Kokusho Drain Chain**
Kokusho dies → each opponent loses 5, you gain 15. Teysa doubles: each opponent loses 10, you gain 30. Sacrifice and reanimate repeatedly. Two Kokusho deaths (doubled) = 60 life drained from the table.

**Line 4 — Living Death Reset**
Stock the graveyard through self-mill (Stitcher's Supplier, Altar of Dementia), looting, and natural play. Living Death sacrifices all creatures on the battlefield (triggering all your death payoffs, doubled by Teysa) and returns everything from your graveyard. Your graveyard is stacked with Gray Merchant, Kokusho, Razaketh, Sephiroth, and drain creatures. Opponents' graveyards are usually worse.

**Line 5 — Razaketh Tutor Chain**
Razaketh sacrifices creatures to tutor any card. With token generators (Desecrated Tomb bats from graveyard recursion, Woe Strider goat token, Sephiroth tokens), Razaketh finds the exact combination needed to close. Typical line: tutor Gravecrawler + Phyrexian Altar + drain piece for Line 1.

-----

## K'rrik Integration (MH3 Upgrade)

K'rrik, Son of Yawgmoth converts every {B} in any mana cost to 2 life. This transforms the deck's speed:

| Card | Normal Cost | With K'rrik |
|---|---|---|
| Dark Ritual | {B} → {B}{B}{B} | 2 life → {B}{B}{B} |
| Reanimate | {B} + life | 2 life + creature MV life |
| Animate Dead | {1}{B} | {1} + 2 life |
| Necromancy | {2}{B} | {2} + 2 life |
| Living Death | {3}{B}{B} | {3} + 4 life |
| Gray Merchant | {3}{B}{B} | {3} + 4 life (then drain 12+ back) |
| Kokusho | {4}{B}{B} | {4} + 4 life (then drain 30 back) |
| Gravecrawler | {B} | 2 life (free with Phyrexian Altar) |
| Victimize | {2}{B} + sac | {2} + 2 life + sac |

K'rrik also contributes 3 devotion to black (his {B/P}{B/P}{B/P} counts), boosting Gray Merchant drains. He has lifelink, partially offsetting life payments. He enables turn 3–4 explosive starts (Dark Ritual for 2 life → chain into reanimation) that the deck previously couldn't achieve until turn 5–6.

The life cost is a non-issue in this deck. Every drain trigger gains life. A single doubled Gray Merchant or Kokusho death repays any life K'rrik spent.

-----

## Conversion Check Breakdown

### Core Loop: 5/5

The loop is "sacrifice creatures → death triggers doubled by Teysa → drain opponents, draw cards, generate tokens → sacrifice again." 26+ cards directly serve this loop across three layers (9 sac outlets counting Phyrexian Tower, 8 death trigger payoffs, 5 reanimation spells, plus Gravecrawler, K'rrik, Dark Ritual, and card draw creatures). The loop is immediately identifiable from the decklist. Teysa is a powerful accelerant (doubling triggers is massive) but the deck still functions without her — sacrificing creatures to drain is the plan regardless; Teysa makes it twice as fast.

**Checkpoint:** Cover the commander. The 99 screams aristocrats sacrifice — sac outlets, drain payoffs, recursive creatures, reanimation. Unmistakable.

### Kill Reliability: 4/5

Five distinct closing lines, including one deterministic loop (Gravecrawler + Phyrexian Altar). Razaketh tutors any missing piece directly. Gray Merchant and Kokusho each threaten lethal in 1–2 sacrifice/reanimate cycles with Teysa out. Estimated 2–3 turns from engine-online to kill. K'rrik accelerates the clock by reducing the mana needed for each reanimation cycle.

Doesn't reach 5 because the deterministic loop requires 4 specific pieces. The non-loop lines (Gary recursion, Kokusho chain) are strong but require reanimation spells in hand and a turn cycle between each iteration. No single-card "I win" equivalent to Tooth and Nail.

**Checkpoint:** Gravecrawler loop kills deterministically. Gary recursion kills in 2 cycles. Both achievable within 2–3 turns of engine-online.

### Durability: 4/5

Five reanimation spells recover key creatures. Gravecrawler self-recurs from the graveyard. Living Death is a full-board reset that favors the deck with the fullest graveyard. Teferi's Protection and Flawless Maneuver dodge board wipes entirely. Phyrexian Tower lets you sacrifice in response to removal for value. K'rrik enables fast rebuilds by converting life into mana.

After a board wipe: reanimate a key creature for 1–3 mana, or cast Living Death to rebuild everything at once. Threatening again in 1–2 turns. Teysa is an accelerant, not a dependency — her removal doesn't stop the sacrifice plan, just halves the trigger output.

Doesn't reach 5 because the deck fundamentally needs creatures on the battlefield to function. Repeated wraths with no reanimation in hand is a real vulnerability. Graveyard exile (Bojuka Bog, Rest in Peace) shuts off Gravecrawler recursion and Living Death simultaneously.

**Checkpoint:** Cyclonic Rift on turn 7. Reanimate Razaketh (1 mana + 8 life, or just 10 life with K'rrik), sacrifice any creature to tutor the next reanimation target or Gravecrawler. Threatening again in 1–2 turns.

### Interaction: 4/5

12 interaction pieces across multiple types:

- **Targeted removal (5):** Swords to Plowshares, Path to Exile, Generous Gift, Feed the Swarm, Cathar Commando
- **Edict effects (3):** Fleshbag Marauder, Merciless Executioner, Plaguecrafter — each doubled by Teysa, forcing opponents to sacrifice 2 permanents
- **Board wipes (2):** Toxic Deluge, Farewell
- **Protection (5):** Teferi's Protection, Flawless Maneuver, Selfless Spirit, Grand Abolisher, Lightning Greaves
- **Creature protection (2):** Giver of Runes, Mother of Runes

The edict creatures double as sacrifice fodder — they interact with the table AND feed the engine. Grand Abolisher protects combo turns. Teferi's Protection is a hard reset button.

Doesn't reach 5 because the deck has zero counterspells. Orzhov can't counter spells, so a combo that resolves on the stack can't be stopped — only prevented proactively (Grand Abolisher on your turn) or punished afterward (Fleshbag effects). Against the pod's combo player, this is a meaningful gap compared to blue decks.

### Total: 17/20 — Structurally excellent. Pilot skill is the main variable.

The MH3 upgrades (K'rrik, Phyrexian Tower) don't change the total score but meaningfully improve the deck's speed and consistency within the existing framework. K'rrik accelerates kill lines by 1–2 turns. Phyrexian Tower adds a sac outlet on a land slot.

-----

## Bracket 3 Compliance

- **Game Changers:** Farewell, Smothering Tithe, Teferi's Protection (3 of 3 slots used). All three GC slots are occupied — no further Game Changers can be added without a swap.
- **Infinite combos:** The Gravecrawler loop is technically infinite but requires 4 pieces (Gravecrawler + Phyrexian Altar + Zombie + drain payoff) and does not consistently assemble before turn 6. Compliant with B3's "no early two-card infinite combos" restriction.
- **Extra turns:** None.
- **Mass land denial:** None.

-----

## Pod Fit

The aristocrats archetype has natural pod advantages:

1. **Hard to interact with.** Drain triggers don't target. Sacrifice triggers can't be countered. The damage comes from multiple small sources, not one big spell.
2. **Punishes removal.** Opponents removing your creatures triggers your payoffs. A board wipe against this deck often deals more damage to the table than it prevents.
3. **Grinds through stax.** The deck operates on small mana increments (1–3 mana per action) and recursive creatures. Tax effects like Rhystic Study or Thalia don't meaningfully slow it.
4. **Weak to graveyard hate.** Rest in Peace, Dauthi Voidwalker, and Bojuka Bog all shut off key lines. The deck has limited answers to enchantments (Feed the Swarm, Generous Gift, Cathar Commando only).
5. **Weak to combo without blue.** No counterspells means the combo player can resolve their win condition if the deck doesn't have Grand Abolisher or a sacrifice-based answer available.

-----

## Differentiation From Other Decks

| | Teysa (Diminishing Returns) | Scarab God (Curse of the Scarab) |
|---|---|---|
| Engine | Sacrifice + death triggers | Zombie tribal + drain |
| Token role | Sacrifice fodder | Persistent army |
| Commander role | Passive doubler | Active reanimator + scry |
| Win speed | Fast (2–3 turns from engine) | Moderate (3–4 turns) |
| Color access | WB (removal + protection) | UB (counters + card draw) |
| Graveyard dependency | High (Gravecrawler, reanimation) | Moderate (Scarab God exiles from GY) |

No overlap in engine pieces. The decks share only generic staples (Sol Ring, lands).

-----

## Decklist (100 cards)

### Commander (1)

1 Teysa Karlov

### Sacrifice Outlets (8)

1 Viscera Seer
1 Carrion Feeder
1 Yahenni, Undying Partisan
1 Woe Strider
1 Ashnod's Altar
1 Phyrexian Altar
1 Altar of Dementia
1 Priest of Forgotten Gods

### Death Trigger Payoffs (8)

1 Zulaport Cutthroat
1 Nadier's Nightblade
1 Mirkwood Bats
1 Agent of the Iron Throne
1 Syr Konrad, the Grim
1 Midnight Reaper
1 Morbid Opportunist
1 Desecrated Tomb

### Drain Bombs (3)

1 Gray Merchant of Asphodel
1 Kokusho, the Evening Star
1 Sephiroth, Fabled SOLDIER

### Mana Acceleration (2)

1 K'rrik, Son of Yawgmoth
1 Dark Ritual

### Edict Creatures (3)

1 Fleshbag Marauder
1 Merciless Executioner
1 Plaguecrafter

### Reanimation (5)

1 Reanimate
1 Animate Dead
1 Necromancy
1 Victimize
1 Living Death

### Tutor / Payoff (2)

1 Razaketh, the Foulblooded
1 Vindictive Lich

### Recursive Creatures (2)

1 Gravecrawler
1 Stitcher's Supplier

### Card Draw (5)

1 Dark Confidant
1 Welcoming Vampire
1 Skullclamp
1 Black Market Connections
1 Soldevi Adnate

### Commander Protection (5)

1 Lightning Greaves
1 Giver of Runes
1 Mother of Runes
1 Selfless Spirit
1 Skrelv, Defector Mite

### Board Protection (3)

1 Teferi's Protection
1 Flawless Maneuver
1 Grand Abolisher

### Targeted Removal (4)

1 Swords to Plowshares
1 Path to Exile
1 Generous Gift
1 Feed the Swarm

### Flexible Removal (2)

1 Cathar Commando
1 Recruiter of the Guard

### Board Wipes (2)

1 Toxic Deluge
1 Farewell

### Ramp Artifacts (6)

1 Sol Ring
1 Arcane Signet
1 Fellwar Stone
1 Mind Stone
1 Thought Vessel
1 Wayfarer's Bauble

### Equipment (1)

1 Swiftfoot Boots

### Other (2)

1 Esper Sentinel
1 Smothering Tithe

### MDFC Land/Spell (1)

1 Malakir Rebirth

### Lands (35 + Malakir Rebirth above = 36 total mana sources)

1 Command Tower
1 Exotic Orchard
1 Phyrexian Tower
1 Urborg, Tomb of Yawgmoth
1 Urza's Saga
1 Bojuka Bog
1 Takenuma, Abandoned Mire
1 Eiganjo, Seat of the Empire
1 Castle Shimura
1 Demolition Field
1 Vault of Champions
1 Concealed Courtyard
1 Caves of Koilos
1 Fabled Passage
1 Prismatic Vista
1 Polluted Delta
1 Verdant Catacombs
1 Desolate Mire
1 Gemstone Caverns
8 Plains
8 Swamp
