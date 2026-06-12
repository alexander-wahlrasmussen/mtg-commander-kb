#!/usr/bin/env python3
"""kvd_clock_lab.py — Asset Stripping (Korvold, Fae-Cursed King) KILL-TURN goldfish.

Stage 3 of the 2026-06-12 candidate bake-off. Deck:
decks/considering/asset-stripping-20260612.txt. Built on speed_lab_core.py.

TWO CLOCKS: a closed-loop aristocrats INFINITE (kill_all, decap = table) and a
finite GRIND drain (decap/table tracked separately). Loop conditions encode
the Stage-2 precision notes exactly (oracle-verified 2026-06-12):

  L1 GRAVECRAWLER LOOP — Pitiless Plunderer + Gravecrawler (bf or yard) +
     a FREE sac outlet + ANOTHER Zombie on the battlefield (Gravecrawler's
     recast clause; in-deck zombie bodies: Carrion Feeder, Midnight Reaper,
     Dreadhorde Invasion's Army token) + a damage payoff. Each loop: sac (0),
     Plunderer Treasure (+1 any colour), recast {B} -> net 0, infinite deaths.
     Goblin Bombardment needs NO other payoff (the outlet IS the payoff);
     Mayhem Devil pings per sac (incl. Treasure sacs); Zulaport / Nadier's
     hit every opponent per death / token-leave; Blood Artist & Marionette
     Master drain one at a time — unbounded loop = table kill regardless.
  L2 SKELETON LOOP — Ashnod's Altar + Reassembling Skeleton + Plunderer:
     sac -> {C}{C} + Treasure, return {1}{B} -> net +1 infinite (the
     Treasure covers the {B}). Without Ashnod's the Skeleton loop is mana-
     NEGATIVE (Stage-2 note: only Plunderer's Treasures self-sustain) and is
     modelled as finite grind loops only. Sifter of Skulls' Scions make {C}
     ONLY — they never pay the {B} halves and are deliberately NOT a loop
     enabler here.

  GRIND — per turn: Korvold's attack sac, Dreadhorde token, mana-paid
  Skeleton/Gravecrawler rebuys (capped by spare mana). Each death: +1 per
  opponent per hit-all payoff (Zulaport, Nadier's — Nadier's also counts
  Treasure-token leaves), Blood Artist/Mayhem Devil/Marionette pooled as
  focus damage. Korvold grows +1/+1 per sacrifice and swings (focus).

TUTORS: Worldly Tutor (1, creature -> TOP, next draw: Plunderer first),
Gamble (1, anything). Reanimation (Victimize/Living Death/Meren) OMITTED.
MANA: lands + rocks + dorks + land-ramp; Mana Vault (1,3) repeating-rock
optimism as documented in the other labs. Draw engines modelled: Korvold
himself (+1 per sac, the deck's engine), Midnight Reaper (+1 per nontoken
death), Deadly Dispute/Village Rites (cast for value when fodder spare).
OMITTED (conservative): Mazirek pump, Woe Strider escape, Living Death
blowouts, Marionette fabricate-Servo fodder, treasure ramp spells' burst
beyond +1 rock-equivalent. Trust shapes and deltas, not second decimals.

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

DECK = ROOT / "decks" / "considering" / "asset-stripping-20260612.txt"
SEED = 20260612
TURNS = 12
SHOW = [4, 5, 6, 7, 8, 9, 10, 12]

ROCKS = {"Sol Ring": (1, 2), "Mana Vault": (1, 3), "Arcane Signet": (2, 1),
         "Rakdos Signet": (2, 1), "Gruul Signet": (2, 1),
         "Talisman of Resilience": (2, 1), "Commander's Sphere": (3, 1),
         "Mind Stone": (2, 1)}
DORKS = {"Birds of Paradise": 1, "Elvish Mystic": 1}
LAND_RAMP = {"Three Visits": 2, "Farseek": 2, "Rampant Growth": 2,
             "Sakura-Tribe Elder": 2, "Cultivate": 3, "Kodama's Reach": 3}
FREE_OUTLETS = {"Carrion Feeder": 1, "Viscera Seer": 1,
                "Goblin Bombardment": 2, "Woe Strider": 3,
                "Ashnod's Altar": 3}
HITALL = {"Zulaport Cutthroat": 2, "Nadier's Nightblade": 3}
FOCUS = {"Blood Artist": 2, "Mayhem Devil": 3, "Marionette Master": 6}
ZOMBIE_BODIES = {"Carrion Feeder", "Midnight Reaper"}
LOOP_CORE = {"Pitiless Plunderer": 4, "Gravecrawler": 1,
             "Reassembling Skeleton": 2, "Sifter of Skulls": 4}


class Trial:
    def __init__(self, library, rng):
        self.g = slc.Goldfish(library, rng, rocks=ROCKS)
        self.tbl = slc.Table()
        self.bf = set()
        self.korvold = False
        self.kpow = 4
        self.dork_out = 0
        self.dork_new = 0
        self.dreadhorde = False
        self.army = False           # a Zombie Army token exists
        self.pending_top = []
        self.gc_yard = False        # Gravecrawler in yard
        self.sk_yard = False        # Skeleton in yard

    # ---- loop predicates --------------------------------------------------
    def payoff_live(self):
        return (self.bf & set(HITALL)) or (self.bf & set(FOCUS)) \
            or "Goblin Bombardment" in self.bf

    def zombie_other(self):
        return bool(self.bf & ZOMBIE_BODIES) or self.army

    def loop_check(self, T):
        g = self.g
        free_out = self.bf & set(FREE_OUTLETS)
        plund = "Pitiless Plunderer" in self.bf
        gc = "Gravecrawler" in self.bf or self.gc_yard
        sk = "Reassembling Skeleton" in self.bf or self.sk_yard
        if plund and gc and free_out and self.zombie_other() and self.payoff_live():
            self.tbl.kill_all(T)
            return True
        if plund and sk and "Ashnod's Altar" in self.bf and self.payoff_live():
            self.tbl.kill_all(T)
            return True
        return False

    # ---- one turn -----------------------------------------------------------
    def turn(self, T):
        g = self.g
        self.dork_out += self.dork_new
        self.dork_new = 0
        g.begin_turn(T)
        for nm in self.pending_top:
            g.fetch(nm)
        self.pending_top = []
        g.deploy_rocks()
        g.add_mana(self.dork_out)
        if self.dreadhorde:
            self.army = True

        progress = True
        while progress:
            progress = False
            # loop pieces from hand, most constrained first
            order = [("Pitiless Plunderer", 4), ("Ashnod's Altar", 3),
                     ("Goblin Bombardment", 2), ("Carrion Feeder", 1),
                     ("Viscera Seer", 1), ("Gravecrawler", 1),
                     ("Reassembling Skeleton", 2), ("Zulaport Cutthroat", 2),
                     ("Blood Artist", 2), ("Nadier's Nightblade", 3),
                     ("Mayhem Devil", 3), ("Woe Strider", 3),
                     ("Midnight Reaper", 3), ("Sifter of Skulls", 4),
                     ("Dreadhorde Invasion", 2), ("Marionette Master", 6)]
            for nm, c in order:
                if nm not in self.bf and g.has(nm) and g.avail >= c:
                    g.cast(nm, c)
                    self.bf.add(nm)
                    if nm == "Dreadhorde Invasion":
                        self.dreadhorde = True
                    progress = True
                    break
            if self.loop_check(T):
                return
            # commander
            if not self.korvold and g.avail >= 5:
                g.avail -= 5
                self.korvold = True
                progress = True
            # tutors -> missing loop piece
            tgt = None
            if "Pitiless Plunderer" not in self.bf \
                    and not g.has("Pitiless Plunderer"):
                tgt = "Pitiless Plunderer"
            elif not (self.bf & set(FREE_OUTLETS)) \
                    and not any(g.has(o) for o in FREE_OUTLETS):
                tgt = "Goblin Bombardment"
            elif not ("Gravecrawler" in self.bf or self.gc_yard
                      or g.has("Gravecrawler")):
                tgt = "Gravecrawler"
            if tgt:
                if g.has("Worldly Tutor") and g.avail >= 1 \
                        and tgt != "Goblin Bombardment":
                    if any(g.deck[i][0] == tgt for i in range(g.ptr, len(g.deck))):
                        g.cast("Worldly Tutor", 1)
                        self.pending_top.append(tgt)
                        progress = True
                elif g.has("Gamble") and g.avail >= 1:
                    if g.fetch(tgt):
                        g.cast("Gamble", 1)
                        progress = True
            # dorks / ramp
            for nm, c in list(DORKS.items()):
                if g.has(nm) and g.avail >= c:
                    g.cast(nm, c)
                    self.dork_new += 1
                    progress = True
            for nm, c in LAND_RAMP.items():
                if g.has(nm) and g.avail >= c:
                    g.cast(nm, c)
                    g.lands += 1
                    progress = True
                    break
            # value draw with spare fodder
            for nm, c in (("Village Rites", 1), ("Deadly Dispute", 2)):
                if g.has(nm) and g.avail >= c and (self.army or self.korvold):
                    g.cast(nm, c)
                    g.draw(2)
                    self.army = False if self.army else self.army
                    progress = True
                    break

        # ---- grind: finite sacs this turn --------------------------------------
        free_out = self.bf & set(FREE_OUTLETS)
        deaths = 0
        if self.korvold:
            deaths += 1                       # Korvold attack-trigger sac
            self.kpow += 1
        if free_out:
            if self.army:
                deaths += 1
                self.army = False
            # mana-paid rebuys: Gravecrawler {B}=1, Skeleton {1}{B}=2
            gc_live = ("Gravecrawler" in self.bf or self.gc_yard) \
                and self.zombie_other()
            rebuy_cost = 1 if gc_live else (
                2 if ("Reassembling Skeleton" in self.bf or self.sk_yard) else 0)
            if rebuy_cost:
                loops = min(g.avail // rebuy_cost, 8)
                g.avail -= loops * rebuy_cost
                deaths += loops
                if gc_live:
                    self.gc_yard = True
                    self.bf.discard("Gravecrawler")
                else:
                    self.sk_yard = True
                    self.bf.discard("Reassembling Skeleton")
        if deaths:
            per_opp = deaths * sum(1 for p in HITALL if p in self.bf)
            if "Pitiless Plunderer" in self.bf \
                    and "Nadier's Nightblade" in self.bf:
                per_opp += deaths             # Treasures made then spent = leaves
            if per_opp:
                self.tbl.hit_all(per_opp, T)
            focus = deaths * sum(1 for p in FOCUS if p in self.bf)
            if "Goblin Bombardment" in self.bf:
                focus += deaths
            if focus:
                self.tbl.hit_focus(focus, T)
            if self.korvold:
                g.draw(min(deaths, 4))        # Korvold draws per sac (capped)
            if "Midnight Reaper" in self.bf:
                g.draw(1)
        # combat
        if self.korvold:
            self.tbl.hit_focus(self.kpow, T)


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
    print(f"CLOCK — Asset Stripping (Korvold) kill-turn goldfish "
          f"({trials} trials, seed {SEED})")
    print("=" * 72)
    rng = random.Random(SEED)
    library, commander = slc.load_parsed(DECK, index, aliases)
    print(f"  library {len(library)} + commander {commander}")
    print("  turns:".ljust(44) + "".join(f"{t:6d}" for t in SHOW))
    res = goldfish(library, trials, rng)
    print(slc.row("decap (one opponent, cum %)", slc.cum(res, 0, SHOW), SHOW))
    print(slc.row("table (all three, cum %)", slc.cum(res, 1, SHOW), SHOW))
    nv_d = 100.0 * sum(1 for d, _ in res if d is None) / trials
    nv_t = 100.0 * sum(1 for _, t in res if t is None) / trials
    print(f"\n  median decap {slc.median(res, 0)} / table {slc.median(res, 1)}"
          f"   ·   never-in-{TURNS}: decap {nv_d:.0f}% / table {nv_t:.0f}%")
    print("\n  Proposal self-clock: 'median ~T7-9, resilient/grindy'. Rows above are the test.")


if __name__ == "__main__":
    slc.run_cli(__doc__, {"clock": mode_clock})
