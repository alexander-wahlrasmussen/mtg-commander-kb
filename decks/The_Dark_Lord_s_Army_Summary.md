# Deck 13 — The Dark Lord’s Army

**Commander:** Sauron, the Dark Lord ({3}{U}{B}{R}, 7/6 Avatar Horror)  
**Colors:** Grixis (UBR)  
**Archetype:** Amass engine / drain grinder  
**Bracket:** 3 (3 Game Changers: Orcish Bowmasters, Cyclonic Rift, Demonic Tutor)  
**Conversion Check:** 19/20 (5/4/5/5)  
**Kill Window:** **Clock (vs pod-activity — engine is opponent-driven): decap T8–10 / table T11–15 by pod tempo; typical decap T9 / table T12** **(spell, instant — passive drain on opp draws)** (lab 2026-06-13, `dla_clock_lab.py`). Kills FASTER vs active pods (amass/drain feed on opponents' spells + draws). Claim "T8–10 / interaction T10–12" corroborated — among the best in the sweep. See `analysis/Dark_Lords_Army_Clock_Lab_2026-06-13.md`.  
**Ramp:** 10 sources (3 burst / 7 repeatable) · 46 mana sources, 36 land · in band (`ramp_audit.py` 2026-06-21)  
**Estimated buy cost:** ~$369 (48 cards to acquire; 42 already owned with surplus)

-----

## What the Deck Does

Sauron punishes opponents for playing the game. Every spell an opponent casts triggers amass Orcs 1, growing a single Army token passively. The deck gives that Army evasion, connects for combat damage to trigger Ring temptation, then uses the Ring’s draw-4 ability alongside Sheoldred, the Apocalypse to drain massive life every turn cycle. The Army is treated as expendable — sacrifice it for cards, mana, or forced sacrifices, and it reforms for free the next time any opponent casts a spell.

In a 4-player game, Sauron triggers 3+ amass before your next turn just from normal play. The deck doesn’t need to generate its own sacrifice fodder like traditional aristocrats — opponents generate it for you involuntarily.

### The Core Loop

1. **Opponents cast spells** → Sauron amasses Orcs 1 (Army grows passively)
1. **Army connects** (via Cover of Darkness / Corsairs of Umbar / Rogue’s Passage) → Ring tempts you
1. **Ring temptation under Sauron** → Discard hand, draw 4 → +8 life to you (Sheoldred fires on your 4 draws). Defensive cushion, not opponent drain — opponents bleed when *they* draw, not when you do.
1. **Sacrifice Army** to Goblin Bombardment / Yawgmoth / Braids / Skullclamp / Deadly Dispute for value
1. **Army reforms free** on the next opponent’s spell → Return to step 1

### The Oppression Package

The deck runs Ellie’s Rage (Dictate of Erebos, flash), Propaganda, Underworld Dreams, and Wound Reflection to create a tax-and-drain web that makes every action opponents take painful. Braids, Arisen Nightmare forces end-step sacrifices or gives you cards + drain. Yawgmoth provides repeatable sacrifice + draw + removal via -1/-1 counters, and his proliferate grows amass counters. Strionic Resonator copies Sauron’s amass trigger (or Saruman’s, or Pitiless Plunderer’s treasure trigger) for explosive turns. Barad-dûr is a hidden amass engine — `{X}{X}{B}, {T}` to amass Orcs X if a creature died this turn.

### What Makes It Distinct

This deck occupies a unique space compared to other common archetypes:

- **Not traditional aristocrats** (like Teysa) — the sacrifice fodder is free and self-replacing. You never need to invest cards to create things to sacrifice.
- **Not spellslinger** (like Kuja) — damage comes from opponents’ actions, not your own spell sequencing.
- **Not zombie tribal** (like Scarab God) — you have ONE big Army token, not a horde of creatures. The token is a vehicle for Ring temptation and sacrifice value, not a beatdown plan.
- **Not goodstuff** — 22+ cards directly serve Sauron’s amass/Ring/drain engine. The commander is central and irreplaceable.

-----

## Kill Lines

**Line 1 — Drain:** Sheoldred + Underworld Dreams + Bowmasters punish opponents’ card draws — 3 life per draw (Sheoldred 2, Underworld Dreams 1) plus a Bowmasters ping on bonus draws. Wound Reflection doubles opponents’ life loss at end step. Gray Merchant ETB closes from a stocked board (devotion to black is high here). Sauron’s own discard-and-draw ability gains *you* 8 life per Ring tempt under Sheoldred — a defensive cushion that lets the slow drain finish the game.

**Line 2 — Voltron Army:** The Army grows via amass stacking across the turn cycle. With evasion, a 10+ power unblockable token closes games in 2–3 swings.

**Line 3 — Aristocrats Grind:** Dictate of Erebos + Goblin Bombardment + Pitiless Plunderer. Sacrifice the Army → opponents each sacrifice a creature → you get a treasure → Army reforms free on next spell. Not infinite, but relentless.

**Line 4 — Graveyard Reset:** Ring temptation discards stock the graveyard. Living Death, Reanimate, Agadeem’s Awakening, or Animate Dead bring back Sheoldred, Gray Merchant, Yawgmoth, etc.


## Conversion Check — 19/20

### Core Loop — 5/5

22+ cards directly serve the amass → evasion → Ring temptation → drain/sac → reform loop. The engine is immediately recognizable from the decklist. Sauron enables the loop (amass triggers come from his ability), but the deck has enough redundancy (Call of the Ring, Sauron Lord of the Rings, Nazgûl ×4, Saruman) that losing the commander temporarily doesn’t shut down the entire strategy. The Army reforms for zero cost, making the loop nearly impossible to fully disrupt without exiling Sauron permanently.

### Kill Reliability — 4/5

Four distinct closing lines (drain, voltron Army, aristocrats grind, graveyard reset). The fastest line (Sheoldred + Ring temptation) kills in 2–3 turn cycles from engine-online. Wound Reflection accelerates all drain lines. The deck can close through removal — Sheoldred dying is painful but not fatal since drain also comes from Underworld Dreams, Orcish Bowmasters, and combat damage. Not a 5 because the deck lacks a single-turn explosive finish; it wins through accumulated advantage over 2–4 turns.

### Durability — 5/5

The Army token reforms for free whenever any opponent casts a spell — this is zero-cost recovery baked into the commander’s text. A board wipe kills the Army, but the next spell anyone casts brings it back. Sauron himself has ward (sacrifice a legendary artifact or legendary creature), making targeted removal extremely costly. The reanimation package (Reanimate, Animate Dead, Necromancy, Living Death, Agadeem’s Awakening) recovers key creatures. Card draw is redundant across Call of the Ring, Black Market Connections, Ring temptation itself, Yawgmoth, Ledger Shredder, Skullclamp, Dauthi Voidwalker (evasive drainer that also exiles opponents’ graveyards), and cantrips. Tutors: Demonic Tutor, Diabolic Intent, Ringsight (color-of-legendary tutor — Sauron is BUR, so it hits anything).

### Interaction — 5/5

15 interaction pieces across multiple types and speeds:

- **Counterspells (6):** Counterspell, Mana Drain, Force of Negation, Swan Song, It’ll Quench Ya! (Mana Leak variant), Deflecting Swat
- **Creature removal (4):** Go for the Throat, Deadly Rollick, Claim the Precious, Yawgmoth (-1/-1 counters)
- **Catch-all removal (1):** Chaos Warp
- **Enchantment removal (1):** Feed the Swarm
- **Board wipes (3):** Blasphemous Act, Toxic Deluge, Cyclonic Rift

Notably, Mana Drain, Force of Negation, and Deflecting Swat are all free or mana-positive — the deck can interact without falling behind on tempo. Every counterspell opponents cast to fight you also triggers Sauron’s amass.

-----

## Budget Breakdown

|Category                                   |Cards                    |Est. Cost|
|-------------------------------------------|-------------------------|---------|
|Must buy (not in collection)               |18                       |~$232    |
|Additional copies (shared with other decks)|30                       |~$137    |
|Already owned with surplus                 |42                       |$0       |
|**Total**                                  |**90 unique (100 slots)**|**~$369**|

**Big tickets:** Sheoldred (~$90), Cyclonic Rift (~$35), Demonic Tutor (~$35), Force of Negation (~$25), Cover of Darkness (~$15), Snapcaster Mage (~$15), Yawgmoth (~$12), Wound Reflection (~$10).

-----

## Decklist (100 cards)

### Commander (1)

1 Sauron, the Dark Lord

### Amass & Ring Engine (13)

1 Sauron, Lord of the Rings
1 Witch-king of Angmar
1 Saruman, the White Hand
1 Mauhúr, Uruk-hai Captain
4 Nazgûl
1 Corsairs of Umbar
1 Call of the Ring
1 Cover of Darkness
1 March from the Black Gate
1 Strionic Resonator

### Drain Payoffs (5)

1 Sheoldred, the Apocalypse
1 Orcish Bowmasters
1 Underworld Dreams
1 Wound Reflection
1 Gray Merchant of Asphodel

### Sacrifice & Aristocrats (7)

1 Goblin Bombardment
1 Ellie's Rage
1 Braids, Arisen Nightmare
1 Yawgmoth, Thran Physician
1 Pitiless Plunderer
1 Skullclamp
1 Deadly Dispute

### Reanimation (4)

1 Animate Dead
1 Necromancy
1 Reanimate
1 Living Death

### Oppression / Tax (2)

1 Propaganda
1 Black Market Connections

### Utility Creatures (4)

1 Baleful Strix
1 Dauthi Voidwalker
1 Ledger Shredder
1 Snapcaster Mage

### Counterspells (6)

1 Counterspell
1 It'll Quench Ya!
1 Swan Song
1 Mana Drain
1 Force of Negation
1 Deflecting Swat

### Removal & Wipes (9)

1 Cyclonic Rift
1 Deadly Rollick
1 Chaos Warp
1 Go for the Throat
1 Claim the Precious
1 Feed the Swarm
1 Blasphemous Act
1 Toxic Deluge
1 Nihil Spellbomb

### Ramp & Rocks (8)

1 Sol Ring
1 Arcane Signet
1 Talisman of Dominance
1 Talisman of Creativity
1 Fellwar Stone
1 Lightning Greaves
1 Lotus Petal
1 Dark Ritual

### Tutors (3)

1 Demonic Tutor
1 Diabolic Intent
1 Ringsight

### Draw & Selection (2)

1 Night's Whisper
1 Faithless Looting

### Lands (36)

1 Agadeem's Awakening
1 Barad-dûr
1 Blood Crypt
1 Bloodstained Mire
1 Command Tower
1 Crumbling Necropolis
1 Dragonskull Summit
1 Drowned Catacomb
1 Exotic Orchard
1 Fabled Passage
1 Haunted Ridge
3 Island
1 Luxury Suite
1 Morphic Pool
2 Mountain
1 Otawara, Soaring City
1 Polluted Delta
1 Rogue's Passage
1 Scalding Tarn
1 Shipwreck Marsh
1 Shizo, Death's Storehouse
1 Steam Vents
1 Sulfur Falls
6 Swamp
1 The Black Gate
1 Training Center
1 Undercity Sewers
1 Watery Grave

### Sideboard (not counted in 99)

1 Phyrexian Tower  
1 An Offer You Can’t Refuse  
1 Arcane Denial  
1 Ponder  
1 Preordain

## Don't-Miss Rulings

- **The Ring-tempt draw gains *you* life** (Sheoldred fires on *your* 4 draws) — it's a **defensive cushion, not opponent drain.** Opponents bleed when *they* draw, not when you do.
- **The Army reforms for free on the next opponent's spell** — board wipes are only a speed bump, so sacrifice it freely for value.
- **Sauron has ward — sacrifice a legendary artifact or legendary creature** — which makes targeted removal on him very expensive for opponents.
- **Strionic Resonator copies Sauron's amass trigger** (also works on Saruman's amass or Pitiless Plunderer's Treasure trigger) for explosive turns.
- **Barad-dûr is a hidden amass engine:** {X}{X}{B}, {T}: amass Orcs X if a creature died this turn.
- **Yawgmoth proliferates the amass counters** (and his -1/-1 counters double as removal).
- **Reanimation pulls from the graveyard, not amass** — it's a separate recovery tool, not part of the Army loop.

## Piloting Notes (for borrowers)

**Mulligan.** Looking for: **lands + ramp toward a turn-5–6 Sauron**, plus an early drain piece (Underworld Dreams, Sheoldred) or interaction to survive into the grind.

- **Keep:** ramp into Sauron with a drain enabler or counters to back it up.
- **Toss:** no-land hands; payoff cards with no mana behind them.
- You **do not** need a kill piece in your opener — the engine grinds and the deck draws deep.

**Threats & timing.**

- **Durability is the whole point** — the Army's free reform and Sauron's ward mean you recover from wipes trivially. Don't play scared.
- **There's no single explosive finish** — you win over 2–4 turns of accumulating drain (the slowest clock in the collection). Manage threat perception so you aren't ganged up on before the drain matters.
- **Fast combo can race the grind.** Lean on the counter suite — 6 counters including Mana Drain, Force of Negation, and Deflecting Swat (free/mana-positive) — and remember **every counterspell an opponent casts at you also amasses.**
- **Graveyard hate** clamps the reset backup, but the primary drain doesn't need the yard, so it's survivable.

## Reskins (for borrowers)

| On the card | Really is | What it does |
|---|---|---|
| Ellie's Rage | Dictate of Erebos | Flash enchantment: whenever a creature you control dies, each opponent sacrifices a creature. |
| It'll Quench Ya! | (Mana Leak variant) | Counter a spell unless its controller pays 3. |
