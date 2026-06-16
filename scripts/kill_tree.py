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
re-derive card text. Output: Mermaid to stdout and to analysis/kill_trees/.
Validate/render the .mmd with the Mermaid Chart tool.

Usage
    python scripts/kill_tree.py radiation-sickness      # one deck
    python scripts/kill_tree.py --all                   # every encoded deck
    python scripts/kill_tree.py --list
"""
import argparse
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

# spec: line = (id, need?, kill, clock, kind). kind in {combo,table,combat,enabler}
DECKS = {
    "radiation-sickness": {
        "title": "Radiation Sickness — The Wise Mothman",
        "root": "The Wise Mothman resolved<br/>rad counters tick every opponent's main phase",
        "background": ("rad counters + proliferate<br/>(Vorinclex / Tekuthal / Inexorable Tide)",
                       "all-opponent rad drain", "table ~T10", "table"),
        "lines": [
            ("combo", "Mindcrank + Bloodchief Ascension<br/>(3 quest counters live)",
             "infinite mill → drain loop", "table T7", "combo"),
            ("simic", "Simic Ascendancy reaches<br/>20 growth counters",
             "win at your upkeep", "table T8–9", "combo"),
            ("triumph", "Triumph of the Hordes<br/>+ a wide creature board",
             "+1/+1, trample & INFECT → 10 poison", "table T8", "table"),
            ("combat", "counter-grown creatures connect<br/>(fallback)",
             "focus one opponent", "decap T7", "combat"),
        ],
        "stall": "keep ticking rad + stacking counters —<br/>the passive drain closes ~T10",
        "src": "rs_clock_lab.py + Radiation_Sickness_Summary.md",
    },
    "diminishing-returns": {
        "title": "Diminishing Returns — Teysa Karlov",
        "root": "Teysa Karlov online<br/>every death trigger fires TWICE",
        "background": None,
        "lines": [
            ("loop", "Gravecrawler + Phyrexian Altar<br/>+ a sac outlet",
             "infinite deaths → drain (deterministic)", "table T9+", "combo"),
            ("gary", "Gray Merchant of Asphodel<br/>+ heavy black devotion",
             "ETB drain ×2", "table", "table"),
            ("kokusho", "Kokusho, the Evening Star<br/>+ a sac outlet",
             "5-drain ×2 each death cycle", "table", "table"),
            ("living", "Living Death<br/>(mass reanimation)",
             "refill board → re-fire every death", "reset → table", "table"),
            ("razaketh", "Razaketh, the Foulblooded<br/>+ fodder to sacrifice",
             "tutor the missing piece of any line", "enabler", "enabler"),
            ("combat", "wide token board swings<br/>(fallback)",
             "focus one opponent", "decap T9", "combat"),
        ],
        "stall": "grind deaths — the table drain is slow (T12+);<br/>this deck disrupts, it doesn't race",
        "src": "dr_clock_lab.py + Diminishing_Returns_Summary.md",
    },
    "genome-project": {
        "title": "The Genome Project — Kuja, Genome Sorcerer",
        "root": "Kuja resolved — Wizard tokens ping EVERY opponent on each noncreature cast<br/>transforms to Trance Kuja (×2 ALL Wizard damage) at 4 Wizards",
        # No passive lane: pings require CASTS, so decap and table converge (T7/T8)
        # off the same ping clock rather than diverging like the combat decks.
        "background": None,
        "lines": [
            ("oneshot", "Trance Kuja + City on Fire (×3 all dmg)<br/>and/or Harmonic Prodigy / Roaming Throne",
             "12–16+ damage per opponent per spell → one or two casts kill the table", "table T7", "combo"),
            ("storm", "Trance Kuja + 4 Wizard tokens<br/>(Birgi / Storm-Kiln refund the mana)",
             "8 dmg per opponent per noncreature cast → ~5 cheap casts", "table T8", "table"),
            ("gystorm", "stocked graveyard + Mizzix's Mastery<br/>(Dawn Warriors' Legacy) or Underworld Breach",
             "recast every i/s from the yard — each a REAL cast = full pings", "table T7–8", "combo"),
            ("backup", "mana flood (Mana Geyser / Neheb / Jeska's Will)<br/>or 50 life via Aetherflux Reservoir",
             "board-independent table drain / 50-life laser", "table (backup)", "table"),
            ("combat", "Trance Kuja + a Wizard board<br/>(Trance doubles Wizard power) (fallback)",
             "focus one opponent", "decap T7", "combat"),
        ],
        "stall": "build Wizards toward the 4-count transform & stock the yard —<br/>pings need CASTS (no passive drain), so dig for a multiplier + a cheap chain",
        "src": "gp_clock_lab.py + The_Genome_Project_Summary.md",
    },
    "replication-crisis": {
        "title": "The Replication Crisis — Satya, Aetherflux Genius",
        "root": "Satya attacking — each attack makes a free token COPY of a nontoken<br/>creature you control + {E}{E} · EVERY line needs Satya to ATTACK (fires on attack, not on connect)",
        # Combat-gated, so the clock DIVERGES: decap T7 (focus one) / table T10+.
        "background": None,
        "lines": [
            ("infinite", "Sword of Feast and Famine on Satya<br/>+ Aggravated Assault",
             "combat untaps all lands → infinite combats → infinite tokens + ETBs", "decap T6–7", "combo"),
            ("brudiclad", "Brudiclad + a token pile<br/>+ a fat Satya copy (Inferno Titan)",
             "convert every token into the bomb → lethal alpha (no infinite needed)", "decap T7", "combat"),
            ("adeline", "Adeline + Anointed Procession",
             "~6 humans per attack + doubled Satya token → wide alpha swing", "decap T7–8", "combat"),
            ("conscripts", "Satya copies Zealous Conscripts<br/>(+ Strionic Resonator / Aggravated Assault)",
             "steal the pod's best permanents, one per combat", "disrupt → decap", "enabler"),
            ("grind", "repeated ETB copies (Inferno Titan ping,<br/>Cloudblazer draw, Skyclave exile) (fallback)",
             "grind the pod out over 3–4 combats", "table T10+", "table"),
        ],
        "stall": "Satya must survive as a 3/5 through combat — protect her<br/>(Greaves / Boots / Slip Out the Back) and hold for a safe swing",
        "src": "rc_speed_lab.py + The_Replication_Crisis_Summary.md",
    },
}

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
