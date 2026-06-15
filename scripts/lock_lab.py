#!/usr/bin/env python3
"""lock_lab.py — the persistent-lock availability lab (the honest "opponent-clock tax").

WHY THIS LAB EXISTS. pod_gauntlet.py's load-bearing limitation #1 is "no opponent-clock
tax": every deck races the SAME fixed combo-turn K, so decks that SLOW the pod are
underrated. The intended fix was a mana-tax (Sphere/Thalia) accumulator. But an audit
of all 16 active decklists (2026-06-15, grep + full read + oracle verification) found
the roster runs ESSENTIALLY NO mana-tax stax — and the deck whose "Favoured" verdict
this was meant to rescue, Calamity Tax, has ZERO tax/lock pieces (its "Tax" is the
Torment-of-Hailfire LIFE drain, not a Sphere). So the real axis is not mana-tax; it is
PERSISTENT LOCKS — a static that, once in play, stops the pod EVERY turn until removed.

THE MODEL (vs delay_lab's one-shot D). delay_lab and the gauntlet treat disruption as
ONE-SHOT: an answer stops one combo attempt and is re-rolled next turn (so over n turns a
deck holds with prob D^n — leaky). A persistent lock is different: once live and effective
it holds D≈1 every turn until the pod removes it. That distinction is exactly limitation
#1 ("their real edge is making K=10+"), modelled honestly. This lab measures the input the
gauntlet's --lock race needs: P(a hard-lock is live by turn t), per deck, from the actual
list. The race itself (lock-aware) lives in pod_gauntlet.lock_race.

TWO STATIC KINDS (oracle text verified 2026-06-15 against collection/oracle-cards.json):

  HARD-LOCK  while live & unremoved the pod can't combo (prob e = does it stop THIS pod's
             line). Cursed Totem, Rule of Law / Eidolon / Archon, Drannith, Linvala,
             Deafening Silence, (Opposition Agent / Aven Mindcensor = softer tutor-locks).
  MANA-TAX   while live, adds tau mana to the pod's combo turn -> shifts K by tau/g (the
             pod's mana growth). Sphere of Resistance, Trinisphere, Damping Sphere, and
             Esper Sentinel (negligible: first noncreature spell only, ~1 mana, payable).

EXCLUDED, and WHY (named so the inventory's zeros are auditable, not silent):
  Teferi, Time Raveler  sorcery-speed lock — protects OUR interaction, does NOT stop a
                        main-phase combo. e~=0 as clock-tax (delay_lab says the same).
  Grand Abolisher       "during YOUR turn" — protect-own; the pod combos on THEIR turn.
  Notion Thief          draw-replacement punisher — value/anti-wheel, not a combo-stop.

THE POD (project_pod_combo_opponent + delay_lab): Ur-Dragon ramp shell +
Hidetsugu / Kairi / Kenrith / Kinnan. 3 of 4 win through ACTIVATED abilities, Kairi
through spells/triggers — which is why the e values below turn on creature-activation vs
spell vs commander-cast. These are COMMANDER-combo decks, so Drannith (cast-from-hand-only)
bites hard. e/tau are documented JUDGMENT (the delay_lab W_* convention), printed and swept.

CEILING CONVENTIONS (same as every lab). Availability is a DRAWN-and-CAST floor + a
generic-tutor ceiling; mana is a lands + a few ubiquitous rocks floor (mana is rarely the
binding constraint for a <=3-mana lock by T5-7 — DRAWING it is). A live lock != an
EFFECTIVE one (that's e) and != an UN-REMOVED one (that's the pod-removal-rate r, swept in
the gauntlet). Trust shapes/deltas, not the second decimal. HEURISTIC, not a rules engine.

Emits analysis/lock_availability.json (consumed by pod_gauntlet.py --lock, the same
lab->JSON->gauntlet pattern as pod_gauntlet_clocks.json).
Writeup: analysis/Opponent_Clock_Lock_Model_2026-06-15.md
"""
import argparse
import importlib.util
import json
import random
from pathlib import Path

_spec = importlib.util.spec_from_file_location(
    "speed_lab_core", Path(__file__).parent / "speed_lab_core.py")
core = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(core)
ds = core.ds
ROOT = Path(__file__).parent.parent

for _s in (__import__("sys").stdout, __import__("sys").stderr):
    if hasattr(_s, "reconfigure"):
        try:
            _s.reconfigure(encoding="utf-8", errors="replace")
        except (ValueError, OSError):
            pass

SEED = 20260615
GRID = [2, 3, 4, 5, 6, 7, 8]
MAXT = 9
LOCK_JSON = ROOT / "analysis" / "lock_availability.json"

# Generic mana floor: ubiquitous cheap rocks the lab auto-includes if the deck runs them.
# Mana is rarely binding for a <=3-cost lock by T5-7, so a small set suffices (DRAWING the
# lock dominates); kept minimal on purpose. name -> (cost, net mana output).
GENERIC_ROCKS = {"Sol Ring": (1, 2), "Mana Crypt": (0, 2), "Mana Vault": (1, 3),
                 "Arcane Signet": (2, 1), "Mind Stone": (2, 1), "Fellwar Stone": (2, 1),
                 "Chrome Mox": (0, 1), "Mox Diamond": (0, 1), "Talisman of Dominance": (2, 1),
                 "Dimir Signet": (2, 1), "Golgari Signet": (2, 1), "Izzet Signet": (2, 1)}

# Broad tutor set for the with-tutors ceiling (treated as able to fetch the lock, flat
# cost 2 — optimistic: they'd often rather tutor the combo/answer). Note, don't over-read.
TUTORS = {"Demonic Tutor", "Vampiric Tutor", "Diabolic Tutor", "Grim Tutor",
          "Mastermind's Acquisition", "Enlightened Tutor", "Idyllic Tutor",
          "Wishclaw Talisman", "Beseech the Mirror", "Fabricate", "Whir of Invention",
          "Trinket Mage", "Tribute Mage", "Drift of Phantasms"}
TUTOR_COST = 2

# --- the catalog: kind, cast cost, value (e for hardlock / tau for manatax), oracle note.
# Verified 2026-06-15 via the oracle dump (see module docstring for the pod model the e's
# are judged against). "excluded" entries score 0 and exist to make the inventory explicit.
HARDLOCK, MANATAX, EXCLUDED = "hardlock", "manatax", "excluded"
CATALOG = {
    "Cursed Totem": (HARDLOCK, 2, 0.50,
        "creature activated abilities can't be activated: stops Kenrith/Hidetsugu "
        "creature-activation, partial Kinnan (artifact mana), nil Kairi (spells); symmetric "
        "but free for spell/trigger kills"),
    "Linvala, Keeper of Silence": (HARDLOCK, 4, 0.50,
        "one-sided Cursed Totem on a 3/4 flyer (same shell coverage, no symmetry cost)"),
    "Rule of Law": (HARDLOCK, 3, 0.55,
        "each player one spell/turn: hard-stops Kairi spell-combo + slows all assembly; a "
        "resolved activation engine still loops"),
    "Eidolon of Rhetoric": (HARDLOCK, 3, 0.55, "Rule of Law on a 1/4 body"),
    "Archon of Emeria": (HARDLOCK, 3, 0.58,
        "Rule of Law + opponents' nonbasics enter tapped (extra tempo tax) + 2/3 flyer"),
    "Deafening Silence": (HARDLOCK, 1, 0.45,
        "one NONCREATURE spell/turn: combo pieces are mostly noncreature, creature lines slip"),
    "Drannith Magistrate": (HARDLOCK, 2, 0.60,
        "opponents cast only from hand: stops recasting their COMMANDER (the combo piece) + "
        "gy/exile casts; weaker once their commander has resolved"),
    "Opposition Agent": (HARDLOCK, 3, 0.40,
        "flash; hijacks their library searches: taxes tutor-reliant assembly; removable "
        "body, pre-assembled lines dodge (softer)"),
    "Aven Mindcensor": (HARDLOCK, 3, 0.25,
        "flash; tutors find top 4 only: soft tutor-tax, they still hit often"),

    "Sphere of Resistance": (MANATAX, 2, 2.0,
        "spells cost {1} more: ~2-3 extra mana across a multi-spell combo turn (modelled 2.0)"),
    "Trinisphere": (MANATAX, 3, 3.5,
        "each spell under 3 costs 3: brutal vs cheap dorks/rituals/tutors"),
    "Damping Sphere": (MANATAX, 2, 2.5,
        "escalating per-spell tax + shuts off 2+-mana lands (Coffers etc.)"),
    "Esper Sentinel": (MANATAX, 1, 0.3,
        "first noncreature spell/turn taxed by power(~1) and payable -> negligible; the "
        "roster's only mana-tax, and it's really a draw engine"),

    "Teferi, Time Raveler": (EXCLUDED, 3, 0.0,
        "sorcery-speed lock protects OUR interaction; does not stop a main-phase combo"),
    "Grand Abolisher": (EXCLUDED, 2, 0.0,
        "'during your turn' = protect-own; the pod combos on their turn"),
    "Notion Thief": (EXCLUDED, 4, 0.0,
        "draw-replacement punisher: anti-wheel value, not a combo stop"),
}

# slug -> decklist. The 16 active decks (pod_gauntlet CLOCKS slugs) + the Kefka build
# candidate (its whole pitch is the one anti-Abolisher lock-kill; it is not in the active
# gauntlet but is the deck this model most illuminates).
DECKS = {
    "genome_project":     "decks/the-genome-project-20260510.txt",
    "radiation_sickness": "decks/radiation-sickness-20260615.txt",
    "replication_crisis": "decks/the-replication-crisis-20260504-202914.txt",
    "lorehold_spirits":   "decks/lorehold-spirit-20260503-154449.txt",
    "earthbend_the_meta": "decks/earthbend-the-meta-20260404-075423.txt",
    "exiles_return":      "decks/the-exiles-return-20260417-194010.txt",
    "zero_sum_game":      "decks/zero-sum-game-20260611.txt",
    "curse_of_the_scarab": "decks/curse-of-the-scarab-20260510-215526.txt",
    "bumbleflower":       "decks/this-bunny-goes-to-market-20260404-080311.txt",
    "eldrazi_stampede":   "decks/eldrazi-stampede-chaos-20260306-133311.txt",
    "dark_lords_army":    "decks/the-dark-lords-army-20260417-211206.txt",
    "diminishing_returns": "decks/diminishing-returns-20260505.txt",
    "lightning_war":      "decks/lightning-war-20260614.txt",
    "grand_design":       "decks/the-grand-design-20260502.txt",
    "crystal_sickness":   "decks/crystal-sickness-20260322-152311.txt",
    "calamity_tax":       "decks/calamity-tax-20260405-061741.txt",
    "kefka":              "decks/considering/forced-liquidation-20260612.txt",
}
NAMES = {  # display names (match the gauntlet where they overlap)
    "genome_project": "The Genome Project", "radiation_sickness": "Radiation Sickness",
    "replication_crisis": "The Replication Crisis", "lorehold_spirits": "Lorehold Spirits",
    "earthbend_the_meta": "Earthbend the Meta", "exiles_return": "The Exile's Return",
    "zero_sum_game": "Zero-Sum Game", "curse_of_the_scarab": "Curse of the Scarab",
    "bumbleflower": "Ms. Bumbleflower", "eldrazi_stampede": "Eldrazi Stampede Chaos",
    "dark_lords_army": "The Dark Lord's Army", "diminishing_returns": "Diminishing Returns",
    "lightning_war": "Lightning War", "grand_design": "The Grand Design",
    "crystal_sickness": "Crystal Sickness", "calamity_tax": "The Calamity Tax",
    "kefka": "Kefka (Forced Liquidation, build)",
}


def inventory(lib):
    """Scan a parsed library against the catalog -> the deck's static package."""
    names = {nm for nm, _ in lib}
    pkg = {HARDLOCK: [], MANATAX: [], EXCLUDED: []}
    for nm in names:
        if nm in CATALOG:
            kind, cost, val, note = CATALOG[nm]
            pkg[kind].append((nm, cost, val, note))
    for k in pkg:
        pkg[k].sort(key=lambda x: x[1])
    return pkg


def measure(lib, pkg, trials, rng, use_tutors=False):
    """Monte-Carlo availability of the static package. Returns
    (hl_avail[t]%, tau_mean[t], online_turns[]) over GRID.

    hl_avail = P(>=1 hard-lock cast & live by turn t). tau_mean = E[live mana-tax by t].
    A lock must be DRAWN (or tutored, ceiling) and CAST (mana floor = lands + GENERIC_ROCKS
    present). online_turns is the per-trial first-hardlock-live turn (None if never)."""
    hl_names = {nm: cost for nm, cost, _v, _n in pkg[HARDLOCK]}
    mt = [(nm, cost, val) for nm, cost, val, _n in pkg[MANATAX]]
    present_rocks = {nm: GENERIC_ROCKS[nm] for nm, _ in lib if nm in GENERIC_ROCKS}
    hl_hits = [0] * (MAXT + 1)
    tau_sum = [0.0] * (MAXT + 1)
    online = []

    for _ in range(trials):
        g = core.Goldfish(lib, rng, rocks=present_rocks)
        hl_live = None
        tau_live = 0.0
        live_mt = set()
        per_turn_tau = [0.0] * (MAXT + 1)
        for T in range(1, MAXT + 1):
            g.begin_turn(T)
            g.deploy_rocks()
            # with-tutors ceiling: fetch the cheapest undrawn hard-lock if we hold a tutor
            if use_tutors and hl_live is None and hl_names:
                tut = next((t for t in TUTORS if g.has(t)), None)
                undrawn = [p for p in hl_names if not g.has(p)]
                if tut and undrawn and g.avail >= TUTOR_COST:
                    g.cast(tut, TUTOR_COST)
                    for p in sorted(undrawn, key=lambda p: hl_names[p]):
                        if g.fetch(p):
                            break
            # cast affordable hard-locks (cheapest first) -> record first live turn
            for nm in sorted(hl_names, key=lambda p: hl_names[p]):
                if hl_live is None and g.has(nm) and g.avail >= hl_names[nm]:
                    g.cast(nm, hl_names[nm])
                    hl_live = T
            # cast affordable mana-tax (they stack)
            for nm, cost, val in mt:
                if nm not in live_mt and g.has(nm) and g.avail >= cost:
                    g.cast(nm, cost)
                    live_mt.add(nm)
                    tau_live += val
            per_turn_tau[T] = tau_live
        online.append(hl_live)
        for t in range(1, MAXT + 1):
            if hl_live is not None and hl_live <= t:
                hl_hits[t] += 1
            tau_sum[t] += per_turn_tau[t]
    hl_avail = {t: 100.0 * hl_hits[t] / trials for t in GRID}
    tau_mean = {t: tau_sum[t] / trials for t in GRID}
    return hl_avail, tau_mean, online


def combined_e(pkg):
    """Best (max) hard-lock effectiveness in the package. Max not product: extra locks
    add REDUNDANCY (availability), but their shell coverage overlaps, so e doesn't stack."""
    return max((v for _, _, v, _ in pkg[HARDLOCK]), default=0.0)


def total_tau(pkg):
    """Mana-tax magnitudes add (they all raise the combo turn's mana)."""
    return sum(v for _, _, v, _ in pkg[MANATAX])


def med_online(online, trials):
    vals = sorted((o if o is not None else 99) for o in online)
    m = vals[len(vals) // 2]
    return f"T{m}" if m < 99 else "never"


def load(slug, index, aliases):
    lib, _ = core.load_parsed(ROOT / DECKS[slug], index, aliases, warn=False)
    return lib


def mode_roster(index, aliases, trials):
    print(f"\n{'='*100}\nLOCK LAB — persistent-lock availability per deck   trials={trials} seed={SEED}")
    print("  HL = hard-lock (stop-while-live), MT = mana-tax (tau). e = best hard-lock's "
          "P(stops THIS pod).")
    print("  avail@6/7 = P(a hard-lock is live by their combo turn), drawn-only (with-tutors).\n")
    print(f"  {'deck':34}{'HL':>3}{'MT':>3}{'e':>6}{'tau':>6}{'online':>8}"
          f"{'avail@6':>14}{'avail@7':>14}")
    out = {}
    rows = []
    for slug in DECKS:
        lib = load(slug, index, aliases)
        pkg = inventory(lib)
        d_av, d_tau, d_on = measure(lib, pkg, trials, random.Random(SEED))
        t_av, _t_tau, _ = measure(lib, pkg, trials, random.Random(SEED), use_tutors=True)
        e, tau = combined_e(pkg), total_tau(pkg)
        rows.append((slug, pkg, e, tau, d_av, t_av, d_tau, d_on))
        out[slug] = dict(
            name=NAMES[slug], grid=GRID,
            hl_drawn=[round(d_av[t], 1) for t in GRID],
            hl_tut=[round(t_av[t], 1) for t in GRID],
            tau=[round(d_tau[t], 2) for t in GRID],
            e=e, tau_total=round(tau, 2), median_online=med_online(d_on, trials),
            package=[dict(name=nm, kind=k, cost=c, val=v)
                     for k in (HARDLOCK, MANATAX, EXCLUDED)
                     for nm, c, v, _n in pkg[k]])
    # sort: decks with a real package first, by e then tau
    rows.sort(key=lambda r: (-(r[2] > 0 or r[3] > 0), -r[2], -r[3]))
    for slug, pkg, e, tau, d_av, t_av, _dt, d_on in rows:
        nhl, nmt = len(pkg[HARDLOCK]), len(pkg[MANATAX])
        a6 = f"{d_av[6]:.0f}% ({t_av[6]:.0f}%)" if nhl else "—"
        a7 = f"{d_av[7]:.0f}% ({t_av[7]:.0f}%)" if nhl else "—"
        on = med_online(d_on, trials) if nhl else "—"
        print(f"  {NAMES[slug]:34}{nhl:>3}{nmt:>3}{e:>6.2f}{tau:>6.1f}{on:>8}{a6:>14}{a7:>14}")
    print(f"\n  packages (HL hard-lock · MT mana-tax · EXCL excluded, scored 0):")
    for slug, pkg, *_ in rows:
        items = ([f"HL {nm}(e{v:.2f})" for nm, _c, v, _n in pkg[HARDLOCK]]
                 + [f"MT {nm}(τ{v:.1f})" for nm, _c, v, _n in pkg[MANATAX]]
                 + [f"EXCL {nm}" for nm, _c, _v, _n in pkg[EXCLUDED]])
        if items:
            print(f"    {NAMES[slug]:34} " + " · ".join(items))
    LOCK_JSON.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"\n  wrote {LOCK_JSON.relative_to(ROOT)} (consumed by pod_gauntlet.py --lock)")
    print("  HEADLINE: a deck with no HL/MT package is provably unchanged by the lock model "
          "(it falls back to\n  the gauntlet's one-shot D). The roster's only real persistent "
          "lock vs this pod is Kefka's Cursed Totem.")


def mode_whatif(index, aliases, trials):
    """What would adding each catalog hard-lock buy a lock-LESS deck? Availability here;
    the P(win) lift is pod_gauntlet.py --lock --add <slug>=<piece> (imports lock_lab)."""
    targets = ["calamity_tax", "diminishing_returns", "grand_design", "dark_lords_army"]
    adds = ["Cursed Totem", "Drannith Magistrate", "Rule of Law", "Sphere of Resistance",
            "Trinisphere", "Linvala, Keeper of Silence"]
    print(f"\n{'='*100}\nLOCK LAB — WHAT-IF: add one static to a lock-less deck   trials={trials}")
    print("  availability (drawn / with-tutors) of the injected piece by the pod's combo turn.")
    print("  P(win) lift is the gauntlet's job: python scripts/pod_gauntlet.py --lock "
          "--add <slug>=<piece>\n")
    print(f"  {'deck + add':52}{'kind':>9}{'online':>8}{'avail@6':>16}{'avail@7':>16}")
    for slug in targets:
        base = load(slug, index, aliases)
        for add in adds:
            kind, cost, val, _n = CATALOG[add]
            rec = index.get(add.lower())
            if rec is None:
                print(f"  {NAMES[slug]+' + '+add:52}  NOT IN ORACLE")
                continue
            lib = base + [(add, rec)]
            pkg = inventory(lib)
            d_av, d_tau, d_on = measure(lib, pkg, trials, random.Random(SEED))
            t_av, _tt, _ = measure(lib, pkg, trials, random.Random(SEED), use_tutors=True)
            if kind == HARDLOCK:
                a6 = f"{d_av[6]:.0f}% ({t_av[6]:.0f}%)"
                a7 = f"{d_av[7]:.0f}% ({t_av[7]:.0f}%)"
                on = med_online(d_on, trials)
                tag = f"HL e{val:.2f}"
            else:
                a6 = f"τ={d_tau[6]:.1f}"
                a7 = f"τ={d_tau[7]:.1f}"
                on = "—"
                tag = f"MT τ{val:.1f}"
            print(f"  {NAMES[slug]+' + '+add:52}{tag:>9}{on:>8}{a6:>16}{a7:>16}")
        print()


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--mode", choices=["roster", "whatif", "all"], default="roster")
    ap.add_argument("--trials", type=int, default=40000)
    args = ap.parse_args()
    index = ds.load_oracle_index()
    aliases = ds.load_reskin_aliases()
    if args.mode in ("roster", "all"):
        mode_roster(index, aliases, args.trials)
    if args.mode in ("whatif", "all"):
        mode_whatif(index, aliases, args.trials)


if __name__ == "__main__":
    main()
