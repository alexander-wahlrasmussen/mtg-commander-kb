#!/usr/bin/env python3
"""wb_storm_lab.py — Zero-Sum Game LINE B (affinity magecraft storm) clock.

The combo lab (wb_clock_lab.py) measures the lifeloop (T9) and OMITS Line B. This
lab models that omitted second axis — the one Witherbloom's spell-affinity uniquely
powers — to answer: "does the affinity-spell plan stand on its own, and does adding
a redundant payoff (Professor Onyx) make it a real loop-independent win condition?"

THE LINE IS AN INFINITE (corrected 2026-06-19 — an earlier version of this lab
wrongly modelled it as a finite drip and concluded "never closes"; that was a
modelling error, not a property of the deck). Pieces card_lookup-verified:
  Witherbloom, the Balancer: instants/sorceries have affinity for creatures
    (generic cost -1 per creature).
  Sprout Swarm {1}{G}, Convoke, Buyback {3}, makes a 1/1 GREEN Saproling. With
    >=4 creatures, affinity zeroes the {1}+{3}=4 generic -> cost {G}; convoke taps
    ONE green creature to pay it; the Saproling it makes is a fresh untapped green
    body to tap next cast. => INFINITE casts, each an instant cast.
  Payoff (each cast drains the WHOLE table): Witherbloom Apprentice (each opp -1,
    the deck's ONLY one) or Professor Onyx (BUY; each opp -2). Either makes the
    infinite lethal. Onyx is REDUNDANCY for the payoff slot, not required.
  => the deck ALREADY contains this 2nd infinite (commander-DEPENDENT, unlike the
    lifeloop). It fires the turn {Witherbloom + a payoff + Sprout Swarm castable +
    board>=4 with a green source} all come together. kill_all on assembly.

This ISOLATES Line B (lifeloop assumed unavailable — the resilience scenario). The
A/B is Apprentice-only vs +Professor Onyx (does the redundant payoff close more
games / sooner?). OPTIMISTIC: unblocked/uninteracted, colour-blind mana floor,
rocks tap same turn. Trust shapes and the A/B gap, not second decimals.

Data: collection/oracle-cards.json    Run: python scripts/wb_storm_lab.py
"""
import importlib.util
import random
from pathlib import Path

ROOT = Path(__file__).parent.parent
_spec = importlib.util.spec_from_file_location(
    "speed_lab_core", Path(__file__).parent / "speed_lab_core.py")
slc = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(slc)
ds = slc.ds

DECK = ROOT / "decks" / "zero-sum-game-20260707.txt"
SEED = 20260619
TURNS = 14
SHOW = [4, 5, 6, 7, 8, 9, 10, 12]
ROCKS = {"Sol Ring": (1, 2), "Arcane Signet": (2, 1), "Jet Medallion": (2, 1)}
DORKS = {"Birds of Paradise", "Llanowar Elves", "Elvish Mystic", "Fyndhorn Elves",
         "Boreal Druid", "Arbor Elf", "Elves of Deep Shadow", "Delighted Halfling"}
TOKEN_MAKERS = {"Bitterblossom": False, "Tendershoot Dryad": True,   # name -> makes GREEN
                "Saproling Migration": True, "Hornet Queen": True, "Sprout Swarm": True}
ANY_TUTORS = {"Demonic Tutor": 2, "Beseech the Queen": 3, "Increasing Ambition": 5,
              "Dark Petition": 3, "Diabolic Intent": 2}    # fetch to hand (generic shrinks)
CREATURE_TUTORS = {"Chord of Calling", "Finale of Devastation", "Nature's Rhythm"}


def run(library, trials, payoffs, label):
    """payoffs: list of magecraft-drain payoff names available in this variant.
    Line B is an INFINITE: fires when {commander + a payoff in play + Sprout Swarm
    castable + board>=4 with a green source}. kill_all on assembly."""
    rng = random.Random(SEED)
    out = []
    for _ in range(trials):
        g = slc.Goldfish(library, rng, rocks=ROCKS)
        tbl = slc.Table()
        board = 0; green = 0; dork_out = 0; cmdr = False
        payoff_in = False
        for T in range(1, TURNS + 1):
            g.begin_turn(T); g.deploy_rocks(); g.add_mana(dork_out)
            prog = True
            while prog:
                prog = False
                for nm in DORKS:
                    if g.has(nm) and g.cast(nm, 1):
                        board += 1; green += 1; dork_out += 1; prog = True
                for nm, is_green in TOKEN_MAKERS.items():
                    if nm == "Sprout Swarm":
                        continue                         # held as the engine, not pre-cast
                    if g.has(nm) and g.cast(nm):
                        board += 2; green += (2 if is_green else 0); prog = True
                if not cmdr:
                    c = max(2, 8 - board)                 # affinity floor {B}{G}
                    if g.avail >= c:
                        g.pay(c); cmdr = True; board += 1; green += 1; prog = True
                for nm in payoffs:                        # Apprentice (2) / Onyx (6)
                    cost = 2 if nm == "Witherbloom Apprentice" else 6
                    if not payoff_in and g.has(nm) and g.cast(nm, cost):
                        payoff_in = True; board += 1; prog = True
                # tutor for the missing piece: Sprout Swarm first, else a payoff
                if not g.has("Sprout Swarm"):
                    for tnm, base in ANY_TUTORS.items():
                        red = min(base, board) if cmdr else 0
                        if g.has(tnm) and g.cast(tnm, max(1, base - red)):
                            g.fetch("Sprout Swarm"); prog = True; break
                if not payoff_in:
                    for tnm in CREATURE_TUTORS:
                        if g.has(tnm) and g.cast(tnm, max(2, 2 + 2 - min(2, board))):
                            if g.fetch("Witherbloom Apprentice"):
                                payoff_in = True; board += 1
                            prog = True; break
            # assembly check: Sprout Swarm in hand, board>=4, a green source, +1 mana
            sprout_ready = g.has("Sprout Swarm") and board >= 4 and green >= 1
            if cmdr and payoff_in and sprout_ready:
                tbl.kill_all(T)
            if tbl.done:
                break
        out.append((tbl.decap, tbl.table))
    print(slc.row(f"{label}", slc.cum(out, 1, SHOW), SHOW)
          + f"   med {slc.median(out, 1)} · never {slc.never_pct(out, 1, trials):.0f}%")


def mode_storm(index, aliases, trials):
    # 2026-06-19: Professor Onyx is now IN the .txt, so the A/B inverts — the
    # "pre-Onyx" baseline removes it (adds Beast Within back as filler).
    base, _ = slc.load_parsed(DECK, index, aliases, warn=False)
    no_onyx = slc.build_lib(base, index, ["Professor Onyx"], ["Beast Within"])
    print("=" * 78)
    print(f"LINE B (Sprout Swarm INFINITE) — loop-independent clock   {trials} trials")
    print("  table-kill (decap==table) cum % by turn:".ljust(46) + "".join(f"{t:6d}" for t in SHOW))
    run(no_onyx, trials, ["Witherbloom Apprentice"], "pre-Onyx (Apprentice only)")
    run(base, trials, ["Witherbloom Apprentice", "Professor Onyx"], "as-built (+ Onyx)")
    print("\n  Fires on assembly (infinite). A/B = does a redundant payoff close more games?\n"
          "  Compare to the lifeloop's T9. Loop assumed unavailable (resilience scenario).")


if __name__ == "__main__":
    slc.run_cli(__doc__, {"storm": mode_storm}, default_trials=20000)
