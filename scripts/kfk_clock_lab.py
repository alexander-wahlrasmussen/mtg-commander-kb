#!/usr/bin/env python3
"""kfk_clock_lab.py — Forced Liquidation (Kefka, Court Mage — Grixis forced-draw
BURN) KILL-TURN goldfish, with the 2026-06-25 combo axis.

Deck: decks/considering/forced-liquidation-20260625.txt (codename Forced
Liquidation). Built on speed_lab_core.py. Re-pointed + rebuilt 2026-06-25 — the
prior version pointed at the stale 06-12 list and predated the Displacer Kitten /
Aether Channeler / Jace's Archivist / Molten Psyche changes.

TWO WIN AXES modelled, reported combo-ON vs combo-OFF so the combo's clock
contribution is the delta (per the lab-before-proposing rule):

  AXIS 1 — BURN (always on): wheels through static punishers. Damage is largely
  symmetric (hit_all), so decap and table converge — the anti-Abolisher thesis
  (statics deliver damage, not spells). Per-wheel damage to each opponent:
    opp-DISCARD punishers: Megrim / Liliana's Caress  -> 2 x H_opp each.
    opp-DRAW punishers:    Underworld Dreams / Fate Unraveler / Ob Nixilis /
                           Kederekt Parasite -> 1 x draws; Sheoldred -> 2 x draws.
    your-DISCARD:          Glint-Horn Buccaneer -> 1 x (your hand dumped).
    your-DRAW:             Psychosis Crawler -> 1 x your draws to EACH opp;
                           Niv-Mizzet Parun -> 1 x your draws, pooled as focus.
  NOTION THIEF inverts a wheel: opponents draw NOTHING (their draws become yours
  -> ~28), opp-draw punishers contribute 0, Psychosis/Niv see 28.
  BLOODLETTER doubles every opponent life loss on YOUR turn.
  KEFKA / NICOL BOLAS the RAVAGER: ETB -> each opponent discards 1 (2 x
  discard-punisher rate, doubled on your turn).
  WHEELS (06-25 build): Windfall 3, Dark Deal 3 (draws H-1), Reforge the Soul 5,
  Echo of Eons 6 (flashback 3 once binned), MOLTEN PSYCHE 3 (shuffle wheel,
  your draws = hand size; metalcraft burn = each opp's draws once >=3 artifacts),
  MAGUS of the WHEEL (3 body, sac for 2), JACE'S ARCHIVIST (cast 2, then a FREE
  repeatable wheel every later turn). Peer into the Abyss: Notion+Psychosis ->
  table nuke; else one opp-draw punisher -> single-target decap.
  TUTORS: Demonic 2 / Grim 3 / Final Parting 5 -> first missing punisher
  (Sheoldred priority), Final Parting also bins Echo of Eons for flashback.

  AXIS 2 — COMBO (combo-ON only): Displacer Kitten + Aether Channeler + Sol Ring
  + Mana Vault assembled in play, with Niv-Mizzet or Psychosis Crawler also out,
  = infinite ETB -> infinite draw -> lethal (CSB combo 1170-1393-2364-5034,
  find_combos-verified complete in deck). Modelled as: table dead the turn all
  five are online. Commander-independent, resolves on your turn (Abolisher-proof).

OMITTED (conservative): Past in Flames rebuys, Waste Not, Niv pinging your
non-wheel draws, counter protection, looting-as-damage. OPTIMISTIC: colour-blind
mana, rocks repeat (Mana Vault convention), opp hands refill to 7, all pieces
survive, Molten Psyche opp-draws modelled at full wheel rate (slightly high — it
is shuffle-not-discard, a simplification shared with Echo). Trust shapes/deltas.

Data: collection/oracle-cards.json. Writeup: analysis/Buy_List_ZeroSum_Lightning
War_ForcedLiquidation_2026-06-25.md (Bolas/Channeler pass).
"""
import importlib.util
import random
from pathlib import Path

ROOT = Path(__file__).parent.parent
_spec = importlib.util.spec_from_file_location(
    "speed_lab_core", Path(__file__).parent / "speed_lab_core.py")
slc = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(slc)
ds = slc.ds

DECK = ROOT / "decks" / "forced-liquidation-20260625.txt"   # promoted from considering/ 2026-06-28
SEED = 20260625
TURNS = 12
SHOW = [4, 5, 6, 7, 8, 9, 10, 12]

ROCKS = {"Sol Ring": (1, 2), "Mana Vault": (1, 3), "Arcane Signet": (2, 1),
         "Dimir Signet": (2, 1), "Rakdos Signet": (2, 1),
         "Izzet Signet": (2, 1), "Talisman of Dominance": (2, 1),
         "Mind Stone": (2, 1), "Thought Vessel": (2, 1),
         "Commander's Sphere": (3, 1), "Ruby Medallion": (2, 1)}
OPP_DISCARD = {"Megrim": 3, "Liliana's Caress": 2}          # 2 per card
OPP_DRAW_1 = {"Underworld Dreams": 3, "Fate Unraveler": 4,
              "Ob Nixilis, the Hate-Twisted": 5, "Kederekt Parasite": 1}
SHEOLDRED = "Sheoldred, the Apocalypse"                      # 2 per draw
YOUR_DRAW_ALL = {"Psychosis Crawler": 5}                     # each opp
YOUR_DRAW_FOCUS = {"Niv-Mizzet, Parun": 6}
GLINT = "Glint-Horn Buccaneer"
WHEELS = {"Windfall": 3, "Dark Deal": 3, "Molten Psyche": 3,
          "Reforge the Soul": 5, "Echo of Eons": 6}
PUNISHER_COSTS = {**OPP_DISCARD, **OPP_DRAW_1, SHEOLDRED: 4,
                  **YOUR_DRAW_ALL, **YOUR_DRAW_FOCUS, GLINT: 3,
                  "Bloodletter of Aclazotz": 4, "Notion Thief": 4}
TUTORS = {"Demonic Tutor": 2, "Grim Tutor": 3, "Final Parting": 5}
# combo pieces
COMBO_CREATURES = {"Displacer Kitten": 4, "Aether Channeler": 3}
COMBO_ROCKS = {"Sol Ring", "Mana Vault"}
COMBO_PAYOFF = {"Psychosis Crawler", "Niv-Mizzet, Parun"}


class Trial:
    def __init__(self, library, rng, combo=True):
        self.g = slc.Goldfish(library, rng, rocks=ROCKS)
        self.tbl = slc.Table()
        self.bf = set()
        self.combo = combo
        self.deployed = set()      # rock names in play (by name)
        self.rock_count = 0
        self.kefka = False
        self.kefka_turn = None     # turn Kefka landed (summoning-sickness gate)
        self.bolas = False
        self.opp_hand = 7
        self.echo_yard = False
        self.magus = False
        self.archivist = None      # turn Jace's Archivist landed (None = not out)

    # ---- punisher rates -----------------------------------------------------
    def opp_draw_rate(self):
        r = sum(1 for p in OPP_DRAW_1 if p in self.bf)
        if SHEOLDRED in self.bf:
            r += 2
        return r

    def opp_discard_rate(self):
        return 2 * sum(1 for p in OPP_DISCARD if p in self.bf)

    def n_punishers(self):
        """Draw/discard punishers in play. Lethal-or-bust: never spin a wheel on
        <2 (a half-loaded wheel just refuels the pod). Notion Thief counts — it
        denies opp draws AND (with Psychosis/Niv) is the 2-card kill."""
        P = (set(OPP_DRAW_1) | {SHEOLDRED} | set(OPP_DISCARD) | set(YOUR_DRAW_ALL)
             | set(YOUR_DRAW_FOCUS) | {GLINT, "Notion Thief"})
        return len(self.bf & P)

    def mult(self):
        return 2 if "Bloodletter of Aclazotz" in self.bf else 1

    def wheel_worth(self, opp_draws=7, my_draws=7):
        notion = "Notion Thief" in self.bf
        per = self.opp_discard_rate() * self.opp_hand
        if not notion:
            per += self.opp_draw_rate() * opp_draws
        md = my_draws + (21 if notion else 0)
        per += sum(1 for p in YOUR_DRAW_ALL if p in self.bf) * md
        per += (1 if GLINT in self.bf else 0) * len(self.g.hand)
        return per * self.mult()

    def fire_wheel(self, nm, cost, T):
        g = self.g
        notion = "Notion Thief" in self.bf
        g.avail = max(0, g.avail - cost)
        h = len(g.hand)
        molten = nm == "Molten Psyche"
        opp_draws = self.opp_hand if molten else 7
        my_draws = h if molten else (6 if nm == "Dark Deal" else 7)
        per = self.wheel_worth(opp_draws, my_draws)
        if molten and self.rock_count >= 3:          # metalcraft burst
            per += opp_draws * self.mult()
        focus = sum(1 for p in YOUR_DRAW_FOCUS if p in self.bf) \
            * (my_draws + (21 if notion else 0)) * self.mult()
        for _ in range(h):
            t = g.hand.pop()
            g.yard.append(t)
            if t[0] == "Echo of Eons":
                self.echo_yard = True
        g.draw(my_draws + (21 if notion else 0))
        if per:
            self.tbl.hit_all(per, T)
        if focus:
            self.tbl.hit_focus(focus, T)
        if nm == "Dark Deal":
            self.opp_hand = max(0, self.opp_hand - 1)
        elif not molten:
            self.opp_hand = 7
        if notion and nm != "Dark Deal":
            self.opp_hand = 0

    def combo_online(self):
        return (self.combo
                and {"Displacer Kitten", "Aether Channeler"} <= self.bf
                and COMBO_ROCKS <= self.deployed
                and bool(self.bf & COMBO_PAYOFF))

    # ---- one turn -------------------------------------------------------------
    def turn(self, T):
        g = self.g
        chip = self.opp_draw_rate()                  # opp draw steps feed punishers
        if chip:
            self.tbl.hit_all(chip, T)
        if self.tbl.done:
            return
        self.opp_hand = min(self.opp_hand + 1, 7)
        g.begin_turn(T)
        pre = {nm for nm in g.rocks if g.has(nm)}
        g.deploy_rocks()
        for nm in pre:
            if not g.has(nm):
                self.deployed.add(nm)
                self.rock_count += 1
        arch_used = False

        progress = True
        while progress:
            progress = False
            # punishers first (cheapest first)
            for nm, c in sorted(PUNISHER_COSTS.items(), key=lambda x: x[1]):
                if nm not in self.bf and g.has(nm) and g.avail >= c:
                    g.cast(nm, c)
                    self.bf.add(nm)
                    progress = True
            # combo creatures + Kefka + Bolas Ravager + Magus + Archivist (bodies)
            for nm, c in COMBO_CREATURES.items():
                if nm not in self.bf and g.has(nm) and g.avail >= c:
                    g.cast(nm, c)
                    self.bf.add(nm)
                    progress = True
            if not self.kefka and g.avail >= 5:
                g.avail -= 5
                self.kefka = True
                self.kefka_turn = T
                self.bf.add("Kefka, Court Mage")
                progress = True
                if self.opp_hand >= 1:
                    per = self.opp_discard_rate() * self.mult()
                    if per:
                        self.tbl.hit_all(per, T)
                    self.opp_hand -= 1
                g.draw(3)
            if not self.bolas and g.has("Nicol Bolas, the Ravager") and g.avail >= 4:
                g.cast("Nicol Bolas, the Ravager", 4)
                self.bolas = True
                progress = True
                if self.opp_hand >= 1:
                    per = self.opp_discard_rate() * self.mult()
                    if per:
                        self.tbl.hit_all(per, T)
                    self.opp_hand -= 1
            if not self.magus and g.has("Magus of the Wheel") and g.avail >= 3:
                g.cast("Magus of the Wheel", 3)
                self.magus = True
                progress = True
            if self.archivist is None and g.has("Jace's Archivist") and g.avail >= 2:
                g.cast("Jace's Archivist", 2)
                self.archivist = T
                progress = True
            # combo check — assembled in play = win this turn
            if self.combo_online():
                self.tbl.kill_all(T)
                return
            # Peer into the Abyss lines
            if g.has("Peer into the Abyss") and g.avail >= 7:
                if "Notion Thief" in self.bf and (self.bf & set(YOUR_DRAW_ALL)):
                    g.cast("Peer into the Abyss", 7)
                    self.tbl.hit_all(30 * self.mult(), T)
                    g.draw(10)
                    progress = True
                elif self.opp_draw_rate() >= 1:
                    g.cast("Peer into the Abyss", 7)
                    self.tbl.hit_focus(40, T)
                    progress = True
            # wheels — when they hurt, or when the hand is spent. Lethal-or-bust:
            # never spin on <2 punishers (a half-loaded wheel refuels the pod)
            # (2026-07-02 audit).
            worth = self.wheel_worth()
            if (worth >= 4 or len(g.hand) <= 2) and self.n_punishers() >= 2:
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
                elif (self.archivist is not None and T > self.archivist
                      and not arch_used and worth >= 4):
                    arch_used = True                 # free repeatable wheel
                    self.fire_wheel("Jace's Archivist", 0, T)
                    progress = True
                elif self.magus and g.avail >= 2 and worth >= 8:
                    self.magus = False
                    self.fire_wheel("Magus of the Wheel", 2, T)
                    progress = True
                elif cheapest:
                    self.fire_wheel(*cheapest, T)
                    progress = True
            # tutors -> missing punisher, then a wheel; Final Parting bins Echo
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
                    if tgt is None:
                        for cand in WHEELS:
                            if not g.has(cand) and any(
                                    g.deck[i][0] == cand
                                    for i in range(g.ptr, len(g.deck))):
                                tgt = cand
                                break
                    if tgt:
                        g.cast(tut, c)
                        g.fetch(tgt)
                        if tut == "Final Parting" and any(
                                g.deck[i][0] == "Echo of Eons"
                                for i in range(g.ptr, len(g.deck))):
                            g.fetch("Echo of Eons")
                            g.discard("Echo of Eons")
                            self.echo_yard = True
                        progress = True
                        break
            if self.tbl.done:
                return

        # Kefka attacks: trigger + 4 combat. Kefka (4/5) has no native haste, so
        # he cannot attack the turn he lands — gate on T > cast turn (2026-07-02
        # audit; Greaves/Boots haste line is unmodelled, i.e. conservative).
        if self.kefka and T > self.kefka_turn:
            if self.opp_hand >= 1:
                per = self.opp_discard_rate() * self.mult()
                if per:
                    self.tbl.hit_all(per, T)
                self.opp_hand -= 1
                g.draw(2)
            self.tbl.hit_focus(4, T)


def _run(index, aliases, trials, combo):
    rng = random.Random(SEED)
    library, commander = slc.load_parsed(DECK, index, aliases)
    res = slc.run_goldfish(lambda: Trial(library, rng, combo=combo), trials, TURNS)
    return res, library, commander


def mode_clock(index, aliases, trials):
    print("=" * 72)
    print(f"CLOCK — Forced Liquidation (Kefka-burn + Kitten combo) kill-turn "
          f"goldfish ({trials} trials, seed {SEED})")
    print("=" * 72)
    res_on, library, commander = _run(index, aliases, trials, combo=True)
    print(f"  library {len(library)} + commander {commander}\n")
    print("  --- COMBO ON (burn + Kitten/Channeler combo) ---")
    slc.report_clock(res_on, SHOW, TURNS, trials)
    res_off, _, _ = _run(index, aliases, trials, combo=False)
    print("\n  --- COMBO OFF (burn axis only — baseline) ---")
    slc.report_clock(res_off, SHOW, TURNS, trials)
    md_on, md_off = slc.median(res_on, 1), slc.median(res_off, 1)
    print(f"\n  DELTA (combo's contribution): table median {md_off} -> {md_on}")
    print("  Proposal ceiling ~17/20; brief bar is T6-7. Both clocks stated per "
          "the verification rule.")


if __name__ == "__main__":
    slc.run_cli(__doc__, {"clock": mode_clock})
