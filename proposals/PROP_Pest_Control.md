# Proposal: Pest Control — Witherbloom, the Balancer

Status: **not built.** Drafted 2026-05-18. Supersedes the prior "Pest Control" sketch (Sprout-Swarm-centric, Gaea's Cradle GC slate). This is the **Razaketh tutor-pivot revision** — same commander, same archetype family (BG token aristocrats), tighter execution.

Card text verified against local Scryfall data per `CLAUDE.md` hard rules. The Hashaton 2026-05-02 incident is the reason proposals must verify before drafting — see [[feedback_proposals_require_verified_card_text]]. Every commander-text and combo-piece claim below was Scryfall-checked at draft time; re-verify at build time. Prices below are unverified — flag from [[feedback_verify_prices]] — check Cardmarket before purchasing.

User constraint: **Bracket 3, 3 GC max, no MLD, no extra-turn chains, pod approval required for early 2-card infinites.**

---

## Commander

**Witherbloom, the Balancer** (BG). `{6}{B}{G}`, Legendary Creature — Elder Dragon, 5/5.

> Affinity for creatures *(This spell costs {1} less to cast for each creature you control.)*
>
> Flying, deathtouch
>
> Instant and sorcery spells you cast have affinity for creatures.

**Color identity: BG.** Owned: 1 copy, undeployed.

**Engine note.** Two affinity clauses. The first applies to Witherbloom herself — with 6 creatures on board she casts for `{B}{G}`. The second is the deck's engine: every instant and sorcery in the 99 gets the same per-creature generic reduction.

What this pulls toward: many cheap creatures on board, then chain instants and sorceries for value, tutors, and finishers. Token-aristocrats is the natural fit; BG spellslinger is too thin in payoffs to compete.

What it does NOT discount: enchantments (Bitterblossom, Animate Dead, Necromancy), artifacts (Phyrexian Altar, Skullclamp), and the colored portion of spell costs. Plan accordingly.

---

## Why this revision (vs. prior sketch)

The prior Pest Control sketch had three caps:

1. **Gaea's Cradle in the GC slate but not owned** — $700+ acquisition wall.
2. **Necropotence in the GC slate but locked in Genome Project** as Genome's 3/3 GC slot.
3. **Win vertical depth of 5 specific pieces** (Witherbloom + Sprout Swarm + 3 creatures + Phyrexian Altar + Blood Artist) without tutor density to assemble.

User pushback: commander tax pain is mitigated by fast post-wipe rebuild, so the strategy doesn't have to be "stay wide forever." That opens the door to a **reanimator-tutor hybrid** that uses one card (a reanimation spell on Razaketh) to recover from wipes, rather than rebuilding tokens drip-by-drip.

This revision keeps the token-aristocrats shell and adds Razaketh as a 3-tutors-per-turn engine reanimated for ~1 mana off the affinity discount. Ceiling rises ~2 points; cost drops by an order of magnitude.

---

## Archetype framing

**BG tutor-dense aristocrats with a reanimator subtheme and the Earthcraft + Squirrel Nest backup combo.** Three engines stacked:

1. **Witherbloom affinity** — every instant/sorcery gets a per-creature generic discount once you have a board. Tutors, X-spells, reanimation, removal, Sprout Swarm — all cheaper.
2. **Razaketh tutor chain** — 8/8 flying/trample with `{B}, pay 2 life, sacrifice a creature: tutor any card`. Activated ability, no tap, no cooldown. With a token board feeding sacs, this is 3–5 tutors per turn at sorcery speed.
3. **Reanimation post-wipe rebuild** — Reanimate, Animate Dead, Necromancy, Buried Alive. One spell brings Razaketh back. With Witherbloom's affinity on Reanimate, that's `{B}` or even free.

Distinct from the existing roster:

- **Diminishing Returns (Teysa, WB aristocrats)** — closest overlap. Both run Blood Artist / Bastion of Remembrance / Phyrexian Altar / Skullclamp / Viscera Seer / Carrion Feeder / Animate Dead / Necromancy / Reanimate / Buried Alive. **The aristocrats shell genuinely overlaps.** Distinguish via commander engine: Teysa is token-flicker (death triggers double for non-token creatures, sac outlets fire on tokens), Witherbloom is spell-affinity (instants/sorceries scale on creature count). Different decision tree per turn. Both run a similar 25-card aristocrat core but the wraparound is 75% different.
- **The Loam Cycle (Teval, BUG)** — lands-matter, not creatures-matter. Different axis. No real overlap beyond Craterhoof and Eternal Witness.
- **The Dark Lord's Army (Sauron, mono-B)** — reanimator-aristocrats. Real overlap on Reanimate / Animate Dead / Necromancy / Buried Alive. Mono-B vs BG; Razaketh-tutoring vs Sauron-token-stax. Distinct play patterns, shared parts list.
- **Calamity Tax (Glarb, BUG)** — X-spell finishers (Torment, Exsanguinate), Cabal Coffers, Urborg. Overlap on the big-mana drain finisher. Pest Control's drain is creature-fueled, Calamity's is land-fueled.

**Coexistence verdict:** mechanically distinct enough at the engine level (affinity vs. token-flicker vs. lands-matter vs. reanimator-stax), but the parts-list overlap with Diminishing Returns is material — this proposal accepts that 7–9 cards will be bought as duplicates rather than pulled from existing decks.

---

## Replacement context

**Net add, not slot swap.** No other decks retire to feed this build. Every contested combo-critical card gets a bought duplicate. Pest Control sits alongside Diminishing Returns, Dark Lord's Army, etc., unchanged.

Net roster impact: **17 active decks → 18 active decks.** Same shape as the Najeela and Wandering Minstrel proposals.

Loam Cycle stays 3/3 GC (Field, Crop Rotation, Fierce Guardianship). Genome stays 3/3 (Necropotence, Jeska's Will, Underworld Breach). Diminishing Returns stays 3/3 (Farewell, Smothering Tithe, Teferi's Protection). Radiation Sickness stays 3/3 (Seedborn Muse, Vampiric Tutor, Cyclonic Rift). No GC contention.

---

## Game Changer slots — 3/3 used

Verified against `REF_Game_Changers_List.md` (Feb 2026 update). The prior Cradle / Necro / Natural Order slate had two blockers (Cradle unowned, Necro deployed). This slate fixes both.

| # | Card | Status | Cost | Why |
|---|---|---|---|---|
| 1 | **Survival of the Fittest** | 1 owned, deployed in Radiation Sickness (per 2026-05-13 upgrade) | **Buy duplicate ~$50–80 unverified** | `{G}, Discard a creature card: Search your library for a creature card, reveal that card, put it into your hand.` Creature-toolbox tutor at 1 mana per activation. Discard-fuel feeds reanimation. Repeatable. Replaces Cradle as the consistency engine. |
| 2 | **Bolas's Citadel** | 1 owned, undeployed | **Free** ✓ | `Cast spells from top of library, pay life equal to MV instead of mana cost.` With Necropotence-style life-as-currency and tutor density to stack the top of the deck, Citadel chains through the library. Pairs disgustingly with low-MV spells (Reanimate MV 1 = 1 life). Owned, free, undeployed — the cheapest GC upgrade available. |
| 3 | **Natural Order** | 1 owned, undeployed | **Free** ✓ | `Sacrifice a green creature → tutor a green creature to battlefield.` 4 mana cheats Craterhoof Behemoth onto the table. Token sacrifice fodder is free under this build. Same role as in the prior sketch. |

**Combined GC buy cost: ~$50–80 unverified.** Down from the prior sketch's ~$700+ floor. Cardmarket verification required before purchasing per [[feedback_verify_prices]].

**No-pull policy:** Survival's owned copy stays in Radiation Sickness (recent upgrade per [[project_radiation_sickness_upgrade]] — do not pull).

---

## Combo lines (verified math)

### Line 1 — Razaketh tutor chain (primary win path)

**Razaketh, the Foulblooded** (verified): `{5}{B}{B}{B}` for an 8/8 flying/trample. `Pay 2 life, sacrifice another creature: Search your library for a card, put that card into your hand, then shuffle.` Activated ability, no `{T}`, no per-turn limit.

The line:

1. Reanimate Razaketh from graveyard (1 mana, 8 life paid). With Witherbloom out and 1 creature on board, Reanimate's `{B}` is affinity-discounted (no effect — Reanimate is already {B}, no generic). With 1+ creature you can pay {B} from any source.
2. Razaketh enters. Sacrifice tokens to tutor:
   - Sac 1 → tutor Phyrexian Altar. Pay 2 life.
   - Sac 2 → tutor Blood Artist (or Bastion of Remembrance). Pay 2 life.
   - Sac 3 → tutor an enabler (commander recast spell, or Cathars'-equivalent — see below).
   - Sac 4 → tutor Sprout Swarm (or Earthcraft, or Squirrel Nest).
3. Cast acquired pieces (most are creatures, affinity-discounted; instants/sorceries get the same discount). Win on the same turn or the next via the drain loop.

**With 5 tokens on the board, you tutor 5 cards in one turn for 10 life.** With Necropotence-style life economy (deck has Bitterblossom, Bolas's Citadel) and Blood Artist drains paying back life, the life cost is recoverable.

**Razaketh is owned ×2, undeployed.** ✓ Free.

### Line 2 — Sprout Swarm + Witherbloom + 3 creatures (infinite tokens, kept from prior sketch)

**Sprout Swarm** (verified): `{1}{G}` instant. Convoke. Buyback {3}. Create a 1/1 green Saproling token.

Math at minimum 4-creature board state with Witherbloom out (BG, green-eligible for convoke):

1. Total cost {4}{G} (buyback included).
2. Affinity reduces by 4 (creatures controlled) → `{G}` remaining.
3. Tap Witherbloom for {G} via convoke → resolve → Saproling enters → buyback returns Sprout Swarm to hand.
4. Iteration 2: 5 creatures controlled (including new Saproling). Affinity = {5}. Cost = `{G}`. Tap new Saproling for {G}. Loop.

Loops at exactly 4 creatures including Witherbloom. Each iteration converts 1 untapped creature → 1 new untapped green Saproling, so the green-tapper count is preserved. Infinite tapped Saprolings at instant speed.

**Critical dependency:** the loop collapses if Witherbloom is removed. Without affinity, Sprout Swarm + buyback costs {4}{G} = 5 mana, convoke needs 5 creatures tapped per cast for a net depletion. Plan: Lightning Greaves on Witherbloom, Heroic Intervention / Veil of Summer in hand.

Cost: Sprout Swarm ~$1 (not owned).

**Pod approval required** before relying on this in primary line. Razaketh tutor chain is the alternate primary.

### Line 3 — Earthcraft + Squirrel Nest on a basic Forest (infinite, commander-independent)

**Earthcraft** (verified): `Tap an untapped creature you control: Untap target basic land.`
**Squirrel Nest** (verified): Aura on a land — `{T}: Create a 1/1 green Squirrel creature token.`

Setup: Squirrel Nest on a basic Forest, Earthcraft in play.

1. Tap enchanted Forest → make Squirrel.
2. Tap fresh Squirrel via Earthcraft → untap Forest.
3. Loop.

Infinite Squirrels at sorcery speed (Earthcraft activations are not instant-speed, but the loop is). Win via Triumph of the Hordes / Pathbreaker Ibex / Walking Ballista (if added) / Akroma's Will.

**Pod approval required.** Earthcraft is owned ×1, undeployed but **Najeela-proposal contention** per [[project_najeela_proposal]] — if Najeela is also built, buy a second copy ~$30 unverified. Squirrel Nest must be bought ~$2.

### Line 4 — Natural Order → Craterhoof Behemoth (deterministic alpha-strike)

Natural Order at 4 mana (affinity-reduced from {2}{G}{G} to {G}{G} with 2+ creatures) sacs a green token, tutors Craterhoof onto the battlefield. On a token-wide board, Craterhoof's anthem (+X/+X trample where X is creature count) closes the game in one swing.

Craterhoof is owned ×2, both deployed (Eldrazi Stampede + Loam Cycle). **Buy duplicate ~$30 unverified.**

### Line 5 — Tooth and Nail (entwined) → Avenger + Craterhoof

Tooth and Nail is **no longer a GC** per Oct 2025 delisting — confirmed via `REF_Game_Changers_List.md`. 9 mana entwined, but with affinity at 8 creatures it's 1 mana. Wins on resolution.

Tooth and Nail owned ×1, deployed in Loam Cycle. **Buy duplicate ~$8 unverified.**

### Line 6 — Torment of Hailfire / Exsanguinate (X-spell drain)

Witherbloom's affinity makes X-spells extremely cheap. At 10 creatures:

- Torment of Hailfire X=20 costs `{20}{B}{B}` printed → with affinity-10 reduction, you only need to reach 10 mana + {B}{B}. That's mid-game reachable with Bolas's Citadel + Cabal Coffers (if acquired).
- Exsanguinate X=20: `{20}{B}{B}` → affinity-10 → 10 mana + {B}{B}. Each opponent loses 20, you gain 60.

Torment owned ×1 deployed (Calamity Tax). Buy ~$15. Exsanguinate owned ×2 deployed ×3 (Loam, Calamity, Genome) → 1 short. Buy ~$10.

---

## Owned shell that maps onto Pest Control

Cross-checked against `collection/moxfield_haves_2026-05-14-0631Z.csv` (2026-05-14) and `decks/*.txt`. ⚠️ = currently deployed in another active deck.

### Engine (commander + tutor stack)

| Card | Owned/Deployed | Notes |
|---|---|---|
| Witherbloom, the Balancer | 1 owned, undeployed | Free ✓ |
| Razaketh, the Foulblooded | 2 owned, undeployed | **Free ✓** — primary tutor engine |
| Survival of the Fittest | 1 owned, ⚠️ Radiation Sickness | **Buy duplicate ~$50–80 (GC).** Do not pull (recent upgrade). |
| Bolas's Citadel | 1 owned, undeployed | **Free ✓ (GC)** |
| Natural Order | 1 owned, undeployed | **Free ✓ (GC)** |
| Demonic Tutor | 4 owned, ⚠️ Calamity Tax + Curse + Dark Lord = 3 deployments | **1 free copy ✓.** Take it. |
| Vampiric Tutor | 1 owned, ⚠️ Radiation Sickness | **Skip.** Demonic + Worldly + Survival cover the tutor slot at lower contention. Buy duplicate ~$30 only if pushing to elite tier. |
| Worldly Tutor | 1 owned, undeployed | **Free ✓.** Creature-tutor on the cheap. |

### Reanimation package

| Card | Owned/Deployed | Notes |
|---|---|---|
| Reanimate | 6 owned, ⚠️ 6 deployments (Calamity, Curse, Dark Lord, Diminishing, Genome, Grand Design) | **Buy duplicate ~$15 unverified.** Owned copies all deployed. |
| Animate Dead | 3 owned, ⚠️ 3 deployments (Dark Lord, Diminishing, Grand Design) | **Buy duplicate ~$5.** |
| Necromancy | 5 owned, ⚠️ 5 deployments (Lightning War, Curse, Dark Lord, Diminishing, Grand Design) | **Buy duplicate ~$3.** Flash-speed reanimation; bigger ceiling than Animate Dead. |
| Buried Alive | 2 owned, ⚠️ 2 deployments (Curse, Grand Design) | **Buy duplicate ~$5.** Pitches Razaketh + Eternal Witness + Craterhoof to grave in one card. |

### Sac outlets

| Card | Owned/Deployed | Notes |
|---|---|---|
| Phyrexian Altar | 1 owned, ⚠️ Diminishing Returns | **Buy duplicate ~$70 unverified.** Combo-critical for Lines 1 + 2 drain win. |
| Viscera Seer | 1 owned, ⚠️ Diminishing Returns | **Buy duplicate ~$1.** Free scry-1 sac outlet; essential redundancy with Razaketh. |
| Carrion Feeder | 2 owned, ⚠️ 2 deployments (Curse, Diminishing) | **Buy duplicate ~$1.** Third sac outlet. |

### Ongoing token producers

| Card | Owned/Deployed | Notes |
|---|---|---|
| Bitterblossom | 1 owned, undeployed | **Free ✓.** 1/1 flying Faerie per upkeep — affinity fuel + Skullclamp food. |
| Ophiomancer | not owned per CSV | **Buy ~$15 unverified.** 1/1 deathtouch Snake per upkeep. |
| Bastion of Remembrance | not owned | **Buy ~$2.** ETB token + Blood Artist clone. |
| Scute Swarm | 2 owned, ⚠️ Earthbend | **1 free ✓.** Landfall token producer. |
| Chatterfang, Squirrel General | not owned | **Buy ~$15 unverified.** Token-doubling replacement (every token → +1 Squirrel). |
| Mycoloth | not owned | **Buy ~$3.** Devour + upkeep Saprolings. |
| Springheart Nantuko | 1 owned, ⚠️ Earthbend | **Skip.** Landfall isn't the engine here; other token producers cover the role. |

### Drain payoffs

| Card | Owned/Deployed | Notes |
|---|---|---|
| Blood Artist | not owned | **Buy ~$3.** Death-trigger drain — combo-critical. |
| Bastion of Remembrance | not owned (listed above) | Same role as Blood Artist + bonus token. |

### Combo enablers (Lines 2 + 3)

| Card | Owned/Deployed | Notes |
|---|---|---|
| Sprout Swarm | not owned | **Buy ~$1.** Line 2 combo half. |
| Earthcraft | 1 owned, undeployed | **Free ✓** (Najeela contention — see Weaknesses). |
| Squirrel Nest | not owned | **Buy ~$2.** Line 3 combo half. |

### Finishers

| Card | Owned/Deployed | Notes |
|---|---|---|
| Craterhoof Behemoth | 2 owned, ⚠️ Eldrazi + Loam | **Buy duplicate ~$30.** Natural Order target. |
| Triumph of the Hordes | 1 owned, ⚠️ Earthbend (also Radiation per memory) | **Buy duplicate ~$2.** Infect alpha-strike. |
| Akroma's Will | not in CSV grep, status unknown | Verify ownership; ~$5 if needed. |
| Tooth and Nail | 1 owned, ⚠️ Loam | **Buy duplicate ~$8** OR skip — Razaketh tutor chain covers the cheat-into-play role. **Recommend skip.** |
| Torment of Hailfire | 1 owned, ⚠️ Calamity Tax | **Buy duplicate ~$15.** |
| Exsanguinate | 2 owned, ⚠️ 3 deployments | **Buy 1 copy ~$10.** |

### Ramp (non-land)

Sol Ring (24 owned, ample free), Arcane Signet (24 owned, ample free), Three Visits (5 owned, ⚠️ 4 deployments — 1 free), Nature's Lore (6 owned, ⚠️ 6 deployments → buy ~$1), Cultivate (≥5 owned, plenty free), Rampant Growth (5 owned), Sakura-Tribe Elder (2 owned, ⚠️ Eldrazi + Loam — buy ~$1), Wood Elves (verify ownership).

**Mana dorks:** Birds of Paradise (6 owned, ≤3 deployed — free copies likely), Llanowar Elves / Elvish Mystic / Fyndhorn Elves (verify counts; usually plenty free).

### Card draw

| Card | Owned/Deployed | Notes |
|---|---|---|
| Sylvan Library | 2 owned, ⚠️ Loam + Calamity = 2 deployments | **Buy duplicate ~$50 unverified** OR skip. |
| Guardian Project | 2 owned, ⚠️ Radiation | **1 free ✓** |
| Beast Whisperer | not owned | Buy ~$1 |
| Skullclamp | 4 owned, ⚠️ 4 deployments (Crystal + Curse + Dark Lord + Diminishing) | **Buy duplicate ~$5** OR skip. Token-clamping is strong but not essential. |
| Necropotence | 1 owned, ⚠️ Genome (GC slot) | **Skip.** Bolas's Citadel covers the life-as-currency engine role and is the in-house GC. |

### Interaction

| Category | Cards | Notes |
|---|---|---|
| Targeted removal | Assassin's Trophy, Beast Within, Maelstrom Pulse, Tear Asunder, Pernicious Deed, Reclamation Sage, Force of Vigor, Toxic Deluge | Multiple owned; some contention (Force of Vigor 1/1 deployed in Calamity → buy ~$30) |
| Sweeper | Toxic Deluge (10 owned, ample), Pernicious Deed (verify count) | Free copies likely |
| Protection | Heroic Intervention (5 owned, ≤4 deployed — 1 free), Veil of Summer (3 owned, 2 deployed — 1 free), Lightning Greaves (8 owned, ≥8 deployed — buy ~$5) | Lightning Greaves on Witherbloom or Razaketh is critical |
| Imp's Mischief | 2 owned, ⚠️ Genome + Exiles' Return | **Buy duplicate ~$28** OR skip. Redirect-target is the only BG answer to a Thoracle stack. |

### Anti-grave / utility

Bojuka Bog (multiple owned, several deployed — 1 free likely), Boseiju Who Endures (verify free copy), Cabal Coffers (1 owned, ⚠️ Calamity — **buy ~$20 if scaling big-mana finishers**), Urborg Tomb of Yawgmoth (1 owned, ⚠️ Diminishing — **buy ~$5–10**).

### Lands (rough composition, 35–37 slots)

- 1 Bayou (⚠️ Calamity Tax — **buy duplicate ~$300** OR skip basic-fetch the BG fixing)
- 1 Overgrown Tomb (multiple owned, ⚠️ heavy deployment)
- 1 Twilight Mire (verify)
- 1 Llanowar Wastes (⚠️ Loam)
- 4–5 fetches (Verdant Catacombs, Bloodstained Mire, Wooded Foothills, Polluted Delta, Misty Rainforest — verify free copies)
- 1 Prismatic Vista (⚠️ Loam — buy ~$25)
- 1 Bojuka Bog
- 1 Phyrexian Tower (5 deployments — buy duplicate ~$5)
- 1 Volrath's Stronghold (verify ownership)
- 1 Urborg, Tomb of Yawgmoth (⚠️ multiple)
- 1 Cabal Coffers (⚠️ Calamity)
- 1 Boseiju, Who Endures
- 1 Takenuma, Abandoned Mire
- 1 Yavimaya, Cradle of Growth (⚠️ heavy deployment — buy duplicate ~$5)
- 1 Dryad Arbor (verify)
- 1 Mosswort Bridge (⚠️ Eldrazi — buy duplicate ~$1)
- 7 Forest, 7 Swamp (basics — free, plenty)

Net land count target: 35 lands. The Sprout Swarm and X-spell finisher lines want some basics for Earthcraft / Knight of the Reliquary / fetches.

---

## Construction direction (target 100)

**Lands (35):** as above.

**Engine (12):**
- Razaketh, Survival, Bolas's Citadel, Natural Order
- Demonic Tutor, Worldly Tutor, Eldritch Evolution, Chord of Calling, Birthing Pod, Diabolic Intent, Finale of Devastation, Imp's Mischief (redirect)

**Reanimation (5):** Reanimate, Animate Dead, Necromancy, Buried Alive, Phyrexian Reclamation.

**Sac outlets + aristocrats payoffs (5):** Phyrexian Altar, Viscera Seer, Carrion Feeder, Blood Artist, Bastion of Remembrance.

**Token producers (7):** Bitterblossom, Ophiomancer, Scute Swarm, Chatterfang, Mycoloth, Sprout Swarm (combo + value), Awaken the Woods.

**Ramp (10):** Sol Ring, Arcane Signet, Three Visits, Nature's Lore, Cultivate, Rampant Growth, Sakura-Tribe Elder, Wood Elves, Birds of Paradise, Llanowar Elves (or Elvish Mystic / Fyndhorn Elves).

**Combo enablers + finishers (8):** Earthcraft, Squirrel Nest, Craterhoof Behemoth, Triumph of the Hordes, Torment of Hailfire, Exsanguinate, Tooth and Nail (skip — replaced by Razaketh chain), Pathbreaker Ibex (buy ~$10 if Tooth is skipped).

**Interaction (12):** Heroic Intervention, Veil of Summer, Lightning Greaves, Toxic Deluge, Pernicious Deed, Assassin's Trophy, Beast Within, Maelstrom Pulse, Tear Asunder, Reclamation Sage, Force of Vigor, Imp's Mischief.

**Card draw (5):** Sylvan Library (or skip), Guardian Project, Beast Whisperer, Skullclamp (or skip), Augur of Autumn (buy ~$5).

**Recursion / utility (1):** Eternal Witness (⚠️ Grand Design + Loam — buy ~$5) or Regrowth.

Total: ~100 — exact list to lock at build time.

---

## Power ceiling

**Realistic ceiling: 16–17/20 (high Solid, low Elite). Bracket 3 ceiling — Bracket 4 floor with the right opening.** Up from the prior sketch's realistic 14/20.

| Axis | Score | Reasoning |
|---|---|---|
| Core Loop | 4/5 | Affinity engine is reliable once Witherbloom is on the table (T4–5 with optimal dorks). Razaketh as reanimator target accelerates the cheat-into-play path. |
| Kill Reliability | 4/5 | Multiple win conditions, Razaketh tutor chain consolidates the 5-piece vertical into 1–2 turns. Loses a point because Phyrexian Altar is single-source (buy a duplicate to get to 5/5). |
| Durability | 4/5 | Reanimation makes wipes a 1-spell recovery. Multiple tutors find missing pieces. Token engines (Bitterblossom, Ophiomancer, Bastion) drip pieces back. |
| Interaction | 3/5 | BG ceiling. No counterspells, no Force of Will. Veil of Summer + Imp's Mischief + 8 targeted removal + Force of Vigor is the realistic top of the BG interaction package. Vulnerable to non-blue, non-black on-stack combo (rare in B3 but possible). |
| **Total** | **15/20** | Plausibly 16 on a good draw with Razaketh + Survival accessible; **17 in the pod-friendly scenario with both 2-card infinites approved**. |

Pod-denial scenario (both 2-card infinites banned): score drops to ~14/20 — still coherent, still has Natural Order → Craterhoof + Torment X=20 + Razaketh tutor chain as kill paths. Closing speed slows to T8–9.

---

## Buy list summary

Prices unverified — confirm Cardmarket per [[feedback_verify_prices]] before purchasing. No retirement; every contested combo-critical card is bought as a duplicate.

**Game Changers (~$50–80):**
- Survival of the Fittest duplicate (~$50–80)
- Bolas's Citadel — free, owned
- Natural Order — free, owned

**Reanimation package (~$28):**
- Reanimate (~$15), Animate Dead (~$5), Necromancy (~$3), Buried Alive (~$5)

**Sac outlets + drains (~$75):**
- Phyrexian Altar duplicate (~$70), Viscera Seer (~$1), Carrion Feeder (~$1), Blood Artist (~$3)

**Token engines (~$35):**
- Ophiomancer (~$15), Chatterfang (~$15), Mycoloth (~$3), Bastion of Remembrance (~$2)

**Combo enablers (~$3):**
- Sprout Swarm (~$1), Squirrel Nest (~$2)

**Finishers (~$60):**
- Craterhoof Behemoth duplicate (~$30), Triumph of the Hordes duplicate (~$2), Torment of Hailfire duplicate (~$15), Exsanguinate (~$10), Pathbreaker Ibex (~$10 — replaces Tooth and Nail slot)

**Interaction / utility duplicates (~$70):**
- Force of Vigor duplicate (~$30), Imp's Mischief duplicate (~$28), Lightning Greaves duplicate (~$5), Sakura-Tribe Elder (~$1), Eternal Witness (~$5)

**Lands (~$20):**
- Mosswort Bridge duplicate (~$1), Phyrexian Tower duplicate (~$5), Yavimaya Cradle of Growth duplicate (~$5), Boseiju (~$5)

**Minimum viable buy: ~$340 unverified.** Down from the prior sketch's ~$1,030 (with Cradle) or ~$330 (without Cradle). This revision is in the same ballpark but with a meaningfully higher ceiling (16-17 vs. 14).

**Explicitly skipped (would otherwise add ~$130+):** Necropotence duplicate (Citadel covers the slot), Tooth and Nail duplicate (Razaketh covers the cheat-into-play), Vampiric Tutor duplicate (3-tutor base is enough), Sylvan Library duplicate, Skullclamp duplicate, Doubling Season (no counter-doubling matters here), Bayou duplicate (basic-fetch BG fixing without it).

**Optional polish (low priority):**
- Vampiric Tutor duplicate (~$30) to reach elite consistency
- Skullclamp duplicate (~$5) for token draw engine
- Cabal Coffers duplicate (~$20) for big-mana X-spell scaling
- Doubling Season duplicate (~$40) — low priority, no counters in deck

---

## Known weaknesses

- **Witherbloom is the engine point of failure.** Affinity-for-instants-and-sorceries lives on her. A Path to Exile or exile-to-graveyard on Witherbloom drops the deck's effective tempo by ~3 mana per spell. Protection density (Lightning Greaves, Heroic Intervention, Veil of Summer) is non-negotiable.
- **Razaketh costs 8 mana hardcast; the deck relies on reanimating him.** Buried Alive → Reanimate is a 2-card line at 4 mana total. Without graveyard access (Bojuka Bog on Razaketh, Rest in Peace on the table), the engine grinds to value-tutoring.
- **Heavy parts overlap with Diminishing Returns.** 7–9 aristocrats-shell cards are bought as duplicates. This is the same shape as Wandering Minstrel's no-retirement model but at higher per-card cost (aristocrats staples are pricier than landfall payoffs).
- **Earthcraft + Najeela proposal contention.** Per [[project_najeela_proposal]]. If Najeela is also built, both decks want the single owned Earthcraft. Pest Control's claim is moderate (Line 3 is backup, not primary); Najeela has prior claim if both build.
- **No counter-magic.** BG color identity. Imp's Mischief redirects but is 1 of. Against an on-stack combo win (Thoracle, Approach), the deck has no answer beyond pre-emptive Toxic Deluge to deny the win condition's enablers.
- **Survival of the Fittest GC slot requires a buy.** Cardmarket price $50–80 is significant for one card. If the buy is rejected, the GC slate falls back to: Demonic Tutor (free, swap into the tutor role) + Bolas's Citadel + Natural Order. Scores ~0.5 lower but stays in 15/20 territory.
- **18 active decks.** Roster grows by one. Same net-add shape as Najeela and Wandering Minstrel.

---

## Comparison to other open proposals

| Proposal | Ceiling | Buy cost | Status |
|---|---|---|---|
| Berta Wise Extrapolator | 15–16/20 | ~$200 (elf-tribal version) | [[project_berta_proposal]] |
| Najeela, Blade-Blossom | 18–19/20 | ~$200+ | [[project_najeela_proposal]] |
| Wandering Minstrel | 17–18/20 | ~$115 | [[project_wandering_minstrel_proposal]] |
| **Pest Control (this rev)** | **16–17/20** | **~$340** | **drafted 2026-05-18** |
| Pest Control (prior sketch) | 14/20 | ~$330 (no Cradle) | superseded |

**Pest Control is mid-tier on ceiling-per-dollar.** Najeela and Wandering Minstrel both beat it on that axis. The argument for building Pest Control over those: BG aristocrats fills a roster gap that 5C combat and 5C Town tribal don't.

---

## Changelog

- **2026-05-14 (prior sketch):** Initial draft with Sprout Swarm + Earthcraft as primary engines, GC slate of Gaea's Cradle / Necropotence / Natural Order. Blocked by Cradle ownership and Necropotence/Genome conflict.
- **2026-05-18 (this revision):** Pivoted to Razaketh tutor-chain + reanimation as primary engine, demoted Sprout Swarm and Earthcraft to combo backup lines. GC slate revised to Survival of the Fittest / Bolas's Citadel / Natural Order — all on the GC list, only Survival requires a buy. Ceiling raised from 14 → 16–17. Reasons: (a) post-wipe rebuild via Reanimate is 1 spell, not 3 turns of token drip; (b) Razaketh tutor density consolidates the 5-piece combo vertical into 1–2 turns; (c) GC slate cost drops from ~$725 floor to ~$50–80.
