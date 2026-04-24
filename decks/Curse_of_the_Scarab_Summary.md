# Curse of the Scarab — The Scarab God

## Quick Reference

| Field | Value |
|---|---|
| **Commander** | The Scarab God ({3}{U}{B}, 5/5 Legendary Creature — God) |
| **Colors** | Dimir (UB) |
| **Archetype** | Zombie tribal / drain |
| **Bracket** | 3 (3 Game Changers: Cyclonic Rift, Demonic Tutor, Fierce Guardianship) |
| **Game Changers** | Cyclonic Rift, Demonic Tutor, Fierce Guardianship |
| **Conversion Check** | **17/20** (5/4/4/4) |
| **Kill Window** | Goldfish: T7–9 · Through interaction: T9–12 |

-----

## Commander Rules Text

The Scarab God has three abilities:

1. **Upkeep drain + scry:** At the beginning of your upkeep, each opponent loses X life and you scry X, where X is the number of Zombies you control.
2. **Activated reanimation:** {2}{U}{B}: Exile target creature card from a graveyard. Create a token that's a copy of it, except it's a 4/4 black Zombie.
3. **Death resilience:** When The Scarab God dies, return it to its owner's hand at the beginning of the next end step.

Key rulings: The upkeep trigger counts zombies at resolution, so instant-speed zombie creation (Cryptbreaker, Cemetery Reaper) can increase the count in response. The activated ability exiles the creature card — it doesn't return it, so the original is gone. The token copy keeps all abilities of the original creature but becomes a 4/4 black Zombie regardless of original stats or colors. The death trigger returns The Scarab God to hand, not the command zone — this means no commander tax accumulates if you choose the death trigger over the command zone replacement. If The Scarab God leaves the graveyard before the end step (exiled, shuffled in), the trigger does nothing.

-----

## What the Deck Does

The deck floods the board with zombies through tribal synergy, token generation, and reanimation, then exploits zombie count for passive drain, card advantage, and lethal combat. Every zombie entering the battlefield simultaneously grows the army (Champion of the Perished, Diregraf Colossus), replaces itself on death (Wilhelt, Headless Rider), triggers card draw (Kindred Discovery, Undead Augur), and increases the upkeep drain from The Scarab God.

### Layer 1 — Zombie Lords (7 pieces)

The deck runs a deep lord package that turns individually weak zombies into a lethal combat force:

- **Death Baron:** +1/+1 and deathtouch to all zombies and skeletons. Deathtouch makes every zombie token a credible blocker and forces unfavorable blocks from opponents.
- **Diregraf Captain:** +1/+1 to zombies, drains 1 life from target opponent whenever a zombie you control dies. Dual-role: lord + death trigger payoff.
- **Lord of the Accursed:** +1/+1 to zombies, tap to give all zombies menace until end of turn. Menace with a wide board is frequently unblockable.
- **Undead Warchief:** +2/+1 to zombies, zombie spells cost {1} less. The biggest stat boost in the package and the only cost reducer.
- **Cemetery Reaper:** +1/+1 to zombies, pay {2}{B} and tap to exile a creature card from a graveyard and create a 2/2 zombie token. Lord + graveyard hate + token generation on one card.
- **Zombie Master:** Gives all zombies swampwalk and "{B}: Regenerate this permanent." With Urborg, Tomb of Yawgmoth in play, swampwalk is unblockable. Regeneration protects against destroy-based removal and damage-based wipes.
- **Narfi, Betrayer King:** +1/+1 to snow and zombie creatures. Costs {3}{U}{B} but can return from graveyard to battlefield for {S}{S}{S} — self-recurring lord that doesn't need to be cast from hand.

With two lords in play, 2/2 zombie tokens become 4/4s. Three lords make them 5/5s or larger. The density ensures at least one lord is in play at almost any point in the game.

**Mikaeus, the Unhallowed** functions as a pseudo-lord — he gives all non-Human creatures +1/+1 and undying. He's not a zombie himself, but the +1/+1 buff to the entire army is a lord-equivalent stat boost, and undying means every zombie comes back once after dying. This makes board wipes cost opponents two wipes to fully clear the board.

### Layer 2 — Zombie Token Generation (6 pieces)

- **Grave Titan:** Creates two 2/2 zombie tokens on ETB and on each attack. Six power plus four tokens over two turns. One of the highest-impact single cards in the deck.
- **Ghoulcaller Gisa:** Tap, sacrifice a creature, create X 2/2 zombies where X is the sacrificed creature's power. With a lord-pumped zombie, this converts one creature into many. Sacrificing Grave Titan (6 power) creates 6 zombies.
- **Diregraf Colossus:** Enters with +1/+1 counters equal to zombies in graveyard. Whenever you cast a zombie spell, create a 2/2 zombie token. Snowballs rapidly — every zombie cast creates a free body.
- **Necroduality:** Whenever a nontoken zombie enters the battlefield under your control, create a token copy of it. Doubles every zombie cast. A second lord, a second Grave Titan, a second of anything.
- **Wilhelt, the Rotcleaver:** Whenever a zombie you control dies (if it didn't have decayed), create a 2/2 zombie with decayed. Also, at the beginning of your end step, sacrifice a zombie to draw a card. Replacement engine — every zombie death creates a new body.
- **Crowded Crypt:** Whenever a creature you control dies, put a corpse counter on Crowded Crypt. Pay {4}{B}{B}, sacrifice Crowded Crypt: create X 2/2 zombie tokens, where X is the number of corpse counters on it. Tracks deaths throughout the game, then converts them into a single massive board.

### Layer 3 — Card Draw and Selection (5 pieces)

- **Kindred Discovery:** Whenever a zombie enters the battlefield or attacks, draw a card. In a zombie tribal deck, this draws 3–6 cards per turn cycle once the engine is running. The single strongest draw engine in the deck — if it resolves, the game is often over.
- **Skullclamp:** Equip to a 1/1 or decayed 2/2 token (Wilhelt tokens die immediately to the -1 toughness). Draw 2 per death. With Gravecrawler or token generators, this is repeatable draw.
- **Graveborn Muse:** At your upkeep, draw X and lose X life, where X is the number of zombies you control. Powerful but dangerous — with 5+ zombies, the life loss adds up quickly. The Scarab God's drain on opponents partially offsets this.
- **Cryptbreaker:** Tap, discard a card: create a 2/2 zombie token. Tap three untapped zombies: draw a card and lose 1 life. Early-game token generator that transitions to a draw engine once the board develops.
- **Undead Augur / Midnight Reaper:** Whenever a zombie you control dies, draw a card and lose 1 life. Death-trigger draw that stacks with Wilhelt's replacement tokens. Two copies of this effect provide reliable draw through creature deaths.
- **Black Market Connections:** Steady incremental draw, Treasure, and token generation.

### Layer 4 — Reanimation, Recursion, and Tutoring (8 pieces)

- **Living Death:** Each player sacrifices all creatures, then returns all creature cards from their graveyard to the battlefield. In a deck designed to stock the graveyard (Buried Alive, Entomb, self-mill, natural creature deaths), this is a one-sided mass reanimation. The single most explosive card in the deck.
- **Zombie Apocalypse:** Return all zombie creature cards from your graveyard to the battlefield, then destroy all humans. Asymmetric mass reanimation for zombies specifically — no risk of returning opponents' creatures.
- **Agadeem's Awakening:** MDFC that enters as a tapped land or casts as a mass reanimation spell returning creatures with different mana values. Late-game, this is Living Death #2. Zero deckbuilding cost since it occupies a land slot.
- **Reanimate:** One mana to put any creature from any graveyard onto the battlefield. Life cost equal to its mana value is trivial at 40 life. Entomb + Reanimate on turn 2 = Grave Titan or Gray Merchant.
- **Necromancy:** Reanimation at flash speed. Deploy at end of turn or in response to an opponent's attack. Flash reanimation is uniquely powerful because it lets you "hold up interaction" while actually deploying threats. Bring back Gray Merchant at instant speed for a surprise drain.
- **Dread Return:** Reanimate a creature. Has flashback — sacrifice three creatures to cast from graveyard. With expendable zombie tokens, the flashback cost is trivial.
- **Victimize:** Sacrifice a creature, return two creature cards from graveyard to the battlefield. Net +1 creature, and the sacrificed creature triggers death payoffs.
- **Buried Alive / Entomb:** Tutor-quality graveyard setup. Buried Alive puts three creatures into the graveyard; Entomb puts one at instant speed for {B}. Both set up Living Death, Reanimate, Necromancy, Dread Return, and The Scarab God's activated ability. Entomb specifically enables turn-1 setup into turn-2 Reanimate — the fastest play the deck can make.
- **Demonic Tutor:** Finds whatever the deck needs for the current board state. Against graveyard hate: Feed the Swarm. Against combo: Fierce Guardianship or Counterspell. Against an open board: Living Death, Kindred Discovery, or Rooftop Storm. This is the single card that transforms the deck's inconsistency into precision.

### Layer 5 — Drain and Damage Acceleration (6 pieces)

Beyond The Scarab God's upkeep drain:

- **Gray Merchant of Asphodel:** Drains each opponent for your black devotion on ETB. In a deck with Death Baron ({B}{B}{B}), Undead Warchief ({2}{B}{B}), Liliana ({4}{B}{B}), Black Market Connections, and Phyrexian mana symbols throughout, devotion of 6–10 is routine. That's 6–10 life drained from each opponent on a single ETB — and you gain all of it. Recurrable via Reanimate, Necromancy, Victimize, Dread Return, or The Scarab God's activated ability for repeated burst drain. This is the deck's highest-impact single card for closing games.
- **Shepherd of Rot:** Tap: each player loses 1 life for each zombie you control. Instant-speed, no mana cost, hits all opponents simultaneously. With 8 zombies, tapping Shepherd deals 8 to each opponent (and to you).
- **Gempalm Polluter:** Cycle for {1}{B}: each opponent loses life equal to the number of zombies you control. Uncounterable (cycling is a special action), instant speed, draws a card. Premium finisher.
- **Plague Belcher:** Drains 1 life from target opponent when a zombie you control dies. Stacks with Diregraf Captain for 2 drain per zombie death.
- **Diregraf Captain:** (Listed under lords, but the death-trigger drain is a kill-line component.)
- **Lost Monarch of Ifnir:** Afflict 3 on itself and all other zombies. Whenever a zombie deals combat damage to a player, mill three cards and may return a creature from graveyard to hand. Punishes blocking (afflict 3 per blocked zombie) while rewarding attacks with self-mill and recursion.

### The Play Pattern

Turn 1–2: Deploy a 1-drop zombie (Gravecrawler, Champion of the Perished, Cryptbreaker) or a mana rock. Entomb + Reanimate enables a turn-2 Grave Titan or Gray Merchant for explosive openings. Turn 3–4: Deploy zombie lords and token generators. Board grows to 3–5 zombies. Turn 5: Cast The Scarab God. Upkeep drain begins — 3–5 per opponent. Scry 3–5 sculpts draws to find Kindred Discovery, mass reanimation, or Gray Merchant. Turn 6–8: Deploy Kindred Discovery or Rooftop Storm to accelerate. Board grows to 8+ zombies. Drain hits 8+ per opponent per upkeep, plus combat damage with lord-pumped creatures. Demonic Tutor finds the closer that matches the board state. If opponents wipe the board, Living Death, Zombie Apocalypse, or Agadeem's Awakening rebuild instantly. Cyclonic Rift clears opponents' boards for a lethal alpha strike. Turn 7–9: Accumulated drain, combat damage, Gray Merchant recursion, and finishers (Gempalm Polluter, Shepherd of Rot) close the game.

-----

## Kill Lines

### Line 1 — The Scarab God Upkeep Drain (Primary)

The passive kill. Each upkeep, every opponent loses life equal to your zombie count. This requires no mana, no attack, no tap — it just happens. With 8 zombies, that's 8 damage to each opponent per upkeep. Five upkeeps from 40 life is lethal, but parallel damage from combat, Shepherd of Rot, and Gempalm Polluter shortens this to 3–4 turn cycles.

The drain stacks with Shepherd of Rot (tap: each player loses 1 per zombie) and Gempalm Polluter (cycle: each opponent loses 1 per zombie). In a single turn cycle with 8 zombies, the deck can deal: 8 (Scarab God upkeep) + 8 (Shepherd of Rot) + 8 (Gempalm cycle) = 24 drain per opponent, plus combat damage. Two turn cycles of stacked drain from a developed board is lethal.

### Line 2 — Gray Merchant Burst Drain (Fastest Non-Combo Kill)

Gray Merchant of Asphodel drains each opponent for your black devotion on ETB. With devotion 8 (common with 2–3 black permanents and Gary's own {3}{B}{B} contributing 2), that's 8 from each opponent and 24 gained. Reanimate it for {B} (lose 5 life, net +19 with the drain). Necromancy it back at flash speed. Victimize it by sacrificing a token. Each recurrence drains 6–10 per opponent.

Two Gray Merchant ETBs in a game = 16–20 drain per opponent. Combined with The Scarab God's passive upkeep drain, this often represents 60–80% of an opponent's life total. Demonic Tutor can find Gray Merchant, and Entomb + Reanimate can deploy it as early as turn 2.

### Line 3 — Lord-Pumped Zombie Combat + Cyclonic Rift

With two lords in play, 2/2 zombie tokens are 4/4s. An army of five 4/4 zombies deals 20 damage per attack. Evasion comes from multiple sources: Lord of the Accursed grants menace, Hordewing Skaab grants flying to all zombies, Wonder grants flying from the graveyard, Zombie Master grants swampwalk (unblockable with Urborg).

Cyclonic Rift (overloaded for 7 mana) bounces all opponents' nonland permanents to their hands — creatures, artifacts, enchantments, everything. A developed zombie board + overloaded Rift = lethal alpha strike into empty defenses. Demonic Tutor can find Cyclonic Rift when the board is ready for the kill.

Lost Monarch of Ifnir adds afflict 3 to the entire zombie army, punishing blocking. An opponent choosing to block five zombies takes 15 afflict damage regardless of how combat resolves.

### Line 4 — Aristocrats Drain (Death Triggers)

Diregraf Captain and Plague Belcher each drain an opponent for 1 life per zombie death. With both in play, every zombie that dies deals 2 drain to a target opponent. Warren Soultrader (sacrifice a creature: create a Treasure, lose 1 life) and Ghoulcaller Gisa provide sacrifice outlets. Mikaeus's undying means each zombie dies twice before staying dead, doubling the death triggers.

### Line 5 — Mass Reanimation into Burst Drain

Buried Alive or Entomb stocks the graveyard with high-impact zombies (Grave Titan, Gray Merchant, Diregraf Captain). Living Death, Zombie Apocalypse, or Agadeem's Awakening brings them all back simultaneously. A single Living Death resolving with 8+ zombies in the graveyard creates a board that threatens lethal drain on the next upkeep — and if Gray Merchant is among the returned creatures, the drain starts immediately on ETB.

This line functions as a recovery kill — the deck is at its most dangerous immediately after a board wipe, when both graveyards are full and Living Death creates a massive asymmetry.

### Line 6 — Rooftop Storm Explosion

Rooftop Storm makes all zombie spells cost {0}. With Necroduality doubling every zombie cast and Diregraf Colossus creating additional tokens per cast, emptying a hand of 4 zombies creates 4 + 4 copies + 4+ Colossus tokens = 12+ zombies in a single turn. Kindred Discovery draws a card per zombie entering, refueling the hand immediately. The following upkeep, Scarab God drains 12+ from each opponent.

### Line 7 — Warren Soultrader Infinite (Rule 0)

Warren Soultrader + Gravecrawler + Diregraf Captain or Plague Belcher is a three-card infinite loop. Sacrifice Gravecrawler to Warren Soultrader (create Treasure, lose 1 life) → spend Treasure to recast Gravecrawler for {B} → repeat. Each cycle drains an opponent for 1 (or 2 with both payoffs). Self-limiting by your life total — at 40 life, deals up to 39 damage. Flagged for pod Rule 0 discussion.

-----

## Conversion Check Breakdown

### Core Loop: 5/5

The loop is "deploy zombies → zombies generate more zombies → zombie count drives drain, draw, and combat." 25+ cards in the deck directly serve the zombie tribal engine: 7 lords plus Mikaeus, 6 token generators, 6 drain payoffs (including Gray Merchant), 8 recursion/reanimation/tutor pieces, plus Rooftop Storm. Every creature in the deck except Wonder and Mikaeus is a zombie or creates zombies. Mikaeus gives all non-Humans +1/+1 and undying, making him functionally part of the tribal engine despite not being a zombie himself.

The commander is the primary drain payoff, but the 99 alone is unmistakably a zombie tribal deck — cover the commander and the identity is immediately obvious from the lord density, death triggers, and tribal-specific spells.

**Checkpoint:** Cover the commander. 7 lords, Mikaeus, Kindred Discovery, Necroduality, Rooftop Storm, Living Death, Zombie Apocalypse, Buried Alive, 15+ zombie creatures. The strategy is unmistakable.

### Kill Reliability: 4/5

Seven closing lines spanning drain, burst ETB damage, combat, death triggers, mass reanimation, and explosive casting. Gray Merchant provides the burst finisher the deck previously lacked — a single recurrable ETB that removes 15–30% of each opponent's life total per resolution. Cyclonic Rift creates deterministic lethal alpha strikes from developed boards. Demonic Tutor finds whichever closer matches the current board state.

The fastest reliable kill from engine-online (5+ zombies, Scarab God in play) is 2–3 turns through Gray Merchant recursion plus stacked drain and combat. Entomb + Reanimate enables a turn-2 Grave Titan or Gray Merchant for explosive openings that previous builds couldn't achieve.

All kill lines still depend on the shared resource of zombie/creature count on the battlefield — a board wipe weakens everything simultaneously. This structural dependency on a single resource type is what prevents a 5. But Demonic Tutor's ability to find mass reanimation (Living Death, Zombie Apocalypse, Agadeem's Awakening) after a wipe means the recovery-into-kill line is now reliably accessible rather than draw-dependent.

**Checkpoint:** Engine-online, 8 zombies, Scarab God in play, Gray Merchant in graveyard. Upkeep drains 8, Reanimate Gray Merchant for 8+ devotion drain, Shepherd of Rot drains 8. That's 24–32 per opponent in a single turn cycle. Lethal in one cycle if devotion is high enough.

### Durability: 4/5

The Scarab God's death trigger is the deck's best structural advantage. When The Scarab God dies, it returns to your hand — not the command zone. No commander tax accumulates from death-based removal. Only exile effects permanently deal with it.

Beyond the commander, the deck has layered recovery:

- **Mass reanimation (3 pieces):** Living Death, Zombie Apocalypse, and Agadeem's Awakening rebuild the entire board from the graveyard after a wipe. Three mass reanimation options means you're likely to have access to at least one.
- **Targeted reanimation (4 pieces):** Reanimate, Necromancy (flash speed), Dread Return (flashback from GY), Victimize. Deep targeted reanimation means every key creature lost can be recovered.
- **Self-recurring creatures:** Gravecrawler returns from graveyard for {B} with any zombie in play. Narfi returns from graveyard for {S}{S}{S}. These restart the engine without requiring reanimation spells.
- **Undying (Mikaeus):** Every non-Human creature comes back once after dying with a +1/+1 counter. Board wipes cost opponents two wipes to fully clear.
- **Death replacement:** Wilhelt and Headless Rider create replacement zombies on creature deaths, making 1-for-1 removal nearly pointless.
- **Tutor recovery:** Demonic Tutor finds the right recovery tool for the situation — Living Death after a wipe, Feed the Swarm against Rest in Peace, Fierce Guardianship to protect against the next wipe.

Doesn't reach 5 because graveyard hate cripples multiple recovery lines simultaneously. Rest in Peace, Leyline of the Void, and Dauthi Voidwalker shut off the entire reanimation package, Gravecrawler, Narfi, and The Scarab God's activated ability. The deck has Feed the Swarm and counterspells to answer these, and Demonic Tutor can find Feed the Swarm, but a resolved Rest in Peace before the deck finds an answer is still devastating.

**Checkpoint:** Cyclonic Rift on turn 7. Scarab God returns to hand (death trigger). Replay for 5 mana next turn. Demonic Tutor for Living Death or Zombie Apocalypse. Full board recovery in 1–2 turns.

### Interaction Profile: 4/5

13 interaction pieces:

- **Free counterspells (2):** Fierce Guardianship (free with Scarab God in play), Force of Negation (exile a blue card from hand; the draw engines provide fuel). Two free counterspells completely solve the develop-vs-hold-up tension — cast Rooftop Storm or Kindred Discovery on your turn and still threaten to stop a combo attempt.
- **Paid counterspells (3):** Counterspell, An Offer You Can't Refuse, Arcane Denial.
- **Asymmetric board wipe (1):** Cyclonic Rift — overloaded, bounces all opponents' nonland permanents. The single most impactful interaction spell in Commander.
- **Board wipe (1):** Toxic Deluge.
- **Creature removal (3):** Go for the Throat, Rapid Hybridization, Feed the Swarm (also hits enchantments).
- **Pseudo-wipe (1):** Noxious Ghoul — gives all non-zombies -1/-1 whenever a zombie enters. With Necroduality or Grave Titan creating multiple zombies in one turn, this is a one-sided board wipe.
- **Planeswalker removal (1):** Liliana, Dreadhorde General — her -4 forces each opponent to sacrifice two creatures.
- **Graveyard hate (1):** Bojuka Bog — exiles a target opponent's graveyard.

Five counterspells with two free ones is a meaningful stack presence. The deck can now protect its combo turns (Rooftop Storm, Living Death) while still developing the board. Cyclonic Rift adds an asymmetric reset that doubles as a kill enabler. Demonic Tutor can find whichever interaction piece the situation demands.

Doesn't reach 5 because Feed the Swarm remains the only answer to enchantments, and it's sorcery speed. A resolved Rest in Peace or opposing Rhystic Study can only be countered on the stack or removed by this single card. Dimir's structural inability to handle enchantments is the permanent ceiling on this axis. 12+ interaction pieces is nominally a 5 count, but the enchantment blindspot and the tempo-negative counters (Arcane Denial gives opponent cards, An Offer gives Treasures) keep the quality at 4.

**Checkpoint:** Opponent is about to combo off. You have Fierce Guardianship or Force of Negation available at no mana cost. The combo is stopped. Your zombie board survives. You untap and drain.

### Total: 17/20 — Structurally excellent. Pilot skill is the main variable.

The upgrades directly addressed both weak axes. Gray Merchant, Cyclonic Rift, and Demonic Tutor transformed kill reliability from "grind and hope" into "find the right closer and execute." Fierce Guardianship and Force of Negation gave the deck genuine stack presence without sacrificing board development. The Core Loop remains elite, Durability is unchanged, and the deck now converts strong positions into wins reliably.

-----

## Expected Kill Window

**Goldfish: T7–9.** Entomb + Reanimate enables a turn-2 Gray Merchant or Grave Titan, accelerating the clock by 2 turns over the pre-upgrade version. Scarab God typically resolves turn 5. Board grows to 8+ zombies by turn 6–7 with token generators. Demonic Tutor finds the right closer. Gray Merchant recursion or stacked drain + combat closes by turn 7–9 uncontested.

**Through interaction: T9–12.** A board wipe on turn 6–7 resets zombie count. Recovery now takes 1–2 turns (Demonic Tutor finds mass reanimation, three mass reanimation options increase likelihood of natural draws). Fierce Guardianship and Force of Negation protect key turns without mana investment. Cyclonic Rift creates lethal alpha strikes that bypass normal combat math. Games against interaction-heavy pods close by turn 9–12.

The 2–3 turn gap between goldfish and through-interaction is tighter than the pre-upgrade version because free counterspells protect key development turns and Demonic Tutor ensures the right recovery tool is available post-wipe.

-----

## Bracket 3 Compliance

**Game Changers (3 of 3 used):**
1. **Cyclonic Rift** — asymmetric board wipe (overload bounces all opponents' nonland permanents)
2. **Demonic Tutor** — unrestricted tutor (find any card in library)
3. **Fierce Guardianship** — free counterspell with commander in play

All three GC slots are occupied — no further Game Changers can be added without a swap.

**Notable non-GC power cards:** Force of Negation, Kindred Discovery, Rooftop Storm, Living Death, Necroduality, Skullclamp, Gray Merchant of Asphodel, Reanimate, Necromancy, Entomb, Mikaeus the Unhallowed, Liliana Dreadhorde General, Toxic Deluge, Buried Alive, Agadeem's Awakening.

**Infinite combos:** Warren Soultrader + Gravecrawler + a drain payoff (Diregraf Captain or Plague Belcher) forms a three-card infinite loop. Sacrifice Gravecrawler to Warren Soultrader (create a Treasure, lose 1 life) → spend the Treasure to recast Gravecrawler from the graveyard for {B} → repeat. Each cycle drains one opponent for 1 (Plague Belcher) or 1 to target opponent (Diregraf Captain). The loop is self-limiting by your life total — each cycle costs you 1 life, so you can loop as many times as you have life points minus 1. At 40 life, this deals up to 39 damage. With both Diregraf Captain and Plague Belcher, each cycle drains 2 per iteration. This should be flagged for pod Rule 0 discussion per B3 guidelines, as it is a three-card infinite that can assemble naturally. Demonic Tutor could find the missing piece, but the loop doesn't consistently assemble before turn 6.

**Extra turns:** None.

**Mass land denial:** None.

-----

## Pod Fit

The zombie tribal archetype has distinctive pod characteristics:

1. **Grinds through attrition.** Board wipes against this deck are often counterproductive — they stock the graveyard for Living Death, Zombie Apocalypse, Agadeem's Awakening, and The Scarab God's activated ability. Mikaeus's undying means the first wipe doesn't even fully clear the board. Opponents who wipe repeatedly may be helping the zombie player more than hurting them.
2. **Passive inevitability.** The Scarab God's upkeep drain doesn't require an attack, a tap, or mana. Once zombie count is high, opponents are on a clock whether they interact or not. This creates natural pressure without painting a visible target.
3. **Genuine stack presence.** Fierce Guardianship and Force of Negation give the deck two free counterspells. Against the pod's combo player, this is a credible deterrent — the deck can tap out to develop the board and still threaten to stop a win attempt. Three additional paid counterspells provide backup.
4. **Punishes creature-heavy metas.** Noxious Ghoul's -1/-1 per zombie ETB is devastating against token strategies and small-creature decks. Cemetery Reaper and The Scarab God exile opponents' creature graveyards, denying recursion strategies. Death Baron's deathtouch makes every zombie a credible blocker.
5. **Vulnerable to graveyard hate.** Rest in Peace, Leyline of the Void, Dauthi Voidwalker, and Bojuka Bog all cripple multiple lines simultaneously — reanimation, Gravecrawler recursion, Scarab God's activated ability. The deck has Feed the Swarm (for enchantments), counterspells, and Demonic Tutor to find answers, but a resolved Rest in Peace before an answer is drawn remains the deck's worst-case scenario.
6. **Cyclonic Rift creates unrecoverable game states.** An overloaded Rift with a developed zombie board is often game-ending. Opponents may play more conservatively once they know Rift is in the deck, which buys time for the zombie engine to develop.
7. **Threat perception ramps gradually.** Early turns look innocuous — a few 2/2 zombies and some mana rocks. By the time the drain is noticeable, the board is often too developed to cleanly answer. Opponents who wait too long to interact face the deck at its strongest.

-----

## Differentiation From Other Decks

| | Scarab God (Curse of the Scarab) | Golbez (Crystal Sickness) |
|---|---|---|
| Engine | Zombie tribal → death triggers → drain | Artifact ETBs → surveil → threshold drain |
| Token type | Zombie tokens (creature) | Thopters, Clues, Servos (artifact) |
| Commander role | Active engine (drain + reanimation + scry) | Active engine (surveil + recursion + drain) |
| Win axis | Drain (count-based), burst ETB (Gary), combat | Drain (power-based), mill, artifact combat |
| Graveyard dependency | High (mass reanimation + Reanimate/Necromancy) | High (Golbez recurs from GY) |
| Vulnerability | Graveyard hate | Artifact hate |

Both are Dimir and use the graveyard, but the resource they exploit is completely different. Scarab God cares about zombie creature count on the battlefield; Golbez cares about artifact count. No shared engine pieces beyond generic Dimir staples. Both now run 3/3 GC slots: Golbez uses Chrome Mox, Fierce Guardianship, The One Ring; Scarab God uses Cyclonic Rift, Demonic Tutor, Fierce Guardianship. Fierce Guardianship is the only shared GC.

| | Scarab God (Curse of the Scarab) | Teysa (Diminishing Returns) |
|---|---|---|
| Engine | Zombie tribal + passive drain | Sacrifice + death triggers |
| Token role | Persistent army (stays on board) | Sacrifice fodder (intentionally dies) |
| Commander role | Active drain + reanimation | Passive doubler (doubles death triggers) |
| Kill speed | Moderate-fast (2–3 turns from engine) | Fast (2–3 turns from engine) |
| Color access | UB (counters + card draw) | WB (removal + protection) |
| Sacrifice density | Light (Warren Soultrader, Ghoulcaller Gisa) | Heavy (6+ sac outlets, engine depends on it) |

Both decks drain opponents through creature deaths, but Teysa actively feeds the death trigger engine through sacrifice loops while Scarab God drains passively through upkeep triggers. Gray Merchant appears in both decks as a recurrable burst finisher. Different colors, different roles for tokens, no engine overlap beyond Gray Merchant.

| | Scarab God (Curse of the Scarab) | Sauron (The Dark Lord's Army) |
|---|---|---|
| Engine | Zombie horde (many creatures) | Single amass Army token |
| Token strategy | Go wide with 2/2 tokens | Go tall with one growing token |
| Commander resilience | Returns to hand on death | Ward (sacrifice legendary) |
| Drain source | Zombie count + Gray Merchant ETB | Ring temptation + Sheoldred |
| Colors | UB | UBR (red adds Jeska's Will, removal) |
| Board wipe recovery | Mass reanimation (Living Death) | Army reforms for free on any spell cast |

Both are "dark" Dimir-adjacent decks with drain elements, but the board strategies are opposite: Scarab God goes wide with many small creatures, Sauron goes tall with one large Army token. No engine overlap.

-----

## Maybeboard (Sideboard Cards)

The following cards are tracked as potential swaps or meta-dependent includes:

| Card | Role | Notes |
|---|---|---|
| Dread Summons | Mass mill + token generation | Each player mills X, create a 2/2 zombie for each creature milled. Scales with table's creature density. |
| Dreadhorde Invasion | Steady token generation | Creates a 1/1 Army token at upkeep (amass 1). Slow but consistent — survives board wipes as an enchantment. |
| Endless Ranks of the Dead | Exponential tokens | Half your zombie count as new tokens each upkeep. Win-more — devastating when ahead, useless when behind. |
| Fleshbag Marauder | Edict removal | Forces each player to sacrifice a creature on ETB. Recurrable via Scarab God, Reanimate. Hits hexproof/indestructible creatures. |
| Lich Lord of Unx | Alternate drain + mill | Tap {U}{B}: create a 1/1 zombie. Pay {U}{U}{B}{B}: each opponent loses X life and mills X cards, where X = zombies. Mana-intensive but provides both tokens and a direct kill. |
| Liliana, Death's Majesty | Planeswalker reanimation | +1 creates a 2/2 zombie and mills 2. -3 reanimates a creature from graveyard. -7 destroys all non-zombie creatures. All three modes serve the deck's plan. |
| Mindless Conscription | Enchantment token engine | Creates zombie tokens on draw triggers — pairs with Kindred Discovery for exponential growth. Risk of self-decking if unchecked. |
| Phyrexian Arena | Steady draw | One card per upkeep for 1 life. Consistent but slow. Cut for Necromancy in the current build. |
| Poppet Stitcher | Spellcast tokens | Creates 2/2 zombies on instant/sorcery casts. Transforms to make all tokens 3/3. Cut for Gray Merchant — deck runs too few instants/sorceries to trigger reliably. |
| Rot Hulk | Mass reanimation on ETB | When Rot Hulk enters, return X zombie creature cards from graveyard to the battlefield, where X = opponents. In a 4-player pod, that's 3 free reanimations. |
| Undead Alchemist | Mill-to-zombie conversion | Replaces zombie combat damage with mill; milled creatures become zombie tokens. Devastating against creature-heavy decks, useless against creatureless combo. |

-----

## Decklist (100 cards)

### Commander (1)

1 The Scarab God

### Game Changers (3)

1 Cyclonic Rift
1 Demonic Tutor
1 Fierce Guardianship

### Zombie Lords (7)

1 Cemetery Reaper
1 Death Baron
1 Diregraf Captain
1 Lord of the Accursed
1 Narfi, Betrayer King
1 Undead Warchief
1 Zombie Master

### Zombie Token Generators (4)

1 Diregraf Colossus
1 Ghoulcaller Gisa
1 Grave Titan
1 Wilhelt, the Rotcleaver

### Token Enchantments (2)

1 Crowded Crypt
1 Necroduality

### Drain / Damage Payoffs (5)

1 Gempalm Polluter
1 Gray Merchant of Asphodel
1 Lost Monarch of Ifnir
1 Plague Belcher
1 Shepherd of Rot

### Zombie Synergy Creatures (5)

1 Champion of the Perished
1 Cryptbreaker
1 Gravecrawler
1 Headless Rider
1 Noxious Ghoul

### Non-Zombie Creatures (1)

1 Mikaeus, the Unhallowed

### Sacrifice / Value (1)

1 Warren Soultrader

### Draw Engines (5)

1 Black Market Connections
1 Corpse Augur
1 Graveborn Muse
1 Kindred Discovery
1 Undead Augur

### Death-Trigger Draw (1)

1 Midnight Reaper

### Evasion (2)

1 Hordewing Skaab
1 Wonder

### Reanimation / Recursion (9)

1 Agadeem's Awakening
1 Buried Alive
1 Dread Return
1 Entomb
1 Living Death
1 Necromancy
1 Reanimate
1 Victimize
1 Zombie Apocalypse

### Cost Reduction (1)

1 Rooftop Storm

### Planeswalkers (1)

1 Liliana, Dreadhorde General

### Counterspells (3)

1 An Offer You Can't Refuse
1 Arcane Denial
1 Counterspell

### Free Interaction (1)

1 Force of Negation

### Removal (3)

1 Feed the Swarm
1 Go for the Throat
1 Rapid Hybridization

### Board Wipe (1)

1 Toxic Deluge

### Protection (1)

1 Lightning Greaves

### Draw Artifacts (2)

1 Skullclamp
1 Thought Vessel

### Mana Rocks (6)

1 Sol Ring
1 Arcane Signet
1 Dimir Signet
1 Fellwar Stone
1 Mind Stone
1 Talisman of Dominance

### Utility Lands (5)

1 Bojuka Bog
1 Cavern of Souls
1 Path of Ancestry
1 Reliquary Tower
1 Unholy Grotto

### Dual / Fetch Lands (9)

1 Drowned Catacomb
1 Exotic Orchard
1 Fetid Pools
1 Flooded Strand
1 Morphic Pool
1 Sunken Hollow
1 Tainted Isle
1 Watery Grave
1 Three Tree City

### Other Lands (3)

1 Command Tower
1 Underground River
1 Urborg, Tomb of Yawgmoth

### Basic Lands (18)

7 Snow-Covered Island
4 Snow-Covered Swamp
7 Swamp
