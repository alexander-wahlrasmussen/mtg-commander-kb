# Workflow: Summary Generation

Producing a `_Summary.md` file for a deck. Format matches existing summaries (The Loam Cycle, The Grand Design, Lightning War, etc.).

---

## Inputs

- Final, audited decklist (`.txt` — ground truth).
- Conversion Check score from `WF_Deck_Audit.md`.
- Core loop statement (one sentence).
- Two or more named closing lines with turn estimates.
- Kill window estimates (Goldfish, Through-Interaction).
- Any archetype-specific notes.

---

## Template

Use `TPL_Deck_Summary.md` as the starting skeleton. Do not reinvent the structure — consistency across summaries is part of the value.

---

## Style

- **Direct, dense, no fluff.**
- No emojis, no motivational filler, no "this deck is amazing because" framing.
- `---` separators between major sections.
- Card names in plain text. Mechanical identity is stated, not celebrated.
- When referencing a UB reskin: name the reskin first, then the original in parentheses. "Aang's Shelter (Teferi's Protection)".
- Summaries are **arguments**, not inventories. The `.txt` is the list. The summary explains what the list *does*.

---

## Required sections

1. **Header.** Deck name, commander, colors, score (X/X/X/X = total/20), bracket, archetype.
2. **Core Loop.** One paragraph. Name the machine, not the flavor. Do not describe the commander's ability text — describe what the deck does with it.
3. **Closing Lines.** Minimum two. Each with a turn estimate from engine-online to lethal.
4. **Kill Window.** Goldfish / Through-Interaction.
5. **Durability notes.** How does the deck recover from a Cyclonic Rift on turn 7? Name the redundant engine pieces. Name the recursion tools. Estimate turns to threat re-establishment.
6. **Interaction Package.** Count + categories. Instant-speed percentage.
7. **Game Changer Slots.** X/3 with names and aliases. Cross-reference `REF_Game_Changers_List.md`.
8. **Known Weaknesses.** Honest. At least one. "None" is not an acceptable answer.
9. **Changelog** *(optional)*. Recent swaps with one-line rationale each.

---

## After writing

- Save as `<deck-name-kebab>_Summary.md` (e.g., `the-exiles-return_Summary.md`). Claude Project convention uses title case with underscores; pick one and be consistent.
- Update `Deck_Index.md` with the new score if it changed.
- Update `Collection_Master_Status.md` with the summary status (generated / updated / needs re-audit).

---

## Do not

- Do not include pod-specific notes in the summary. Those live in a separate pod log or in the player's head.
- Do not inflate the score to match the tone of the summary. If the summary reads enthusiastically and the score is 15/20, recheck the score.
- Do not list every card in the deck. The `.txt` is the inventory.
- Do not skip the Known Weaknesses section. Every deck has one.
