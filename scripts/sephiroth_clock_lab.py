#!/usr/bin/env python3
"""sephiroth_clock_lab.py — Sephiroth aristocrats KILL-TURN goldfish (combo-assembly clock).

The Sephiroth-commander variant of the Diminishing Returns rebuild. The thesis vs the
yawgmoth_clock_lab version: the diagnosed bottleneck was REDUNDANCY in two singleton slots —
the undying enabler and the DRAIN payoff (mana was 0%-gated). This build fixes both:

  * Sephiroth, Fabled SOLDIER (commander, card_lookup 2026-06-19): "Whenever another creature
    dies, target opponent loses 1 life and you gain 1." => the DRAIN now lives in the command
    zone, always available (and on its 4th-death transform it becomes a removal-proof EMBLEM).
  * Targeted BUYS add undying + drain redundancy the collection lacked: Geralf's Messenger
    (undying + ETB drain 2), Butcher Ghoul (undying), Putrid Goblin (persist); Blood Artist,
    Bastion of Remembrance, Vengeful Bloodwitch (extra drains); Pawn of Ulamog (death fuel).

KILL = board-independent, own-turn, Abolisher-proof INFINITE DRAIN (decap == table). Lines
(all pieces verified 2026-06-19), drain supplied by the commander so each is ~1 piece shorter:
  A) Yawgmoth (in the 99) + drain + TWO undying bodies (printed undying, or — with Mikaeus —
     any two non-Human bodies, since Mikaeus grants undying). Yawgmoth's -1/-1 is the reset.
  B) Gravecrawler + Phyrexian Altar + a Zombie source + drain (mana-neutral recast loop).
  (Excluded from this clock: Mikaeus + Walking Ballista is a 2-card infinite => house-rule
   GATED on pod approval, so it is NOT counted as a free kill here.)

OPTIMISTIC: no interaction; mana = lands+rocks floor (Cabal Coffers + Urborg big-mana OMITTED
  => understates mana, but the diagnostic showed mana isn't the gate). CONSERVATIVE/OMITTED:
  the Sephiroth/Geralf's/Gray-Merchant incremental CHIP plan is unmodelled (this lab is the
  COMBO clock only); the gated Mikaeus+Ballista line is excluded. Trust shapes, not decimals.
  decap == table by construction (infinite hit-all). Bracketed on the draw engines, as the
  yawgmoth lab is, for apples-to-apples comparison.

Data: collection/oracle-cards.json (refresh via update_scryfall_data.py)
Run:  python scripts/sephiroth_clock_lab.py --trials 40000
"""
import importlib.util
import random
from pathlib import Path

ROOT = Path(__file__).parent.parent
_spec = importlib.util.spec_from_file_location(
    "speed_lab_core", Path(__file__).parent / "speed_lab_core.py")
slc = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(slc)
ds = slc.ds

DECK = ROOT / "decks" / "considering" / "sephiroth-liquidation-20260619.txt"
SEED = 20260619
TURNS = 14
SHOW = [4, 5, 6, 7, 8, 9, 10, 12]

COMMANDER = "Sephiroth, Fabled SOLDIER"
ROCKS = {"Sol Ring": (1, 2), "Mind Stone": (2, 1), "Arcane Signet": (2, 1)}
DRAIN = {"Zulaport Cutthroat", "Blood Artist", "Bastion of Remembrance",
         "Vengeful Bloodwitch", "Syr Konrad, the Grim"}     # + commander (always)
UNDYING = {"Geralf's Messenger", "Butcher Ghoul", "Putrid Goblin"}   # printed undying
ZOMBIE_SRC = {"Cryptbreaker", "Ghoulcaller Gisa", "Dreadhorde Invasion", "Carrier Thrall"}
TOKEN_ENG = {"Bitterblossom", "Dreadhorde Invasion", "Cryptbreaker"}  # ~1 body/turn
TUTORS = {"Demonic Tutor", "Grim Tutor", "Diabolic Intent",
          "Sidisi, Undead Vizier", "Razaketh, the Foulblooded"}
DRAW_ENGINES = {"Necropotence", "Bolas's Citadel", "Phyrexian Arena", "Skullclamp",
                "Black Market Connections", "Vilis, Broker of Blood", "Midnight Reaper"}
STRONG = {"Necropotence", "Bolas's Citadel"}
KEY_B = {"Gravecrawler", "Phyrexian Altar"}


def is_creature(rec): return "Creature" in rec.get("type_line", "")
def is_human(rec):
    tl = rec.get("type_line", "")
    return "—" in tl and "Human" in tl.split("—")[1]


class Trial:
    def __init__(self, library, rng, dig=4, gated=False):
        self.g = slc.Goldfish(library, rng, rocks=ROCKS)
        self.rng = rng
        self.dig = dig
        self.gated = gated         # True = also allow the pod-GATED 2-card Mikaeus+Ballista
        self.tbl = slc.Table()
        self.inplay = set()
        self.seph = False          # commander in play => drain online
        self.bodies = 0            # creatures in play (combo fodder proxy)
        self.undying = 0           # printed-undying bodies in play
        self.draw_weight = 0

    def _drain(self):
        return self.seph or any(n in self.inplay for n in DRAIN)

    def _line_a(self):
        return ("Yawgmoth, Thran Physician" in self.inplay and self._drain()
                and (self.undying >= 2
                     or ("Mikaeus, the Unhallowed" in self.inplay and self.bodies >= 2)))

    def _line_b(self):
        return (KEY_B <= self.inplay and self._drain()
                and any(n in self.inplay for n in ZOMBIE_SRC))

    def _line_c(self):   # GATED 2-card infinite: Mikaeus + Walking Ballista (no drain needed)
        return (self.gated and "Mikaeus, the Unhallowed" in self.inplay
                and "Walking Ballista" in self.inplay)

    def _missing(self):
        # steer a tutor toward the nearest line. If gated and Mikaeus is already down,
        # Ballista COMPLETES the 2-card line — grab it; otherwise pursue the redundant
        # house-legal lines (chasing two unique singletons is slower than redundancy).
        if self.gated and "Mikaeus, the Unhallowed" in self.inplay \
                and "Walking Ballista" not in self.inplay:
            return "Walking Ballista"
        if self._drain():
            if "Yawgmoth, Thran Physician" not in self.inplay:
                return "Yawgmoth, Thran Physician"
            if self.undying < 2 and "Mikaeus, the Unhallowed" not in self.inplay:
                return "Mikaeus, the Unhallowed"
            if "Gravecrawler" not in self.inplay:
                return "Gravecrawler"
            if "Phyrexian Altar" not in self.inplay:
                return "Phyrexian Altar"
        return "Yawgmoth, Thran Physician"

    def turn(self, T):
        g = self.g
        g.begin_turn(T)
        g.deploy_rocks()
        if g.has("Dark Ritual") and g.cast("Dark Ritual", 1):
            g.add_mana(3)
        g.draw(min(self.draw_weight, 8))
        # token engines add a body per turn while online
        self.bodies += sum(1 for n in TOKEN_ENG if n in self.inplay)

        progressed = True
        while progressed:
            progressed = False
            if not self.seph and g.avail >= 3:           # cast commander Sephiroth
                g.pay(3); self.seph = True; progressed = True; continue
            castable = sorted(
                ((i, nm, r) for i, (nm, r) in enumerate(g.hand)
                 if nm not in ROCKS and (r.get("cmc", 0) or 0) <= g.avail),
                key=lambda x: x[2].get("cmc", 0) or 0)
            for i, nm, r in castable:
                want = (nm in DRAIN or nm in UNDYING or nm in ZOMBIE_SRC or nm in DRAW_ENGINES
                        or nm in TUTORS or nm in KEY_B
                        or nm in {"Yawgmoth, Thran Physician", "Mikaeus, the Unhallowed"})
                if not want or not g.cast(nm):
                    continue
                if nm in DRAW_ENGINES:
                    self.draw_weight += self.dig if nm in STRONG else 1
                if nm in TUTORS:
                    miss = self._missing()
                    if miss:
                        g.fetch(miss)
                else:
                    self.inplay.add(nm)
                    if is_creature(r):
                        self.bodies += 1
                        if nm in UNDYING:
                            self.undying += 1
                progressed = True
                break

        if self._line_a() or self._line_b() or self._line_c():
            self.tbl.kill_all(T)


    # -------------------------------------------------------------------------
    # GRIND clock: the REAL win condition the combo lab ignores. Sac fodder ->
    # death triggers -> drains/burn chip the table. Damage is from drains (which
    # don't care about blockers), so "unblocked" is honest here, not optimistic.
    # -------------------------------------------------------------------------
    def grind_turn(self, T, fodder_bonus=0, each_bonus=0):
        g = self.g
        g.begin_turn(T)
        g.deploy_rocks()
        if g.has("Dark Ritual") and g.cast("Dark Ritual", 1):
            g.add_mana(3)
        g.draw(min(self.draw_weight, 8))

        # deploy everything relevant
        progressed = True
        while progressed:
            progressed = False
            if not self.seph and g.avail >= 3:
                g.pay(3); self.seph = True; progressed = True; continue
            cast = sorted(((i, nm, r) for i, (nm, r) in enumerate(g.hand)
                           if nm not in ROCKS and (r.get("cmc", 0) or 0) <= g.avail),
                          key=lambda x: x[2].get("cmc", 0) or 0)
            for i, nm, r in cast:
                if not g.cast(nm):
                    continue
                if nm in DRAW_ENGINES:
                    self.draw_weight += self.dig if nm in STRONG else 1
                else:
                    self.inplay.add(nm)
                    if is_creature(r):
                        self.bodies += 1
                progressed = True
                break

        # online state
        each = sum(1 for n in ("Zulaport Cutthroat", "Bastion of Remembrance") if n in self.inplay) + each_bonus
        single = sum(1 for n in ("Blood Artist", "Vengeful Bloodwitch", "Syr Konrad, the Grim")
                     if n in self.inplay) + (1 if self.seph else 0)
        outlet = any(n in self.inplay for n in
                     ("Viscera Seer", "Carrion Feeder", "Woe Strider", "Phyrexian Altar",
                      "Ashnod's Altar", "Yahenni, Undying Partisan", "Priest of Forgotten Gods",
                      "Yawgmoth, Thran Physician")) or self.seph
        fodder_eng = sum(1 for n in ("Bitterblossom", "Dreadhorde Invasion", "Cryptbreaker",
                                     "Endrek Sahr, Master Breeder", "Ghoulcaller Gisa")
                         if n in self.inplay)
        recur = sum(1 for n in ("Reassembling Skeleton", "Gravecrawler") if n in self.inplay)
        deaths = (fodder_eng + recur + fodder_bonus) if outlet else 0
        for _ in range(deaths):
            if each:
                self.tbl.hit_all(each, T)
            if single:
                self.tbl.hit_focus(single, T)
        # one-shot bursts
        if "Gray Merchant of Asphodel" in self.inplay and not getattr(self, "_gary", False):
            self._gary = True; self.tbl.hit_all(min(6, 2 + self.bodies), T)
        if "Kokusho, the Evening Star" in self.inplay and outlet and not getattr(self, "_koku", False):
            self._koku = True; self.tbl.hit_all(5, T)


def _run(index, aliases, trials, dig, gated, label):
    print(f"\n### CLOCK ({label}) — Sephiroth combo-assembly   trials={trials} seed={SEED}")
    rng = random.Random(SEED)
    library, commander = slc.load_parsed(DECK, index, aliases)
    print(f"  library {len(library)} + commander {commander}")
    res = slc.run_goldfish(lambda: Trial(library, rng, dig=dig, gated=gated), trials, TURNS)
    slc.report_clock(res, SHOW, TURNS, trials, single=True)


def mode_clock(index, aliases, trials):
    _run(index, aliases, trials, dig=4, gated=False, label="HOUSE-LEGAL (3+ card lines, realistic dig)")
    _run(index, aliases, trials, dig=4, gated=True, label="POD-APPROVED (adds 2-card Mikaeus+Ballista)")
    print("\n  decap == table (infinite hit-all). Chip plan NOT counted (combo clock only).")


def _grind(index, aliases, trials, fodder_bonus, each_bonus, label):
    print(f"\n### GRIND ({label}) — Sephiroth drain-accumulation   trials={trials} seed={SEED}")
    rng = random.Random(SEED)
    library, commander = slc.load_parsed(DECK, index, aliases)
    out = []
    for _ in range(trials):
        tr = Trial(library, rng, dig=4)
        for T in range(1, TURNS + 1):
            tr.grind_turn(T, fodder_bonus=fodder_bonus, each_bonus=each_bonus)
            if tr.tbl.done:
                break
        out.append((tr.tbl.decap, tr.tbl.table))
    slc.report_clock(out, SHOW, TURNS, trials)   # decap (one opp) vs table (all three)


def mode_grind(index, aliases, trials):
    # Real win condition: drains are unblockable, so this clock is honest, not a goldfish ceiling.
    _grind(index, aliases, trials, 0, 0, "as-built")
    # SENSITIVITY — which constraint moves the clock? more deaths/turn vs more each-opp drains
    _grind(index, aliases, trials, 2, 0, "+2 fodder/turn (death VOLUME)")
    _grind(index, aliases, trials, 0, 2, "+2 each-opp drains (drain QUALITY/breadth)")
    print("\n  decap leads table when drains are single-target; each-opp drains close the table.")


if __name__ == "__main__":
    slc.run_cli(__doc__, {"clock": mode_clock, "grind": mode_grind}, default_trials=40000)
