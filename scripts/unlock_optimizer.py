#!/usr/bin/env python3
"""unlock_optimizer.py — rank cross-deck card contention and one-purchase unlocks.

Backlog #3. Automates `Build_And_Swap_Tracker.md` §4 ("cross-deck contention —
don't double-spend the same card") and the "which buy unlocks the most" question,
straight from the Moxfield CSV + decklists instead of by hand.

DEMAND = how many decks physically want a card. A card in N decks needs N copies
to be in all N at once; owning M < N is an OVER-COMMITMENT (deficit = N − M). We
count two demand sources:
  * ACTIVE decks (decks/*.txt) — deployed demand (the card is in the list now).
  * BUILD targets (decks/considering/<name>.txt) — planned demand (a pending
    build wants it). Default builds = the two the user committed to (Hashaton +
    Kefka); override with --build, or fold in everything with --all-considering
    (noisy — the considering/ folder holds mutually-exclusive candidates, e.g. 8
    Glarb variants, so their shared cards over-count).

TWO ANSWERS:
  OVER-COMMITTED  owned cards with demand > owned, ranked by deficit — the
                  staples you're double-booking (the §4 table, automated).
  ONE-PURCHASE    buy candidates ranked by how many distinct plans a copy serves
  UNLOCK          — the single buys that free the most pending swaps/builds.

Reskin aliases are resolved on BOTH the decklist and the CSV (CLAUDE.md: never
declare a card unowned without the alias check) so a UB-printed name and its
canonical never miss-match. GC cards are flagged (3-GC-cap contention matters).

Heuristic, like everything here: it counts list membership, not whether a copy is
"free" vs locked in a protected deck (that's `availability_check.py`'s job, which
this complements). Proxies are reported separately and never counted as owned.

Usage
    python scripts/unlock_optimizer.py                       # active + the 2 live builds
    python scripts/unlock_optimizer.py --build hashaton-thoracle insider-trading
    python scripts/unlock_optimizer.py --all-considering     # every candidate (noisy)
    python scripts/unlock_optimizer.py --csv collection/moxfield_haves_....csv
"""
import argparse
import csv
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from deck_sim import load_reskin_aliases                      # noqa: E402
from validate import load_game_changers                       # noqa: E402
from availability_check import read_decklist, norm            # noqa: E402

DEFAULT_BUILDS = ["hashaton-thoracle", "forced-liquidation"]  # Hashaton + Kefka (the live builds)


def latest_csv():
    csvs = sorted((ROOT / "collection").glob("moxfield_haves_*.csv"))
    if not csvs:
        sys.exit("ERROR: no collection/moxfield_haves_*.csv found")
    return csvs[-1]


def label(stem):
    """Trim the dated suffix: 'the-grand-design-20260502' -> 'the-grand-design'."""
    for i, part in enumerate(stem.split("-")):
        if part[:2] == "20" and part[2:].isdigit():
            return "-".join(stem.split("-")[:i]) or stem
    return stem


def display(name):
    """Title-case a normalized name without mangling apostrophes/commas
    ('an offer you can't refuse' -> "An Offer You Can't Refuse")."""
    import re
    return re.sub(r"(^|[\s(])([a-z])", lambda m: m.group(1) + m.group(2).upper(), name)


def deck_cards(path, aliases):
    out = defaultdict(int)
    for k, v in read_decklist(path).items():
        out[aliases.get(k, k)] += v
    return out


def load_owned(csv_path, aliases):
    owned, proxy = defaultdict(int), defaultdict(int)
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            key = aliases.get(norm(row["Name"]), norm(row["Name"]))
            (proxy if row.get("Proxy", "False") == "True" else owned)[key] += int(row["Count"])
    return owned, proxy


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--csv", type=Path, default=None)
    ap.add_argument("--build", nargs="*", default=None,
                    help="considering/ build name fragments to treat as live demand")
    ap.add_argument("--all-considering", action="store_true",
                    help="fold in every decks/considering build (over-counts exclusive candidates)")
    ap.add_argument("--min-demand", type=int, default=2,
                    help="only show cards wanted by >= this many decks (default 2)")
    ap.add_argument("--no-proxy", action="store_true",
                    help="count only REAL copies (default: proxies count as physical copies — "
                         "this is a proxy-friendly Bracket-3 collection)")
    args = ap.parse_args()

    aliases = load_reskin_aliases()
    gc = load_game_changers()
    csv_path = args.csv or latest_csv()
    owned, proxy = load_owned(csv_path, aliases)

    active = sorted((ROOT / "decks").glob("*.txt"))
    cdir = ROOT / "decks" / "considering"
    if args.all_considering:
        builds = sorted(cdir.glob("*.txt"))
    else:
        want = args.build if args.build is not None else DEFAULT_BUILDS
        builds = [p for p in sorted(cdir.glob("*.txt"))
                  if any(frag in p.stem for frag in want)]

    # demand: card -> {"active": [labels], "build": [labels]}
    demand = defaultdict(lambda: {"active": [], "build": []})
    for df in active:
        for card in deck_cards(df, aliases):
            demand[card]["active"].append(label(df.stem))
    for bf in builds:
        for card in deck_cards(bf, aliases):
            demand[card]["build"].append(label(bf.stem))

    print(f"collection: {csv_path.relative_to(ROOT)}")
    print(f"demand sources: {len(active)} active decks + {len(builds)} build(s): "
          f"{', '.join(label(b.stem) for b in builds) or '(none)'}\n")

    proxy_counts = not args.no_proxy
    avail_kind = "owned + proxy" if proxy_counts else "owned (real only)"

    def tag(card):
        return " (GC)" if card in gc else ""

    # --- Report 1: over-commitment (the §4 contention table, automated) -------
    # A card in N decks needs N physical copies; short = N − available copies.
    rows = []
    for card, d in demand.items():
        n = len(d["active"]) + len(d["build"])
        real, prox = owned.get(card, 0), proxy.get(card, 0)
        a = real + (prox if proxy_counts else 0)
        if n >= args.min_demand and n > a:
            rows.append((n - a, n, real, prox, card, d))
    rows.sort(key=lambda r: (-r[0], -r[1], r[4]))

    print(f"{'='*94}\nOVER-COMMITTED — wanted by ≥{args.min_demand} decks, short of "
          f"physical copies (short = demand − {avail_kind}).\n")
    print(f"  {'short':>5} {'dem':>3} {'real':>4} {'pxy':>3}  {'card':32} wanted by")
    for short, n, real, prox, card, d in rows[:30]:
        who = d["active"] + [f"[BUILD]{w}" for w in d["build"]]
        print(f"  {short:>5} {n:>3} {real:>4} {prox:>3}  {display(card)[:32]:32} "
              f"{', '.join(who)}{tag(card)}")
    if not rows:
        print("  (nothing short once proxies are counted — try --no-proxy)")
    elif len(rows) > 30:
        print(f"  … +{len(rows) - 30} more")

    # --- Report 2: build acquisitions / one-purchase unlock -------------------
    # Cards a live BUILD wants that you own 0 REAL of = a buy-or-proxy decision.
    # Shared buys (wanted by >1 build) are the highest-leverage single purchases.
    buys = []
    for card, d in demand.items():
        if d["build"] and owned.get(card, 0) == 0:
            buys.append((len(d["build"]), len(d["active"]) + len(d["build"]),
                         proxy.get(card, 0), card, d))
    buys.sort(key=lambda r: (-r[0], -r[1], r[3]))

    print(f"\n{'='*94}\nONE-PURCHASE UNLOCK — cards the live build(s) need (own 0 real); "
          f"shared buys first.\n")
    print(f"  {'bld':>3} {'dem':>3} {'pxy':>3}  {'card':32} for")
    for nb, n, prox, card, d in buys[:25]:
        for_str = " + ".join(d["build"])
        if d["active"]:
            for_str += f"  (also in {len(d['active'])} active)"
        print(f"  {nb:>3} {n:>3} {prox:>3}  {display(card)[:32]:32} {for_str}{tag(card)}")
    if not buys:
        print("  (no live build, or every build card owned — pass --build <name>)")

    # --- top line -------------------------------------------------------------
    print(f"\n{'='*94}\nTOP LINE")
    if rows:
        t = rows[0]
        print(f"  most over-committed: {display(t[4])} — wanted by {t[1]}, "
              f"have {t[2]} real{f'+{t[3]} proxy' if t[3] else ''}, short {t[0]}{tag(t[4])}")
    shared = [b for b in buys if b[0] >= 2]
    if shared:
        s = shared[0]
        print(f"  highest-leverage buy: {display(s[3])} — one copy serves "
              f"{s[0]} builds ({' + '.join(s[4]['build'])}){tag(s[3])}")
    elif buys:
        print(f"  top build buy: {display(buys[0][3])} — for {buys[0][4]['build'][0]}{tag(buys[0][3])}")
    gc_rows = [r for r in rows if r[4] in gc]
    if gc_rows:
        print(f"  GC contention (watch the 3-GC cap): "
              f"{', '.join(display(r[4]) for r in gc_rows[:6])}")
    print("\n  NOTE: demand = current decklists + considering builds. Pending per-deck "
          "swaps not yet\n        written to a .txt (e.g. the Kiki-Jiki Exile's/Replication "
          "swap) are NOT seen.")


if __name__ == "__main__":
    main()
