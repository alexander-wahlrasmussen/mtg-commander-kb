# Workflow: Deck-Safe Collection

Building or refreshing the master collection spreadsheet that tracks owned-vs-needed across all active decks.

---

## Primary path: run the DeckSafe tool

The DeckSafe tool (`deck_safe_collection_builder.py`) lives in a separate repo alongside this knowledge base:

- Windows example: `C:\Users\Alex\Projects\MTGDecks`
- macOS / Linux example: `~/Projects/MTGDecks`

These paths differ per machine. The rest of this doc uses `$DECKSAFE_REPO` as a placeholder — substitute the actual path for the machine you're on. On Windows PowerShell: `$env:DECKSAFE_REPO`. On macOS/Linux: `export DECKSAFE_REPO=~/Projects/MTGDecks` in your shell rc.

### First-time setup (per machine)

From the DeckSafe repo:

```bash
cd $DECKSAFE_REPO
pip install -r requirements.txt
```

Optional Google Sheets setup:

1. Create a Google Cloud project, enable the **Google Sheets API** and **Google Drive API**.
2. Create an OAuth 2.0 Client ID (application type: Desktop), download the JSON.
3. Save it as `~/.config/gspread/credentials.json` (same on Windows under `%USERPROFILE%\.config\gspread\credentials.json`).
4. First run opens a browser for auth; token cached after.

If you skip this, use `--no-google` on every invocation.

### Common invocations

All examples assume you run from the KB repo root (wherever `collection/` and `decks/` live) and invoke the tool by absolute path.

**Full build** — Google Sheets + local `.xlsx`:

```bash
python $DECKSAFE_REPO/deck_safe_collection_builder.py \
  collection/moxfield_haves_YYYYMMDDHHMMZ.csv \
  --deck-dir ./decks/ \
  -o collection/deck_safe_collection.xlsx
```

**Local-only** (no Google Sheets upload):

```bash
python $DECKSAFE_REPO/deck_safe_collection_builder.py \
  collection/moxfield_haves_YYYYMMDDHHMMZ.csv \
  --deck-dir ./decks/ \
  -o collection/deck_safe_collection.xlsx \
  --no-google
```

**Skip proxy generation:**

Add `--no-proxy`.

**Custom proxy directory:**

Add `--proxy-dir ./collection/proxy/`.

**Custom Google Sheets name:**

Add `--sheet-name "My Sheet Name"` (default: "Deck-Safe Collection").

### What gets produced

| Output | Default location |
|---|---|
| Spreadsheet (local) | `-o` target path, e.g. `collection/deck_safe_collection.xlsx` |
| Spreadsheet (Google) | Google Drive (unless `--no-google`) |
| Proxy `.txt` files | `<deck-dir>/proxy/` (unless `--no-proxy` or `--proxy-dir` override) |

The spreadsheet contains these tabs (Summary, Shopping List, Shared Cards, Full Card Matrix, Reskin Aliases, Considering, Per-Deck Tabs). See "Spreadsheet structure" below for details on each.

---

## Integration with this knowledge base

### Inputs (live in this repo)

- **Collection CSV:** `collection/moxfield_haves_YYYYMMDDHHMMZ.csv` — exported from Moxfield. Replace on each regeneration; archive the old one if you want history.
- **Decklists:** `decks/*.txt` — one `.txt` per deck, flat. Format is `1 Card Name` per line, with an optional `SIDEBOARD:` section followed by a blank line, then the commander as the last entry.
- **Considering decks:** `decks/considering/*.txt` — candidate decks the tool will analyze for completability against surplus cards.

### Outputs (land back in this repo)

- **`collection/deck_safe_collection.xlsx`** — commit this. It's a build artifact, but versioning it makes "what was my shopping list two months ago" answerable.
- **Proxy `.txt` files** — by default `decks/proxy/`. Consider `.gitignore`-ing this directory since it's derived and bulky.

### Cadence

- **After any decklist change:** re-run the tool so the spreadsheet doesn't drift from reality.
- **After a Moxfield export refresh:** re-run. Moxfield CSVs should be refreshed monthly or after any significant acquisition.
- **Archive the old Moxfield CSV** to `archive/` rather than deleting — useful for diffing acquisitions over time.

---

## Parsing rules (domain knowledge)

These rules describe what the tool does. They're preserved here because the logic matters for Q&A ("why does the spreadsheet show Aang's Shelter as owned when I only have Teferi's Protection?") even when you're not building the spreadsheet by hand.

### Collection parsing

- Sum all copies of each card across all printings and editions.
- Proxies count as owned copies.

### Deck parsing

- The main deck is everything before `SIDEBOARD:` (or before the final blank line if there's no sideboard section).
- The commander is the last card after a blank line (after SIDEBOARD content, or after the main deck).
- Cards between `SIDEBOARD:` and the blank line are **considering/maybeboard** — tracked separately, not counted as deck demand.
- Every deck should be exactly 100 cards (99 main + 1 commander). Tool warns on mismatch.

### Card name resolution (apply in order)

1. **Exact match** — deck card name matches collection card name.
2. **DFC / double-faced cards** — collection uses full name with ` // ` (e.g. `Sephiroth, Fabled SOLDIER // Sephiroth, One-Winged Angel`), deck lists use front face only. Match deck card to the front half of any `//` collection card.
3. **Split cards** — deck lists may use `/` (e.g. `Dusk/Dawn`) while collection uses ` // ` (e.g. `Dusk // Dawn`). Normalize and match.
4. **Universes Beyond reskin aliases** — see `REF_Reskin_Aliases.md` for the full table. The authoritative list of aliases lives there, not here.

   Important: when two decks use different names for the same card (one uses "Counterspell", another uses "Wild Rose Rebellion"), merge them into one demand pool under the original MTG name.

### Demand calculation

- For each card, total demand = sum of copies needed across all decks (main + commander only; considering/maybeboard excluded).
- Owned = total copies in collection, with aliases and name resolution applied.
- Surplus = Owned − Total Demand. Negative means short.

---

## Spreadsheet structure

What each tab is for:

| Tab | Purpose |
|---|---|
| Summary | Collection stats, demand stats, per-deck breakdown with % complete |
| Shopping List | Cards with surplus < 0. Sorted by deficit, worst first |
| Shared Cards | Cards in 2+ decks. Surplus/deficit color-coded |
| Full Card Matrix | Every card, every deck, one column per deck. Sorted by surplus ascending |
| Reskin Aliases | UB-to-original mappings in use, with coverage |
| Considering | Maybeboard cards — tracked but not counted in demand |
| Per-Deck Tabs | One tab per deck, with missing/conflict cards surfaced first |

Color coding: green = OK, yellow = shared conflict, red = not in collection.

---

## Fallback: building the spreadsheet as an LLM prompt

If the DeckSafe tool isn't available (fresh machine, dependency issue, traveling), the parsing rules above are complete enough to serve as an LLM spec. Provide Claude with:

1. This workflow file.
2. The Moxfield CSV.
3. The deck `.txt` files.
4. `REF_Reskin_Aliases.md`.

Ask for the spreadsheet following the "Spreadsheet structure" table. The output won't have Google Sheets integration or proxy file generation, but the core analysis will match the tool's output.

This fallback is not a substitute for the tool — it's slower, more error-prone, and harder to re-run identically. Use it only when the tool path is blocked.

---

## Troubleshooting

**A card appears missing that I know I own.**

1. Check the Full Card Matrix for a surplus copy — the physical card may be lost, not the logical one.
2. Check `REF_Reskin_Aliases.md` — a UB reskin might not be mapped, so it's searching under the wrong name.
3. Check the Moxfield CSV directly for the expected name. Exports sometimes drop cards during incremental edits; a full re-export fixes this.

**DeckSafe reports a deck with 101 or 99 cards.**

The `.txt` is off by one. Usually a missing blank line before the commander, or an accidental duplicated line.

**Proxy files aren't generating.**

Check you're not running with `--no-proxy`. Check the proxy directory is writable. On Windows, check for path-length issues if the deck directory is deeply nested.

**Google Sheets upload fails with auth errors.**

Token cache may be stale. Delete `~/.config/gspread/authorized_user.json` and re-auth on next run.

---

## Notes on folder structure

DeckSafe expects `.txt` decklists **directly inside `--deck-dir`** (plus the optional `considering/` subdirectory). It does not recurse arbitrarily. This means the KB's `decks/` folder should hold `.txt` files flat, with summaries alongside them:

```
decks/
├── the-loam-cycle-20260404-074432.txt
├── The_Loam_Cycle_Summary.md
├── the-exiles-return-20260424.txt
├── The_Exiles_Return_Summary.md
├── considering/
│   └── najeela-candidate-20260420.txt
└── proxy/
    └── (generated)
```

When a `.txt` is superseded, move the old version to `archive/old_decklists/` to keep the active `decks/` folder clean and prevent double-counting.