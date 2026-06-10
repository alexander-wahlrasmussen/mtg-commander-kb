#!/usr/bin/env python3
"""gd_clock_lab.py — The Grand Design (Atraxa) KILL-TURN goldfish.

Closes the gap flagged in proposals/Framework_Clock_Gap_2026-06-09.md §5: the
Summary's "Goldfish T6-8" was never goldfished. gd_speed_lab.py measured kill-piece
*availability* (P(Finale drawn by T)), the Speed-Curve analysis measured the mana
curve — neither measured *what turn the deck actually kills*. This does, the same
way rc/er_speed_lab did for their combat decks: a per-trial goldfish that develops
a board and records the decap turn (first opponent dead) and table turn (all three).

Built on speed_lab_core.py (the shared harness extracted 2026-06-10). The deck's
two real kill axes, verified against card_lookup.py oracle text:

  FINALE   Finale of Devastation {X}{G}{G}. ONLY a finisher at X>=10 (= 12 mana):
           creatures you control get +X/+X and gain haste. It is a SORCERY, so the
           creature-tutor suite cannot fetch it — modelled DRAWN-ONLY. The burst
           is checked while mana is still unspent (the optimal line holds up 12).

  BOARD    Reanimator/combat beatdown. Buried Alive deterministically bins the fat
           targets (Razaketh/Vilis, P8); a reanimate spell + a fat in yard cheats
           ~8 power onto the board for 1-3 mana. Atraxa (P7, ETB draws 5) and the
           rest of the creature suite are hard-cast cheapest-first. Unblocked
           goldfish (same convention as rc/er): decap at 40 power, table at 120.

Each turn the deck takes whichever kill (Finale burst or combat) lands first.

HEURISTIC, not a rules engine. Mana = lands + rocks/dorks + land-ramp spells (a
floor; Bloom Tender counted optimistically at 1, board-conditionality ignored).
Damage is unblocked. Buried Alive's binned fats are tracked as reanimation fuel
without being pulled from the library (a small double-count optimism). Trust the
shape and the front edge, not the second decimal. Per the verification rule, decap
and table are reported separately.

Data: collection/oracle-cards.json (refresh via update_scryfall_data.py)
Writeup: proposals/Grand_Design_Speed_Curve_Analysis.md (clock addendum)
"""
import importlib.util
import random
from pathlib import Path

ROOT = Path(__file__).parent.parent
_spec = importlib.util.spec_from_file_location("speed_lab_core", Path(__file__).parent / "speed_lab_core.py")
slc = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(slc)
ds = slc.ds

NEW = ROOT / "decks" / "the-grand-design-20260502.txt"
SEED = 12345
TURNS = 12
SHOW = [4, 5, 6, 7, 8, 9, 10, 12]

DECAP, TABLE = 40, 120          # unblocked thresholds: one player / whole table

# fixed mana producers the scaffold deploys as rocks: name -> (cost, output)
ROCKS = {"Sol Ring": (1, 2), "Arcane Signet": (2, 1), "Birds of Paradise": (1, 1)}
# Bloom Tender is handled manually: it taps for one mana PER COLOUR among your
# permanents, so it floors at ~2 (Birds + a coloured creature) and jumps to 4
# once Atraxa (WUBG) is out — the single biggest swing toward a 12-mana Finale.
# land-ramp spells: cost -> +1 untapped land (taps this turn; conservative)
RAMP = {"Nature's Lore": 2, "Three Visits": 2, "Farseek": 2}
# reanimate spells (cheapest first): cheat a fat creature from yard onto the board
REANIM = [("Reanimate", 1), ("Animate Dead", 2), ("Persist", 2), ("Necromancy", 3),
          ("Victimize", 3), ("Dread Return", 4), ("Living Death", 5)]
FAT = ["Razaketh, the Foulblooded", "Vilis, Broker of Blood"]   # Buried Alive bins these


def _powmap(library, commander):
    names = [nm for nm, r in library if "creature" in r["type_line"].lower()]
    names.append(commander)
    raw = slc.load_powers(names)
    return {k: (v if isinstance(v, int) else 1) for k, v in raw.items()}


def goldfish_kill(library, commander, index, powmap, rng):
    """One trial. Returns (decap_turn, table_turn) from the core Table tracker.

    Each turn: ramp, then the EXISTING board (in play since last turn — summoning
    sickness respected) attacks, then develop. Finale is a haste alpha-strike that
    pumps the in-play board the same turn. Combat is focus-fire with no trample
    spill (Table.hit_focus), so a big swing decaps ONE opponent — the table clock
    is the sum of repeated swings, which is how this midrange deck actually closes.
    """
    def pw(nm):
        return powmap.get(nm.lower(), 1)

    g = slc.Goldfish(library, rng, rocks=ROCKS)
    tbl = slc.Table()        # 3 opponents @ 40
    board = 0                # base power in play (from prior turns)
    ncre = 0                 # creatures in play
    yard_fat = []            # powers of fat creatures in the yard, reanimatable
    atraxa = bloom = False

    for T in range(1, TURNS + 1):
        g.begin_turn(T)
        g.deploy_rocks()
        for rs, cost in RAMP.items():                 # land-ramp: +1 untapped land
            while g.has(rs) and g.avail >= cost:
                g.cast(rs, cost); g.lands += 1; g.avail += 1
        if not bloom and g.has("Bloom Tender") and g.avail >= 2:
            g.cast("Bloom Tender", 2); bloom = True
        if bloom:
            g.avail += 4 if atraxa else 2             # colours among permanents

        # --- attack step: Finale alpha-strike, else the standing board swings ---
        fired = False
        if g.has("Finale of Devastation") and g.avail >= 12 and ncre >= 1:
            X = g.avail - 2                            # {X}{G}{G}
            if X >= 10:                                # +X/+X and haste to all creatures
                pumped = board + (ncre + 1) * X + 8    # whole board + fetched creature, pumped
                tbl.hit_focus(pumped, T)               # no trample: one opponent
                board += 8; ncre += 1                  # fetched creature persists at base
                fired = True
        if not fired and board > 0:
            tbl.hit_focus(board, T)
        if tbl.done:
            return tbl.decap, tbl.table

        # --- develop (these creatures attack from NEXT turn) ---
        if not fired:
            if g.has("Buried Alive") and g.avail >= 3:
                g.cast("Buried Alive", 3); yard_fat += [8, 8]
            if g.has("Grisly Salvage") and g.avail >= 2:
                g.cast("Grisly Salvage", 2)
                for nm in g.mill(5):
                    rec = index.get(nm.lower())
                    if rec and "creature" in rec["type_line"].lower():
                        yard_fat.append(pw(nm))
            for rn, cost in REANIM:
                while yard_fat and g.has(rn) and g.avail >= cost:
                    g.cast(rn, cost)
                    board += max(yard_fat); ncre += 1; yard_fat.remove(max(yard_fat))
            if not atraxa and g.avail >= 7:
                board += pw(commander); ncre += 1; atraxa = True
                g.avail -= 7; g.draw(5)               # Atraxa ETB ~5 cards
            more = True
            while more:
                more = False
                cands = sorted(((i, r["cmc"], nm) for i, (nm, r) in enumerate(g.hand)
                                if "creature" in r["type_line"].lower()), key=lambda x: x[1])
                for i, cmc, nm in cands:
                    if g.avail >= cmc:
                        g.cast(nm, cmc); board += pw(nm); ncre += 1; more = True
                        break

    return tbl.decap, tbl.table


def mode_clock(index, aliases, trials):
    print(f"\n### CLOCK — Grand Design kill-turn goldfish   trials={trials} seed={SEED}")
    print("    decap = first opponent dead (40) · table = all three (120), unblocked.")
    print("    Finale burst (X>=10, drawn-only) vs reanimator/combat board, earliest wins.\n")
    library, commander = slc.load_parsed(NEW, index, aliases)
    powmap = _powmap(library, commander)
    rng = random.Random(SEED)
    res = [goldfish_kill(library, commander, index, powmap, rng) for _ in range(trials)]

    print("  P(kill <= turn T) %".ljust(40) + "".join(f"{t:>6}" for t in SHOW))
    print(slc.row("decap (one opponent, 40)", slc.cum(res, 0, SHOW), SHOW))
    print(slc.row("table (all three, 120)", slc.cum(res, 1, SHOW), SHOW))
    never_d = 100.0 * sum(1 for d, _ in res if d is None) / trials
    never_t = 100.0 * sum(1 for _, t in res if t is None) / trials
    print(f"\n  median decap {slc.median(res, 0)}   median table {slc.median(res, 1)}"
          f"   ·   never-in-{TURNS}: decap {never_d:.0f}% / table {never_t:.0f}%")
    print(f"\n  Claimed in Summary: Goldfish T6-8. Front-edge T6 decap odds above are the test.")


if __name__ == "__main__":
    slc.run_cli(__doc__, {"clock": mode_clock}, default_trials=40000)
