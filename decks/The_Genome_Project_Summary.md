# Deck 6 — The Genome Project

**Commander:** Kuja, Genome Sorcerer ({2}{B}{R}, 3/4 Human Mutant Wizard) // Trance Kuja, Fate Defied (4/6 Avatar Wizard)  
**Colors:** Rakdos (BR)  
**Archetype:** Wizard-token spellslinger burn  
**Bracket:** 3 (3 Game Changers: Necropotence, Jeska's Will, Underworld Breach)  
**Conversion Check:** 15/20 (4/4/3/4)  
**Kill Window:** Goldfish: T7–9 · Through interaction: T9–12 *(unverified — no lab run; flagged 2026-06-10 per `proposals/Framework_Clock_Gap_2026-06-09.md`)*  
**Decklist file:** `decks/the-genome-project-20260510.txt`  
**Card text verified:** 2026-05-10 — every engine piece, multiplier, mana source, removal, and reskin lookup'd via `card_lookup.py`. Drift corrections applied below; see Changelog.

-----

## Commander Rules Text

**Front — Kuja, Genome Sorcerer** ({2}{B}{R}, 3/4, Legendary Creature — Human Mutant Wizard)

At the beginning of your end step, create a tapped 0/1 black Wizard creature token with "Whenever you cast a noncreature spell, this token deals 1 damage to each opponent." Then if you control four or more Wizards, transform Kuja.

**Back — Trance Kuja, Fate Defied** (4/6, Legendary Creature — Avatar Wizard, BR color indicator)

Flare Star — If a Wizard you control would deal damage to a permanent or player, it deals double that damage instead.

**Key rulings:**

- Kuja himself is a Wizard and counts toward the four-Wizard threshold.
- The Wizard tokens' triggered ability resolves *before* the spell that caused it to trigger. The damage happens even if the spell is countered.
- Trance Kuja's Flare Star is a replacement effect (not triggered), so it doubles all Wizard damage including combat damage from Wizard creatures.
- The doubled damage retains its original source — Trance Kuja doesn't become the source of the damage.

-----

## What the Deck Does

Kuja builds an army of 0/1 Wizard tokens that ping each opponent for 1 whenever you cast a noncreature spell. The commander produces one token per end step automatically. Once you control four Wizards (including Kuja), he transforms into Trance Kuja, doubling all Wizard damage. The deck then chains cheap noncreature spells — draw, rituals, cantrips — to deal escalating burn damage to the entire table simultaneously.

The damage math scales multiplicatively. With four Wizard tokens and Trance Kuja, each noncreature spell deals 4 × 2 = 8 to each opponent. Add Harmonic Prodigy (doubles Wizard triggered abilities) and each spell deals 4 × 2 triggers × 2 Trance = 16 per opponent. Add City on Fire (which triples *all* damage from sources you control — combat or noncombat) and a single spell deals 48 to each opponent. The deck's ceiling is absurd; the challenge is surviving long enough to assemble the pieces.

### The Core Loop

1. **Cast Kuja turn 4.** End step: create a Wizard token.
2. **Accumulate Wizards** over 2–3 end steps, supplemented by Vivi's Persistence, Circle of Power, Cornered by Black Mages, and Black Mage's Rod.
3. **Transform Kuja** once you control 4+ Wizards (Kuja counts). All Wizard damage now doubled.
4. **Go off:** Generate mana via Birgi, Bayo/Electro, Storm-Kiln Artist, Jeska's Will, or Mana Geyser. Chain noncreature spells. Each spell triggers every Wizard token simultaneously. Multipliers (Harmonic Prodigy, Roaming Throne, City on Fire) push individual spells into lethal range.
5. **Close the game** in one explosive turn or finish with Exsanguinate, Aetherflux Reservoir, or Peer into the Abyss refueling another spell chain.

### Kill Lines

**Line 1 — Wizard Ping Storm (primary):** Trance Kuja + 4 Wizard tokens = 8 damage per opponent per noncreature spell. Five spells kills the table. With Birgi refunding {R} per spell and Storm-Kiln Artist generating Treasures, chaining five cheap spells is achievable in a single turn.

**Line 2 — Multiplier Stack:** Trance Kuja + Harmonic Prodigy (or Roaming Throne) + 3–4 Wizard tokens = 12–16 damage per spell per opponent. Three spells kills the table. Adding City on Fire to any multiplier configuration creates one-spell lethality.

**Line 3 — Bonus Round / Mizzix's Mastery / Underworld Breach Graveyard Storm:** Bonus Round doubles every instant and sorcery for the rest of the turn. Each copy also triggers Wizard pings. Dawn Warriors' Legacy (Mizzix's Mastery) overloaded replays every instant and sorcery from the graveyard at once — each cast triggers all Wizards. Underworld Breach gives every nonland card in the graveyard escape (mana cost + exile 3 other GY cards) for a turn — slower per-spell than Mastery but more flexible (you can pace the chain, hold up reactive escapes, and the exile cost itself fuels other graveyard payoffs). Storm-Kiln Artist Treasures pay the escape costs; Birgi rebates a {R} per cast. Combined with Trance Kuja, any of these three is often lethal from a stocked graveyard.

**Line 4 — Aetherflux Reservoir:** Chain spells to gain escalating life (1st spell = 1 life, 2nd = 2, etc.). Reach 50+ life and pay 50 to laser a player. This line operates independently of Wizard tokens and serves as a backup when the token board has been swept.

**Line 5 — Exsanguinate:** After generating large mana via Mana Geyser (multiplayer = massive output), Neheb (post-combat mana from ping damage), or Jeska's Will, fire a lethal Exsanguinate at the table.

**Line 6 — Peer into the Abyss → Chain:** Draw half your library. Cast everything cheap to trigger Wizard pings. This is the reload line when the hand is depleted but the board is set.

### The Multiplier Web

The deck stacks damage multipliers that interact multiplicatively:

| Piece | Effect | Type |
|---|---|---|
| Trance Kuja | All Wizard damage ×2 | Replacement effect |
| Harmonic Prodigy | Wizard / Shaman triggered abilities trigger an additional time (note: "another Wizard" — does not double its own prowess) | Static ability |
| Roaming Throne (Wizard) | Triggered abilities of *other* creatures of the chosen type trigger an additional time | Static ability |
| City on Fire | **All damage from sources you control ×3** (combat included). Two copies = ×9, three = ×27. | Replacement effect |

Harmonic Prodigy and Roaming Throne are additive with each other (both double triggers — having both means triple triggers), but multiplicative with Trance Kuja and City on Fire. Worst-case realistic stack: Trance Kuja + 1 trigger doubler + 3 tokens = 12 per spell per opponent. Best-case: Trance + Prodigy + City + 4 tokens = triple triggers × ×2 × ×3 = ×18 per token = 72 per spell per opponent. One spell kills the table twice over.

### Wizard Producer Layer — Pilot Notes

The 7 Wizard producers (beyond Kuja and Stormsplitter copies) each have non-obvious mechanics worth knowing at the table:

- **Black Mage's Rod** ({1}{B} Equipment, Job Select): Creates a **1/1 colorless Hero token** on ETB and auto-attaches. The equipped creature gets +1/+0, gains the noncreature-spell ping ability ("deals 1 damage to each opponent"), AND becomes a **Wizard in addition to its other types**. The token isn't a Wizard until equipped — but once equipped, it counts toward the 4-Wizard transform threshold *and* it pings.
- **Black Waltz No. 3** ({2}{B}{R}, 2/2 Wizard with flying + deathtouch): Pings each opponent for **2** (not 1) per noncreature spell. Highest per-spell damage of any single Wizard in the deck. Trance Kuja doubles each instance to 4. With Prodigy + Throne stacking to 3 trigger instances per spell, that's 2 base × 3 triggers × 2 Trance = **12 per spell from Black Waltz alone** to each opponent. Add City on Fire for ×3 = 36 per spell. He's a target — protect him.
- **Circle of Power** ({3}{B} sorcery): Draws 2 cards, lose 2 life, creates a 0/1 Wizard token, *and* gives all your Wizards +1/+0 lifelink until end of turn. The lifelink mode is a one-turn life-buffer for combo turns.
- **Cornered by Black Mages** ({1}{B}{B} sorcery): Edict + Wizard token. Removes a hexproof/indestructible creature *and* adds to the token count. Dual-role.
- **Coruscation Mage** ({1}{R}, 2/2 Otter Wizard with Offspring {2}): Pings 1 per noncreature spell. **The Offspring token is a 1/1 copy with the same ping ability** (Offspring copies printed text). Casting for {3}{R} = two pingers in one card.
- **Vivi's Persistence** ({1}{R} instant): Creates a 0/1 Wizard token. **Recursion clause is "Whenever your commander enters or attacks, you may pay {2}"** — so the recursion is gated on Kuja entering (good — recasts after removal) or attacking (less common — Kuja prefers main-phase storming). Active recursion piece, not auto-recur.
- **Stormsplitter** ({3}{R}, 1/4 Otter Wizard with haste): Creates a 1/4 Otter Wizard **token copy of itself** on each instant/sorcery cast. The copies inherit the trigger, so they self-replicate exponentially in a chain. Each Stormsplitter token is a Wizard (counts toward Trance threshold) but does NOT have the ping ability — its damage is combat-only. Categorized as a Wizard Producer (not a Damage Multiplier) because the copies generate Wizards, not pings.

**Hidden Wizard producers / value modes:**

- **Lindblum, Industrial Regency** is in the lands section, but its DFC face is **Mage Siege** ({2}{R} Adventure instant): "Create a 0/1 Wizard token with the ping ability." Cast Lindblum as the Adventure first for a Wizard, then play the (tapped) land later from exile. Effectively a land + Cornered-style Wizard producer hybrid.
- **Midgar, City of Mako** is the analogous BR card: DFC face **Reactor Raid** ({2}{B} Adventure sorcery): "You may sacrifice an artifact or creature. If you do, draw two cards." Hidden 2-mana Deadly-Dispute equivalent in a land slot.
- **Black Market Connections — Hire a Mercenary mode:** Creates a 3/2 colorless **Shapeshifter creature token with changeling**. Changeling is *every creature type, including Wizard*. So this mode counts toward the 4-Wizard transform threshold. (Also adds a 3/2 body, which Trance Kuja then doubles to 6/4 effective combat damage.) Often the right pick over Sell Contraband / Buy Information when you're 1 Wizard short of transforming.

### What Makes It Distinct

- **Not combat-phase spellslinger** (like Azula) — Kuja's engine is main-phase storm, not combat-phase doubling. Spells are cast for their own value, not to exploit a copy trigger.
- **Not aristocrats** (like Teysa) — the Wizard tokens are damage sources, not sacrifice fodder. You want them alive, not dead.
- **Not traditional burn** — damage comes from triggered abilities on tokens, not from the spells themselves. A Faithless Looting deals 8 damage to each opponent with Trance Kuja and 4 Wizards.
- **Not amass/drain** (like Sauron) — you control many small tokens, not one big one. The Army reforms for free; Wizard tokens do not.

-----

## Conversion Check Assessment: 15/20

### Core Loop — 4/5

The engine is immediately recognizable: Wizard tokens + noncreature spell chains + damage multipliers. 26+ cards directly serve this loop across wizard production (7 sources beyond the commander, plus Lindblum's Adventure side and Black Market Connections's Mercenary mode as hidden producers), mana generation (5 enablers), damage multiplication (3 pieces), and spell copying/replay (5 pieces). The commander is central — Kuja both produces the tokens and provides the key damage doubler on his back face.

Docked from 5 because Kuja is a hard dependency. Without the commander, the supplementary wizard-makers (Vivi's Persistence, Circle of Power, Cornered by Black Mages, Black Mage's Rod) produce tokens slowly and piecemeal. The Trance transformation requires 4+ Wizards including Kuja, which means 3 end steps minimum plus Kuja surviving. Early commander removal before any tokens exist resets the entire plan to zero.

*Checkpoint: Cover the commander — can you identify the loop from the 99 alone?* Yes. The wizard-making noncreature spells, the multipliers, the ritual chains, and the burn finishers all point to "make wizard tokens, cast spells, multiply ping damage." The identity is clear.

### Kill Reliability — 4/5

Six distinct closing lines, several of which can win in a single explosive turn once the engine is online. The fastest configuration (Trance Kuja + trigger doubler + 3 tokens + a chain of 3 cheap spells) kills the entire table in one main phase. Backup lines (Aetherflux Reservoir, Exsanguinate, Mizzix's Mastery) provide alternative angles that don't require the Wizard board to be intact.

Docked from 5 because assembly time is real. The deck needs 2–3 turns of token accumulation before the wizard board threatens, and the best kills require at least one multiplier alongside the tokens. Rakdos has no tutors in this list (no Demonic Tutor, no Gamble) to consistently find the right multiplier or mana engine. You're relying on raw card draw density (Necropotence, Black Market Connections, Peer into the Abyss) to assemble naturally rather than surgically.

*Checkpoint: Name two closing lines and estimate turns from engine-online.* Wizard Ping Storm: 1–2 turns. Bonus Round + graveyard replay: 1 turn. Both realistic once Trance Kuja + 3 tokens exist.

### Durability — 3/5

The deck's key vulnerability is board wipes. A Cyclonic Rift, Toxic Deluge, or Farewell destroys every Wizard token and resets progress to zero. Rebuilding requires re-casting Kuja (or re-playing wizard-making spells) and then waiting multiple end steps for new tokens. Recovery time: 3–4 turns from a full wipe, which is too slow against aggressive pods.

Commander protection exists but is modest: Lightning Greaves, Kaya's Ghostform, Not Dead After All, plus three redirect effects (Imp's Mischief, Redirect Lightning, Untimely Malfunction). Card draw redundancy is excellent (Necropotence, Black Market Connections, Peer into the Abyss, 8+ additional draw spells), which helps find rebuild pieces. Mizzix's Mastery replays the graveyard, providing a recovery path after spell chains have stocked the yard. Reanimate retrieves key creatures (Harmonic Prodigy, Birgi, Storm-Kiln Artist).

Docked from 4 because the wizard tokens have no native resilience. They're 0/1s with no protection, and the deck runs no mass indestructible or phasing effects. A timely exile effect on Kuja specifically (e.g., Swords to Plowshares, Oubliette) is devastating because the tokens can't transform without him.

*Checkpoint: Cyclonic Rift on turn 7 — how many turns to threaten again?* Re-cast Kuja next turn (1 turn). Make a token per end step (2–3 turns). Need 3+ tokens before threatening. Total: 3–4 turns. Acceptable but not fast.

### Interaction Profile — 4/5

12 interaction pieces across multiple types and speeds:

- **Board wipe (1):** Blasphemous Act
- **Creature removal (5):** Deadly Rollick (free), Snuff Out (free/4 life), Fire Covenant (life-paid, multi-target), Withering Torment (also hits enchantments), Cornered by Black Mages (edict + wizard token)
- **Artifact removal (2):** Vandalblast (overload option), Untimely Malfunction (modal)
- **Catch-all (1):** Chaos Warp
- **Redirect/protection (3):** Imp's Mischief (redirect single-target), Redirect Lightning (redirect single-target), Return the Favor (copy or redirect)
- **Dual-use (1):** Saw in Half (destroys a creature; can target opponents' creatures for removal or own creatures for value)

Two free removal spells (Deadly Rollick, Snuff Out) and three redirect effects provide meaningful instant-speed interaction. The redirect package is especially valuable in Rakdos, compensating partially for the lack of counterspells — Imp's Mischief can redirect a counterspell targeting your key spell, and Return the Favor can copy an opponent's game-winning spell.

Docked from 5 because Rakdos fundamentally cannot interact with the stack beyond redirects. Non-targeting combo wins (e.g., Thassa's Oracle, storm chains, ETB combos) are difficult to stop. Against the pod's combo player specifically, the deck relies on preemptive removal of combo pieces rather than reactive stack interaction.

-----

## Bracket 3 Compliance

**Game Changers (3/3):**
1. Necropotence — pay-life card engine, the deck's primary draw source for assembling combo pieces
2. Jeska's Will — massive mana generation + card exile, feeds explosive turns
3. Underworld Breach — graveyard escape engine; in a spellslinger that wins by chaining noncreature spells, every escaped instant/sorcery is another Wizard-token ping trigger and another Storm-Kiln Treasure. Sacrifices at end step, but the deck wins in single explosive turns anyway.

**Infinite combos:** None. The deck wins through finite but explosive damage multiplication. No two-card or three-card infinite loops exist.

**Extra turns:** None.  
**Mass land denial:** None.

-----

## Pod Fit

1. **Explosive kill turns punish shields-down moments.** When the combo player taps out to attempt their own win, Kuja can chain spells through an uncontested board.
2. **Redirect effects disrupt targeted interaction.** Imp's Mischief, Redirect Lightning, and Return the Favor can protect your kill turn or redirect key removal.
3. **Simultaneous damage to all opponents.** Every Wizard ping hits each opponent — political alliances don't reduce incoming damage.
4. **Vulnerable to early aggression.** The 2–3 turn setup window before wizards accumulate is a real weakness. Fast combat decks can pressure life totals before the engine comes online.
5. **Weak to graveyard hate.** Mizzix's Mastery and the graveyard-based recovery plan fold to Rest in Peace or Dauthi Voidwalker.
6. **No counterspells means combo must be answered preemptively.** Against the pod's combo player, this deck must remove combo pieces before they're assembled rather than counter the winning spell.

-----

## Differentiation From Existing Decks

| | Kuja (Genome Project) | Azula (Lightning War) | Sauron (Dark Lord's Army) |
|---|---|---|---|
| Engine timing | Main phase spell chains | Combat phase doubling | Passive (opponents' spells) |
| Win condition | Wizard token pings × multipliers | Infinite combats / doubled value | Drain + Ring temptation + Army voltron |
| Colors | BR | UBR | UBR |
| Token type | Many 0/1 Wizards (fragile) | Copied creatures (temporary) | One growing Army (self-replacing) |
| Interaction density | Moderate (12 pieces, no counters) | Very high (8 counters + 7 removal) | High (6 counters + creature removal) |
| Commander dependency | Very high | Medium | Medium–high |
| Play pattern | Build → explode in one turn | Incremental pressure with protection | Passive accumulation + drain web |

Kuja is the only pure Rakdos deck in the collection. Its spellslinger burn archetype shares no engine overlap with any other deck — Azula doubles spells during combat (fundamentally different timing), and Sauron generates value from opponents' actions rather than your own spell sequencing.

-----

## Reskin / FF Set Reference

User-applied reskins map to canonical MTG cards; FF set originals listed for pilots unfamiliar with the set.

| Deck Card Name | Type | Notes |
|---|---|---|
| Bayo, Irritable Instructor | Reskin → **Electro, Assaulting Battery** | {1}{R}{R} 2/3 flying. Mana engine ({R} per instant/sorcery cast, mana doesn't empty as steps end) **plus** "When Electro leaves the battlefield, you may pay {X}. He deals X damage to target player." X-damage finisher when sac'd, removed, or destroyed — sac to Phyrexian Tower for two mana and a finisher in one shot. |
| Dawn Warriors' Legacy | Reskin → **Mizzix's Mastery** | Overload exile-and-cast-free every instant/sorcery in graveyard. |
| Lindblum, Industrial Regency // Mage Siege | FF set DFC (Town + Adventure) | Land taps for {R} (enters tapped). Adventure side **Mage Siege** ({2}{R} instant): create a 0/1 Wizard ping token. Cast Adventure → exile card → play land later. |
| Midgar, City of Mako // Reactor Raid | FF set DFC (Town + Adventure) | Land taps for {B} (enters tapped). Adventure side **Reactor Raid** ({2}{B} sorcery): sac an artifact or creature, draw 2. |
| Summon: G.F. Cerberus | FF set Saga creature | {2}{R}{R} 3/3 Enchantment Creature — Saga Dog. I — Surveil 1; II — Next instant/sorcery copied; III — Next instant/sorcery copied twice. |

-----

## Decklist (100 cards)

### Commander (1)
1 Kuja, Genome Sorcerer

### Game Changers (3)
1 Jeska's Will  
1 Necropotence  
1 Underworld Breach

### Wizard Producers / Wizard Synergy (7)
1 Black Mage's Rod  
1 Black Waltz No. 3  
1 Circle of Power  
1 Cornered by Black Mages  
1 Coruscation Mage  
1 Stormsplitter  
1 Vivi's Persistence

### Damage Multipliers (3)
1 City on Fire  
1 Harmonic Prodigy  
1 Roaming Throne

### Mana Engines (5)
1 Bayo, Irritable Instructor  
1 Birgi, God of Storytelling  
1 Dark Ritual  
1 Mana Geyser  
1 Storm-Kiln Artist

### Spell Multipliers / Replay (5)
1 Bonus Round  
1 Dawn Warriors' Legacy  
1 Overmaster  
1 Primal Amulet  
1 Summon: G.F. Cerberus

### Burn Finishers (3)
1 Aetherflux Reservoir  
1 Exsanguinate  
1 Price of Progress

### Value Creatures (2)
1 Neheb, the Eternal  
1 Urabrask

### Enchantments (1)
1 Black Market Connections

### Card Draw / Selection (11)
1 Big Score  
1 Deadly Dispute  
1 Demand Answers  
1 Ensnared by the Mara  
1 Faithless Looting  
1 Highway Robbery  
1 Light Up the Stage  
1 Night's Whisper  
1 Peer into the Abyss  
1 Sign in Blood  
1 Unexpected Windfall

### Commander Protection (3)
1 Kaya's Ghostform  
1 Lightning Greaves  
1 Not Dead After All

### Interaction (12)
1 Blasphemous Act  
1 Chaos Warp  
1 Deadly Rollick  
1 Fire Covenant  
1 Imp's Mischief  
1 Redirect Lightning  
1 Return the Favor  
1 Saw in Half  
1 Snuff Out  
1 Untimely Malfunction  
1 Vandalblast  
1 Withering Torment

### Recursion (1)
1 Reanimate

### Utility (1)
1 Dance with Calamity

### Ramp (6)
1 Arcane Signet  
1 Fellwar Stone  
1 Rakdos Signet  
1 Ruby Medallion  
1 Sol Ring  
1 Talisman of Indulgence

### Lands (36)
1 Arid Mesa  
1 Blazemire Verge  
1 Blood Crypt  
1 Bloodstained Mire  
1 Command Tower  
1 Dragonskull Summit  
1 Emergence Zone  
1 Graven Cairns  
1 Haunted Ridge  
1 Lindblum, Industrial Regency  
1 Luxury Suite  
1 Malakir Rebirth  
1 Marsh Flats  
1 Midgar, City of Mako  
1 Phyrexian Tower  
1 Polluted Delta  
1 Scalding Tarn  
1 Shatterskull Smashing  
1 Smoldering Marsh  
1 Urborg, Tomb of Yawgmoth  
1 Valakut Awakening  
1 Wooded Foothills  
8 Mountain  
6 Swamp

-----

## Changelog

- **2026-05-10 (full audit + Underworld Breach swap):** First formal audit pass against the Conversion Check. Score holds at 4/4/3/4 = **15/20**. Decklist: `the-genome-project-20260510.txt`. Card text verified for every engine piece, multiplier, mana source, removal, and reskin via `card_lookup.py`.
  - **Card swap:** Underworld Breach added as 3rd Game Changer; Lively Dirge cut to sideboard. Breach gives the deck a third graveyard-replay axis alongside Bonus Round and Dawn Warriors' Legacy. Increases graveyard-hate vulnerability — already a Pod Fit weakness.
  - **Card-text corrections** (documentation only; mechanics unchanged):
    - **City on Fire** triples *all* damage from sources you control (combat included), not "noncombat damage." Math in the multiplier table came out the same but the description was wrong. Two copies = ×9, three = ×27.
    - **Black Mage's Rod** creates a **1/1 colorless Hero token** (not a Wizard token); the equipped creature gains the noncreature-spell ping ability AND becomes a Wizard via the granted ability. The token only counts toward the 4-Wizard threshold once equipped.
    - **Coruscation Mage's Offspring** ({2} additional cost) creates a 1/1 token copy that **inherits the printed ping ability** — casting for {3}{R} = two pingers in one card.
    - **Vivi's Persistence** recursion is gated on **commander entering or attacking** (not auto-recur from graveyard). Active piece tied to Kuja recasts.
    - **Bayo, Irritable Instructor / Electro** has an **X-damage death trigger** undocumented in prior summary — when it leaves the battlefield, pay X to deal X to target player. Sacrifice to Phyrexian Tower for {B}{B} and a finisher.
    - **Black Market Connections's Hire a Mercenary mode** creates a 3/2 colorless **Shapeshifter changeling** — every creature type, *including Wizard*. Hidden mode for hitting the 4-Wizard transform threshold.
    - **Stormsplitter** recategorized: it's a Wizard token replicator (1/4 Otter Wizard token copies on each instant/sorcery cast), not a damage multiplier. Counts: Wizard Producers 6 → 7, Damage Multipliers 4 → 3.
  - **Hidden synergies surfaced** (added to Reskin / FF Set Reference and Wizard Producer Layer notes):
    - **Lindblum, Industrial Regency**'s DFC Adventure side **Mage Siege** is a {2}{R} Wizard-token producer.
    - **Midgar, City of Mako**'s DFC Adventure side **Reactor Raid** is a {2}{B} sac-to-loot.
    - **Summon: G.F. Cerberus** mechanics documented in reference table.
- **2026-04-03 (baseline build):** Decklist `the-genome-project-20260403-050230.txt`. 99 main + 1 commander. Pre-audit summary scored 4/4/3/4 = 15/20.
