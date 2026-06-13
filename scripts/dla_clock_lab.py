#!/usr/bin/env python3
"""dla_clock_lab.py — The Dark Lord's Army (Sauron, the Dark Lord) KILL-TURN lab.

Kill-Window Lab Sweep, deck 10 — the LAST row. Summary claims "Goldfish T8-10".
Built on speed_lab_core.py. Commander mana-gated.

**This deck cannot be goldfished like the others.** Its entire engine is OPPONENT-DRIVEN
(verified card_lookup.py 2026-06-13):
  * Sauron: whenever an OPPONENT casts a spell -> amass Orcs 1 (the Army only grows from
    opponent activity).
  * Underworld Dreams: opp draws a card -> 1 to that player. Sheoldred: opp draws -> lose 2.
    Orcish Bowmasters: opp's *bonus* draws -> 1 to any target + amass 1.
  * Wound Reflection: each end step, each opponent loses life = life they lost this turn
    (DOUBLES the drain).
  * Gray Merchant ETB: each opp loses devotion-to-black (the one self-contained drain).
  * Sauron's Ring draw-4 gains YOU life (Sheoldred on your draws) — DEFENSIVE, not opp drain.

A self-contained goldfish (no opponents) would show this deck killing ~never and badly
misrepresent it. So — like `delay_lab.py` vs a pod combo turn — this lab models an explicit
**pod-activity assumption**: SPELLS opponent spells/cycle (feed amass) and DRAWS opponent
draws/cycle (feed the drain). Run at LOW / MID / HIGH pod tempo; the clock is a FUNCTION of
that assumption, stated, not a self-contained number.

KILL SHAPE — MIXED, drain-dominant CONVERGE:
  DRAIN (hit_all, primary)  per opp draw: Sheoldred 2 + Underworld Dreams 1 (+Bowmasters 1
                            on bonus draws); Wound Reflection doubles it; Gray Merchant ETB.
                            Hits all opponents ~symmetrically -> converge.
  ARMY  (focus, secondary)  amass grows the Army by opponent spells; evasion (Cover of
                            Darkness / Rogue's Passage) -> unblockable -> focus-fire one player.

HEURISTIC. Self mana = lands + rocks floor (for deploying the engine + the 6-mana commander).
Drain per opp = (DRAWS/3) x (2·Sheoldred + 1·UD), applied hit_all; Wound doubles; Bowmasters
bonus pings focus. Devotion = summed B pips of deployed black engine. Army = cumulative amass
(SPELLS/cycle while Sauron out), focus-fired (goldfish-unblocked). Trust the SHAPE and the
tempo-sensitivity, not the second decimal.

OMITTED (conservative): aristocrats grind (Dictate+Bombardment+Plunderer forced sacs),
graveyard-reset reanimation loops, Strionic copies, Barad-dur self-amass, Yawgmoth engine,
Call-of-the-Ring/Nazgul redundant amass. OPTIMISTIC: rocks tap turn they land; the assumed
pod tempo is steady (real pods spike/lull); no opposing interaction with OUR engine.

Data: collection/oracle-cards.json   ·   Writeup: proposals/Dark_Lords_Army_Clock_Lab_2026-06-13.md
"""
import importlib.util
import random
from pathlib import Path

ROOT = Path(__file__).parent.parent
_spec = importlib.util.spec_from_file_location("speed_lab_core", Path(__file__).parent / "speed_lab_core.py")
slc = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(slc)
ds = slc.ds

DECK = ROOT / "decks" / "the-dark-lords-army-20260417-211206.txt"
SEED = 20260613
TURNS = 16
SHOW = [6, 7, 8, 9, 10, 12, 14, 16]

ROCKS = {"Sol Ring": (1, 2), "Arcane Signet": (2, 1), "Talisman of Dominance": (2, 1),
         "Talisman of Creativity": (2, 1), "Fellwar Stone": (2, 1), "Lotus Petal": (0, 1)}
# engine pieces: name -> (cost, B-pips for devotion)
ENGINE = {"Underworld Dreams": (3, 3), "Sheoldred, the Apocalypse": (4, 2),
          "Orcish Bowmasters": (2, 1), "Gray Merchant of Asphodel": (5, 2),
          "Wound Reflection": (6, 1), "Pitiless Plunderer": (4, 1)}
SAURON = "Sauron, the Dark Lord"      # commander, 6 mana, 1 B pip


def goldfish_kill(library, rng, spells, draws):
    """One trial under a pod-activity assumption (spells/draws per cycle)."""
    g = slc.Goldfish(library, rng, rocks=ROCKS)
    tbl = slc.Table()
    sauron = gray_done = False
    bf = set()
    army = 0
    bonus = max(0, draws - 3)              # draws beyond the 3 base draw-steps (Bowmasters)

    def devotion():
        return 1 * sauron + sum(ENGINE[n][1] for n in bf)

    for T in range(1, TURNS + 1):
        g.begin_turn(T)
        g.deploy_rocks()
        if g.has("Dark Ritual"):
            g.cast("Dark Ritual", 1); g.add_mana(3)
        # commander (mana-gate) then engine cheapest-first
        if not sauron and g.avail >= 6:
            g.avail -= 6; sauron = True
        for nm, (cost, _pip) in sorted(ENGINE.items(), key=lambda x: x[1][0]):
            if nm not in bf and g.cast(nm, cost):
                bf.add(nm)
                if nm == "Orcish Bowmasters":
                    army += 1                      # ETB amass 1
                if nm == "Gray Merchant of Asphodel" and not gray_done:
                    tbl.hit_all(devotion(), T); gray_done = True

        # ---- amass (opponent spells) ------------------------------------------
        if sauron:
            army += spells
        if "Orcish Bowmasters" in bf:
            army += bonus                          # bonus-draw amass

        # ---- drain (opponent draws), hit_all -> converge ----------------------
        per_opp = (draws / 3.0) * (2 * ("Sheoldred, the Apocalypse" in bf)
                                   + 1 * ("Underworld Dreams" in bf))
        if per_opp > 0:
            tbl.hit_all(per_opp, T)
            if "Wound Reflection" in bf:           # end-step doubling of the loss
                tbl.hit_all(per_opp, T)
        if "Orcish Bowmasters" in bf and bonus:
            tbl.hit_focus(bonus, T)                # bonus-draw pings (any target)

        # ---- Army voltron (focus, evasive/unblocked) --------------------------
        if army > 0:
            tbl.hit_focus(army, T)
        if tbl.done:
            return tbl.decap, tbl.table
    return tbl.decap, tbl.table


def mode_pod(index, aliases, trials):
    print(f"\n### CLOCK — The Dark Lord's Army, vs POD-ACTIVITY assumption   trials={trials} seed={SEED}")
    print("    OPPONENT-DRIVEN engine: amass on opp spells, drain on opp draws. NOT a")
    print("    self-contained goldfish. decap = first opp dead / table = all three.")
    print("    Drain hit_all (converge); Army focus. Tempo = (opp spells/cycle, opp draws/cycle).\n")
    library, commander = slc.load_parsed(DECK, index, aliases)
    tempos = [("LOW pod  (3 spells / 3 draws)", 3, 3),
              ("MID pod  (6 spells / 4 draws)", 6, 4),
              ("HIGH pod (9 spells / 6 draws)", 9, 6)]
    print("  tempo".ljust(40) + "".join(f"{t:>6}" for t in SHOW) + "   median")
    for tag, sp, dr in tempos:
        rng = random.Random(SEED)
        res = [goldfish_kill(library, rng, sp, dr) for _ in range(trials)]
        print(slc.row(f"{tag}  decap", slc.cum(res, 0, SHOW), SHOW) + f"   {slc.median(res, 0)}")
        print(slc.row(" " * len(tag) + "  table", slc.cum(res, 1, SHOW), SHOW) + f"   {slc.median(res, 1)}")
        nt = 100.0 * sum(1 for _, t in res if t is None) / trials
        print(f"    table never-in-{TURNS}: {nt:.0f}%")
    print("\n  Claimed in Summary: Goldfish T8-10 / through interaction T10-12.")


if __name__ == "__main__":
    slc.run_cli(__doc__, {"pod": mode_pod}, default_trials=40000)
