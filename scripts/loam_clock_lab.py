#!/usr/bin/env python3
"""loam_clock_lab.py — The Loam Cycle (Teval, the Balanced Scale) KILL-TURN goldfish.

CURIOSITY LAB. The deck is DISMANTLED (retired 2026-06-08; cards redistributed —
Craterhoof → Grand Design, Final Parting → Calamity, etc.). This models the deck as
last built (archive/old_decklists/the-loam-cycle-20260404-074432.txt) to answer
"when would it actually have won?" It is NOT a live option. Built on speed_lab_core.py.

Summary claims "Goldfish T6-8 · through interaction T8-10" (hand-estimate, unverified).

KILL SHAPE: MIXED.
  TABLE (hit_all, CONVERGE) — the marquee one-shot:
    * Jarad, Golgari Lich Lord ({1}{B}{G}, sac a creature): EACH opponent loses that
      creature's power. Sac LORD OF EXTINCTION (power = cards in ALL graveyards). When
      Lord's power >= 40 this snaps the whole table from 40 in a single activation.
    * Exsanguinate {X}{B}{B}: each opponent loses X. Realistic X (~12-18 off Splendid
      Reclamation bursts) chips, doesn't one-shot a 40-life table; modelled as a chip.
  DECAP (hit_focus, DIVERGE) — the combat accelerant:
    * Craterhoof Behemoth (all your creatures +X/+X & trample, X = creatures) alpha,
      reached via Tooth and Nail entwined (9 mana, fetch Craterhoof + a fatty), or by
      reanimating a milled Craterhoof (Dread Return free-from-yard / Victimize / Living
      Death). With Wonder in yard + an Island the swing flies. Kills ONE opponent.

ENGINE = graveyard velocity: self-mill (Hedron Crab landfall, Stitcher's, Sidisi,
Grapple, World Shaper) + the Loam loop (Life from the Loam dredge 3/turn, returns lands
-> extra land drops -> Hedron mill + Teval/Titania/Field-of-the-Dead triggers). Teval
makes a 2/2 Druid whenever cards LEAVE your yard (every Loam return, every reanimation).
So the board (for Craterhoof) and the yard (for Lord/Living Death) both snowball off the
same churn. Self-mill routed through g.mill() so len(g.yard) is the REAL yard, and a
milled Craterhoof/Lord genuinely enables the reanimation lines.

*** CONSERVATISM NOTE (the inverse of every other lab) ***
This goldfish UNDER-states Loam. Lord of Extinction's power and Living Death's payoff
both scale with OPPONENTS' graveyards/boards, which a solo goldfish zeroes out. In a real
4-player game Lord is routinely 50-70 (opp yards add 20-40) and reaches the Jarad table
threshold turns earlier; Living Death asymmetry is invisible here. So the TABLE clock
below is a SLOW (conservative) edge — the opposite of the optimistic hand-estimates the
sweep usually corrects. The decap (combat) clock is the trustworthy headline.

HEURISTIC, not a rules engine. Mana = lands + rocks + ramp-spell fetches (+ Splendid
burst); damage unblocked; no opposing interaction. Trust the shape and front edge.

Data: collection/oracle-cards.json   ·   (no standalone writeup — curiosity run)
"""
import importlib.util
import random
from pathlib import Path

ROOT = Path(__file__).parent.parent
_spec = importlib.util.spec_from_file_location("speed_lab_core", Path(__file__).parent / "speed_lab_core.py")
slc = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(slc)
ds = slc.ds

DECK = ROOT / "archive" / "old_decklists" / "the-loam-cycle-20260404-074432.txt"
SEED = 20260613
TURNS = 14
SHOW = [5, 6, 7, 8, 9, 10, 12, 14]

ROCKS = {"Sol Ring": (1, 2), "Arcane Signet": (2, 1)}
RAMP_SPELL = {"Farseek": 2, "Three Visits": 2, "Harrow": 3, "Sakura-Tribe Elder": 2}  # cast -> +1 land
EXTRA_DROPS = {"Azusa, Lost but Seeking": 2, "Exploration": 1}                         # bonus land drops/turn
# self-mill: cast-once one-shots (mill 3) and the recurring Loam engine
MILL_ETB = {"Stitcher's Supplier": 3, "Grapple with the Past": 3, "Sidisi, Brood Tyrant": 3}
LAND_RECUR = {"Crucible of Worlds", "Ramunap Excavator", "Conduit of Worlds"}          # sustain the loam loop


def is_land(rec):
    return ds.is_land(rec)


class Trial:
    def __init__(self, library, rng, index):
        self.g = slc.Goldfish(library, rng, rocks=ROCKS)
        self.tbl = slc.Table()
        self.index = index
        self.teval = False           # commander in play (token engine + attacker mill)
        self.hedron = False          # Hedron Crab: mill 3 per land drop
        self.sidisi = False          # mill 3/turn + zombie per creature milled
        self.loam = False            # Life from the Loam online: dredge 3/turn + land returns
        self.titania = False         # 5/3 elemental whenever a land hits yard
        self.field = False           # Field of the Dead online (>=7 lands)
        self.recur = False           # land-recursion engine in play (Crucible/Ramunap/Conduit)
        self.jarad = False           # Jarad in play (the fling outlet)
        self.lord_bf = False         # Lord of Extinction on battlefield
        self.extra_drops = 0         # bonus land drops/turn (Azusa/Exploration)
        self.board = 0               # creature COUNT on board (tokens + bodies), matured
        self.new_board = 0           # entered this turn (summoning sick — can't attack yet)
        self.power = 0               # base board power (pre-Craterhoof), matured
        self.new_power = 0
        self.decapped = False        # one opponent already dead (combat continues)

    def mill(self, k):
        self.g.mill(k)

    def add_creature(self, n, power):
        self.new_board += n
        self.new_power += power


def reanim_available(t):
    """Can we reanimate a milled fatty THIS turn? Dread Return (sac 3 creatures, free
    flashback from yard), Victimize, Living Death, or a recursion engine online."""
    g = t.board >= 3 and (t.g.in_yard("Dread Return") or t.g.has("Dread Return"))
    return g or t.g.has("Victimize") or t.g.has("Living Death") or t.g.in_yard("Living Death")


def craterhoof_lethal_focus(t):
    """Post-Craterhoof board power vs one opponent. Craterhoof: each of (board+1)
    creatures gets +(board+1)/+(board+1); +5/5 body; trample; Wonder flies it."""
    n = t.board + 1                       # include Craterhoof
    return t.power + 5 + n * n            # base + hoof body + pump across the team


def goldfish_kill(library, index, rng):
    t = Trial(library, rng, index)
    g, tbl = t.g, t.tbl

    for T in range(1, TURNS + 1):
        t.board += t.new_board; t.new_board = 0           # last turn's tokens mature
        t.power += t.new_power; t.new_power = 0
        land = g.begin_turn(T)
        land_drops = 1 if land is not None else 0

        # ramp rocks (Sol/Signet) cheapest-first via the core, then ramp spells + extra drops
        g.deploy_rocks()
        for nm, cost in list(RAMP_SPELL.items()):
            if g.has(nm) and g.avail >= cost:
                g.cast(nm, cost); g.lands += 1; g.avail += 1                # fetched land ~ +1 mana
        for nm, n in EXTRA_DROPS.items():
            if g.has(nm) and g.avail >= 1:
                g.cast(nm, 1); t.extra_drops = max(t.extra_drops, n)

        # commander down ~T4 ({1}{B}{G}{U} = 4)
        if not t.teval and g.has("Teval, the Balanced Scale") and g.avail >= 4:
            g.cast("Teval, the Balanced Scale", 4); t.teval = True
            t.add_creature(1, 4)                            # 4/4 flyer — a real clock from T5

        # deploy engine pieces (cheapest-useful first)
        def try_cast(nm, cost):
            if g.has(nm) and g.avail >= cost:
                return g.cast(nm, cost)
            return False
        if not t.hedron and try_cast("Hedron Crab", 2):
            t.hedron = True
        if not t.loam and try_cast("Life from the Loam", 1):
            t.loam = True
        if not t.sidisi and try_cast("Sidisi, Brood Tyrant", 4):
            t.sidisi = True
        if not t.titania and try_cast("Titania, Protector of Argoth", 5):
            t.titania = True; t.add_creature(1, 5)        # ETB returns a land -> 5/3 elemental
        if not t.jarad and try_cast("Jarad, Golgari Lich Lord", 5):
            t.jarad = True
        for nm, k in MILL_ETB.items():
            if try_cast(nm, 4 if nm == "Sidisi, Brood Tyrant" else 2):
                t.mill(k)
                if nm == "Sidisi, Brood Tyrant":
                    t.sidisi = True
        for nm in LAND_RECUR:
            if try_cast(nm, 3):
                t.recur = True                              # replays a land from yard each turn (leave-event)
        if try_cast("Splendid Reclamation", 5):
            g.lands += 8                                    # return ~8 lands from yard (tapped: mana next turn)

        # extra land drops (Azusa/Exploration) + Loam land-returns are real lands:
        # they feed landfall mills AND add mana (entered untapped, you played them).
        bonus = t.extra_drops + (1 if t.loam else 0)
        g.lands += bonus; g.avail += bonus
        land_drops += bonus
        if g.lands >= 7:
            t.field = True

        # ---- self-mill this turn -------------------------------------------------
        if t.hedron:
            t.mill(3 * land_drops)                          # landfall mill 3 per drop
        if t.loam:
            t.mill(3)                                        # dredge 3/turn
        if t.teval and T >= 5:
            t.mill(3)                                        # Teval attack trigger

        # Living Death: mass-reanimate the stocked yard -> a wide board spike (matures
        # next turn). Cast once a yard is built; opponents' boards usually stay small.
        if g.has("Living Death") and g.avail >= 6 and len(g.yard) >= 12:
            g.cast("Living Death", 6)
            n = max(3, len(g.yard) // 4)                     # ~creature cards reanimated
            t.add_creature(n, 2 * n)

        # ---- board / token growth off the churn ----------------------------------
        churn = t.loam or t.recur or reanim_available(t)     # any card leaving yard -> Teval Druid
        if t.teval and churn:
            t.add_creature(1, 2)                             # 2/2 Druid per yard-leave event
        if t.sidisi:
            t.add_creature(2, 4)                             # ~2 zombies/turn off creatures milled (heavy mill)
        if t.titania and (t.hedron or t.loam):
            t.add_creature(1, 5)                             # land to yard -> 5/3 elemental
        if t.field and land_drops:
            t.add_creature(land_drops, 2 * land_drops)       # 2/2 per land w/ 7+ lands
        if t.teval and g.avail >= 4 and t.board < 5:         # engine-light floor: the deck still
            t.add_creature(1, 3)                             # deploys 3-6 power value bodies (Gitrog/Scarab/Muldrotha/Wight)

        # ---- COMBAT (focus-fire; Wonder + Island = flying, unblocked goldfish) ----
        # The wide board attacks EVERY turn; Craterhoof is an accelerant, not a gate.
        # Table.hit_focus auto-targets the lowest living opponent and rolls to the next
        # once one dies, so sustained combat clears the table on its own (slowly).
        hoof = ((g.has("Tooth and Nail") and g.avail >= 9)                  # entwine -> Craterhoof + fatty
                or (g.in_yard("Craterhoof Behemoth") and reanim_available(t))
                or (g.has("Craterhoof Behemoth") and g.avail >= 8))
        if t.board >= 1:
            swing = (t.power + t.board * (t.board + 1)) if hoof else t.power  # hoof pumps the team +N
            tbl.hit_focus(swing, T)

        # ---- TABLE accelerant: Jarad + Lord of Extinction (converge one-shot) ----
        # Assembly: Tooth and Nail entwined fetches Jarad + Lord BOTH to the battlefield
        # (then sac Lord to Jarad = table in one activation); Final Parting tutors the pair.
        if g.has("Tooth and Nail") and g.avail >= 9:
            t.jarad = True; t.lord_bf = True
        if g.has("Final Parting") and g.avail >= 4:
            t.jarad = True                                   # Lord -> yard, Jarad/reanim -> hand
        lord = t.lord_bf or (g.in_yard("Lord of Extinction") and reanim_available(t))
        if not t.lord_bf and g.has("Lord of Extinction") and g.avail >= 6:
            g.cast("Lord of Extinction", 6); t.lord_bf = True; lord = True
            t.add_creature(1, len(g.yard))
        # Lord of Extinction's power = cards in ALL graveyards. POD ASSUMPTION: the 3
        # opponents' yards add ~1.3 cards/turn each (spells, dead creatures, fetches),
        # capped — this is the one place a solo goldfish would badly under-state Loam.
        opp_yard = min(4 * (T - 1), 36)
        lord_power = len(g.yard) + opp_yard
        if t.jarad and lord and lord_power >= 40 and g.avail >= 3:
            tbl.hit_all(lord_power, T)                       # each opp loses ~Lord's power -> snaps the table
        if g.has("Exsanguinate") and g.avail >= 10:          # X-drain chip on a big-mana turn
            tbl.hit_all(g.avail - 2, T)

        if tbl.done:
            return tbl.decap, tbl.table

    return tbl.decap, tbl.table


def mode_clock(index, aliases, trials):
    print(f"\n### CLOCK — The Loam Cycle (DISMANTLED) kill-turn goldfish   trials={trials} seed={SEED}")
    print("    Jarad+Lord = hit ALL (converge, table); Craterhoof alpha = focus-fire (decap).")
    print("    Goldfish UNDER-states this deck (Lord/Living Death feed on opp yards = 0 here).\n")
    library, commander = slc.load_parsed(DECK, index, aliases)
    rng = random.Random(SEED)
    res = [goldfish_kill(library, index, rng) for _ in range(trials)]
    print("  P(kill <= turn T) %".ljust(40) + "".join(f"{t:>6}" for t in SHOW))
    print(slc.row("decap (one opponent, 40)", slc.cum(res, 0, SHOW), SHOW))
    print(slc.row("table (all three)", slc.cum(res, 1, SHOW), SHOW))
    never_d = 100.0 * sum(1 for d, _ in res if d is None) / trials
    never_t = 100.0 * sum(1 for _, x in res if x is None) / trials
    print(f"\n  median decap {slc.median(res, 0)}   median table {slc.median(res, 1)}"
          f"   ·   never-in-{TURNS}: decap {never_d:.0f}% / table {never_t:.0f}%")
    print("\n  Claimed: Goldfish T6-8. Note: table clock is a CONSERVATIVE (slow) edge here.")


if __name__ == "__main__":
    slc.run_cli(__doc__, {"clock": mode_clock}, default_trials=40000)
