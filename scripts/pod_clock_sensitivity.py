#!/usr/bin/env python3
"""pod_clock_sensitivity.py — Phase 0 of "measure the pod": is the tier list ROBUST to K_DIST?

Every ANTI-POD number in the tower races the OPPONENT PROFILE K_DIST (pod_gauntlet.py:
"wins T6-7", mean T6.70) — a hand-assumed distribution, never lab-measured. The repo's
deepest learning is that hand-estimated kill windows were falsified 7-of-8 times when labbed
(project_framework_clock_gap) — and the pod's clock is the LAST hand-estimated clock still
load-bearing. Before paying for the fix (reconstruct + clock-lab the pod's actual decks),
this measures whether the assumption MATTERS: sweep the profile, watch the tier verdicts.

WHAT SWEEPS / WHAT'S HELD FIXED (attribution by construction):
  swept  K_DIST shifted by δ ∈ {-2..+2} whole turns (mean ~T4.65 → ~T8.65), plus the two
         preset SHAPES pod_gauntlet already carries (--pod-fast / --pod-slow, via pod_kdist).
  moves  ONLY the ANTI-POD axis — pg.simulate_vs over the OPPONENTS blend, the exact model
         tier_list.antipod_blend runs, with the kdist injected instead of pg.K_DIST.
  fixed  INTER / SELF raw values at the compute_rows baseline (they race the roster's own
         table clocks; the pod profile never enters them). CC is context-only in v2 anyway.
  redone min-max norm + COMP + tier cut per sweep point (tier_list math REUSED, not copied).

READING IT: min-max normalisation cancels any UNIFORM anti-pod shift — only DIFFERENTIAL
movement (a fortress gaining more from a slower pod than a racer does) can move a tier. So a
tier flip here is real ranking sensitivity, not "everything got better against a slow pod."

CAVEATS (honest-instrument notes):
  * Disruption rows are measured on K∈{6,7} and CLAMPED outside (pod_gauntlet.disruption):
    at δ=-2 our answers are slightly OVERstated (a T6 row answering a K4 attempt), at δ=+2
    slightly UNDERstated (T7 row for a K9 attempt). Both compress the sweep, so the measured
    sensitivity is a mild FLOOR. MEASURED row deltas are ≤4pp — second-order vs the K shift.
  * MC noise: the δ=0 column is recomputed with this tool's own rng threading; its max gap vs
    the compute_rows baseline anti% is printed as the NOISE YARDSTICK. Trust tier letters and
    the ranking, not the second decimal (house rule).
  * PURE RACE (closed form Σ p_K·F_decap(K), zero noise) is reported alongside as the exact
    race-only sensitivity — the MC columns add the answer/protect overlay on top of it.

Verdict per deck: ROBUST (same tier at every profile) · EDGE (tier moves only at the |δ|=2
extremes) · SENSITIVE (tier moves within ±1 turn of baseline — the plausible band).

Phase 1/2 (reconstruct + clock-lab the pod's actual decks) is justified only if verdicts are
SENSITIVE inside the plausible band. Writeup: analysis/Pod_Clock_Sensitivity_2026-07-02.md
"""
import argparse
import importlib.util
import random
import sys
from pathlib import Path
from types import SimpleNamespace

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


tl = _load("tier_list")                 # -> tl.pg (pod_gauntlet), tl.sm, tl.norm, tl.W_V2 ...
pg = tl.pg
fb = _load("framework_bakeoff")         # -> fb.spearman (tie-aware; the canonical impl)


# --- pure helpers (hermetically tested in tests/test_pod_clock_sensitivity.py) ---
def shift_kdist(kdist, delta):
    """Shift the whole profile by `delta` turns, shape preserved. Keys stay >= 1."""
    out = {}
    for k, p in kdist.items():
        nk = max(1, k + delta)
        out[nk] = out.get(nk, 0.0) + p          # clamp-merge (only fires at absurd deltas)
    return out


def kdist_mean(kdist):
    return sum(k * p for k, p in kdist.items())


def composite(raw, W=None, TIERS=None):
    """The exact compute_rows composite math (tier_list.py) on raw axis dicts:
    min-max norm per axis -> weighted mean with None-weight redistribution -> tier cut.
    raw = {axis: {slug: value|None}} restricted to the axes in W (v2: antipod/inter/self).
    Returns {slug: (comp, tier)}."""
    W = tl.W_V2 if W is None else W
    TIERS = tl.TIERS_V2 if TIERS is None else TIERS
    n = {ax: tl.norm(raw[ax]) for ax in W}
    out = {}
    for s in raw["antipod"]:
        parts = {ax: n[ax][s] for ax in W}
        avail = {ax: v for ax, v in parts.items() if v is not None}
        wsum = sum(W[ax] for ax in avail)
        comp = sum(W[ax] * parts[ax] for ax in avail) / wsum
        out[s] = (comp, tl.tier_of(comp, TIERS))
    return out


def verdict(tiers_by_profile, base_tier, deltas):
    """ROBUST / EDGE / SENSITIVE from the per-profile tier letters (see module docstring).
    tiers_by_profile: {profile_key: tier}; deltas: {profile_key: |shift| or None (presets,
    treated as inside the plausible band — they are alternative T6-7 shapes)."""
    moved_in = [k for k, t in tiers_by_profile.items()
                if t != base_tier and (deltas.get(k) is None or deltas[k] <= 1)]
    moved_edge = [k for k, t in tiers_by_profile.items()
                  if t != base_tier and deltas.get(k) is not None and deltas[k] >= 2]
    if moved_in:
        return "SENSITIVE"
    if moved_edge:
        return "EDGE"
    return "ROBUST"


# --- the sweep --------------------------------------------------------------
def antipod_for(kdist, slugs, C, trials, seed):
    """tier_list.antipod_blend with the kdist INJECTED (and its own rng, so every profile
    is computed under identical threading — profile deltas are signal, not rng drift)."""
    rng = random.Random(seed)
    out = {}
    for s in slugs:
        F = pg.build_cdf(C[s]["grid"], C[s]["decap"])
        per = {k: pg.simulate_vs(s, F, pg.OPPONENTS[k], kdist, trials, rng)[0]
               for k in pg.OPPONENTS}
        out[s] = 100.0 * sum(pg.OPPONENTS[k]["weight"] * per[k] for k in pg.OPPONENTS)
    return out


def pure_race_for(kdist, slugs, C):
    """Closed-form P(decap <= K) per deck — analytic, zero-noise (pg.pure_race)."""
    return {s: 100.0 * pg.pure_race(pg.build_cdf(C[s]["grid"], C[s]["decap"]), kdist)
            for s in slugs}


def antipod_measured(slugs, C, trials, seed):
    """The FULL measured model (Backlog #13 Phase 3): pg.set_profile(True) swaps in the four
    real opponents (Acererak v2 / Ur-Dragon / H&K / Henzie), each with its own MEASURED K curve,
    the observed-rotation weights, and the no-Abolisher disruption. Unlike a δ-shift this is not
    a single global kdist — it changes K per opponent AND weights AND disruption together — so
    it's reported as its own column, not a sweep point. Restores the default profile after."""
    pg.set_profile(True)
    try:
        rng = random.Random(seed)
        out = {}
        for s in slugs:
            F = pg.build_cdf(C[s]["grid"], C[s]["decap"])
            per = {k: pg.simulate_vs(s, F, pg.OPPONENTS[k], None, trials, rng)[0]
                   for k in pg.OPPONENTS}     # kdist=None -> each opp uses its own measured curve
            out[s] = 100.0 * sum(pg.OPPONENTS[k]["weight"] * per[k] for k in pg.OPPONENTS)
    finally:
        pg.set_profile(False)
    return out


def profiles(deltas):
    """(key, kdist, |δ| or None) — δ-shifts of K_DIST + pod_gauntlet's two preset shapes,
    ordered by profile mean so the table reads fast -> slow."""
    ps = [(f"{d:+d}" if d else "base", shift_kdist(pg.K_DIST, d), abs(d)) for d in deltas]
    for flag in ("pod_fast", "pod_slow"):
        kd = pg.pod_kdist(SimpleNamespace(pod_fast=flag == "pod_fast",
                                          pod_slow=flag == "pod_slow"))
        ps.append((flag.replace("pod_", ""), kd, None))
    return sorted(ps, key=lambda p: kdist_mean(p[1]))


def run(trials, seed, deltas):
    print(f"# pod-clock sensitivity — baseline tier_list.compute_rows @ {trials} trials "
          f"(seed {seed}) ...", flush=True)
    base = tl.compute_rows(trials=trials, seed=seed)
    rows = {r["slug"]: r for r in base["rows"]}
    slugs = list(rows)
    order = [r["slug"] for r in base["rows"]]                 # COMP-descending
    C = pg.merged_clocks()
    fixed = {"inter": {s: rows[s]["inter"] for s in slugs},
             "self": {s: rows[s]["self"] for s in slugs}}

    profs = profiles(deltas)
    res = {}                                                  # key -> (kdist, anti, comp/tier)
    for key, kd, _d in profs:
        print(f"  sweeping {key:5} (mean T{kdist_mean(kd):.2f}) ...", flush=True)
        anti = antipod_for(kd, slugs, C, trials, seed)
        res[key] = (kd, anti, composite({"antipod": anti, **fixed}),
                    pure_race_for(kd, slugs, C))
    dmap = {key: d for key, _, d in profs}

    # --- report -------------------------------------------------------------
    keys = [k for k, _, _ in profs]
    base_key = "base"
    noise = max(abs(res[base_key][1][s] - rows[s]["anti"]) for s in slugs)
    print(f"\n{'='*100}\nPOD-CLOCK SENSITIVITY — the tier list vs the hand-assumed K_DIST"
          f"\n{'='*100}")
    print(f"  baseline K_DIST mean T{kdist_mean(pg.K_DIST):.2f} ('wins T6-7'); swept means "
          f"T{kdist_mean(profs[0][1]):.2f} -> T{kdist_mean(profs[-1][1]):.2f}"
          f"   ·   trials={trials}, seed={seed}")
    print(f"  INTER/SELF held at baseline (pod-profile-independent); only ANTI-POD moves."
          f"\n  MC-noise yardstick: recomputed base vs compute_rows anti = "
          f"{noise:.1f}pp max abs gap.\n")

    hdr = "".join(f"{k:>7}" for k in keys)
    print(f"  ANTI-POD % by profile (raw axis; min-max norm cancels uniform shift)")
    print(f"  {'deck':26}{hdr}")
    print(f"  {'(profile mean)':26}" + "".join(f"{'T%.1f' % kdist_mean(res[k][0]):>7}"
                                               for k in keys))
    for s in order:
        print(f"  {rows[s]['name']:26}" + "".join(f"{res[k][1][s]:>7.0f}" for k in keys))

    print(f"\n  PURE RACE % (closed form, zero noise) — the race component alone")
    print(f"  {'deck':26}{hdr}")
    for s in order:
        print(f"  {rows[s]['name']:26}" + "".join(f"{res[k][3][s]:>7.0f}" for k in keys))

    print(f"\n  TIER by profile (v2 composite, INTER/SELF fixed)   ·   base tier from the "
          f"live compute_rows")
    print(f"  {'deck':26}{'live':>6}{hdr}   verdict")
    flips = []
    for s in order:
        tiers = {k: res[k][2][s][1] for k in keys}
        v = verdict(tiers, rows[s]["tier"], dmap)
        if v != "ROBUST":
            flips.append((s, v))
        print(f"  {rows[s]['name']:26}{rows[s]['tier']:>6}" +
              "".join(f"{tiers[k]:>7}" for k in keys) + f"   {v}")

    base_comp = [rows[s]["comp"] for s in order]
    print(f"\n  RANK STABILITY — Spearman rho of the swept COMP vs the live baseline COMP")
    for k in keys:
        rho, n = fb.spearman(base_comp, [res[k][2][s][0] for s in order])
        print(f"    {k:5} (mean T{kdist_mean(res[k][0]):.2f}):  rho={rho}  (n={n})")

    print(f"\n  VERDICT SUMMARY: {sum(1 for s in order if (s, 'SENSITIVE') in flips)} "
          f"SENSITIVE, {sum(1 for s in order if (s, 'EDGE') in flips)} EDGE, "
          f"{len(order) - len(flips)} ROBUST of {len(order)}.")
    if flips:
        for s, v in flips:
            tiers = {k: res[k][2][s][1] for k in keys}
            path = " ".join(f"{k}:{tiers[k]}" for k in keys if tiers[k] != rows[s]["tier"])
            print(f"    {v:9} {rows[s]['name']:26} live {rows[s]['tier']} -> {path}")
    print(f"\n  Read: SENSITIVE inside ±1 turn = the hand-assumed pod clock is load-bearing "
          f"there -> Phase 1/2\n  (reconstruct + lab the pod decks) is justified. "
          f"All-ROBUST = the tier list survives the assumption.\n")

    # --- Phase 3: the tier list AT the MEASURED profile (not a sweep point) -----------------
    print(f"{'='*100}\nAT THE MEASURED PROFILE — the full Phase-3 model vs the hand-assumed baseline"
          f"\n{'='*100}")
    print(f"  pg.set_profile(True): four real opponents (Acererak v2 / Ur-Dragon / H&K / Henzie),")
    print(f"  per-opponent MEASURED K + observed-rotation weights + no-Abolisher disruption. INTER/")
    print(f"  SELF held at baseline (pod-independent). This is the whole point of Backlog #13.\n")
    m_anti = antipod_measured(slugs, C, trials, seed)
    m_comp = composite({"antipod": m_anti, **fixed})
    print(f"  {'deck':26}{'base tier':>10}{'meas tier':>10}{'base anti%':>12}{'meas anti%':>12}   move")
    moved = []
    for s in order:
        bt, mt = rows[s]["tier"], m_comp[s][1]
        arrow = "" if bt == mt else f"  {bt}->{mt}"
        if bt != mt:
            moved.append((s, bt, mt))
        print(f"  {rows[s]['name']:26}{bt:>10}{mt:>10}{rows[s]['anti']:>11.0f}%"
              f"{m_anti[s]:>11.0f}%{arrow}")
    rho, n = fb.spearman([rows[s]["comp"] for s in order], [m_comp[s][0] for s in order])
    print(f"\n  RANK STABILITY vs baseline: Spearman rho={rho} (n={n}).")
    print(f"  TIER MOVES under the measured profile: {len(moved)} of {len(order)}"
          + ("" if not moved else " — " + ", ".join(f"{rows[s]['name']} {b}->{m}"
                                                     for s, b, m in moved)))
    print(f"\n  CAVEATS (load-bearing): both sides are UNBLOCKED goldfish ceilings (our decap curves")
    print(f"  race his kill ceilings); Acererak's slow K is memory-bias-flagged (his real deck may")
    print(f"  be faster); the BLEND hides H&K, the real stomp threat (see --vs --measured Δ column).")
    print(f"  The RANKING is the robust read (rho above); absolute levels inherit the PROXY band.\n")
    return res


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--trials", type=int, default=40000,
                    help="MC trials per (deck, opponent, profile); default matches tier_list")
    ap.add_argument("--seed", type=int, default=tl.sm.SEED)
    ap.add_argument("--deltas", type=int, nargs="*", default=[-2, -1, 0, 1, 2],
                    help="whole-turn shifts of K_DIST to sweep (0 = recomputed base)")
    args = ap.parse_args()
    if 0 not in args.deltas:
        args.deltas = sorted({0, *args.deltas})               # base column is load-bearing
    run(args.trials, args.seed, args.deltas)


if __name__ == "__main__":
    main()
