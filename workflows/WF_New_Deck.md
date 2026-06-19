# Workflow: Add a New Deck to the Roster (registry-first)

Wire a **new active-roster deck** into every tool — the clock labs, the bake-off, the
mulligan keep specs, the pod gauntlet, the kill trees and `report.py` — with the least
work and no drift. After the 2026-06-17 consolidation the per-deck facts live in ONE place
(`scripts/deck_registry.py`), so adding a deck is **one registry row + one kill lab**, not an
edit in five files.

Distinct from `WF_Candidate_Bakeoff.md` (choose one of many *un-built* candidates) and
`WF_Kill_Window_Lab.md` (build the clock lab — Stage 2 here delegates to it). Use this when a
candidate has *won* and is becoming a real, tracked roster deck.

The single source of truth and who reads it:

| Reads the registry | For |
|---|---|
| `framework_bakeoff.py` | `DECKS` (identity + CC) · `WIN_LINE` |
| `keep_spec.py` | `JUDGMENT` · `ALSO` (mulligan keep) |
| `deck_sim.py` | `COMMANDERS` · `DISPLAY` (active roster) |
| `pod_gauntlet.py` | display name + lab pointer (guarded) |
| `kill_tree.py` | `KILL_TREES` decision-tree specs |
| `report.py` | the whole row |

---

## Stage 0 — Read the cards first (CLAUDE.md hard rule)

`python scripts/card_lookup.py "<commander>"` and every card named in a kill line, before
writing anything. Card-text misreads are the dominant failure mode. Resolve UB names through
`REF_Reskin_Aliases.md`. If Scryfall data is stale, `python scripts/update_scryfall_data.py`.

## Stage 1 — Land the decklist

- Save the Moxfield-format list as `decks/<deck-kebab>-YYYYMMDD*.txt` (dated filename = version
  history; commander in its own block at the end — a line-1 commander breaks the parser).
- Exactly 100 cards (99 + commander). ≤ 3 Game Changers. Confirm with `scripts/validate.py`.

## Stage 2 — Build the kill lab (the one irreducible artifact)

Follow **`WF_Kill_Window_Lab.md`** end to end: copy `scripts/clock_lab_template.py`, encode the
deck's KILL CHECKS, produce `scripts/<xx>_clock_lab.py` with a `--mode clock` that prints decap
/ table medians. This bespoke turn-by-turn logic is the part that *can't* be data. Note its
`(module, mode)` — e.g. `("xx_clock_lab", "clock")` — for the registry row.

## Stage 3 — Add the registry row (`scripts/deck_registry.py`)

One entry in `DECKS`, keyed by slug (underscore form). Copy the schema from a neighbour; fill:

- `name`, `stem` (decklist prefix), `commander` — identity.
- `lab` — the `(module, mode)` tuple from Stage 2, or `None` for a multi-variant lab.
- `cc`, `cc_axes` — Conversion Check total + (core, kill, durability, interaction); `None`
  until audited (`WF_Deck_Audit.md`).
- `win_line` — cheapest documented kill line: `pieces` (+ `needs_cmdr: False` if
  commander-independent, `override: N` for X/mana-gated lethal, `fuzzy: True` for a
  combat/attrition estimate, `line` prose).
- `bottleneck` (FINDING|MANA|BOARD) + `min_lands`/`max_lands`/`hi_curve` + `mixed` note;
  `also` only if it is a genuinely two-line deck (union keep).

Row ORDER is load-bearing (it is the bake-off's column order) — append at the natural spot,
don't reshuffle. A *candidate/considering* build that is NOT joining the roster goes in
`EXTRA_COMMANDERS` instead (so `deck_sim` can still parse it), not in `DECKS`.

## Stage 4 — Harvest the clock into the gauntlet (`scripts/pod_gauntlet.py`)

Add a `CLOCKS["<slug>"]` entry with the curves — `grid` / `decap` / `table` / `med` / `never`
/ `sel` / `disrupt_class` / `score`. The `name` + `lab` must match the registry (a load-time
guard enforces it). Seed the arrays from your Stage 2 run, then make them authoritative:

```
python scripts/pod_gauntlet.py --refresh        # re-runs the labs -> analysis/pod_gauntlet_clocks.json
```

## Stage 5 — Re-flow the derived data

```
python scripts/keep_spec.py --write             # regenerates analysis/keep_specs.json card buckets
python scripts/kill_tree.py --all               # (only if you added a KILL_TREES spec) re-emit .mmd
```

A kill tree is optional: to draw one, add a `KILL_TREES["<display-slug>"]` spec (note the
display slug drops a leading "the-") with `reg_slug` pointing back at the `DECKS` row.

## Stage 6 — Scout it, then write it up

```
python scripts/report.py <slug>                 # the full cross-oracle / cross-framework card
```

- Add the Summary (`TPL_Deck_Summary.md` → `WF_Summary_Generation.md`); its Kill Window line
  must cite the lab (`Clock: Tx–y decap / Tz table (lab YYYY-MM-DD)`).
- Register in `Deck_Index.md` and update `Collection_Master_Status.md` if deployment changes.

## Stage 7 — Verify green

```
python scripts/validate.py        # 100 cards, ≤3 GC, citation EXISTS, filename unique
python scripts/clock_check.py     # the cited decap/table still MATCH the lab (0 DRIFT)
```

Both clean (pre-existing warnings aside) = the deck is fully wired into every tool.
