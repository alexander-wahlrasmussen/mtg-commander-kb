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
    # deck-building fill — owned ramp in a deck's colours that it doesn't already run:
    python scripts/collection_by_tag.py --tags ramp --color BRU --exclude-deck dark-lord
    # narrow a broad tag in a wide identity to a shortlist of cheap engine pieces:
    python scripts/collection_by_tag.py --tags draw --color BGUW --exclude-deck grand-design \
                                        --max-cmc 4 --permanents --no-lands

Data: collection/moxfield_haves_*.csv (ownership) x collection/oracle-tags.json
(tags) x collection/oracle-cards.json (name -> oracle_id join). Refresh tags with
update_tag_index.py, cards with update_scryfall_data.py.
"""
import argparse
import json
import sys
from collections import defaultdict, namedtuple
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

from deck_sim import load_reskin_aliases                    # noqa: E402
from unlock_optimizer import load_owned, latest_csv         # noqa: E402
import card_lookup                                          # noqa: E402

TAGS_FILE = ROOT / "collection" / "oracle-tags.json"
DEFAULT_OUT = ROOT / "collection" / "collection_by_tag.md"

# One resolved card: identity for the colour filter, cmc/perm/land for the narrowing cuts.
CardInfo = namedtuple("CardInfo", "oid disp ci cmc perm land")


def build_oid_index(cards):
    """name.lower() -> CardInfo(oracle_id, display_name, color_identity, cmc, perm).

    Mirrors deck_sim.load_oracle_index precedence: a real card's name never gets
    overwritten by a junk layout (token / art series) that shares it. color_identity
    is the whole-card identity (Scryfall keeps it at top level for DFCs) — the value
    the --color filter tests for commander-legality in a deck's colors. perm is False
    only for cards that are purely instant/sorcery (front face), so --permanents keeps
    the persistent "engine" pieces and drops one-shot spells.
    """
    idx = {}
    for c in cards:
        oid = c.get("oracle_id")
        if not oid:
            continue
        front = c.get("type_line", "").split("//")[0].lower()   # front face for DFC/adventure/split
        info = CardInfo(
            oid=oid,
            disp=c.get("name", ""),
            ci=frozenset(c.get("color_identity", [])),
            cmc=c.get("cmc", 0.0),
            perm=not ("instant" in front or "sorcery" in front),
            land="land" in front,
        )
        junk = c.get("layout", "normal") in card_lookup.JUNK_LAYOUTS
        for nm in card_lookup.face_names(c):   # already lowercased, full name + faces
            if nm and (nm not in idx or not junk):
                idx[nm] = info
    return idx


def parse_colors(s):
    """'BRU' / 'wubrg' -> frozenset of WUBRG letters. Empty (or 'C') means colourless-only."""
    allowed = frozenset(ch for ch in s.upper() if ch in "WUBRG")
    if not allowed and s.strip().lower() not in {"c", "colorless", "colourless", ""}:
        sys.exit(f"ERROR: --color '{s}' has no WUBRG letters (use e.g. BRU, or C for colourless-only)")
    return allowed


def resolve_deck_exclusions(fuzzy, oid_index, aliases):
    """Fuzzy deck-name -> (deck_stem, {oracle_ids it runs}), reskin-resolved.

    Reuses availability_check.read_decklist (canonical decklist parser); the latest
    dated .txt wins when a prefix matches several versions.
    """
    from availability_check import read_decklist                # noqa: E402 (repo cross-module idiom)
    matches = sorted(p for p in (ROOT / "decks").glob("*.txt") if fuzzy.lower() in p.stem.lower())
    if not matches:
        sys.exit(f"ERROR: --exclude-deck '{fuzzy}' matched no decks/*.txt")
    path = matches[-1]
    oids = set()
    for name in read_decklist(path):            # keys already normalised (lowercased front-face)
        entry = oid_index.get(aliases.get(name, name).lower())
        if entry:
            oids.add(entry.oid)
    return path.stem, oids


def load_tag_data():
    """(by_oracle_id: {oid: [tags]}, fetched_at). Same file as card_lookup.load_tags_index."""
    if not TAGS_FILE.exists():
        sys.exit(f"ERROR: {TAGS_FILE} not found — run scripts/update_tag_index.py first")
    with TAGS_FILE.open(encoding="utf-8") as f:
        data = json.load(f)
    return data.get("by_oracle_id", {}), data.get("fetched_at", "unknown")


def collect(owned, proxy, oid_index, by_oracle_id,
            allowed=None, excluded=None, max_cmc=None, permanents=False, no_lands=False):
    """Return (tag -> sorted [(display, own, prox)], stats).

    owned/proxy are canonical-name -> count (reskin-resolved by load_owned). We
    first aggregate by resolved oracle_id so a card owned under BOTH its reskin and
    its canonical name folds into one line with summed counts — which also makes the
    output order-independent (set-iteration order can no longer leak into it). A card
    with multiple tags then lands in every one of its sections: the point of the
    grouped view, and the reason it is larger than a flat list.

    allowed:    frozenset of colours (WUBRG); keep only cards whose colour identity is
                a subset (colourless always passes) — a deck's in-identity candidates.
    excluded:   set of oracle_ids to drop (e.g. cards a deck already runs).
    max_cmc:    keep only cards with mana value <= this.
    permanents: keep only permanents (drop instants/sorceries).
    no_lands:   drop lands (a land tagged 'draw' is manabase, not a draw spell).

    These cuts narrow a broad tag in a wide identity (e.g. 'draw' in a 4-colour deck)
    toward an actionable shortlist of cheap, persistent engine pieces — though a tag
    that broad still needs the reader's engine-vs-one-shot judgment at the end.
    """
    excluded = excluded or set()
    agg = {}                                   # oid -> [display, own, prox, ci, cmc, perm, land]
    unresolved = 0
    for key in set(owned) | set(proxy):
        own, prox = owned.get(key, 0), proxy.get(key, 0)
        if own + prox <= 0:
            continue
        entry = oid_index.get(key.lower())
        if entry is None:
            unresolved += 1                    # name unmatched to oracle data (tokens/odd exports)
            continue
        slot = agg.setdefault(entry.oid,
                              [entry.disp, 0, 0, entry.ci, entry.cmc, entry.perm, entry.land])
        slot[1] += own
        slot[2] += prox

    kept = {}
    for oid, (disp, own, prox, ci, cmc, perm, land) in agg.items():
        if oid in excluded:
            continue
        if allowed is not None and not ci <= allowed:
            continue
        if max_cmc is not None and cmc > max_cmc:
            continue
        if permanents and not perm:
            continue
        if no_lands and land:
            continue
        kept[oid] = (disp, own, prox)

    tag_cards = defaultdict(list)
    tagged = 0
    for oid, (disp, own, prox) in kept.items():
        tags = by_oracle_id.get(oid, [])
        if not tags:
            continue                           # in the tag DB but no function tag (lands, vanillas)
        tagged += 1
        for t in tags:
            tag_cards[t].append((disp, own, prox, oid))
    # Sort by name, then oid — a total order, so ties never depend on run-time hashing.
    ordered = {t: [(d, o, p) for d, o, p, _ in sorted(v, key=lambda r: (r[0].lower(), r[3]))]
               for t, v in tag_cards.items()}
    filtering = (allowed is not None or bool(excluded) or max_cmc is not None
                 or permanents or no_lands)
    stats = {
        "owned_uniques": len(kept) if filtering else len(agg) + unresolved,
        "tagged_uniques": tagged,
        "unresolved": 0 if filtering else unresolved,
    }
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
    ap.add_argument("--color", help="keep only cards whose colour identity fits these colours (e.g. BRU); "
                                    "colourless always included")
    ap.add_argument("--exclude-deck", help="drop cards a deck already runs (fuzzy decks/*.txt name) — "
                                           "the gap-fill view: what could I ADD")
    ap.add_argument("--max-cmc", type=float, metavar="N", help="keep only cards with mana value <= N")
    ap.add_argument("--permanents", action="store_true",
                    help="keep only permanents (drop instants/sorceries) — persistent 'engine' pieces")
    ap.add_argument("--no-lands", action="store_true",
                    help="drop lands (a land tagged e.g. 'draw'/'ramp' is manabase, not a spell)")
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

    allowed = parse_colors(args.color) if args.color is not None else None
    excluded, deck_stem = set(), None
    if args.exclude_deck:
        deck_stem, excluded = resolve_deck_exclusions(args.exclude_deck, oid_index, aliases)
    if allowed is not None or excluded or args.max_cmc is not None or args.permanents or args.no_lands:
        scope = []
        if allowed is not None:
            scope.append(f"colour identity ⊆ {{{''.join(sorted(allowed)) or 'C'}}}")
        if excluded:
            scope.append(f"excluding {len(excluded)} cards already in {deck_stem}")
        if args.max_cmc is not None:
            scope.append(f"mana value ≤ {args.max_cmc:g}")
        if args.permanents:
            scope.append("permanents only")
        if args.no_lands:
            scope.append("no lands")
        print("Filtered view: " + "; ".join(scope), file=sys.stderr)

    tag_cards, stats = collect(owned, proxy, oid_index, by_oracle_id, allowed=allowed,
                               excluded=excluded, max_cmc=args.max_cmc,
                               permanents=args.permanents, no_lands=args.no_lands)
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
