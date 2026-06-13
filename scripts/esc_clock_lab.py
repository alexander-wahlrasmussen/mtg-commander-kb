#!/usr/bin/env python3
"""esc_clock_lab.py — Eldrazi Stampede Chaos (Maelstrom Wanderer) KILL-TURN goldfish.

Kill-Window Lab Sweep, deck 1 of 10 (proposals/Kill_Window_Lab_Sweep_2026-06-13.md).
The Summary claims "Goldfish T6-8" with the front-edge T6 flagged suspect — this is
the test. Built on speed_lab_core.py.

KILL SHAPE: combat board-building. Two clocks the verification rule wants split:

  DECAP (focus)   Maelstrom Wanderer cast = two cascades (nonland MV<8 hits) that
                  attack THE SAME TURN (Wanderer's haste static) + Wanderer's own
                  7 power. That, plus the cheapest-first beater pile, focus-fires
                  one opponent (Table.hit_focus). Repeated swings roll to the next
                  opponent as each dies.
  TABLE (alpha)   Craterhoof Behemoth ({5}{G}{G}{G}, MV8, HAS HASTE): on ETB every
                  creature you control gets +X/+X and TRAMPLE, X = creatures you
                  control (tokens included). With trample the swing distributes
                  across the whole table in one turn — the deck's real table-kill.
                  Token producers (Avenger plants/land, Rampaging Baloths landfall
                  4/4s, Tendershoot saprolings) inflate X.

Oracle facts encoded (card_lookup.py 2026-06-13):
  * Wanderer 7/5; cascade twice, each into a NONLAND with MV < 8 (so it CANNOT
    cascade into the MV8+ titans/Craterhoof/Ghalta); grants haste to all your
    creatures including itself. Commander -> always castable at 8 (recast tax ignored).
  * Craterhoof HAS HASTE; pump X is locked at resolution and applies to creatures
    you control then (this-turn deploys included), trample on all.
  * Ghalta {10}{G}{G} reduced by total power of your creatures, floor {G}{G}=2; 12/12.
  * Avenger of Zendikar (MV7): ETB a 0/1 Plant per land you control.
  * Selvala, Heart of the Wilds ({1}{G}{G}): {G},{T}: add X = greatest power among
    your creatures (board-conditional ramp; floors at a dork until a beater lands).

HEURISTIC, not a rules engine. Mana = lands + rocks/dorks + land-ramp spells
(a floor; Ancient Tomb counted as 1, Nykthos/Selvala-into-titan upside ignored or
capped). Damage is unblocked. Cascade hits are resolved against the ACTUAL library
(scan top until a nonland MV<8; power added only if it's a creature, so whiffs into
ramp/removal cost nothing — faithful to the deck's ~50% creature density). Normal
swings focus-fire (decap-fast/table-slow convention shared with rc/er/gd); only the
Craterhoof alpha distributes across the table. Trust shape and front edge, not the
second decimal. decap and table reported separately.

Data: collection/oracle-cards.json   ·   Writeup: proposals/Eldrazi_Stampede_Clock_Lab_2026-06-13.md
"""
import importlib.util
import random
from pathlib import Path

ROOT = Path(__file__).parent.parent
_spec = importlib.util.spec_from_file_location("speed_lab_core", Path(__file__).parent / "speed_lab_core.py")
slc = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(slc)
ds = slc.ds

DECK = ROOT / "decks" / "eldrazi-stampede-chaos-20260306-133311.txt"
SEED = 20260613
TURNS = 14
SHOW = [5, 6, 7, 8, 9, 10, 12, 14]

# fixed mana producers + dorks the scaffold deploys greedily: name -> (cost, output)
ROCKS = {
    "Sol Ring": (1, 2), "Mana Vault": (1, 3), "Arcane Signet": (2, 1),
    "Talisman of Impulse": (2, 1), "Thran Dynamo": (4, 3),
    "Birds of Paradise": (1, 1), "Delighted Halfling": (1, 1),
    "Lotus Cobra": (2, 1), "Llanowar Loamspeaker": (3, 1),
}
# land-ramp spells: name -> (cost, lands added untapped-ish, taps this turn = conservative)
RAMP = {
    "Rampant Growth": (2, 1), "Farseek": (2, 1), "Nature's Lore": (2, 1),
    "Cultivate": (3, 1), "Kodama's Reach": (3, 1), "Skyshroud Claim": (4, 2),
    "Sakura-Tribe Elder": (2, 1), "Solemn Simulacrum": (4, 1),
}
# creatures NOT to hard-cast in the generic beater loop (handled specially or are ramp)
SPECIAL = set(ROCKS) | {"Selvala, Heart of the Wilds", "Avenger of Zendikar",
                        "Rampaging Baloths", "Tendershoot Dryad", "Craterhoof Behemoth",
                        "Ghalta, Primal Hunger", "Solemn Simulacrum"}
TRAMPLE_GRANTERS = {"Garruk's Uprising", "Goreclaw, Terror of Qal Sisma"}


def _powmap(library, commander):
    names = [nm for nm, r in library if "creature" in r["type_line"].lower()]
    names.append(commander)
    raw = slc.load_powers(names)
    return {k: (v if isinstance(v, int) else 1) for k, v in raw.items()}


def trample_distribute(tbl, P, T):
    """A trample alpha: assign P across living opponents, filling each to lethal in
    turn (kills as many as the swing allows)."""
    remaining = P
    for i in range(len(tbl.dmg)):
        if remaining <= 0:
            break
        if tbl.dmg[i] < tbl.life:
            take = min(tbl.life - tbl.dmg[i], remaining)
            tbl.dmg[i] += take
            remaining -= take
    tbl._update(T)


def goldfish_kill(library, commander, index, powmap, rng):
    """One trial -> (decap_turn, table_turn)."""
    def pw(nm):
        return powmap.get(nm.lower(), 1)

    g = slc.Goldfish(library, rng, rocks=ROCKS)
    tbl = slc.Table()
    board, ncre = 0, 0          # matured power / creature count (can attack)
    new_pow, new_cre = 0, 0     # deployed this turn (sick unless Wanderer haste)
    maxpow = 0                  # greatest single creature power (for Selvala)
    wanderer = False            # haste static online
    selvala = False
    baloths = tender = False
    trample = False

    def remember(p):
        nonlocal maxpow
        if p > maxpow:
            maxpow = p

    def cascade():
        """Resolve one cascade against the real library; return power if a creature."""
        while g.ptr < len(g.deck):
            nm, rec = g.deck[g.ptr]; g.ptr += 1
            if not ds.is_land(rec) and rec["cmc"] < 8:
                if "creature" in rec["type_line"].lower():
                    return pw(nm)
                return 0
        return 0

    for T in range(1, TURNS + 1):
        # matured: last turn's deploys can attack now
        board += new_pow; ncre += new_cre; new_pow = new_cre = 0
        land = g.begin_turn(T)
        g.deploy_rocks()
        lands_in = 1 if land else 0
        # land-ramp spells
        for rs, (cost, n) in RAMP.items():
            while g.has(rs) and g.avail >= cost:
                g.cast(rs, cost); g.lands += n; g.avail += n; lands_in += n
        # Selvala mana (board-conditional)
        if not selvala and g.has("Selvala, Heart of the Wilds") and g.avail >= 3:
            g.cast("Selvala, Heart of the Wilds", 3); selvala = True
            new_pow += 2; new_cre += 1; remember(2)
        if selvala:
            g.avail += max(1, maxpow)
        # landfall token producers (lands entered this turn)
        if baloths and lands_in:
            new_pow += 4 * lands_in; new_cre += lands_in; remember(4)
        if tender:
            new_pow += 1; new_cre += 1

        # ---- ATTACK STEP: Craterhoof alpha (table) > Wanderer dump > board swing --
        fired = False
        # Craterhoof: cast for 8, haste; pump X = all creatures incl this-turn tokens
        if not fired and g.has("Craterhoof Behemoth") and g.avail >= 8:
            g.cast("Craterhoof Behemoth", 8)
            attackers = ncre + 1 + (new_cre if wanderer else 0)   # +Craterhoof (haste)
            total_cre = ncre + new_cre + 1                         # X (incl sick/tokens)
            base = board + 5 + (new_pow if wanderer else 0)
            swing = base + total_cre * attackers
            trample_distribute(tbl, swing, T)
            board += 5; ncre += 1; remember(5); fired = True
        # Wanderer: commander, castable at 8; two hasty cascades + 7 attack this turn
        if not fired and not wanderer and g.avail >= 8:
            g.avail -= 8
            c1, c2 = cascade(), cascade()
            wanderer = True
            swing = 7 + c1 + c2
            tbl.hit_focus(swing, T)
            board += 7 + c1 + c2; ncre += 1 + (c1 > 0) + (c2 > 0)
            remember(7); fired = True
        # otherwise the standing board attacks (focus)
        if not fired and board > 0:
            if trample:
                trample_distribute(tbl, board, T)
            else:
                tbl.hit_focus(board, T)
        if tbl.done:
            return tbl.decap, tbl.table

        # ---- DEVELOP (matures next turn) ---------------------------------------
        if g.has("Avenger of Zendikar") and g.avail >= 7:
            g.cast("Avenger of Zendikar", 7)
            new_pow += 5; new_cre += 1 + g.lands; remember(5)   # 5/5 + 0/1 plant per land
        if not baloths and g.has("Rampaging Baloths") and g.avail >= 6:
            g.cast("Rampaging Baloths", 6); baloths = True
            new_pow += 7; new_cre += 1; remember(7)
        if not tender and g.has("Tendershoot Dryad") and g.avail >= 5:
            g.cast("Tendershoot Dryad", 5); tender = True
            new_pow += 1; new_cre += 1
        for rs, (cost, n) in (("Solemn Simulacrum", (4, 1)),):
            if g.has(rs) and g.avail >= cost:
                g.cast(rs, cost); g.lands += n; g.avail += n
                new_pow += 2; new_cre += 1
        # Ghalta: cost reduced by total power, floor 2
        tot = board + new_pow
        gcost = max(2, 12 - tot)
        if g.has("Ghalta, Primal Hunger") and g.avail >= gcost:
            g.cast("Ghalta, Primal Hunger", gcost)
            new_pow += 12; new_cre += 1; remember(12)
        for tg in TRAMPLE_GRANTERS:
            if not trample and g.has(tg):
                r = index.get(tg.lower())
                if r and g.avail >= r["cmc"]:
                    g.cast(tg, r["cmc"]); trample = True
                    if "creature" in r["type_line"].lower():
                        new_pow += pw(tg); new_cre += 1; remember(pw(tg))
        # generic beaters cheapest-first
        more = True
        while more:
            more = False
            cands = sorted(((i, r["cmc"], nm) for i, (nm, r) in enumerate(g.hand)
                            if "creature" in r["type_line"].lower() and nm not in SPECIAL),
                           key=lambda x: x[1])
            for i, cmc, nm in cands:
                if g.avail >= cmc:
                    g.cast(nm, cmc); new_pow += pw(nm); new_cre += 1; remember(pw(nm))
                    more = True
                    break

    return tbl.decap, tbl.table


def mode_clock(index, aliases, trials):
    print(f"\n### CLOCK — Eldrazi Stampede Chaos kill-turn goldfish   trials={trials} seed={SEED}")
    print("    decap = first opponent dead (40, focus) · table = all three dead.")
    print("    Craterhoof alpha distributes (trample); Wanderer dump + beaters focus-fire.\n")
    library, commander = slc.load_parsed(DECK, index, aliases)
    powmap = _powmap(library, commander)
    rng = random.Random(SEED)
    res = [goldfish_kill(library, commander, index, powmap, rng) for _ in range(trials)]

    print("  P(kill <= turn T) %".ljust(40) + "".join(f"{t:>6}" for t in SHOW))
    print(slc.row("decap (one opponent, 40)", slc.cum(res, 0, SHOW), SHOW))
    print(slc.row("table (all three)", slc.cum(res, 1, SHOW), SHOW))
    never_d = 100.0 * sum(1 for d, _ in res if d is None) / trials
    never_t = 100.0 * sum(1 for _, t in res if t is None) / trials
    print(f"\n  median decap {slc.median(res, 0)}   median table {slc.median(res, 1)}"
          f"   ·   never-in-{TURNS}: decap {never_d:.0f}% / table {never_t:.0f}%")
    print("\n  Claimed in Summary: Goldfish T6-8. Front-edge T6 decap odds above are the test.")


if __name__ == "__main__":
    slc.run_cli(__doc__, {"clock": mode_clock}, default_trials=40000)
