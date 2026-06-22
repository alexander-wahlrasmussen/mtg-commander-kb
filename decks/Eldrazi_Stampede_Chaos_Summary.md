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
| **Kill Window** | Clock: **T8 decap** (median; T6 ≈ 10% god-hand) / **T12 table** **(board)** (lab 2026-06-13, `esc_clock_lab.py`) · Through interaction: slower *(unverified — goldfish only; no blockers/disruption model)*. The old "Goldfish T6–8" was the optimistic decap edge and conflated decap with table: decap median is T8 (T6 only 10%), the table clock is T12 (never stated). See `analysis/Eldrazi_Stampede_Clock_Lab_2026-06-13.md` |

-----

## Commander Rules Text

Maelstrom Wanderer has two abilities:

1. **Static — "Creatures you control have haste."** Every creature you cheat into play (cascade, Etali, Selvala's Stampede, Aetherworks Marvel, Creative Technique, Sunbird's Invocation, Wildsear cascade) attacks immediately.
2. **Cascade, cascade.** When cast, two separate cascade triggers fire. Each exiles cards from the top of your library until you exile a *nonland* card with mana value strictly less than 8, which you may cast for free. The two triggers resolve independently — the spell from the first cascade resolves before the second cascade exiles cards.

Key reading: cascade requires the resulting spell to have **mana value strictly less than 8** (rules change post-2021). So Wanderer cannot cascade into Ulamog Ceaseless Hunger (10), Ulamog Infinite Gyre (11), Kozilek Butcher (10), Kozilek Great Distortion (10), Craterhoof Behemoth (8), Breaker of Creation (8), Cityscape Leveler (8), Portal to Phyrexia (9), Summon: Bahamut (9), Artisan of Kozilek (9), Void Winnower (9), It That Betrays (12), or Ghalta (12). It *can* cascade into Avenger of Zendikar (7), Bane of Bala Ged (7), Sire of Seven Deaths (7), Devourer of Destiny (7), Combustible Gearhulk (6), Etali (6), Sunbird's Invocation (6), Selvala's Stampede (6), Conduit of Ruin (6), Rampaging Baloths (6), Kodama of the East Tree (6), Tendershoot Dryad (5), Wildsear Scouring Maw (5), Greater Good (4), and lower.

This matters for closing-line math: Wanderer's two cascades are *not* deterministic Eldrazi reveals — they're more often a 6-7 mana hit each.

-----

## Core Loop

The deck ramps aggressively (19 dedicated ramp pieces — Sol Ring, Arcane Signet, Mana Vault, Ancient Tomb, Talisman, Thran Dynamo, Birds of Paradise, Llanowar Loamspeaker, Lotus Cobra, Sakura-Tribe Elder, Solemn Simulacrum, Tireless Provisioner, Delighted Halfling, Cultivate, Kodama's Reach, Farseek, Nature's Lore, Rampant Growth, Skyshroud Claim) into a wall of high-mana-value threats and cascade/free-cast effects, then chains the chaos to compound triggers.

**Engine layer 1 — Cascade and free-cast (9):** Maelstrom Wanderer (cascade x2 + haste), Wildsear Scouring Maw (enchantment spells you cast from hand have cascade), Sunbird's Invocation (each spell cast **from your hand** → reveal X cards, may cast one for free — does NOT trigger off cascade hits, Aetherworks/Etali/Creative-Technique free-casts, or permanents put in by Selvala's Stampede), Etali Primal Storm (each attack: cast top of each library), Aetherworks Marvel (6 energy + tap → cast a spell from top 6 free), Creative Technique (shuffle, exile until non-land, cast it free + Demonstrate so an opponent also copies), Selvala's Stampede (council's dilemma — each player votes wild or free independently; each wild = reveal creatures from library to put in play, each free = permanent from hand), Conduit of Ruin (first creature each turn costs {2} less + **cast trigger** tutors a 7+ MV colorless creature on top), Kodama of the East Tree (whenever another permanent enters, you may put a permanent card with equal-or-lesser MV from hand onto the battlefield — chains hard with cascade hits and Eldrazi entering).

**Engine layer 2 — Power-matters payoffs (6):** Selvala Heart of the Wilds ({G},{T}: add X mana = greatest creature power; **its controller** may draw when an entering creature has the greatest power — note this is two-way, opponents draw on their own greatest-power ETBs too), The Great Henge (cost-reduced by greatest power; +1/+1 + draw on each nontoken creature; {T}: {G}{G} + 2 life), Garruk's Uprising (creatures have trample, draw on each power-4+ ETB), Garruk's Packleader (draw on each other power-3+ ETB), Goreclaw (creature spells with power 4+ cost {2} less; when Goreclaw attacks, **each of your power-4+ creatures** gets +1/+1 and trample EOT — not just attackers), Greater Good (sac creature → draw cards equal to its power, discard 3).

**Engine layer 3 — Landfall payoffs (3):** Avenger of Zendikar (token-per-land + landfall +1/+1 to all Plants), Rampaging Baloths (4/4 trample on landfall), Tendershoot Dryad (Saproling per upkeep + Saprolings get +2/+2 with city's blessing). Lotus Cobra and Tireless Provisioner pull double duty as ramp + landfall enablers.

**Payoff bombs (13):** Ulamog Ceaseless Hunger (**indestructible**; cast: exile 2 permanents; attack: exile top 20 cards of defending player's library), Ulamog Infinite Gyre (**indestructible**; cast: destroy any permanent; Annihilator 4; graveyard reshuffle), Kozilek Butcher of Truth (cast: draw 4; Annihilator 4; graveyard reshuffle), Kozilek Great Distortion (cast: if fewer than 7 in hand, refill to 7; menace; discard-X-MV-card → counter X-MV spell), Artisan of Kozilek (cast: reanimate from your grave; Annihilator 2), Conduit of Ruin, Cityscape Leveler (cast/attack: destroy up to one nonland → its controller gets Powerstone; trample; unearth 8), It That Betrays (steal opp's sacrificed nontoken permanents; Annihilator 2), Bane of Bala Ged (attack: defender exiles 2 permanents), Breaker of Creation (cast: gain life per colorless permanent; hexproof from each color; Annihilator 2), Devourer of Destiny (cast: exile colored permanent; opening-hand library manipulation), Sire of Seven Deaths (first strike, vigilance, menace, trample, reach, lifelink, ward—pay 7 life), Void Winnower (**opponents can't cast spells with even MV** — including instant-speed removal and counters at 2/4/6 — AND can't block with even-MV creatures), Portal to Phyrexia (ETB: each opp sacs 3 **creatures**; upkeep: reanimate creature from any graveyard to your side as Phyrexian), Combustible Gearhulk (first strike; ETB: opp picks — give you 3 cards or mill 3 + take damage = total MV of milled cards), Summon: Bahamut (Saga Dragon creature 9/9 flying; I/II destroy nonland, III draw 2, IV Mega Flare: damage to each opp = total MV of other permanents you control).

**The play pattern:** T1–3 ramp aggressively. T4–6 land Maelstrom Wanderer (cascade x2 = often 2 free midsize bodies with haste) or hardcast Conduit of Ruin (tutoring an Eldrazi to top) or Sunbird's Invocation. T6+ start chaining big casts — each one triggers Sunbird, Garruk's Uprising/Packleader draws, Selvala's mana, and (if Wildsear is out) cascade-on-enchantments. Annihilator and exile-on-cast effects strip opponents' boards. Close via combat.

-----

## Closing Lines

**Line 1 — Maelstrom Wanderer cascade dump (T6–7).** Cast Wanderer for {5}{G}{U}{R}. Two cascades resolve: each often hits a 6–7 MV creature with haste (Avenger of Zendikar floods board with 0/1 Plants then a landfall pump; Etali attacks immediately and casts off two opponents' top decks; Bane of Bala Ged or Sire of Seven Deaths attack for big damage). Wanderer itself attacks for 7 trampleless. Combined turn-of-cast damage: typically 15–25. Engine-online → kill: 1–2 turns.

**Line 2 — Craterhoof Behemoth alpha (T7–8).** Build a wide board (Avenger creates a 0/1 Plant token per land; Rampaging Baloths produces 4/4 vanilla Beast tokens on landfall — they don't have trample unless Garruk's Uprising is out; Tendershoot drips Saprolings on **each** upkeep, not just yours) and resolve Craterhoof Behemoth (MV 8 with {5}{G}{G}{G} — note Craterhoof cannot be cascaded into). All your creatures gain trample and +X/+X where X = creatures you control. With 8+ creatures, this is reliably lethal across the table. Engine-online → kill: 1 turn.

**Line 3 — Ghalta + Eldrazi pile (T5–7).** Ghalta Primal Hunger costs {10}{G}{G} reduced by total power of creatures you control (floor {G}{G}). With Selvala Heart, Llanowar Loamspeaker (3/3 in elemental mode), and a couple of 6-power Eldrazi, Ghalta lands for {G}{G}. From there, Annihilator chains and trample close out 1–2 turns later. Engine-online → kill: 2–3 turns.

**Line 4 — Ulamog Ceaseless mill (T8+).** Hardcast Ulamog Ceaseless Hunger ({10}). Cast trigger exiles 2 permanents; attacks exile 20 cards from defending player's library. 5 attacks empty a 100-card library — slow but uncounterable as a back-up plan against decks running graveyard recursion. Engine-online → kill: 4–5 turns.

**Line 5 — Sunbird's Invocation chain (T6+).** Resolve Sunbird's Invocation. Each subsequent spell **cast from hand** reveals X cards (X = MV) and lets you cast one with MV ≤ X for free. Hardcasting an Eldrazi (10) reveals 10 cards and pulls another up-to-10-MV free spell. Note the from-hand restriction: cascade hits, Aetherworks/Etali/Creative-Technique free-casts, and creatures put in by Selvala's Stampede do NOT trigger Sunbird. Selvala's Stampede hardcast does trigger it once (revealing 6 cards). Engine-online → kill: 2 turns.

-----

## Kill Window

- **Clock (lab 2026-06-13, `esc_clock_lab.py`, 40k trials):** decap median **T8** (2% T5 / 10% T6 / 26% T7 / 50% T8 / 71% T9 / 85% T10) · table median **T12** (2% T8 / 8% T9 / 20% T10 / 61% T12 / 89% T14) · never-in-14: decap 1% / table 11%.
- **Through interaction:** slower *(unverified — goldfish only; no blockers/disruption model)*.

The old hand-estimate "Goldfish T6–8" was the **optimistic decap edge** and conflated two clocks. The lab puts the decap median at T8 (T6 is a 10% god-hand, not the norm) and the **table clock at T12** — four turns slower and never previously stated. Decap is gated on the 8-mana Wanderer cast (≈T6–7 even with 19 ramp pieces) plus ~2 swings; the table-kill is the Craterhoof alpha (trample + X/X distributed across the table), which needs Craterhoof, 8 mana, and a wide board *simultaneously* (61% by T12). Against the T6–7 combo pod the deck clears a **T≤7 decap only 26%** of the time — it does not race; this matches the deck's known "vulnerable to combo / slow goldfish" posture. A single Cyclonic Rift on T7 pushes the kill back 3–4 turns. Full writeup: `analysis/Eldrazi_Stampede_Clock_Lab_2026-06-13.md`.

-----

## Durability

After a Cyclonic Rift on T7: rebuild via Conduit of Worlds (play lands from graveyard; sorcery-speed tap **only if you haven't cast a spell this turn** — and if you cast the targeted card from grave, you **can't cast additional spells that turn**, so it's one-spell-per-turn-total, not a free bonus cast), Aetherworks Marvel (energy from dying permanents → tap-and-pay-6E to cast off the top), the indestructible clause on both Ulamogs (they survive non-exile board wipes), and the deck's deep ramp suite. Two of the big Eldrazi self-recur — Ulamog Infinite Gyre and Kozilek Butcher of Truth shuffle the graveyard (including themselves) into the library when put into a graveyard from anywhere. **Ulamog Ceaseless Hunger does NOT have this clause** — once exiled or milled, it's gone (though it IS indestructible while on the battlefield).

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
  - *Boseiju, Who Endures* (channel — discard the land for {1}{G}: destroy artifact / enchantment / nonbasic land an opp controls; opp ramps a basic; cost reduced by {1} per legendary creature you control, **floor is {G}** so Maelstrom alone on the field is enough).
  - *Kozilek's Command* ({X}{C}{C}, **instant**, modal) — choose two: target player creates X 0/1 Eldrazi Spawn with "Sacrifice this token: Add {C}", target player scries X then draws a card, exile creature with MV ≤ X, exile up to X cards from graveyards. Removal mode is X-cost, so flexible at 4+ mana. Instant speed makes this the deck's most flexible answer.

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

Instant speed: ~50% of the spell-based interaction (Beast Within, Chaos Warp, Boseiju channel, Kozilek's Command, Kozilek Great Distortion discard-counter). Sorcery speed: Decimate. The on-cast Eldrazi triggers fire at the speed of their parent creature spells (sorcery for cast triggers).

Void Winnower is a passive interaction piece worth naming separately — while on the battlefield it shuts off every opponent spell with even MV (2/4/6/8). That's a hard wall against most counterspells and removal staples, not just blocking.

**The structural interaction gap is proactive hard counters.** Despite blue access, the deck runs zero true counterspells. Kozilek Great Distortion's discard-counter is the only on-stack counter — and it requires an MV-matched card in hand. Combo decks that win on the stack will resolve unanswered unless Void Winnower happens to be on the battlefield and the win spell has even MV.

-----

## Game Changer Slots

**2 / 3 used.**

1. **Ancient Tomb** — fast mana land, 2 mana for 2 damage.
2. **Mana Vault** — 3 colorless on T1, doesn't untap normally.

*Verified against `REF_Game_Changers_List.md` (current as of 2026-02-09) on 2026-05-08. No other cards in the deck are on the GC list — Selvala Heart of the Wilds is **not** a GC; Maelstrom Wanderer is **not** a GC.*

**Open slot:** the deck has room for one more GC without violating Bracket 3's 3-cap. Plausible additions (Temur-legal — GUR only): Worldly Tutor (tutor a big), Seedborn Muse (mana doubling on opps' turns + Selvala mana), Mystical Tutor, Force of Will / Fierce Guardianship (the deck's structural counterspell gap), Cyclonic Rift, Rhystic Study, Crop Rotation, Survival of the Fittest, Natural Order. ~~Smothering Tithe~~ is **not legal** here — it's {3}{W}, outside Temur color identity.

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

### Cascade & Free-Cast Engines (9)

1 Wildsear, Scouring Maw
1 Sunbird's Invocation
1 Etali, Primal Storm
1 Aetherworks Marvel
1 Creative Technique
1 Selvala's Stampede
1 Conduit of Ruin
1 Conduit of Worlds
1 Kodama of the East Tree *(cheats permanents of equal-or-lesser MV from hand on every permanent ETB — a major engine, not a partner-shell card)*

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

### Big Creatures / Closers (6)

1 Avenger of Zendikar
1 Combustible Gearhulk
1 Craterhoof Behemoth
1 Ghalta, Primal Hunger
1 Grothama, All-Devouring
1 Rampaging Baloths

### Combat Doublers / Pump (1)

1 Berserkers' Onslaught

### ETB Damage Trigger (1)

1 Warstorm Surge *(when a creature you control enters, it deals damage equal to its power to any target — pairs with Avenger plant flood, Tendershoot Saprolings, and the +1/+1 from Henge)*

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

### Ramp — Land Tutors (6)

1 Cultivate
1 Kodama's Reach
1 Farseek
1 Nature's Lore
1 Rampant Growth
1 Skyshroud Claim

*(Skyshroud Claim brings 6 — 6 land tutors total, listed as 6 above; Rampant Growth + Farseek + Nature's Lore + Cultivate + Kodama's Reach + Skyshroud Claim = 6.)*

### Ramp — Creature (7)

1 Birds of Paradise
1 Delighted Halfling
1 Llanowar Loamspeaker
1 Lotus Cobra
1 Sakura-Tribe Elder
1 Solemn Simulacrum
1 Tireless Provisioner

### Lands (36, plus Ancient Tomb listed under GCs = 37 total)

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

- **2026-06-13:** Kill-turn clock lab (`scripts/esc_clock_lab.py`, 40k trials, seed 20260613) — first deck of the Kill-Window Lab Sweep. **"Goldfish T6–8" falsified as a single number:** decap median **T8** (T6 ≈ 10% god-hand), table median **T12**, never-in-14 table 11%. The claim was the optimistic decap front edge and didn't state the table clock. No card swaps (verification pass only); 14/20 Solid posture confirmed — the deck does not race the pod (T≤7 decap 26%). No card-text errors found (2026-05-16 audit held); reinforced that Craterhoof's own haste makes its alpha a same-turn table swing. Writeup: `analysis/Eldrazi_Stampede_Clock_Lab_2026-06-13.md`.

- **2026-05-16:** Formal audit pass. 14/20 (4/4/3/3) holds — Solid. ~10 card-text errors corrected: Conduit of Worlds is one-spell-per-turn-total when used, not a bonus cast; Void Winnower locks **all** even-MV opponent spells (not just creatures); both Ulamogs are **indestructible** (was omitted); Selvala Heart's draw is two-way (creature's controller draws, opponents trigger on their own greatest-power ETBs); Sunbird's Invocation triggers only on hand-cast spells (cascade/free-cast/Stampede ETBs don't trigger it); Rampaging Baloths landfall tokens are 4/4 vanilla Beasts (no trample by default); Conduit of Ruin's tutor is a cast trigger, not ETB; Goreclaw's attack-time pump applies to all your power-4+ creatures, not just attackers; Kozilek's Command is **instant** speed (instant-speed coverage was undercounted at ~30% — actual is ~50%); Boseiju channel floor is {G} — Maelstrom alone is enough, stacking legendaries doesn't help further. Structural fixes: **Kodama of the East Tree** recategorized from "Partner-shell" to a core cascade/free-cast engine (cheats equal-or-lesser-MV permanents from hand on every ETB); **Warstorm Surge** recategorized from "Combat Doublers" to ETB damage trigger. Land count corrected — section claimed 33, actual is **36** (37 including Ancient Tomb). Cascade exclusion list expanded to include Craterhoof (MV 8) and Breaker of Creation (MV 8); Kodama (MV 6) added to the "can cascade into" list. GC candidates fixed — **Smothering Tithe is illegal** in this deck (white, outside Temur). Legal alternatives named (Worldly Tutor, Seedborn Muse, Mystical Tutor, Force of Will, Fierce Guardianship, Cyclonic Rift, Rhystic Study, Crop Rotation, Survival of the Fittest, Natural Order). No card swaps made yet — chaos-leaning refinement pass pending; initial Moxfield CSV check showed most cascade staples (Apex Devastator, Bloodbraid Elf, Imoti, Maelstrom Nexus, Garruk's Horde, Wild-Magic Sorcerer, Etali Primal Conqueror) are not in the collection. Owned chaos-flavored hits so far: Tibalt's Trickery (x2), Insurrection, Birthing Pod, Inferno Titan. Wider net to be cast in a follow-up.

- **2026-05-08:** Summary file created from scratch during deck audit. Decklist verified 100 cards (99 + commander). GC count 2/3 (Ancient Tomb, Mana Vault — room for one more). Commander text verified against local Scryfall data. `Green Dragon Inn` confirmed by user as reskin for `Homeward Path` (C16) — anti-creature-theft utility land — alias added to `REF_Reskin_Aliases.md`. Conversion Check 14/20 (4/4/3/3) — Solid. No card swaps recommended at this time; closest open item is filling the third GC slot (candidates: Worldly Tutor, Smothering Tithe, Seedborn Muse). *(Note 2026-05-16: Smothering Tithe was incorrectly suggested — it's {3}{W}, illegal in Temur.)*

## Don't-Miss Rulings

- **Cascade requires MV *strictly less than 8*.** Wanderer **cannot** cascade into the Eldrazi titans (Ulamogs 10/11, Kozileks 10), Craterhoof (8), or Ghalta (12) — those must be hardcast. It *can* hit Avenger (7), Etali (6), Selvala's Stampede (6), and lower.
- **Sunbird's Invocation triggers ONLY on spells cast from hand** — cascade hits, Aetherworks / Etali / Creative Technique free-casts, and Selvala's Stampede ETBs do NOT trigger it.
- **Both Ulamogs are indestructible** (survive non-exile wipes). Ulamog Infinite Gyre and Kozilek Butcher self-shuffle from the graveyard; **Ulamog Ceaseless Hunger does NOT self-recur** — once milled or exiled it's gone, so hardcast it or keep it in hand.
- **Void Winnower:** while it's on the battlefield, opponents can't cast *even-MV* spells (2/4/6 removal and counters) AND can't block with even-MV creatures.
- **Conduit of Worlds is one-spell-per-turn-total** when you grave-cast (not a bonus cast), and only at sorcery speed if you haven't cast a spell yet that turn.
- **Creative Technique's Demonstrate lets an opponent copy it too** (you resolve first).
- **Decimate needs a legal target in all four categories** (artifact + creature + enchantment + land) or it can't be cast.

## Piloting Notes (for borrowers)

**Mulligan.** Looking for: **ramp that reaches 6+ mana by T4–5**, plus a payoff or an engine piece (Wanderer, Conduit of Ruin, Sunbird's).

- **Keep:** 2+ ramp pieces + a threat or a cascade engine.
- **Toss:** no-land hands; all-bombs with no ramp to cast them.

**Threats & timing.**

- **How you lose:** **no hard counterspells despite blue.** Kozilek the Great Distortion's discard-counter (MV-match) is the only stack interaction — combo decks that go off T4–6 pre-empt your T6–8 kill window. Disrupt their pieces early.
- **Cyclonic Rift / Farewell are devastating** — recursion is thin, recovery takes 3+ turns. Re-ramp and re-deploy from hand.
- **Politically loud** — Annihilator triggers and 12/12 Eldrazi draw the table's fire. Expect to be the early target once the engine fires.
- **Strong against creature aggro** — Void Winnower wall, lifelink/ward bodies, token floods.

## Reskins (for borrowers)

| On the card | Really is | What it does |
|---|---|---|
| The Banyan Tree | The Great Henge | Cost reduced by your greatest creature power; +1/+1 and a draw on each nontoken creature ETB; {T}: {G}{G} + 2 life. |
| Green Dragon Inn | Homeward Path | Utility land; {T}: each player gains control of creatures they own — undoes creature theft. |
