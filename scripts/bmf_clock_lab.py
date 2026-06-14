#!/usr/bin/env python3
"""bmf_clock_lab.py — Ms. Bumbleflower (This Bunny Goes to Market) KILL-TURN goldfish.

Kill-Window Lab Sweep, deck 9 (proposals/Kill_Window_Lab_Sweep_2026-06-13.md).
Summary claims "Goldfish T8-10". Built on speed_lab_core.py. Commander mana-gated.

KILL SHAPE — COMBAT focus-fire (diverge). All three of the deck's lines are combat
and slow (the Summary's own defining weakness: "out-values the table long before it
out-damages it"). Per the carried prior: predict decap off the focused combat axis,
table ~2-3 later.

  JOLRAEL  (primary)   {4}{G}{G}: creatures you control have base P/T X/X, X = cards
                       in hand. With the draw engine's full hand + a wide board (Cats
                       + payoffs), an X/X alpha. Focus-fires one player -> decap leads.
  COUNTER-BEATS        Bumbleflower puts a +1/+1 counter (and flying) on a creature
                       per spell cast; pile them on a threat. Slow, single-carrier.
  WILLBREAKER theft    aim the counter at an opponent's creature to steal it. GOLDFISH-
                       INVISIBLE (dummies have no creatures) — like CT's oppression, the
                       goldfish cannot credit this line; noted, not modelled.

Engine, oracle-verified (card_lookup.py 2026-06-13):
  * Bumbleflower: each spell you cast -> +1/+1 counter on a creature (+flying); the
    SECOND resolution each turn -> you draw 2. Cheap/free cantrips chain to the 2nd cast.
  * Jolrael: your 2nd draw each turn -> a 2/2 Cat; the {4}{G}{G} pump is the alpha.
  * Ledger Shredder / Fathom Mage / Dusk Legion Duelist etc. are draw payoffs (hand
    velocity = Jolrael X). Modelled coarsely as draw on the 2nd cast.

HEURISTIC. Spell velocity: each turn cast nonland cards from hand cheapest-first
(creatures stay as bodies; instants/sorceries act as cantrips = draw 1 selection proxy),
capped at 5 Bumbleflower triggers/turn (free spells would otherwise loop). The goldfish
casts its interaction proactively for triggers (no opponents) — a ceiling. Mana = lands
+ rocks/dorks floor. Jolrael X = len(hand) at activation. Combat focus-fire, unblocked.
Trust the SHAPE and front edge, not the second decimal. decap/table stated separately.

OMITTED (conservative): Willbreaker theft (no opp board), Sin counter-vacuum finish,
Smuggler's Share / Tataru Treasure ramp, Snapcaster/flash rebuys, evasive blocking math.
OPTIMISTIC: rocks tap turn they land; proactive spell-dumping; no interaction / static 40.

Data: collection/oracle-cards.json   ·   Writeup: proposals/Ms_Bumbleflower_Clock_Lab_2026-06-13.md
"""
import importlib.util
import random
from pathlib import Path

ROOT = Path(__file__).parent.parent
_spec = importlib.util.spec_from_file_location("speed_lab_core", Path(__file__).parent / "speed_lab_core.py")
slc = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(slc)
ds = slc.ds

DECK = ROOT / "decks" / "this-bunny-goes-to-market-20260404-080311.txt"
SEED = 20260613
TURNS = 14
SHOW = [5, 6, 7, 8, 9, 10, 12, 14]
COMMANDER = "Ms. Bumbleflower"
JOLRAEL = "Jolrael, Mwonvuli Recluse"

ROCKS = {"Sol Ring": (1, 2), "Arcane Signet": (2, 1), "Bender's Waterskin": (2, 1),
         "Paradise Chocobo": (1, 1), "Incubation Druid": (2, 1), "Hardbristle Bandit": (2, 1)}
TRIG_CAP = 5                      # Bumbleflower triggers/turn (free-spell loop guard)


def _powmap(library, commander):
    names = [nm for nm, r in library if "creature" in r["type_line"].lower()]
    names.append(commander)
    raw = slc.load_powers(names)
    return {k: (v if isinstance(v, int) else 1) for k, v in raw.items()}


def goldfish_kill(library, commander, powmap, rng):
    def pw(nm):
        return powmap.get(nm.lower(), 1)

    g = slc.Goldfish(library, rng, rocks=ROCKS)
    tbl = slc.Table()
    bumble = jolrael = False
    ncre = 0                      # creature bodies (incl. commander, Cats, payoffs)
    base_pow = 0                  # summed printed power of bodies
    counters = 0                  # Bumbleflower +1/+1 counters banked on the team

    for T in range(1, TURNS + 1):
        g.begin_turn(T)
        g.deploy_rocks()
        # commander (mana-gate: she's in the command zone, not the library)
        if not bumble and g.avail >= 4:
            g.avail -= 4; bumble = True; ncre += 1; base_pow += 1   # 1/5

        # ---- spell-velocity chain: cast nonlands cheapest-first ----------------
        trig = 0
        while trig < TRIG_CAP:
            cand = sorted(((i, r["cmc"], nm, r) for i, (nm, r) in enumerate(g.hand)
                           if not ds.is_land(r) and nm not in ROCKS),
                          key=lambda x: x[1])
            cast = None
            for i, cmc, nm, r in cand:
                if g.avail >= cmc:
                    cast = (i, cmc, nm, r); break
            if cast is None:
                break
            i, cmc, nm, r = cast
            g.hand.pop(i); g.avail -= cmc
            is_cre = "creature" in r["type_line"].lower()
            if is_cre:
                ncre += 1; base_pow += pw(nm)
                if nm == JOLRAEL:
                    jolrael = True
            else:
                g.draw(1)                       # cantrip / selection proxy
            trig += 1
            if bumble:                          # Bumbleflower trigger
                counters += 1                   # +1/+1 counter on a creature
                if trig == 2:                   # 2nd resolution -> draw two
                    g.draw(2)
                    if jolrael:                 # 2nd draw -> 2/2 Cat
                        ncre += 1; base_pow += 2

        # ---- attack ------------------------------------------------------------
        hand = len(g.hand)
        if jolrael and ncre >= 1 and g.avail >= 6:        # Jolrael alpha
            g.avail -= 6
            board = ncre * hand + counters                # base X/X + counters
        else:
            board = base_pow + counters                   # counter-beats / Cats
        if board > 0:
            tbl.hit_focus(board, T)
        if tbl.done:
            return tbl.decap, tbl.table
    return tbl.decap, tbl.table


def mode_clock(index, aliases, trials):
    print(f"\n### CLOCK — Ms. Bumbleflower kill-turn goldfish   trials={trials} seed={SEED}")
    print("    decap = first opponent dead (40) · table = all three. Combat focus-fire")
    print("    (Jolrael alpha / counter-beats); Willbreaker theft is goldfish-invisible.\n")
    library, commander = slc.load_parsed(DECK, index, aliases)
    powmap = _powmap(library, commander)
    rng = random.Random(SEED)
    res = [goldfish_kill(library, commander, powmap, rng) for _ in range(trials)]
    slc.report_clock(res, SHOW, TURNS, trials)
    print("\n  Claimed in Summary: Goldfish T8-10. Front-edge odds are the test.")


if __name__ == "__main__":
    slc.run_cli(__doc__, {"clock": mode_clock}, default_trials=40000)
