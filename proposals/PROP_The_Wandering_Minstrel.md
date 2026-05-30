# Proposal: The Wandering Minstrel

Status: **not built.** Drafted 2026-05-14.

Card text verified against local Scryfall data per `CLAUDE.md` hard rules. The Hashaton 2026-05-02 incident is the reason proposals must verify before drafting. Every card text quoted below was Scryfall-checked at draft time; re-verify at build time. Prices below are unverified — flag from `feedback_verify_prices` memory — check Cardmarket before purchasing.

User instruction: **cap at 3 Game Changers, infinites permitted.**

---

## Commander

**The Wandering Minstrel** (BGRUW). `{G}{U}`, Legendary Creature — Human Bard, 1/3.

> Lands you control enter untapped.
>
> The Minstrel's Ballad — At the beginning of combat on your turn, if you control five or more Towns, create a 2/2 Elemental creature token that's all colors.
>
> `{3}{W}{U}{B}{R}{G}`: Other creatures you control get +X/+X until end of turn, where X is the number of Towns you control.

**Color identity: BGRUW (5C).** Cheap to cast at `{G}{U}`. Owned: 1 copy, undeployed.

**Engine note.** The first line — "Lands you control enter untapped" — is the load-bearing one. Every Town (and Town is a real subtype, confirmed via Lindblum oracle ruling: "Town is a land type with no special meaning") is printed ETB-tapped and taps for one color, like a shock-line dual without the life loss. With the Minstrel out, Towns become strict upgrades over basics. The combat trigger and the anthem activation are payoffs on top, not the core; the deck wants to play many Towns because every Town is a free-roll dual *and* a counter on the anthem *and* a different-named land for Field of the Dead.

The +X/+X is on **other** creatures, so this is a go-wide anthem (not Voltron). The trigger requires 5+ Towns to make the Elemental; the anthem scales linearly with Town count regardless of threshold. Both clauses reward Town density.

---

## Archetype framing

**5C Town tribal with a lands-matter spine and a 2-card infinite finisher.** Three engines stacked:

1. **Town manabase** — entering untapped, color-fixing without tempo cost. Manabase doubles as the win condition (Field of the Dead) and the anthem scaler.
2. **Lands-matter payoffs** — Avenger of Zendikar, Scute Swarm, Maja, Rampaging Baloths, Field of the Dead, Titania, World Shaper. Every land drop = multiple triggers.
3. **Cathars' Crusade + Scurry Oak infinite** — clean 2-card win that doesn't require the commander.

Distinct from current roster:
- **The Loam Cycle (Teval, BUG/Sultai)** is the closest archetype overlap — also lands-matter, also runs Crucible/Excavator/Splendid Reclamation. Loam Cycle is 3C and graveyard-Sultai-flavored; Wandering Minstrel is 5C and combat/anthem-flavored. **They cannot coexist** — see Replacement context below.
- **The Genome Project (Kuja, 5C storm)** is the only other 5C. Different engine (Vivi spell-storm vs Town/landfall).
- **Earthbend the Meta (Toph, GW landfall)** is landfall-adjacent but 2C and pillowfort-style.

---

## Replacement context

**Net add, not slot swap.** Per user instruction (2026-05-14): no other decks retire to feed this build. Every contested card gets a bought duplicate. Wandering Minstrel sits alongside Loam Cycle, Genome Project, Earthbend, Radiation, etc., unchanged.

Net roster impact: **17 active decks → 18 active decks.** Same shape as the Najeela proposal.

**Power-ceiling implication: zero.** Bought duplicates of Field of the Dead, Crop Rotation, Splendid Reclamation, World Shaper, and Underworld Breach are functionally identical to pulled copies — both flavors of the build reach the same ~17–18/20 ceiling. The choice is "spend ~$110 on cards" vs. "gut Loam Cycle." User chose money. The card pieces that *would* have been pulled now appear in the buy list below.

Loam Cycle's GC slots (Field of the Dead, Crop Rotation, Fierce Guardianship) and Genome Project's GC slots (Necropotence, Jeska's Will, Underworld Breach) remain intact — both decks stay at 3/3 GC. Wandering Minstrel runs its own duplicate copies of the GC cards.

---

## Power ceiling from collection

**Realistic ceiling: 17–18/20 (high Solid / low Elite), Bracket 4.** Identical to the cannibalize version — buying duplicates does not change deck power. Lower than Najeela (18–19) for three reasons:

1. **Commander dependency is moderate, not high.** Lands-untapped clause is the strongest part, but the Field+Scapeshift+Cathars-Oak win conditions function without the commander. This is *good* — but it also means the commander doesn't accelerate the win, she just enables the manabase.
2. **No turn-3 combo line.** Cathars' Crusade + Scurry Oak requires 5W mana on top of board presence. Scapeshift→Field is 4G plus enough Towns in deck (achievable T6–T7). No `{R}{1}` LED+Breach cheese.
3. **Field of the Dead is the engine.** Without Field, the deck drops to ~15/20. Field is a single-point-of-failure; if exiled (Bojuka Bog can't catch it, but a Farewell or stax piece neutralizes it), the deck plays as a slower midrange.

Hard cap: ~18/20 with the GCs and buys spec'd below. If a 4th GC were permitted (e.g., adding Necropotence from Genome), ceiling raises to ~19/20.

---

## Combo lines (verified math)

### Line 1 — Cathars' Crusade + Scurry Oak (primary infinite, 2-card)

**Cathars' Crusade** (verified): `Whenever a creature you control enters, put a +1/+1 counter on each creature you control.`

**Scurry Oak** (verified): `Evolve. Whenever one or more +1/+1 counters are put on this creature, you may create a 1/1 green Squirrel creature token.`

Setup: both on the battlefield, then trigger by any creature enters (commander recast counts).

1. Squirrel enters → Crusade triggers, +1/+1 on each creature including Scurry Oak.
2. Scurry Oak's trigger fires (counter put on it) → create 1/1 Squirrel.
3. Squirrel enters → loop to step 1.

**Infinite** Squirrel tokens, all growing in size each iteration. Win by attacking — even without commander on board, a board of arbitrarily-large Squirrels with Triumph of the Hordes / Akroma's Will / Pathbreaker Ibex / Beastmaster Ascension closes. With commander out: +X/+X anthem activation adds +20 power per Squirrel on top.

Cost: Scurry Oak ~$0.50 buy. Cathars' Crusade owned ×3. **Combo total: ~$0.50.**

### Line 2 — Earthcraft + Squirrel Nest (secondary infinite, 2-card)

**Earthcraft** (verified): `Tap an untapped creature you control: Untap target basic land.`

**Squirrel Nest** (verified): `Enchant land. Enchanted land has "{T}: Create a 1/1 green Squirrel creature token."`

Setup: Squirrel Nest on a basic land (or any land if Dryad of the Ilysian Grove is also out, since Dryad makes all lands every basic type), Earthcraft on the battlefield.

1. Tap enchanted land → create Squirrel.
2. Tap fresh Squirrel via Earthcraft → untap enchanted land.
3. Loop.

**Infinite** Squirrels. Same win conditions as Line 1.

Cost: Earthcraft owned ×1 free. Squirrel Nest ~$2 buy. **Combo total: ~$2.**

Note on Earthcraft vs. Najeela proposal: the Najeela memory (`project_najeela_proposal.md`) tags Earthcraft as a Najeela deep-redundancy slot. The card is currently 1/0 free — one undeployed copy. **If Najeela is also built, Earthcraft contention requires a buy of a second copy** (~$30) or the two decks split it. Najeela uses Earthcraft only as Line 5 (deep redundancy); Wandering Minstrel uses it as its second primary combo. Wandering Minstrel has stronger claim.

### Line 3 — Scapeshift → Field of the Dead (deterministic win)

**Scapeshift** (verified): `Sacrifice any number of lands. Search your library for up to that many land cards, put them onto the battlefield tapped, then shuffle.`

**Field of the Dead** (verified): `Whenever this land or another land you control enters, if you control seven or more lands with different names, create a 2/2 black Zombie creature token.`

Setup: Field of the Dead in play, 5+ lands sacrificed via Scapeshift, 5+ different-named Towns in library.

1. Scapeshift sacrifices 5 lands → searches up 5 differently-named Towns (deck has 22 differently-named Towns; library will always have 5+ options).
2. Each enters, each triggers Field separately (rulings confirm simultaneous-ETB triggers all count). With 7+ different-named lands controlled (which is automatic once the 5 Towns enter alongside existing lands), each ETB makes a 2/2 Zombie.
3. **5 Zombies from one Scapeshift.** With Wandering Minstrel on board, the 5 sacrificed lands re-enter *untapped* — so the mana is fully refunded for follow-up.

With Parallel Lives or Anointed Procession out (both 4-mana, both owned): **10 Zombies from one Scapeshift.** With both: 20.

This line costs 4G on the spell + 0 on the engine (Field is the GC). Available T5–T6 reliably with Crop Rotation tutoring Field on T3–T4. **Bracket 4 finisher.**

### Line 4 — Splendid Reclamation + Field (graveyard-fueled lands burst)

**Splendid Reclamation** (verified): `Return all land cards from your graveyard to the battlefield tapped.`

Splendid Reclamation's ruling explicitly notes: ETB-tapped replacements still apply because Splendid says "tapped" rather than "enters tapped." **Wandering Minstrel's lands-enter-untapped clause is a different replacement effect — it modifies the ETB condition, which Splendid Reclamation doesn't override.** Lands brought back via Splendid still enter, but they enter "tapped" per Splendid's word. The Minstrel clause and Splendid clause conflict: Minstrel says "enter untapped," Splendid says "tapped." **Rule 616.1 (replacement effects): the affected player chooses order.** Minstrel's controller chooses → enter untapped wins.

Verified via the Splendid Reclamation Scryfall ruling: "If an effect states that a land enters the battlefield tapped *unless a condition is met*, Splendid Reclamation's effect puts that land onto the battlefield tapped even if that condition is true." This addresses *check-land*-style "unless" replacements, not blanket "enter untapped" effects like Wandering Minstrel. The Minstrel's clause is unconditional, so it applies.

Setup: 5+ lands in graveyard (from Crop Rotation sacs, fetches, World Shaper sac, Splendid's own engine over multiple turns), Field of the Dead in play, Wandering Minstrel in play.

1. Cast Splendid Reclamation (4G). All graveyard lands return — untapped, courtesy of Minstrel.
2. Each ETB triggers Field with 7+ different-named lands → Zombies for each.
3. 5+ Zombies, all available mana refunded.

Slower than Scapeshift but doesn't sacrifice lands — pure value. With **Underworld Breach** in graveyard, the spell is recurrable for 4G + 3 mill.

### Line 5 — Tooth and Nail (entwine) → Avenger + Craterhoof

**Tooth and Nail** (verified, **no longer a Game Changer** per Oct 2025 removal): entwine puts two creatures from library into play. Avenger creates plant tokens equal to lands; Craterhoof gives all creatures +X/+X trample where X is creature count.

7 mana. With Minstrel's mana refund off existing Towns, achievable T6. Wins on the spot.

### Line 6 — Commander anthem alpha-strike (non-combo win)

With 10+ Towns and a board of bodies (Squirrels from any of the above, Elementals from the combat trigger, Plant tokens, Zombies), pay 7 mana → +10/+10 to everything → swing. Each Squirrel hits for 11+. Lethal across multiple opponents with Triumph or Pathbreaker Ibex doubling.

This is the floor win condition. Even without finding any combo, Field, or Scapeshift, the deck closes via Town anthem swing by T8–T9.

---

## Owned shell that maps onto Wandering Minstrel

Cross-checked against `collection/moxfield_haves_2026-05-14-0631Z.csv` and `decks/*.txt`. ⚠️ = currently deployed in another active deck (one copy tied up).

### Towns (the manabase)

**20 of 26 Towns currently owned. 17 are free** (not deployed anywhere); 3 are tied up (Lindblum ×2 in Lightning War + Genome, Midgar in Genome, Starting Town in Lightning War). Lindblum has 2 owned copies but both are deployed.

Free Towns to slot directly (17): Adventurer's Inn, Capital City, Crossroads Village, Eden Seat of the Sanctum, The Gold Saucer, Gohn Town of Ruin, Gongaga Reactor Town, Guadosalam Farplane Gateway, Insomnia Crown City, Ishgard the Holy See, Jidoor Aristocratic Capital, Rabanastre Royal City, Sharlayan Nation of Scholars, Treno Dark City, Vector Imperial Capital, Windurst Federation Center, Baron Airship Kingdom.

**Tied-up Towns: buy duplicates instead of pulling.**
- Lindblum, Industrial Regency — buy ~$1 (R adventure)
- Midgar, City of Mako — buy ~$1 (B adventure)
- Starting Town — buy ~$0.50 (colorless)

**Missing-from-collection Towns: buy** ~$0.50–$2 each:
- Clive's Hideaway, Zanarkand Ancient Metropolis, A-Town, Second City, Value Town, Balamb Garden SeeD Academy.

**Target Town count in deck: 20–22 different-named Towns.** Pure-Town manabase + 1 Field of the Dead + supporting non-Town lands. Pick the cheaper-or-better-flavored 3 of the 6 missing + 3 tied-up duplicates → 20 different Towns at ~$8 in Town buys.

### Lands engine

| Card | Status | Notes |
|---|---|---|
| Field of the Dead | ⚠️ Loam Cycle | **Buy duplicate ~$30 (GC).** Loam's copy stays. |
| Crop Rotation | ⚠️ Loam Cycle | **Buy duplicate ~$10 (GC).** Loam's copy stays. |
| Crucible of Worlds | 4 owned, 2 deployed (Loam + Crystal Sickness) | **1 free copy.** Take it. |
| Ramunap Excavator | 2 owned, 1 deployed (Loam) | **1 free copy.** Take it. |
| Life from the Loam | 2 owned, 1 deployed (Loam) | **1 free copy.** Take it. |
| Splendid Reclamation | 1 owned (Loam) | **Buy duplicate ~$5.** |
| World Shaper | 1 owned (Loam) | **Buy duplicate ~$1.** |
| Tooth and Nail | 1 owned (Loam) | **Skip.** Pathbreaker Ibex + Beastmaster Ascension + Akroma's Will cover the alpha-strike role for ~$13 total vs. ~$8 for one Tooth and Nail duplicate. Not worth the slot. |
| Scapeshift | 0 | **Buy ~$30.** Cornerstone finisher. |
| Dryad of the Ilysian Grove | 2 owned, undeployed | Free. Enables Earthcraft on Towns. |
| Knight of the Reliquary | 0 | **Buy ~$3.** |
| Sylvan Scrying | 0 | **Buy ~$3.** Town tutor. |
| Expedition Map | 3 owned, ≤1 deployed (Loam) | Free copy. |
| Azusa, Lost but Seeking | 2 owned, 2 deployed (Calamity Tax + Loam) | **Skip.** Oracle of Mul Daya + Augur of Autumn already cover extra-land-drop slot at lower cost. |
| Exploration | 2 owned, 2 deployed | **Skip.** Same reasoning as Azusa. |
| Titania, Protector of Argoth | 1 owned per CSV; 2 deployments (Calamity Tax + Loam — data discrepancy) | **Skip.** Verify physical ownership later, but the deck doesn't need it given the landfall stack already includes Avenger, Scute Swarm, Rampaging Baloths, Maja. |

### Landfall payoffs

| Card | Status |
|---|---|
| Avenger of Zendikar | 2 owned, free |
| Scute Swarm | 2 owned, free |
| Rampaging Baloths | 1 owned, free |
| Tireless Provisioner | 2 owned, free |
| Tireless Tracker | 2 owned, free |
| Oracle of Mul Daya | 1 owned, free |
| Felidar Retreat | 1 owned, in Earthbend the Meta. **Skip.** Avenger + Scute + Baloths + Maja cover the role. |
| Maja, Bretagard Protector | 0. **Buy ~$1.** |
| Augur of Autumn | 0. **Buy ~$5.** |
| Beast Whisperer | 0. **Buy ~$1.** |

### Token doublers

| Card | Status |
|---|---|
| Parallel Lives | 1 owned, free |
| Anointed Procession | 2 owned, free |
| Cathars' Crusade | 3 owned, free |
| Doubling Season | 1 owned, in Radiation Sickness (just added 2026-05-13). **Do not pull — recent upgrade.** Buy duplicate ~$40 if wanted. |
| Mondrak, Glory Dominus | 0. **Buy ~$15 unverified.** Lowest priority — Parallel Lives + Anointed Procession already in deck. |

### Combo pieces

| Card | Status |
|---|---|
| Scurry Oak | 0. **Buy ~$0.50.** Primary infinite. |
| Cathars' Crusade | 3 owned, free. Primary infinite half. |
| Earthcraft | 1 owned, undeployed. ⚠️ Najeela contention if both decks are built — see Combo Line 2 note. |
| Squirrel Nest | 0. **Buy ~$2.** Secondary infinite. |
| Walking Ballista | 1 owned, free. Alt win condition off Cathars+Scurry counters. |

### Anthem / finishers

| Card | Status |
|---|---|
| Akroma's Will | 3 owned, free |
| Craterhoof Behemoth | 2 owned, 2 deployed (Eldrazi Stampede + Loam Cycle). **Skip.** Pathbreaker Ibex + Beastmaster Ascension at ~$13 combined cover the role at less than half the cost of one Craterhoof duplicate (~$30). |
| Triumph of the Hordes | 2 owned, 2 deployed (Earthbend + Radiation). **Skip.** Akroma's Will + Pathbreaker Ibex cover the doubled-damage win condition. |
| Beastmaster Ascension | 0. **Buy ~$3.** |
| Pathbreaker Ibex | 0. **Buy ~$10.** |

### Commander-amplifiers

| Card | Status |
|---|---|
| Roaming Throne | 2 owned, 1 deployed (Genome). **1 free.** Set type = Bard, doubles the combat token trigger. |
| Strionic Resonator | 2 owned, free. Doubles the combat trigger. |

### Card draw

| Card | Status |
|---|---|
| Sylvan Library | 2 owned, free |
| Guardian Project | 2 owned, free |
| Esper Sentinel | 4 owned, ≤4 deployed (zero slack per Najeela memory — verify). **Skip.** Sylvan Library + Guardian Project + Augur of Autumn + Beast Whisperer already cover draw density. |
| Mystic Remora | 1 owned, in Replication Crisis. **Skip.** Above draw package is sufficient. |
| Underworld Breach | 1 owned, in Genome Project (added 2026-05-10). **Buy duplicate ~$3 (GC).** Genome's copy stays. |

### Interaction

| Category | Cards |
|---|---|
| Counterspells | Counterspell (free), Swan Song (likely free), An Offer You Can't Refuse (likely free) |
| Targeted removal | Swords to Plowshares, Path to Exile, Assassin's Trophy, Beast Within, Generous Gift — all multiples owned |
| Sweeper | Toxic Deluge (10 owned, multiple free) |
| Protection | Lightning Greaves (free copy), Swiftfoot Boots (free copy), Heroic Intervention (5 owned, ≤3 deployed — free) |

### Ramp (non-land)

Sol Ring (24 owned), Arcane Signet (24 owned), Three Visits (5 owned), Nature's Lore (6 owned), Cultivate (6 owned), Kodama's Reach (5 owned), Skyshroud Claim (2 owned), Rampant Growth (5 owned). **All free, ample slack.**

---

## Game Changer slots — 3/3 used (per user instruction)

Verified against `REF_Game_Changers_List.md` (Feb 2026 update). All three are **bought duplicates** — no donations, no other decks affected.

1. **Field of the Dead** (~$30 buy) — engine-defining; without Field the deck loses Combo Lines 3 and 4 and drops to ~15/20. The existing owned copy stays in Loam Cycle.
2. **Crop Rotation** (~$10 buy) — instant-speed Field tutor at 1 mana. Sacs an excess Town, finds Field (or an unowned Town, or Gaea's Cradle if ever acquired). Existing copy stays in Loam.
3. **Underworld Breach** (~$3 buy) — recursion for Splendid Reclamation, Scapeshift, big spells. Existing copy stays in Genome Project. Cheapest of the three GCs because Breach is currently at low market price.

**No-donation impact:** Loam Cycle stays at 3/3 GC (Field, Crop Rotation, Fierce Guardianship). Genome stays at 3/3 GC (Necropotence, Jeska's Will, Underworld Breach). All other active decks unchanged.

**Combined GC buy cost: ~$43 unverified.** Confirm prices before purchasing.

---

## Buy list summary — no-retirement version

Prices unverified — flag from `feedback_verify_prices` memory. Confirm Cardmarket before purchasing. No cards pulled from other decks; every contested card is bought as a duplicate.

**Game Changers (3, ~$43):**
- Field of the Dead (~$30)
- Crop Rotation (~$10)
- Underworld Breach (~$3)

**Engine duplicates from Loam Cycle (~$6):**
- Splendid Reclamation (~$5)
- World Shaper (~$1)

**Cornerstone finisher (~$30):**
- Scapeshift

**Combo enablers (~$2.50):**
- Scurry Oak (~$0.50)
- Squirrel Nest (~$2)

**Town completion (~$8):**
- 6 missing Towns at $0.50–$2 each, plus 3 tied-up duplicates (Lindblum, Midgar, Starting Town). Pick any 3 missing + 3 tied-up = ~$5–8.

**Missing-from-collection support (~$25):**
- Knight of the Reliquary (~$3)
- Sylvan Scrying (~$3)
- Maja, Bretagard Protector (~$1)
- Augur of Autumn (~$5)
- Pathbreaker Ibex (~$10)
- Beastmaster Ascension (~$3)
- Beast Whisperer (~$1)

**Total minimum viable: ~$115 unverified.** Confirm prices before buying.

**Explicitly skipped (would otherwise be ~$60+):** Tooth and Nail duplicate, Craterhoof duplicate, Triumph of the Hordes duplicate, Felidar Retreat duplicate, Azusa duplicate, Exploration duplicate, Esper Sentinel duplicate, Mystic Remora duplicate, Doubling Season duplicate. Each is replaceable by cheaper owned cards or already-bought alternatives — the deck does not need them to function.

**Optional polish (low priority):**
- Balamb Garden, SeeD Academy (~$2) — 21st Town, also a UG Vehicle
- Mondrak, Glory Dominus (~$15) — third token doubler
- Cradle of Vitality, Akroma's Memorial, Doubling Season — open-ended upgrades

---

## Construction direction

**Lands (38):**
- 20 different-named Towns (17 free + 3 buys, or 18 free + 2 buys if pulling Starting Town from Lightning War)
- 1 Field of the Dead
- 5 basics (1 of each — feeds Earthcraft, gives Cultivate/Kodama's Reach targets)
- 4 fetches (any owned — Misty Rainforest, Wooded Foothills, Polluted Delta, Bloodstained Mire)
- 4 utility (Command Tower, Reliquary Tower, Path of Ancestry, Boseiju Who Endures if pullable from Loam)
- 4 duals (any owned shocks/triomes/checks)

**Non-land 60 (rough breakdown):**
- 10 ramp (signets + green sorcery ramp + Crop Rotation)
- 8 land tutors / lands engine (Expedition Map, Sylvan Scrying, Knight of the Reliquary, Scapeshift, Splendid Reclamation, Crucible, Ramunap Excavator, Life from the Loam)
- 8 landfall payoffs (Avenger, Scute Swarm, Rampaging Baloths, Maja, Felidar Retreat, Titania, World Shaper, Tireless Provisioner)
- 5 token doublers / anthems (Parallel Lives, Anointed Procession, Cathars' Crusade, Beastmaster Ascension, Cathars-pair Scurry Oak)
- 6 combo / finishers (Scurry Oak, Earthcraft, Squirrel Nest, Tooth and Nail, Craterhoof, Underworld Breach)
- 6 card draw (Sylvan Library, Guardian Project, Esper Sentinel, Augur of Autumn, Oracle of Mul Daya, Tireless Tracker)
- 4 anthem/finishers (Akroma's Will, Pathbreaker Ibex, Triumph if pulled, Dryad of the Ilysian Grove)
- 3 commander amplifiers (Roaming Throne, Strionic Resonator, Lightning Greaves)
- 10 interaction (Counterspell, Swan Song, An Offer, Swords to Plowshares, Path to Exile, Assassin's Trophy, Beast Within, Generous Gift, Heroic Intervention, Toxic Deluge)

---

## Known weaknesses

- **Field-dependency.** Removing or exiling Field of the Dead (Farewell, Bojuka Bog can't catch it but a hand-stax piece keeps it in hand) drops the deck's win-rate noticeably. Crop Rotation mitigates but Field has no functional reprint.
- **Slow start in 5C.** Without an early Town drop, the deck plays as a 3-mana ramp deck without payoffs until T4. Mulligan aggressively for Sol Ring + Town + green ramp.
- **Cathars+Scurry combo can be disrupted by a single instant.** Counterspells, exile-target removal, or even a Pongify on Scurry Oak post-Cathars-resolution breaks the line. Single-card win conditions need protection density (Heroic Intervention, Lightning Greaves on Scurry Oak).
- **Earthcraft contention with Najeela proposal.** If Najeela also gets built, both decks want the single owned Earthcraft. Wandering Minstrel's claim is stronger (Line 2 primary combo vs. Najeela's Line 5 deep redundancy). If both decks coexist, buy a second Earthcraft (~$30 unverified) — not in the minimum buy list above.
- **No Gaea's Cradle.** Crop Rotation can theoretically find Cradle if ever acquired (~$700). Not in scope.
- **18 active decks.** Roster grows by one. Same shape as the Najeela proposal — net add, not slot swap.

---

## Changelog

- **2026-05-14:** Initial draft. 3-GC cap (Field of the Dead, Crop Rotation, Underworld Breach). Primary combo: Cathars' Crusade + Scurry Oak. Original framing retired Loam Cycle to feed the build.
- **2026-05-14:** Revised to no-retirement / buy-duplicates per user instruction. All contested cards now bought as duplicates instead of pulled. Roster grows 17 → 18 (net add). Ceiling unchanged at 17–18/20. Buy total ~$115 minimum viable (up from $45 in the cannibalize version — the $70 delta is GC duplicates + Splendid Reclamation + World Shaper).
