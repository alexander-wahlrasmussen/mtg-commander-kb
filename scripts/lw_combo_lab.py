#!/usr/bin/env python3
"""lw_combo_lab.py — Fire Lord Azula COMBO-ASSEMBLY clock (deck-agnostic).

lw_clock_lab.py models OUR Lightning War BURN RACE. This lab models the thing that
race doesn't: assembling Azula's infinite/draw-deck combos (BDD review,
reference_bdd_azula_b4_combo). It runs on any Azula list, so it doubles as the
benchmark for "how fast are BDD's dedicated combo lists vs ours?".

COMBOS (Azula attacking copies the spell):
  A  Narset's Reversal + (Frantic Search OR Turnabout) -> draw the deck / infinite mana.
     All halves are INSTANTS/SORCERIES -> instant-tutors reach them.
  B  Reiterate + a Seething Song SOURCE -> infinite red mana -> Comet Storm/Crackle.
     The CURRENT deck (20260621) runs TWO sources: a standalone Seething Song (an
     INSTANT every I/S tutor reaches) AND Blazing Firesinger // Seething Song (a prepare
     CREATURE whose Seething Song half is only castable AFTER the creature is in play
     -> only an ANY-card tutor reaches that one). The standalone copy un-gates Combo B
     vs the pre-upgrade 20260614 list, which had ONLY the creature. With the standalone
     Seething Song + the doubled tutor/selection suite now maindeck, Combo B assembles
     at median ~T9 (vs never-in-horizon pre-upgrade) — a real secondary kill, not a
     fringe. The combo-lean swaps this lab once *proposed* are now APPLIED, so the old
     swap-comparison modes were retired; bench/assemble measure the shipped deck.

Two clocks, stated separately (verification rule): SEEN = Azula online + a combo's
pieces accessible (finding clock); CAST = + the mana to go off. SEEN~=CAST => finding-
gated (selection/tutors help); CAST<<SEEN => mana-gated.

HEURISTIC, not a rules engine. Mana = lands + a per-deck rock floor (FAST_MANA) +
Azula's +2 + banked Storm-Kiln treasure + rituals in hand. The rock model is mildly
GENEROUS to fast mana (persistent Moxen/Vault), so a fast deck's CAST clock is an
upper bound on its speed. Selection = a shallow conditional tutor over the top D.
Trust shapes/deltas, not second decimals.

Data: collection/oracle-cards.json
"""
import importlib.util
import random
from pathlib import Path

ROOT = Path(__file__).parent.parent
_spec = importlib.util.spec_from_file_location("speed_lab_core", Path(__file__).parent / "speed_lab_core.py")
slc = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(slc)
ds = slc.ds

OURS = ROOT / "decks" / "lightning-war-20260621.txt"                          # current list
PRIOR = ROOT / "archive" / "old_decklists" / "lightning-war-20260614.txt"     # pre-upgrade
BENCH = {
    "Lightning War (pre-upgrade 20260614)": PRIOR,
    "Lightning War (CURRENT 20260621)": OURS,
    "BDD expensive (B4 combo)": ROOT / "decks" / "considering" / "bdd-azula-expensive-20260618.txt",
    "BDD budget (B4 combo)": ROOT / "decks" / "considering" / "bdd-azula-budget-20260618.txt",
}
SEED = 20260618
TURNS = 14
SHOW = [4, 5, 6, 7, 8, 9, 10, 12]

# mana rocks across all three decks (cost, output). Mildly generous on fast mana.
FAST_MANA = {
    "Sol Ring": (1, 2), "Mana Vault": (1, 2), "Chrome Mox": (0, 1), "Mox Diamond": (0, 1),
    "Arcane Signet": (2, 1), "Fellwar Stone": (2, 1), "Dimir Signet": (2, 1),
    "Izzet Signet": (2, 1), "Rakdos Signet": (2, 1), "Fire Diamond": (2, 1),
    "Sky Diamond": (2, 1), "Talisman of Dominance": (2, 1), "Talisman of Indulgence": (2, 1),
    "Talisman of Creativity": (2, 1),
}
RITUALS = {"Dark Ritual": 2, "Desperate Ritual": 1, "Pyretic Ritual": 1, "Jeska's Will": 4}

# cheap selection (cost, dig_depth, net_draw). Sink into Stupor is a bounce, excluded.
SELECTION = {
    "Frantic Search": (0, 2, 0), "Consider": (1, 2, 1), "Faithless Looting": (1, 2, 0),
    "Valakut Awakening": (3, 2, 1), "Brainstorm": (1, 3, 1), "Ponder": (1, 3, 1),
    "Preordain": (1, 3, 1), "Serum Visions": (1, 3, 1), "Opt": (1, 2, 1),
    "Impulse": (2, 4, 1), "Sleight of Hand": (1, 2, 1), "Thrill of Possibility": (1, 2, 0),
    "Demand Answers": (1, 2, 0), "Electric Revelation": (2, 2, 0), "Sazacap's Brew": (2, 2, 0),
}
ADDED_SELECTION = set()    # the once-proposed selection package (Brainstorm/Ponder/Preordain) is now maindeck

# tutors. ANY reaches a creature (Blazing Firesinger); IS only instants/sorceries.
TUTOR_ANY = {"Demonic Tutor", "Vampiric Tutor", "Imperial Seal", "Wishclaw Talisman",
             "Gifts Ungiven", "Intuition", "Lim-Dol's Vault", "Lim-Dûl's Vault",
             "Emeritus of Woe"}
TUTOR_IS = {"Mystical Teachings", "Waterlogged Teachings", "Sanar, Unfinished Genius",
            "Mystical Tutor", "Merchant Scroll", "Muddle the Mixture", "Solve the Equation",
            "Personal Tutor"}
# instant-speed tutors -> Azula copies them in combat -> fetch TWO pieces at once
COPYABLE_TUTOR = {"Mystical Teachings", "Waterlogged Teachings", "Gifts Ungiven",
                  "Intuition", "Muddle the Mixture"}
# spell graveyard recursion: an instant/sorcery combo piece in the yard is castable
# while one of these is in hand. Grixis "second hand" (Snapcaster + the rest).
RECUR = {"Yawgmoth's Will", "Past in Flames", "Invoke Calamity", "Snapcaster Mage"}

NARSET, REIT, BF, SS = "Narset's Reversal", "Reiterate", "Blazing Firesinger", "Seething Song"
A_PARTNERS = ["Frantic Search", "Turnabout"]
IS_PIECES = {NARSET, REIT, SS, "Frantic Search", "Turnabout"}     # tutorable by IS tutors
COMBO_PIECES = IS_PIECES | {BF}    # never spend these as cantrips (Frantic Search overlaps)
NEED_A, NEED_B = 5, 7


def deck_rocks(library):
    names = {nm for nm, _ in library}
    return {nm: FAST_MANA[nm] for nm in names if nm in FAST_MANA}


def top_names(g, depth):
    return [g.deck[i][0] for i in range(g.ptr, min(g.ptr + depth, len(g.deck)))]


def assembly_turn(library, rng, rocks, g=None, dig_on=True, use_added=True, recursion_on=True):
    if g is None:                                    # lw_clock_lab.bestline injects a shared start
        g = slc.Goldfish(library, rng, rocks=rocks)
    azula_turn = None
    bf_play = stormkiln = goldspan = False
    has_ss_card = any(nm == SS for nm, _ in library)              # standalone Seething Song?
    treasure = 0
    yard = set()                                                 # I/S combo pieces in graveyard
    seen_turn = cast_turn = None

    def recur_ok():
        # a recursion enabler in hand + the mana to fire it
        return recursion_on and any(g.has(r) for r in RECUR) and (g.avail + 2) >= 5

    def have(p):                                                # in hand OR recurrable from yard
        return g.has(p) or (p in IS_PIECES and p in yard and recur_ok())

    def ss_ready():
        return (has_ss_card and have(SS)) or bf_play

    def missing():
        w = [p for p in (NARSET,) if not have(p)]
        if not any(have(p) for p in A_PARTNERS):
            w.append(A_PARTNERS[0])                               # need a partner
        if not have(REIT):
            w.append(REIT)
        if not ss_ready() and not (has_ss_card and have(SS)):
            w.append(SS if has_ss_card else BF)                   # creature in our deck
        return w

    def ready():
        a_seen = have(NARSET) and any(have(p) for p in A_PARTNERS)
        b_seen = have(REIT) and ss_ready()
        total = g.avail + 2 + treasure * (2 if goldspan else 1) \
            + sum(v for r, v in RITUALS.items() if g.has(r))
        return (a_seen or b_seen), ((a_seen and total >= NEED_A) or (b_seen and total >= NEED_B))

    def bin_to_yard(m):                                          # move a piece library->graveyard
        if g.fetch(m):
            g.discard(m); yard.add(m)

    def try_tutor(online):
        miss = missing()
        if not miss:
            return
        # Azula copies an INSTANT-speed tutor cast in her combat -> it fetches TWO
        # pieces at once (BDD's core accelerant: one copied Teachings = the whole
        # Combo A). Only reaches instant/sorcery pieces, never the creature half.
        # sorted() so the pick is hash-seed-INDEPENDENT (the model doesn't claim a "best"
        # tutor — any reaches the pieces — but a set's iteration order would make the lab
        # non-reproducible run-to-run, which the bestline golden snapshot can't tolerate).
        copyable = next((t for t in sorted(COPYABLE_TUTOR) if g.has(t)), None)
        if online and copyable and g.avail >= 4:
            g.cast(copyable, 4)
            miss_is = [x for x in miss if x in IS_PIECES]
            if copyable == "Gifts Ungiven":
                # opponent bins the pieces you need -> they go to the YARD; only
                # recursion makes them live (BDD: "everything we didn't get is now
                # in our graveyard"). Beyond 2, the surplus comes to hand.
                for m in miss_is[:2]:
                    bin_to_yard(m)
                for m in miss_is[2:4]:
                    g.fetch(m)
            else:
                for m in miss_is[:2]:
                    g.fetch(m)
            return
        if g.has("Emeritus of Woe") and g.avail >= 2:
            g.cast("Emeritus of Woe", 2); g.fetch(miss[0]); return
        anyt = next((t for t in sorted(TUTOR_ANY) if g.has(t)), None)   # sorted: hash-seed-independent
        if anyt and g.avail >= 2:
            g.cast(anyt, 2); g.fetch(miss[0]); return
        ist = next((t for t in sorted(TUTOR_IS) if g.has(t)), None)     # sorted: hash-seed-independent
        tgt = next((m for m in miss if m in IS_PIECES), None)     # IS tutors can't get the creature
        if ist and tgt and g.avail >= 3:
            g.cast(ist, 3); g.fetch(tgt)

    for T in range(1, TURNS + 1):
        g.begin_turn(T)
        g.deploy_rocks()
        if azula_turn is None and g.avail >= 4:
            g.avail -= 4; azula_turn = T
        online = azula_turn is not None and T > azula_turn

        if not bf_play and g.has(BF) and g.avail >= 3:
            g.cast(BF, 3); bf_play = True
        for nm in ("Storm-Kiln Artist", "Goldspan Dragon"):
            if g.has(nm) and g.cast(nm):
                if nm == "Storm-Kiln Artist": stormkiln = True
                else: goldspan = True

        if online:
            seen, cast = ready()
            if seen and seen_turn is None:
                seen_turn = T
            if not cast:
                try_tutor(online)
                seen, cast = ready()
                if seen and seen_turn is None:
                    seen_turn = T
            if cast and cast_turn is None:
                return T if seen_turn is None else seen_turn, T

        ncast = 0
        for nm, (cost, depth, nd) in sorted(SELECTION.items(), key=lambda x: x[1][0]):
            if nm in ADDED_SELECTION and not use_added:
                continue
            if nm in COMBO_PIECES:          # hold Frantic Search for the combo, don't cantrip it away
                continue
            while g.has(nm) and g.avail >= cost:
                g.cast(nm, cost)
                pulled = False
                if dig_on:
                    want = missing()
                    for c in top_names(g, depth):
                        if c in want:
                            g.fetch(c); pulled = True; break
                g.draw(nd if not pulled else max(0, nd - 1))
                ncast += 1
        if stormkiln:
            treasure += ncast

    return seen_turn, cast_turn


def _report(label, res):
    print(slc.row(label + " SEEN", slc.cum(res, 0, SHOW), SHOW) + f"   med {slc.median(res, 0)}")
    print(slc.row(label + " CAST", slc.cum(res, 1, SHOW), SHOW) + f"   med {slc.median(res, 1)}")


def _run(library, trials, rocks, **kw):
    rng = random.Random(SEED)
    return [assembly_turn(library, rng, rocks, **kw) for _ in range(trials)]


def _count(library, names):
    return sum(1 for nm, _ in library if nm in names)


def mode_bench(index, aliases, trials):
    print(f"\n### COMBO-ASSEMBLY BENCH — ours vs BDD's lists   trials={trials} seed={SEED}")
    print("    SEEN = Azula online + a combo's pieces accessible; CAST = + mana to go off.")
    print("    NB: for BDD this IS the kill clock (pure combo); for us the combo is a")
    print("    SECONDARY axis — our PRIMARY kill is the burn race (lw_clock_lab: decap T8/")
    print("    table T10). Tutors / cheap-selection density drives the finding clock.\n")
    print("  P(combo <= turn T) %".ljust(40) + "".join(f"{t:>6}" for t in SHOW))
    for label, path in BENCH.items():
        if not path.exists():
            print(f"  -- {label}: MISSING {path.name}"); continue
        lib, _ = slc.load_parsed(path, index, aliases)
        rocks = deck_rocks(lib)
        nt = _count(lib, TUTOR_ANY | TUTOR_IS)
        nsel = _count(lib, set(SELECTION))
        nrock = _count(lib, set(FAST_MANA))
        print(f"  -- {label}: {nt} tutors · {nsel} selection · {nrock} rocks " + "-" * 6)
        _report("   ", _run(lib, trials, rocks))


def mode_assemble(index, aliases, trials):
    print(f"\n### CURRENT DECK — bracket the dig (is the combo finding- or mana-gated?)"
          f"   trials={trials} seed={SEED}")
    print("    dig OFF = raw draw + tutors only; dig ON = + the deck's own selection. If SEEN~=CAST")
    print("    and dig moves little, the combo is FINDING-gated (more tutors help, not rituals).\n")
    cur, _ = slc.load_parsed(OURS, index, aliases)
    rk = deck_rocks(cur)
    print("  P(combo <= turn T) %".ljust(40) + "".join(f"{t:>6}" for t in SHOW))
    print("  -- current, dig OFF (raw draw + tutors) " + "-" * 8)
    _report("   ", _run(cur, trials, rk, dig_on=False))
    print("  -- current, dig ON (own selection) " + "-" * 13)
    _report("   ", _run(cur, trials, rk, dig_on=True))


if __name__ == "__main__":
    # The combo-lean swap modes (race/fast/gc/gc2/recur) were retired once their
    # recommendations shipped to the deck (standalone Seething Song + the tutor/
    # selection/recursion suite are now maindeck). bench/assemble measure the live list;
    # see git history for the swap-exploration modes (proposals/Lightning_War_Consistency_Upgrade_2026-06-18.md).
    slc.run_cli(__doc__, {"bench": mode_bench, "assemble": mode_assemble},
                default_trials=40000)
