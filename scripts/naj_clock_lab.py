#!/usr/bin/env python3
"""naj_clock_lab.py — Najeela, the Blade-Blossom (5C) candidate KILL-TURN goldfish.

Lab run requested 2026-06-13. Najeela is UN-BUILT (proposals/PROP_Najeela_Blade_Blossom.md);
the list labbed here is a GC-verified modelling build at decks/considering/najeela-blade-
blossom-20260613.txt (3 GCs: Demonic Tutor, Vampiric Tutor, Mana Vault — the proposal's
"Bracket 4 / unlimited GC" framing violates the repo's hard 3-GC cap, and its Smothering
Tithe / Chrome Mox / Cyclonic Rift are GCs and were cut). Built on speed_lab_core.py;
structure follows godo_clock_lab.py. Kill shape: infinite combats -> infinite tokens
overwhelm the table, so decap = table by construction (kill_all).

KILL LINES (oracle-verified via card_lookup.py 2026-06-13):
  1. NAJEELA + DRUIDS' REPOSITORY + >=5 non-sick attackers: each combat the attackers
     add >=5 charge counters; remove 5 -> WUBRG -> Najeela activation (untap all
     attacking + extra combat + a 1/1 Warrior token per Warrior attacking). Net +charges
     once >=6 attack -> infinite combats/tokens. The charges SELF-FUND (no external mana).
  2. NAJEELA + (BEAR UMBRA on a creature | SWORD OF FEAST AND FAMINE equipped) + >=5
     lands: the attack trigger untaps all lands -> WUBRG every combat -> Najeela loop.
  3. NAJEELA + AGGRAVATED ASSAULT + spare mana (>=10) + a board: AA untaps creatures +
     extra combat; Najeela's tokens snowball. Mana-hungry backup (no self-refund).

The enablers ARE tutorable (unlike Berta's auras): Demonic/Vampiric/Idyllic Tutor +
Diabolic Intent/Grim Tutor/Wishclaw fetch Druids' Repository; Open the Armory fetches
Bear Umbra/Sword. So the bottleneck is 5C MANA + a creature board + the commander
({2}{R}, removable, recast tax), not finding the piece.

MANA: lands + rocks + dorks floor. Lotus Petal modelled as a (0,1) repeating rock
(small over-credit). OMITTED (conservative): Cryptolith/Earthcraft as kill enablers
(ramp only), fair combat beats, Mana Reflection. OPTIMISTIC (documented, godo/wb
convention): rocks repeat (Mana Vault untap tax ignored), mana colour-blind, Najeela
survives to activate (her real-table glass jaw at {2}{R} 3/2). Trust shapes.

Data: collection/oracle-cards.json   ·   Proposal: proposals/PROP_Najeela_Blade_Blossom.md
"""
import importlib.util
import random
from pathlib import Path

ROOT = Path(__file__).parent.parent
_spec = importlib.util.spec_from_file_location(
    "speed_lab_core", Path(__file__).parent / "speed_lab_core.py")
slc = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(slc)
ds = slc.ds

DECK = ROOT / "decks" / "considering" / "najeela-blade-blossom-20260613.txt"
SEED = 20260613
TURNS = 12
SHOW = [3, 4, 5, 6, 7, 8, 9, 10, 12]
COMMANDER = "Najeela, the Blade-Blossom"

ROCKS = {"Sol Ring": (1, 2), "Mana Vault": (1, 3), "Arcane Signet": (2, 1),
         "Fellwar Stone": (2, 1), "Lotus Petal": (0, 1)}
DORK_OUT = {"Birds of Paradise": 1, "Ignoble Hierarch": 1, "Noble Hierarch": 1,
            "Bloom Tender": 2, "Faeburrow Elder": 2, "Selvala, Heart of the Wilds": 2}
DORK_COST = {"Birds of Paradise": 1, "Ignoble Hierarch": 1, "Noble Hierarch": 1,
             "Bloom Tender": 2, "Faeburrow Elder": 3, "Selvala, Heart of the Wilds": 3}
ENABLERS = {"Druids' Repository": 3, "Bear Umbra": 4, "Sword of Feast and Famine": 3,
            "Aggravated Assault": 5, "Hellkite Charger": 6, "Combat Celebrant": 3}
REPO_TUTORS = {"Demonic Tutor": 2, "Idyllic Tutor": 3, "Grim Tutor": 3,
               "Diabolic Intent": 2, "Wishclaw Talisman": 3}      # -> hand
TOKEN_MAKERS = {"Goblin Rabblemaster", "Krenko, Mob Boss", "Hero of Bladehold",
                "Adeline, Resplendent Cathar", "Hanweir Garrison", "Monastery Mentor"}


class Trial:
    def __init__(self, library, rng):
        self.g = slc.Goldfish(library, rng, rocks=ROCKS)
        self.tbl = slc.Table()
        self.bf = set()
        self.najeela = False
        self.board = 0          # non-sick creatures (deployed before this turn)
        self.new_cre = 0
        self.dork_out = 0
        self.dork_new = 0
        self.vamp_pending = False

    def kill(self, T):
        g = self.g
        if not self.najeela:
            return False
        if "Druids' Repository" in self.bf and self.board >= 5:
            self.tbl.kill_all(T); return True
        if (self.bf & {"Bear Umbra", "Sword of Feast and Famine"}) \
                and g.lands >= 5 and self.board >= 1:
            self.tbl.kill_all(T); return True
        if "Aggravated Assault" in self.bf and self.board >= 3 and g.avail >= 10:
            self.tbl.kill_all(T); return True
        return False

    def turn(self, T):
        g = self.g
        self.board += self.new_cre; self.new_cre = 0
        self.dork_out += self.dork_new; self.dork_new = 0
        g.begin_turn(T)
        if self.vamp_pending:                     # Vampiric Tutor put Repository on top
            g.fetch("Druids' Repository"); self.vamp_pending = False
        g.deploy_rocks()
        g.add_mana(self.dork_out)

        # commander {2}{R} = 3 (recastable; tax ignored — optimistic)
        if not self.najeela and g.avail >= 3:
            g.avail -= 3; self.najeela = True

        # token makers already online widen the board each turn
        self.new_cre += min(2, len(self.bf & TOKEN_MAKERS))

        if self.kill(T):
            return

        progress = True
        while progress:
            progress = False
            # enablers from hand (cheapest first)
            for nm, c in sorted(ENABLERS.items(), key=lambda x: x[1]):
                if nm not in self.bf and g.has(nm) and g.avail >= c:
                    g.cast(nm, c); self.bf.add(nm); progress = True; break
            # dorks
            for nm, c in DORK_COST.items():
                if nm not in self.bf and g.has(nm) and g.avail >= c:
                    g.cast(nm, c); self.bf.add(nm)
                    self.dork_new += DORK_OUT.get(nm, 0)
                    self.new_cre += 1; progress = True; break
            # creatures (build the board) cheapest-first
            ccands = sorted(
                (r["cmc"], nm) for nm, r in g.hand
                if "creature" in r["type_line"].lower()
                and nm not in DORK_COST and nm not in ENABLERS)
            for c, nm in ccands:
                if g.avail >= c:
                    g.cast(nm, c); self.bf.add(nm)
                    self.new_cre += 1
                    progress = True; break
            # tutor for Druids' Repository if no enabler online/in hand
            has_enabler = bool(self.bf & set(ENABLERS)) \
                or any(g.has(e) for e in ("Druids' Repository", "Bear Umbra",
                                          "Sword of Feast and Famine"))
            if not has_enabler:
                for tut, c in REPO_TUTORS.items():
                    if g.has(tut) and g.avail >= c and g.fetch("Druids' Repository"):
                        g.cast(tut, c); progress = True; break
                if not progress and g.has("Vampiric Tutor") and g.avail >= 1 \
                        and any(d[0] == "Druids' Repository"
                                for d in g.deck[g.ptr:]):
                    g.cast("Vampiric Tutor", 1); self.vamp_pending = True
            if self.kill(T):
                return


def mode_clock(index, aliases, trials):
    print("=" * 72)
    print(f"CLOCK — Najeela, the Blade-Blossom candidate kill-turn goldfish "
          f"({trials} trials, seed {SEED})")
    print("=" * 72)
    rng = random.Random(SEED)
    library, commander = slc.load_parsed(DECK, index, aliases)
    print(f"  library {len(library)} + commander {commander}")
    res = slc.run_goldfish(lambda: Trial(library, rng), trials, TURNS)
    slc.report_clock(res, SHOW, TURNS, trials, single=True)
    print("\n  PROP claim: 'deterministic + tutorable; ceiling 18-19/20'. "
          "The cum % rows above are the test.")


if __name__ == "__main__":
    slc.run_cli(__doc__, {"clock": mode_clock})
