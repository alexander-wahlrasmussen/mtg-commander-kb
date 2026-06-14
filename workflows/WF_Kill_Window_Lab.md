# Workflow: Kill-Window Clock Lab (verify one deck's claim)

Build a kill-turn goldfish clock for **one existing roster deck** and replace its
hand-estimated Kill Window with a lab-cited one. This is the per-deck unit of the
2026-06-13 verification sweep (`campaigns/Kill_Window_Lab_Sweep_2026-06-13.md` —
the tracker that says which deck is next and holds the running ranking).

Distinct from `WF_Candidate_Bakeoff.md` (choose one of many *un-built* candidates)
and `WF_Deck_Audit.md` (score an existing deck on the Conversion Check). This one
answers only **"what turn does the deck actually kill?"** for a deck already in the
roster, per the verification rule in `REF_The_Conversion_Check.md`.

Origin of the rule and the evidence it rests on: `campaigns/Framework_Clock_Gap_2026-06-09.md`
(5 hand-estimated windows falsified, all optimistic; score and clock uncorrelated
in the 15–19/20 band).

---

## Inputs

- The deck's `.txt` (ground truth) and `_Summary.md` (the claim to test).
- `scripts/speed_lab_core.py` — the shared harness. New labs import it; do **not**
  retrofit the 4 originals (lw/rc/er/gd) — they're committed evidence.
- `scripts/card_lookup.py`, local Scryfall data, `REF_Reskin_Aliases.md`.
- `scripts/clock_lab_template.py` — the canonical thin-lab skeleton to copy (or
  the closest existing lab, picked by kill shape — see Stage 1).

## Stage 0 — Read the kill, not the name

- `card_lookup.py` the commander **and every card named in a kill line** before
  modelling it. Card-text misreads are the #1 source of bad labs (a kill module
  encodes oracle text — get it wrong and the clock is fiction that looks rigorous).
- Resolve UB reskins via `REF_Reskin_Aliases.md` so the parser finds the cards.
- Write down the deck's actual kill **lines** (not "it wins with X") — each line is
  a branch the kill module checks, cheapest-first.

## Stage 1 — Pre-register the kill shape + a falsifiable prior

Classify the kill before running anything. The shape predicts the decap/table
pattern (validated 7-for-7 across the 2026-06-12 bake-off labs):

| Kill shape | decap vs table | Template lab |
|---|---|---|
| All-opponent simultaneous (pings / drains / symmetric burn) | **converge** (≈equal) | `gp_clock_lab.py`, `wb_clock_lab.py` |
| Combat focus-fire (attack one player) | **diverge 2–3 turns** | `er_speed_lab.py`, `rc_speed_lab.py` |
| On-cast / closed-loop combo (Thoracle-type, infinite) | **decap = table by construction** | `knn`/`kfx`/`kvd_clock_lab.py` |

State the prior as a number against the existing claim: *"claim is T6–8; combat
focus-fire so I expect decap ~T7–8, table ~T10; front edge suspect."* A prior is
not a result — it's what the lab is allowed to falsify. Every front edge measured
so far has come back optimistic, so distrust low front edges most.

**Producer inventory (only bites damage/body-race kills).** If the shape is combat
focus-fire or a go-wide/drain race — anything whose damage *scales with how many
bodies/counters/tokens you have* — list **every** token/producer/anthem/damage-
amplifier in the `.txt` before coding, and confirm each is modelled as a *producer*
(not cast as a vanilla beater contributing only its own stats). Omitting one always
biases the clock **slower** (it has happened ≥3× — lw/cs/cos), which in this sweep
means a **false negative on the decap-T≤7 pod bar**: the deck looks too slow and we
under-rate its race. Watch specifically for combat-damage doublers (double strike /
extra combats), per-ETB burn (Warstorm Surge class), and counter→token engines.
**Combo-assembly and `kill_all` shapes are exempt** — there one body/igniter is
enough and more don't help (Zero-Sum's loop, Radiation's rad-drain). The
2026-06-13 esc/rs re-check confirmed the asymmetry: singleton producers move only
the tail, not the median, so the risk is concentrated in body-race medians, not
combo clocks.

## Stage 2 — Build the kill module on the core

- New script `scripts/<abbr>_clock_lab.py` — copy `clock_lab_template.py`. Import
  `speed_lab_core as slc` and reuse the whole harness: `Goldfish`, `Table`,
  `run_goldfish` (the per-trial loop), `report_clock` (the decap/table block),
  `row/cum/median`, `run_cli`. Per-deck kill logic (the `Trial.turn()` branches)
  is the only deck-specific code — rewrite those branches and nothing else. A
  class-style deck plugs into `run_goldfish`; a lever/sweep lab keeps a kill
  *function* with kwargs and calls `report_clock` directly (see `lw_clock_lab.py`).
- `Table.kill_all()` for hit-all kills (decap=table); focus-fire one opponent and
  let `Table` track decap vs table separately for combat decks.
- Mana is a **lands + rocks floor** (plus ritual/temporary nets if the deck has
  them — see `godo_clock_lab.py`'s `burst`/`spend`). It is heuristic, not a rules
  engine: trust shapes and deltas, not second decimals.
- The lab is also a **decklist linter** — a parse error is usually a misspelt or
  nonexistent card in the `.txt`. Fix ground truth before trusting the clock.

## Stage 3 — Run, compare, judge

- 20 000+ trials, fixed seed (`SEED = YYYYMMDD`), dated. Print the cum-% T-grid
  plus **median decap, median table, never-in-12** (the reliability tail).
- Compare to the claim. State the direction of any correction and *why* (god-hand
  rounded into the range / two clocks conflated / mana-gated not availability-gated).
- Optional lever test (the `--mode b4`/lever pattern): does any single 2-card add
  move the median? Usually flat — report it so nobody re-litigates.

## Stage 4 — Write back (the deliverable)

1. **Summary Kill Window field** → the verification-rule format, replacing the
   `(unverified)` flag:
   `Clock: Tx–y decap / Tz table (lab YYYY-MM-DD, ` + "`<abbr>_clock_lab.py`)" + `· Through interaction: … (unverified — goldfish only)`
2. **A proposal write-up** `proposals/<Deck>_Clock_Lab_YYYY-MM-DD.md` (mirror
   `Genome_Project_Clock_Lab_2026-06-10.md`): claim, measured, direction, key
   findings, any card-text corrections, lever results. Add it to `proposals/README.md`
   Reference table (it's now a kill-window citation — **do not move it later**).
3. **`Deck_Index.md`** → append the clock annotation to the score:
   `NN/20 · Clock: Tx–y decap / Tz table (lab YYYY-MM-DD)`. Score is judged, clock
   is measured — report together, never merged.
4. **The sweep tracker** → flip the row to DONE, fill measured / delta / doc, and
   slot the deck into the running ranking.
5. **Commit** the script + docs (per `feedback_store_analysis_scripts` — labs with
   reuse value are committed, not throwaway `_tmp_` scripts).

## Do not

- Do not model a card from its name/art/memory — `card_lookup.py` first, every kill card.
- Do not report one number — decap and table are different clocks; state both.
- Do not trust a low front edge without the lab; it has an unbroken optimistic record.
- Do not retrofit lw/rc/er/gd_speed_lab.py — they're frozen evidence; build new on the core.
- Do not let a card-text error into a kill branch; a wrong branch makes a rigorous-looking false clock.
- Do not model a body/damage-race deck without inventorying its producers/amplifiers first (Stage 1) — an omitted producer silently biases the clock slow and under-rates the pod race.
