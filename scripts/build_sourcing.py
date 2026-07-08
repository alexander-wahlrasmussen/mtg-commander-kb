#!/usr/bin/env python
"""build_sourcing.py — per-card physical-build provenance for target decks.

For each card in a target decklist, classify where its physical copy comes from
when you sleeve the deck up:

  <box>       - supplied physically by a purchased box / precon (--box Label=path)
                REGARDLESS of Moxfield ownership. Checked first: a precon ships the
                card in the box, so it is never a Buy even when owned 0. Use for a
                sealed product whose cards are not (yet) in the collection CSV.
  Buy         - not owned, OR owned but every copy is locked in a deck that stays
                built (so a copy had to be acquired). With --baseline-csv, buys
                already made (owned went 0 -> N, or a contention duplicate was
                bought) are still detected AFTER the purchase landed. With --pending
                the Buy bucket reads as "not owned yet" (unbuilt proposal) instead
                of "already in hand".
  <source>    - freed by dismantling a named deck (--dismantle) or taken from an
                already-dismantled pile (--source Label=path). Attributed only
                when no independent pool spare exists (your other copies are
                committed to kept decks, so the freed copy is the one you use).
  Collection  - owned with a spare loose in the general pool (basics always here).

Model: the --dismantle decks are torn down (their cards become sources and are
NOT counted as committed); every other active deck in --deck-dir stays built and
holds its copies. Multiple targets each treat the others as built, so a shared
scarce card surfaces as a Buy/contention rather than being double-allocated.
HEURISTIC, per-target-independent contention — trust the buckets, and spot-check
cards two targets share (a bought duplicate shows as Buy for the deck using it).

Reuses the DeckSafe builder's parser so DFC / split / UB-reskin aliases resolve
exactly like the spreadsheet. Set $DECKSAFE_REPO if the builder isn't at the
default path.

Example — regenerate the 2026-07-06 Zero-Sum + Forced Liquidation sourcing doc
(the pre-purchase baseline is recoverable from git:
 `git show <rev>:collection/moxfield_haves_2026-06-25-0748Z.csv`):

  python scripts/build_sourcing.py \
      decks/zero-sum-game-20260707.txt decks/forced-liquidation-20260625.txt \
      --csv collection/moxfield_haves_2026-07-06-1850Z.csv \
      --baseline-csv old_prepurchase.csv \
      --dismantle "diminishing returns" \
      --source Loam=archive/old_decklists/the-loam-cycle-20260404-074432.txt \
      --md analysis/Physical_Build_Sourcing_ZeroSum_ForcedLiquidation_2026-07-06.md
"""
import argparse
import os
import sys
from collections import defaultdict

sys.path.insert(0, os.environ.get("DECKSAFE_REPO", r"C:\Users\Alex\Projects\MTGDecks"))
from deck_safe_collection_builder import (   # noqa: E402
    parse_collection, parse_deck, resolve_owned, canonical_name, clean_deck_name,
)

BASICS = {"Swamp", "Forest", "Island", "Mountain", "Plains", "Wastes"}


def deck_counts(path):
    """canonical card -> count for one decklist (main + commander)."""
    actual, _sb, cmd = parse_deck(path)
    d = defaultdict(int)
    for card, n in actual.items():
        d[canonical_name(card)] += n
    if cmd:
        for c in (cmd if isinstance(cmd, (list, tuple)) else [cmd]):
            cn = canonical_name(c)
            if cn not in d:          # parse_deck may already list the commander
                d[cn] += 1
    return d


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("decks", nargs="+", help="target decklist path(s)")
    ap.add_argument("--csv", required=True, help="current collection (Moxfield haves)")
    ap.add_argument("--baseline-csv", help="pre-purchase collection, to detect buys post-purchase")
    ap.add_argument("--dismantle", action="append", default=[],
                    help="clean name of an ACTIVE deck being torn down (repeatable)")
    ap.add_argument("--source", action="append", default=[],
                    help="Label=path of an already-dismantled source pile (repeatable)")
    ap.add_argument("--box", action="append", default=[],
                    help="Label=path of a purchased box/precon that supplies its cards "
                         "physically even when owned 0; checked before Buy (repeatable)")
    ap.add_argument("--pending", action="store_true",
                    help="targets are not yet built: Buy reads as 'not owned yet', not 'in hand'")
    ap.add_argument("--deck-dir", default="decks")
    ap.add_argument("--md", help="write a markdown report to this path")
    ap.add_argument("--title", default="Physical Build Sourcing")
    ap.add_argument("--date", default="", help="date stamp for the markdown header")
    args = ap.parse_args()

    _n, cur = parse_collection(args.csv)
    base = parse_collection(args.baseline_csv)[1] if args.baseline_csv else cur

    dismantle = {d.lower() for d in args.dismantle}

    # boxes: purchased products that supply their cards physically (owned or not)
    boxes = []   # (label, cardset)
    for s in args.box:
        if "=" not in s:
            sys.exit(f"--box needs Label=path, got {s!r}")
        label, path = s.split("=", 1)
        boxes.append((label, set(deck_counts(path))))
    box_labels = [l for l, _ in boxes]

    active = {}
    for f in os.listdir(args.deck_dir):
        if f.endswith(".txt"):
            p = os.path.join(args.deck_dir, f)
            active[clean_deck_name(os.path.basename(p)).lower()] = p

    # ordered named sources: dismantled active decks first, then external piles
    sources = []   # (label, cardset)
    for name, p in active.items():
        if name in dismantle:
            sources.append((clean_deck_name(os.path.basename(p)), set(deck_counts(p))))
    dismantle_labels = [lbl for lbl, _ in sources]
    for s in args.source:
        if "=" not in s:
            sys.exit(f"--source needs Label=path, got {s!r}")
        label, path = s.split("=", 1)
        sources.append((label, set(deck_counts(path))))

    def kept_committed(target_path):
        self_clean = clean_deck_name(os.path.basename(target_path)).lower()
        kc = defaultdict(int)
        for name, p in active.items():
            if name == self_clean or name in dismantle:
                continue
            for c, n in deck_counts(p).items():
                kc[c] += n
        return kc

    def classify(c, need, kc):
        if c in BASICS:
            return "Collection", "basic land — from your basics pile"
        for lbl, cs in boxes:
            if c in cs:
                return lbl, "shipped in the box"
        owned_now = resolve_owned(c, cur)
        owned_base = resolve_owned(c, base)
        committed = kc.get(c, 0)
        if owned_base <= 0:
            return "Buy", "owned 0 (true buy)"
        if owned_base - committed < need:
            if owned_now > owned_base:
                return "Buy", f"owned {owned_base}, locked in kept decks; bought +{owned_now - owned_base}"
            return "Buy", f"owned {owned_base}, {committed} locked in kept decks (short)"
        in_sources = [lbl for lbl, cs in sources if c in cs]
        spare = owned_base - committed - len(in_sources)
        if spare >= need:
            return "Collection", f"owned {owned_base}, {committed} in kept decks; pool spare"
        if in_sources:
            return in_sources[0], f"owned {owned_base}; freed copy"
        return "Collection", f"owned {owned_base}"

    bucket_order = (box_labels + dismantle_labels
                    + [l for l, _ in sources if l not in dismantle_labels]
                    + ["Collection", "Buy"])
    seen = set()
    bucket_order = [b for b in bucket_order if not (b in seen or seen.add(b))]

    results = {}   # deck path -> {bucket: [(card, n, note)]}
    for path in args.decks:
        counts = deck_counts(path)
        kc = kept_committed(path)
        buckets = defaultdict(list)
        for c in sorted(counts):
            src, note = classify(c, counts[c], kc)
            buckets[src].append((c, counts[c], note))
        results[path] = (counts, buckets)

    # ---- console summary ----
    for path, (counts, buckets) in results.items():
        name = clean_deck_name(os.path.basename(path))
        tally = ", ".join(f"{b}={sum(n for _, n, _ in buckets.get(b, []))}"
                          for b in bucket_order if buckets.get(b))
        print(f"{name}: {tally}")

    if not args.md:
        return

    # ---- markdown report ----
    L = []
    L.append(f"# {args.title}")
    L.append("")
    if args.date:
        L.append(f"_Generated {args.date}. Where to physically pull each card when you sleeve these up._")
        L.append("")
    dm = ", ".join(f"**{l}**" for l in dismantle_labels) or "(none)"
    bx = ", ".join(f"**{l}**" for l in box_labels)
    buy_model = ("*Buy* = not owned from any source above — buy or proxy needed."
                 if args.pending else "All *Buy* cards are already acquired.")
    L.append(f"**Model:** {('open ' + bx + '; ') if bx else ''}dismantle {dm}; external "
             f"source piles are already loose; every other deck stays built. {buy_model}")
    L.append("")
    L.append("| Tag | Where to grab it |")
    L.append("|---|---|")
    for lbl in box_labels:
        L.append(f"| **{lbl}** | Ships in the box — pull it straight from the opened precon. |")
    for lbl in dismantle_labels:
        L.append(f"| **{lbl}** | Pull from the **{lbl}** deck as you take it apart. |")
    for lbl, _ in sources:
        if lbl not in dismantle_labels:
            L.append(f"| **{lbl}** | From the already-dismantled **{lbl}** pile (loose). |")
    L.append("| **Collection** | Loose in the binder / general pool (basics from your basics pile). |")
    buy_desc = ("Not owned from any source above — **buy or proxy**."
                if args.pending else "Already purchased — in the new-cards pile (incl. contention duplicates).")
    L.append(f"| **Buy** | {buy_desc} |")
    L.append("")
    L.append("> A card two targets share, where you bought a duplicate, shows as **Buy** for "
             "the deck using the fresh copy — practically correct (use the copy you bought).")
    L.append("")

    buy_title = "Buy / proxy — not yet owned" if args.pending else "Buy — already in hand"
    head = {"Buy": buy_title, "Collection": "From the collection / pool"}
    for lbl in box_labels:
        head[lbl] = f"From {lbl} (in the box)"
    for path, (counts, buckets) in results.items():
        name = clean_deck_name(os.path.basename(path))
        total = sum(counts.values())
        tally = " · ".join(f"{b} {sum(n for _, n, _ in buckets.get(b, []))}"
                           for b in bucket_order if buckets.get(b))
        L.append(f"## {name}")
        L.append(f"{len(counts)} unique / {total} cards. **{tally}**")
        L.append("")
        for b in bucket_order:
            items = buckets.get(b)
            if not items:
                continue
            cop = sum(n for _, n, _ in items)
            title = head.get(b, f"From {b}")
            L.append(f"### {title} ({len(items)} cards / {cop} copies)")
            for c, n, _note in items:
                L.append(f"- {(str(n) + '× ') if n > 1 else ''}{c}")
            L.append("")

    if dismantle_labels:
        L.append("## Teardown pulls — what leaves each dismantled deck")
        L.append("")
        for lbl in dismantle_labels:
            L.append(f"**{lbl}** →")
            for path, (counts, buckets) in results.items():
                name = clean_deck_name(os.path.basename(path))
                cards = [c for c, _, _ in buckets.get(lbl, [])]
                if cards:
                    L.append(f"- **{name} ({len(cards)}):** {', '.join(cards)}")
            L.append("")

    with open(args.md, "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")
    print(f"\nwrote {args.md} ({len(L)} lines)")


if __name__ == "__main__":
    main()
