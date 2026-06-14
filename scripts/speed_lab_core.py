#!/usr/bin/env python3
"""speed_lab_core.py — shared harness for the per-deck speed labs.

Extracted 2026-06-10 per proposals/Framework_Clock_Gap_2026-06-09.md §5 item 4:
the first four labs (lw/rc/er/gd_speed_lab.py) each re-implemented ~70% of the
same machinery. New labs import this module; the four originals are committed
evidence for their writeups and are deliberately NOT retrofitted.

What lives here (and what doesn't):

  ENGINE   load_deck_sim() bootstraps deck_sim.py (oracle index, reskin aliases,
           decklist parsing, London mulligan, land heuristics). build_lib()
           constructs swap variants. load_powers() reads printed power off the
           raw oracle file (front + back faces).

  AVAIL    simulate_groups(): P(>=1 member of EVERY group seen by turn T),
           drawn-only and with generic tutor wildcards (gd_speed_lab style).
           simulate_packages(): per-slot tutor sets with honest bipartite
           assignment (er_speed_lab style) — use when tutors are narrow.

  CLOCK    Goldfish: the per-turn scaffold every kill module shares — zones,
           draw, land drop (pure lands first), greedy cheapest-first mana-rock
           deployment, cast/fetch/mill primitives, a mana floor of
           lands + rocks. Table: a 3-opponent @40 damage tracker that knows
           the difference between focus-fire (combat) and hit-all (drains)
           and records decap turn vs table turn — the two clocks the
           verification rule requires stating separately.

  REPORT   row()/cum()/median(): the fixed T-grid percent table all labs print.
           run_cli(): the standard --mode/--trials argparse runner with one
           shared oracle load.

Everything here is HEURISTIC, not a rules engine. The same caveats as every
lab apply: mana is a lands+rocks floor, goldfish damage is unblocked, and the
numbers are availability/ceiling curves. Trust shapes and deltas, not second
decimals. Per-deck kill logic does NOT belong in this file.
"""
import argparse
import importlib.util
import json
import random
from pathlib import Path

ROOT = Path(__file__).parent.parent


def load_deck_sim():
    spec = importlib.util.spec_from_file_location(
        "deck_sim", Path(__file__).parent / "deck_sim.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ds = load_deck_sim()


# ---------------------------------------------------------------------------
# library construction / card data
# ---------------------------------------------------------------------------

def build_lib(base, index, removes, adds):
    """Variant library: base minus one copy of each remove, plus each add."""
    rm = list(removes)
    lib = []
    for t in base:
        if t[0] in rm:
            rm.remove(t[0])
            continue
        lib.append(t)
    if rm:
        raise SystemExit(f"remove not in library: {rm}")
    for nm in adds:
        rec = index.get(nm.lower())
        if rec is None:
            raise SystemExit(f"add not in oracle: {nm}")
        lib.append((nm, rec))
    return lib


def load_parsed(deck_path, index, aliases, warn=True):
    """parse_deck + unresolved warning in one step. Returns (library, commander)."""
    library, commander, diag = ds.parse_deck(deck_path, index, aliases)
    if warn and diag["unresolved"]:
        print(f"  UNRESOLVED: {diag['unresolved']}")
    return library, commander


def load_powers(names):
    """name(lower) -> int printed power (None = '*'/no power). Reads the raw
    oracle file so back faces (e.g. transformed commanders) resolve too."""
    with (ROOT / "collection" / "oracle-cards.json").open(encoding="utf-8") as f:
        cards = json.load(f)
    want = {n.lower() for n in names}
    out = {}

    def put(k, p):
        if k in want and k not in out:
            try:
                out[k] = int(p)
            except (TypeError, ValueError):
                out[k] = None

    for c in cards:
        put(c.get("name", "").lower(), c.get("power"))
        for face in c.get("card_faces") or []:
            put(face.get("name", "").lower(), face.get("power"))
    return out


# ---------------------------------------------------------------------------
# availability models
# ---------------------------------------------------------------------------

def simulate_groups(library, groups, tutors, trials, rng, turns):
    """P(>=1 member of EVERY group seen by turn T). Generic tutors are
    wildcards, each standing in for one missing group — optimistic (real
    tutors have colour/type limits and cost mana). Returns (drawn, with_tutors)
    as {t: pct} curves."""
    n = len(library)
    grp_sets = [{g.lower() for g in grp} for grp in groups]
    tutor_set = {t.lower() for t in tutors}
    drawn = [0] * (turns + 1)
    with_t = [0] * (turns + 1)
    for _ in range(trials):
        deck = library[:]
        hand, _ = ds.opening_hand(deck, rng)
        seen = {nm.lower() for nm, _ in hand}
        ptr = 7
        for t in range(1, turns + 1):
            if t > 1 and ptr < n:
                seen.add(deck[ptr][0].lower())
                ptr += 1
            missing = sum(1 for gs in grp_sets if not (gs & seen))
            tutors_seen = sum(1 for nm in seen if nm in tutor_set)
            if missing == 0:
                drawn[t] += 1
                with_t[t] += 1
            elif tutors_seen >= missing:
                with_t[t] += 1
    pct = lambda h: {t: 100.0 * h[t] / trials for t in range(1, turns + 1)}
    return pct(drawn), pct(with_t)


def slot_complete(slots, seen):
    """slots = [(member_set, tutor_set), ...] (lowercase). True when every slot
    is covered by a seen member or a distinct seen tutor that reaches it.
    Honest per-slot tutor mapping; brute assignment (labs use <=2 open slots)."""
    missing = [tut for mem, tut in slots if not (mem & seen)]
    if not missing:
        return True
    tutors_seen = list(set().union(*missing) & seen)
    if len(tutors_seen) < len(missing):
        return False
    if len(missing) == 1:
        return bool(missing[0] & seen)
    a, b = missing[0], missing[1]
    for t in tutors_seen:
        if t in a and (set(tutors_seen) - {t}) & b:
            return True
    return False


def simulate_packages(library, packages, trials, rng, turns):
    """{label: curve} of P(package reachable <= T). packages = {label: [slot]}
    with slot = (member-names, tutor-names-that-fetch-it), case-insensitive."""
    n = len(library)
    pk = {name: [({m.lower() for m in mem}, {t.lower() for t in tut})
                 for mem, tut in slots]
          for name, slots in packages.items()}
    hits = {name: [0] * (turns + 1) for name in pk}
    for _ in range(trials):
        deck = library[:]
        hand, _ = ds.opening_hand(deck, rng)
        seen = {nm.lower() for nm, _ in hand}
        ptr = 7
        for t in range(1, turns + 1):
            if t > 1 and ptr < n:
                seen.add(deck[ptr][0].lower())
                ptr += 1
            for name, slots in pk.items():
                if slot_complete(slots, seen):
                    hits[name][t] += 1
    return {name: {t: 100.0 * h[t] / trials for t in range(1, turns + 1)}
            for name, h in hits.items()}


# ---------------------------------------------------------------------------
# goldfish scaffold
# ---------------------------------------------------------------------------

class Goldfish:
    """Zones + the greedy mana floor every clock model shares.

    The kill module owns the turn loop and all deck-specific logic; this class
    owns: opening hand (London mulligan via deck_sim), draw, the land drop
    (pure lands first so flex lands stay castable), cheapest-first mana-rock
    deployment, and cast/fetch/mill/bin primitives. Mana available each turn
    = lands + deployed rock output (+ whatever the module adds via add_mana).
    Call begin_turn(T) first each turn, then deploy_rocks(), then spend
    self.avail through cast()/pay().
    """

    def __init__(self, library, rng, rocks=None):
        self.deck = library[:]
        hand, _ = ds.opening_hand(self.deck, rng)
        self.hand = list(hand)
        self.ptr = 7
        self.yard = []                 # (name, record) — mills, binned cards
        self.lands = 0
        self.rock_out = 0
        self.rocks = rocks or {}       # name -> (cost, mana_output)
        self.avail = 0

    # -- zones ---------------------------------------------------------------
    def draw(self, k=1):
        for _ in range(k):
            if self.ptr < len(self.deck):
                self.hand.append(self.deck[self.ptr])
                self.ptr += 1

    def mill(self, k):
        """Move k cards off the top into the yard; returns their names."""
        out = []
        for _ in range(k):
            if self.ptr < len(self.deck):
                self.yard.append(self.deck[self.ptr])
                out.append(self.deck[self.ptr][0])
                self.ptr += 1
        return out

    def in_hand(self, nm):
        return next((i for i, (h, _) in enumerate(self.hand) if h == nm), None)

    def has(self, nm):
        return self.in_hand(nm) is not None

    def discard(self, nm):
        i = self.in_hand(nm)
        if i is not None:
            self.yard.append(self.hand.pop(i))
            return True
        return False

    def in_yard(self, nm):
        return any(h == nm for h, _ in self.yard)

    def take_yard(self, nm):
        i = next((i for i, (h, _) in enumerate(self.yard) if h == nm), None)
        return self.yard.pop(i) if i is not None else None

    def fetch(self, nm):
        """Tutor: move named card from the undrawn library into hand."""
        for i in range(self.ptr, len(self.deck)):
            if self.deck[i][0] == nm:
                self.hand.append(self.deck[i])
                self.deck[i] = self.deck[len(self.deck) - 1]
                self.deck.pop()
                return True
        return False

    # -- turn skeleton ---------------------------------------------------------
    def begin_turn(self, T):
        """Draw (after T1), drop a land (pure lands first). Resets avail to the
        lands+rocks floor. Returns the name of the land played (or None)."""
        if T > 1:
            self.draw()
        played = None
        li = next((i for i, (_, r) in enumerate(self.hand) if ds.is_pure_land(r)), None)
        if li is None:
            li = next((i for i, (_, r) in enumerate(self.hand) if ds.is_land(r)), None)
        if li is not None:
            played = self.hand[li][0]
            self.hand.pop(li)
            self.lands += 1
        self.avail = self.lands + self.rock_out
        return played

    def deploy_rocks(self):
        """Greedy cheapest-first: cast every affordable rock; new output taps
        the same turn (matches the four original labs)."""
        changed = True
        while changed:
            changed = False
            cand = sorted(((i, self.rocks[nm]) for i, (nm, _) in enumerate(self.hand)
                           if nm in self.rocks), key=lambda x: x[1][0])
            for i, (cost, out) in cand:
                if self.avail >= cost:
                    self.hand.pop(i)
                    self.avail += out - cost
                    self.rock_out += out
                    changed = True
                    break

    # -- spending ---------------------------------------------------------------
    def pay(self, cost):
        if self.avail >= cost:
            self.avail -= cost
            return True
        return False

    def cast(self, nm, cost=None):
        """Cast nm from hand if affordable (cost defaults to oracle cmc)."""
        i = self.in_hand(nm)
        if i is None:
            return False
        c = self.hand[i][1]["cmc"] if cost is None else cost
        if self.avail < c:
            return False
        self.hand.pop(i)
        self.avail -= c
        return True

    def add_mana(self, n):
        self.avail += n


class Table:
    """3 opponents @40, decap/table clock tracker.

    hit_all(x, T)   — drains: every living opponent loses x (Exsanguinate,
                      Zulaport class). No spill.
    hit_focus(x, T) — combat: the lowest-index living opponent takes x.
    kill_all(T)     — an infinite/overwhelm line ends the game this turn.
    decap = first opponent's death turn; table = last's. State both per the
    verification rule (they diverge 2-3 turns in combat decks).
    """

    def __init__(self, n=3, life=40):
        self.life = life
        self.dmg = [0] * n
        self.decap = None
        self.table = None

    def _update(self, T):
        dead = sum(1 for d in self.dmg if d >= self.life)
        if dead >= 1 and self.decap is None:
            self.decap = T
        if dead == len(self.dmg) and self.table is None:
            self.table = T

    def hit_all(self, x, T):
        for i in range(len(self.dmg)):
            if self.dmg[i] < self.life:
                self.dmg[i] += x
        self._update(T)

    def hit_focus(self, x, T):
        for i in range(len(self.dmg)):
            if self.dmg[i] < self.life:
                self.dmg[i] += x
                break
        self._update(T)

    def kill_all(self, T):
        self.dmg = [self.life] * len(self.dmg)
        self._update(T)

    @property
    def done(self):
        return self.table is not None


# ---------------------------------------------------------------------------
# reporting
# ---------------------------------------------------------------------------

def row(label, d, show, width=40):
    return "  " + label.ljust(width) + "".join(f"{d[t]:6.0f}" for t in show)


def cum(results, idx, show):
    """results = list of tuples; idx selects a turn-or-None field. Returns the
    cumulative {t: pct} curve over the SHOW grid."""
    n = len(results)
    return {t: 100.0 * sum(1 for r in results if r[idx] is not None and r[idx] <= t) / n
            for t in show}


def median(results, idx, cap=99):
    vals = sorted((r[idx] if r[idx] is not None else cap) for r in results)
    m = vals[len(vals) // 2]
    return f"T{m}" if m < cap else f">T (never in horizon)"


def run_cli(doc, modes, default_trials=40000):
    """Standard lab CLI: --mode {<modes>,all} --trials N. Loads the oracle index
    and aliases once and calls each selected mode(index, aliases, trials)."""
    ap = argparse.ArgumentParser(description=doc,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--mode", choices=list(modes) + ["all"], default="all")
    ap.add_argument("--trials", type=int, default=default_trials)
    args = ap.parse_args()
    index = ds.load_oracle_index()
    aliases = ds.load_reskin_aliases()
    for name, fn in modes.items():
        if args.mode in (name, "all"):
            fn(index, aliases, args.trials)


# ---------------------------------------------------------------------------
# shared clock runner + report
#
# The class-style trial loop and the decap/table report block were copy-pasted
# into every clock lab. They are hoisted here so a lab is just its bespoke kill
# model (the Trial class) plus a short spec. The kill model is unchanged, so a
# migrated lab's NUMBERS are identical — only the surrounding scaffold moves.
# See clock_lab_template.py for the thin pattern. Function-style labs (a kill fn
# returning (decap, table)) keep their own loop; these helpers are for the common
# class-style case.
# ---------------------------------------------------------------------------

def run_goldfish(make_trial, trials, turns):
    """Run the standard kill-turn goldfish loop.

    make_trial() returns a fresh per-trial object exposing .turn(T) and a .tbl
    (a Table). Each trial runs turns 1..turns, breaking once the table is dead,
    and contributes one (decap, table) pair. Returns [(decap, table), ...]."""
    out = []
    for _ in range(trials):
        tr = make_trial()
        for T in range(1, turns + 1):
            tr.turn(T)
            if tr.tbl.done:
                break
        out.append((tr.tbl.decap, tr.tbl.table))
    return out


def never_pct(results, idx, trials):
    """% of trials where clock `idx` (0=decap, 1=table) never fired in horizon."""
    return 100.0 * sum(1 for r in results if r[idx] is None) / trials


def report_clock(results, show, turns, trials, single=False, indent="  "):
    """The standard kill-turn report: P(kill <= T) cumulative grid over the SHOW
    T-grid + medians + never-in-horizon %.

    results = [(decap, table), ...] (e.g. from run_goldfish). single=True
    collapses to one row for decks where decap == table by construction (an
    overwhelm / hit-all kill); otherwise both clocks print, as the verification
    rule requires (state decap and table separately)."""
    print(indent + "P(kill <= turn T) %".ljust(40) + "".join(f"{t:>6}" for t in show))
    if single:
        print(row("kill (decap = table, cum %)", cum(results, 1, show), show))
        nv = never_pct(results, 1, trials)
        print(f"\n{indent}median kill {median(results, 1)}"
              f"   ·   never-in-{turns}: {nv:.0f}%")
    else:
        print(row("decap (one opponent, 40)", cum(results, 0, show), show))
        print(row("table (all three)", cum(results, 1, show), show))
        nd, nt = never_pct(results, 0, trials), never_pct(results, 1, trials)
        print(f"\n{indent}median decap {median(results, 0)}   median table {median(results, 1)}"
              f"   ·   never-in-{turns}: decap {nd:.0f}% / table {nt:.0f}%")
