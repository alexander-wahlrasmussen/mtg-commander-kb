#!/usr/bin/env python3
"""calibrate.py — grade the labs against REAL games (the Layer-C back-test).

The whole simulation tower (`*_clock_lab.py`, `pod_gauntlet.py`, `self_meta_lab.py`,
`interaction_meta_lab.py`, and the `tier_list.py` synthesis on top) predicts how the decks
perform. Every lab has falsified a *hand-estimate* — but nothing has ever checked the LABS
themselves against reality. `game_log.py` is the capture end of that loop; THIS is the grading
end. It reads `analysis/game_results.jsonl` and asks, per deck and per oracle:

  CLOCK calibration   observed table clock (mean win_turn | I won)   vs lab `table` median
                      observed decap clock (mean first_decap_turn)   vs lab `decap` median
                      -> signed error per deck + MAE in turns. The cleanest test: the clock is
                         deck-intrinsic, and the labs predict it directly.

  WIN-RATE calibration  observed per-deck win% vs each oracle's predicted P(win):
                        ANTI-POD (pod_gauntlet), SELF (self_meta), INTER (interaction_meta).
                        -> Spearman(observed_win%, predicted) per oracle: which instrument
                           actually orders the decks the way real games do?

This is the same question as the Framework Bake-Off (`framework_bakeoff.py`) — *does the number
predict the result?* — but graded against REAL outcomes instead of the sim's own outcome oracle.
It is the L2 frontier the Backlog (#5/#6) and `REF_Simulation_Fidelity.md` named and deferred.

Honest by construction: every per-deck stat carries its game count `n`; decks below `--min-games`
are shown but EXCLUDED from MAE / Spearman, and the correlations need n>=3 decks to compute at
all. With an empty log (today's state) it prints the armed-but-ungraded loop and exits 0 — it is
useful as a contract *before* the first game is logged.

Usage
    python scripts/calibrate.py                      # grade analysis/game_results.jsonl
    python scripts/calibrate.py --log path.jsonl     # grade a different log (fixtures/tests)
    python scripts/calibrate.py --min-games 5        # raise the per-deck inclusion bar
    python scripts/calibrate.py --power              # how many games/deck to log? (needs NO games)

Caveats (inherited + new)
    * Lab predictions are unblocked goldfish ceilings / soft-overlay P(win); see each source.
    * `first_decap_turn` is a POD-level event (first seat out, by anyone) — only an approximation
      of MY deck's decap clock. Treated as the game_log schema documents it; flagged, not laundered.
    * SELF/INTER predict a MIRROR pod; real games are vs opponents' decks. ANTI-POD (vs the
      recurring T6-7 combo pod) is the least-confounded win-rate predictor — read it first.
"""
import argparse
import importlib.util
import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_LOG = ROOT / "analysis" / "game_results.jsonl"

for _s in (sys.stdout, sys.stderr):
    if hasattr(_s, "reconfigure"):
        try:
            _s.reconfigure(encoding="utf-8", errors="replace")
        except (ValueError, OSError):
            pass


def _load(name):
    """Lazy module loader — kept out of module scope so importing calibrate (for the unit
    tests of the pure helpers below) does NOT pull the whole oracle chain."""
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ------------------------------------------------------------------ pure helpers
# (no oracle imports here — unit-tested directly on synthetic inputs)
def load_log(path):
    """Read a game_results.jsonl into a list of records (skip blanks; raise on bad JSON)."""
    p = Path(path)
    if not p.exists():
        return []
    out = []
    for i, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError as e:
            sys.exit(f"{p}: line {i}: invalid JSON — {e}")
    return out


def _mean(xs):
    xs = [x for x in xs if isinstance(x, (int, float))]
    return (sum(xs) / len(xs)) if xs else None


def observed_stats(records):
    """Per-deck observed metrics from MY point of view — mirrors game_log.cmd_summary so the
    two tools agree. table = mean(win_turn) over games I WON (the table clock when I closed);
    decap = mean(first_decap_turn) over ALL my games (pod-level first KO, per the schema)."""
    decks = {}
    for r in records:
        mine = r.get("mine")
        if not mine:
            continue
        d = decks.setdefault(mine, {"n": 0, "w": 0, "win_turns": [], "decap_turns": []})
        d["n"] += 1
        if r.get("winner") == mine:
            d["w"] += 1
            d["win_turns"].append(r.get("win_turn"))
        d["decap_turns"].append(r.get("first_decap_turn"))
    for d in decks.values():
        d["win_rate"] = 100.0 * d["w"] / d["n"] if d["n"] else None
        d["table_mean"] = _mean(d["win_turns"])
        d["decap_mean"] = _mean(d["decap_turns"])
    return decks


def parse_med(s):
    """Lab median string -> (turn:float, open:bool). 'T7'->(7,False); '>T14'->(14,True);
    open=True flags a right-censored median (the true value is at least this) so a signed
    error against it is a lower bound on the deck's slowness, not a point estimate."""
    if s is None:
        return None, False
    s = str(s).strip()
    opened = s.startswith((">", "<", "≥", "≤"))
    digits = "".join(ch for ch in s if ch.isdigit())
    return (float(digits) if digits else None), opened


def clock_rows(observed, clocks, min_games):
    """Per-deck (slug, n, obs_table, lab_table, dT, obs_decap, lab_decap, dD, eligible)."""
    rows = []
    for slug, o in observed.items():
        lab = clocks.get(slug, {})
        med = lab.get("med", [None, None])
        lab_decap, _od = parse_med(med[0] if med else None)
        lab_table, _ot = parse_med(med[1] if len(med) > 1 else None)
        rows.append({
            "slug": slug, "n": o["n"],
            "obs_table": o["table_mean"], "lab_table": lab_table,
            "d_table": (o["table_mean"] - lab_table)
                       if o["table_mean"] is not None and lab_table is not None else None,
            "obs_decap": o["decap_mean"], "lab_decap": lab_decap,
            "d_decap": (o["decap_mean"] - lab_decap)
                       if o["decap_mean"] is not None and lab_decap is not None else None,
            "eligible": o["n"] >= min_games,
        })
    return rows


def mae(rows, key):
    """Mean absolute error over eligible rows with a value for `key`."""
    errs = [abs(r[key]) for r in rows if r["eligible"] and r.get(key) is not None]
    return (sum(errs) / len(errs)) if errs else None


def power_curve(truth_pct, n_grid, trials, seed, spearman, detect=0.5):
    """How many games-per-deck before reality can adjudicate? A Monte-Carlo power analysis: IF
    `truth_pct` (slug -> true win%) were the real ordering and games were i.i.d. Bernoulli, draw
    N games for every deck, rank the decks by OBSERVED win%, and Spearman it against the truth —
    `trials` times per N. Returns [(N, median_rho, p10_rho, p_detect)] where p_detect =
    P(rho >= detect): the chance N games/deck recovers the ranking cleanly enough to act on.

    `spearman` is injected (framework_bakeoff.spearman) so this stays a pure, seeded, testable
    function. Assumes the oracle IS the truth and games are independent — an OPTIMISTIC floor:
    real pilot variance / meta drift / non-independence only push the required N up."""
    slugs = sorted(truth_pct)
    truth = [truth_pct[s] for s in slugs]
    ps = [truth_pct[s] / 100.0 for s in slugs]
    rng = random.Random(seed)
    out = []
    for N in n_grid:
        rhos = []
        for _ in range(trials):
            obs = [100.0 * sum(rng.random() < pi for _ in range(N)) / N for pi in ps]
            r, _n = spearman(obs, truth)
            rhos.append(r if r is not None else 0.0)
        rhos.sort()
        med = rhos[len(rhos) // 2]
        p10 = rhos[max(0, len(rhos) // 10 - 1)]
        pdet = sum(r >= detect for r in rhos) / len(rhos)
        out.append((N, med, p10, pdet))
    return out


# --------------------------------------------------------------------- rendering
def _fmt(v, suffix="", nd=1):
    return f"{v:.{nd}f}{suffix}" if isinstance(v, (int, float)) else "—"


def render_empty():
    print("\n" + "=" * 78)
    print("LAYER C — CALIBRATION: the labs vs reality")
    print("=" * 78)
    print(f"\n  {DEFAULT_LOG.relative_to(ROOT)} holds 0 games — the loop is ARMED but ungraded.")
    print("  Log a game after a pod with:  python scripts/game_log.py log")
    print("\n  Once games land, this tool grades, per deck and per oracle:")
    print("    • CLOCK   — observed table/decap clock  vs  the lab medians  (MAE in turns)")
    print("    • WIN-RATE — observed win%  vs  ANTI-POD / SELF / INTER P(win)  (Spearman ρ)")
    print("\n  That is the only thing that can tell us whether the tower predicts anything —")
    print("  every number it emits today predicts a *simulated* outcome.\n")


def cmd_power(args):
    """How many games/deck before the REAL oracle can adjudicate? Uses the committed ANTI-POD
    snapshot (framework_bakeoff.RICHER_ORACLE) as the assumed truth — no games and no live sim
    needed, so it yields an actionable logging target TODAY."""
    fb = _load("framework_bakeoff")
    truth = {s: g for s, (g, _sm) in fb.RICHER_ORACLE.items() if g is not None}
    grid = [3, 5, 8, 12, 20, 30, 50]
    rows = power_curve(truth, grid, max(args.trials // 20, 1000), args.seed, fb.spearman, args.detect)

    print("\n" + "=" * 78)
    print("LAYER C — POWER: how many games per deck before reality can adjudicate?")
    print("=" * 78)
    print(f"  Assumed truth = the ANTI-POD oracle ({len(truth)} decks); games i.i.d. Bernoulli;")
    print(f"  trials={max(args.trials // 20, 1000)}, seed={args.seed}. 'detect' = P(Spearman >= {args.detect}).")
    print(f"\n  {'games/deck':>11}{'median ρ':>11}{'p10 ρ':>9}{'P(ρ>=' + str(args.detect) + ')':>11}")
    for N, med, p10, pdet in rows:
        print(f"  {N:>11}{med:>11.2f}{p10:>9.2f}{pdet:>10.0%}")
    # the smallest N that recovers the ranking >=80% of the time
    target = next((N for N, _m, _p, pd in rows if pd >= 0.80), None)
    print()
    if target:
        total = target * len(truth)
        print(f"  → Log ~{target} games/deck (~{total} games across {len(truth)} decks) to recover the")
        print(f"    predicted ranking ≥80% of the time. Below that, the REAL column is noise — the")
        print(f"    3-deck synthetic fixture hitting ρ=±1 is exactly that small-sample artifact.")
    else:
        print(f"  → Even {grid[-1]} games/deck doesn't clear 80% detection at this threshold — the")
        print(f"    roster's true win-rates are too bunched to rank-separate cheaply (lower --detect).")
    print("  OPTIMISTIC floor: pilot variance / meta drift / non-independence push the target UP.\n")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--log", default=str(DEFAULT_LOG), help="game_results.jsonl to grade")
    ap.add_argument("--min-games", type=int, default=3,
                    help="per-deck game floor for MAE / Spearman inclusion (default 3)")
    ap.add_argument("--trials", type=int, default=40000)
    ap.add_argument("--seed", type=int, default=20260614)
    ap.add_argument("--tax", type=float, default=0.6, help="interaction-overlay tax")
    ap.add_argument("--power", action="store_true",
                    help="games-per-deck power analysis (needs NO games — answers 'how much to log?')")
    ap.add_argument("--detect", type=float, default=0.5,
                    help="--power: the Spearman threshold counted as 'signal recovered' (default 0.5)")
    args = ap.parse_args()

    if args.power:
        cmd_power(args)
        return

    records = load_log(args.log)
    if not records:
        render_empty()
        return

    observed = observed_stats(records)

    # Predictions: reuse the tier_list axes (DRY — the same oracles the tier list ranks on).
    tl = _load("tier_list")
    fb = _load("framework_bakeoff")
    pg, sm = tl.pg, tl.sm
    C = pg.merged_clocks()
    slugs = [s for s in sm.dl.ROSTER if s in C]
    rng = random.Random(args.seed)
    preds = {
        "antipod": tl.antipod_blend(slugs, C, args.trials, rng),
        "self": tl.self_meta(slugs, C, args.trials, rng, sm.T_GRIND),
        "inter": tl.interaction(slugs, C, args.trials, rng, sm.T_GRIND, args.tax),
    }

    ngames = len(records)
    elig = [s for s in observed if observed[s]["n"] >= args.min_games]
    print("\n" + "=" * 86)
    print("LAYER C — CALIBRATION: the labs vs reality")
    print("=" * 86)
    print(f"  {ngames} games logged across {len(observed)} of my decks  ·  "
          f"{len(elig)} deck(s) with n>={args.min_games}  ·  trials={args.trials}\n")

    # --- CLOCK calibration --------------------------------------------------
    rows = clock_rows(observed, C, args.min_games)
    rows.sort(key=lambda r: (-r["n"], r["slug"]))
    print("  CLOCK CALIBRATION   (observed mean turn  vs  lab median; Δ = obs − lab)")
    print(f"  {'deck':22}{'n':>3}{'obsTbl':>8}{'labTbl':>8}{'Δ':>6}"
          f"{'obsDec':>8}{'labDec':>8}{'Δ':>6}")
    for r in rows:
        flag = "" if r["eligible"] else " ·"
        nm = C.get(r["slug"], {}).get("name", r["slug"])
        print(f"  {nm[:22]:22}{r['n']:>3}"
              f"{_fmt(r['obs_table'],'T'):>8}{_fmt(r['lab_table'],'T'):>8}{_fmt(r['d_table']):>6}"
              f"{_fmt(r['obs_decap'],'T'):>8}{_fmt(r['lab_decap'],'T'):>8}{_fmt(r['d_decap']):>6}{flag}")
    mt, md = mae(rows, "d_table"), mae(rows, "d_decap")
    print(f"\n  MAE (n>={args.min_games} decks):  table = {_fmt(mt,' turns')}  ·  "
          f"decap = {_fmt(md,' turns')}   (· = below the game floor, excluded)\n")

    # --- WIN-RATE calibration ----------------------------------------------
    print("  WIN-RATE CALIBRATION   (observed win%  vs  each oracle's predicted P(win))")
    print(f"  {'deck':22}{'n':>3}{'obsWin':>8}{'antipod':>9}{'self':>7}{'inter':>7}")
    obs_win, p_anti, p_self, p_inter = [], [], [], []
    for r in rows:
        s = r["slug"]
        ow = observed[s]["win_rate"]
        a, sf, it = preds["antipod"].get(s), preds["self"].get(s), preds["inter"].get(s)
        flag = "" if r["eligible"] else " ·"
        nm = C.get(s, {}).get("name", s)
        print(f"  {nm[:22]:22}{r['n']:>3}{_fmt(ow,'%',0):>8}"
              f"{_fmt(a,'%',0):>9}{_fmt(sf,'%',0):>7}{_fmt(it,'%',0):>7}{flag}")
        if r["eligible"]:
            obs_win.append(ow); p_anti.append(a); p_self.append(sf); p_inter.append(it)
    ra, na = fb.spearman(obs_win, p_anti)
    rs, _ = fb.spearman(obs_win, p_self)
    ri, _ = fb.spearman(obs_win, p_inter)
    print(f"\n  Spearman(observed win%, oracle)  over {na} eligible deck(s):")
    print(f"    ANTI-POD = {ra if ra is not None else 'n/a (need n>=3 decks)'}  ·  "
          f"SELF = {rs if rs is not None else 'n/a'}  ·  "
          f"INTER = {ri if ri is not None else 'n/a'}")
    print("    +1 = the oracle orders decks exactly as real games do; ~0 = no signal; <0 = inverted.")
    print("\n  Read clocks before win-rates (less confounded). ANTI-POD is the least-confounded")
    print("  win predictor (vs the real T6-7 pod); SELF/INTER predict a mirror, shown for contrast.\n")


if __name__ == "__main__":
    main()
