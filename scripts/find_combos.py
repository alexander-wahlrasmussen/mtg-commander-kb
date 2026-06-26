#!/usr/bin/env python3
"""
find_combos.py — check a full decklist for combos via Commander Spellbook.

Posts a decklist to Commander Spellbook's "Find My Combos" endpoint and reports:

  - COMPLETE combos already in the deck (every piece present)
  - ALMOST-there combos missing exactly N specific cards (the actionable buys —
    directly serves the "don't cap combo lines for lack of cards" house rule:
    these are the combos a purchase would unlock)
  - (optionally) combos you'd gain by changing commanders

This is NOT a rules engine and interprets no card text — it asks Commander
Spellbook's curated combo database what it knows about this exact card list.
Card *names* are the only input, so accuracy is bounded by name resolution:
UB reskins are mapped to their real names first (REF_Reskin_Aliases.md, the
CLAUDE.md hard rule), but any name CSB doesn't recognise is silently dropped on
their side — names we had to alias are reported so misses are auditable.

Usage:
    python scripts/find_combos.py calamity            # fuzzy stem match in decks/
    python scripts/find_combos.py decks/foo.txt       # explicit path
    python scripts/find_combos.py glarb --almost-max 2 # widen near-miss search
    python scripts/find_combos.py kefka --almost-max 0 # complete combos only
    python scripts/find_combos.py rad --changing       # also "if you swapped commanders"
    python scripts/find_combos.py rad --json out.json  # raw API results

Commander resolution reuses deck_registry (single source of truth); reskin
aliases reuse deck_sim.load_reskin_aliases(). Network is required at runtime
(POST https://backend.commanderspellbook.com/find-my-combos).
"""

import argparse
import json
import sys
import urllib.error
import urllib.request
import importlib.util as _il
from pathlib import Path

ROOT = Path(__file__).parent.parent
DECKS_DIR = ROOT / "decks"
API = "https://backend.commanderspellbook.com/find-my-combos"
COMBO_URL = "https://commanderspellbook.com/combo/{}/"


def _load_sibling(name):
    """Load a sibling script as a module (repo idiom — no package on sys.path)."""
    spec = _il.spec_from_file_location(name, Path(__file__).parent / f"{name}.py")
    mod = _il.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# deck_sim is stdlib-only; importing it gives us the canonical commander map
# (deck_registry-backed) and the reskin alias parser in one shot.
deck_sim = _load_sibling("deck_sim")
COMMANDERS = deck_sim.COMMANDERS


# ---------------------------------------------------------------------------
# Decklist parsing
# ---------------------------------------------------------------------------
def _entries(lines):
    """'<qty> <name>' lines -> [(qty, name)], skipping SIDEBOARD blocks."""
    out, sideboard = [], False
    for s in lines:
        if s.upper().startswith("SIDEBOARD"):
            sideboard = True
            continue
        if sideboard:
            continue
        parts = s.split(" ", 1)
        if len(parts) != 2 or not parts[0].isdigit():
            continue
        out.append((int(parts[0]), parts[1].strip()))
    return out


def parse_decklist(path):
    """Return (commanders, main, meta) as lists of (qty, name).

    Commander is taken from deck_registry by filename-stem prefix (authoritative).
    For lists not in the registry (considering/ candidates, external decks) the
    Moxfield export convention is used as a fallback: the final blank-line-
    separated block of 1-2 cards is the commander(s).
    """
    raw = path.read_text(encoding="utf-8")
    segments, cur = [], []
    for line in raw.splitlines():
        s = line.strip()
        if not s:
            if cur:
                segments.append(cur)
                cur = []
            continue
        cur.append(s)
    if cur:
        segments.append(cur)

    all_entries = [e for seg in segments for e in _entries(seg)]
    stem = path.stem
    deck_key = next((k for k in COMMANDERS if stem.startswith(k)), None)
    reg_cmd = COMMANDERS.get(deck_key)

    commanders, main = [], []
    if reg_cmd:
        for qty, name in all_entries:
            (commanders if name.lower() == reg_cmd.lower() else main).append((qty, name))
        if not commanders:  # registry knows the commander but it wasn't listed inline
            commanders.append((1, reg_cmd))
    else:
        tail = _entries(segments[-1]) if len(segments) > 1 else []
        if tail and len(tail) <= 2:
            commanders = tail
            names = {n.lower() for _, n in commanders}
            main = [e for e in all_entries if e[1].lower() not in names]
        else:
            main = all_entries  # can't tell — send everything; CSB still finds combos

    return commanders, main, {"stem": stem, "deck_key": deck_key, "registry_commander": reg_cmd}


# ---------------------------------------------------------------------------
# Commander Spellbook API
# ---------------------------------------------------------------------------
def _post(url, payload):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url, data=data, method="POST",
        headers={"Content-Type": "application/json", "User-Agent": "mtg-commander-kb/find_combos"},
    )
    with urllib.request.urlopen(req, timeout=45) as resp:
        return json.loads(resp.read().decode("utf-8"))


def find_my_combos(payload, limit=500):
    """POST the deck, following pagination. Returns (identity, included, almost, changing)."""
    url = f"{API}?limit={limit}"
    identity, included, almost, changing = None, [], [], []
    while url:
        d = _post(url, payload)
        res = d.get("results") or {}
        identity = res.get("identity") or identity
        included += res.get("included", [])
        almost += res.get("almostIncluded", [])
        changing += res.get("includedByChangingCommanders", [])
        url = d.get("next")  # re-POSTs the body to the offset URL if more pages exist
    return identity, included, almost, changing


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------
def _uses(combo):
    return [u["card"]["name"] for u in combo.get("uses", [])]


def _features(combo):
    return [p["feature"]["name"] for p in combo.get("produces", [])]


def _fmt_combo(combo, deck_lower=None, indent="    "):
    feats = ", ".join(_features(combo)) or "(see page)"
    lines = [f"{indent}[{combo['id']}] {feats}"]
    if deck_lower is None:
        lines.append(f"{indent}  uses: " + " + ".join(_uses(combo)))
    else:
        have = [n for n in _uses(combo) if n.lower() in deck_lower]
        need = [n for n in _uses(combo) if n.lower() not in deck_lower]
        if have:
            lines.append(f"{indent}  have: " + ", ".join(have))
        lines.append(f"{indent}  need: " + (", ".join(need) if need else "(non-card requirement — see page)"))
    lines.append(f"{indent}  {COMBO_URL.format(combo['id'])}")
    return "\n".join(lines)


def query_deck(path):
    """Parse a decklist, resolve reskins, and ask Commander Spellbook what combos
    it holds. Returns a dict {identity, included, almost, changing, deck_lower,
    meta, aliased}. Raises urllib/Timeout errors on network failure (caller's to
    handle). The reusable core of main() — also used by deck_doctor's combo audit."""
    commanders, main, meta = parse_decklist(path)
    aliases = deck_sim.load_reskin_aliases()
    aliased = []

    def card_objs(entries):
        objs = []
        for qty, name in entries:
            real = aliases.get(name.lower(), name)
            if real != name:
                aliased.append(f"{name} -> {real}")
            objs.append({"card": real, "quantity": qty})
        return objs

    payload = {"commanders": card_objs(commanders), "main": card_objs(main)}
    deck_lower = {c["card"].lower() for c in payload["commanders"] + payload["main"]}
    identity, included, almost, changing = find_my_combos(payload)
    return {"identity": identity, "included": included, "almost": almost,
            "changing": changing, "deck_lower": deck_lower, "meta": meta,
            "aliased": sorted(set(aliased))}


def resolve_deck(arg):
    """Path or fuzzy stem substring -> Path to a decklist in decks/."""
    p = Path(arg)
    if p.exists() and p.suffix == ".txt":
        return p
    pool = list(DECKS_DIR.glob("*.txt")) + list((DECKS_DIR / "considering").glob("*.txt"))
    matches = sorted(f for f in pool if arg.lower() in f.stem.lower())
    if not matches:
        sys.exit(f"No decklist in {DECKS_DIR} (or considering/) matches '{arg}'.")
    if len(matches) > 1:
        names = "\n  ".join(m.name for m in matches)
        sys.exit(f"'{arg}' is ambiguous; matches:\n  {names}")
    return matches[0]


def main():
    ap = argparse.ArgumentParser(description="Check a decklist for combos via Commander Spellbook.")
    ap.add_argument("deck", help="decks/*.txt path or fuzzy stem substring")
    ap.add_argument("--almost-max", type=int, default=1, metavar="N",
                    help="show near-miss combos missing up to N specific cards (default 1; 0 = hide)")
    ap.add_argument("--changing", action="store_true",
                    help="also list combos unlocked by changing commanders")
    ap.add_argument("--json", metavar="PATH", help="dump raw API results to PATH")
    args = ap.parse_args()

    path = resolve_deck(args.deck)

    try:
        q = query_deck(path)
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as e:
        sys.exit(f"Commander Spellbook request failed: {e}\n(Network access is required; nothing was reported.)")
    identity, included, almost, changing = q["identity"], q["included"], q["almost"], q["changing"]
    deck_lower, meta, aliased = q["deck_lower"], q["meta"], q["aliased"]

    commanders, main, _ = parse_decklist(path)
    cmd_disp = ", ".join(name for _, name in commanders) or "(none resolved)"
    print(f"Deck: {meta['stem']}")
    print(f"Commander(s): {cmd_disp}   |   color identity: {identity or '?'}")
    print(f"Cards sent: {len(main)} main + {len(commanders)} commander")
    if not meta["registry_commander"]:
        print("  ! commander not in deck_registry — used Moxfield trailing-block fallback")
    if aliased:
        print("  reskin aliases applied: " + "; ".join(sorted(set(aliased))))

    print(f"\n=== COMPLETE COMBOS IN DECK ({len(included)}) ===")
    if included:
        for c in included:
            print(_fmt_combo(c))
    else:
        print("    (none)")

    if args.almost_max > 0:
        near = []
        for c in almost:
            missing = sum(1 for n in _uses(c) if n.lower() not in deck_lower)
            if missing <= args.almost_max:
                near.append((missing, c))
        near.sort(key=lambda mc: mc[0])
        print(f"\n=== ALMOST (missing <= {args.almost_max} card{'s' if args.almost_max != 1 else ''}) "
              f"-- buys that complete a combo ({len(near)}) ===")
        if near:
            for _, c in near:
                print(_fmt_combo(c, deck_lower))
        else:
            print("    (none)")

    if args.changing and changing:
        print(f"\n=== IF YOU CHANGED COMMANDERS ({len(changing)}) ===")
        for c in changing:
            print(_fmt_combo(c, deck_lower))

    if args.json:
        Path(args.json).write_text(json.dumps(
            {"identity": identity, "included": included, "almostIncluded": almost,
             "includedByChangingCommanders": changing}, indent=2), encoding="utf-8")
        print(f"\nRaw results written to {args.json}")


if __name__ == "__main__":
    main()
