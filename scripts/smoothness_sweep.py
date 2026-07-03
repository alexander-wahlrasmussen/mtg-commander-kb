#!/usr/bin/env python3
"""smoothness_sweep.py — joint test of the two "smoothness" hypotheses.

The user framed two hypotheses about keeping a deck able to *do something* every
turn (never mana-starved, never topdecking an empty hand):

  H1 (mulligan primacy): the opening hand is most crucial, so a sharper, more
     deck-specific mulligan is the main lever.
  H2 (momentum): the deck needs enough draw/selection/ramp to keep the hand stocked.

This sweep measures both against the SAME instrument — deck_sim.simulate_flow
(paced 'one' spend, the draw-aware smoothness pass) — under a 2x2 per deck:

    keep  in { land   = land-count default mulligan,
               plan   = the deck's plan-aware keep-spec }        <- H1 lever
    draw  in { on      = real card draw executed (draw_map),
               off     = draw spells draw nothing }              <- H2 lever

Primary metric: mean dead turns over T1-10 (lower = smoother). It then contrasts
the two levers roster-wide:

    dMull = dead(land) - dead(plan)   at a fixed draw level  (H1 effect)
    dDraw = dead(off)  - dead(on)     at a fixed keep level  (H2 effect)

and the INTERACTION the user's framing implies — is the mulligan a bigger lever
when the gas is off? (dMull measured at draw=off vs draw=on).

Paired design: one fixed shuffle stream per deck (deck_rng seeded by deck only) is
reused across all four cells, so the deltas are low-variance A/Bs, not noise.

NOT a rules engine, goldfish, lands-only mana floor — inherits every
simulate_flow caveat (see deck_sim.py). Read the deltas as a relative comparison
of the two levers, not absolute turn counts.

Usage:
    python scripts/smoothness_sweep.py                 # whole roster
    python scripts/smoothness_sweep.py --deck radiation
    python scripts/smoothness_sweep.py --trials 12000
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import deck_sim as ds


def sweep_deck(library, deck_key, trials, seed):
    """Return {(keep, draw): {'dead': mean_dead, 'hlb8': hellbent@T8}} for the 2x2."""
    dm = ds.draw_map(library)
    spec = ds._load_keep_specs().get(deck_key) if deck_key else None
    plan_set = ds.plan_card_set(deck_key)
    out = {}
    for keep in ("land", "plan"):
        ds.set_keep_spec(spec if keep == "plan" else None)
        for draw in ("on", "off"):
            rng = ds.deck_rng(seed, deck_key or "x")   # same stream every cell = paired
            flow = ds.simulate_flow(library, 10, trials, rng, plan_set=plan_set,
                                    spend="one", draw_profiles=(dm if draw == "on" else {}))
            out[(keep, draw)] = {"dead": flow["mean_dead_turns"],
                                 "hlb8": flow["hellbent_by_turn"][8]}
    ds.set_keep_spec(None)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--deck", help="Fuzzy filename filter")
    ap.add_argument("--trials", type=int, default=8000)
    ap.add_argument("--seed", type=int, default=12345)
    args = ap.parse_args()

    index = ds.load_oracle_index()
    aliases = ds.load_reskin_aliases()
    txts = sorted(ds.DECKS_DIR.glob("*.txt"))
    if args.deck:
        txts = [p for p in txts if args.deck.lower() in p.stem.lower()]
        if not txts:
            sys.exit(f"No decklist matches '{args.deck}'")

    print(f"=== Smoothness sweep — mulligan x momentum ({args.trials} trials/cell, paced) ===")
    print("mean dead turns T1-10 (lower=smoother). dMull=land-plan (H1), dDraw=off-on (H2).\n")
    hdr = (f"{'deck':26}{'L/on':>6}{'P/on':>6}{'L/off':>7}{'P/off':>7}"
           f"{'dMull':>7}{'dDraw':>7}{'dMull|gasoff':>13}")
    print(hdr)
    print("-" * len(hdr))

    agg = {"dMull_on": [], "dDraw_plan": [], "dMull_off": []}
    for path in txts:
        library, _, diag = ds.parse_deck(path, index, aliases)
        deck_key = diag["deck_key"]
        name = ds.DISPLAY.get(deck_key, path.stem)
        r = sweep_deck(library, deck_key, args.trials, args.seed)
        d = {k: v["dead"] for k, v in r.items()}
        dMull_on = d[("land", "on")] - d[("plan", "on")]      # H1 with real gas
        dMull_off = d[("land", "off")] - d[("plan", "off")]   # H1 with gas off
        dDraw_plan = d[("plan", "off")] - d[("plan", "on")]   # H2 at the sharp mulligan
        agg["dMull_on"].append(dMull_on)
        agg["dDraw_plan"].append(dDraw_plan)
        agg["dMull_off"].append(dMull_off)
        print(f"{name[:25]:26}{d[('land','on')]:6.2f}{d[('plan','on')]:6.2f}"
              f"{d[('land','off')]:7.2f}{d[('plan','off')]:7.2f}"
              f"{dMull_on:+7.2f}{dDraw_plan:+7.2f}{dMull_off:+13.2f}")

    n = len(agg["dMull_on"]) or 1
    avg = lambda k: sum(agg[k]) / n
    print("-" * len(hdr))
    print(f"\nRoster averages ({n} decks):")
    print(f"  H1  sharpen mulligan (land->plan), gas ON : {avg('dMull_on'):+.3f} dead turns removed")
    print(f"  H2  add the draw suite (off->on), plan keep: {avg('dDraw_plan'):+.3f} dead turns removed")
    print(f"  H1  sharpen mulligan, gas OFF              : {avg('dMull_off'):+.3f} dead turns removed")
    inter = avg("dMull_off") - avg("dMull_on")
    print(f"\n  Interaction (H1 lever gas-off minus gas-on): {inter:+.3f}")
    print("  positive => the mulligan matters MORE when the deck lacks gas (the")
    print("  user's joint intuition); |dDraw| vs |dMull| says which lever dominates.")


if __name__ == "__main__":
    main()
