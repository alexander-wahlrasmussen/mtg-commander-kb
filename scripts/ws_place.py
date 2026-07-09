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

--measure-inter (2026-07-04, user follow-up "what's the interaction axis today?"):
run the canonical delay_lab engine on the merged list (answer spec below, oracle-verified)
and inject the result into pg.MEASURED + pg.PROTECT — the same harvest a promoted deck
gets from delay_lab --emit-json. This turns the tier's interaction axis from `—` into a
MEASURED value, and upgrades the gauntlet for merged too (measured disruption replaces
the conservative "warn" bucket; PROTECT replaces the 0.0 default).

Run:  python scripts/ws_place.py            # gauntlet + tier (merged replaces Earthbend)
      python scripts/ws_place.py --keep-earthbend
      python scripts/ws_place.py --measure-inter
      python scripts/ws_place.py --tuned --measure-inter   # the Lever-2+3 tuned variant
      python scripts/ws_place.py --dragon [--variant tuned]  # P(win vs Ur-Dragon)

--dragon (2026-07-05) injects the active variant into vs_dragon_roster_lab the same
way. Its kill CDF there is the COMBAT-OFF clock (ws_clock_lab --mode comboclock
--deck <list> @40k, harvested per variant in OVER_CDF below): what the deck does
when plain combat is fully answered — the honest "over the flying wall" clock.
Merged-list mixture in that run: land-sac drain 39% / Mazirek combo 18% / landfall
slug 12% / AWBO 9% / Purphoros 7% / pumped-Spawn swing 11% (the swing slice is still
combat-delivered; it survives here only via the tapped-attacker crackback argument —
flagged, small). axis=over, race=False (drain hits each opponent). protect=0.0
(conservative: Veil/Swat not modelled as counter-war).
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

# --- delay_lab answer spec for the merged list (--measure-inter) ---------------------
# Classification per delay_lab's rules, oracle text card_lookup-verified 2026-07-04.
# Exclusions per the canonical lab: Deflecting Swat (redirect), Veil of Summer
# (protect-own), Pest Infestation + Boseiju channel (artifact/enchantment/land removal —
# the pod's combo pieces are creatures). Tear Asunder costed KICKED (4): unkicked it
# cannot touch a creature. Blasphemous Act at the roster's cost-reduction override (5).
# Tutors left empty — gauntlet/tier read the DRAWN composed value (roster convention;
# Gamble/Natural Order are combo tutors here, not answer tutors).
WS_ANSWERS = {
    "answers": {
        "Infernal Grasp":       ({"R", "P"}, 2, {"ios"}),
        "Rakdos Charm":         ({"R", "P"}, 2, {"ios"}),
        "Putrefy":              ({"R", "P"}, 3, {"ios"}),
        "Beast Within":         ({"R", "P"}, 3, {"ios"}),
        "Tear Asunder":         ({"R", "P"}, 4, {"ios"}),
        "Windgrace's Judgment": ({"R", "P"}, 5, {"ios"}),
        "Blasphemous Act":      ({"P"}, 5, {"ios"}),
    },
    "tutors": {},
}
# protect-own prior, same 2026-06-15 rubric as pg.PROTECT: zero counters, but the close
# is counter/Abolisher-immune (drain + Mazirek loop are triggers/mana abilities; only the
# creature casts are counter-exposed) and Veil of Summer + Deflecting Swat cover exactly
# that window. Mirrors zero_sum_game 0.30 ("board-independent Abolisher-proof kill + Veil,
# no counters").
WS_PROTECT = 0.30

MERGED_LIST = ROOT / "decks" / "considering" / "world-shapers-merged-20260704.txt"

# --- the TUNED variant (--tuned, 2026-07-04): Lever 2 + Lever 3 applied to the merged
# list, core plan untouched. 12-for-12: −Escape to the Wilds −Augur of Autumn −Tireless
# Tracker −Springbloom Druid −Evolving Wilds −Terramorphic Expanse −6 basics (11→5) →
# +Abrade +Bitter Triumph +Murderous Rider +The Meathook Massacre (interaction; the PROP's
# Rollick/Trophy/Warp/GftT package measured NOT free — availability_check 2026-07-04) and
# +Prismatic Vista +Verdant Catacombs +Woodland Cemetery +Tainted Wood +Raging Ravine
# +Myriad Landscape +Takenuma +Command Beacon (premium lands; Vista/Catacombs/Takenuma/
# Meathook are Diminishing Returns donor pulls per the user's carve-out). Clock re-labbed:
# decap slips ~2pp on the front edge (draw cuts), table median T11 holds.
# 2026-07-05 correction: the 2026-07-04 harvest ran with commander None —
# "world-shapers-tuned" was missing from deck_registry.EXTRA_COMMANDERS, so Hearthhull
# sat in the library. Re-harvested after the registry fix (~1-2pp faster, medians hold).
TUNED = dict(
    name="World Shapers (tuned)", score="17", disrupt_class="warn",
    lab=None, sel=("decap", "table"),
    grid=[5, 6, 7, 8, 9, 10, 12, 14],
    decap=[0, 1, 6, 22, 50, 73, 92, 97],
    table=[0, 1, 3, 7, 17, 35, 76, 93],
    med=("T10", "T11"), never=(1, 2),
    src="ws_clock_lab --mode external @40k on world-shapers-tuned 2026-07-05 (post registry fix)")

TUNED_LIST = ROOT / "decks" / "considering" / "world-shapers-tuned-20260704.txt"
# adds card_lookup-verified 2026-07-04: Murderous Rider costed at the Swift End half
# ({1}{B}{B} instant); The Meathook Massacre at X=2 (a {4} preempt wipe — enchantment,
# so no ios tag; P-only, same class logic as Toxic Deluge in the canonical lab).
TUNED_ANSWERS = {
    "answers": dict(WS_ANSWERS["answers"]) | {
        "Abrade":                ({"R", "P"}, 2, {"ios"}),
        "Bitter Triumph":        ({"R", "P"}, 2, {"ios"}),
        "Murderous Rider":       ({"R", "P"}, 3, {"ios"}),
        "The Meathook Massacre": ({"P"}, 4, set()),
    },
    "tutors": {},
}

# --- the EXTERNAL primer build (--variant external, 2026-07-04): the ~$1400 community
# list, placed for the tuned-vs-external comparison. Clock re-harvested @40k (true
# external list, not the merged --deck run). Answer suite verified 2026-07-04: only FOUR
# pod-relevant instants — Abrupt Decay (uncounterable, MV<=3: Abolisher/Kinnan/dorks),
# Assassin's Trophy, Beast Within, Tear Asunder (kicked=4). Glacial Chasm / Constant
# Mists / Sylvan Safekeeper are protect-own/defensive (excluded per delay_lab rules —
# the Chasm damage-prevention lock is real but belongs to a --vs-lock overlay, not
# disruption; conservative for this list). No CC judgment exists for it → score None
# (tier_list redistributes weights, same as Zero-Sum).
EXTERNAL = dict(
    name="World Shapers (external)", score=None, disrupt_class="warn",
    lab=None, sel=("decap", "table"),
    grid=[5, 6, 7, 8, 9, 10, 12, 14],
    decap=[0, 0, 4, 22, 50, 73, 92, 97],
    table=[0, 0, 0, 4, 14, 35, 76, 92],
    med=("T9", "T11"), never=(1, 3),
    src="ws_clock_lab --mode external @40k 2026-07-04 (true external list)")

EXTERNAL_LIST = ROOT / "decks" / "considering" / "world-shapers-external-20260704.txt"
EXTERNAL_ANSWERS = {
    "answers": {
        "Abrupt Decay":      ({"R", "P"}, 2, {"ios"}),
        "Assassin's Trophy": ({"R", "P"}, 2, {"ios"}),
        "Beast Within":      ({"R", "P"}, 3, {"ios"}),
        "Tear Asunder":      ({"R", "P"}, 4, {"ios"}),
    },
    "tutors": {},
}

# --- SENSITIVITY BOUND, not a measurement (--variant externalfast, 2026-07-04): the
# external clock shifted one FULL turn earlier on both curves (non-uniform grid tail
# interpolated), as a deliberately generous stand-in for its unmodelled combo lines.
# Generosity check: ws_combo_lab assembly (same instrument, external taxonomy) puts a
# win engine online in 1-3% of games drawn / <=26% at the free-tutor CEILING by T12 —
# a full turn on 100% of games credits far more than that option is worth. If this
# still places deep Tier D, the tuned-vs-external verdict is clock-robust.
EXTERNAL_FAST = dict(
    name="World Shapers (ext +1T)", score=None, disrupt_class="warn",
    lab=None, sel=("decap", "table"),
    grid=[5, 6, 7, 8, 9, 10, 12, 14],
    decap=[0, 4, 22, 50, 73, 82, 95, 98],
    table=[0, 0, 4, 14, 35, 55, 84, 94],
    med=("T8", "T10"), never=(1, 3),
    src="SENSITIVITY: external @40k curves shifted -1 turn (combo-credit bound)")

VARIANTS = {
    "merged":   dict(slug="world_shapers_merged", entry=MERGED, deck=MERGED_LIST,
                     spec=WS_ANSWERS),
    "tuned":    dict(slug="world_shapers_tuned", entry=TUNED, deck=TUNED_LIST,
                     spec=TUNED_ANSWERS),
    "external": dict(slug="world_shapers_external", entry=EXTERNAL, deck=EXTERNAL_LIST,
                     spec=EXTERNAL_ANSWERS),
    "externalfast": dict(slug="world_shapers_ext_fast", entry=EXTERNAL_FAST,
                         deck=EXTERNAL_LIST, spec=EXTERNAL_ANSWERS),
}


def _defense_spec(spec):
    """Dummy-name defense spec for dl.ROSTER with the variant's real R/P counts
    (sm.defense_counts only counts classes; names/costs are never simulated)."""
    n_r = sum(1 for cls, _c, _t in spec["answers"].values() if "R" in cls)
    n_p = sum(1 for cls, _c, _t in spec["answers"].values() if cls == {"P"})
    return {"answers": {f"r{i}": ({"R"}, 2, set()) for i in range(n_r)}
                     | {f"sweep{i}": ({"P"}, 8, set()) for i in range(n_p)},
            "tutors": {}}


# active variant (rebound by select_variant in main; default = the base merged build)
ACTIVE = VARIANTS["merged"]


def select_variant(name):
    global ACTIVE, SLUG
    ACTIVE = VARIANTS[name]
    SLUG = ACTIVE["slug"]


def measure_inter(trials):
    """Run the canonical delay_lab engine on the active variant's list and inject the
    measurement into pg.MEASURED + pg.PROTECT (the promoted-deck harvest path). Must run
    BEFORE gauntlet()/tiers() so both synthesis oracles read it."""
    dlab = _load("delay_lab")
    index = dlab.ds.load_oracle_index()
    aliases = dlab.ds.load_reskin_aliases()
    lib, _ = dlab.slc.load_parsed(ACTIVE["deck"], index, aliases, warn=False)
    dlab.check_names(SLUG, lib, ACTIVE["spec"])
    comp = dlab.simulate(SLUG, lib, ACTIVE["spec"], trials, random.Random(dlab.SEED), 0.5)
    rows = {k: [round(100.0 * comp[k][a][0] / trials, 1) for a in dlab.A_SWEEP]
            for k in (6, 7)}
    pg.MEASURED[SLUG] = rows
    pg.PROTECT[SLUG] = WS_PROTECT
    # tier_list's interaction oracle reads a SECOND pod_gauntlet instance (im loads its
    # own copy) — inject there too, or im.interact_at KeyErrors on the merged slug.
    tl.im.pg.MEASURED[SLUG] = rows
    tl.im.pg.PROTECT[SLUG] = WS_PROTECT
    print(f"\n  injected pg.MEASURED[{SLUG}]: T6 {rows[6]} / T7 {rows[7]}"
          f"\n  (drawn, a-grid {dlab.A_SWEEP}) + pg.PROTECT {WS_PROTECT} — gauntlet now"
          f"\n  uses MEASURED disruption (not the 'warn' bucket) and the tier's"
          f"\n  interaction axis is real (not '—'/injected).")
    return rows


def inject(keep_earthbend):
    """Add the active variant's entry to pg.CLOCKS + a defense spec to dl.ROSTER.
    Optionally drop earthbend (the retired seat). Returns nothing — mutates the
    imported modules."""
    pg.CLOCKS[SLUG] = ACTIVE["entry"]
    dl.ROSTER[SLUG] = (ACTIVE["deck"].name, _defense_spec(ACTIVE["spec"]))
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
    src = ("MEASURED delay_lab disruption + PROTECT" if SLUG in pg.MEASURED
           else "the (conservative 'warn') disruption bucket")
    print(f"\n  merged places #{r} of {len(rows)} on P(WIN). PURE RACE is the data-backed"
          f"\n  front edge; P(WIN) folds in {src}.")


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


# combat-OFF clocks per variant slug (ws_clock_lab --mode comboclock --deck <list> @40k)
# — the decap curve with plain combat fully answered, i.e. the over-the-flying-wall kill.
OVER_CDF = {
    "world_shapers_merged":                                            # 2026-07-05
        ([5, 6, 7, 8, 9, 10, 12, 14, 16], [0, 1, 3, 8, 18, 34, 70, 89, 96]),
    "world_shapers_tuned":       # 2026-07-05, AFTER the EXTRA_COMMANDERS registry fix
        ([5, 6, 7, 8, 9, 10, 12, 14, 16], [0, 1, 3, 7, 16, 32, 68, 88, 96]),
}


def dragon(trials, seed):
    """Inject the active variant into vs_dragon_roster_lab (axis=over, combat-off
    clock) and rank it against the roster + the retiring Earthbend seat."""
    if SLUG not in OVER_CDF:
        raise SystemExit(f"--dragon: no combat-off clock harvested for {SLUG} — run "
                         f"ws_clock_lab --mode comboclock --deck {ACTIVE['deck']} "
                         f"and add the decap curve to OVER_CDF")
    vd = _load("vs_dragon_roster_lab")
    decks = vd.build_decks(trials)
    lib, _ = vd.core.load_parsed(ACTIVE["deck"], vd.ds.load_oracle_index(),
                                 vd.ds.load_reskin_aliases(), warn=False)
    tk = vd.classify([nm for nm, _ in lib])
    decks[SLUG] = dict(
        slug=SLUG, name=ACTIVE["entry"]["name"], axis="over", race=False,
        note="COMBAT-OFF clock: drain ~40% / Mazirek ~18% / slug+AWBO+Purphoros ~27% — board-independent",
        protect=0.0, toolkit=tk, F=vd.build_cdf(*OVER_CDF[SLUG]), **vd.cap_counts(tk))

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
    ap.add_argument("--measure-inter", action="store_true",
                    help="MEASURE the merged deck's interaction via the delay_lab engine "
                         "(injects pg.MEASURED + pg.PROTECT; supersedes --inter)")
    ap.add_argument("--tuned", action="store_true",
                    help="place the interaction+manabase TUNED variant "
                         "(world-shapers-tuned-20260704) instead of the base merged list")
    ap.add_argument("--variant", choices=list(VARIANTS), default=None,
                    help="which World Shapers list to place (merged/tuned/external); "
                         "--tuned is kept as an alias for --variant tuned")
    ap.add_argument("--dragon", action="store_true",
                    help="rank the active variant in the vs-Ur-Dragon roster model "
                         "(needs a combat-off clock in OVER_CDF)")
    args = ap.parse_args()
    select_variant(args.variant or ("tuned" if args.tuned else "merged"))
    if args.dragon:
        dragon(args.trials, args.seed)
        return
    inject(args.keep_earthbend)
    if args.measure_inter:
        measure_inter(args.trials)
    gauntlet(args.trials, args.seed)
    tiers(args.trials, args.seed, args.keep_earthbend, inter=args.inter)


if __name__ == "__main__":
    main()
