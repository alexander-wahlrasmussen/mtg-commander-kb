#!/usr/bin/env python3
"""kfk_clock_lab.py — Forced Liquidation (Kefka, Court Mage — INTERNAL burn) KILL-TURN goldfish.

Stage 3 of the 2026-06-12 candidate bake-off. Deck:
decks/considering/forced-liquidation-20260612.txt (candidate #9, the internal
Grixis forced-draw BURN proposal — distinct from the external combo-control
Kefka list, labbed in kfx_clock_lab.py). Built on speed_lab_core.py.

THE KILL: wheels through static punishers. Damage is symmetric across
opponents (hit_all), so decap and table largely CONVERGE — the deck's whole
anti-Abolisher thesis (triggers, not spells, deliver the damage). Rules facts
encoded (card_lookup.py 2026-06-12):

  PER-WHEEL DAMAGE to each opponent (opponents discard their hand ~H_opp,
  draw 7):
    opp-DISCARD punishers: Megrim / Liliana's Caress 2 x H_opp.
    opp-DRAW punishers:    Underworld Dreams / Fate Unraveler / Ob Nixilis /
                           Kederekt Parasite (red permanent: Kefka or any
                           red rock — modelled true once any is out) 1 x 7;
                           Sheoldred 2 x 7.
    your-DISCARD punisher: Glint-Horn Buccaneer 1 x (your hand dumped).
    your-DRAW punishers:   Psychosis Crawler 1 x (your draws) to EACH
                           opponent; Niv-Mizzet 1 x draws, pooled as focus.
  NOTION THIEF inverts a wheel: opponents draw NOTHING (their 7 draws are
  yours -> your draws = 7 + 21 = 28), so opp-draw punishers contribute ZERO
  on that wheel while Psychosis/Niv see 28. Discard punishers still fire.
  BLOODLETTER doubles every opponent life loss on YOUR turn (passive chip on
  their turns is NOT doubled).
  PASSIVE CHIP each round: each opponent's own draw step feeds the opp-draw
  punishers (1 draw x rate, not doubled).
  KEFKA: ETB + each attack -> each opponent discards 1 (2 x discard-punisher
  rate each, doubled on your turn) and you draw ~3; he swings 4 (focus).
  PEER INTO THE ABYSS (7): with Notion Thief + Psychosis Crawler -> you draw
  ~30, 30 x mult to EACH opponent (table nuke). With an opp-draw punisher:
  ~30 draws + half life = one opponent dead (decap tool). Held otherwise.
  WHEELS: Wheel of Fortune 3, Windfall 3, Dark Deal 3 (draws = H-1),
  Reforge the Soul 5 (miracle ignored — conservative), Echo of Eons 6
  (flashback 3 once in yard via a prior wheel/loot), Time Spiral 6 (refunds
  min(6, lands)), Memory Jar 5 (modelled as a plain wheel), Magus of the
  Wheel 3 + 2 to pop, Naktamun Lorespinner (prepared at upkeep if YOUR hand
  <=1 -> a {2}{R} Wheel of Fortune copy that turn).
  TUTORS: Demonic 2 / Diabolic 4 / Mastermind's Acquisition 4 -> first
  missing punisher (Sheoldred priority), then Wheel of Fortune.

OMITTED (conservative): Past in Flames rebuys, Waste Not value, Niv-Mizzet
pinging on YOUR non-wheel draws, counterspell protection, Cursed Totem
politics, looting spells as damage (Faithless Looting etc. counted only as
hand-fixing -> ignored entirely). OPTIMISTIC: colour-blind mana, rocks
repeat (Mana Vault convention), opponents' hands refill to 7 by your next
wheel, all punishers survive. Trust shapes and deltas.

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

DECK = ROOT / "decks" / "considering" / "forced-liquidation-20260612.txt"
SEED = 20260612
TURNS = 12
SHOW = [4, 5, 6, 7, 8, 9, 10, 12]

ROCKS = {"Sol Ring": (1, 2), "Mana Vault": (1, 3), "Arcane Signet": (2, 1),
         "Dimir Signet": (2, 1), "Rakdos Signet": (2, 1),
         "Izzet Signet": (2, 1), "Talisman of Dominance": (2, 1),
         "Mind Stone": (2, 1), "Thought Vessel": (2, 1),
         "Commander's Sphere": (3, 1), "Prismatic Lens": (2, 1),
         "Ruby Medallion": (2, 1)}
OPP_DISCARD = {"Megrim": 3, "Liliana's Caress": 2}          # 2 per card
OPP_DRAW_1 = {"Underworld Dreams": 3, "Fate Unraveler": 4,
              "Ob Nixilis, the Hate-Twisted": 5, "Kederekt Parasite": 1,
              "Razorkin Needlehead": 2}                      # 1 per draw
SHEOLDRED = "Sheoldred, the Apocalypse"                      # 2 per draw
YOUR_DRAW_ALL = {"Psychosis Crawler": 5}                     # each opp
YOUR_DRAW_FOCUS = {"Niv-Mizzet, Parun": 6}
GLINT = "Glint-Horn Buccaneer"
WHEELS = {"Wheel of Fortune": 3, "Windfall": 3, "Dark Deal": 3,
          "Reforge the Soul": 5, "Memory Jar": 5, "Echo of Eons": 6,
          "Time Spiral": 6}
PUNISHER_COSTS = {**OPP_DISCARD, **OPP_DRAW_1, SHEOLDRED: 4,
                  **YOUR_DRAW_ALL, **YOUR_DRAW_FOCUS, GLINT: 3,
                  "Bloodletter of Aclazotz": 4, "Notion Thief": 4}
TUTORS = {"Demonic Tutor": 2, "Diabolic Tutor": 4,
          "Mastermind's Acquisition": 4}


class Trial:
    def __init__(self, library, rng):
        self.g = slc.Goldfish(library, rng, rocks=ROCKS)
        self.tbl = slc.Table()
        self.bf = set()
        self.kefka = False
        self.opp_hand = 7
        self.echo_yard = False
        self.naktamun = False
        self.magus = False

    # ---- punisher rates -----------------------------------------------------
    def opp_draw_rate(self):
        r = sum(1 for p in OPP_DRAW_1 if p in self.bf)
        if SHEOLDRED in self.bf:
            r += 2
        return r

    def opp_discard_rate(self):
        return 2 * sum(1 for p in OPP_DISCARD if p in self.bf)

    def mult(self):
        return 2 if "Bloodletter of Aclazotz" in self.bf else 1

    def wheel_worth(self):
        """Damage one wheel deals to each opponent right now."""
        notion = "Notion Thief" in self.bf
        per = self.opp_discard_rate() * self.opp_hand
        if not notion:
            per += self.opp_draw_rate() * 7
        my_draws = 7 + (21 if notion else 0)
        per += sum(1 for p in YOUR_DRAW_ALL if p in self.bf) * my_draws
        per += (1 if GLINT in self.bf else 0) * len(self.g.hand)
        return per * self.mult()

    def fire_wheel(self, nm, cost, T):
        g = self.g
        notion = "Notion Thief" in self.bf
        g.avail -= cost
        per = self.wheel_worth()
        focus = sum(1 for p in YOUR_DRAW_FOCUS if p in self.bf) \
            * (7 + (21 if notion else 0)) * self.mult()
        if nm == "Time Spiral":
            g.add_mana(min(6, g.lands))
        # your hand cycles
        h = len(g.hand)
        for _ in range(h):
            t = g.hand.pop()
            g.yard.append(t)
            if t[0] == "Echo of Eons":
                self.echo_yard = True
        draws = 6 if nm == "Dark Deal" else 7
        g.draw(draws + (21 if notion else 0))
        if per:
            self.tbl.hit_all(per, T)
        if focus:
            self.tbl.hit_focus(focus, T)
        self.opp_hand = (self.opp_hand - 1 if nm == "Dark Deal" else 7)
        if notion:
            self.opp_hand = 0 if nm != "Dark Deal" else self.opp_hand

    # ---- one turn -------------------------------------------------------------
    def turn(self, T):
        g = self.g
        # opponents' own draw steps feed the draw punishers (not doubled)
        chip = self.opp_draw_rate()
        if chip:
            self.tbl.hit_all(chip, T)
        if self.tbl.done:
            return
        self.opp_hand = min(self.opp_hand + 1, 7)
        g.begin_turn(T)
        g.deploy_rocks()
        # Naktamun prepared: free Wheel copy for 3 if our hand emptied out
        naktamun_wheel = self.naktamun and len(g.hand) <= 1

        progress = True
        while progress:
            progress = False
            # punishers first
            for nm, c in sorted(PUNISHER_COSTS.items(), key=lambda x: x[1]):
                if nm not in self.bf and g.has(nm) and g.avail >= c:
                    g.cast(nm, c)
                    self.bf.add(nm)
                    progress = True
            # Kefka (5): ETB chip + engine
            if not self.kefka and g.avail >= 5:
                g.avail -= 5
                self.kefka = True
                self.bf.add("Kefka, Court Mage")
                progress = True
                if self.opp_hand >= 1:
                    per = self.opp_discard_rate() * self.mult()
                    if per:
                        self.tbl.hit_all(per, T)
                    self.opp_hand -= 1
                g.draw(3)
            # bodies that wheel
            for nm, c, flag in (("Naktamun Lorespinner", 3, "naktamun"),
                                ("Magus of the Wheel", 3, "magus")):
                if not getattr(self, flag) and g.has(nm) and g.avail >= c:
                    g.cast(nm, c)
                    setattr(self, flag, True)
                    progress = True
            # Peer into the Abyss lines
            if g.has("Peer into the Abyss") and g.avail >= 7:
                if "Notion Thief" in self.bf and \
                        (self.bf & set(YOUR_DRAW_ALL)):
                    g.cast("Peer into the Abyss", 7)
                    self.tbl.hit_all(30 * self.mult(), T)
                    g.draw(10)
                    progress = True
                elif self.opp_draw_rate() >= 1:
                    g.cast("Peer into the Abyss", 7)
                    self.tbl.hit_focus(40, T)        # ~30 triggers + half life
                    progress = True
            # wheels — when they hurt, or when the hand is spent
            worth = self.wheel_worth()
            if worth >= 4 or len(g.hand) <= 2:
                cheapest = None
                for nm, c in sorted(WHEELS.items(), key=lambda x: x[1]):
                    if g.has(nm) and g.avail >= c:
                        cheapest = (nm, c)
                        break
                if self.echo_yard and g.avail >= 3 and (
                        cheapest is None or cheapest[1] > 3):
                    self.echo_yard = False
                    self.fire_wheel("Echo of Eons", 3, T)
                    progress = True
                elif naktamun_wheel and g.avail >= 3:
                    naktamun_wheel = False
                    self.fire_wheel("Wheel of Fortune", 3, T)
                    progress = True
                elif self.magus and g.avail >= 2 and worth >= 8:
                    self.magus = False
                    self.fire_wheel("Wheel of Fortune", 2, T)
                    progress = True
                elif cheapest:
                    self.fire_wheel(*cheapest, T)
                    progress = True
            # tutors -> missing punisher, then Wheel
            for tut, c in TUTORS.items():
                if g.has(tut) and g.avail >= c + 1:
                    tgt = None
                    if not (self.bf & ({SHEOLDRED} | set(OPP_DRAW_1)
                                       | set(OPP_DISCARD))):
                        for cand in (SHEOLDRED, "Underworld Dreams", "Megrim"):
                            if any(g.deck[i][0] == cand
                                   for i in range(g.ptr, len(g.deck))):
                                tgt = cand
                                break
                    if tgt is None and not g.has("Wheel of Fortune") and any(
                            g.deck[i][0] == "Wheel of Fortune"
                            for i in range(g.ptr, len(g.deck))):
                        tgt = "Wheel of Fortune"
                    if tgt:
                        g.cast(tut, c)
                        g.fetch(tgt)
                        progress = True
                        break
            if self.tbl.done:
                return

        # Kefka attacks: trigger + 4 combat
        if self.kefka:
            if self.opp_hand >= 1:
                per = self.opp_discard_rate() * self.mult()
                if per:
                    self.tbl.hit_all(per, T)
                self.opp_hand -= 1
                g.draw(2)
            self.tbl.hit_focus(4, T)


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
    print(f"CLOCK — Forced Liquidation (Kefka-burn, internal) kill-turn goldfish "
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
    print("\n  Proposal ceiling ~17/20, no formal turn claim; brief bar is T6-7.")


if __name__ == "__main__":
    slc.run_cli(__doc__, {"clock": mode_clock})
