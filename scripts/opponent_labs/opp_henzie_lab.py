#!/usr/bin/env python3
"""opp_henzie_lab.py — BLITZ-VALUE kill-turn goldfish for the archenemy's Henzie deck
(opponents/major-tool-PROXY-20260702.txt — his real 66 spells + our 33-land fill; a PROXY
clock, see scripts/opponent_labs/README.md). Seen ONCE (user lost to it) — the lightest
rotation weight, so the model is deliberately lean.

KILL SHAPE (encoded cards card_lookup-verified 2026-07-02): blitzed fatties hitting the
focus player + drain/burn riders, recursion keeping the yard flowing:

  Henzie {B}{R}{G}: MV4+ creature spells have blitz AT MANA COST; blitz costs -{1} per
    commander cast this game (so each Henzie recast discounts the whole deck). Blitz =
    haste + dies EOT + draw a card.
  Blitz a fatty -> its power swings NOW (unblocked ceiling) -> Warstorm Surge ETB burn
    (= power, focus) -> EOT death: +1 draw, Stalking Vengeance (its power AGAIN, focus),
    Kokusho (each opp -5) / Junji (each opp -2) death riders, Archon of Cruelty ETB -3.
  Recursion: Chainer (once/turn, discard -> cast the biggest yard fatty, it re-blitzes)
    · Victimize (sac -> return 2 tapped, ETBs fire) · Living Death (mass return, all ETBs).
  Goreclaw: power>=4 creature spells cost {2} less (stacks with the blitz discount).

OPTIMISTIC (ceiling): unblocked, colour-blind mana, engine pieces (Warstorm/Stalking/
Goreclaw/Chainer) never removed. CONSERVATIVE / OMITTED: Etali free casts, Ilharg cheats,
Birthing Pod chains, Skullclamp/Life's Legacy draw, Dictate of Erebos pressure, Protean
Hulk piles, Riveteers Ascendancy/Industrial Advancement/Shadow in the Warp, reanimation
via Animate Dead/Junji mode-2. The 33 fill lands are ours; spells are all his.

Data: collection/oracle-cards.json · Run: python scripts/opponent_labs/opp_henzie_lab.py
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
DECK = ROOT / "opponents" / "major-tool-PROXY-20260702.txt"
COMMANDER = 'Henzie "Toolbox" Torre'
SEED = 20260702
TURNS = 14
SHOW = [4, 5, 6, 7, 8, 9, 10, 12]
ROCKS = {"Sol Ring": (1, 2), "Arcane Signet": (2, 1), "Fellwar Stone": (2, 1),
         "Birds of Paradise": (1, 1), "Ignoble Hierarch": (1, 1),
         "Farseek": (2, 1), "Nature's Lore": (2, 1), "Three Visits": (2, 1),
         "Cultivate": (3, 1), "Kodama's Reach": (3, 1)}

WARSTORM, STALKING = "Warstorm Surge", "Stalking Vengeance"
GORECLAW, CHAINER = "Goreclaw, Terror of Qal Sisma", "Chainer, Nightmare Adept"
KOKUSHO, JUNJI, ARCHON = "Kokusho, the Evening Star", "Junji, the Midnight Sky", "Archon of Cruelty"
VICTIMIZE, LIVING_DEATH = "Victimize", "Living Death"
ENGINES = {WARSTORM: 6, STALKING: 7, GORECLAW: 4, CHAINER: 4}   # cast normally, persist


def pull_commander(library, name):
    for i, (nm, _rec) in enumerate(library):
        if nm.lower() == name.lower():
            return library[:i] + library[i + 1:]
    raise SystemExit(f"commander {name!r} not in parsed list")


def is_creature(rec):
    return "Creature" in rec.get("type_line", "")


class Trial:
    def __init__(self, library, rng, powers):
        self.g = slc.Goldfish(library, rng, rocks=ROCKS)
        self.tbl = slc.Table()
        self.p = powers
        self.board = set()               # persistent engines
        self.henzie = False
        self.casts = 0                   # commander casts (blitz discount)
        self.yard_fatties = []           # (name, power) blitzed-away bodies
        self.mature = 0.0                # persistent board power (engines that attack)

    def power(self, nm):
        return float(self.p.get(nm.lower(), 3) or 3)

    def blitz_cost(self, rec):
        c = int(rec.get("cmc", 4)) - self.casts
        if GORECLAW in self.board:
            c -= 2
        return max(1, c)

    def blitz_fire(self, nm, pw, T, cmc=5):
        """One blitzed body: swings now + ETB/death riders + the blitz draw."""
        dmg = pw                                        # unblocked swing
        if WARSTORM in self.board:
            dmg += pw                                   # ETB burn
        if STALKING in self.board:
            dmg += pw                                   # dies EOT -> power again
        if nm == ARCHON:
            dmg += 3
        self.tbl.hit_focus(dmg, T)
        if nm == KOKUSHO:
            self.tbl.hit_all(5, T)
        if nm == JUNJI:
            self.tbl.hit_all(2, T)
        self.g.draw(1)                                  # blitz death draw
        self.yard_fatties.append((nm, pw, cmc))

    def biggest_hand_fatty(self):
        best, bi = None, None
        for i, (nm, rec) in enumerate(self.g.hand):
            if is_creature(rec) and rec.get("cmc", 0) >= 4 and nm not in ENGINES:
                if best is None or self.power(nm) > self.power(best[0]):
                    best, bi = (nm, rec), i
        return bi, best

    def turn(self, T):
        g = self.g
        g.begin_turn(T)
        g.deploy_rocks()
        chainer_used = False

        progress = True
        while progress and not self.tbl.done:
            progress = False
            # commander (recasts add blitz discount; tax 2 per recast)
            if not self.henzie and g.avail >= 3 + 2 * self.casts:
                g.avail -= 3 + 2 * self.casts
                self.henzie = True; self.casts += 1; progress = True
            # persistent engines, cheapest first (they attack from next turn)
            for nm, c in sorted(ENGINES.items(), key=lambda kv: kv[1]):
                cost = max(1, c - (2 if GORECLAW in self.board and self.power(nm) >= 4 else 0))
                if nm not in self.board and g.has(nm) and g.avail >= cost and g.cast(nm, cost):
                    self.board.add(nm)
                    self.mature += 0 if nm == CHAINER else self.power(nm)
                    progress = True; break
            if not self.henzie:
                break
            # Living Death: mass return when the yard is stocked
            if len(self.yard_fatties) >= 3 and g.has(LIVING_DEATH) and g.avail >= 5 \
                    and g.cast(LIVING_DEATH, 5):
                burst = 0.0
                for nm, pw, _c in self.yard_fatties:
                    # Chainer's static: not-cast-from-hand creatures get haste -> swing
                    # NOW with him out; otherwise ETB burn only, attack next turn
                    if CHAINER in self.board:
                        burst += pw
                    if WARSTORM in self.board:
                        burst += pw
                    self.mature += pw
                    if nm == ARCHON:
                        burst += 3
                self.yard_fatties = []
                if burst:
                    self.tbl.hit_focus(burst, T)
                progress = True
            # Victimize: two biggest back (tapped; ETB burn fires, attack next turn)
            if len(self.yard_fatties) >= 2 and g.has(VICTIMIZE) and g.avail >= 3 \
                    and g.cast(VICTIMIZE, 3):
                back = sorted(self.yard_fatties, key=lambda t: -t[1])[:2]
                for nm, pw, _c in back:
                    self.yard_fatties.remove((nm, pw, _c))
                    self.mature += pw
                    if WARSTORM in self.board:
                        self.tbl.hit_focus(pw, T)
                    if nm == ARCHON:
                        self.tbl.hit_focus(3, T)
                progress = True
            # blitz the biggest hand fatty
            bi, best = self.biggest_hand_fatty()
            if best is not None:
                cost = self.blitz_cost(best[1])
                if g.avail >= cost:
                    g.hand.pop(bi); g.avail -= cost
                    self.blitz_fire(best[0], self.power(best[0]), T,
                                    int(best[1].get("cmc", 5)))
                    progress = True
            # Chainer: once/turn re-blitz the biggest yard fatty (discard = worst card)
            if not chainer_used and CHAINER in self.board and self.yard_fatties \
                    and len(g.hand) > 0:
                nm, pw, cmc = max(self.yard_fatties, key=lambda t: t[1])
                cost = max(1, cmc - self.casts
                           - (2 if GORECLAW in self.board and pw >= 4 else 0))
                if g.avail >= cost:
                    g.hand.pop()                         # discard cost
                    g.avail -= cost
                    self.yard_fatties.remove((nm, pw, cmc))
                    self.blitz_fire(nm, pw, T, cmc)
                    chainer_used = True; progress = True

        if self.tbl.done:
            return
        if self.mature > 0:                              # persistent engines swing too
            self.tbl.hit_focus(self.mature, T)


def mode_clock(index, aliases, trials, deck=None):
    deck = deck or DECK
    print("=" * 74)
    print(f"OPP CLOCK — Henzie blitz-value goldfish ({trials} trials, seed {SEED})")
    print("=" * 74)
    print("  PROXY clock: his real 66 spells + our 33-land fill; lean model (docstring).")
    rng = random.Random(SEED)
    library, _ = slc.load_parsed(deck, index, aliases)
    library = pull_commander(library, COMMANDER)
    library = [t for t in library if t[0] != "Lurking Predators"] + \
              [t for t in library if t[0] == "Lurking Predators"]   # category quirk: in the 99
    powers = slc.load_powers([nm for nm, _ in library])
    print(f"  library {len(library)} + commander {COMMANDER}   [{deck.name}]")
    res = slc.run_goldfish(lambda: Trial(library, rng, powers), trials, TURNS)
    slc.report_clock(res, SHOW, TURNS, trials)
    print("\n  Read: unblocked blitz ceiling; the deck is value-attrition in real games")
    print("  (Dictate/recursion unmodelled) — the decap curve is the K-attempt schedule.")


if __name__ == "__main__":
    slc.run_cli(__doc__, {"clock": mode_clock})
