#!/usr/bin/env python3
"""wb_mana_engine_lab.py — Zero-Sum Game: does the Enduring Vitality x Badgermole
Cub mana engine pull the mana-gated axis (Line B) earlier?

WHY THIS LAB. 2026-06-30 the user asked whether Badgermole Cub, Enduring Vitality
and Pest Infestation were considered, noting (correctly) that Badgermole is
SYNERGISTIC with Enduring Vitality. card_lookup-verified text:

  Enduring Vitality {1}{G}{G}, Enchantment Creature, Vigilance, 3/3: "Creatures
    you control have '{T}: Add one mana of any color.'" Dies -> returns as an
    enchantment (still granting the mana). => turns the whole go-wide board into
    mana dorks; resilient to a wrath.
  Badgermole Cub {1}{G}, 2/2: "Whenever you tap a creature for mana, add an
    additional {G}." (Ruling: triggers only on a {T} mana ability of a creature —
    so it fires on dorks AND on Enduring Vitality's granted ability, but NOT on
    convoke / "tap an untapped creature" costs.)

  TOGETHER, with Enduring Vitality out, EVERY non-sick creature taps for 1 (any)
  + 1 {G} from Badgermole = 2 mana per creature. In a token deck that scales.

COMBO STATUS (find_combos.py / Commander Spellbook, 2026-06-30): adding
{Enduring Vitality, Badgermole Cub, Pest Infestation} to the list produces ZERO
new COMPLETE combos (still 14). The pair is a missing-1 away from an infinite —
Badgermole + Enduring Vitality + *Pili-Pala* = infinite colored mana (combo
1247-6006-7008) — but Pili-Pala is not in the deck. So as a PAIR this is RAMP,
not a wincon. This lab measures that ramp on the one mana-gated axis.

WHICH AXIS. The primary lifeloop (wb_clock_lab, T9) is cheap (3-5 MV halves) and
is already known flat-to-fast-mana (its gcswap row: -Demonic +Mana Vault is
flat-to-worse at every turn). The mana-gated axis is LINE B, the affinity
magecraft infinite (wb_storm_lab): it needs the 8-MV commander + a payoff (Onyx
6 / Apprentice 2) + Sprout Swarm castable + board>=4. THAT is where a
board-scaling mana engine should bite, so that is what this A/B isolates.

MODEL (extends the wb_storm_lab assembly model; same OPTIMISM caveats:
unblocked, colour-blind floor, rocks tap same turn — trust the A/B DELTA, not
the absolute turns). Engine mana is added at the start of each turn from
creatures that were already in play last turn (prev_board) so summoning
sickness on the {T} abilities is respected:

  nondork_prev = prev_board - dork_out            (tokens, cmdr, payoff, EV, Cub)
  EV active   -> + nondork_prev                   (non-dorks now tap for 1)
  Cub active  -> + (prev_board if EV else dork_out)  (+1 {G} per creature tapped)
  => EV+Cub  ~= 2 * prev_board mana per turn once the board is wide.

EV/Cub are cast when drawn (never tutored for — conservative; understates them).
The A/B REMOVES are model-inert placeholders (Toxic Deluge / Pernicious Deed are
not used by the Line-B model) chosen only to hold library size at 100 — they are
NOT a recommended real cut; a real include trades against the Interaction axis.

Data: collection/oracle-cards.json    Run: python scripts/wb_mana_engine_lab.py
Companion: wb_storm_lab.py (baseline Line B), wb_clock_lab.py (lifeloop T9).
"""
import importlib.util
import random
from pathlib import Path

ROOT = Path(__file__).parent.parent
_spec = importlib.util.spec_from_file_location(
    "speed_lab_core", Path(__file__).parent / "speed_lab_core.py")
slc = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(slc)
ds = slc.ds

DECK = ROOT / "decks" / "zero-sum-game-20260619.txt"
SEED = 20260630
TURNS = 14
SHOW = [4, 5, 6, 7, 8, 9, 10, 12]
ROCKS = {"Sol Ring": (1, 2), "Arcane Signet": (2, 1), "Jet Medallion": (2, 1)}
DORKS = {"Birds of Paradise", "Llanowar Elves", "Elvish Mystic", "Fyndhorn Elves",
         "Boreal Druid", "Arbor Elf", "Elves of Deep Shadow", "Delighted Halfling"}
TOKEN_MAKERS = {"Bitterblossom": False, "Tendershoot Dryad": True,   # name -> makes GREEN
                "Saproling Migration": True, "Hornet Queen": True, "Sprout Swarm": True}
ANY_TUTORS = {"Demonic Tutor": 2, "Beseech the Queen": 3, "Increasing Ambition": 5,
              "Dark Petition": 3, "Diabolic Intent": 2}
CREATURE_TUTORS = {"Chord of Calling", "Finale of Devastation", "Nature's Rhythm"}
EV = "Enduring Vitality"
CUB = "Badgermole Cub"


def run(library, trials, label, engine=False):
    """Line B (Sprout Swarm INFINITE) assembly clock. engine=True deploys EV/Cub
    when drawn and adds their board-scaling mana. kill_all on assembly."""
    rng = random.Random(SEED)
    out = []
    for _ in range(trials):
        g = slc.Goldfish(library, rng, rocks=ROCKS)
        tbl = slc.Table()
        board = 0; green = 0; dork_out = 0; cmdr = False; payoff_in = False
        prev_board = 0
        ev_in = ev_T = 0; cub_in = cub_T = 0
        for T in range(1, TURNS + 1):
            g.begin_turn(T); g.deploy_rocks(); g.add_mana(dork_out)
            # --- engine mana from creatures already in play last turn ---
            if engine:
                ev_active = bool(ev_in) and ev_T < T
                cub_active = bool(cub_in) and cub_T < T
                nondork_prev = max(0, prev_board - dork_out)
                extra = (nondork_prev if ev_active else 0)
                if cub_active:
                    extra += prev_board if ev_active else dork_out
                g.add_mana(extra)
            prog = True
            while prog:
                prog = False
                for nm in DORKS:
                    if g.has(nm) and g.cast(nm, 1):
                        board += 1; green += 1; dork_out += 1; prog = True
                for nm, is_green in TOKEN_MAKERS.items():
                    if nm == "Sprout Swarm":
                        continue
                    if g.has(nm) and g.cast(nm):
                        board += 2; green += (2 if is_green else 0); prog = True
                if engine:
                    if not ev_in and g.has(EV) and g.cast(EV, 3):
                        ev_in = 1; ev_T = T; board += 1; green += 1; prog = True
                    if not cub_in and g.has(CUB) and g.cast(CUB, 2):
                        cub_in = 1; cub_T = T; board += 1; green += 1; prog = True
                if not cmdr:
                    c = max(2, 8 - board)
                    if g.avail >= c:
                        g.pay(c); cmdr = True; board += 1; green += 1; prog = True
                for nm in ("Witherbloom Apprentice", "Professor Onyx"):
                    cost = 2 if nm == "Witherbloom Apprentice" else 6
                    if not payoff_in and g.has(nm) and g.cast(nm, cost):
                        payoff_in = True; board += 1; prog = True
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
            sprout_ready = g.has("Sprout Swarm") and board >= 4 and green >= 1
            if cmdr and payoff_in and sprout_ready:
                tbl.kill_all(T)
            prev_board = board
            if tbl.done:
                break
        out.append((tbl.decap, tbl.table))
    print(slc.row(label, slc.cum(out, 1, SHOW), SHOW)
          + f"   med {slc.median(out, 1)} · never {slc.never_pct(out, 1, trials):.0f}%")


def mode_engine(index, aliases, trials):
    base, _ = slc.load_parsed(DECK, index, aliases, warn=False)
    both = slc.build_lib(base, index, ["Toxic Deluge", "Pernicious Deed"], [EV, CUB])
    ev_only = slc.build_lib(base, index, ["Toxic Deluge"], [EV])
    cub_only = slc.build_lib(base, index, ["Pernicious Deed"], [CUB])
    print("=" * 80)
    print(f"LINE B assembly clock — EV x Badgermole mana engine A/B   {trials} trials")
    print("  (the mana-GATED axis; lifeloop T9 is cheap & flat-to-mana, see wb_clock_lab gcswap)")
    print("  table-kill cum % by turn:".ljust(46) + "".join(f"{t:6d}" for t in SHOW))
    run(base, trials, "as-built (no engine)", engine=False)
    run(cub_only, trials, "+ Badgermole Cub only", engine=True)
    run(ev_only, trials, "+ Enduring Vitality only", engine=True)
    run(both, trials, "+ both (EV x Cub)", engine=True)
    print("\n  Removes (Toxic Deluge / Pernicious Deed) are model-INERT placeholders to hold")
    print("  library at 100 — NOT a recommended cut. Engine cards cast-when-drawn, never")
    print("  tutored (conservative). Trust the A/B delta vs as-built, not the absolute turn.")


if __name__ == "__main__":
    slc.run_cli(__doc__, {"engine": mode_engine}, default_trials=20000)
