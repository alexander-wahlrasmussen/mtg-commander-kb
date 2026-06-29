#!/usr/bin/env python3
"""gd_ramp_lab.py — The Grand Design (Atraxa) mana-AVAILABILITY lab.

Companion to the ramp-composition read (ramp_audit.py) and the consistency floor
(deck_sim --need ramp). Those answer "is ramp present / castable?". This answers
the AVAILABILITY question the user asked: WHEN does the deck reach the mana it
actually needs, and would ADDING cheap ramp shift that curve left?

The deck's mana-gated payoffs:
  7 mana = hardcast Atraxa (7) / Finale of Devastation for a lethal X / Chord big
  8 mana = Craterhoof Behemoth (the labbed finisher fix) hardcast

So the relevant availability curve is P(reach K mana by turn T), K in {7,8}. The
reanimator suite (Reanimate/Animate Dead/Necromancy/Persist/Dread Return/Living
Death) deliberately CHEATS the mana cost — that line bypasses ramp entirely, so it
is NOT what ramp accelerates and is out of scope here (measured separately in
gd_speed_lab mode_reanim). This lab isolates the hardcast clock ramp DOES move.

Goldfish, land-only-floor + modelled ramp. Each ramp source verified via
card_lookup 2026-06-24 (text + cmc); all net +1 mana/land:
  rocks/dorks (repeatable, tap same turn — lab convention, ~1T generous for dorks):
    Sol Ring {1}->2, Arcane Signet {2}->1, Coalition Relic {3}->1 (charge ignored,
    conservative), Birds {G}->1, Bloom Tender {1G}->1 (Vivid >=2 later — conservative
    floor of 1), Fanatic of Rhonas {1G}->1 ({G}; ferocious {G}{G}{G}{G} ignored).
  land-ramp (one-shot, +1 land tapped -> no same-turn mana): Farseek/Nature's Lore/
    Three Visits {1G}, Sakura-Tribe Elder {1G} (sac self), Kodama's Reach {2G} (+1
    to play, the 2nd basic to hand modelled as the immediate +1 net), Springbloom
    Druid {2G} (sac a land, fetch 2 = net +1), Solemn Simulacrum {4} (+1).

A/B rows pure-ADD cheap rocks (UPPER bound: free, no cut) to test the lever. If even
+4 fast rocks barely moves the K=7/K=8 median, ramp availability is saturated and
adding ramp does not accelerate the deck — spend the slots on the labbed bottleneck
(finisher / draw / protection) instead.

HEURISTIC, not a rules engine. Trust the DELTA vs baseline, not the second decimal.
"""
import importlib.util
import random
from pathlib import Path

_spec = importlib.util.spec_from_file_location(
    "speed_lab_core", Path(__file__).parent / "speed_lab_core.py")
core = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(core)
ds = core.ds

ROOT = Path(__file__).parent.parent
DECK = ROOT / "decks" / "the-grand-design-20260623.txt"
SEED = 12345
TURNS = 10
SHOW = [3, 4, 5, 6, 7, 8, 10]

# repeatable mana (rocks + dorks) -> (cost, output); deployed greedy cheapest-first
ROCKS = {"Sol Ring": (1, 2), "Arcane Signet": (2, 1), "Coalition Relic": (3, 1),
         "Birds of Paradise": (1, 1), "Bloom Tender": (2, 1),
         "Fanatic of Rhonas": (2, 1)}
# one-shot land-ramp -> cost (each nets +1 land, enters tapped)
LAND_RAMP = {"Farseek": 2, "Nature's Lore": 2, "Three Visits": 2,
             "Sakura-Tribe Elder": 2, "Kodama's Reach": 3, "Springbloom Druid": 3,
             "Solemn Simulacrum": 4}
# cheap fast rocks for the counterfactual (all colourless-castable in WUBG)
FAST_ADD = {"Mind Stone": (2, 1), "Fellwar Stone": (2, 1),
            "Prismatic Lens": (2, 1), "Talisman of Dominance": (2, 1)}


def reach_turns(library, rng, rocks):
    """One trial. Returns (turn_reached_7, turn_reached_8); None if not in horizon."""
    g = core.Goldfish(library, rng, rocks=rocks)
    t7 = t8 = None
    for T in range(1, TURNS + 1):
        g.begin_turn(T)
        # one-shot land-ramp: cast cheapest-first, each +1 land (tapped)
        moved = True
        while moved:
            moved = False
            for nm, cost in sorted(LAND_RAMP.items(), key=lambda x: x[1]):
                if g.has(nm) and g.avail >= cost:
                    g.cast(nm, cost)        # cast() already pays the cost (avail -= cost)
                    g.lands += 1            # fetched land enters TAPPED: no same-turn
                    # mana, untaps next turn via begin_turn's lands+rocks floor. Do NOT
                    # reset avail to lands+rock_out here — that refunded the spell's cost
                    # AND counted the tapped land this turn (land-ramp chained for free).
                    moved = True
                    break
        g.deploy_rocks()
        if t7 is None and g.avail >= 7:
            t7 = T
        if t8 is None and g.avail >= 8:
            t8 = T
    return t7, t8


def main():
    index = ds.load_oracle_index()
    aliases = ds.load_reskin_aliases()
    trials = 20000
    print(f"\n### GD RAMP AVAILABILITY — P(reach K mana by turn T)   trials={trials} seed={SEED}")
    print("    K=7 = hardcast Atraxa / Finale / Chord big ;  K=8 = Craterhoof.")
    print("    Reanimator line cheats mana (bypasses ramp) -> out of scope, see gd_speed_lab.\n")
    base, _ = core.load_parsed(DECK, index, aliases)
    add2 = ["Mind Stone", "Fellwar Stone"]
    add4 = add2 + ["Prismatic Lens", "Talisman of Dominance"]
    rocks2 = {**ROCKS, **{k: FAST_ADD[k] for k in add2}}
    rocks4 = {**ROCKS, **FAST_ADD}
    variants = [
        ("baseline (as published)", base, ROCKS),
        ("+2 fast rocks (101 cards)", core.build_lib(base, index, [], add2), rocks2),
        ("+4 fast rocks (103 cards)", core.build_lib(base, index, [], add4), rocks4),
    ]
    for K, idx in ((7, 0), (8, 1)):
        print(f"  -- K={K} mana --")
        print("  build".ljust(34) + "".join(f"{t:>6}" for t in SHOW) + "   median")
        for tag, lib, rocks in variants:
            rng = random.Random(SEED)
            res = [reach_turns(lib, rng, rocks) for _ in range(trials)]
            print(core.row(tag, core.cum(res, idx, SHOW), SHOW, width=32)
                  + f"   {core.median(res, idx)}")
        print()
    print("  Read the DELTA vs baseline. Flat curves => ramp availability is saturated;")
    print("  adding ramp does not pull the hardcast clock (spend slots on finisher/draw).")


if __name__ == "__main__":
    main()
