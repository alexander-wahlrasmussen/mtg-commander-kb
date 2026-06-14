# Backlog — tooling & analysis ideas

Forward-looking ideas we want to try but haven't started. Captured 2026-06-14 (after the
`validate.py` + clock-lab-harness session). Not a commitment or a spec — a "don't forget"
list. When one is picked up it graduates to a `scripts/` tool + (if it's a clock/analysis)
an `analysis/` write-up, and its row moves to Done.

---

## 1. The Pod Gauntlet — simulate the matrix verdicts ⭐ (top pick)

Turn `Pod_Matchup_Matrix.md` from hand-judged ("Favoured — disruption-led") into a
**win-probability per deck vs the recurring archenemy**.

- **The question:** does each deck actually beat the pod combo opponent (Ur-Dragon +
  Hidetsugu / Kairi / Kenrith / Kinnan, ~T6–7 behind Grand Abolisher)?
- **Ingredients already exist:** each deck's decap-clock distribution (the `*_clock_lab.py`
  suite), each deck's disruption availability (`delay_lab.py`), and the opponent profile.
- **The model:** race our kill/lock turn vs their combo turn. Crucially, Grand Abolisher
  **zeroes out reactive answers** (counterspells) — only credit *proactive* hate already on
  the battlefield (Drannith, Cursed Totem, Rule of Law, Mindcensor). Output: P(we win the race).
- **Builds on:** `delay_lab.py` (already does answer-availability vs the pod combo turn), the
  clock labs, the pod-opponent + Grand-Abolisher domain notes.
- **Spirit:** heuristic race model, not a rules engine — same "trust shapes, not decimals"
  caveat as every lab. State decap vs table clocks separately, as the verification rule requires.

## 2. Close the clock-claim loop — verify, don't just cite

`validate.py` checks that a clock citation *exists*; this would check it's *still true*. Our
#1 recurring failure is clock claims drifting from reality (7 of 8 hand-estimates falsified).

- Have the labs emit a tiny JSON `{deck, decap_median, table_median, never}` (cheap now that
  `report_clock` is centralized in `speed_lab_core.py` — it already computes all four).
- A checker reads every `Clock: Tx–y (lab …)` line in the Summaries and flags any whose
  numbers no longer match the lab's current output — catches a Summary that went stale after
  its deck changed.
- **Builds on:** the centralized `report_clock`, `validate.py`'s doc-scanning.

## 3. The "one-purchase unlock" optimizer

`Build_And_Swap_Tracker.md` §4 (cross-deck contention) and "what unlocks the most swaps" are
hand-maintained. Automate the ranking.

- Over the Moxfield CSV + all decklists: *which single card, bought once, frees the most
  pending swaps across decks*, and *which owned card is most over-committed* (wanted by N
  decks, owned ×M < N).
- **Builds on:** `availability_check.py`, `collection/moxfield_haves_*.csv`, the swap rows in
  the tracker.

## 4. Kill-tree diagrams (the fun one)

Render a deck's kill **lines** as a visual decision tree — the labs already enumerate them as
cheapest-first branches. The Mermaid Chart tool is available. Pure visualization, a nice
artifact for a Summary or primer. Low priority, high delight.

---

*Source: 2026-06-14 brainstorm. Order ≈ value; #1 is the recommended first build.*
