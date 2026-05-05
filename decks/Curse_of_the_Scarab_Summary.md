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

The deck floods the board with zombies through tribal synergy, token generation, and reanimation, then exploits zombie count for passive drain, card advantage, and lethal combat. Every zombie entering the battlefield simultaneously grows the army (Diregraf Colossus, Necroduality), replaces itself on death (Wilhelt, the Rotcleaver), triggers card draw (Kindred Discovery, Undead Augur), and increases the upkeep drain from The Scarab God.

### Layer 1 — Zombie Lords (6 pieces)

The deck runs a deep lord package that turns individually weak zombies into a lethal combat force:

- **Death Baron:** +1/+1 and deathtouch to all zombies and skeletons. Deathtouch makes every zombie token a credible blocker and forces unfavorable blocks from opponents.
- **Lord of the Accursed:** +1/+1 to other Zombies. {1}{B}, {T}: all Zombies gain menace until end of turn. Menace with a wide board is frequently unblockable.
- **Undead Warchief:** +2/+1 to zombies, zombie spells cost {1} less. The biggest stat boost in the package and the only cost reducer.
- **Cemetery Reaper:** +1/+1 to zombies, pay {2}{B} and tap to exile a creature card from a graveyard and create a 2/2 zombie token. Lord + graveyard hate + token generation on one card.
- **Zombie Master:** Gives all zombies swampwalk and "{B}: Regenerate this permanent." With Urborg, Tomb of Yawgmoth in play, swampwalk is unblockable. Regeneration protects against destroy-based removal and damage-based wipes.
- **Narfi, Betrayer King:** +1/+1 to snow and zombie creatures. Costs {3}{U}{B} but can return from graveyard to battlefield for {S}{S}{S} — self-recurring lord that doesn't need to be cast from hand.

With two lords in play, 2/2 zombie tokens become 4/4s. Three lords make them 5/5s or larger. Diregraf Captain is in the sideboard as a seventh lord and a death-trigger drain payoff.

**Mikaeus, the Unhallowed** functions as a pseudo-lord — he gives all non-Human creatures +1/+1 and undying. He's not a zombie himself, but the +1/+1 buff to the entire army is a lord-equivalent stat boost, and undying means every zombie comes back once after dying. This makes board wipes cost opponents two wipes to fully clear the board.

### Layer 2 — Zombie Token Generation (6 pieces)

- **Grave Titan:** Creates two 2/2 zombie tokens on ETB and on each attack. Six power plus four tokens over two turns. One of the highest-impact single cards in the deck.
- **Ghoulcaller Gisa:** {B}, {T}, sacrifice another creature: create X 2/2 zombies where X is the sacrificed creature's power. With a lord-pumped zombie, this converts one creature into many. Sacrificing Grave Titan (6 power) creates 6 zombies.
- **Diregraf Colossus:** Enters with +1/+1 counters equal to zombies in graveyard. Whenever you cast a zombie spell, create a tapped 2/2 zombie token. Snowballs rapidly — every zombie cast creates a free body (tapped, so it blocks the next turn but doesn't attack immediately).
- **Necroduality:** Whenever a nontoken zombie enters the battlefield under your control, create a token copy of it. Doubles every zombie cast. A second lord, a second Grave Titan, a second of anything.
- **Wilhelt, the Rotcleaver:** Whenever a zombie you control dies (if it didn't have decayed), create a 2/2 zombie with decayed. Also, at the beginning of your end step, sacrifice a zombie to draw a card. Replacement engine — every zombie death creates a new body.
- **Crowded Crypt:** Taps for {B}. Whenever a creature you control dies, put a corpse counter on Crowded Crypt. {4}{B}{B}, {T}, sacrifice it: create a 2/2 zombie token **with decayed** for each corpse counter. Tracks deaths throughout the game and converts them into a wide one-shot board — the decayed clause means the tokens self-sacrifice at end of combat when they attack, but they still trigger Plague Belcher, Wilhelt's replacement, and Scarab God's drain count for at least one upkeep before swinging.

### Layer 3 — Card Draw and Selection (6 pieces)

- **Kindred Discovery:** Whenever a zombie enters the battlefield or attacks, draw a card. In a zombie tribal deck, this draws 3–6 cards per turn cycle once the engine is running. The single strongest draw engine in the deck — if it resolves, the game is often over.
- **Skullclamp:** Equip a 1/1 (Stitcher's Supplier, Carrion Feeder pre-counters, Cryptbreaker, Gravecrawler) — the -1 toughness drops it to 0 toughness on equip and Skullclamp draws 2. Wilhelt's 2/2 decayed tokens become 3/1 when equipped, so they survive equip but enable a profitable swing-then-sacrifice draw line. Repeatable draw via the cheap one-drop zombies.
- **Graveborn Muse:** At your upkeep, draw X and lose X life, where X is the number of zombies you control. Powerful but dangerous — with 5+ zombies, the life loss adds up quickly. The Scarab God's drain on opponents partially offsets this.
- **Cryptbreaker:** {1}{B}, {T}, discard a card: create a 2/2 zombie token. Tap three untapped zombies: draw a card, lose 1 life. Early-game token generator that transitions to a draw engine once the board develops; the discard mode pairs with Bone Miser to recoup either a body, mana, or a card per activation.
- **Bone Miser:** Three triggers: discard a *creature* card → create a 2/2 zombie token; discard a *land* → add {B}{B}; discard a *noncreature, nonland* → draw a card. Pairs with Cryptbreaker (which discards) — every discard generates a body, mana, or a card depending on what was pitched. Also fuels the graveyard for reanimation.
- **Undead Augur / Midnight Reaper:** Whenever a zombie you control dies, draw a card and lose 1 life. Death-trigger draw that stacks with Wilhelt's replacement tokens. Two copies of this effect provide reliable draw through creature deaths.
- **Black Market Connections:** Steady incremental draw, Treasure, and token generation.

### Layer 4 — Reanimation, Recursion, and Tutoring (10 pieces)

- **Living Death:** Each player sacrifices all creatures, then returns all creature cards from their graveyard to the battlefield. In a deck designed to stock the graveyard (Buried Alive, Entomb, Stitcher's Supplier self-mill, natural creature deaths), this is a one-sided mass reanimation. The single most explosive card in the deck.
- **Agadeem's Awakening:** MDFC that enters as a tapped land or casts as a mass reanimation spell returning creatures with different mana values. Late-game, this is Living Death #2. Zero deckbuilding cost since it occupies a land slot.
- **Rot Hulk:** Menace. When Rot Hulk enters, return up to X target Zombie cards from your graveyard to the battlefield, where X equals the number of opponents. In a four-player pod, that's three free reanimations on a single ETB. Recurrable via Reanimate, Necromancy, or The Scarab God's activated ability for repeated mass reanimation. Replaces Zombie Apocalypse as the deck's asymmetric zombie-only mass reanimation.
- **Liliana, Death's Majesty:** Five-mana planeswalker ({3}{B}{B}). +1 creates a 2/2 zombie token and mills 2 — fuels both the board and the graveyard simultaneously. -3 reanimates a creature card **from your graveyard** (and that creature becomes a black Zombie in addition to its other types — so anything you reanimate counts toward Zombie tribal). -7 destroys all non-zombie creatures. All three modes serve the deck's plan; the +1/-3 axis is a self-sufficient reanimation engine that survives one round of removal.
- **Reanimate:** One mana to put any creature from any graveyard onto the battlefield. Life cost equal to its mana value is trivial at 40 life. Entomb + Reanimate on turn 2 = Grave Titan or Gray Merchant.
- **Necromancy:** Reanimation at flash speed. Deploy at end of turn or in response to an opponent's attack. Flash reanimation is uniquely powerful because it lets you "hold up interaction" while actually deploying threats. Bring back Gray Merchant at instant speed for a surprise drain.
- **Dread Return:** Reanimate a creature. Has flashback — sacrifice three creatures to cast from graveyard. With expendable zombie tokens, the flashback cost is trivial.
- **Victimize:** Sacrifice a creature, return two creature cards from graveyard to the battlefield. Net +1 creature, and the sacrificed creature triggers death payoffs.
- **Buried Alive / Entomb:** Tutor-quality graveyard setup. Buried Alive puts three creatures into the graveyard; Entomb puts one at instant speed for {B}. Both set up Living Death, Reanimate, Necromancy, Dread Return, Rot Hulk, Liliana DM's -3, and The Scarab God's activated ability. Entomb specifically enables turn-1 setup into turn-2 Reanimate — the fastest play the deck can make.
- **Stitcher's Supplier:** One-mana 1/1 zombie that mills 3 on ETB and again when it dies. Cheap, repeatable graveyard fill that turns on every reanimation spell in the deck. Pairs with Carrion Feeder as a free sac outlet to immediately trigger the death mill.
- **Demonic Tutor:** Finds whatever the deck needs for the current board state. Against graveyard hate: Feed the Swarm. Against combo: Fierce Guardianship or Counterspell. Against an open board: Living Death, Kindred Discovery, or Rooftop Storm. This is the single card that transforms the deck's inconsistency into precision.

### Layer 5 — Drain and Damage Acceleration (4 pieces)

Beyond The Scarab God's upkeep drain:

- **Gray Merchant of Asphodel:** Drains each opponent for your black devotion on ETB. In a deck with Death Baron ({B}{B}{B}), Undead Warchief ({2}{B}{B}), Liliana ({4}{B}{B}), Black Market Connections, and Phyrexian mana symbols throughout, devotion of 6–10 is routine. That's 6–10 life drained from each opponent on a single ETB — and you gain all of it. Recurrable via Reanimate, Necromancy, Victimize, Dread Return, or The Scarab God's activated ability for repeated burst drain. This is the deck's highest-impact single card for closing games.
- **Shepherd of Rot:** {T}: each player loses 1 life for each Zombie **on the battlefield** (yours plus any opponents'). Instant-speed activated ability, no mana cost. With 8 of your zombies on the battlefield, tapping Shepherd deals 8 to each player including you — combine with The Scarab God upkeep and Gray Merchant lifegain to net positive.
- **Gempalm Polluter:** Cycle {B}{B}: target player loses life equal to the number of Zombies on the battlefield. Instant speed, draws a card. Targets *one player* only (pick the lowest-life opponent), not each opponent — this is a focused finisher rather than a board-wide drain.
- **Plague Belcher:** ETBs by putting two -1/-1 counters on a creature you control (downside — pick a token, Carrion Feeder where the counters are absorbed alongside the +1/+1 ones, or a Mikaeus undying creature; never put on Gravecrawler/Stitcher's Supplier/Cryptbreaker, the -2/-2 will kill them). Then whenever **another** Zombie you control dies, **each opponent** loses 1 life — 3 across the table per death in a 4-player pod, doubled by Mikaeus's undying. The mainboard's only death-trigger drain payoff after Diregraf Captain moved to the sideboard — pairs with Carrion Feeder and Warren Soultrader as the engine for the deck's Rule 0 combo line.
- **Lost Monarch of Ifnir:** Afflict 3 on itself and all other Zombies. At the beginning of your second main phase, **if a player was dealt combat damage by a Zombie this turn**, mill three cards, then you may return a creature card from your graveyard to your hand. Once-per-turn delayed trigger (not per zombie hit), but afflict 3 punishes every blocked zombie regardless. Combat-driven self-mill plus recursion.

### Layer 6 — Sacrifice and Discard Outlets (3 pieces)

- **Carrion Feeder:** One-mana 1/1 zombie with a free sacrifice ability. Each zombie sacrificed grows it +1/+1 permanently. The free outlet is what makes the engine sing — sacrifice Stitcher's Supplier on ETB to mill 3, sacrifice Gravecrawler at instant speed for a Plague Belcher drain trigger, sacrifice tokens to threshold the graveyard for Living Death. Carrion Feeder enables most of the deck's death-trigger lines and the Rule 0 combo loop.
- **Warren Soultrader:** Pay 1 life, sacrifice another creature: create a Treasure. **No tap requirement and no summoning-sickness gate** — Soultrader can sacrifice on the turn it enters. Mana-positive sacrifice outlet that doubles as the Rule 0 combo's mana engine.
- **Cryptbreaker:** (Also listed under draw.) Tap and discard to create a 2/2 zombie. With Bone Miser in play, every discard adds {B} or draws a card — Cryptbreaker becomes a one-card engine that produces a token, draws or ramps, and fuels the graveyard simultaneously.

### The Play Pattern

Turn 1–2: Deploy a 1-drop zombie (Gravecrawler, Carrion Feeder, Stitcher's Supplier, Cryptbreaker) or a mana rock. Stitcher's Supplier on turn 1 immediately mills 3 cards into the graveyard, setting up turn-2 Reanimate or Entomb-into-Reanimate for an early Grave Titan or Gray Merchant. Turn 3–4: Deploy zombie lords and token generators. Board grows to 3–5 zombies. When Plague Belcher comes down, ETB it onto a token, Carrion Feeder (the -1/-1 counters cancel some of its accumulated +1/+1 counters but the body survives), or a Mikaeus undying creature — never put the -2/-2 onto a 1-toughness zombie like Gravecrawler, Stitcher's Supplier, or Cryptbreaker, since it will kill them on the spot. Turn 5: Cast The Scarab God. Upkeep drain begins — 3–5 per opponent. Scry 3–5 sculpts draws to find Kindred Discovery, mass reanimation, or Gray Merchant. Turn 6–8: Deploy Kindred Discovery or Rooftop Storm to accelerate. Board grows to 8+ zombies. Drain hits 8+ per opponent per upkeep, plus combat damage with lord-pumped creatures. Demonic Tutor finds the closer that matches the board state. If opponents wipe the board, Living Death, Agadeem's Awakening, or Rot Hulk rebuild instantly; Liliana DM's -3 reanimates a key piece even through graveyard pressure. Cyclonic Rift clears opponents' boards for a lethal alpha strike. Turn 7–9: Accumulated drain, combat damage, Gray Merchant recursion, and finishers (Gempalm Polluter, Shepherd of Rot) close the game.

-----

## Kill Lines

### Line 1 — The Scarab God Upkeep Drain (Primary)

The passive kill. Each upkeep, every opponent loses life equal to your zombie count. This requires no mana, no attack, no tap — it just happens. With 8 zombies, that's 8 damage to each opponent per upkeep. Five upkeeps from 40 life is lethal, but parallel damage from combat, Shepherd of Rot, and Gempalm Polluter shortens this to 3–4 turn cycles.

The drain stacks with Shepherd of Rot (tap: each player loses 1 per Zombie on the battlefield) and Gempalm Polluter (cycle: target player loses 1 per Zombie on the battlefield). In a single turn cycle with 8 zombies, the deck can deal: 8 (Scarab God upkeep, each opponent) + 8 (Shepherd of Rot, each player including you) = 16 across the table per opponent, plus a focused 8 onto the lowest-life opponent via Gempalm = 24 to that opponent. Plus combat damage. Two turn cycles of stacked drain from a developed board is lethal.

### Line 2 — Gray Merchant Burst Drain (Fastest Non-Combo Kill)

Gray Merchant of Asphodel drains each opponent for your black devotion on ETB. With devotion 8 (common with 2–3 black permanents and Gary's own {3}{B}{B} contributing 2), that's 8 from each opponent and 24 gained. Reanimate it for {B} (lose 5 life, net +19 with the drain). Necromancy it back at flash speed. Victimize it by sacrificing a token. Each recurrence drains 6–10 per opponent.

Two Gray Merchant ETBs in a game = 16–20 drain per opponent. Combined with The Scarab God's passive upkeep drain, this often represents 60–80% of an opponent's life total. Demonic Tutor can find Gray Merchant, and Entomb + Reanimate can deploy it as early as turn 2.

### Line 3 — Lord-Pumped Zombie Combat + Cyclonic Rift

With two lords in play, 2/2 zombie tokens are 4/4s. An army of five 4/4 zombies deals 20 damage per attack. Evasion comes from multiple sources: Lord of the Accursed grants menace, Hordewing Skaab grants flying to all zombies, Wonder grants flying from the graveyard, Zombie Master grants swampwalk (unblockable with Urborg).

Cyclonic Rift (overloaded for 7 mana) bounces all opponents' nonland permanents to their hands — creatures, artifacts, enchantments, everything. A developed zombie board + overloaded Rift = lethal alpha strike into empty defenses. Demonic Tutor can find Cyclonic Rift when the board is ready for the kill.

Lost Monarch of Ifnir adds afflict 3 to the entire zombie army, punishing blocking. An opponent choosing to block five zombies takes 15 afflict damage regardless of how combat resolves.

### Line 4 — Aristocrats Drain (Death Triggers)

Plague Belcher drains **each opponent** for 1 life per zombie death — 3 across the table per death in a 4-player pod. Carrion Feeder and Warren Soultrader provide free or near-free sacrifice outlets, and Ghoulcaller Gisa converts a single creature into many tokens to feed the engine. Mikaeus's undying means each zombie dies twice before staying dead, doubling the death triggers. Diregraf Captain in the sideboard would double the per-death drain to 2 per opponent (6 across the table) if the meta favored it.

### Line 5 — Mass Reanimation into Burst Drain

Buried Alive or Entomb stocks the graveyard with high-impact zombies (Grave Titan, Gray Merchant, Rot Hulk). Living Death, Agadeem's Awakening, or a Rot Hulk ETB brings them all back simultaneously. A single Living Death resolving with 8+ zombies in the graveyard creates a board that threatens lethal drain on the next upkeep — and if Gray Merchant is among the returned creatures, the drain starts immediately on ETB. Rot Hulk specifically returns a zombie per opponent on ETB, making it a self-contained 4-for-1 in any pod.

This line functions as a recovery kill — the deck is at its most dangerous immediately after a board wipe, when both graveyards are full and Living Death creates a massive asymmetry. Stitcher's Supplier on the way out also mills 3 fresh cards into the yard, often deepening the pile mid-recovery.

### Line 6 — Rooftop Storm Explosion

Rooftop Storm makes all zombie spells cost {0}. With Necroduality doubling every zombie cast and Diregraf Colossus creating additional tokens per cast, emptying a hand of 4 zombies creates 4 + 4 copies + 4+ Colossus tokens = 12+ zombies in a single turn. Kindred Discovery draws a card per zombie entering, refueling the hand immediately. The following upkeep, Scarab God drains 12+ from each opponent.

### Line 7 — Warren Soultrader Loop (Rule 0)

Warren Soultrader + Gravecrawler + Plague Belcher is a three-card mana-neutral loop. Sacrifice Gravecrawler to Warren Soultrader (create Treasure, lose 1 life) → spend Treasure to recast Gravecrawler for {B} → repeat. Each cycle drains an opponent for 1 via Plague Belcher's death trigger. Self-limiting by your life total — at 40 life, deals up to 39 damage. Carrion Feeder is a free alternate outlet for the same loop, but without a Treasure-style mana source the loop becomes mana-limited rather than indefinite. Flagged for pod Rule 0 discussion.

-----

## Conversion Check Breakdown

### Core Loop: 5/5

The loop is "deploy zombies → zombies generate more zombies → zombie count drives drain, draw, and combat." 24+ cards directly serve the engine: 4 token generators, 2 token enchantments, 8 reanimation/recursion spells, Rot Hulk's ETB mass reanimation, Liliana Death's Majesty as a self-contained token+reanimation engine, Rooftop Storm cost reduction, two free sacrifice outlets (Carrion Feeder, Warren Soultrader), Stitcher's Supplier as graveyard fuel, Bone Miser as a discard payoff, and Gravecrawler/Narfi as self-recurring zombies. On top of that engine, 6 lords and Mikaeus multiply combat output, 5 drain payoffs and 6 draw engines convert the engine's output into wins, and Demonic Tutor finds whichever piece is missing. Every creature in the deck except Wonder and Mikaeus is a zombie or creates zombies.

The commander is the primary drain payoff, but the 99 alone is unmistakably a zombie tribal deck — cover the commander and the identity is immediately obvious from the lord density, death triggers, and tribal-specific spells.

**Checkpoint:** Cover the commander. 6 lords, Mikaeus, Kindred Discovery, Necroduality, Rooftop Storm, Living Death, Rot Hulk, Buried Alive, 15+ zombie creatures. The strategy is unmistakable.

### Kill Reliability: 4/5

Seven named closing lines spanning Scarab God upkeep drain, Gray Merchant burst ETB, lord-pumped combat with Cyclonic Rift, aristocrats death triggers (Plague Belcher), mass reanimation into burst drain, Rooftop Storm explosion, and the Warren Soultrader Rule 0 loop. Gray Merchant's recurrable ETB removes 15–30% of each opponent's life total per resolution. Cyclonic Rift creates deterministic lethal alpha strikes from developed boards. Demonic Tutor finds whichever closer matches the current board state.

The fastest reliable kill from engine-online (5+ zombies, Scarab God in play) is 2–3 turns through Gray Merchant recursion plus stacked drain and combat. Stitcher's Supplier on turn 1 plus Entomb + Reanimate on turn 2 enables a turn-2 Grave Titan or Gray Merchant — the deck's fastest opening. Carrion Feeder as a free sac outlet adds a new instant-speed line: hold up B, sacrifice Gravecrawler at end of turn for a Plague Belcher death trigger, recast for {B} next turn.

The cut of Diregraf Captain to the sideboard halved the per-death drain output (now 1 per zombie death from Plague Belcher only, vs. 2 with both). The aristocrats kill line is materially slower than before, but the other six lines are unchanged or improved (Rot Hulk replaces Zombie Apocalypse with ETB tempo and Scarab God recurrence; Liliana DM provides a fourth reanimation axis). Net: the line that got slower wasn't the primary one.

All kill lines still depend on the shared resource of zombie/creature count on the battlefield — a board wipe weakens everything simultaneously. This structural dependency on a single resource type is what prevents a 5. But Demonic Tutor's ability to find mass reanimation (Living Death, Agadeem's Awakening, Rot Hulk, Liliana DM) after a wipe means the recovery-into-kill line is reliably accessible rather than draw-dependent.

**Checkpoint:** Engine-online, 8 zombies, Scarab God in play, Gray Merchant in graveyard. Upkeep drains 8 to each opponent, Reanimate Gray Merchant for 8+ devotion drain to each opponent, Shepherd of Rot drains 8 to each player. That's 24+ to each opponent in a single turn cycle. Lethal in one cycle if devotion is high enough.

### Durability: 4/5

The Scarab God's death trigger is the deck's best structural advantage. When The Scarab God dies, it returns to your hand — not the command zone. No commander tax accumulates from death-based removal. Only exile effects permanently deal with it.

Beyond the commander, the deck has layered recovery:

- **Mass reanimation (3 pieces + 1 ETB):** Living Death and Agadeem's Awakening reanimate everything from the graveyard. Rot Hulk's ETB returns one zombie per opponent — equivalent to a small mass reanimation, and recurrable through The Scarab God's activated ability. Liliana, Death's Majesty's -3 is a fourth, planeswalker-based reanimation source. Multiple options means you're likely to have access to at least one after a wipe.
- **Targeted reanimation (4 pieces):** Reanimate, Necromancy (flash speed), Dread Return (flashback from GY), Victimize. Deep targeted reanimation means every key creature lost can be recovered.
- **Self-recurring creatures:** Gravecrawler returns from graveyard for {B} with any zombie in play. Narfi returns from graveyard for {S}{S}{S}. These restart the engine without requiring reanimation spells.
- **Undying (Mikaeus):** Every non-Human creature comes back once after dying with a +1/+1 counter. Board wipes cost opponents two wipes to fully clear.
- **Death replacement:** Wilhelt creates a 2/2 decayed replacement zombie on each non-decayed zombie death — 1-for-1 removal trades a creature for a token rather than clearing a slot. Headless Rider in the sideboard would stack with this for two replacement tokens per death.
- **Tutor recovery:** Demonic Tutor finds the right recovery tool for the situation — Living Death after a wipe, Feed the Swarm against Rest in Peace, Fierce Guardianship to protect against the next wipe.

Doesn't reach 5 because graveyard hate cripples multiple recovery lines simultaneously. Rest in Peace, Leyline of the Void, and Dauthi Voidwalker shut off the entire reanimation package, Gravecrawler, Narfi, and The Scarab God's activated ability. The deck has Feed the Swarm and counterspells to answer these, and Demonic Tutor can find Feed the Swarm, but a resolved Rest in Peace before the deck finds an answer is still devastating.

**Checkpoint:** Cyclonic Rift on turn 7. Scarab God returns to hand (death trigger). Replay for 5 mana next turn. Demonic Tutor for Living Death, Rot Hulk, or Agadeem's Awakening. Full board recovery in 1–2 turns.

### Interaction Profile: 4/5

13 interaction pieces:

- **Free counterspells (2):** Fierce Guardianship (free with Scarab God in play), Force of Negation (exile a blue card from hand; the draw engines provide fuel). Two free counterspells completely solve the develop-vs-hold-up tension — cast Rooftop Storm or Kindred Discovery on your turn and still threaten to stop a combo attempt.
- **Paid counterspells (3):** Counterspell, An Offer You Can't Refuse, Arcane Denial.
- **Asymmetric board wipe (1):** Cyclonic Rift — overloaded, bounces all opponents' nonland permanents. The single most impactful interaction spell in Commander.
- **Board wipe (1):** Toxic Deluge.
- **Creature removal (3):** Go for the Throat, Rapid Hybridization, Feed the Swarm (also hits enchantments).
- **Pseudo-wipe (1):** Noxious Ghoul — gives all non-zombies -1/-1 whenever a zombie enters. With Necroduality or Grave Titan creating multiple zombies in one turn, this is a one-sided board wipe.
- **Planeswalker removal (1):** Liliana, Dreadhorde General — her -4 forces **each player** (including you) to sacrifice two creatures of their choice. Net asymmetric in this deck because the deck deploys throwaway zombie tokens that absorb the cost cheaply.
- **Graveyard hate (1):** Bojuka Bog — exiles a target opponent's graveyard.

Five counterspells with two free ones is a meaningful stack presence. The deck can now protect its combo turns (Rooftop Storm, Living Death) while still developing the board. Cyclonic Rift adds an asymmetric reset that doubles as a kill enabler. Demonic Tutor can find whichever interaction piece the situation demands.

Doesn't reach 5 because Feed the Swarm remains the only answer to enchantments, and it's sorcery speed. A resolved Rest in Peace or opposing Rhystic Study can only be countered on the stack or removed by this single card. Dimir's structural inability to handle enchantments is the permanent ceiling on this axis. 12+ interaction pieces is nominally a 5 count, but the enchantment blindspot and the tempo-negative counters (Arcane Denial gives opponent cards, An Offer gives Treasures) keep the quality at 4.

**Checkpoint:** Opponent is about to combo off. You have Fierce Guardianship or Force of Negation available at no mana cost. The combo is stopped. Your zombie board survives. You untap and drain.

### Total: 17/20 — Structurally excellent. Pilot skill is the main variable.

Re-audited 2026-04-29 after the Diregraf Captain / Headless Rider / Champion of the Perished / Zombie Apocalypse / Thought Vessel cut and the Bone Miser / Carrion Feeder / Stitcher's Supplier / Liliana DM / Rot Hulk / Polluted Delta inclusion. Same 5/4/4/4 = 17/20 as the prior build. The swap traded one death-trigger drain payoff (Diregraf Captain) and one death-replacement zombie (Headless Rider) for cheaper graveyard fuel (Stitcher's Supplier), a free sac outlet (Carrion Feeder), a discard payoff (Bone Miser), a fourth reanimation axis (Liliana DM), and a creature-based mass reanimation (Rot Hulk) — net lateral, with marginal gains on early-game speed and post-wipe recovery offsetting losses on the aristocrats kill line.

Re-audited 2026-05-05: documentation pass corrected ~15 card-text errors across the layer descriptions and kill lines (Bone Miser triggers, Plague Belcher's "each opponent" drain and -1/-1 ETB downside, Gempalm Polluter's correct cycle cost and target-player-only drain, Liliana DM's "your graveyard" reanimation, Liliana DG's "each player" -4, Skullclamp's interaction with 2/2 Wilhelt tokens, Cryptbreaker and Warren Soultrader and Ghoulcaller Gisa cost text, Lost Monarch trigger timing, Crowded Crypt decayed tokens, Rot Hulk's menace and "up to X" reanimation, Lord of the Accursed activation cost, Diregraf Colossus tapped tokens, Shepherd of Rot's "battlefield" count). Also swapped Path of Ancestry → Tainted Isle: Path's scry trigger never fires (commander is "God," no other Gods in 99) so it was a tapped Command Tower; Tainted Isle ETBs untapped, taps for {C} or {U}/{B} (the swamp condition is trivially met with 11 Swamps + Urborg + Watery Grave/Sunken Hollow). Score holds at 5/4/4/4 = 17/20 — the corrected math tightens the descriptions but no individual axis breaks; Gray Merchant burst + Scarab God upkeep still carry Kill Reliability at 4.

-----

## Expected Kill Window

**Goldfish: T7–9.** Stitcher's Supplier on turn 1 dumps 3 cards into the graveyard immediately; Entomb + Reanimate on turn 2 brings back Grave Titan or Gray Merchant. Scarab God typically resolves turn 5. Board grows to 8+ zombies by turn 6–7 with token generators. Demonic Tutor finds the right closer. Gray Merchant recursion or stacked drain + combat closes by turn 7–9 uncontested.

**Through interaction: T9–12.** A board wipe on turn 6–7 resets zombie count. Recovery takes 1–2 turns (Demonic Tutor finds mass reanimation; Living Death, Agadeem's Awakening, Rot Hulk's ETB, and Liliana DM's -3 are four distinct reanimation axes). Fierce Guardianship and Force of Negation protect key turns without mana investment. Cyclonic Rift creates lethal alpha strikes that bypass normal combat math. Games against interaction-heavy pods close by turn 9–12.

The 2–3 turn gap between goldfish and through-interaction is held tight by free counterspells protecting key development turns and Demonic Tutor ensuring the right recovery tool is available post-wipe.

-----

## Bracket 3 Compliance

**Game Changers (3 of 3 used):**
1. **Cyclonic Rift** — asymmetric board wipe (overload bounces all opponents' nonland permanents)
2. **Demonic Tutor** — unrestricted tutor (find any card in library)
3. **Fierce Guardianship** — free counterspell with commander in play

All three GC slots are occupied — no further Game Changers can be added without a swap.

**Notable non-GC power cards:** Force of Negation, Kindred Discovery, Rooftop Storm, Living Death, Necroduality, Skullclamp, Gray Merchant of Asphodel, Reanimate, Necromancy, Entomb, Mikaeus the Unhallowed, Liliana Dreadhorde General, Liliana Death's Majesty, Rot Hulk, Toxic Deluge, Buried Alive, Agadeem's Awakening.

**Infinite combos:** Warren Soultrader + Gravecrawler + Plague Belcher forms a three-card combo loop. Sacrifice Gravecrawler to Warren Soultrader (create a Treasure, lose 1 life) → spend the Treasure to recast Gravecrawler from the graveyard for {B} → Plague Belcher drain trigger → repeat. Each cycle drains a target opponent for 1. The loop is self-limiting by your life total — each cycle costs you 1 life, so you can loop as many times as you have life points minus 1. At 40 life, this deals up to 39 damage. Carrion Feeder is a free alternate sac outlet but without a Treasure-style mana source the loop becomes mana-limited. This should be flagged for pod Rule 0 discussion per B3 guidelines, as it is a three-card combo that can assemble naturally. Demonic Tutor could find the missing piece, but the loop doesn't consistently assemble before turn 6.

**Extra turns:** None.

**Mass land denial:** None.

-----

## Pod Fit

The zombie tribal archetype has distinctive pod characteristics:

1. **Grinds through attrition.** Board wipes against this deck are often counterproductive — they stock the graveyard for Living Death, Agadeem's Awakening, Rot Hulk, Liliana DM's -3, and The Scarab God's activated ability. Mikaeus's undying means the first wipe doesn't even fully clear the board. Opponents who wipe repeatedly may be helping the zombie player more than hurting them.
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
| Sacrifice density | Moderate (Carrion Feeder, Warren Soultrader, Ghoulcaller Gisa) | Heavy (6+ sac outlets, engine depends on it) |

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
| Champion of the Perished | One-drop counter accumulator | +1/+1 counter whenever a zombie enters under your control. Cut for Carrion Feeder as the preferred one-drop — Carrion Feeder is a free sac outlet plus a counter accumulator. |
| Diregraf Captain | Lord + death-trigger drain | +1/+1 to zombies, drains 1 from target opponent per zombie death. Stacks with Plague Belcher for 2 drain per death. Bring in against decks that don't run early board wipes — pairs into the Warren Soultrader Rule 0 line. |
| Dread Summons | Mass mill + token generation | Each player mills X, create a 2/2 zombie for each creature milled. Scales with table's creature density. |
| Dreadhorde Invasion | Steady token generation | Creates a 1/1 Army token at upkeep (amass 1). Slow but consistent — survives board wipes as an enchantment. |
| Fleshbag Marauder | Edict removal | Forces each player to sacrifice a creature on ETB. Recurrable via Scarab God, Reanimate. Hits hexproof/indestructible creatures. |
| Headless Rider | Death replacement | Whenever a non-token zombie dies, create a 2/2 zombie token. Stacks with Wilhelt for two replacement tokens per death. Bring in against creature-removal-heavy metas. |
| Lich Lord of Unx | Alternate drain + mill | Tap {U}{B}: create a 1/1 zombie. Pay {U}{U}{B}{B}: each opponent loses X life and mills X cards, where X = zombies. Mana-intensive but provides both tokens and a direct kill. |
| Thought Vessel | Ramp + no max hand | Two-mana colorless rock that lifts the hand-size cap. Cut for graveyard fillers; bring in if the deck is leaning harder on Necropotence-style draw. |
| Zombie Apocalypse | Asymmetric mass reanimation | Return all zombies from your graveyard, destroy all humans. Replaced in main by Rot Hulk's ETB reanimation, but a strong sideboard option against decks where Rot Hulk's mana cost is prohibitive. |

-----

## Decklist (100 cards)

### Commander (1)

1 The Scarab God

### Game Changers (3)

1 Cyclonic Rift
1 Demonic Tutor
1 Fierce Guardianship

### Zombie Lords (6)

1 Cemetery Reaper
1 Death Baron
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

1 Bone Miser
1 Cryptbreaker
1 Gravecrawler
1 Noxious Ghoul
1 Stitcher's Supplier

### Non-Zombie Creatures (1)

1 Mikaeus, the Unhallowed

### Sacrifice / Value (2)

1 Carrion Feeder
1 Warren Soultrader

### Mass Reanimation Creature (1)

1 Rot Hulk

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

### Reanimation / Recursion (8)

1 Agadeem's Awakening
1 Buried Alive
1 Dread Return
1 Entomb
1 Living Death
1 Necromancy
1 Reanimate
1 Victimize

### Cost Reduction (1)

1 Rooftop Storm

### Planeswalkers (2)

1 Liliana, Death's Majesty
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

### Draw Artifacts (1)

1 Skullclamp

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
1 Reliquary Tower
1 Tainted Isle
1 Unholy Grotto

### Dual / Fetch Lands (9)

1 Drowned Catacomb
1 Exotic Orchard
1 Fetid Pools
1 Flooded Strand
1 Morphic Pool
1 Polluted Delta
1 Sunken Hollow
1 Watery Grave
1 Three Tree City

### Other Lands (3)

1 Command Tower
1 Underground River
1 Urborg, Tomb of Yawgmoth

### Basic Lands (18)

7 Snow-Covered Island
2 Snow-Covered Swamp
9 Swamp
