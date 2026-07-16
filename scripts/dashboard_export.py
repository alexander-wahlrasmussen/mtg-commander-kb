#!/usr/bin/env python3
"""dashboard_export.py — bake the dashboard's sim results to static JSON.

Precompute a grid of scenarios so the React app can run with NO Python backend
(deploy ui/dist to GitHub Pages / Netlify and view it on a phone).
Reuses dashboard_server's compute_* functions — the SAME engine the live API
serves — so static and live are identical, just precomputed vs on-demand.

Writes:
    dashboard/data/clocks.json         (the harvested CDFs — already static)
    dashboard/data/gauntlet.json       keyed "pod|strict|a"
    dashboard/data/locks.json          keyed "pod|strict|a|r"
    dashboard/data/championship.json   keyed "tgrind|swapped"
    dashboard/data/manifest.json       the baked axis values (front-end snaps to these)

The front-end auto-detects data/manifest.json and switches to static mode; sliders
snap to the baked axes and precision/unbaked controls lock. Re-bake after any deck
or engine change. The Locks grid is the expensive part (it measures availability
per deck×lock) — tune LOCKS_* below if the bake is too slow.

Usage:
    python scripts/dashboard_export.py
"""
import argparse
import importlib.util
import json
import shutil
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "dashboard" / "data"
UI_OUT = ROOT / "ui" / "public" / "data"   # the React build reads its baked JSON here too
ORACLE_CARDS = ROOT / "collection" / "oracle-cards.json"   # heavy Scryfall dump (locks step only)

for _s in (sys.stdout, sys.stderr):
    if hasattr(_s, "reconfigure"):
        try:
            _s.reconfigure(encoding="utf-8", errors="replace")
        except (ValueError, OSError):
            pass


def _load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ds = _load("dashboard_server")            # compute_gauntlet/clocks/lock_sweep/championship
mt = _load("mulligan_trainer")            # baked mulligan-drill hands (static, no backend)
MULLIGAN_HANDS = 40                       # opening hands baked per deck for the drill

# ---- baked grids (regular so the sliders land exactly on baked values) ------
GAUNTLET_A = [round(i * 0.05, 2) for i in range(0, 21)]   # 0.00 .. 1.00 step .05 (matches slider)
GAUNTLET_POD = ["fast", "base", "slow"]
GAUNTLET_STRICT = [False, True]
GAUNTLET_TRIALS = 20000

LOCKS_A = [0.0, 0.15, 0.30, 0.45, 0.60, 0.75]   # step .15, includes baseline .30
LOCKS_R = [0.0, 0.25, 0.50, 0.75]               # step .25, includes baseline .25
LOCKS_POD = ["base"]
LOCKS_STRICT = [False]                          # decap only (the headline; table doubles the bake)
LOCKS_TRIALS = 2000

CHAMP_TGRIND = list(range(6, 15))               # 6..14 (matches slider)
CHAMP_SWAPPED = [False, True]
CHAMP_TRIALS = 20000
CHAMP_SEASON = 40000
CHAMP_DRAWS = 8                                  # sample random draws baked per key (Re-draw cycles them)

MATCHUP_STRICT = [False, True]                  # decap / table
MATCHUP_TRIALS = 20000

GSEED, LSEED, CSEED = 20260614, 20260614, ds.sm.SEED


def k_strict(b):
    return 1 if b else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--content", action="store_true",
                    help="bake ONLY the content + deck pages (skip the sim grids); merges into the "
                         "existing manifest. Use after a KB-content change (e.g. a Summary edit) "
                         "to refresh deck pages without re-running gauntlet/championship/locks.")
    ap.add_argument("--grids", action="store_true",
                    help="bake ONLY the sim grids (clocks/gauntlet/championship/locks); skip content.")
    args = ap.parse_args()
    # default (neither flag) = both, matching the original behaviour.
    do_grids = not (args.content and not args.grids)
    do_content = not (args.grids and not args.content)

    OUT.mkdir(parents=True, exist_ok=True)
    decks_dir = OUT / "decks"
    t0 = time.time()
    slugs = []

    if do_grids:
        # clocks — already static
        print("clocks ...", end="", flush=True)
        (OUT / "clocks.json").write_text(json.dumps(ds.compute_clocks()), encoding="utf-8")
        print(" done")

        # gauntlet
        g = {}
        total = len(GAUNTLET_POD) * len(GAUNTLET_STRICT) * len(GAUNTLET_A)
        n = 0
        for pod in GAUNTLET_POD:
            for strict in GAUNTLET_STRICT:
                for a in GAUNTLET_A:
                    g[f"{pod}|{k_strict(strict)}|{a:.2f}"] = ds.compute_gauntlet(
                        a=a, pod=pod, strict=strict, trials=GAUNTLET_TRIALS, seed=GSEED)
                    n += 1
                    print(f"\rgauntlet {n}/{total} ...", end="", flush=True)
        (OUT / "gauntlet.json").write_text(json.dumps(g), encoding="utf-8")
        print(" done")

        # championship
        c = {}
        total = len(CHAMP_TGRIND) * len(CHAMP_SWAPPED)
        n = 0
        for tg in CHAMP_TGRIND:
            for sw in CHAMP_SWAPPED:
                c[f"{tg}|{k_strict(sw)}"] = ds.compute_championship(
                    trials=CHAMP_TRIALS, season_trials=CHAMP_SEASON, t_grind=tg, swapped=sw,
                    seed=CSEED, draw_seed=CSEED, n_draws=CHAMP_DRAWS)
                n += 1
                print(f"\rchampionship {n}/{total} ...", end="", flush=True)
        (OUT / "championship.json").write_text(json.dumps(c), encoding="utf-8")
        print(" done")

        # matchup matrix — deck × measured opponent (cheap: 2 scenarios)
        mu = {f"{k_strict(s)}": ds.compute_matchup(strict=s, trials=MATCHUP_TRIALS, seed=GSEED)
              for s in MATCHUP_STRICT}
        (OUT / "matchup.json").write_text(json.dumps(mu), encoding="utf-8")
        print("matchup ... done")

        # locks (the expensive one — measures availability per deck×lock). Needs the heavy
        # Scryfall oracle dump; if it's absent, skip and keep the existing locks.json rather
        # than aborting the whole bake (everything else above doesn't need the oracle data).
        if not ORACLE_CARDS.is_file():
            print(f"locks ... SKIPPED — {ORACLE_CARDS.relative_to(ROOT)} missing "
                  f"(run scripts/update_scryfall_data.py to refresh locks); keeping existing locks.json")
        else:
            lk = {}
            total = len(LOCKS_POD) * len(LOCKS_STRICT) * len(LOCKS_A) * len(LOCKS_R)
            n = 0
            for pod in LOCKS_POD:
                for strict in LOCKS_STRICT:
                    for a in LOCKS_A:
                        for r in LOCKS_R:
                            lk[f"{pod}|{k_strict(strict)}|{a:.2f}|{r:.2f}"] = ds.compute_lock_sweep(
                                a=a, r=r, strict=strict, trials=LOCKS_TRIALS, pod=pod, seed=LSEED)
                            n += 1
                            print(f"\rlocks {n}/{total} (slow) ...", end="", flush=True)
            (OUT / "locks.json").write_text(json.dumps(lk), encoding="utf-8")
            print(" done")

    if do_content:
        # content pages (KB markdown / CSV / Scryfall — single payloads, no scenario grid)
        print("content ...", end="", flush=True)
        roster = ds.compute_roster()
        (OUT / "roster.json").write_text(json.dumps(roster), encoding="utf-8")
        (OUT / "wishlist.json").write_text(json.dumps(ds.compute_wishlist()), encoding="utf-8")
        (OUT / "collection.json").write_text(json.dumps(ds.compute_collection()), encoding="utf-8")
        (OUT / "home.json").write_text(json.dumps(ds.compute_home(GSEED)), encoding="utf-8")
        (OUT / "tierlist.json").write_text(json.dumps(ds.compute_tierlist(
            trials=40000, t_grind=ds.sm.T_GRIND, tax=ds.tl.im.TAX, seed=ds.sm.SEED, legacy=False)),
            encoding="utf-8")
        # Doctor board — vitals ON at bake time (the MC smoothness facts are too slow
        # for the live default). check_build stays off inside compute_doctor: the baked
        # payload is public, no ownership data.
        (OUT / "doctor.json").write_text(json.dumps(ds.compute_doctor(vitals=True)),
                                         encoding="utf-8")
        # Auto-Brewer leaderboard — a pure reshape of the already-baked
        # analysis/autobrew/ sweep (no bulk, no network). Skip (don't abort the
        # whole content bake) if the sweep was never run.
        try:
            (OUT / "autobrew.json").write_text(json.dumps(ds.compute_autobrew()),
                                               encoding="utf-8")
        except FileNotFoundError as e:
            print(f"\n  autobrew ... SKIPPED — {e}")
        decks_dir.mkdir(exist_ok=True)
        slugs = [d["slug"] for d in roster["decks"]]
        for slug in slugs:
            page = ds.compute_deck(slug)
            # Bake the mulligan drill here (not in the live compute_deck path): it loads the
            # Scryfall bulk + sims hands, too heavy for a per-request server hit. Verdicts are
            # the authoritative keep_hand, computed once and baked (no client-side re-impl).
            page["mulligan"] = mt.bake_hands(slug, n=MULLIGAN_HANDS, seed=0)
            # Hover previews for the drill too: hand names come from the sim's own parse
            # and can differ in spelling from the .txt keys already in page["images"].
            if page.get("mulligan") and page.get("images"):
                hand_names = {c["n"] for h in page["mulligan"]["hands"] for c in h["cards"]}
                page["images"].update(
                    ds.kb.card_images(sorted(hand_names - set(page["images"]))))
            (decks_dir / f"{slug}.json").write_text(json.dumps(page), encoding="utf-8")
        print(f" done ({len(slugs)} deck pages)")

    # manifest — MERGE so a partial bake (--content / --grids) doesn't clobber the other
    # half's axes. A full run rewrites every field as before.
    manifest_path = OUT / "manifest.json"
    manifest = {}
    if manifest_path.is_file():
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (ValueError, OSError):
            manifest = {}
    manifest["generated"] = time.strftime("%Y-%m-%d %H:%M")
    if do_grids:
        manifest.update(dict(
            clocks=True,
            gauntlet=dict(pod=GAUNTLET_POD, strict=[0, 1], a=GAUNTLET_A, trials=GAUNTLET_TRIALS),
            locks=dict(pod=LOCKS_POD, strict=[k_strict(s) for s in LOCKS_STRICT],
                       a=LOCKS_A, r=LOCKS_R, trials=LOCKS_TRIALS),
            championship=dict(t_grind=CHAMP_TGRIND, swapped=[0, 1],
                              trials=CHAMP_TRIALS, season_trials=CHAMP_SEASON, draws=CHAMP_DRAWS),
            matchup=dict(strict=[k_strict(s) for s in MATCHUP_STRICT], trials=MATCHUP_TRIALS),
        ))
    if do_content:
        manifest["content"] = dict(roster=True, home=True, wishlist=True,
                                   collection=True, tierlist=True, doctor=True,
                                   autobrew=(OUT / "autobrew.json").is_file(),
                                   decks=slugs)
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    # mirror the whole bake into the React app's public/data (its static fallback)
    UI_OUT.mkdir(parents=True, exist_ok=True)
    (UI_OUT / "decks").mkdir(exist_ok=True)
    for p in OUT.glob("*.json"):
        shutil.copy2(p, UI_OUT / p.name)
    if decks_dir.is_dir():
        for p in decks_dir.glob("*.json"):
            shutil.copy2(p, UI_OUT / "decks" / p.name)

    sizes = {p.name: p.stat().st_size for p in sorted(OUT.glob("*.json"))}
    print(f"\nwrote {len(sizes)} files (+{len(slugs)} deck pages) to "
          f"{OUT.relative_to(ROOT)} (mirrored to {UI_OUT.relative_to(ROOT)}) in {time.time()-t0:.0f}s")
    for name, sz in sizes.items():
        print(f"  {name:22} {sz/1024:6.1f} KB")


if __name__ == "__main__":
    main()
