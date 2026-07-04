#!/usr/bin/env python3
"""ws_place.py — place the merged World Shapers build into the two SYNTHESIS oracles
(pod_gauntlet + tier_list) without editing their baked harvests. It reuses their own
functions (build_cdf / pure_race / simulate / simulate_vs / seed_field / compute_rows),
injecting the merged deck's MEASURED clock the same way a promoted deck would be
harvested — so the numbers are apples-to-apples with the roster.

Clock = ws_clock_lab --mode external on world-shapers-merged (40k, 2026-07-04):
  grid  [5, 6, 7, 8, 9, 10, 12, 14]
  decap [0, 1, 6, 23, 51, 74, 93, 98]   median T9
  table [0, 1, 3, 8, 18, 37, 78, 94]    median T11   never(decap,table)=(1,2)

CC score = 17 (5/4/4/4, judged 2026-07-04, same rubric as the roster): Core Loop 5
(18+ land-sac/landfall engine cards), Kill 4 (3 independent axes — drain / Mazirek /
Springheart — plus fair combat), Durability 4 (Loam/Crucible/Ramunap/Splendid/Titania/
Victimize recursion), Interaction 4 (7 instant removal + Blasphemous + Veil + Deflecting
Swat, mechanism-diverse). Note: tier_list v2 uses CC only as a CONTEXT column, so this
barely moves the tier — the composite is the three OUTCOME oracles.

disrupt_class = "warn" (a real one-shot removal suite). CONSERVATIVE for this deck: its
anti-combo removal is PROACTIVE (kill the piece on our own turn), which survives Grand
Abolisher — the "warn" bucket models reactive answers dying to Abolisher, so true P(win)
sits a touch ABOVE the bucketed number. Flagged, not corrected (same discipline as the
roster's bucketed decks).

defense count (self_meta durability) = 7 R/P answers (Beast Within, Putrefy, Infernal
Grasp, Tear Asunder, Windgrace's Judgment, Rakdos Charm = R; Blasphemous Act = P).

The tier run REPLACES earthbend_the_meta with the merged deck (the real post-retirement
roster: same seat, one deck in the field, not both). Pass --keep-earthbend to instead
INSERT merged alongside (17-deck field) for a head-to-head read.

Run:  python scripts/ws_place.py            # gauntlet + tier (merged replaces Earthbend)
      python scripts/ws_place.py --keep-earthbend
"""
import argparse
import importlib.util
import random
from pathlib import Path

ROOT = Path(__file__).parent.parent


def _load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


tl = _load("tier_list")
# Use tier_list's OWN module instances (compute_rows reads tl.pg / tl.sm.dl); loading a
# second pod_gauntlet would inject into the wrong object and the tier run wouldn't see it.
pg = tl.pg
sm = tl.sm
dl = sm.dl

SLUG = "world_shapers_merged"
MERGED = dict(
    name="World Shapers (merged)", score="17", disrupt_class="warn",
    lab=None, sel=("decap", "table"),
    grid=[5, 6, 7, 8, 9, 10, 12, 14],
    decap=[0, 1, 6, 23, 51, 74, 93, 98],
    table=[0, 1, 3, 8, 18, 37, 78, 94],
    med=("T9", "T11"), never=(1, 2), src="ws_clock_lab --mode external @40k 2026-07-04")


def inject(keep_earthbend):
    """Add the merged entry to pg.CLOCKS + a defense spec to dl.ROSTER. Optionally drop
    earthbend (the retired seat). Returns nothing — mutates the imported modules."""
    pg.CLOCKS[SLUG] = MERGED
    dl.ROSTER[SLUG] = ("world-shapers-merged-20260704.txt",
                       {"answers": {f"r{i}": ({"R"}, 2, set()) for i in range(6)}
                                  | {"sweep": ({"P"}, 8, set())}})   # 7 R/P answers
    if not keep_earthbend:
        pg.CLOCKS.pop("earthbend_the_meta", None)
        dl.ROSTER.pop("earthbend_the_meta", None)


def gauntlet(trials, seed):
    """Reproduce pod_gauntlet.run()'s ranking (decap clock, a=0.30) with merged in."""
    rng = random.Random(seed)
    kdist = pg.K_DIST
    C = pg.merged_clocks()
    rows = []
    for slug, c in C.items():
        F = pg.build_cdf(c["grid"], c["decap"])
        pr = pg.pure_race(F, kdist)
        win, _, _ = pg.simulate(slug, F, 0.30, kdist, trials, rng)
        rows.append((slug, c["name"], c["med"][0], pr, win))
    rows.sort(key=lambda r: -r[4])
    print("=" * 78)
    print("  POD GAUNTLET — P(beat the T6-7 combo pod)   decap clock, Abolisher P=0.30")
    print("=" * 78)
    print(f"  {'#':>2} {'deck':26}{'decap':>6}{'pure':>7}{'P(WIN)':>8}")
    for i, (slug, name, med, pr, win) in enumerate(rows, 1):
        star = "  <<< MERGED" if slug == SLUG else ""
        print(f"  {i:>2} {name:26}{med:>6}{pr*100:>6.0f}%{win*100:>7.0f}%{star}")
    r = next(i for i, x in enumerate(rows, 1) if x[0] == SLUG)
    print(f"\n  merged places #{r} of {len(rows)} on P(WIN). PURE RACE is the data-backed"
          f"\n  front edge; P(WIN) folds in the (conservative 'warn') disruption bucket.")


def tiers(trials, seed, keep_earthbend):
    rows = tl.compute_rows(trials=trials, seed=seed)["rows"]
    print("\n" + "=" * 78)
    lbl = "merged INSERTED (17-deck field)" if keep_earthbend else \
          "merged REPLACES Earthbend (real post-retirement roster)"
    print(f"  DEFINITIVE TIER LIST v2 (composite of antipod/inter/self) — {lbl}")
    print("=" * 78)
    print(f"  {'tier':>4} {'#':>2} {'deck':26}{'comp':>6}{'anti%':>7}{'inter%':>7}"
          f"{'self%':>7}{'cc':>5}")
    for i, row in enumerate(rows, 1):
        slug = row["slug"]
        star = "  <<< MERGED" if slug == SLUG else ""
        anti, inter, self_ = row.get("anti"), row.get("inter"), row.get("self")
        print(f"  {row['tier']:>4} {i:>2} {row['name']:26}{row['comp']:>6.1f}"
              f"{(anti or 0):>7.0f}{(inter if inter is not None else 0):>7.0f}"
              f"{(self_ or 0):>7.0f}{str(row.get('cc') or '—'):>5}{star}")
    r = next((i for i, x in enumerate(rows, 1) if x["slug"] == SLUG), None)
    t = next((x["tier"] for x in rows if x["slug"] == SLUG), None)
    print(f"\n  merged places #{r} of {len(rows)} -> TIER {t} on the v2 composite.")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--trials", type=int, default=20000)
    ap.add_argument("--seed", type=int, default=12345)
    ap.add_argument("--keep-earthbend", action="store_true")
    args = ap.parse_args()
    inject(args.keep_earthbend)
    gauntlet(args.trials, args.seed)
    tiers(args.trials, args.seed, args.keep_earthbend)


if __name__ == "__main__":
    main()
