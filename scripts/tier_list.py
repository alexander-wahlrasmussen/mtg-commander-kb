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

v2 (2026-06-28) ranks on the THREE convergent OUTCOME oracles (POWER → INTER replaces CC, which
becomes a context column); `--legacy-power` reproduces the v1 (CC-as-axis) composite.

Writeup: analysis/Definitive_Tier_List_2026-06-28.md  (v1: analysis/Definitive_Tier_List_2026-06-15.md)
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
im = _load("interaction_meta_lab")      # the interaction-overlay oracle (added 2026-06-27)

# --- v2 (default): THREE convergent OUTCOME oracles. CC drops out of the composite (it's
#     clock-blind — shown only as a context column). The mirror bar is measured twice, at two
#     fidelities (self_meta + its interaction refinement); together they outweigh the single
#     external-pod axis, but the external pod stays the largest SINGLE axis ("the meta that
#     matters"). INTER, the more complete mirror oracle, carries more than raw SELF.
W_V2 = {"antipod": 0.45, "inter": 0.35, "self": 0.20}
TIERS_V2 = [("S", 70), ("A", 52), ("B", 40), ("C", 28), ("D", 0)]
# --- v1 (--legacy-power): the 2026-06-15 composite (CC as the build-quality axis).
W_V1 = {"antipod": 0.40, "self": 0.35, "power": 0.25}
TIERS_V1 = [("S", 70), ("A", 50), ("B", 42), ("C", 30), ("D", 0)]


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


def interaction(slugs, C, trials, rng, t_grind, tax):
    """The interaction-overlay mirror oracle (self_meta + a measured interaction tax). Reuses
    im.simulate (the same engine the lab prints), restricted to im's MEASURED pod order."""
    mslugs = [s for s in slugs if s in pg.MEASURED]
    tcdf = {s: pg.build_cdf(C[s]["grid"], C[s]["table"]) for s in mslugs}
    defense = sm.defense_counts()
    dura = {s: sm.durability(s, C, defense) for s in mslugs}
    _, inter, appear = im.simulate(mslugs, C, tcdf, dura, trials, tax, t_grind, rng)
    return {s: (100.0 * inter[s] / (appear[s] or 1) if s in inter else None) for s in slugs}


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


def tier_of(comp, tiers):
    for name, cut in tiers:
        if comp >= cut:
            return name
    return "D"


def compute_rows(trials=40000, t_grind=None, tax=None, seed=None, legacy=False):
    """The shared v2 (or legacy v1) ranking core behind main()'s print AND the dashboard's
    /api/tierlist. Returns dict(version, weights, tiers, tax, t_grind, trials, rows) with rows
    ordered COMP-descending; each row carries the FULL-precision axis values (anti/inter/self/cc),
    the COMP, the tier letter, and the deck's clock. Rounding/formatting is the caller's job —
    so the CLI's printed numbers stay byte-identical to before this was factored out."""
    t_grind = sm.T_GRIND if t_grind is None else t_grind
    tax = im.TAX if tax is None else tax
    seed = sm.SEED if seed is None else seed
    W, TIERS = (W_V1, TIERS_V1) if legacy else (W_V2, TIERS_V2)
    rng = random.Random(seed)
    C = pg.merged_clocks()
    slugs = [s for s in sm.dl.ROSTER if s in C]
    raw = {
        "antipod": antipod_blend(slugs, C, trials, rng),
        "self": self_meta(slugs, C, trials, rng, t_grind),
        "power": power(slugs, C),
    }
    if not legacy:
        raw["inter"] = interaction(slugs, C, trials, rng, t_grind, tax)
    n = {ax: norm(raw[ax]) for ax in raw}
    comp = {}
    for s in slugs:
        parts = {ax: n[ax][s] for ax in W}
        avail = {ax: v for ax, v in parts.items() if v is not None}
        wsum = sum(W[ax] for ax in avail)
        comp[s] = sum(W[ax] * parts[ax] for ax in avail) / wsum
    order = sorted(slugs, key=lambda s: -comp[s])
    rows = [dict(
        slug=s, name=C[s]["name"], tier=tier_of(comp[s], TIERS), comp=comp[s],
        anti=raw["antipod"][s], self=raw["self"][s],
        inter=(raw["inter"][s] if not legacy else None),
        cc=raw["power"][s], decap=C[s]["med"][0], table=C[s]["med"][1],
    ) for s in order]
    return dict(version=("v1" if legacy else "v2"), weights=W,
                tiers=[t for t, _ in TIERS], tax=tax, t_grind=t_grind,
                trials=trials, rows=rows)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--trials", type=int, default=40000)
    ap.add_argument("--t-grind", type=int, default=sm.T_GRIND)
    ap.add_argument("--seed", type=int, default=sm.SEED)
    ap.add_argument("--tax", type=float, default=im.TAX, help="interaction-overlay tax (v2 axis)")
    ap.add_argument("--legacy-power", action="store_true",
                    help="reproduce the 2026-06-15 composite (CC as the 3rd axis, no overlay)")
    args = ap.parse_args()

    payload = compute_rows(args.trials, args.t_grind, args.tax, args.seed, args.legacy_power)
    rows, W = payload["rows"], payload["weights"]

    if args.legacy_power:
        title = "THE DEFINITIVE TIER LIST (v1, legacy) — composite of POWER · SELF-META · ANTI-POD"
        wline = (f"  weights: anti-pod {W['antipod']} · self-meta {W['self']} · power "
                 f"{W['power']}  (closing > building)")
        cols = f"  {'tier':>4}  {'deck':24}{'pwr/20':>7}{'self%':>7}{'anti%':>7}{'clock':>7}{'COMP':>7}"
    else:
        title = "THE DEFINITIVE TIER LIST (v2) — composite of THREE convergent OUTCOME oracles"
        wline = (f"  weights: anti-pod {W['antipod']} · interaction {W['inter']} · self-meta "
                 f"{W['self']}  (CC = context only)  ·  tax={args.tax}")
        cols = (f"  {'tier':>4}  {'deck':24}{'anti%':>7}{'inter%':>7}{'self%':>7}"
                f"{'(cc)':>6}{'clock':>7}{'COMP':>7}")

    print(f"\n{'='*94}\n{title}\n{'='*94}")
    print(f"{wline}  ·  trials={args.trials}, T_grind={args.t_grind}\n")
    print(cols)
    last = None
    for r in rows:
        t = r["tier"]
        if t != last:
            print(f"  {'─'*4}  {('Tier '+t):─<60}")
            last = t
        sct = f"{r['cc']:.0f}" if r["cc"] is not None else "—"
        if args.legacy_power:
            print(f"  {t:>4}  {r['name']:24}{sct:>7}{r['self']:>6.0f}%"
                  f"{r['anti']:>6.0f}%{r['table']:>7}{r['comp']:>7.0f}")
        else:
            ivs = f"{r['inter']:.0f}%" if r["inter"] is not None else "—"
            print(f"  {t:>4}  {r['name']:24}{r['anti']:>6.0f}%{ivs:>7}"
                  f"{r['self']:>6.0f}%{sct:>6}{r['table']:>7}{r['comp']:>7.0f}")
    print(f"\n  COMP = weighted mean of the min-max-normalised axes (0-100). Each axis inherits "
          f"its\n  source's caveats (goldfish ceilings; soft durability/disruption priors). "
          f"Synthesis, not a new sim.")
    if not args.legacy_power:
        print(f"  v2 ranks by the three OUTCOME oracles; CC (cc) is shown for contrast, NOT in the "
              f"composite.\n  self%/inter% are the SAME mirror bar at two fidelities (inter = "
              f"self + interaction tax).\n  Zero-Sum has no Conversion score (—); v2 scores it "
              f"fully (CC isn't a composite axis).\n  Legacy 2026-06-15 list: --legacy-power.\n")
    else:
        print(f"  Zero-Sum has no formal Conversion score (audit pending) — scored on the two "
              f"win-axes only.\n")


if __name__ == "__main__":
    main()
