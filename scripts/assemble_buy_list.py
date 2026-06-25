#!/usr/bin/env python
"""Buy-list analysis for assembling a chosen set of decks simultaneously.

Given a set of TARGET decklists you want physically built at the same time, a
set of decks you are DISMANTLING (their cards return to the pool), and the rest
of the active roster (which stays built and keeps its physical cards), this
computes how many copies of each card you must BUY.

A physical card lives in exactly one deck. So a card the targets need is only
"free" if you own more copies than are already committed to decks that stay
built. Dismantling a deck frees whatever it was holding.

Reuses the DeckSafe builder's parsing so DFC / split / UB-reskin alias
resolution matches the spreadsheet exactly.
"""
import sys, os
sys.path.insert(0, r"C:\Users\Alex\Projects\MTGDecks")
from collections import defaultdict
from deck_safe_collection_builder import (
    parse_collection, parse_deck, resolve_owned, canonical_name, clean_deck_name,
)

CSV = r"collection/moxfield_haves_2026-06-07-1031Z.csv"
DECKS_DIR = r"decks"

TARGETS = [
    "decks/zero-sum-game-20260619.txt",
    "decks/lightning-war-20260621.txt",
    "decks/considering/forced-liquidation-20260625.txt",
]
DISMANTLE = [
    "decks/diminishing-returns-20260505.txt",
]


def deck_demand(path):
    """canonical card -> count for a single deck (main + commander)."""
    actual, _sb, _cmd = parse_deck(path)
    d = defaultdict(int)
    for card, n in actual.items():
        d[canonical_name(card)] += n
    return d


def main():
    _raw, collection = parse_collection(CSV)

    target_paths = [os.path.normpath(p) for p in TARGETS]
    dismantle_paths = [os.path.normpath(p) for p in DISMANTLE]

    # Active roster (flat decks/*.txt)
    active = [os.path.normpath(os.path.join(DECKS_DIR, f))
              for f in os.listdir(DECKS_DIR) if f.endswith(".txt")]

    # Decks that STAY built = active, minus dismantled, minus targets.
    kept_others = [p for p in active
                   if p not in dismantle_paths and p not in target_paths]

    # Demand pools
    target_demand = defaultdict(int)
    target_sources = defaultdict(list)
    for p in target_paths:
        dd = deck_demand(p)
        name = clean_deck_name(os.path.basename(p))
        for card, n in dd.items():
            target_demand[card] += n
            target_sources[card].append((name, n))

    kept_demand = defaultdict(int)
    kept_sources = defaultdict(list)
    for p in kept_others:
        dd = deck_demand(p)
        name = clean_deck_name(os.path.basename(p))
        for card, n in dd.items():
            kept_demand[card] += n
            kept_sources[card].append((name, n))

    dismantle_holds = defaultdict(int)
    for p in dismantle_paths:
        for card, n in deck_demand(p).items():
            dismantle_holds[card] += n

    true_buys = []        # owned 0 anywhere
    contention_buys = []  # owned, but committed to kept decks
    for card in sorted(target_demand):
        need = target_demand[card]
        owned = resolve_owned(card, collection)
        committed = kept_demand.get(card, 0)
        available = owned - committed
        short = need - available
        if short <= 0:
            continue
        rec = {
            "card": card, "need": need, "owned": owned,
            "committed": committed, "short": short,
            "targets": target_sources[card],
            "kept": kept_sources.get(card, []),
            "freed_from_dismantle": dismantle_holds.get(card, 0),
        }
        if owned == 0:
            true_buys.append(rec)
        else:
            contention_buys.append(rec)

    def fmt_sources(srcs):
        return ", ".join(f"{n}x {nm}" for nm, n in srcs)

    print("=" * 70)
    print("TARGET DECKS:")
    for p in target_paths:
        print(f"  - {clean_deck_name(os.path.basename(p))}")
    print("DISMANTLING (cards freed):")
    for p in dismantle_paths:
        print(f"  - {clean_deck_name(os.path.basename(p))}")
    print(f"DECKS THAT STAY BUILT (hold their cards): {len(kept_others)}")
    print("=" * 70)

    print(f"\n### TRUE BUYS — owned 0 copies ({len(true_buys)} cards)\n")
    for r in sorted(true_buys, key=lambda x: (fmt_sources(x["targets"]), x["card"])):
        print(f"  {r['short']}x  {r['card']:35s} <- {fmt_sources(r['targets'])}")

    print(f"\n### CONTENTION BUYS — owned but committed to a deck that stays built ({len(contention_buys)} cards)\n")
    if not contention_buys:
        print("  (none)")
    for r in sorted(contention_buys, key=lambda x: x["card"]):
        print(f"  {r['short']}x  {r['card']}  (own {r['owned']}, "
              f"need {r['need']} for targets [{fmt_sources(r['targets'])}], "
              f"{r['committed']} locked in: {fmt_sources(r['kept'])})")

    # Good news: cards the targets need that the DISMANTLED deck was holding
    freed_used = [(c, dismantle_holds[c]) for c in target_demand
                  if dismantle_holds.get(c, 0) > 0]
    print(f"\n### Cards the targets need that DISMANTLING frees up ({len(freed_used)} cards)\n")
    for c, n in sorted(freed_used):
        owned = resolve_owned(c, collection)
        print(f"  {c}  (freed {n}x; own {owned} total)")

    print("\n### FLAT COPY-PASTE LIST (worst case = true + contention)\n")
    flat = sorted(true_buys + contention_buys, key=lambda x: x["card"])
    for r in flat:
        print(f"{r['short']} {r['card']}")

    total_buy_copies = sum(r["short"] for r in true_buys + contention_buys)
    print("\n" + "=" * 70)
    print(f"SUMMARY: {len(true_buys)} true buys + {len(contention_buys)} contention buys "
          f"= {total_buy_copies} copies to acquire")
    print("=" * 70)


if __name__ == "__main__":
    main()
