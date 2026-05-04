# The Replication Crisis — Satya, Aetherflux Genius

## Quick Reference

| Field | Value |
|---|---|
| **Commander** | Satya, Aetherflux Genius ({1}{U}{R}{W}, 3/5 Legendary Creature — Human Artificer) |
| **Colors** | Jeskai (URW) |
| **Archetype** | ETB / Token Combo |
| **Bracket** | 3 (3 Game Changers) |
| **Game Changers** | Fierce Guardianship, Cyclonic Rift, The One Ring (Deflecting Swat remains in deck as a free redirect but no longer counts toward the GC cap as of Oct 2025) |
| **Conversion Check** | **17/20** (5/4/4/4) — *needs rescore after 2026-05-04 swap pass* |
| **Kill Window** | Goldfish: T5–7 · Through interaction: T7–10 |
| **Last swap pass** | 2026-05-04 — 6 cards swapped to add a real infinite (Sword of F&F + AA), token multiplier (Anointed Procession + Adeline), draw engine (Bident, The One Ring), premium ETB (Solitude). See bottom of summary. |

-----

## Commander Rules Text

**Satya, Aetherflux Genius — {1}{U}{R}{W}, 3/5 Legendary Creature — Human Artificer**

- **Menace, haste**
- Whenever Satya **attacks**, create a tapped and attacking token that's a copy of up to one other target **nontoken** creature you control. **You get {E}{E}** (two energy counters). At the beginning of the next end step, sacrifice that token **unless you pay an amount of {E} equal to its mana value**.

Key implications:
- The trigger is **on attack**, not at beginning of combat. Satya must declare-attack each turn for the engine to fire. Aurelia / Helm of the Host / Sword of Feast and Famine etc. that grant additional Satya attacks are direct multipliers.
- Energy is **gained for free** on each Satya attack, not paid. Tokens are kept by paying mana value in {E} at end step (e.g. an Inferno Titan token costs 6{E} to keep). Three attacks bank enough energy to keep one Inferno Titan; six attacks bank enough to keep two.
- The token must copy a **nontoken** creature. Brudiclad-converted tokens cannot be Satya targets.
- Token copies of creatures without haste cannot attack again in extra combats unless **Brudiclad** ("creature tokens you control have haste") is in play or the copied creature itself has haste. This matters for Aggravated Assault / Aurelia loops.
- ETB and "when this attacks" abilities of the copied creature both trigger on the token (it's an ETB *and* enters attacking).

-----

## What the Deck Does

Satya's "whenever attacks" trigger creates a free token copy of any nontoken creature you control, plus 2 free energy. The deck stacks ETB creatures for Satya to repeatedly copy, with token doublers and a real combat-loop kill line.

**Layer 1 — ETB Creatures (16 pieces):** Satya's copy targets, ranked by impact:

- **Value ETBs:** Cloudblazer (draw 2, gain 2), Wall of Omens (draw 1), Knight of the White Orchid (fetch Plains if behind), Snapcaster Mage (flashback an instant/sorcery), Archivist of Oghma (draw on opponent search)
- **Board impact ETBs:** Inferno Titan (deal 3 damage), Reflector Mage (bounce a creature), Skyclave Apparition (exile nonland permanent ≤5 MV), Loran of the Third Path (destroy artifact/enchantment), Zealous Conscripts (steal any permanent), Solitude (exile a creature, lifelink)
- **Token/pump ETBs:** Angel of Invention (fabricate 2 + anthem), Blade Splicer (create 3/3 golem with first strike), Siege-Gang Commander (create 3 goblin tokens), Adeline (Satya copy of Adeline doesn't fire her trigger from entering attacking, but a real attack with Adeline + Satya generates 3 humans/turn for the Brudiclad pile)
- **Utility ETBs:** Restoration Angel (flash, flicker a non-Angel)

**Layer 2 — Combat Engine (1 piece):** Aggravated Assault gives an extra combat for {3}{R}{R} (sorcery speed). Combined with **Sword of Feast and Famine** equipped to Satya, each combat untaps all lands → infinite combats.

**Layer 3 — ETB Doublers / Token Multipliers (5 pieces):** Panharmonicon (doubles ETBs), Elesh Norn Mother of Machines (doubles your ETBs, shuts off opponents'), Strionic Resonator (copies triggers — including Satya's attack trigger for a second token), Phelia Exuberant Shepherd (flickers a permanent on each attack, re-triggering its ETB), **Anointed Procession** (doubles every token Satya creates, every Adeline trigger, every Siege-Gang trigger, every Brudiclad Myr).

**Layer 4 — Token Conversion (1 piece):** Brudiclad converts your token pile into copies of one token. Satya tokens, Adeline humans, Siege-Gang goblins, Angel of Invention servos, and the Brudiclad Myr can all become Inferno Titan copies for a lethal swing. Brudiclad-converted tokens shed Satya's EoT-sacrifice trigger.

**The play pattern:** Turns 1–3: ramp. Turn 4: Satya (or hold for a protected turn). Turn 5+: attack — make a token, gain 2 energy, trigger an ETB. Each attack is pure value. Goal turns 6–8: equip Sword of F&F + activate AA, or Brudiclad-convert into a lethal alpha strike.

-----

## Kill Lines

**Line 1 — Sword of F&F + Aggravated Assault (infinite combats, 3 cards including commander)**
Equip Sword of Feast and Famine to Satya (menace + haste makes her hard to chump). Activate AA in main phase. Combat: Satya attacks, deals combat damage to a player → untap all lands. Post-combat main: AA again. Repeat indefinitely. Each loop also generates: a Satya token + 2 energy. With Anointed Procession, two tokens. With Brudiclad in play, all tokens become haste copies of whatever you chose.

Earliest realistic assembly: turn 6 (Satya turn 4, Sword + equip turn 5, AA turn 6).

**Line 2 — Brudiclad Token Conversion (alpha strike, no infinite required)**
Sequencing: Turn N combat — Brudiclad's beginning-of-combat trigger fires *before* Satya attacks. The conversion that matters is **the following combat phase**. By that point, the Satya copy of Inferno Titan / Adeline / etc. is on the field. Brudiclad converts all your tokens (Myr, goblins from Siege-Gang, servos from Angel of Invention, humans from Adeline, the Satya token) into copies of the chosen token. Brudiclad-converted tokens **shed Satya's EoT-sacrifice clause** (the delayed trigger sticks to the original Satya token only), so the conversion also preserves them.

**Line 3 — Adeline + Anointed Procession Token Flood**
With Adeline + Anointed Procession on board: each attack generates ~6 1/1 humans (3 per opponent in pod, doubled). Plus Satya's token (also doubled = 2). Plus Adeline herself (* power = creature count, often 8+ on a flooded board). Brudiclad on top converts the swarm. This is a 3–4 card alpha that doesn't need infinite combats.

**Line 4 — Zealous Conscripts Steal**
Satya copies Zealous Conscripts → steal an opponent's best permanent. Strionic Resonator copies Satya's attack trigger → second steal. Aggravated Assault → one steal per combat.

**Line 5 — Value Grind**
Repeated ETB abuse turn after turn. Inferno Titan copies deal 3 damage each combat. Cloudblazer copies draw 2 each combat. Skyclave Apparition copies exile a permanent each combat. Most pods can't survive 3–4 turns of this without running out of resources.

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

-----

## Bracket 3 Compliance

**Game Changers (3 of 3):**
1. Fierce Guardianship — free counterspell with commander in play
2. Cyclonic Rift — asymmetric board wipe
3. The One Ring — protection turn + scaling card draw (added 2026-05-04 to fill the slot opened by Deflecting Swat's GC delisting)

*Note:* Deflecting Swat remains in the deck as a free redirect but no longer counts toward the GC cap.

**Infinite combos:** Sword of Feast and Famine (equipped to a connecting attacker — typically Satya, who has menace + haste) + Aggravated Assault = infinite combat phases. Each combat: Satya deals damage, untaps all lands, post-combat main re-activates AA. Earliest realistic assembly turn ~6.

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
1 The One Ring

### ETB Creatures — Value (5)

1 Cloudblazer
1 Wall of Omens
1 Knight of the White Orchid
1 Snapcaster Mage
1 Archivist of Oghma

### ETB Creatures — Board Impact (6)

1 Inferno Titan
1 Reflector Mage
1 Skyclave Apparition
1 Loran of the Third Path
1 Zealous Conscripts
1 Solitude

### ETB Creatures — Tokens/Pump (4)

1 Angel of Invention
1 Blade Splicer
1 Siege-Gang Commander
1 Adeline, Resplendent Cathar

### ETB Creatures — Utility (1)

1 Restoration Angel

### Combat Engine (1)

1 Aggravated Assault

### ETB Doublers / Token Multipliers (5)

1 Panharmonicon
1 Elesh Norn, Mother of Machines
1 Strionic Resonator
1 Phelia, Exuberant Shepherd
1 Anointed Procession

### Token Conversion (1)

1 Brudiclad, Telchor Engineer

### Combat Value Creatures (2)

1 Goldspan Dragon
1 Professional Face-Breaker

### Tutors (1)

1 Ranger-Captain of Eos

### Stax / Draw (3)

1 Esper Sentinel
1 Mystic Remora
1 Bident of Thassa

### Counterspells (3)

1 Counterspell
1 Swan Song
1 An Offer You Can't Refuse

### Removal (5)

1 Swords to Plowshares
1 Path to Exile
1 Generous Gift
1 Chaos Warp
1 Pongify

### Flexible Removal (2)

1 Abrade
1 Prismari Command

### Flexible Interaction (3)

1 Narset's Reversal
1 Expansion/Explosion
1 Deflecting Swat

### Protection (4)

1 Akroma's Will
1 Clever Concealment
1 Slip Out the Back
1 Lightning Greaves

### Equipment (2)

1 Swiftfoot Boots
1 Sword of Feast and Famine

### Card Selection (2)

1 Ponder
1 Preordain

### Ramp (10)

1 Sol Ring
1 Arcane Signet
1 Fellwar Stone
1 Mind Stone
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

-----

## Swap Log

### 2026-05-04 — Audit-driven upgrade pass (6 cards)

The audit found the advertised primary kill line (Combat Celebrant + Satya 2-card infinite) was broken — tokens that enter "tapped and attacking" cannot be exerted. Six in-collection swaps were applied to (a) install a real infinite, (b) multiply the token engine, and (c) shore up draw and survivability.

| Out | In | Rationale |
|---|---|---|
| Combat Celebrant | Adeline, Resplendent Cathar | Broken infinite → "whenever you attack" 1/1 token generator (≈3/attack in pod). Stacks with Anointed Procession and Brudiclad for an alpha lethal. |
| Lightning Runner | Sword of Feast and Famine | Slow 8-energy extra-combat → equip to Satya (menace + haste), combat damage untaps all lands, AA loops infinitely. |
| Charming Prince | Anointed Procession | Redundant flicker (Phelia + Restoration Angel cover) → doubles every Satya token *and* every Adeline trigger. |
| Arcane Denial | Solitude | Card-disadvantage counter → premium ETB target, free evoke from a white card. |
| Reprieve | Bident of Thassa | Worst counter (gives opp a card) → 1 card/creature/turn from combat damage. Force-attack mode is a niche bonus. |
| Coalition Relic | The One Ring *(GC)* | Slow 3-mana rock → fills the GC slot opened by Deflecting Swat's Oct 2025 delisting. ETB protection turn covers the deck's wrath-recovery weakness; scaling card draw addresses thin draw suite. |

### Knock-on rules notes flagged during audit (do not misplay)

- **Tokens entering "tapped and attacking" do NOT trigger "whenever ~ attacks" abilities.** Satya copies of Goldspan, Lightning Runner, Bident-bearers, etc. do not fire those creatures' attack triggers. ETB triggers DO fire.
- **Skullclamp-style tricks require post-combat equip** (sorcery-speed equip). Not relevant to current deck after swaps but flagged for any future Skullclamp consideration.
- **Brudiclad-converted tokens shed Satya's EoT-sacrifice clause** (it's a delayed trigger tied to the original Satya token). This is the cleanest way to keep tokens alive without paying energy.
- **Sword of F&F + AA loop relies on Satya (the equipped creature) connecting**, not the tokens. Menace + haste + 5 toughness makes this reliable but not guaranteed against decks with 2+ blockers.

Pending: Conversion Check rescore. Working theory: Kill Reliability rebounds to 4/5 (real infinite restored), Core Loop holds at 5/5, Durability climbs to 4/5 (One Ring), Interaction holds at 4/5 — projected **17/20** unchanged but with a more stable composition.
