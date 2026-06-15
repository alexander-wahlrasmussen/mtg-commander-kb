# analysis/ — per-deck lab evidence (index)

Kill-turn **clock labs** and earlier **speed-curve analyses** — the measured
provenance behind each deck Summary's Kill-Window line (the CLAUDE.md lab-citation
rule). These are permanent reference, not proposals: a deck's `*_Summary.md` cites
its writeup here by path.

**Moving or renaming a file in this folder breaks that citation** — if you move one,
rewrite the `analysis/<name>` reference in the Summary (and any dashboard) in the same
change. Methodology and the cross-deck ranking live in `../campaigns/`; the scripts
that produced these numbers live in `../scripts/` (`*_clock_lab.py`, `*_speed_lab.py`,
shared harness `speed_lab_core.py`). **Not synced to the Claude Project** (the sync
script walks only `decks/` + `collection/`).

## Clock labs — measured decap/table kill-turn (the current metric)

| File | Backs (Summary) |
|---|---|
| `Crystal_Sickness_Clock_Lab_2026-06-13.md` | `decks/Crystal_Sickness_Summary.md` |
| `Curse_of_the_Scarab_Clock_Lab_2026-06-13.md` | `decks/Curse_of_the_Scarab_Summary.md` |
| `Dark_Lords_Army_Clock_Lab_2026-06-13.md` | `decks/The_Dark_Lord_s_Army_Summary.md` |
| `Diminishing_Returns_Clock_Lab_2026-06-10.md` | `decks/Diminishing_Returns_Summary.md` |
| `Earthbend_the_Meta_Clock_Lab_2026-06-13.md` | `decks/Earthbend_the_Meta_Summary.md` |
| `Eldrazi_Stampede_Clock_Lab_2026-06-13.md` | `decks/Eldrazi_Stampede_Chaos_Summary.md` |
| `Genome_Project_Clock_Lab_2026-06-10.md` | `decks/The_Genome_Project_Summary.md` |
| `Lightning_War_Clock_Lab_2026-06-13.md` | `decks/Lightning_War_Summary.md` |
| `Lorehold_Spirits_Clock_Lab_2026-06-13.md` | `decks/Lorehold_Spirits_Summary.md` |
| `Ms_Bumbleflower_Clock_Lab_2026-06-13.md` | `decks/Ms_Bumbleflower_Summary.md` |
| `Radiation_Sickness_Clock_Lab_2026-06-13.md` | `decks/Radiation_Sickness_Summary.md` |
| `Calamity_Tax_Kill_Turn_Lab_2026-06-13.md` | `decks/The_Calamity_Tax_Summary.md` |

## Speed-curve analyses — earlier availability/lever labs

| File | Backs |
|---|---|
| `Grand_Design_Speed_Curve_Analysis.md` | `decks/The_Grand_Design_Summary.md` |
| `Replication_Crisis_Speed_Curve_Analysis.md` | RC Summary + `Pod_Matchup_Matrix.md` |
| `Exiles_Return_Speed_Curve_Analysis.md` | `decks/The_Exiles_Return_Summary.md` |
| `Calamity_Tax_Speed_Curve_Analysis.md` | `decks/The_Calamity_Tax_Summary.md` |
| `Lightning_War_Speed_Curve_Analysis.md` | `../campaigns/Framework_Clock_Gap_2026-06-09.md` |

## Cross-cutting matchup models (not per-deck Summary backers)

| File | What |
|---|---|
| `Opponent_Clock_Lock_Model_2026-06-15.md` | persistent-lock / mana-tax overlay closing pod_gauntlet limitation #1 (`lock_lab.py` + `pod_gauntlet.py --lock`); data `lock_availability.json` |
| `Measured_Disruption_All16_2026-06-15.md` | delay_lab-measured disruption for all 16 (closes limitation #2); replaces the 2-value class bucket; data `delay_disruption.json` (via `delay_lab.py --emit-json`) |
| `Self_Meta_Quantified_2026-06-15.md` | the long-game model: quantifies the self-meta ranking (table-close race + durability overlay) via `self_meta_lab.py`; decomposes measured-vs-judgment, pivots on `T_grind` |

(`pod_gauntlet_clocks.json`, `lock_availability.json`, `delay_disruption.json` and `kill_trees/`
also live here; their writeups are in `../campaigns/` or above.)

Per-deck procedure: `../workflows/WF_Kill_Window_Lab.md`. The roster ranking that
consumes these clocks: `../campaigns/Kill_Window_Lab_Sweep_2026-06-13.md`.
