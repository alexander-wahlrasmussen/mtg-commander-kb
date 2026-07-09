#!/usr/bin/env python3
"""vs_dragon_roster_lab.py — per-deck P(win vs the archenemy's Ur-Dragon fair-board
deck), COMPUTED for all 16 active decks (not archetype-judged).

WHY THIS EXISTS. `vs_dragon_lab.py` answered one question — does Glarb's anti-dragon
PACKAGE help (A/B, ~87% archetype, +2-3pp pkg). The Pod_Matchup_Matrix then carried an
*archetype-tiered* read of the rest of the roster ("grind = bring, race = walled"). That
tier table was JUDGMENT, and the repo's #1 lesson is that un-modelled judgments drift from
reality (7 of 8 hand-estimated clocks were falsified). This lab does the math per deck.

THE MATCHUP (project_ur_dragon_matchup, card text verified). Ur-Dragon is a FAIR board
deck: eminence cost-reduction + an attack trigger that draws + cheats a permanent per
attacking dragon -> a snowballing FLYING army. No combo turn K. So beating it is a
SURVIVAL RACE: stay alive (wraths reset the board, fogs skip an attack, Maze/tax blunt it,
lifegain buys life) until OUR kill lands — and crucially the kill must get THROUGH a flying
wall.

THE LOAD-BEARING AXIS (verified per deck from the kill lines, see KILL):
  over   = a board-independent kill (drain / burn / ping / mill / alt-win / lifeloop, or a
           combat kill with global evasion) that goes OVER the flying board. Lands on clock.
  combat = needs ground attackers to connect -> WALLED by dragon blockers; only lands in a
           window (pre-go-live or just after our own wrath; tapped-out attackers = p_connect).
This is the inversion: grind/over decks convert, combat racers get walled — and it cuts
against prior judgment (Grand Design's kill is "96% incremental COMBAT, almost no trample"
per its Summary -> WALLED here, not the "over-the-top Bring" the tier table called it).

WHAT'S MEASURED vs JUDGED (same discipline as every lab):
  MEASURED  - each deck's KILL CLOCK CDF (analysis/pod_gauntlet_clocks.json; the *_clock_lab
              suite). decap or table per deck per KILL[].cdf (a combat-decap deck that wins
              vs dragons only through its slow DRAIN uses the table clock).
            - each deck's anti-dragon TOOLKIT counts (wraths / fogs / combat-taxes / spot
              removal / maze / lifegain), classified from ORACLE TEXT (collection/
              oracle-cards.json) by the regexes below + audited INCLUDE/EXCLUDE overrides.
              The matched cards are PRINTED per deck so the classification is auditable.
  JUDGED    - the kill AXIS tag (over/combat), one line of justification per deck from the
              verified kill line.
            - the Ur-Dragon damage curve, go-live, and mitigation magnitudes — PRIORS,
              every one SWEPT. Read the RANKING and whether it survives the sweep.
HEURISTIC, not a rules engine. Trust the shape and the order, not the second decimal.

Emits analysis/vs_dragon_roster.json. Writeup: analysis/VsDragon_Roster_2026-06-15.md
"""
import argparse
import importlib.util
import json
import random
import re
import sys
from pathlib import Path

_spec = importlib.util.spec_from_file_location(
    "speed_lab_core", Path(__file__).parent / "speed_lab_core.py")
core = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(core)
ds = core.ds
ROOT = Path(__file__).parent.parent

# pull the verified PROTECT (counter-war) priors + deck->file map from the gauntlet/lock lab
_pg = importlib.util.spec_from_file_location("pod_gauntlet", ROOT / "scripts" / "pod_gauntlet.py")
PG = importlib.util.module_from_spec(_pg); _pg.loader.exec_module(PG)
_ll = importlib.util.spec_from_file_location("lock_lab", ROOT / "scripts" / "lock_lab.py")
LL = importlib.util.module_from_spec(_ll); _ll.loader.exec_module(LL)

for _s in (sys.stdout, sys.stderr):
    if hasattr(_s, "reconfigure"):
        try:
            _s.reconfigure(encoding="utf-8", errors="replace")
        except (ValueError, OSError):
            pass

SEED = 20260615
HORIZON = 16
START_LIFE = 40
CLOCKS_JSON = ROOT / "analysis" / "pod_gauntlet_clocks.json"
OUT_JSON = ROOT / "analysis" / "vs_dragon_roster.json"

# Ur-Dragon go-live + damage priors (= vs_dragon_lab defaults, the single-deck model they
# were tuned in). All swept below.
G_DIST = {6: 0.20, 7: 0.35, 8: 0.30, 9: 0.15}

# current decklists = lock_lab's map (croak_and_dagger already points at the deployed
# grind/lands list since the Calamity->Croak rebuild); kefka dropped — off-roster.
DECKS = dict(LL.DECKS)
DECKS.pop("kefka", None)
NAMES = {s: LL.NAMES[s] for s in DECKS}

# Croak (the grind-fortress rebuild of Calamity) uses the grind-fortress decap curve
# (the deployed anti-fair list; same curve vs_dragon_lab.py races), not the clocks-JSON
# base. (grid, decap).
GRIND_FORTRESS_CDF = ([6, 7, 8, 9, 10, 12, 14], [3, 16, 38, 63, 80, 96, 99])

# --- KILL AXIS + which clock, verified per deck from the kill lines (Summaries, this
# session). axis: over = goes over a flying board; combat = walled by blockers. cdf: which
# lab clock is the board-RELEVANT kill. race = burn/ping that chases ONE life total (dragon
# lifegain slows it; swept). note = the verified justification.
KILL = {
    "radiation_sickness": dict(axis="over", cdf="decap", race=False,
        note="Exsanguinate / Jarad+Lord drain / Mindcrank mill / Toxrill / Simic Asc — multiple board-independent lines"),
    "croak_and_dagger":   dict(axis="over", cdf="grind", race=False,
        note="grind/lands rebuild of Calamity; X-drain (Torment of Hailfire, 1-card, no board) + Gray Merchant/Kokusho — deployed grind-fortress curve"),
    "genome_project":     dict(axis="over", cdf="decap", race=True,
        note="Wizard-token PINGS = direct damage to a player; Exsanguinate table line — board-independent but a RACE on one total"),
    "lightning_war":      dict(axis="over", cdf="decap", race=True,
        note="burn + copy-amplified X-spells (Comet Storm/Crackle/Banefire) = direct damage; chases a life total"),
    "zero_sum_game":      dict(axis="over", cdf="decap", race=False,
        note="life-loop closes on our triggers, board-independent (Summary L1: 'the kill doesn't care')"),
    "crystal_sickness":   dict(axis="over", cdf="decap", race=False,
        note="drain + Mirrodin Besieged Phyrexian alt-win; 'win conditions (drain, mill) don't rely on creatures'"),
    "dark_lords_army":    dict(axis="over", cdf="decap", race=False,
        note="Gray Merchant drain + opponent-FED amass-drain (+ Cover of Darkness fear = army largely unblockable by dragons)"),
    "grand_design":       dict(axis="combat", cdf="decap", race=False,
        note="Summary: '96% of kills are incremental COMBAT, almost no trample' -> WALLED by the flying board"),
    "curse_of_the_scarab": dict(axis="combat", cdf="decap", race=False,
        note="zombie alpha strike; even the Cyc-Rift line is 'a lethal alpha strike into empty defenses' = combat"),
    "exiles_return":      dict(axis="combat", cdf="decap", race=False,
        note="Summary: 'the kill requires combat'; commander damage / Kiki combat"),
    "replication_crisis": dict(axis="combat", cdf="decap", race=False,
        note="combat-loop / token swarm; flying blockers wall it"),
    "lorehold_spirits":   dict(axis="combat", cdf="decap", race=False,
        note="spirit combat (only a niche Boros Charm burn goes over)"),
    "earthbend_the_meta": dict(axis="combat", cdf="decap", race=False,
        note="Toph lands-as-creatures combat swing"),
    "eldrazi_stampede":   dict(axis="combat", cdf="decap", race=False,
        note="'Combat / Annihilator' (Summary win-condition row)"),
    "bumbleflower":       dict(axis="combat", cdf="decap", race=False,
        note="Willbreaker theft + combat steal"),
}

# load-time invariant: every modelled deck needs a KILL axis/clock and vice versa.
# This is the guard that would have caught the Calamity->Croak slug drift that crashed
# this lab (a deck in DECKS with no KILL entry KeyErrors in build_decks/kill_cdf).
assert set(DECKS) == set(KILL), \
    f"DECKS/KILL slug mismatch (update both together): {set(DECKS) ^ set(KILL)}"

# === toolkit classification (ORACLE TEXT, collection/oracle-cards.json) ===================
# A card counts in a category if its oracle text matches the regex AND it isn't in that
# category's EXCLUDE set; INCLUDE sets force tricky cards the regex misses (overload, counter
# effects, recurring -1/-1). Matched cards are PRINTED for audit. Patterns are deliberately
# specific to FLYING-AGNOSTIC effects (dragons fly), so e.g. "can't block" pumps don't count.
ORACLE = {}  # name(lower) -> oracle text (lower), built lazily

WRATH_RE = re.compile(
    r"destroy all (creatures|nonland permanents)|destroy each creature|exile all creatures|"
    r"all creatures get -|creatures? (you don't control|your opponents control) get -|"
    r"deals? \d+ damage to each creature|to each creature an opponent|each creature gets -")
WRATH_INCLUDE = {  # verified flying-agnostic sweeps the regex under-catches
    "cyclonic rift",            # overload = bounce EACH nonland permanent you don't control
    "toxrill, the corrosive",   # each end step: -1/-1 counter on each creature you don't control (recurring)
    "massacre wurm",            # opponents' creatures get -2/-2
    "the meathook massacre",    # X: creatures get -X/-X
    "necromantic selection",    # destroy all creatures, reanimate one
    "in garruk's wake",         # destroy all creatures you don't control
    "killing wave",             # each player sacrifices unless pays life (flying-agnostic edict)
}
WRATH_EXCLUDE = {  # NOT a flying-board reset
    "culling ritual",           # destroys only MV<=2 -> doesn't touch fat dragons
    "blasphemous edict",        # (if present) symmetric small-creature sac in these shells
}
FOG_RE = re.compile(
    r"prevent all (combat )?damage|prevent the next \d+ damage|prevent all damage that would be dealt this turn")
FOG_INCLUDE = {"spore frog", "constant mists", "darkness", "fog", "blunt the assault",
               "dawn charm", "tangle", "defend the celestus"}
FOG_REPEAT = {"constant mists", "spore frog"}   # buyback land-sac / reanimable body
TAX_RE = re.compile(
    r"can't attack you( or planeswalkers you control)? unless|"
    r"creatures can't attack unless|attack you or planeswalkers you control unless")
TAX_INCLUDE = {"propaganda", "ghostly prison", "sphere of safety", "norn's annex",
               "windborn muse", "archangel of tithes", "baird, steward of argive"}
SPOT_RE = re.compile(
    r"(destroy|exile) target creature|"
    r"destroy target (creature or planeswalker|nonland permanent|permanent|artifact or creature)|"
    r"exile target (creature or planeswalker|nonland permanent|permanent)|"
    r"target creature you don't control|deals? \d+ damage to (any target|target creature)")
SPOT_EXCLUDE = set()
LIFE_RE = re.compile(r"gain \d+ life|gain life|gain that much life|whenever .*gain \d+ life")
MAZE_INCLUDE = {"maze of ith", "glacial chasm", "moat", "solitary confinement",
                "silent arbiter", "kami of false hope", "constant mists"}


def load_oracle():
    if ORACLE:
        return
    data = json.loads((ROOT / "collection" / "oracle-cards.json").read_text(encoding="utf-8"))
    for c in data:
        nm = c.get("name", "").lower()
        txt = c.get("oracle_text", "") or ""
        for f in c.get("card_faces", []) or []:
            txt += " " + (f.get("oracle_text", "") or "")
        txt = txt.lower()
        # textless printings (art-series-style "X // X" entries) must not poison the
        # index — they otherwise land via the face-name path below and blank out the
        # real card (caught 2026-07-05: otext("Infernal Grasp") == "  ")
        if not txt.strip():
            continue
        if not ORACLE.get(nm, "").strip():
            ORACLE[nm] = txt
        # also index each face name (adventures / MDFCs are listed as "A // B")
        if " // " in nm:
            for part in nm.split(" // "):
                p = part.strip()
                if not ORACLE.get(p, "").strip():
                    ORACLE[p] = txt


def otext(name):
    return ORACLE.get(name.lower(), "")


def classify(names):
    """Count anti-dragon toolkit from oracle text. Returns counts + the matched card lists."""
    wr, fog, tax, spot, life, maze = [], [], [], [], [], []
    fog_repeat = False
    for nm in names:
        low = nm.lower()
        t = otext(nm)
        if low in WRATH_EXCLUDE:
            pass
        elif low in WRATH_INCLUDE or WRATH_RE.search(t):
            wr.append(nm)
        if low in FOG_INCLUDE or FOG_RE.search(t):
            fog.append(nm)
            fog_repeat = fog_repeat or low in FOG_REPEAT
        if low in TAX_INCLUDE or TAX_RE.search(t):
            tax.append(nm)
        if low in MAZE_INCLUDE:
            maze.append(nm)
        # spot removal: single-target destroy/exile/burn a creature (shave a payoff dragon)
        if low not in WRATH_INCLUDE and SPOT_RE.search(t) and "all creatures" not in t:
            spot.append(nm)
        if LIFE_RE.search(t):
            life.append(nm)
    return dict(wraths=wr, fogs=fog, taxes=tax, spot=spot, lifegain=life, maze=maze,
                fog_repeat=fog_repeat)


# === clocks ==============================================================================
def build_cdf(grid, cum):
    F = [0.0] * (HORIZON + 1)
    pts = list(zip(grid, cum))
    for t in range(1, HORIZON + 1):
        if t <= pts[0][0]:
            F[t] = pts[0][1] / 100.0 if t == pts[0][0] else 0.0
        elif t >= pts[-1][0]:
            F[t] = pts[-1][1] / 100.0
        else:
            for (t0, c0), (t1, c1) in zip(pts, pts[1:]):
                if t0 <= t <= t1:
                    F[t] = (c0 + (t - t0) / (t1 - t0) * (c1 - c0)) / 100.0
                    break
    for t in range(1, HORIZON + 1):
        F[t] = max(F[t], F[t - 1])
    return F


def kill_cdf(slug, clocks):
    which = KILL[slug]["cdf"]
    if which == "grind":
        return build_cdf(*GRIND_FORTRESS_CDF)
    c = clocks[slug]
    return build_cdf(c["grid"], c[which])


def sample_kill(F, rng):
    u = rng.random()
    for t in range(1, HORIZON + 1):
        if u <= F[t]:
            return t
    return HORIZON + 1


def dragon_damage(turn, g_eff, base, step):
    return 0 if turn < g_eff else base + step * (turn - g_eff)


# === the survival race ===================================================================
def simulate(deck, F, kdist, P, rng):
    """P(win vs Ur-Dragon). deck = {axis, race, protect, toolkit counts, fog_repeat}."""
    ks, kp = zip(*kdist.items())
    win = 0
    cap_life = P.life_per_gain * deck["nlife"]
    cap_life = min(P.life_cap, cap_life)
    for _ in range(P.trials):
        t_kill = sample_kill(F, rng)
        if deck["race"]:
            t_kill += P.race_delay            # dragon lifegain slows a chase-the-total kill
        G = rng.choices(ks, weights=kp)[0]
        life = START_LIFE + cap_life
        g_eff = G
        cur_base = P.dmg_base
        wraths, fogs, removal = deck["nwr"], deck["nfog"], deck["nspot"]
        ntax, tax_live = deck["ntax"], 0
        maze = deck["maze"] and rng.random() < P.maze_online
        p_stop = P.kill_disrupt * (1 - deck["protect"])
        decided = False
        for t in range(1, HORIZON + 1):
            # --- OUR turn t (we precede their turn t) ---
            if t >= t_kill:
                if deck["axis"] == "over":
                    connects = True           # board-independent kill ignores the flying wall
                elif t < G:
                    connects = True           # COMBAT deck that RACED the dragons before they came online
                else:
                    # board live & GROWING: only a tapped-attacker window, decaying as the army snowballs.
                    # (own symmetric wraths clear OUR board too, so they don't open a swing window — hence
                    # combat kills do NOT key off g_eff; the natural pre-go-live race G is the real window.)
                    connects = rng.random() < P.p_connect * (P.connect_decay ** (t - G))
                if connects and rng.random() >= p_stop:
                    win += 1; decided = True; break
                if connects:                 # only their counter stopped it -> reload
                    t_kill = t + 1; p_stop *= 0.5
                # else combat blocked by the wall: wait for a window (no reload)
            # a passive combat-tax comes online once drawn (cheap, sticks)
            if ntax > tax_live and rng.random() < P.draw:
                tax_live += 1
            # --- THEIR turn t ---
            incoming = dragon_damage(t, g_eff, cur_base, P.dmg_step)
            if tax_live:
                incoming = int(incoming * max(0.0, 1 - P.tax_block * tax_live))
            if incoming > 0:
                lethal = incoming >= life
                acted = rng.random() < P.p_act
                acted_cheap = acted or rng.random() < (1 - P.p_act) * 0.7
                if acted_cheap and fogs > 0 and incoming >= 10 and rng.random() < P.draw:
                    incoming = 0
                    if not deck["fog_repeat"] or rng.random() < 0.25:
                        fogs -= 1
                elif acted and wraths > 0 and incoming >= 12 and rng.random() < P.draw:
                    wraths -= 1                                  # reset the board (also opens a combat window)
                    g_eff = t + 1 + P.rebuild
                    cur_base = max(4, int(cur_base * P.reset_mult))
                    incoming = 0
                elif acted and removal > 0 and (lethal or incoming >= 16) and rng.random() < P.draw:
                    removal -= 1
                    incoming = max(0, incoming - P.removal_block)
                elif maze:
                    incoming = max(0, incoming - P.maze_block)
                life -= incoming
            if life <= 0:
                decided = True; break
        if not decided and t_kill <= HORIZON and deck["axis"] == "over":
            win += 1                          # alive at horizon, over-the-wall kill online -> grind through
        # combat decks that never found a window do NOT win (survive != close)
    return win / P.trials


# === build per-deck records ==============================================================
def cap_counts(tk):
    """Counts feeding the sim (a few diminishing-return caps so 8 wraths != 8 turns of safety)."""
    return dict(nwr=min(len(tk["wraths"]), 4), nfog=min(len(tk["fogs"]), 3),
                ntax=min(len(tk["taxes"]), 2), nspot=min(len(tk["spot"]), 4),
                nlife=min(len(tk["lifegain"]), 6), maze=bool(tk["maze"]),
                fog_repeat=tk["fog_repeat"])


def build_decks(trials):
    load_oracle()
    index = ds.load_oracle_index(); aliases = ds.load_reskin_aliases()
    clocks = json.loads(CLOCKS_JSON.read_text(encoding="utf-8"))
    out = {}
    for slug in DECKS:
        lib, _ = core.load_parsed(ROOT / DECKS[slug], index, aliases, warn=False)
        names = [nm for nm, _ in lib]
        tk = classify(names)
        rec = dict(slug=slug, name=NAMES[slug], axis=KILL[slug]["axis"],
                   race=KILL[slug]["race"], note=KILL[slug]["note"],
                   protect=PG.PROTECT.get(slug, 0.0), toolkit=tk,
                   F=kill_cdf(slug, clocks), **cap_counts(tk))
        out[slug] = rec
    return out


def params(args, **ov):
    P = argparse.Namespace(
        trials=args.trials, dmg_base=args.dmg_base, dmg_step=args.dmg_step,
        rebuild=args.rebuild, reset_mult=args.reset_mult, kill_disrupt=args.kill_disrupt,
        maze_block=args.maze_block, maze_online=args.maze_online, removal_block=args.removal_block,
        draw=args.draw, p_act=args.p_act, p_connect=args.p_connect, tax_block=args.tax_block,
        connect_decay=args.connect_decay,
        life_per_gain=args.life_per_gain, life_cap=args.life_cap, race_delay=args.race_delay)
    for k, v in ov.items():
        setattr(P, k, v)
    return P


def run(args):
    decks = build_decks(args.trials)
    kdist = dict(G_DIST)
    if args.dragon_fast:
        kdist = {5: 0.15, 6: 0.35, 7: 0.32, 8: 0.13, 9: 0.05}
    if args.dragon_slow:
        kdist = {7: 0.25, 8: 0.35, 9: 0.25, 10: 0.15}
    P = params(args)

    print(f"\n{'='*100}\nVS-DRAGON ROSTER LAB — P(win vs the Ur-Dragon fair-board deck), per deck")
    gd = " ".join(f"T{k}:{int(p*100)}%" for k, p in sorted(kdist.items()))
    print(f"  go-live G={{{gd}}} · dmg {args.dmg_base}+{args.dmg_step}/turn focused on us · "
          f"p_connect(combat thru wall)={args.p_connect} · trials={args.trials}")
    print(f"  KILL AXIS verified per deck (over = goes over the flying board; combat = walled). "
          f"toolkit = ORACLE-classified, capped.\n")
    rng = random.Random(args.seed)
    rows = []
    for slug, d in decks.items():
        p = simulate(d, d["F"], kdist, P, rng)
        rows.append((p, d))
    rows.sort(key=lambda r: -r[0])

    print(f"  {'deck':24}{'axis':>7}{'wr':>3}{'fog':>4}{'tax':>4}{'spot':>5}{'mz':>3}"
          f"{'prot':>6}{'P(win)':>8}   kill (verified)")
    out = {}
    for p, d in rows:
        tk = d["toolkit"]
        print(f"  {d['name']:24}{d['axis']:>7}{d['nwr']:>3}{d['nfog']:>4}{d['ntax']:>4}"
              f"{d['nspot']:>5}{'Y' if d['maze'] else '·':>3}{d['protect']*100:>5.0f}%"
              f"{p*100:>7.0f}%   {d['note'][:48]}")
        out[d["slug"]] = dict(name=d["name"], axis=d["axis"], p_win=round(p, 4),
                              wraths=tk["wraths"], fogs=tk["fogs"], taxes=tk["taxes"],
                              spot=len(tk["spot"]), maze=tk["maze"], lifegain=len(tk["lifegain"]),
                              protect=d["protect"], race=d["race"], note=d["note"])
    OUT_JSON.write_text(json.dumps(out, indent=2), encoding="utf-8")

    print(f"\n  SWEEP — does the RANKING hold? (P(win) per deck across the priors)")
    scen = [
        ("baseline", {}),
        ("go-live FAST", dict(_kd="fast")),
        ("go-live SLOW", dict(_kd="slow")),
        ("hyper-aggro 22+9", dict(dmg_base=22, dmg_step=9)),
        ("grindy 12+5", dict(dmg_base=12, dmg_step=5)),
        ("combat thru-wall .15", dict(p_connect=0.15)),
        ("combat thru-wall .45", dict(p_connect=0.45)),
        ("we brick (draw .45)", dict(draw=0.45)),
        ("dragons gain life (race +2)", dict(race_delay=2)),
    ]
    labels = [s[0] for s in scen]
    print(f"  {'deck':24}" + "".join(f"{l[:10]:>11}" for l in labels))
    grids = {}
    for slug, d in decks.items():
        cells = []
        for _, ov in scen:
            kd = kdist
            ov = dict(ov)
            tag = ov.pop("_kd", None)
            if tag == "fast":
                kd = {5: 0.15, 6: 0.35, 7: 0.32, 8: 0.13, 9: 0.05}
            if tag == "slow":
                kd = {7: 0.25, 8: 0.35, 9: 0.25, 10: 0.15}
            Pp = params(args, **ov)
            cells.append(simulate(d, d["F"], kd, Pp, random.Random(args.seed + 7)))
        grids[slug] = cells
    for p, d in rows:
        print(f"  {d['name']:24}" + "".join(f"{c*100:>10.0f}%" for c in grids[d['slug']]))

    print(f"\n  Toolkit AUDIT (oracle-classified; verify the matches) — wraths · fogs · taxes · maze:")
    for p, d in rows:
        tk = d["toolkit"]
        bits = []
        if tk["wraths"]: bits.append("WR " + ", ".join(tk["wraths"][:5]))
        if tk["fogs"]:   bits.append("FOG " + ", ".join(tk["fogs"][:4]) + (" [rep]" if tk["fog_repeat"] else ""))
        if tk["taxes"]:  bits.append("TAX " + ", ".join(tk["taxes"][:3]))
        if tk["maze"]:   bits.append("MAZE " + ", ".join(tk["maze"][:2]))
        print(f"    {d['name']:22} " + " · ".join(bits) if bits else f"    {d['name']:22} (none)")
    print(f"\n  wrote {OUT_JSON.relative_to(ROOT)}")
    print(f"  Priors (go-live, damage, mitigation magnitudes) are JUDGMENT — swept above. The kill")
    print(f"  CLOCK and the TOOLKIT counts are measured; the kill AXIS is verified. Read the ranking.")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--trials", type=int, default=40000)
    ap.add_argument("--seed", type=int, default=SEED)
    ap.add_argument("--dmg-base", type=int, default=16, dest="dmg_base")
    ap.add_argument("--dmg-step", type=int, default=7, dest="dmg_step")
    ap.add_argument("--rebuild", type=int, default=1)
    ap.add_argument("--reset-mult", type=float, default=0.70, dest="reset_mult")
    ap.add_argument("--kill-disrupt", type=float, default=0.15, dest="kill_disrupt")
    ap.add_argument("--maze-block", type=int, default=8, dest="maze_block")
    ap.add_argument("--maze-online", type=float, default=0.55, dest="maze_online")
    ap.add_argument("--removal-block", type=int, default=7, dest="removal_block")
    ap.add_argument("--draw", type=float, default=0.58)
    ap.add_argument("--p-act", type=float, default=0.70, dest="p_act")
    ap.add_argument("--p-connect", type=float, default=0.22, dest="p_connect",
                    help="P(a COMBAT kill connects on the FIRST live-board turn: tapped attackers / partial push)")
    ap.add_argument("--connect-decay", type=float, default=0.5, dest="connect_decay",
                    help="per-turn decay of the combat connect window as the dragon army snowballs")
    ap.add_argument("--tax-block", type=float, default=0.25, dest="tax_block",
                    help="incoming reduction per live combat-tax (Propaganda-class)")
    ap.add_argument("--life-per-gain", type=int, default=2, dest="life_per_gain",
                    help="effective life buffer per lifegain source")
    ap.add_argument("--life-cap", type=int, default=12, dest="life_cap")
    ap.add_argument("--race-delay", type=int, default=0, dest="race_delay",
                    help="turns a chase-the-total kill (race=True) is slowed by dragon lifegain")
    ap.add_argument("--dragon-fast", action="store_true", dest="dragon_fast")
    ap.add_argument("--dragon-slow", action="store_true", dest="dragon_slow")
    run(ap.parse_args())


if __name__ == "__main__":
    main()
