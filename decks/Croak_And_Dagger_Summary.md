# Croak and Dagger — Glarb, Calamity's Augur

## Quick Reference

| Field | Value |
|---|---|
| **Commander** | Glarb, Calamity's Augur ({B}{G}{U}, 2/4 Frog Wizard Noble) |
| **Colors** | Sultai (BUG) |
| **Archetype** | Topdeck combo-control / inevitability — Sensei's Top loop → counter-immune burst, with a lands/Torment grind backup |
| **Bracket** | 3 by GC count (3/3). B4-in-spirit (a 3-card combo); the pod accepts infinites/combos (Rule-0 since 2026-06-19). No MLD, no extra turns. |
| **Game Changers** | Bolas's Citadel, Fierce Guardianship, Seedborn Muse (3 of 3) |
| **Conversion Check** | **18/20 (5/5/4/4)** · audited 2026-07-01 |
| **Kill Window** | Clock: **T9 decap / T9 table** (lab `glarb_inevitable_lab.py`, 2026-07-01) — the loop kills the whole table at once, so decap == table. Counter-immune Aetherflux payoff; protection ~76% available by T7. |
| **Status** | Built — promoted 2026-07-01 from the "Glarb Inevitable" proposal. Ground truth: `decks/croak-and-dagger-20260701.txt` |

-----

## Commander Rules Text

Glarb, Calamity's Augur {B}{G}{U}
Legendary Creature — Frog Wizard Noble (2/4)

- Deathtouch
- You may look at the top card of your library any time.
- You may play lands and cast spells with mana value 4 or greater from the top of your library.
- {T}: Surveil 2.

Glarb is the deck's **dig + big-spell engine**, not the combo linchpin. His surveil 2 (a free tap ability, untapped every opponent's turn by Seedborn Muse) sculpts the top of the library toward the combo pieces; his top-cast clause deploys the MV4+ enablers/payoffs/tutors for free. He is **not** the loop enabler himself — his top-cast is restricted to MV4+, and Sensei's Top is MV1, so the Top-recast loop runs off the no-MV-restriction enablers (Bolas's Citadel / One with the Multiverse / Fortune Teller's Talent / The Reality Chip). He costs only 3 mana, so he recasts trivially at 5, 7, 9 after removal.

-----

## What the Deck Does

The deck assembles a redundant "Topdeck Matters" loop and converts it into a counter-immune burst. **Sensei's Divining Top** ({T}: draw a card, then put Top back on top of the library) is the loop core; any **no-mana-value-restriction top-caster** — Bolas's Citadel (pay life = mana value), One with the Multiverse (one free cast/turn), Fortune Teller's Talent at level 2, or The Reality Chip — lets you recast Top off the top each iteration, chaining through the library. With a **payoff** online — Aetherflux Reservoir (gain 1 life per spell cast this turn, then "Pay 50 life: deal 50 to any target," an *ability* that can't be countered) or Ancient Cellarspawn (drain an opponent on every under-costed cast) — the loop banks arbitrary life and flings 50 at each opponent, or drains the table one cast at a time. Inevitability comes from **redundancy, not one combo**: four interchangeable enablers × two payoffs, stacked onto the top by non-GC topdeck tutors (Insidious Dreams, Emergent Ultimatum, Scheming Symmetry) and fed by Glarb's surveil, Sylvan Library, and Oracle of Mul Daya. Underneath the combo sits the old grind shell — 38 lands, Cabal Coffers + Urborg, and **Torment of Hailfire** as a board-independent X-drain backup for the ~10% of games the combo bricks — plus a full counter suite and **Tidal Barracuda** (a one-sided Grand Abolisher on your own turn) to protect the kill.

-----

## Kill Lines

**Line 1 — Aetherflux loop (primary, combo):** Sensei's Divining Top + any top-caster (Bolas's Citadel / One with the Multiverse / Fortune Teller's Talent L2 / The Reality Chip) + **Aetherflux Reservoir** all in play. Tap Top (draw it, Top goes back on top), recast Top off the library via the enabler, replay it, tap again — each cycle is a spell cast, so Aetherflux's per-turn gain escalates and you bank 50+ life fast, then **Pay 50: deal 50 to any target** (a counter-immune *ability*) at each opponent in turn. Assembles median **T9**; the loop kills the whole table, so decap == table.
**Line 2 — Cellarspawn drain (combo, redundant payoff):** the same loop with **Ancient Cellarspawn** as the payoff — every free/discounted Top recast (mana spent < mana value) drains the difference from an opponent, grinding the table out one cast at a time. This is the second, independent payoff axis so the kill isn't single-threaded on Aetherflux.
**Line 3 — Topdeck-tutored assembly (enabler):** Insidious Dreams (discard X → stack X cards on top in any order), Emergent Ultimatum (find 3 monocolored, cast 2 free), or Scheming Symmetry stacks the missing loop category on top for Glarb/Citadel; GSZ / Chord / Finale fetch the creature pieces (Ancient Cellarspawn, The Reality Chip). Pulls the T9 assembly a turn or two sooner.
**Line 4 — Torment of Hailfire (grind backup):** X=12+ off ~14 mana via Cabal Coffers + Urborg — a board-independent table drain for the ~10% of games the combo never assembles. *Single high-mana haymaker; the reason this line exists is the combo's brick rate, not speed.*
**Line 5 — Value grind (fallback):** Seedborn Muse + Glarb top-casting deploy Archon of Cruelty / Massacre Wurm and grind a focused opponent out when nothing else is up.

-----

## Kill Window

- **Goldfish:** Clock **T9 decap / T9 table** (lab `scripts/glarb_inevitable_lab.py --mode clock`, 20k trials, on `croak-and-dagger-20260701.txt`, 2026-07-01). FULL build (4 enablers · 2 payoffs · all tutors): median T9, ~90% assembled by T14, never-in-14 ≈ 10%. The exact 3-card LEAN line (Citadel + Top + Aetherflux only) is a mirage — median never, 59% never-in-14 — so **redundancy is the clock**, not any single trio.
- **Dig sensitivity:** median T10 → T8 across dig −1..+2 (robust, monotonic). Cabal Coffers/Urborg are *not* modelled, so the real clock is a touch faster than printed.
- **Through interaction:** protection ≥1 piece available ≈ **76% by T7** (→87% by T12): Fierce Guardianship / Force of Negation / Pact / Swan Song / Mana Drain / Veil / Tidal Barracuda. Pod standing: `pod_gauntlet.py` P(beat the T6–7 combo pod) ≈ **27–31%** (pure race 21%), up ~4× from the old grind's ~7–8% — a fair table share, not a top-tier pod-crusher (deliberately Bracket-3 + protection-heavy for the Abolisher meta).

-----

## Conversion Check — 18/20 (audited 2026-07-01)

Scored from the list per `reference/REF_The_Conversion_Check.md`. Four judged axes; the clock is measured. Re-scored on promotion from the old grind build's 18 (5/4/4/5) — **kill +1, interaction −1**.

| Axis | Score | Rationale |
|---|---|---|
| **Core Loop** | **5/5** | A redundant, coherent topdeck engine: Glarb top-casting + Sensei's Top + four interchangeable enablers, with Seedborn Muse / Valley Floodcaller untapping Glarb for surveil and free casts across the turn cycle. No single removal spell disrupts it — any enabler works. |
| **Kill Reliability** | **5/5** | A redundant 3-category combo (4 enablers × 2 payoffs) assembling median T9, ~90% in horizon, with a **counter-immune** payoff (Aetherflux's activated ability) — plus Torment of Hailfire as a board-independent grind backup for brick games. Up from 4: the old single, telegraphed, counterable, ~14-mana Torment is no longer the only plan. |
| **Durability** | **4/5** | Redundant (any-of-N pieces), 38 lands survive every wipe, Glarb recasts for 3, and Muldrotha / Noxious Revival / Savvy Trader / Timeless Witness rebuild the engine. Docked from 5: the combo pieces are removable permanents (artifact / enchantment / creature), and the promotion cut the grind shell's land-recursion (Crucible / Loam / Ramunap / Splendid), thinning the post-wipe land rebuild; graveyard hate bites the recursion. |
| **Interaction** | **4/5** | 5 counterspells (3 free) + Tidal Barracuda soft-lock + a real removal suite (Beast Within, Deadly Rollick, Force of Vigor, Culling Ritual, Meathook, Toxic Deluge, Venser) + Veil. Docked from the grind's 5: dropped Submerge, V.A.T.S., and Spore Frog for combo pieces — the raw answer count fell and the package tilted toward protecting our own combo over disrupting the table. |

**Reading:** Structurally excellent (18/20). The limiting axes are Durability and Interaction — both a function of the combo's fragility to targeted removal and graveyard hate, mitigated (not erased) by the redundancy and the retained Torment/grind floor.

-----

## Durability

Board wipe on turn 7? The 38-land base and Cabal Coffers survive it, Glarb recasts for 3 mana, and the combo is any-of-N: four enablers and two payoffs mean one Disenchant rarely stops the plan. Muldrotha replays a combo permanent from the yard every turn, Noxious Revival puts any card back on top (for Glarb/Citadel to cast for free), Savvy Trader re-buys a piece from the graveyard, and Timeless Witness / Reanimate recur the value creatures. The weaker recovery vector is against **graveyard hate**, which shuts the recursion off at once — answered by Force of Vigor, Beast Within, and Boseiju. When the combo can't be rebuilt, the deck falls back to the board-independent Torment/Coffers grind, which cares about none of the above.

-----

## Interaction Package

**13 pieces total.** Counters: 5 — Fierce Guardianship (free), Force of Negation (free), Pact of Negation (free), Mana Drain, Swan Song. Removal / sweepers: 7 — Beast Within, Deadly Rollick (free), Force of Vigor (free), Culling Ritual, The Meathook Massacre, Toxic Deluge, Venser Shaper Savant. Targeted protection / soft-stax: Tidal Barracuda (opponents can't cast on your turn — protects the combo turn), Veil of Summer. Instant speed: the counters + Deadly Rollick / Force of Vigor / Beast Within / Venser are all instant, and Seedborn Muse means you hold them up without skipping development.

-----

## Known Weaknesses

- **The combo pieces are removable permanents.** Spot removal / disenchant on the enabler or payoff sets you back — redundancy mitigates this but doesn't erase it.
- **Graveyard hate** (Rest in Peace, Dauthi Voidwalker) shuts off Reanimate, Noxious Revival, Muldrotha, and Savvy Trader at once. Answers: Force of Vigor, Beast Within, Boseiju.
- **Life-payment risk.** Bolas's Citadel casts cost life equal to mana value; a low life total with Aetherflux not yet online can kill *you*. Sequence a payoff (or Aetherflux's life gain) before deep Citadel digging.
- **Telegraphed.** Sensei's Top + Citadel + Aetherflux on the board screams combo — combo on your own turn behind Tidal Barracuda + counters, and don't announce it.
- **The exact 3-card line is rare.** The LEAN trio assembles only ~42% by T12; the deck leans on the *full* redundant suite. Cut too many enablers/payoffs and the clock collapses.

-----

## Don't-Miss Rulings

- **The Top loop needs a no-MV-restriction top-caster** — Bolas's Citadel / One with the Multiverse / Fortune Teller's Talent (level 2) / The Reality Chip. **Glarb alone cannot recast Sensei's Top** (it's MV1, and his top-cast is restricted to MV4+); Glarb digs and casts the big pieces, the enabler runs the Top loop.
- **Aetherflux Reservoir** gains "1 life for **each** spell you've cast **this turn**" (escalating — the nth cast this turn gains n), and **"Pay 50 life: deal 50 damage to any target" is an activated ability** — it can't be countered and hits *one* target per activation, so bank the life, then fling 50 at each opponent in turn.
- **Bolas's Citadel** casts from the top cost **life equal to mana value** (not mana). Watch your life total; get the payoff / lifegain online before digging deep.
- **Tidal Barracuda** — "your opponents can't cast spells during your turn" (a one-sided Grand Abolisher that protects the combo turn), but it *also* lets **any** player cast at flash, so opponents gain flash on **their** turns. Combo on your own turn.
- **Ancient Cellarspawn** drains only when **mana spent < mana value** — it needs a free or discounted cast (One with the Multiverse's free cast, Savvy Trader / Fortune Teller L3 reductions) to trigger; a normally-paid spell does nothing.
- **Emergent Ultimatum** finds three **monocolored** cards with **different names**; an opponent shuffles one back and you cast the other two for free — Glarb, most tutors, and the payoffs are monocolored, so grab an enabler + a payoff.
- **Seedborn Muse** untaps Glarb and all your lands on **every** opponent's turn — surveil, hold up counters, and free-cast off the top each turn cycle without skipping development.
- **Valley Floodcaller** flash-enables your noncreature spells **and** untaps Glarb (a Frog) on each noncreature cast — chain surveils and casts in a single turn.

-----

## Decklist (100 cards)

### Commander (1)
- Glarb, Calamity's Augur

### Game Changers (3)
- Bolas's Citadel  *(GC)*
- Fierce Guardianship  *(GC)*
- Seedborn Muse  *(GC)*

### Combo — Loop & Enablers (4)
- Sensei's Divining Top
- One with the Multiverse
- Fortune Teller's Talent
- The Reality Chip

### Combo — Payoffs (2)
- Aetherflux Reservoir
- Ancient Cellarspawn

### Combo — Topdeck Tutors (3)
- Insidious Dreams
- Emergent Ultimatum
- Scheming Symmetry

### Creature Tutors (3)
- Green Sun's Zenith
- Chord of Calling
- Finale of Devastation

### X-Drain / Grind Backup (1)
- Torment of Hailfire

### Extra Land Drops (4)
- Exploration
- Azusa, Lost but Seeking
- Oracle of Mul Daya
- Icetill Explorer

### Landfall / Ramp Payoffs (5)
- Aesi, Tyrant of Gyre Strait
- Lotus Cobra
- Nissa, Resurgent Animist
- Lumra, Bellow of the Woods
- Tatyova, Benthic Druid

### Land Tutors / Ramp (11)
- Farseek
- Nature's Lore
- Three Visits
- Skyshroud Claim
- Hour of Promise
- Open the Way
- Tempt with Discovery
- Pir's Whim
- Sowing Mycospawn
- Omenpath Journey
- Planar Genesis

### Mana Acceleration (2)
- Sol Ring
- Birds of Paradise

### Card Advantage / Engine (2)
- Sylvan Library
- Valley Floodcaller

### Recursion / Cost-Reducers (6)
- Reanimate
- Agadeem's Awakening
- Noxious Revival
- Muldrotha, the Gravetide
- Timeless Witness
- Savvy Trader

### Finishers — Value Creatures (2)
- Archon of Cruelty
- Massacre Wurm

### Counterspells (4)
- Force of Negation
- Mana Drain
- Pact of Negation
- Swan Song

### Removal / Interaction (7)
- Beast Within
- Deadly Rollick
- Force of Vigor
- Culling Ritual
- The Meathook Massacre
- Toxic Deluge
- Venser, Shaper Savant

### Protection (2)
- Tidal Barracuda
- Veil of Summer

### Lands (38)
- Alchemist's Refuge
- Ba Sing Se
- Bayou
- Bloodstained Mire
- Bojuka Bog
- Boseiju, Who Endures
- Breeding Pool
- Cabal Coffers
- Command Tower
- Dryad Arbor
- Flooded Strand
- Forest
- Golgari Rot Farm
- Hedge Maze
- Horizon of Progress
- Marsh Flats
- Maze of Ith
- Minamo, School at Water's Edge
- Mistrise Village
- Misty Rainforest
- Otawara, Soaring City
- Overgrown Tomb
- Polluted Delta
- Scalding Tarn
- Shifting Woodland
- Talon Gates of Madara
- Three Tree City
- Tropical Island
- Undercity Sewers
- Underground Mortuary
- Underground Sea
- Urborg, Tomb of Yawgmoth
- Urza's Cave
- Verdant Catacombs
- Vesuva
- Windswept Heath
- Wooded Foothills
- Yavimaya, Cradle of Growth

-----

## Piloting Notes (for borrowers)

**Mulligan.** Finding-gated: keep 2–4 lands with a way toward the pieces — Glarb castable on curve, Sensei's Top, an enabler, or a topdeck tutor. Ramp-heavy hands are also keepable (they power the Torment/Coffers backup). Toss no-land spell hands and hands with a payoff but no engine behind it. The deck's redundancy does the finding — keep A/B testing (glarb_inevitable_lab, 2026-07-03) showed plan-mulliganing buys only ~+1pp on the assembly clock, and digging with real card costs bleeds held protection (66→60% by T4). Mulligan clearly dead hands once; keep serviceable sixes.

- **Keep:** Glarb + fixing; Top + an enabler; ramp toward Coffers.
- **Toss:** spell-heavy no-land hands; a lone payoff with no dig.

**Threats & timing.**

- **Combo on your own turn** behind Tidal Barracuda (opponents locked out) + a held counter. The kill (Aetherflux's ability) can't be countered, but the *enabler/payoff* can be removed in response, so protect the setup.
- **Don't dig yourself to death** with Bolas's Citadel — get a payoff or lifegain online first.
- **Graveyard hate is the real weakness** — hold Force of Vigor / Beast Within / Boseiju for Rest in Peace.
- **When the combo bricks, pivot to grind:** 38 lands + Coffers + Urborg → Torment of Hailfire X=12+ is board-independent and cares about none of the pod's creature removal.
- **Seedborn Muse means you never choose** between holding counters and developing — do both.

-----

## Changelog

- **2026-07-01:** **Promoted the "Glarb Inevitable" topdeck-combo rebuild to the roster** (`croak-and-dagger-20260701.txt`), replacing the grind-fortress lands build (`…20260623-215731`, archived). −13 (Demonic Tutor, Gray Merchant, Kokusho, Rite of Replication, Submerge, V.A.T.S., Crucible of Worlds, Life from the Loam, Splendid Reclamation, Ramunap Excavator, Titania's Command, Spore Frog, Blossoming Tortoise) / +13 (Bolas's Citadel, Sensei's Divining Top, Aetherflux Reservoir, Ancient Cellarspawn, One with the Multiverse, Fortune Teller's Talent, The Reality Chip, Savvy Trader, Emergent Ultimatum, Insidious Dreams, Tidal Barracuda, Tatyova, Scheming Symmetry). Only GC change: Demonic Tutor → Bolas's Citadel (still 3/3). Clock T13→T9 (lab `glarb_inevitable_lab.py`); CC 18 re-scored (5/4/4/5 → 5/5/4/4); P(beat pod) ~7–8% → ~27–31%. Trade-off: vs Ur-Dragon ~88% → ~78% (the retained Torment grind covers the ~10% brick, so likely ~83–85%). Reconciled the candidate to a legal 100 by restoring Tempt with Discovery (the proposal's Out list was 13; the candidate had over-cut it, leaving 99).
