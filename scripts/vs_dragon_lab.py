#!/usr/bin/env python3
"""vs_dragon_lab.py — does the Glarb (Calamity Tax) anti-dragon package actually
BEAT the archenemy's Ur-Dragon deck? The Pod Gauntlet can't answer this: it races
a *combo turn K*, and Ur-Dragon is a FAIR BOARD deck (no fixed lethal turn — a
snowballing dragon army that a wrath RESETS and a fog SKIPS). This is the
`--vs-board` model the gauntlet flagged as missing (project_ur_dragon_matchup).

THE MATCHUP (project_ur_dragon_matchup, card text verified):
  * The Ur-Dragon "goes live" turn G: it untaps with dragons, attacks, draws that
    many + cheats a permanent → the board SNOWBALLS. Focused on us (the archenemy
    guns the player telegraphing a Torment), it kills us a few turns after G.
  * OUR kill is a BOARD-INDEPENDENT drain (Torment of Hailfire / Kokusho+Rite /
    Gray Merchant) that goes OVER the flying board. Its clock is the grind-fortress
    decap curve (ct_speed_lab, via pod_gauntlet SWAPS) — UNCHANGED by the package,
    which cuts win-more (Doppelgang/Espers/Edict), not kill pieces.

So the A/B is clean and measurable: SAME T_kill, does the package raise
P(we survive to it)? The package is purely defensive —
  + Spore Frog        one-shot Fog (+ recurs via Reanimate/Noxious/Witness)
  + Constant Mists    REPEATABLE Fog (buyback = sac a land; 39 lands + Crucible/Loam)
  + Beast Within      instant destroy-any-permanent (kills a dragon / the avatar)
  − Blasphemous Edict / Espers to Magicite / Doppelgang  (dead vs a fair board deck)

MITIGATION MODEL (per their attack turn, focused on us, life 40):
  * WRATH  — a flying-agnostic scalable reset (Toxic Deluge, Meathook Massacre;
    Massacre Wurm partial). RESETS their board: 0 damage for `rebuild` turns, then
    they resume at a reduced base (lost the cheated-in dragons). FINITE count, drawn.
  * FOG    — skips ONE attack entirely (incoming = 0). Constant Mists is REPEATABLE
    while we have spare lands; Spore Frog ~1-2 uses (recursion). The package's edge.
  * MAZE of Ith — removes the single biggest attacker every turn (repeatable). BOTH.
  * REMOVAL — Deadly Rollick (both) + Beast Within (package): a one-shot dragon kill
    that shaves the per-turn damage.

HONESTY (same discipline as the gauntlet — trust the A/B and the shape, not the
second decimal): their go-live turn, damage base/step, and reset/fog effects are
PRIORS (judgment), so every one is SWEPT. The kill clock is lab-sourced. Read the
LIFT (upgrade − base) and whether it survives the sweep, not the absolute %.
"""
import argparse
import random

# --- OUR kill clock: grind-fortress decap (board-independent drain) ----------
# From pod_gauntlet SWAPS["croak_and_dagger"] (lab ct_speed_lab on glarb-grind-fortress,
# 12k). The package does NOT touch these cards, so base & upgrade share this curve.
KILL_GRID = [6, 7, 8, 9, 10, 12, 14]
KILL_DECAP = [3, 16, 38, 63, 80, 96, 99]          # cum P(over-the-top drain lethal <= T)
HORIZON = 16
START_LIFE = 40

# --- Ur-Dragon: the fair board deck ----------------------------------------
# "Goes live" turn G — the only fair deck in his stable, slower than his T6-7 combo.
G_DIST = {6: 0.20, 7: 0.35, 8: 0.30, 9: 0.15}     # mean ~7.4 (PRIOR; --dragon-fast/-slow)
DMG_BASE = 16                                      # first live swing: it has SPAT OUT a board (2-3 fat dragons)
DMG_STEP = 7                                       # +/turn as the attack trigger cheats in another dragon
KILL_DISRUPT = 0.15                                # P(they counter OUR drain) — fair deck, few counters
REBUILD = 1                                        # turns of ~0 damage after we wrath (they redeploy fast — eminence)
RESET_BASE_MULT = 0.70                             # post-wrath swing is smaller (lost the cheated-in dragons; eminence persists)


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


def sample_kill(F, rng):
    u = rng.random()
    for t in range(1, HORIZON + 1):
        if u <= F[t]:
            return t
    return HORIZON + 1


# --- the two suites ---------------------------------------------------------
# protect = P(our drain resolves through their counter) — Glarb runs Veil/counters.
SUITES = {
    "base": dict(
        name="grind-fortress (no package)",
        wraths=3,          # Toxic Deluge, Meathook, Massacre Wurm (Culling Ritual hits MV<=2 only -> NOT dragons)
        fogs=0, fog_repeat=False,
        maze=True,         # Maze of Ith
        removal=1,         # Deadly Rollick
        protect=0.55),
    "upgrade": dict(
        name="+Spore Frog +Constant Mists +Beast Within",
        wraths=3,
        fogs=2, fog_repeat=True,    # Spore Frog (1-2) + Constant Mists (REPEATABLE while lands)
        maze=True,
        removal=2,                  # Deadly Rollick + Beast Within
        protect=0.55),
    # --- 2026-06-30: the ACTUAL deployed list (croak-and-dagger-20260623-215731.txt).
    # The 06-23 lands/graveyard swap CUT Constant Mists, so the deployed fog is just
    # Spore Frog (recurs via Muldrotha/Noxious/Witness — slower than buyback). The old
    # "upgrade" suite above is now STALE (assumes Constant Mists) → deployed is a touch
    # weaker on the repeatable-fog axis. This is the honest current baseline.
    "deployed": dict(
        name="deployed Croak (Spore Frog only; Constant Mists cut)",
        wraths=3,                   # Toxic Deluge, Meathook, Massacre Wurm (Culling = MV<=2, not dragons)
        fogs=1, fog_repeat=True, fog_consume=0.5,   # Spore Frog + slow gy-recursion (no land-buyback)
        maze=True,
        removal=2,                  # Deadly Rollick + Beast Within
        protect=0.55),
    # --- the "meaty" package on TOP of the deployed list:
    #   +Ancient Brass Dragon  7/6 FLYER + on-hit d20 mass-reanimate (blocks air; refills blockers)
    #   +Sheoldred, Whispering One  recurring EDICT (each opp sacs a creature/turn => board attrition)
    #   +Tatyova, Benthic Druid  landfall LIFEGAIN (~2/turn once online in a 39-land + extra-drop shell)
    # (Mirrorform is an OFFENSE add — a 2nd Kokusho kill line — so it lives in the kill clock,
    #  not this survival model; it is intentionally NOT represented here.)
    "meaty": dict(
        name="deployed +Ancient Brass(flyer/reanimate) +Sheoldred WO(edict) +Tatyova(lifegain)",
        wraths=3,
        fogs=1, fog_repeat=True, fog_consume=0.5,
        maze=True,
        removal=2,
        protect=0.55,
        # flying blocker: a 7-power flier soaks ~one dragon/turn; removable, but Ancient Brass
        # reanimates a replacement flier (Kokusho/Archon) -> 2 effective "charges". Online ~T7 (7 mana).
        blocker_block=7, blocker_charges=2, blocker_remove=0.30, blocker_earliest=7,
        lifegain=2, lifegain_earliest=5,        # Tatyova {3}{G}{U}
        edict_shrink=4, edict_earliest=7),      # Sheoldred WO {5}{B}{B}: -1 mid dragon/turn off the swing
}


def dragon_damage(turn, g_eff, base, step):
    """Incoming this turn if their board is live (turn >= g_eff)."""
    if turn < g_eff:
        return 0
    return base + step * (turn - g_eff)


def simulate(suite, F, kdist, args, rng):
    ks, kp = zip(*kdist.items())
    g_base, g_step = args.dmg_base, args.dmg_step
    rebuild = args.rebuild
    win = 0
    for _ in range(args.trials):
        t_kill = sample_kill(F, rng)
        G = rng.choices(ks, weights=kp)[0]
        life = START_LIFE
        g_eff = G                                  # their effective go-live (pushed back by wraths)
        cur_base = g_base
        wraths = suite["wraths"]
        fogs = suite["fogs"]
        removal = suite["removal"]
        fog_consume = suite.get("fog_consume", 0.25)
        # wrath/fog/removal availability is gated on being DRAWN — model as a per-turn draw chance
        p_stop = args.kill_disrupt * (1 - suite["protect"])   # P(they answer our drain), eased by protect-own
        maze_online = suite["maze"] and rng.random() < args.maze_online   # 1 land of 39: not guaranteed
        # --- meaty package mechanics (INERT unless the suite enables them) ---------
        blk_block = suite.get("blocker_block", 0) if args.blocker_block is None else args.blocker_block
        blk_charges = suite.get("blocker_charges", 0)
        blk_remove = suite.get("blocker_remove", 0.0) if args.blocker_remove is None else args.blocker_remove
        blk_earliest = suite.get("blocker_earliest", 99)
        blk_online = False
        lg = suite.get("lifegain", 0) if args.lifegain is None else args.lifegain
        lg_earliest = suite.get("lifegain_earliest", 99)
        lg_online = False
        ed_shrink = suite.get("edict_shrink", 0) if args.edict_shrink is None else args.edict_shrink
        ed_earliest = suite.get("edict_earliest", 99)
        ed_online = False
        decided = False
        for t in range(1, HORIZON + 1):
            # --- lifegain (Tatyova landfall): a per-turn life buffer once drawn/online ---
            if not lg_online and t >= lg_earliest and rng.random() < args.draw:
                lg_online = True
            if lg_online:
                life += lg
            # --- OUR turn t (we precede their turn t in seat order) ---
            if t >= t_kill:                        # over-the-top drain is online
                if rng.random() >= p_stop:         # resolves -> we neutralise Ur-Dragon
                    win += 1; decided = True; break
                t_kill = t + 1                     # answered -> reload next turn
                p_stop *= 0.5                       # their interaction is finite
            # --- edict (Sheoldred WO): their board attrites one creature each upkeep ---
            if not ed_online and t >= ed_earliest and rng.random() < args.draw:
                ed_online = True
            if ed_online:
                cur_base = max(4, cur_base - ed_shrink)
            # --- flying blocker (Ancient Brass / reanimated flier) comes online once cast ---
            if not blk_online and blk_charges > 0 and t >= blk_earliest and rng.random() < args.draw:
                blk_online = True
            # --- THEIR turn t: ONE meaningful interaction (we're also holding kill mana / developing) ---
            incoming = dragon_damage(t, g_eff, cur_base, g_step)
            if incoming > 0:
                lethal = incoming >= life
                # We don't always have mana up to interact — we're casting our own engine / holding
                # counters for the OTHER two seats. p_act = P(we get to spend an answer this turn).
                acted = rng.random() < args.p_act
                # A 1-mana Spore Frog / 2-mana Constant Mists is castable when a 4-mana wrath ISN'T —
                # cheap fogs largely bypass the mana tax (the package's real edge under pressure).
                acted_cheap = acted or rng.random() < (1 - args.p_act) * 0.7
                # priority: FOG a lethal-ish swing (best answer, the package's edge) > WRATH (reset, finite)
                #           > spot REMOVAL. MAZE is a PASSIVE floor (a permanent, costs no mana → always on).
                if acted_cheap and fogs > 0 and incoming >= 10 and rng.random() < args.draw:
                    incoming = 0                                  # Fog: skip the whole attack
                    if not suite["fog_repeat"] or rng.random() < fog_consume:
                        fogs -= 1
                elif acted and wraths > 0 and incoming >= 12 and t + 1 < t_kill and rng.random() < args.draw:
                    wraths -= 1                                   # Wrath: reset their board
                    g_eff = t + 1 + rebuild
                    cur_base = max(4, int(cur_base * RESET_BASE_MULT))
                    incoming = 0
                elif acted and removal > 0 and (lethal or incoming >= 16) and rng.random() < args.draw:
                    removal -= 1
                    incoming = max(0, incoming - args.removal_block)
                elif maze_online:
                    incoming = max(0, incoming - args.maze_block)  # passive: neutralise one attacker
                # --- flying blocker soaks ~one attacker, PASSIVELY (independent of the mana-gated answers) ---
                if blk_online and blk_charges > 0 and incoming > 0:
                    incoming = max(0, incoming - blk_block)
                    if rng.random() < blk_remove:
                        blk_charges -= 1          # removed; Ancient Brass reanimates a replacement flier
                        if blk_charges <= 0:
                            blk_online = False
                life -= incoming
            if life <= 0:
                decided = True; break
        if not decided and t_kill <= HORIZON:
            win += 1                                # alive at horizon with the kill online -> grind through
    return win / args.trials


def run(args):
    rng = random.Random(args.seed)
    F = build_cdf(KILL_GRID, KILL_DECAP)
    kdist = dict(G_DIST)
    if args.dragon_fast:
        kdist = {5: 0.15, 6: 0.35, 7: 0.32, 8: 0.13, 9: 0.05}
    if args.dragon_slow:
        kdist = {7: 0.25, 8: 0.35, 9: 0.25, 10: 0.15}

    # Which A/B pair: default = the 06-15 fog package; --meaty = the deployed list vs the
    # +Ancient Brass/+Sheoldred WO/+Tatyova package (blocker / edict / lifegain mechanics).
    lo, hi = ("deployed", "meaty") if args.meaty else ("base", "upgrade")
    title = "the MEATY package (flyer + edict + lifegain)" if args.meaty else "the anti-dragon fog package"

    print(f"\n{'='*78}\nVS-DRAGON LAB — Glarb (Croak and Dagger) vs the Ur-Dragon fair-board deck")
    print(f"  our kill = board-independent drain, decap median ~T13 (grind-fortress, lab-sourced)")
    gd = " ".join(f"T{k}:{int(p*100)}%" for k, p in sorted(kdist.items()))
    print(f"  Ur-Dragon go-live G = {{{gd}}}  ·  dmg {args.dmg_base}+{args.dmg_step}/turn focused on us"
          f"  ·  trials={args.trials}")
    print(f"  maze -{args.maze_block}/turn · removal -{args.removal_block} · wrath reset +{args.rebuild}t"
          f" · they counter our drain {int(args.kill_disrupt*100)}%")
    if args.meaty:
        print(f"  MEATY priors: flyer soaks {SUITES['meaty']['blocker_block']}/turn × "
              f"{SUITES['meaty']['blocker_charges']} charges (remove {SUITES['meaty']['blocker_remove']:.0%}/t) ·"
              f" lifegain +{SUITES['meaty']['lifegain']}/t · edict -{SUITES['meaty']['edict_shrink']}/t\n")
    else:
        print()
    res = {}
    for key in (lo, hi):
        res[key] = simulate(SUITES[key], F, kdist, args, rng)
        print(f"  {SUITES[key]['name']:62} P(win) = {res[key]*100:4.0f}%")
    lift = (res[hi] - res[lo]) * 100
    print(f"\n  LIFT from {title}: {lift:+.0f} pp\n")

    print("  SWEEP — is the lift robust? (rows = stress; cols = baseline / package / lift)")
    print(f"  {'scenario':32}{'base':>8}{'pkg':>8}{'lift':>7}")
    scen = [
        ("their go-live FAST", dict(fast=True), {}),
        ("their go-live SLOW", dict(slow=True), {}),
        ("hyper-aggro (22+9/turn)", dict(dmg_base=22, dmg_step=9), {}),
        ("grindy dragons (12+5/turn)", dict(dmg_base=12, dmg_step=5), {}),
        ("they pack counters (35%)", dict(kill_disrupt=0.35), {}),
        ("we flood answers (draw .80)", dict(draw=0.80), {}),
        ("we brick on answers (draw .45)", dict(draw=0.45), {}),
    ]
    if args.meaty:                     # isolate each meaty mechanic's contribution
        scen += [
            ("  meaty: blocker fragile (.60)", {}, dict(blocker_remove=0.60)),
            ("  meaty: no edict (Sheoldred cut)", {}, dict(edict_shrink=0)),
            ("  meaty: no lifegain (Tatyova cut)", {}, dict(lifegain=0)),
            ("  meaty: blocker only", {}, dict(edict_shrink=0, lifegain=0)),
        ]
    for label, ov, suite_ov in scen:
        a = argparse.Namespace(**vars(args))
        kd = dict(G_DIST)
        if ov.pop("fast", False):
            kd = {5: 0.15, 6: 0.35, 7: 0.32, 8: 0.13, 9: 0.05}
        if ov.pop("slow", False):
            kd = {7: 0.25, 8: 0.35, 9: 0.25, 10: 0.15}
        for k, v in ov.items():
            setattr(a, k, v)
        lo_suite = SUITES[lo]
        hi_suite = {**SUITES[hi], **suite_ov}   # suite_ov tweaks only the package arm
        rng2 = random.Random(args.seed + 1)
        b = simulate(lo_suite, F, kd, a, rng2)
        rng3 = random.Random(args.seed + 1)
        u = simulate(hi_suite, F, kd, a, rng3)
        print(f"  {label:32}{b*100:>7.0f}%{u*100:>7.0f}%{(u-b)*100:>+6.0f}")
    print(f"\n  Priors (go-live, damage curve, reset/fog/maze/blocker/edict/lifegain) are JUDGMENT — swept.")
    print(f"  The kill clock is lab-sourced; the package is purely defensive (same T_kill).")
    print(f"  Read the LIFT and whether it holds across the sweep, not the absolute %.\n")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--trials", type=int, default=40000)
    p.add_argument("--seed", type=int, default=17)
    p.add_argument("--dmg-base", type=int, default=DMG_BASE, dest="dmg_base")
    p.add_argument("--dmg-step", type=int, default=DMG_STEP, dest="dmg_step")
    p.add_argument("--rebuild", type=int, default=REBUILD)
    p.add_argument("--kill-disrupt", type=float, default=KILL_DISRUPT, dest="kill_disrupt")
    p.add_argument("--maze-block", type=int, default=8, dest="maze_block")
    p.add_argument("--maze-online", type=float, default=0.55, dest="maze_online",
                   help="P(Maze of Ith is drawn & online by the time it matters)")
    p.add_argument("--removal-block", type=int, default=7, dest="removal_block")
    p.add_argument("--draw", type=float, default=0.58, help="P(a relevant answer is in hand on a given turn)")
    p.add_argument("--p-act", type=float, default=0.70, dest="p_act",
                   help="P(we have mana free to interact this turn — not tapped on our engine / the other 2 seats)")
    p.add_argument("--dragon-fast", action="store_true", dest="dragon_fast")
    p.add_argument("--dragon-slow", action="store_true", dest="dragon_slow")
    # --- meaty package (deployed vs +Ancient Brass/+Sheoldred WO/+Tatyova) ---
    p.add_argument("--meaty", action="store_true",
                   help="A/B the deployed list vs the meaty (flyer/edict/lifegain) package")
    p.add_argument("--blocker-block", type=int, default=None, dest="blocker_block",
                   help="override: flying-blocker damage soaked per turn")
    p.add_argument("--blocker-remove", type=float, default=None, dest="blocker_remove",
                   help="override: P(their deck removes our blocker each turn)")
    p.add_argument("--lifegain", type=int, default=None,
                   help="override: life gained per turn once Tatyova online")
    p.add_argument("--edict-shrink", type=int, default=None, dest="edict_shrink",
                   help="override: damage shaved off their swing per turn by the edict")
    run(p.parse_args())


if __name__ == "__main__":
    main()
