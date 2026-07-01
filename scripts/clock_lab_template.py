#!/usr/bin/env python3
"""clock_lab_template.py — copy me to start a new <deck> KILL-TURN goldfish.

THE THIN PATTERN. A clock lab is just three things:
  1. a short spec (DECK / SEED / TURNS / SHOW / ROCKS),
  2. a bespoke `Trial` class that owns THIS deck's kill logic, and
  3. a 3-line main.
Everything that used to be copy-pasted into every lab — the per-trial turn loop,
the decap/table report block, the --mode/--trials CLI — now lives in
speed_lab_core.py (run_goldfish / report_clock / run_cli). Do NOT re-implement
those here; that duplication is exactly what this template removes. Only the
`Trial` class should differ lab-to-lab.

HOW TO USE
  1. FIRST confirm the deck's KILL SHAPE before you model it: run
     `python scripts/find_combos.py <deck>` (+ read the commander's ability) and decide
     combo vs voltron vs drain vs go-wide from THAT, not from the card mix. A voltron-
     looking aura deck can be an infinite-combo deck — verified card text does NOT save
     you from modelling the wrong archetype (see feedback: verify the kill shape before
     labbing; Cass 2026-07-01). Model the kill you actually find.
  2. Copy to scripts/<xx>_clock_lab.py and rewrite this docstring: name each kill
     line and cite card_lookup.py for every card text you encode (CLAUDE.md hard
     rule — read the card before modelling it; proposals/labs are not exempt).
     State what is OPTIMISTIC and what is OMITTED, like the existing labs do.
  3. Point DECK at the .txt; set SEED / TURNS / SHOW; list the deck's mana ROCKS.
  4. Put this deck's real kill model in Trial.turn(). That is the only part that
     should vary between labs.
  5. Run:  python scripts/<xx>_clock_lab.py --trials 40000
     (add --deck PATH|stem to run the same model against a variant list — see
     run_cli; a mode gets the override by declaring a `deck=None` parameter.)

Mana is a lands+rocks floor, damage is unblocked, and the output is an
availability / ceiling curve — not a rules engine. Trust shapes and deltas, not
second decimals. decap and table are different clocks; report both (the
verification rule). For a lab that needs lever/sweep modes (chip rates, A/B
swaps), add more functions to the run_cli dict and keep a kill *function* with
kwargs instead of a class — see lw_clock_lab.py.

Data: collection/oracle-cards.json (refresh via update_scryfall_data.py)
"""
import importlib.util
import random
from pathlib import Path

ROOT = Path(__file__).parent.parent
_spec = importlib.util.spec_from_file_location(
    "speed_lab_core", Path(__file__).parent / "speed_lab_core.py")
slc = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(slc)
ds = slc.ds

# --- spec ------------------------------------------------------------------
DECK = ROOT / "decks" / "considering" / "REPLACE-ME.txt"
SEED = 20260614
TURNS = 14
SHOW = [5, 6, 7, 8, 9, 10, 12, 14]

# name -> (cost, mana_output). Repeating rocks (Mana Vault untap tax ignored)
# are the documented optimism every lab shares.
ROCKS = {"Sol Ring": (1, 2), "Arcane Signet": (2, 1)}


# --- bespoke kill model (THE ONLY PART THAT VARIES PER DECK) ----------------
class Trial:
    """One goldfish game; owns this deck's combo/damage logic.

    Contract required by slc.run_goldfish:
      * expose .tbl       — an slc.Table() (the decap/table tracker)
      * expose .turn(T)   — advance one turn, dealing damage when the kill fires
    run_goldfish ends the game once self.tbl.done.
    """

    def __init__(self, library, rng):
        self.g = slc.Goldfish(library, rng, rocks=ROCKS)
        self.tbl = slc.Table()
        self.combo = set()          # <-- replace with this deck's real board state

    def turn(self, T):
        g = self.g
        g.begin_turn(T)             # draw (after T1) + land drop (pure lands first)
        g.deploy_rocks()            # cheapest-first mana rocks; new output taps now
        # Deploy the commander / pieces / tutors using the Goldfish primitives:
        #   g.has(name) · g.cast(name, cost) · g.fetch(name) · g.draw(k) · g.avail
        # then check the win condition and deal damage through self.tbl:
        #   self.tbl.kill_all(T)          # overwhelm/infinite -> decap == table
        #   self.tbl.hit_focus(power, T)  # combat focus-fire  -> decap leads table
        #   self.tbl.hit_all(x, T)        # symmetric drain    -> decap == table
        raise NotImplementedError("fill in this deck's kill model, then delete me")


def mode_clock(index, aliases, trials):
    print(f"\n### CLOCK — <Deck> kill-turn goldfish   trials={trials} seed={SEED}")
    rng = random.Random(SEED)
    library, commander = slc.load_parsed(DECK, index, aliases)
    print(f"  library {len(library)} + commander {commander}")
    res = slc.run_goldfish(lambda: Trial(library, rng), trials, TURNS)
    # single=True when decap == table by construction (overwhelm / hit-all kill);
    # leave it off for combat decks where the two clocks diverge.
    slc.report_clock(res, SHOW, TURNS, trials)
    print("\n  Summary claim: '<Tx-y>'. The cum % rows above are the test.")


if __name__ == "__main__":
    slc.run_cli(__doc__, {"clock": mode_clock}, default_trials=40000)
