# proposals/ — index & status legend

Working docs: build proposals, speed/clock-lab write-ups, and the candidate
bake-off record. **Not synced to the Claude Project** (the sync script walks only
`decks/` + `collection/`), so these are local-only working material.

Status tags:

- **LIVE** — an active build decision or open candidate.
- **REFERENCE** — cited by path from an active deck Summary / `Pod_Matchup_Matrix.md`
  / `Framework_Clock_Gap`. **Do not move these** — moving breaks a kill-window
  citation (CLAUDE.md lab-citation rule).
- **PIPELINE** — un-built candidate, linked from `Deck_Index.md` "Candidate new builds."

Spent docs (bake-off losers, superseded passes, built-deck readiness) live in
`archive/proposals/`; superseded decklists in `archive/old_decklists/`.

---

## Bake-off (2026-06-12) — pick-one decision

| File | Status | Note |
|---|---|---|
| `Candidate_Bakeoff_Verdict_2026-06-12.md` | LIVE | The decision hub. **Build Yuriko / Insider Trading** (gated on pod approval of Thoracle+Consult); fallback = internal Kefka-burn. |
| `Candidate_Bakeoff_2026-06-12.md` | LIVE | Stages 0–3 evidence tracker. |
| `Delay_Lab_Disruption_Analysis_2026-06-12.md` | LIVE | Disruption-axis lab (verdict addendum). |
| `PROP_Yuriko_Insider_Trading.md` | LIVE | **Winner**, to build → `decks/considering/insider-trading-20260612.txt`. |
| `PROP_Kefka_Court_Mage.md` | LIVE | **Fallback** (internal Kefka-burn) → `decks/considering/forced-liquidation-20260612.txt`. No pod approval needed. |
| `Witherbloom_External_Build_Comparison.md` | LIVE | Comparison-doc format precedent the verdict mirrors. |

Methodology is codified in `workflows/WF_Candidate_Bakeoff.md`. Losing candidate
proposals (Godo, Urza, Kinnan, Thrasios, Korvold, Clive-ext, Kefka-ext) are in
`archive/proposals/`; their priced/labbed `.txt` builds in `archive/old_decklists/`
(restorable in a weekend if a slot opens — Godo in particular, ~€50).

## Pipeline candidates (un-built)

| File | Status | Note |
|---|---|---|
| `PROP_Berta_Wise_Extrapolator.md` | PIPELINE | Replaces Wise Mothman (Radiation Sickness); ceiling 15–16/20. |
| `PROP_Hashaton_Scarabs_Fist.md` | PIPELINE | Esper. |
| `PROP_Najeela_Blade_Blossom.md` | PIPELINE | 5C Warrior tribal, Bracket-4. |
| `PROP_The_Wandering_Minstrel.md` | PIPELINE | 5C Town tribal; **deferred** — Earthcraft contention with Najeela; not on the `Deck_Index` shortlist. |

## Reference — cited by active decks (do not move)

| File | Cited by |
|---|---|
| `Framework_Clock_Gap_2026-06-09.md` | the lab-citation rule's origin doc |
| `Calamity_Tax_Speed_Curve_Analysis.md` | `The_Calamity_Tax_Summary.md` |
| `Exiles_Return_Speed_Curve_Analysis.md` | `The_Exiles_Return_Summary.md` |
| `Grand_Design_Speed_Curve_Analysis.md` | `The_Grand_Design_Summary.md` |
| `Replication_Crisis_Speed_Curve_Analysis.md` | RC Summary + `Pod_Matchup_Matrix.md` |
| `Lightning_War_Speed_Curve_Analysis.md` | `Framework_Clock_Gap` |
| `Grand_Design_ETB_Disruption_Pass_2026-06-09.md` | `Pod_Matchup_Matrix.md` |
| `Grand_Design_Finisher_Upgrade_2026-06-08.md` | `The_Grand_Design_Summary.md` |
| `Grand_Design_Mana_Fixing_Pass_2026-06-09.md` | `Pod_Matchup_Matrix.md` |
| `Genome_Project_Clock_Lab_2026-06-10.md` | `The_Genome_Project_Summary.md` |
| `Diminishing_Returns_Clock_Lab_2026-06-10.md` | `Diminishing_Returns_Summary.md` |
| `Diminishing_Returns_B4_Pivot_2026-06-10.md` | `Diminishing_Returns_Summary.md` |
| `PROP_Witherbloom_the_Balancer.md` | `Zero_Sum_Game_Summary.md` (proposal-of-record for the built deck) |

---

When the Yuriko/Kefka build is actually made, archive the four bake-off LIVE docs
(verdict, tracker, delay lab, comparison) to `archive/proposals/` and update this
table.
