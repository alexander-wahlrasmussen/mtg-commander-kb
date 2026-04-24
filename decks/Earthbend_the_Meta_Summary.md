# Earthbend the Meta — Toph, the First Metalbender

## Quick Reference

| Field | Value |
|---|---|
| **Commander** | Toph, the First Metalbender ({1}{R}{G}{W}, 3/3 Legendary Creature — Human Warrior Ally) |
| **Colors** | Naya (RGW) |
| **Archetype** | Lands / Artifacts / Earthbend / +1/+1 Counters |
| **Bracket** | 3 (3 Game Changers used; no early infinite combos; no MLD; no extra turns) |
| **Game Changers** | Field of the Dead, Smothering Tithe, Crop Rotation (3 of 3 slots used) |
| **Conversion Check** | **17/20** (5/4/4/4) |
| **Kill Window** | Goldfish: T7–9 · Through interaction: T10–12 |

-----

## Commander Rules Text

Toph has two abilities:

1. **Artifact-land bridge:** Nontoken artifacts you control are lands in addition to their other types. (They don't gain the ability to tap for mana.)
2. **Earthbend 2:** At the beginning of your end step, target land you control becomes a 0/0 creature with haste that's still a land. Put two +1/+1 counters on it. When it dies or is exiled, return it to the battlefield tapped.

Key rulings: Artifacts becoming lands triggers landfall effects (Lotus Cobra, Felidar Retreat, etc.) when they enter the battlefield. Earthbend can target an already-animated land to add more counters. Earthbent lands that die return as lands (no longer creatures) — this protects against losing land drops to removal. Toph's artifact-land bridge does NOT give artifacts mana abilities; you need Dryad of the Ilysian Grove to make them tap for colored mana.

-----

## Rules Interactions Reference

Earthbend is a new mechanic with several non-obvious interactions that affect how this deck plays. This section covers the key rules you need to understand to pilot the deck correctly.

### Earthbend Fundamentals

"Earthbend N" means: target land you control becomes a 0/0 creature with haste that's still a land. Put N +1/+1 counters on it. When it dies or is exiled, return it to the battlefield tapped.

Key properties:

- **Return clause** fires on death OR exile, not on bounce. Cyclonic Rift bouncing an earthbent land sends it to your hand — no return trigger. Swords to Plowshares exiling it DOES trigger the return. This matters for threat assessment.
- **Return clause** is a delayed triggered ability. It can be countered by Stifle effects (rare, but be aware). The land returns as a non-creature land — no counters, no creature status, just a land entering tapped.
- **Stacking earthbend** on an already-animated land works. The land gets additional +1/+1 counters, its base power/toughness resets to 0/0 (then counters apply), it gains haste again (redundant), and a NEW return clause is created. Multiple return clauses are independent — each one tries to return the land, but only the first one that fires does anything (the land is only in one zone).
- **The animated land keeps all types and subtypes.** A Forest that gets earthbent is still a Forest creature land. It can still tap for {G}. This is important for mana sequencing during combat — earthbent lands can attack AND tap for mana if they have vigilance (from Earthbending Student or Teysa tokens).
- **Colorless.** Earthbend does not give the land a color. The resulting creature is typically colorless, which matters for protection spells and color-specific removal.

### Toph's Artifact-Land Bridge

Toph's static ability makes all nontoken artifacts you control lands IN ADDITION to their other types. This does NOT give them mana abilities. An artifact that becomes a land via Toph cannot tap for mana unless something else grants that ability (Dryad of the Ilysian Grove making all lands tap for any color, or the artifact already having a mana ability like Sol Ring).

The bridge creates the following triggers when an artifact enters:

- Artifacts entering the battlefield trigger ALL your landfall effects (Lotus Cobra, Felidar Retreat, Scute Swarm, Evolution Sage, etc.)
- Field of the Dead checks for 7+ differently named lands — each artifact-land has its own name, counting toward the threshold
- Artifacts that are also lands can be targeted by earthbend, gaining the return clause

**Critical: token artifacts are excluded.** Treasure tokens, Clue tokens, Food tokens, and other artifact tokens are NOT lands via Toph's static. However, if another effect makes them artifacts (they already are) AND something like Bootleggers' Stash creates them from land abilities, they enter as artifacts — but Toph only covers NONtoken artifacts. The Smothering Tithe / Bootleggers' Stash landfall chains work differently from how you might assume at first glance.

**Correction on Smothering Tithe + Toph:** Treasure tokens from Smothering Tithe are TOKEN artifacts. Toph's static only affects NONTOKEN artifacts. Treasures do NOT become lands via Toph. However, Smothering Tithe still provides massive mana generation that fuels the deck's expensive payoffs (Avatar Kyoshi at 8 mana, Awaken the Woods for large X, Bootleggers' Stash at 6 mana). It is a ramp/engine card, not a landfall combo with Toph.

**Bootleggers' Stash works differently.** Stash makes your lands gain "{T}: Create a Treasure token." The Treasures are tokens, so they don't become lands via Toph either. However, the Stash ITSELF is a nontoken artifact — it becomes a land via Toph, triggers landfall on entry, and can be earthbent for protection.

### Commander Protection via Liquimetal

The deck's answer to commander dependency:

1. Liquimetal Coating (or Liquimetal Torque) targets Toph → Toph becomes an artifact
2. Toph's own static makes her a land (nontoken artifact you control = land)
3. Earthbend targets Toph → she becomes a 0/0 creature with +N/+N counters, gains haste, gains the return clause
4. If Toph dies or is exiled → she returns to the battlefield tapped. Choose to let her go to the graveyard (not the command zone) and the return clause brings her back with no commander tax

This line is the primary answer to repeated commander removal, which the summary identifies as the deck's biggest structural weakness. Both Liquimetal Coating and Liquimetal Torque enable it — having two copies of this effect is intentional redundancy, not excess.

**Timing note:** You need to earthbend Toph BEFORE she would be targeted for removal. The ideal sequence is: play Toph → next turn, use Liquimetal to make her an artifact → earthbend her at end step → she now has the return clause for all future removal. The earthbend trigger targets, so you must do this during your end step (from Toph's own trigger) or whenever another earthbend source fires.

### Zuran Orb + Earthbent Lands

Zuran Orb: {0}, sacrifice a land — gain 2 life. No mana cost to activate, no tap requirement.

With any earthbent land, this becomes: sacrifice the land (free) → gain 2 life → earthbend return clause triggers → land returns to the battlefield tapped → returning land triggers ALL landfall effects (Lotus Cobra, Felidar Retreat, Scute Swarm, Evolution Sage, etc.). With Amulet of Vigor also in play, the returning land enters untapped, and you can sacrifice it again immediately for another cycle.

Even without Amulet, each earthbent land sacrificed to Zuran Orb is: 2 life + a full suite of landfall triggers + the land comes back. With 3 earthbent lands, that's 3 free landfall cycles in a single turn. This is an engine piece, not a life gain card.

### Crop Rotation Interactions

Crop Rotation: {G}, sacrifice a land — search for any land, put it onto the battlefield. The sacrifice is a COST (happens on announcement, can't be responded to before the land is gone).

In this deck:

- Sacrifice an earthbent land → it returns via the return clause → search for any land (Field of the Dead, Lotus Field, Kessig Wolf Run, Boseiju to destroy a permanent at instant speed, Yavimaya) → the searched land enters → TWO landfall triggers total (one from the returned land, one from the searched land)
- At instant speed, making it a surprise combat trick, a response to removal, or an end-of-turn engine activation
- Finding Boseiju, Who Endures then channeling it gives the deck instant-speed artifact/enchantment/land removal at the cost of a single card

### Counter Amplifier Stacking

When earthbend places +1/+1 counters, multiple replacement effects can modify the number. The controller (you) chooses the order. Optimal ordering:

1. Start: earthbend 2 (2 counters to be placed)
2. Hardened Scales: "If one or more +1/+1 counters would be placed, that many plus one are placed instead" → 3 counters
3. The Earth Crystal: "If one or more +1/+1 counters would be placed on a creature you control, twice that many are placed instead" → 6 counters
4. Doubling Season: "If an effect would place one or more counters, it places twice that many instead" → 12 counters

All Will Be One then triggers: "Whenever one or more counters are put on a permanent you control or a player, deal that much damage to any target" → 12 damage from a single earthbend 2.

**Important:** All Will Be One triggers once per EVENT, not once per counter. It sees the final number after all replacement effects have applied. Multiple earthbend triggers in the same turn each create separate events — each one triggers All Will Be One independently.

**Hardened Scales vs. Doubling Season ordering:** You always want additive effects (Hardened Scales, +1) BEFORE multiplicative effects (Doubling Season, ×2; Earth Crystal, ×2). Applying Hardened Scales last would only add 1 to an already-doubled number, wasting the multiplication.

### Ashaya, Soul of the Wild

Ashaya makes all nontoken creatures you control Forests in addition to their other types. This means every nontoken creature entering the battlefield triggers all landfall effects. Combined with Cathars' Crusade (each creature entering puts a +1/+1 counter on all your creatures), every creature that enters triggers landfall AND grows the whole team. With All Will Be One, each counter placement deals damage.

Ashaya does NOT affect token creatures. Scute Swarm tokens, Felidar Retreat cat tokens, Field of the Dead zombies, and Awaken the Woods dryads are all tokens and are NOT Forests via Ashaya.

### Scute Swarm Exponential Math

At 6+ lands, Scute Swarm's landfall creates a COPY of Scute Swarm (not just a 1/1 insect). Each copy has the landfall ability. On the next landfall trigger, ALL Scute Swarms trigger independently.

- Landfall 1: 1 Scute → creates 1 copy → 2 Scutes total
- Landfall 2: 2 Scutes trigger → 2 copies → 4 total
- Landfall 3: 4 Scutes trigger → 4 copies → 8 total
- Landfall 4: 8 → 16
- Landfall 5: 16 → 32

With Entish Restoration fetching 3 basics (3 landfall triggers starting from 1 Scute): you end with 8 Scute Swarms. Each entering Scute triggers Cathars' Crusade (counter on everything), Impact Tremors (1 damage each), Purphoros (2 damage each), and potentially All Will Be One.

### Purphoros, God of the Forge — Key Rulings

Purphoros deals 2 damage to each opponent whenever a CREATURE enters the battlefield under your control. Not artifacts, not lands — creatures specifically.

- Token creatures entering trigger Purphoros: Scute Swarm tokens, Felidar Retreat cats, Field of the Dead zombies, Awaken the Woods dryads (they are creature tokens)
- Nontoken creatures entering trigger Purphoros: any creature spell resolving, earthbent lands are creatures (but they were already on the battlefield — earthbend doesn't cause them to "enter")
- Earthbent lands returning after death DO trigger Purphoros — wait, no. The returning land enters as a LAND, not as a creature. The earthbend creature status is lost when it dies. The return clause just returns a land. Purphoros does NOT trigger on returned earthbent lands.
- Purphoros triggers off: Scute copies, Felidar cats, Field of the Dead zombies, Awaken the Woods dryads, Springheart Nantuko insects, and any creature spell you cast.

With devotion to red below 5 (likely in this Naya deck), Purphoros is an indestructible enchantment. He cannot be destroyed by creature removal, board wipes that destroy creatures, or combat damage. Only enchantment removal or exile effects hit him.

### Triumph of the Hordes — Infect Math

Triumph gives all your creatures +1/+1, trample, and infect until end of turn. Infect means combat damage is dealt as poison counters to players. 10 poison counters = lethal regardless of life total.

With three earthbent lands at 4 counters each (after amplifiers): each is a 5/5 with trample and infect after Triumph. Three of them = 15 infect damage, needing to be split across blockers and players. Trample means excess damage over blockers goes through. Against a single opponent with no blockers, one 5/5 infect creature is lethal in two hits — but you likely have lethal in one swing across multiple creatures.

### Legend Rule and Toph Variants

The four Toph variants in the deck all have DIFFERENT card names: Toph Earthbending Master, Toph Greatest Earthbender, Toph Hardheaded Teacher, Toph the Blind Bandit. The legend rule only applies to permanents with the SAME name. You can have all four on the battlefield simultaneously alongside the commander (Toph, the First Metalbender). Five different Tophs, five different earthbend triggers.

### Annie Joins Up — Doubled Triggers

Annie Joins Up: "Whenever a legendary creature enters the battlefield under your control, it deals damage equal to its power to target opponent or planeswalker. Triggered abilities of legendary creatures you control trigger an additional time."

This doubles Toph commander's earthbend trigger (earthbend 2 fires twice = two different lands animated per end step). It also doubles Tannuk's landfall damage trigger, Avatar Kyoshi's earthbend 8 trigger, and any other legendary creature's triggered ability. It does NOT double replacement effects (Hardened Scales, Doubling Season).

-----

## What the Deck Does

The deck operates on three synergistic layers that all feed each other through Toph's static ability and the earthbend mechanic.

### Layer 1 — Artifacts Become Lands (Toph's Static)

Every nontoken artifact on the battlefield is also a land. This means playing an artifact triggers all landfall effects. Sol Ring entering the battlefield triggers Lotus Cobra (mana), Felidar Retreat (token or counters), Evolution Sage (proliferate), Scute Swarm (token), Tireless Provisioner (treasure), Tannuk (damage + draw), and Field of the Dead (zombie). Dryad of the Ilysian Grove makes these artifact-lands tap for any color, turning mana rocks into dual-purpose cards.

Key artifacts that become lands: Sol Ring, Arcane Signet, Liquimetal Torque, Liquimetal Coating, Lightning Greaves, Swiftfoot Boots, The Earth Crystal, The Ozolith, Bootleggers' Stash, Darksteel Citadel (already a land), Amulet of Vigor.

### Layer 2 — Landfall Payoffs

Each land entering (including artifacts via Toph) fires the landfall suite:

- **Lotus Cobra** — mana of any color per landfall
- **Felidar Retreat** — create a 2/2 cat OR put +1/+1 counters + vigilance on all creatures
- **Scute Swarm** — 1/1 insect, or if 6+ lands, a full copy of Scute Swarm (exponential)
- **Evolution Sage** — proliferate (grows all counters on all permanents)
- **Moraug, Fury of Akoum** — extra combat phase + creatures get +1/+0 per attack
- **Tireless Provisioner** — Treasure or Food token
- **Tannuk, Memorial Ensign** — 1 damage to each opponent; 2nd trigger each turn draws a card
- **Bristly Bill, Spine Sower** — +1/+1 counter on a creature; activated ability doubles all counters
- **Springheart Nantuko** — 1/1 insect token, or pay {1}{G} to copy enchanted creature
- **Field of the Dead** (GC) — 2/2 zombie when 7+ differently named lands

Entish Restoration is a premium landfall enabler: {2}{G} instant, sacrifice a land, search for 2 basics (3 if power 4+). With earthbend's return clause, the sacrificed earthbent land returns tapped, AND 2–3 new lands enter triggering all landfall effects simultaneously. Awaken the Woods creates X Forest Dryad creature tokens that are also lands, triggering X landfall triggers on resolution.

### Layer 3 — +1/+1 Counter Amplifiers

Earthbend places counters. Landfall payoffs place counters. This layer multiplies them:

- **Hardened Scales** — each instance of counters gets +1
- **Doubling Season** — doubles all counters AND all tokens
- **The Earth Crystal** — doubles +1/+1 counters placed on creatures, reduces green spell costs by {1}
- **Cathars' Crusade** — every creature entering puts +1/+1 on ALL your creatures
- **The Ozolith** — stores counters from dying creatures, moves them to a new one
- **All Will Be One** — every counter placement event deals that much damage to any target

With the full amplifier suite, Toph's earthbend 2 at end step becomes: 2 counters → Hardened Scales (+1 = 3) → Earth Crystal (×2 = 6) → Doubling Season (×2 = 12). All Will Be One then deals 12 damage. Each turn. From a single end step trigger.

### Key Cross-Layer Interactions

**Bootleggers' Stash + Toph:** Lands tap to create Treasure tokens. The Stash itself is a nontoken artifact — it becomes a land via Toph, triggers landfall on entry, and can be earthbent for protection. The Treasures it creates are token artifacts (Toph's static doesn't apply to them), but they provide massive mana acceleration for the deck's expensive payoffs.

**Smothering Tithe (GC) as mana engine:** Opponents drawing cards generates Treasure tokens passively. The Tithe itself is not an artifact, but the mana it generates fuels Awaken the Woods (large X), Avatar Kyoshi (8 mana), Bristly Bill's activated ability (double all counters), and early deployment of the amplifier suite. In a 4-player game, 3+ Treasures per turn cycle without spending a card.

**Ashaya + landfall:** All nontoken creatures are also Forests. Every nontoken creature entering triggers landfall. Combined with Cathars' Crusade: every creature entering puts counters on all creatures AND triggers landfall.

**Zuran Orb + earthbent lands:** Sacrifice any earthbent land for free → gain 2 life → land returns tapped → full landfall cycle. With Amulet of Vigor, the returning land untaps, allowing repeated cycles. Without Amulet, each earthbent land is still one free landfall trigger + 2 life. With three earthbent lands, that's three free cycles per turn.

**Crop Rotation (GC) + earthbent lands:** Sacrifice an earthbent land to Crop Rotation → land returns via return clause → searched land enters → two landfall triggers from one spell. Also finds Boseiju for instant-speed removal or Field of the Dead for token generation.

**Liquimetal Coating/Torque + Toph + earthbend = commander protection:** Make Toph an artifact → she becomes a land via her own static → earthbend her → she gains the return clause. If Toph dies, let her go to the graveyard (not the command zone) and she returns to the battlefield with no commander tax.

**Annie Joins Up:** Doubles triggered abilities of legendary creatures. This doubles Toph's earthbend trigger (earthbend 2 twice = two animated lands per end step), doubles all legendary Toph variants' triggers, doubles Tannuk's landfall damage, and the ETB deals 5 damage.

-----

## Kill Lines

**Line 1 — Scute Swarm Exponential + Purphoros**
With 6+ lands, each landfall creates a copy of Scute Swarm. Each copy triggers on subsequent landfall. Playing 2–3 lands in a turn creates dozens to hundreds of Scute Swarm copies. Purphoros, God of the Forge deals 2 damage to each opponent per creature entering — 10 Scute copies = 20 damage to each opponent. With Cathars' Crusade: each entering Scute puts +1/+1 on everything, and All Will Be One deals damage per counter placed. With Impact Tremors: additional 1 damage per creature entering.

**Line 2 — Triumph of the Hordes (one-card closer)**
{2}{G}{G}: all creatures get +1/+1, trample, and infect. Three earthbent lands with 4+ counters each = 15+ infect damage with trample. 10 poison counters = lethal regardless of life total. This is the "I win now" the deck was missing — converts any developed board of earthbent lands into a single lethal swing.

**Line 3 — Moraug Extra Combats**
Each landfall triggers an extra combat phase. With multiple land drops per turn (Entish Restoration getting 2–3 basics, Awaken the Woods, Crop Rotation + earthbent land for two triggers), Moraug creates 3–5 combat phases. Earthbent land-creatures with double strike (Toph, Greatest Earthbender) swing for lethal through accumulated combat steps.

**Line 4 — Toph Greatest Earthbender Double Strike**
Toph Greatest Earthbender gives all land creatures double strike. Earthbent lands with 4–12 counters (after amplifiers) swing for 8–24 double strike damage each. With 3–4 earthbent lands, that's lethal.

**Line 5 — All Will Be One Burn**
Each +1/+1 counter placed deals that much damage. With the amplifier suite (Hardened Scales + Doubling Season + Earth Crystal), a single earthbend 2 deals 12+ damage. Multiple earthbend sources per turn (Toph commander + Toph Hardheaded Teacher casting spells + Toph Earthbending Master attacking) stack the damage. Annie Joins Up doubling legendary triggers multiplies this further.

**Line 6 — Purphoros + Awaken the Woods**
Awaken the Woods for X creates X 1/1 Forest Dryad creature tokens. Each one enters as a creature, triggering Purphoros (2 damage each). X=10 = 20 damage to each opponent. With Cathars' Crusade, each dryad also puts a +1/+1 counter on all your creatures, potentially triggering All Will Be One 10 times.

-----

## Expected Kill Window

### Goldfish: T7–9

The uncontested timeline:

- **T1–2:** Ramp (Sol Ring, Arcane Signet, Nature's Lore, Farseek). Deploy cheap engine pieces if drawn (Hardened Scales, Lotus Cobra, Badgermole Cub).
- **T3–4:** Toph lands (4 mana, achievable T3 with Sol Ring or T4 naturally). End step: earthbend 2 on the first land. From this point forward, one land animates per end step automatically.
- **T5–6:** Deploy landfall payoffs (Scute Swarm, Felidar Retreat, Evolution Sage) and amplifiers (Doubling Season, Earth Crystal, Cathars' Crusade). Second and third earthbent lands accumulate. Smothering Tithe starts generating Treasure if deployed early, accelerating toward expensive payoffs. Scute Swarm becomes exponential once 6+ lands are in play.
- **T7–9:** Close with one of the decisive finishers. Triumph of the Hordes with 3 earthbent lands at 4+ counters each = lethal infect swing. Purphoros + Awaken the Woods for X=7–10 (achievable with Smothering Tithe mana) = 14–20 damage to each opponent. All Will Be One + amplifier suite turns a single earthbend trigger into 12+ damage.

The fastest goldfish is T6: Sol Ring T1, Toph T2, Hardened Scales + Scute Swarm T3–4, Triumph T6 with 3 animated lands. This requires a near-perfect opening hand and is not typical.

The average goldfish is T8: Toph on T4, 2–3 turns of engine building, closer drawn or in hand by T8. The deck doesn't tutor for its finishers (no Tooth and Nail, no Chord of Calling for Purphoros), so finding a closer depends on natural draws and Terrasymbiosis/Esper Sentinel providing card advantage.

### Through Interaction: T10–12

Realistic disruption scenario:

- **Toph removed once (T5–6):** Recast for 6 mana, or return for free if the Liquimetal protection line was established. Costs 1–2 turns of engine momentum.
- **Board wipe around T7 (Wrath of God / Farewell):** Earthbent lands return as lands (not creatures) — you keep your mana base. Purphoros survives if devotion is below 5 (indestructible enchantment). Non-indestructible creatures and enchantments are lost. Rebuild: replay Toph (4–6 mana), earthbend at end step, redeploy 1–2 payoffs. Threatening again in 2 turns.
- **Cyclonic Rift (worst case):** Earthbent lands do NOT return (bounced to hand, not death/exile). Everything goes to hand. Recovery takes 3–4 turns — replay Toph, replay engine pieces, re-earthbend lands. This is the scenario that pushes the kill window toward T12.

The 3-turn gap between goldfish and through-interaction is consistent with a snowball deck that doesn't tutor. The deck rebuilds faster than most after a standard Wrath (earthbend return clause), but slower than graveyard decks (Teval) or tutor-heavy decks (The Grand Design) after Cyclonic Rift.

The deck does NOT threaten a decisive turn before T6 under any circumstances. No early combo restriction is violated. The earliest realistic kill through interaction is T9 (one piece of removal absorbed, closer already in hand).

-----

## Conversion Check Breakdown

### Core Loop: 5/5

The loop is "play permanents → Toph makes artifacts into lands → landfall triggers fire → counters placed → amplifiers multiply → earthbend animates lands → repeat." 30+ cards directly serve this loop across three layers. The engine is recognizable from the decklist and has deep redundancy within each layer.

Two independent paths now generate landfall triggers: natural land drops (significantly strengthened by Crop Rotation, which doubles as a landfall engine piece and utility land tutor), and nontoken artifacts entering as lands via Toph's static. Smothering Tithe doesn't trigger landfall directly (Treasures are tokens, excluded by Toph's static), but it provides massive mana acceleration that gets the deck to its expensive payoffs (Avatar Kyoshi at 8 mana, large Awaken the Woods, Bristly Bill activation) 1–2 turns earlier. Cutting dead weight (Mindslaver, Mycosynth Lattice, Terra Eternal) and adding functional density (Crop Rotation, Purphoros, Triumph of the Hordes) means fewer games where you draw engine-irrelevant cards.

Toph is still a meaningful dependency for Layer 1 (artifact-land bridge), but the Liquimetal commander protection line means she's harder to remove than she looks. The landfall and counter engines function independently of Toph when fed by actual land drops.

**Checkpoint:** Cover the commander. The 99 has 10 earthbend sources, 10 landfall payoffs, 5 counter amplifiers, Smothering Tithe generating mana, and Crop Rotation tutoring utility lands. The strategy is unmistakable.

### Kill Reliability: 4/5

Six distinct closing lines, now including two decisive finishers that convert any developed board into lethal in a single turn. Triumph of the Hordes is a one-card kill from a board of earthbent lands. Purphoros + Scute Swarm or Awaken the Woods threatens lethal from token generation alone. All Will Be One with the full amplifier suite deals 12+ damage per earthbend trigger.

The window between "threatening" and "winning" has collapsed from 3–4 turns to 1–2. Triumph of the Hordes specifically doesn't care about life totals — 10 poison is lethal.

Doesn't reach 5 because the deck still lacks a single-card "from nothing" win like Tooth and Nail. Triumph requires a board presence. Purphoros requires creature token generation. The kills are fast from engine-online but still need the engine to be online first.

**Checkpoint:** Engine online with 3 earthbent lands at 4+ counters → Triumph of the Hordes = lethal in one swing. Scute Swarm + 2 landfall triggers + Purphoros = 20+ damage from an empty board. Both achievable by turn 6–7.

### Durability: 4/5

Earthbend's return clause is the defining durability feature. Animated lands that die return to the battlefield tapped — they don't go to the graveyard permanently. A board wipe kills your earthbent land-creatures, but they all return as lands. Sylvan Safekeeper sacrifices a land to protect a creature, and earthbent lands return after being sacrificed.

The Liquimetal commander protection line (Coating/Torque → Toph becomes artifact-land → earthbend → return clause) means Toph herself can survive removal without commander tax. This significantly reduces the deck's commander dependency — the biggest weakness identified in the previous assessment.

The Ozolith stores counters from dying creatures and reattaches them, preserving the investment in counter amplification. After a wipe: Toph returns (4 mana or free via return clause), earthbend at end step, rebuild counters in 1–2 turns.

Doesn't reach 5 because the non-earthbent enchantments and artifacts (Hardened Scales, Doubling Season, All Will Be One, Cathars' Crusade, Smothering Tithe) are vulnerable to enchantment/artifact hate. A Bane of Progress dismantles the amplifier suite, and the deck has limited ways to recover those pieces. The earthbend return clause protects creatures and lands, not enchantments.

**Checkpoint:** Cyclonic Rift on turn 7. Earthbent lands do NOT return (Rift bounces to hand, not death/exile). This is the deck's worst-case disruption. Recovery: replay Toph (4 mana), replay cheap pieces from hand, earthbend at end step. Threatening again in 2 turns. A standard board wipe (Wrath of God) is much better for you — earthbent lands return immediately, Purphoros is indestructible, and only the non-indestructible creatures die.

### Interaction: 4/5

12 interaction and protection pieces:

- **Stack interaction (3):** Deflecting Swat (free redirect), Red Elemental Blast (counter/destroy blue), Pyroblast (counter/destroy blue)
- **Targeted removal (5):** Path to Exile, Swords to Plowshares, Beast Within, Generous Gift, Origin of Metalbending
- **Artifact/enchantment removal (2):** Haywire Mite (exile), Boseiju Who Endures (channel)
- **Land tutor as removal (1):** Crop Rotation finding Boseiju = instant-speed artifact/enchantment/land destruction
- **Protection (3):** Galadriel's Dismissal (phase out), Earthshape (earthbend 3 + hexproof/indestructible for creatures), Collective Resistance (flexible escalate)
- **Commander protection (2):** Liquimetal Coating + Liquimetal Torque enabling the earthbend return clause on Toph

Going from 1 stack answer to 3 (Deflecting Swat + REB + Pyroblast) is the most impactful change. Against the pod's combo player, having three answers to a resolved spell across a game is realistic draw probability in a 99-card deck. Generous Gift replaces the self-destructive board wipes with a surgical instant-speed catch-all.

Doesn't reach 5 because the stack interaction is narrow — REB and Pyroblast only hit blue. Against non-blue combo or non-blue threats, Deflecting Swat is still the only stack answer. The deck also runs zero board wipes (deliberately — they're self-destructive in this strategy), which means a board full of opponent creatures must be answered one at a time or raced.

-----

## Upgrade Log

### April 2026 — Seven Swaps (14/20 → 17/20)

| Out | In | Rationale |
|---|---|---|
| Mindslaver | Smothering Tithe (GC) | 10-mana repeatable combo replaced by passive mana engine. Smothering Tithe generates Treasures that fund the deck's expensive payoffs (Kyoshi, Awaken the Woods, Bristly Bill activation). |
| Terra Eternal | Crop Rotation (GC) | Redundant protection (earthbend return clause already handles land death) replaced by instant-speed utility land tutor. Sacrifice triggers return clause; searched land triggers landfall; finds Boseiju for removal. |
| Mycosynth Lattice | Purphoros, God of the Forge | 6-mana Toph-dependent win-more replaced by indestructible finisher. Purphoros converts Scute Swarm tokens, Field of the Dead zombies, and Awaken the Woods dryads into direct damage without needing combat. |
| Ondu Inversion | Triumph of the Hordes | 8-mana self-destructive sorcery-speed wipe replaced by one-card lethal closer. 10 poison from earthbent lands with trample ends games that life-total damage can't. |
| Great Divide Guide | Pyroblast | Mana fixing role already covered by Dryad of the Ilysian Grove. Pyroblast adds a second anti-blue stack answer for the combo matchup. |
| Secret Tunnel | Red Elemental Blast | Colorless land with an expensive ability replaced by a third stack answer. Goes from 1 way to stop a combo (Deflecting Swat) to 3. |
| Hour of Revelation | Generous Gift | Self-destructive board wipe (destroys your own engine) replaced by {2}{W} instant that catches any permanent. Surgical over nuclear. |

**GC correction:** Doubling Season was originally labeled as a Game Changer but is NOT on the official GC list. Field of the Dead IS a Game Changer and was already in the deck. After this upgrade, all 3 GC slots are now used: Field of the Dead, Smothering Tithe, Crop Rotation.

### MH3 — Springheart Nantuko (previous upgrade)

Springheart Nantuko replaced Solemn Simulacrum. The Nantuko is a {1}{G} enchantment creature with bestow {1}{G}{G}{G} and landfall — create a 1/1 insect OR pay {1}{G} to create a token copy of enchanted creature. At 2 mana it deploys early and provides a landfall trigger on every land drop for the rest of the game. In copy mode with bestow on Scute Swarm, it goes exponential.

-----

## Bracket 3 Compliance

**Game Changers (3 of 3 used):**
1. Field of the Dead — land that creates zombie tokens with 7+ differently named lands
2. Smothering Tithe — passive Treasure generation from opponent draws
3. Crop Rotation — instant-speed land tutor (sacrifice a land, search for any land)

**Infinite combos:** No deterministic infinite. The closest is Zuran Orb + Amulet of Vigor + earthbent lands creating repeatable landfall, but this requires specific pieces and doesn't go infinite by itself (limited by how many lands are earthbent and by the number of untap cycles Amulet provides).

**Extra turns:** None.

**Mass land denial:** None. The deck creates and recurs its own lands, never destroys opponents'.

-----

## Pod Fit

1. **Snowball threat.** The deck gets stronger every turn as counters accumulate and the board widens. Left unchecked for 2–3 turns after Toph lands, it becomes unmanageable.
2. **Resilient to creature removal.** Earthbent lands return after dying. Individual removal barely slows the engine. Toph herself can gain the return clause via Liquimetal + earthbend.
3. **Decisive closing speed.** Triumph of the Hordes and Purphoros mean the deck no longer needs 3–4 turns to convert advantage into lethal. One good turn with a developed board is enough.
4. **Vulnerable to enchantment/artifact hate.** The amplifier suite (Hardened Scales, Doubling Season, The Earth Crystal, Cathars' Crusade, All Will Be One, Smothering Tithe) is entirely enchantments and artifacts. A Bane of Progress or Vandalblast dismantles the engine.
5. **Improved against combo.** Three stack answers (Deflecting Swat, REB, Pyroblast) plus Crop Rotation finding Boseiju gives realistic odds of stopping a combo attempt. Still not blue-deck levels of protection, but no longer a free win for the combo player.
6. **Vulnerable to Cyclonic Rift specifically.** Rift bounces rather than destroys, so earthbent lands do NOT return. This is the deck's worst-case scenario among common disruption.

-----

## Differentiation From Other Decks

| | Toph (Earthbend the Meta) | Teval (The Loam Cycle) |
|---|---|---|
| Engine | Artifacts → lands → landfall → counters | Self-mill → graveyard recursion |
| Land interaction | Animate lands as creatures, return on death | Recur lands from graveyard |
| Colors | RGW (white removal + protection) | BUG (blue counters + black recursion) |
| Kill speed | Moderate (1–2 turns from developed board) | Fast (1–2 turns, Tooth and Nail) |
| Durability | High (earthbend return clause) | Very high (graveyard survives wipes) |

Both are lands-matter decks but use completely different resources. Teval recurs from the graveyard; Toph animates on the battlefield. No shared engine pieces beyond generic ramp.

-----

## Decklist (100 cards)

### Commander (1)

1 Toph, the First Metalbender

### Game Changers (3)

1 Field of the Dead
1 Smothering Tithe
1 Crop Rotation

### Earthbend Sources (10)

1 Toph, Earthbending Master
1 Toph, Greatest Earthbender
1 Toph, Hardheaded Teacher
1 Toph, the Blind Bandit
1 Bumi, Eclectic Earthbender
1 Bumi, Unleashed
1 Badgermole Cub
1 Earthbender Ascension
1 Earthshape
1 Bitter Work

### Landfall Payoffs (9, plus Field of the Dead above)

1 Felidar Retreat
1 Scute Swarm
1 Evolution Sage
1 Lotus Cobra
1 Moraug, Fury of Akoum
1 Tireless Provisioner
1 Tannuk, Memorial Ensign
1 Bristly Bill, Spine Sower
1 Springheart Nantuko

### Counter Amplifiers (5)

1 Hardened Scales
1 Doubling Season
1 The Earth Crystal
1 Cathars' Crusade
1 The Ozolith

### Damage Payoffs (3)

1 All Will Be One
1 Impact Tremors
1 Purphoros, God of the Forge

### Creature-Land Bridges (2)

1 Ashaya, Soul of the Wild
1 Dryad of the Ilysian Grove

### Artifact-Land Enablers (3)

1 Liquimetal Coating
1 Liquimetal Torque
1 Bootleggers' Stash

### Land Synergy (2)

1 Amulet of Vigor
1 Zuran Orb

### Token Generation (1)

1 Awaken the Woods

### ATLA Theme / Utility (3)

1 Avatar Kyoshi, Earthbender
1 The Legend of Kyoshi
1 Earthbending Student

### Legendary Trigger Doubler (1)

1 Annie Joins Up

### Card Draw (2)

1 Terrasymbiosis
1 Esper Sentinel

### Planeswalker (1)

1 Wrenn and Realmbreaker

### Removal (5)

1 Path to Exile
1 Swords to Plowshares
1 Beast Within
1 Origin of Metalbending
1 Generous Gift

### Artifact/Enchantment Removal (2)

1 Haywire Mite
1 Boseiju, Who Endures

### Stack Interaction (3)

1 Deflecting Swat
1 Red Elemental Blast
1 Pyroblast

### Protection (3)

1 Galadriel's Dismissal
1 Collective Resistance
1 Sylvan Safekeeper

### Finishers (1)

1 Triumph of the Hordes

### Equipment (2)

1 Lightning Greaves
1 Swiftfoot Boots

### Ramp (6)

1 Sol Ring
1 Arcane Signet
1 Farseek
1 Nature's Lore
1 Entish Restoration
1 Brightglass Gearhulk

### MDFC Land/Spells (2)

1 Disciple of Freyalise
1 Witch Enchanter

### Lands (30 + Field of the Dead in GC + Boseiju in removal + 2 MDFCs above = 34 total mana sources)

1 Command Tower
1 Exotic Orchard
1 Sacred Foundry
1 Stomping Ground
1 Temple Garden
1 Jetmir's Garden
1 Arid Mesa
1 Windswept Heath
1 Wooded Foothills
1 Fabled Passage
1 Evolving Wilds
1 Terramorphic Expanse
1 Darksteel Citadel
1 Kessig Wolf Run
1 Lotus Field
1 Riftstone Portal
1 Urza's Saga
1 Yavimaya, Cradle of Growth
1 Ba Sing Se
1 Talon Gates of Madara
5 Forest
2 Mountain
3 Plains
