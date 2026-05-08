# Eldrazi Stampede Chaos — Maelstrom Wanderer

## Quick Reference

| Field | Value |
|---|---|
| **Commander** | Maelstrom Wanderer ({5}{G}{U}{R}, 7/5 Legendary Creature — Elemental) |
| **Colors** | Temur (GUR) |
| **Archetype** | Ramp / cascade / "huge stuff" — chain free-casts into Eldrazi-flavored beats |
| **Bracket** | 3 (2 Game Changers used; no two-card infinites; no extra turns; no MLD) |
| **Game Changers** | Ancient Tomb, Mana Vault (2 of 3 slots used — room for one more) |
| **Conversion Check** | **14/20** (4/4/3/3) — Solid |
| **Kill Window** | Goldfish: T6–8 · Through interaction: T8–11 |

-----

## Commander Rules Text

Maelstrom Wanderer has two abilities:

1. **Static — "Creatures you control have haste."** Every creature you cheat into play (cascade, Etali, Selvala's Stampede, Aetherworks Marvel, Creative Technique, Sunbird's Invocation, Wildsear cascade) attacks immediately.
2. **Cascade, cascade.** When cast, two separate cascade triggers fire. Each exiles cards from the top of your library until you exile a *nonland* card with mana value strictly less than 8, which you may cast for free. The two triggers resolve independently — the spell from the first cascade resolves before the second cascade exiles cards.

Key reading: cascade requires the resulting spell to have **mana value strictly less than 8** (rules change post-2021). So Wanderer cannot cascade into Ulamog (10), Ulamog Infinite Gyre (11), Kozilek Butcher (10), Kozilek Great Distortion (10), Cityscape Leveler (8), Portal to Phyrexia (9), Summon: Bahamut (9), Artisan of Kozilek (9), Void Winnower (9), It That Betrays (12), or Ghalta (12). It *can* cascade into Avenger of Zendikar (7), Bane of Bala Ged (7), Sire of Seven Deaths (7), Devourer of Destiny (7), Combustible Gearhulk (6), Etali (6), Sunbird's Invocation (6), Selvala's Stampede (6), Conduit of Ruin (6), Rampaging Baloths (6), Tendershoot Dryad (5), Wildsear Scouring Maw (5), Greater Good (4), and lower.

This matters for closing-line math: Wanderer's two cascades are *not* deterministic Eldrazi reveals — they're more often a 6-7 mana hit each.

-----

## Core Loop

The deck ramps aggressively (19 dedicated ramp pieces — Sol Ring, Arcane Signet, Mana Vault, Ancient Tomb, Talisman, Thran Dynamo, Birds of Paradise, Llanowar Loamspeaker, Lotus Cobra, Sakura-Tribe Elder, Solemn Simulacrum, Tireless Provisioner, Delighted Halfling, Cultivate, Kodama's Reach, Farseek, Nature's Lore, Rampant Growth, Skyshroud Claim) into a wall of high-mana-value threats and cascade/free-cast effects, then chains the chaos to compound triggers.

**Engine layer 1 — Cascade and free-cast (8):** Maelstrom Wanderer (cascade x2 + haste), Wildsear Scouring Maw (cascade on each enchantment from hand), Sunbird's Invocation (each cast from hand → reveal X cards, may cast one for free), Etali Primal Storm (each attack: cast top of each library), Aetherworks Marvel (6 energy + tap → cast a spell from top 6 free), Creative Technique (shuffle, exile until non-land, cast it free + Demonstrate so an opponent also copies), Selvala's Stampede (council vote — wild = creatures from library, free = permanents from hand), Conduit of Ruin (first creature each turn costs {2} less + ETB tutors a 7+ MV colorless creature on top).

**Engine layer 2 — Power-matters payoffs (6):** Selvala Heart of the Wilds ({G},{T}: add X mana = greatest creature power; draws when an entering creature has greatest power), The Great Henge (cost-reduced by greatest power; +1/+1 + draw on each nontoken creature), Garruk's Uprising (creatures have trample, draw on each power-4+ ETB), Garruk's Packleader (draw on each power-3+ ETB), Goreclaw (creature spells with power 4+ cost {2} less; +1/+1 trample on power-4+ attackers), Greater Good (sac creature → draw cards equal to its power, discard 3).

**Engine layer 3 — Landfall payoffs (3):** Avenger of Zendikar (token-per-land + landfall +1/+1 to all Plants), Rampaging Baloths (4/4 trample on landfall), Tendershoot Dryad (Saproling per upkeep + Saprolings get +2/+2 with city's blessing). Lotus Cobra and Tireless Provisioner pull double duty as ramp + landfall enablers.

**Payoff bombs (13):** Ulamog Ceaseless Hunger (cast: exile 2 permanents; attack: exile 20 cards from a library), Ulamog Infinite Gyre (cast: destroy any permanent; Annihilator 4; graveyard reshuffle), Kozilek Butcher of Truth (cast: draw 4; Annihilator 4; graveyard reshuffle), Kozilek Great Distortion (cast: refill to 7; menace; discard-X-MV-card → counter X-MV spell), Artisan of Kozilek (cast: reanimate from grave; Annihilator 2), Conduit of Ruin, Cityscape Leveler (cast/attack: destroy nonland → opp gets Powerstone; unearth 8), It That Betrays (steal opp's sacrificed nontoken permanents; Annihilator 2), Bane of Bala Ged (attack: exile 2 permanents), Breaker of Creation (cast: gain life per colorless permanent; hexproof from each color; Annihilator 2), Devourer of Destiny (cast: exile colored permanent; opening-hand library manipulation), Sire of Seven Deaths (first strike, vigilance, menace, trample, reach, lifelink, ward 7 life), Void Winnower (opps can't cast or block with even-MV creatures), Portal to Phyrexia (ETB: each opp sacs 3 creatures; upkeep: reanimate from any graveyard), Combustible Gearhulk (ETB: opp picks — give you 3 cards or mill 3 + take damage = total MV), Summon: Bahamut (saga: I/II destroy nonland, III draw 2, IV deals damage equal to total MV of other permanents).

**The play pattern:** T1–3 ramp aggressively. T4–6 land Maelstrom Wanderer (cascade x2 = often 2 free midsize bodies with haste) or hardcast Conduit of Ruin (tutoring an Eldrazi to top) or Sunbird's Invocation. T6+ start chaining big casts — each one triggers Sunbird, Garruk's Uprising/Packleader draws, Selvala's mana, and (if Wildsear is out) cascade-on-enchantments. Annihilator and exile-on-cast effects strip opponents' boards. Close via combat.

-----

## Closing Lines

**Line 1 — Maelstrom Wanderer cascade dump (T6–7).** Cast Wanderer for {5}{G}{U}{R}. Two cascades resolve: each often hits a 6–7 MV creature with haste (Avenger of Zendikar floods board with 0/1 Plants then a landfall pump; Etali attacks immediately and casts off two opponents' top decks; Bane of Bala Ged or Sire of Seven Deaths attack for big damage). Wanderer itself attacks for 7 trampleless. Combined turn-of-cast damage: typically 15–25. Engine-online → kill: 1–2 turns.

**Line 2 — Craterhoof Behemoth alpha (T7–8).** Build a wide board (Avenger creates a token per land; Rampaging Baloths produces 4/4s on landfall; Tendershoot drips Saprolings) and resolve Craterhoof Behemoth (8 mana with {5}{G}{G}{G}). All your creatures gain trample and +X/+X where X = creatures you control. With 8+ creatures, this is reliably lethal across the table. Engine-online → kill: 1 turn.

**Line 3 — Ghalta + Eldrazi pile (T5–7).** Ghalta Primal Hunger costs {10}{G}{G} reduced by total power of creatures you control (floor {G}{G}). With Selvala Heart, Llanowar Loamspeaker (3/3 in elemental mode), and a couple of 6-power Eldrazi, Ghalta lands for {G}{G}. From there, Annihilator chains and trample close out 1–2 turns later. Engine-online → kill: 2–3 turns.

**Line 4 — Ulamog Ceaseless mill (T8+).** Hardcast Ulamog Ceaseless Hunger ({10}). Cast trigger exiles 2 permanents; attacks exile 20 cards from defending player's library. 5 attacks empty a 100-card library — slow but uncounterable as a back-up plan against decks running graveyard recursion. Engine-online → kill: 4–5 turns.

**Line 5 — Sunbird's Invocation chain (T6+).** Resolve Sunbird's Invocation. Each subsequent spell from hand reveals X cards (X = MV) and lets you cast one with MV ≤ X for free. Casting an Eldrazi (10) reveals 10 cards and pulls another up-to-10-MV free spell — chains escalate quickly. Selvala's Stampede + Sunbird is particularly explosive (council vote can flood the board, Sunbird then offers a 6-MV free spell). Engine-online → kill: 2 turns.

-----

## Kill Window

- **Goldfish:** T6–8
- **Through interaction:** T8–11

The deck is mid-speed — 19 ramp pieces let it reach 6+ mana by T4–5 reliably, but the kills require a creature already on board (Maelstrom + cascade hits, Craterhoof alpha) or a chain to develop (Sunbird's Invocation). A single Cyclonic Rift on T7 pushes the kill back 3–4 turns.

-----

## Durability

After a Cyclonic Rift on T7: rebuild via Conduit of Worlds (play lands from graveyard, sorcery-speed cast a non-land permanent from graveyard once per turn), Aetherworks Marvel (energy from dying permanents → tap-and-pay-6E to cast off the top), and the deck's deep ramp suite. Two of the big Eldrazi self-recur — Ulamog Infinite Gyre and Kozilek Butcher of Truth shuffle the graveyard (including themselves) into the library when put into a graveyard from anywhere. **Ulamog Ceaseless Hunger does NOT have this clause** — once exiled or milled, it's gone.

Targeted recursion is thin: no Eternal Witness, no Regrowth, no Sun Titan. The deck recovers by re-ramping and re-deploying from hand or from the top of a freshly-shuffled library — reasonable but not fast.

Re-threatening after a full wipe: 2–3 turns with a normal hand, faster if Wanderer or a free-cast (Aetherworks Marvel) is online.

The deck is **not** strictly commander-dependent — Maelstrom Wanderer is an accelerant (haste + 2 cascades on cast), but the deck's bigs and ramp suite still execute without him. Two-tax recast is steep ({5}{G}{U}{R} + {2} = 10).

-----

## Interaction Package

**~10 pieces total**, most attached to expensive creatures.

- **Direct removal spells (5):**
  - *Beast Within* (instant) — destroy any permanent → opp gets a 3/3 token. Universal answer at instant speed.
  - *Decimate* (sorcery, {2}{R}{G}) — destroy target artifact + creature + enchantment + land. **Requires legal targets in all four categories or it cannot be cast.** Pod-dependent.
  - *Chaos Warp* (instant) — owner shuffles target permanent and reveals top card; if it's a permanent, it enters. Random-but-flexible answer.
  - *Boseiju, Who Endures* (channel — discard the land for {1}{G}: destroy artifact / enchantment / nonbasic land an opp controls; cost reduced by {1} per legendary creature you control). With Maelstrom + a legendary Eldrazi, channel is often {G}.
  - *Kozilek's Command* ({X}{C}{C}, modal) — choose two: make X 0/1 Eldrazi Spawn, scry-and-draw, exile creature with MV ≤ X, exile up to X cards from graveyards. Removal mode is X-cost, so flexible at 4+ mana.

- **Creature-rider removal (5):**
  - *Cityscape Leveler* (cast & on each attack: destroy nonland → opp gets Powerstone token).
  - *Ulamog Ceaseless Hunger* (cast: exile 2 permanents).
  - *Ulamog Infinite Gyre* (cast: destroy any permanent).
  - *Devourer of Destiny* (cast: exile target permanent that's one or more colors).
  - *Bane of Bala Ged* (each attack: defending player exiles 2 permanents — they choose).

- **Soft counter (1):**
  - *Kozilek, the Great Distortion* — discard a card with MV X to counter a target spell with MV X. Situational and hand-size dependent.

- **Damage / mass-damage (2):**
  - *Combustible Gearhulk* (opp chooses: give you 3 cards or mill 3 + take damage = total MV — usually 6–12 damage).
  - *Summon: Bahamut* (saga IV — Mega Flare = damage to each opp = total MV of other permanents you control; with bigs out, this is often 30+ damage).

Instant speed: ~30% (Beast Within, Chaos Warp, Boseiju channel, Kozilek discard-counter).
Sorcery speed: most of the rest, including Decimate and the on-cast Eldrazi triggers.

**The structural interaction gap is true counterspells.** Despite blue access, the deck runs zero hard counters. Kozilek's discard-counter is the only stack interaction — and it requires an MV-matched card in hand. Combo decks that win on the stack will resolve unanswered.

-----

## Game Changer Slots

**2 / 3 used.**

1. **Ancient Tomb** — fast mana land, 2 mana for 2 damage.
2. **Mana Vault** — 3 colorless on T1, doesn't untap normally.

*Verified against `REF_Game_Changers_List.md` (current as of 2026-02-09) on 2026-05-08. No other cards in the deck are on the GC list — Selvala Heart of the Wilds is **not** a GC; Maelstrom Wanderer is **not** a GC.*

**Open slot:** the deck has room for one more GC without violating Bracket 3's 3-cap. Plausible additions: Worldly Tutor (tutor a big), Smothering Tithe (ramp + treasure), Seedborn Muse (mana doubling on opps' turns + Selvala mana).

-----

## Bracket 3 Compliance

- **Game Changers:** 2 of 3 used. Room for one more.
- **Infinite combos:** None.
- **Extra turns:** None.
- **Mass land denial:** None. Decimate hits 1 land but requires 4 distinct targets.
- **Two-card infinites:** None.

-----

## Pod Fit

1. **Robust to single-piece disruption.** Multiple cascade/free-cast engines (Wanderer, Wildsear, Sunbird's, Etali, Aetherworks, Creative Technique, Selvala's Stampede). Removing any one doesn't shut the deck down.
2. **Vulnerable to mass exile.** Path/Swords on Eldrazi titans bypasses the graveyard reshuffle clause on Ulamog Infinite Gyre and Kozilek Butcher (exile, not graveyard). Farewell is brutal — exiles creatures, artifacts, graveyards, and enchantments.
3. **Vulnerable to Cyclonic Rift.** Recovery requires re-ramping; 3–4 turn delay.
4. **Vulnerable to combo.** No hard counters, no Grand Abolisher equivalent. T5–6 combo decks pre-empt the deck's own T6–8 kill window.
5. **Strong vs. creature aggro.** Avenger of Zendikar, Tendershoot Dryad tokens, Sire of Seven Deaths (lifelink + ward), and Void Winnower (opps can't block with even-MV) shut down board-based aggression.
6. **Politically loud.** Annihilator triggers and 12/12 Eldrazi draw the table's attention. Expect to be the early target if the engine starts firing.

-----

## Differentiation From Other Decks

| | Eldrazi Stampede Chaos (Wanderer) | The Loam Cycle (Teval) | The Calamity Tax (Glarb) |
|---|---|---|---|
| Engine | Ramp → cascade/free-cast → big creatures | Graveyard recursion + lands matter | Tax + augur control |
| Mana strategy | Aggressive ramp, big payoffs | Lands recur from graveyard | Selective lock pieces |
| Win condition | Combat / Annihilator | Mill / value attrition | Slow value + combat |
| Color overlap | GUR (Temur) | BUG (Sultai) | BUG (Sultai) |
| Speed | T6–8 | T8–11 | T9–12 |
| Counterspells | Soft only (Kozilek MV-counter) | Some | Yes |

No engine overlap with other decks in the roster — the Temur color identity and the Eldrazi-cascade theme are unique. Generic staples are shared (Sol Ring, Arcane Signet, Cultivate, Kodama's Reach, Farseek, Skyshroud Claim, Birds of Paradise, Sakura-Tribe Elder, Solemn Simulacrum) — the zero-surplus shared pool already accounts for these.

-----

## Known Weaknesses

- **No hard counterspells.** Despite blue access, the deck runs zero. Kozilek's discard-counter is the only stack interaction and requires an MV-match. Combo decks that resolve on the stack are unanswerable.
- **Slow goldfish (T6–8).** Combo decks that go off T4–6 pre-empt the deck. Maelstrom is an 8-mana commander.
- **Cyclonic Rift / Farewell are devastating.** The deck has limited targeted recursion and cannot quickly re-deploy its lost board.
- **Cascade math is misleading.** Maelstrom's two cascades cap at MV 7 hits — the Eldrazi titans (10–12 MV) cannot be cascaded into. The deck's biggest payoffs need to be hardcast.
- **Decimate has a 4-target requirement.** If the pod is light on artifacts or enchantments, Decimate becomes uncastable. Pod-dependent.
- **Ulamog Ceaseless Hunger does not self-recur.** Unlike Ulamog Infinite Gyre and Kozilek Butcher, the Ceaseless version has no graveyard-reshuffle clause. Once milled or exiled, it's gone. Worth keeping in hand or hardcasting rather than relying on cheating it.
- **Creative Technique gives an opponent a copy.** Demonstrate forces you to also let an opponent free-cast the same card. Asymmetric upside (you go first) but real downside.

-----

## Conversion Check Breakdown

### Core Loop: 4/5

The loop — "ramp aggressively, cheat on cost via cascade and free-cast effects, deploy huge creatures with on-cast / on-attack triggers, and let the chaos compound" — is dense and recognizable. 8 dedicated cascade/free-cast enablers + 6 power-matters payoffs + 13+ big-creature payoffs + 19 ramp pieces = 30+ cards directly serving the strategy. Wildsear gives every enchantment in the deck cascade; Sunbird gives every hand-cast spell a free piggyback; Conduit of Ruin tutors an Eldrazi on cast and discounts your next creature; Maelstrom is two cascades on a single trigger.

Doesn't reach 5 because the loop is a **loose, probabilistic** chaining of free-cast effects rather than a tight, deterministic engine. The deck's identity is "ramp into bigs that snowball" — high-quality but not surgically machined.

**Checkpoint:** Cover the commander. The 99 reads "Eldrazi titans + ramp + cascade/free-cast." Identifiable.

### Kill Reliability: 4/5

Five distinct closing lines: Wanderer cascade dump (T6–7), Craterhoof alpha (T7–8), Ghalta + Eldrazi pile (T5–7), Ulamog Ceaseless mill (T8+), Sunbird's Invocation chain (T6+). At least two are fast (Wanderer, Craterhoof alpha). The Annihilator triggers strip opponents' resources mid-attack.

Doesn't reach 5 because every line requires combat (no spell-based win), and Maelstrom's cascade math caps below the Eldrazi titans — the deck can't reliably "cheat the unbeatable threat" in a single cast.

**Checkpoint:** Wanderer + cascade hits closes in 1–2 turns. Craterhoof alpha closes in 1 turn from a wide board.

### Durability: 3/5

19 ramp pieces give massive mana redundancy — even after a wipe, the deck can resume mana production within 1–2 turns. Two Eldrazi titans (Ulamog Infinite Gyre, Kozilek Butcher) self-shuffle from graveyard, putting their copies back on the deck. Conduit of Worlds (lands + sorcery-speed grave-cast) and Aetherworks Marvel (energy from dying permanents → free cast off top 6) provide some recovery.

Doesn't reach 4 because: (1) targeted recursion is essentially absent — no Eternal Witness, Regrowth, Sun Titan, etc.; (2) Ulamog Ceaseless Hunger does **not** self-recur and is the deck's strongest single payoff; (3) recovery from a Cyclonic Rift takes 3+ turns; (4) graveyard hate (Bojuka Bog) doesn't hurt much, but exile-based hate (Rest in Peace, Leyline of the Void) shuts down the limited recursion the deck does have.

**Checkpoint:** Cyclonic Rift on T7. 2–3 turns to re-threaten via re-ramp and another big cast.

### Interaction: 3/5

10 interaction pieces, but most are riders on 6–12 mana creatures. Direct removal: Beast Within, Decimate, Chaos Warp, Boseiju Channel, Kozilek's Command — 5 spells. Soft counter: Kozilek Great Distortion. Combat / mass damage: Combustible Gearhulk, Summon: Bahamut.

Doesn't reach 4 because: (1) no hard counterspells despite blue access; (2) most "interaction" doesn't arrive until T6+ tied to Eldrazi creatures; (3) instant-speed coverage is thin (~30%); (4) Decimate's 4-target requirement makes it unreliable; (5) cannot stop a combo turn — Grand Abolisher / Drannith Magistrate equivalents absent.

**Checkpoint:** Opponent is about to combo on T5. Realistic answers in hand: Beast Within / Chaos Warp on a key piece if drawn. No reliable proactive answer.

### Total: 14/20 — Solid foundation. Lowest axes are Durability and Interaction.

-----

## Decklist (100 cards)

### Commander (1)

1 Maelstrom Wanderer

### Cascade & Free-Cast Engines (8)

1 Wildsear, Scouring Maw
1 Sunbird's Invocation
1 Etali, Primal Storm
1 Aetherworks Marvel
1 Creative Technique
1 Selvala's Stampede
1 Conduit of Ruin
1 Conduit of Worlds

### Power-Matters Payoffs (6)

1 Selvala, Heart of the Wilds
1 The Banyan Tree *(reskin: The Great Henge)*
1 Garruk's Uprising
1 Garruk's Packleader
1 Goreclaw, Terror of Qal Sisma
1 Greater Good

### Eldrazi Bombs (13)

1 Artisan of Kozilek
1 Bane of Bala Ged
1 Breaker of Creation
1 Cityscape Leveler
1 Devourer of Destiny
1 It That Betrays
1 Kozilek, Butcher of Truth
1 Kozilek, the Great Distortion
1 Sire of Seven Deaths
1 Ulamog, the Ceaseless Hunger
1 Ulamog, the Infinite Gyre
1 Void Winnower
1 Portal to Phyrexia

### Other Big Creatures / Closers (6)

1 Avenger of Zendikar
1 Combustible Gearhulk
1 Craterhoof Behemoth
1 Ghalta, Primal Hunger
1 Grothama, All-Devouring
1 Rampaging Baloths

### Combat Doublers / Pump (2)

1 Berserkers' Onslaught
1 Warstorm Surge

### Saga (1)

1 Summon: Bahamut

### Mana Doublers / Specialty (1)

1 Tendershoot Dryad

### Interaction (5)

1 Beast Within
1 Chaos Warp
1 Decimate
1 Kozilek's Command
1 Harmonize *(card draw, not interaction — listed here for completeness)*

### Cost Reducer (already in engines list)

*(Goreclaw, Conduit of Ruin, The Great Henge double as cost-reducers — counted under engines/payoffs above.)*

### Card Draw (1)

1 Return of the Wildspeaker

### Ramp — Mana Rocks (4)

1 Sol Ring
1 Arcane Signet
1 Talisman of Impulse
1 Thran Dynamo

### Ramp — Game Changers (2)

1 Ancient Tomb
1 Mana Vault

### Ramp — Land Tutors (5)

1 Cultivate
1 Kodama's Reach
1 Farseek
1 Nature's Lore
1 Rampant Growth
1 Skyshroud Claim

*(Skyshroud Claim brings 6 — 6 land tutors total, listed as 6 above; Rampant Growth + Farseek + Nature's Lore + Cultivate + Kodama's Reach + Skyshroud Claim = 6.)*

### Ramp — Creature (5)

1 Birds of Paradise
1 Delighted Halfling
1 Llanowar Loamspeaker
1 Lotus Cobra
1 Sakura-Tribe Elder
1 Solemn Simulacrum
1 Tireless Provisioner

### Other / Partner-shell (1)

1 Kodama of the East Tree

### Lands (33)

1 Boseiju, Who Endures
1 Breeding Pool
1 Cinder Glade
1 Command Tower
1 Copperline Gorge
1 Evolving Wilds
1 Exotic Orchard
4 Forest
1 Game Trail
1 Green Dragon Inn *(reskin: Homeward Path — anti-creature-theft utility land)*
1 Hinterland Harbor
2 Island
1 Karplusan Forest
1 Mossfire Valley
1 Mosswort Bridge
2 Mountain
1 Myriad Landscape
1 Nykthos, Shrine to Nyx
1 Reliquary Tower
1 Rootbound Crag
1 Sheltered Thicket
1 Shivan Reef
1 Spire Garden
1 Stomping Ground
1 Sulfur Falls
1 Temple of Abandon
1 Terramorphic Expanse
1 Training Center
1 Willowrush Verge
1 Wooded Ridgeline
1 Yavimaya Coast

-----

## Changelog

- **2026-05-08:** Summary file created from scratch during deck audit. Decklist verified 100 cards (99 + commander). GC count 2/3 (Ancient Tomb, Mana Vault — room for one more). Commander text verified against local Scryfall data. `Green Dragon Inn` confirmed by user as reskin for `Homeward Path` (C16) — anti-creature-theft utility land — alias added to `REF_Reskin_Aliases.md`. Conversion Check 14/20 (4/4/3/3) — Solid. No card swaps recommended at this time; closest open item is filling the third GC slot (candidates: Worldly Tutor, Smothering Tithe, Seedborn Muse).
