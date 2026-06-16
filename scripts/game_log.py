#!/usr/bin/env python3
"""game_log.py — record real pod-game outcomes (Layer 2 ground truth).

The whole simulation stack (the `*_clock_lab.py` suite, `pod_gauntlet.py`,
`self_meta_lab.py`) predicts how our decks perform. Every lab so far has
*falsified* a hand-estimate — but nothing has ever checked the LABS against
real games. This file is the capture end of that loop: a structured, append-only
record of actual pod results that a future `calibrate.py` (and the framework
bake-off's outcome oracle) can back-test against.

What it feeds, and the lab it validates:
    win_turn          -> the TABLE clock (winner closed all seats)      vs *_clock_lab table median
    first_decap_turn  -> the DECAP clock (first player knocked out)     vs *_clock_lab decap median
    per-deck win rate -> P(beat the pod)                                vs pod_gauntlet / self_meta
    disruption[]      -> answer availability on the kill turn           vs delay_lab / lock_lab

Ground truth = `analysis/game_results.jsonl` (one JSON object per line,
APPEND-ONLY — never rewrite history; the dated records ARE the log). Committed,
not generated — unlike sim_results.json this is hand-entered and must be tracked.

Record schema (one line of game_results.jsonl):
    {
      "date": "2026-06-16",            # ISO date the game was played
      "mine": "genome_project",        # MY deck this game (a slug from DECKS)
      "pod": [                         # every seat, including mine
        {"deck": "genome_project", "pilot": "me",  "result": "win",  "ko_turn": null},
        {"deck": "ur_dragon",      "pilot": "Sam", "result": "loss", "ko_turn": 9,
         "archetype": "board/eminence"}
      ],
      "winner": "genome_project",      # which deck won
      "win_turn": 9,                   # turn the game ENDED (table clock if won by closing out)
      "win_type": "combo",             # combo | combat-decap | table-drain | concede | other
      "first_decap_turn": 8,           # turn the FIRST seat was knocked out (decap clock)
      "disruption": [                  # events that mattered to a kill turn
        {"turn": 6, "type": "counter",   "by": "Sam", "target": "Genome Project"},
        {"turn": 7, "type": "abolisher", "by": "Mia"}
      ],
      "notes": "Mulligan to 6; Abolisher walled my counters, raced under it."
    }

Usage
    # rich path — write the record as JSON and pipe it in (recommended for real games)
    python scripts/game_log.py add --from-json game.json
    cat game.json | python scripts/game_log.py add --from-json -

    # quick path — flags (repeat --seat / --event)
    python scripts/game_log.py add --date 2026-06-16 --mine genome_project \\
        --winner genome_project --win-turn 9 --win-type combo --first-decap-turn 8 \\
        --seat "genome_project,me,win," --seat "ur_dragon,Sam,loss,9" \\
        --event "7,abolisher,Mia," --notes "Raced under Abolisher."

    python scripts/game_log.py list                 # compact log
    python scripts/game_log.py summary              # per-deck W/L, avg clocks (the proto-oracle)
    python scripts/game_log.py validate             # schema-check every record
"""
import argparse
import json
import sys
from datetime import date as _date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOG = ROOT / "analysis" / "game_results.jsonl"

for _s in (sys.stdout, sys.stderr):               # safe echo of arbitrary notes
    if hasattr(_s, "reconfigure"):
        try:
            _s.reconfigure(encoding="utf-8", errors="replace")
        except (ValueError, OSError):
            pass

# Canonical active-roster slugs — kept identical to clock_check.py / pod_gauntlet
# so `mine`/`winner`/seat decks map straight onto the labs for back-testing.
# Opponents' decks may use any slug (they have no lab); only `mine` is checked.
DECKS = {
    "genome_project", "radiation_sickness", "replication_crisis", "lorehold_spirits",
    "earthbend_the_meta", "exiles_return", "zero_sum_game", "curse_of_the_scarab",
    "bumbleflower", "eldrazi_stampede", "dark_lords_army", "diminishing_returns",
    "lightning_war", "grand_design", "crystal_sickness", "calamity_tax",
}
WIN_TYPES = {"combo", "combat-decap", "table-drain", "concede", "other"}


# --------------------------------------------------------------------------- IO
def read_log():
    """Yield (lineno, record) for every non-blank line; raise on bad JSON."""
    if not LOG.exists():
        return
    for i, line in enumerate(LOG.read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        try:
            yield i, json.loads(line)
        except json.JSONDecodeError as e:
            sys.exit(f"game_results.jsonl line {i}: invalid JSON — {e}")


def append(record):
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


# ------------------------------------------------------------------ validation
def problems(rec):
    """Return a list of human-readable issues with one record (empty == clean)."""
    out = []
    for field in ("date", "mine", "pod", "winner", "win_turn"):
        if field not in rec:
            out.append(f"missing required field '{field}'")
    if "mine" in rec and rec["mine"] not in DECKS:
        out.append(f"'mine' = {rec['mine']!r} is not an active-roster slug "
                   f"(can't back-test against a lab)")
    if rec.get("win_type") and rec["win_type"] not in WIN_TYPES:
        out.append(f"win_type {rec['win_type']!r} not in {sorted(WIN_TYPES)}")
    pod = rec.get("pod")
    if isinstance(pod, list):
        if not pod:
            out.append("pod is empty")
        if "mine" in rec and not any(s.get("deck") == rec["mine"] for s in pod):
            out.append(f"'mine' deck {rec['mine']!r} is not a seat in the pod")
        winners = [s for s in pod if s.get("result") == "win"]
        if len(winners) > 1:
            out.append("more than one seat marked result='win'")
    elif pod is not None:
        out.append("pod must be a list of seats")
    return out


# -------------------------------------------------------------- flag → record
def parse_seat(spec):
    """'deck,pilot,result,ko_turn' -> seat dict (trailing fields optional)."""
    parts = [p.strip() for p in spec.split(",")]
    parts += [""] * (4 - len(parts))
    deck, pilot, result, ko = parts[:4]
    seat = {"deck": deck, "pilot": pilot or None, "result": result or None}
    seat["ko_turn"] = int(ko) if ko else None
    return seat


def parse_event(spec):
    """'turn,type,by,target' -> disruption dict (target optional)."""
    parts = [p.strip() for p in spec.split(",")]
    parts += [""] * (4 - len(parts))
    turn, typ, by, target = parts[:4]
    ev = {"turn": int(turn) if turn else None, "type": typ or None, "by": by or None}
    if target:
        ev["target"] = target
    return ev


def record_from_args(a):
    rec = {
        "date": a.date or _date.today().isoformat(),
        "mine": a.mine,
        "pod": [parse_seat(s) for s in (a.seat or [])],
        "winner": a.winner,
        "win_turn": a.win_turn,
        "win_type": a.win_type,
        "first_decap_turn": a.first_decap_turn,
        "disruption": [parse_event(e) for e in (a.event or [])],
        "notes": a.notes or "",
    }
    return {k: v for k, v in rec.items() if v not in (None, [], "")}


# --------------------------------------------------------------------- commands
def cmd_add(a):
    if a.from_json:
        raw = sys.stdin.read() if a.from_json == "-" else Path(a.from_json).read_text(encoding="utf-8")
        rec = json.loads(raw)
        rec.setdefault("date", _date.today().isoformat())
    else:
        rec = record_from_args(a)

    issues = problems(rec)
    if issues:
        print("Refusing to add — record has problems:", file=sys.stderr)
        for p in issues:
            print(f"  - {p}", file=sys.stderr)
        sys.exit(1)

    print(json.dumps(rec, ensure_ascii=False, indent=2))
    if a.dry_run:
        print("\n(dry run — not written)")
        return
    append(rec)
    print(f"\nAppended to {LOG.relative_to(ROOT)} "
          f"({sum(1 for _ in read_log())} games on record).")


def cmd_list(_a):
    rows = list(read_log())
    if not rows:
        print("No games logged yet.")
        return
    for _, r in rows:
        won = r.get("winner") == r.get("mine")
        flag = "W" if won else "L"
        print(f"{r.get('date','?'):<11} [{flag}] {r.get('mine','?'):<20} "
              f"win:{r.get('winner','?'):<20} T{r.get('win_turn','?')} "
              f"decapT{r.get('first_decap_turn','-')} {r.get('win_type','')}")
    print(f"\n{len(rows)} games.")


def _mean(xs):
    xs = [x for x in xs if isinstance(x, (int, float))]
    return round(sum(xs) / len(xs), 1) if xs else None


def cmd_summary(_a):
    """Per-deck record from MY point of view — the Layer-2 oracle in miniature."""
    rows = [r for _, r in read_log()]
    if not rows:
        print("No games logged yet — nothing to summarise.")
        return
    decks = {}
    for r in rows:
        d = decks.setdefault(r.get("mine", "?"), {"g": 0, "w": 0, "wt": [], "dt": []})
        d["g"] += 1
        if r.get("winner") == r.get("mine"):
            d["w"] += 1
            d["wt"].append(r.get("win_turn"))
        d["dt"].append(r.get("first_decap_turn"))

    print(f"{'deck':<22}{'G':>3}{'W':>3}{'win%':>6}{'avg win T':>11}{'avg decap T':>13}")
    print("-" * 58)
    for deck in sorted(decks, key=lambda k: -decks[k]["w"] / max(decks[k]["g"], 1)):
        d = decks[deck]
        wr = f"{100*d['w']/d['g']:.0f}%"
        print(f"{deck:<22}{d['g']:>3}{d['w']:>3}{wr:>6}"
              f"{str(_mean(d['wt'])):>11}{str(_mean(d['dt'])):>13}")
    print(f"\n{len(rows)} games across {len(decks)} of my decks. "
          f"Compare these to the lab clocks (clock_check) and pod_gauntlet P(win).")


def cmd_validate(_a):
    rows = list(read_log())
    if not rows:
        print("No games logged yet.")
        return
    bad = 0
    for lineno, r in rows:
        issues = problems(r)
        if issues:
            bad += 1
            print(f"line {lineno} ({r.get('date','?')} / {r.get('mine','?')}):")
            for p in issues:
                print(f"  - {p}")
    if bad:
        print(f"\n{bad}/{len(rows)} records have problems.")
        sys.exit(1)
    print(f"All {len(rows)} records valid.")


# ------------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0],
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    add = sub.add_parser("add", help="append one game (—from-json, or quick flags)")
    add.add_argument("--from-json", metavar="PATH",
                     help="load a full record from a JSON file, or '-' for stdin")
    add.add_argument("--date", help="ISO date (default: today)")
    add.add_argument("--mine", help="my deck slug this game")
    add.add_argument("--winner", help="winning deck slug")
    add.add_argument("--win-turn", type=int, help="turn the game ended")
    add.add_argument("--win-type", choices=sorted(WIN_TYPES), help="how it ended")
    add.add_argument("--first-decap-turn", type=int, help="turn first seat was KO'd")
    add.add_argument("--seat", action="append", metavar="deck,pilot,result,ko_turn",
                     help="a pod seat (repeatable)")
    add.add_argument("--event", action="append", metavar="turn,type,by,target",
                     help="a disruption event (repeatable)")
    add.add_argument("--notes", help="free text")
    add.add_argument("--dry-run", action="store_true", help="print the record, don't write")
    add.set_defaults(func=cmd_add)

    sub.add_parser("list", help="compact list of logged games").set_defaults(func=cmd_list)
    sub.add_parser("summary", help="per-deck W/L + avg clocks (proto-oracle)").set_defaults(func=cmd_summary)
    sub.add_parser("validate", help="schema-check every record").set_defaults(func=cmd_validate)

    a = ap.parse_args()
    a.func(a)


if __name__ == "__main__":
    main()
