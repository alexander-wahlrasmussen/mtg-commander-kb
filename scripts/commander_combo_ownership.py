#!/usr/bin/env python3
"""commander_combo_ownership.py — for candidate commanders, pull EVERY combo that
uses that card from Commander Spellbook and score it against the OWNED pool.

Unlike pool_commander_combos.py (which POSTs a capped 499-card body and can miss
pieces to truncation), this queries CSB's variants endpoint keyed on the commander
card itself, so it sees ALL published combos the commander anchors — then checks
which of the *other* pieces you already own.

Per commander it reports:
  - OWNED   : every non-commander piece is in the collection (buildable today)
  - 1-AWAY  : missing exactly one card (the actionable buy)
sorted by CSB popularity (deck count). Reskin names are resolved both directions
so owned UB printings match CSB's real names.

This is discovery, not rules adjudication. card_lookup every piece before acting.

Usage:
    python scripts/commander_combo_ownership.py "K'rrik, Son of Yawgmoth" "Prosper, Tome-Bound"
"""
import csv, json, sys, urllib.request, urllib.parse, importlib.util as il
from pathlib import Path

ROOT = Path(__file__).parent.parent
CSV = ROOT / "collection" / "moxfield_haves_2026-07-11-0716Z.csv"
BASE = "https://backend.commanderspellbook.com/variants/"

def load_owned():
    spec = il.spec_from_file_location("deck_sim", ROOT / "scripts" / "deck_sim.py")
    m = il.module_from_spec(spec); spec.loader.exec_module(m)
    aliases = m.load_reskin_aliases()  # reskin_lower -> real
    owned = set()
    with open(CSV, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            n = r["Name"].strip().lower()
            owned.add(n)
            if n in aliases:
                owned.add(aliases[n].lower())        # own reskin -> count real name
            if " // " in n:
                owned.add(n.split(" // ")[0].strip())
    return owned

def fetch_variants(card):
    q = f'card:"{card}"'
    url = BASE + "?" + urllib.parse.urlencode({"q": q, "limit": 100})
    out = []
    while url:
        req = urllib.request.Request(url, headers={"User-Agent": "combo-own"})
        with urllib.request.urlopen(req, timeout=60) as r:
            d = json.loads(r.read())
        out += d.get("results", [])
        url = d.get("next")
    return out

def _front(name):
    """Front face of a DFC/split name, lowercased — CSB stores full 'A // B' names,
    so a query for the front face must still match (Sephiroth bug, 2026-07-12)."""
    return name.split(" // ")[0].strip().lower()


def main():
    owned = load_owned()
    for cmd in sys.argv[1:]:
        cl = _front(cmd)
        try:
            variants = fetch_variants(cmd)
        except Exception as e:
            print(f"\n### {cmd}: CSB ERROR {e}"); continue
        # only combos legal to run with this commander (identity subset handled by CSB legality flag)
        rows = []
        for v in variants:
            uses = [u["card"]["name"] for u in v.get("uses", [])]
            if not any(_front(u) == cl for u in uses):
                continue
            others = [u for u in uses if _front(u) != cl]
            missing = [u for u in others if u.lower() not in owned]
            if len(missing) <= 1 and v.get("legalities", {}).get("commander") is not False:
                rows.append((len(missing), -(v.get("popularity") or 0), others, missing,
                             [p["feature"]["name"] for p in v.get("produces", [])],
                             v.get("popularity") or 0, v.get("bracketTag")))
        rows.sort(key=lambda x: (x[0], x[1]))
        owned_n = sum(1 for r in rows if r[0] == 0)
        away_n = sum(1 for r in rows if r[0] == 1)
        print(f"\n### {cmd}  — {owned_n} OWNED combos, {away_n} one-away  (of {len(variants)} total using it)")
        for miss, _, others, missing, feats, pop, brk in rows[:12]:
            tag = "OWNED " if miss == 0 else f"BUY:{missing[0]}"
            f = ", ".join(feats)[:70]
            print(f"    [{tag:>22}] pop={pop:>4} {brk or ''} :: {' + '.join(others)}  => {f}")

if __name__ == "__main__":
    main()
