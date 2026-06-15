#!/usr/bin/env python3
"""tier_list.py — the definitive tier list, as a COMPOSITE of the three measured rankings.

The repo has three independent, lab-measured ways to rank a deck — and they DISAGREE at the
top (a 19/20 fortress can sit at 1% self-meta). This aggregates them into one honest composite
so the tier list isn't narrated:

  POWER    Conversion Check score /20 (the 20-point framework; CLOCKS[].score). "How good is
           the build." Authoritative but clock-blind — it rewards fortresses that can't close.
  SELF     self_meta_lab P(win | random 4-seat pod of your own decks). "Wins in YOUR pods."
  ANTIPOD  pod_gauntlet --vs blended P(win) vs the recurring T6-7 combo opponent. "Wins in the
           meta that actually matters."

Each axis is min-max normalised across the 16 decks; the composite weights the two
"does-it-actually-win" axes over raw build quality (the hard-won lesson of the whole lab
stack — closing > building):  ANTIPOD 0.40 · SELF 0.35 · POWER 0.25.  A deck with no formal
Conversion score (Zero-Sum, audit pending) is scored on the two win-axes only (weight
redistributed), and flagged.

Tiers are cut on the composite. This is a SYNTHESIS read, not a new sim — it just reuses the
existing labs (no narrated numbers). Caveats of each source are inherited (goldfish ceilings,
soft durability/disruption priors). Reproduce: `python scripts/tier_list.py`.

Writeup: analysis/Definitive_Tier_List_2026-06-15.md
"""
import argparse
import importlib.util
import random
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
for _s in (sys.stdout, sys.stderr):
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


pc = _load("pod_championship")          # -> pc.pg (pod_gauntlet), pc.sm (self_meta_lab)
pg, sm = pc.pg, pc.sm

W = {"antipod": 0.40, "self": 0.35, "power": 0.25}
# composite cutoffs, set on the roster's natural breaks (gaps at ~70 / 50 / 42 / 30)
TIERS = [("S", 70), ("A", 50), ("B", 42), ("C", 30), ("D", 0)]


def antipod_blend(slugs, C, trials, rng):
    out = {}
    for s in slugs:
        F = pg.build_cdf(C[s]["grid"], C[s]["decap"])
        per = {k: pg.simulate_vs(s, F, pg.OPPONENTS[k], pg.K_DIST, trials, rng)[0]
               for k in pg.OPPONENTS}
        out[s] = 100.0 * sum(pg.OPPONENTS[k]["weight"] * per[k] for k in pg.OPPONENTS)
    return out


def self_meta(slugs, C, trials, rng, t_grind):
    tcdf = {s: pg.build_cdf(C[s]["grid"], C[s]["table"]) for s in slugs}
    defense = sm.defense_counts()
    dura = {s: sm.durability(s, C, defense) for s in slugs}
    _, pwin = pc.seed_field(slugs, tcdf, dura, t_grind, trials, rng)
    return pwin


def power(slugs, C):
    out = {}
    for s in slugs:
        try:
            out[s] = float(C[s]["score"])
        except (TypeError, ValueError):
            out[s] = None              # unaudited (Zero-Sum)
    return out


def norm(d):
    vals = [v for v in d.values() if v is not None]
    lo, hi = min(vals), max(vals)
    return {k: (None if v is None else (100.0 * (v - lo) / (hi - lo) if hi > lo else 50.0))
            for k, v in d.items()}


def tier_of(comp):
    for name, cut in TIERS:
        if comp >= cut:
            return name
    return "D"


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--trials", type=int, default=40000)
    ap.add_argument("--t-grind", type=int, default=sm.T_GRIND)
    ap.add_argument("--seed", type=int, default=sm.SEED)
    args = ap.parse_args()

    rng = random.Random(args.seed)
    C = pg.merged_clocks()
    slugs = [s for s in sm.dl.ROSTER if s in C]
    names = {s: C[s]["name"] for s in slugs}

    raw = {
        "antipod": antipod_blend(slugs, C, args.trials, rng),
        "self": self_meta(slugs, C, args.trials, rng, args.t_grind),
        "power": power(slugs, C),
    }
    n = {ax: norm(raw[ax]) for ax in raw}

    comp = {}
    for s in slugs:
        parts = {ax: n[ax][s] for ax in W}
        avail = {ax: v for ax, v in parts.items() if v is not None}
        wsum = sum(W[ax] for ax in avail)
        comp[s] = sum(W[ax] * parts[ax] for ax in avail) / wsum
    order = sorted(slugs, key=lambda s: -comp[s])

    print(f"\n{'='*94}")
    print("THE DEFINITIVE TIER LIST — composite of POWER · SELF-META · ANTI-POD")
    print(f"{'='*94}")
    print(f"  weights: anti-pod {W['antipod']} · self-meta {W['self']} · power {W['power']}  "
          f"(closing > building)  ·  trials={args.trials}, T_grind={args.t_grind}\n")
    print(f"  {'tier':>4}  {'deck':24}{'pwr/20':>7}{'self%':>7}{'anti%':>7}"
          f"{'clock':>7}{'COMP':>7}")
    last = None
    for s in order:
        t = tier_of(comp[s])
        if t != last:
            print(f"  {'─'*4}  {('Tier '+t):─<54}")
            last = t
        scd = raw["power"][s]
        sct = f"{scd:.0f}" if scd is not None else "—"
        print(f"  {t:>4}  {names[s]:24}{sct:>7}{raw['self'][s]:>6.0f}%"
              f"{raw['antipod'][s]:>6.0f}%{C[s]['med'][1]:>7}{comp[s]:>7.0f}")
    print(f"\n  COMP = weighted mean of the three min-max-normalised axes (0-100). Each axis "
          f"inherits its\n  source's caveats (goldfish ceilings; soft durability/disruption "
          f"priors). Synthesis, not a new sim.")
    print(f"  Zero-Sum has no formal Conversion score (audit pending) — scored on the two "
          f"win-axes only.\n")


if __name__ == "__main__":
    main()
