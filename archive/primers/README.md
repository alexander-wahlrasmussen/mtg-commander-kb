# Retired pilot primers

These 16 `*_Primer.md` pilot-reference pages (and `TPL_Deck_Primer.md`) were retired on
2026-06-22. The dashboard deck page (`ui/` → DeckPage) is now the living pilot reference:
it bakes from the `.txt` + `*_Summary.md`, so it can't go stale the way these frozen
snapshots did (15 of 16 were last touched 2026-05-30, and several carried kill-window
claims the June clock-lab sweep had since falsified).

Before retirement, the durable, unique content was ported into each deck's `*_Summary.md`:

- **Don't-Miss Rulings** — now a `## Don't-Miss Rulings` section in the Summary, surfaced
  live on the deck page (parsed by `kb_content._rulings`).
- **Mulligan + Threats & timing** — folded into `## Piloting Notes (for borrowers)`.
- **Reskins** — `## Reskins (for borrowers)` where the Summary lacked one.

Stale bits were dropped or corrected on the way in (bare "Goldfish Tx–y" clocks → the
deck page's lab clock; Lightning War's "no infinite" line → the Seething Song + Reiterate
line; cut cards like Opposition Agent / High Fae Trickster removed).

Kept here for reference and git history only — they are **not** synced to the Claude
Project (the sync script skips `archive/`).
