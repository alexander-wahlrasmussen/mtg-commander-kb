#!/usr/bin/env python3
"""mulligan_audit.py — how much operating room does the plan-aware mulligan have?

The smoothness sweep (analysis/Smoothness_Sweep_2026-07-03.md) concluded the
mulligan lever is ~15x weaker than the draw suite. That comparison is only
informative if the two keeps being contrasted — land-count vs plan-aware —
actually DISAGREE on a meaningful fraction of hands: the mulligan lever can only
act on hands where the verdicts differ. This audit measures that room, per deck,
plus WHICH clause of the plan predicate does the work (a predicate that admits
~every hand via a trivially-true clause is a land-count keep in disguise).

Per deck, over N sampled first-7s (no mulligan):
  land% / plan%    pass rate of each keep on a raw 7
  ship>keep%       land keeps but plan ships — the plan mulligan's entire room
  keep>ship%       plan keeps but land ships (5-land hands a tighter band drops, etc.)
  why-kept         share of plan-kept hands admitted by each clause (union axes
                   overlap, so shares can sum >100%):
                     FINDING: key piece / tutor / >=2 selection
                     MANA:    ramp piece / hi-curve 4+ lands
                     BOARD:   split into "trivial" (min_lands already >= cmdr_cmc-2,
                              so commander-reach is guaranteed by the land band and
                              the axis degenerates to "has a cmc<=3 nonland") vs
                              "real" (lands/ramp actually checked)
  mull depth       under the plan keep in opening_hand: 0/1/2 mulls used, and
                   %final-UNKEEPABLE — the sim mulls at most twice, FREE (fresh 7,
                   no London bottoming), then keeps whatever it holds.

Diagnostic only — prints a table, writes nothing. The keep logic is deliberately
recomputed clause-by-clause here (mirroring deck_sim._axis_ok) and cross-checked
against deck_sim.keep_hand on every sampled hand, so a drift between the two
fails loudly.

Usage:
  python scripts/mulligan_audit.py                # roster table
  python scripts/mulligan_audit.py --deck croak   # one deck, verbose clauses
  python scripts/mulligan_audit.py --trials 20000
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import deck_sim as ds


def hand_features(hand, spec):
    """Clause-level features of one 7-card hand against a spec."""
    names = {nm.lower() for nm, _ in hand}
    lands = sum(1 for _, rec in hand if ds.is_land(rec))
    sets = spec["_sets"]
    return {
        "lands": lands,
        "key": len(names & sets["key_cards"]) >= spec.get("n_key_needed", 1),
        "tutor": bool(names & sets["tutors"]),
        "sel2": len(names & sets["selection"]) >= spec["n_selection_needed"],
        "ramp": bool(names & sets["ramp"]),
        "early": any((not ds.is_land(rec)) and rec["cmc"] <= ds.EARLY_PLAY_MAX_CMC
                     for _, rec in hand),
    }


def axis_pass(axis, f, spec):
    if axis == "FINDING":
        return f["key"] or f["tutor"] or f["sel2"]
    if axis == "MANA":
        return f["ramp"] or (spec["hi_curve"] and f["lands"] >= 4)
    # BOARD
    reach = f["lands"] >= spec["cmdr_cmc"] - 2 or f["ramp"]
    return reach and f["early"]


def audit_deck(library, spec, trials, rng):
    """Sample raw first-7s; classify under land keep vs plan keep, clause shares,
    then emulate opening_hand mull depth under the plan keep."""
    axes = [spec["bottleneck"], *spec.get("also", [])]
    board_trivial = spec["min_lands"] >= spec["cmdr_cmc"] - 2   # reach guaranteed in-band

    n = {"land": 0, "plan": 0, "ship_keep": 0, "keep_ship": 0}
    why = {}                                    # clause label -> count among plan-kept
    deck = library[:]
    ds.set_keep_spec(spec)
    for _ in range(trials):
        rng.shuffle(deck)
        hand = deck[:7]
        f = hand_features(hand, ds._KEEP_SPEC)   # installed copy has _sets
        land_ok = 2 <= f["lands"] <= 5
        band_ok = spec["min_lands"] <= f["lands"] <= spec["max_lands"]
        plan_ok = band_ok and any(axis_pass(ax, f, spec) for ax in axes)
        if plan_ok != ds.keep_hand(hand):
            raise AssertionError("clause recomputation drifted from deck_sim.keep_hand")
        n["land"] += land_ok
        n["plan"] += plan_ok
        n["ship_keep"] += land_ok and not plan_ok
        n["keep_ship"] += plan_ok and not land_ok
        if plan_ok:
            for ax in axes:
                if not axis_pass(ax, f, spec):
                    continue
                if ax == "FINDING":
                    for lbl, hit in (("key", f["key"]), ("tutor", f["tutor"]),
                                     ("2xsel", f["sel2"])):
                        if hit:
                            why[lbl] = why.get(lbl, 0) + 1
                elif ax == "MANA":
                    lbl = "ramp" if f["ramp"] else "hiC-4land"
                    why[lbl] = why.get(lbl, 0) + 1
                else:
                    lbl = "board(trivial)" if board_trivial else "board"
                    why[lbl] = why.get(lbl, 0) + 1

    # Mull-depth emulation (fresh rng draws from the same stream; free mulls, cap 2).
    mulls = [0, 0, 0]
    unkeepable = 0
    for _ in range(trials):
        m = 0
        rng.shuffle(deck)
        while not ds.keep_hand(deck[:7]) and m < 2:
            rng.shuffle(deck)
            m += 1
        mulls[m] += 1
        unkeepable += not ds.keep_hand(deck[:7])
    ds.set_keep_spec(None)

    pct = lambda c: 100.0 * c / trials
    return {
        "land": pct(n["land"]), "plan": pct(n["plan"]),
        "ship_keep": pct(n["ship_keep"]), "keep_ship": pct(n["keep_ship"]),
        "why": {k: 100.0 * v / max(1, n["plan"]) for k, v in sorted(why.items())},
        "mull1": pct(mulls[1]), "mull2": pct(mulls[2]), "unkeepable": pct(unkeepable),
        "board_trivial": board_trivial, "axes": axes,
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0],
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--deck", help="fuzzy filename filter")
    ap.add_argument("--trials", type=int, default=10000)
    ap.add_argument("--seed", type=int, default=12345)
    args = ap.parse_args()

    index = ds.load_oracle_index()
    aliases = ds.load_reskin_aliases()
    specs = ds._load_keep_specs()
    txts = sorted(ds.DECKS_DIR.glob("*.txt"))
    if args.deck:
        txts = [p for p in txts if args.deck.lower() in p.stem.lower()]
        if not txts:
            sys.exit(f"No decklist matches '{args.deck}'")

    print(f"=== Mulligan operating-room audit ({args.trials} first-7s/deck) ===")
    print("ship>keep = land-keep keeps it, plan-keep mulls: the plan lever's total room.\n")
    hdr = (f"{'deck':22}{'axes':16}{'land%':>7}{'plan%':>7}{'ship>':>7}{'keep>':>7}"
           f"{'mull1':>7}{'mull2':>7}{'stuck':>7}  why-kept")
    print(hdr)
    print("-" * (len(hdr) + 24))
    for path in txts:
        library, _, diag = ds.parse_deck(path, index, aliases)
        spec = specs.get(diag["deck_key"])
        if not spec:
            continue
        rng = ds.deck_rng(args.seed, diag["deck_key"])
        r = audit_deck(library, dict(spec), args.trials, rng)
        why = " ".join(f"{k}:{v:.0f}" for k, v in r["why"].items())
        print(f"{spec['name'][:21]:22}{'+'.join(r['axes']):16}"
              f"{r['land']:7.1f}{r['plan']:7.1f}{r['ship_keep']:7.1f}{r['keep_ship']:7.1f}"
              f"{r['mull1']:7.1f}{r['mull2']:7.1f}{r['unkeepable']:7.1f}  {why}")
    print("\nstuck = final hand still fails the keep after both free mulls (sim keeps it).")
    print("board(trivial) = commander-reach is guaranteed by the land band; the BOARD")
    print("axis is then just 'has a cmc<=3 nonland' — a generic smart-keep, not a plan.")


if __name__ == "__main__":
    main()
