#!/usr/bin/env python3
"""ext_glarb_vs_calamity_lab.py — rank the external "Yd Freehold" Glarb list
(proposals/External Glarb.md) against our own Glarb deck, The Croak and Dagger.

Both decks share the SAME commander (Glarb, Calamity's Augur) and the SAME
archetype (Sultai grind/value, mana-gated drain/aristocrat finish), so this is a
clean apples-to-apples on the axes a model can measure HONESTLY and COMPARABLY:

  SMOOTH  = keepable opening-hand % + "has a play by turn T" (deck_sim floor).
  ANSWER  = P(>=1 interaction in hand by T), split into FREE/near-free (0-1 mana,
            held up WHILE developing) vs TOTAL (everything incl. mana-up counters
            and sorcery-speed removal). The FREE split is the real differentiator:
            the external author himself flags "holding up 3 mana for interaction
            has felt awkward" — our build leans on a pitch/0-mana free suite.
  FINISH  = payoff-in-hand by T (+own tutors as wildcards). MANA-GATED CEILING for
            both (Glarb-grind kills are ~T8-T11 real, cf. calamity V1 lab T9), NOT
            the real kill turn. Trust the DELTA between the two decks, not the level.

NOT measured here (qualitative, see the writeup): SCARY = inevitability/scale of the
finish (our Cabal Coffers + Torment of Hailfire / Finale-X vs their Gray Merchant /
Syr Konrad incremental burn); and the fact the external list as pasted has already
CUT Bloodthirsty Conqueror, so its headline 3-card combo is not even assembled.

Card text for the win/answer lists verified via card_lookup.py 2026-06-16.
Two external land names are missing from our Scryfall snapshot; per the user they
resolve to Bojuka Bog (Barrow-Downs) and Reflecting Pool (Henneth Annun), patched
below so the external land count / keepable% is honest.
"""
import importlib.util
import json
import random
from pathlib import Path

ROOT = Path(__file__).parent.parent
_spec = importlib.util.spec_from_file_location("speed_lab_core", Path(__file__).parent / "speed_lab_core.py")
core = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(core)
ds = core.ds
_drspec = importlib.util.spec_from_file_location("deck_registry", Path(__file__).parent / "deck_registry.py")
deck_registry = importlib.util.module_from_spec(_drspec); _drspec.loader.exec_module(deck_registry)

SEED = 20260616
TURNS = 11
SHOW = [3, 4, 5, 6, 7, 8, 10]

# "CAL" = our own Glarb deck (same commander as the external list). The Croak and Dagger was
# rebuilt into Croak and Dagger; resolve the current dated list so this can't go stale.
CAL = deck_registry.resolve_deck("croak-and-dagger")
EXT = ROOT / "decks" / "considering" / "glarb-external-ext-20260616.txt"

# Land names missing from our oracle snapshot -> the real cards they stand for
# (per user): so they count as lands with correct identity in keepable/has-a-play.
_PATCH = {"barrow-downs": "Bojuka Bog", "henneth annûn": "Reflecting Pool",
          "henneth annun": "Reflecting Pool"}


def patched(lib, index):
    out = []
    for nm, rec in lib:
        if rec["type_line"] == "UNKNOWN" and nm.lower() in _PATCH:
            rec = index[_PATCH[nm.lower()].lower()]
        out.append((nm, rec))
    return out


# --- ANSWER lists (interaction held while developing) -----------------------
CAL_FREE = ["Force of Negation", "Force of Vigor", "Fierce Guardianship",
            "Pact of Negation", "Deadly Rollick", "Swan Song", "Veil of Summer"]
CAL_ALL = CAL_FREE + ["Mana Drain", "Beast Within", "Venser, Shaper Savant",
                      "Submerge", "Toxic Deluge", "The Meathook Massacre", "Massacre Wurm"]

EXT_FREE = ["Force of Vigor", "Snuff Out", "Mindbreak Trap", "An Offer You Can't Refuse"]
EXT_ALL = EXT_FREE + ["Counterspell", "Counterbalance", "Sink into Stupor",
                      "Ertai Resurrected", "Assassin's Trophy", "Baleful Mastery",
                      "Archdruid's Charm", "Colossal Skyturtle", "Fell the Profane",
                      "Toxic Deluge", "Massacre Wurm", "Culling Ritual"]

# --- FINISH ceilings (payoff in hand, +own tutors; MANA-GATED) --------------
CAL_FINISH = {"payoff in hand (MANA-GATED ceiling)": [
    (["Torment of Hailfire", "Finale of Devastation", "Gray Merchant of Asphodel"],
     ["Demonic Tutor", "Green Sun's Zenith", "Chord of Calling"])]}
EXT_FINISH = {"payoff in hand (MANA-GATED ceiling)": [
    (["Gray Merchant of Asphodel", "Syr Konrad, the Grim", "Doom Whisperer",
      "Archon of Cruelty", "Breach the Multiverse", "Abhorrent Oculus"],
     ["Chord of Calling", "Nature's Rhythm", "Archdruid's Charm"])]}

DECKS = [
    ("The Croak and Dagger (ours)", CAL, CAL_FREE, CAL_ALL, CAL_FINISH),
    ("External Glarb (Yd Freehold)", EXT, EXT_FREE, EXT_ALL, EXT_FINISH),
]

# Sensitivity: "complete the combo" — put Bloodthirsty Conqueror back over the
# off-thesis Teferi, Master of Time (the one card whose role the primer never
# describes). Tests whether re-arming the headline combo changes the picture.
COMBO_VARIANT = ("External + combo re-armed (+Bloodthirsty Conqueror / -Teferi MoT)",
                 ["Teferi, Master of Time"], ["Bloodthirsty Conqueror"])
COMBO_LINE = {"Cistern + Doom + Conqueror (3-card)": [
    (["Polluted Cistern/Dim Oubliette"], ["Archdruid's Charm", "Shifting Woodland"]),
    (["Doom Whisperer"], ["Chord of Calling", "Nature's Rhythm", "Archdruid's Charm"]),
    (["Bloodthirsty Conqueror"], ["Chord of Calling", "Nature's Rhythm"])]}


def run(index, aliases, trials):
    print(f"\n### EXTERNAL GLARB vs CROAK AND DAGGER   trials={trials} seed={SEED}")
    print("    Same commander (Glarb), same archetype. SMOOTH/ANSWER are honest &")
    print("    comparable; FINISH is a MANA-GATED ceiling (trust the delta).\n")
    rows = []
    for name, path, free, allint, finish in DECKS:
        lib, _ = core.load_parsed(path, index, aliases, warn=False)
        lib = patched(lib, index)
        identity = sorted({c for _, r in lib for c in r["color_identity"]})
        stats = ds.simulate(lib, identity, TURNS, trials, random.Random(SEED))
        fdraw, _ = core.simulate_groups(lib, [free], [], trials, random.Random(SEED + 1), TURNS)
        adraw, _ = core.simulate_groups(lib, [allint], [], trials, random.Random(SEED + 2), TURNS)
        fin = core.simulate_packages(lib, finish, trials, random.Random(SEED + 3), TURNS)
        print("=" * 84)
        print(f"  {name}   | keepable {stats['keepable_pct']:.0f}%  "
              f"| FREE-int {len(free)} cards | TOTAL-int {len(allint)} cards")
        print("  turn:".ljust(46) + "".join(f"{t:>6}" for t in SHOW))
        print(core.row("(smooth) has a play by T", {t: stats['castable_by_turn'][t] for t in SHOW}, SHOW))
        print(core.row("ANSWER: >=1 FREE interaction in hand", {t: fdraw[t] for t in SHOW}, SHOW))
        print(core.row("ANSWER: >=1 ANY interaction in hand", {t: adraw[t] for t in SHOW}, SHOW))
        for label, curve in fin.items():
            print(core.row(f"FINISH: {label}", curve, SHOW))
        rows.append((name, stats['keepable_pct'], fdraw[6], adraw[6], list(fin.values())[0][8]))

    # combo-re-armed sensitivity on the external shell
    lib, _ = core.load_parsed(EXT, index, aliases, warn=False)
    lib = patched(lib, index)
    name, rm, add = COMBO_VARIANT
    lib2 = core.build_lib(lib, index, rm, add)
    pk = core.simulate_packages(lib2, COMBO_LINE, trials, random.Random(SEED + 4), TURNS)
    print("=" * 84)
    print(f"  {name}")
    print("  turn:".ljust(46) + "".join(f"{t:>6}" for t in SHOW))
    for label, curve in pk.items():
        print(core.row(f"COMBO: {label} assembled+in hand", curve, SHOW))
    print("  (combo assembly ignores mana/life/library-size gating — an OPTIMISTIC ceiling)")

    print("=" * 84)
    print("\n  SUMMARY".ljust(46) + "keepable  free@T6  any@T6  finish@T8")
    for nm, kp, f6, a6, x8 in rows:
        print(f"  {nm:<40}{kp:9.0f}{f6:9.0f}{a6:8.0f}{x8:11.0f}")


# ===========================================================================
# CLOSING mode — does Maldhound's concise-kill subset move the closing number
# toward our Croak and Dagger, and does plan-aware mulliganing surface it?
# ===========================================================================
KEEP_SPECS = ROOT / "analysis" / "keep_specs.json"

# Maldhound's concise-kill subset (his verified named cards): kicked Rite (already
# in) + Gogo (copy the Archon/Gary trigger to win outright) + Doomsday (stack a kill
# on top, Glarb plays it off the top) + re-arm the 3-card loop (+Bloodthirsty). Cut
# his trim candidates: Scarab God (Rite-over-Scarab), High Fae Trickster, Teferi MoT.
VAR_OUT = ["The Scarab God", "High Fae Trickster", "Teferi, Master of Time"]
VAR_IN = ["Gogo, Master of Mimicry", "Bloodthirsty Conqueror", "Doomsday"]

EXT_RAMP = ["Birds of Paradise", "Deathrite Shaman", "Delighted Halfling", "Elves of Deep Shadow",
            "Carpet of Flowers", "Exploration", "Sol Ring", "Enduring Vitality",
            "Dryad of the Ilysian Grove", "Icetill Explorer", "Prismatic Undercurrents", "Hedge Shredder"]
VAR_KEY = ["Doom Whisperer", "Polluted Cistern/Dim Oubliette", "Bloodthirsty Conqueror",
           "Gogo, Master of Mimicry", "Archon of Cruelty", "Gray Merchant of Asphodel",
           "Rite of Replication", "Syr Konrad, the Grim"]
VAR_TUT = ["Chord of Calling", "Nature's Rhythm", "Archdruid's Charm", "Doomsday",
           "Lim-Dûl's Vault", "Waterlogged Teachings"]
VAR_SEL = ["Sylvan Library", "Ripples of Undeath", "Palantír of Orthanc", "Wan Shi Tong, Librarian",
           "Uro, Titan of Nature's Wrath", "Talion, the Kindly Lord", "The Unagi of Kyoshi Island",
           "Abhorrent Oculus"]

# Discrete kills with <=2 OPEN slots (slot_complete is exact only to 2). The 3-card
# loop is reported separately in `compare` (2-6% even re-armed) — too rare to model here.
# Packages are DECK-SPECIFIC: a slot's member must actually be IN that deck, and a tutor
# only counts if its target exists (else slot_complete would credit a fetch of an absent
# card). So as-is gets only the kicked-Rite line it really has; the variant adds the Gogo
# line + Doomsday as a top-stack tutor.
_CREA = ["Chord of Calling", "Nature's Rhythm", "Archdruid's Charm", "Lim-Dûl's Vault"]   # creature tutors (both decks)
_CREA_V = _CREA + ["Doomsday"]                                                            # variant adds Doomsday
CONCISE_EXT = {
    "kicked Rite on a fat creature": [
        (["Rite of Replication"], ["Lim-Dûl's Vault"]),
        (["Archon of Cruelty", "Gray Merchant of Asphodel", "Massacre Wurm"], _CREA)],
}
CONCISE_VAR = {
    "Gogo + drain trigger (Gary/Archon)": [
        (["Gogo, Master of Mimicry"], _CREA_V),
        (["Gray Merchant of Asphodel", "Archon of Cruelty"], _CREA_V)],
    "kicked Rite on a fat creature": [
        (["Rite of Replication"], ["Doomsday", "Lim-Dûl's Vault"]),
        (["Archon of Cruelty", "Gray Merchant of Asphodel", "Massacre Wurm"], _CREA_V)],
}
CAL_FINISH_LBL = "scalable X-drain (Torment/Finale/Gary)"


def mk_spec(bottleneck, key, tutors, ramp, selection, lands=(2, 4)):
    return {"bottleneck": bottleneck, "also": [], "min_lands": lands[0], "max_lands": lands[1],
            "hi_curve": False, "cmdr_cmc": 3.0, "n_selection_needed": 2,
            "key_cards": [s.lower() for s in key], "tutors": [s.lower() for s in tutors],
            "ramp": [s.lower() for s in ramp], "selection": [s.lower() for s in selection]}


def simulate_any(library, packages, trials, rng, turns):
    """P(ANY listed package complete by T) — the union over concise kill lines."""
    pk = [[({m.lower() for m in mem}, {t.lower() for t in tut}) for mem, tut in slots]
          for slots in packages.values()]
    n = len(library)
    hits = [0] * (turns + 1)
    for _ in range(trials):
        deck = library[:]
        hand, _ = ds.opening_hand(deck, rng)
        seen = {nm.lower() for nm, _ in hand}
        ptr = 7
        for t in range(1, turns + 1):
            if t > 1 and ptr < n:
                seen.add(deck[ptr][0].lower())
                ptr += 1
            if any(core.slot_complete(slots, seen) for slots in pk):
                hits[t] += 1
    return {t: 100.0 * hits[t] / trials for t in range(1, turns + 1)}


def _block(title, lib, ident, spec, trials, finish=None, concise=None):
    """Run one deck under one keep-spec; print keepable + curves. Resets the spec after."""
    ds.set_keep_spec(spec)
    try:
        stats = ds.simulate(lib, ident, TURNS, trials, random.Random(SEED))
        print(f"  {title}".ljust(56) + f"keepable {stats['keepable_pct']:.0f}%")
        print("  turn:".ljust(46) + "".join(f"{t:>6}" for t in SHOW))
        print(core.row("(smooth) has a play by T", {t: stats['castable_by_turn'][t] for t in SHOW}, SHOW))
        out = None
        if finish is not None:
            fin = core.simulate_packages(lib, finish, trials, random.Random(SEED + 3), TURNS)
            for lbl, curve in fin.items():
                print(core.row(f"FINISH: {lbl}", curve, SHOW))
            out = (stats['keepable_pct'], list(fin.values())[0][6], list(fin.values())[0][8])
        if concise is not None:
            per = core.simulate_packages(lib, concise, trials, random.Random(SEED + 4), TURNS)
            for lbl, curve in per.items():
                print(core.row(f"  · {lbl}", curve, SHOW))
            uni = simulate_any(lib, concise, trials, random.Random(SEED + 5), TURNS)
            print(core.row("CONCISE KILL (any 2-card line, +tutors)", uni, SHOW))
            out = (stats['keepable_pct'], uni[6], uni[8])
        return out
    finally:
        ds.set_keep_spec(None)


def mode_closing(index, aliases, trials):
    print(f"\n### CLOSING — Maldhound's concise-kill subset, under PLAN-AWARE mulligan   "
          f"trials={trials} seed={SEED}")
    print("    Reference bar = our Croak and Dagger (its real keep-spec, MANA).")
    print("    CONCISE = P(any board-independent 2-card kill assembled/in hand by T, +tutors).")
    print("    All curves are availability CEILINGS (ignore mana/life) — trust the DELTAS.\n")
    cal, _ = core.load_parsed(CAL, index, aliases, warn=False); cal = patched(cal, index)
    ext, _ = core.load_parsed(EXT, index, aliases, warn=False); ext = patched(ext, index)
    var = core.build_lib(ext, index, VAR_OUT, VAR_IN)
    cal_id = sorted({c for _, r in cal for c in r["color_identity"]})
    ext_id = sorted({c for _, r in ext for c in r["color_identity"]})

    cal_spec = json.loads(KEEP_SPECS.read_text(encoding="utf-8"))["croak-and-dagger"]
    ext_spec = mk_spec("MANA", [], [], EXT_RAMP, [])
    var_find = mk_spec("FINDING", VAR_KEY, VAR_TUT, EXT_RAMP, VAR_SEL)

    rows = []
    print("=" * 84)
    rows.append(("Croak and Dagger (MANA keep) [BAR]",
                 _block("Croak and Dagger  · MANA keep (reference bar)", cal, cal_id, cal_spec, trials,
                        finish={CAL_FINISH_LBL: list(CAL_FINISH.values())[0]})))
    print("=" * 84)
    rows.append(("External as-is (MANA keep)",
                 _block("External Glarb as-is  · MANA keep", ext, ext_id, ext_spec, trials, concise=CONCISE_EXT)))
    print("=" * 84)
    rows.append(("Maldhound variant (default keep)",
                 _block("Maldhound concise-kill variant  · DEFAULT land keep", var, ext_id, None, trials, concise=CONCISE_VAR)))
    print("=" * 84)
    rows.append(("Maldhound variant (FINDING keep)",
                 _block("Maldhound concise-kill variant  · FINDING keep (mulligan toward kill)", var, ext_id, var_find, trials, concise=CONCISE_VAR)))
    print("=" * 84)
    print("\n  SUMMARY".ljust(50) + "keepable   @T6    @T8   (FINISH for the bar, else CONCISE-kill)")
    for nm, m in rows:
        kp, a6, a8 = m
        print(f"  {nm:<46}{kp:7.0f}{a6:7.0f}{a8:7.0f}")
    print("\n  Read: does the variant's CONCISE-kill availability (and the FINDING-keep lift)")
    print("  approach the bar's FINISH availability? The 3-card loop stays rare (see `compare`).")


# ===========================================================================
# UPGRADE mode — steal the external's best ideas INTO our Croak and Dagger.
# +Counterbalance (buy; soft-counter, exceptional w/ Glarb's known top card)
# +Wan Shi Tong (OWNED $0; draw engine)  +Abhorrent Oculus (buy; dig/board engine)
# for -Submerge (narrowest answer) -Open the Way (redundant ramp) -Spore Frog (one-shot fog).
# All adds are non-GC -> deck stays 3/3 GC. card text verified 2026-06-16.
# ===========================================================================
UP_OUT = ["Submerge", "Open the Way", "Spore Frog"]
UP_IN = ["Counterbalance", "Wan Shi Tong, Librarian", "Abhorrent Oculus"]


def mode_upgrade(index, aliases, trials):
    print(f"\n### UPGRADE PASS — Croak and Dagger + external's best ideas   trials={trials} seed={SEED}")
    print("    -Submerge/-Open the Way/-Spore Frog  +Counterbalance/+Wan Shi Tong/+Abhorrent Oculus.")
    print("    Counterbalance counts in TOTAL interaction (deploy-2 then free); the rest are")
    print("    card-advantage/board engines whose value is in axes this lab does NOT score.\n")
    cal, _ = core.load_parsed(CAL, index, aliases, warn=False); cal = patched(cal, index)
    up = core.build_lib(cal, index, UP_OUT, UP_IN)
    rows = []
    for name, lib, allint in [("Croak and Dagger — current", cal, CAL_ALL),
                              ("Croak and Dagger — UPGRADED", up, CAL_ALL + ["Counterbalance"])]:
        ident = sorted({c for _, r in lib for c in r["color_identity"]})
        stats = ds.simulate(lib, ident, TURNS, trials, random.Random(SEED))
        fdraw, _ = core.simulate_groups(lib, [CAL_FREE], [], trials, random.Random(SEED + 1), TURNS)
        adraw, _ = core.simulate_groups(lib, [allint], [], trials, random.Random(SEED + 2), TURNS)
        fin = core.simulate_packages(lib, CAL_FINISH, trials, random.Random(SEED + 3), TURNS)
        print("=" * 84)
        print(f"  {name}   | keepable {stats['keepable_pct']:.0f}%  | TOTAL-int {len(allint)} cards")
        print("  turn:".ljust(46) + "".join(f"{t:>6}" for t in SHOW))
        print(core.row("(smooth) has a play by T", {t: stats['castable_by_turn'][t] for t in SHOW}, SHOW))
        print(core.row("ANSWER: >=1 FREE interaction in hand", {t: fdraw[t] for t in SHOW}, SHOW))
        print(core.row("ANSWER: >=1 ANY interaction in hand", {t: adraw[t] for t in SHOW}, SHOW))
        print(core.row("FINISH: X-drain payoff (mana-gated)", list(fin.values())[0], SHOW))
        rows.append((name, stats['keepable_pct'], fdraw[6], adraw[6], list(fin.values())[0][8]))
    print("=" * 84)
    print("\n  SUMMARY".ljust(46) + "keepable  free@T6  any@T6  finish@T8")
    for nm, kp, f6, a6, x8 in rows:
        print(f"  {nm:<40}{kp:9.0f}{f6:9.0f}{a6:8.0f}{x8:11.0f}")
    print("\n  (FREE/FINISH should be ~flat — no free counters or finishers added. ANY-int rises")
    print("   with Counterbalance. The real lift = Glarb+Counterbalance lock + draw/board engines,")
    print("   axes this availability lab can't score — same lesson as every prior upgrade pass.)")


if __name__ == "__main__":
    core.run_cli(__doc__, {"compare": run, "closing": mode_closing, "upgrade": mode_upgrade})
