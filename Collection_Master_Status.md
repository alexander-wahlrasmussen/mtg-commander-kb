# Collection Master Status

Last updated: 2026-04-24
Source: `moxfield_haves_2026-04-24-2112Z.csv` — DeckSafe run against 11 digitized decks.

---

## Collection snapshot

| Stat | Value |
|---|---|
| Unique cards owned | 2,676 |
| Total copies owned | 5,868 |
| Digitized decks tracked | 11 |
| Decks at 100% owned | 10 |
| Cards with insufficient copies | 8 unique / 9 copies |
| Shared cards (2+ decks) | 135 |

---

## Per-deck completion

Decks with `.txt` files in `decks/` and tracked by DeckSafe. Completion is physical ownership — a shared card counts for whichever deck holds it.

| Deck | Commander | % Complete | Notes |
|---|---|---|---|
| Crystal Sickness | Golbez, Crystal Collector | 100% | — |
| Curse of the Scarab | The Scarab God | 94% | 6 cards missing — see Shopping List |
| Diminishing Returns | Teysa Karlov | 100% | — |
| Earthbend the Meta | Toph, the First Metalbender | 100% | — |
| Eldrazi Stampede Chaos | Maelstrom Wanderer | 100% | Not in Deck_Index.md — needs entry |
| Peace Offering | Ms. Bumbleflower | 100% | — |
| Radiation Sickness | The Wise Mothman | 100% | — |
| The Genome Project | Kuja, Genome Sorcerer | 100% | — |
| The Loam Cycle | Teval, the Balanced Scale | 100% | — |
| The Replication Crisis | Satya, Aetherflux Genius | 100% | — |
| This Bunny Goes To Market | Ms. Bumbleflower | 100% | Not in Deck_Index.md — needs entry |

---

## Decks without digital decklists

These appear in `Deck_Index.md` but have no `.txt` in `decks/`. Not tracked by DeckSafe — collection completeness unknown.

| Deck | Commander |
|---|---|
| The Grand Design | Atraxa, Grand Unifier |
| Divine Constellation | Sythis, Harvest's Hand |
| The Calamity Tax | Glarb, Calamity's Augur |
| Lightning War | Fire Lord Azula |
| The Dark Lord's Army | Sauron, the Dark Lord |
| The Exile's Return | Fire Lord Zuko |
| Lorehold Spirits | Quintorius |

---

## Shopping list

Cards to acquire as of last DeckSafe run.

| Card | Need | Have | Deck |
|---|---|---|---|
| Champion of the Perished | 1 | 0 | Curse of the Scarab |
| Diregraf Captain | 1 | 0 | Curse of the Scarab |
| Headless Rider | 1 | 0 | Curse of the Scarab |
| Zombie Apocalypse | 1 | 0 | Curse of the Scarab |
| Snow-Covered Swamp | 2 | 2 | Curse of the Scarab |
| Yavimaya Coast | 2 more | 1 of 3 | Eldrazi, Peace Offering, Bunny |
| Willowrush Verge | 1 more | 1 of 2 | Eldrazi, Radiation Sickness |
| Sunpetal Grove | 1 more | 1 of 2 | Peace Offering, Bunny |

See full Shopping List tab in `collection/deck_safe_collection.xlsx` or the [Google Sheet](https://docs.google.com/spreadsheets/d/1UjtdLELu2PzlvE99_r1vbvzPb22Vmi0qVBpo6nnt6UY).

---

## Zero-surplus shared cards (physical swap required to play both decks)

Cards where owned copies exactly equal demand across multiple decks — physically moving them between decks to play simultaneously. Not a collection gap, but a logistics note.

High-value cards at exactly zero surplus:

| Card | Copies | # Decks |
|---|---|---|
| An Offer You Can't Refuse | 7 | 7 |
| Esper Sentinel | 4 | 4 |
| Arcane Denial | 3 | 3 |
| Pongify | 3 | 3 |
| Craterhoof Behemoth | 2 | 2 |
| The Scarab God | 2 | 2 |

Full zero-surplus list is in the Shared Cards tab of the spreadsheet.

---

## Maintenance

- Re-run DeckSafe after any decklist change or new Moxfield export (see `WF_Deck_Safe_Collection.md`).
- Archive the old Moxfield CSV to `archive/` rather than deleting.
- Update this file after each DeckSafe run — the spreadsheet is the source of truth, this file is the human-readable summary.
