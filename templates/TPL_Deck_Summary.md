<!--
CANONICAL DECK SUMMARY SCHEMA (harmonized 2026-06-28).
Section ORDER and H2 NAMES below are the canonical format. `scripts/validate.py` lints every
`decks/*_Summary.md` against it (the "Summary section schema" check) and `kb_content.py` parses
these headings to build the dashboard deck pages — so keep the **## headings verbatim**:
  Required: What the Deck Does · Kill Lines · Conversion Check — N/20 · Don't-Miss Rulings · Decklist
Don't reintroduce the retired variants (Core Loop / Closing Lines / How We End Games / Lab Results /
Conversion Check Assessment|Breakdown) — the lint will flag them. Keep Kill Lines as a top-level ##
(not a ### nested under What the Deck Does).
-->
# [Deck Name]

## Quick Reference

| Field | Value |
|---|---|
| **Commander** | [Name] ([cost], [type line]) |
| **Colors** | [Guild/shard] ([WUBRG]) |
| **Archetype** | [Aggro / Control / Combo / Aristocrats / Reanimator / Spellslinger / …] |
| **Bracket** | 3 by GC count (X/3). [house-rule notes] |
| **Game Changers** | [Card, Card, Card] (X of 3) |
| **Conversion Check** | **XX/20 (A/B/C/D)** · audited YYYY-MM-DD |
| **Kill Window** | Clock: **TX decap / TY table** (lab `*_clock_lab.py`, YYYY-MM-DD) |
| **Status** | [built / cards on order / proposal] — [ground-truth .txt] |

-----

## Commander Rules Text

[Verified oracle text via `card_lookup.py` (read the card — do not paraphrase from memory), then
one line on what the deck DOES with each ability. Note whether the commander is a combo linchpin or
just a value/disruption engine.]

-----

## What the Deck Does

[One paragraph. What resource does this deck exploit, and how does it turn that resource into a win?
Name the machine, not the flavor. Target 3–6 sentences. This paragraph is what the dashboard deck
page shows as the game plan, so lead with substance (no table, no list lead-in stub).]

-----

## Kill Lines

**Line 1 — [Title] (primary):** [Mechanical description. Pieces required; engine-online → lethal in
N turns. Flag any single must-have card.]
**Line 2 — [Title]:** [As above.]

*(Minimum two; canonical format is `**Line N — Title (tag):** desc`. Letter indices `Line A` are
also accepted by the parser. Label single-point-of-failure cards so the fragility is visible.)*

-----

## Kill Window

- **Goldfish:** Clock decap TX / table TY (lab `scripts/*_clock_lab.py`, YYYY-MM-DD).
- **Through interaction:** TX–Y *(or `(unverified)` if unmodeled)*.

*(A kill-window/turn claim MUST cite a `*_clock_lab.py` / `deck_sim.py` run or carry `(unverified)` —
`validate.py` lints this. Decap and table are different clocks; state both.)*

-----

## Conversion Check — XX/20 (audited YYYY-MM-DD)

Scored from the list per `reference/REF_The_Conversion_Check.md`. Four judged axes; the clock is
measured.

| Axis | Score | Rationale |
|---|---|---|
| **Core Loop** | **X/5** | […] |
| **Kill Reliability** | **X/5** | […] |
| **Durability** | **X/5** | […] |
| **Interaction** | **X/5** | […] |

**Reading:** [band + the limiting axis.]

-----

## Durability

[One paragraph. How does the deck recover from a board wipe on turn 7? Redundant engine pieces,
recursion tools, turns to re-threaten.]

-----

## Interaction Package

**[N] pieces total.** Removal: [count] — [examples]. Counters: [count] — [examples]. Targeted
disruption / stax: [count] — [examples]. Instant speed: [%].

-----

## Known Weaknesses

- [At least one. Honest. "None" is not acceptable.]

-----

## Don't-Miss Rulings

[The card-text gotchas that lose games when missed — verify each via `card_lookup.py` (read the
card + its official rulings; no writing from memory).]

- **[Card / interaction]** — [the gotcha: hidden type, trigger order, replacement-vs-trigger, threshold counting, reskin behaviour].
- **[Card / interaction]** — […].

-----

## Decklist (100 cards)

### Commander (1)
- [Card]

### [Bucket name] (N)
- [Card]  *(GC)*

*(Functional buckets with `### Name (N)` headings; the counts must total 99 + commander. The dated
`.txt` is ground truth — the Summary only supplies the labels.)*

-----

## Piloting Notes (for borrowers)

[Mulligan priorities, threat assessment, lines to hold. Optional but recommended.]

-----

## Changelog

- **YYYY-MM-DD:** [Swap, with one-line rationale.]
