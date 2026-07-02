#!/usr/bin/env python3
"""opp_urdragon_lab.py — DRAGON-SWARM kill-turn goldfish for the archenemy's Ur-Dragon deck
(opponents/dragon-dragon-dragon-PROXY-20260702.txt — his real 72 spells + our 28-land fill;
a PROXY clock, see scripts/opponent_labs/README.md). Seen EVERY meetup, so this curve
carries the largest observed-rotation weight.

KILL SHAPE (every encoded card card_lookup-verified 2026-07-02): go-tall dragon COMBAT with
a real ETB-BURN sub-axis and one alternate WINCON — not a combo deck, but far from fair:

  BURN per dragon ETB: Dragon Tempest (X = #dragons, + flyer haste) · Scourge of Valkas
    (X = #dragons) · Terror of the Peaks (= entering power). Token engines multiply the
    ETBs: Miirym (nontoken dragon -> token copy) · Lathliss (nontoken dragon -> 5/5).
  DOUBLERS: Twinflame Tyrant (ALL damage to opponents x2) · Neriv (damage from creatures
    that entered this turn x2 — fresh hasty dragons + their ETB burn) -> stack to x4.
  CHEAT/DUMP: Dracogenesis (cast Dragon spells FREE) · Sneak Attack ({R}: hasty, sac EOT) ·
    Tooth and Nail entwined (2 from library) · Majestic Genesis (top 9 -> dragons in play) ·
    Ureni (ETB/attack -> dragon from top 8) · Hellkite Courser (ETB -> UD visits from CZ,
    attacks, returns) · Tiamat (on cast: 5 dragons to hand).
  COMMANDER: The Ur-Dragon 9 ({4}WUBRG): eminence discounts OTHER dragons {1} (CZ or
    battlefield); ON battlefield, attacks draw #dragons + put a permanent from hand FREE.
  ALT WINCON: Call the Spirit Dragons — at upkeep, +1/+1 counter on a dragon of each color;
    five colours countered = WIN THE GAME. Modelled as: in play + >=5 dragons on board
    surviving one upkeep -> table kill (his dragons are heavily multicolour; colour
    coverage assumed at 5+ bodies — a stated simplification).
  DISCOUNTS: eminence -1 · Urza's Incubator -2 · Temur Battlecrier -1 per power>=4
    creature (your turn) — cost floor = 2 (multicolour pips), UD floor 5.
  HASTE: Tempest/Crossroads/Ascendancy/Rhythm/Frostcliff(Temur)/Fire Crystal — any one
    present -> new dragons swing the turn they land.
  DRAW: Elemental Bond / Garruk's Uprising / Temur Ascendancy / Guardian Project / Great
    Henge (+1 per qualifying dragon ETB); UD attack trigger draws #attacking dragons.

OPTIMISTIC (ceiling): unblocked combat (the pod DOES block dragons; vs_dragon_lab models
the defended matchup — this is the K-attempt clock, not P(win)); Mox Jasper counted from
T1 (dragon gate ignored); colour-blind mana. CONSERVATIVE / OMITTED: Goldspan/Old Gnawbone
treasures, Hellkite Charger extra combats, Dragonhawk exile-burn, Betor thresholds, Zurgo
dig, Imoti cascade, riot counters-mode, Smuggler's Surprise, non-dragon beaters (dorks
don't attack). PROXY note: the 28 fill lands are ours; spells are all his.

Data: collection/oracle-cards.json · Run: python scripts/opponent_labs/opp_urdragon_lab.py
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
DECK = ROOT / "opponents" / "dragon-dragon-dragon-PROXY-20260702.txt"
COMMANDER = "The Ur-Dragon"
SEED = 20260702
TURNS = 14
SHOW = [4, 5, 6, 7, 8, 9, 10, 12]
UD_COST, UD_FLOOR, DRAGON_FLOOR = 9, 5, 2
ROCKS = {"Sol Ring": (1, 2), "Arcane Signet": (2, 1), "Mox Jasper": (0, 1),
         "Birds of Paradise": (1, 1), "Noble Hierarch": (1, 1), "Ignoble Hierarch": (1, 1),
         "Delighted Halfling": (1, 1), "Wild Growth": (1, 1), "Bloom Tender": (2, 2),
         "Scaled Nurturer": (2, 1), "Nature's Lore": (2, 1), "Three Visits": (2, 1),
         "Cultivate": (3, 1), "Kodama's Reach": (3, 1), "Skyshroud Claim": (4, 2),
         "Chromatic Lantern": (3, 1)}

HASTE = {"Dragon Tempest": 2, "Concordant Crossroads": 1, "Temur Ascendancy": 3,
         "Rhythm of the Wild": 3, "Frostcliff Siege": 3, "The Fire Crystal": 4}
BURN_TEMPEST = "Dragon Tempest"          # X = #dragons per dragon ETB
BURN_SCOURGE = "Scourge of Valkas"       # X = #dragons per dragon ETB (a dragon itself)
BURN_TERROR = "Terror of the Peaks"      # = entering power (a dragon itself)
MIIRYM, LATHLISS = "Miirym, Sentinel Wyrm", "Lathliss, Dragon Queen"
TWINFLAME, NERIV = "Twinflame Tyrant", "Neriv, Heart of the Storm"
DRAW_ENG = {"Elemental Bond": 3, "Garruk's Uprising": 3, "Temur Ascendancy": 3,
            "Guardian Project": 4}       # Great Henge handled separately (dynamic cost)
HENGE = "The Great Henge"
INCUBATOR, BATTLECRIER = "Urza's Incubator", "Temur Battlecrier"
DRACO, SNEAK, TOOTH, GENESIS = "Dracogenesis", "Sneak Attack", "Tooth and Nail", "Majestic Genesis"
URENI, COURSER, TIAMAT = "Ureni of the Unwritten", "Hellkite Courser", "Tiamat"
CTSD = "Call the Spirit Dragons"


def pull_commander(library, name):
    for i, (nm, _rec) in enumerate(library):
        if nm.lower() == name.lower():
            return library[:i] + library[i + 1:]
    raise SystemExit(f"commander {name!r} not in parsed list")


def is_dragon(rec):
    tl = rec.get("type_line", "")
    return "Dragon" in tl and "Creature" in tl


class Trial:
    def __init__(self, library, rng, powers):
        self.g = slc.Goldfish(library, rng, rocks=ROCKS)
        self.tbl = slc.Table()
        self.p = powers                   # name(lower) -> power
        self.board = set()                # named engines
        self.dragons = 0                  # dragon bodies (incl. tokens)
        self.mature = 0.0                 # power that can attack
        self.fresh = 0.0                  # power that entered this turn (haste-gated)
        self.ud = False                   # commander on battlefield
        self.ctsd_turn = None             # turn CtSD hit play

    # -- helpers ---------------------------------------------------------------
    def power(self, nm):
        return float(self.p.get(nm.lower(), 3) or 3)

    def haste(self):
        return any(h in self.board for h in HASTE)

    def mult(self, entered_now):
        m = 2 if TWINFLAME in self.board else 1
        if entered_now and NERIV in self.board:
            m *= 2
        return m

    def discount(self):
        d = 1 + (2 if INCUBATOR in self.board else 0)      # eminence + Incubator
        if BATTLECRIER in self.board:
            d += self.dragons                              # -1 per power>=4 body (his turn)
        return d

    def dragon_cost(self, rec):
        return max(DRAGON_FLOOR, int(rec.get("cmc", 4)) - self.discount())

    def dragon_etb(self, nm, T, nontoken=True):
        """One dragon body enters: burn triggers, token engines, draw engines."""
        entries = [(nm, self.power(nm), nontoken)]
        if nontoken and MIIRYM in self.board:
            entries.append((nm, self.power(nm), False))            # Miirym copy
        if nontoken and LATHLISS in self.board and nm != LATHLISS:
            entries.append(("dragon-token-5-5", 5.0, False))       # Lathliss 5/5
        for ename, pw, _nt in entries:
            self.dragons += 1
            self.fresh += pw
            burn = 0
            if BURN_TEMPEST in self.board:
                burn += self.dragons
            if BURN_SCOURGE in self.board:
                burn += self.dragons
            if BURN_TERROR in self.board and ename != BURN_TERROR:
                burn += pw
            if burn:
                self.tbl.hit_focus(burn * self.mult(True), T)
            draws = sum(1 for e in DRAW_ENG if e in self.board and pw >= 4)
            if HENGE in self.board:
                draws += 1
            if draws:
                self.g.draw(min(draws, 3))
            if self.tbl.done:
                return

    def put_dragon(self, nm, rec, T):
        """A dragon lands (cast or cheated): engine bookkeeping + ETB chain."""
        if nm in (BURN_SCOURGE, BURN_TERROR, MIIRYM, LATHLISS, TWINFLAME, NERIV,
                  URENI, BATTLECRIER):
            self.board.add(nm)
        self.dragon_etb(nm, T)
        if nm == URENI:
            self.ureni_dig(T)
        if nm == TIAMAT:
            self.tiamat_fetch()

    def biggest_hand_dragon(self):
        best, bi = None, None
        for i, (nm, rec) in enumerate(self.g.hand):
            if is_dragon(rec) and (best is None or self.power(nm) > self.power(best[0])):
                best, bi = (nm, rec), i
        return bi, best

    def ureni_dig(self, T):
        """Ureni ETB: put a dragon from the top 8 into play (scan the real library)."""
        g = self.g
        window = list(range(g.ptr, min(g.ptr + 8, len(g.deck))))
        pick = max((i for i in window if is_dragon(g.deck[i][1])),
                   key=lambda i: self.power(g.deck[i][0]), default=None)
        if pick is not None:
            nm, rec = g.deck[pick]
            g.deck[pick] = g.deck[len(g.deck) - 1]; g.deck.pop()
            self.put_dragon(nm, rec, T)

    def cheat_from_library(self, nm, T):
        """Move nm from library into play, tolerant of nested digs (Ureni/Miirym chains
        may have already taken it mid-resolution)."""
        g = self.g
        if not g.fetch(nm):
            return False
        i = g.in_hand(nm)
        if i is None:
            return False
        _, rec = g.hand.pop(i)
        self.put_dragon(nm, rec, T)
        return True

    def tiamat_fetch(self):
        """Tiamat cast trigger: five biggest distinct dragons from library to hand."""
        g = self.g
        names = sorted({g.deck[i][0] for i in range(g.ptr, len(g.deck))
                        if is_dragon(g.deck[i][1]) and g.deck[i][0] != TIAMAT},
                       key=self.power, reverse=True)[:5]
        for nm in names:
            g.fetch(nm)

    # -- turn --------------------------------------------------------------------
    def turn(self, T):
        g = self.g
        g.begin_turn(T)
        # Call the Spirit Dragons: survived an upkeep with 5+ dragons -> the game ends
        if self.ctsd_turn is not None and T > self.ctsd_turn and self.dragons >= 5:
            self.tbl.kill_all(T); return
        self.mature += self.fresh
        self.fresh = 0.0
        g.deploy_rocks()

        progress = True
        while progress and not self.tbl.done:
            progress = False
            # 1. engines cheapest-first (haste / burn enchantments / draw / discounts)
            for nm, c in sorted({**HASTE, "Urza's Incubator": 3, CTSD: 5}.items(),
                                key=lambda kv: kv[1]):
                if nm not in self.board and g.has(nm) and g.avail >= c and g.cast(nm, c):
                    self.board.add(nm)
                    if nm == CTSD:
                        self.ctsd_turn = T
                    progress = True; break
            for nm, c in DRAW_ENG.items():
                if nm not in self.board and g.has(nm) and g.avail >= c and g.cast(nm, c):
                    self.board.add(nm); progress = True; break
            if HENGE not in self.board and g.has(HENGE) and self.mature + self.fresh > 0:
                hc = max(2, 9 - int(max(self.mature, self.fresh, 5)))
                if g.avail >= hc and g.cast(HENGE, hc):
                    self.board.add(HENGE); progress = True
            # 2. Dracogenesis -> then every hand dragon is free
            if DRACO not in self.board and g.has(DRACO) and g.avail >= 8 and g.cast(DRACO, 8):
                self.board.add(DRACO); progress = True
            if DRACO in self.board:
                bi, best = self.biggest_hand_dragon()
                while best is not None and not self.tbl.done:
                    g.hand.pop(bi)
                    self.put_dragon(best[0], best[1], T)
                    bi, best = self.biggest_hand_dragon()
                if self.tbl.done:
                    return
            # 3. mass cheat: Tooth entwined / Majestic Genesis
            if g.has(TOOTH) and g.avail >= 9 and g.cast(TOOTH, 9):
                for _ in range(2):
                    names = [g.deck[i][0] for i in range(g.ptr, len(g.deck))
                             if is_dragon(g.deck[i][1])]
                    if not names:
                        break
                    self.cheat_from_library(max(names, key=self.power), T)
                progress = True
            if g.has(GENESIS) and g.avail >= 8 and g.cast(GENESIS, 8):
                window = [g.deck[i] for i in range(g.ptr, min(g.ptr + 9, len(g.deck)))]
                for nm, _rec in [t for t in window if is_dragon(t[1])]:
                    self.cheat_from_library(nm, T)
                progress = True
            # 4. the commander (floor 5; eminence doesn't discount himself)
            if not self.ud:
                udc = max(UD_FLOOR, UD_COST - (self.discount() - 1))
                if g.avail >= udc:
                    g.avail -= udc; self.ud = True
                    self.put_dragon(COMMANDER, {"type_line": "Creature — Dragon Avatar",
                                                "cmc": 9}, T)
                    progress = True
            # 5. hand dragons biggest-first (Tiamat priority: she refuels)
            if g.has(TIAMAT):
                tc = max(UD_FLOOR, 7 - self.discount())
                if g.avail >= tc and g.cast(TIAMAT, tc):
                    self.put_dragon(TIAMAT, {"type_line": "Creature — Dragon God",
                                             "cmc": 7}, T)
                    progress = True
            bi, best = self.biggest_hand_dragon()
            if best is not None:
                cost = self.dragon_cost(best[1])
                if g.avail >= cost:
                    g.hand.pop(bi); g.avail -= cost
                    self.put_dragon(best[0], best[1], T)
                    progress = True
            # 6. Sneak Attack: biggest hand dragon swings this turn only
            if SNEAK not in self.board and g.has(SNEAK) and g.avail >= 4 and g.cast(SNEAK, 4):
                self.board.add(SNEAK); progress = True
        if self.tbl.done:
            return

        # combat: matured power (+fresh if haste) + Sneak/Courser one-shots
        swing = self.mature + (self.fresh if self.haste() else 0)
        oneshot = 0.0
        if SNEAK in self.board and self.g.avail >= 1:
            bi, best = self.biggest_hand_dragon()
            if best is not None:
                self.g.avail -= 1; self.g.hand.pop(bi)
                self.dragon_etb(best[0], T)                  # ETB burn fires
                pw = self.power(best[0])
                self.fresh -= pw                             # sacked at EOT
                oneshot += pw * self.mult(True)
        if swing > 0 or oneshot > 0:
            dmg = swing * self.mult(False) + oneshot
            # Neriv also doubles the FRESH share of a hasty swing
            if NERIV in self.board and self.haste() and self.fresh > 0:
                dmg += self.fresh * self.mult(False)
            self.tbl.hit_focus(dmg, T)
            if self.ud and self.dragons:
                self.g.draw(min(self.dragons, 4))            # UD attack trigger: draw
                bi, best = self.biggest_hand_dragon()        # + free permanent from hand
                if best is not None:
                    self.g.hand.pop(bi)
                    self.put_dragon(best[0], best[1], T)


def mode_clock(index, aliases, trials, deck=None):
    deck = deck or DECK
    print("=" * 74)
    print(f"OPP CLOCK — Ur-Dragon swarm goldfish ({trials} trials, seed {SEED})")
    print("=" * 74)
    print("  PROXY clock: his real 72 spells + our 28-land fill; caveats in the docstring.")
    rng = random.Random(SEED)
    library, _ = slc.load_parsed(deck, index, aliases)
    library = pull_commander(library, COMMANDER)
    powers = slc.load_powers([nm for nm, _ in library] + [COMMANDER])
    print(f"  library {len(library)} + commander {COMMANDER}   [{deck.name}]")
    res = slc.run_goldfish(lambda: Trial(library, rng, powers), trials, TURNS)
    slc.report_clock(res, SHOW, TURNS, trials)
    print("\n  Read: UNBLOCKED ceiling — the pod blocks dragons, so real pressure lands")
    print("  later (vs_dragon_lab owns the defended matchup). This curve is the K-attempt")
    print("  schedule + the burn sub-axis, which ignores blockers for real.")


if __name__ == "__main__":
    slc.run_cli(__doc__, {"clock": mode_clock})
