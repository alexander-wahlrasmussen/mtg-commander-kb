#!/usr/bin/env python3
"""ws_combo_lab.py — combo POWER + PLAYABILITY study for the merged World Shapers
build (decks/considering/world-shapers-merged-20260704.txt, Hearthhull commander).

Two questions the clock lab doesn't answer:

  1. POWER  — how many real infinite-combo WIN engines does the deck assemble, how
              fast, and how redundant are they? (`--mode assembly`)
  2. FEEL   — how smooth is it to pilot: dead turns (starved vs flooded), hand-size /
              hellbent trajectory, keepable hands, and how reliably Hearthhull lands
              on curve — the "you shuffle a lot / mana is volatile" primer warnings
              measured, not asserted. (`--mode smoothness`)

Both reuse the canonical deck_sim engine (simulate / simulate_flow / draw_map /
opening_hand) via speed_lab_core; only the combo taxonomy is bespoke. deck_sim's
--combos/--flow CLI globs decks/*.txt and can't see decks/considering/, which is the
only reason this driver exists — the MATH is the repo's, not re-derived.

THE COMBO TAXONOMY (find_combos 2026-07-04 = 9 CSB-COMPLETE lines; every piece
card_lookup-verified this session — the CLAUDE.md hard rule). Grouped into engines,
each with its per-iteration output, the in-deck PAYOFF that converts it to a win, and
its assembly slots (a slot = interchangeable members + the tutors that can fetch one):

  A. Mazirek loop [CSB 317-5641]  — WIN
     Mazirek + Basking Broodscale -> infinite {C} / sac / death / +1/+1 counters.
     Ignition: any land sac (free — 11+ fetches / Hearthhull) or Broodscale adapt {1}{G}.
     Payoff IN DECK: All Will Be One (each counter = dmg), Mayhem Devil (each sac =
       ping), Exsanguinate (X off the {C}), Jarad. -> whole table.
     Slots: Mazirek {NO/GSZ/Gamble} · Broodscale {Gamble only — DEVOID, not green}.

  B. Springheart landfall [CSB 3470/3875-5702]  — WIN via drain
     Springheart Nantuko (bestowed) + a mana-per-landfall source, made infinite by
     Ashaya (nontoken creatures ARE Forest lands, so the token copies tap for mana)
     -> infinite landfall + infinite tapped land tokens.
     Payoff IN DECK: Tannuk / Sabotender / Ob Nixilis / Retreat to Hagra (drain per
       landfall); Scute Swarm (infinite bodies); Lotus Cobra mana -> Exsanguinate.
     Slots: Springheart {NO/GSZ/Gamble} · mana {Lotus Cobra|Tireless Provisioner|
       Nissa Resurgent Animist, all NO/GSZ/Gamble} · enabler {Ashaya|Badgermole, NO/GSZ/Gamble}.

  C. Ashaya + Badgermole + free sac outlet [CSB 539-6620/1315/997-7008]  — WIN via drain
     Ashaya + Badgermole Cub + a free land-sac outlet (Sylvan Safekeeper | Zuran Orb |
     Woe Strider) -> infinite landfall / sac / death / ETB. Same drain payoffs as B.
     Slots: Ashaya {NO/GSZ/Gamble} · Badgermole {NO/GSZ/Gamble} · outlet
       {Safekeeper|Zuran|Woe Strider, Gamble (+NO/GSZ reach Safekeeper)}.

  D. Gitrog + Dakmor Salvage [CSB 250-779]  — ENGINE, not a standalone win here
     Dredge Dakmor -> mill 2 -> Gitrog draws per land binned -> re-dredge. Self-mill +
     draw + fills the yard with lands for Splendid Reclamation / Aftermath Analyst / a
     huge landfall wave. NO Thassa's Oracle in the list, so it does NOT win by itself —
     scored as a value/enabler engine, reported separately.
     Slots: Gitrog {NO/GSZ/Gamble} · Dakmor {Gamble/Crop Rotation — it's a LAND}.

  LINCHPIN: Ashaya sits in BOTH B and C. Drawing/tutoring Ashaya arms two engines;
  removing it disables both, leaving Mazirek + the fair Plan-A drain. Badgermole is in
  C and enables B. The free sac outlets (Zuran/Safekeeper/Woe Strider) double as the
  Plan-A mass-sac drain outlets — value pieces that happen to also be combo pieces,
  which is the primer's whole thesis.

Assembly model: per trial, walk turns 1..T over a shuffled deck (opening_hand +
one draw/turn). An engine is ONLINE at T when every slot is covered by a seen member
OR a distinct unused seen tutor that reaches it (exact bipartite match on the tutor
multiset). Two curves: DRAWN-only (no tutor help) and +TUTORS (optimistic — tutors
are free, no mana/colour/discard cost; Gamble's random discard ignored). This is a
CARD-FLOW ceiling; read it beside the mana curve in --mode smoothness. Ignition mana
and the payoff-in-hand are NOT gated (both are plentiful / free) — same convention as
sim_profiles.json.

Run:  python scripts/ws_combo_lab.py --mode assembly   --trials 40000
      python scripts/ws_combo_lab.py --mode smoothness  --trials 40000
"""
import argparse
import importlib.util
import random
from itertools import permutations
from pathlib import Path

ROOT = Path(__file__).parent.parent
_spec = importlib.util.spec_from_file_location(
    "speed_lab_core", Path(__file__).parent / "speed_lab_core.py")
slc = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(slc)
ds = slc.ds

DECK = ROOT / "decks" / "considering" / "world-shapers-merged-20260704.txt"
SEED = 20260704
TURNS = 12
SHOW = [3, 4, 5, 6, 7, 8, 9, 10, 12]
ROCKS = {"Sol Ring": (1, 2), "Arcane Signet": (2, 1), "Mana Vault": (1, 3)}

GC = {"natural order", "green sun's zenith", "gamble"}          # library tutors here
GREEN = {"natural order", "green sun's zenith", "gamble"}       # fetch a green creature
ANY = {"gamble"}
LAND_T = {"gamble", "crop rotation"}

# slot = (frozenset(member names lower), frozenset(tutor names lower))
def slot(members, tutors):
    return (frozenset(m.lower() for m in members), frozenset(t.lower() for t in tutors))

ENGINES = {
    "A. Mazirek loop (WIN)": [
        slot(["Mazirek, Kraul Death Priest"], GREEN),
        slot(["Basking Broodscale"], ANY),                     # devoid: Gamble only
    ],
    "B. Springheart landfall (WIN)": [
        slot(["Springheart Nantuko"], GREEN),
        slot(["Lotus Cobra", "Tireless Provisioner", "Nissa, Resurgent Animist"], GREEN),
        slot(["Ashaya, Soul of the Wild", "Badgermole Cub"], GREEN),
    ],
    "C. Ashaya+Badgermole+outlet (WIN)": [
        slot(["Ashaya, Soul of the Wild"], GREEN),
        slot(["Badgermole Cub"], GREEN),
        slot(["Sylvan Safekeeper", "Zuran Orb", "Woe Strider"],
             {"gamble", "natural order", "green sun's zenith"}),   # NO/GSZ reach Safekeeper
    ],
    "D. Gitrog+Dakmor (engine, not a win)": [
        slot(["The Gitrog Monster"], GREEN),
        slot(["Dakmor Salvage"], LAND_T),
    ],
}
WIN_ENGINES = [k for k in ENGINES if "WIN" in k]


def engine_online(slots, seen, tutors_seen):
    """True if every slot is covered by a seen member, or (with tutors) by an exact
    assignment of distinct unused seen tutors to the still-open slots."""
    open_slots = [tut for mem, tut in slots if not (mem & seen)]
    if not open_slots:
        return True, True                       # drawn-only complete
    # with-tutors: match each open slot to a distinct seen tutor that reaches it
    avail = list(tutors_seen)
    ok = False
    if len(avail) >= len(open_slots):
        for perm in permutations(avail, len(open_slots)):
            if all(perm[i] in open_slots[i] for i in range(len(open_slots))):
                ok = True
                break
    return False, ok


def mode_assembly(library, trials):
    n = len(library)
    all_tutors = set().union(*[t for slots in ENGINES.values() for _, t in slots])
    drawn = {k: [0] * (TURNS + 1) for k in ENGINES}
    tut = {k: [0] * (TURNS + 1) for k in ENGINES}
    any_win_drawn = [0] * (TURNS + 1)
    any_win_tut = [0] * (TURNS + 1)
    rng = random.Random(SEED)
    for _ in range(trials):
        deck = library[:]
        hand, _ = ds.opening_hand(deck, rng)
        seen = {nm.lower() for nm, _ in hand}
        ptr = 7
        for t in range(1, TURNS + 1):
            if t > 1 and ptr < n:
                seen.add(deck[ptr][0].lower())
                ptr += 1
            tutors_seen = seen & all_tutors
            win_d = win_t = False
            for k, slots in ENGINES.items():
                d, tt = engine_online(slots, seen, tutors_seen)
                if d:
                    drawn[k][t] += 1
                if tt:
                    tut[k][t] += 1
                if k in WIN_ENGINES:
                    win_d = win_d or d
                    win_t = win_t or tt
            if win_d:
                any_win_drawn[t] += 1
            if win_t:
                any_win_tut[t] += 1

    def pct(a):
        return {t: 100.0 * a[t] / trials for t in SHOW}

    print("=" * 78)
    print(f"COMBO ASSEMBLY — merged World Shapers   trials={trials} seed={SEED}")
    print("=" * 78)
    print("  P(engine online <= turn T) %        drawn-only / +tutors (NO,GSZ,Gamble)")
    print("  turn:".ljust(40) + "".join(f"{t:>6}" for t in SHOW))
    for k in ENGINES:
        print(slc.row(k + "  drawn", pct(drawn[k]), SHOW, width=38))
        print(slc.row("      +tutors", pct(tut[k]), SHOW, width=38))
    print("  " + "-" * 74)
    print(slc.row(">=1 WIN engine  drawn", pct(any_win_drawn), SHOW, width=38))
    print(slc.row("      +tutors", pct(any_win_tut), SHOW, width=38))
    print("\n  Read: A (Mazirek) and B/C (Ashaya landfall) are the win engines; D is a")
    print("  draw/yard engine, not a standalone win. B & C share Ashaya — the linchpin.")
    print("  +tutors is a CEILING (free tutors, no mana/discard). The deck almost never")
    print("  NEEDS the combo (primer): this measures how OFTEN it has the option.")


def mode_smoothness(library, trials):
    rng = random.Random(SEED)
    identity = sorted({c for _, r in library for c in r["color_identity"]}
                      | set(ds.load_oracle_index().get("hearthhull, the worldseed",
                            {"color_identity": ()})["color_identity"]))
    stats = ds.simulate(library, identity, 10, trials, random.Random(SEED))
    dmap = ds.draw_map(library)
    flow_g = ds.simulate_flow(library, 10, trials, random.Random(SEED),
                              spend="greedy", draw_profiles=dmap)
    flow_1 = ds.simulate_flow(library, 10, trials, random.Random(SEED),
                              spend="one", draw_profiles=dmap)

    # Hearthhull-on-curve: mana floor (lands + greedy rocks) reaches 4 by turn T?
    hh = [0] * (TURNS + 1)
    rng2 = random.Random(SEED)
    for _ in range(trials):
        g = slc.Goldfish(library[:], rng2, rocks=ROCKS)
        online = None
        for t in range(1, 8):
            g.begin_turn(t)
            g.deploy_rocks()
            if online is None and g.avail >= 4:
                online = t
        for t in SHOW:
            if online is not None and online <= t:
                hh[t] += 1

    show = [2, 3, 4, 5, 6, 8, 10]
    p = lambda d: "".join(f"{d[t]:6.0f}" for t in show)
    print("=" * 78)
    print(f"SMOOTHNESS — merged World Shapers   trials={trials} seed={SEED}")
    print("=" * 78)
    print(f"  keepable opening hand: {stats['keepable_pct']:.1f}%   "
          f"(London mull, deck_sim keep-spec)")
    print(f"\n  turn:".ljust(24) + "".join(f"{t:>6}" for t in show))
    print("  avg lands:      " + "".join(f"{stats['lands_by_turn'][t]:6.1f}" for t in show))
    print("  all colours:    " + p(stats['all_colors_by_turn']))
    print(f"\n  --- tempo (greedy spend = upper bound on emptying) ---")
    print("  live turn:      " + p(flow_g['live_by_turn']))
    print("  dead-starved:   " + p(flow_g['starved_by_turn']) + "   (spell stuck, mana too low)")
    print("  dead-flooded:   " + p(flow_g['flooded_by_turn']) + "   (nothing to cast)")
    print("  hand size:      " + "".join(f"{flow_g['hand_size_by_turn'][t]:6.1f}" for t in show))
    print("  hellbent(<=1):  " + p(flow_g['hellbent_by_turn']))
    print(f"  mean dead turns (T1-10): {flow_g['mean_dead_turns']:.2f}")
    print(f"\n  --- tempo (one-play spend = lower bound; paced pilot) ---")
    print("  dead-starved:   " + p(flow_1['starved_by_turn']))
    print("  hellbent(<=1):  " + p(flow_1['hellbent_by_turn']))
    print(f"  mean dead turns (T1-10): {flow_1['mean_dead_turns']:.2f}")
    print(f"\n  --- Hearthhull on curve (>=4 mana from lands+rocks) ---")
    print("  P(HH online<=T):" + "".join(f"{100.0*hh[t]/trials:6.0f}" for t in show))
    print("\n  Read: starved% = the 'mana is volatile' tax (a spell stranded under lands);")
    print("  flooded% = classic flood. Real feel sits between greedy and one. Compare the")
    print("  mean-dead-turns to the benchmark decks below.")


def bench_smoothness(trials):
    """mean dead turns + keepable for a couple roster reference points, so the merged
    number has a scale. Reads decks/ directly (these are active-roster lists)."""
    index = ds.load_oracle_index()
    aliases = ds.load_reskin_aliases()
    refs = [("world-shapers-merged (considering)", DECK),
            ("earthbend-the-meta (retiring)",
             ROOT / "decks" / "earthbend-the-meta-20260404-075423.txt"),
            ("the-genome-project (smooth ref)",
             ROOT / "decks" / "the-genome-project-20260510.txt"),
            ("croak-and-dagger (grind ref)",
             ROOT / "decks" / "croak-and-dagger-20260701.txt")]
    print("\n" + "=" * 78)
    print("  BENCHMARK — mean dead turns (greedy) + keepable%, same seed/trials")
    print("=" * 78)
    print("  deck".ljust(42) + "keepable%   mean-dead(greedy/one)")
    for name, path in refs:
        lib, commander, _ = ds.parse_deck(path, index, aliases)
        ident = sorted({c for _, r in lib for c in r["color_identity"]})
        st = ds.simulate(lib, ident, 10, trials, random.Random(SEED))
        dm = ds.draw_map(lib)
        fg = ds.simulate_flow(lib, 10, trials, random.Random(SEED), spend="greedy", draw_profiles=dm)
        f1 = ds.simulate_flow(lib, 10, trials, random.Random(SEED), spend="one", draw_profiles=dm)
        print(f"  {name:<40}{st['keepable_pct']:6.1f}      "
              f"{fg['mean_dead_turns']:.2f} / {f1['mean_dead_turns']:.2f}")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--mode", choices=["assembly", "smoothness", "all"], default="all")
    ap.add_argument("--trials", type=int, default=40000)
    ap.add_argument("--deck", type=Path, default=DECK,
                    help="decklist to study (default: the merged 2026-07-04 list) — "
                         "for A/B-ing swap-package variants")
    args = ap.parse_args()
    index = ds.load_oracle_index()
    aliases = ds.load_reskin_aliases()
    library, commander = slc.load_parsed(args.deck, index, aliases)
    print(f"library {len(library)} + commander {commander}   [{args.deck.name}]\n")
    if args.mode in ("assembly", "all"):
        mode_assembly(library, args.trials)
    if args.mode in ("smoothness", "all"):
        mode_smoothness(library, args.trials)
        bench_smoothness(args.trials)


if __name__ == "__main__":
    main()
