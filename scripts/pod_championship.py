#!/usr/bin/env python3
"""pod_championship.py — crown a champion of the 16 active decks.

The fun finale (2026-06-15). self_meta_lab.py answers "P(win | in a RANDOM 4-seat pod
of my own decks)". This stages an actual TOURNAMENT on the same engine:

  REGULAR SEASON  the self-meta ranking (random-pod P(win)) -> seeds 1..16.
  GROUP STAGE     snake-seed the 16 into 4 balanced pods of 4 (1-8-9-16, 2-7-10-15,
                  3-6-11-14, 4-5-12-13). Each pod is simulated over --trials games;
                  the deck with the highest WIN SHARE in that pod ADVANCES.
  FINAL FOUR      the 4 group winners play one last 4-seat pod -> CHAMPION.

The per-game winner of a pod is decided EXACTLY as in self_meta_lab.run():
  * each seat samples a TABLE-close turn from its lab table CDF (pod_gauntlet_clocks.json);
  * if the earliest close is <= T_grind, that seat wins (CLOSE-RACE, lab-measured);
  * else the most DURABLE seat outlasts (durability overlay — documented judgment, swept).

This reuses self_meta_lab's clocks, defense_counts(), and durability() unchanged, so the
championship and the self-meta ranking are the same model — one just brackets the other.

HONESTY (gauntlet discipline, inherited): table clocks are UNBLOCKED goldfish ceilings; the
durability tiebreak and T_grind are judgment, not a 4-body rules engine. Trust the bracket
shape and the upsets, not the second decimal. It's a celebration of the lab stack, scored
on real curves — not a ladder ranking to retune a deck on.

Writeup: analysis/Pod_Championship_2026-06-15.md
"""
import argparse
import importlib.util
import random
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent

for _s in (sys.stdout, sys.stderr):            # box-drawing + trophy glyphs
    if hasattr(_s, "reconfigure"):
        try:
            _s.reconfigure(encoding="utf-8", errors="replace")
        except (ValueError, OSError):
            pass


def _load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


sm = _load("self_meta_lab")            # reuse the SAME engine the ranking is built on
pg = sm.pg                             # pod_gauntlet (clocks, build_cdf, sample_kill, HORIZON)


def pod_game(pod, tcdf, dura, t_grind, rng):
    """One game of a fixed pod -> the winning seat(s) (shared ties), per self_meta_lab."""
    turns = {s: pg.sample_kill(tcdf[s], rng) for s in pod}
    tmin = min(turns.values())
    if tmin <= t_grind:
        return [s for s in pod if turns[s] == tmin]
    dmax = max(dura[s] for s in pod)
    return [s for s in pod if abs(dura[s] - dmax) < 1e-9]


def pod_shares(pod, tcdf, dura, t_grind, trials, rng):
    """Win share for each seat in a fixed pod over `trials` games."""
    win = {s: 0.0 for s in pod}
    for _ in range(trials):
        champs = pod_game(pod, tcdf, dura, t_grind, rng)
        for s in champs:
            win[s] += 1.0 / len(champs)
    return {s: win[s] / trials for s in pod}


def seed_field(slugs, tcdf, dura, t_grind, trials, rng):
    """Regular season: P(win | random 4-seat pod) per deck -> ranked seeds (== self_meta)."""
    win = {s: 0.0 for s in slugs}
    appear = {s: 0 for s in slugs}
    for _ in range(trials):
        pod = rng.sample(slugs, 4)
        for s in pod:
            appear[s] += 1
        champs = pod_game(pod, tcdf, dura, t_grind, rng)
        for s in champs:
            win[s] += 1.0 / len(champs)
    pwin = {s: 100.0 * win[s] / (appear[s] or 1) for s in slugs}
    return sorted(slugs, key=lambda s: -pwin[s]), pwin


def snake_groups(seeds):
    """Snake-seed 16 ranked seeds into 4 balanced pods: 1-8-9-16, 2-7-10-15, ..."""
    groups = [[], [], [], []]
    order = list(range(4)) + list(range(3, -1, -1))   # 0,1,2,3,3,2,1,0
    for i, slug in enumerate(seeds):
        groups[order[i % 8]].append(slug)
    return groups


def fmt(slug, names, seedmap):
    return f"{names[slug]} (#{seedmap[slug]})"


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--trials", type=int, default=60000, help="games per playoff pod")
    ap.add_argument("--season-trials", type=int, default=120000, help="random pods for seeding")
    ap.add_argument("--t-grind", type=int, default=sm.T_GRIND)
    ap.add_argument("--seed", type=int, default=sm.SEED)
    ap.add_argument("--md", action="store_true", help="emit the markdown writeup to stdout")
    args = ap.parse_args()

    rng = random.Random(args.seed)
    C = pg.merged_clocks()
    slugs = [s for s in sm.dl.ROSTER if s in C]
    names = {s: C[s]["name"] for s in slugs}
    tcdf = {s: pg.build_cdf(C[s]["grid"], C[s]["table"]) for s in slugs}
    defense = sm.defense_counts()
    dura = {s: sm.durability(s, C, defense) for s in slugs}

    seeds, pwin = seed_field(slugs, tcdf, dura, args.t_grind, args.season_trials, rng)
    seedmap = {s: i + 1 for i, s in enumerate(seeds)}
    groups = snake_groups(seeds)

    out = []  # markdown lines, mirrored to terminal sections below

    # ---- regular season ----------------------------------------------------
    print(f"\n{'='*78}")
    print("🏆  THE POD CHAMPIONSHIP  —  16 decks, one crown")
    print(f"{'='*78}")
    print(f"  engine: self_meta_lab table-clock race + durability  ·  T_grind={args.t_grind}")
    print(f"  seeding={args.season_trials} random pods  ·  playoff pods={args.trials} games each\n")
    print("  REGULAR SEASON — seeded by P(win | random 4-seat pod)")
    print(f"  {'seed':>4}  {'deck':24}{'table':>7}{'never':>7}{'dura':>6}{'P(win)':>8}")
    for i, s in enumerate(seeds, 1):
        print(f"  {i:>4}  {names[s]:24}{C[s]['med'][1]:>7}{C[s]['never'][1]:>6}%"
              f"{dura[s]:>6.2f}{pwin[s]:>7.0f}%")

    # ---- group stage -------------------------------------------------------
    print(f"\n  GROUP STAGE — 4 snake-seeded pods, highest win share advances")
    winners = []
    group_results = []
    for gi, pod in enumerate(groups):
        pod = sorted(pod, key=lambda s: seedmap[s])
        shares = pod_shares(pod, tcdf, dura, args.t_grind, args.trials, rng)
        ranked = sorted(pod, key=lambda s: -shares[s])
        w = ranked[0]
        winners.append(w)
        group_results.append((gi, ranked, shares))
        print(f"\n   Pod {chr(65+gi)}:")
        for s in ranked:
            tag = "  ➜ ADVANCES" if s == w else ""
            print(f"      {shares[s]*100:>5.1f}%   {fmt(s, names, seedmap)}{tag}")

    # ---- final -------------------------------------------------------------
    final = sorted(winners, key=lambda s: seedmap[s])
    shares = pod_shares(final, tcdf, dura, args.t_grind, args.trials, rng)
    ranked = sorted(final, key=lambda s: -shares[s])
    champ = ranked[0]
    print(f"\n  THE FINAL FOUR")
    for i, s in enumerate(ranked):
        medal = ["🥇", "🥈", "🥉", "  "][i]
        print(f"      {medal} {shares[s]*100:>5.1f}%   {fmt(s, names, seedmap)}")

    print(f"\n{'='*78}")
    print(f"  🏆  CHAMPION:  {names[champ]}   (seed #{seedmap[champ]})")
    print(f"{'='*78}")

    # upset / story note
    runner = ranked[1]
    cinderella = max(winners, key=lambda s: seedmap[s])
    print(f"\n  Runner-up: {fmt(runner, names, seedmap)}")
    if seedmap[champ] > 1:
        print(f"  UPSET — the #{seedmap[champ]} seed took the crown over the field's top seed "
              f"({fmt(seeds[0], names, seedmap)}).")
    if seedmap[cinderella] >= 9:
        print(f"  Cinderella run: {fmt(cinderella, names, seedmap)} escaped its group from "
              f"the bottom half.")
    print(f"\n  Reminder: table clocks are goldfish ceilings; the durability tiebreak is judgment.")
    print(f"  This is a celebration of the lab stack on real curves — not a deck-tuning ranking.\n")


if __name__ == "__main__":
    main()
