# Framework Clock Gap — Findings & Backlog (2026-06-09)

**Trigger:** user observation after the five speed-curve analyses (Lightning War, Replication Crisis, Calamity Tax, Grand Design, Exile's Return): decks that score high on the Conversion Check still fail to win inside acceptable Bracket-3 timing, and the gap only surfaced once the goal became "bracket 4 in spirit" against the pod's T6–7 combo clock.

**Status:** Findings 1–2 codified 2026-06-09 (see §3). Findings 3–5 are standing practice / backlog — this doc is the revert-point for a future session.

---

## 1. The flaw

The Conversion Check's four axes (Core Loop, Kill Reliability, Durability, Interaction) are all **turn-agnostic**. Kill Reliability asks "when you go for the kill, does it work?" — never "**what turn** does the deck reach 'go for it'?" Durability and Interaction actively trade against clock. A deck can legitimately score 18–19/20 as a fortress that kills on T10.

Meanwhile the bracket system defines behaviour by **expected win turn** — an output — while our compliance checks (3-GC cap, combo approval rules) police **inputs**. The pod's combo decks exploit the gap from one side (ingredient-B3, behaviour-B4); our roster sat on the other (ingredient-legal, behaviourally too slow).

**Score and measured clock were essentially uncorrelated in the 15–19/20 band.**

## 2. The evidence

| Deck | Hand-claimed window | Lab-measured | Direction |
|---|---|---|---|
| Replication Crisis | Goldfish T5–7 | decap median T7 (T5 ≈ 2%), table T10+ | optimistic |
| Exile's Return | Goldfish T6–8 | decap T7–8 (T6 = 9%), table T10 | optimistic |
| Lightning War (pre-pivot) | "fast burn" | old combo ~1% by T6; honest kill only post-rebuild (T6–7) | optimistic |
| Calamity Tax (31-May swap) | "sped up" | NOT faster — T7–9 unchanged, mana-gated | optimistic |
| Grand Design | Goldfish T6–8 | decap median T10 (T6 ≈ 1%, T8 ≈ 20%), table T12+ | optimistic (~2 turns at median) |
| ER Kiki swap / RC Kiki swap docs | "T6–8 → T5–7" / faster | both swaps measured *slower* than baseline | optimistic |

**Six labs, six corrections, all in the same direction.** Narrative estimation systematically rounds the god-hand into the stated range — and Grand Design (2026-06-10) is the largest gap yet (~2 turns at the median, not ~1 at the front edge). Separately, Grand Design held 19/20 while every kill line funnelled through one sorcery its creature-tutors can't find — the score gave no warning. The clock now confirms the consequence the rubric was blind to: the named finisher (Finale X≥10) fires median **T11** in only **~9%** of goldfish games, so **96% of the deck's decaps are incremental combat**, median **T10**. A legitimate 19/20 fortress that kills late — the cleanest single instance of "score and measured clock are uncorrelated in the 15–19/20 band."

## 3. Codified 2026-06-09 (done — no action needed)

1. **Verification rule** — no kill-window claim without a lab citation (script + date) or an explicit *(unverified)* flag. Same standard as prices.
   - `REF_The_Conversion_Check.md` → "Verification rule (added 2026-06-09)" under Expected Kill Window.
   - `REF_Domain_Principles.md` → new "Clock discipline" section.
   - `CLAUDE.md` → hard-rule bullet.
2. **Clock annotation** — score and clock reported together, never merged: `NN/20 · Clock: Tx–y decap / Tz table (lab YYYY-MM-DD)`. Not a fifth axis (judged vs measured; preserves comparability of historical audits). Decap and table stated separately (they diverge 2–3 turns in combat decks).
   - `REF_The_Conversion_Check.md` → "Clock annotation (added 2026-06-09)".

## 4. Standing practice (no codification needed)

3. **The Pod Matchup Matrix is the real bracket instrument.** Every deck classifies as *Race* / *Disrupt* / *Both* against the pod's T6–7 clock. ER is the proof the two instruments complement: it lost the race but landed Favoured *because of* the rubric's axes (interaction that survives Abolisher). Keep maintaining the matrix as the deliverable; the Conversion Check answers *whether*, the lab answers *when*, the matrix answers *so what*.

## 5. Backlog (revert here in a future session)

4. **Extract a shared speed-lab harness.** The four labs (`lw_speed_lab.py`, `rc_speed_lab.py`, `gd_speed_lab.py`, `er_speed_lab.py`) share ~70% machinery: greedy mana model (lands+rocks), draw/mulligan engine, fixed-seed lever harness, tutor-wildcard assignment, T-grid reporting. **When the next lab is built**, extract `speed_lab_core.py` with per-deck kill modules. Do not retrofit the existing four — they're committed evidence for their writeups.

5. **Lab the unverified windows.** Current status of every Summary's Kill Window claim (grep audit 2026-06-09):

| Deck | Claimed goldfish | Status |
|---|---|---|
| Lightning War | T6–7 | ✅ lab-verified (2026-06-08) |
| Replication Crisis | T7–8 decap / T10+ table | ✅ lab-verified (2026-06-09) |
| Exile's Return | T7–8 decap / T10 table | ✅ lab-verified (2026-06-09) |
| Calamity Tax | T7–9 | ◐ corroborated by speed analysis (mana-gated, "same T7–9") but no kill-turn goldfish run |
| Grand Design | T6–8 | ✅ lab-verified 2026-06-10 (`gd_clock_lab.py`) — decap median T10 (T6 ≈ 1%, T8 ≈ 20%) / table T12+; the 6th optimistic front edge and the largest gap. Finale fires median T11 / ~9%; decaps are 96% incremental combat |
| Eldrazi Stampede Chaos | T6–8 | ❌ unverified — front-edge claim, priority |
| Radiation Sickness | T6–9 | ❌ unverified — wide range, priority |
| Crystal Sickness | T7–9 | ❌ unverified |
| Curse of the Scarab | T7–9 | ❌ unverified |
| Diminishing Returns | T7–9 | ❌ unverified |
| Earthbend the Meta | T7–9 | ❌ unverified |
| Lorehold Spirits | T7–9 | ❌ unverified |
| The Genome Project | T7–9 | ❌ unverified |
| Ms. Bumbleflower | T8–10 | ❌ unverified |
| The Dark Lord's Army | T8–10 | ❌ unverified |
| The Loam Cycle | T6–8 | — being dismantled, skip |

   **First action when reverting:** sweep the ❌/◐ Summaries and append *(unverified)* to their Kill Window fields per the new rule — cheap, honest, and makes the backlog self-documenting. Then lab opportunistically as decks come up; prioritize the front-edge claims (Eldrazi T6–8, Grand Design T6–8, Mothman T6–9) since every front edge measured so far was optimistic.

---

## Related

- `proposals/Exiles_Return_Speed_Curve_Analysis.md` — the run that triggered the user's framework question
- `proposals/Replication_Crisis_Speed_Curve_Analysis.md`, `proposals/Lightning_War_Speed_Curve_Analysis.md`, `proposals/Calamity_Tax_Speed_Curve_Analysis.md`, `proposals/Grand_Design_Speed_Curve_Analysis.md`
- `Pod_Matchup_Matrix.md` — the Race/Disrupt/Both verdicts
- `REF_The_Conversion_Check.md` §Expected Kill Window — the codified rules
