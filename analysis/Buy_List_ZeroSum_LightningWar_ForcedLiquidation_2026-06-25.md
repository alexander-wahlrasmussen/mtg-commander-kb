# Buy List — Assemble Zero-Sum Game + Lightning War + Forced Liquidation

**Date:** 2026-06-25
**Scenario:** Keep all three target decks built at once; **dismantle Diminishing Returns** (cards return to pool); the other 13 active decks stay built and hold their physical copies.
**Mode:** **Worst case** = true buys (owned 0) **+** contention buys (owned but locked in a deck that stays built).
**Source:** `scripts/assemble_buy_list.py` over `collection/moxfield_haves_2026-06-25-0748Z.csv`.
**Forced Liquidation build:** `decks/considering/forced-liquidation-20260625.txt` (Displacer Kitten pass + Bolas/Channeler combo pass — see below). Prior builds archived under `archive/old_decklists/` (`-20260612`, `-20260623`).

> ✅ **Verified against the current collection.** Re-run on the fresh **2026-06-25** Moxfield export and the result is byte-identical to the earlier 06-07 run — so the count is a real shortfall, not a stale-snapshot ceiling. (The 06-25 export differs from 06-07 only by −Sublime Epiphany −Timeless Witness +Thassa's Oracle, none of which are in these three decks.)

**Total: 80 copies** — 57 true buys + 23 contention buys. *(Down from 87 before the FL passes.)*

---

## Forced Liquidation optimization pass (Displacer Kitten)

The 06-23 build applied 7 swaps to the 06-12 list. **GC count unchanged at 3/3** (Mana Vault, Notion Thief, Demonic Tutor — all swap-ins verified non-GC and Commander-legal). Net effect on the buy list: drops the single priciest card (Wheel of Fortune) plus Memory Jar, and adds only one cheap new buy (Jace's Archivist) — the other 6 swap-ins are already owned and free.

| Out (was a buy) | In | Swap-in status |
|---|---|---|
| Wheel of Fortune *(premium buy)* | Jace's Archivist | **buy** (owned 0) — repeatable wheel-on-a-stick |
| Memory Jar *(premium buy)* | Displacer Kitten | owned, free — blinks Kefka / rocks per noncreature spell |
| Diabolic Tutor | Grim Tutor | owned, free |
| Mastermind's Acquisition | Final Parting | owned, free |
| Bedevil | Soul Shatter | owned, free |
| Terminate | Heartless Act | owned, free |
| Infernal Grasp | Dismember | owned, free |

*(Dark Deal kept — it's a discard wheel.)*

**Final Parting** is confirmed free — the old Calamity-Tax contention note was stale (that deck is now Croak and Dagger with its swaps applied; it doesn't run Final Parting).

### 06-25 follow-up pass — Bolas/Channeler combo (all owned, $0)

Two further swaps, both owned (no buy-list impact — total stays 81):

| Out | In | Rationale |
|---|---|---|
| Naktamun Lorespinner *(`// Wheel of Fortune`, conditional/slow wheel)* | Aether Channeler | combo piece + flexible value; deck still runs ~7 wheel effects |
| Prismatic Lens *(weakest of 11 mana rocks)* | Nicol Bolas, the Ravager | ETB *each opponent discards* → triggers Megrim / Liliana's Caress / Waste Not; cheap evasive threat that transforms |

**New win axis — combo-lab verified (CSB `find_combos`):**

> **Displacer Kitten + Aether Channeler + Sol Ring + Mana Vault → infinite ETB + infinite colorless mana** (registered complete combo `1170-1393-2364-5034`).

Kill conversion (sound by card text; CSB registers the engine, not the final drain): choose Aether Channeler's *"draw a card"* ETB each iteration with a draw-payoff already in the deck —
- **Niv-Mizzet, Parun** → 1 damage to any target per draw → aim lethal at all opponents (cleanest, no self-deck risk), or
- **Psychosis Crawler** → each opponent loses 1 per draw → table drain.

Commander-independent and resolves on your turn (Abolisher-proof) — a second win axis alongside the wheel/punisher kill. GC count unchanged at 3/3 (both adds verified non-GC).

### Cost-cut: Time Spiral → Molten Psyche (owned, drops an €80 buy)

Time Spiral (~€80, the deck's priciest remaining buy) replaced by **Molten Psyche** (owned, ~€1–2): a {1}{R}{R} shuffle-wheel with a metalcraft burn (deck runs 11+ artifacts, so it deals damage = each opponent's draws on top of the punishers). Cheaper to cast (3 vs 6), easier color (RR vs UUU). Only loss is Time Spiral's land-untap. **Drops the buy-list total 81 → 80; the only premium FL buy left is Niv-Mizzet, Parun.**

### Clock lab (`scripts/kfk_clock_lab.py`, 40k trials, 2026-06-25)

| | T6 | T7 | T8 | T9 | median |
|---|---|---|---|---|---|
| decap (one opp) | 15% | 34% | 56% | 74% | **T8** |
| table (all three) | 9% | 21% | 40% | 59% | **T9** |

- **Clock = decap T8 / table T9.** Slower than the proposal's T6–7 brief bar (consistent with the framework's optimistic-hand-estimate pattern).
- **Combo contribution = zero.** The Kitten+Channeler combo assembles in only ~1.2% of games by T12 and never beats the burn — confirmed **resilience, not speed** (board/commander-independent, Abolisher-proof backup; justified because it's $0 and the pieces are good cards).
- **Time Spiral → Molten Psyche is clock-neutral** (1 of ~8 wheel sources; median unchanged).

---

## True buys — owned 0 copies in the snapshot (57)

### Forced Liquidation / Kefka (17)

| Card | Notes |
|---|---|
| Niv-Mizzet, Parun | premium — price-check (only premium FL buy left) |
| Echo of Eons | |
| Reforge the Soul | |
| Jace's Archivist | new from FL pass (replaces Wheel of Fortune) |
| Dark Deal | |
| Glint-Horn Buccaneer | |
| Kederekt Parasite | |
| Fate Unraveler | |
| Megrim | |
| Liliana's Caress | |
| Ob Nixilis, the Hate-Twisted | |
| Waste Not | |
| Bloodletter of Aclazotz | |
| Cursed Totem | |
| Bloodchief's Thirst | |
| Rakdos Charm | |
| Negate | |

### Zero-Sum Game / Witherbloom (32)

| Card | Notes |
|---|---|
| Deathrite Shaman | premium — price-check |
| Llanowar Elves | bulk dork |
| Arbor Elf | bulk dork |
| Fyndhorn Elves | bulk dork |
| Boreal Druid | bulk dork |
| Elves of Deep Shadow | bulk dork |
| Blood Artist | aristocrats core |
| Cauldron Familiar | aristocrats core |
| Witch's Oven | aristocrats core |
| Sprout Swarm | token engine (infinite piece) |
| Witherbloom Apprentice | |
| Vito, Thorn of the Dusk Rose | |
| Sanguine Bond | |
| Exquisite Blood | |
| Defiant Bloodlord | |
| Enduring Tenacity | |
| Pernicious Deed | |
| Abrupt Decay | |
| Professor Onyx | |
| Beseech the Queen | |
| Dark Petition | |
| Cabal Ritual | |
| Chain of Smog | |
| Corpse Dance | |
| Lab Rats | |
| Saproling Migration | |
| Hornet Queen | |
| Nature's Rhythm | |
| Increasing Ambition | |
| Castle Locthwain | |
| Darkbore Pathway | |
| Necroblossom Snarl | |

### Lightning War / Azula (8)

| Card | Notes |
|---|---|
| Banefire | |
| Comet Storm | |
| Galvanic Iteration | |
| Increasing Vengeance | |
| Reiterate | |
| Turnabout | |
| Gifts Ungiven | |
| Emeritus of Woe | |

---

## Contention buys — owned, but the physical copy is locked in a deck that stays built (23)

Not strictly must-buy. Alternatives: leave the card out of the new deck, proxy it, or accept it can only live in one deck. Buying a second copy lets both run it.

| Card | Own | Need (targets) | Locked in (kept decks) |
|---|---|---|---|
| Demonic Tutor | 4 | 2 (Zero-Sum, Forced Liq.) | Croak & Dagger, Curse of the Scarab, Dark Lords Army |
| Vampiric Tutor | 1 | 1 (Zero-Sum) | Radiation Sickness |
| Necropotence | 1 | 1 (Zero-Sum) | Genome Project |
| Deadly Rollick | 6 | 2 (Zero-Sum, Lightning War) | 5x (Croak, Dark Lords, Exiles, Genome, Grand Design) |
| Chaos Warp | 5 | 1 (Forced Liq.) | 5x (Eldrazi, Dark Lords, Exiles, Genome, Replication) |
| Go for the Throat | 2 | 1 (Forced Liq.) | Curse of the Scarab, Dark Lords Army |
| Drown in the Loch | 1 | 1 (Forced Liq.) | Radiation Sickness |
| Peer into the Abyss | 1 | 1 (Forced Liq.) | Genome Project |
| Underworld Dreams | 1 | 1 (Forced Liq.) | Dark Lords Army |
| Torment of Hailfire | 1 | 1 (Lightning War) | Croak & Dagger |
| Bonus Round | 1 | 1 (Lightning War) | Genome Project |
| Diabolic Intent | 2 | 1 (Zero-Sum) | Dark Lords Army, Exiles Return |
| Delighted Halfling | 1 | 1 (Zero-Sum) | Eldrazi Stampede |
| Dryad Arbor | 1 | 1 (Zero-Sum) | Croak & Dagger |
| Springheart Nantuko | 1 | 1 (Zero-Sum) | Earthbend the Meta |
| Tendershoot Dryad | 1 | 1 (Zero-Sum) | Eldrazi Stampede |
| Underground Mortuary | 1 | 1 (Zero-Sum) | Croak & Dagger |
| Warren Soultrader | 1 | 1 (Zero-Sum) | Curse of the Scarab |
| Yavimaya, Cradle of Growth | 5 | 1 (Zero-Sum) | 5x (Croak, Earthbend, Radiation, Grand Design, Bunny) |
| Past in Flames | 1 | 2 (Lightning War, Forced Liq.) | *internal dup — need 2nd copy* |
| Seething Song | 1 | 2 (Lightning War, Forced Liq.) | *internal dup — need 2nd copy* |
| Ponder | 2 | 2 (Lightning War, Forced Liq.) | Crystal Sickness |
| Preordain | 2 | 2 (Lightning War, Forced Liq.) | Crystal Sickness |

---

## Freed by dismantling Diminishing Returns (resolve to $0, already counted)

Phyrexian Altar, Ashnod's Altar, Viscera Seer, Zulaport Cutthroat, Skullclamp, Toxic Deluge, Razaketh the Foulblooded, Malakir Rebirth, Mirkwood Bats, Bojuka Bog, Phyrexian Tower, Polluted Delta, Verdant Catacombs, Gemstone Caverns, plus mana rocks (Sol Ring, Arcane Signet, Command Tower, Fellwar Stone, Mind Stone, Thought Vessel, Exotic Orchard, Lightning Greaves, Swiftfoot Boots, Dark Ritual) and 8 Swamp.

---

## Full copy-paste list (80 lines — Moxfield / Cardmarket / CardTrader format)

```
1 Abrupt Decay
1 Arbor Elf
1 Banefire
1 Beseech the Queen
1 Blood Artist
1 Bloodchief's Thirst
1 Bloodletter of Aclazotz
1 Bonus Round
1 Boreal Druid
1 Cabal Ritual
1 Castle Locthwain
1 Cauldron Familiar
1 Chain of Smog
1 Chaos Warp
1 Comet Storm
1 Corpse Dance
1 Cursed Totem
1 Dark Deal
1 Dark Petition
1 Darkbore Pathway
1 Deadly Rollick
1 Deathrite Shaman
1 Defiant Bloodlord
1 Delighted Halfling
1 Demonic Tutor
1 Diabolic Intent
1 Drown in the Loch
1 Dryad Arbor
1 Echo of Eons
1 Elves of Deep Shadow
1 Emeritus of Woe
1 Enduring Tenacity
1 Exquisite Blood
1 Fate Unraveler
1 Fyndhorn Elves
1 Galvanic Iteration
1 Gifts Ungiven
1 Glint-Horn Buccaneer
1 Go for the Throat
1 Hornet Queen
1 Increasing Ambition
1 Increasing Vengeance
1 Jace's Archivist
1 Kederekt Parasite
1 Lab Rats
1 Liliana's Caress
1 Llanowar Elves
1 Megrim
1 Nature's Rhythm
1 Necroblossom Snarl
1 Necropotence
1 Negate
1 Niv-Mizzet, Parun
1 Ob Nixilis, the Hate-Twisted
1 Past in Flames
1 Peer into the Abyss
1 Pernicious Deed
1 Ponder
1 Preordain
1 Professor Onyx
1 Rakdos Charm
1 Reforge the Soul
1 Reiterate
1 Sanguine Bond
1 Saproling Migration
1 Seething Song
1 Springheart Nantuko
1 Sprout Swarm
1 Tendershoot Dryad
1 Torment of Hailfire
1 Turnabout
1 Underground Mortuary
1 Underworld Dreams
1 Vampiric Tutor
1 Vito, Thorn of the Dusk Rose
1 Warren Soultrader
1 Waste Not
1 Witch's Oven
1 Witherbloom Apprentice
1 Yavimaya, Cradle of Growth
```
