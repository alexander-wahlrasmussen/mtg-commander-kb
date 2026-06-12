#!/usr/bin/env python3
"""godo_clock_lab.py — Hostile Takeover (Godo, Bandit Warlord) KILL-TURN goldfish.

Stage 3 of the 2026-06-12 candidate bake-off (proposals/Candidate_Bakeoff_2026-06-12.md).
Deck: decks/considering/hostile-takeover-20260612.txt. Built on speed_lab_core.py.

THE KILL IS GODO + HELM OF THE HOST ATTACHED, AT ANY COMBAT. Rules facts the
model encodes (each checked against card_lookup.py 2026-06-12):

  * Godo {5}{R}: ETB searches an EQUIPMENT onto the battlefield (NOT attached).
  * Helm of the Host {4}, equip {5}: at the beginning of combat on YOUR turn
    (every combat phase), create a non-legendary COPY of the equipped creature
    with haste. A Helm-token copy of Godo is itself named Godo and carries his
    attack trigger ("untap + additional combat phase, first time each turn" —
    the token is a new object, so its own trigger is fresh) -> infinite combats
    with a growing hasty army. GODO HIMSELF NEEDS NO HASTE: the token attacks.
  * Hammer of Nazahn: when ANOTHER Equipment enters, attach it free; also
    +2/+0 & indestructible. Hammer on board first = cast Godo (6) -> Helm
    enters -> auto-attach -> SAME-TURN table kill for 6 mana total.
  * No Hammer: 6 (Godo) + 5 (equip) = 11 mana same-turn, or equip 5 the turn
    after Godo (goldfish assumes he survives — flagged optimism, the deck's
    real-table glass jaw).
  * Backup: Aggravated Assault + Neheb the Eternal (postcombat main adds {R}
    per 1 life opponents lost this turn) = infinite combats once the standing
    board swings for >=5. Modelled as kill_all when both on bf and the prior
    board's power >= 5.

MANA: lands + rocks floor. Mana Vault (1,3) / Grim Monolith (2,3) modelled as
repeating rocks (untap tax ignored — same documented optimism as wb_clock_lab).
Ruby Medallion approximated as a (2,1) rock. Rituals (Seething Song +2,
Pyretic/Desperate +1) are banked and popped only to complete a kill-cast.
Treasonous Ogre: once on bf, up to 8 extra mana (24 life) — only spent to
complete a kill. Birgi: +1 toward the kill sequence when out.

TUTORS: Gamble (1) and Wishclaw (cast 2 + activate 1, modelled 3 same-turn)
fetch Hammer of Nazahn if the kill isn't already faster without it.

OMITTED (conservative): plain combat beats before the combo (Godo decks
don't win T6 fair), Magda treasure-fetch, Goblin Engineer (Helm is MV4, his
return is MV<=3 — CANNOT recur Helm), Imperial Recruiter chains, extra-combat
creatures as a damage engine. OPTIMISTIC (documented): rocks repeat, Godo
survives the table for the two-turn line, mana is colour-blind. Decap = table
by construction (infinite combats end the game). Trust shapes, not decimals.

Data: collection/oracle-cards.json (refreshed 2026-06-12)
Writeup: proposals/Candidate_Bakeoff_2026-06-12.md (Stage 3)
"""
import importlib.util
import random
from pathlib import Path

ROOT = Path(__file__).parent.parent
_spec = importlib.util.spec_from_file_location(
    "speed_lab_core", Path(__file__).parent / "speed_lab_core.py")
slc = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(slc)
ds = slc.ds

DECK = ROOT / "decks" / "considering" / "hostile-takeover-20260612.txt"
SEED = 20260612
TURNS = 12
SHOW = [3, 4, 5, 6, 7, 8, 9, 10, 12]

ROCKS = {"Sol Ring": (1, 2), "Mana Vault": (1, 3), "Grim Monolith": (2, 3),
         "Arcane Signet": (2, 1), "Worn Powerstone": (3, 2),
         "Ruby Medallion": (2, 1)}
RITUALS = {"Seething Song": (3, 5), "Pyretic Ritual": (2, 3),
           "Desperate Ritual": (2, 3)}          # (cost, output) — net banked
# standing-board creatures worth casting while waiting (power for the AA line)
BEATERS = {"Neheb, the Eternal": (5, 4), "Birgi, God of Storytelling": (3, 3),
           "Treasonous Ogre": (4, 2), "Terror of the Peaks": (5, 5),
           "Inferno Titan": (6, 6), "Hellkite Tyrant": (6, 6),
           "Seasoned Pyromancer": (3, 2), "Combat Celebrant": (3, 4),
           "Port Razer": (5, 4), "Scourge of the Throne": (6, 5),
           "Fanatic of Mogis": (4, 4), "Ogre Battledriver": (4, 3)}


class Trial:
    def __init__(self, library, rng):
        self.g = slc.Goldfish(library, rng, rocks=ROCKS)
        self.tbl = slc.Table()
        self.bf = set()
        self.board_pow = 0          # power on bf at START of this turn
        self.new_pow = 0
        self.rituals = []           # banked (output-cost) nets
        self.godo = False           # Godo on battlefield
        self.helm_bf = False
        self.attached = False
        self.ogre_budget = 0

    def burst(self, need):
        """Mana the kill could reach this turn: avail + banked rituals + Ogre
        life-mana + Birgi. Spends only if the kill completes."""
        extra = sum(out - cost for cost, out in self.rituals)
        if "Treasonous Ogre" in self.bf:
            extra += self.ogre_budget
        if "Birgi, God of Storytelling" in self.bf:
            extra += 1
        return self.g.avail + extra

    def spend(self, n):
        """Commit n mana from avail + rituals + Ogre (kill confirmed)."""
        for cost, out in list(self.rituals):
            if self.g.avail >= n:
                break
            if self.g.avail >= cost:
                self.g.avail += out - cost
                self.rituals.remove((cost, out))
        if "Birgi, God of Storytelling" in self.bf:
            self.g.avail += 1
        if self.g.avail < n and "Treasonous Ogre" in self.bf:
            take = min(self.ogre_budget, n - self.g.avail)
            self.g.avail += take
            self.ogre_budget -= take
        self.g.avail -= n

    def deploy(self, nm, cost):
        if self.g.cast(nm, cost):
            self.bf.add(nm)
            return True
        return False

    def turn(self, T):
        g = self.g
        self.board_pow += self.new_pow
        self.new_pow = 0
        g.begin_turn(T)
        g.deploy_rocks()
        # bank rituals (held for the kill)
        for r in RITUALS:
            while g.has(r):
                g.hand.pop(g.in_hand(r))
                self.rituals.append(RITUALS[r])
        if "Treasonous Ogre" in self.bf:
            self.ogre_budget = 8

        # --- kill checks, cheapest line first ---------------------------------
        # 1. Godo already out, Helm out: attach (free if Hammer, else equip 5)
        if self.godo and self.helm_bf:
            if self.attached or "Hammer of Nazahn" in self.bf:
                self.tbl.kill_all(T); return
            if self.burst(5) >= 5:
                self.spend(5); self.tbl.kill_all(T); return
        # 2. cast Godo this turn (6), Helm enters from library
        if not self.godo:
            cost_g = 6
            if self.burst(cost_g) >= cost_g:
                hammer = "Hammer of Nazahn" in self.bf
                if hammer:
                    self.spend(cost_g)
                    self.godo = self.helm_bf = self.attached = True
                    self.tbl.kill_all(T); return
                if self.burst(cost_g + 5) >= cost_g + 5:
                    self.spend(cost_g + 5)
                    self.godo = self.helm_bf = self.attached = True
                    self.tbl.kill_all(T); return
                # can't kill this turn: deploy Godo anyway, kill next turn
                self.spend(cost_g)
                self.godo = self.helm_bf = True
                self.new_pow += 3
        # 3. Aggravated Assault + Neheb + standing board >= 5
        if ("Aggravated Assault" in self.bf and "Neheb, the Eternal" in self.bf
                and self.board_pow >= 5 and self.burst(5) >= 5):
            self.spend(5); self.tbl.kill_all(T); return

        # --- develop -----------------------------------------------------------
        # Hammer first (turns the kill into 6 mana), then AA, then beaters
        if "Hammer of Nazahn" not in self.bf and g.has("Hammer of Nazahn"):
            self.deploy("Hammer of Nazahn", 4)
        if not self.godo and "Hammer of Nazahn" not in self.bf:
            for tut, cost in (("Gamble", 1), ("Wishclaw Talisman", 3)):
                if g.has(tut) and g.avail >= cost:
                    if g.fetch("Hammer of Nazahn"):
                        g.cast(tut, cost)
                        break
        if g.has("Helm of the Host") and g.avail >= 4:   # drawn naturally
            g.cast("Helm of the Host", 4)
            self.helm_bf = True
            if "Hammer of Nazahn" in self.bf:
                self.attached = self.godo and True
        if "Aggravated Assault" not in self.bf and g.has("Aggravated Assault") \
                and g.avail >= 3:
            self.deploy("Aggravated Assault", 3)
        for nm, (cost, pw) in BEATERS.items():
            if nm not in self.bf and g.has(nm) and g.avail >= cost:
                self.deploy(nm, cost)
                self.new_pow += pw


def goldfish(library, trials, rng):
    out = []
    for _ in range(trials):
        tr = Trial(library, rng)
        for T in range(1, TURNS + 1):
            tr.turn(T)
            if tr.tbl.done:
                break
        out.append((tr.tbl.decap, tr.tbl.table))
    return out


def mode_clock(index, aliases, trials):
    print("=" * 72)
    print(f"CLOCK — Hostile Takeover (Godo) kill-turn goldfish "
          f"({trials} trials, seed {SEED})")
    print("=" * 72)
    rng = random.Random(SEED)
    library, commander = slc.load_parsed(DECK, index, aliases)
    print(f"  library {len(library)} + commander {commander}")
    print("  turns:".ljust(44) + "".join(f"{t:6d}" for t in SHOW))
    res = goldfish(library, trials, rng)
    print(slc.row("kill (decap = table, cum %)", slc.cum(res, 1, SHOW), SHOW))
    nv = 100.0 * sum(1 for _, t in res if t is None) / trials
    print(f"\n  median kill {slc.median(res, 1)}   ·   never-in-{TURNS}: {nv:.0f}%")
    print("\n  Proposal claim: 'fastest target T5-6'. The cum % rows above are the test.")


if __name__ == "__main__":
    slc.run_cli(__doc__, {"clock": mode_clock})
