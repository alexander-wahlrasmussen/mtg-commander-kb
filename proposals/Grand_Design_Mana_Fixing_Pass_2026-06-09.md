# The Grand Design — Mana-Fixing Pass (Resolved: Measurement Artifact, No Land Changes)

**Date:** 2026-06-09
**Ask:** Execute the mana-fixing pass the Pod Matchup Matrix flagged as higher priority than any card swap ("Fix Grand Design's mana base — 39% all-colours-from-lands by T6").
**Result:** **The pass is closed with zero land changes.** The 39% figure was a **simulator measurement artifact**, not a deck flaw. The model was fixed in `deck_sim.py`; under the corrected model the deck's colour floor is **89–90% by T6** — among the roster's healthy bases. The matrix's recommendation #2 is retracted, and the freed priority goes back to the merged ETB/finisher build.

---

## 1. What was wrong: the sim scored the deck's best fixers as zero-colour lands

`deck_sim.py` credited each land with its Scryfall **`color_identity`** — a field that is **empty** for:

- **all 6 sac-fetches** (Polluted Delta, Windswept Heath, Verdant Catacombs, Misty Rainforest, Flooded Strand, Marsh Flats) — they have no mana ability of their own;
- **all 4 rainbow lands** (Command Tower, Exotic Orchard, Reflecting Pool, City of Brass);
- Yavimaya, Cradle of Growth read as G-only (correct for itself; its Forest-ification of other lands is unmodelled — acceptable).

**11 of 39 lands (28%) — including the five best fixers in the deck — were scored as producing no colours.** Of course the deck "failed" to assemble WUBG: the model deleted Command Tower.

### Hand-count of real sources (39 lands)

| Colour | Printed sources | + fetches that find one | Total |
|---|---|---|---|
| W | 14 (4 rainbow, 3 shocks, Indatha, Vault, Eiganjo, 4 Plains) | +3 (Strand, Heath, Flats) | **17** |
| U | 14 (4 rainbow, 3 shocks, Zagoth, Springs, Morphic, Otawara, 3 Island) | +3 (Delta, Misty, Strand) | **17** |
| B | 16 (4 rainbow, 3 shocks, 2 triomes, Stadium, Vault, Morphic, Bojuka, Phyrexian Tower*, 2 Swamp) | +3 (Delta, Catacombs, Flats) | **19** |
| G | 13 (4 rainbow, 3 shocks, 2 triomes, Springs, Stadium, Yavimaya, 3 Forest) | +3 (Heath, Catacombs, Misty) | **16** |

*Phyrexian Tower's {B}{B} requires sacrificing a creature — counted with that caveat.

≥16 sources per colour in a 39-land base is textbook-healthy for 4 colours. The deck was never colour-fragile.

## 2. The fix (in `deck_sim.py`, canonical — affects the whole roster)

Two changes, both data-driven (no card-text parsing, consistent with the tool's design):

1. **Use Scryfall's structured `produced_mana` field** when present, restricted to WUBRG (Command Tower/City of Brass → WUBRG; Phyrexian Tower → B; Ancient Tomb → none).
2. **Resolve sac-fetches against the deck's own lands**: an explicit `FETCH_TYPED` table (the 10 standard fetches + Krosan Verge) maps each fetch to its fetchable basic types; its effective colours = union of colours of the deck's lands carrying those types. Basic-only fetchers (Prismatic Vista / Evolving Wilds class) see basics only.

Remaining, documented optimism: enters-tapped is ignored, Exotic Orchard/Reflecting Pool are board-dependent, fetch-target depletion is ignored. Still a *floor* on castability — just no longer a broken one.

## 3. Corrected numbers

**Grand Design (40k trials, seed 12345):**

| All colours from lands | T2 | T3 | T4 | T5 | **T6** | T8 |
|---|---|---|---|---|---|---|
| old (broken) model | 4 | 12 | 22 | 31 | **39** | 51 |
| **corrected model** | 49 | 68 | 80 | 86 | **90** | 94 |

Identical for the pre-swap (20260402) and post-swap (20260502) lists, and identical for the proposed ETB build (land-neutral swaps) — every *relative* conclusion in the earlier analyses survives; only the *level* was wrong.

**Roster-wide (T6, 20k trials):** every deck rises; the spread compresses to **88–99%**. The two "⚠⚠ structurally rock-dependent" outliers were pure artifacts of fetch/rainbow-heavy bases:

| Deck | old | corrected |
|---|---|---|
| **Grand Design** | 39 ⚠⚠ | **89** |
| **Earthbend the Meta** | 40 ⚠⚠ | **90** |
| Calamity Tax | 48 ⚠ | 96 |
| Lightning War | 67 | 97 |
| Dark Lord's Army | 67 | 89 |
| (all others) | 66–95 | 88–99 |

The matrix finding "colour-fixing is the real consistency divide" is **retracted** — the divide was an artifact gradient: decks with basics-heavy bases scored high, decks with premium fetch/rainbow bases scored low. The model punished exactly the lands players buy *for* fixing.

## 4. Verdict & what still holds

- **No land swaps recommended.** At a 90% T6 land-only floor — *before* Sol Ring, Arcane Signet, Birds, Bloom Tender, and Carpet of Flowers are counted — additional fixing buys ~nothing. Spending slots or money here would be optimizing a solved problem.
- **What's genuinely left on mana:** the floor at T2–3 (49/68%) is ordinary 4-colour reality — mitigated by the existing dorks/rocks and by mull decisions, not by land swaps. Phyrexian Tower and Bojuka Bog are the only "taxed" sources, both there for their abilities. Fine.
- **Priority returns to the card passes:** with mana off the table, the highest-leverage Grand Design work is the **merged ETB/finisher build** (`Grand_Design_ETB_Disruption_Pass_2026-06-09.md` §5): −Grisly Salvage / −Ghostly Flicker / −Dread Return / −Persist → **+Craterhoof Behemoth ($0) +Skyclave Apparition ($0) +Spellseeker (~$3) +Noxious Gearhulk ($0)** — a finisher the engine can find plus disruption that breaks *their* clock through an Abolisher.

## 5. Corrections propagated

- `Pod_Matchup_Matrix.md` — Colour T6 column rebuilt for all 16 decks; finding #2 and recommendation #2 rewritten; Grand Design verdict upgraded to unconditional **Favoured**.
- `Grand_Design_ETB_Disruption_Pass_2026-06-09.md` §3/§5/§6 — 39% references corrected.
- `Grand_Design_Finisher_Upgrade_2026-06-08.md` §4 — Reliquary Tower note corrected (verdict unchanged).
- `Grand_Design_Speed_Curve_Analysis.md` — colour row annotated.
- Memory: `project_deck_sim_and_matchup_matrix` finding 2 corrected; `project_grand_design_etb_pass` updated.

---

Related: `Pod_Matchup_Matrix.md` · `Grand_Design_ETB_Disruption_Pass_2026-06-09.md` · `Grand_Design_Speed_Curve_Analysis.md` · [[project_deck_sim_and_matchup_matrix]]
