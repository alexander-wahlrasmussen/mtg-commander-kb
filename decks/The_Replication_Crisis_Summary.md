# The Replication Crisis — Satya, Aetherflux Genius

## Quick Reference

| Field | Value |
|---|---|
| **Commander** | Satya, Aetherflux Genius ({1}{U}{R}{W}, 3/5 Legendary Creature — Human Artificer) |
| **Colors** | Jeskai (URW) |
| **Archetype** | ETB / Token Combo |
| **Bracket** | 3 (3 Game Changers) |
| **Game Changers** | Fierce Guardianship, Cyclonic Rift, The One Ring (Deflecting Swat remains in deck as a free redirect but no longer counts toward the GC cap as of Oct 2025) |
| **Conversion Check** | **18/20** (5/4/4/5) — Interaction 4→5 on the 2026-06-22 add of a 2nd, one-sided sweeper (Winds of Abandon) + a premium modal counter (Sublime Epiphany), which retire the two reasons the axis was capped. Was 17/20 (5/4/4/4) rescored 2026-05-13. |
| **Kill Window** | Clock: **T7 decap / T10–12 table** (board) · strict goldfish, `rc_speed_lab.py` 40k 2026-06-22 (decap T6 ≈ 16–18%). The 2026-06-22 Satya + Lightning Runner add (commander + 1 card; available ~12% by T6, ~18% by T12; converts to a table kill ~5% T6, ~18% T12, vs the old Sword+AA's 1–3%) buys a reliable infinite, **not** speed — **still not a T6–7 racer**, the decap clock is unchanged; bring it as a reliable closer / value engine, not to out-race the combo pod. See `analysis/Replication_Crisis_Speed_Curve_Analysis.md` |
| **Last swap pass** | 2026-06-22 — **(a)** −Goldspan Dragon / −Ponder / −Preordain (each physically deployed in another deck, so the slots were already empty) → +Lightning Runner (the Satya+LR infinite), +Sleight of Hand, +Opt (cantrips to find it); **(b)** −Expansion // Explosion (needed in Lightning War) → +Sublime Epiphany; −Bident of Thassa → +Winds of Abandon (2nd sweeper). All owned, no purchase. See `The_Replication_Crisis_Swaps_2026-06-22.md` + swap log below. |

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

**Layer 2 — Combat Engine / Infinite (2 pieces):** **Lightning Runner** is the primary kill — with Satya it makes infinite combats off the deck's own energy (commander + 1 card; see Line 1). **Aggravated Assault** gives an extra combat for {3}{R}{R} (sorcery speed); combined with **Sword of Feast and Famine** equipped to Satya, each combat untaps all lands → infinite combats (the backup infinite, Line 2).

**Layer 3 — ETB Doublers / Token Multipliers (4 pieces):** Panharmonicon (doubles ETBs of every Satya copy), Elesh Norn Mother of Machines (doubles your ETBs, shuts off opponents'), Strionic Resonator (copies Satya's attack trigger for a second token — the copied trigger creates a new token without re-using the "declared as attacking" check), **Anointed Procession** (doubles every token Satya creates, every Adeline trigger, every Siege-Gang trigger, every Brudiclad Myr).

**Layer 3a — Flicker engines (2 pieces):** Restoration Angel (ETB flicker — Satya copies of Resto re-trigger her flicker on entry), Phelia Exuberant Shepherd (attack-trigger flicker — only fires when Phelia herself attacks, NOT when Satya creates a Phelia token; growing +1/+1 counters when flickering your own permanents).

**Layer 4 — Token Conversion (1 piece):** Brudiclad converts your token pile into copies of one token. Satya tokens, Adeline humans, Siege-Gang goblins, Angel of Invention servos, and the Brudiclad Myr can all become Inferno Titan copies for a lethal swing. Brudiclad-converted tokens shed Satya's EoT-sacrifice trigger.

**The play pattern:** Turns 1–3: ramp. Turn 4: Satya (or hold for a protected turn). Turn 5+: attack — make a token, gain 2 energy, trigger an ETB. Each attack is pure value. Goal turns 6–8: equip Sword of F&F + activate AA, or Brudiclad-convert into a lethal alpha strike.

-----

## Kill Lines

**Line 1 — Satya + Lightning Runner (infinite combats, 2 cards = commander + 1) — PRIMARY (added 2026-06-22)**
Both real Satya and real Lightning Runner attack. Each gives {E}{E}. Satya makes a token copy of Lightning Runner (enters tapped + attacking — its "whenever ~ attacks" does *not* fire that combat, same ruling as Adeline/Phelia). Lightning Runner's trigger: pay 8{E} → untap all creatures + an additional combat phase. In the next combat the token Runner is untapped and **declared** as an attacker, so it triggers too. Per-combat energy = 2 × (Satya + every Lightning Runner attacking). Once you have Satya + 3 Runners (combat 3, or combat 2 with Anointed Procession doubling the tokens) you generate ≥8/combat = self-sustaining → **infinite combats / energy / tokens / double-strike damage.** Bootstrap needs ~6 banked energy (4 with Procession) — trivial in a deck that banks 2{E} every Satya attack. Tokens persist through the loop (end step never arrives). Lethal regardless of blockers if Inferno Titan is a copy target (infinite ETB pings) or just by infinite attackers.

Why it's the best line: **one piece is the commander** (always available) and the other is a single owned creature, so it's the deck's most-*assemblable* infinite by ~6–10× (available ~12% T6 / ~18% T12 drawn vs Sword+AA's ~1–3%; `rc_speed_lab.py` 2026-06-22). CSB combo [4918-5658]. Card text verified 2026-06-22.

**Line 2 — Sword of F&F + Aggravated Assault (infinite combats, 3 cards including commander) — backup infinite**
Equip Sword of Feast and Famine to Satya (menace + haste makes her hard to chump). Activate AA in main phase. Combat: Satya attacks, deals combat damage to a player → untap all lands. Post-combat main: AA again. Repeat indefinitely. Each loop also generates: a Satya token + 2 energy. With Anointed Procession, two tokens. With Brudiclad in play, all tokens become haste copies of whatever you chose.

Earliest realistic assembly: turn 6 (Satya turn 4, Sword + equip turn 5, AA turn 6). Lower availability than Line 1 (needs two specific cards drawn, no tutors), so it's the redundancy, not the plan.

**Line 3 — Brudiclad Token Conversion (alpha strike, no infinite required)**
Sequencing: Turn N combat — Brudiclad's beginning-of-combat trigger fires *before* Satya attacks. The conversion that matters is **the following combat phase**. By that point, the Satya copy of Inferno Titan / Adeline / etc. is on the field. Brudiclad converts all your tokens (Myr, goblins from Siege-Gang, servos from Angel of Invention, humans from Adeline, the Satya token) into copies of the chosen token. Brudiclad-converted tokens **shed Satya's EoT-sacrifice clause** (the delayed trigger sticks to the original Satya token only), so the conversion also preserves them.

**Line 4 — Adeline + Anointed Procession Token Flood**
With Adeline + Anointed Procession on board: each attack generates ~6 1/1 humans (3 per opponent in pod, doubled). Plus Satya's token (also doubled = 2). Plus Adeline herself (* power = creature count, often 8+ on a flooded board). Brudiclad on top converts the swarm. This is a 3–4 card alpha that doesn't need infinite combats.

**Line 5 — Zealous Conscripts Steal**
Satya copies Zealous Conscripts → steal an opponent's best permanent. Strionic Resonator copies Satya's attack trigger → second steal. Aggravated Assault → one steal per combat.

**Line 6 — Value Grind**
Repeated ETB abuse turn after turn. Inferno Titan copies deal 3 damage each combat. Cloudblazer copies draw 2 each combat. Skyclave Apparition copies exile a permanent each combat. Most pods can't survive 3–4 turns of this without running out of resources.

-----

## Conversion Check — 17/20

### Core Loop: 5/5

23+ cards directly serve the ETB-copy engine. 15 ETB creatures, 3 extra combat pieces, 4 doublers/multipliers, and Brudiclad. The loop is "attack → copy → ETB → snowball" and it's immediately identifiable from the decklist. Satya is the engine's centerpiece, but the deck still functions without her — Panharmonicon, Elesh Norn, Phelia, and Restoration Angel all generate ETB value independently. The energy system is self-sustaining: each Satya activation costs {E}{E}, each creature entering generates {E}, and the token itself generates {E} on entry, so each activation costs a net of {E} at worst.

**Checkpoint:** Cover the commander. The 99 has 15 ETB creatures, Panharmonicon, Elesh Norn, flicker effects, and extra combat pieces. The strategy is unmistakable.

### Kill Reliability: 4/5 (a much stronger 4 after the 2026-06-22 Lightning Runner add)

Six distinct closing lines, now including **two** infinite combat loops. The primary — **Satya + Lightning Runner** (commander + 1 card) — is the deck's most-*assemblable* kill by ~6–10×: because one half is the commander, its availability is just P(draw Lightning Runner) (~12% T6 / ~18% T12 drawn, `rc_speed_lab.py` 2026-06-22), versus the Sword + Aggravated Assault pair's ~1–3% (two specific cards, no tutors). Adeline + Anointed Procession is a fast non-infinite alpha; Brudiclad converts the token pile into a lethal swing. Estimated 2–3 turns from engine-online to kill.

Still doesn't reach 5 because **every line — including both infinites — requires Satya to be attacking**: she must survive as a 3/5 through a combat step, and instant-speed removal in response to the combat trigger shuts the turn down. (The owned-cards-only constraint means the one combat-*independent* fix — Kiki + Conscripts/Resto — isn't available; Kiki is unowned. See `The_Replication_Crisis_Swaps_2026-06-01.md`.) The deck has protection (Lightning Greaves, Swiftfoot Boots, Slip Out the Back, Clever Concealment) and Sword of F&F grants protection from black and green, but can't guarantee Satya survives every time and menace is stopped by any 2 blockers. A 5 would need kills that function independently of the combat step. **Kill Reliability stays 4** — the LR add is a large within-axis reliability gain, not a new axis. (The deck's *total* rose to 18/20 the same day via a separate Interaction 4→5 bump — see that axis below.)

**Checkpoint:** Satya + Lightning Runner = infinite combats off the deck's own energy (2 cards, commander + 1) — the line you reach for. Sword of F&F + Aggravated Assault + Satya = infinite combats (3 cards) as the backup. Adeline + Anointed Procession + Satya = ~6 humans per attack in a 4-player pod plus a Satya copy, lethal alpha with Brudiclad conversion.

### Durability: 4/5

The deck has meaningful redundancy across its ETB creature suite — losing any individual creature barely matters since Satya copies whichever is best in the current situation. Elesh Norn and Panharmonicon provide independent value even without Satya. Phelia and Restoration Angel keep the flicker engine running through commander removal.

After a board wipe: replay Satya (4 mana), need at least one ETB creature in hand, then attack next turn. Recovery is 2 turns to be threatening again. The energy system resets on wipe (energy counters persist on the player, not the board), so Satya can immediately copy something if you had banked energy.

Doesn't reach 5 because the deck is meaningfully commander-dependent for its primary game plan. Without Satya, the ETB creatures are solid but not explosive — you're playing fair Magic until she returns. Repeated commander removal (5, 6, 7+ mana) is genuinely painful in a deck that wants to curve out.

**Checkpoint:** Cyclonic Rift on turn 7. Replay Satya for 4 mana, deploy a creature. Next turn, attack and copy. Threatening again in 2 turns.

### Interaction: 5/5 (4→5 on the 2026-06-22 add)

Deep, flexible, and now with two mass answers:

- **Counter-capable (7):** Fierce Guardianship (free), Deflecting Swat (free redirect), Counterspell, Swan Song, An Offer You Can't Refuse, Narset's Reversal (counter/copy), **Sublime Epiphany** (modal: counter spell *or* ability, bounce, copy a creature, draw)
- **Removal (8):** Cyclonic Rift (asymmetric wipe), **Winds of Abandon** (overload = one-sided creature wipe), Swords to Plowshares, Path to Exile, Generous Gift, Chaos Warp, Pongify, Abrade
- **Flexible / ETB-based:** Prismari Command (removal/ramp/draw); plus Reflector Mage, Skyclave Apparition, Solitude, Loran — repeatable removal Satya can copy
- **Board protection (3):** Akroma's Will, Clever Concealment, Slip Out the Back
- **Equipment (2):** Lightning Greaves, Swiftfoot Boots

Two free spells (Fierce Guardianship, Deflecting Swat) protect the combo turn while tapped out.

**Reaches 5 (2026-06-22):** the two reasons this axis was held at 4 are both retired — the deck now has a **second mass answer** (Winds of Abandon's one-sided overload, alongside Cyclonic Rift) and a **premium flexible counter** (Sublime Epiphany) replacing the do-one-thing Expansion // Explosion. *Caveat:* Winds is a soft sweeper — 6-mana overload that hands opponents a basic land each — so this is a clean-but-not-overwhelming 5.

### Total: 18/20 — Structurally excellent. Pilot skill is the main variable.

-----

## Phelia Integration (MH3 Upgrade)

Phelia, Exuberant Shepherd replaced Inspiring Overseer. She's a flicker engine on a 2-drop:

**What Phelia does in context:**
- *Her own attack* exiles up to one target nonland permanent until end-of-turn (returns at the next end step). When the permanent returns under your control, Phelia gains a +1/+1 counter — so flickering your own ETB creatures grows her into a real clock.
- Can flicker your own ETB creatures (Cloudblazer = draw 2, Reflector Mage = bounce, Skyclave Apparition = exile, Solitude = exile a creature)
- Can temporarily exile an opponent's threat through the attack (it returns at end of turn, but it's gone during your combat)
- At 2 mana with flash, she can deploy at the end of the turn before Satya hits to bait removal or hold up interaction

**Rules note — Satya copies of Phelia DO NOT flicker.** Phelia's trigger is "Whenever Phelia attacks." A Satya copy enters tapped and attacking but is *never declared as an attacker*, so the trigger doesn't fire (same ruling as Adeline). A Satya copy of Phelia is a 2/2 body with flash — useful as a chump or hold-up bluff, but not a second flicker. The flicker engine is one trigger per turn, from Phelia herself.

**What Inspiring Overseer did:** Drew 1 card and gained 1 life on ETB. Functional but the weakest ETB in the creature suite. Phelia's attack-trigger flicker is engine-quality; Overseer was filler.

-----

## Bracket 3 Compliance

**Game Changers (3 of 3):**
1. Fierce Guardianship — free counterspell with commander in play
2. Cyclonic Rift — asymmetric board wipe
3. The One Ring — protection turn + scaling card draw (added 2026-05-04 to fill the slot opened by Deflecting Swat's GC delisting)

*Note:* Deflecting Swat remains in the deck as a free redirect but no longer counts toward the GC cap.

**Infinite combos (both produce infinite combat *phases*, not extra turns — pod-OK as of 2026-06-19, see [[infinites_ok_in_pod]]):**
1. **Satya + Lightning Runner** (commander + 1 card) = infinite combats / energy / tokens / double-strike damage. Bootstrap ~6 banked energy. The primary kill — see Line 1.
2. **Sword of Feast and Famine + Aggravated Assault** (equipped to a connecting Satya) = infinite combat phases (untap all lands → re-cast AA). Backup — see Line 2. Earliest realistic assembly turn ~6.

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

### Combat Engine / Infinite Combo Pieces (2)

1 Lightning Runner
1 Aggravated Assault

### ETB Doublers / Token Multipliers (5)

1 Panharmonicon
1 Elesh Norn, Mother of Machines
1 Strionic Resonator
1 Phelia, Exuberant Shepherd
1 Anointed Procession

### Token Conversion (1)

1 Brudiclad, Telchor Engineer

### Combat Value Creatures (1)

1 Professional Face-Breaker

### Tutors (1)

1 Ranger-Captain of Eos

### Stax / Draw (2)

1 Esper Sentinel
1 Mystic Remora

### Counterspells (3)

1 Counterspell
1 Swan Song
1 An Offer You Can't Refuse

### Removal (6)

1 Swords to Plowshares
1 Path to Exile
1 Generous Gift
1 Chaos Warp
1 Pongify
1 Winds of Abandon

*(Winds of Abandon overloads into a one-sided creature wipe — the deck's second mass answer alongside Cyclonic Rift.)*

### Flexible Removal (2)

1 Abrade
1 Prismari Command

### Flexible Interaction (3)

1 Narset's Reversal
1 Sublime Epiphany
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

1 Sleight of Hand
1 Opt

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

### 2026-05-13 — Conversion Check rescore (post-swap)

Rescore confirms the working theory: **17/20 (5/4/4/4) — holds with a more stable composition than the pre-swap 17.** Full card-text re-verification done against local Scryfall data for Satya, Aggravated Assault, Sword of Feast and Famine, The One Ring, Adeline, Anointed Procession, Brudiclad, Solitude, Bident of Thassa, Phelia, Strionic Resonator, Restoration Angel, Ranger-Captain of Eos, Goldspan Dragon, Esper Sentinel, Deflecting Swat. 100-card count verified (99 main + 1 commander). GC count 3/3 (Fierce Guardianship, Cyclonic Rift, The One Ring) — verified against `REF_Game_Changers_List.md`. Deflecting Swat remains in the deck as a free redirect and no longer counts toward the cap (delisted Oct 2025).

**Axis-by-axis:**
- **Core Loop 5/5** — ~22 engine pieces (16 ETB creatures + 4 doublers/multipliers + 2 flicker engines + Brudiclad + AA + Sword). Loop is unmistakable from the decklist.
- **Kill Reliability 4/5** — Sword + AA real infinite restored; Adeline + Anointed Procession adds a parallel non-infinite alpha; Brudiclad alpha line still in. Five lines total, three of which are fast. Held under 5 because every line still requires Satya to connect for combat damage.
- **Durability 4/5** — The One Ring adds a protection turn and scaling draw (replacing slow Coalition Relic). 16 ETB creatures provide deep redundancy; Cyclonic Rift is the asymmetric reset; Restoration Angel and flash interaction keep the deck alive through wraths. Held under 5 because Satya remains a critical dependency.
- **Interaction 4/5** — 14+ pieces (6 counters + 7 removal + 4 board protection + ETB-based interaction via Reflector Mage / Skyclave Apparition / Loran / Solitude). Two free spells (FG + Swat). Held under 5 because the deck runs only one true board wipe (Cyclonic Rift) and the counter suite includes weaker options (Swan Song, An Offer).

**Errors corrected during the rescore (documentation only, no card swaps):**
1. **Phelia rules error** — prior summary claimed Satya copies of Phelia flicker. They do not: Phelia's "Whenever Phelia attacks" trigger does not fire on tokens that enter tapped-and-attacking (same Adeline ruling already documented in the 2026-05-04 swap log).
2. **Layer 3 miscount** — Phelia was listed as a "Token Multiplier" but isn't one. Layer 3 corrected to 4 pieces; Phelia moved to a new Layer 3a (Flicker engines) alongside Restoration Angel.
3. **Kill Reliability checkpoint** — previously cited Combat Celebrant + Satya 2-card infinite (Celebrant is now sideboard) and Goldspan Dragon as the AA partner (Sword of F&F is now the AA partner). Both fixed.
4. **Satya stat** — text said "3/4," she's 3/5. Fixed.

No card swaps applied during this audit.

### 2026-06-09 — Kill-window correction (speed-curve analysis, no card swaps)

The `scripts/rc_speed_lab.py` goldfish combat lab (40k trials; writeup in
`analysis/Replication_Crisis_Speed_Curve_Analysis.md`) falsified the Quick
Reference's "Goldfish: T5–7" window. Measured, with every attacker unblocked
and zero opposing interaction: **one focused opponent dead median T7** (T6 =
16%, T5 = 2%), **table dead median T10–11**; a defended-board proxy (only
Satya + her tokens attack) gives median T8 / T10 = 16%. Key structural facts
confirmed against printed text: the Sword+AA infinite is ~1–3% of games (zero
tutors find it), Adeline's tokens are spread 1-per-opponent (2 with
Procession) rather than focused, Brudiclad's conversion pays off one combat
*after* the token it copies exists, and early Satya tokens die at end step
(energy 2/attack vs. keep cost = MV). Kill Window field corrected; Conversion
Check score unchanged (Kill Reliability 4/5 already discounted the combat
dependence). The deck remains what Pod Fit says it is — an incremental value
engine, **not** a racer; see the analysis doc before bringing it against the
T6–7 combo pod.

### 2026-06-22 — Lightning Runner infinite + interaction tune (5-card swap, all owned)

New `.txt`: `the-replication-crisis-20260622.txt` (old `…-20260504-202914.txt`
moved to `archive/old_decklists/`). Full writeup +
benchmark: `The_Replication_Crisis_Swaps_2026-06-22.md`.

| Out | In | Why |
|---|---|---|
| Goldspan Dragon | **Lightning Runner** | Goldspan is physically in Lightning War (1 owned, contended), so the RC slot was already empty. Lightning Runner completes the **Satya + Lightning Runner** infinite (commander + 1 card) — CSB [4918-5658], text-verified. Itself a 2/2 (a future power-2 tutor target) and a copy target. |
| Ponder | **Sleight of Hand** | Ponder is a 1-of shared across 4 decks (physically elsewhere). Sleight of Hand (dig-2) is owned + unallocated; keeps card-selection count at 2 to find the new combo. |
| Preordain | **Opt** | Same contention story. Opt (2 owned, 1 free) replaces the selection 1-for-1. |
| Expansion // Explosion | **Sublime Epiphany** | E // E was needed in Lightning War (contended). Sublime Epiphany ({2}{U}{U} instant) is a strictly more flexible modal answer — counter spell/ability, bounce, copy a creature you control (ETB synergy), or draw. 2 owned + unallocated. |
| Bident of Thassa | **Winds of Abandon** | Bident (the prior Kiki proposal's earmarked weakest card — redundant with the deep draw suite) makes room for the deck's **second mass answer**: Winds overloads into a one-sided creature wipe (exile each creature you don't control), which a go-wide creature deck wants far more than a symmetric wrath. |

**Why this is the upgrade (`rc_speed_lab.py`, 40k, 2026-06-22):** the old deck's
only true infinite (Sword + AA) is two specific cards with no tutors → complete
~1% T6 / ~3% T12. Satya + Lightning Runner is **commander + 1 card**, so it's
available ~12% T6 / ~18% T12 (just P(draw Lightning Runner)), fuelled by the
deck's native energy. Table-kill-via-an-infinite rises **1→5% T6, 3→18% T12**;
defended-board (SQUAD) table kill **47→56% T12** with far more T6–8 mass. The
**decap clock is unchanged** — this is a reliability/closing upgrade, *not* a
speed one; the deck still isn't a T6–7 racer (the 2026-06-09 verdict holds).

**Compliance:** 99 + 1 = 100 (verified). GC 3/3 unchanged (Fierce Guardianship,
Cyclonic Rift, The One Ring — none of the five swap cards are GCs, checked against
`REF_Game_Changers_List.md`). Both infinites produce infinite combat *phases*,
not extra turns — pod-OK as of 2026-06-19 ([[infinites_ok_in_pod]]). Card text
verified via `card_lookup.py`: Satya, Lightning Runner, Sleight of Hand, Opt,
Sublime Epiphany, Winds of Abandon.

**Conversion Check 17 → 18/20.** Kill Reliability stays 4 (the LR infinite still
needs Satya to connect — doesn't clear the "combat-step-independent" bar a 5
requires). **Interaction 4 → 5:** the two reasons it was capped are retired — a
second mass answer (Winds of Abandon, one-sided) and a premium flexible counter
(Sublime Epiphany). Caveat: Winds is a soft 6-mana sweeper that ramps opponents,
so it's a clean-but-not-overwhelming 5.

**Knock-on:** Bident is now benched, so the pending −Bident +Kiki swap
(`…_Swaps_2026-06-01.md`) would need a different donor; Kiki would stack as a
3rd, Satya-free infinite. Removing Expansion // Explosion also drops the
Narset's Reversal + E // E "infinite magecraft" near-combo (no magecraft payoff
here, so no loss).

### 2026-06-30 — Kiki-Jiki add evaluated and DECLINED (no card change)

Re-ran `rc_speed_lab.py` (40k) on current vs **+Kiki-Jiki / −Aggravated Assault**
(the −Bident donor from `…_Swaps_2026-06-01.md` was already spent on Winds of
Abandon). Result: **Kiki + Conscripts/Resto assembles ~6% by T12 (mana-online
~4%)** — ~3× *rarer* than the Satya + Lightning Runner infinite already in the
deck (18% T12), because LR is a commander+1 line and Kiki is a no-tutor 2-card
combo. The swap is ~availability-neutral (the Sword+AA line it would replace is
itself only 1%/3%) and moves **neither** the decap nor table clock. Kiki's lone
distinguishing merit — Satya-removal insurance — is unscoreable by a goldfish
lab. **Not bought, no `.txt` change.** The 2026-06-01 swap doc is annotated
DECLINED in place; its 17→18–19/20 projection is retracted (it predates the LR
infinite). The Kill Reliability 4/5 cap therefore stands — the lever that
targets the deck's *primary* line rather than a rare 3rd infinite is a tutor for
Lightning Runner, and that one labbed well (next note).

### 2026-06-30 — Imperial Recruiter APPROVED (tutor the primary line; 2nd copy on order)

Instead of a third infinite, add a second *find* for the existing one. **−Strionic
Resonator (in no kill package) +Imperial Recruiter** ({2}{R}, ETB tutors a creature
power ≤ 2 → hand; fetches the 2/2 Lightning Runner). `rc_speed_lab.py --mode avail`
(40k, 2026-06-30): the Satya + LR line goes **11→22% (T6) / 18→32% (T12)** — drawing
LR *or* the tutor — and ANY-kill-line availability rises **24→33% (T6) / 36→48%
(T12)**, with Sword+AA kept live. Roughly **doubles** how often the primary infinite
is online vs the ~6%/T12 Kiki backup that was declined; on-axis and commander-
independent. **Reliability, not speed** — decap/table clocks don't move, deck still
can't out-race a T6–7 pod. **APPLIED 2026-06-30** (as-if-bought per user direction)
→ `the-replication-crisis-20260630.txt`; old list archived. The single owned
Recruiter is still in Exile's Return, so a **2nd physical copy is owed** before
both decks sleeve at once. Full writeup + caveats:
`The_Replication_Crisis_Swaps_2026-06-30.md`.

## Don't-Miss Rulings

- **Tokens entering "tapped and attacking" do NOT trigger "whenever ~ attacks" abilities** *the combat they're made* — but they **CAN attack normally in a later combat** (once untapped + declared), and *then* they trigger. Satya copies of Adeline, Phelia, Bident-bearers, etc. don't fire attack triggers on entry, but their **ETB triggers DO**. This is the whole engine of the Lightning Runner combo: the token Runner makes no energy the combat Satya creates it, but it untaps with the others and **does** make energy when it attacks in the next combat. (It's also why the old Combat Celebrant "infinite" was fake — exert is a one-time, can't-untap thing.)
- **The copy must target a *nontoken* creature** — Brudiclad-converted tokens are not legal Satya targets.
- **Energy is gained free; tokens are kept by paying their mana value in {E} at end step.** An Inferno Titan token costs 6{E} to keep — three attacks bank enough for one. Unkept tokens are sacrificed.
- **Brudiclad-converted tokens shed Satya's end-of-turn sacrifice clause** (it's a delayed trigger stuck to the original token) — the cleanest way to keep tokens without paying energy.
- **The Sword + AA loop relies on Satya herself connecting**, not the tokens. Menace + haste + 5 toughness makes it reliable, but **two blockers stop menace.**
- **Panharmonicon / Elesh Norn double the *ETBs* of every Satya copy**; Strionic Resonator copies Satya's attack trigger for a second token. Phelia and Restoration Angel are the flicker engines (Phelia only flickers when *she* attacks).

## Piloting Notes (for borrowers)

**Mulligan.** Looking for: **lands + ramp + a path to Satya on T4**, plus at least one ETB creature to start copying.
The primary infinite is Satya + Lightning Runner, so a hand holding Lightning Runner or Imperial
Recruiter (which fetches it) is a stronger keep than the Sword of Feast and Famine + Aggravated
Assault pair (~1–3% assembly, no tutors). Ranger-Captain of Eos fetches nothing in the combo
package — don't keep it as a "tutor."

- **Keep:** ramp + Satya + an ETB creature; or ramp + interaction with Satya findable.
- **Toss:** no-land hands; hands with Satya but zero ETB creatures to copy; all-payoff/no-mana.
- You **don't** need the combo in your opener — the deck grinds ETB value and assembles it.

**Threats & timing.**

- **Commander-dependent.** Every kill line needs Satya attacking as a 3/5 — instant-speed removal in response to the combat trigger blanks the turn. Repeated Satya removal is the best counterplay against you. A reliable closer, not a racer.
- **Protect the swing.** Lightning Greaves / Swiftfoot Boots, Slip Out the Back, Clever Concealment, Akroma's Will; Sword grants pro-black/green. Hold a free counter (Fierce Guardianship, Deflecting Swat) for the combo turn.
- **Weak to stax / pillowfort.** Ghostly Prison & Propaganda tax your attacks; Torpor Orb & Hushbringer shut off the ETBs entirely. Enchantment removal is thin (Loran, Generous Gift).
- **Two mass answers: Cyclonic Rift + Winds of Abandon** (overload = one-sided creature exile — doesn't touch your board). Plus Sublime Epiphany as a flexible modal counter/bounce/copy. 16 ETB creatures give deep redundancy, so you recover fast off any single creature.
