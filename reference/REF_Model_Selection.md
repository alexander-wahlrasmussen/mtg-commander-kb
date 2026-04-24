# REF_Model_Selection — Model & /effort Guide

When to reach for which Claude model and which `/effort` level for work in this KB. Available models: Opus 4.7, Sonnet 4.6, Haiku 4.5.

---

## Default posture

**Opus 4.7 is the default for this KB.** Most work here is judgment-heavy — card text discipline, 4-axis Conversion Check scoring, Bracket 3 rule compliance, mechanical distinctiveness. The cost of a wrong answer (silent 4th GC, inflated score, missed combo, cutting a load-bearing card, spending money on the wrong acquisition) is higher than the cost of compute.

Downgrade only when the task is genuinely mechanical.

---

## Task → Model

### Haiku 4.5 — pure lookups and counting

- Verify a decklist is exactly 100 cards (99 + commander)
- Reskin alias lookup against `REF_Reskin_Aliases.md` (literal string match)
- Single-card GC check against `REF_Game_Changers_List.md` (yes / no)
- File renames with date bumping per the hard rule
- Listing decks by tier / colors / commander from `Deck_Index.md`
- Grepping a decklist for a card name

If Haiku starts making evaluative claims ("this would be better than…", "this interacts with…"), stop and re-roll on Opus.

### Sonnet 4.6 — routine docs, drafting from finalized state

- Updating `Deck_Index.md` after a confirmed change
- Drafting a `*_Summary.md` from a **finalized** decklist using `TPL_Deck_Summary.md` — facts already settled, only transcription remains
- Changelog appends on existing summaries
- Filling in `Collection_Master_Status.md` from the spreadsheet
- Running the sync script and reporting results
- Navigational Q&A ("where is X documented?", "which decks run card Y?")

Sonnet's sweet spot is narrow in this KB: the judgment has already happened elsewhere; the task is transcription, templating, or navigation.

### Opus 4.7 — anything with a judgment call

- `WF_Deck_Audit.md` — 4-axis Conversion Check scoring
- `WF_Card_Swap_Evaluation.md` — card text + role + math + interactions + Bracket 3 compliance (all 6 steps map to past failure modes)
- `WF_GC_Verification.md` beyond the grep step — ambiguous cases, overage handling, reskin edge cases
- `WF_Summary_Generation.md` when the deck is still in flux (fresh scoring, not just transcription)
- New deck build evaluation — mechanical distinctiveness, pod approval for 3+ card infinites, archetype coverage
- Cross-deck re-audits after GC list updates (Oct 2025, Feb 2026, and future shifts)
- Updates to `REF_Domain_Principles.md` — the generalization has to be right or it will mis-steer future sessions
- Conflicts between sources requiring the ground truth hierarchy to be applied
- Scoring disputes where a score feels inflated or deflated relative to the rubric

---

## `/effort` by task

`/effort` controls reasoning depth independent of model. Higher = more careful, slower, more tokens. `xhigh` is Opus-only; `max` is the ceiling.

| Effort | When to use |
|---|---|
| **low** | Haiku lookups; Sonnet transcription from finalized state; single-file renames |
| **medium** | Sonnet drafts from a pinned-down decklist; Opus on well-defined swaps (clear role, clear math, no GC implications) |
| **high** | Opus full deck audits; Opus swap evals where role or interactions are non-obvious; single-deck GC re-audit after a list update |
| **xhigh** | New deck architecture from scratch; cross-deck re-audits spanning 5+ decks; `REF_Domain_Principles.md` updates; judgment calls against Bracket 3 house rules where precedent is thin |
| **max** | The hardest calls — "should this deck exist at all", scoring disputes that have already been re-run once, new ruleset or framework drafts |

---

## Rules of thumb

- Conversion Check scoring never runs below **Opus + high**. A one-axis rubric error propagates through the whole 20-point score.
- Swap evals are Opus territory by default. Sonnet may appear to handle them but silently misses interaction and card-text gotchas.
- If a lookup hedges ("probably", "I think"), re-roll on a larger model. Don't act on a hedge.
- When an audit or swap result surprises you, re-run **one effort level higher** before arguing with it. If it doesn't change, the surprise is the signal.
- Model choice never substitutes for the authoritative reference. `REF_Game_Changers_List.md` and `REF_Reskin_Aliases.md` win over any model's memory at any effort level.
- Cost of a mistake here is usually measured in money (wrong card bought), time (re-auditing all 16 decks), or trust (a bad summary that gets referenced later). Price compute accordingly.
