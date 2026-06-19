#!/usr/bin/env python3
"""keep_spec.py — generate per-deck mulligan KEEP specs (Backlog #5).

Emits analysis/keep_specs.json: per deck, what a "good hand" is, so deck_sim can
mulligan toward THIS deck's plan instead of on land count alone (the generic
"has a CMC<=3 play" keep moved 0/16 medians; see analysis/Plan_Aware_Mulligan_2026-06-16.md).

Two layers, kept separate on purpose:
  JUDGMENT (hand-curated, reviewed with the user 2026-06-16): bottleneck class +
    land band + hi_curve flag. This is the domain call — which constraint actually
    gates each deck's kill (FINDING a piece / MANA acceleration / BOARD-commander).
  BUCKETS (generated, never hand-typed): the key / tutor / ramp / selection card
    lists, derived from framework_bakeoff's already-verified machinery — the
    WIN_LINE pieces (each Summary's cheapest kill line) + the function tagger
    (ramp/draw/tutor). So the card lists inherit the bake-off's verification, and
    a decklist edit re-flows them on the next --write.

Spec per deck (keyed by the decklist stem = deck_sim's deck_key):
  bottleneck          FINDING | MANA | BOARD     (which keep_hand branch runs)
  min_lands/max_lands keep band, closed interval (ceiling 4; 5 only hi_curve)
  hi_curve            bool — a MANA deck that tolerates a 4-land no-ramp keep
  cmdr_cmc, cmdr      commander mana value + name (BOARD curve check)
  key_cards[]         WIN_LINE pieces present in the deck — a piece = advancing
  tutors[]            cards tagged 'tutor' — a virtual key card (FINDING)
  ramp[]              cards tagged 'ramp' incl. mana rocks (MANA / BOARD curve)
  selection[]         cards tagged 'draw' — dig; n_selection_needed = a FINDING keep
  n_selection_needed  default 2
  mixed               note when the deck also leans on a second axis (watch list)
All card names are PRINTED names (lowercased) exactly as they appear in the .txt,
so deck_sim — which keys its hand on the printed name — matches without re-aliasing.

Usage:
  python scripts/keep_spec.py --show     # human-readable per-deck summary
  python scripts/keep_spec.py --write    # (re)write analysis/keep_specs.json
"""
import argparse
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "analysis" / "keep_specs.json"

for _s in (sys.stdout, sys.stderr):
    if hasattr(_s, "reconfigure"):
        try:
            _s.reconfigure(encoding="utf-8", errors="replace")
        except (ValueError, OSError):
            pass

# import framework_bakeoff (the verified WIN_LINE + tagger + loaders live there)
_spec = importlib.util.spec_from_file_location(
    "framework_bakeoff", Path(__file__).parent / "framework_bakeoff.py")
fb = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(fb)

# --- JUDGMENT (the domain call) ---------------------------------------------
# The bottleneck class + land band + hi_curve flag are the hand-curated part of the spec
# (reviewed with the user 2026-06-16, incl. the Radiation/Lorehold FINDING->BOARD re-tags
# and the union-keep `also` lists). They now live in deck_registry (single source of truth).
#   JUDGMENT: slug -> (bottleneck, min_lands, max_lands, hi_curve, mixed-note)
#   ALSO:     slug -> [secondary axes] for genuinely two-line decks (union keep)
# Ceiling is 4 lands; 5 only for genuinely high-curve decks. MANA = needs a rock/ramp piece.
JUDGMENT = fb.deck_registry.judgment()
ALSO = fb.deck_registry.also()

N_SELECTION_NEEDED = 2
TAG_TO_BUCKET = {"ramp": "ramp", "tutor": "tutors", "draw": "selection"}


def build_spec(slug, idx, gc, aliases):
    """One deck's spec: hand-curated JUDGMENT + generated card buckets."""
    bottleneck, lo, hi, hi_curve, mixed = JUDGMENT[slug]
    cmdr_cmc, cmdr_canon = fb.commander_mv(slug, idx, aliases)

    # printed-name buckets, generated from the tagger; canon->printed map to
    # resolve WIN_LINE pieces (canonical) to the deck's printed name.
    buckets = {"ramp": [], "tutors": [], "selection": []}
    canon_to_printed = {}
    deckset = set()
    for cnt, name, canon, card, is_cmd in fb.deck_cards(slug, idx, aliases):
        if is_cmd or card is None:
            continue
        canon_to_printed.setdefault(canon, name.lower())
        deckset.add(canon)
        for tg in fb.tag_card(card):
            b = TAG_TO_BUCKET.get(tg)
            if b and name.lower() not in buckets[b]:
                buckets[b].append(name.lower())

    # key cards = WIN_LINE pieces actually in this deck (printed name, lowercased)
    key_cards, missing = [], []
    for piece in fb.WIN_LINE[slug]["pieces"]:
        canon = aliases.get(piece.lower(), piece.lower())
        if canon in deckset:
            key_cards.append(canon_to_printed[canon])
        else:
            missing.append(piece)        # finisher named in WIN_LINE but not in list

    return {
        "deck_key": fb.DECKS[slug][1],
        "name": fb.DECKS[slug][0],
        "bottleneck": bottleneck,
        "also": ALSO.get(slug, []),
        "min_lands": lo, "max_lands": hi, "hi_curve": hi_curve,
        "cmdr": cmdr_canon, "cmdr_cmc": cmdr_cmc,
        "key_cards": sorted(key_cards),
        "tutors": sorted(buckets["tutors"]),
        "ramp": sorted(buckets["ramp"]),
        "selection": sorted(buckets["selection"]),
        "n_selection_needed": N_SELECTION_NEEDED,
        "mixed": mixed,
        "key_missing": missing,
    }


def build_all():
    idx = fb.load_oracle()
    gc = fb.load_gc()
    aliases = fb.load_aliases()
    return {fb.DECKS[slug][1]: build_spec(slug, idx, gc, aliases) for slug in fb.DECKS}


def cmd_show(specs):
    print(f"{'deck':<22}{'bottleneck':<9}{'band':>6}{'hiC':>4}{'cmdr':>5}"
          f"{'key':>4}{'tut':>4}{'ramp':>5}{'sel':>4}  mixed / key-missing")
    print("-" * 96)
    for key, s in specs.items():
        band = f"{s['min_lands']}-{s['max_lands']}"
        note = s["mixed"] or ""
        if s["key_missing"]:
            note = (note + " · " if note else "") + f"key not in list: {s['key_missing']}"
        print(f"{s['name']:<22}{s['bottleneck']:<9}{band:>6}{'Y' if s['hi_curve'] else '·':>4}"
              f"{s['cmdr_cmc']:>5.0f}{len(s['key_cards']):>4}{len(s['tutors']):>4}"
              f"{len(s['ramp']):>5}{len(s['selection']):>4}  {note}")
    print("\nbottleneck: FINDING=keep a piece/tutor/2-selection · MANA=keep ramp (~3 lands) "
          "· BOARD=cmdr on curve + early play")
    print("Per-deck buckets: keep_spec.py --show <deck> (or read analysis/keep_specs.json).")


def cmd_show_one(specs, frag):
    hits = [s for s in specs.values() if frag.lower() in s["name"].lower()
            or frag.lower() in s["deck_key"]]
    if not hits:
        sys.exit(f"no deck matches {frag!r}")
    for s in hits:
        axes = " + ".join([s["bottleneck"], *s.get("also", [])])
        print(f"\n=== {s['name']} ({s['deck_key']}) — {axes} ===")
        print(f"  band {s['min_lands']}-{s['max_lands']} lands · hi_curve {s['hi_curve']} "
              f"· commander {s['cmdr']} (cmc {s['cmdr_cmc']:.0f})")
        if s["mixed"]:
            print(f"  mixed: {s['mixed']}")
        for b in ("key_cards", "tutors", "ramp", "selection"):
            cards = s[b]
            print(f"  {b:<11}({len(cards):>2}): {', '.join(cards) if cards else '—'}")
        if s["key_missing"]:
            print(f"  WIN_LINE piece(s) not in decklist: {s['key_missing']}")


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0],
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("deck", nargs="?", help="show one deck's full buckets (fuzzy)")
    ap.add_argument("--write", action="store_true", help="(re)write analysis/keep_specs.json")
    ap.add_argument("--show", action="store_true", help="summary table (default)")
    a = ap.parse_args()
    specs = build_all()
    if a.write:
        OUT.write_text(json.dumps(specs, indent=2), encoding="utf-8")
        print(f"wrote {OUT.relative_to(ROOT)} ({len(specs)} decks)")
    if a.deck:
        cmd_show_one(specs, a.deck)
    elif a.show or not a.write:
        cmd_show(specs)


if __name__ == "__main__":
    main()
