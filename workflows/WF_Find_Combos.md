# Workflow: Find Combos in a Decklist

Check a full decklist against Commander Spellbook's curated combo database — both
combos already complete in the deck and combos one card away (the actionable
buys). Use this when auditing a deck, evaluating a candidate, or hunting for the
purchase that unlocks a new line.

This complements, and does not replace, reading card text. Commander Spellbook
tells you a combo *exists* between named cards; you still confirm the line is
legal in the deck's identity and acceptable under the house rules before acting.

---

## Why this matters here

- **Infinite combos are pod-accepted** (`REF_Bracket_3_House_Rules.md`). Combo
  lines are evaluated on merit, so systematically finding them is now in-scope.
- **Don't cap a deck's combo lines for lack of cards** (same doc). The
  "almost-there" list *is* that check made concrete: it surfaces the single
  purchase that completes a combo, which feeds a measurable-improvement buy.

---

## Tool

`scripts/find_combos.py` — POSTs the decklist to
`https://backend.commanderspellbook.com/find-my-combos` and reports results.
Network access is required at runtime. Commander resolution reuses
`deck_registry` (the single source of truth); UB reskins are mapped to their
real names via `REF_Reskin_Aliases.md` before submission (CLAUDE.md hard rule —
otherwise Commander Spellbook silently fails to recognise the reskin).

```bash
python scripts/find_combos.py calamity              # fuzzy stem match (decks/ + considering/)
python scripts/find_combos.py decks/foo.txt         # explicit path
python scripts/find_combos.py glarb  --almost-max 2  # widen near-miss search to 2 cards away
python scripts/find_combos.py kefka  --almost-max 0  # complete combos only (suppress near-miss)
python scripts/find_combos.py rad    --changing      # also list "if you swapped commanders"
python scripts/find_combos.py rad    --json out.json # raw API results for further processing
```

---

## Steps

### 1. Run it against the `.txt`, not the summary

The decklist is ground truth. Confirm the printed header shows the right
commander and color identity; if it warns the commander wasn't in
`deck_registry`, it fell back to the Moxfield trailing-block convention — sanity
check the commander line before trusting the rest.

### 2. Read the three buckets

- **COMPLETE COMBOS IN DECK** — every named piece is present. These are real
  lines the deck can already assemble. Cross-check each against the deck's plan:
  a listed combo may be incidental (e.g. two flexible enablers that happen to
  loop) rather than a line you'd actually pursue.
- **ALMOST (missing ≤ N cards)** — the buys. Each entry lists what you `have`
  and what you `need`. Missing-exactly-1 is the highest-signal: one purchase
  completes the line. Decks with flexible enablers (Bloom Tender, Rite of
  Replication, Sol Ring) generate long near-miss lists — scan for the lines that
  fit the deck's plan, not every technically-valid loop.
- **IF YOU CHANGED COMMANDERS** (`--changing`) — usually noise for an existing
  build; useful when scouting a new commander for the same card pool.

### 3. Verify before acting

For any combo you intend to act on:

- **Read the card text** (`scripts/card_lookup.py`) — confirm the loop actually
  works and the payoff is real. Commander Spellbook is curated but the *fit* to
  your deck (mana, protection, redundancy) is yours to judge.
- **Check identity** — the tool reports the deck's color identity; a near-miss
  needing an out-of-identity card is not a legal buy.
- **Check availability + GC status** for any `need` card before recommending a
  buy: `deck_safe_collection.xlsx` / grep `decks/*.txt`
  (`feedback_card_availability_check`), and `REF_Game_Changers_List.md` (the
  3-GC cap still binds — a combo piece that is a GC counts).
- **Price the buy** only if it changes the decision, and flag it unverified
  unless freshly checked (`feedback_verify_prices`).

---

## Caveats

- **Names are the only input.** A card name Commander Spellbook doesn't
  recognise is dropped on their side with no error — reskin aliasing covers the
  known cases, but a typo or a very new card can cause a silent miss. The header
  reports how many cards were sent and which aliases were applied.
- **Not a rules engine.** It does not check whether you can *cast* the pieces,
  protect the line, or close before the pod does. Pair combo discovery with a
  clock lab (`WF_Kill_Window_Lab.md`) before claiming a kill turn.
- **The database evolves.** Re-run when the list changes; results are only as
  current as Commander Spellbook.
