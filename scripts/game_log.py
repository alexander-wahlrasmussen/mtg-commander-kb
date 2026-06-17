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
    # frictionless path — answer prompts, nothing to remember (recommended after a game)
    python scripts/game_log.py log
    python scripts/game_log.py log --dry-run        # walk the prompts, write nothing

    # rich path — write the record as JSON and pipe it in
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


# ---------------------------------------------------------- interactive logging
# A guided front-door so a real game can be recorded without recalling the
# --seat/--event comma syntax or the exact roster slugs. Per-field validation
# keeps the assembled record clean by construction; it still runs problems()
# before writing. Pipe a transcript on stdin to script it; --dry-run never writes.
def _input(prompt):
    try:
        return input(prompt)
    except (EOFError, KeyboardInterrupt):
        print("\nAborted — nothing written.")
        sys.exit(1)


def ask(prompt, default=None):
    suffix = f" [{default}]" if default not in (None, "") else ""
    val = _input(f"{prompt}{suffix}: ").strip()
    if val:
        return val
    return default if default is not None else ""


def ask_int(prompt, optional=True, default=None):
    suffix = f" [{default}]" if default is not None else (" [blank=skip]" if optional else "")
    while True:
        raw = _input(f"{prompt}{suffix}: ").strip()
        if raw == "":
            if default is not None:
                return default
            if optional:
                return None
            print("  (required — enter a number)")
            continue
        try:
            return int(raw)
        except ValueError:
            print(f"  '{raw}' isn't a whole number — try again.")


def ask_yesno(prompt, default=False):
    hint = "Y/n" if default else "y/N"
    while True:
        raw = _input(f"{prompt} [{hint}]: ").strip().lower()
        if raw == "":
            return default
        if raw in ("y", "yes"):
            return True
        if raw in ("n", "no"):
            return False
        print("  please answer y or n.")


def ask_choice(prompt, choices, default=None):
    choices = list(choices)
    while True:
        raw = ask(f"{prompt} ({'/'.join(choices)})", default)
        if raw in choices:
            return raw
        hits = [c for c in choices if c.startswith(raw)] if raw else []
        if len(hits) == 1:
            return hits[0]
        print(f"  pick one of: {', '.join(choices)}")


def _norm_slug(raw):
    return raw.strip().lower().replace(" ", "_").replace("-", "_")


def ask_my_deck():
    print("  your active decks: " + ", ".join(sorted(DECKS)))
    while True:
        key = _norm_slug(ask("Your deck this game"))
        if key in DECKS:
            return key
        hits = sorted(d for d in DECKS if key and (d.startswith(key) or key in d))
        if len(hits) == 1:
            return hits[0]
        if hits:
            print(f"  ambiguous — matches: {', '.join(hits)}")
        else:
            print("  no match — it must be one of your active decks (back-tested against a lab).")


def cmd_log(a):
    print("Log a pod game — Enter accepts the [default]; Ctrl-C aborts.\n")
    date = ask("Date played", _date.today().isoformat())
    mine = ask_my_deck()

    i_won = ask_yesno("Did you win?", default=False)
    my_seat = {"deck": mine, "pilot": "me", "result": "win" if i_won else "loss"}
    if not i_won:
        ko = ask_int("  what turn were you knocked out?")
        if ko is not None:
            my_seat["ko_turn"] = ko
    pod = [my_seat]

    print("\nOpponents — one seat at a time; blank deck name to finish.")
    while True:
        deck = ask("  opponent deck (blank = done)")
        if not deck:
            break
        seat = {"deck": _norm_slug(deck)}
        pilot = ask("    pilot name")
        if pilot:
            seat["pilot"] = pilot
        seat["result"] = ask_choice("    result", ["win", "loss", "draw"],
                                     default="loss" if i_won else None)
        ko = ask_int("    KO turn")
        if ko is not None:
            seat["ko_turn"] = ko
        arch = ask("    archetype (optional, e.g. board/eminence)")
        if arch:
            seat["archetype"] = arch
        pod.append(seat)

    win_seats = [s for s in pod if s.get("result") == "win"]
    if i_won:
        winner = mine
    elif len(win_seats) == 1:
        winner = win_seats[0]["deck"]
    else:
        winner = _norm_slug(ask("Winning deck slug"))

    win_turn = ask_int("Turn the game ENDED (table clock)", optional=False)
    win_type = ask_choice("How did it end?", sorted(WIN_TYPES))
    decap = ask_int("Turn the FIRST player was knocked out (decap clock)")

    disruption = []
    if ask_yesno("\nLog disruption events (counters, Abolisher, key removal)?", default=False):
        print("  enter each as  turn,type,by[,target]  — blank to finish.")
        while True:
            raw = ask("  event")
            if not raw:
                break
            disruption.append(parse_event(raw))

    notes = ask("\nNotes (free text)")

    rec = {
        "date": date, "mine": mine, "pod": pod, "winner": winner,
        "win_turn": win_turn, "win_type": win_type,
        "first_decap_turn": decap, "disruption": disruption, "notes": notes,
    }
    rec = {k: v for k, v in rec.items() if v not in (None, [], "")}

    issues = problems(rec)
    print("\n" + json.dumps(rec, ensure_ascii=False, indent=2))
    if issues:
        print("\nThis record still has problems:", file=sys.stderr)
        for p in issues:
            print(f"  - {p}", file=sys.stderr)
    if a.dry_run:
        print("\n(dry run — not written)")
        return
    prompt = "Append anyway?" if issues else "\nAppend this game?"
    if not ask_yesno(prompt, default=not issues):
        print("Not written.")
        return
    append(rec)
    print(f"\nAppended to {LOG.relative_to(ROOT)} ({sum(1 for _ in read_log())} games on record).")
    print("Next: `python scripts/game_log.py summary` — your real results vs the lab clocks.")


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

    lg = sub.add_parser("log", help="guided interactive entry (no flags to remember)")
    lg.add_argument("--dry-run", action="store_true", help="walk the prompts, write nothing")
    lg.set_defaults(func=cmd_log)

    sub.add_parser("list", help="compact list of logged games").set_defaults(func=cmd_list)
    sub.add_parser("summary", help="per-deck W/L + avg clocks (proto-oracle)").set_defaults(func=cmd_summary)
    sub.add_parser("validate", help="schema-check every record").set_defaults(func=cmd_validate)

    a = ap.parse_args()
    a.func(a)


if __name__ == "__main__":
    main()
