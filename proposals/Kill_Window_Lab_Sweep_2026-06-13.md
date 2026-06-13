# Kill-Window Lab Sweep — tracker & ranking (opened 2026-06-13)

**Goal.** Give every active roster deck a lab-cited kill-turn clock, replacing the
hand-estimated Kill Windows that the `Framework_Clock_Gap_2026-06-09` evidence
showed are systematically optimistic. End state: a roster **ranked by measured
decap clock**, with the Conversion Check score alongside (the framework's finding
was that the two are uncorrelated in the 15–19/20 band — so we report both).

**This is a multi-session campaign.** This file is the durable store. Per-deck
procedure: `workflows/WF_Kill_Window_Lab.md`. Rule of record:
`REF_The_Conversion_Check.md` → Verification rule.

**Resume here each session:** read the Status board below, pick the top
`TODO`/`PARTIAL` row (priority-ordered), run the workflow, append to the Session
log, and update the Ranking. One deck per sitting is fine.

---

## The bar (what the ranking measures)

- **Decap clock = the race metric.** Pod-beating bar is **decap by T≤7** (the pod's
  combo decks win T6–7 behind Grand Abolisher — see `project_pod_combo_opponent`).
- **Table clock = the reliability metric**, not the race. Genome's T8 table is the
  roster benchmark for "reliable." Decap and table are stated separately, always.
- **Never-in-12** is the reliability tail.
- Score (NN/20) is judged on the Conversion Check; clock is measured. Reported
  together, never merged.

## Status legend

- ✅ **DONE** — kill-turn clock measured (decap + table), Summary cites it.
- ◐ **PARTIAL** — has a speed-curve / availability lab but **no kill-turn decap/table
  clock**. Needs a proper clock run for consistency.
- ❌ **TODO** — no lab; Kill Window is hand-estimated (`(unverified)` flagged).

---

## Status board — work queue (priority-ordered)

Priority rule (from `Framework_Clock_Gap` §5): **front-edge / low claims first** —
every front edge measured so far came back optimistic. Then the T7–9 cluster, then
the slow decks. Kill-shape prediction is the pre-registered prior (Stage 1 of the WF).

| # | Deck | Commander (colors) | Claim | Kill shape → prediction | Status |
|---|---|---|---|---|---|
| 1 | Eldrazi Stampede Chaos | Maelstrom Wanderer (Temur) | T6–8 | combat focus-fire → decap fast / table slow; **front edge suspect** | ✅ DONE — decap T8 / table T12 (`esc_clock_lab.py`, 2026-06-13); claim was optimistic front edge + decap/table conflation |
| 2 | Radiation Sickness | Wise Mothman (Sultai) | T6–9 | rad/toxic attrition + drain → likely converge; **front edge suspect** | ✅ DONE — table-win T10 / decap T7 (`rs_clock_lab.py`, 2026-06-13); claim optimistic on the win clock; coarse engine model |
| 3 | Lightning War | Fire Lord Azula (Grixis) | T6–7 | burn: single-target finishers + pingers → mixed; availability-verified, no kill-turn clock | ✅ DONE (v2) — decap T9 / table ~T13 strict goldfish (`lw_clock_lab.py`, 2026-06-13); from-40 sweep = 14-mana Crackle, so "T6–7" is the chip-/disruption-assisted clock; goldfish understates this tempo/disruption deck (v1's T11 was a model bug — fixed) |
| 4 | Crystal Sickness | Golbez (Dimir) | T7–9 | reanimate a fatty → combat focus-fire → diverge | ✅ DONE — decap T11 / table T13 (`cs_clock_lab.py`, 2026-06-13); claim optimistic ~2–4 turns; shape is MIXED (drain+Tezzeret converge / combat diverges), not the pure diverge predicted; engine = card draw |
| 5 | Curse of the Scarab | The Scarab God (Dimir) | T7–9 | zombies + Gray Merchant drain → mixed combat/drain | ✅ DONE — decap T8 / table T11 (`cos_clock_lab.py`, 2026-06-13); **decap claim HELD** (first in sweep), only correction is decap/table split; combat decaps, drain tables |
| 6 | Earthbend the Meta | Toph (Naya) | T7–9 | artifact stompy → combat focus-fire → diverge | ❌ TODO |
| 7 | Lorehold Spirits | Quintorius (Boros) | T7–9 | Goblin Bombardment combo (ping) + spirits → combo converge / combat diverge | ❌ TODO |
| 8 | The Calamity Tax | Glarb (Sultai) | T7–9 | X-drain (Exsanguinate) + Kokusho reanimator → mana-gated; speed-curve done, no kill-turn clock | ◐ PARTIAL |
| 9 | Ms. Bumbleflower | Ms. Bumbleflower (Bant) | T8–10 | spellslinger tempo, evasive/Jolrael alpha → combat diverge | ❌ TODO |
| 10 | The Dark Lord's Army | Sauron (Grixis) | T8–10 | go-wide tokens / The Ring → combat focus-fire → diverge | ❌ TODO |

**Scope note (2026-06-13):** rows 3 (Lightning War) and 8 (Calamity Tax) already
have *speed-curve* labs (`lw_speed_lab.py`, `ct_speed_lab.py`) but those measured
availability/levers, not a kill-turn decap/table distribution — CT's Summary says
so explicitly ("no kill-turn goldfish run"); LW's "T6–7" came from finisher
availability. They're in-scope as PARTIAL so the ranking rests on one consistent
metric. If the user wants them treated as already-done, drop them from the queue —
they don't block the 8 TODO decks.

---

## Already verified (baseline for the ranking)

These six already carry a kill-turn clock — no work, they seed the ranking.

| Deck | Commander | Score | Decap | Table | Lab | Date |
|---|---|---|---|---|---|---|
| The Genome Project | Kuja (Rakdos) | 15/20 | **T7** | T8 | `gp_clock_lab.py` | 2026-06-10 |
| The Replication Crisis | Satya (Jeskai) | 17/20 | **T7** (med) | T10+ | `rc_speed_lab.py` | 2026-06-09 |
| The Exile's Return | Zuko (Mardu) | 17/20 | **T8** (med) | T10 | `er_speed_lab.py` | 2026-06-09 |
| Diminishing Returns | Teysa (Orzhov) | 17/20 | **T9** | T12+ | `dr_clock_lab.py` | 2026-06-10 |
| Zero-Sum Game | Witherbloom (Golgari) | not audited | **T9** | T9 | `wb_clock_lab.py` | 2026-06-11 |
| The Grand Design | Atraxa (WUBG) | 19/20 | **T10** (med) | T12+ | `gd_clock_lab.py` | 2026-06-10 |

---

## Session log (append-only — newest at bottom)

Each entry: date · deck · what ran · result vs claim · direction · doc.

- **2026-06-13** — Sweep opened. Inventoried roster: 6 decks already clock-labbed
  (above), 8 fully unverified, 2 partial (speed-curve only). Built
  `workflows/WF_Kill_Window_Lab.md` and this tracker. No deck labbed yet — queue
  is ordered, ready to start at row 1 (Eldrazi Stampede Chaos).
- **2026-06-13** — **Deck 1: Eldrazi Stampede Chaos.** Ran `esc_clock_lab.py` (40k,
  seed 20260613). Claim "Goldfish T6–8" **falsified as a single number**: decap
  median **T8** (T6 = 10% god-hand), table median **T12**, never-in-14 table 11%.
  Optimistic front edge (7-for-7) + decap/table conflation; decap median in-band
  so a milder miss than Grand Design. Kill-shape prior held (8-for-8). No card-text
  errors. Wrote `proposals/Eldrazi_Stampede_Clock_Lab_2026-06-13.md`; updated
  Summary + Deck_Index. Pod bar: T≤7 decap only 26% — does not race. Next: row 2,
  Radiation Sickness.
- **2026-06-13** — **Deck 2: Radiation Sickness.** Ran `rs_clock_lab.py` (40k, seed
  20260613 — coarsest lab in the sweep, expected-value counter-engine model).
  Claim "Goldfish T6–9" **optimistic on the win clock**: table-win median **T10**
  (T6 ≈ 1%, T9 ≈ 49%), decap one opponent median T7. Marquee T5–6 combo is a
  five-piece god-hand (1–4% by T7). No card-text errors (2026-05-13 audit holds).
  **Kill-shape lens nuance learned:** the converge *kills* converged as predicted,
  but the deck's *fastest* clock was the incidental combat decap, not the marquee
  combo — classify the fastest line, not the named one. No swaps; 18/20 unchanged.
  Wrote `proposals/Radiation_Sickness_Clock_Lab_2026-06-13.md`; updated Summary +
  Deck_Index. Next: row 3, Lightning War (PARTIAL — has speed-curve, needs kill-turn clock).
- **2026-06-13** — **Deck 3: Lightning War** (was PARTIAL). Built `lw_clock_lab.py`
  — the kill-turn goldfish lw_speed_lab never ran. **v1 → v2 after user push-back.**
  v1 (decap T11 / table never) was too slow — a real model bug: it swung only Azula's
  4 power and omitted Vivi Ornitier (2nd pinger + ramp) and Fated Firepower (damage
  amplifier). **v2: decap median T9, table ~T13 (40% never).** The from-40 one-cast
  sweep is 14-mana Crackle (`{X}{X}{X}{R}{R}`; corroborated by lw_speed_lab's 20% T12
  / 70% never), so "T6–7" is the **chip-/disruption-assisted real-pod clock**, not a
  from-full goldfish median — NOT a clean falsification (goldfish models no disruption
  and a static-40 table; the deck's tempo/race identity is legitimate). 19/20 stands;
  corrected stale 18/20 in Deck_Index. **LESSON: inventory the full board + every
  pinger/amplifier before trusting a burn deck's clock — and goldfish strictness
  (static 40, no disruption) penalizes tempo/control decks; flag it, don't over-read.**
  No card-text errors. Wrote `proposals/Lightning_War_Clock_Lab_2026-06-13.md`. Next:
  row 4, Crystal Sickness.
- **2026-06-13** — **Deck 4: Crystal Sickness.** Built `cs_clock_lab.py`. Claim
  "Goldfish T7–9" **optimistic**: decap median **T11** (T7 = 7%), table median
  **T13**; never-in-14 decap 21% / table 34% (table tail is an UPPER bound — see
  below). **Same v1-class model bug as Lightning War, caught and fixed:** the first
  model had no card draw and flatlined at ~1 artifact/turn (killed never), because
  the deck's engine drivers are *non-artifact* permanents an artifact-only deploy
  loop skipped — Matoya (draw per surveil = per artifact ETB), Sai (creature),
  Efficient Construction / Mirrodin Besieged (enchantments), Forensic Gadgeteer /
  Mechanist (creatures). Adding the draw engine (Matoya + Thought Monitor/Thoughtcast/
  Skullclamp/Baubles/One Ring) made it run. **Two real bottlenecks** gate the kill:
  (a) reach 8 artifacts (~T8 median), (b) dig a drain BOMB to the yard — only 3 in
  99 (Dreadnought 12 / Master = arts / Troll 6), ~50% by T9, matching raw card-
  finding odds; the table then needs 3–4 drain cycles. **Kill-shape:** tracker's
  "combat focus-fire → diverge" was corrected at Stage 0 to MIXED (named primary
  drain + Tezzeret +2 = all-table converge; Urza Construct/Thopters = combat
  diverge). Measured mixed (decap T11 / table T13, ~2-turn gap). **Lesson: the
  shape lens held (9-for-9 on the pattern) but my corrected absolute prior (decap
  ~T8) was itself 3 turns optimistic — the lens predicts the pattern, not the turn.**
  No card-text errors (2026-05-06 re-audit held; reconfirmed Master-CDA-in-yard,
  Golbez-returns-to-hand re-bin, Tezzeret-no-self-affinity). Pod bar: decap T≤7 only
  7% — does NOT race; the deck interacts/grinds (5 counters) rather than out-speeds.
  No swaps; 17/20 stands. Caveat: model captures the primary drain + Tezzeret +
  combat but OMITS the slower redundant closers (Mirrodin Phyrexian 15-yard alt-win,
  Cruel Captain emblem, Urza mana→hardcast), so 34% table-never is an upper bound on
  the tail, not the front edge. Wrote `proposals/Crystal_Sickness_Clock_Lab_2026-06-13.md`;
  updated Summary + Deck_Index + README reference table (added ESC/RS/LW/CS rows).
  Next: row 5, Curse of the Scarab.
- **2026-06-13** — **Deck 5: Curse of the Scarab.** Built `cos_clock_lab.py`. Claim
  "Goldfish T7–9" is the **most accurate hand-estimate in the sweep** — decap median
  **T8** (T7 = 32%, a healthy front edge, NOT a god-hand), squarely in-band. **First
  deck whose front edge did not come back optimistic.** Only correction: the single
  number conflated decap with table — table median **T11** (never-in-14 9%). **Two
  engines drive the two clocks:** lord-pumped **combat** focus-fires the decap (~T8);
  the **all-table Scarab/Gary drain** is modest per turn (~4–5 Zombies median at T7–9)
  so it *tables* at T11 — i.e. the deck's named primary (Scarab upkeep) is the table
  clock, the combat is the decap clock (opposite of the Summary's framing). Soultrader
  loop kill_all assembles only ~1% by T12. **Two model bugs caught:** (1) devotion
  zeroed because parsed records carry no `mana_cost` field → Gary drained 0 (fixed via
  oracle pip map); (2) zombie engine under-counted (~3 at T7) until I added the token
  generators I'd omitted — Grave Titan attack tokens, Liliana DM +1, Cryptbreaker, Rot
  Hulk ETB, Living Death/Agadeem's mass dump (cs/lw lesson, 3rd time). Model still
  OMITS deaths-based token engines (Gisa, Wilhelt, Crowded Crypt) so T11 table is a
  CONSERVATIVE (slow) edge — real table likely T10–11. No card-text errors (2026-05-05
  re-audit held; reconfirmed Scarab-is-a-God-not-Zombie, Gary=devotion, loop=kill_all).
  Pod bar: decap T≤7 = 32% (highest in sweep) — can pressure early via combat, but the
  *win* clock is T11 and the real pod plan is interaction + inevitability, not a race.
  No swaps; 17/20 stands. Wrote `proposals/Curse_of_the_Scarab_Clock_Lab_2026-06-13.md`;
  updated Summary + Deck_Index + README. Next: row 6, Earthbend the Meta.

---

## RANKING — roster by measured decap clock

Fills in as the sweep completes. Sorted fastest decap first; ties broken by table
clock then never-in-12. `—` = not yet measured. Final deliverable of the campaign.

| Rank | Deck | Decap | Table | Never-in-12 (table) | Score | Kill shape |
|---:|---|---|---|---|---|---|
| 1 | The Genome Project | T7 | T8 | — | 15/20 | drain/ping (converge) |
| 2 | Radiation Sickness | T7 decap | T10 | 1% | 18/20 | counter-engine (combo/Simic/Triumph converge; combat decap leads) |
| 3 | The Replication Crisis | T7 (med) | T10+ | — | 17/20 | combat focus-fire |
| 4 | The Exile's Return | T8 (med) | T10 | — | 17/20 | combat focus-fire |
| 5 | Curse of the Scarab | T8 | T11 | 9% | 17/20 | combat decaps / Scarab+Gary drain tables (mixed; **decap claim held**) |
| 6 | Eldrazi Stampede Chaos | T8 | T12 | 39% | 14/20 | combat focus-fire / Craterhoof alpha |
| 7 | Zero-Sum Game | T9 | T9 | — | n/a | lifeloop (converge) |
| 8 | Diminishing Returns | T9 | T12+ | — | 17/20 | aristocrat drain |
| 9 | Lightning War | T9 | ~T13 | 40% | 19/20 | burn chip + X-spell fork (**strict goldfish; tempo/disruption understated — real clock faster**) |
| 10 | The Grand Design | T10 (med) | T12+ | — | 19/20 | combat (96%) |
| 11 | Crystal Sickness | T11 | T13 | 34% (upper bd) | 17/20 | artifact drain + Tezzeret (converge) / combat decap (mixed) |
| ? | Earthbend the Meta | — | — | — | 17/20 | TBD |
| ? | Lorehold Spirits | — | — | — | 18/20 | TBD |
| ? | The Calamity Tax | — | — | — | 18/20 | TBD |
| ? | Ms. Bumbleflower | — | — | — | 15/20 | TBD |
| ? | The Dark Lord's Army | — | — | — | 19/20 | TBD |

**Reading the ranking (closing note, write when complete):** the framework's whole
thesis is that this column order and the Score column disagree. Once full, summarize
where score and clock most diverge (a high-score / slow-clock fortress is the
signature gap), and which decks clear the **decap T≤7 pod bar**.

---

## Related

- `workflows/WF_Kill_Window_Lab.md` — the per-deck procedure.
- `proposals/Framework_Clock_Gap_2026-06-09.md` — why the sweep exists; the rule.
- `REF_The_Conversion_Check.md` — Verification rule + Clock annotation format.
- `Pod_Matchup_Matrix.md` — the Race/Disrupt/Both verdicts the clock feeds.
- `project_pod_combo_opponent` (memory) — the T6–7 pod the bar is set against.
