# Croak and Dagger — Glarb, Calamity's Augur

## Quick Reference

| Field | Value |
|---|---|
| **Commander** | Glarb, Calamity's Augur ({B}{G}{U}, 2/4 Frog Wizard Noble) |
| **Colors** | Sultai (BUG) |
| **Archetype** | Lands-matter / big mana → X-drain + reanimator (grind-fortress, anti-Ur-Dragon) |
| **Bracket** | 3 (3 Game Changers; no infinite combos; no MLD; no extra turns) |
| **Game Changers** | Seedborn Muse, Fierce Guardianship, Demonic Tutor (3 of 3 slots used) |
| **Conversion Check** | **18/20** (5/4/4/5) |
| **Kill Window** | **Clock (lab, realistic Glarb dig=2): ~T10 decap / ~T11 table** **(spell; instant if Seedborn + flash enabler)**. Mana-gated — fast once Seedborn is online but **cannot out-race the T6–7 combo pod** (pure-race ~11%, P(beat pod) ~20% via `pod_gauntlet`). The old Summary "T7–9" was falsified; this deck wins by **grinding + disrupting**, not racing. Re-roled 2026-06-15 → the pod's **anti-Ur-Dragon specialist** (Thoracle line dropped — Hashaton owns it): `scripts/vs_dragon_lab.py` puts it ~**87% heads-up vs Ur-Dragon by archetype** (flying-agnostic wraths + Maze + recursion + board-independent drain), the fog/removal package being +2–3pp insurance, not the win. Caveat: 87% is a heads-up goldfish ceiling, and Glarb is the *worst* deck vs his **combo** decks (~5% in the gauntlet). 3/3 GCs. Labs: `ct_speed_lab.py --mode clock/croak/gary`, `vs_dragon_lab.py`, `pod_gauntlet.py`. |

-----

## Commander Rules Text

Glarb, Calamity's Augur {B}{G}{U}
Legendary Creature — Frog Wizard Noble (2/4)

- Deathtouch
- You may look at the top card of your library any time.
- You may play lands and cast spells with mana value 4 or greater from the top of your library.
- {T}: Surveil 2.

Key rulings: Normal timing rules apply — lands only during your main phase, sorceries at sorcery speed unless a flash enabler is in play. Instants with MV4+ can be cast from the top at instant speed naturally. The surveil 2 is a tap ability with no mana cost. Glarb costs only {B}{G}{U} (3 mana), making him trivially cheap to recast at 5, 7, 9.

-----

## What the Deck Does

The deck ramps aggressively into a massive land count, uses Glarb's top-of-library engine to convert that mana into free spells and card advantage, then kills the table with a scaling X-drain (Torment of Hailfire) or a burst copy/reanimator line (kicked Rite of Replication on a drainer). Seedborn Muse transforms Glarb from a once-per-turn engine into a once-per-opponent's-turn engine, and flash enablers let the deck cast MV4+ sorceries on any player's turn.

### Layer 1 — Ramp / Lands Engine (20+ pieces)

The deck runs 39 lands plus 20+ ramp pieces that aggressively accelerate land count. Extra land drop creatures (Exploration, Azusa, Oracle of Mul Daya, Icetill Explorer) stack with Glarb's ability to play lands from the top, enabling 3–4 land drops per turn. Land tutors (Farseek, Nature's Lore, Three Visits, Skyshroud Claim, Hour of Promise, Open the Way, Tempt with Discovery, Pir's Whim, Sowing Mycospawn, Titania's Command, Omenpath Journey, Planar Genesis) ensure consistent ramp. Nissa Resurgent Animist and Lotus Cobra generate mana on landfall. Cabal Coffers + Urborg, Tomb of Yawgmoth produces 12–20+ black mana from a single land tap in the mid-to-late game.

### Layer 2 — Top-of-Library Value Engine

Glarb's {T}: Surveil 2 sculpts the top of the library, clearing sub-4 MV cards and positioning lands or big spells for free casting. **Seedborn Muse** (Game Changer) transforms this: Glarb untaps during each opponent's untap step, allowing surveil 2 on every player's turn — four activations per turn cycle in a 4-player game. With flash enablers (Valley Floodcaller, Alchemist's Refuge), MV4+ sorceries can also be cast on opponents' turns.

Valley Floodcaller has two distinct roles. First, it is a full flash enabler — "You may cast noncreature spells as though they had flash" — allowing MV4+ sorceries from the top on any turn independently of any other enabler. Second, every noncreature spell cast untaps all Birds, Frogs, Otters, and Rats you control (and gives them +1/+1). Since Glarb is a Frog, each noncreature spell untaps him for another surveil 2, enabling chains through the library on a single turn.

### Layer 3 — The Copy Payoff (Rite of Replication)

The 2026-06-15 re-role cut the wide copy package (Doppelgang, Mirrorform, Flash Photography, Espers to Magicite, Starfield Vocalist) in favour of the grind-fortress shell, so **Rite of Replication is now the deck's single copy effect** — and it's a finisher, not value. Kicked (9 mana, one Coffers tap) it makes five token copies of a creature already on the battlefield; on the deck's drainers that is lethal:

- **on Gray Merchant of Asphodel** — the five copies count each other's black pips, so each of the five ETBs sees ~11–13 devotion → **~60 per opponent** (the lab's most frequent copy kill — see How We End Games).
- **on Kokusho, the Evening Star** — five legendary copies die at once to the legend rule → **25 per opponent**, devotion-independent.

Unkicked (4 mana) it's a flexible single copy — a second Lumra / Oracle of Mul Daya / Archon when grinding value is what the turn needs.

### Layer 4 — The Coffers Engine

Cabal Coffers taps for {B} equal to the number of Swamps you control. Urborg, Tomb of Yawgmoth makes all lands Swamps in addition to their other types. Yavimaya, Cradle of Growth makes all lands Forests. With 12+ lands in play (typical by turn 6–7), Coffers produces 12+ mana from a single land. This directly fuels Torment of Hailfire kills and pays for kicked Rite of Replication in one tap.

-----

## Kill Lines

### Kill Line 1 — Torment of Hailfire (Primary)

**Cost:** {X}{B}{B} (MV = X+2, castable from top via Glarb at X≥2). **Cards needed:** Just Torment + mana.

With Cabal Coffers + Urborg + 10 other lands = tap Coffers for 12+ mana. Torment at X=12 means each opponent faces 12 iterations of "lose 3 life, sacrifice a nonland permanent, or discard a card." Against a typical mid-game board (5 nonlands, 3 cards in hand, 30+ life), this forces: sacrifice 5 + discard 3 + lose 12 life from the remaining 4 iterations = lethal for most opponents. At X=15+ (very achievable), the table dies regardless of board state.

This is the primary kill because it converts the deck's core strength (massive mana production) directly into a win without requiring any other cards on board. Demonic Tutor finds it. Glarb can cast it from the top. One card, one turn, game over.

### Kill Line 2 — Kicked Rite of Replication on a drainer

**Cost:** kicked Rite (9 mana, one Coffers tap) + a drainer on the battlefield. **Best target: Gray Merchant of Asphodel** (~60 per opponent — lethal from full); fallback **Kokusho** (25 per opponent, devotion-free).

The five token copies are all on the battlefield *before* any ETB resolves, so each counts the other four. On **Gray Merchant** that means each of the five ETBs sees ~11–13 devotion to black (4 copies × 2 pips + Glarb + incidentals) → ~11–13 × 5 ≈ **60 per opponent**, one-shotting a full table. On **Kokusho**, five legendary copies die at once to the legend rule → **25 per opponent** — smaller, but needs no devotion and works straight from the graveyard.

Cleanest line: Glarb's surveil bins Gary, **Reanimate** (1) returns him, **kicked Rite** (9) one-shots the table — ~10 mana, two cards. Demonic Tutor / GSZ / Chord / Finale all assemble the missing half.

> **Lab note (2026-06-23, `ct_speed_lab --mode gary`):** the Gray + Rite line is the **closer in ~45% of modelled kills**; removing Gray drops the kill rate 86% → 78% and pushes both clocks out a turn (decap T10→T11, table T11→T12). So Gary *is* pulling real weight — but **only through Rite**: it's a 2-card, ~10-mana combo, and a bare Gray Merchant is a 5-mana 2/4 draining ~3–6 (Sultai devotion is low — Glarb is a single black pip). The 45% is a goldfish ceiling; real removal/counters make the 2-card line meaningfully more fragile, and a replacement 2nd X-drain (Exsanguinate) does **not** recover the lost rate because it's redundant with Torment rather than a separate axis.

### Kill Line 3 — Value grind (the Seedborn engine)

No single combo. Seedborn Muse untaps Glarb + all lands on every opponent's turn; with a flash enabler the deck casts 3–4 free MV4+ spells per turn cycle. The table cannot outpace this indefinitely. **Archon of Cruelty** (drain/discard/sac on every ETB *and* attack), **Massacre Wurm** (a -2/-2 sweep that also drains on each opposing creature death), and repeated land drops via Lumra, Nissa, Aesi, and Icetill Explorer grind out wins through accumulated value — and Archon/Massacre Wurm double as the deck's bodies and removal.

-----

## The Finishers & Their Weak Points

The deck closes on **two independent axes**, which is its real strength — kill it on one and the other still operates:

| Axis | Cards | Shape | Needs | Weak to |
|---|---|---|---|---|
| **A — X-drain (primary)** | Torment of Hailfire | Board-independent; mana → life loss | Just the spell + a big Coffers tap | Pure mana-gate (slow); a resolved counter; doesn't care about *their* board |
| **B — copy / reanimator burst** | Kicked Rite on Gray Merchant (~60/opp) or Kokusho (25/opp) | A 2-card combo that one-shots the table | A drainer on the battlefield + kicked Rite (~10 mana) | Spot removal / counter on the kill turn; graveyard hate (kills the Reanimate line); exile of the creature pool |

**Why two axes matters:** Axis A asks *"do they have a counter?"* and Axis B asks *"can they remove a creature or hate the yard?"* — different questions, so a single piece of interaction rarely stops both. Demonic Tutor picks whichever the table is weak to.

**The weak points, plainly:**

- **It's a slow clock.** Lab decap median ~T10 (table ~T11) — the deck **cannot out-race the T6–7 combo pod** (pure-race ~11%, P(beat pod) ~20%). It wins by *grinding and disrupting*, not racing. This is by design (the anti-Ur-Dragon re-role), but it means against a fast combo deck you are leaning on the counter suite, not your own clock.
- **The finisher creature pool is thin** — Gray, Kokusho, Archon, Massacre Wurm (4 cards). Exile effects (Swords, Path, Farewell) that hit two of them gut Axis B; Torment is the resilience answer because it needs no creatures.
- **Axis B is a 2-card combo.** Gary/Kokusho do ~nothing alone (a bare Gary drains ~3–6 in this low-devotion Sultai shell). Both halves are tutorable and Glarb digs hard, so it shows up often — but it is interactable on the kill turn in a way Torment isn't.
- **Graveyard hate is the single worst card against us** (Rest in Peace, Dauthi Voidwalker) — it shuts off Reanimate, Noxious Revival, Lumra's land return, and Icetill Explorer at once. Answers: Force of Vigor, Boseiju, Beast Within.
- **Telegraphed kills.** A 12+ land board with Coffers + Urborg screams "Torment next turn." Don't announce it — let it resolve.

-----

## Conversion Check — 18/20

### Core Loop: 5/5

The engine is the deck. 20+ ramp/lands cards directly serve the core loop. Seedborn Muse transforms Glarb from once-per-turn to once-per-opponent's-turn, creating 3–4 surveil cycles and potential free casts per turn rotation. With a flash enabler in play, every opponent's turn becomes: untap Glarb → surveil 2 → if MV4+ spell on top, cast it → check new top → potentially play a land or cast another spell.

Extra land drops (Exploration, Azusa, Oracle of Mul Daya, Icetill Explorer) + land tutors (10+ pieces) + top-of-library casting (Glarb) + Seedborn untaps = a coherent machine that's hard to fully disrupt. Even without Glarb, the ramp package independently produces 10+ lands by turn 7, and the big spells can be hardcast.

Valley Floodcaller provides the chain mechanic: each noncreature spell untaps Glarb (Frog type) → surveil 2 → new top → potentially another spell → untap again. On a good turn, this chains through 3–4 cards.

*Checkpoint: Cover the commander. The 99 has Exploration, Azusa, Oracle of Mul Daya, Icetill Explorer, 10+ land tutors, Seedborn Muse, Rite of Replication, Torment of Hailfire, Cabal Coffers. The strategy is unmistakable: "produce massive mana, play threats from the top, drain the table."*

### Kill Reliability: 4/5

Two independent closing axes (see *The Finishers & Their Weak Points*), at least one fast from engine-online. Torment of Hailfire at X=12+ is a one-card kill that needs only mana — the deck's core product. Kicked Rite of Replication on Gray Merchant (~60/opp) or Kokusho (25/opp) is a 2-card burst (~10 mana via Reanimate + kicked Rite). Demonic Tutor ensures the right closer is found when needed.

From engine-online (10+ lands, approximately turn 6–7), the deck kills in 1–2 turns with either Torment (needs Coffers mana + the spell) or Kokusho + Rite (needs 2 specific cards). Three free counterspells protect the kill turn.

Docked from 5 because every kill line requires either massive mana accumulation (Torment needs X=12+ for reliability, requiring 14+ total mana) or assembling a specific 2-card combination. No deterministic infinite combo exists. A 5 would need a one-card guaranteed kill or a compact infinite loop.

*Checkpoint: Demonic Tutor → Torment of Hailfire with Coffers + Urborg + 10 lands = table kill. Kokusho in graveyard + Reanimate + kicked Rite = 25 per opponent. Both achievable 1–2 turns from engine-online.*

### Durability: 4/5

Strong structural resilience across multiple dimensions. Glarb costs 3 mana — recastable at 5, 7, 9 without meaningful tempo loss. Land advantage survives every board wipe (39 lands stay on the battlefield). Reanimate and Noxious Revival recover killed creatures. Lumra returns all lands from graveyard to battlefield on ETB. Icetill Explorer replays lands from graveyard with self-mill fueling it. The ramp density (20+ pieces) means the engine rebuilds fast.

Seedborn Muse is a key accelerant but not a hard dependency — without it, the deck functions at reduced speed but the core engine (ramp → Glarb top-casting) still works. The commander is important but trivially cheap to recast. The sheer mass of redundant ramp pieces means no single removal spell derails the plan.

Docked from 5 because the finisher creature pool is thin: Archon, Kokusho, Gray Merchant, Massacre Wurm = 4 cards. If multiple are exiled (Swords, Path, Farewell), the copy line (Rite of Replication) loses its best targets. Torment of Hailfire doesn't need creatures, which provides resilience — but the copy/reanimator burst becomes significantly weaker. Graveyard hate (Rest in Peace, Dauthi Voidwalker) shuts off Reanimate, Noxious Revival, Lumra's land return, and Icetill Explorer simultaneously.

*Checkpoint: Cyclonic Rift on turn 7. Lands stay (39 of them). Recast Glarb for 5 mana. Surveil to find next threat. Noxious Revival puts best card on top for free casting. Threatening again in 1–2 turns.*

### Interaction Profile: 5/5

20 interaction pieces across diverse types and timings:

**Counterspells (5, including 3 free):** Fierce Guardianship (free with commander), Force of Negation (free with blue card), Pact of Negation (free, pay 5 on upkeep), Mana Drain ({U}{U}, generates mana), Swan Song ({U})

**Free/Cheap Removal (4):** Deadly Rollick (free with commander), Force of Vigor (free with green card), Submerge (free if opponent has Forest), V.A.T.S. (split second, destroys any number of creatures with equal toughness)

**Sweepers (3):** Toxic Deluge (scalable, ignores indestructible), Culling Ritual (destroys all MV2- nonlands, generates mana), The Meathook Massacre (scalable -X/-X + ongoing drain)

**Permanent Removal (4):** Beast Within (instant, destroy any permanent — hits a dragon, the Ur-Dragon avatar, or a Rest in Peace), Boseiju Who Endures (channel, uncounterable), Otawara Soaring City (channel bounce), Venser Shaper Savant (flash bounce any spell or permanent)

**Utility Interaction (4):** Bojuka Bog (graveyard exile on ETB), Maze of Ith (neutralizes any attacker), Veil of Summer (protection + draw vs blue/black), Spore Frog (recurring Fog — sac to prevent all combat damage, returns via Reanimate/Muldrotha)

Five counterspells including three that cost zero mana. Four free removal spells. Seedborn Muse untapping all lands on each opponent's turn resolves the develop-vs-hold-up tension completely — the deck holds counterspell mana while continuing to develop via Glarb's top-casting. This is the structural advantage that pushes to 5/5.

*Checkpoint: Opponent about to win with a spell on the stack. Fierce Guardianship (free), Force of Negation (free), Pact of Negation (free), Mana Drain (2 mana), Swan Song (1 mana). Five answers, three of which cost zero mana.*

### Total: 18/20 — Structurally excellent. Pilot skill is the main variable.

| Axis | Score | Key Strength | Limiting Factor |
|---|---|---|---|
| Core Loop | 5 | Seedborn + Glarb = 3–4 activations per turn cycle | — |
| Kill Reliability | 4 | Torment + Coffers = 1-turn kill from engine-online | No deterministic combo; X-kills need massive mana |
| Durability | 4 | 39 lands survive everything; 3-mana commander | Thin finisher creature pool; exile vulnerability |
| Interaction | 5 | 20 pieces including 3 free counters + 4 free removal | — |

-----

## The Path to 19

The intuitive lever — a second X-drain (**Exsanguinate**) for finisher redundancy — was **lab-falsified** (`ct_speed_lab --mode gary`, 2026-06-23): swapping a creature for Exsanguinate left the kill rate flat (78% either way), because a second X-drain is *redundant with Torment* (same mana, same axis), not a new one. The deck already finds Torment reliably via tutors + Glarb dig, so the marginal X-drain adds almost nothing.

The real Reliability lever is **a second distinct burst axis or better protection for the existing one**, not redundancy — e.g. a second copy enabler so the Gray/Kokusho line isn't single-threaded on Rite of Replication, or a way to make the 2-card burst harder to interact with. This is a candidate-search question, held pending a focused lab rather than a named swap.

-----

## Bracket 3 Compliance

**Game Changers (3 of 3 used):**
1. Seedborn Muse — untap all permanents on every opponent's turn
2. Fierce Guardianship — free counterspell with commander in play
3. Demonic Tutor — unrestricted tutor for any card

**Notable non-GC power cards:** Force of Negation, Mana Drain, Pact of Negation, Deadly Rollick, Force of Vigor, Torment of Hailfire, Rite of Replication, Finale of Devastation, Chord of Calling, Green Sun's Zenith, Toxic Deluge, Reanimate, Sylvan Library, The Meathook Massacre, Cabal Coffers

**Infinite combos:** None. All kills are finite (X-spell scaling, copy-based ETB/death triggers, combat damage).

**Extra turns:** None.

**Mass land denial:** None.

-----

## Pod Fit

1. **Converts mana advantage into decisive kills.** Unlike ramp decks that build impressive boards but can't close, Torment of Hailfire and the Kokusho/Rite combo convert mana directly into lethal damage. Left alone past turn 8, this deck wins.
2. **Resilient to creature removal.** The primary kill (Torment) doesn't require any creatures on board. Board wipes help by clearing opponents' boards before a Torment turn.
3. **Punishes tap-out plays.** With Seedborn Muse, the deck holds counterspell mana while developing. Opponents who tap out to advance their plans walk into free counterspells on their combo turns.
4. **Vulnerable to graveyard hate.** Rest in Peace, Leyline of the Void, and Dauthi Voidwalker threaten Reanimate, Noxious Revival, Lumra, and Icetill Explorer. The deck has Force of Vigor, Beast Within, and Boseiju for answers, but a resolved Rest in Peace is painful.
5. **Draws archenemy attention.** A visible 12+ land count with Cabal Coffers and Urborg signals an imminent kill. Manage threat perception — Torment doesn't need to be announced until it's resolving.
6. **Strong against combo.** Five counterspells (3 free) mean the deck credibly threatens to stop any combo win attempt. This is the structural advantage over non-blue ramp strategies.

-----

## Reskin Reference

| Deck Card Name | Original MTG Name | Notes |
|---|---|---|
| Ba Sing Se | Ba Sing Se | ATLA original card — {T}: Add {G}; Earthbend 2 ability; not a reskin of an existing card |
| V.A.T.S. | V.A.T.S. | Fallout original — split second; destroys any number of creatures with equal toughness; not a reskin |

-----

## Decklist (100 cards)

> Re-derived 2026-06-23 from `decks/croak-and-dagger-20260623-215731.txt` (the
> deployed grind-fortress + anti-Ur-Dragon list), replacing the retired V1
> (`…20260405`, archived). Functional buckets feed the dashboard composition bar /
> decklist view.
>
> **2026-06-23 swap: −Lier, Disciple of the Drowned (loaned out) +Aesi, Tyrant of
> Gyre Strait.** Aesi adds an extra land drop each turn + a landfall draw, deepening
> the lands engine. Lab-tested clock-neutral on the kill (`ct_speed_lab --mode croak`,
> 20k @ realistic dig=2): decap median **T10 unchanged**, table tail +4pp (86→90%
> killed by T14) — the gain sits in the T9+ tail, behind the pod's T6–7 kill, so
> `pod_gauntlet` P(WIN) is unchanged. The swap is a lands-engine/refuel upgrade, **not**
> a speed gain. Note: the model can't credit what Lier did (spells-can't-be-countered
> + the only instant/sorcery recursion, i.e. a 2nd Torment from the yard) — that
> protection/recursion axis is **not** restored by Aesi.

### Commander (1)

1 Glarb, Calamity's Augur

### Game Changers (3)

1 Demonic Tutor
1 Fierce Guardianship
1 Seedborn Muse

### Extra Land Drops (4)

1 Exploration
1 Azusa, Lost but Seeking
1 Oracle of Mul Daya
1 Icetill Explorer

### Landfall Payoffs (4)

1 Lotus Cobra
1 Nissa, Resurgent Animist
1 Lumra, Bellow of the Woods
1 Aesi, Tyrant of Gyre Strait

### Land Recursion (5)

1 Crucible of Worlds
1 Life from the Loam
1 Blossoming Tortoise
1 Ramunap Excavator
1 Splendid Reclamation

### Land Tutors / Ramp (12)

1 Farseek
1 Nature's Lore
1 Three Visits
1 Skyshroud Claim
1 Hour of Promise
1 Open the Way
1 Tempt with Discovery
1 Pir's Whim
1 Sowing Mycospawn
1 Titania's Command
1 Omenpath Journey
1 Planar Genesis

### Mana Acceleration (2)

1 Sol Ring
1 Birds of Paradise

### Creature Tutors (3)

1 Green Sun's Zenith
1 Chord of Calling
1 Finale of Devastation

### Card Advantage / Engines (1)

1 Sylvan Library

### Flash Enablers (1)

1 Valley Floodcaller

### Reanimation / Recursion (5)

1 Reanimate
1 Agadeem's Awakening
1 Timeless Witness
1 Noxious Revival
1 Muldrotha, the Gravetide

### Finishers — Reanimation Targets (4)

1 Archon of Cruelty
1 Kokusho, the Evening Star
1 Gray Merchant of Asphodel
1 Massacre Wurm

### X-Spell Finisher (1)

1 Torment of Hailfire

### Copy (1)

1 Rite of Replication

### Counterspells (4)

1 Force of Negation
1 Mana Drain
1 Pact of Negation
1 Swan Song

### Removal / Interaction (9)

1 Beast Within
1 Deadly Rollick
1 Force of Vigor
1 Submerge
1 V.A.T.S.
1 Toxic Deluge
1 Culling Ritual
1 The Meathook Massacre
1 Venser, Shaper Savant

### Fog / Defense (1)

1 Spore Frog

### Protection (1)

1 Veil of Summer

### Lands (38)

1 Bayou
1 Tropical Island
1 Underground Sea
1 Breeding Pool
1 Overgrown Tomb
1 Hedge Maze
1 Undercity Sewers
1 Underground Mortuary
1 Cabal Coffers
1 Urborg, Tomb of Yawgmoth
1 Yavimaya, Cradle of Growth
1 Command Tower
1 Boseiju, Who Endures
1 Otawara, Soaring City
1 Minamo, School at Water's Edge
1 Bojuka Bog
1 Maze of Ith
1 Three Tree City
1 Shifting Woodland
1 Vesuva
1 Mistrise Village
1 Alchemist's Refuge
1 Talon Gates of Madara
1 Dryad Arbor
1 Golgari Rot Farm
1 Ba Sing Se
1 Urza's Cave
1 Horizon of Progress
1 Polluted Delta
1 Flooded Strand
1 Misty Rainforest
1 Verdant Catacombs
1 Marsh Flats
1 Bloodstained Mire
1 Scalding Tarn
1 Wooded Foothills
1 Windswept Heath
1 Forest

-----

## Maybeboard

| Card | Role | Notes |
|---|---|---|
| Exsanguinate | Finisher | Redundant X-drain alongside Torment — lab-falsified as a Reliability lever (no kill-rate gain; same axis as Torment). Low priority. |
| Avenger of Zendikar | Finisher | Creates plant tokens equal to lands. Strong copy target, threatens lethal next combat. |
| Awaken the Woods | Ramp + landfall | Creates X Forest Dryad land creature tokens. Massive landfall burst. |
| Breach the Multiverse | Reanimation | 7 mana — mill everyone 10, reanimate a creature/PW from each graveyard. |
| The Gitrog Monster | Engine | Extra land drop + draw on land sacrifice. Strong with fetchlands. |
| Scapeshift | Land combo | Sacrifice X lands, search X lands. Enables Coffers/Urborg in one spell. |
| Sphinx of the Second Sun | Engine | Extra beginning phase = extra untap + draw. Redundant to Seedborn Muse. |
| Vein Ripper | Finisher + protection | Ward: sacrifice a permanent. Drains on any creature death. |
| Ertai Resurrected | Interaction | Flash creature — counters a spell/ability OR draws a card on ETB. |
| Titania, Protector of Argoth | Token producer | Creates 5/3 elementals when lands die. Pairs with fetchlands. |
| The Scarab God | Reanimation | Exile creatures from any graveyard as 4/4 zombie copies. |
| Faerie Artisans | Copy | Auto-copies opponents' creatures on ETB. |
| Nyxbloom Ancient | Mana | Triples mana production. Win-more but enormous with Coffers. |
| Consuming Tide | Bounce | Mass bounce with surveil synergy. |
| Coiling Rebirth | Recursion | ? |
| Aggressive Biomancy | Copy | ? |
| Lotuslight Dancers | Value | ? |
| Perfect Defense | Protection | ? |
| Reverent Silence | Enchantment removal | Free if opponent controls a Forest. Hits Rest in Peace. |
| Bala Ged Recovery | Recursion | MDFC — Regrowth on front, tapped land on back. |
| Villainous Wrath | Sweeper | ? |

## Don't-Miss Rulings

- **Glarb plays lands and casts MV4+ spells off the top, but normal timing still applies** — lands and sorceries only on your main phase *unless* a flash enabler is out (Valley Floodcaller / Alchemist's Refuge). MV4+ **instants** can be cast off the top at instant speed naturally.
- **Valley Floodcaller does two things:** (1) flash-enables all your noncreature spells, and (2) each noncreature spell **untaps your Frogs — including Glarb** — for another surveil 2, letting you chain through the library in one turn.
- **Seedborn Muse** untaps Glarb and all your lands on *every* opponent's turn — surveil and free casts each turn cycle, and you can hold up counters without skipping development.
- **Cabal Coffers** taps for {B} per Swamp; **Urborg** makes every land a Swamp. 12+ lands = 12+ mana from a single Coffers tap.
- **Kokusho + Rite:** the copies are legendary, all die instantly to the legend rule, each drains 5 → 25 per opponent.
- **Surveil 2 is a free tap ability** — use it to bin sub-4-MV cards so the top of your library stays castable.

## Piloting Notes (for borrowers)

**Mulligan.** Looking for: **lands + ramp** (Sol Ring, signets, land tutors) pointed at 10+ lands, ideally with an extra-land-drop enabler (Exploration / Azusa / Oracle of Mul Daya) and/or Glarb castable on T3.

- **Keep:** ramp-heavy hands; Glarb + fixing; Cabal Coffers + lands.
- **Toss:** spell-heavy no-land hands; a finisher with no mana engine behind it.
- You **do not** need a kill spell in your opener — surveil + ramp will find Torment.

**Threats & timing.**

- **39 lands survive every wipe and Glarb recasts for 3 mana** — board wipes barely slow you, and they clear opponents' boards before a Torment turn.
- **Graveyard hate is the real weakness** (Rest in Peace, Dauthi Voidwalker) — it shuts off Reanimate, Noxious Revival, Lumra, and Icetill Explorer at once. Answers: Force of Vigor, Beast Within, Boseiju.
- **The finisher creature pool is thin** (Archon, Kokusho, Gray Merchant, Massacre Wurm). If they get exiled, the copy kills weaken — lean on Torment, which needs no creatures.
- **Interaction is deep** — 5 counters (3 free) and 4 free removal spells. Hold them up; Seedborn means you don't sacrifice development to do it.
- **Don't announce the kill.** A 12+ land board with Coffers and Urborg telegraphs a Torment turn — let it resolve before anyone realizes.
