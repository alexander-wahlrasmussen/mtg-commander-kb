# scripts/ — index

Local working tooling: Scryfall lookups, deck validation, the Monte-Carlo sim
stack, the per-deck kill-turn labs, the pod/meta models, and the dashboard
back-end. **Not synced to the Claude Project** (the sync script skips `scripts/`).

Discipline (inherited by every lab): clock curves are **unblocked goldfish
ceilings**, disruption is *availability* not effectiveness, and the durability
tiebreak / `T_grind` are judgment. Read the ranking and the gaps, not the second
decimal. Clock claims in Summaries must cite a lab run — see CLAUDE.md and
`reference/REF_The_Conversion_Check.md`.

**`deck_registry.py` is the single source of truth** for per-deck static metadata
(name, stem, commander, CC score, and the `lab` pointer → which lab script clocks
that deck). When in doubt about which script belongs to which deck, read the
registry, not the filename.

---

## Naming convention

| Pattern | Meaning |
|---|---|
| `<abbr>_clock_lab.py` | Per-deck kill-turn goldfish (decap + table clock). |
| `<abbr>_speed_lab.py` | Per-deck speed / before-after kill-window analysis. |
| `*_lab.py` (no deck abbr) | A cross-roster model (pod, meta, dragon, lock, delay…). |

Deck abbreviations are **not always initials** (`bmf` = Bumbleflower, `cos` =
Curse of the Scarab, `dla` = Dark Lord's Army, `ebm` = Earthbend the Meta,
`esc` = Eldrazi Stampede Chaos, `hsh` = Hashaton, `kfk` = Kefka, `yrk` = Yuriko).
The per-deck tables below give the full mapping.

---

## Shared / canonical tooling

| Script | Does |
|---|---|
| `deck_registry.py` | Single source of truth for per-deck static metadata + lab pointers. |
| `deck_sim.py` | Monte-Carlo consistency + combo-assembly simulator (not a rules engine). |
| `speed_lab_core.py` | Shared harness the per-deck speed/clock labs build on. |
| `clock_lab_template.py` | Copy to start a new `<deck>` kill-turn lab. |
| `card_lookup.py` | Look up Scryfall oracle data + rulings by card name (`--fuzzy`). |
| `update_scryfall_data.py` | Download the latest Scryfall oracle-cards + rulings bulk data. |
| `find_combos.py` | Check a full decklist for combos via Commander Spellbook. |
| `availability_check.py` | Check a candidate decklist against ownership + deployed decks. |
| `unlock_optimizer.py` | Rank cross-deck card contention and one-purchase unlocks. |
| `sync_to_project.py` | Flatten the KB into `_sync_drop/` for Claude Project upload. |
| `build-collection.ps1` | Build the DeckSafe collection from the latest Moxfield export. |
| `validate.py` | Read-only linter for the KB hard rules (100 cards, GC cap…). |
| `clock_check.py` | Flag Summary `Clock:` citations that drifted from the labs. |
| `lint_links.py` | Flag broken intra-repo file references in the markdown corpus. |
| `keep_spec.py` | Generate per-deck mulligan KEEP specs. |
| `report.py` | One deck's full scouting profile across every framework + oracle. |
| `tier_list.py` | Composite tier list across the three measured rankings. |

## Pod & meta models (cross-roster)

| Script | Does |
|---|---|
| `pod_gauntlet.py` | P(beat the recurring archenemy pod), per deck. |
| `pod_championship.py` | Crown a champion of the 16 active decks. |
| `self_meta_lab.py` | Quantify the self-meta ranking (roster as its own field). |
| `delay_lab.py` | Answer-availability ("counter-clock") vs the pod's combo turn. |
| `interaction_meta_lab.py` | Interaction / durability overlay oracle. |
| `lock_lab.py` | Persistent-lock availability (the honest "opponent-clock tax"). |
| `framework_bakeoff.py` | Grade deck-evaluation frameworks against the outcome oracle. |
| `game_log.py` | Record real pod-game outcomes (Layer-2 ground truth). |
| `kill_tree.py` | Render a deck's kill lines as a Mermaid decision tree. |

## Dragon matchup (the archenemy's fair deck)

| Script | Does |
|---|---|
| `vs_dragon_roster_lab.py` | Per-deck P(win) vs the Ur-Dragon fair-board deck, all 16 decks. |
| `vs_dragon_lab.py` | Whether the Glarb (Calamity Tax) anti-dragon package actually works. |

## Glarb / Calamity-Tax rebuild labs

| Script | Does |
|---|---|
| `glarb_compare_lab.py` | Compare four external Glarb (Calamity's Augur) lists. |
| `glarb_hybrid_clock_lab.py` | Kill-turn clock for the Hybrid Glarb direction. |
| `glarb_iso_clock_lab.py` | Kill-turn clock for the Glarb grind + Isochron-combo build. |
| `ext_glarb_vs_calamity_lab.py` | Rank the external "Yd Freehold" Glarb list vs our Calamity Tax. |

## Per-deck kill-turn labs — active roster

| Deck (commander) | Script(s) |
|---|---|
| The Genome Project (Kuja) | `gp_clock_lab.py` |
| Radiation Sickness (The Wise Mothman) | `rs_clock_lab.py` |
| Diminishing Returns (Teysa Karlov) | `dr_clock_lab.py`, `sephiroth_clock_lab.py` |
| Eldrazi Stampede Chaos (Maelstrom Wanderer) | `esc_clock_lab.py` |
| The Exile's Return (Fire Lord Zuko) | `er_speed_lab.py` |
| The Replication Crisis (Satya) | `rc_speed_lab.py` |
| Lightning War (Fire Lord Azula) | `lw_clock_lab.py`, `lw_speed_lab.py`, `lw_combo_lab.py` |
| The Calamity Tax (Glarb) | `ct_speed_lab.py` |
| Crystal Sickness (Golbez) | `cs_clock_lab.py` |
| Curse of the Scarab (The Scarab God) | `cos_clock_lab.py` |
| Ms. Bumbleflower | `bmf_clock_lab.py` |
| Zero-Sum Game (Witherbloom) | `wb_clock_lab.py`, `wb_storm_lab.py`, `wb_raid_lab.py`, `wb_rebuild_vs_dragon.py` |
| The Grand Design (Atraxa) | `gd_clock_lab.py`, `gd_speed_lab.py` |
| The Dark Lord's Army (Sauron) | `dla_clock_lab.py` |
| Earthbend the Meta (Toph) | `ebm_clock_lab.py` |
| Lorehold Spirits (Quintorius) | `lor_clock_lab.py` |

## Per-deck kill-turn labs — candidates / proposals (not built)

| Candidate (commander) | Script |
|---|---|
| Hashaton, Scarab's Fist (Esper Thoracle) | `hsh_clock_lab.py` |
| Insider Trading (Yuriko) | `yrk_clock_lab.py` |
| Forced Liquidation (Kefka — internal burn) | `kfk_clock_lab.py` |
| Berta, Wise Extrapolator | `berta_clock_lab.py` |
| Najeela, the Blade-Blossom | `naj_clock_lab.py` |
| Winota, Joiner of Forces | `winota_clock_lab.py` |
| Yawgmoth (aristocrats) | `yawgmoth_clock_lab.py` |

## Dashboard back-end (web front-end lives in `../dashboard/` + `../ui/`)

| Script | Does |
|---|---|
| `dashboard_server.py` | Interactive front-end server for the gauntlet/lab/championship stack. |
| `dashboard_export.py` | Bake the dashboard's sim results to static JSON for no-backend hosting. |
| `dashboard_screenshot.py` | Render the live dashboard with Playwright and shoot each tab. |
| `ui_screenshot.py` | Render the React rebuild (`../ui/`) with Playwright and shoot each tab. |

## Data files (not scripts)

- `sim_profiles.json` — per-deck sim configuration consumed by the labs.
- `game_results.jsonl` — written by `game_log.py`; read by `framework_bakeoff.py` (gitignored if absent).
