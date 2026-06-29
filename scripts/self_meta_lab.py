#!/usr/bin/env python3
"""self_meta_lab.py — quantify the self-meta ranking (roster as its own field).

`campaigns/Self_Meta_Ranking.md` answers the inverse of the Pod Gauntlet: not "which
deck beats the external T6-7 combo" but "if a 4-player pod were drawn from MY OWN decks,
which deck wins?" That doc is **explicit judgment** — "there is no multiplayer rules-engine
sim ... and I won't fake one." This lab quantifies the part that IS measurable and
DECOMPOSES how much of the ranking rests on the unmeasured rest — the same discipline the
gauntlet used for anti-pod (measured race + soft disruption).

THE SELF-META WIN CONDITION (from that doc): close all three other seats AND outlast. Its
three reward axes: (1) CONVERGE — a hit-all kill closes a 3-seat table far faster than
focus-fire (so the TABLE clock, not decap, is the metric); (2) DURABILITY / inevitability —
survive the grind; (3) OPPONENT-FED engines that scale in a spell-dense field.

THE MODEL — random 4-seat pods drawn from the 16 active decks, Monte Carlo:
  * each seat samples a TABLE-close turn from its lab table CDF (pod_gauntlet_clocks.json;
    HORIZON+1 = "never closes in horizon").
  * CLOSE-RACE (measured): if the earliest table-close among the 4 seats is <= T_grind, that
    seat wins (it actively closes the table first). Pure lab table clocks — no judgment.
  * GRIND fallback (soft): if NO seat closes by T_grind (a true stall), the most DURABLE seat
    wins — it outlasts and mops up. This is the "fortress" path the race can't score.
  P(win | in a random pod) is tallied per deck, plus CLOSE-RACE-only (durability off) so the
  two are stated separately.

DURABILITY index (0-1, the SOFT axis — documented, swept):
    durability = W_INEV*(1 - table_never%) + W_DEF*min(1, defense/DEF_NORM) + W_FED*opp_fed
  * inevitability = 1 - table_never% (lab): do you EVER close the table? A high never% means
    "survives but can't close" — the lab's check on the doc's generous "inevitability".
  * defense = count of R (instant removal) + P (sweepers/edicts) answers, READ FROM the
    delay_lab roster suites (already authored + oracle-verified 2026-06-15). Counters (C)
    are one-shot and don't buy grind survival, so they're excluded.
  * opp_fed = opponent-fed engine bonus. Dark Lord's Army (Sauron amasses on their spells;
    Sheoldred / Underworld Dreams / Bowmasters drain on their draws) is the clear case; others
    omitted as minor (Esper Sentinel / Mystic Remora are card-tax, not win engines).

HONESTY (gauntlet discipline): the CLOSE-RACE is lab-measured; the DURABILITY overlay and
T_grind are documented judgment, SWEPT. Trust the decomposition (how much a deck leans on the
soft overlay), not the second decimal. Still not a 4-body rules engine — no politics, no
focus-fire targeting, no combat math; "most durable outlasts" is an abstraction.

Writeup: analysis/Self_Meta_Quantified_2026-06-15.md
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


pg = _load("pod_gauntlet")           # clocks (table CDFs), build_cdf, sample_kill, HORIZON
dl = _load("delay_lab")              # ROSTER answer suites -> defense counts

SEED = 20260615
T_GRIND = 10                         # earliest table-close > this = a true grind -> durability decides
W_INEV, W_DEF, W_FED = 0.50, 0.35, 0.15
DEF_NORM = 8.0                       # ~8 R/P answers = saturated defense
OPP_FED = {"dark_lords_army": 1.0}   # Sauron shell; others minor, omitted (documented)

# judgment tiers from Self_Meta_Ranking.md, for the Δrank comparison column. This is the doc's
# REASONED ranking (an independent baseline), so it's deliberately a SUBSET of the sim roster:
# croak_and_dagger inherits #7 from the renamed Calamity Tax (same deck, the lands/graveyard
# re-role only deepened its Tier-3 "durable but can't close" profile), and forced_liquidation
# (the new Kefka build) is intentionally ABSENT — the doc predates it, so its Δrank shows "—"
# rather than a fabricated judgment (the model measures it ~#4, suggesting Tier 2 when judged).
JUDGMENT = {
    "dark_lords_army": 1, "radiation_sickness": 2, "genome_project": 3, "lightning_war": 4,
    "zero_sum_game": 5, "grand_design": 6, "croak_and_dagger": 7, "lorehold_spirits": 8,
    "diminishing_returns": 9, "curse_of_the_scarab": 10, "exiles_return": 11,
    "earthbend_the_meta": 12, "replication_crisis": 13, "eldrazi_stampede": 14,
    "bumbleflower": 15, "crystal_sickness": 16,
}
# Guard (2026-06-29 audit): a JUDGMENT key that isn't in the live roster is a dead anchor — the
# Calamity->Croak rename left "calamity_tax" pointing Δrank at a deck no longer simmed. The dict
# may be a subset (new decks unranked) but must never name a slug outside delay_lab.ROSTER.
assert set(JUDGMENT) <= set(dl.ROSTER), (
    f"self_meta JUDGMENT names retired slug(s): {set(JUDGMENT) - set(dl.ROSTER)}")


def defense_counts():
    """#(instant removal + sweeper/edict) answers per deck, from the delay_lab roster suites
    (oracle-verified 2026-06-15). Counters excluded — one-shot, don't buy grind survival."""
    out = {}
    for slug, (_fname, spec) in dl.ROSTER.items():
        out[slug] = sum(1 for cls, _cost, _tags in spec["answers"].values()
                        if cls & {"R", "P"})
    return out


def durability(slug, clocks, defense):
    never_table = clocks[slug]["never"][1] / 100.0
    inev = 1.0 - never_table
    dfn = min(1.0, defense.get(slug, 0) / DEF_NORM)
    fed = OPP_FED.get(slug, 0.0)
    return max(0.0, min(1.0, W_INEV * inev + W_DEF * dfn + W_FED * fed))


def run(args):
    rng = random.Random(args.seed)
    C = pg.merged_clocks()
    slugs = [s for s in dl.ROSTER if s in C]          # the 16 active decks
    tcdf = {s: pg.build_cdf(C[s]["grid"], C[s]["table"]) for s in slugs}
    defense = defense_counts()
    dura = {s: durability(s, C, defense) for s in slugs}

    win = {s: 0.0 for s in slugs}                      # combined (race + grind fallback)
    race = {s: 0.0 for s in slugs}                     # close-race only (durability off)
    appear = {s: 0 for s in slugs}
    NSEAT = 4
    for _ in range(args.trials):
        pod = rng.sample(slugs, NSEAT)
        for s in pod:
            appear[s] += 1
        turns = {s: pg.sample_kill(tcdf[s], rng) for s in pod}   # table-close turn per seat
        tmin = min(turns.values())
        # --- close-race winner (measured): earliest table-close, ties shared ---
        if tmin <= pg.HORIZON:
            earliest = [s for s in pod if turns[s] == tmin]
            for s in earliest:
                race[s] += 1.0 / len(earliest)
        # --- combined: race if someone closes by T_grind, else most-durable outlasts ---
        if tmin <= args.t_grind:
            champs = [s for s in pod if turns[s] == tmin]
        else:
            dmax = max(dura[s] for s in pod)
            champs = [s for s in pod if abs(dura[s] - dmax) < 1e-9]
        for s in champs:
            win[s] += 1.0 / len(champs)

    rows = []
    for s in slugs:
        a = appear[s] or 1
        rows.append((s, C[s]["name"], 100.0 * win[s] / a, 100.0 * race[s] / a,
                     dura[s], C[s]["med"][1], C[s]["never"][1], defense.get(s, 0)))
    rows.sort(key=lambda r: -r[2])

    print(f"\n{'='*100}\nSELF-META — P(win | in a random 4-seat pod of your own decks)   "
          f"[T_grind={args.t_grind} · trials={args.trials}]")
    print("  CLOSE = measured table-clock race (earliest closer wins). WIN = + grind fallback")
    print("  (if nobody closes by T_grind, most DURABLE outlasts). dura = soft index (0-1).\n")
    print(f"  {'#':>2} {'deck':24}{'table':>7}{'never':>6}{'def':>5}{'dura':>6}"
          f"{'CLOSE':>7}{'WIN':>6}  {'judg':>5}  Δrank")
    for i, (s, name, w, rc, d, med, nev, dfn) in enumerate(rows, 1):
        j = JUDGMENT.get(s, 0)
        drank = f"{j - i:+d}" if j else "  —"
        print(f"  {i:>2} {name:24}{med:>7}{nev:>5}%{dfn:>5}{d:>6.2f}{rc:>6.0f}%{w:>5.0f}%"
              f"  {('#'+str(j)) if j else '—':>5}  {drank}")
    print(f"\n  weights W_inev/def/fed={W_INEV}/{W_DEF}/{W_FED}; defense from delay_lab R+P "
          f"answers; opp-fed={list(OPP_FED)}.")
    print("  CLOSE is lab-measured (table clocks). WIN folds in the soft durability overlay.")
    print("  Read the CLOSE→WIN gap (how much a deck leans on durability not closing) and Δrank")
    print("  vs the judgment tiers. Sweep --t-grind to see the race↔grind crossover.")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--trials", type=int, default=80000)
    ap.add_argument("--seed", type=int, default=SEED)
    ap.add_argument("--t-grind", type=int, default=T_GRIND,
                    help="earliest table-close > this = grind -> durability decides")
    args = ap.parse_args()
    run(args)


if __name__ == "__main__":
    main()
