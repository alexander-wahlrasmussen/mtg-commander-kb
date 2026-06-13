# Workflow: Candidate Bake-Off (pick-one)

Choosing **one** deck to build from a field of candidates, against a stated
goal — e.g. "answer the recurring combo pod." Distilled from the 2026-06-12
bake-off (9 candidates → Yuriko). The worked example lives in
`campaigns/Candidate_Bakeoff_2026-06-12.md`; the verdict format is
`campaigns/Candidate_Bakeoff_Verdict_2026-06-12.md`.

Use this when there is a real budget/slot for exactly one build and several
contenders. For scoring a single existing deck, use `WF_Deck_Audit.md`.

---

## Inputs

- A candidate field (commanders + rough archetype each).
- The **brief**: the specific problem the build must solve, stated as a
  falsifiable bar. See `project_pod_combo_opponent` for the canonical target.
- Access to the labs (`scripts/*_clock_lab.py` on `speed_lab_core.py`),
  `scripts/card_lookup.py`, the Moxfield CSV, and `decks/*.txt` for sweeps.

---

## Stage 0 — Define the brief and the bar

- State the bar as a number, not an adjective. The pod-beating bar is a
  **decap bar** — "decap the threat by T≤7" — not "kill the table by T7."
  Table clock is the *reliability* metric, not the race metric. (Genome's T8
  table is the roster benchmark for "reliable.")
- The bar is what every later claim is measured against. Write it down before
  looking at any candidate, so it can't drift to fit a favourite.

## Stage 1 — Kill-shape pre-screen (free; orders the field)

Rank candidates *before* paying for labs, using the validated kill-shape lens.
It predicted the decap/table pattern of all seven 2026-06-12 labs:

| Kill shape | decap vs table | Race profile |
|---|---|---|
| All-opponent simultaneous (pings/drains/symmetric burn) | **converge** (≈equal) | honest racer; table clock ≈ decap |
| Combat focus-fire (attack one player) | **diverge 2–3 turns** | decaps fast, tables slow |
| 3-mana on-cast combo (Thoracle-type) | **decap = table by definition** | binary; gated on assembly + approval |

For each surviving candidate, **pre-register a falsifiable clock gate**:
"~T7 median decap or no build." Adjectives ("strong turbo") are not gates and
have an 8-for-8 record of being falsified by the lab. A claim survives only if
it is (a) pre-registered and (b) decap/table-split.

## Stage 2 — Lab the finalists

- Finalize a real 100-card list for each contender (99 + commander; in-identity;
  ≤3 GCs per `WF_GC_Verification.md`). Commander goes in a separate END block of
  the `.txt` — a line-1 commander breaks the parser.
- Run the clock lab (20 000 trials, fixed seed, dated). Report **decap and
  table separately** — never one number. Record never-in-12 as the reliability tail.
- Labs double as decklist linters: a parse error is usually a misspelt/nonexistent
  card in the `.txt`. Fix ground truth before trusting the clock.

## Stage 3 — Full Conversion Check on the contenders

- Full-pass score (`REF_The_Conversion_Check.md`, via `WF_Deck_Audit.md`) for
  the top 2–3; band estimates for the eliminated. Expect the full pass to
  **correct screen estimates downward** — a measured weak axis (e.g. 42%
  never-in-12) caps Kill Reliability no matter how good the screen looked.
- "No single axis compensates for a catastrophic gap in another." A Durability 2
  is a red flag the clock cannot buy back.

## Cost — sweep, don't estimate

`owned ≠ free`. A cost claim must cite an **availability sweep** (Moxfield CSV +
`grep decks/*.txt` for deployed copies, dated) or carry an explicit *(unverified)*
flag. Optimistic-by-default cost estimates fail the same way clock estimates do
(3 of 5 internal estimates revised up on sweep, one ~3×).

## Two cross-deck correctness traps

- **Singleton combo density.** A "2-card combo" whose halves are 1–2 copies in 99
  assembles like a 4-card combo. Count *copies-in-deck per role*, not
  pieces-in-combo, when judging assembly speed.
- **Goldfish conventions aren't deck-neutral.** "Every attacker unblocked" is
  near-literal for an evasion deck and pure fiction for a ground-token deck facing
  a flying-blocker pod. When *comparing across candidates*, state which decks the
  shared convention flatters — a 1-turn lab edge can be smaller than the asymmetry.

---

## Verdict (Stage 4) — report format

Mirror `Candidate_Bakeoff_Verdict_2026-06-12.md`:

```
THE VERDICT: build [X] — conditional on [gate, if any]; fallback [Y] if gate fails.

Rank table: Candidate | Clock (decap / table) | Never-in-12 | CC | Cost (flag) | one-line
Why [winner] over [runner-up A]  (the clock leader)
Why [winner] over [runner-up B]  (the brief-fit leader)
Why the rest are out
Pod fit vs the actual opponent
Honest weaknesses of the pick
User gates: what must happen before purchase (pod approval, price verify, etc.)
```

The winner is the best **clock × reliability** product that clears the brief and
whose pre-registered gate passed — not the fastest goldfish. Purpose-built beats
expert-built on brief-fit: external "scouting" lists signal card quality, not fit
to your pod's failure mode.

---

## Do not

- Do not let an un-labbed adjective ("turbo," "fast") survive into the verdict.
- Do not conflate decap and table clock — state both, every candidate.
- Do not call an owned card free, or quote a price without a sweep or an *(unverified)* flag.
- Do not pick the goldfish leader without correcting for convention asymmetry across decks.
- Do not exceed 3 GCs in any candidate list; stop and flag if a build would.
