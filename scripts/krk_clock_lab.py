#!/usr/bin/env python3
"""krk_clock_lab.py — kill-turn goldfish for "Deficit Spending" (K'rrik, Son of Yawgmoth, mono-B
life-as-mana aristocrats). Candidate list decks/considering/deficit-spending-20260712.txt.

KILL SHAPE (verified 2026-07-12: find_combos reports 20 COMPLETE combos in this exact list; every
card text below read via card_lookup — no memory-drafting):
  The deck wins by assembling ANY of a redundant web of 2-4 card death-trigger infinites and
  executing for ~zero mana. The verified sets modelled here (CSB combo IDs in the PROP doc):
    S1  Warren Soultrader + Gravecrawler + a drain payoff
        (Soultrader: "Pay 1 life, sac another creature: create a Treasure" — a ZOMBIE, so it
         enables Gravecrawler's own recast; Treasure pays the {B}. Iteration is mana-neutral,
         1 life, refunded by any lifegain drain.)
    S2  Mikaeus, the Unhallowed + Warren Soultrader + a drain (undying loop, infinite Treasures)
    S3  Yawgmoth, Thran Physician + Mikaeus + {Gray Merchant | Kokusho} (undying + -1/-1 cancel;
        pay 1 life per iteration, draw a card, drain triggers)
    S4  Yawgmoth + Nest of Scarabs + a drain (near-infinite: counters mint Insect fodder)
    S5  Chainer, Dementia Master + Gray Merchant + {Viscera Seer | Carrion Feeder | Yahenni}
        (+ K'rrik paying the BBB reanimates with life)
    S6  Gravecrawler + Aetherflux Reservoir + {Carrion Feeder | Viscera Seer} (+ K'rrik)
  Drain payoffs (any one converts a loop to a table kill): Blood Artist, Zulaport Cutthroat,
  Nadier's Nightblade, Bontu's Monument, Aetherflux Reservoir, Sephiroth (both faces drain on
  death; the transform emblem persists through removal).

K'RRIK MODEL: {B} pips are payable with 2 life each ONCE K'rrik is on the battlefield (cast when
4 generic mana available: {4} + 6 life for the {B/P}{B/P}{B/P}). A 12-life reserve is never spent.
Life regen from lifelink/drain refunds is modelled only as loop-execution neutrality, not banked.

OPTIMISTIC (documented): tutors (Emeritus's Demonic Tutor copy / Grim Servant / Increasing
Ambition) always find the best missing piece; rituals are flat +2 net mana the turn used; no
opponent interaction (goldfish); pieces always survive to the kill turn.
PESSIMISTIC / OMITTED: Ad Nauseam is a flat draw-5-for-12-life (real turns see more); Bolas's
Citadel is +1 draw/turn (no storm-off); Victimize/Whisper/Chainer reanimation shortcuts,
Doomsday Excruciator, Gary-ETB chip drains, and combat damage are ALL omitted — the curve is a
combo-assembly clock, not total pressure.

decap == table by construction (an executed loop drains the whole pod). Availability/ceiling
curve, not a rules engine — trust the shape and deltas.

Data: collection/oracle-cards.json (refresh via update_scryfall_data.py)
"""
import importlib.util
import random
from pathlib import Path

ROOT = Path(__file__).parent.parent
_spec = importlib.util.spec_from_file_location(
    "speed_lab_core", Path(__file__).parent / "speed_lab_core.py")
slc = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(slc)

DECK = ROOT / "decks" / "considering" / "deficit-spending-20260712.txt"
SEED = 20260712
TURNS = 14
SHOW = [4, 5, 6, 7, 8, 9, 10, 12, 14]

ROCKS = {"Sol Ring": (1, 2), "Arcane Signet": (2, 1), "Mana Vault": (1, 3)}
RITUALS = {"Dark Ritual": 1, "Cabal Ritual": 2, "Culling the Weak": 2, "Bubbling Muck": 1}

# combo pieces: name -> (generic, black_pips)  [costs read via card_lookup 2026-07-12]
PIECES = {
    "Warren Soultrader": (2, 1), "Gravecrawler": (0, 1),
    "Mikaeus, the Unhallowed": (3, 3), "Yawgmoth, Thran Physician": (2, 2),
    "Nest of Scarabs": (2, 1), "Chainer, Dementia Master": (3, 2),
    "Gray Merchant of Asphodel": (3, 2), "Kokusho, the Evening Star": (4, 2),
    "Aetherflux Reservoir": (4, 0), "Blood Artist": (1, 1),
    "Zulaport Cutthroat": (1, 1), "Nadier's Nightblade": (2, 1),
    "Bontu's Monument": (3, 0), "Sephiroth, Fabled SOLDIER": (2, 1),
    "Carrion Feeder": (0, 1), "Viscera Seer": (0, 1),
    "Yahenni, Undying Partisan": (2, 1),
}
DRAINS = ["Blood Artist", "Zulaport Cutthroat", "Nadier's Nightblade",
          "Bontu's Monument", "Aetherflux Reservoir", "Sephiroth, Fabled SOLDIER"]
SETS = (
    [["Warren Soultrader", "Gravecrawler", d] for d in DRAINS] +
    [["Mikaeus, the Unhallowed", "Warren Soultrader", d]
     for d in ("Blood Artist", "Zulaport Cutthroat", "Sephiroth, Fabled SOLDIER")] +
    [["Yawgmoth, Thran Physician", "Mikaeus, the Unhallowed", t]
     for t in ("Gray Merchant of Asphodel", "Kokusho, the Evening Star")] +
    [["Yawgmoth, Thran Physician", "Nest of Scarabs", d]
     for d in ("Blood Artist", "Zulaport Cutthroat", "Nadier's Nightblade",
               "Sephiroth, Fabled SOLDIER")] +
    [["Chainer, Dementia Master", "Gray Merchant of Asphodel", o]
     for o in ("Viscera Seer", "Carrion Feeder", "Yahenni, Undying Partisan")] +
    [["Gravecrawler", "Aetherflux Reservoir", o]
     for o in ("Carrion Feeder", "Viscera Seer")]
)
TUTORS = {"Emeritus of Woe": 4, "Grim Servant": 4, "Increasing Ambition": 5}
DRAW_ENGINES = {"Dark Confidant": (1, 1), "Phyrexian Arena": (2, 1)}  # (generic, pips)
RESERVE = 12


class Trial:
    def __init__(self, library, rng):
        self.g = slc.Goldfish(library, rng, rocks=ROCKS)
        self.tbl = slc.Table()
        self.life = 40
        self.krrik = False
        self.board = set()
        self.engines = 0          # per-turn extra draws online

    # -- life-as-mana casting -------------------------------------------------
    def cast_cost(self, name):
        g, p = PIECES[name]
        return g, p

    def try_cast(self, name):
        """Cast from hand paying generic with mana and pips with mana-then-life."""
        g = self.g
        if name in self.board or not g.has(name):
            return False
        gen, pips = PIECES[name]
        pips_mana = min(pips, max(0, g.avail - gen))
        pips_life = pips - pips_mana
        if not self.krrik:
            pips_life = 0
            pips_mana = pips
        if g.avail < gen + pips_mana:
            return False
        if pips_life and self.life - 2 * pips_life < RESERVE:
            return False
        if pips - pips_mana - pips_life > 0:
            return False
        g.hand.pop(g.in_hand(name))
        g.avail -= gen + pips_mana
        self.life -= 2 * pips_life
        self.board.add(name)
        return True

    def missing(self, s):
        return [n for n in s if n not in self.board]

    def turn(self, T):
        g = self.g
        g.begin_turn(T)
        g.deploy_rocks()
        # rituals: flat +2 net mana the turn drawn (documented optimism)
        for r in list(RITUALS):
            if g.has(r) and g.avail >= RITUALS[r]:
                g.cast(r, RITUALS[r]); g.add_mana(RITUALS[r] + 2)
        # commander: {4} + 6 life for BBB (K'rrik unlocks life-as-mana)
        if not self.krrik and g.avail >= 4 and self.life - 6 >= RESERVE + 6:
            g.avail -= 4; self.life -= 6; self.krrik = True
        # draw engines
        g.draw(self.engines)
        for e, (gen, pips) in DRAW_ENGINES.items():
            if g.has(e) and g.avail >= gen + pips:
                g.cast(e, gen + pips); self.engines += 1
        if g.has("Read the Bones") and g.avail >= 3:
            g.cast("Read the Bones", 3); self.life -= 2; g.draw(2)
        if g.has("Ad Nauseam") and self.krrik and g.avail >= 3 and self.life - 12 >= RESERVE:
            g.cast("Ad Nauseam", 3); self.life -= 12; g.draw(5)
        if g.has("Bolas's Citadel") and g.avail >= 4 and self.life - 4 >= RESERVE:
            g.cast("Bolas's Citadel", 4); self.life -= 2; self.engines += 1
        # tutor toward the closest-to-complete set (best-case piece selection);
        # fetch the missing piece we do NOT already hold in hand
        best = min(SETS, key=lambda s: len(self.missing(s)))
        need = [n for n in self.missing(best) if not g.has(n)]
        if need:
            for t, cost in TUTORS.items():
                if g.has(t) and g.avail >= cost:
                    g.cast(t, cost)
                    if not g.fetch(need[0]):
                        g.draw(1)
                    break
        # cast combo pieces, cheapest first
        for n in sorted(PIECES, key=lambda n: sum(PIECES[n])):
            if g.has(n) and n not in self.board:
                self.try_cast(n)
        # execute: any complete set + life above reserve -> the loop drains the pod
        if any(not self.missing(s) for s in SETS) and self.life > RESERVE:
            self.tbl.kill_all(T)


def mode_clock(index, aliases, trials):
    print(f"\n### CLOCK — Deficit Spending (K'rrik) combo-assembly goldfish   trials={trials} seed={SEED}")
    rng = random.Random(SEED)
    library, commander = slc.load_parsed(DECK, index, aliases)
    # normalize DFC names to their front face so has()/cast()/fetch() match PIECES/TUTORS
    # (the .txt stores "Sephiroth, Fabled SOLDIER // Sephiroth, One-Winged Angel" etc.)
    library = [(n.split(" // ")[0].strip(), r) for n, r in library]
    print(f"  library {len(library)} + commander {commander}")
    print("  kill = first COMPLETE combo set on battlefield (20-combo web; see docstring)")
    res = slc.run_goldfish(lambda: Trial(library, rng), trials, TURNS)
    slc.report_clock(res, SHOW, TURNS, trials, single=True)
    print("\n  decap == table (executed loop drains the pod). Chip/combat/reanimation OMITTED.")


if __name__ == "__main__":
    slc.run_cli(__doc__, {"clock": mode_clock}, default_trials=40000)
