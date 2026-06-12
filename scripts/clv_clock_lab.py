#!/usr/bin/env python3
"""clv_clock_lab.py — Clive, Ifrit's Dominant (EXTERNAL build) KILL-TURN goldfish.

Stage 3 of the 2026-06-12 candidate bake-off. Deck:
decks/considering/clive-external-20260612.txt (extracted verbatim from
proposals/Clive_External_Build.md; 5 reskin aliases resolve via
REF_Reskin_Aliases.md — Storm's Will = Jeska's Will etc.). Built on
speed_lab_core.py; shares the mono-red rock/ritual conventions with
godo_clock_lab.py.

THE KILL IS A DISCARD-BURN ENGINE, all damage hits EVERY opponent, so decap
and table CONVERGE structurally. Rules facts encoded (card_lookup.py
2026-06-12):

  * Clive {4}{R}{R} 5/5: ETB MAY discard your hand, draw = devotion to red.
    Devotion = {R} pips among permanents you control (tracked per card from
    the raw oracle mana costs; Clive himself counts 2).
  * Per-CARD discard payoffs (fire once per card discarded, to each opponent):
    Brallin +1, Glint-Horn Buccaneer +1, Cool but Rude lvl2 +2 (2 mana to
    level, modelled when spare). Magmakin Artillerist: once per discard EVENT,
    damage = number of cards. Monument to Endurance: 3 life loss, once/turn
    (life loss, NOT damage -> not doubled).
  * Doublers multiply damage (not Monument's life loss): Solphim (noncombat),
    Twinflame Tyrant (any), Gratuitous Violence (creature damage — all the
    payoff sources are creatures). Multiplier = 2^(count on bf).
  * Fanatic of Mogis ETB: devotion damage to each opponent (doubled).
  * Wheels/dump spells (cost, kind): Wheel of Fortune 3, Reforge the Soul 5,
    Decaying Time Loop 4 (dump hand, draw same), Path of the Pyromancer 5
    (dump, +{R} per discarded, draw +1), Brass's Tunnel-Grinder 3 /
    Cavalier of Flame 5 (ETB dump any number, draw that many).
  * Orthion {6}{R}{R}{R}+tap: FIVE temporary Clive copies — five sequential
    hand-dump ETBs, each redrawing devotion. Modelled when Clive on bf.
  * Neheb, the Eternal: postcombat main adds {R} per 1 life opponents lost
    this turn (all three summed) — the engine's storm enabler; modelled as
    extra mana after the first damage pass, capped at 18.
  * Jeska's Will: +5 mana with commander (opponent-hand approximation).

MANA: lands + rocks floor; Throne of Eldraine (5,4 — mono-red), Sceptre of
Eternal Glory (4,3 once 3+ same-name lands — 27 Mountains), Ruby Medallion /
The Fire Crystal approximated as (cost,1) rocks. OMITTED (conservative):
The One Ring, Underworld Breach storm turns, Birgi chains, Runaway Steam-Kin
ritual, Feldon (yard-dependent), Brash Taunter fight line, Sunspine Lynx ETB,
combat except the standing board's focus swing. Twinflame / Molten
Duplication / Cursed Mirror / Devastating Onslaught (X=1) ARE modelled as
one extra Clive ETB dump each (the primer's line 3).
OPTIMISTIC: opponents' hands ignored, rocks repeat, colour-blind mana.

Data: collection/oracle-cards.json (refreshed 2026-06-12)
Writeup: proposals/Candidate_Bakeoff_2026-06-12.md (Stage 3)
"""
import importlib.util
import json
import random
from pathlib import Path

ROOT = Path(__file__).parent.parent
_spec = importlib.util.spec_from_file_location(
    "speed_lab_core", Path(__file__).parent / "speed_lab_core.py")
slc = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(slc)
ds = slc.ds

DECK = ROOT / "decks" / "considering" / "clive-external-20260612.txt"
SEED = 20260612
TURNS = 12
SHOW = [4, 5, 6, 7, 8, 9, 10, 12]

ROCKS = {"Sol Ring": (1, 2), "Arcane Signet": (2, 1), "Thought Vessel": (2, 1),
         "Ruby Medallion": (2, 1), "The Fire Crystal": (4, 1),
         "Sceptre of Eternal Glory": (4, 3), "Throne of Eldraine": (5, 4)}

# per-card / per-event discard payoffs: name -> cast cost
PAYOFF = {"Brallin, Skyshark Rider": 4, "Glint-Horn Buccaneer": 3,
          "Magmakin Artillerist": 3, "Monument to Endurance": 3,
          "Surly Badgersaur": 4, "Containment Construct": 2}
DOUBLER = {"Solphim, Mayhem Dominus": 4, "Twinflame Tyrant": 5,
           "Gratuitous Violence": 5}
# devotion bodies worth pre-Clive deployment (cost; pips come from oracle)
BODIES = {"Birgi, God of Storytelling": 3, "Runaway Steam-Kin": 2,
          "Defiler of Instinct": 4, "Neheb, the Eternal": 5,
          "Razorkin Needlehead": 2, "Terror of the Peaks": 5,
          "Neheb, Dreadhorde Champion": 4, "Enduring Courage": 4,
          "Feldon of the Third Path": 3, "Brash Taunter": 5,
          "Sunspine Lynx": 4, "Cavalier of Flame": 5,
          "Hexing Squelcher": 2, "Tannuk, Steadfast Second": 4}
WHEELS = {"Wheel of Fortune": 3, "Reforge the Soul": 5,
          "Decaying Time Loop": 4, "Path of the Pyromancer": 5}
DUMPERS = {"Brass's Tunnel-Grinder": 3, "Cavalier of Flame": 5}


def load_pips(names):
    with (ROOT / "collection" / "oracle-cards.json").open(encoding="utf-8") as f:
        cards = json.load(f)
    want = {n.lower() for n in names}
    out = {}
    for c in cards:
        k = c.get("name", "").lower()
        mc = c.get("mana_cost")
        if mc is None and c.get("card_faces"):
            mc = c["card_faces"][0].get("mana_cost", "")
        if k in want and k not in out:
            out[k] = (mc or "").count("{R}")
        for face in c.get("card_faces") or []:
            fk = face.get("name", "").lower()
            if fk in want and fk not in out:
                out[fk] = (face.get("mana_cost") or "").count("{R}")
    return out


class Trial:
    def __init__(self, library, rng, pips, powmap):
        self.g = slc.Goldfish(library, rng, rocks=ROCKS)
        self.tbl = slc.Table()
        self.pips = pips
        self.powmap = powmap
        self.bf = set()
        self.devotion = 0
        self.clive = False
        self.cbr_level = False        # Cool but Rude levelled to 2
        self.monument_used = False
        self.board_pow = 0            # standing power (attacks from next turn)
        self.new_pow = 0
        self.dealt = 0                # opponent life lost this turn (x3 summed)
        self.neheb_paid = False

    def mult(self):
        return 2 ** sum(1 for d in DOUBLER if d in self.bf)

    def per_card(self):
        r = 0
        if "Brallin, Skyshark Rider" in self.bf:
            r += 1
        if "Glint-Horn Buccaneer" in self.bf:
            r += 1
        if "Cool but Rude" in self.bf and self.cbr_level:
            r += 2
        return r

    def dump(self, n, T):
        """Discard n cards with payoffs live. Damage to EVERY opponent."""
        if n <= 0:
            return
        dmg = n * self.per_card()
        if "Magmakin Artillerist" in self.bf:
            dmg += n
        dmg *= self.mult()
        loss = 0
        if "Monument to Endurance" in self.bf and not self.monument_used:
            loss = 3
            self.monument_used = True
        total = dmg + loss
        if total:
            self.tbl.hit_all(total, T)
            self.dealt += 3 * total

    def deploy(self, nm, cost):
        if self.g.cast(nm, cost):
            self.bf.add(nm)
            self.devotion += self.pips.get(nm.lower(), 0)
            self.new_pow += self.powmap.get(nm.lower(), 0) or 0
            return True
        return False

    def clive_etb(self, T):
        g = self.g
        h = len(g.hand)
        for _ in range(h):                      # dump whole hand
            g.yard.append(g.hand.pop())
        self.dump(h, T)
        g.draw(self.devotion)

    def turn(self, T):
        g = self.g
        self.board_pow += self.new_pow
        self.new_pow = 0
        self.monument_used = False
        self.dealt = 0
        self.neheb_paid = False
        g.begin_turn(T)
        g.deploy_rocks()
        if g.has("Jeska's Will") and g.avail >= 3:
            g.cast("Jeska's Will", 3)
            g.add_mana(5)

        # standing board swings (focus-fire, unblocked)
        if self.board_pow > 0:
            self.tbl.hit_focus(self.board_pow * (2 if
                "Gratuitous Violence" in self.bf else 1), T)
            self.dealt += self.board_pow
        if self.tbl.done:
            return

        progress = True
        while progress:
            progress = False
            # payoffs and doublers first — they make every later dump lethal
            for nm, c in list(PAYOFF.items()) + list(DOUBLER.items()):
                if nm not in self.bf and g.has(nm) and g.avail >= c:
                    if nm == "Cavalier of Flame":
                        continue                  # handled as dumper
                    self.deploy(nm, c)
                    progress = True
            if "Cool but Rude" in self.bf and not self.cbr_level and g.avail >= 2:
                g.avail -= 2
                self.cbr_level = True
                progress = True
            if not self.cbr_level and g.has("Cool but Rude") and g.avail >= 2:
                self.deploy("Cool but Rude", 2)
                progress = True
            # Clive
            if not self.clive and g.avail >= 6:
                g.avail -= 6
                self.clive = True
                self.bf.add("Clive, Ifrit's Dominant")
                self.devotion += 2
                self.new_pow += 5
                self.clive_etb(T)
                progress = True
            # Fanatic of Mogis: devotion nuke
            if g.has("Fanatic of Mogis") and g.avail >= 4:
                g.cast("Fanatic of Mogis", 4)
                self.devotion += 1
                self.new_pow += 4
                dmg = (self.devotion) * self.mult()
                self.tbl.hit_all(dmg, T)
                self.dealt += 3 * dmg
                progress = True
            # wheels / dumpers when a payoff is live (or hand is spent)
            if self.per_card() or "Magmakin Artillerist" in self.bf \
                    or len(g.hand) <= 2:
                for nm, c in {**WHEELS, **DUMPERS}.items():
                    if g.has(nm) and g.avail >= c:
                        g.cast(nm, c)
                        h = len(g.hand)
                        for _ in range(h):
                            g.yard.append(g.hand.pop())
                        self.dump(h, T)
                        if nm == "Path of the Pyromancer":
                            g.add_mana(h)
                            g.draw(h + 1)
                        elif nm in DUMPERS:
                            g.draw(h + 1)
                            if nm == "Cavalier of Flame":
                                self.bf.add(nm)
                                self.devotion += self.pips.get(nm.lower(), 0)
                                self.new_pow += 6
                        else:
                            g.draw(7)
                        progress = True
                        break
            # small Clive-copy lines: one extra ETB dump each (primer line 3)
            if self.clive:
                for nm, c in (("Twinflame", 2), ("Molten Duplication", 2),
                              ("Cursed Mirror", 3), ("Devastating Onslaught", 3)):
                    if g.has(nm) and g.avail >= c:
                        g.cast(nm, c)
                        h = len(g.hand)
                        for _ in range(h):
                            g.yard.append(g.hand.pop())
                        self.dump(h, T)
                        g.draw(self.devotion)
                        progress = True
                        break
            # Orthion x5 Clive copies: five sequential dumps
            if self.clive and g.has("Orthion, Hero of Lavabrink") \
                    and g.avail >= 4 + 9:
                g.cast("Orthion, Hero of Lavabrink", 4)
                g.avail -= 9
                for _ in range(5):
                    h = len(g.hand)
                    for _ in range(h):
                        g.yard.append(g.hand.pop())
                    self.dump(h, T)
                    g.draw(self.devotion)
                progress = True
            # devotion bodies, cheapest first
            for nm, c in sorted(BODIES.items(), key=lambda x: x[1]):
                if nm not in self.bf and g.has(nm) and g.avail >= c:
                    self.deploy(nm, c)
                    progress = True
                    break
            # Neheb postcombat mana once damage landed
            if "Neheb, the Eternal" in self.bf and self.dealt > 0 \
                    and not self.neheb_paid:
                g.add_mana(min(self.dealt, 18))
                self.neheb_paid = True
                progress = True
            if self.tbl.done:
                return


def goldfish(library, trials, rng, pips, powmap):
    out = []
    for _ in range(trials):
        tr = Trial(library, rng, pips, powmap)
        for T in range(1, TURNS + 1):
            tr.turn(T)
            if tr.tbl.done:
                break
        out.append((tr.tbl.decap, tr.tbl.table))
    return out


def mode_clock(index, aliases, trials):
    print("=" * 72)
    print(f"CLOCK — Clive (external) kill-turn goldfish "
          f"({trials} trials, seed {SEED})")
    print("=" * 72)
    rng = random.Random(SEED)
    library, commander = slc.load_parsed(DECK, index, aliases)
    names = [nm for nm, _ in library] + [commander]
    pips = load_pips(names)
    raw_pow = slc.load_powers(names)
    powmap = {k: (v if isinstance(v, int) else 0) for k, v in raw_pow.items()}
    print(f"  library {len(library)} + commander {commander}")
    print("  turns:".ljust(44) + "".join(f"{t:6d}" for t in SHOW))
    res = goldfish(library, trials, rng, pips, powmap)
    print(slc.row("decap (one opponent, cum %)", slc.cum(res, 0, SHOW), SHOW))
    print(slc.row("table (all three, cum %)", slc.cum(res, 1, SHOW), SHOW))
    nv_d = 100.0 * sum(1 for d, _ in res if d is None) / trials
    nv_t = 100.0 * sum(1 for _, t in res if t is None) / trials
    print(f"\n  median decap {slc.median(res, 0)} / table {slc.median(res, 1)}"
          f"   ·   never-in-{TURNS}: decap {nv_d:.0f}% / table {nv_t:.0f}%")
    print("\n  External primer makes no turn claim; this calibrates the T6-7 brief bar.")


if __name__ == "__main__":
    slc.run_cli(__doc__, {"clock": mode_clock})
