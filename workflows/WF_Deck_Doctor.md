# Workflow: Deck Doctor

One-command, end-to-end **health check** for a single deck. Automates the mechanical
pre-flight that `WF_Deck_Audit.md` Step 1 ("Sanity check the list") does by hand, and
adds the checks that have actually bitten us — a Commander **banlist** scan, a
**colour-identity** scan, the **singleton rule**, and a **buildability** (own / buy-list
/ €) read. `--all` runs the same checks over the whole roster as a PASS/WARN/FAIL table.

Run this BEFORE a Conversion Check audit, after any swap, and before committing a
decklist change. It is read-only and exits non-zero on a hard failure, so it is also
safe as a pre-commit gate.

---

## Command

```bash
python scripts/deck_doctor.py <deck>            # roster slug, stem, candidate name, or a .txt path
python scripts/deck_doctor.py radiation-sickness
python scripts/deck_doctor.py planned-obsolescence          # a decks/considering/ candidate
python scripts/deck_doctor.py grand-design --run-lab        # also run the clock lab live
python scripts/deck_doctor.py planned-obsolescence --run-lab --lab urza_clock_lab:clock
python scripts/deck_doctor.py --all                         # roster PASS/WARN/FAIL dashboard
python scripts/deck_doctor.py --all --candidates            # + the considering/ candidates
python scripts/deck_doctor.py --diff OLD.txt NEW.txt        # swap inspector (did it stay legal?)
python scripts/deck_doctor.py <deck> --no-build             # skip the ownership/buy-cost check
```

The deck argument is flexible: a registry slug (`radiation_sickness`), a decklist stem
(`the-grand-design`), a candidate name (`planned-obsolescence`), a fuzzy display name
(`grand design`), or a path to any `.txt`.

> Commander identity is resolved from the **filename stem**, not by reading the list
> (deck_sim's design). A decklist with an unrecognised filename will WARN "commander not
> recognised" and skip the size + colour-identity checks. Keep the `<deck-kebab>-YYYYMMDD`
> naming and this resolves automatically.

---

## What it checks

| Section | Rule | Severity |
|---|---|---|
| size | exactly 100 (99 + commander) | ERROR |
| singleton | ≤ 1 copy per non-basic (honours "any number" / "up to N" cards) | ERROR |
| legality | every card legal in Commander (banlist) | ERROR |
| colour identity | every card ⊆ the commander's identity | ERROR |
| Game Changers | ≤ 3, reskin-resolved | ERROR |
| unresolved names | every name resolves to oracle data | WARN |
| buildability | own N of 100 (real + proxy), buy list + indicative € | INFO |
| bracket / house rules | mass land denial (house-banned); extra-turn chains; WotC bracket estimate | **ERROR** (MLD) / WARN / INFO |
| consistency vitals `--vitals` | keepable hand % + ramp/draw count-by-turn vs BDD anchors | OK/WARN |
| combos `--combos` | intended kill line present? + CSB combo DB; repeatable extra-turn = banned | **ERROR** / INFO |
| clock | cached lab decap/table medians + Summary `Clock:` drift | WARN |
| Conversion Check | the deck's CC score (reported, **not** computed) | INFO |

Exit code is `1` if any ERROR, `2` if the deck can't be resolved, else `0`. `--vitals`,
`--combos` are opt-in (the MC sim is ~5 s; the combo DB needs network); `--deep` turns both
on. `--all` does **not** run them (kept fast) — its `brk` column is the GC-only bracket read.

The **singleton** check counts the MAIN deck only (it derives quantities from
`deck_sim.parse_deck`, which excludes the `SIDEBOARD:` block — re-reading the raw `.txt`
would wrongly fold sideboard lines in). Basics are exempt; so are cards whose own oracle
text grants it — "any number of cards named …" (Relentless Rats, Dragon's Approach,
Shadowborn Apostle) and "up to N cards named …" (Nazgûl 9, Seven Dwarves 7), with the
stated limit enforced.

The **buildability** check joins each card to the latest `collection/moxfield_haves_*.csv`
on the **oracle canonical name** (so a reskin or a `The`-prefix variance still matches),
counts real **+ proxy** copies, treats basics as owned, and prices the shortfall from the
local Scryfall bulk. Prices are **indicative and dated** — not quotes (REF: verify-prices).
Whether an *owned* copy is free or **locked in another deck** is left to
`availability_check.py` / `unlock_optimizer.py` (pointed to, not re-derived here).

The legality + colour scans resolve **reskin aliases** (`Morgul-Knife` → `Shadowspear`)
and a leading-`The` mismatch (`Wise Mothman` → `The Wise Mothman`) before lookup, and
skip non-playable Scryfall layouts (`art_series` etc.) so a "Farseek // Farseek" art card
can't shadow the real, legal Farseek.

### `--all` batch dashboard

`--all` runs the **same checks** in quiet mode over every roster deck (`--candidates` adds
`decks/considering/`) and prints one row each: `size · sing · ill · off · GC · owned/100 ·
buy €`. A `·` is all-clear; any digit in `sing`/`ill`/`off` is a problem; size `!=100` is
prefixed `!`; a `+` on the buy-€ flags that some cards in the list are unpriced. FAIL/WARN
rows float to the top within each group. Drill into any flagged deck with the single-deck
command. Exit `1` if any deck FAILs.

### Bracket / house rules (default)

Estimates the WotC bracket from local signals — Game Changer count, **mass land denial**,
fast-mana density, extra-turn count, and (with `--combos`) 2-card infinites — and enforces
the pod's house rules from `REF_Bracket_3_House_Rules.md`: **MLD is an ERROR** (hard
exclusion), more than one extra-turn effect is a WARN (allowance is 0–1, no chains), and
infinite combos are pod-accepted (since 2026-06-19) so they're reported, not penalised. The
estimate is a heuristic, not a verdict; the pod runs "B3-by-GC / B4-in-spirit".

### Consistency vitals (`--vitals`)

Chains `deck_sim`'s Monte Carlo: keepable opening-hand % (land-count heuristic, fixed seed)
plus ramp/draw **count-by-turn** measured against the BDD anchors (~12 ramp by T3, ~8 draw
by T6). It's a *consistency* read, not a power grade — it informs **how** to build
(redundancy, bottleneck), per [[feedback_mulligan_is_deckbuilding_input]].

### Combo audit (`--combos`)

Two checks: (1) network-free — is the registry's intended `win_line` actually present in the
list? (2) `find_combos.query_deck` asks Commander Spellbook for **complete** combos and
**one-away** buys. A combo producing repeatable **extra turns** is an ERROR (house-banned);
all other infinites are reported as pod-accepted. Degrades to a WARN if CSB is unreachable.

### `--diff OLD.txt NEW.txt` swap inspector

Compares two dated versions and answers **"did this swap stay legal?"**. Prints the cards
**out** and **in** (added cards annotated `[GC]` / `[off-colour {X}]` / `[BANNED]`), then a
**boundary check** read off the same quiet-doctor facts for each version: `size`, `Game
Changers`, `singleton`, `illegal`, `off-colour`, each shown `old -> new` and flagged when a
limit is `NEWLY` crossed (or `fixed`). The **verdict** line is `OLD-tag -> NEW-tag`; exit
`1` if the swap crossed any boundary. Card matching is canon-keyed, so a reskin printed
differently across versions isn't mistaken for a swap; a commander change is called out as
"more than a swap". **Clock movement is NOT inferred** from two static lists (the cached
medians are per-slug, shared by both files) — the tool prints the `--run-lab` command to
measure it, per the kill-window-needs-a-lab rule.

---

## How it relates to the other tools

- **`validate.py`** lints the *whole repo* (size, GC, filename collisions, clock-citation
  exists). Deck Doctor goes *deep on one deck* and adds the singleton + banlist + colour +
  buildability scans validate doesn't do. Run validate before a commit sweep; run Deck
  Doctor on the deck you're editing (or `--all` for the whole roster at audit altitude).
- **`unlock_optimizer.py` / `availability_check.py`** own the *cross-deck contention*
  question (is a copy free or double-booked across decks?). Deck Doctor's buildability
  answers the *single-deck* question (do I physically own the 100, what's the buy list)
  by reusing `unlock_optimizer.load_owned`; it points to those two for contention.
- **`deck_sim.py`** is the MC engine `--vitals` chains (`simulate` / `need_source_set` /
  `simulate_need`) — Deck Doctor runs a quick 8k-trial read; run `deck_sim.py` directly for
  the full table, more turns, or `--need tutor/interaction/protection`.
- **`find_combos.py`** is the Commander Spellbook client `--combos` chains (via the reusable
  `query_deck`). Run it directly for the full combo list, near-misses, or `--changing`.
- **`clock_check.py`** is reused verbatim for the Summary `Clock:` drift line — Deck Doctor
  reports the same verdict for one deck. Refresh the medians first with
  `python scripts/pod_gauntlet.py --refresh` if a lab changed.
- **`WF_Deck_Audit.md`** is the human Conversion Check scoring that comes *after* a clean
  Deck Doctor pass. Deck Doctor surfaces the CC datum but never grades it — the 20-point
  score is judged by hand.
- **`pod_gauntlet.py`** gives `P(beat the pod)` — printed as a next-step, not run inline
  (per-deck extraction from the whole-pod race is left to the operator).

---

## When to use

- After **any** card swap (catches the off-colour / banned / GC-over-cap class of error).
- Before writing a new dated `.txt` (the size + legality gate).
- On a `decks/considering/` candidate before promoting it (add `--run-lab --lab mod:mode`
  to clock it in the same pass).
- After writing a new dated `.txt`, run `--diff <old> <new>` to confirm the swap stayed
  within every legality boundary (and re-lab if the clock could have moved).
- `--all` at audit altitude to spot any roster deck that has drifted out of legality.
- As the first step of `WF_Deck_Audit.md`.

See also: `WF_Deck_Audit.md`, `WF_GC_Verification.md`, `WF_Kill_Window_Lab.md`.
