#!/usr/bin/env python3
"""glarb_compare_lab.py — compare four external Glarb (Calamity's Augur) lists.

Evaluation of online lists as a possible new direction for The Calamity Tax (the
sweep's row-8 verdict: our V1-V4 are mana-gated grinders that can't race the pod).
The user's four axes: how SCARY, how QUICK, how often it HAS AN ANSWER, how SMOOTH.

This lab measures the two axes a model can measure honestly and COMPARABLY:

  QUICK  = win-line ASSEMBLY availability by turn T (drawn + with that deck's own
           tutors as wildcards) — the bake-off metric (simulate_packages). For the
           COMBO decks (#4/#5/hybrid) the win is low-mana, so assembly ≈ the real
           kill turn. For the GRIND deck (#3) the "payoff in hand" curve is a
           card-availability CEILING — its real kill is mana-gated ~T8-13 (cf. our
           Calamity V1 lab, T13), NOT the assembly turn. Flagged inline.
  ANSWER = P(>=1 interaction/protection piece in hand by turn T) (simulate_groups).
  SMOOTH = keepable opening-hand % + "has a play by T" (deck_sim.simulate floor).

NOT measured here (qualitative, see the writeup): SCARY = power/inevitability of the
win; and the mana-castability of the grind kills (we cite the Calamity precedent).
Card-availability ignores mana — trust it for the cheap combos, discount it for the
grind. Win-cons card-text-verified via card_lookup.py 2026-06-13.

Lists: decks/considering/glarb-*-20260613.txt (commanders registered in deck_sim).
"""
import importlib.util
import random
from pathlib import Path

ROOT = Path(__file__).parent.parent
_spec = importlib.util.spec_from_file_location("speed_lab_core", Path(__file__).parent / "speed_lab_core.py")
core = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(core)
ds = core.ds

CONS = ROOT / "decks" / "considering"
SEED = 20260613
TURNS = 10
SHOW = [3, 4, 5, 6, 7, 8, 10]

DECKS = [
    ("#3 Strong Glarb (grind)", CONS / "glarb-strong-ext-20260613.txt"),
    ("#4 Mastermind (Hermit combo)", CONS / "glarb-mastermind-ext-20260613.txt"),
    ("Hybrid (#3 shell + Thoracle)", CONS / "glarb-hybrid-20260613.txt"),
    ("#5 Croak & Dagger (cEDH)", CONS / "glarb-croak-dagger-ext-20260613.txt"),
]

# win line: {label: [ (member-names, tutor-names), ... ]}  (slot = members + tutors that fetch it)
WIN = {
    "#3 Strong Glarb (grind)": {
        "payoff in hand (MANA-GATED — ceiling)": [
            (["Doppelgang", "Finale of Devastation", "Rite of Replication"],
             ["Vampiric Tutor", "Green Sun's Zenith", "Chord of Calling"])]},
    "#4 Mastermind (Hermit combo)": {
        "Hermit + Thoracle/Jace (2-card)": [
            (["Hermit Druid"], ["Vampiric Tutor", "Sylvan Tutor"]),
            (["Thassa's Oracle", "Jace, Wielder of Mysteries"], ["Vampiric Tutor", "Sylvan Tutor"])]},
    "Hybrid (#3 shell + Thoracle)": {
        "Consult + Thoracle (2-card)": [
            (["Demonic Consultation"], ["Vampiric Tutor", "Demonic Tutor"]),
            (["Thassa's Oracle"], ["Vampiric Tutor", "Demonic Tutor",
                                   "Green Sun's Zenith", "Chord of Calling", "Finale of Devastation"])]},
    "#5 Croak & Dagger (cEDH)": {
        "Isochron + Dramatic Reversal (2-card)": [
            (["Isochron Scepter"], ["Vampiric Tutor", "Demonic Tutor", "Imperial Seal",
                                    "Beseech the Mirror", "Worldly Tutor"]),
            (["Dramatic Reversal"], ["Vampiric Tutor", "Demonic Tutor", "Imperial Seal",
                                     "Beseech the Mirror", "Mystical Tutor"])]},
}

ANSWERS = {
    "#3 Strong Glarb (grind)": ["Submerge", "Deadly Rollick", "Force of Vigor", "Mindbreak Trap",
                                "Blasphemous Edict", "Make an Example", "Venser, Shaper Savant",
                                "Boseiju, Who Endures", "Otawara, Soaring City", "The Meathook Massacre"],
    "#4 Mastermind (Hermit combo)": ["Damnation", "Fell the Profane", "Sink into Stupor",
                                     "Ashiok, Dream Render", "Will of the Abzan", "Will of the Sultai"],
    "Hybrid (#3 shell + Thoracle)": ["Submerge", "Deadly Rollick", "Force of Vigor", "Mindbreak Trap",
                                     "Blasphemous Edict", "Make an Example", "Venser, Shaper Savant",
                                     "Boseiju, Who Endures", "Otawara, Soaring City", "The Meathook Massacre"],
    "#5 Croak & Dagger (cEDH)": ["Force of Will", "Fierce Guardianship", "Misdirection", "Mindbreak Trap",
                                 "Snuff Out", "Baleful Mastery", "Toxic Deluge", "Deadly Rollick",
                                 "Drag to the Roots", "Opposition Agent", "Notion Thief"],
}


def mode_compare(index, aliases, trials):
    print(f"\n### GLARB DIRECTIONS — assembly/answer availability   trials={trials} seed={SEED}")
    print("    QUICK = win-line assembled & in hand by T (+own tutors as wildcards).")
    print("    Combo lines (#4/#5/hybrid) are low-mana so this ~= real kill turn;")
    print("    #3's 'payoff' curve is a MANA-GATED ceiling (real kill ~T8-13, cf. Calamity).")
    print("    ANSWER = >=1 interaction piece in hand by T.\n")
    summary = []
    for name, path in DECKS:
        lib, cmd = core.load_parsed(path, index, aliases)
        identity = set()
        for _, r in lib:
            identity.update(r["color_identity"])
        stats = ds.simulate(lib, sorted(identity), TURNS, trials, random.Random(SEED))
        pk = core.simulate_packages(lib, WIN[name], trials, random.Random(SEED + 1), TURNS)
        drawn, with_t = core.simulate_groups(lib, [ANSWERS[name]], [], trials,
                                             random.Random(SEED + 2), TURNS)
        print("=" * 78)
        print(f"  {name}   | library {len(lib)} | keepable {stats['keepable_pct']:.0f}%")
        print("  turn:".ljust(46) + "".join(f"{t:>6}" for t in SHOW))
        for label, curve in pk.items():
            print(core.row(f"WIN: {label}", curve, SHOW))
        print(core.row("ANSWER: >=1 interaction in hand", {t: drawn[t] for t in SHOW}, SHOW))
        print(core.row("(smooth) has a play by T", {t: stats['castable_by_turn'][t] for t in SHOW}, SHOW))
        win_label = list(pk)[0]
        summary.append((name, pk[win_label][6], pk[win_label][8], drawn[6], stats['keepable_pct']))
    print("=" * 78)
    print("\n  SUMMARY".ljust(46) + "win@T6  win@T8  ans@T6  keepable")
    for name, w6, w8, a6, kp in summary:
        print(f"  {name:<40}{w6:6.0f}{w8:7.0f}{a6:8.0f}{kp:9.0f}")
    print("\n  (win@T = win line assembled/in hand by turn T, +tutors; combo ~= real floor [no dig], #3 = mana-gated ceiling)")


if __name__ == "__main__":
    core.run_cli(__doc__, {"compare": mode_compare})
