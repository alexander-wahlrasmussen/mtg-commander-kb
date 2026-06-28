#!/usr/bin/env python3
"""finisher_mixture.py — Backlog #11 "proper version": per-line finisher mixture with a
pod-state DISABLER vector.

WHY THIS EXISTS (read analysis/Finisher_Coverage_Map_2026-06-28.md first). The coverage
audit proved every deck's harvested clock is ALREADY a best-line min over its kill lines on
ONE correlated game — so per-line emission adds NO speed. What a single blended curve CANNOT
express is a line being switched OFF by pod state:

  graveyard hate (Rest in Peace)  -> a storm / recursion / reanimator line dies
  a table still near 40           -> an incremental CHIP line has nothing to finish
  a one-noncreature-spell lock     -> a multi-spell burn race / spell-combo can't execute
  (Rule of Law / Eidolon of Rhetoric — [[feedback_interaction_role_protect_vs_disrupt]])

This consumer reads each deck's lines SEPARATELY and reports the earliest VIABLE close over
the lines NOT disabled by the active pod conditions. Because it only ever REMOVES lines, the
mixture is BOUNDED ABOVE by the harvested best-line curve — it models degradation, never a
faster fiction. (The "every deck looks faster" worry was about ADDING lines, which the
coverage audit showed is already done.)

NULL REDUCTION: with no pod conditions active, no line is disabled, so the mixture == the
harvested best-line curve bit-for-bit (tests/test_finisher_mixture.py).

STATUS — PILOT. Only Lightning War is "split": wired to its two REAL labbed lines
(lw_clock_lab.perline_kill — burn race + Reiterate/Seething Song combo, raced on one game).
Every other deck DEGRADES honestly to a single pass-through line == its harvested
pod_gauntlet curve (no sub-lines to disable) until its own lab is split to emit per-line
turns. UNCALIBRATED: the disabler tags are card-text-grounded but their effect on real
win-rate is NOT back-tested — that needs logged games (Backlog #10). Do not bake this into
the tier list / gauntlet; it is a separate consumer, exactly as the #11 MVP left the
tournament untouched.

Run:  python scripts/finisher_mixture.py                       # LW under {}, {gy}, {rule_of_law}
      python scripts/finisher_mixture.py --conditions rule_of_law
      python scripts/finisher_mixture.py --emit                 # write analysis/finisher_lines.json
"""
import argparse
import importlib.util
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def _imp(name):
    spec = importlib.util.spec_from_file_location(name, Path(__file__).parent / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


lw = _imp("lw_clock_lab")          # pulls in speed_lab_core + lw_combo_lab
slc = lw.slc
ds = slc.ds

CLOCKS_JSON = ROOT / "analysis" / "pod_gauntlet_clocks.json"
LINES_JSON = ROOT / "analysis" / "finisher_lines.json"
TRIALS_DEFAULT = 8000              # match the pod_gauntlet harvest so the null reduction is exact

# --- pod-state condition vocabulary (card-grounded; informational keys) ------------------
CONDITIONS = {
    "graveyard_hate": "Rest in Peace / Bojuka Bog — graveyards exiled/emptied",
    "table_near_40": "opponents still at/near 40 — no chip softening yet",
    "rule_of_law": "Rule of Law / Eidolon of Rhetoric — one noncreature spell per turn",
}

# --- per-deck, per-line metadata: kind + the conditions that HARD-disable the line --------
# A line survives a pod state iff none of its disablers is active. Only SPLIT decks (those
# with a real per-line emitter below) carry disablers — an unsplit single line has no
# sub-lines to switch off, so it is a pass-through (disablers stay empty: honest, not inert
# by accident). Every tag here is grounded in the named cards' oracle text, NOT guessed.
LINE_META = {
    "lightning_war": {
        "burn": {"kind": "finisher", "disablers": ["rule_of_law"],
                 "note": "X-burn race + per-cast pinger chip — needs to CHAIN several "
                         "noncreature spells a turn; a one-spell lock collapses it. "
                         "Graveyard-independent."},
        "combo": {"kind": "combo", "disablers": ["rule_of_law"],
                  "note": "Reiterate+Seething Song / Narset — the go-off turn casts MULTIPLE "
                          "noncreature spells, so a one-spell lock stops it. Primary assembly "
                          "is from hand, so graveyard hate does NOT disable it."},
    },
}

# Informational primary-kind tags for the UNSPLIT (pass-through) decks — from the coverage
# map (deck_registry win_line + Finisher_Coverage_Map). No disabler hangs on these (the deck
# is one harvested line until its lab is split), so a coarse tag is harmless; it just records
# what the single curve mostly represents.
UNSPLIT_KIND = {
    "genome_project": "storm", "radiation_sickness": "combat", "replication_crisis": "combo",
    "lorehold_spirits": "combat", "earthbend_the_meta": "combat", "exiles_return": "finisher",
    "zero_sum_game": "combo", "curse_of_the_scarab": "combat", "bumbleflower": "finisher",
    "eldrazi_stampede": "combat", "dark_lords_army": "chip", "diminishing_returns": "combo",
    "grand_design": "finisher", "crystal_sickness": "chip", "croak_and_dagger": "finisher",
    "forced_liquidation": "finisher",
}


# --- per-line sampling (SPLIT decks) -----------------------------------------------------
def lw_perline_samples(trials, seed):
    """[{"burn": (decap, table), "combo": (decap, table)}] over `trials` shared games at
    `seed` — the same rolls bestline_kill uses, so the null reduction is exact."""
    index, aliases = ds.load_oracle_index(), ds.load_reskin_aliases()
    library, commander = slc.load_parsed(lw.DECK, index, aliases, warn=False)
    powmap = lw._powmap(library, commander)
    combo_rocks = lw.lcl.deck_rocks(library)
    rng = random.Random(seed)
    return [lw.perline_kill(library, commander, powmap, combo_rocks, rng) for _ in range(trials)]


SPLIT_SAMPLERS = {"lightning_war": lw_perline_samples}


# --- the mixture -------------------------------------------------------------------------
def line_survives(slug, line_id, conditions):
    dis = set(LINE_META[slug][line_id]["disablers"])
    return not (dis & set(conditions))


def mixture_samples(slug, samples, conditions):
    """Per game, the earliest (decap, table) over the lines NOT disabled by `conditions`.
    min over correlated draws on one game — never over independent CDFs."""
    out = []
    for s in samples:
        live = [v for lid, v in s.items() if line_survives(slug, lid, conditions)]
        d = min([x for x, _ in live if x is not None], default=None)
        t = min([x for _, x in live if x is not None], default=None)
        out.append((d, t))
    return out


def curve(samples_dt, grid, trials):
    """(decap, table) samples -> the pod_gauntlet curve shape {grid,decap,table,med,never}."""
    dc, tc = slc.cum(samples_dt, 0, grid), slc.cum(samples_dt, 1, grid)
    return {
        "grid": list(grid),
        "decap": [round(dc[g]) for g in grid],
        "table": [round(tc[g]) for g in grid],
        "med": [slc.median(samples_dt, 0), slc.median(samples_dt, 1)],
        "never": [round(slc.never_pct(samples_dt, 0, trials)),
                  round(slc.never_pct(samples_dt, 1, trials))],
    }


def line_curve(slug, line_id, samples, grid, trials):
    dt = [s[line_id] for s in samples]
    c = curve(dt, grid, trials)
    c.update(line_id=line_id, **{k: LINE_META[slug][line_id][k]
                                 for k in ("kind", "disablers", "note")})
    return c


# --- JSON emission (the schema artifact) -------------------------------------------------
def build_records(trials, seed):
    """The finisher_lines.json content: split decks carry a per-line list + a bestline_check
    (the null-reduction target); unsplit decks carry one pass-through line == their harvested
    pod_gauntlet curve."""
    harvested = json.loads(CLOCKS_JSON.read_text(encoding="utf-8"))
    out = {"_meta": {
        "doc": "Backlog #11 proper version — per-line finisher records. See "
               "scripts/finisher_mixture.py + analysis/Finisher_Mixture_Pilot_2026-06-28.md.",
        "schema": "per deck: {name, grid, split, lines:[{line_id,kind,decap,table,med,never,"
                  "disablers,note}], bestline_check?}. A line survives a pod state iff none "
                  "of its `disablers` (keys in `conditions`) is active; the mixture is the "
                  "earliest viable close over survivors, bounded ABOVE by bestline_check.",
        "conditions": CONDITIONS,
        "status": "PILOT — only lightning_war is split (real per-line labs); the rest are "
                  "single pass-through lines until their labs emit per-line turns. UNCALIBRATED.",
        "trials": trials,
    }}
    for slug, h in harvested.items():
        if slug in SPLIT_SAMPLERS:
            samples = SPLIT_SAMPLERS[slug](trials, seed)
            grid = h["grid"]
            lines = [line_curve(slug, lid, samples, grid, trials) for lid in LINE_META[slug]]
            best = curve(mixture_samples(slug, samples, []), grid, trials)
            out[slug] = {"name": h["name"], "grid": grid, "split": True,
                         "lines": lines, "bestline_check": best}
        else:
            out[slug] = {"name": h["name"], "grid": h["grid"], "split": False,
                         "lines": [{"line_id": "harvested", "kind": UNSPLIT_KIND.get(slug, "?"),
                                    "decap": h["decap"], "table": h["table"],
                                    "med": h["med"], "never": h["never"], "disablers": [],
                                    "note": f"single harvested pod_gauntlet line ({h['src']}); "
                                            "not yet split into per-line CDFs"}]}
    return out


def emit(trials, seed):
    LINES_JSON.write_text(json.dumps(build_records(trials, seed), indent=2), encoding="utf-8")
    rel = LINES_JSON.relative_to(ROOT)
    print(f"  wrote {rel}  (split: {', '.join(SPLIT_SAMPLERS)} · pass-through: the rest)")


# --- null reduction (also asserted in tests) ---------------------------------------------
def null_reduction_ok(trials, seed):
    """mixture(no conditions) == bestline_kill on the same games, per game. Proves the
    disabler vector only ever subtracts: empty conditions reproduce the harvested curve."""
    samples = lw_perline_samples(trials, seed)
    mix = mixture_samples("lightning_war", samples, [])
    index, aliases = ds.load_oracle_index(), ds.load_reskin_aliases()
    library, commander = slc.load_parsed(lw.DECK, index, aliases, warn=False)
    powmap = lw._powmap(library, commander)
    combo_rocks = lw.lcl.deck_rocks(library)
    rng = random.Random(seed)
    best = [lw.bestline_kill(library, commander, powmap, combo_rocks, rng) for _ in range(trials)]
    return mix == best


# --- CLI ---------------------------------------------------------------------------------
def _print_curve(label, c, grid):
    print("  " + label.ljust(34) + "".join(f"{v:6d}" for v in c["decap"]) + f"   med {c['med'][0]}")
    print("  " + "".ljust(34) + "".join(f"{v:6d}" for v in c["table"]) + f"   med {c['med'][1]} (table)")


def mode_show(trials, seed, conditions):
    slug = "lightning_war"
    samples = SPLIT_SAMPLERS[slug](trials, seed)
    grid = json.loads(CLOCKS_JSON.read_text(encoding="utf-8"))[slug]["grid"]
    print(f"\n### FINISHER MIXTURE — {lw.DECK.stem}   trials={trials} seed={seed}")
    print("    P(close <= T) for the earliest VIABLE line under each pod state. The mixture")
    print("    only ever REMOVES lines, so it is bounded ABOVE by the no-conditions row.\n")
    print("  P(kill <= turn T) %".ljust(36) + "".join(f"{t:>6}" for t in grid))
    scenarios = conditions if conditions else [[], ["graveyard_hate"], ["rule_of_law"]]
    for cond in scenarios:
        live = [lid for lid in LINE_META[slug] if line_survives(slug, lid, cond)]
        tag = "{}" if not cond else "{" + ",".join(cond) + "}"
        print(f"  -- pod state {tag}  ->  live lines: {live or 'NONE'} " + "-" * 6)
        _print_curve("   mixture", curve(mixture_samples(slug, samples, cond), grid, trials), grid)
    print(f"\n  null reduction (mixture{{}} == harvested bestline, per game): "
          f"{'OK' if null_reduction_ok(min(trials, 2000), seed) else 'FAIL'}")
    print("  NB: graveyard_hate disables NEITHER LW line (both assemble from hand); "
          "rule_of_law disables BOTH (each is a multi-noncreature-spell turn) -> LW does nothing.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--trials", type=int, default=TRIALS_DEFAULT)
    ap.add_argument("--seed", type=int, default=lw.SEED)
    ap.add_argument("--conditions", default="",
                    help="comma-separated pod conditions, e.g. rule_of_law,graveyard_hate")
    ap.add_argument("--emit", action="store_true", help="write analysis/finisher_lines.json")
    args = ap.parse_args()
    bad = [c for c in args.conditions.split(",") if c and c not in CONDITIONS]
    if bad:
        raise SystemExit(f"unknown condition(s) {bad}; known: {list(CONDITIONS)}")
    if args.emit:
        emit(args.trials, args.seed)
    else:
        conds = [[c for c in args.conditions.split(",") if c]] if args.conditions else []
        mode_show(args.trials, args.seed, conds)
