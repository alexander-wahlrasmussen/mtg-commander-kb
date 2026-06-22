# Zero-Sum Game — Witherbloom, the Balancer

## Quick Reference

| Field | Value |
|---|---|
| **Commander** | Witherbloom, the Balancer ({6}{B}{G}, 5/5 Legendary Creature — Elder Dragon) |
| **Colors** | Golgari (BG) |
| **Archetype** | Spellslinger-drain / lifeloop combo (bracket-4-in-spirit) |
| **Bracket** | 3 by GC count (3/3). Contains a 2-card infinite — **pod-approved** for this build (2026-06-01, extension of the Berta approval). |
| **Game Changers** | Necropotence, Vampiric Tutor, Demonic Tutor (3 of 3 slots used) |
| **Conversion Check** | *Not yet audited.* Proposal ceiling 18–19/20; the clock lab tempers the Speed axis — formal audit after first pod games. |
| **Kill Window** | Clock: **T9 decap = T9 table** **(spell, instant)** (median; 12% T5 / 25% T6 / 37% T7 / 48% T8; lab 2026-06-11, `wb_clock_lab.py`). Decap and table converge by construction — the loop kills the whole table the turn it closes. Blocked-out boards (no combat ignition): median T11. Through interaction: unmodeled *(unverified)*. |
| **Status** | **CARDS ON ORDER** — built 2026-06-11 from the v2b proposal list; 51 cards on the DeckSafe Shopping List (`deck_safe_collection.xlsx`, Zero Sum Game rows). **Rev 2026-06-19:** swap −Beast Within −Heroic Intervention → +Chain of Smog +Professor Onyx (`zero-sum-game-20260619.txt`); the new 2-card infinite is pod-accepted under the 2026-06-19 house-rule revision (infinites accepted). The `.txt` is the target state until the order lands. |

-----

## Commander Rules Text

Witherbloom, the Balancer — three abilities (verified `card_lookup.py` 2026-06-01, re-checked 2026-06-11):

1. **Affinity for creatures** (on herself): she costs {1} less per creature you control — 8 MV shrinks to the {B}{G} floor with 6+ bodies.
2. **Flying, deathtouch.**
3. **"Instant and sorcery spells you cast have affinity for creatures."** Generic-cost reduction only — coloured pips are untouched. This is the deck's mana engine: with a token board out, every tutor, ritual, and buyback spell costs its coloured pips only.

She is not required for the *primary* kill (the lifeloop is commander-independent), but she is **the engine for the secondary affinity-infinite axis** (see Combo Suite Audit) — so she is both a tutor-discount and a combo enabler, not "not a combo piece" as earlier drafts claimed.

-----

## What the Deck Does

Go wide cheaply (dorks, Bitterblossom, Saprolings, Hornet Queen), then convert board width into spell discounts and the board+spells into one of three drain engines:

1. **The lifeloop (primary):** one *blood-half* + one *vito-half* + any life event = the table dies.
   - Blood-halves ("opponent loses → you gain"): **Exquisite Blood**, **Bloodthirsty Conqueror**
   - Vito-halves ("you gain → opponent loses"): **Vito, Thorn of the Dusk Rose**, **Sanguine Bond**, **Enduring Tenacity**, **Defiant Bloodlord** (+ Professor Dellian Fel's −6 emblem as a 7th copy)
   - 2 × 4 redundancy is why this finds itself: 6 of the 8 pieces are creatures or enchantment creatures, so Chord of Calling / Finale of Devastation / Nature's Rhythm fetch them straight onto the battlefield.
2. **Affinity infinite (secondary kill, NOT a "slow clock"):** with Witherbloom out and 4+ creatures, her spell-affinity zeroes the buyback on **Sprout Swarm** (convoke pays the {G}; the green Saproling it makes feeds the next cast) and on **Lab Rats** (paired with **Phyrexian Altar**: sac a Rat for {B}, recast for {B}, repeat). Both are *bona fide infinite* magecraft loops (Commander Spellbook-confirmed, 2026-06-19) — each cast drains the table through **Witherbloom Apprentice**. Earlier drafts called this "a slow drain clock"; that was wrong. It is commander-DEPENDENT (so it comes online later than the loop), which is why it's the secondary axis, not the primary.
3. **Razaketh chain:** tokens become tutors at 2 life each; finds whatever the loop is missing at instant speed.

**Igniters** (anything that starts the loop once both halves are down): any unblocked attacker (combat damage = life loss), Witherbloom Apprentice + any spell, Cauldron Familiar (+ Witch's Oven for every-turn recursion), any Food token ({2}, sac: gain 3 — Gilded Goose ships with one), Blood Artist / Zulaport Cutthroat / Marionette Apprentice + a sacrifice, Dellian Fel's +2.

-----

## Kill Lines

**Line A — Exquisite Blood loop (primary).** Deploy a blood-half (5 MV) and a vito-half (3–5 MV), trigger once, table dies at instant speed. Confirmed by Sanguine Bond's own ruling: the loop runs until a player wins or someone breaks it. Commander-independent; survives a Witherbloom tax-out completely.

**Line B — affinity infinite (secondary).** Witherbloom + 4+ creatures + **Sprout Swarm** (self-contained) OR **Lab Rats + Phyrexian Altar** → infinite free casts → **Witherbloom Apprentice** drains the table. A real infinite, not a clock — but commander-DEPENDENT, so it assembles later than the loop (isolated lab `wb_storm_lab.py`: standalone ~T12 / often beyond horizon because it needs the 8-mana commander + a payoff + the engine + a board; the loop is commander-free and faster). Its value is **resilience**, not speed: it wins through a different vector when the enchantment loop is answered.

**Line C — Razaketh assembly.** 8 MV body that turns every token into Vampiric Tutor. The lab models him fetching missing loop pieces; he also finds answers.

**Backup — combat.** Bitterblossom fliers + Tendershoot + Hornet Queen; irrelevant as a clock (T12+), relevant as ignition and Razaketh fuel.

-----

## Combo Suite Audit (Commander Spellbook find-my-combos, 2026-06-19)

A systematic scan (variants API over the deck's combo-dense cards) confirms Zero-Sum carries **three independent infinite axes**, not one:

1. **Lifeloop** (commander-INDEPENDENT) — Exquisite Blood / Bloodthirsty Conqueror + any of {Sanguine Bond, Vito, Enduring Tenacity, Defiant Bloodlord} (+ Professor Dellian Fel). Up to 8 two-card configs → highest redundancy; the T9 primary.
2. **Sprout Swarm** affinity infinite (commander-dependent) → drains via Witherbloom Apprentice.
3. **Lab Rats + Phyrexian Altar** affinity infinite (commander-dependent) → drains via Witherbloom Apprentice.

~10 infinite kill configurations across two payoff types. Hating out one axis does **not** disarm the deck — its real strength is redundancy/resilience, which the lone T9 clock number understates. (Corrected lab: `wb_storm_lab.py`. An earlier finite-drip model wrongly called the affinity lines "slow"; they are infinites.)

### Added 2026-06-19 (in the `.txt`)

Committed swap **−Beast Within −Heroic Intervention → +Chain of Smog +Professor Onyx** (`decks/zero-sum-game-20260619.txt`, old list archived). Both adds verified mono-B; neither is a Game Changer (3/3 GC unaffected — Necropotence/Vampiric/Demonic). **Prices unverified — check at order.** Chain of Smog is a new 2-card infinite — **pod-accepted** under the 2026-06-19 house-rule revision (`REF_Bracket_3_House_Rules.md`: infinites are now evaluated on merit, not gated on approval).

- **Chain of Smog** ({1}{B}) — with the in-deck Witherbloom Apprentice, a two-card infinite drain needing **no board and no commander** ([combo](https://commanderspellbook.com/combo/326-2522/)). The only line that survives loop-hate AND commander removal AND a clogged board — the highest-value diversification.
- **Professor Onyx** (6, planeswalker) — second magecraft payoff (each opp loses **2**) backing Chain of Smog + both affinity infinites; incidental drain on the deck's instants/sorceries + a resilient body.
- Cut rationale: the deck keeps 3 catch-all removal (Assassin's Trophy, Abrupt Decay, Pernicious Deed) + Toxic Deluge + Deadly Rollick + Veil of Summer, so −Beast Within −Heroic Intervention leaves the interaction/protection suite intact.

Marginal near-misses (NOT recommended — redundant with existing axes): Academy Manufactor / Samwise Gamgee (Cauldron Familiar infinites); additional Exquisite Blood partners (Marauding Blight-Priest, Vizkopa Guildmage, etc.).

-----

## Decklist (100 cards)

### Commander (1)
1 Witherbloom, the Balancer

### Drain Payoffs (lifeloop + magecraft) (9)
1 Exquisite Blood
1 Bloodthirsty Conqueror
1 Vito, Thorn of the Dusk Rose
1 Sanguine Bond
1 Enduring Tenacity
1 Defiant Bloodlord
1 Professor Dellian Fel
1 Witherbloom Apprentice
1 Professor Onyx

### Affinity-Infinite / Magecraft Loop (3)
1 Sprout Swarm
1 Lab Rats
1 Chain of Smog

### Aristocrats — Sac Payoffs & Igniters (5)
1 Blood Artist
1 Zulaport Cutthroat
1 Marionette Apprentice
1 Cauldron Familiar
1 Mirkwood Bats

### Sacrifice Outlets & Recursion (6)
1 Phyrexian Altar
1 Ashnod's Altar
1 Warren Soultrader
1 Viscera Seer
1 Witch's Oven
1 Corpse Dance

### Token Generators / Go-Wide (5)
1 Bitterblossom
1 Saproling Migration
1 Tendershoot Dryad
1 Hornet Queen
1 Springheart Nantuko

### Mana Dorks (10)
1 Birds of Paradise
1 Llanowar Elves
1 Elvish Mystic
1 Fyndhorn Elves
1 Boreal Druid
1 Arbor Elf
1 Elves of Deep Shadow
1 Gilded Goose
1 Delighted Halfling
1 Deathrite Shaman

### Mana Rocks & Rituals (5)
1 Sol Ring
1 Arcane Signet
1 Jet Medallion
1 Dark Ritual
1 Cabal Ritual

### Tutors (10)
1 Vampiric Tutor
1 Demonic Tutor
1 Beseech the Queen
1 Increasing Ambition
1 Dark Petition
1 Chord of Calling
1 Finale of Devastation
1 Nature's Rhythm
1 Diabolic Intent
1 Razaketh, the Foulblooded

### Card Advantage / Draw (4)
1 Necropotence
1 Skullclamp
1 Black Market Connections
1 Night's Whisper

### Interaction & Protection (6)
1 Assassin's Trophy
1 Abrupt Decay
1 Deadly Rollick
1 Toxic Deluge
1 Pernicious Deed
1 Veil of Summer

### Lands (36)
1 Overgrown Tomb
1 Woodland Cemetery
1 Twilight Mire
1 Tainted Wood
1 Llanowar Wastes
1 Necroblossom Snarl
1 Deathcap Glade
1 Darkbore Pathway
1 Undergrowth Stadium
1 Polluted Delta
1 Verdant Catacombs
1 Bloodstained Mire
1 Wooded Foothills
1 Misty Rainforest
1 Marsh Flats
1 Windswept Heath
1 Command Tower
1 Yavimaya, Cradle of Growth
1 Phyrexian Tower
1 Bojuka Bog
1 Boseiju, Who Endures
1 Castle Locthwain
1 Nurturing Peatland
1 Underground Mortuary
1 Khalni Garden
1 Dryad Arbor
1 Gemstone Caverns
5 Swamp
4 Forest

## Lab Results (wb_clock_lab.py, 40k trials, seed 20260611, 2026-06-11)

| cumulative % killed by | T5 | T6 | T7 | T8 | T9 | T10 | T12 | median |
|---|---|---|---|---|---|---|---|---|
| Standard goldfish (attack ignition) | 12 | 25 | 37 | 48 | 56 | 64 | 75 | **T9** |
| No-combat ignition (blocked out) | 2 | 8 | 18 | 27 | 36 | 43 | 57 | T11 |
| GC A/B: −Demonic +Mana Vault | 12 | 24 | 35 | 45 | 53 | 59 | 70 | T9 |

- **GC verdict: keep the tutor suite.** Mana Vault is flat-to-worse at every turn — same conclusion as the DR lab (combos want tutors, not fast mana).
- The proposal's "T6–7, majority by T8" (2026-06-07 deployment model) was again slightly optimistic: the harness says 48% by T8, median T9. Sixth-of-seven optimism for hand/semi-modeled claims; the lab number is the citable one.
- Model is conservative where it matters: Skullclamp / Black Market Connections / Night's Whisper draw, Dellian's 0, Corpse Dance recursion, and the entire Line B storm are all omitted. Optimistic: unblocked combat ignition, colour-blind mana, rocks tap same turn, no opposing interaction.

**Versus the pod combo opponent (T6–7 behind Grand Abolisher):** the raw race is level-or-ahead in ~25–37% of games. The rest is the interaction plan — and the kill itself is Abolisher-proof (triggered loop on our turn, no cast or activation an Abolisher can gate). Veil of Summer ×1 (owned ×3), Heroic Intervention, Deadly Rollick, and instant-speed creature removal (Abrupt Decay / Assassin's Trophy / Beast Within) for their Abolisher on *our* turn cover the combo window. This is the best racing profile in the roster, not a guaranteed out-race — honest framing per the framework clock rule.

-----

## The Grand Abolisher Plan

1. **The kill doesn't care.** Abolisher stops spells and activations *on its controller's turn*; our loop closes on our turn off triggered abilities.
2. **Kill it on sight, on our turn:** Abrupt Decay (uncounterable), Assassin's Trophy, Beast Within, Toxic Deluge, Pernicious Deed.
3. **Race insurance:** Veil of Summer for the combo turn vs UB interaction; Deadly Rollick free at their combo attempt.

-----

## Provenance & Files

- Decklist: `decks/zero-sum-game-20260619.txt` (100 cards: 99 + commander; rev 2026-06-19, prior `zero-sum-game-20260611.txt` archived to `archive/old_decklists/`)
- Proposal: `proposals/PROP_Witherbloom_the_Balancer.md` (2026-06-01, consistency scale-up 2026-06-07)
- Build readiness / donor analysis: `archive/proposals/Witherbloom_Build_Readiness_2026-06-11.md` (archived 2026-06-13 — deck is built)
- Source list: `archive/old_decklists/witherbloom-balancer-v2b-20260607.txt` minus Bayou / Cabal Coffers / Urborg (locked in protected decks, not strategy-critical) plus 2 Swamp 1 Forest
- Clock labs: `scripts/wb_clock_lab.py` (loop clock / gcswap / avail) + `scripts/wb_storm_lab.py` (Line-B affinity-infinite clock, 2026-06-19)
- Combo audit: Commander Spellbook find-my-combos scan, 2026-06-19 (see Combo Suite Audit above)
- Shopping list: `collection/deck_safe_collection.xlsx` → Shopping List tab, "Zero Sum Game" rows (51 cards; **prices unverified — check Cardmarket at order time**). **Added to .txt 2026-06-19: Chain of Smog + Professor Onyx (new buys, prices unverified; the new infinite is pod-accepted per the 2026-06-19 house-rule revision)** — see Combo Suite Audit.
- Card text: all combo pieces, igniters, and tutors verified via `card_lookup.py` (2026-06-01 / 06-07 / 06-11 logs in the proposal and readiness docs)

**Roster notes:** building this standalone consumed the deferred "Witherbloom into Calamity Tax as a 99" option (`decks/The_Calamity_Tax_Swaps_2026-06-01.md` §Witherbloom — now closed). Pest Control proposal is the natural roster casualty (same BG substrate, unbuilt). The Loam Cycle is dismantled and archived.
