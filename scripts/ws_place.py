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
      python scripts/ws_place.py --dragon   # P(win vs Ur-Dragon), merged injected

--dragon injects the merged deck into vs_dragon_roster_lab the same way. Its kill CDF
there is the COMBAT-OFF clock (ws_clock_lab --mode comboclock --deck merged @40k,
2026-07-05): what the deck does when plain combat is fully answered — the honest
"over the flying wall" clock. Mixture in that run: land-sac drain 39% / Mazirek combo
18% / landfall slug 12% / AWBO 9% / Purphoros 7% / pumped-Spawn swing 11% (the swing
slice is still combat-delivered; it survives here only via the tapped-attacker
crackback argument — flagged, small). axis=over, race=False (drain hits each
opponent). protect=0.0 (conservative: Veil/Swat not modelled as counter-war).
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


def tiers(trials, seed, keep_earthbend, inter=None):
    """inter: if set, inject a manual interaction-axis value for the merged deck (the axis
    is otherwise `—` for a non-delay_lab-measured candidate). Answers 'how much does the
    unmeasured interaction axis cost it, and would investing there move the tier?'"""
    if inter is not None:
        _orig = tl.interaction
        def _patched(slugs, C, t, rng, tg, tax):
            d = _orig(slugs, C, t, rng, tg, tax)
            d[SLUG] = inter
            return d
        tl.interaction = _patched
    rows = tl.compute_rows(trials=trials, seed=seed)["rows"]
    if inter is not None:
        tl.interaction = _orig
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


# combat-OFF clock: ws_clock_lab --mode comboclock --deck world-shapers-merged @40k 2026-07-05
MERGED_OVER_CDF = ([5, 6, 7, 8, 9, 10, 12, 14, 16], [0, 1, 3, 8, 18, 34, 70, 89, 96])


def dragon(trials, seed):
    """Inject merged into vs_dragon_roster_lab (axis=over, combat-off clock) and rank."""
    vd = _load("vs_dragon_roster_lab")
    decks = vd.build_decks(trials)
    lib, _ = vd.core.load_parsed(ROOT / "decks" / "considering" / "world-shapers-merged-20260704.txt",
                                 vd.ds.load_oracle_index(), vd.ds.load_reskin_aliases(), warn=False)
    tk = vd.classify([nm for nm, _ in lib])
    decks[SLUG] = dict(
        slug=SLUG, name="World Shapers (merged)", axis="over", race=False,
        note="COMBAT-OFF clock: drain 39% / Mazirek 18% / slug+AWBO+Purphoros 28% — board-independent",
        protect=0.0, toolkit=tk, F=vd.build_cdf(*MERGED_OVER_CDF), **vd.cap_counts(tk))

    ns = argparse.Namespace(
        trials=trials, dmg_base=16, dmg_step=7, rebuild=1, reset_mult=0.70,
        kill_disrupt=0.15, maze_block=8, maze_online=0.55, removal_block=7,
        draw=0.58, p_act=0.70, p_connect=0.22, connect_decay=0.5, tax_block=0.25,
        life_per_gain=2, life_cap=12, race_delay=0)
    P = vd.params(ns)
    rng = random.Random(seed)
    rows = sorted(((vd.simulate(d, d["F"], vd.G_DIST, P, rng), d) for d in decks.values()),
                  key=lambda r: -r[0])
    print("\n" + "=" * 78)
    print("  VS UR-DRAGON — P(win vs the fair flying-board deck), merged INSERTED")
    print("=" * 78)
    print(f"  {'#':>2} {'deck':26}{'axis':>7}{'wr':>3}{'fog':>4}{'spot':>5}{'P(win)':>8}")
    for i, (p, d) in enumerate(rows, 1):
        star = "  <<< MERGED" if d["slug"] == SLUG else \
               ("  <<< retiring seat" if d["slug"] == "earthbend_the_meta" else "")
        print(f"  {i:>2} {d['name']:26}{d['axis']:>7}{d['nwr']:>3}{d['nfog']:>4}"
              f"{d['nspot']:>5}{p*100:>7.0f}%{star}")
    tk = decks[SLUG]["toolkit"]
    print(f"\n  merged toolkit audit — WR: {', '.join(tk['wraths']) or '—'} · "
          f"FOG: {', '.join(tk['fogs']) or '—'} · SPOT: {', '.join(tk['spot'][:6]) or '—'} · "
          f"life x{len(tk['lifegain'])}")
    print("  merged kill CDF = the COMBAT-OFF clock (plain combat fully answered), so the")
    print("  walled slice of its mixture is already excluded; ~11% pumped-Spawn swings kept")
    print("  (tapped-attacker crackback). Earthbend races its full decap clock but is WALLED.")

    print("\n  SWEEP (merged vs the retiring Earthbend seat across the model priors):")
    scen = [("baseline", {}), ("go-live FAST", dict(_kd="fast")), ("go-live SLOW", dict(_kd="slow")),
            ("hyper-aggro 22+9", dict(dmg_base=22, dmg_step=9)), ("grindy 12+5", dict(dmg_base=12, dmg_step=5)),
            ("thru-wall .45", dict(p_connect=0.45)), ("we brick .45", dict(draw=0.45))]
    print(f"  {'deck':26}" + "".join(f"{l[:12]:>13}" for l, _ in scen))
    for slug in (SLUG, "earthbend_the_meta"):
        d = decks[slug]
        cells = []
        for _, ov in scen:
            ov = dict(ov)
            tag = ov.pop("_kd", None)
            kd = {5: 0.15, 6: 0.35, 7: 0.32, 8: 0.13, 9: 0.05} if tag == "fast" else \
                 {7: 0.25, 8: 0.35, 9: 0.25, 10: 0.15} if tag == "slow" else vd.G_DIST
            cells.append(vd.simulate(d, d["F"], kd, vd.params(ns, **ov), random.Random(seed + 7)))
        print(f"  {d['name']:26}" + "".join(f"{c*100:>12.0f}%" for c in cells))


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--trials", type=int, default=20000)
    ap.add_argument("--seed", type=int, default=12345)
    ap.add_argument("--keep-earthbend", action="store_true")
    ap.add_argument("--inter", type=float, default=None,
                    help="inject a manual interaction-axis %% for the merged deck "
                         "(sensitivity on the unmeasured 0.35 axis)")
    ap.add_argument("--dragon", action="store_true",
                    help="also rank the merged deck in the vs-Ur-Dragon roster model")
    args = ap.parse_args()
    if args.dragon:
        dragon(args.trials, args.seed)
        return
    inject(args.keep_earthbend)
    gauntlet(args.trials, args.seed)
    tiers(args.trials, args.seed, args.keep_earthbend, inter=args.inter)


if __name__ == "__main__":
    main()
