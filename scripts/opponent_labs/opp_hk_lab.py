#!/usr/bin/env python3
"""opp_hk_lab.py — CLONE-LOOP kill-turn goldfish for the archenemy's Hidetsugu & Kairi
deck (opponents/you-get-a-clone-BANFIX-PROXY-20260702.txt — his REAL 2023 list with the
two banned cards substituted; a PROXY clock, see scripts/opponent_labs/README.md).

KILL SHAPE (user testimony 2026-07-02: "we died from him cloning his commander and then
doing a lot of damage to a player" — the DECAP pattern; deck read + every encoded card
card_lookup-verified 2026-07-02):

  Hidetsugu and Kairi {2}{U}{U}{B} 5/4:
    ETB   "draw three cards, then put two cards from your hand on top of your library"
          -> he STACKS his biggest instant/sorcery bomb on top, himself.
    DEATH "exile the top card of your library. TARGET OPPONENT loses life equal to its
          mana value. If it's an instant or sorcery card, you may cast it without paying."

  The loop: keep the ORIGINAL H&K; every clone enters as a copy -> legend rule kills the
  copy -> the copy's death trigger = H&K's -> drain the focus player for the stacked bomb's
  MV (7-11 in this list) + free-cast it (Time Stretch/Temporal Trespass/Nexus/Beacon/
  Expropriate = EXTRA TURNS -> more iterations same wall-clock turn). The clone's own ETB
  (it copies H&K) draws 3 and stacks the NEXT bomb. No commander tax is ever paid.
    iterations: 15 clones (Phantasmal Image 2 .. Saheeli's Artistry 6; kicked Rite of
      Replication 9 = FIVE copies = five death triggers), 5 one-mana death-tricks (Feign
      Death / Undying Evil / Undying Malice / Supernatural Stamina / Kaya's Ghostform —
      H&K dies to a sac outlet and RETURNS; outlet = Altars or High Market / Phyrexian
      Tower land drops; an Altar sac also adds 1 mana), Saw in Half 3 (destroy H&K -> two
      half-copies -> legend rule -> +1 extra trigger, H&K survives).
    Drivnod, Carnage Dominus (verified): each death trigger fires an ADDITIONAL time.
    Vampiric Tutor: set the top to the biggest bomb in the library (1 mana).
    unstacked death triggers exile a RANDOM top card and drain its printed MV (lands 0).

OPTIMISTIC (ceiling): no interaction, focus player never gains life, Mana Vault untap tax
ignored (shared labs optimism), free-cast non-ET bombs' effects beyond the drain ignored
EXCEPT Peer into the Abyss (+7 draws). CONSERVATIVE / OMITTED: Sensei's Top top-control,
Strionic Resonator trigger copies, Into the Story / Dig / Cruise draw, Nexus of Fate
reshuffle (each ET bomb fires once), Reanimate/Animate Dead rebuys, Skull Storm's cast
effect (drain-only). The 103-card list is kept verbatim (his committed extras dilute draws
honestly). BANFIX substitution (Mana Vault / Coalition Relic) is our guess — 2 slots.

Data: collection/oracle-cards.json · Run: python scripts/opponent_labs/opp_hk_lab.py
"""
import importlib.util
import random
from pathlib import Path

ROOT = Path(__file__).parents[2]
_spec = importlib.util.spec_from_file_location(
    "speed_lab_core", ROOT / "scripts" / "speed_lab_core.py")
slc = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(slc)
ds = slc.ds

# --- spec ------------------------------------------------------------------
DECK = ROOT / "opponents" / "you-get-a-clone-BANFIX-PROXY-20260702.txt"
COMMANDER = "Hidetsugu and Kairi"
SEED = 20260702
TURNS = 14
SHOW = [4, 5, 6, 7, 8, 9, 10, 12]
HK_COST = 5
ROCKS = {"Sol Ring": (1, 2), "Mana Vault": (1, 3), "Arcane Signet": (2, 1),
         "Fellwar Stone": (2, 1), "Mind Stone": (2, 1), "Talisman of Dominance": (2, 1),
         "Coalition Relic": (3, 1), "Midnight Clock": (3, 1), "Thran Dynamo": (4, 3)}

# one clone cast = one legend-rule death trigger (cost verified per card)
CLONES = {"Phantasmal Image": 2, "Mirror Image": 3, "Cackling Counterpart": 3,
          "Quasiduplicate": 3, "Fated Infatuation": 3, "Glasspool Mimic // Glasspool Shore": 3,
          "Phyrexian Metamorph": 4, "Clever Impersonator": 4, "Vizier of Many Faces": 4,
          "Undercover Operative": 4, "See Double": 4, "Machine God's Effigy": 4,
          "Tempt with Reflections": 4, "Replication Technique": 5, "Saheeli's Artistry": 6}
RITE = "Rite of Replication"                       # 4 = 1 trigger · 9 kicked = 5 triggers
SAW = "Saw in Half"                                # 3 = 2 triggers, H&K survives
DEATHTRICKS = {"Feign Death": 1, "Undying Evil": 1, "Undying Malice": 1,
               "Supernatural Stamina": 1, "Kaya's Ghostform": 1}   # need a sac outlet
ALTARS = {"Ashnod's Altar": 3, "Phyrexian Altar": 3}
OUTLET_LANDS = {"High Market", "Phyrexian Tower"}
DRIVNOD = "Drivnod, Carnage Dominus"               # each death trigger +1
VAMPIRIC = "Vampiric Tutor"

# bombs: name -> (MV, extra_turn?, peer?)
BOMBS = {"Temporal Trespass": (11, True, False), "Time Stretch": (10, True, False),
         "Expropriate": (9, True, False), "Skull Storm": (9, False, False),
         "In Garruk's Wake": (9, False, False), "Rise of the Dark Realms": (9, False, False),
         "Clone Legion": (9, False, False), "Mnemonic Deluge": (9, False, False),
         "Beacon of Tomorrows": (8, True, False), "Nexus of Fate": (7, True, False),
         "Peer into the Abyss": (7, False, True), "Blatant Thievery": (7, False, False),
         "Breach the Multiverse": (7, False, False)}


def pull_commander(library, name):
    for i, (nm, _rec) in enumerate(library):
        if nm.lower() == name.lower():
            return library[:i] + library[i + 1:]
    raise SystemExit(f"commander {name!r} not in parsed list")


class Trial:
    def __init__(self, library, rng):
        self.g = slc.Goldfish(library, rng, rocks=ROCKS)
        self.tbl = slc.Table()
        self.hk = False
        self.drivnod = False
        self.outlet_land = False
        self.altar = False
        self.stacked = None              # (mv, extra_turn, peer) known top card
        self.bonus = 0                   # pending extra turns

    # -- helpers ---------------------------------------------------------------
    def best_bomb_in_hand(self):
        best, bi = None, None
        for i, (nm, _r) in enumerate(self.g.hand):
            if nm in BOMBS and (best is None or BOMBS[nm][0] > best[0]):
                best, bi = BOMBS[nm], i
        return bi, best

    def hk_etb(self):
        """draw 3, stack the biggest bomb from hand on top (it leaves hand)."""
        self.g.draw(3)
        bi, bomb = self.best_bomb_in_hand()
        if bi is not None and self.stacked is None:
            self.g.hand.pop(bi)
            self.stacked = bomb

    def death_trigger(self, T):
        """One H&K death trigger (Drivnod doubles the exile+drain)."""
        for _ in range(2 if self.drivnod else 1):
            if self.stacked:
                mv, et, peer = self.stacked
                self.stacked = None
                self.tbl.hit_focus(mv, T)
                if et:
                    self.bonus += 1
                if peer:
                    self.g.draw(7)
            else:
                names = self.g.mill(1)          # exile a random top card
                if names:
                    rec = self.g.yard[-1][1]
                    self.tbl.hit_focus(int(rec.get("cmc", 0)), T)

    def outlet(self):
        return self.altar or self.outlet_land

    # -- turn --------------------------------------------------------------------
    def casts(self, T):
        """Greedy cast loop for one (possibly bonus) turn segment."""
        g = self.g
        progress = True
        while progress and not self.tbl.done:
            progress = False
            # commander first
            if not self.hk and g.avail >= HK_COST:
                g.avail -= HK_COST; self.hk = True
                self.hk_etb(); progress = True
            # board pieces: Drivnod / an Altar
            if not self.drivnod and g.has(DRIVNOD) and g.avail >= 5 and g.cast(DRIVNOD, 5):
                self.drivnod = True; progress = True
            if not self.altar:
                for nm, c in ALTARS.items():
                    if g.has(nm) and g.avail >= c and g.cast(nm, c):
                        self.altar = True; progress = True; break
            if not self.hk:
                break
            # Vampiric: set the top when nothing is stacked
            if (self.stacked is None and g.has(VAMPIRIC) and g.avail >= 1):
                target = max((nm for nm in BOMBS if self.lib_has(nm)),
                             key=lambda nm: BOMBS[nm][0], default=None)
                if target and g.cast(VAMPIRIC, 1):
                    g.fetch(target)              # to hand in the model...
                    i = g.in_hand(target)
                    g.hand.pop(i)                # ...then onto the top = stacked
                    self.stacked = BOMBS[target]
                    progress = True
            # iterations, biggest-value first: kicked Rite -> Saw -> tricks/clones cheap-first
            if g.has(RITE) and g.avail >= 9 and g.cast(RITE, 9):
                for _ in range(5):
                    self.hk_etb(); self.death_trigger(T)
                    if self.tbl.done:
                        return
                progress = True; continue
            if g.has(SAW) and g.avail >= 3 and g.cast(SAW, 3):
                for _ in range(2):
                    self.hk_etb(); self.death_trigger(T)
                    if self.tbl.done:
                        return
                progress = True; continue
            iters = dict(CLONES)
            if self.outlet():
                iters |= DEATHTRICKS
            for nm, c in sorted(iters.items(), key=lambda kv: kv[1]):
                if g.has(nm) and g.avail >= c and g.cast(nm, c):
                    if nm in DEATHTRICKS and self.altar:
                        g.add_mana(1)            # sac to an Altar pays a mana back
                    self.hk_etb()                # the copy's ETB (tricks: H&K re-enters)
                    self.death_trigger(T)
                    progress = True
                    break

    def turn(self, T):
        g = self.g
        played = g.begin_turn(T)
        if played in OUTLET_LANDS:
            self.outlet_land = True
        g.deploy_rocks()
        self.casts(T)
        while self.bonus and not self.tbl.done:   # extra turns: same wall-clock turn T
            self.bonus -= 1
            played = g.begin_turn(T)
            if played in OUTLET_LANDS:
                self.outlet_land = True
            g.deploy_rocks()
            self.casts(T)

    def lib_has(self, nm):
        g = self.g
        return any(g.deck[i][0] == nm for i in range(g.ptr, len(g.deck)))


def mode_clock(index, aliases, trials, deck=None):
    deck = deck or DECK
    print("=" * 74)
    print(f"OPP CLOCK — Hidetsugu & Kairi clone-loop goldfish ({trials} trials, seed {SEED})")
    print("=" * 74)
    print("  PROXY clock: his real 2023 list + 2-slot banfix; caveats in the docstring.")
    rng = random.Random(SEED)
    library, _ = slc.load_parsed(deck, index, aliases)
    library = pull_commander(library, COMMANDER)
    print(f"  library {len(library)} + commander {COMMANDER}   [{deck.name}]")
    res = slc.run_goldfish(lambda: Trial(library, rng), trials, TURNS)
    slc.report_clock(res, SHOW, TURNS, trials)     # drains are single-target: decap != table
    print("\n  Read: DECAP is the number the pod fears (his kill is target-one-player);")
    print("  K in pod_gauntlet terms = the decap curve. Extra-turn chains land inside the")
    print("  same wall-clock turn, which is exactly how the stomp felt.")


if __name__ == "__main__":
    slc.run_cli(__doc__, {"clock": mode_clock})
