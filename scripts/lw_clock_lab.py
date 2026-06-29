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
# The combo-assembly clock lives in lw_combo_lab; the bestline mode races it against
# this lab's burn goldfish on the SAME shuffled game (Backlog #11 all-finishers MVP).
_cspec = importlib.util.spec_from_file_location("lw_combo_lab", Path(__file__).parent / "lw_combo_lab.py")
lcl = importlib.util.module_from_spec(_cspec); _cspec.loader.exec_module(lcl)

DECK = ROOT / "decks" / "lightning-war-20260621.txt"         # current list (repointed 2026-06-28)
SEED = 20260613
TURNS = 14
SHOW = [5, 6, 7, 8, 9, 10, 12, 14]

# mode_amp injectables (all oracle-verified 2026-06-28; none are GCs; all owned):
#   Torbran {1}{R}{R}{R} 2/4 — a red source's damage to an opp/their permanent is +2.
#   Pyretic Ritual {1}{R} -> {R}{R}{R} (net +1); Rite of Flame {R} -> {R}{R} (net +1).
TORBRAN_REC = {"cmc": 4.0, "type_line": "Legendary Creature — Dwarf Noble",
               "face_types": ["Creature"], "color_identity": ("R",)}
RIT_REC = {"cmc": 2.0, "type_line": "Instant", "face_types": ["Instant"],
           "color_identity": ("R",)}

ROCKS ={"Sol Ring": (1, 2), "Arcane Signet": (2, 1), "Fellwar Stone": (2, 1),
         "Talisman of Dominance": (2, 1), "Talisman of Indulgence": (2, 1)}   # Sol Ring is maindeck (20260621)
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


def goldfish_kill(library, commander, index, powmap, rng, g=None,
                  chip_rate=0, chip_start=3, extra_pingers=0,
                  fin_always=False, enabler_always=False, extra_rituals=None):
    """chip_rate = life each opponent loses per OUR turn from cross-table combat
    (the pod beating on each other), applied from chip_start onward. extra_pingers
    = an ALWAYS-ON pinger CEILING: +1/each per cast from turn 1, no draw/cast cost.
    It is optimistic — a real singleton pinger you must draw and then cast is worth
    far less (see add_pingers). chip_rate=0 reproduces the published baseline.

    A library card named "Extra Pinger*" is a REALISTIC added pinger (0-power, cmc 2,
    must be drawn and cast before it chips). Inject via _inject(); that is the honest
    marginal-pinger measurement, vs extra_pingers' always-on ceiling.

    fin_always / enabler_always = CEILING toggles for the availability-under-chip
    test: treat a finisher as always findable / a flash enabler as always present.
    Each is the upper bound of what infinite redundancy on that axis could buy."""
    def pw(nm):
        return powmap.get(nm.lower(), 1)

    if g is None:                                    # bestline_kill injects a shared start
        g = slc.Goldfish(library, rng, rocks=ROCKS)
    tbl = slc.Table()
    azula_turn = None
    guttersnipe = stormkiln = goldspan = vivi = estatic = torbran_active = False
    fated_x = 0
    rituals = {**RITUALS, **extra_rituals} if extra_rituals else RITUALS
    vivi_pow = 0
    treasure_bank = 0
    board = ncre = 0
    new_pow = new_cre = 0
    live_xp = 0                                      # realistic "Extra Pinger*" in play

    for T in range(1, TURNS + 1):
        board += new_pow; ncre += new_cre; new_pow = new_cre = 0
        g.begin_turn(T)
        g.deploy_rocks()

        # cross-table chip: between our turns the rest of the pod attacks each
        # other, so opponents arrive already below 40. Capped at life-1 per
        # opponent so the TABLE's own beatdown never registers OUR decap/table
        # clock — we still have to land the finishing point. Conservative: chip
        # never lands a kill even stacked with our pings, and aggression aimed at
        # US is not subtracted from the opponents (so the moderate band, not the
        # heavy one, is the honest planning centre).
        if chip_rate and T >= chip_start:
            for i in range(len(tbl.dmg)):
                if tbl.dmg[i] < tbl.life:
                    tbl.dmg[i] = min(tbl.life - 1, tbl.dmg[i] + chip_rate)

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
                    is_xp = nm.startswith("Extra Pinger")
                    g.cast(nm, cmc); new_pow += (0 if is_xp else pw(nm)); new_cre += 1
                    if nm == "Guttersnipe": guttersnipe = True
                    elif nm == "Storm-Kiln Artist": stormkiln = True
                    elif nm == "Goldspan Dragon": goldspan = True
                    elif nm == "Vivi Ornitier": vivi = True
                    elif nm == "Electrostatic Field": estatic = True   # 0/4 pinger (no swing)
                    elif nm == "Torbran": torbran_active = True         # +2 to each red damage instance
                    elif is_xp: live_xp += 1                            # realistic added pinger
                    more = True
                    break
        # Fated Firepower (amplifier): enters with X fire counters (+X to all damage)
        if fated_x == 0 and g.has("Fated Firepower") and g.avail >= 5:
            x = min(4, g.avail - 3)
            g.cast("Fated Firepower", 3 + x); fated_x = x
        # Torbran adds a FLAT +2 to every red damage instance to each opponent and
        # stacks with Fated's +X. amp = the total per-instance bonus live this turn.
        amp = fated_x + (2 if torbran_active else 0)

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
        # pinger chip (Guttersnipe 2 + Vivi 1 + Electrostatic Field 1 per cast, each
        # amplified by Fated). extra_pingers = FURTHER Firebrand-class adds (1/each).
        per_cast = ((2 + amp if guttersnipe else 0) + (1 + amp if vivi else 0)
                    + (1 + amp if estatic else 0)
                    + (live_xp + extra_pingers) * (1 + amp))
        if per_cast and ncast:
            tbl.hit_all(per_cast * ncast, T)
            if tbl.done:
                return tbl.decap, tbl.table

        # ---- combat (Azula online, cast on a prior turn) -----------------------
        if azula_turn is not None and T > azula_turn:
            swing = board + ncre * amp                       # Fated/Torbran add per attacker
            if swing > 0:
                tbl.hit_focus(swing, T)
                if tbl.done:
                    return tbl.decap, tbl.table
            tre_mana = treasure_bank * (2 if goldspan else 1)
            rit = sum(v for r, v in rituals.items() if g.has(r))
            cm = g.avail + 2 + tre_mana + rit
            enabler = enabler_always or any(g.has(e) for e in ENABLERS)
            n_amp = (sum(1 for a in AMPS if g.has(a))
                     + sum(1 for nm, _ in g.hand if nm.startswith("Extra Amp")))
            inst = 2 + n_amp                                 # Azula copy + amps
            # A held tutor (Mystical Teachings {3}{U}=4, Emeritus of Woe {3}{B}=4,
            # Sanar/Wild Idea {U}{R}=2; card_lookup 2026-06-29) lets us FIND a
            # finisher, but casting it the SAME turn must also pay the tutor's own
            # mana — no tutor-into-cast for just the finisher's cost (double-spend,
            # 2026-06-29 audit). tutor_cost = the cheapest held finder; reserve it.
            tutor_costs = [r["cmc"] for nm, r in g.hand
                           if nm in TUTORS or nm.startswith("Extra Tutor")]
            tutor_cost = min(tutor_costs) if tutor_costs else 0
            have_tutor = fin_always or (bool(tutor_costs) and cm >= tutor_cost)
            has_xfin = any(nm.startswith("Extra Finisher") for nm, _ in g.hand)
            living = [i for i in range(3) if tbl.dmg[i] < tbl.life]
            if not living:
                return tbl.decap, tbl.table
            need_each = max(tbl.life - tbl.dmg[i] for i in living)
            need_one = min(tbl.life - tbl.dmg[i] for i in living)

            def castable(fin):
                return (g.has(fin) or have_tutor) and not (fin in SORCERY_FIN and not enabler)

            def fin_cm(in_hand):
                """Mana left to CAST the finisher this turn. Full cm if it's already
                in hand (or the fin_always free-find ceiling); otherwise we had to
                TUTOR it this turn, so reserve the finder's own cost first."""
                return cm if (in_hand or fin_always) else cm - tutor_cost

            killed_table = killed_one = False
            if castable("Crackle with Power"):               # (5X+amp) per instance, x inst
                X = len(living)
                while (5 * X + amp) * inst < need_each:
                    X += 1
                if fin_cm(g.has("Crackle with Power")) >= 3 * X + 2:
                    killed_table = True
            if not killed_table and (castable("Comet Storm") or has_xfin):  # Comet-class
                X = 1
                while (X + amp) * inst < need_each:
                    X += 1
                if fin_cm(g.has("Comet Storm") or has_xfin) >= X + 2 + (len(living) - 1):
                    killed_table = True
            for fin, base in (("Electrodominance", 2), ("Banefire", 1)):
                if castable(fin):
                    X = 1
                    while (X + amp) * inst < need_one:
                        X += 1
                    if fin_cm(g.has(fin)) >= X + base:
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
    print("    decap = first opponent dead (40) · table = all three. Board + 3 pingers")
    print("    (Guttersnipe/Vivi/Electrostatic Field) chip; a copy-amped X-spell forks.\n")
    library, commander = slc.load_parsed(DECK, index, aliases)
    powmap = _powmap(library, commander)
    rng = random.Random(SEED)
    res = [goldfish_kill(library, commander, index, powmap, rng) for _ in range(trials)]

    slc.report_clock(res, SHOW, TURNS, trials)
    print("\n  Claimed in Summary: Goldfish T6-7. Front-edge odds above are the test.")
    print("  (cf. lw_speed_lab one-cast-from-40 table wipe: 20% by T12 / 70% never — no chip/board.)")


def _run(library, commander, powmap, trials, **kw):
    rng = random.Random(SEED)
    return [goldfish_kill(library, commander, None, powmap, rng, **kw) for _ in range(trials)]


def _report(label, res, trials):
    nd = 100.0 * sum(1 for d, _ in res if d is None) / trials
    nt = 100.0 * sum(1 for _, t in res if t is None) / trials
    print(slc.row(label + " decap", slc.cum(res, 0, SHOW), SHOW)
          + f"   med {slc.median(res, 0)}  nvr {nd:.0f}%")
    print(slc.row(label + " table", slc.cum(res, 1, SHOW), SHOW)
          + f"   med {slc.median(res, 1)}  nvr {nt:.0f}%")


FILLER_POOL = ["Mithril Coat", "March of Swirling Mist", "Thunderdrum Soloist",
               "Emeritus of Conflict", "Untimely Malfunction"]   # low-impact cuts in the current list
PINGER_REC = {"cmc": 2.0, "type_line": "Creature — Wall", "face_types": ["Creature"],
              "color_identity": ("R",)}
SPELL_REC = {"cmc": 2.0, "type_line": "Instant", "face_types": ["Instant"],
             "color_identity": ("R",)}


def _inject(library, adds):
    """adds = list of (name, record). Drop one filler per add (keeps lib=99) and append
    each as a real drawable card. A name beginning 'Extra Pinger/Finisher/Tutor/Amp' is
    recognised by goldfish_kill ONLY once in hand — the honest draw+cast marginal model
    (vs the always-on extra_pingers / *_always ceilings)."""
    lib, pool = list(library), list(FILLER_POOL)
    for name, rec in adds:
        for f in list(pool):
            idx = next((i for i, (nm, _) in enumerate(lib) if nm == f), None)
            if idx is not None:
                lib.pop(idx); pool.remove(f); break
        lib.append((name, dict(rec)))
    return lib


# --- BEST-LINE (Backlog #11 all-finishers MVP) -----------------------------
# pod_gauntlet harvests ONE (decap, table) curve per deck. For Lightning War that
# curve was the burn RACE goldfish (mode_clock), which buries the deck's fastest
# table kill — the Reiterate+Seething Song / Narset combo (lw_combo_lab, CAST ~T9).
# bestline races BOTH lines on the SAME simulated game and reports the earliest
# close by either, so the harvested curve means "fastest of all lines," not "race
# only." The min is taken on ONE shared opening hand + library (correlated draws),
# NOT over two independent labs' CDFs — the latter is the optimistic-clock disease
# the kill-window sweep already falsified five times (keeping best-of-N god draws).
def _goldfish_from(start, rocks):
    """A Goldfish pinned to a pre-rolled (deck, hand, ptr) so two kill lines race the
    SAME shuffled game, each carrying its own rock set. __new__ bypasses the shuffle so
    no rng is consumed (the start was already rolled once, shared by both lines)."""
    deck, hand, ptr = start
    g = slc.Goldfish.__new__(slc.Goldfish)
    g.deck, g.hand, g.ptr = list(deck), list(hand), ptr
    g.yard, g.lands, g.rock_out = [], 0, 0
    g.rocks, g.avail = rocks or {}, 0
    return g


def perline_kill(library, commander, powmap, combo_rocks, rng):
    """Per-LINE (decap, table) for each of Lightning War's kill lines on ONE shared game:
      BURN  — chip + copy-amped X-spell race (goldfish_kill, this lab).
      COMBO — Reiterate+Seething Song / Narset assembly (lw_combo_lab); going off ends
              the game, so its CAST turn is both the decap and the table kill.
    Returns {"burn": (decap, table), "combo": (decap, table)}. Both lines start from the
    SAME pre-rolled hand+library (correlated draws — a brick hand bricks both), so a
    consumer can take the min (bestline_kill) OR keep them separate so a pod-state disabler
    can switch one line OFF (finisher_mixture.py, Backlog #11 proper version). This is the
    primitive; bestline_kill is the min wrapper, so the harvested curve is unchanged."""
    g0 = slc.Goldfish(library, rng, rocks=ROCKS)         # roll the shared start once
    start = (g0.deck, g0.hand, g0.ptr)
    db, tb = goldfish_kill(library, commander, None, powmap, rng,
                           g=_goldfish_from(start, ROCKS))
    _, cast = lcl.assembly_turn(library, rng, combo_rocks,
                                g=_goldfish_from(start, combo_rocks))
    return {"burn": (db, tb), "combo": (cast, cast)}


def bestline_kill(library, commander, powmap, combo_rocks, rng):
    """Earliest (decap, table) by ANY of Lightning War's kill lines on one game — the min
    over perline_kill's lines taken on correlated draws (a brick hand is a brick for the
    min), NOT over two independent labs' CDFs. This is the curve pod_gauntlet harvests
    (Backlog #11 MVP); routing it through perline_kill leaves the computation — and so the
    harvested curve and its golden snapshot — byte-identical."""
    lines = perline_kill(library, commander, powmap, combo_rocks, rng)
    (db, tb), (cast, _) = lines["burn"], lines["combo"]
    decap = min([x for x in (db, cast) if x is not None], default=None)
    table = min([x for x in (tb, cast) if x is not None], default=None)
    return decap, table


def mode_bestline(index, aliases, trials):
    print(f"\n### BEST-LINE — earliest decap/table by ANY kill line   trials={trials} seed={SEED}")
    print("    Races the BURN goldfish (this lab) AND the Reiterate+Seething Song / Narset")
    print("    combo (lw_combo_lab) on the SAME shuffled game, reporting the earlier close.")
    print("    This is the curve pod_gauntlet harvests (Backlog #11): 'fastest of all lines',")
    print("    not race-only. min is on ONE game (correlated draws), never over independent CDFs.\n")
    library, commander = slc.load_parsed(DECK, index, aliases)
    powmap = _powmap(library, commander)
    combo_rocks = lcl.deck_rocks(library)
    rng = random.Random(SEED)
    res = [bestline_kill(library, commander, powmap, combo_rocks, rng) for _ in range(trials)]
    slc.report_clock(res, SHOW, TURNS, trials)
    print("\n  cf. --mode clock (burn race only): decap ~T10 / table >T14. The combo line")
    print("  (lw_combo_lab CAST median ~T9) is what this surfaces — invisible to the race goldfish.")


def mode_perline(index, aliases, trials):
    print(f"\n### PER-LINE — each kill line's own decap/table + the bestline min   trials={trials} seed={SEED}")
    print("    The two lines raced on ONE shared game (perline_kill). finisher_mixture.py")
    print("    consumes these SEPARATELY so a pod-state disabler can switch a line off; the")
    print("    BESTLINE row is the min over them (== what pod_gauntlet harvests, unchanged).\n")
    library, commander = slc.load_parsed(DECK, index, aliases)
    powmap = _powmap(library, commander)
    combo_rocks = lcl.deck_rocks(library)
    rng = random.Random(SEED)
    res = [perline_kill(library, commander, powmap, combo_rocks, rng) for _ in range(trials)]
    burn = [r["burn"] for r in res]
    combo = [r["combo"] for r in res]
    best = [(min([x for x in (b[0], c[0]) if x is not None], default=None),
             min([x for x in (b[1], c[1]) if x is not None], default=None))
            for b, c in zip(burn, combo)]
    print("  P(kill <= turn T) %".ljust(42) + "".join(f"{t:>6}" for t in SHOW))
    _report("  BURN  (race)", burn, trials)
    _report("  COMBO (Reiterate+SS)", combo, trials)
    _report("  BESTLINE (min)", best, trials)


def mode_chipsweep(index, aliases, trials):
    print(f"\n### CHIP SWEEP — opponents arrive pre-chipped by the pod   trials={trials} seed={SEED}")
    print("    chip_rate = life each opponent loses per our turn from cross-table combat")
    print("    (from T3). Implied avg opponent life at T6 = 40 - 4*rate. decap=first dead,")
    print("    table=all three (OUR kills; chip itself is capped non-lethal).\n")
    library, commander = slc.load_parsed(DECK, index, aliases)
    powmap = _powmap(library, commander)
    print("  P(kill <= turn T) %".ljust(42) + "".join(f"{t:>6}" for t in SHOW))
    for rate, tag in [(0, "no table chip  (@40 T6, baseline)"), (2, "light 2/turn   (@32 T6)"),
                      (3, "moderate 3/turn(@28 T6)"), (5, "heavy 5/turn   (@20 T6)")]:
        print(f"  -- {tag} " + "-" * (38 - len(tag)))
        _report(f"  r={rate}", _run(library, commander, powmap, trials, chip_rate=rate), trials)


def mode_optimize(index, aliases, trials):
    print(f"\n### OPTIMIZE — REAL (draw+cast) vs ALWAYS-ON pinger   trials={trials} seed={SEED}")
    print("    The deck already runs 3 pingers (Guttersnipe/Vivi/Electrostatic). A REAL added")
    print("    pinger is a drawn+cast singleton (-1 filler); an ALWAYS-ON one chips from T1 for")
    print("    free (optimistic ceiling). The gap between them is the draw/cast tax.\n")
    library, commander = slc.load_parsed(DECK, index, aliases)
    powmap = _powmap(library, commander)
    lib1 = _inject(library, [("Extra Pinger 1", PINGER_REC)])
    print("  P(kill <= turn T) %".ljust(42) + "".join(f"{t:>6}" for t in SHOW))
    for rate, lab in [(3, "moderate chip (3/turn, @28 T6)"), (0, "static @40 (no table chip)")]:
        print(f"  == {lab} ==")
        _report("  current deck (3 pingers)", _run(library, commander, powmap, trials, chip_rate=rate), trials)
        _report("  +1 REAL pinger (draw+cast)", _run(lib1, commander, powmap, trials, chip_rate=rate), trials)
        _report("  +1 ALWAYS-ON (ceiling)", _run(library, commander, powmap, trials, chip_rate=rate, extra_pingers=1), trials)


def mode_avail(index, aliases, trials):
    print(f"\n### AVAIL-UNDER-CHIP — is the kill gated on MANA, FINISHER, or ENABLER?")
    print(f"    trials={trials} seed={SEED}. All held at moderate chip (3/turn from T3, @28 by T6).")
    print("    CEIL rows = infinite redundancy on that axis (upper bound the prize). Compare the")
    print("    axes' ceilings to each other; the REAL pinger shows what one true card buys.\n")
    library, commander = slc.load_parsed(DECK, index, aliases)
    powmap = _powmap(library, commander)
    lib1 = _inject(library, [("Extra Pinger 1", PINGER_REC)])
    print("  P(kill <= turn T) %".ljust(42) + "".join(f"{t:>6}" for t in SHOW))
    rows = [
        ("baseline (current deck)", library, dict()),
        ("+1 REAL pinger (draw+cast)", lib1, dict()),
        ("CEIL pinger always-on", library, dict(extra_pingers=1)),
        ("CEIL enabler always-on", library, dict(enabler_always=True)),
        ("CEIL finisher always-found", library, dict(fin_always=True)),
        ("CEIL finisher+enabler both", library, dict(fin_always=True, enabler_always=True)),
    ]
    for tag, lib, kw in rows:
        print(f"  -- {tag} " + "-" * (42 - len(tag)))
        _report("   ", _run(lib, commander, powmap, trials, chip_rate=3, **kw), trials)


def mode_finlever(index, aliases, trials):
    print(f"\n### FIN-LEVER — REAL (draw+cast) redundancy on the HEADROOM axis   trials={trials} seed={SEED}")
    print("    Moderate chip (3/turn, @28 by T6). avail showed finisher-availability is the")
    print("    binding axis (ceiling table-by-T9 33->73%). This asks what a SINGLE real card")
    print("    on that axis buys, vs the +1 real pinger bar (~+3pp) and the always-found ceiling.")
    print("    finisher = Comet-class instant (enabler-free); tutor = finds one; amp = copy-")
    print("    converter (Twinning-class, +1 instance). All must be drawn to do anything.\n")
    library, commander = slc.load_parsed(DECK, index, aliases)
    powmap = _powmap(library, commander)
    variants = [
        ("baseline (current deck)", library, dict()),
        ("+1 REAL pinger (the bar)", _inject(library, [("Extra Pinger 1", PINGER_REC)]), dict()),
        ("+1 REAL table finisher (Comet-class)", _inject(library, [("Extra Finisher 1", SPELL_REC)]), dict()),
        ("+1 REAL tutor", _inject(library, [("Extra Tutor 1", SPELL_REC)]), dict()),
        ("+1 REAL converter/amp (Twinning-class)", _inject(library, [("Extra Amp 1", SPELL_REC)]), dict()),
        ("CEIL finisher always-found", library, dict(fin_always=True)),
    ]
    print("  P(kill <= turn T) %".ljust(44) + "".join(f"{t:>6}" for t in SHOW))
    for tag, lib, kw in variants:
        print(f"  -- {tag} " + "-" * (44 - len(tag)))
        _report("   ", _run(lib, commander, powmap, trials, chip_rate=3, **kw), trials)


def mode_amp(index, aliases, trials):
    print(f"\n### AMP/RITUAL — Torbran (+2/red instance) & added rituals   trials={trials} seed={SEED}")
    print("    On the current list (DECK). Torbran adds a flat +2 to EVERY red damage")
    print("    instance to each opponent (pingers, swing, finisher); rituals add finisher")
    print("    burst mana. Moderate cross-table chip (3/turn, @28 by T6) — honest centre.")
    print("    Each add is a real drawn+cast card (-1 filler, lib stays 99). Lead = TABLE.\n")
    library, commander = slc.load_parsed(DECK, index, aliases)

    def inj(adds):
        lib, pool = list(library), list(FILLER_POOL)
        for name, rec in adds:
            for f in list(pool):
                k = next((i for i, (nm, _) in enumerate(lib) if nm == f), None)
                if k is not None:
                    lib.pop(k); pool.remove(f); break
            lib.append((name, dict(rec)))
        return lib

    xr = {"Pyretic Ritual": 1, "Rite of Flame": 1}
    variants = [
        ("baseline (current deck)", library, dict()),
        ("+Torbran", inj([("Torbran", TORBRAN_REC)]), dict()),
        ("+2 rituals (Pyretic+Rite)",
         inj([("Pyretic Ritual", RIT_REC), ("Rite of Flame", RIT_REC)]), dict(extra_rituals=xr)),
        ("+Torbran +2 rituals",
         inj([("Torbran", TORBRAN_REC), ("Pyretic Ritual", RIT_REC), ("Rite of Flame", RIT_REC)]),
         dict(extra_rituals=xr)),
    ]
    print("  P(kill <= turn T) %".ljust(42) + "".join(f"{t:>6}" for t in SHOW))
    for tag, lib, kw in variants:
        pm = _powmap(lib, commander)
        print(f"  -- {tag} " + "-" * (42 - len(tag)))
        _report("   ", _run(lib, commander, pm, trials, chip_rate=3, **kw), trials)


if __name__ == "__main__":
    slc.run_cli(__doc__, {"clock": mode_clock, "bestline": mode_bestline,
                          "perline": mode_perline, "chipsweep": mode_chipsweep,
                          "optimize": mode_optimize, "avail": mode_avail,
                          "finlever": mode_finlever, "amp": mode_amp}, default_trials=40000)
