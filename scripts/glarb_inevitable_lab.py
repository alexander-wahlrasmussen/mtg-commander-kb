#!/usr/bin/env python3
"""glarb_inevitable_lab.py — assembly clock for the "inevitable" topdeck-combo
Glarb build. PROMOTED to the active roster 2026-07-01 as Croak and Dagger
(decks/croak-and-dagger-20260701.txt) — DECK repointed off the retired candidate
per the lab-staleness rule (a lab that pins a superseded .txt rots).

WHY: the deployed grind deck wins with a single mana-gated Torment (~T13 decap,
table never-in-horizon — the honest dig=0 clock). This build replaces that fragile
haymaker with the GLARB4EVA "Topdeck Matters" loop, whose strength is REDUNDANCY:

  LOOP     Sensei's Divining Top  ({T}: draw, put Top on top of library)
  ENABLER  any "cast spells from the top, no MV restriction" effect — Bolas's
           Citadel / One with the Multiverse / Fortune Teller's Talent (lvl 2) /
           The Reality Chip. Recast Top off the top each iteration → draw the deck.
  PAYOFF   Aetherflux Reservoir (gain life/cast, "pay 50: deal 50") OR Ancient
           Cellarspawn (drain on each under-costed cast).

Once LOOP + any ENABLER + any PAYOFF are all in play, the loop executes and the
table dies (decap == table by construction, like a Thoracle line). So the clock
is an ASSEMBLY clock: what turn do all three categories hit the battlefield.

THE DIG (honest — selection, NOT raw draw; the 2026-06-29 ct_speed_lab fix):
  each turn the deck SEES toward its pieces = draw 1 + Glarb surveil 2 (once out)
  + Sylvan Library 2 + Sensei's Top 1 + Oracle of Mul Daya 1 (each when in play).
  Pieces among those go to hand; the rest are filtered away (advance the pointer).
  This is net-zero on card count — it models surveil/Top filtering, not extra cards.
  Tutors then fetch a missing piece for mana (Insidious Dreams / Emergent Ultimatum
  multi; Scheming Symmetry single; GSZ/Chord/Finale fetch the creature pieces).

CONSERVATISM (deliberately under-claims): mana = lands + rocks + dorks + ramp floor
ONLY — Cabal Coffers / Urborg are NOT modelled, so real deploy mana is HIGHER and
the real clock a touch FASTER than printed. Heuristic, goldfish, no opposing
interaction — protection availability is reported SEPARATELY (the combo turn's
defensibility, which matters against the Abolisher pod). Trust shape + the dig
sensitivity, not the second decimal.

Compare: current single-Torment plan = ~T13 decap (ct_speed_lab, honest dig=0).
Data: collection/oracle-cards.json
"""
import importlib.util
import random
from pathlib import Path

ROOT = Path(__file__).parent.parent
_spec = importlib.util.spec_from_file_location("speed_lab_core", Path(__file__).parent / "speed_lab_core.py")
core = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(core)
ds = core.ds

DECK = ROOT / "decks" / "croak-and-dagger-20260701.txt"
SEED = 20260630
TURNS = 14
SHOW = [4, 5, 6, 7, 8, 9, 10, 12]

ROCKS = {"Sol Ring": (1, 2)}
DORKS = {"Birds of Paradise": 1, "Lotus Cobra": 1}                      # ~1 mana, turn after
RAMP = {"Farseek": (2, 1), "Nature's Lore": (2, 1), "Three Visits": (2, 1),
        "Skyshroud Claim": (4, 2), "Open the Way": (4, 2), "Hour of Promise": (5, 2)}
EXTRA_LAND = {"Exploration", "Azusa, Lost but Seeking", "Oracle of Mul Daya"}  # +1 land drop/turn

LOOP = {"Sensei's Divining Top": 1}
# enabler cost = FUNCTIONAL mana to make it cast-from-top (Fortune Teller's needs lvl2,
# Reality Chip needs to attach) — conservative single-number deploy cost.
ENABLERS = {"Bolas's Citadel": 6, "One with the Multiverse": 8,
            "Fortune Teller's Talent": 5, "The Reality Chip": 5}
PAYOFFS = {"Aetherflux Reservoir": 4, "Ancient Cellarspawn": 3}
TUT_MULTI = {"Insidious Dreams": 3, "Emergent Ultimatum": 6}            # fetch up to 2 missing
TUT_ONE = {"Scheming Symmetry": 1}                                      # fetch 1 missing
TUT_CREATURE = {"Green Sun's Zenith": 4, "Chord of Calling": 5, "Finale of Devastation": 6}
CREATURE_PIECES = {"Ancient Cellarspawn", "The Reality Chip"}           # fetchable by Chord/Finale
GLARB = "Glarb, Calamity's Augur"


def trial(library, rng, enablers, payoffs, tut_multi, tut_one, tut_creature, dig_bonus=0):
    g = core.Goldfish(library, rng, rocks=ROCKS)
    tbl = core.Table()
    glarb = sylvan = top = oracle = False
    dork_mana = 0
    in_play = set()
    PIECES = set(LOOP) | set(enablers) | set(payoffs) | set(tut_multi) | set(tut_one) | set(tut_creature)
    ALL_TUTORS = dict(tut_multi); ALL_TUTORS.update(tut_one)

    def grab():
        pass  # pieces are read from g.hand directly via g.has()

    def look_filter(n):
        for _ in range(n):
            if g.ptr >= len(g.deck):
                return
            nm = g.deck[g.ptr][0]
            if nm in PIECES:
                g.hand.append(g.deck[g.ptr])
            g.ptr += 1

    def missing_categories():
        m = []
        if not (set(LOOP) & in_play):
            m.append(("loop", LOOP))
        if not (set(enablers) & in_play):
            m.append(("enabler", enablers))
        if not (set(payoffs) & in_play):
            m.append(("payoff", payoffs))
        return m

    def deploy():
        """Cast pieces from hand cheapest-first into play (multi-turn assembly)."""
        progressed = True
        while progressed:
            progressed = False
            cand = []
            for cat in (LOOP, enablers, payoffs):
                for nm, cost in cat.items():
                    if g.has(nm) and nm not in in_play and g.avail >= cost:
                        cand.append((cost, nm))
            for cost, nm in sorted(cand):
                if g.has(nm) and g.avail >= cost:
                    g.cast(nm, cost); in_play.add(nm); progressed = True
                    break

    for T in range(1, TURNS + 1):
        g.begin_turn(T)
        g.deploy_rocks()
        g.add_mana(dork_mana)
        # extra land drop (Exploration / Azusa / Oracle): play one more land if held
        if any(nm in in_play or g.has(nm) for nm in EXTRA_LAND):
            li = next((i for i, (_, r) in enumerate(g.hand) if ds.is_land(r)), None)
            if li is not None:
                g.hand.pop(li); g.lands += 1; g.avail += 1
        # ramp spells
        for nm, (cost, n) in RAMP.items():
            while g.has(nm) and g.avail >= cost:
                g.cast(nm, cost); g.lands += n; g.avail += n
        # dorks
        for nm in DORKS:
            if g.has(nm) and g.avail >= 1:
                g.cast(nm, 1); dork_mana += 1
        # engine pieces that double as dig: Glarb (3), Sylvan (2), Oracle (cmc), Top (1)
        if not glarb and g.avail >= 3:
            g.avail -= 3; glarb = True
        if not sylvan and g.cast("Sylvan Library", 2):
            sylvan = True
        if not oracle and g.cast("Oracle of Mul Daya", 4):
            oracle = True
        if "Sensei's Divining Top" not in in_play and g.cast("Sensei's Divining Top", 1):
            in_play.add("Sensei's Divining Top"); top = True
        # ---- DIG: selection (filter toward pieces), net-zero on card count ----
        look = (2 if glarb else 0) + (2 if sylvan else 0) + (1 if top else 0) + (1 if oracle else 0) + dig_bonus
        if look:
            look_filter(look)
        # ---- tutor a missing category to hand ----
        miss = missing_categories()
        if miss:
            wanted = [next(iter(cat)) for _, cat in miss]   # representative target per missing cat
            # multi-tutor: grab up to 2 missing
            used = False
            for nm, cost in tut_multi.items():
                if g.has(nm) and g.avail >= cost:
                    g.cast(nm, cost)
                    for tgt in wanted[:2]:
                        g.fetch(tgt)
                    used = True
                    break
            if not used:
                for nm, cost in tut_one.items():
                    if g.has(nm) and g.avail >= cost and g.fetch(wanted[0]):
                        g.cast(nm, cost); used = True; break
            if not used:                                    # creature tutor -> creature piece
                cp = next((p for _, cat in miss for p in cat if p in CREATURE_PIECES), None)
                if cp:
                    for nm, cost in tut_creature.items():
                        if g.has(nm) and g.avail >= cost and g.fetch(cp):
                            g.cast(nm, cost); break
        # ---- deploy + win check ----
        deploy()
        if (set(LOOP) & in_play) and (set(enablers) & in_play) and (set(payoffs) & in_play):
            tbl.kill_all(T)
            return tbl.decap, tbl.table
    return tbl.decap, tbl.table


def run(library, rng, trials, **kw):
    return [trial(library, rng, **kw) for _ in range(trials)]


def protection_curve(library, trials, rng):
    prot = ["Fierce Guardianship", "Force of Negation", "Pact of Negation", "Swan Song",
            "Mana Drain", "Veil of Summer", "Tidal Barracuda", "Deadly Rollick",
            "Force of Vigor", "Venser, Shaper Savant"]
    drawn, _ = core.simulate_groups(library, [prot], [], trials, rng, TURNS)
    return drawn


def mode_clock(index, aliases, trials):
    print(f"\n### GLARB INEVITABLE — topdeck-combo assembly clock   trials={trials} seed={SEED}")
    print("    win = Sensei's Top + any enabler + any payoff all in play (loop = decap = table).")
    print("    dig = selection (Glarb surveil 2 + Sylvan 2 + Top 1 + Oracle 1), NOT raw draw.")
    print("    Coffers/Urborg NOT modelled -> real clock a touch faster than shown.\n")
    lib, _ = core.load_parsed(DECK, index, aliases)

    print("  metric".ljust(46) + "".join(f"{t:>6}" for t in SHOW) + "   median  never")
    variants = [
        ("FULL (4 enablers · 2 payoffs · all tutors)",
         dict(enablers=ENABLERS, payoffs=PAYOFFS, tut_multi=TUT_MULTI, tut_one=TUT_ONE, tut_creature=TUT_CREATURE)),
        ("LEAN (Citadel + Top + Aetherflux only)",
         dict(enablers={"Bolas's Citadel": 6}, payoffs={"Aetherflux Reservoir": 4},
              tut_multi={"Insidious Dreams": 3}, tut_one={}, tut_creature={})),
    ]
    for tag, kw in variants:
        res = run(lib, random.Random(SEED), trials, **kw)
        never = 100.0 * sum(1 for d, _ in res if d is None) / trials
        print(core.row(f"{tag}", core.cum(res, 0, SHOW), SHOW) + f"   {core.median(res,0):>5}  {never:3.0f}%")
    print()
    prot = protection_curve(lib, trials, random.Random(SEED + 5))
    print(core.row("protection available (>=1 piece by T)", {t: prot[t] for t in SHOW}, SHOW))
    print("    (Fierce Guardianship/Force of Negation/Pact/Swan Song/Mana Drain/Veil/Tidal Barracuda...)")
    print("\n  Compare: current single-Torment plan = ~T13 decap / table never (ct_speed_lab, dig=0).")


def mode_digsweep(index, aliases, trials):
    print(f"\n### DIG SENSITIVITY (FULL build)   trials={trials}")
    print("    dig_bonus = extra selection looks/turn beyond the modelled engines (robustness).\n")
    lib, _ = core.load_parsed(DECK, index, aliases)
    print("  dig_bonus".ljust(46) + "".join(f"{t:>6}" for t in SHOW) + "   median")
    for db in (-1, 0, 1, 2):
        res = run(lib, random.Random(SEED), trials, enablers=ENABLERS, payoffs=PAYOFFS,
                  tut_multi=TUT_MULTI, tut_one=TUT_ONE, tut_creature=TUT_CREATURE, dig_bonus=db)
        lbl = f"dig_bonus = {db:+d}" + ("  (pessimistic)" if db < 0 else "  (baseline)" if db == 0 else "")
        print(core.row(lbl, core.cum(res, 0, SHOW), SHOW) + f"   {core.median(res,0)}")


if __name__ == "__main__":
    core.run_cli(__doc__, {"clock": mode_clock, "digsweep": mode_digsweep})
