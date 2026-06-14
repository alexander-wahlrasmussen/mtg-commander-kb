#!/usr/bin/env python3
"""hsh_clock_lab.py — Hashaton, Scarab's Fist (Esper Thoracle) KILL-TURN goldfish.

Built 2026-06-14 to BENCHMARK Hashaton against the bake-off finalists Yuriko
(yrk_clock_lab.py, T7/T8) and Kefka-burn (kfk_clock_lab.py, T8/T9) — same harness
(speed_lab_core.py), same SEED 20260612, so the three clocks are directly
comparable. Deck: decks/considering/hashaton-thoracle-20260614.txt (3-GC-legal:
Thassa's Oracle + Demonic Tutor + Vampiric Tutor; the cap-free cEDH version adds
Force of Will / Mystical / Imperial Seal / Consecrated Sphinx / Chrome Mox etc.).

WHAT HASHATON ACTUALLY IS (web-scouted 2026-06-14, every piece card_lookup-verified):
a Thassa's Oracle combo deck with Hashaton as a tutor/dig/resilience engine — NOT
the proposal's "fair value grind". Kill = the universal Esper line, decap = table
(kill_all by construction):

  COMBO: Thassa's Oracle {U}{U} (or Lab Maniac / Jace WoM as redundant oracles)
  + Demonic Consultation {B} (name a card not in the 95 -> exile library) or
  Tainted Pact {1}{B} (name-singleton) -> empty library -> oracle ETB wins.

  HASHATON'S CONTRIBUTION to the CLOCK (the thing being tested):
   - DIG: free repeatable discard outlets (Tireless Tribe / Putrid Imp / Ghostly
     Pilferer / Skirge Familiar) loot toward the combo (+1 effective dig/turn while
     >=1 is online); Frantic Search / Windfall / Echo of Eons wheel-dig; 9 cantrips.
   - TUTORS: 5 mana tutors that find a creature-oracle (Vampiric/Demonic/Grim/
     Wishclaw/Scheming) + 2 instant-only (Spellseeker/Solve -> the exilers) + 2
     token/artifact-fuelled (Diabolic Intent sac, Beseech the Mirror bargain ->
     free-cast Consult/Oracle at MV<=4). Plus RAZAKETH cheated in via Hashaton
     (discard it, pay {2}{U} -> 4/4 copy) = a REPEATABLE tutor (sac a token/outlet,
     2 life). This token-fuelled tutor density is the deck's real engine.
   - HULLBREAKER mana: discard Hullbreaker Horror, pay {2}{U} -> 4/4 copy (its
     "whenever you cast a spell, bounce a nonland permanent" works tapped) + any
     mana rock = infinite mana -> assemble + cast the combo. Backup line.
   - DEPLOY: with an outlet + Hashaton + {2}{U}, an oracle in hand can be DISCARDED
     and copied to win (counter-dodging; ~mana-equal in a goldfish, so it mainly
     adds resilience the lab can't score).

MANA: colour-blind lands+rocks floor + Lotus Petal banked 1 (yrk/kfk convention).
OMITTED (conservative): Astral Dragon / Rot Hulk token value, Snapcaster rebuys,
Beseech free-cast discount past the tutor, Skirge mana refund, ALL protection
(Silence/FoW-class — invisible to a goldfish; this is why a combo deck's lab clock
is a CEILING). OPTIMISTIC: rocks repeat, colour-blind, sac fodder always available
for the sac/Razaketh tutors once Hashaton is online. Trust shapes and deltas, not
second decimals — same caveats as every lab in this repo.

Data: collection/oracle-cards.json   ·   Proposal: proposals/PROP_Hashaton_Scarabs_Fist.md
"""
import importlib.util
import random
from pathlib import Path

ROOT = Path(__file__).parent.parent
_spec = importlib.util.spec_from_file_location(
    "speed_lab_core", Path(__file__).parent / "speed_lab_core.py")
slc = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(slc)
ds = slc.ds

DECK = ROOT / "decks" / "considering" / "hashaton-thoracle-20260614.txt"
SEED = 20260612            # match the bake-off so clocks are comparable
TURNS = 12
SHOW = [3, 4, 5, 6, 7, 8, 9, 10, 12]
COMMANDER = "Hashaton, Scarab's Fist"

ROCKS = {"Sol Ring": (1, 2), "Arcane Signet": (2, 1), "Dimir Signet": (2, 1),
         "Azorius Signet": (2, 1), "Orzhov Signet": (2, 1), "Fellwar Stone": (2, 1),
         "Talisman of Dominance": (2, 1), "Talisman of Progress": (2, 1)}
ORACLES = {"Thassa's Oracle": 2, "Laboratory Maniac": 3,
           "Jace, Wielder of Mysteries": 5}
EXILERS = {"Demonic Consultation": 1, "Tainted Pact": 2}
# tutor -> (cost, can_get_creature?) ; fetch a missing combo piece to hand
TUTORS = {"Vampiric Tutor": (1, True), "Demonic Tutor": (2, True),
          "Grim Tutor": (3, True), "Wishclaw Talisman": (3, True),
          "Scheming Symmetry": (1, True), "Spellseeker": (2, False),
          "Solve the Equation": (3, False)}
SAC_TUTORS = {"Diabolic Intent": 2, "Beseech the Mirror": 4}   # need sac/bargain fodder
OUTLET_COST = {"Tireless Tribe": 1, "Putrid Imp": 1, "Ghostly Pilferer": 2,
               "Skirge Familiar": 5, "Merfolk Looter": 2, "Forgotten Creation": 4,
               "Liliana of the Veil": 3}
LOOTERS = {"Merfolk Looter", "Forgotten Creation"}   # draw+discard: +1 dig/turn online
DIG_SPELLS = {"Frantic Search": 3, "Windfall": 3, "Echo of Eons": 6,
              "Whispering Madness": 4, "Memory Jar": 5}
CANTRIPS = {"Brainstorm": 1, "Ponder": 1, "Preordain": 1, "Opt": 1, "Consider": 1,
            "Sleight of Hand": 1, "Night's Whisper": 2, "Sign in Blood": 2,
            "Painful Truths": 3}


class Trial:
    def __init__(self, library, rng):
        self.g = slc.Goldfish(library, rng, rocks=ROCKS)
        self.tbl = slc.Table()
        self.bf = set()
        self.hashaton = False
        self.outlet = False
        self.infinite = False
        self.petal = 0
        self.digs = set()

    def lib_has(self, nm):
        g = self.g
        return any(g.deck[i][0] == nm for i in range(g.ptr, len(g.deck)))

    def mana(self):
        return self.g.avail + self.petal

    def spend(self, n):
        """Spend n, drawing from petals last."""
        g = self.g
        use_p = max(0, n - g.avail)
        self.petal -= use_p
        g.avail -= (n - use_p)

    def combo_check(self, T):
        g = self.g
        have_o = [o for o in ORACLES if g.has(o)]
        have_e = [e for e in EXILERS if g.has(e)]
        for o in have_o:
            for e in have_e:
                if self.mana() >= ORACLES[o] + EXILERS[e]:
                    self.spend(ORACLES[o] + EXILERS[e])
                    self.tbl.kill_all(T); return True
        # Hashaton deploy: discard an in-hand oracle, copy it after emptying library
        if self.hashaton and self.outlet and have_o and have_e:
            if self.mana() >= 3 + EXILERS[have_e[0]]:     # {2}{U} copy + exiler
                self.tbl.kill_all(T); return True
        return False

    def combo_tutor(self):
        g = self.g
        have_o = any(g.has(o) for o in ORACLES)
        have_e = any(g.has(e) for e in EXILERS)
        if have_o and have_e:
            return False
        need_creature = not have_o
        target = "Thassa's Oracle" if need_creature else "Demonic Consultation"
        if not self.lib_has(target):
            target = ("Laboratory Maniac" if need_creature else "Tainted Pact")
            if not self.lib_has(target):
                return False
        # Razaketh on bf = repeatable token-fuelled tutor (mana-free)
        if "Razaketh, the Foulblooded" in self.bf and g.fetch(target):
            return True
        for tut, (c, getcre) in TUTORS.items():
            if need_creature and not getcre:
                continue
            if g.has(tut) and g.avail >= c and self.lib_has(target) and g.fetch(target):
                self.spend(c); return True
        # sac/bargain tutors — fodder assumed once Hashaton/rocks are online
        if self.hashaton or self.bf & set(OUTLET_COST) or g.rock_out:
            for tut, c in SAC_TUTORS.items():
                if g.has(tut) and g.avail >= c and self.lib_has(target) and g.fetch(target):
                    self.spend(c); return True
        return False

    def turn(self, T):
        g = self.g
        g.begin_turn(T)
        if self.bf & LOOTERS:
            g.draw(len(self.bf & LOOTERS))    # repeatable looters dig toward combo
        g.deploy_rocks()
        if self.infinite:
            g.add_mana(9000)                  # Hullbreaker + rock: infinite mana persists
        while g.has("Lotus Petal"):
            g.hand.pop(g.in_hand("Lotus Petal")); self.petal += 1
        if self.combo_check(T):
            return
        progress = True
        while progress:
            progress = False
            if not self.hashaton and g.avail >= 2:        # commander {W}{B}
                g.avail -= 2; self.hashaton = True; progress = True
            for nm, c in OUTLET_COST.items():
                if nm not in self.bf and g.has(nm) and g.avail >= c:
                    g.cast(nm, c); self.bf.add(nm); self.outlet = True
                    progress = True; break
            for nm, c in DIG_SPELLS.items():
                if nm not in self.digs and g.has(nm) and g.avail >= c:
                    g.cast(nm, c); g.draw(2 if nm == "Frantic Search" else 3)
                    self.digs.add(nm); progress = True; break
            for nm, c in CANTRIPS.items():
                if g.has(nm) and g.avail >= c:
                    g.cast(nm, c)
                    g.draw(2 if nm in ("Night's Whisper", "Sign in Blood") else
                           3 if nm == "Painful Truths" else 1)
                    progress = True; break
            # cheat Hullbreaker / Razaketh onto bf via Hashaton (discard + {2}{U})
            if self.hashaton and self.outlet:
                for tgt in ("Hullbreaker Horror", "Razaketh, the Foulblooded"):
                    if tgt not in self.bf and g.has(tgt) and g.avail >= 3:
                        g.avail -= 3; g.hand.pop(g.in_hand(tgt)); self.bf.add(tgt)
                        if tgt == "Hullbreaker Horror" and g.rock_out:
                            self.infinite = True; g.add_mana(9000)
                        progress = True; break
            if self.combo_tutor():
                progress = True
            if self.combo_check(T):
                return


def mode_clock(index, aliases, trials):
    print("=" * 72)
    print(f"CLOCK — Hashaton (Esper Thoracle) kill-turn goldfish "
          f"({trials} trials, seed {SEED})")
    print("=" * 72)
    rng = random.Random(SEED)
    library, commander = slc.load_parsed(DECK, index, aliases)
    print(f"  library {len(library)} + commander {commander}")
    res = slc.run_goldfish(lambda: Trial(library, rng), trials, TURNS)
    slc.report_clock(res, SHOW, TURNS, trials, single=True)
    print("\n  BENCHMARK: Yuriko T7 decap / T8 table (9% never); Kefka-burn T8 / T9"
          " (11% never). Pod bar: decap T<=7.")


def mode_variants(index, aliases, trials):
    """The discard-outlet 'variations' the user weighed, built as build_lib swaps on
    the shared Thoracle base — all keep the (sound) Thoracle closer; only the ~3
    outlet/dig slots differ. Tests whether the OUTLET STRATEGY moves the combo clock."""
    print("=" * 72)
    print(f"VARIANTS — Hashaton discard-outlet packages on the Thoracle shell "
          f"({trials} trials, seed {SEED})")
    print("=" * 72)
    base, _ = slc.load_parsed(DECK, index, aliases)
    VARIANTS = {
        "cEDH base":      ([], []),
        "Looter-heavy":   (["Windfall", "Echo of Eons"],
                           ["Merfolk Looter", "Forgotten Creation"]),
        "Wheel-heavy":    (["Tireless Tribe", "Putrid Imp", "Skirge Familiar"],
                           ["Whispering Madness", "Memory Jar", "Forgotten Creation"]),
        "Hybrid (+Lili)": (["Shark Typhoon"], ["Liliana of the Veil"]),
    }
    print("  kill (decap = table, cum %) — all keep the Thoracle closer")
    print("  turns:".ljust(44) + "".join(f"{t:6d}" for t in SHOW))
    for name, (rm, ad) in VARIANTS.items():
        rng = random.Random(SEED)
        lib = slc.build_lib(base, index, rm, ad)
        res = slc.run_goldfish(lambda: Trial(lib, rng), trials, TURNS)
        nv = 100.0 * sum(1 for _, t in res if t is None) / trials
        print(slc.row(name, slc.cum(res, 1, SHOW), SHOW)
              + f"  med {slc.median(res, 1)} nv{nv:.0f}%")
    print("\n  Read: outlet flavour is a minor lever once the tutor/dig combo core is"
          " present; the closer (Thoracle) is what matters. cf. cEDH baseline T6.")


if __name__ == "__main__":
    slc.run_cli(__doc__, {"clock": mode_clock, "variants": mode_variants})
