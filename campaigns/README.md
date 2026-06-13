# campaigns/ — multi-session campaigns & methodology (index)

Cross-deck **process** docs: the framework rationale that started the clock-lab work,
the roster-wide sweep + ranking, and the pick-one candidate bake-off. These are
multi-session trackers — they hold queues, session logs, and verdicts that are
appended over time, not one-shot writeups. Per-deck lab evidence lives in
`../analysis/`; forward-looking build proposals in `../proposals/`. **Not synced to
the Claude Project.**

| File | Status | What it is |
|---|---|---|
| `Framework_Clock_Gap_2026-06-09.md` | REFERENCE | Origin of the lab-citation rule — the evidence that hand-estimated kill windows run systematically optimistic. Cited as the "why" by the sweep + the workflows. |
| `Kill_Window_Lab_Sweep_2026-06-13.md` | LIVE (complete) | The roster-wide campaign: clock-lab every active deck, then **rank by measured decap clock**. Holds the queue, the append-only session log, and the final ranking. Procedure: `../workflows/WF_Kill_Window_Lab.md`. |
| `Candidate_Bakeoff_Verdict_2026-06-12.md` | LIVE | The pick-one **decision hub** — build **Yuriko / Insider Trading** (gated on pod approval of Thoracle+Consult); fallback = internal Kefka-burn. |
| `Candidate_Bakeoff_2026-06-12.md` | LIVE | Stages 0–3 evidence tracker behind the verdict (9 candidates → Yuriko). |
| `Delay_Lab_Disruption_Analysis_2026-06-12.md` | LIVE | Answer-availability (counter-clock) lab — the disruption-axis addendum the bake-off verdict leans on. |
| `Self_Meta_Ranking.md` | REFERENCE | Which deck wins if the roster *is* the field — the self-meta companion to `../Pod_Matchup_Matrix.md` (anti-pod). Built on the sweep's decap/table clocks. |

Methodology is codified in `../workflows/WF_Kill_Window_Lab.md` and
`../workflows/WF_Candidate_Bakeoff.md`. The candidate *proposals* themselves
(`PROP_*`) stay in `../proposals/`; losing candidates are in `../archive/proposals/`,
their priced `.txt` builds in `../decks/considering/` (+ scratch in
`../archive/build_scratch/`).
