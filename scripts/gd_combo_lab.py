#!/usr/bin/env python3
"""gd_combo_lab.py — The Grand Design (Atraxa): board-INDEPENDENT combo assembly speed.

mode_finishers (gd_speed_lab.py) showed the OVERRUN finisher is now reliably FOUND
(~69% by T6 with the tutor suite) but is BOARD-DEPENDENT — useless on an empty board
after a wrath. find_combos.py flagged the deck is 1-2 owned cards from a board-
independent kill that REUSES the same creature-tutor suite:

  DRAIN COMBO  Karmic Guide + Reveillark + Viscera Seer (free sac outlet) = infinite
               death triggers; Zulaport Cutthroat converts that to infinite drain = win.
               Karmic Guide + Reveillark are ALREADY maindecked; the proposal adds
               Viscera Seer + Zulaport Cutthroat (both owned, ~$1 to buy a fresh copy).

This lab measures P(all four pieces assembled onto the battlefield <= turn T) through
the deck's real mana + tutor + reanimator engine, so the "then suggest the swap"
decision rests on a turn clock, not the presence-only find_combos result.

Loop mechanics (card text verified via card_lookup 2026-06-24):
  Reveillark LTB returns two power<=2 creatures (Karmic Guide is P2); Karmic Guide
  ETB returns a creature from the yard (-> Reveillark). With a free sac outlet
  (Viscera Seer {B}, sac a creature: scry) the pair loops, each loop = >=2 creature
  deaths -> Zulaport drains each opponent. Once all four are in play the loop needs
  NO further mana, so "combo online" = all four on the battlefield.

Enablers MODELLED (every one verified): hardcast from hand; Reanimate {B}/Animate Dead
{1B}/Necromancy {2B} on a binned Karmic Guide or Reveillark (Karmic Guide ETB then
chains Reveillark back free); Buried Alive {2B} bins Karmic Guide+Reveillark (one
Reanimate then returns both); Eladamri's Call {GW} (creature -> hand); Chord of Calling
{X}{G}{G}{G} and Finale of Devastation {X}{G}{G} (creature MV<=X -> battlefield, convoke
IGNORED = conservative); Sidisi exploit (cast {3}{B}{B}, sac itself -> any -> hand);
Birthing Pod (1/turn -> battlefield); Fauna Shaman (1/turn -> hand); Razaketh (hardcast
8 or reanimate -> repeatable any-card tutor, fodder ASSUMED available — generous).

NOT modelled: Defense of the Heart, Grisly Salvage's random bin, Demonic/Vampiric-class
(none in deck). Razaketh's fodder is assumed free, so the full-engine row is an upper-
ish estimate; the draw+hardcast row is the hard floor. Mana is the shared lands +
rocks/dorks/land-ramp floor (see gd_ramp_lab.py).

HEURISTIC, not a rules engine. Trust the shape and the draw-only-vs-full-engine delta.
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
TURNS = 12
SHOW = [3, 4, 5, 6, 7, 8, 10, 12]

# mana engine (shared with gd_ramp_lab) -------------------------------------
ROCKS = {"Sol Ring": (1, 2), "Arcane Signet": (2, 1), "Coalition Relic": (3, 1),
         "Birds of Paradise": (1, 1), "Bloom Tender": (2, 1),
         "Fanatic of Rhonas": (2, 1)}
LAND_RAMP = {"Farseek": 2, "Nature's Lore": 2, "Three Visits": 2,
             "Sakura-Tribe Elder": 2, "Kodama's Reach": 3, "Springbloom Druid": 3,
             "Solemn Simulacrum": 4}

# combo -----------------------------------------------------------------------
KG, REV, VS, ZULA = ("Karmic Guide", "Reveillark", "Viscera Seer", "Zulaport Cutthroat")
PIECES = {KG: 5, REV: 5, VS: 1, ZULA: 2}
REANIM = {"Reanimate": 1, "Animate Dead": 2, "Necromancy": 3}   # cost to reanimate a yard creature
BURIED = "Buried Alive"
ELADAMRI = "Eladamri's Call"
SIDISI = "Sidisi, Undead Vizier"
CHORD = "Chord of Calling"            # X+GGG  -> MV<=X to battlefield (convoke ignored)
FINALE = "Finale of Devastation"      # X+GG   -> MV<=X to battlefield
RAZAKETH = "Razaketh, the Foulblooded"  # in play: repeatable any-card tutor to hand (fodder assumed)
POD = "Birthing Pod"                  # in play: creature MV n -> MV n+1 to battlefield (sorcery)
FAUNA = "Fauna Shaman"                # in play: discard a creature -> creature to hand, 1/turn
ADDS = [VS, ZULA]


def _bin_from_lib(g, nm):
    """Buried Alive: move a named card from the undrawn library into the yard."""
    for i in range(g.ptr, len(g.deck)):
        if g.deck[i][0] == nm:
            g.yard.append(g.deck[i])
            g.deck[i] = g.deck[len(g.deck) - 1]; g.deck.pop()
            return True
    return False


def _bf_fetch(g, nm):
    """Tutor straight to the battlefield (Chord/Finale): pull from library, not hand."""
    for i in range(g.ptr, len(g.deck)):
        if g.deck[i][0] == nm:
            g.deck[i] = g.deck[len(g.deck) - 1]; g.deck.pop()
            return True
    return False


def assemble_turn(library, rng, use_engine=True):
    """One trial. Returns the turn all four combo pieces are on the battlefield, or None."""
    g = core.Goldfish(library, rng, rocks=ROCKS)
    board = set()
    sidisi_used = False
    buried_used = False
    razaketh_on = pod_on = fauna_on = False

    def enter(nm):
        board.add(nm)
        if nm == KG and REV in [y[0] for y in g.yard]:   # Karmic Guide ETB -> Reveillark
            g.take_yard(REV); board.add(REV)

    for T in range(1, TURNS + 1):
        g.begin_turn(T)
        # land-ramp (each +1 land tapped) then rocks/dorks
        moved = True
        while moved:
            moved = False
            for nm, cost in sorted(LAND_RAMP.items(), key=lambda x: x[1]):
                if g.has(nm) and g.avail >= cost:
                    g.cast(nm, cost); g.lands += 1
                    g.avail = g.lands + g.rock_out; moved = True; break
        g.deploy_rocks()

        if use_engine:
            # Buried Alive: bin the two EXPENSIVE pieces only (one Reanimate then chains
            # both back via Karmic Guide's ETB). Zulaport/Viscera stay cheap to hardcast.
            if (not buried_used and g.has(BURIED) and g.avail >= 3
                    and KG not in board and REV not in board):
                g.cast(BURIED, 3); buried_used = True
                for nm in (KG, REV):
                    if nm not in board and not g.in_yard(nm):
                        _bin_from_lib(g, nm)
            # deploy the tutor permanents when drawn & affordable
            if not pod_on and g.has(POD) and g.avail >= 4:
                g.cast(POD, 4); pod_on = True
            if not fauna_on and g.has(FAUNA) and g.avail >= 2:
                g.cast(FAUNA, 2); fauna_on = True
            # Razaketh: hardcast (8) or reanimate from yard -> repeatable any-tutor engine
            if not razaketh_on and g.has(RAZAKETH) and g.avail >= 8:
                g.cast(RAZAKETH, 8); razaketh_on = True
            elif not razaketh_on and g.in_yard(RAZAKETH):
                rs = next((r for r in REANIM if g.has(r) and g.avail >= REANIM[r]), None)
                if rs:
                    g.cast(rs, REANIM[rs]); g.take_yard(RAZAKETH); razaketh_on = True
            # Sidisi: cast + exploit itself -> tutor a missing piece to hand
            if not sidisi_used and g.has(SIDISI) and g.avail >= 5:
                miss = next((p for p in PIECES if p not in board and not g.has(p)), None)
                if miss:
                    g.cast(SIDISI, 5); sidisi_used = True; g.fetch(miss)
            # Razaketh online: tutor every missing piece to hand (pay-2-life + sac fodder
            # assumed available; the deck runs ~22 creatures). Repeatable, mana-free.
            if razaketh_on:
                for p in list(PIECES):
                    if p not in board and not g.has(p):
                        g.fetch(p)
            # Fauna Shaman: 1/turn, {G} + discard a spare creature -> a missing piece to hand
            if fauna_on and g.avail >= 1:
                miss = next((p for p in PIECES if p not in board and not g.has(p)), None)
                spare = next((nm for nm, r in g.hand
                              if "Creature" in r.get("type_line", "") and nm not in PIECES), None)
                if miss and spare:
                    g.avail -= 1; g.discard(spare); g.fetch(miss)
            # Birthing Pod: 1/turn, {1}{G/P} + sac fodder -> cheapest missing piece to battlefield
            if pod_on and g.avail >= 2 and board:
                miss = next((p for p in sorted(PIECES, key=PIECES.get)
                             if p not in board), None)
                if miss and _bf_fetch(g, miss):
                    g.avail -= 2; enter(miss)

        # assembly passes: hardcast / reanimate / tutor each missing piece
        progress = True
        while progress:
            progress = False
            for p, mv in sorted(PIECES.items(), key=lambda x: x[1]):
                if p in board:
                    continue
                # reanimate a binned piece (cheapest; KG chains Reveillark)
                if use_engine and g.in_yard(p):
                    rs = next((r for r in REANIM if g.has(r) and g.avail >= REANIM[r]), None)
                    if rs:
                        g.cast(rs, REANIM[rs]); g.take_yard(p); enter(p)
                        progress = True; break
                # hardcast from hand
                if g.has(p) and g.avail >= mv:
                    g.cast(p, mv); enter(p); progress = True; break
                if not use_engine:
                    continue
                # tutor straight to battlefield (Chord X+3 / Finale X+2)
                if g.has(CHORD) and g.avail >= mv + 3 and _bf_fetch(g, p):
                    g.hand.pop(g.in_hand(CHORD)); g.avail -= mv + 3; enter(p)
                    progress = True; break
                if g.has(FINALE) and g.avail >= mv + 2 and _bf_fetch(g, p):
                    g.hand.pop(g.in_hand(FINALE)); g.avail -= mv + 2; enter(p)
                    progress = True; break
                # tutor to hand (Eladamri) -> cast in a later pass if mana remains
                if g.has(ELADAMRI) and g.avail >= 2 and g.fetch(p):
                    g.hand.pop(g.in_hand(ELADAMRI)); g.avail -= 2; progress = True; break

        if board.issuperset(PIECES):
            return T
    return None


def main():
    index = ds.load_oracle_index()
    aliases = ds.load_reskin_aliases()
    trials = 20000
    base, _ = core.load_parsed(DECK, index, aliases)
    lib = core.build_lib(base, index, [], ADDS)   # + Viscera Seer + Zulaport Cutthroat
    print(f"\n### GD COMBO ASSEMBLY — P(drain combo online <= turn T) %   trials={trials} seed={SEED}")
    print("    pieces = Karmic Guide + Reveillark (in deck) + Viscera Seer + Zulaport (added).")
    print("    online = all four on the battlefield; the loop then needs no more mana.")
    print("    full engine = hardcast + reanimate + Buried + Eladamri/Chord/Finale/Sidisi/")
    print("    Pod/Fauna/Razaketh (Razaketh fodder assumed free = generous).\n")
    print("  build".ljust(34) + "".join(f"{t:>6}" for t in SHOW) + "   median  never")
    for tag, eng in [("draw + hardcast only (floor)", False),
                     ("full engine (tutors+reanim)", True)]:
        rng = random.Random(SEED)
        res = [(assemble_turn(lib, rng, use_engine=eng),) for _ in range(trials)]
        never = 100.0 * sum(1 for r in res if r[0] is None) / trials
        print(core.row(tag, core.cum(res, 0, SHOW), SHOW, width=32)
              + f"   {core.median(res, 0)}   {never:.0f}%")
    print("\n  Read against mode_finishers' overrun line (~69% found by T6, but BOARD-dependent).")
    print("  The combo is the board-INDEPENDENT second axis; this is its assembly clock.")


if __name__ == "__main__":
    main()
