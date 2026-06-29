#!/usr/bin/env python3
"""urza_clock_lab.py — Urza "Planned Obsolescence" (mono-U artifact combo) kill-turn goldfish.

Built 2026-06-25 for the Urza, Lord High Artificer candidate
(decks/considering/planned-obsolescence-20260625.txt; 3-GC-legal: Mana Vault +
The One Ring + Cyclonic Rift). Same harness/seed family as hsh/raf so the clock is
comparable. Every card card_lookup-verified + legality/color-identity scanned 2026-06-25
(mono-U: Thopter Foundry [BUW] and Tezzeret, Agent of Bolas [BU] were caught off-color
and cut). Goldfish ceiling — unblocked, no opponent interaction.

THE KILL: assemble ANY of three redundant 2-card infinite-mana combos, then Urza's
{5} ability (no tap symbol -> repeatable with infinite mana) digs to a payoff and casts
it. decap == table (the payoff hits the whole table at once):

  INFINITE MANA (any one):
    A) Isochron Scepter (imprint Dramatic Reversal) + >= {2} from nonland permanents
       (Urza taps artifacts for U) -> copy Reversal: untap all -> infinite mana+storm.
    B) Grand Architect + Pili-Pala -> Architect taps Pili (made blue) for {C}{C};
       Pili {2}{Q} -> 1 any-color, untapping itself -> net +1/cycle = infinite colored.
    C) Power Artifact on Basalt Monolith -> Basalt {T}{C}{C}{C}, untap {3}->{1} -> +2/cycle.
  PAYOFF: Walking Ballista (cast X = infinite -> ping the table) OR Blue Sun's Zenith
    (target each opponent draws beyond their library -> decks them out). With Urza in
    play, his {5} ability finds the payoff if it isn't already in hand.

TUTOR DENSITY (the consistency this deck has and Raffine lacked): artifact tutors
(Whir/Fabricate/Reshape/Tribute/Trinket/Trophy Mage/Tezzeret the Seeker) fetch the
artifact combo pieces + Ballista; blue tutors (Merchant Scroll/Spellseeker/Muddle
transmute) fetch Dramatic Reversal/Blue Sun's/Power Artifact. Modelled per piece below.

MANA: colour-blind lands+rocks floor + Lotus Petal banked; Urza in play adds a small
artifact-tap bonus. OPTIMISTIC (ceiling): rocks repeat, colour-blind, every infinite-mana
combo's "enough enabling mana" is assumed once >= its deploy cost is available, and ALL
protection (the deck's heavy counter suite) is invisible to a goldfish. OMITTED: the
Winter Orb / Back to Basics / Static Orb stax soft-locks (pure upside vs a real pod).
Trust shapes and deltas, not second decimals.

RESULT (8000 trials, seed 20260612): bracketed by the Urza-{5}-dig proxy strength
(DIG_DRAW) — conservative draw-1 = median T8 / 49% by T7 / 8% never; generous draw-2 =
median T7 / 57% by T7 / 2% never. So **T7-8 decap=table, ~49-57% by T7** — pod-competitive
(decap T<=8) and reliable, a touch behind the Hashaton T6 benchmark. (Corrected 2026-06-29:
the Urza artifact-tap +2 was regranted on every spend() — overstating mana, ~1 turn too
fast; it's now a per-turn pool. Old read: T6-7 / 60-71% by T7.) Ceiling: opponent interaction
unmodeled; the deck's heavy mono-U counter suite + stax soft-locks are protection upside here.

Data: collection/oracle-cards.json  ·  Deck: decks/considering/planned-obsolescence-20260625.txt
"""
import importlib.util
import random
from pathlib import Path

ROOT = Path(__file__).parent.parent
_spec = importlib.util.spec_from_file_location(
    "speed_lab_core", Path(__file__).parent / "speed_lab_core.py")
slc = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(slc)
ds = slc.ds

DECK = ROOT / "decks" / "considering" / "planned-obsolescence-20260625.txt"
SEED = 20260612
TURNS = 12
SHOW = [2, 3, 4, 5, 6, 7, 8, 9, 10, 12]
COMMANDER = "Urza, Lord High Artificer"

ROCKS = {"Sol Ring": (1, 2), "Mana Vault": (1, 3), "Mind Stone": (2, 1),
         "Coldsteel Heart": (2, 1), "Sky Diamond": (2, 1), "Fellwar Stone": (2, 1),
         "Prophetic Prism": (2, 1), "Mox Amber": (1, 1), "Worn Powerstone": (3, 2),
         "Thran Dynamo": (4, 3), "Gilded Lotus": (5, 3), "Basalt Monolith": (3, 3),
         "Everflowing Chalice": (2, 1), "Palladium Myr": (3, 2),
         "Sapphire Medallion": (2, 0)}

# combos: each a pair of pieces. Deploy cost = sum of piece mvs (infinite mana then
# covers the payoff). All three are GC-free.
COMBOS = [
    ("Isochron+Reversal", ("Isochron Scepter", "Dramatic Reversal"), 4),
    ("Architect+Pili",    ("Grand Architect", "Pili-Pala"),          5),
    ("PowerArt+Basalt",   ("Power Artifact", "Basalt Monolith"),     5),
]
PAYOFFS = {"Walking Ballista": 0, "Blue Sun's Zenith": 2}   # free under infinite mana
DIG_DRAW = 2   # cards seen per Urza {5} activation (proxy: see 1 + free-play value ~= 2)

# tutor -> (cost, set-of-fetchable-pieces). Modelled from each card's real text.
ART = {"Isochron Scepter", "Pili-Pala", "Basalt Monolith", "Walking Ballista"}
BLUE = {"Dramatic Reversal", "Blue Sun's Zenith", "Power Artifact"}
TUTORS = {
    "Whir of Invention": (4, ART), "Fabricate": (3, ART), "Reshape": (3, ART),
    "Tribute Mage": (3, {"Isochron Scepter", "Pili-Pala"}),       # MV2 artifact
    "Trinket Mage": (3, {"Walking Ballista"}),                    # MV<=1 artifact
    "Trophy Mage": (3, {"Basalt Monolith"}),                      # MV3 artifact
    "Tezzeret the Seeker": (5, ART),                              # any artifact
    "Merchant Scroll": (2, {"Dramatic Reversal", "Blue Sun's Zenith"}),  # blue instant
    "Spellseeker": (3, {"Dramatic Reversal", "Blue Sun's Zenith"}),      # MV<=2 i/s
    "Muddle the Mixture": (4, {"Isochron Scepter", "Dramatic Reversal", "Pili-Pala",
                               "Power Artifact"}),               # transmute MV2
}
CANTRIPS = {"Brainstorm": 1, "Ponder": 1, "Preordain": 1, "Sensei's Divining Top": 1,
            "Chromatic Star": 1, "Aether Spellbomb": 1}
DIG = {"Frantic Search": 1, "Fact or Fiction": 3, "Dig Through Time": 2}  # net cheap dig
DRAW = {"The One Ring": 4, "Mystic Remora": 1, "Mystic Forge": 4}


class Trial:
    def __init__(self, library, rng):
        self.g = slc.Goldfish(library, rng, rocks=ROCKS)
        self.tbl = slc.Table()
        self.bf = set()
        self.urza = False
        self.petal = 0
        self.used = set()
        self.urza_pool = 0                 # Urza's artifact-tap mana, refreshed once/turn

    def mana(self):
        # +2 abstracts tapping a couple of non-rock artifacts for {U} (rocks are in avail).
        # It's a per-TURN pool that depletes as you spend — "tap an untapped artifact" is
        # once per artifact per turn, NOT regranted on every spend() (2026-06-29 audit).
        return self.g.avail + self.petal + self.urza_pool

    def spend(self, n):
        take_bonus = min(self.urza_pool, n)   # draw down the Urza pool first
        self.urza_pool -= take_bonus
        n -= take_bonus
        use_p = max(0, n - self.g.avail)
        self.petal -= use_p
        self.g.avail -= (n - use_p)

    def lib_has(self, nm):
        g = self.g
        return any(g.deck[i][0] == nm for i in range(g.ptr, len(g.deck)))

    def have(self, nm):
        return self.g.has(nm) or nm in self.bf

    def payoff_ready(self):
        # a payoff in hand, OR Urza in play to dig one (his {5} ability), OR tutorable
        if any(self.have(p) for p in PAYOFFS):
            return True
        if self.urza and any(self.lib_has(p) for p in PAYOFFS):
            return True
        return False

    def combo_check(self, T):
        for _name, (a, b), cost in COMBOS:
            if self.have(a) and self.have(b) and self.mana() >= cost and self.payoff_ready():
                self.spend(cost); self.tbl.kill_all(T); return True
        return False

    def tutor_missing(self):
        """Fetch one missing combo piece (prefer completing a combo we're half-on)."""
        g = self.g
        # rank combos: prefer ones where we already have a piece
        order = sorted(COMBOS, key=lambda c: -sum(self.have(x) for x in c[1]))
        for _name, (a, b), _cost in order:
            for piece in (a, b):
                if self.have(piece) or not self.lib_has(piece):
                    continue
                for tut, (tc, reach) in TUTORS.items():
                    if tut in self.used:
                        continue
                    # Reserve the tutor's own mana BEFORE the fetched piece is later
                    # deployed by combo_check: gate on mana()>=tc, then spend(tc). With
                    # spend() draining the finite per-turn urza_pool (2026-06-29 per-spend
                    # fix), the tutor and the combo cost can't both re-claim Urza's tap
                    # bonus — so there is no tutor-into-cast double-spend here.
                    if piece in reach and g.has(tut) and self.mana() >= tc:
                        if g.fetch(piece):
                            self.spend(tc); self.used.add(tut); return True
        # no half-combo to complete: fetch a payoff if we can't otherwise reach one
        if not self.payoff_ready():
            for p in PAYOFFS:
                if not self.lib_has(p):
                    continue
                for tut, (tc, reach) in TUTORS.items():
                    if tut in self.used:
                        continue
                    if p in reach and g.has(tut) and self.mana() >= tc and g.fetch(p):
                        self.spend(tc); self.used.add(tut); return True
        return False

    def turn(self, T):
        g = self.g
        g.begin_turn(T)
        g.deploy_rocks()
        self.urza_pool = 2 if self.urza else 0        # refresh once/turn (artifacts untap)
        while g.has("Lotus Petal"):
            g.hand.pop(g.in_hand("Lotus Petal")); self.petal += 1
        self.used = set()
        if not self.urza and self.mana() >= 4:        # deploy the commander
            self.spend(4); self.urza = True; self.urza_pool = 2   # tap her artifacts this turn
        if self.combo_check(T):
            return
        progress = True
        while progress:
            progress = False
            if not self.urza and self.mana() >= 4:
                self.spend(4); self.urza = True; self.urza_pool = 2; progress = True
            for nm, c in DRAW.items():
                if nm not in self.bf and g.has(nm) and self.mana() >= c:
                    g.cast(nm, c); self.bf.add(nm)
                    g.draw(2 if nm != "Mystic Remora" else 1); progress = True
            for nm, c in {**CANTRIPS, **DIG}.items():
                if g.has(nm) and self.mana() >= c:
                    self.spend(c); g.discard(nm)
                    g.draw(3 if nm in ("Dig Through Time", "Fact or Fiction") else
                           2 if nm == "Frantic Search" else 1)
                    progress = True; break
            if self.tutor_missing():
                progress = True
            if self.combo_check(T):
                return
            # Urza's {5} ability: exile top, play it free -> repeatable dig once he has
            # spare mana. Models the deck's real find engine (proxy: spend 5, see ~2).
            if self.urza and self.mana() >= 7:
                self.spend(5); g.draw(DIG_DRAW); progress = True
                if self.combo_check(T):
                    return


def mode_clock(index, aliases, trials):
    print("=" * 72)
    print(f"CLOCK — Urza (mono-U artifact combo) kill-turn goldfish "
          f"({trials} trials, seed {SEED})")
    print("=" * 72)
    library, commander = slc.load_parsed(DECK, index, aliases)
    print(f"  library {len(library)} + commander {commander}")
    rng = random.Random(SEED)
    res = slc.run_goldfish(lambda: Trial(library, rng), trials, TURNS)
    slc.report_clock(res, SHOW, TURNS, trials, single=True)
    print("\n  BENCHMARK: Hashaton (Esper Thoracle) T6 decap=table; Raffine reanimator")
    print("  ~16%/T12 (falsified). Pod bar: decap T<=7. 3 redundant infinite-mana combos.")


def mode_lines(index, aliases, trials):
    """Which combo carries the kill + how often each is the one that assembles."""
    print("=" * 72)
    print(f"LINES — which infinite-mana combo fires ({trials} trials, seed {SEED})")
    print("=" * 72)
    library, _ = slc.load_parsed(DECK, index, aliases)
    import collections
    rng = random.Random(SEED)
    first = collections.Counter()
    killed = 0
    for _ in range(trials):
        tr = Trial(library, rng)
        for T in range(1, TURNS + 1):
            tr.turn(T)
            if tr.tbl.done:
                killed += 1
                for name, (a, b), _c in COMBOS:
                    if tr.have(a) and tr.have(b):
                        first[name] += 1; break
                break
    print(f"  killed {100*killed/trials:.0f}% of games in {TURNS} turns; combo that was online at kill:")
    for name, _p, _c in COMBOS:
        print(f"    {name:20} {100*first[name]/max(1,killed):.0f}% of kills")


if __name__ == "__main__":
    slc.run_cli(__doc__, {"clock": mode_clock, "lines": mode_lines})
