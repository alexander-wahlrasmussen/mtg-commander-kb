# Workflow: Deck Doctor

One-command, end-to-end **health check** for a single deck. Automates the mechanical
pre-flight that `WF_Deck_Audit.md` Step 1 ("Sanity check the list") does by hand, and
adds the two checks that have actually bitten us — a Commander **banlist** scan and a
**colour-identity** scan.

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
| legality | every card legal in Commander (banlist) | ERROR |
| colour identity | every card ⊆ the commander's identity | ERROR |
| Game Changers | ≤ 3, reskin-resolved | ERROR |
| unresolved names | every name resolves to oracle data | WARN |
| clock | cached lab decap/table medians + Summary `Clock:` drift | WARN |
| Conversion Check | the deck's CC score (reported, **not** computed) | INFO |

Exit code is `1` if any ERROR, `2` if the deck can't be resolved, else `0`.

The legality + colour scans resolve **reskin aliases** (`Morgul-Knife` → `Shadowspear`)
and a leading-`The` mismatch (`Wise Mothman` → `The Wise Mothman`) before lookup, and
skip non-playable Scryfall layouts (`art_series` etc.) so a "Farseek // Farseek" art card
can't shadow the real, legal Farseek.

---

## How it relates to the other tools

- **`validate.py`** lints the *whole repo* (size, GC, filename collisions, clock-citation
  exists). Deck Doctor goes *deep on one deck* and adds the banlist + colour scans validate
  doesn't do. Run validate before a commit sweep; run Deck Doctor on the deck you're editing.
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
- As the first step of `WF_Deck_Audit.md`.

See also: `WF_Deck_Audit.md`, `WF_GC_Verification.md`, `WF_Kill_Window_Lab.md`.
