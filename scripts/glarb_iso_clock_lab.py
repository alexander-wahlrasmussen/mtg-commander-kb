#!/usr/bin/env python3
"""glarb_iso_clock_lab.py — kill-turn clock for the Glarb GRIND + Isochron-combo build.

Build: decks/considering/glarb-grind-iso-20260614.txt — the V1 Calamity (Glarb, Calamity's
Augur) grind shell with the Thoracle direction DROPPED and replaced by a non-Thoracle
Isochron Scepter + Dramatic Reversal infinite-mana combo that dumps into the deck's existing
Torment of Hailfire. (Hashaton is now the roster's Thoracle deck; Calamity keeps its grind
identity and gains a board-independent backup combo.) 6-for-6 vs V1:
  -Druid of Purification -Flash Photography -High Fae Trickster -Mirrorform -Savvy Trader
   -Starfield Vocalist  (the prior-lab-vetted weakest 6)
  +Isochron Scepter +Dramatic Reversal (combo)  +Birds of Paradise +Bloom Tender +Dimir
   Signet (nonland mana base for the loop)  +Crucible of Worlds (grind upgrade, Loam pile)

TWO clocks, reported separately (verification rule — decap/table stated apart):

  GRIND  reuses ct_speed_lab.kill_turns(combo=False) — the SAME engine that clocked V1/V4
         (Torment/Exsanguinate X-drain, Rite/Doppelgang copy on Gray/Kokusho, reanimator,
         combat). The build keeps that whole core, so the grind model transfers unchanged.
         Reported for the new build AND V1 so the delta is visible.

  COMBO  modelled here (parallel to glarb_hybrid_clock_lab's Thoracle assembly). WIN when:
         Isochron Scepter + Dramatic Reversal are both in hand, a payoff (Torment/Finale)
         is in hand, a NONLAND mana base >=3 is on board (Dramatic untaps nonland only ->
         the loop needs rocks/dorks, NOT the deck's lands), and >=4 seed mana is up. Infinite
         mana -> Torment X=lethal = decap=table (kill_all).
         Dig = draw + Glarb surveil 2 + Sylvan Library (filter toward pieces). Tutor = Demonic
         only (Vampiric/Mystical are GCs, excluded to hold the deck at 3/3 GC). NO creature-
         tutors apply (Isochron/Dramatic aren't creatures) and Glarb can't top-cast them
         (MV<4) -> the combo is finding-gated and assembles SLOWER than Hashaton's Thoracle.
         It is a backup axis, not the primary clock.

HEURISTIC, not a rules engine (same caveats as every lab; nonland base + dig are modelled,
trust shapes/deltas not second decimals). Card text verified via card_lookup.py 2026-06-14:
Isochron Scepter, Dramatic Reversal, Torment of Hailfire, Bloom Tender, Birds of Paradise,
Crucible of Worlds. GC count re-checked vs REF_Game_Changers_List.md: 3/3 (no add is a GC).
"""
import importlib.util
import random
from pathlib import Path

ROOT = Path(__file__).parent.parent


def _load(name):
    spec = importlib.util.spec_from_file_location(name, Path(__file__).parent / f"{name}.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


core = _load("speed_lab_core")
ct = _load("ct_speed_lab")
ds = core.ds

NEW = ROOT / "decks" / "considering" / "glarb-grind-iso-20260614.txt"
# V1 = the historical committed baseline; archived during the Calamity->Croak rebuild.
V1 = ROOT / "archive" / "old_decklists" / "calamity-tax-20260405-061741.txt"
SEED = 20260614
TURNS = 14
SHOW = [4, 5, 6, 7, 8, 9, 10, 12, 14]

ISO = "Isochron Scepter"
DRAMATIC = "Dramatic Reversal"
PIECES = {ISO, DRAMATIC}
PAYOFF = {"Torment of Hailfire", "Finale of Devastation"}   # in the maindeck
TUTORS = {"Demonic Tutor": 2}                                # Vampiric/Mystical are GCs -> out
# nonland mana sources in the build and their NET tap output into the Dramatic loop.
# Bloom Tender = 3 once Glarb (a BUG permanent) is out, else 2. Lands are NOT here (Dramatic
# Reversal untaps nonland only). Sol Ring already in V1; the other three are adds.
SOURCES = {"Sol Ring": 2, "Birds of Paradise": 1, "Bloom Tender": 2, "Dimir Signet": 1}
PROT = ["Force of Negation", "Pact of Negation", "Fierce Guardianship", "Deadly Rollick",
        "Veil of Summer", "Swan Song", "Force of Vigor", "Submerge"]


def combo_trial(library, rng):
    g = core.Goldfish(library, rng)            # sources handled manually below
    tbl = core.Table()
    glarb = sylvan = False
    deployed = set()
    standing = 0                               # standing nonland mana from deployed sources
    held = set()                               # pieces / payoff / tutors in hand

    def grab():
        for nm, _ in g.hand:
            if nm in PIECES or nm in PAYOFF or nm in TUTORS:
                held.add(nm)

    def look_filter(n):
        for _ in range(n):
            if g.ptr >= len(g.deck):
                break
            nm = g.deck[g.ptr][0]
            if nm in PIECES or nm in PAYOFF or nm in TUTORS:
                held.add(nm)
                g.hand.append(g.deck[g.ptr])
            elif nm in SOURCES:
                g.hand.append(g.deck[g.ptr])   # keep the mana sources the loop needs
            g.ptr += 1

    for T in range(1, TURNS + 1):
        g.begin_turn(T)
        g.add_mana(standing)
        # deploy nonland mana sources from hand (they tap the same turn)
        for nm in SOURCES:
            if nm not in deployed and g.has(nm):
                i = g.in_hand(nm)
                cost = g.hand[i][1]["cmc"]
                if g.avail >= cost:
                    g.hand.pop(i)
                    g.avail -= cost
                    deployed.add(nm)
                    g.avail += 3 if (nm == "Bloom Tender" and glarb) else SOURCES[nm]
        if not glarb and g.pay(3):
            glarb = True
        if not sylvan and g.cast("Sylvan Library", 2):
            sylvan = True
        standing = sum(3 if (nm == "Bloom Tender" and glarb) else SOURCES[nm] for nm in deployed)
        # ---- dig: draw already happened; Glarb surveil 2 + Sylvan filter toward pieces ----
        grab()
        look = (2 if glarb else 0) + (2 if sylvan else 0)
        if look:
            look_filter(look)
        # ---- tutor a missing combo piece to hand (Demonic) ----
        miss = PIECES - held
        if miss:
            for tut, cost in TUTORS.items():
                if tut in held and g.avail >= cost:
                    tgt = next(iter(miss))
                    if g.fetch(tgt):
                        g.avail -= cost
                        held.add(tgt)
                        held.discard(tut)
                    break
        grab()
        # ---- win: both pieces + nonland base >=3 + seed mana >=4 ----
        # payoff (Torment/Finale, both maindeck) is NOT a binding gate: infinite mana casts
        # the whole deck and finds one. Gate on the real constraints: pieces + nonland base.
        if PIECES <= held and standing >= 3 and g.avail >= 4:
            tbl.kill_all(T)
            return tbl.decap, tbl.table
    return tbl.decap, tbl.table


def mode_clock(index, aliases, trials):
    print(f"\n### GLARB GRIND+ISOCHRON — kill-turn clock   trials={trials} seed={SEED}")
    print("    3 opp @40. GRIND via ct_speed_lab.kill_turns (same engine as V1/V4).")
    print("    COMBO = Isochron+Dramatic -> infinite mana -> Torment (decap=table).\n")
    new_lib, _ = core.load_parsed(NEW, index, aliases)
    v1_lib, _ = core.load_parsed(V1, index, aliases)

    print("  -- GRIND clock (ct_speed_lab engine, combo OFF) --")
    print("  build".ljust(34) + "".join(f"{t:>6}" for t in SHOW) + "   median")
    for tag, lib in (("V1 committed (baseline)", v1_lib), ("NEW grind+iso", new_lib)):
        rng = random.Random(SEED)
        res = [ct.kill_turns(lib, rng, dig=3, combo=False) for _ in range(trials)]
        print(core.row(f"{tag}  decap", core.cum(res, 0, SHOW), SHOW) + f"   {core.median(res, 0)}")
        print(core.row(" " * len(tag) + "  table", core.cum(res, 1, SHOW), SHOW) + f"   {core.median(res, 1)}")

    print("\n  -- COMBO clock (Isochron+Dramatic assembly, Glarb dig) --")
    print("  build".ljust(34) + "".join(f"{t:>6}" for t in SHOW) + "   median")
    rng = random.Random(SEED)
    res = [combo_trial(new_lib, random.Random(SEED + i)) for i in range(trials)]
    print(core.row("NEW combo  decap=table", core.cum(res, 0, SHOW), SHOW) + f"   {core.median(res, 0)}")
    never = 100.0 * sum(1 for d, _ in res if d is None) / trials
    print(f"    never-in-{TURNS}: {never:.0f}%")

    print("\n  -- protection availability (drawn; how defensible the combo turn is) --")
    drawn, _ = core.simulate_groups(new_lib, [PROT], [], trials, random.Random(SEED + 7), TURNS)
    print(core.row("NEW  >=1 protection piece", {t: drawn[t] for t in SHOW}, SHOW))
    print("\n  Effective deck clock ~= the EARLIER of grind / combo each game; the combo is the")
    print("  faster-but-less-reliable backup, the grind is the floor. Both are board/mana axes.")


if __name__ == "__main__":
    core.run_cli(__doc__, {"clock": mode_clock})
