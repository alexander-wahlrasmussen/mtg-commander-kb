#!/usr/bin/env python3
"""interaction_meta_lab.py — the interaction/durability OVERLAY oracle (Backlog #6).

The Framework Bake-Off (analysis/Framework_Bakeoff_2026-06-16.md) hit an honest wall: NO
deck-quality framework predicts winning, because every outcome oracle is a SOLITAIRE
GOLDFISH. Interaction and Durability — two of the Conversion Check's four axes, and
Disciple's whole `I` term — score 0 with no opponents, so a framework that rewards them
cannot correlate with results. self_meta_lab already lets DURABILITY decide, but only in the
GRIND tail (nobody closes by T_grind); in a normal race the raw clock wins and interaction is
invisible. This lab puts interaction INTO the normal race.

THE OVERLAY (NOT a rules engine — same discipline as self_meta_lab / pod_gauntlet's lock and
swap overlays: measured substrate, swept magnitude, reduces to the base model at zero knob):
self_meta's 4-seat random roster pod, but a closing seat must push its win THROUGH the rest of
the table's available answers.

  For each seat s in the pod, sample its RAW table-close turn t_raw[s] (the goldfish clock,
  pg.sample_kill on the table CDF — identical draw to self_meta). Then compute its EFFECTIVE
  close: starting at t_raw, each turn the other three seats contest the close —
      P(stopped at t) = clamp( TAX · pressure(others,t) · (1 - PROTECT[s]) )
      pressure(others,t) = 1 - PROD_o (1 - interact[o]·decay)   (>=1 other holds a live answer)
  If stopped, the close slips a turn and the table's answer pool DECAYS (ANSWER_DECAY; finite
  interaction); else the effective close is t. The pod winner is the EARLIEST EFFECTIVE close;
  if none by T_grind, the most DURABLE seat outlasts (self_meta's fallback, unchanged).

WHAT IT REWARDS (exactly the axes the goldfish can't see):
  * protect-own / counter-immune kills (high PROTECT) shrug off the tax and keep their clock;
  * interaction-dense decks (high interact) tax opponents' closes (helping themselves win
    races they'd otherwise lose to a faster but answerable deck);
  * glass cannons (fast clock, low PROTECT, low interact) get delayed in an interactive pod
    and lose races they used to win;
  * durable fortresses still take the grind tail.

NULL REDUCTION (the correctness gate): TAX=0 => P(stopped)=0 => effective close = raw close =>
output is IDENTICAL to self_meta_lab within Monte-Carlo noise. Verify:
  python scripts/interaction_meta_lab.py --tax 0   vs   python scripts/self_meta_lab.py

DATA — all already MEASURED + oracle-verified, imported not re-derived:
  * interact[s] = each deck's measured P(disrupt a combo on T6/T7) with reactive answers live
    (pg.MEASURED[slug][6|7][0], the a=0 column from delay_lab --emit-json). turnscale: T6 value
    for t<=6, T7 for t>=7 (pod_gauntlet's row-pick rule), flat beyond. CAVEAT: this OVER-credits
    interaction at very early closes (T4-5 have less mana than the T6 measurement assumes) and
    flat-extends the late game — bounded effects, swept.
  * PROTECT[s] = protect-own (counter-war + counter-immune kill), pg.PROTECT.
  * table CDFs / clocks / durability / T_grind / defense — pg + self_meta_lab.
  * NEW judgment params (printed + swept): TAX, ANSWER_DECAY (reuse pg's 0.5). Trust the
    CLOSE->WIN->INTERACTIVE decomposition and the TAX-sweep DIRECTION, not the second decimal.

LIMITATIONS: still not a 4-body rules engine — no targeting, no stack, no politics, no combat,
no shared-answer accounting (each seat faces a "fresh" table). A heuristic race overlay whose
job is to let interaction/durability MOVE the oracle, so the bake-off can ask whether a quality
framework correlates once they're no longer worth zero.

Writeup: analysis/Interaction_Oracle_2026-06-16.md
"""
import argparse
import importlib.util
import random
from pathlib import Path

ROOT = Path(__file__).parent.parent


def _load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


pg = _load("pod_gauntlet")        # clocks, build_cdf, sample_kill, HORIZON, PROTECT, MEASURED, ANSWER_DECAY
sm = _load("self_meta_lab")       # durability, defense_counts, T_GRIND, JUDGMENT, weights

SEED = sm.SEED                    # share self_meta's seed so the no-tax column tracks it
TAX = 0.6                         # interaction-tax strength (swept; 0 == self_meta)
TAX_SWEEP = [0.0, 0.3, 0.6, 0.9]
NSEAT = 4


def interact_at(slug, t):
    """Measured P(this deck holds a live answer) on turn t, a=0 (reactive answers live).
    T6 value for t<=6, T7 for t>=7 (pod_gauntlet's row-pick rule), flat beyond."""
    row = pg.MEASURED[slug]
    return (row[6][0] if t <= 6 else row[7][0]) / 100.0


def effective_close(slug, t_raw, others, prot, tax, rng):
    """Raw table-close turn pushed out by the table's interaction. tax<=0 => t_raw (the
    null-reduction path: consumes NO rng, so --tax 0 stays bit-identical to self_meta)."""
    if tax <= 0.0:
        return t_raw
    p = prot.get(slug, 0.0)
    decay = 1.0
    t = t_raw
    while t <= pg.HORIZON:
        leak = 1.0
        for o in others:
            leak *= (1.0 - interact_at(o, t) * decay)    # P(this opponent has NO live answer)
        pres = 1.0 - leak                                 # P(>=1 opponent can contest the close)
        pstop = tax * pres * (1.0 - p)
        if pstop > 1.0:
            pstop = 1.0
        if rng.random() < pstop:
            t += 1
            decay *= pg.ANSWER_DECAY
        else:
            return t
    return pg.HORIZON + 1


def _winners(closes, pod, dura, t_grind):
    """self_meta's decision rule on a {seat: close-turn} map: earliest closer by T_grind,
    else most durable. Returns the champion list (ties shared)."""
    tmin = min(closes.values())
    if tmin <= t_grind:
        return [s for s in pod if closes[s] == tmin]
    dmax = max(dura[s] for s in pod)
    return [s for s in pod if abs(dura[s] - dmax) < 1e-9]


def simulate(slugs, C, tcdf, dura, trials, tax, t_grind, rng):
    """Core overlay sim, factored out of run() so tier_list.py can reuse it (DRY). Returns
    (notax, inter, appear): per-deck self_meta-reproduction wins (TAX=0 branch), interaction-tax
    wins, and pod appearances. The rng-consumption order is byte-identical to the historical
    run() loop, so the printed table AND the null-reduction tests (which drive run() by
    subprocess) are unchanged."""
    notax = {s: 0.0 for s in slugs}        # self_meta reproduction (TAX=0 branch, same pods)
    inter = {s: 0.0 for s in slugs}        # with the interaction tax
    appear = {s: 0 for s in slugs}
    for _ in range(trials):
        pod = rng.sample(slugs, NSEAT)
        for s in pod:
            appear[s] += 1
        t_raw = {s: pg.sample_kill(tcdf[s], rng) for s in pod}        # identical draw to self_meta
        champs0 = _winners(t_raw, pod, dura, t_grind)
        for s in champs0:
            notax[s] += 1.0 / len(champs0)
        eff = {s: effective_close(s, t_raw[s], [o for o in pod if o != s],
                                  pg.PROTECT, tax, rng) for s in pod}
        champs = _winners(eff, pod, dura, t_grind)
        for s in champs:
            inter[s] += 1.0 / len(champs)
    return notax, inter, appear


def run(args):
    rng = random.Random(args.seed)
    C = pg.merged_clocks()
    slugs = [s for s in sm.dl.ROSTER if s in C and s in pg.MEASURED]  # self_meta's pod order (parity)
    tcdf = {s: pg.build_cdf(C[s]["grid"], C[s]["table"]) for s in slugs}
    defense = sm.defense_counts()
    dura = {s: sm.durability(s, C, defense) for s in slugs}
    interact = {s: interact_at(s, 7) for s in slugs}                  # headline value (T7)

    notax, inter, appear = simulate(slugs, C, tcdf, dura, args.trials, args.tax,
                                    args.t_grind, rng)

    rows = []
    for s in slugs:
        a = appear[s] or 1
        rows.append((s, C[s]["name"], 100.0 * notax[s] / a, 100.0 * inter[s] / a,
                     interact[s], pg.PROTECT.get(s, 0.0), dura[s],
                     C[s]["med"][1], C[s]["never"][1]))
    rows.sort(key=lambda r: -r[3])

    print(f"\n{'='*104}\nINTERACTION-META — P(win | random 4-seat roster pod) WITH the interaction overlay")
    print(f"  [TAX={args.tax} · T_grind={args.t_grind} · trials={args.trials} · seed={args.seed}]\n")
    print("  WIN(sm) = self_meta reproduction (TAX=0, same pods). INTER = + interaction tax on")
    print("  the close. int/prot drive the tax: a closing seat is stopped with")
    print("  P = TAX·(table holds an answer)·(1-protect), slips a turn, table's answers decay.\n")
    print(f"  {'#':>2} {'deck':24}{'table':>6}{'int':>6}{'prot':>6}{'dura':>6}"
          f"{'WIN(sm)':>9}{'INTER':>7}{'Δ':>6}  {'judg':>5} Δrank")
    for i, (s, name, w0, w1, it, pr, d, med, nev) in enumerate(rows, 1):
        j = sm.JUDGMENT.get(s, 0)
        drank = f"{j - i:+d}" if j else "  —"
        print(f"  {i:>2} {name:24}{med:>6}{it*100:>5.0f}%{pr*100:>5.0f}%{d:>6.2f}"
              f"{w0:>8.0f}%{w1:>6.0f}%{w1 - w0:>+6.0f}  {('#'+str(j)) if j else '—':>5} {drank}")
    print(f"\n  int = measured P(hold a live answer T7, a=0; pg.MEASURED). prot = protect-own (pg.PROTECT).")
    print("  Δ = INTER - WIN(sm): + = interaction LIFTS this deck (resists tax / taxes others);")
    print("  - = a fast-but-answerable deck loses races it goldfished. TAX=0 => Δ=0 (null reduction).")
    return {s: round(w1, 1) for s, _n, _w0, w1, *_ in rows}


def sweep(args):
    """INTERACTIVE P(win) per deck across the TAX grid — so no single magnitude drives a claim."""
    print(f"\nTAX SWEEP — INTERACTIVE P(win) per deck   [trials={args.trials}, seed={args.seed}]\n")
    cols = {}
    for tx in TAX_SWEEP:
        a = argparse.Namespace(**vars(args))
        a.tax = tx
        import io
        import contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            cols[tx] = run(a)
    C = pg.merged_clocks()
    slugs = sorted(cols[TAX_SWEEP[0]], key=lambda s: -cols[TAX_SWEEP[-1]][s])
    print(f"  {'deck':24}" + "".join(f"{('TAX'+str(t)):>8}" for t in TAX_SWEEP) + f"{'Δ(hi-0)':>9}")
    for s in slugs:
        d = cols[TAX_SWEEP[-1]][s] - cols[TAX_SWEEP[0]][s]
        print(f"  {C[s]['name']:24}" + "".join(f"{cols[t][s]:>7.0f}%" for t in TAX_SWEEP)
              + f"{d:>+8.0f}")
    print("\n  TAX0 column is the self_meta null. Read the SIGN of Δ(hi-0): which decks interaction")
    print("  lifts (protect-own / interaction-dense) vs sinks (fast-but-answerable glass cannons).")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--trials", type=int, default=40000)
    ap.add_argument("--seed", type=int, default=SEED)
    ap.add_argument("--tax", type=float, default=TAX, help="interaction-tax strength (0 == self_meta)")
    ap.add_argument("--t-grind", type=int, default=sm.T_GRIND)
    ap.add_argument("--sweep", action="store_true", help="INTERACTIVE P(win) across the TAX grid")
    args = ap.parse_args()
    if args.sweep:
        sweep(args)
    else:
        run(args)


if __name__ == "__main__":
    main()
