#!/usr/bin/env python3
"""pod_championship.py — crown a champion of the 16 active decks.

The fun finale (2026-06-15). self_meta_lab.py answers "P(win | in a RANDOM 4-seat pod
of my own decks)". This stages an actual TOURNAMENT on the same engine:

  REGULAR SEASON  the self-meta ranking (random-pod P(win)) -> seeds 1..16.
  GROUP STAGE     a pot-based RANDOM DRAW: split the 16 seeds into 4 pots (1-4, 5-8,
                  9-12, 13-16) and draw one deck from each pot into each of 4 pods, so
                  every pod is balanced but the field is freshly shuffled each run. Each
                  pod is simulated over --trials games; highest WIN SHARE ADVANCES.
                  (--snake forces the old deterministic 1-8-9-16 bracket; --draw-seed
                  reproduces a specific draw.)
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


def draw_groups(seeds, rng):
    """Pot-based RANDOM draw: split the 16 ranked seeds into 4 pots (1-4, 5-8, 9-12,
    13-16) and deal one deck from each pot into each of the 4 pods. Every pod gets
    exactly one deck from each pot (balanced like the snake) but which decks land
    together is shuffled — a fresh, valid bracket per `rng`."""
    groups = [[], [], [], []]
    for p in range(4):
        pot = seeds[4 * p:4 * p + 4]
        rng.shuffle(pot)
        for pod_i, slug in enumerate(pot):
            groups[pod_i].append(slug)
    return groups


def fmt(slug, names, seedmap):
    return f"{names[slug]} (#{seedmap[slug]})"


def med_turn(grid, cum):
    """Median-close turn label from a (grid, cumulative%) curve, for display."""
    for t, c in zip(grid, cum):
        if c >= 50:
            return f"T{t}"
    return f">T{grid[-1]}"


def swapped_clocks(slugs, C, defense, swapped):
    """Table CDFs + durability, optionally with pod_gauntlet.SWAPS applied (Build_And_Swap §2).
    The tournament RACES TABLE clocks, so only a swap carrying a `table` curve moves it — that
    is just Calamity's grind-fortress rebuild. The decap-only (Grand Design ramp) and
    resilience-only (Exile/Replication Kiki, Diminishing Deathmantle) swaps add value this
    goldfish table engine cannot score; they're applied-but-inert here and reported as such.
    Returns (tcdf, dura, disp, changed): disp[s]=(med,never) for the table; changed=movers."""
    tcdf, dura, disp, changed = {}, {}, {}, []
    for s in slugs:
        sw = pg.SWAPS.get(s) if swapped else None
        if sw and sw.get("table") is not None:
            grid, tab = sw["grid"], sw["table"]
            never = 100 - tab[-1]
            med = med_turn(grid, tab)          # no stored median for the swap; derive it
            changed.append(s)
        else:
            grid, tab = C[s]["grid"], C[s]["table"]
            never = C[s]["never"][1]
            med = C[s]["med"][1]               # keep the lab's stored median (consistent display)
        tcdf[s] = pg.build_cdf(grid, tab)
        disp[s] = (med, never)
        inev = 1.0 - never / 100.0
        dfn = min(1.0, defense.get(s, 0) / sm.DEF_NORM)
        fed = sm.OPP_FED.get(s, 0.0)
        dura[s] = max(0.0, min(1.0, sm.W_INEV * inev + sm.W_DEF * dfn + sm.W_FED * fed))
    return tcdf, dura, disp, changed


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--trials", type=int, default=60000, help="games per playoff pod")
    ap.add_argument("--season-trials", type=int, default=120000, help="random pods for seeding")
    ap.add_argument("--t-grind", type=int, default=sm.T_GRIND)
    ap.add_argument("--seed", type=int, default=sm.SEED,
                    help="RNG for the regular-season seeding (fixed -> stable seeds/pots)")
    ap.add_argument("--draw-seed", type=int, default=None,
                    help="RNG for the group draw + playoffs (default: fresh random each run)")
    ap.add_argument("--snake", action="store_true",
                    help="force the old deterministic snake bracket (1-8-9-16, ...) instead of a draw")
    ap.add_argument("--md", action="store_true", help="emit the markdown writeup to stdout")
    ap.add_argument("--swapped", action="store_true",
                    help="apply all proposed swaps (pod_gauntlet.SWAPS / Build_And_Swap §2)")
    args = ap.parse_args()

    # Two RNGs: the season seed is fixed so the seeds/pots are stable; the draw seed
    # shuffles the pots into pods (and drives the playoff sims) — fresh each run unless pinned.
    season_rng = random.Random(args.seed)
    draw_seed = args.draw_seed if args.draw_seed is not None else random.randrange(1 << 30)
    draw_rng = random.Random(draw_seed)
    C = pg.merged_clocks()
    slugs = [s for s in sm.dl.ROSTER if s in C]
    names = {s: C[s]["name"] for s in slugs}
    defense = sm.defense_counts()
    tcdf, dura, disp, changed = swapped_clocks(slugs, C, defense, args.swapped)

    seeds, pwin = seed_field(slugs, tcdf, dura, args.t_grind, args.season_trials, season_rng)
    seedmap = {s: i + 1 for i, s in enumerate(seeds)}
    groups = snake_groups(seeds) if args.snake else draw_groups(seeds, draw_rng)

    out = []  # markdown lines, mirrored to terminal sections below

    # ---- regular season ----------------------------------------------------
    tag = "  [ALL PROPOSED SWAPS APPLIED]" if args.swapped else ""
    print(f"\n{'='*78}")
    print(f"🏆  THE POD CHAMPIONSHIP  —  16 decks, one crown{tag}")
    print(f"{'='*78}")
    print(f"  engine: self_meta_lab table-clock race + durability  ·  T_grind={args.t_grind}")
    print(f"  seeding={args.season_trials} random pods  ·  playoff pods={args.trials} games each")
    draw_label = "snake (deterministic)" if args.snake else f"pot-based random draw (draw-seed={draw_seed})"
    print(f"  group stage: {draw_label}")
    if args.swapped:
        movers = ", ".join(names[s] for s in changed) or "(none)"
        print(f"  swaps that move the TABLE clock: {movers}")
        print(f"  decap-only / resilience-only swaps (GD ramp, Exile/Replication Kiki, "
              f"Diminishing Deathmantle) are\n  applied but inert here — the table goldfish "
              f"can't score them.")
    print()
    print("  REGULAR SEASON — seeded by P(win | random 4-seat pod)")
    print(f"  {'seed':>4}  {'deck':24}{'table':>7}{'never':>7}{'dura':>6}{'P(win)':>8}")
    for i, s in enumerate(seeds, 1):
        mark = " ←swap" if s in changed else ""
        print(f"  {i:>4}  {names[s]:24}{disp[s][0]:>7}{disp[s][1]:>6}%"
              f"{dura[s]:>6.2f}{pwin[s]:>7.0f}%{mark}")

    # ---- group stage -------------------------------------------------------
    drawn = "snake-seeded" if args.snake else "randomly drawn (pot-balanced)"
    print(f"\n  GROUP STAGE — 4 {drawn} pods, highest win share advances")
    winners = []
    group_results = []
    for gi, pod in enumerate(groups):
        pod = sorted(pod, key=lambda s: seedmap[s])
        shares = pod_shares(pod, tcdf, dura, args.t_grind, args.trials, draw_rng)
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
    shares = pod_shares(final, tcdf, dura, args.t_grind, args.trials, draw_rng)
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
