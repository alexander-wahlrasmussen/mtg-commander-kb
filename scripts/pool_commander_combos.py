#!/usr/bin/env python3
"""pool_commander_combos.py — for a candidate commander, ask Commander Spellbook
which COMPLETE combos are already assemblable from the OWNED pool.

For each commander name given, we:
  1. resolve its color identity from oracle-cards.json,
  2. take every owned card whose color identity is a subset of the commander's
     (the legal card pool for that commander), capped at 499 nonland cards
     (CSB's find-my-combos rejects larger bodies),
  3. POST {commanders:[cmd], main:[pool]} to CSB find-my-combos,
  4. report complete combos, flagging those that USE the commander.

This is a discovery tool for "what could I build" — NOT a rules engine. It only
knows what CSB's curated DB knows, keyed on card names. Verify card text with
card_lookup before acting on anything it surfaces.

Usage:
    python scripts/pool_commander_combos.py "Niv-Mizzet, Parun" "Selvala, Heart of the Wilds"
"""
import csv, json, sys, urllib.request
from pathlib import Path

ROOT = Path(__file__).parent.parent
CSV = ROOT / "collection" / "moxfield_haves_2026-07-11-0716Z.csv"
ORACLE = ROOT / "collection" / "oracle-cards.json"
API = "https://backend.commanderspellbook.com/find-my-combos?limit=500"

def owned_names():
    out = {}
    with open(CSV, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            n = r["Name"].strip()
            out[n] = out.get(n, 0) + int(r["Count"] or 1)
    return out

def load_oracle():
    data = json.load(open(ORACLE, encoding="utf-8"))
    by = {}
    for c in data:
        by[c["name"].lower()] = c
        if "//" in c["name"]:
            by.setdefault(c["name"].split("//")[0].strip().lower(), c)
    return by

def post(commander, pool):
    payload = {"commanders": [{"card": commander, "quantity": 1}],
               "main": [{"card": n, "quantity": 1} for n in pool]}
    req = urllib.request.Request(API, data=json.dumps(payload).encode(),
        method="POST", headers={"Content-Type": "application/json", "User-Agent": "pool-combo"})
    with urllib.request.urlopen(req, timeout=90) as r:
        return json.loads(r.read()).get("results", {})

def main():
    owned = owned_names()
    oracle = load_oracle()
    for cmd in sys.argv[1:]:
        c = oracle.get(cmd.lower())
        if not c:
            print(f"\n### {cmd}: NOT FOUND in oracle\n"); continue
        ci = set(c.get("color_identity", []))
        # owned cards whose CI is subset of commander CI; exclude the commander itself
        pool, lands = [], 0
        for n in owned:
            oc = oracle.get(n.lower())
            if not oc or n.lower() == cmd.lower():
                continue
            if not set(oc.get("color_identity", [])) <= ci:
                continue
            if "Land" in oc.get("type_line", "") and "Creature" not in oc.get("type_line", ""):
                lands += 1
                continue  # drop pure lands to stay under the 499 cap; combos rarely need basics
            pool.append(n)
        pool = pool[:499]
        try:
            res = post(cmd, pool)
        except Exception as e:
            print(f"\n### {cmd} [{''.join(sorted(ci)) or 'C'}]: CSB ERROR {e}\n"); continue
        inc = res.get("included", [])
        cmdl = cmd.lower()
        uses_cmd = [k for k in inc if any(u["card"]["name"].lower() == cmdl for u in k.get("uses", []))]
        print(f"\n### {cmd}  [{''.join(sorted(ci)) or 'C'}]  pool={len(pool)} (+{lands} lands dropped)")
        print(f"    complete combos in pool: {len(inc)}   | using the commander: {len(uses_cmd)}")
        for k in uses_cmd:
            feats = ", ".join(p["feature"]["name"] for p in k.get("produces", [])) or "(see page)"
            parts = " + ".join(u["card"]["name"] for u in k.get("uses", []))
            print(f"      * {feats}\n          {parts}")

if __name__ == "__main__":
    main()
