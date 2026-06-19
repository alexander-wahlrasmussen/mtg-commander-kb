#!/usr/bin/env python3
"""kill_tree.py — render a deck's kill LINES as a Mermaid decision tree.

Backlog #4 (the fun one). The clock labs already enumerate each deck's kills as
cheapest-first branches; this draws them. A kill tree reads top-to-bottom as
"try the fastest available line; if its pieces aren't assembled, fall to the
next" — the decision a pilot actually makes. Pure visualization: a nice artifact
for a Summary or a primer, NOT another model.

Each deck is a small spec: a root (commander/engine online), an ordered list of
LINES (fastest/cheapest first — the order the lab checks them), an optional
always-on BACKGROUND clock (passive drains that tick regardless), and a STALL
leaf (what you're doing when no line is up yet). Lines carry the lab-measured
clock so the picture stays honest. Kinds colour the leaves:
  combo  — deterministic/loop kill        table  — all-opponent drain/poison
  combat — focus-fire one opponent (decap) enabler— tutor/reset that feeds a line

The kill text is taken from each deck's `*_clock_lab.py` KILL CHECKS + its
Summary (oracle-verified there); this file only re-draws them, it does not
re-derive card text. The specs themselves live in deck_registry (the single
source of truth). Output: Mermaid to stdout and to analysis/kill_trees/.
Validate/render the .mmd with the Mermaid Chart tool.

Usage
    python scripts/kill_tree.py radiation-sickness      # one deck
    python scripts/kill_tree.py --all                   # every encoded deck
    python scripts/kill_tree.py --list
"""
import argparse
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "analysis" / "kill_trees"

for _s in (sys.stdout, sys.stderr):            # the diagrams use →, ⏱, en-dashes
    if hasattr(_s, "reconfigure"):
        try:
            _s.reconfigure(encoding="utf-8", errors="replace")
        except (ValueError, OSError):
            pass

# The decision-tree specs (display-slug -> title/root/background/lines/stall/src, in render
# order) live in deck_registry, the single source of truth. spec line = (id, need?, kill,
# clock, kind); kind in {combo,table,combat,enabler}. This file only renders them.
_rspec = importlib.util.spec_from_file_location(
    "deck_registry", Path(__file__).parent / "deck_registry.py")
deck_registry = importlib.util.module_from_spec(_rspec)
_rspec.loader.exec_module(deck_registry)
DECKS = deck_registry.kill_trees()

# Every class sets an explicit text `color:` — without it the node text inherits
# the viewer's theme foreground, so on a DARK theme (e.g. gruvbox in Obsidian) the
# light pastel fills render light-text-on-light and wash out. Fills are deepened
# enough to read as distinct islands on a dark canvas yet stay light enough for
# near-black text; works on GitHub light/dark too. Accents are gruvbox-tinted.
STYLE = """    classDef root fill:#3c3836,color:#fbf1c7,stroke:#fabd2f,stroke-width:3px;
    classDef ask fill:#ebdbb2,color:#1d2021,stroke:#7c6f64,stroke-width:1.5px;
    classDef combo fill:#f5b8d6,color:#1d2021,stroke:#b16286,stroke-width:2px;
    classDef table fill:#aed1f0,color:#1d2021,stroke:#458588,stroke-width:2px;
    classDef combat fill:#fec07c,color:#1d2021,stroke:#d65d0e,stroke-width:2px;
    classDef enabler fill:#b8e6a0,color:#1d2021,stroke:#689d6e,stroke-width:2px;
    classDef bg fill:#cbe8b8,color:#1d2021,stroke:#689d6e,stroke-width:1.5px,stroke-dasharray:5 4;
    classDef stall fill:#d5c4a1,color:#3c3836,stroke:#928374,stroke-width:1.5px;"""


def mermaid(slug):
    d = DECKS[slug]
    L = ["flowchart TD", STYLE, "", f'    S(["{d["root"]}"]):::root']
    prev = "S"
    for i, (lid, need, kill, clock, kind) in enumerate(d["lines"], 1):
        ask, leaf = f"A{i}", f"K{i}"
        L.append(f'    {prev} --> {ask}{{"{need}"}}:::ask')
        L.append(f'    {ask} -- assembled --> {leaf}["<b>{kill}</b><br/>⏱ {clock}"]:::{kind}')
        prev = ask
    # the 'no' tail from the last decision -> stall
    L.append(f'    {prev} -- not yet --> STALL["{d["stall"]}"]:::stall')
    if d["background"]:
        need, kill, clock, kind = d["background"]
        L.append(f'    BG[["{need}"]]:::bg')
        L.append(f'    BG -. always on .-> KBG["<b>{kill}</b><br/>⏱ {clock}"]:::{kind}')
    return "\n".join(L)


def emit(slug):
    OUT.mkdir(parents=True, exist_ok=True)
    txt = mermaid(slug)
    path = OUT / f"{slug}-kill-tree.mmd"
    path.write_text(txt + "\n", encoding="utf-8")
    print(f"# {DECKS[slug]['title']}\n# source: {DECKS[slug]['src']}\n"
          f"# wrote {path.relative_to(ROOT)}\n")
    print(txt)
    print()


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("deck", nargs="?", help="deck slug (see --list)")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--list", action="store_true")
    args = ap.parse_args()
    if args.list:
        for s in DECKS:
            print(f"  {s}")
        return
    if args.all:
        for s in DECKS:
            emit(s)
    elif args.deck in DECKS:
        emit(args.deck)
    else:
        sys.exit(f"unknown deck {args.deck!r}; --list to see encoded decks")


if __name__ == "__main__":
    main()
