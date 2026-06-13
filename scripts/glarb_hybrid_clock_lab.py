#!/usr/bin/env python3
"""glarb_hybrid_clock_lab.py — real kill-turn clock for the Hybrid Glarb direction.

Follow-up to glarb_compare_lab.py, which used a draw-only availability model and so
UNDER-counted every combo (no digging). That is wrong for Glarb specifically: the
commander IS a selection engine ("look at the top card any time; play lands and cast
MV>=4 from the top; {T}: Surveil 2"), so filtering toward the combo is the core plan.
This lab models that dig explicitly and reports the real combo kill-turn.

DECK: decks/considering/glarb-hybrid-20260613.txt (#3 Strong Glarb shell + Demonic
Consultation + Thassa's Oracle as a fast, low-mana, board-independent finish).
Two variants (the user is OK trading interaction for redundancy/speed):
  BASE       1 enabler (Consult) + 1 finisher (Thoracle)
  REDUNDANT  +Tainted Pact (2nd library-exile enabler) +Jace, Wielder of Mysteries
             (2nd finisher), -Submerge -Make an Example (soft interaction)

KILL = the Thoracle combo (decap = table by construction — it wins the game):
  cast Thassa's Oracle ({U}{U}); in response Demonic Consultation / Tainted Pact
  ({B}/{1}{B}) exiles your library; Thoracle ETB sees an empty library -> you win.
  ~3 mana. Jace line: Consult/Pact empties library, then any draw wins (~5 mana w/ Jace).
  All win-cons card-text-verified via card_lookup.py 2026-06-13.

THE DIG MODEL (the point of this lab; explicit + tunable):
  Each turn the deck "sees" cards toward its pieces = 1 (draw) + Glarb surveil 2 (once
  Glarb is out, ~T3) + Sylvan Library 2 + Sensei's Top 1 (when each is in play). Pieces
  and tutors among those go to hand; the rest are filtered away (advance the pointer —
  this is the surveil/Top/fetch thinning that makes the next looks hit pieces sooner).
  Tutors then fetch a missing piece for mana (Vampiric/Demonic to hand; GSZ/Chord/Finale
  fetch Thoracle the creature). Win when an enabler + a finisher + the line's mana are up.

HEURISTIC, NOT a rules engine. Mana = lands + rocks + dorks floor; Glarb cast at 3.
Surveil modelled as look-and-filter (optimistic: assumes you keep pieces, bin junk).
No opposing interaction (goldfish) — protection availability reported SEPARATELY so you
can see how defensible the combo turn is. Trust the shape + the dig sensitivity.

Data: collection/oracle-cards.json   ·   Compare: scripts/glarb_compare_lab.py
"""
import importlib.util
import random
from pathlib import Path

ROOT = Path(__file__).parent.parent
_spec = importlib.util.spec_from_file_location("speed_lab_core", Path(__file__).parent / "speed_lab_core.py")
core = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(core)
ds = core.ds

DECK = ROOT / "decks" / "considering" / "glarb-hybrid-20260613.txt"
DECK_FINAL = ROOT / "decks" / "considering" / "glarb-hybrid-final-20260613.txt"
SEED = 20260613
TURNS = 12
SHOW = [3, 4, 5, 6, 7, 8, 10, 12]

ROCKS = {"Sol Ring": (1, 2)}                     # the hybrid's only true rock
DORKS = {"Birds of Paradise": 1, "Delighted Halfling": 1, "Lotus Cobra": 1,
         "Utopia Sprawl": 1, "Wild Growth": 1}   # ~1 mana each (turn after, conservative)
RAMP = {"Farseek": (2, 1), "Nature's Lore": (2, 1), "Skyshroud Claim": (4, 2)}

ENABLERS_BASE = {"Demonic Consultation"}
FINISH_BASE = {"Thassa's Oracle"}
TUT_HAND = {"Demonic Tutor": 2, "Vampiric Tutor": 1}          # fetch a piece to hand
TUT_CREATURE = {"Green Sun's Zenith": 4, "Chord of Calling": 5,
                "Finale of Devastation": 5}                   # fetch Thoracle (creature)
GLARB = "Glarb, Calamity's Augur"


def trial(library, rng, enablers, finishers):
    g = core.Goldfish(library, rng, rocks=ROCKS)
    tbl = core.Table()
    glarb = sylvan = top = False
    dork_mana = 0
    hand_pieces = set()          # enablers/finishers/tutors held
    PIECES = enablers | finishers | set(TUT_HAND) | set(TUT_CREATURE)

    def grab_from_hand():
        for nm, _ in list(g.hand):
            if nm in PIECES:
                hand_pieces.add(nm)

    def look_filter(n):
        """Surveil/Sylvan/Top: scan the next n library cards; keep pieces/tutors, bin
        the rest (advance pointer). Models filtering toward the combo."""
        kept = 0
        for _ in range(n):
            if g.ptr >= len(g.deck):
                break
            nm = g.deck[g.ptr][0]
            if nm in PIECES:
                hand_pieces.add(nm); g.hand.append(g.deck[g.ptr])
            g.ptr += 1                          # binned or taken either way
            kept += 1

    def have_win():
        have_e = bool(hand_pieces & enablers)
        have_f = bool(hand_pieces & finishers)
        # Thoracle line = 3 mana; Jace line = 5
        cost = 3 if "Thassa's Oracle" in (hand_pieces & finishers) else 5
        return have_e and have_f and g.avail >= cost

    for T in range(1, TURNS + 1):
        g.begin_turn(T)
        g.deploy_rocks()
        g.add_mana(dork_mana)
        # ramp
        for nm, (cost, n) in RAMP.items():
            while g.has(nm) and g.avail >= cost:
                g.cast(nm, cost); g.lands += n; g.avail += n
        for nm in DORKS:
            if g.has(nm) and g.avail >= 1:
                g.cast(nm, 1); dork_mana += 1
        # Glarb / Sylvan / Top
        if not glarb and g.avail >= 3:
            g.avail -= 3; glarb = True
        if not sylvan and g.cast("Sylvan Library", 2):
            sylvan = True
        if not top and g.cast("Sensei's Divining Top", 1):
            top = True
        # ---- DIG: draw already happened; now surveil/Sylvan/Top filtering ----
        grab_from_hand()
        look = (2 if glarb else 0) + (2 if sylvan else 0) + (1 if top else 0)
        if look:
            look_filter(look)
        # ---- tutors: fetch a missing piece for mana ----
        missing = None
        if not (hand_pieces & enablers):
            missing = next(iter(enablers))
        elif not (hand_pieces & finishers):
            missing = "Thassa's Oracle" if "Thassa's Oracle" in finishers else next(iter(finishers))
        if missing:
            done = False
            for nm, cost in TUT_HAND.items():               # Vampiric/Demonic -> piece to hand
                if nm in hand_pieces and g.avail >= cost and g.fetch(missing):
                    g.avail -= cost
                    hand_pieces.discard(nm); hand_pieces.add(missing)
                    done = True
                    break
            if not done and missing == "Thassa's Oracle":   # GSZ/Chord/Finale -> Thoracle (creature)
                for nm, cost in TUT_CREATURE.items():
                    if nm in hand_pieces and g.avail >= cost and g.fetch("Thassa's Oracle"):
                        g.avail -= cost; hand_pieces.discard(nm); hand_pieces.add("Thassa's Oracle")
                        break
        # ---- win check ----
        if have_win():
            tbl.kill_all(T)
            return tbl.decap, tbl.table
    return tbl.decap, tbl.table


def protection_curve(library, trials, rng):
    """P(>=1 protection piece in hand by T) — how defensible the combo turn is.
    Includes the FINAL build's free counters (Force of Will/Negation, Pact of Negation),
    which are absent from BASE so its curve is lower / soft-only."""
    prot = ["Force of Will", "Force of Negation", "Pact of Negation",   # FINAL free counters
            "Deadly Rollick", "Force of Vigor", "Mindbreak Trap",
            "Venser, Shaper Savant", "Boseiju, Who Endures", "Otawara, Soaring City"]
    drawn, _ = core.simulate_groups(library, [prot], [], trials, rng, TURNS)
    return drawn


def run(library, rng, trials, enablers, finishers):
    res = [trial(library, rng, enablers, finishers) for _ in range(trials)]
    return res


def mode_clock(index, aliases, trials):
    print(f"\n### GLARB HYBRID — real combo kill-turn (dig modelled)   trials={trials} seed={SEED}")
    print("    Thoracle combo = decap = table by construction. Dig = draw + Glarb surveil 2")
    print("    + Sylvan 2 + Top 1 (filter to pieces). Compare to compare-lab's no-dig floor (14% T6).\n")
    base, _ = core.load_parsed(DECK, index, aliases)
    final, _ = core.load_parsed(DECK_FINAL, index, aliases)
    redun = core.build_lib(base, index, ["Submerge", "Make an Example"],
                           ["Tainted Pact", "Jace, Wielder of Mysteries"])
    variants = [
        ("BASE (Consult + Thoracle)", base, ENABLERS_BASE, FINISH_BASE),
        ("REDUNDANT (+Pact +Jace)", redun,
         ENABLERS_BASE | {"Tainted Pact"}, FINISH_BASE | {"Jace, Wielder of Mysteries"}),
        ("FINAL (redundant + 3 free counters)", final,
         ENABLERS_BASE | {"Tainted Pact"}, FINISH_BASE | {"Jace, Wielder of Mysteries"}),
    ]
    print("  metric".ljust(46) + "".join(f"{t:>6}" for t in SHOW) + "   median")
    for tag, lib, en, fi in variants:
        res = run(lib, random.Random(SEED), trials, en, fi)
        print(core.row(f"{tag}  combo win", core.cum(res, 0, SHOW), SHOW) + f"   {core.median(res, 0)}")
        never = 100.0 * sum(1 for d, _ in res if d is None) / trials
        print(f"    never-in-{TURNS}: {never:.0f}%")
    print()
    for tag, lib in (("BASE  protection (soft only)", base),
                     ("FINAL protection (+free counters)", final)):
        prot = protection_curve(lib, trials, random.Random(SEED + 5))
        print(core.row(tag, {t: prot[t] for t in SHOW}, SHOW))
    print("    (FINAL adds Force of Will/Negation + Pact of Negation = FREE protection for the combo turn)")


if __name__ == "__main__":
    core.run_cli(__doc__, {"clock": mode_clock})
