#!/usr/bin/env python3
"""delay_lab.py — answer-availability ("counter-clock") lab vs the pod's combo turn.

Post-bake-off follow-up (2026-06-12, user request). The Stage-3 clock labs
measured how fast WE kill; the other clock is how reliably we can DISRUPT the
recurring pod combo deck's T6-7 win attempt (project_pod_combo_opponent:
Ur-Dragon + Hidetsugu/Kairi/Kenrith/Kinnan shells, wins behind Grand
Abolisher). Key user correction baked into the design: **Abolisher is a drawn
card, not a constant** — so this lab measures OUR answer availability as
scenario CONDITIONALS and composes them across a swept P(Abolisher out).

SCENARIOS on the opponent's key turn K (we are assumed earlier in turn order,
so we have completed our turn K — a half-turn optimism, shared by all configs):

  A   no Abolisher out. Live: reactive answers (counters, instant removal)
      held with mana open, plus any deployed static.
  B1  Abolisher out with >=1 turn of window. Verified rules fact: Abolisher
      stops ALL our spells on their turn (not just counters). Live: deployed
      statics, OR own-turn removal on OUR turn K (kill Abolisher / the visible
      piece) followed by a held reactive answer (cost_removal + cost_react <=
      our mana — lands tapped on our turn stay tapped on theirs).
  B2  Abolisher dropped the same turn as the combo (no window). Statics only.

  P(disrupt) = (1-a)*A + a*( w*B1 + (1-w)*B2 ),  a swept 0..1, w = --window.

COVERAGE WEIGHTS — judgment parameters, printed with results, NOT measured:
the pod rotates 4 shells; Kinnan/Kenrith/Hidetsugu win through ACTIVATED
abilities (Cursed Totem / Phyrexian Revoker class works; a counterspell
cannot counter an activation), Kairi through spells/triggers.
  W_STATIC  = 0.75  (activation share, 3 of 4 known shells)
  W_REMOVAL = 0.90  (combo pieces are creatures; discount for boots/greaves)
  W_COUNTER = 0.50  (full vs spell lines, partial vs activation lines — the
                     key turn usually still casts *something*)

CEILING CONVENTIONS (same philosophy as the clock labs — trust deltas, not
absolutes): a seen singleton is a held singleton; mana = lands-only floor
(min(turn, lands seen)); we are always willing to hold mana open; the tutor
variant pays tutor + target in one turn. This lab measures answer
AVAILABILITY, not EFFECTIVENESS — a live answer does not model their backup
lines, a second protection piece, or recursion. Decap/table racing is the
other half of the matchup and lives in the *_clock_lab.py results.

CLASSIFICATION (oracle text verified via card_lookup.py / oracle dump,
2026-06-12). Excluded on verified text, per deck below: redirects (Deflecting
Swat, Bolt Bend — the pod loops aren't single-target-dependent),
combat-conditioned pieces (Dokuchi Silencer, Hope of Ghirapur), protect-own
(Siren Stormtamer, Fugitive Droid, Greaves/Boots), sorcery tempo/steal that
doesn't answer a key turn (Consuming Tide, Blatant Thievery), narrow tutors
(Demonic Counsel demon-only sans delirium, Step Through wizard-only, Lively
Dirge fetches to yard). Cost overrides documented inline.

Configs: the bake-off pick (Yuriko), the fallback (Kefka-burn), the fallback +
the 3-card Kefka-external port (-Negate -Arcane Denial -An Offer / +Phyrexian
Revoker +Volatile Stormdrake +Fire Covenant), and Kefka-external itself as the
counter-wall calibrator.

Data: collection/oracle-cards.json (refreshed 2026-06-12)
Writeup: proposals/Delay_Lab_Disruption_Analysis_2026-06-12.md
"""
import argparse
import importlib.util
import random
from pathlib import Path

ROOT = Path(__file__).parent.parent
_spec = importlib.util.spec_from_file_location(
    "speed_lab_core", Path(__file__).parent / "speed_lab_core.py")
slc = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(slc)
ds = slc.ds

SEED = 20260612
KS = [5, 6, 7, 8]            # the opponent's candidate key turns
A_SWEEP = [0.0, 0.25, 0.50, 0.75, 1.0]   # P(Abolisher out on the key turn)

W_STATIC, W_REMOVAL, W_COUNTER = 0.75, 0.90, 0.50

# answer spec: name -> (classes, effective_cost, tags)
#   classes subset of {"C","R","P","S"}: Counter / Reactive removal (instant) /
#   Preempt-capable on our own turn / Static. Every instant R is also P.
#   tags: "ios" instant-or-sorcery (Mystical/Solve fetchable),
#         "ublue" blue instant (Merchant Scroll fetchable).
# tutor spec: name -> (cost, filter) with filter in {"any","ios","ublue","mv2"};
#   "mv2" = transmute for mana value exactly 2 (real MV, not the override).

YURIKO = {
    "answers": {
        "Counterspell":             ({"C"}, 2, {"ios", "ublue"}),
        "Mana Drain":               ({"C"}, 2, {"ios", "ublue"}),
        "Swan Song":                ({"C"}, 1, {"ios", "ublue"}),
        "Spell Pierce":             ({"C"}, 1, {"ios", "ublue"}),
        "An Offer You Can't Refuse": ({"C"}, 1, {"ios", "ublue"}),
        "Dispel":                   ({"C"}, 1, {"ios", "ublue"}),
        "Commandeer":               ({"C"}, 7, {"ios", "ublue"}),  # pitch-cast ignored: underestimates
        "Go for the Throat":        ({"R", "P"}, 2, {"ios"}),
        "Fatal Push":               ({"R", "P"}, 1, {"ios"}),      # MV<=2 catches Kinnan/Abolisher
        "Murderous Cut":            ({"R", "P"}, 3, {"ios"}),      # delve override (MV5; Yuriko bins fast)
        "Curtains' Call":           ({"R", "P"}, 3, {"ios"}),      # undaunted, 3 opponents (MV6)
        "Bloodchief's Thirst":      ({"P"}, 1, {"ios"}),           # SORCERY: preempt only; unkicked hits MV<=2
    },
    "tutors": {
        "Demonic Tutor": (2, "any"), "Wishclaw Talisman": (4, "any"),  # cast 2 + activate 1+tap
        "Mystical Tutor": (1, "ios"), "Merchant Scroll": (2, "ublue"),
        "Solve the Equation": (3, "ios"), "Lim-Dûl's Vault": (2, "any"),  # dig-to-top, modelled broad
    },
}

KEFKA_BURN = {
    "answers": {
        "Counterspell":             ({"C"}, 2, {"ios"}),
        "Negate":                   ({"C"}, 2, {"ios"}),
        "Swan Song":                ({"C"}, 1, {"ios"}),
        "An Offer You Can't Refuse": ({"C"}, 1, {"ios"}),
        "Arcane Denial":            ({"C"}, 2, {"ios"}),
        "Drown in the Loch":        ({"C", "R", "P"}, 2, {"ios"}),  # genuinely both modes
        "Bedevil":                  ({"R", "P"}, 3, {"ios"}),
        "Terminate":                ({"R", "P"}, 2, {"ios"}),
        "Go for the Throat":        ({"R", "P"}, 2, {"ios"}),
        "Infernal Grasp":           ({"R", "P"}, 2, {"ios"}),
        "Rakdos Charm":             ({"R", "P"}, 2, {"ios"}),
        "Chaos Warp":               ({"R", "P"}, 3, {"ios"}),
        "Bloodchief's Thirst":      ({"P"}, 1, {"ios"}),
        "Blasphemous Act":          ({"P"}, 5, {"ios"}),            # cost-reduction judgment override (MV9)
        "Cursed Totem":             ({"S"}, 2, set()),
    },
    "tutors": {
        "Demonic Tutor": (2, "any"), "Diabolic Tutor": (4, "any"),
        "Mastermind's Acquisition": (4, "any"),
    },
}

# the 3-card port from the Kefka-external scout (availability checked 2026-06-12:
# Stormdrake owned free / Revoker + Fire Covenant = buys, Genome's Covenant protected)
PORT_REMOVES = ["Negate", "Arcane Denial", "An Offer You Can't Refuse"]
PORT_ADDS = {
    "Phyrexian Revoker":   ({"S"}, 2, set()),        # names Kinnan/Kenrith/Hidetsugu (informed by key turn)
    "Volatile Stormdrake": ({"P"}, 2, set()),        # own-turn theft; can take Abolisher itself (MV2 <= 4 energy)
    "Fire Covenant":       ({"R", "P"}, 3, {"ios"}), # X-life multi-kill: Abolisher AND a dork in one instant
}

KEFKA_EXT = {
    "answers": {
        "An Offer You Can't Refuse": ({"C"}, 1, {"ios"}),
        "Arcane Denial":            ({"C"}, 2, {"ios"}),
        "Delay":                    ({"C"}, 2, {"ios"}),
        "Dispel":                   ({"C"}, 1, {"ios"}),
        "Drown in the Loch":        ({"C", "R", "P"}, 2, {"ios"}),
        "Memory Lapse":             ({"C"}, 2, {"ios"}),
        "Miscast":                  ({"C"}, 1, {"ios"}),
        "Spell Pierce":             ({"C"}, 1, {"ios"}),
        "Malevolent Hermit":        ({"C"}, 2, set()),  # sac = OUR creature ability on THEIR turn: Abolisher-dead too
        "Lightning Bolt":           ({"R", "P"}, 1, {"ios"}),
        "Fatal Push":               ({"R", "P"}, 1, {"ios"}),
        "Abrade":                   ({"R", "P"}, 2, {"ios"}),
        "Fire Covenant":            ({"R", "P"}, 3, {"ios"}),
        "Suspend":                  ({"R", "P"}, 1, {"ios"}),   # temporary exile: answers the key turn
        "Snapback":                 ({"R", "P"}, 1, {"ios"}),   # pitch override (MV2): bounce, tempo only
        "Unsubstantiate":           ({"R", "P"}, 2, {"ios"}),
        "Retraction Helix":         ({"R"}, 1, {"ios"}),        # needs an untapped creature; reactive only
        "Volatile Stormdrake":      ({"P"}, 2, set()),
        "Phyrexian Revoker":        ({"S"}, 2, set()),
    },
    "tutors": {
        "Wishclaw Talisman": (4, "any"),
        "Ringsight": (3, "any"),       # needs a legendary creature out; Grixis shares broadly — optimistic
        "Shred Memory": (3, "mv2"),    # transmute: MV-2 targets only (Revoker, Counterspell-class)
    },
}


def fits(filt, entry, real_mv):
    classes, cost, tags = entry
    if filt == "any":
        return True
    if filt == "ios":
        return "ios" in tags
    if filt == "ublue":
        return "ublue" in tags
    if filt == "mv2":
        return real_mv == 2
    return False


def check_names(label, lib, spec):
    names = {nm for nm, _ in lib}
    missing = [n for n in list(spec["answers"]) + list(spec["tutors"]) if n not in names]
    if missing:
        raise SystemExit(f"{label}: spec names not in parsed deck: {missing}")


def simulate(label, lib, spec, trials, rng, window):
    answers, tutors = spec["answers"], spec["tutors"]
    mv = {nm: rec["cmc"] for nm, rec in lib if nm in answers}
    cnt = {k: {"C": 0, "R": 0, "S": 0, "PR": 0, "TC": 0, "TR": 0, "TS": 0} for k in KS}
    comp = {k: {a: [0.0, 0.0] for a in A_SWEEP} for k in KS}   # [drawn, with-tutors]

    for _ in range(trials):
        deck = lib[:]
        hand, _m = ds.opening_hand(deck, rng)
        seen, lands = set(), 0
        for nm, rec in hand:
            seen.add(nm)
            if ds.is_land(rec):
                lands += 1
        ptr = 7
        for K in range(2, max(KS) + 1):
            if ptr < len(deck):
                nm, rec = deck[ptr]; ptr += 1
                seen.add(nm)
                if ds.is_land(rec):
                    lands += 1
            if K not in cnt:
                continue
            M = min(K, lands)
            held = [(n,) + answers[n] for n in seen if n in answers]
            C = any("C" in c and cost <= M for _, c, cost, _t in held)
            R = any("R" in c and cost <= M for _, c, cost, _t in held)
            S = any("S" in c and cost <= M for _, c, cost, _t in held)
            PRr = PRc = False
            pre = [(n, cost) for n, c, cost, _t in held if "P" in c]
            for pn, pc in pre:
                for qn, qc, qcost, _t in held:
                    if qn == pn or pc + qcost > M:
                        continue
                    if "R" in qc:
                        PRr = True
                    if "C" in qc:
                        PRc = True
            # tutor variant: fetch an unseen answer, tutor + target in one payment
            TC, TR, TS = C, R, S
            tut = [(n, tutors[n]) for n in seen if n in tutors]
            if tut:
                unseen = [(n,) + answers[n] for n in answers if n not in seen]
                for _tn, (tc, filt) in tut:
                    for n, c, cost, tags in unseen:
                        if tc + cost <= M and fits(filt, (c, cost, tags), mv[n]):
                            TC = TC or "C" in c
                            TR = TR or "R" in c
                            TS = TS or "S" in c
            for key, val in (("C", C), ("R", R), ("S", S), ("PR", PRr or PRc),
                             ("TC", TC), ("TR", TR), ("TS", TS)):
                cnt[K][key] += val
            effA = 1 - (1 - W_STATIC * S) * (1 - W_REMOVAL * R) * (1 - W_COUNTER * C)
            effA_t = 1 - (1 - W_STATIC * TS) * (1 - W_REMOVAL * TR) * (1 - W_COUNTER * TC)
            effB1 = 1 - (1 - W_STATIC * S) * (1 - W_REMOVAL * PRr) * (1 - W_COUNTER * PRc)
            effB1_t = 1 - (1 - W_STATIC * TS) * (1 - W_REMOVAL * PRr) * (1 - W_COUNTER * PRc)
            for a in A_SWEEP:
                comp[K][a][0] += (1 - a) * effA + a * (window * effB1 + (1 - window) * W_STATIC * S)
                comp[K][a][1] += (1 - a) * effA_t + a * (window * effB1_t + (1 - window) * W_STATIC * TS)

    nC = sum(1 for v in answers.values() if "C" in v[0])
    nR = sum(1 for v in answers.values() if "R" in v[0])
    nS = sum(1 for v in answers.values() if "S" in v[0])
    nP = sum(1 for v in answers.values() if v[0] == {"P"})
    print(f"\n== {label} ==")
    print(f"  suite: {nC} counters / {nR} instant removal / {nP} preempt-only / "
          f"{nS} statics ; {len(tutors)} tutors")
    print("  measured availability, % of games (drawn-only):"
          + "".join(f"   their T{k}" for k in KS))
    rows = [("counter held + mana open  (C)", "C"), ("instant removal held      (R)", "R"),
            ("static deployed           (S)", "S"), ("preempt->reactive chain  (B1)", "PR"),
            ("C with tutors", "TC"), ("R with tutors", "TR"), ("S with tutors", "TS")]
    for txt, key in rows:
        print("    " + txt.ljust(34)
              + "".join(f"{100.0 * cnt[k][key] / trials:10.0f}" for k in KS))
    print(f"  composed P(disrupt their key turn)  [w(indow)={window}]:")
    print("    " + "P(Abolisher out) ->".ljust(34)
          + "".join(f"{int(a * 100):9d}%" for a in A_SWEEP))
    for k in (6, 7):
        for j, lab in ((0, "drawn"), (1, "+tutors")):
            print(f"    their T{k} {lab}".ljust(38)
                  + "".join(f"{100.0 * comp[k][a][j] / trials:10.0f}" for a in A_SWEEP))
    return comp


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--trials", type=int, default=20000)
    ap.add_argument("--seed", type=int, default=SEED)
    ap.add_argument("--window", type=float, default=0.5,
                    help="P(Abolisher deployed >=1 turn before the combo | out)")
    args = ap.parse_args()
    rng = random.Random(args.seed)
    index = ds.load_oracle_index()
    aliases = ds.load_reskin_aliases()

    cons = ROOT / "decks" / "considering"
    yur, _ = slc.load_parsed(cons / "insider-trading-20260612.txt", index, aliases)
    kfk, _ = slc.load_parsed(cons / "forced-liquidation-20260612.txt", index, aliases)
    ext, _ = slc.load_parsed(cons / "kefka-external-20260612.txt", index, aliases)
    port = slc.build_lib(kfk, index, PORT_REMOVES, list(PORT_ADDS))
    burn_port = {"answers": {n: v for n, v in KEFKA_BURN["answers"].items()
                             if n not in PORT_REMOVES} | PORT_ADDS,
                 "tutors": KEFKA_BURN["tutors"]}

    configs = [
        ("Yuriko / Insider Trading (the pick)", yur, YURIKO),
        ("Kefka-burn / Forced Liquidation (fallback)", kfk, KEFKA_BURN),
        ("Kefka-burn + 3-card port (-Negate -ArcDenial -AnOffer "
         "/ +Revoker +Stormdrake +FireCov)", port, burn_port),
        ("Kefka-external (counter-wall calibrator)", ext, KEFKA_EXT),
    ]
    print(f"delay_lab — trials={args.trials} seed={args.seed} window={args.window}")
    print(f"weights (judgment): static {W_STATIC} / removal {W_REMOVAL} / counter {W_COUNTER}")
    for label, lib, spec in configs:
        check_names(label, lib, spec)
        simulate(label, lib, spec, args.trials, random.Random(args.seed), args.window)


if __name__ == "__main__":
    main()
