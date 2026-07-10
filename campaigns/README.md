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
| `Candidate_Bakeoff_Verdict_2026-06-12.md` | RESOLVED | The pick-one **decision hub** — winner **Yuriko / Insider Trading** stays gated on pod approval of Thoracle+Consult (**un-built**); the no-approval fallback **Kefka-burn was built & physically assembled 2026-07-08** as Forced Liquidation (`../decks/Forced_Liquidation_Summary.md`; `PROP_Kefka_Court_Mage.md` archived). |
| `Candidate_Bakeoff_2026-06-12.md` | RESOLVED | Stages 0–3 evidence tracker behind the verdict (9 candidates → Yuriko; fallback Kefka built 2026-07-08). |
| `Delay_Lab_Disruption_Analysis_2026-06-12.md` | LIVE | Answer-availability (counter-clock) lab — the disruption-axis addendum the bake-off verdict leans on. |
| `Pod_Gauntlet_2026-06-14.md` | LIVE | **Quantitative companion to `../Pod_Matchup_Matrix.md`**: races each deck's decap clock + disruption into `P(beat the pod)`. Tool `../scripts/pod_gauntlet.py`, data `../analysis/pod_gauntlet_clocks.json`. Separates the race vs disruption axes the matrix collapsed; challenges Calamity's "Favoured." |
| `Self_Meta_Ranking.md` | REFERENCE | Which deck wins if the roster *is* the field — the self-meta companion to `../Pod_Matchup_Matrix.md` (anti-pod). Built on the sweep's decap/table clocks. |
| `Collection_State_2026-06-14.md` | SNAPSHOT | Point-in-time read of the whole collection: runs the full tool stack (validate / clock_check / pod_gauntlet / unlock_optimizer / kill_tree) into one health + standing + buy-pressure picture, with the loose ends named. Regenerate, don't cite. |

Methodology is codified in `../workflows/WF_Kill_Window_Lab.md` and
`../workflows/WF_Candidate_Bakeoff.md`. The candidate *proposals* themselves
(`PROP_*`) stay in `../proposals/`; losing candidates are in `../archive/proposals/`,
their priced `.txt` builds in `../decks/considering/` (+ scratch in
`../archive/build_scratch/`).
