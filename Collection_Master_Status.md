# Collection Master Status

Cross-deck collection rollup — what's owned, deployed, and shared across decks (DeckSafe snapshot). Deck *contents* are ground-truthed by each `.txt`; this is the collection-wide view.

Last updated: **2026-07-08 (real DeckSafe run).**
Source: `collection/moxfield_haves_2026-07-06-1850Z.csv` — DeckSafe run against the 16 active digitized decks.

> **2026-07-08 — DeckSafe re-run (this replaces the 06-30/07-08 "as-if-bought" planning markers).**
> **Zero-Sum Game** and **Forced Liquidation** are now **physically assembled and DeckSafe-verified 100% owned**
> (their final cards were sourced by **dismantling Diminishing Returns** — 10 cards → Zero-Sum, Lightning Greaves →
> Forced Liquidation; the rest of DR returned to the pool). **Diminishing Returns is retired** — its `.txt`+summary
> are archived to `archive/old_decklists/` and it is out of the tracked set. Roster is now **16 decks, 15 at 100%**;
> the only gap is **Croak and Dagger (92%)** — the 8 "Glarb Inevitable" combo buys still predate this CSV — plus four
> shared cards owed a 2nd copy (Aetherflux Reservoir, Triumph of the Hordes, Willowrush Verge, Imperial Recruiter).

> **2026-07-03 DeckSafe re-run (xlsx only):** rebuilt `collection/deck_safe_collection.xlsx`
> against the 2026-06-25 CSV after the Bumbleflower **quiet-exits swap**
> (`this-bunny-goes-to-market-20260703.txt`: −Misleading Signpost −Sin −Rewind → +Intruder Alarm
> +Approach of the Second Sun +Wizard Class). New unowned demand: **Intruder Alarm** (≈ €2.84) +
> **Approach of the Second Sun** (≈ €2.79) — 2-card buy ≈ €6 *(indicative, Scryfall 2026-07-03)*;
> Wizard Class owned. The prose tables below are otherwise unchanged from the last full pass.

---

## Collection snapshot

| Stat | Value |
|---|---|
| Unique cards owned | 3,088 |
| Total copies owned | 6,754 |
| Digitized decks tracked | 16 |
| Decks at 100% owned | 15 of 16 (Croak and Dagger at 92%) |
| Cards with insufficient copies | 12 unique / 12 copies |
| Shared cards (2+ decks) | 232 |

---

## Per-deck completion

Decks with `.txt` files in `decks/` and tracked by DeckSafe. Completion is physical ownership — a shared card counts for whichever deck holds it. Percentages are the 2026-07-08 DeckSafe run.

| Deck                      | Commander                   | % Complete | Notes                              |
| ------------------------- | --------------------------- | ---------- | ---------------------------------- |
| Croak and Dagger          | Glarb, Calamity's Augur     | 92%        | 8 short — the Glarb Inevitable topdeck-combo buys (Ancient Cellarspawn, Emergent Ultimatum, Fortune Teller's Talent, Insidious Dreams, One with the Multiverse, Scheming Symmetry, The Reality Chip, Tidal Barracuda) predate this CSV |
| Crystal Sickness          | Golbez, Crystal Collector   | 100%       | —                                  |
| Curse of the Scarab       | The Scarab God              | 100%       | —                                  |
| Earthbend the Meta        | Toph, the First Metalbender | 100%       | —                                  |
| Eldrazi Stampede Chaos    | Maelstrom Wanderer          | 100%       | —                                  |
| Forced Liquidation        | Kefka, Court Mage           | 100%       | **Physically assembled 2026-07-08** (final card — Lightning Greaves — from the DR teardown); DeckSafe-verified |
| Lightning War             | Fire Lord Azula             | 100%       | —                                  |
| Lorehold Spirits          | Quintorius, History Chaser  | 100%       | —                                  |
| Radiation Sickness        | The Wise Mothman            | 100%       | —                                  |
| The Dark Lord's Army      | Sauron, the Dark Lord       | 100%       | —                                  |
| The Exile's Return        | Fire Lord Zuko              | 100%       | Imperial Recruiter is a zero-surplus share with Replication Crisis (own 1, both want it) |
| The Genome Project        | Kuja, Genome Sorcerer       | 100%       | Aetherflux Reservoir is a zero-surplus share with Croak and Dagger |
| The Grand Design          | Atraxa, Grand Unifier       | 100%       | —                                  |
| The Replication Crisis    | Satya, Aetherflux Genius    | 100%       | −Strionic +Imperial Recruiter (`-20260630.txt`); 2nd Recruiter copy owed (shared with Exile's Return) |
| This Bunny Goes To Market | Ms. Bumbleflower            | 100%       | —                                  |
| Zero-Sum Game             | Witherbloom, the Balancer   | 100%       | **Physically assembled 2026-07-08** (10 cards from the DR teardown); DeckSafe-verified |

### Retired / dismantled (not tracked by DeckSafe)

| Deck                | Commander                 | Note |
| ------------------- | ------------------------- | ---- |
| Diminishing Returns | Teysa Karlov              | **Dismantled 2026-07-08** — donor for Zero-Sum Game (10 cards) + Forced Liquidation (Lightning Greaves); cards returned to pool, `.txt`+summary archived |
| Peace Offering      | Ms. Bumbleflower          | **Dismantled 2026-06-13** — redundant 2nd Bumbleflower (This Bunny is active); cards returned to pool |
| The Loam Cycle      | Teval, the Balanced Scale | **Dismantled 2026-06-08** — decklist archived 2026-06-11; cards returned to pool |

---

## Decks without digital decklists

These appear in `Deck_Index.md` but have no `.txt` in `decks/`. Not tracked by DeckSafe — collection completeness unknown.

| Deck                 | Commander              |
| -------------------- | ---------------------- |
| Divine Constellation | Sythis, Harvest's Hand |

---

## Shopping list

The 14 cards short across the full demand pool (2026-07-08 run + the quiet-exits buys restored 2026-07-09 — the 07-08 run predated the stranded `this-bunny-goes-to-market-20260703.txt` landing). The bulk is Croak and Dagger's combo package; the rest are 2nd copies of cards shared between two decks (zero-surplus — you own one, two decks want it).

| Card                    | Need | Have | Decks                                          |
| ----------------------- | ---- | ---- | ---------------------------------------------- |
| Ancient Cellarspawn     | 1    | 0    | Croak and Dagger                               |
| Emergent Ultimatum      | 1    | 0    | Croak and Dagger                               |
| Fortune Teller's Talent | 1    | 0    | Croak and Dagger                               |
| Insidious Dreams        | 1    | 0    | Croak and Dagger                               |
| One with the Multiverse | 1    | 0    | Croak and Dagger                               |
| Scheming Symmetry       | 1    | 0    | Croak and Dagger                               |
| The Reality Chip        | 1    | 0    | Croak and Dagger                               |
| Tidal Barracuda         | 1    | 0    | Croak and Dagger                               |
| Intruder Alarm          | 1    | 0    | This Bunny Goes To Market (quiet-exits 07-03)  |
| Approach of the Second Sun | 1 | 0    | This Bunny Goes To Market (quiet-exits 07-03)  |
| Aetherflux Reservoir    | 2    | 1    | Croak and Dagger, The Genome Project           |
| Triumph of the Hordes   | 2    | 1    | Earthbend the Meta, Radiation Sickness         |
| Willowrush Verge        | 2    | 1    | Eldrazi Stampede Chaos, Radiation Sickness     |
| Imperial Recruiter      | 2    | 1    | The Exile's Return, The Replication Crisis     |

See full Shopping List tab in `collection/deck_safe_collection.xlsx` or the [Google Sheet](https://docs.google.com/spreadsheets/d/1UjtdLELu2PzlvE99_r1vbvzPb22Vmi0qVBpo6nnt6UY).

---

## Zero-surplus shared cards (physical swap required to play both decks)

Cards where owned copies exactly equal demand across multiple decks — physically moving them between decks to play simultaneously. Not a collection gap, but a logistics note. **112** cards sit at zero surplus (2026-07-08 run); top instances by deck count:

| Card                       | Copies | # Decks |
| -------------------------- | ------ | ------- |
| Swan Song                  | 7      | 7       |
| Deadly Rollick             | 7      | 7       |
| Counterspell               | 7      | 7       |
| Yavimaya, Cradle of Growth | 6      | 6       |
| Otawara, Soaring City      | 6      | 6       |
| Nature's Lore              | 6      | 6       |
| Force of Negation          | 6      | 6       |
| Chaos Warp                 | 6      | 6       |
| Dark Ritual                | 5      | 5       |
| Cyclonic Rift              | 5      | 5       |
| Boseiju, Who Endures       | 5      | 5       |
| Black Market Connections   | 5      | 5       |
| Beast Within               | 5      | 5       |

Full zero-surplus list is in the Shared Cards tab of the spreadsheet.

---

## Maintenance

- Re-run DeckSafe after any decklist change or new Moxfield export (see `WF_Deck_Safe_Collection.md`).
- Archive the old Moxfield CSV to `archive/` rather than deleting.
- Update this file after each DeckSafe run — the spreadsheet is the source of truth, this file is the human-readable summary.
