# Collection Master Status

Last updated: 2026-04-29
Source: `moxfield_haves_2026-04-29-1826Z.csv` — DeckSafe run against 16 digitized decks.

---

## Collection snapshot

| Stat | Value |
|---|---|
| Unique cards owned | 2,952 |
| Total copies owned | 6,389 |
| Digitized decks tracked | 16 |
| Decks at 100% owned | 16 |
| Cards with insufficient copies | 4 unique / 4 copies |
| Shared cards (2+ decks) | 243 |

---

## Per-deck completion

Decks with `.txt` files in `decks/` and tracked by DeckSafe. Completion is physical ownership — a shared card counts for whichever deck holds it.

| Deck                      | Commander                   | % Complete | Notes                              |
| ------------------------- | --------------------------- | ---------- | ---------------------------------- |
| Calamity Tax              | Glarb, Calamity's Augur     | 100%       | —                                  |
| Crystal Sickness          | Golbez, Crystal Collector   | 100%       | —                                  |
| Curse of the Scarab       | The Scarab God              | 100%       | Cuts moved missing cards to SB     |
| Diminishing Returns       | Teysa Karlov                | 100%       | —                                  |
| Earthbend the Meta        | Toph, the First Metalbender | 100%       | —                                  |
| Eldrazi Stampede Chaos    | Maelstrom Wanderer          | 100%       | Not in Deck_Index.md — needs entry |
| Lightning War             | Fire Lord Azula             | 100%       | —                                  |
| Peace Offering            | Ms. Bumbleflower            | 100%       | —                                  |
| Radiation Sickness        | The Wise Mothman            | 100%       | —                                  |
| The Dark Lord's Army      | Sauron, the Dark Lord       | 100%       | —                                  |
| The Exile's Return        | Fire Lord Zuko              | 100%       | —                                  |
| The Genome Project        | Kuja, Genome Sorcerer       | 100%       | —                                  |
| The Grand Design          | Atraxa, Grand Unifier       | 100%       | —                                  |
| The Loam Cycle            | Teval, the Balanced Scale   | 100%       | —                                  |
| The Replication Crisis    | Satya, Aetherflux Genius    | 100%       | —                                  |
| This Bunny Goes To Market | Ms. Bumbleflower            | 100%       | Not in Deck_Index.md — needs entry |

---

## Decks without digital decklists

These appear in `Deck_Index.md` but have no `.txt` in `decks/`. Not tracked by DeckSafe — collection completeness unknown.

| Deck                 | Commander              |
| -------------------- | ---------------------- |
| Divine Constellation | Sythis, Harvest's Hand |
| Lorehold Spirits     | Quintorius             |

---

## Shopping list

Cards short across the full demand pool. None are in Curse of the Scarab.

| Card             | Need | Have | Decks                                                         |
| ---------------- | ---- | ---- | ------------------------------------------------------------- |
| Willowrush Verge | 2    | 1    | Eldrazi Stampede Chaos, Radiation Sickness                    |
| Yavimaya Coast   | 3    | 2    | Eldrazi Stampede Chaos, Peace Offering, This Bunny To Market  |
| Sunpetal Grove   | 2    | 1    | Peace Offering, This Bunny Goes To Market                     |
| Night's Whisper  | 3    | 2    | The Dark Lord's Army, The Exile's Return, The Genome Project  |

See full Shopping List tab in `collection/deck_safe_collection.xlsx` or the [Google Sheet](https://docs.google.com/spreadsheets/d/1UjtdLELu2PzlvE99_r1vbvzPb22Vmi0qVBpo6nnt6UY).

---

## Zero-surplus shared cards (physical swap required to play both decks)

Cards where owned copies exactly equal demand across multiple decks — physically moving them between decks to play simultaneously. Not a collection gap, but a logistics note.

High-value cards at exactly zero surplus (top instances by deck count):

| Card                      | Copies | # Decks |
| ------------------------- | ------ | ------- |
| Toxic Deluge              | 10     | 10      |
| Fellwar Stone             | 9      | 9       |
| Lightning Greaves         | 9      | 9       |
| Fierce Guardianship       | 8      | 8       |
| An Offer You Can't Refuse | 7      | 7       |
| Counterspell              | 7      | 7       |
| Morphic Pool              | 7      | 7       |
| Swan Song                 | 7      | 7       |
| Bojuka Bog                | 6      | 6       |
| Boseiju, Who Endures      | 6      | 6       |
| Deadly Rollick            | 6      | 6       |
| Nature's Lore             | 6      | 6       |
| Otawara, Soaring City     | 6      | 6       |
| Path to Exile             | 6      | 6       |
| Reanimate                 | 6      | 6       |
| Beast Within              | 6      | 6       |
| Black Market Connections  | 5      | 5       |
| Three Visits              | 5      | 5       |
| Yavimaya, Cradle of Growth| 5      | 5       |

Full zero-surplus list is in the Shared Cards tab of the spreadsheet.

---

## Maintenance

- Re-run DeckSafe after any decklist change or new Moxfield export (see `WF_Deck_Safe_Collection.md`).
- Archive the old Moxfield CSV to `archive/` rather than deleting.
- Update this file after each DeckSafe run — the spreadsheet is the source of truth, this file is the human-readable summary.
