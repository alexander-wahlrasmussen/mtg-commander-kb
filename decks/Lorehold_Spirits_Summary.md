# Lorehold Spirits — Quintorius, History Chaser

**Status:** Post-upgrade. 12 swaps applied 2026-05-03 — see Changelog. Goblin Bombardment is included in the .txt as a placeholder for a planned physical purchase; until acquired, the combo line in Kill Reliability is offline and the deck plays at the lower of the two scores listed.

## Quick Reference

| Field | Value |
|---|---|
| **Commander** | Quintorius, History Chaser ({2}{R}{W}, Legendary Planeswalker — Quintorius) |
| **Colors** | Boros (RW) |
| **Archetype** | Spirit tokens powered by graveyard cycling — recursion *is* the token engine |
| **Bracket** | 3 (3 Game Changers used; 3-card combo line under house-rules exception; no MLD; no extra turns) |
| **Game Changers** | Gamble, Smothering Tithe, Teferi's Protection — verified against `REF_Game_Changers_List.md` on 2026-05-03 |
| **Conversion Check** | **17/20** (5/4/4/4) — rises to **18/20** (5/5/4/4) when Goblin Bombardment is physically present |
| **Kill Window** | Goldfish: T7–9 · Through interaction: T9–11 |
| **Decklist file** | `decks/lorehold-spirit-20260503-154449.txt` |

The 17/20 supersedes both the inherited 17/20 entry in `Deck_Index.md` (which was undocumented) and the audited pre-upgrade 12/20. The score is now grounded in a written assessment of the post-upgrade list.

**Card text verification status:** Quintorius (user-supplied), Anointed Procession, Purphoros, Hofri Ghostforge, Reveillark verified via web sources during this audit. Other proposed adds rely on widely-known oracle text and are flagged text-unverified — review on Scryfall before sleeve-up.

-----

## Commander Rules Text

> **Quintorius, History Chaser** — {2}{R}{W} — Legendary Planeswalker — Quintorius
>
> Whenever one or more cards leave your graveyard, create a 3/2 red and white Spirit creature token.
>
> +1: You may discard a card. If you do, draw two cards, then mill a card.
>
> −4: Spirits you control gain double strike and vigilance until end of turn.
>
> *Quintorius, History Chaser can be your commander.*

The static ability is the central engine. Every recursion piece in the deck — Sun Titan, Karmic Guide, Reveillark, Sevinne's Reclamation, Serra Paragon, Teshar, Mistveil Plains, Emeria the Sky Ruin, flashback spells — triggers a 3/2 Spirit token creation. A *single* graveyard event makes one Spirit (the trigger reads "one or more cards"); reanimating two creatures with one Reveillark trigger still produces only one token, not two. But repeated graveyard activity over a turn cycle stacks tokens fast.

The +1 is a discard outlet that nets cards (discard 1, draw 2, mill 1 = +1 card and +1 yard activity). The mill grows the graveyard *for the next time something leaves it*, which is why this loyalty button is itself an engine piece, not just card draw.

The −4 is a finisher button. From a 6-spirit board with anthems active, double strike + vigilance turns combat into lethal across the table.

**Critical note: planeswalker durability profile.** Quintorius is a planeswalker, not a creature. He doesn't die to creature wipes (Wrath, Tragic Arrogance, Fateful Tempest), but he dies to combat damage redirected by opponents and to direct damage. He cannot be protected by Selfless Spirit / Guardian of Faith.

**Rules nuance — verify at the table:** Whether tokens "leaving the graveyard" via state-based actions (a token dying, briefly entering the graveyard, then ceasing to exist) triggers Quintorius's static is the rules-critical question. Mainstream interpretation says yes, which means Hofri Spirit tokens dying and Treasures from Smothering Tithe being sacrificed each fire the static. If a judge rules otherwise, the deck still works — the static fires plenty from real-card recursion alone — but several of the multipliers in the Kill Lines below contract.

-----

## What the Deck Does

The engine is graveyard cycling, and the engine is the token engine. Cards entering the graveyard via discard, sacrifice, death, or self-mill set up Quintorius's static; cards leaving the graveyard via recursion fire it. Every recursion event is a Spirit token. Anointed Procession doubles each Spirit. Purphoros pings 2 per Spirit ETB. The deck is designed to feed itself.

### Layer 1 — Graveyard Fillers (set up the static)

- **Discard outlets:** Quintorius +1 (discard 1, draw 2, mill 1), Faithless Looting, Conspiracy Theorist (discard payoff), Containment Construct (discard outlet that ramps), Squee Goblin Nabob (free discard target — recurs from yard), Seize the Spoils (discard 2 + treasure ramp).
- **Sacrifice outlets:** Goblin Bombardment (sac creature for 1 damage — the combo enabler, pending physical purchase). Smothering Tithe Treasures sacrificed for mana.
- **Direct cast from yard:** Faithless Looting flashback, Sevinne's Reclamation flashback (each "leaves graveyard" event = 1 static trigger).
- **Yard-targeting plays:** Hofri Ghostforge exiling dying nontoken creatures (the *exile* doesn't trigger Quintorius — only when those exiled cards eventually return to graveyard via the Hofri token's leaves-bf clause).

### Layer 2 — Recursion (fire the static)

Every card returning from graveyard to battlefield, hand, or library is one or more Quintorius static triggers:

- **From graveyard to battlefield:** Sun Titan attacks (≤MV3 permanent), Karmic Guide ETB (any creature), Reveillark leaves bf (up to two ≤2 power), Sevinne's Reclamation ({2}{W}, ≤MV3 permanent + flashback), Serra Paragon (≤MV3 permanent each turn), Teshar (creature on legendary cast), Angel of Indemnity (lifegain + recursion), Emeria the Sky Ruin (free creature with 7+ Plains).
- **From graveyard to hand:** Squee Goblin Nabob (returns to hand at upkeep — leaves graveyard).
- **From graveyard to library:** Mistveil Plains (target white card → bottom of library).

### Layer 3 — Token Multiplier and Payoffs

- **Anointed Procession:** Every Quintorius static trigger creates 2 Spirits instead of 1. Every Hofri token doubled. Every Treasure from Tithe doubled.
- **Purphoros, God of the Forge:** Every Spirit ETB = 2 damage to each opponent. Indestructible at low devotion. With Procession in play, each static trigger = 4 damage to each opponent.
- **Patchwork Banner:** Spirit anthem + +1/+1 counter on each Spirit entry.
- **Balefire Liege:** Anthem (+1/+1 to RW creatures) + 3 damage to opponent on each RW spell cast.
- **Tocasia's Welcome:** Token-entry draws.
- **Staff of the Storyteller:** Spirit-themed token + draw engine.
- **Hofri Ghostforge:** +1/+1 trample haste to all Spirits; nontoken-creature death → token Spirit copy.

### Layer 4 — Kill Buttons

- **Quintorius −4:** Double strike + vigilance EOT for all your Spirits.
- **Akroma's Will:** Both modes with commander on bf — flying, vigilance, double strike, lifelink, indestructible, protection from each color. Instant. Closes lethal turns through removal.
- **Boros Charm:** Three modes — indestructible team / 4 damage to player or planeswalker / target gets double strike. Multi-tool.
- **Moonshaker Cavalry:** ETB gives all your creatures flying + counter. From a wide board, one-turn lethal.

### Layer 5 — Tutors and Ramp

- **Gamble** (GC): Tutors any card at random-discard cost. Finds Hofri, Reveillark, Goblin Bombardment, Purphoros, Anointed Procession. Random discard is acceptable in a graveyard deck — discarded targets become recursion fodder.
- **Smothering Tithe** (GC): Treasure tokens from opponent draws. Treasures sacrificed for mana = potential static triggers.
- **Mox Amber:** With 9+ legendary permanents in the deck plus a planeswalker commander, effectively turn-1 ramp.

### Layer 6 — Combo Finish (pending Goblin Bombardment)

Reveillark + Karmic Guide + Goblin Bombardment + a 2-or-less creature card in graveyard:

1. Sac Reveillark to GB (1 dmg). Reveillark trigger: return Karmic Guide + the 2-or-less from graveyard. *(Quintorius static: 2 cards left graveyard simultaneously = 1 Spirit token.)*
2. Karmic Guide ETB: return Reveillark from graveyard. *(Quintorius static: 1 card left graveyard = 1 Spirit token.)*
3. Sac the 2-or-less creature to GB (1 dmg). Now in graveyard.
4. Sac Karmic Guide to GB (1 dmg). Now in graveyard. Persist returns it with -1/-1 counter (Karmic Guide is power 2 base, so persist returns once; after that the persist trigger doesn't fire because she has a -1/-1 counter).
5. Sac Reveillark again. Reveillark trigger: return Karmic Guide (now power 1) + the 2-or-less. Loop continues.

Per cycle: 3+ damage from GB, 2+ Quintorius static triggers, +2 Spirit tokens (4 with Anointed Procession). With Hofri off the battlefield (he interferes — see Rules Edges), the loop is unbounded once assembled.

**Hofri interaction:** Hofri's exile-and-token replacement effect interferes with the Reveillark loop because Reveillark itself gets exiled when it dies (rather than landing in graveyard for re-recursion). The combo turn often wants Hofri removed first, sacrificed as fuel, or the Hofri Spirit tokens used as the sac-outlet creatures. Practically, the combo and the Hofri value-engine are alternative paths to lethal — both cards are valuable, and either is sufficient.

-----

## Kill Lines

Six closing lines. The combo line (Line 6) is offline until Goblin Bombardment is physically acquired. The other five close T7–9 from a stable position.

### Line 1 — Quintorius Ultimate + Akroma's Will (Primary)

Activate Quintorius's −4 with 4+ Spirits in play (most turns of the mid-game). Cast Akroma's Will at end of opponent's turn or in response to removal: gives the team flying + vigilance + double strike + lifelink + indestructible + protection from each color. Swing for lethal across the table. Akroma's Will makes the alpha-strike unstoppable through removal AND wraths. Closes T7–9 reliably.

### Line 2 — Purphoros + Procession + Recursion Turn

With Purphoros and Anointed Procession both in play, every Quintorius static trigger creates 2 Spirits = 4 damage to each opponent from Purphoros. A turn with three recursion events (Sun Titan attack, Karmic Guide ETB, Sevinne's Reclamation flashback) = 12 damage to each opponent passively. Add Hofri token deaths and the math escalates. Non-combat closer; works through tap-down or chump blockers.

### Line 3 — Moonshaker Cavalry Burst

Moonshaker Cavalry ETB gives each creature flying + counter. With Anointed Procession multiplying tokens prior and Patchwork Banner anthem, one-turn lethal swing on a single opponent. Recurring Moonshaker via Hofri (Spirit token copy) re-fires the ETB.

### Line 4 — Boros Charm 4 Damage Mode

Sometimes the kill is "Boros Charm 4 damage" to finish a low-life opponent at instant speed. Niche, but a real line — the deck has so many incremental damage sources that opponents often arrive at the kill turn with 4–8 life.

### Line 5 — Spirit Swarm + Anthem Grindout (Backup)

Patchwork Banner, Balefire Liege (+ 3 dmg per RW spell cast), and Tocasia's Welcome (draw) provide a 3–4 turn grindout when Quintorius and Moonshaker are both unavailable.

### Line 6 — Reveillark / Karmic Guide / Goblin Bombardment Combo (Pending)

See Layer 6 above. Once GB is in the deck, the loop assembles around T7–8, deals arbitrary damage, generates arbitrary Spirit tokens, and is house-rules legal as a 3+ card combo per `REF_Bracket_3_House_Rules.md`. Until GB is acquired, this line is **offline**.

-----

## Expected Kill Window

### Goldfish: T7–9 (T6 fastest)

- T1: Sol Ring or Mox Amber. Discard outlet on curve.
- T2–3: Mind Stone / Fellwar Stone / Arcane Signet. Smothering Tithe T3 if drawn.
- T4: Quintorius commander. First Spirit token created on next yard event.
- T5–6: Hofri Ghostforge (4 mana) or Karmic Guide (5 mana with WW). First recursion turn.
- T6–7: Anointed Procession (4 mana) or Purphoros (5 mana). Engine multiplier active.
- T7–9: Quintorius +1 → +1 → −4 with Akroma's Will. Lethal across table.

The fastest goldfish is T6: Sol Ring T1, Quintorius T2 (Mox Amber + Sol Ring + 1 land), Hofri T3 (with continued ramp), recursion T4, Procession T5, kill T6. Requires near-perfect opening.

The average goldfish is T8.

### Through Interaction: T9–11

- **Quintorius removed once:** Recast for 6 mana, accepts loyalty reset. Hofri / engine pieces continue to fire static.
- **Single board wipe at T7:** Hofri exiles dying creatures and creates Spirit tokens — the wipe converts to a refill. Selfless Spirit and Guardian of Faith protect the team from one wipe. Akroma's Will indestructibility blocks creature wipes outright. Recovery: 1–2 turns.
- **Repeated commander removal + Hofri removal:** Slowest scenario. Falls back to Sun Titan, Sevinne's Reclamation, Serra Paragon, Reveillark recursion. Still a real game plan — the recursion shell doesn't depend on either commander or Hofri to function — but kill window slips to T11.
- **Cyclonic Rift:** Worst case. Bounces Hofri / recursion creatures to hand, Spirit tokens vanish. Recovery: 3 turns. Teferi's Protection is the answer if held — phases out the team and saves the kill turn.

The 2-turn gap between goldfish and through-interaction is consistent with a deck whose engine is genuinely resilient: Quintorius (planeswalker) survives creature wipes, Hofri tokens replace dying creatures, recursion shell rebuilds from any single reset.

-----

## Conversion Check Breakdown

### Core Loop: 5/5

The loop is "graveyard activity → Quintorius static → Spirit tokens → multipliers → damage / pressure." Counted engine pieces:

- 7 token producers (Quintorius cmdr, Quintorius FH, Hofri, Venerable Warsinger, Vanguard, Augusta, Anointed Procession multiplier)
- 9 recursion pieces (Sun Titan, Karmic Guide, Reveillark, Sevinne's, Serra Paragon, Teshar, Angel of Indemnity, Emeria, Mistveil Plains)
- 6 yard fillers (Faithless Looting, Conspiracy Theorist, Containment Construct, Squee, Seize the Spoils, Quintorius +1 ability)
- 6 payoffs (Patchwork Banner, Tocasia's Welcome, Staff of the Storyteller, Balefire Liege, Purphoros, Anointed Procession)
- 2 tutors (Gamble for any piece, Smothering Tithe for mana to deploy them)
- 1 combo enabler (Goblin Bombardment, pending)

That's 30+ cards directly serving the loop. Past the 18-card threshold for 5. The integration is also tight — Quintorius's static is the single bridge between yard activity and tokens, which means every recursion piece is a token producer and every token producer feeds future yard activity. Cover the commander and the engine identity is unmistakable.

**Checkpoint:** Cover the commander. The 99 has 9 recursion pieces, 7 token producers, 6 yard fillers, 6 payoffs, 2 tutors. The deck is the engine.

### Kill Reliability: 4/5 (5/5 once Goblin Bombardment is acquired)

Six closing lines. Five active, one pending. Two are non-combat (Purphoros + Procession passive damage; future combo). Two are instant-speed alpha strikes (Quintorius + Akroma's Will; Boros Charm 4 dmg mode). One is a standard combat threat (Moonshaker burst). One is grindout backup.

The window from engine-online to lethal is 1–2 turns thanks to Akroma's Will making the alpha strike unstoppable. The line is also resilient against removal — Akroma's Will gives indestructible AND protection from each color, which dodges most board interaction.

Doesn't reach 5 currently because the combo line (Line 6) is offline pending GB. With Bombardment in the deck, the combo provides a closing line that ignores combat entirely and assembles late enough to be house-rules legal — that's a 5.

**Checkpoint:** Engine online (Quintorius + Hofri + 4 Spirits) → Quintorius +1 +1 then −4 + Akroma's Will + Patchwork Banner anthem = ~30+ damage spread across the table. Achievable T7–8. Through one wipe, T9.

### Durability: 4/5

Quintorius (planeswalker) survives creature wipes. Hofri converts deaths into Spirit tokens — wipes become refills. Akroma's Will indestructibility + protection blocks most board removal outright. Teferi's Protection (GC) phases out the team for a full turn cycle, surviving Cyclonic Rift, Farewell, and the table's combo turn.

Recursion redundancy is high: Sun Titan, Karmic Guide, Reveillark, Sevinne's Reclamation, Serra Paragon, Teshar, Angel of Indemnity, Emeria the Sky Ruin. Losing any one piece doesn't break the engine. Smothering Tithe + Mox Amber + ramp suite means recasting Quintorius after removal isn't crippling.

Doesn't reach 5 because the deck still folds to graveyard hate (Rest in Peace, Leyline of the Void, Grafdigger's Cage shut off the recursion shell entirely). There are zero answers to graveyard hate in the 99 — the deck has no enchantment removal beyond Kami of Ancient Law (single creature, easy to kill back) and Generous Gift (only 1 copy). A resolved graveyard-hate enchantment effectively wins the game against this deck.

**Checkpoint:** Cyclonic Rift on T7. Teferi's Protection if held. Otherwise: replay Quintorius for 6, replay Hofri or substitute recursion piece for 4–5, refill yard via Quintorius +1 over 2 turns. Threatening again T9–10.

### Interaction: 4/5

12 interaction pieces:

- **Targeted removal (5):** Path to Exile, Swords to Plowshares, Skyclave Apparition (ETB exile), Rip Apart (modal creature/artifact), Generous Gift (instant catch-all)
- **Land hate (1):** White Orchid Phantom (basic land destruction)
- **Enchantment removal (1):** Kami of Ancient Law
- **Graveyard hate (1):** Remorseful Cleric
- **Board wipes (3):** Tragic Arrogance (asymmetric), Fateful Tempest, Wave of Reckoning (combat damage)
- **Protection / save (1):** Teferi's Protection (GC, instant team phase-out)

Generous Gift and Teferi's Protection are the new-quality interaction pieces. Generous Gift answers any permanent at instant speed for {2}{W} — it's the closest thing to a counterspell this deck has. Teferi's Protection saves the team from a pod-killer turn.

Doesn't reach 5 because the deck still has zero stack interaction. Boros lacks counters; the closest substitutes are sorcery-speed answers and Generous Gift's instant-speed target removal. Against a resolved combo trigger or a counterspell at the wrong time, the deck can't intervene. Also: the wipes are mana-intensive (5–6 each) and partially symmetric.

**Checkpoint:** The player across from you is about to win next turn. Realistic odds of a stop in this deck: Generous Gift in hand on a key permanent, Path / Swords on a creature, Teferi's Protection to save your own kill turn. ~35–45% odds of a meaningful intervention in any given game.

### Total: 17/20 — Elite tier (just clearing the floor)

5/4/4/4 with Goblin Bombardment as a pending upgrade. Once GB physically arrives, the combo line goes live and Kill Reliability moves to 5 → 18/20.

The structural pattern — 5 in Core Loop, 4 across the other three — is typical of a strongly-integrated engine deck. The deck *runs* its plan reliably. The remaining ceiling is held back by two specific gaps: graveyard-hate vulnerability (Durability) and zero stack interaction (Interaction). Both are accepted Boros constraints.

-----

## Bracket 3 Compliance

**Game Changers:** 3 of 3 used.
1. **Gamble** — random-discard tutor for any card. Finds engine pieces and combo halves.
2. **Smothering Tithe** — Treasure tokens from opponent draws. Ramp + resource pressure.
3. **Teferi's Protection** — instant team phase-out. Pod-killer save.

**Infinite combos:** One 3-card combo line — Reveillark + Karmic Guide + Goblin Bombardment + a 2-or-less creature card in graveyard. House-rules legal under `REF_Bracket_3_House_Rules.md` (3+ cards required, late-game assembly typical T7+). Currently *offline* until GB is physically acquired. Pod approval recommended before activating in tournament-grade play.

**Extra turns:** None.

**Mass land denial:** None. White Orchid Phantom destroys a single basic — does not constitute MLD.

-----

## Pod Fit

1. **Mid-speed but resilient.** Goldfish T7–9 puts the deck in line with Earthbend, Replication Crisis, Crystal Sickness — competitive against most Bracket 3 pods, behind Loam Cycle and Calamity Tax.
2. **Strong against creature decks.** Tragic Arrogance, Wave of Reckoning, Fateful Tempest are still here. Akroma's Will indestructible mode protects your team from opposing wipes.
3. **Improved against combo.** Generous Gift answers any permanent at instant speed. Teferi's Protection saves the team. Still no counter-magic — combo pods remain the worst matchup, but no longer a free win for the opponent.
4. **Vulnerable to graveyard hate.** A resolved Rest in Peace, Leyline of the Void, or Grafdigger's Cage shuts off recursion entirely. Kami of Ancient Law and Generous Gift are the only answers — one of each in 99 cards is thin coverage.
5. **Improved against repeated commander removal.** Quintorius is a planeswalker (survives creature wipes), and Mox Amber + Smothering Tithe make recasting cheap. The deck no longer collapses if Quintorius eats two consecutive removal spells.
6. **Combo-pod legal.** The Reveillark loop is a 3+ card combo and assembles T7+ in normal play. Pre-pod disclosure recommended in tournament-style settings; kitchen-table pods can let it ride.

-----

## Differentiation From Other Decks

| | Lorehold Spirits (Quintorius HC) | Diminishing Returns (Teysa) |
|---|---|---|
| Engine | Cards leaving graveyard → Spirit tokens | Sacrifice triggers → drain |
| Token type | Spirits (3/2 from static, copies from Hofri) | Various (Teysa doublings) |
| Closing line | Combat (Quintorius ult / Akroma's Will) + burn (Purphoros) + combo (Reveillark/KG/GB) | Drain / aristocrat triggers |
| Colors | RW (no counters, weak GY hate) | WB (removal + drain, no counters) |
| Graveyard role | Recursion-driven Spirit production | Triggered abilities source |
| Combo line | 3-card (Reveillark + KG + GB) | None |

Both lean on death triggers, but Lorehold returns creatures to the battlefield where Diminishing Returns drains opponents from the deaths themselves. Mechanically distinct.

| | Lorehold Spirits (Quintorius HC) | Crystal Sickness (Golbez) |
|---|---|---|
| Engine | Graveyard cycling → tokens via static | Artifact ETBs → surveil → drain |
| Color identity | RW | UB |
| Recursion target | Creatures + permanents (Sun Titan/Sevinne's range) | Creatures (drain bombs) |
| Kill speed | T7–9 | T7–9 |

Both reanimator-adjacent, different resources (yard + tokens vs. artifact count + yard), different colors.

-----

## Known Weaknesses

- **Graveyard hate.** Rest in Peace / Leyline of the Void / Grafdigger's Cage shut off the recursion shell. Two answers in the 99 (Kami of Ancient Law, Generous Gift) is below where this deck wants to be — consider tutoring with Gamble specifically when graveyard hate is on the table.
- **Stack interaction is still zero.** Boros constraint. A counterspell on the kill turn can't be stopped. Mitigated by Akroma's Will protection + Teferi's Protection, both of which dodge interaction differently.
- **Combo line dependence on Goblin Bombardment.** Until GB is acquired physically, Line 6 is paper. The deck still scores 17/20 without it (5/4/4/4); the upgrade to 18 requires the physical card.
- **Hofri / Reveillark interaction is awkward.** Hofri exiles dying creatures, which interferes with the Reveillark loop's need for the actual cards in graveyard. Real-table play will require sequencing — typically removing Hofri before assembling the combo, or using Hofri Spirit tokens as the sac fuel.
- **Mana base is now adequate, not strong.** Sacred Foundry adds one true Boros dual, but the deck still has no fetchlands. Tapped lands punish the curve at T3–T5.

-----

## Future Upgrade Targets

- **Goblin Bombardment** (planned purchase) — activates the combo line.
- **Heliod's Intervention** or similar — Boros enchantment removal, if found. Closes the graveyard-hate gap.
- **Replenish** — re-deploys multiple destroyed enchantments at once (Hardened Scales / Anointed Procession recovery).
- **Cathars' Crusade** — every creature entering puts +1/+1 on all your creatures. Massive Spirit-token amplifier, would push Core Loop and Kill Reliability density further.

-----

## Changelog

- **2026-05-03 (upgrade pass):** 12 swaps. **Adds:** Anointed Procession, Gamble (GC), Purphoros, Reveillark, Sacred Foundry, Smothering Tithe (GC), Akroma's Will, Boros Charm, Generous Gift, Mox Amber, Teferi's Protection (GC), Goblin Bombardment (placeholder pending purchase). **Cuts:** Currency Converter, Drumbellower, Millikin, Secret Rendezvous, Naktamun Lorespinner, Lorehold Charm, Primary Research, Ceaseless Conflict, Monologue Tax, Claim Jumper, Lorehold Archivist, 1 Plains. **Score:** 12/20 (3/3/3/3) → 17/20 (5/4/4/4), 18/20 once GB arrives. **GC slots:** 0/3 → 3/3.
- **2026-05-03 (baseline audit):** Summary created. Pre-upgrade baseline: 12/20 (3/3/3/3). Supersedes the inherited 17/20 entry in `Deck_Index.md`.

-----

## Decklist (100 cards) — current state, file `lorehold-spirit-20260503-154449.txt`

### Commander (1)

1 Quintorius, History Chaser

### Game Changers (3)

1 Gamble
1 Smothering Tithe
1 Teferi's Protection

### Token Producers / Spirit Tribal (7)

1 Quintorius, Field Historian
1 Hofri Ghostforge
1 Venerable Warsinger
1 Augusta, Order Returned
1 Vanguard of the Restless
1 Spirit of Resilience
1 Anointed Procession

### Token Payoffs (5)

1 Patchwork Banner
1 Tocasia's Welcome
1 Staff of the Storyteller
1 Balefire Liege
1 Purphoros, God of the Forge

### Recursion Engines (8)

1 Sun Titan
1 Karmic Guide
1 Reveillark
1 Sevinne's Reclamation
1 Serra Paragon
1 Teshar, Ancestor's Apostle
1 Angel of Indemnity
1 Relic Retriever

### Big ETB / Death Trigger Targets (5)

1 Ao, the Dawn Sky
1 Atsushi, the Blazing Sky
1 Moonshaker Cavalry
1 Skyclave Apparition
1 White Orchid Phantom

### Discard Outlets / Yard Fillers (5)

1 Faithless Looting
1 Conspiracy Theorist
1 Containment Construct
1 Squee, Goblin Nabob
1 Seize the Spoils

### Sacrifice Outlet (1)

1 Goblin Bombardment *(placeholder — pending physical purchase)*

### Yard / Library Manipulation (1)

1 Perpetual Timepiece

### Lorehold / Quintorius Support (2)

1 Quintorius, Loremaster
1 Kirol, History Buff

### Counter / Equipment Synergy (3)

1 Bitterthorn, Nissa's Animus
1 Excava, the Risen Past
1 Laelia, the Blade Reforged

### Removal — Targeted (5)

1 Path to Exile
1 Swords to Plowshares
1 Rip Apart
1 Generous Gift
1 Kami of Ancient Law

### Graveyard Hate (1)

1 Remorseful Cleric

### Wipes (3)

1 Tragic Arrogance
1 Fateful Tempest
1 Wave of Reckoning

### Protection / Combat Tricks (4)

1 Selfless Spirit
1 Guardian of Faith
1 Akroma's Will
1 Boros Charm

### Card Advantage (1)

1 Advanced Reconstruction

### Yard Utility / Misc (2)

1 Anger
1 Guardian Scalelord

### Ramp / Rocks (6)

1 Sol Ring
1 Arcane Signet
1 Mind Stone
1 Fellwar Stone
1 Archaeomancer's Map
1 Mox Amber

### Lands (37)

1 Battlefield Forge
1 Clifftop Retreat
1 Command Tower
1 Emeria, the Sky Ruin
1 Exotic Orchard
1 Fabled Passage
1 Fields of Strife
1 Furycalm Snarl
1 Glittering Massif
1 Lorehold Campus
1 Lotus Field
1 Mistveil Plains
1 Radiant Summit
1 Rugged Prairie
1 Sacred Foundry
1 Sacred Peaks
1 Study Hall
1 Sunscorched Divide
1 Temple of Triumph
1 Terramorphic Expanse
1 Turbulent Steppe
6 Mountain
10 Plains

*Total: 99 mainboard + 1 commander = 100. Game Changers: 3 of 3.*
