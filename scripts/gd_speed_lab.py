#!/usr/bin/env python3
"""gd_speed_lab.py — The Grand Design (Atraxa, Grand Unifier) before/after lab.

Tests whether the 2026-05-02 6-for-6 replacement swaps
(The_Grand_Design_Swaps_2026-05-02.md) made the deck FASTER and/or MORE RELIABLE.

  OUT: Beast Within, Boseiju, Fierce Guardianship, Sakura-Tribe Elder,
       Seedborn Muse, Entomb
  IN:  Assassin's Trophy, Bojuka Bog, Force of Will, Bloom Tender,
       Rhystic Study, Grisly Salvage

Built on deck_sim.py's engine + oracle index. Three views:

  compare  Consistency (lands/colour/keepable/has-a-play/avg nonland CMC/type
           counts) + grouped kill-line availability (the stock fixed-piece sim
           can't express ">=1 of a named group by turn T").

  etb      The 2026-06-09 ETB-creature optimization pass: tests whether a $0-core
           package of ETB disruptors/tutors (Skyclave Apparition, Spellseeker,
           Noxious Gearhulk, Fierce Empath in; Grisly/Ghostly Flicker/Dread
           Return/Persist out) worsens the thin colour floor (it doesn't — land-
           neutral) and how available the new proactive ETB toolbox is, drawn vs.
           via the creature-tutor suite. Writeup in the same proposals/ folder.

  reanim   The one swap that changes a RELIABILITY quality the availability model
           can't see: Entomb (deterministic bin) -> Grisly Salvage (reveal top 5,
           random). Models P(reanimation setup online = a fat target actually in
           the yard AND a reanimate spell in hand by turn T), honouring each
           enabler's success quality. Run with the full suite (Buried Alive
           cushions the hit) and with Buried Alive removed (isolates the swap).

HEURISTIC, not a rules engine. Mana is a land-only floor plus the shared cheap
rocks/dorks; availability % ignore mana and the board. Trust the OLD-vs-NEW
delta (apples-to-apples), not the second decimal.

Writeup: proposals/Grand_Design_Speed_Curve_Analysis.md
Data: collection/oracle-cards.json (refresh via update_scryfall_data.py)
"""
import argparse
import importlib.util
import random
from pathlib import Path

ROOT = Path(__file__).parent.parent
_spec = importlib.util.spec_from_file_location("deck_sim", Path(__file__).parent / "deck_sim.py")
ds = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(ds)

OLD = ROOT / "archive" / "old_decklists" / "the-grand-design-20260402-100951.txt"
# NEW tracks the DEPLOYED list. Re-pointed 2026-06-24: the 0502 6-for-6 swap is the
# historical milestone (frozen in proposals/Grand_Design_Speed_Curve_Analysis.md and the
# 0502 file in archive/old_decklists/); it has since been folded into the deployed list,
# which ALSO already carries the 2026-06-09 finisher fix (Craterhoof in). So the POST
# column and the forward-looking modes now reflect the current deck, not the 0502 snapshot.
NEW = ROOT / "decks" / "the-grand-design-20260623.txt"
SEED = 12345
TURNS = 10
SHOW = [2, 3, 4, 5, 6, 7, 8, 10]

# ---- card sets (exact decklist names) ------------------------------------
FINALE = ["Finale of Devastation"]
DEFENSE = ["Defense of the Heart"]
REANIM_SPELLS = ["Reanimate", "Animate Dead", "Necromancy", "Persist",
                 "Victimize", "Dread Return", "Living Death"]
FAT = ["Razaketh, the Foulblooded", "Vilis, Broker of Blood",
       "Elesh Norn, Mother of Machines"]

# Dedicated mana accelerants that help power a 12-mana Finale X>=10.
# Shared by both lists, then per-list extras.
MANA_SHARED = ["Sol Ring", "Arcane Signet", "Carpet of Flowers", "Birds of Paradise",
               "Three Visits", "Nature's Lore", "Farseek"]
MANA_OLD = MANA_SHARED + ["Seedborn Muse", "Sakura-Tribe Elder"]
# Mana accelerants in the DEPLOYED list (0623 ramp suite) that help power a big Finale X.
# Defined explicitly (not via MANA_SHARED) so the POST column matches the actual deck —
# e.g. Carpet of Flowers is no longer run. Verified against the 0623 decklist 2026-06-24.
MANA_NEW = ["Sol Ring", "Arcane Signet", "Coalition Relic", "Birds of Paradise",
            "Bloom Tender", "Fanatic of Rhonas", "Three Visits", "Nature's Lore",
            "Farseek", "Kodama's Reach", "Sakura-Tribe Elder", "Springbloom Druid",
            "Solemn Simulacrum"]

# Broad creature tutors modelled as wildcards for the Finale/Defense find.
TUTORS = ["Eladamri's Call", "Chord of Calling", "Birthing Pod"]

FREE_COUNTER = {"OLD": ["Fierce Guardianship"], "NEW": ["Force of Will"]}

# Graveyard enablers: name -> (cast cost, success-kind)
ENAB_OLD = {"Buried Alive": (3, "det"), "Entomb": (1, "det"), "Fauna Shaman": (2, "fauna")}
ENAB_NEW = {"Buried Alive": (3, "det"), "Grisly Salvage": (2, "grisly"), "Fauna Shaman": (2, "fauna")}


# ==========================================================================
# grouped availability (>=1 member of every group by turn T)
# ==========================================================================
def simulate_groups(library, groups, tutors, trials, rng):
    n = len(library)
    grp_sets = [{g.lower() for g in grp} for grp in groups]
    tutor_set = {t.lower() for t in tutors}
    drawn = [0] * (TURNS + 1)
    with_t = [0] * (TURNS + 1)
    for _ in range(trials):
        deck = library[:]
        hand, _ = ds.opening_hand(deck, rng)
        seen = {nm.lower() for nm, _ in hand}
        ptr = 7
        for t in range(1, TURNS + 1):
            if t > 1 and ptr < n:
                seen.add(deck[ptr][0].lower()); ptr += 1
            satisfied = sum(1 for gs in grp_sets if gs & seen)
            missing = len(grp_sets) - satisfied
            tutors_seen = sum(1 for nm in seen if nm in tutor_set)
            if missing == 0:
                drawn[t] += 1; with_t[t] += 1
            elif tutors_seen >= missing:
                with_t[t] += 1
    return ({t: 100.0 * drawn[t] / trials for t in range(1, TURNS + 1)},
            {t: 100.0 * with_t[t] / trials for t in range(1, TURNS + 1)})


def _nonland_cmc(library):
    cmcs = [rec["cmc"] for _, rec in library if not ds.is_land(rec)]
    return sum(cmcs) / len(cmcs) if cmcs else 0.0


def _tc(library, kw):
    return sum(1 for _, rec in library if kw.lower() in rec["type_line"].lower())


def _row(label, d):
    return "  " + label.ljust(34) + "".join(f"{d[t]:6.0f}" for t in SHOW)


def load(path, index, aliases):
    library, commander, diag = ds.parse_deck(path, index, aliases)
    identity = set()
    for _, r in library:
        identity.update(r["color_identity"])
    if commander and index.get(commander.lower()):
        identity.update(index[commander.lower()]["color_identity"])
    return library, commander, diag, sorted(identity)


def mode_compare(index, aliases, trials):
    print(f"\n### COMPARE (before/after)   trials={trials} seed={SEED}\n")
    for tag, path, key in [("PRE-SWAP (20260402)", OLD, "OLD"), ("POST-SWAP (20260502)", NEW, "NEW")]:
        rng = random.Random(SEED)
        library, commander, diag, identity = load(path, index, aliases)
        stats = ds.simulate(library, identity, TURNS, trials, rng)
        print("=" * 78)
        print(f"  {tag}   library={diag['library_size']}  cmdr={commander}  identity={''.join(identity)}")
        if diag["unresolved"]:
            print(f"  UNRESOLVED: {diag['unresolved']}")
        print(f"  keepable={stats['keepable_pct']:.1f}%   avg nonland CMC={_nonland_cmc(library):.3f}"
              f"   lands={_tc(library,'land')}")
        print(f"  creatures={_tc(library,'creature')} instants={_tc(library,'instant')}"
              f" sorceries={_tc(library,'sorcery')} enchantments={_tc(library,'enchantment')}")
        print("  turn:                             " + "".join(f"{t:6}" for t in SHOW))
        print(_row("avg lands", stats["lands_by_turn"]))
        print(_row("all colours(land floor)", stats["all_colors_by_turn"]))
        print(_row("has a play", stats["castable_by_turn"]))

        mana = MANA_OLD if key == "OLD" else MANA_NEW
        enab = list(ENAB_OLD if key == "OLD" else ENAB_NEW)
        rng = random.Random(SEED)
        d, _ = simulate_groups(library, [FINALE], [], trials, rng)
        print(_row("Finale in hand (solo)", d))
        d, wt = simulate_groups(library, [FINALE, mana], TUTORS, trials, rng)
        print(_row(f"Finale + mana-engine ({len(mana)}) drawn", d))
        print(_row("Finale + mana-engine +tutors", wt))
        d, _ = simulate_groups(library, [DEFENSE], [], trials, rng)
        print(_row("Defense of the Heart (solo)", d))
        d, wt = simulate_groups(library, [enab, REANIM_SPELLS], TUTORS, trials, rng)
        print(_row("reanim pair (enabler+spell) drawn", d))
        print(_row("reanim pair +tutors", wt))
        d, _ = simulate_groups(library, [FREE_COUNTER[key]], [], trials, rng)
        print(_row(f"free counter in hand ({FREE_COUNTER[key][0]})", d))
        print()


# ==========================================================================
# reanim — determinism quality (Entomb det. vs Grisly random)
# ==========================================================================
FATSET = {c.lower() for c in FAT}
REANIMSET = {c.lower() for c in REANIM_SPELLS}
# light shared mana: a land floor + these cheap rocks/dorks when in hand & a land down
ROCKS = {"Sol Ring": 2, "Arcane Signet": 1, "Birds of Paradise": 1}


def reanim_setup(library, rng, enablers, use_buried=True):
    """First turn a fat reanimation target is actually in the yard AND a reanimate
    spell is in hand. Enabler success honoured per kind:
      det    (Buried Alive / Entomb)  -> bins a fat target with certainty
      grisly (Grisly Salvage)         -> reveal ACTUAL top 5; hit only if a fat is there
      fauna  (Fauna Shaman)           -> slow: bins a fat one turn after activation
    Mana = lands (floor) + Sol Ring/Signet/Birds when available. Apples-to-apples;
    the only structural difference between OLD and NEW is Entomb vs Grisly."""
    deck = library[:]
    hand, _ = ds.opening_hand(deck, rng)
    hand = list(hand); ptr = 7
    lands = rock = 0
    fat = False
    fauna_at = None
    enab = {k: v for k, v in enablers.items() if use_buried or k != "Buried Alive"}
    for T in range(1, TURNS + 1):
        if T > 1 and ptr < len(deck):
            hand.append(deck[ptr]); ptr += 1
        li = next((i for i, (_, r) in enumerate(hand) if ds.is_pure_land(r)), None)
        if li is None:
            li = next((i for i, (_, r) in enumerate(hand) if ds.is_land(r)), None)
        if li is not None:
            hand.pop(li); lands += 1
        for i, (nm, _) in enumerate(hand):
            if nm in ROCKS and lands >= 1:
                rock += ROCKS[nm]
        mana = lands + rock
        if fauna_at is not None and T >= fauna_at:
            fat = True
        if not fat:
            for i, (nm, _) in enumerate(hand):
                if nm in enab:
                    cost, kind = enab[nm]
                    if mana < cost:
                        continue
                    if kind == "det":
                        fat = True
                    elif kind == "grisly":
                        top5 = deck[ptr:ptr + 5]
                        if any(c[0].lower() in FATSET for c in top5):
                            fat = True
                        ptr = min(len(deck), ptr + 5)   # mills 5
                    elif kind == "fauna":
                        if fauna_at is None:
                            fauna_at = T + 1            # tutor a fat, bin it next turn
                    hand.pop(i)
                    break
        if fat and any(nm.lower() in REANIMSET for nm, _ in hand):
            return T
    return None


def _dist(results):
    return {t: 100.0 * sum(1 for r in results if r and r <= t) / len(results) for t in SHOW}


def mode_reanim(index, aliases, trials):
    print(f"\n### REANIM — P(reanimation setup online <= turn T) %   trials={trials} seed={SEED}")
    print("    setup = a fat target (Razaketh/Vilis/Elesh Norn) in the yard via a")
    print("    resolved enabler AND a reanimate spell in hand.\n")
    print("  build".ljust(36) + "".join(f"{t:>6}" for t in SHOW))
    aliases = aliases or {}
    for tag, path, enab in [("PRE-SWAP  (Entomb, det.)", OLD, ENAB_OLD),
                            ("POST-SWAP (Grisly, rng.)", NEW, ENAB_NEW)]:
        library, _, _, _ = load(path, index, aliases)
        rng = random.Random(SEED)
        res = [reanim_setup(library, rng, enab, use_buried=True) for _ in range(trials)]
        never = 100.0 * sum(1 for r in res if r is None) / trials
        d = _dist(res)
        print("  " + tag.ljust(34) + "".join(f"{d[t]:6.0f}" for t in SHOW) + f"   never={never:.0f}%")
    print("  --- Buried Alive REMOVED (isolates the swapped enabler) ---")
    for tag, path, enab in [("PRE-SWAP  (Entomb only)", OLD, ENAB_OLD),
                            ("POST-SWAP (Grisly only)", NEW, ENAB_NEW)]:
        library, _, _, _ = load(path, index, aliases)
        rng = random.Random(SEED)
        res = [reanim_setup(library, rng, enab, use_buried=False) for _ in range(trials)]
        never = 100.0 * sum(1 for r in res if r is None) / trials
        d = _dist(res)
        print("  " + tag.ljust(34) + "".join(f"{d[t]:6.0f}" for t in SHOW) + f"   never={never:.0f}%")
    # also: bare hit rate of one Grisly activation (top-5 contains a fat)
    library, _, _, _ = load(NEW, index, aliases)
    rng = random.Random(SEED)
    hits = 0
    for _ in range(trials):
        deck = library[:]; rng.shuffle(deck)
        top5 = deck[7:12]
        if any(c[0].lower() in FATSET for c in top5):
            hits += 1
    print(f"\n  Grisly single-activation hit rate (>=1 of 3 fat in a random top-5): {100.0*hits/trials:.1f}%")


# ==========================================================================
# finishers — redundancy of the kill (the 2026-06-08 optimization pass)
# ==========================================================================
def build_lib(base, index, removes, adds):
    rm = list(removes)
    lib = []
    for t in base:
        if t[0] in rm:
            rm.remove(t[0]); continue
        lib.append(t)
    for nm in adds:
        rec = index.get(nm.lower())
        if rec is None:
            raise SystemExit(f"add not in oracle: {nm}")
        lib.append((nm, rec))
    return lib


# Creature tutors that can fetch a CREATURE finisher (Craterhoof/Ibex/End-Raze).
# They canNOT fetch Finale or Triumph (sorceries) — but Finale ITSELF puts a creature
# onto the battlefield (and is a standalone overrun at X>=10), so it is BOTH a finisher
# and a Craterhoof/Ibex tutor. Defense of the Heart fetches two creatures; Razaketh/
# Sidisi/Fauna/Pod/Chord/Eladamri all reach a creature finisher. This is the whole point
# of the 2026-06-09 fix: the deck's closer is now visible to its own tutor engine.
CTUT = ["Birthing Pod", "Chord of Calling", "Eladamri's Call",
        "Defense of the Heart", "Fauna Shaman", "Sidisi, Undead Vizier",
        "Razaketh, the Foulblooded", "Finale of Devastation"]


def mode_finishers(index, aliases, trials):
    print(f"\n### FINISHERS — P(>=1 overrun finisher available by turn T) %   trials={trials} seed={SEED}")
    print("    The DEPLOYED list already carries the fix (Craterhoof in), so a creature")
    print("    finisher is now fetchable by the whole creature-tutor suite. This measures")
    print("    the CURRENT reliability and whether a 2nd/3rd tutorable creature overrun")
    print("    (Pathbreaker Ibex / End-Raze Forerunners) adds redundancy. Triumph of the")
    print("    Hordes (a 4-MV sorcery overrun) shown as the untutorable-redundancy contrast.")
    print("    drawn = a finisher in hand;  +tutors = also reachable via a creature tutor")
    print("    (Craterhoof/Ibex/End-Raze only — Finale/Triumph are sorceries tutors miss).\n")
    base, _, _, _ = load(NEW, index, aliases)
    plus_ibex = build_lib(base, index, [], ["Pathbreaker Ibex"])
    plus_two = build_lib(plus_ibex, index, [], ["End-Raze Forerunners"])
    plus_tri = build_lib(base, index, [], ["Triumph of the Hordes"])
    print("  build".ljust(40) + "".join(f"{t:>6}" for t in SHOW))
    # historical baseline: Finale alone, untutorable (why the deck used to funnel)
    rng = random.Random(SEED)
    d, _ = simulate_groups(base, [["Finale of Devastation"]], [], trials, rng)
    print(_row("Finale only, untutorable (drawn)", d))
    # current reality: Finale + Craterhoof, with the creature-tutor suite reaching it
    rng = random.Random(SEED)
    d, wt = simulate_groups(base, [["Finale of Devastation", "Craterhoof Behemoth"]], CTUT, trials, rng)
    print(_row("CURRENT  Finale+Craterhoof drawn", d))
    print(_row("CURRENT  Finale+Craterhoof +tutors", wt))
    # +Ibex (2nd tutorable creature overrun)
    rng = random.Random(SEED)
    d, wt = simulate_groups(plus_ibex,
        [["Finale of Devastation", "Craterhoof Behemoth", "Pathbreaker Ibex"]], CTUT, trials, rng)
    print(_row("+IBEX    3 finishers drawn", d))
    print(_row("+IBEX    3 finishers +tutors", wt))
    # +Ibex +End-Raze (3rd tutorable creature overrun)
    rng = random.Random(SEED)
    d, wt = simulate_groups(plus_two,
        [["Finale of Devastation", "Craterhoof Behemoth", "Pathbreaker Ibex", "End-Raze Forerunners"]],
        CTUT, trials, rng)
    print(_row("+IBEX+ENDRAZE drawn", d))
    print(_row("+IBEX+ENDRAZE +tutors", wt))
    # contrast: +Triumph (sorcery) lifts DRAWN but not the +tutors reach
    rng = random.Random(SEED)
    d, wt = simulate_groups(plus_tri,
        [["Finale of Devastation", "Craterhoof Behemoth", "Triumph of the Hordes"]], CTUT, trials, rng)
    print(_row("+TRIUMPH (sorcery) drawn", d))
    print(_row("+TRIUMPH (sorcery) +tutors", wt))
    print("\n  Read: the +tutors lift OVER drawn = the value of a FETCHABLE finisher. Each")
    print("  creature overrun (Ibex/End-Raze) raises the +tutors line; Triumph (a sorcery)")
    print("  only raises drawn. Pure additions = UPPER bound; a real add needs a cut.")
    print("  CAVEAT: all overruns are BOARD-dependent — availability != a board to swing.")


# ==========================================================================
# etb — ETB-disruption / ETB-tutor optimization pass (2026-06-09)
# ==========================================================================
# Proposed $0-core package (text-verified, GC-checked 3/3, ownership-checked):
#   OUT: Grisly Salvage, Ghostly Flicker, Dread Return, Persist
#   IN : Skyclave Apparition, Spellseeker, Noxious Gearhulk, Fierce Empath
# Question 1 (RISK): does adding two double-pip creatures (WW, BB) and cutting a
#   binner/flicker/2 reanimates measurably worsen the deck's already-thin colour
#   floor (39% all-colours-from-lands by T6)?
# Question 2 (GAIN): the current deck has almost no flickerable/reanimatable ETB
#   *removal* and CANNOT tutor noncreature interaction. How available is the new
#   proactive ETB toolbox, drawn vs. via the creature-tutor suite?
ETB_OUT = ["Grisly Salvage", "Ghostly Flicker", "Dread Return", "Persist"]
ETB_IN = ["Skyclave Apparition", "Spellseeker", "Noxious Gearhulk", "Fierce Empath"]
ETB_REMOVAL = ["Skyclave Apparition", "Noxious Gearhulk"]   # new proactive ETB removal
# noncreature interaction Spellseeker (MV<=2 instant/sorcery) can fetch, in-deck:
NC_ANSWERS = ["Counterspell", "Mana Drain", "Swan Song", "Dovin's Veto",
              "Path to Exile", "Swords to Plowshares", "Veil of Summer", "Assassin's Trophy"]


def _identity(library, commander, index):
    ident = set()
    for _, r in library:
        ident.update(r["color_identity"])
    if commander and index.get(commander.lower()):
        ident.update(index[commander.lower()]["color_identity"])
    return sorted(ident)


def mode_etb(index, aliases, trials):
    print(f"\n### ETB pass — CURRENT vs PROPOSED   trials={trials} seed={SEED}")
    print(f"    OUT {ETB_OUT}")
    print(f"    IN  {ETB_IN}\n")
    base, commander, _, _ = load(NEW, index, aliases)
    prop = build_lib(base, index, ETB_OUT, ETB_IN)
    ident = _identity(base, commander, index)

    for tag, lib in [("CURRENT", base), ("PROPOSED", prop)]:
        rng = random.Random(SEED)
        stats = ds.simulate(lib, ident, TURNS, trials, rng)
        print("=" * 78)
        print(f"  {tag}   nonland avg CMC={_nonland_cmc(lib):.3f}  creatures={_tc(lib,'creature')}"
              f"  keepable={stats['keepable_pct']:.1f}%")
        print("  turn:                             " + "".join(f"{t:6}" for t in SHOW))
        print(_row("all colours(land floor)", stats["all_colors_by_turn"]))
        print(_row("has a play", stats["castable_by_turn"]))
        print()

    print("  --- proactive ETB removal: P(>=1 of Skyclave/Noxious avail) ---")
    print("  build".ljust(40) + "".join(f"{t:>6}" for t in SHOW))
    rng = random.Random(SEED)
    d, wt = simulate_groups(prop, [ETB_REMOVAL], CTUT, trials, rng)
    print(_row("PROPOSED  drawn", d))
    print(_row("PROPOSED  + creature-tutors", wt))
    print("  (CURRENT has no flickerable/reanimatable ETB removal to compare.)\n")

    print("  --- noncreature interaction reachable (the 4/5 ceiling) ---")
    rng = random.Random(SEED)
    d, _ = simulate_groups(base, [NC_ANSWERS], [], trials, rng)
    print(_row("CURRENT  drawn (untutorable)", d))
    rng = random.Random(SEED)
    d, wt = simulate_groups(prop, [["Spellseeker"]], CTUT, trials, rng)
    print(_row("PROPOSED  Spellseeker drawn", d))
    print(_row("PROPOSED  Spellseeker +creature-tutors", wt))
    print("  (Spellseeker, unlike the spells, is itself fetchable by Pod/Chord/Eladamri's,")
    print("   so a creature-tutor can now dig to a counter/removal it could never find before.)")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--mode", choices=["compare", "reanim", "finishers", "etb", "both", "all"], default="both")
    ap.add_argument("--trials", type=int, default=40000)
    args = ap.parse_args()
    index = ds.load_oracle_index()
    aliases = ds.load_reskin_aliases()
    if args.mode in ("compare", "both", "all"):
        mode_compare(index, aliases, args.trials)
    if args.mode in ("reanim", "both", "all"):
        mode_reanim(index, aliases, args.trials)
    if args.mode in ("finishers", "all"):
        mode_finishers(index, aliases, args.trials)
    if args.mode in ("etb", "all"):
        mode_etb(index, aliases, args.trials)


if __name__ == "__main__":
    main()
