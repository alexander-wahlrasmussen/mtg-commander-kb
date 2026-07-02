# Opponent clock labs — Backlog #13 Phase 2

Clock labs for the **archenemy's decks** (`opponents/*.txt`), kept deliberately separate
from the roster lab suite. Same `speed_lab_core` harness → numbers directly comparable to
our own labs, but:

- **NEVER registered** in `deck_registry`, `pod_gauntlet.CLOCKS`, the golden snapshot, or
  `clock_check` — those chains assume *our* decks and their Summary-citation discipline.
- **PROXY clocks, not citation-grade.** Every input list is either his real (possibly
  stale/incomplete) Archidekt export or an evidence-tiered reconstruction — see each
  `opponents/*.txt` header. A lab number here is written `~Tx (PROXY lab YYYY-MM-DD)`.
- **Purpose:** replace the hand-assumed `pod_gauntlet.K_DIST` ("wins T6-7") with *measured*
  per-opponent attempt-turn distributions + rebuild the `OPPONENTS` blend weights from the
  observed rotation (2026-07-02: Ur-Dragon + Acererak every meetup, H&K occasional but
  dominant, Henzie rare). See `analysis/Pod_Clock_Sensitivity_2026-07-02.md` for why the
  middle tier band + all absolute P(beat pod) levels depend on this measurement.

Commander note: opponent stems aren't in `deck_sim.COMMANDERS`, so each lab pulls its own
commander from the parsed library (`pull_commander`) instead of registering the deck in the
roster core.

Run any lab: `python scripts/opponent_labs/<lab>.py --trials 40000`
