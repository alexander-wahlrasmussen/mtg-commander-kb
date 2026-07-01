# Workflow: Game Logging

The capture end of the **Layer-C** loop — turning real pod games into the ground truth that
`calibrate.py` grades the whole simulation tower against (`*_clock_lab.py`, `pod_gauntlet.py`,
`self_meta_lab.py`, the `tier_list.py` synthesis). Every lab has falsified a *hand-estimate*;
nothing has yet checked the **labs themselves** against reality. That check needs games in
`analysis/game_results.jsonl`, and today it holds **0**. The whole point of this workflow is to
make logging a game cost seconds, so the loop actually gets fed.

The bottleneck was never capability (`game_log.py` + `calibrate.py` are built and tested) — it
was **friction at capture** (details go fuzzy before you're back at the desk) and **no payoff on
game #1** (`calibrate` needs n≥3/deck before it computes anything). This workflow closes both.

---

## 1. At the table — jot the pocket scorecard

Five fields, on a phone note or a scrap of paper, the moment the game ends (before the numbers
fade). Everything else is optional colour.

```
my deck   :  <which of my decks>
result    :  W / L
end turn  :  T__     (turn the game ENDED — the table clock, win or lose)
first KO  :  T__     (turn the FIRST player was knocked out — the decap clock)
won by / winner : combo | combat-decap | table-drain | concede   /  <deck that won if not me>
```

`end turn` and `first KO` are the two numbers the labs are graded on — get those even if you
skip the rest.

## 2. At the desk — one line in

The fastest path is `quick`: type the scorecard as a single string. `|` separates seats,
`#` starts a note.

```bash
python scripts/game_log.py quick "genome W T9 d8 combo | ur_dragon L | kinnan L"
python scripts/game_log.py quick "grand_design L T11 d9 | ur_dragon W # raced, folded to wrath"
python scripts/game_log.py quick "genome W T7 combo | ur_dragon L" --dry-run   # parse + grade, write nothing
```

Grammar of the first (your) segment:

```
<mydeck>  W|L  T<end>  [d<decap>]  [wintype]
```

- `<mydeck>` — a prefix is enough (`genome` → `genome_project`); ambiguous prefixes are rejected with the matches.
- `W`/`L` — did **you** win.
- `T<n>` — the turn the game ENDED (required; it's the table clock either way).
- `d<n>` — first decap turn (optional but it's half the calibration signal — include it).
- `wintype` — `combo` | `combat-decap` | `table-drain` | `concede` | `other`.

Each later `| <opp> [W|L]` segment is an opponent seat; mark the winner with `W` when you lost.
Per-seat KO turns and disruption events (counters, Abolisher) don't fit the one-liner — use the
richer doors below for those.

**Other doors** (same record, more detail):

```bash
python scripts/game_log.py log                     # guided prompts — nothing to remember
python scripts/game_log.py add --from-json game.json   # full record incl. disruption[] / per-seat ko
```

## 3. The instant payoff

Every append prints a **grade card**: how *this* game's clocks compared to the lab median for
your deck, from game one.

```
── this game vs the lab ──────────────────────────────
  The Genome Project — 1 game(s) logged for this deck.
  table close  T9  vs lab median  T8  → lab ran 1 turn FAST this game
  first decap  T8  vs lab median  T7  → lab ran 1 turn FAST this game
  one game is an anecdote — calibrate.py needs n≥3 for this deck (2 to go; ~5 for a stable rank).
```

Read the sign as: **FAST** = the lab was optimistic (you were slower than it predicted);
**SLOW** = the lab was pessimistic (you closed faster). One game is an anecdote — it's the
*trend* over games that grades the lab.

## 4. When the games add up — grade the tower

```bash
python scripts/game_log.py summary        # per-deck W/L + avg clocks (the proto-oracle)
python scripts/calibrate.py               # observed clocks/win% vs the labs (MAE + Spearman)
python scripts/calibrate.py --power       # how many games/deck until reality can adjudicate (needs NO games)
```

`--power` (no games needed) sets the target: **~5 games/deck (~80 total)** recovers the predicted
ranking ≥80% of the time. Below that the REAL column is small-sample noise. So the concrete ask is
"log ~5 per deck," not "log a couple and trust it."

---

## Hard rules

- **`analysis/game_results.jsonl` is append-only** — the dated records ARE the log; never rewrite
  history. It is committed (hand-entered ground truth), unlike the generated `sim_results.json`.
- **`mine` must be an active-roster slug** (derived from `deck_registry`) — that's what pins the
  record to a lab for back-testing. Opponents' decks may use any slug. `quick`/`log`/`add` all
  enforce this before writing.
- **Don't invent numbers you didn't observe.** A missing decap turn is fine (leave it out); a
  guessed one poisons the calibration. Same discipline as the kill-window cite-a-lab rule, applied
  to reality this time.

See also: `scripts/game_log.py` (capture), `scripts/calibrate.py` (grading), and Backlog #10 for
the Layer-C frontier this feeds.
