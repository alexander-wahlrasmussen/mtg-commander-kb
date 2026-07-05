#!/usr/bin/env python3
"""
collection_by_tag.py — group the owned collection by Scryfall function-tag.

Turns "when I build a deck and need N ramp / N draw pieces, what do I own?" into a
lookup. Joins the Moxfield haves CSV (ownership, reskin-alias resolved) to the
Scryfall Tagger function-tags in collection/oracle-tags.json and emits one section
per tag listing the owned cards that carry it.

DERIVED, not maintained: re-run after a collection pull or update_tag_index.py and
the view is current — the file is never hand-edited. Output is deterministic (keyed
off the input CSV + tag-fetch date, no wall-clock), so a git diff reflects a real
change in what you own or how Scryfall tags it, nothing else.

CAVEAT (same as card_lookup): function-tags are coarse and advisory — ~40 buckets,
~2 per card, crowd-sourced and incomplete. A section is a shortlist to READ from
before adding a card, not a finished package, and a tag is not the oracle text.

Usage:
    python scripts/collection_by_tag.py                    # write collection/collection_by_tag.md
    python scripts/collection_by_tag.py --tags ramp,draw   # print just those sections to stdout
    python scripts/collection_by_tag.py --list-tags        # available tags + owned counts, then exit
    python scripts/collection_by_tag.py --csv collection/moxfield_haves_....csv
    python scripts/collection_by_tag.py --out somewhere.md

Data: collection/moxfield_haves_*.csv (ownership) x collection/oracle-tags.json
(tags) x collection/oracle-cards.json (name -> oracle_id join). Refresh tags with
update_tag_index.py, cards with update_scryfall_data.py.
"""
import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

from deck_sim import load_reskin_aliases                    # noqa: E402
from unlock_optimizer import load_owned, latest_csv         # noqa: E402
import card_lookup                                          # noqa: E402

TAGS_FILE = ROOT / "collection" / "oracle-tags.json"
DEFAULT_OUT = ROOT / "collection" / "collection_by_tag.md"


def build_oid_index(cards):
    """name.lower() -> (oracle_id, display_name).

    Mirrors deck_sim.load_oracle_index precedence: a real card's name never gets
    overwritten by a junk layout (token / art series) that shares it.
    """
    idx = {}
    for c in cards:
        oid = c.get("oracle_id")
        if not oid:
            continue
        disp = c.get("name", "")
        junk = c.get("layout", "normal") in card_lookup.JUNK_LAYOUTS
        for nm in card_lookup.face_names(c):   # already lowercased, full name + faces
            if nm and (nm not in idx or not junk):
                idx[nm] = (oid, disp)
    return idx


def load_tag_data():
    """(by_oracle_id: {oid: [tags]}, fetched_at). Same file as card_lookup.load_tags_index."""
    if not TAGS_FILE.exists():
        sys.exit(f"ERROR: {TAGS_FILE} not found — run scripts/update_tag_index.py first")
    with TAGS_FILE.open(encoding="utf-8") as f:
        data = json.load(f)
    return data.get("by_oracle_id", {}), data.get("fetched_at", "unknown")


def collect(owned, proxy, oid_index, by_oracle_id):
    """Return (tag -> sorted [(display, own, prox)], stats).

    owned/proxy are canonical-name -> count (reskin-resolved by load_owned). We
    first aggregate by resolved oracle_id so a card owned under BOTH its reskin and
    its canonical name folds into one line with summed counts — which also makes the
    output order-independent (set-iteration order can no longer leak into it). A card
    with multiple tags then lands in every one of its sections: the point of the
    grouped view, and the reason it is larger than a flat list.
    """
    agg = {}                                   # oid -> [display, own, prox]
    unresolved = 0
    for key in set(owned) | set(proxy):
        own, prox = owned.get(key, 0), proxy.get(key, 0)
        if own + prox <= 0:
            continue
        entry = oid_index.get(key.lower())
        if entry is None:
            unresolved += 1                    # name unmatched to oracle data (tokens/odd exports)
            continue
        oid, disp = entry
        slot = agg.setdefault(oid, [disp, 0, 0])
        slot[1] += own
        slot[2] += prox

    tag_cards = defaultdict(list)
    tagged = 0
    for oid, (disp, own, prox) in agg.items():
        tags = by_oracle_id.get(oid, [])
        if not tags:
            continue                           # in the tag DB but no function tag (lands, vanillas)
        tagged += 1
        for t in tags:
            tag_cards[t].append((disp, own, prox, oid))
    # Sort by name, then oid — a total order, so ties never depend on run-time hashing.
    ordered = {t: [(d, o, p) for d, o, p, _ in sorted(v, key=lambda r: (r[0].lower(), r[3]))]
               for t, v in tag_cards.items()}
    stats = {"owned_uniques": len(agg) + unresolved, "tagged_uniques": tagged, "unresolved": unresolved}
    return ordered, stats


def fmt_card(disp, own, prox):
    if own == 0 and prox:
        ann = ["proxy" if prox == 1 else f"{prox} proxy"]
    else:
        ann = ([f"x{own}"] if own > 1 else []) + ([f"{prox} proxy"] if prox else [])
    return f"- {disp}" + (f"  ({', '.join(ann)})" if ann else "")


def render_sections(tag_cards, tags):
    out = []
    for t in tags:
        cards = tag_cards.get(t, [])
        out.append(f"## {t}  ({len(cards)} cards)")
        out.extend(fmt_card(*c) for c in cards)
        out.append("")
    return "\n".join(out)


def render_markdown(tag_cards, stats, csv_name, fetched_at):
    untagged = stats["owned_uniques"] - stats["tagged_uniques"]
    header = [
        "# Collection by Function Tag",
        "",
        f"_Generated by `scripts/collection_by_tag.py` — {csv_name} x oracle-tags.json "
        f"(Tagger fetch {fetched_at})._",
        "_Scryfall Tagger function-tags are coarse & advisory (~2 per card, crowd-sourced, "
        "incomplete)._",
        "_A section is a shortlist to READ from before adding a card, not a finished package. "
        "A tag is not the oracle text._",
        "",
        f"Owned uniques: {stats['owned_uniques']} · with >=1 function tag: "
        f"{stats['tagged_uniques']} · untagged (lands / vanillas / unmatched, not listed): "
        f"{untagged}.",
        "",
        "Cards with multiple tags appear in each of their sections.",
        "",
        "---",
        "",
    ]
    return "\n".join(header) + render_sections(tag_cards, sorted(tag_cards)) + "\n"


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description="Group the owned collection by Scryfall function-tag.")
    ap.add_argument("--csv", help="Moxfield haves CSV (default: latest collection/moxfield_haves_*.csv)")
    ap.add_argument("--out", help=f"output .md (default: {DEFAULT_OUT.relative_to(ROOT)})")
    ap.add_argument("--tags", help="comma-separated tags: print just those sections to stdout, write nothing")
    ap.add_argument("--list-tags", action="store_true", help="list available tags with owned counts, then exit")
    args = ap.parse_args()

    aliases = load_reskin_aliases()
    csv_path = Path(args.csv) if args.csv else latest_csv()
    if not csv_path.is_absolute():
        csv_path = ROOT / csv_path
    if not csv_path.exists():
        sys.exit(f"ERROR: CSV not found: {csv_path}")
    owned, proxy = load_owned(csv_path, aliases)

    by_oracle_id, fetched_at = load_tag_data()
    print("Loading card data (large file, a few seconds)...", file=sys.stderr)
    oid_index = build_oid_index(card_lookup.load_cards())

    tag_cards, stats = collect(owned, proxy, oid_index, by_oracle_id)
    if not tag_cards:
        sys.exit("ERROR: no owned card resolved to a function tag — check the CSV and oracle-tags.json.")

    if args.list_tags:
        for t in sorted(tag_cards, key=lambda t: (-len(tag_cards[t]), t)):
            print(f"{len(tag_cards[t]):4d}  {t}")
        return 0

    if args.tags:
        want = [t.strip() for t in args.tags.split(",") if t.strip()]
        unknown = [t for t in want if t not in tag_cards]
        if unknown:
            print(f"Unknown tag(s): {', '.join(unknown)}", file=sys.stderr)
            print(f"Available: {', '.join(sorted(tag_cards))}", file=sys.stderr)
        want = [t for t in want if t in tag_cards]
        if not want:
            return 2
        print(render_sections(tag_cards, want).rstrip())
        return 0

    out_path = Path(args.out) if args.out else DEFAULT_OUT
    if not out_path.is_absolute():
        out_path = ROOT / out_path
    out_path.write_text(render_markdown(tag_cards, stats, csv_path.name, fetched_at), encoding="utf-8")
    print(f"Wrote {out_path.relative_to(ROOT)} — {len(tag_cards)} tags, "
          f"{stats['tagged_uniques']} tagged cards of {stats['owned_uniques']} owned uniques "
          f"({stats['unresolved']} names unmatched to oracle data).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
