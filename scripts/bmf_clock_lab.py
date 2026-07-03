#!/usr/bin/env python3
"""bmf_clock_lab.py — Ms. Bumbleflower (This Bunny Goes to Market) KILL-TURN goldfish.

Kill-Window Lab Sweep, deck 9 (proposals/Kill_Window_Lab_Sweep_2026-06-13.md).
Summary claims "Goldfish T8-10". Built on speed_lab_core.py. Commander mana-gated.
2026-07-03: extended to the ALL-LINES best-line model (the Backlog #11 discipline —
min over correlated draws on ONE game, never independent CDFs) for the "feels great"
close package. All new-line logic gates on the new cards being present, so the
2026-04-04 baseline list runs the ORIGINAL model unchanged (clean A/B via --deck).

KILL SHAPE — combat focus-fire + (new) three quiet no-combat exits (kill_all).

  JOLRAEL   (combat)   {4}{G}{G}: creatures you control have base P/T X/X, X = cards
                       in hand. Focus-fires one player -> decap leads, table lags.
  COUNTER-BEATS        Bumbleflower's per-cast +1/+1 counters piled on a threat. Slow.
  WILLBREAKER theft    GOLDFISH-INVISIBLE (dummies have no creatures) — noted, not
                       modelled; a real-pod bonus the clock cannot credit.
  APPROACH  (kill_all) Approach of the Second Sun. Cast #2 from hand = WIN. Rulings
                       verified 2026-07-03: the win checks the first was CAST, not
                       resolved — so Reprieve (already in deck) bouncing your OWN
                       first cast back to hand is a legal shortcut. Modelled lines:
                       9-mana Reprieve-split (cast + self-bounce, win next turn at 7),
                       16-mana same-turn double, and the natural 7th-from-top redraw
                       (reinserted at real library depth; the deck's draw engine
                       fetches it back).
  ALARM     (kill_all) Intruder Alarm + Shrieking Drake/Whitemane Lion (both already
                       in deck) + any mana dork + commander: each self-bounce recast
                       is a Bumbleflower trigger (mana-neutral off one dork — Drake
                       {U} vs Chocobo any / Druid 1-3); "target opponent draws"
                       iterated = the table draws out. Oracle-verified 2026-07-03.
  WIZ-FATHOM (enabler) Wizard Class lvl 3 ("whenever you draw, +1/+1 counter on
                       target creature you control") aimed at Fathom Mage ("whenever
                       a +1/+1 counter is put on this, you MAY draw") = draw the
                       library at will. Not a kill itself: it makes Jolrael X huge
                       and puts Approach/Alarm pieces in hand.

Engine, oracle-verified (card_lookup.py 2026-06-13 + 2026-07-03):
  * Bumbleflower: each spell you cast -> +1/+1 counter on a creature (+flying); the
    SECOND resolution each turn -> you draw 2. Cheap/free cantrips chain to the 2nd cast.
  * Jolrael: your 2nd draw each turn -> a 2/2 Cat; the {4}{G}{G} pump is the alpha.
  * Combo-piece casts (Approach/Reprieve/Alarm/Wizard Class) count toward the trigger
    bookkeeping like any other cast; Class LEVELING is an activated ability, not a
    cast (no trigger) — ruling-verified.

HEURISTIC. Spell velocity: each turn cast nonland cards from hand cheapest-first
(creatures stay as bodies; instants/sorceries act as cantrips = draw 1 selection proxy),
capped at 5 Bumbleflower triggers/turn (free-spell loop guard). Combo pieces are
RESERVED from the chain only while their line is live in this list (baseline lists
without the cards are untouched). The goldfish casts its interaction proactively for
triggers (no opponents) — a ceiling. Mana = lands + rocks/dorks floor. Jolrael X =
len(hand) at activation. Combat focus-fire, unblocked. Trust the SHAPE and front edge,
not the second decimal. decap/table stated separately, plus the close-mixture split
(which line actually ended each game — the "not the same combo every game" check).

OMITTED (conservative): Willbreaker theft (no opp board), Smuggler's Share / Tataru
Treasure ramp, Snapcaster/flash rebuys, Wizard Class lvl-3 counters on ordinary draws,
evasive blocking math. OPTIMISTIC: rocks tap turn they land; proactive spell-dumping;
no interaction / static 40; Intruder Alarm's symmetric untap-stop ignored in the mana
floor (loop iterations themselves are modelled mana-honest).

Data: collection/oracle-cards.json   ·   Writeup: proposals/Ms_Bumbleflower_Clock_Lab_2026-06-13.md
"""
import importlib.util
import random
from pathlib import Path

ROOT = Path(__file__).parent.parent
_spec = importlib.util.spec_from_file_location("speed_lab_core", Path(__file__).parent / "speed_lab_core.py")
slc = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(slc)
ds = slc.ds

DECK = ROOT / "decks" / "this-bunny-goes-to-market-20260703.txt"
SEED = 20260613
TURNS = 14
SHOW = [5, 6, 7, 8, 9, 10, 12, 14]
COMMANDER = "Ms. Bumbleflower"
JOLRAEL = "Jolrael, Mwonvuli Recluse"

APPROACH = "Approach of the Second Sun"
REPRIEVE = "Reprieve"
ALARM = "Intruder Alarm"
WIZCLASS = "Wizard Class"
FATHOM = "Fathom Mage"
BOUNCERS = ("Shrieking Drake", "Whitemane Lion")   # self-bounce loop bodies, cost 1 / 2
LOOP_DORKS = ("Paradise Chocobo", "Incubation Druid")  # repeatable any-colour dorks

ROCKS = {"Sol Ring": (1, 2), "Arcane Signet": (2, 1), "Bender's Waterskin": (2, 1),
         "Paradise Chocobo": (1, 1), "Incubation Druid": (2, 1), "Hardbristle Bandit": (2, 1)}
TRIG_CAP = 5                      # Bumbleflower triggers/turn (free-spell loop guard)


def _powmap(library, commander):
    names = [nm for nm, r in library if "creature" in r["type_line"].lower()]
    names.append(commander)
    raw = slc.load_powers(names)
    return {k: (v if isinstance(v, int) else 1) for k, v in raw.items()}


def goldfish_kill(library, commander, powmap, rng, why=None):
    """One goldfish game; returns (decap, table). why: optional dict tallying
    which line closed the TABLE ('approach'/'alarm'/'combat')."""
    def pw(nm):
        return powmap.get(nm.lower(), 1)

    names = {nm for nm, _ in library}
    has_approach = APPROACH in names        # line-live flags: gate ALL new logic,
    has_alarm = ALARM in names              # so a list without the cards runs the
    has_wiz = WIZCLASS in names             # original model bit-for-bit.

    g = slc.Goldfish(library, rng, rocks=ROCKS)
    tbl = slc.Table()
    bumble = jolrael = False
    ncre = 0                      # creature bodies (incl. commander, Cats, payoffs)
    base_pow = 0                  # summed printed power of bodies
    counters = 0                  # Bumbleflower +1/+1 counters banked on the team
    alarm = fathom = False
    wiz_lvl = 0                   # 0 = not on board
    app_casts = 0                 # times Approach has been cast this game
    dorks_out = set()             # loop-capable dorks deployed (subset of LOOP_DORKS)
    closer = None                 # which line tabled the game

    def close(kind, T):
        nonlocal closer
        tbl.kill_all(T)
        closer = kind

    for T in range(1, TURNS + 1):
        g.begin_turn(T)
        if has_alarm:
            before = {d for d in LOOP_DORKS if g.has(d)}
        g.deploy_rocks()
        if has_alarm:
            dorks_out |= {d for d in before if not g.has(d)}
        # commander (mana-gate: she's in the command zone, not the library)
        if not bumble and g.avail >= 4:
            g.avail -= 4; bumble = True; ncre += 1; base_pow += 1   # 1/5

        trig = 0

        def bumble_trig(is_cre_body=False, nm=None, r=None):
            """Shared per-cast bookkeeping: body/cantrip effect + Bumbleflower."""
            nonlocal trig, ncre, base_pow, counters, jolrael, fathom
            if r is not None and is_cre_body:
                ncre += 1; base_pow += pw(nm)
                if nm == JOLRAEL:
                    jolrael = True
                if nm == FATHOM:
                    fathom = True
            elif r is not None:
                g.draw(1)                       # cantrip / selection proxy
            trig += 1
            if bumble:
                counters += 1
                if trig == 2:                   # 2nd resolution -> draw two
                    g.draw(2)
                    if jolrael:                 # 2nd draw -> 2/2 Cat
                        ncre += 1; base_pow += 2

        # ---- combo actions first (the win outranks chain velocity) -------------
        if has_approach or has_alarm or has_wiz:
            # Approach cast #2 from hand = win (rulings: first CAST suffices)
            if app_casts >= 1 and g.has(APPROACH) and g.avail >= 7:
                g.cast(APPROACH, 7)
                close("approach", T)
            # Alarm loop: commander + Alarm out + self-bouncer in hand + loop dork(s)
            # that SUSTAIN the cycle: Drake {U} loops off any dork; Lion {1}{W} needs
            # 2 mana/cycle — Druid (Bumbleflower's counter -> taps for 3) or both dorks.
            if not tbl.done and bumble and alarm and dorks_out:
                bouncer = next((b for b in BOUNCERS if g.has(b)), None)
                if bouncer:
                    cost = 1 if bouncer == BOUNCERS[0] else 2
                    sustain = (LOOP_DORKS[1] in dorks_out) or (len(dorks_out) >= cost)
                    if sustain and g.avail >= cost:
                        close("alarm", T)
            if not tbl.done and has_approach and app_casts == 0 and g.has(APPROACH):
                if g.has(REPRIEVE) and g.avail >= 9:
                    # cast #1 + Reprieve it back to hand (2 casts, draw 1)
                    i = g.in_hand(APPROACH)
                    card = g.hand.pop(i); g.avail -= 7
                    g.cast(REPRIEVE, 2)
                    g.hand.append(card)
                    app_casts = 1
                    bumble_trig(); bumble_trig()
                    g.draw(1)                                   # Reprieve cantrips
                    if g.avail >= 7:                            # 16-mana same-turn double
                        g.cast(APPROACH, 7)
                        close("approach", T)
                elif g.avail >= 7:
                    # natural cast #1: reinsert 7th from the top of the real library
                    i = g.in_hand(APPROACH)
                    card = g.hand.pop(i); g.avail -= 7
                    g.deck.insert(min(g.ptr + 6, len(g.deck)), card)
                    app_casts = 1
                    bumble_trig()
            if not tbl.done and has_alarm and not alarm and g.has(ALARM) and g.avail >= 3:
                g.cast(ALARM, 3); alarm = True
                bumble_trig()
            if not tbl.done and has_wiz and wiz_lvl == 0 and g.has(WIZCLASS) and g.avail >= 1:
                g.cast(WIZCLASS, 1); wiz_lvl = 1
                bumble_trig()
        if tbl.done:
            if why is not None and closer:
                why[closer] = why.get(closer, 0) + 1
            return tbl.decap, tbl.table

        # ---- spell-velocity chain: cast nonlands cheapest-first ----------------
        reserved = set()
        if has_approach:
            reserved.add(APPROACH)
            if g.has(APPROACH) or app_casts >= 1:
                reserved.add(REPRIEVE)          # held for the shortcut / protection
        if has_alarm:
            reserved.add(ALARM)
            if alarm or g.has(ALARM):
                reserved.update(BOUNCERS)       # held as loop fuel
        if has_wiz:
            reserved.add(WIZCLASS)
        while trig < TRIG_CAP:
            cand = sorted(((i, r["cmc"], nm, r) for i, (nm, r) in enumerate(g.hand)
                           if not ds.is_land(r) and nm not in ROCKS and nm not in reserved),
                          key=lambda x: x[1])
            cast = None
            for i, cmc, nm, r in cand:
                if g.avail >= cmc:
                    cast = (i, cmc, nm, r); break
            if cast is None:
                break
            i, cmc, nm, r = cast
            g.hand.pop(i); g.avail -= cmc
            bumble_trig("creature" in r["type_line"].lower(), nm, r)

        # ---- leftover mana: level Wizard Class; lvl3 + Fathom = draw the deck ---
        if has_wiz and wiz_lvl:
            if wiz_lvl == 1 and g.avail >= 3:
                g.pay(3); wiz_lvl = 2; g.draw(2)    # leveling: ability, not a cast
            if wiz_lvl == 2 and g.avail >= 5:
                g.pay(5); wiz_lvl = 3
            if wiz_lvl == 3 and fathom and g.ptr < len(g.deck):
                g.draw(len(g.deck) - g.ptr)         # Fathom loop: draw the library

        # ---- attack ------------------------------------------------------------
        hand = len(g.hand)
        if jolrael and ncre >= 1 and g.avail >= 6:        # Jolrael alpha
            g.avail -= 6
            board = ncre * hand + counters                # base X/X + counters
        else:
            board = base_pow + counters                   # counter-beats / Cats
        if board > 0:
            tbl.hit_focus(board, T)
        if tbl.done:
            if why is not None:
                why["combat"] = why.get("combat", 0) + 1
            return tbl.decap, tbl.table
    return tbl.decap, tbl.table


def mode_clock(index, aliases, trials, deck=None):
    path = deck or DECK
    print(f"\n### CLOCK — Ms. Bumbleflower kill-turn goldfish   trials={trials} seed={SEED}")
    print(f"    deck: {Path(path).name}")
    print("    decap = first opponent dead (40) · table = all three. Combat focus-fire")
    print("    (Jolrael alpha / counter-beats) + Approach / Alarm-loop kill_all exits when")
    print("    present in the list; Willbreaker theft is goldfish-invisible.\n")
    library, commander = slc.load_parsed(path, index, aliases)
    powmap = _powmap(library, commander)
    rng = random.Random(SEED)
    why = {}
    res = [goldfish_kill(library, commander, powmap, rng, why=why) for _ in range(trials)]
    slc.report_clock(res, SHOW, TURNS, trials)
    tabled = sum(why.values())
    if tabled:
        split = " · ".join(f"{k} {100.0 * v / tabled:.0f}%" for k, v in
                           sorted(why.items(), key=lambda kv: -kv[1]))
        print(f"\n  Close-mixture (which line tabled the game): {split}  (of {tabled} tabled)")
    print("\n  Claimed in Summary: Goldfish T8-10. Front-edge odds are the test.")


if __name__ == "__main__":
    slc.run_cli(__doc__, {"clock": mode_clock}, default_trials=40000)
