#!/usr/bin/env python3
"""report.py — one deck's full scouting profile across every framework and oracle.

The consolidation capstone. Once deck_registry made the per-deck facts single-source, this
ties them together with the lab clocks and the results oracles into one card you can read
before a game or when deciding a build — instead of cross-referencing the bake-off, the
clock sweep, the gauntlet and the self-meta tables by hand.

Everything here is READ from existing sources (no new modelling):
  - deck_registry            identity, commander, win line, mulligan keep band, kill tree
  - framework_bakeoff        the framework scorers (CC / Disciple / WotC / BDD) + front_edge
  - pod_gauntlet_clocks.json the lab decap/table medians + curves (front edge off the curve)
  - the oracle snapshots     pod_gauntlet / self_meta / interaction P(win), from framework_bakeoff

Usage
    python scripts/report.py genome          # fuzzy match on slug / name / stem
    python scripts/report.py "grand design"
    python scripts/report.py --all           # every roster deck, one card each
    python scripts/report.py --list
"""
import argparse
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

for _s in (sys.stdout, sys.stderr):            # cards use →, ·, en-dashes, ✓
    if hasattr(_s, "reconfigure"):
        try:
            _s.reconfigure(encoding="utf-8", errors="replace")
        except (ValueError, OSError):
            pass

# framework_bakeoff carries the scorers, loaders, oracle snapshots AND the registry handle.
_spec = importlib.util.spec_from_file_location(
    "framework_bakeoff", Path(__file__).parent / "framework_bakeoff.py")
fb = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(fb)
reg = fb.deck_registry


def resolve(frag):
    """Fuzzy: match the argument against slug, display name, or decklist stem."""
    f = frag.lower()
    for slug, d in reg.DECKS.items():
        if f in (slug, d["stem"]) or f == slug:
            return slug
    hits = [slug for slug, d in reg.DECKS.items()
            if f in slug or f in d["name"].lower() or f in d["stem"]]
    if len(hits) == 1:
        return hits[0]
    if not hits:
        sys.exit(f"no roster deck matches {frag!r} (try --list)")
    sys.exit(f"ambiguous {frag!r} -> {', '.join(hits)}; be more specific")


def kill_tree_for(slug):
    """The kill-tree spec for this deck's registry slug, or None (only 4 are encoded)."""
    for spec in reg.KILL_TREES.values():
        if spec["reg_slug"] == slug:
            return spec
    return None


def fmt_pct(v):
    return f"{v:.0f}%" if isinstance(v, (int, float)) else "  —"


def card(slug, idx, gc, aliases, clocks):
    d = reg.DECKS[slug]
    prof = fb.profile(slug, idx, gc, aliases)
    c = clocks.get(slug, {})
    decap, table = (c.get("med", ["?", "?"]) + ["?", "?"])[:2]
    f6, f7, f8 = (fb.front_edge(c, t) if c else None for t in (6, 7, 8))
    bm, _bd, _miss = fb.score_bdd_mana(slug, idx, aliases)
    gpw, smw = fb.RICHER_ORACLE.get(slug, (None, None))
    iaw = fb.INTERACTION_ORACLE.get(slug)
    cc = d["cc"]
    axes = "/".join(map(str, d["cc_axes"])) if d["cc_axes"] else "—"
    lab = f"{d['lab'][0]} --mode {d['lab'][1]}" if d["lab"] else "(multi-variant; no base lab)"
    band = f"{d['min_lands']}-{d['max_lands']} lands" + (" (hi-curve)" if d["hi_curve"] else "")
    axes_keep = " + ".join([d["bottleneck"], *d.get("also", [])])

    print(f"\n{'═' * 78}")
    print(f" {d['name']}   ·   {d['commander']}")
    print(f" slug {slug} · deck {reg.resolve_deck(d['stem']).name if reg.resolve_deck(d['stem']) else '!! MISSING'}")
    print(f"{'═' * 78}")

    print(" CLOCK (lab goldfish)")
    print(f"   decap median {decap} · table median {table} · never-in-horizon "
          f"{fmt_pct(c.get('never',[None])[0]) if c else '—'} decap")
    print(f"   front edge P(decap≤T):  T6 {fmt_pct(f6)} · T7 {fmt_pct(f7)} · T8 {fmt_pct(f8)}"
          "   (the pod's real bar = T7)")
    print(f"   lab: {lab}")

    print(" RESULTS ORACLES (P win)")
    print(f"   vs combo pod (gauntlet) {fmt_pct(gpw)} · roster pod (self-meta) {fmt_pct(smw)}"
          f" · + interaction {fmt_pct(iaw)}")

    print(" FRAMEWORK SCORES")
    print(f"   Conversion Check {cc if cc is not None else '—'}/20 (core/kill/dur/intr {axes})"
          f" · Disciple {fb.score_disciple(slug, prof)} · WotC b{fb.score_wotc(slug, prof)}")
    print(f"   BDD consistency {fb.score_bdd_consistency(slug, prof)}/5 · BDD win-line mana {bm:g}"
          f" · Game Changers {len(prof['gc'])}")

    print(" PLAN")
    print(f"   win line: {d['win_line']['line']}")
    print(f"   mulligan: {axes_keep} bottleneck · keep {band}")
    if d.get("mixed"):
        print(f"   note: {d['mixed']}")

    kt = kill_tree_for(slug)
    if kt:
        print(" KILL TREE (cheapest-first)")
        for _lid, need, kill, clock, kind in kt["lines"]:
            need1 = need.replace("<br/>", " ").split(" (")[0]
            kill1 = kill.replace("<br/>", " ")
            print(f"   • [{kind:<7}] {need1}  →  {kill1}  (⏱ {clock})")


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0],
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("deck", nargs="?", help="slug / name / stem (fuzzy)")
    ap.add_argument("--all", action="store_true", help="one card per roster deck")
    ap.add_argument("--list", action="store_true", help="list roster slugs")
    a = ap.parse_args()
    if a.list:
        for slug, d in reg.DECKS.items():
            print(f"  {slug:<22}{d['name']}")
        return
    if not a.all and not a.deck:
        ap.error("give a deck (fuzzy), or --all / --list")
    idx = fb.load_oracle()
    gc = fb.load_gc()
    aliases = fb.load_aliases()
    clocks = fb.load_clocks()
    slugs = list(reg.DECKS) if a.all else [resolve(a.deck)]
    for slug in slugs:
        card(slug, idx, gc, aliases, clocks)
    print()


if __name__ == "__main__":
    main()
