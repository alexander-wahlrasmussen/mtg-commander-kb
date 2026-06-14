#!/usr/bin/env python3
"""lw_speed_lab.py — Lightning War (Fire Lord Azula) speed/kill analysis lab.

Two modes, both built on top of deck_sim.py's engine + oracle index:

  --mode compare  Before/after speed-curve: the archived pre-pivot list vs the
                  current burn build, on consistency (lands/colour/keepable/CMC)
                  AND a GROUPED kill-enabler availability model the stock
                  fixed-piece sim can't express (">=1 member of each named group
                  by turn T", with optional tutor wildcards).

  --mode levers   Joint kill-turn Monte Carlo for upgrade testing: per trial it
                  tracks BOTH gates (a table-finisher castable in Azula's combat,
                  sorceries gated on a flash enabler, AND enough kill-turn mana
                  incl. the Treasure-storm engine) and reports P(one-cast table
                  wipe <= turn T). Used to rank which add pulls the kill earlier.

  --mode both     (default) run compare then levers.

This is a HEURISTIC, NOT a rules engine. The levers model's mana/lethal numbers
rest on documented assumptions (see kill_turn's docstring); trust the relative
ranking and the life-total sensitivity, not the second decimal. The config block
is Azula-specific; to reuse for another deck, copy and retune the constants.

Writeup: proposals/Lightning_War_Speed_Curve_Analysis.md
Data: collection/oracle-cards.json (refresh via update_scryfall_data.py)
"""
import argparse
import importlib.util
import random
from pathlib import Path

ROOT = Path(__file__).parent.parent
_spec = importlib.util.spec_from_file_location("deck_sim", Path(__file__).parent / "deck_sim.py")
ds = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(ds)

OLD = ROOT / "archive" / "old_decklists" / "lightning-war-20260413-153124.txt"
NEW = ROOT / "decks" / "lightning-war-20260614.txt"
SEED = 12345

# ---- shared card sets (decklist names) -----------------------------------
FINISHERS = ["Crackle with Power", "Comet Storm", "Electrodominance", "Banefire"]
TABLE_FINISHERS = ["Crackle with Power", "Comet Storm"]   # only these fork to all opps per instance
AMPLIFIERS = ["Twinning Staff", "Galvanic Iteration", "Increasing Vengeance", "Reiterate"]
TUTORS = ["Mystical Teachings", "Emeritus of Woe", "Sanar, Unfinished Genius"]


# ==========================================================================
# MODE: compare  (before/after)
# ==========================================================================
SHOW = [2, 3, 4, 5, 6, 7, 8, 10]


def simulate_groups(library, groups, tutors, turns, trials, rng):
    """P(>=1 member of every group available by turn T). Tutors are wildcards
    (each in hand can satisfy one unmet group). Ignores mana -> availability
    ceiling, read next to the mana curve."""
    n = len(library)
    grp_sets = [{g.lower() for g in grp} for grp in groups]
    tutor_set = {t.lower() for t in tutors}
    drawn = [0] * (turns + 1)
    with_t = [0] * (turns + 1)
    for _ in range(trials):
        deck = library[:]
        hand, _ = ds.opening_hand(deck, rng)
        seen = {nm.lower() for nm, _ in hand}
        ptr = 7
        for t in range(1, turns + 1):
            if t > 1 and ptr < n:
                seen.add(deck[ptr][0].lower()); ptr += 1
            satisfied = sum(1 for gs in grp_sets if gs & seen)
            missing = len(grp_sets) - satisfied
            tutors_seen = sum(1 for nm in seen if nm in tutor_set)
            if missing == 0:
                drawn[t] += 1; with_t[t] += 1
            elif tutors_seen >= missing:
                with_t[t] += 1
    return ({t: 100.0 * drawn[t] / trials for t in range(1, turns + 1)},
            {t: 100.0 * with_t[t] / trials for t in range(1, turns + 1)})


def _nonland_cmc(library):
    cmcs = [rec["cmc"] for _, rec in library if not ds.is_land(rec)]
    return sum(cmcs) / len(cmcs) if cmcs else 0.0


def _type_count(library, kw):
    return sum(1 for _, rec in library if kw.lower() in rec["type_line"].lower())


def _row(label, d):
    return "  " + label.ljust(28) + "".join(f"{d[t]:6.0f}" for t in SHOW)


def mode_compare(index, aliases, trials=40000, turns=10):
    print(f"\n### COMPARE (before/after)   trials={trials} seed={SEED}\n")
    for tag, path in [("PRE-PIVOT (20260413)", OLD), ("CURRENT (20260607)", NEW)]:
        rng = random.Random(SEED)
        library, commander, diag = ds.parse_deck(path, index, aliases)
        identity = set()
        for _, r in library:
            identity.update(r["color_identity"])
        if commander and index.get(commander.lower()):
            identity.update(index[commander.lower()]["color_identity"])
        stats = ds.simulate(library, sorted(identity), turns, trials, rng)
        print("=" * 70)
        print(f"  {tag}   library={diag['library_size']}  cmdr={commander}")
        if diag["unresolved"]:
            print(f"  UNRESOLVED: {diag['unresolved']}")
        print(f"  keepable={stats['keepable_pct']:.1f}%   avg nonland CMC={_nonland_cmc(library):.3f}"
              f"   instants={_type_count(library,'instant')} sorceries={_type_count(library,'sorcery')}"
              f" creatures={_type_count(library,'creature')}")
        print("  turn:                       " + "".join(f"{t:6}" for t in SHOW))
        print(_row("avg lands", stats["lands_by_turn"]))
        print(_row("all colours(land)", stats["all_colors_by_turn"]))
        print(_row("has a play", stats["castable_by_turn"]))
        rng = random.Random(SEED)
        if "20260413" in str(path):
            d, _ = simulate_groups(library, [["Aggravated Assault"], ["Ozai, the Phoenix King"]],
                                   [], turns, trials, rng)
            print(_row("OLD combo drawn (AggAss+Ozai)", d))
            d2, _ = simulate_groups(library, [FINISHERS], [], turns, trials, rng)
            print(_row(">=1 X-finisher drawn", d2))
        else:
            d, wt = simulate_groups(library, [FINISHERS], TUTORS, turns, trials, rng)
            print(_row(">=1 burn finisher drawn", d)); print(_row(">=1 burn finisher +tutors", wt))
            dt, wtt = simulate_groups(library, [TABLE_FINISHERS], TUTORS, turns, trials, rng)
            print(_row(">=1 TABLE-finisher drawn", dt)); print(_row(">=1 TABLE-finisher +tutors", wtt))
            d2, wt2 = simulate_groups(library, [FINISHERS, AMPLIFIERS], TUTORS, turns, trials, rng)
            print(_row("finisher+amp drawn", d2)); print(_row("finisher+amp +tutors", wt2))
        print()


# ==========================================================================
# MODE: levers  (joint kill-turn model)
# ==========================================================================
BASE_ROCKS = {"Arcane Signet": (2, 1), "Fellwar Stone": (2, 1),
              "Talisman of Dominance": (2, 1), "Talisman of Indulgence": (2, 1)}
BASE_DIG = {"Faithless Looting": (1, 2), "Frantic Search": (3, 2), "Consider": (1, 2),
            "Valakut Awakening": (5, 2), "Sink into Stupor": (2, 1), "Dirgur Focusmage": (5, 3)}
BASE_FIN = {"Crackle with Power": (14, 11), "Comet Storm": (24, 18)}   # (no-amp, amp) lethal mana @40
BASE_SORC_FIN = {"Crackle with Power"}            # sorcery finisher -> needs a flash enabler in combat
ENGINE = {"Storm-Kiln Artist": (4, 4), "Goldspan Dragon": (5, 2)}     # (cast cost, kill-turn mana add)
ENABLERS = {"Leyline of Anticipation", "Vedalken Orrery", "Borne Upon a Wind", "High Fae Trickster"}
RIT_INSTANT = {"Dark Ritual": 2}
RIT_SORCERY = {"Jeska's Will": 5, "Blazing Firesinger": 2}            # need enabler to fire in combat
KILL_TURNS = 14                                   # turns to simulate in the kill-turn model
FILLER = "March of Swirling Mist"                 # the flex slot each lever consumes (keep lib at 99)
ART = {"cmc": 1.0, "type_line": "Artifact", "face_types": ["Artifact"], "color_identity": ()}
SPL = {"cmc": 2.0, "type_line": "Sorcery", "face_types": ["Sorcery"], "color_identity": ("R",)}
COLS = (5, 6, 7, 8, 9, 10, 12)


def kill_turn(deck_lib, rng, rocks, dig, fin, sorc_fin, enab, amps):
    """First turn a one-cast TABLE wipe is possible (or None).

    Assumptions: kill-turn mana = lands + rocks (tap same turn) + Azula +2
    + Treasure-storm (Storm-Kiln +4 / Goldspan +2 if cast) + rituals in hand
    (Dark Ritual +2 always; Jeska +5 / Seething +2 only with an enabler).
    Lethal thresholds assume 3 opp @40 with Azula's copy (+1 more if an amp is
    in hand). Single-target Banefire/Electrodominance are excluded (not wipes).
    Draw spells dig extra cards. CONSERVATIVE-ish: cantrips dig 'for free', but
    no chip damage is modelled (see the life sensitivity for that)."""
    deck = deck_lib[:]
    hand, _ = ds.opening_hand(deck, rng)
    hand = list(hand); ptr = 7
    lands = rock_out = 0
    azula_turn = None
    engine = {}
    enablers_seen = set()
    dug = set()
    for T in range(1, KILL_TURNS + 1):
        if T > 1 and ptr < len(deck):
            hand.append(deck[ptr]); ptr += 1
        li = next((i for i, (_, r) in enumerate(hand) if ds.is_pure_land(r)), None)
        if li is None:
            li = next((i for i, (_, r) in enumerate(hand) if ds.is_land(r)), None)
        if li is not None:
            hand.pop(li); lands += 1
        enablers_seen |= {nm for nm, _ in hand} & enab
        avail = lands + rock_out
        changed = True
        while changed:
            changed = False
            cand = sorted(((i, rocks[nm]) for i, (nm, _) in enumerate(hand) if nm in rocks),
                          key=lambda x: x[1][0])
            for i, (cost, out) in cand:
                if avail >= cost:
                    hand.pop(i); avail += out - cost; rock_out += out; changed = True; break
        for slot in hand:
            nm = slot[0]
            if nm in dig and id(slot) not in dug:
                cmc, k = dig[nm]
                if avail >= cmc:
                    dug.add(id(slot))
                    for _ in range(k):
                        if ptr < len(deck):
                            hand.append(deck[ptr]); ptr += 1
        if azula_turn is None and avail >= 4:
            azula_turn = T; avail -= 4
        for nm, (cost, add) in ENGINE.items():
            if nm not in engine:
                idx = next((i for i, (h, _) in enumerate(hand) if h == nm), None)
                if idx is not None and avail >= cost:
                    engine[nm] = add; avail -= cost
        if azula_turn is not None and T > azula_turn:
            nmset = {nm for nm, _ in hand}
            amp = bool(nmset & amps)
            enabler = bool(enablers_seen)
            burst = sum(v for k2, v in RIT_INSTANT.items() if k2 in nmset)
            if enabler:
                burst += sum(v for k2, v in RIT_SORCERY.items() if k2 in nmset)
            combat_mana = lands + rock_out + 2 + burst + sum(engine.values())
            have = [f for f in fin if f in nmset and not (f in sorc_fin and not enabler)]
            if nmset & set(TUTORS):
                have.append("Crackle with Power" if enabler else "Comet Storm")
            for f in have:
                if combat_mana >= (fin[f][1] if amp else fin[f][0]):
                    return T
    return None


def make_deck(index, aliases, levers):
    library, _, _ = ds.parse_deck(NEW, index, aliases)
    lib = list(library)
    rocks, dig, fin = dict(BASE_ROCKS), dict(BASE_DIG), dict(BASE_FIN)
    sorc, enab, amps = set(BASE_SORC_FIN), set(ENABLERS), set(AMPLIFIERS)
    for lv in levers:
        for i, (nm, _) in enumerate(lib):
            if nm == FILLER:
                lib.pop(i); break
        name, kind, p = lv["name"], lv["kind"], lv["params"]
        if kind == "rock":
            rocks[name] = p; lib.append((name, ART))
        elif kind == "dig":
            dig[name] = p; lib.append((name, SPL))
        elif kind == "fin":
            fin[name] = p; sorc.add(name); lib.append((name, SPL))
        elif kind == "enab":
            enab.add(name); lib.append((name, SPL))
        elif kind == "amp":
            amps.add(name); lib.append((name, SPL))
    return lib, rocks, dig, fin, sorc, enab, amps


def _lever_run(label, index, aliases, levers, trials):
    rng = random.Random(SEED)
    lib, rocks, dig, fin, sorc, enab, amps = make_deck(index, aliases, list(levers))
    res = [kill_turn(lib, rng, rocks, dig, fin, sorc, enab, amps) for _ in range(trials)]
    row = {T: 100.0 * sum(1 for r in res if r and r <= T) / trials for T in COLS}
    never = 100.0 * sum(1 for r in res if r is None) / trials
    print(f"  {label:<32}" + "".join(f"{row[T]:6.0f}" for T in COLS) + f"   never={never:.0f}%")


def mode_levers(index, aliases, trials=60000):
    print(f"\n### LEVERS — P(one-cast table wipe <= turn T) %   trials={trials} seed={SEED}\n")
    print("  lever".ljust(34) + "".join(f"{t:>6}" for t in COLS))
    _lever_run("BASELINE (current 99)", index, aliases, [], trials)
    print("  --- single 1-for-1 swap (-1 flex) ---")
    _lever_run("+ Sol Ring (fast mana)", index, aliases, [{"name": "Sol Ring", "kind": "rock", "params": (1, 2)}], trials)
    _lever_run("+ Lotus Petal (1-shot)", index, aliases, [{"name": "Lotus Petal", "kind": "rock", "params": (0, 1)}], trials)
    _lever_run("+ 5th Signet-class rock", index, aliases, [{"name": "Extra Signet", "kind": "rock", "params": (2, 1)}], trials)
    _lever_run("+ draw spell (dig 2)", index, aliases, [{"name": "Extra Cantrip", "kind": "dig", "params": (2, 2)}], trials)
    _lever_run("+ Night's Whisper (dig 3)", index, aliases, [{"name": "Extra Draw", "kind": "dig", "params": (2, 3)}], trials)
    _lever_run("+ forking finisher", index, aliases, [{"name": "Forking Fin", "kind": "fin", "params": (22, 16)}], trials)
    _lever_run("+ flash enabler", index, aliases, [{"name": "Extra Enabler", "kind": "enab", "params": None}], trials)
    _lever_run("+ amplifier (copy-doubler)", index, aliases, [{"name": "Extra Amp", "kind": "amp", "params": None}], trials)
    print("  --- stacking ---")
    _lever_run("+ Sol Ring & dig-3", index, aliases,
               [{"name": "Sol Ring", "kind": "rock", "params": (1, 2)},
                {"name": "Extra Draw", "kind": "dig", "params": (2, 3)}], trials)
    print("  --- sensitivity: opponents pre-chipped by the incremental clock ---")
    saved = dict(BASE_FIN)
    BASE_FIN.clear(); BASE_FIN.update({"Crackle with Power": (11, 8), "Comet Storm": (19, 14)})
    _lever_run("BASELINE, opp @30 life", index, aliases, [], trials)
    BASE_FIN.clear(); BASE_FIN.update({"Crackle with Power": (8, 5), "Comet Storm": (14, 9)})
    _lever_run("BASELINE, opp @20 life", index, aliases, [], trials)
    BASE_FIN.clear(); BASE_FIN.update(saved)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--mode", choices=["compare", "levers", "both"], default="both")
    ap.add_argument("--trials", type=int, default=None)
    args = ap.parse_args()
    index = ds.load_oracle_index()
    aliases = ds.load_reskin_aliases()
    if args.mode in ("compare", "both"):
        mode_compare(index, aliases, trials=args.trials or 40000)
    if args.mode in ("levers", "both"):
        mode_levers(index, aliases, trials=args.trials or 60000)


if __name__ == "__main__":
    main()
