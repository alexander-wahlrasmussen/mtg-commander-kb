#!/usr/bin/env python3
"""lw_clock_lab.py — Lightning War (Fire Lord Azula) KILL-TURN goldfish.

Kill-Window Lab Sweep, deck 3 of 10 (proposals/Kill_Window_Lab_Sweep_2026-06-13.md).
lw_speed_lab.py measured the ONE-CAST table wipe from 40 (20% by T12 / 70% never)
and the same wipe against pre-chipped opponents (@20: 22% by T7), but never an
unconditional kill-turn goldfish. This is that goldfish. Built on speed_lab_core.py.

KILL SHAPE: burn/tempo — chip + copy-amplified X-spell. The deck races by
PRESSURING with an evasive board + two pingers (Guttersnipe, Vivi) and finishing
with a forked X-spell. v2 (2026-06-13, after user push-back) fixes a too-conservative
v1 that swung only Azula (4 power) and ignored Vivi + Fated Firepower.

Oracle facts encoded (card_lookup.py 2026-06-13):
  * Azula (cmd, 4 mana, 4/4): attacking adds {R}{R}; spells cast while she attacks
    are COPIED (the copy isn't "cast" — no re-trigger of Guttersnipe/Vivi, but it
    deals its own damage). Modelled as a x2 instance multiplier on the finisher.
  * Crackle with Power {X}{X}{X}{R}{R} (cost 3X+2): 5X to each of up to X targets.
    SORCERY -> needs a flash enabler to fire in Azula's combat.
  * Comet Storm {X}{R}{R} + multikick {1}/extra target: X to each. INSTANT.
  * Banefire {X}{R} / Electrodominance {X}{R}{R}: single target.
  * Guttersnipe: each I/S you CAST -> 2 to EACH opponent. Vivi Ornitier: each
    NONCREATURE spell -> +1/+1 on Vivi AND 1 to EACH opponent; {0}: add its power
    in mana once/turn (a snowballing ramp + pinger).
  * Fated Firepower: a source you control dealing damage to an opponent deals +X
    (its fire counters) — an amplifier on EVERY ping, swing, and finisher instance.
  * Beaters: Goldspan 4/4 haste-fly, Hullbreaker 7/8, Leyline Tyrant 4/4 fly,
    Vendilion 3/1 fly, Opposition Agent 3/2, Storm-Kiln 2/2 (treasures/cast+copy).

HEURISTIC, not a rules engine. Mana = lands + rocks floor + Azula's +2 in combat +
banked Storm-Kiln Treasures + Vivi's tap + rituals in hand. Chip = (Guttersnipe 2 +
Vivi 1)/noncreature-cast to all, plus the creature board (focus). Fated adds X per
damage instance. Finisher fires the turn its lethal X is affordable vs current life.
No opposing interaction or blockers — and NONE of the deck's own disruption (8
counters) is modelled, so against a real pod the deck is stronger than this goldfish.
decap and table reported separately.

Data: collection/oracle-cards.json   ·   Writeup: proposals/Lightning_War_Clock_Lab_2026-06-13.md
"""
import importlib.util
import math
import random
from pathlib import Path

ROOT = Path(__file__).parent.parent
_spec = importlib.util.spec_from_file_location("speed_lab_core", Path(__file__).parent / "speed_lab_core.py")
slc = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(slc)
ds = slc.ds

DECK = ROOT / "decks" / "lightning-war-20260607-122049.txt"
SEED = 20260613
TURNS = 14
SHOW = [5, 6, 7, 8, 9, 10, 12, 14]

ROCKS = {"Arcane Signet": (2, 1), "Fellwar Stone": (2, 1),
         "Talisman of Dominance": (2, 1), "Talisman of Indulgence": (2, 1)}
ENABLERS = {"Leyline of Anticipation", "Vedalken Orrery", "Borne Upon a Wind", "High Fae Trickster"}
AMPS = {"Twinning Staff", "Galvanic Iteration", "Increasing Vengeance", "Reiterate"}
TUTORS = {"Mystical Teachings", "Emeritus of Woe", "Sanar, Unfinished Genius"}
SORCERY_FIN = {"Crackle with Power", "Banefire"}            # need a flash enabler in combat
CANTRIPS = {"Consider": 1, "Faithless Looting": 1, "Frantic Search": 0, "Sink into Stupor": 2,
            "Valakut Awakening": 5, "Waterlogged Teachings": 2, "Snap": 2}
RITUALS = {"Dark Ritual": 2, "Desperate Ritual": 1, "Jeska's Will": 4}


def _powmap(library, commander):
    names = [nm for nm, r in library if "creature" in r["type_line"].lower()]
    names.append(commander)
    raw = slc.load_powers(names)
    return {k: (v if isinstance(v, int) else 1) for k, v in raw.items()}


def goldfish_kill(library, commander, index, powmap, rng):
    def pw(nm):
        return powmap.get(nm.lower(), 1)

    g = slc.Goldfish(library, rng, rocks=ROCKS)
    tbl = slc.Table()
    azula_turn = None
    guttersnipe = stormkiln = goldspan = vivi = False
    fated_x = 0
    vivi_pow = 0
    treasure_bank = 0
    board = ncre = 0
    new_pow = new_cre = 0

    for T in range(1, TURNS + 1):
        board += new_pow; ncre += new_cre; new_pow = new_cre = 0
        g.begin_turn(T)
        g.deploy_rocks()

        # Azula (commander) at 4 — a 4/4 that attacks from next turn
        if azula_turn is None and g.avail >= 4:
            g.avail -= 4; azula_turn = T; new_pow += 4; new_cre += 1
        # Vivi taps for its (grown) power, once per turn
        if vivi and vivi_pow > 0:
            g.avail += vivi_pow

        # deploy creatures cheapest-first (race line: develop the board)
        more = True
        while more:
            more = False
            cands = sorted(((i, r["cmc"], nm) for i, (nm, r) in enumerate(g.hand)
                            if "creature" in r["type_line"].lower()), key=lambda x: x[1])
            for i, cmc, nm in cands:
                if g.avail >= cmc:
                    g.cast(nm, cmc); new_pow += pw(nm); new_cre += 1
                    if nm == "Guttersnipe": guttersnipe = True
                    elif nm == "Storm-Kiln Artist": stormkiln = True
                    elif nm == "Goldspan Dragon": goldspan = True
                    elif nm == "Vivi Ornitier": vivi = True
                    more = True
                    break
        # Fated Firepower (amplifier): enters with X fire counters (+X to all damage)
        if fated_x == 0 and g.has("Fated Firepower") and g.avail >= 5:
            x = min(4, g.avail - 3)
            g.cast("Fated Firepower", 3 + x); fated_x = x

        # noncreature spell velocity (cantrips + a held burn/interaction cast)
        ncast = 0
        for nm, cost in sorted(CANTRIPS.items(), key=lambda x: x[1]):
            while g.has(nm) and g.avail >= cost:
                g.cast(nm, cost); g.draw(1); ncast += 1
        if azula_turn is not None and T > azula_turn:
            ncast += 1
        if vivi and ncast:
            vivi_pow += ncast
        if stormkiln:
            treasure_bank += ncast
        # pinger chip (Guttersnipe 2 + Vivi 1 per cast, each amplified by Fated)
        per_cast = (2 + fated_x if guttersnipe else 0) + (1 + fated_x if vivi else 0)
        if per_cast and ncast:
            tbl.hit_all(per_cast * ncast, T)
            if tbl.done:
                return tbl.decap, tbl.table

        # ---- combat (Azula online, cast on a prior turn) -----------------------
        if azula_turn is not None and T > azula_turn:
            swing = board + ncre * fated_x                   # Fated adds X per attacker
            if swing > 0:
                tbl.hit_focus(swing, T)
                if tbl.done:
                    return tbl.decap, tbl.table
            tre_mana = treasure_bank * (2 if goldspan else 1)
            rit = sum(v for r, v in RITUALS.items() if g.has(r))
            cm = g.avail + 2 + tre_mana + rit
            enabler = any(g.has(e) for e in ENABLERS)
            n_amp = sum(1 for a in AMPS if g.has(a))
            inst = 2 + n_amp                                 # Azula copy + amps
            have_tutor = any(g.has(t) for t in TUTORS) and cm >= 2
            living = [i for i in range(3) if tbl.dmg[i] < tbl.life]
            if not living:
                return tbl.decap, tbl.table
            need_each = max(tbl.life - tbl.dmg[i] for i in living)
            need_one = min(tbl.life - tbl.dmg[i] for i in living)

            def castable(fin):
                return (g.has(fin) or have_tutor) and not (fin in SORCERY_FIN and not enabler)

            killed_table = killed_one = False
            if castable("Crackle with Power"):               # (5X+fated) per instance, x inst
                X = len(living)
                while (5 * X + fated_x) * inst < need_each:
                    X += 1
                if cm >= 3 * X + 2:
                    killed_table = True
            if not killed_table and castable("Comet Storm"):
                X = 1
                while (X + fated_x) * inst < need_each:
                    X += 1
                if cm >= X + 2 + (len(living) - 1):
                    killed_table = True
            for fin, base in (("Electrodominance", 2), ("Banefire", 1)):
                if castable(fin):
                    X = 1
                    while (X + fated_x) * inst < need_one:
                        X += 1
                    if cm >= X + base:
                        killed_one = True
            if killed_table:
                tbl.kill_all(T)
            elif killed_one:
                lo = min(living, key=lambda i: tbl.life - tbl.dmg[i])
                tbl.dmg[lo] = tbl.life; tbl._update(T)
            if tbl.done:
                return tbl.decap, tbl.table

    return tbl.decap, tbl.table


def mode_clock(index, aliases, trials):
    print(f"\n### CLOCK — Lightning War kill-turn goldfish (v2)   trials={trials} seed={SEED}")
    print("    decap = first opponent dead (40) · table = all three. Board + 2 pingers")
    print("    (Guttersnipe/Vivi) chip; a copy-amped X-spell forks the table.\n")
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
    print("\n  Claimed in Summary: Goldfish T6-7. Front-edge odds above are the test.")
    print("  (cf. lw_speed_lab one-cast-from-40 table wipe: 20% by T12 / 70% never — no chip/board.)")


if __name__ == "__main__":
    slc.run_cli(__doc__, {"clock": mode_clock}, default_trials=40000)
