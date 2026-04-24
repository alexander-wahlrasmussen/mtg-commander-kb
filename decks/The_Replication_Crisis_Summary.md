# The Replication Crisis — Satya, Aetherflux Genius

## Quick Reference

| Field | Value |
|---|---|
| **Commander** | Satya, Aetherflux Genius ({1}{U}{R}{W}, 3/4 Legendary Creature — Human Artificer) |
| **Colors** | Jeskai (URW) |
| **Archetype** | ETB / Token Combo |
| **Bracket** | 3 (3 Game Changers; Combat Celebrant 2-card infinite with commander requires combat step, not early) |
| **Game Changers** | Fierce Guardianship, Cyclonic Rift, Deflecting Swat |
| **Conversion Check** | **17/20** (5/4/4/4) |
| **Kill Window** | Goldfish: T5–7 · Through interaction: T7–10 |

-----

## Commander Rules Text

Satya has two abilities:

1. **Aetherflux trigger:** At the beginning of combat on your turn, you may pay {E}{E}. If you do, create a tapped and attacking token that's a copy of another creature you control. That token gains haste. Sacrifice it at the beginning of the next end step.
2. **Energy generation:** Whenever Satya or another creature enters the battlefield under your control, you get {E}.

Key rulings: The token copy enters tapped and attacking, bypassing any "when this attacks" restrictions. The token has all abilities of the copied creature, including ETB triggers. The token dies at end step unless something changes its status (Brudiclad converting it into a different token). Every creature entering — including the token itself — generates energy, so each Satya activation partially refunds the {E}{E} cost.

-----

## What the Deck Does

The deck abuses Satya's ability to create hasty token copies of ETB creatures every combat. Each copy triggers enter-the-battlefield abilities, and each entering creature generates energy to fuel the next copy.

**Layer 1 — ETB Creatures (15 pieces):** The deck runs 15 creatures with strong ETB effects that Satya can copy:

- **Value ETBs:** Cloudblazer (draw 2, gain 2), Wall of Omens (draw 1), Knight of the White Orchid (fetch Plains if behind), Snapcaster Mage (flashback an instant/sorcery)
- **Board impact ETBs:** Inferno Titan (deal 3 damage split), Reflector Mage (bounce a creature), Skyclave Apparition (exile nonland permanent ≤5 MV), Loran of the Third Path (destroy artifact/enchantment), Zealous Conscripts (steal any permanent), Siege-Gang Commander (create 3 goblin tokens)
- **Token/pump ETBs:** Angel of Invention (fabricate 2 + anthem), Blade Splicer (create 3/3 golem with first strike)
- **Utility ETBs:** Charming Prince (scry 2, or flicker another creature, or gain 3), Restoration Angel (flash, flicker a non-Angel)

**Layer 2 — Extra Combats (3 pieces):** Each extra combat gives Satya another activation. Combat Celebrant (exert for extra combat — goes infinite with Satya since each token copy is a new creature that hasn't exerted), Lightning Runner (energy-based extra combats), Aggravated Assault (mana-based infinite combats).

**Layer 3 — ETB Doublers and Multipliers (4 pieces):** Panharmonicon (doubles artifact and creature ETBs), Elesh Norn Mother of Machines (doubles your ETBs, shuts off opponents'), Strionic Resonator (copies any triggered ability), Phelia Exuberant Shepherd (flickers a permanent on each attack, re-triggering its ETB).

**Layer 4 — Token Conversion (1 piece):** Brudiclad, Telchor Engineer creates a Myr token at beginning of combat, then can make all your tokens become copies of any one token. Convert goblin tokens, Myr tokens, and the Satya copy token into copies of Inferno Titan or Angel of Invention for a lethal swing.

**The play pattern:** Turns 1–3: ramp with signets and talismans. Turn 4: deploy Satya. Turn 5+: attack, spend {E}{E} to copy the best ETB creature, trigger its ability, generate energy back, hold up countermagic during opponents' turns. Each combat produces incremental advantage — a free Reflector Mage bounce, a free Inferno Titan ping, a free Cloudblazer draw. The deck snowballs through repeated ETB triggers rather than a single explosive turn.

-----

## Kill Lines

**Line 1 — Combat Celebrant Infinite Combats (primary, 2-card with commander)**
Satya + Combat Celebrant on the battlefield. At beginning of combat, Satya copies Celebrant. The token enters tapped and attacking with haste. Exert the token for an extra combat phase. In the new combat, Satya triggers again, copies Celebrant again, new token exerts again. This loops infinitely — each token is a new creature that hasn't exerted. Satya + whatever other creatures you control attack infinite times. Requires Satya to survive combat and no instant-speed removal during the sequence.

**Line 2 — Aggravated Assault Infinite Combats**
Aggravated Assault costs {3}{R}{R} for each extra combat. Goldspan Dragon creates a Treasure on attack, and any Treasure it generates produces 2 mana. A Satya token copy of Goldspan attacks, creates a Treasure (2 mana from Goldspan's ability), plus the real Goldspan's Treasure = 4 mana from treasures + whatever lands are untapped. With 5+ total mana per combat, this goes infinite. Professional Face-Breaker provides backup treasure generation.

**Line 3 — Brudiclad Token Conversion**
Brudiclad at beginning of combat creates a Myr, then converts all tokens into copies of one token. If you've accumulated goblin tokens (Siege-Gang Commander), golem tokens (Blade Splicer), servo tokens (Angel of Invention), and a Satya copy of Inferno Titan — Brudiclad converts them all into Inferno Titan copies. Each deals 3 damage on attack, and you're swinging with 5+ Inferno Titans.

**Line 4 — Zealous Conscripts Steal**
Satya copies Zealous Conscripts → steal an opponent's best permanent (it enters tapped and attacking alongside your team). With Panharmonicon, steal two permanents. With repeated combats (Celebrant or Aggravated Assault), steal one permanent per combat indefinitely.

**Line 5 — Value Grind**
No single combo — just repeated ETB abuse turn after turn. Inferno Titan copies deal 3 damage each combat. Cloudblazer copies draw 2 each combat. Skyclave Apparition copies exile a permanent each combat. Most pods can't survive 3–4 turns of this without running out of resources.

-----

## Conversion Check Breakdown

### Core Loop: 5/5

23+ cards directly serve the ETB-copy engine. 15 ETB creatures, 3 extra combat pieces, 4 doublers/multipliers, and Brudiclad. The loop is "attack → copy → ETB → snowball" and it's immediately identifiable from the decklist. Satya is the engine's centerpiece, but the deck still functions without her — Panharmonicon, Elesh Norn, Phelia, and Restoration Angel all generate ETB value independently. The energy system is self-sustaining: each Satya activation costs {E}{E}, each creature entering generates {E}, and the token itself generates {E} on entry, so each activation costs a net of {E} at worst.

**Checkpoint:** Cover the commander. The 99 has 15 ETB creatures, Panharmonicon, Elesh Norn, flicker effects, and extra combat pieces. The strategy is unmistakable.

### Kill Reliability: 4/5

Five distinct closing lines, including two infinite combat loops (Celebrant is 2-card with commander, Aggravated Assault is 3-card). The Celebrant line is especially reliable since one half lives in the command zone. Brudiclad provides an alternative lethal swing that doesn't require infinite combats. Estimated 2–3 turns from engine-online to kill.

Doesn't reach 5 because every kill line requires Satya to be attacking — meaning she must survive as a 3/4 through a combat step. Instant-speed removal in response to the combat trigger shuts down the turn entirely. The deck has protection (Lightning Greaves, Swiftfoot Boots, Slip Out the Back, Clever Concealment) but can't guarantee Satya survives every time. A 5 would need kills that function independently of the combat step.

**Checkpoint:** Combat Celebrant + Satya = infinite combats from 2 cards. Aggravated Assault + Goldspan Dragon + Satya = infinite combats from 3 cards. Both achievable by turn 5–6.

### Durability: 4/5

The deck has meaningful redundancy across its ETB creature suite — losing any individual creature barely matters since Satya copies whichever is best in the current situation. Elesh Norn and Panharmonicon provide independent value even without Satya. Phelia and Restoration Angel keep the flicker engine running through commander removal.

After a board wipe: replay Satya (4 mana), need at least one ETB creature in hand, then attack next turn. Recovery is 2 turns to be threatening again. The energy system resets on wipe (energy counters persist on the player, not the board), so Satya can immediately copy something if you had banked energy.

Doesn't reach 5 because the deck is meaningfully commander-dependent for its primary game plan. Without Satya, the ETB creatures are solid but not explosive — you're playing fair Magic until she returns. Repeated commander removal (5, 6, 7+ mana) is genuinely painful in a deck that wants to curve out.

**Checkpoint:** Cyclonic Rift on turn 7. Replay Satya for 4 mana, deploy a creature. Next turn, attack and copy. Threatening again in 2 turns.

### Interaction: 4/5

17 interaction and protection pieces:

- **Counterspells (7):** Fierce Guardianship (free), Deflecting Swat (free redirect), Counterspell, Swan Song, An Offer You Can't Refuse, Arcane Denial, Reprieve
- **Removal (7):** Cyclonic Rift (asymmetric wipe), Swords to Plowshares, Path to Exile, Generous Gift, Chaos Warp, Pongify, Abrade
- **Flexible (2):** Narset's Reversal (counter/copy), Prismari Command (removal/ramp/draw)
- **Board protection (4):** Akroma's Will, Clever Concealment, Slip Out the Back, Expansion/Explosion (can copy a counter)
- **Equipment (2):** Lightning Greaves, Swiftfoot Boots

Two free spells (Fierce Guardianship, Deflecting Swat) mean the deck can protect its combo turn while tapped out. Reflector Mage and Skyclave Apparition double as ETB-based interaction that Satya can repeatedly copy.

Doesn't reach 5 because the counterspell suite, while deep, includes several weaker options (Arcane Denial gives the opponent cards, An Offer gives them treasures, Reprieve only delays). The deck also lacks a second board wipe beyond Cyclonic Rift — if Rift is exiled or countered, there's no backup mass answer.

### Total: 17/20 — Structurally excellent. Pilot skill is the main variable.

-----

## Phelia Integration (MH3 Upgrade)

Phelia, Exuberant Shepherd replaced Inspiring Overseer. She's a repeatable flicker engine on a 2-drop:

**What Phelia does in context:**
- Attacks → flickers any nonland permanent → permanent returns at end of combat with its ETBs
- When Satya copies Phelia, the token copy also attacks and flickers something — two flickers per Satya activation
- Can flicker your own ETB creatures (Cloudblazer = draw 2, Reflector Mage = bounce, Skyclave Apparition = exile)
- Can temporarily exile an opponent's threat (it returns at end of combat, but it's gone during your attack)
- At 2 mana, she deploys turn 2, enabling Satya turn 3, combat turn 4 with a flicker target already in play

**What Inspiring Overseer did:** Drew 1 card and gained 1 life on ETB. Functional but the weakest ETB in the creature suite. The deck already has 6+ card draw sources. Phelia's repeatable flicker is engine-quality; Overseer was filler-quality.

## Cursed Mirror Sidegrade (MH3, Optional)

Cursed Mirror replaced Coalition Relic. This is a **sidegrade, not a strict upgrade:**

**What Cursed Mirror does:** 3-mana rock, taps for {R} only. On ETB, becomes a copy of any creature on the battlefield until end of turn with haste. One free attack as the best creature on the board, then stays as a rock.

**What Coalition Relic did:** 3-mana rock, taps for any color. Can charge for a burst turn (5 mana on turn 4).

**Tradeoff:** Cursed Mirror's one-shot creature copy with haste is fun and occasionally high-impact (copy an opponent's bomb, or copy your own Inferno Titan for a surprise 6/6 haste swing). But it only makes {R}, and this is a 3-color deck with double-white (Elesh Norn {3}{W}{W}) and blue-heavy counters. Coalition Relic's any-color flexibility is genuinely valuable.

**Note:** Cursed Mirror does NOT re-trigger the copied creature's ETB — it enters as an artifact, then becomes a copy after ETB resolution. The creature copy gets haste from the Mirror's text, but any ETB the copied creature has does not fire. This limits the upside compared to Satya's copies, which do enter as the creature and trigger ETBs.

**Recommendation:** Keep this swap if you want the more exciting card. Revert to Coalition Relic if you notice color problems in practice.

-----

## Bracket 3 Compliance

**Game Changers (3 of 3):**
1. Fierce Guardianship — free counterspell with commander in play
2. Cyclonic Rift — asymmetric board wipe
3. Deflecting Swat — free redirect with commander in play

**Infinite combos:** Combat Celebrant + Satya is a 2-card infinite using the commander, but it requires a successful attack step (earliest realistic turn 5) and doesn't violate B3's "no early two-card infinite combos" restriction. Aggravated Assault combo is 3-card.

**Extra turns:** None.

**Mass land denial:** None.

-----

## Pod Fit

The ETB/token engine has strong pod characteristics:

1. **Flexible threat assessment.** Satya copies whatever creature is best for the current board state — she can copy removal creatures (Reflector Mage, Skyclave Apparition) when you need answers, or damage creatures (Inferno Titan) when you need to close. One deck, multiple modes.
2. **Incremental rather than explosive.** The deck threatens consistently from turn 5 onward but rarely demands "stop me this turn or die" — making it a secondary threat while the archenemy gets focused.
3. **Punishes empty boards.** When opponents wrath and rebuild slowly, Satya's token copies provide immediate board presence with ETB value. You recover faster than decks that need to assemble multiple pieces.
4. **Weak to stax and pillowfort.** Cards that prevent attacking (Ghostly Prison, Propaganda) or shut off ETBs (Torpor Orb, Hushbringer) directly counter the deck's engine. Limited enchantment removal (Loran, Generous Gift only).
5. **Commander-dependent.** Repeated Satya removal is the most effective counterplay. Without her, the deck is fair creatures with good ETBs but no exponential value.

-----

## Differentiation From Other Decks

| | Satya (Replication Crisis) | Azula (Lightning War) |
|---|---|---|
| Engine | ETB creature copies during combat | Spell doubling during combat |
| Card types | Creature-heavy (15+ ETB creatures) | Spell-heavy (instants/sorceries) |
| Commander role | Active (creates tokens, costs energy) | Passive (copies spells while attacking) |
| Kill method | Infinite combats + ETB damage | Infinite combats + spell burn |
| Color identity | URW (white protection + removal) | UBR (black tutors + removal) |
| Pod role | Flexible value engine | Combo hunter / tempo |

Both decks use combat as their engine phase, but they share zero engine pieces. Satya wants creatures; Azula wants instants and sorceries.

-----

## Decklist (100 cards)

### Commander (1)

1 Satya, Aetherflux Genius

### Game Changers (3)

1 Fierce Guardianship
1 Cyclonic Rift
1 Deflecting Swat

### ETB Creatures — Value (5)

1 Cloudblazer
1 Wall of Omens
1 Knight of the White Orchid
1 Snapcaster Mage
1 Archivist of Oghma

### ETB Creatures — Board Impact (5)

1 Inferno Titan
1 Reflector Mage
1 Skyclave Apparition
1 Loran of the Third Path
1 Zealous Conscripts

### ETB Creatures — Tokens/Pump (3)

1 Angel of Invention
1 Blade Splicer
1 Siege-Gang Commander

### ETB Creatures — Utility (2)

1 Charming Prince
1 Restoration Angel

### Extra Combats (3)

1 Combat Celebrant
1 Lightning Runner
1 Aggravated Assault

### ETB Doublers / Multipliers (4)

1 Panharmonicon
1 Elesh Norn, Mother of Machines
1 Strionic Resonator
1 Phelia, Exuberant Shepherd

### Token Conversion (1)

1 Brudiclad, Telchor Engineer

### Combat Value Creatures (2)

1 Goldspan Dragon
1 Professional Face-Breaker

### Tutors (1)

1 Ranger-Captain of Eos

### Stax / Draw (2)

1 Esper Sentinel
1 Mystic Remora

### Counterspells (5)

1 Counterspell
1 Swan Song
1 An Offer You Can't Refuse
1 Arcane Denial
1 Reprieve

### Removal (5)

1 Swords to Plowshares
1 Path to Exile
1 Generous Gift
1 Chaos Warp
1 Pongify

### Flexible Removal (2)

1 Abrade
1 Prismari Command

### Flexible Interaction (2)

1 Narset's Reversal
1 Expansion/Explosion

### Protection (4)

1 Akroma's Will
1 Clever Concealment
1 Slip Out the Back
1 Lightning Greaves

### Equipment (1)

1 Swiftfoot Boots

### Card Selection (2)

1 Ponder
1 Preordain

### Ramp (11)

1 Sol Ring
1 Arcane Signet
1 Fellwar Stone
1 Mind Stone
1 Cursed Mirror
1 Azorius Signet
1 Boros Signet
1 Izzet Signet
1 Talisman of Conviction
1 Talisman of Creativity
1 Talisman of Progress

### Lands (36)

1 Command Tower
1 Exotic Orchard
1 Hallowed Fountain
1 Sacred Foundry
1 Arid Mesa
1 Glacial Fortress
1 Sulfur Falls
1 Clifftop Retreat
1 Shivan Reef
1 Adarkar Wastes
1 Battlefield Forge
1 Inspiring Vantage
1 Spectator Seating
1 Deserted Beach
1 Sundown Pass
1 Port Town
1 Frostboil Snarl
1 Furycalm Snarl
1 Mystic Monastery
1 Castle Vantress
1 Demolition Field
1 Reliquary Tower
1 Evolving Wilds
5 Island
3 Mountain
5 Plains
