#!/usr/bin/env python3
"""wb_rebuild_vs_dragon.py — does a Witherbloom TOKEN-COMBO + FOG rebuild beat the
current Zero-Sum (70%) vs the Ur-Dragon fair-board deck, and how close to Glarb (94%)?

Alex's #2 (2026-06-16): rebuild Witherbloom around the token-infinite as the PRIMARY
plan, accepting board-dependence (Ur-Dragon plays no wipes -> rock-paper-scissors). The
vs_dragon model's lever is SURVIVAL (fogs/wraths) to reach the over-axis kill, not the
combo. This races three lists through vs_dragon_roster_lab.simulate (default priors +
sweep), reusing zero_sum's over/decap clock for the token over-kill (~T9 per wb_raid_lab):

  base zero_sum       — current list (the 70% reference)
  zero_sum + fogs     — base + Spore Frog/Constant Mists/Darkness (ISOLATES the fog lever)
  tokens-rebuild      — decks/considering/witherbloom-tokens-rebuild-20260616.txt
  Glarb (calamity)    — the deployed anti-fair specialist (94% reference)

over-axis + race=False are correct for all (drain/lifeloop = board-independent). Clock is
reused (the token over-kill is ~T9, same as the lifeloop); toolkit is oracle-classified
from each list. HEURISTIC — trust the deltas and the ranking, not the second decimal.
"""
import argparse
import importlib.util
import json
import random
from pathlib import Path

ROOT = Path(__file__).parent.parent
_s = importlib.util.spec_from_file_location("vsd", ROOT / "scripts" / "vs_dragon_roster_lab.py")
V = importlib.util.module_from_spec(_s); _s.loader.exec_module(V)

DEFAULTS = dict(trials=20000, seed=20260615, dmg_base=16, dmg_step=7, rebuild=1,
                reset_mult=0.70, kill_disrupt=0.15, maze_block=8, maze_online=0.55,
                removal_block=7, draw=0.58, p_act=0.70, p_connect=0.22,
                connect_decay=0.5, tax_block=0.25, life_per_gain=2, life_cap=12,
                race_delay=0, dragon_fast=False, dragon_slow=False)
ARGS = argparse.Namespace(**DEFAULTS)

V.load_oracle()
index = V.ds.load_oracle_index(); aliases = V.ds.load_reskin_aliases()
clocks = json.loads(V.CLOCKS_JSON.read_text(encoding="utf-8"))


def names_of(path):
    lib, _ = V.core.load_parsed(ROOT / path, index, aliases, warn=False)
    return [nm for nm, _ in lib]


def record(names, clock_slug="zero_sum_game", axis="over", race=False,
           protect_slug="zero_sum_game"):
    tk = V.classify(names)
    return dict(slug="custom", name="custom", axis=axis, race=race,
                protect=V.PG.PROTECT.get(protect_slug, 0.0), toolkit=tk,
                F=V.kill_cdf(clock_slug, clocks), **V.cap_counts(tk))


ZS = names_of(V.DECKS["zero_sum_game"])
GLARB = names_of(V.DECKS["calamity_tax"])
REBUILD = names_of("decks/considering/witherbloom-tokens-rebuild-20260616.txt")

DECKS = {
    "base zero_sum (ref 70%)": record(ZS),
    "zero_sum + 3 fogs": record(ZS + ["Spore Frog", "Constant Mists", "Darkness"]),
    "tokens-rebuild": record(REBUILD),
    # Glarb: its own grind clock + axis=over (Torment), protect from its slug
    "Glarb / Calamity (ref 94%)": record(GLARB, clock_slug="calamity_tax",
                                         protect_slug="calamity_tax"),
}

SCEN = [("baseline", {}), ("go-live FAST", dict(_kd="fast")),
        ("go-live SLOW", dict(_kd="slow")),
        ("hyper-aggro 22+9", dict(dmg_base=22, dmg_step=9)),
        ("dragons gain life", dict(race_delay=2))]


def kd_for(tag):
    if tag == "fast":
        return {5: 0.15, 6: 0.35, 7: 0.32, 8: 0.13, 9: 0.05}
    if tag == "slow":
        return {7: 0.25, 8: 0.35, 9: 0.25, 10: 0.15}
    return dict(V.G_DIST)


print("=" * 92)
print("WITHERBLOOM TOKEN-REBUILD vs UR-DRAGON — P(win), default priors + sweep "
      f"(trials={ARGS.trials})")
print("=" * 92)
print(f"  {'deck':28}{'fog':>4}{'wr':>3}{'life':>5}{'spot':>5}{'maze':>5}"
      + "".join(f"{s[0][:9]:>10}" for s in SCEN))
for label, d in DECKS.items():
    tk = d["toolkit"]
    cells = []
    for _, ov in SCEN:
        ov = dict(ov); tag = ov.pop("_kd", None)
        P = V.params(ARGS, **ov)
        rng = random.Random(ARGS.seed + 7)
        cells.append(V.simulate(d, d["F"], kd_for(tag), P, rng))
    print(f"  {label:28}{d['nfog']:>4}{d['nwr']:>3}{d['nlife']:>5}{d['nspot']:>5}"
          f"{('Y' if d['maze'] else '-'):>5}"
          + "".join(f"{c*100:>9.0f}%" for c in cells))

print("\n  toolkit (oracle-classified):")
for label, d in DECKS.items():
    tk = d["toolkit"]
    print(f"    {label:28} fogs={tk['fogs']}  wraths={tk['wraths'][:4]}")
