#!/usr/bin/env python3
"""game_log.py — record real pod-game outcomes (Layer 2 ground truth).

The whole simulation stack (the `*_clock_lab.py` suite, `pod_gauntlet.py`,
`self_meta_lab.py`) predicts how our decks perform. Every lab so far has
*falsified* a hand-estimate — but nothing has ever checked the LABS against
real games. This file is the capture end of that loop: a structured, append-only
record of actual pod results that `calibrate.py` (the grading end, shipped
2026-06-28) and the framework bake-off's outcome oracle back-test against.

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
    # fastest path — one line, typed straight from a scorecard (non-interactive)
    python scripts/game_log.py quick "genome W T9 d8 combo | ur_dragon L | kinnan L"
    python scripts/game_log.py quick "grand_design L T11 d9 | ur_dragon W"   # I lost
    #   <mydeck> W|L T<end> [d<decap>] [wintype]  |  <opp> [W|L]  ...  # notes
    #   W/L = did you win · T<n> = turn the game ENDED · d<n> = first decap turn

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
import re
import sys
from datetime import date as _date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOG = ROOT / "analysis" / "game_results.jsonl"
CLOCKS = ROOT / "analysis" / "pod_gauntlet_clocks.json"  # harvested lab medians (grade card)

for _s in (sys.stdout, sys.stderr):               # safe echo of arbitrary notes
    if hasattr(_s, "reconfigure"):
        try:
            _s.reconfigure(encoding="utf-8", errors="replace")
        except (ValueError, OSError):
            pass

# Canonical active-roster slugs — DERIVED from deck_registry (the single source of
# truth, shared with framework_bakeoff/clock_check) so `mine`/`winner`/seat decks
# map straight onto the labs for back-testing and can never drift behind a deck
# rename (the old hand-maintained literal silently went stale on Calamity->Croak).
# Opponents' decks may use any slug (they have no lab); only `mine` is checked.
sys.path.insert(0, str(Path(__file__).resolve().parent))
import deck_registry  # noqa: E402

DECKS = set(deck_registry.fb_decks())
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
    already = sum(1 for _, r in read_log() if r.get("mine") == rec.get("mine"))
    if a.dry_run:
        print("\n(dry run — not written)")
        print_grade_card(rec, already + 1)
        return
    append(rec)
    print(f"\nAppended to {LOG.relative_to(ROOT)} "
          f"({sum(1 for _ in read_log())} games on record).")
    print_grade_card(rec, already + 1)


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


def resolve_slug(raw, decks):
    """(slug|None, hits): exact match wins; else a UNIQUE prefix/substring match resolves,
    an ambiguous or empty match returns (None, hits) so callers can guide. Shared by the
    interactive prompt and the `quick` parser so both accept 'genome' for genome_project."""
    key = _norm_slug(raw)
    if key in decks:
        return key, [key]
    hits = sorted(d for d in decks if key and (d.startswith(key) or key in d))
    return (hits[0] if len(hits) == 1 else None), hits


def ask_my_deck():
    print("  your active decks: " + ", ".join(sorted(DECKS)))
    while True:
        slug, hits = resolve_slug(ask("Your deck this game"), DECKS)
        if slug:
            return slug
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
    already = sum(1 for _, r in read_log() if r.get("mine") == rec.get("mine"))
    append(rec)
    print(f"\nAppended to {LOG.relative_to(ROOT)} ({sum(1 for _ in read_log())} games on record).")
    print_grade_card(rec, already + 1)
    print("\nNext: `python scripts/game_log.py summary` — your real results vs the lab clocks.")


# -------------------------------------------------------- instant grade card
# The payoff that turns "armed but ungraded" into a habit: after a game lands, grade it
# against the lab clock it exists to validate — from game ONE, not after calibrate.py's
# n>=3 floor. Reads only the small committed medians JSON (no card bulk), so it's cheap.
def _parse_med(s):
    """'T7'->(7.0,False); '>T14'->(14.0,True); None->(None,False). Mirrors calibrate.parse_med
    (a parity test pins them equal) so the grade card doesn't hard-import the Layer-C grader
    just to read two medians — degrade-gracefully over DRY for a 4-line parse."""
    if s is None:
        return None, False
    s = str(s).strip()
    opened = s.startswith((">", "<", "≥", "≤"))
    digits = "".join(ch for ch in s if ch.isdigit())
    return (float(digits) if digits else None), opened


def load_clock_medians(path=CLOCKS):
    """slug -> {'name', 'decap': (turn, open), 'table': (turn, open)} from the committed
    harvested clocks JSON. Returns {} if the file is missing so the grade card degrades to a
    soft note instead of erroring."""
    p = Path(path)
    if not p.exists():
        return {}
    raw = json.loads(p.read_text(encoding="utf-8"))
    out = {}
    for slug, rec in raw.items():
        if not isinstance(rec, dict):
            continue
        med = rec.get("med") or [None, None]
        out[slug] = {
            "name": rec.get("name", slug),
            "decap": _parse_med(med[0] if len(med) > 0 else None),
            "table": _parse_med(med[1] if len(med) > 1 else None),
        }
    return out


def grade_game(rec, medians):
    """Grade ONE record's observed clocks against the lab medians for rec['mine'] (pure).
    Returns None if the deck has no lab clock, else {'deck','name','table','decap'} where each
    clock is {'obs','lab','open','delta'} | None. delta = observed - lab (calibrate's sign:
    +ve = I was SLOWER than the lab predicted; -ve = I closed FASTER than the lab said).
    table is graded only when MY deck actually closed the game; decap whenever it's recorded."""
    lab = medians.get(rec.get("mine"))
    if not lab:
        return None
    out = {"deck": rec.get("mine"), "name": lab["name"], "table": None, "decap": None}
    if rec.get("winner") == rec.get("mine") and isinstance(rec.get("win_turn"), (int, float)):
        lt, lo = lab["table"]
        out["table"] = {"obs": rec["win_turn"], "lab": lt, "open": lo,
                        "delta": (rec["win_turn"] - lt) if lt is not None else None}
    dec = rec.get("first_decap_turn")
    if isinstance(dec, (int, float)):
        ld, lo = lab["decap"]
        out["decap"] = {"obs": dec, "lab": ld, "open": lo,
                        "delta": (dec - ld) if ld is not None else None}
    return out


def _delta_phrase(delta, open_med=False):
    """Plain-English read of one signed clock error (obs - lab)."""
    if delta is None:
        return "no lab median to compare"
    tag = " (lab median is open, so this is a bound)" if open_med else ""
    if delta == 0:
        return "matched the lab exactly" + tag
    n = int(delta) if float(delta).is_integer() else round(delta, 1)
    n = abs(n)
    turns = "turn" if n == 1 else "turns"
    # smaller observed turn = happened sooner = the lab was pessimistic (ran slow)
    return f"lab ran {n} {turns} {'SLOW' if delta < 0 else 'FAST'} this game" + tag


def print_grade_card(rec, n_deck):
    """After a game lands, show how it graded against the lab it validates. `n_deck` = games
    now on record for this deck (the caller knows whether it just appended). Silently soft-skips
    when the medians are unavailable or the deck has no harvested lab clock."""
    print("\n── this game vs the lab " + "─" * 38)
    g = grade_game(rec, load_clock_medians())
    if not g:
        print(f"  ({rec.get('mine','?')} has no harvested lab clock — nothing to grade.)")
        return
    print(f"  {g['name']} — {n_deck} game(s) logged for this deck.")
    for kind, label in (("table", "table close"), ("decap", "first decap")):
        cell = g[kind]
        if not cell:
            continue
        lab = f"T{int(cell['lab'])}" if cell["lab"] is not None else "—"
        if cell.get("open"):
            lab = "≥" + lab
        print(f"  {label:12} T{int(cell['obs'])}  vs lab median {lab:>5}  → "
              f"{_delta_phrase(cell['delta'], cell.get('open'))}")
    if g["table"] is None:
        print("  (you didn't close the game — table clock not graded; decap still counts.)")
    need = max(0, 3 - n_deck)
    if need:
        print(f"  one game is an anecdote — calibrate.py needs n≥3 for this deck "
              f"({need} to go; ~5 for a stable rank).")
    else:
        print("  n≥3 for this deck — `python scripts/calibrate.py` now grades its "
              "clock + win-rate.")


# ---------------------------------------------------------- one-line quick entry
_T_RE = re.compile(r"^t(\d+)$")
_D_RE = re.compile(r"^(?:d|decap)(\d+)$")


def parse_quick(spec):
    """One-line shorthand -> a full record (pure; raises ValueError with guidance on any snag).

        <mydeck> W|L T<end> [d<decap>] [wintype]  |  <opp> [W|L]  |  <opp> [W|L]  # notes

    e.g.  genome W T9 d8 combo | ur_dragon L | kinnan L
          grand_design L T11 d9 | ur_dragon W          (I lost; ur_dragon closed)

    W/L on your line = did you win; T<n> = the turn the game ENDED (table clock, win or lose);
    d<n> = first decap turn; wintype in WIN_TYPES. Per-seat ko turns / disruption go through
    `log` or `add --from-json` — quick is the fast 90% path."""
    notes = ""
    if "#" in spec:
        spec, notes = spec.split("#", 1)
        notes = notes.strip()
    segs = [s.strip() for s in spec.split("|") if s.strip()]
    if not segs:
        raise ValueError("empty spec — e.g. 'genome W T9 d8 combo | ur_dragon L'")

    mine_toks = segs[0].split()
    mine, hits = resolve_slug(mine_toks[0], DECKS)
    if not mine:
        hint = f" did you mean {', '.join(hits)}?" if hits else ""
        raise ValueError(f"'{mine_toks[0]}' isn't one of your active decks.{hint}")

    i_won = win_turn = decap = win_type = None
    for tok in mine_toks[1:]:
        t = tok.lower()
        if t in ("w", "win"):
            i_won = True
        elif t in ("l", "loss", "lose"):
            i_won = False
        elif t in WIN_TYPES:
            win_type = t
        elif _T_RE.match(t):
            win_turn = int(_T_RE.match(t).group(1))
        elif _D_RE.match(t):
            decap = int(_D_RE.match(t).group(1))
        else:
            raise ValueError(f"didn't understand {tok!r} on your line (expected W/L, T<n>, "
                             f"d<n>, or a win-type {sorted(WIN_TYPES)})")
    if i_won is None:
        raise ValueError("mark your result with W or L on your line (e.g. 'genome W T9').")
    if win_turn is None:
        raise ValueError("add the end turn with T<n> (the turn the game ended — the table clock).")

    pod = [{"deck": mine, "pilot": "me", "result": "win" if i_won else "loss"}]
    winner = mine if i_won else None
    for seg in segs[1:]:
        toks = seg.split()
        oslug = _norm_slug(toks[0])
        seat = {"deck": oslug}
        for tok in toks[1:]:
            t = tok.lower()
            if t in ("w", "win"):
                seat["result"] = "win"
                winner = oslug
            elif t in ("l", "loss", "lose"):
                seat["result"] = "loss"
            else:
                raise ValueError(f"didn't understand {tok!r} for opponent {oslug!r} "
                                 f"(quick takes only W/L per opponent; use `log` for ko turns).")
        pod.append(seat)
    if winner is None:
        raise ValueError("you lost — mark who won with W on an opponent (e.g. 'ur_dragon W').")

    rec = {
        "date": _date.today().isoformat(), "mine": mine, "pod": pod, "winner": winner,
        "win_turn": win_turn, "win_type": win_type, "first_decap_turn": decap, "notes": notes,
    }
    return {k: v for k, v in rec.items() if v not in (None, [], "")}


def cmd_quick(a):
    try:
        rec = parse_quick(a.spec)
    except ValueError as e:
        sys.exit(f"quick: {e}")
    issues = problems(rec)
    print(json.dumps(rec, ensure_ascii=False, indent=2))
    if issues:
        print("\nRefusing to add — record has problems:", file=sys.stderr)
        for p in issues:
            print(f"  - {p}", file=sys.stderr)
        sys.exit(1)
    already = sum(1 for _, r in read_log() if r.get("mine") == rec["mine"])
    if a.dry_run:
        print("\n(dry run — not written)")
        print_grade_card(rec, already + 1)
        return
    append(rec)
    print(f"\nAppended to {LOG.relative_to(ROOT)} ({sum(1 for _ in read_log())} games on record).")
    print_grade_card(rec, already + 1)


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

    qk = sub.add_parser("quick", help="one-line shorthand entry (fast desk capture)")
    qk.add_argument("spec", help="e.g. 'genome W T9 d8 combo | ur_dragon L | kinnan L'")
    qk.add_argument("--dry-run", action="store_true", help="parse + grade, write nothing")
    qk.set_defaults(func=cmd_quick)

    sub.add_parser("list", help="compact list of logged games").set_defaults(func=cmd_list)
    sub.add_parser("summary", help="per-deck W/L + avg clocks (proto-oracle)").set_defaults(func=cmd_summary)
    sub.add_parser("validate", help="schema-check every record").set_defaults(func=cmd_validate)

    a = ap.parse_args()
    a.func(a)


if __name__ == "__main__":
    main()
