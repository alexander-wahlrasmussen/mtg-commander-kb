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
| `Lorehold_Spirits_Clock_Lab_2026-06-13.md` | `decks/Lorehold_Spirits_Summary.md` |
| `Ms_Bumbleflower_Clock_Lab_2026-06-13.md` | `decks/Ms_Bumbleflower_Summary.md` |
| `Radiation_Sickness_Clock_Lab_2026-06-13.md` | `decks/Radiation_Sickness_Summary.md` |
| `Calamity_Tax_Kill_Turn_Lab_2026-06-13.md` | `decks/Croak_And_Dagger_Summary.md` (Calamity Tax was rebuilt into Croak and Dagger) |

## Speed-curve analyses — earlier availability/lever labs

| File | Backs |
|---|---|
| `Grand_Design_Speed_Curve_Analysis.md` | `decks/The_Grand_Design_Summary.md` |
| `Replication_Crisis_Speed_Curve_Analysis.md` | RC Summary + `Pod_Matchup_Matrix.md` |
| `Exiles_Return_Speed_Curve_Analysis.md` | `decks/The_Exiles_Return_Summary.md` |
| `Calamity_Tax_Speed_Curve_Analysis.md` | `decks/Croak_And_Dagger_Summary.md` (Calamity Tax was rebuilt into Croak and Dagger) |

## Cross-cutting matchup models (not per-deck Summary backers)

| File | What |
|---|---|
| `Opponent_Clock_Lock_Model_2026-06-15.md` | persistent-lock / mana-tax overlay closing pod_gauntlet limitation #1 (`lock_lab.py` + `pod_gauntlet.py --lock`); data `lock_availability.json` |
| `Measured_Disruption_All16_2026-06-15.md` | delay_lab-measured disruption for all 16 (closes limitation #2); replaces the 2-value class bucket; data `delay_disruption.json` (via `delay_lab.py --emit-json`) |
| `Self_Meta_Quantified_2026-06-15.md` | the long-game model: quantifies the self-meta ranking (table-close race + durability overlay) via `self_meta_lab.py`; decomposes measured-vs-judgment, pivots on `T_grind` |
| `Pod_Championship_2026-06-15.md` | the fun finale: a seeded 16-deck tournament on the self-meta engine (`pod_championship.py`); Genome champion in both fast & grindy metas, Dark Lord rises on low `T_grind` |
| `Pod_Championship_Swapped_2026-06-15.md` | the championship re-run with all Build_And_Swap §2 swaps (`pod_championship.py --swapped`); only Calamity's rebuild moves the table clock → it crashes the podium (🥉), but Genome's crown is unchanged |
| `Definitive_Tier_List_2026-06-28.md` | **(current)** ranked tier list = composite of the THREE convergent OUTCOME oracles ANTI-POD · INTERACTION · SELF-META (`tier_list.py`), CC demoted to a context column; reconciles where the external-pod vs mirror bars disagree; headline: the two 19/20 decks (Lightning War, Dark Lord) rank 11th–12th — score ⊥ winning |
| `Definitive_Tier_List_2026-06-15.md` | *(superseded by the 06-28 v2)* the original composite of POWER (Conversion /20) · SELF-META · ANTI-POD (`tier_list.py --legacy-power`) |

(`pod_gauntlet_clocks.json`, `lock_availability.json`, `delay_disruption.json` and `kill_trees/`
also live here; their writeups are in `../campaigns/` or above.)

Per-deck procedure: `../workflows/WF_Kill_Window_Lab.md`. The roster ranking that
consumes these clocks: `../campaigns/Kill_Window_Lab_Sweep_2026-06-13.md`.
