#!/usr/bin/env python3
"""yrk_clock_lab.py — Insider Trading (Yuriko, the Tiger's Shadow) KILL-TURN goldfish.

Stage 3 of the 2026-06-12 candidate bake-off. Deck:
decks/considering/insider-trading-20260612.txt. Built on speed_lab_core.py.
The proposal's GATE (memory 2026-06-11): build only if the lab shows ~T7
median — this lab is that gate.

TWO KILL AXES (oracle-verified 2026-06-12):

  CHIP — Yuriko's trigger: whenever a NINJA you control deals combat damage
  to a player, reveal the top card, EACH OPPONENT loses its mana value, the
  card goes to your hand. One trigger PER ninja connecting. Drains hit all
  three opponents (Genome shape — the converging clock); the combat damage
  itself is focus-fire. Modelled honestly: the reveal is the ACTUAL next
  library card's MV and it is drawn. Top-stack policies: Scroll Rack ({1},
  put the biggest hand card >=MV5 on top — Draco 16 / Blinkmoth Infusion 14
  / Treasure Cruise 8...), Sensei's Top (reorder top 3, biggest first),
  Mystical Tutor at 1 spare mana (biggest I/S to top when no combo hunt).
  Ninjutsu: evaders (Slither Blade class, power 1) attack unblocked
  (goldfish convention; they're printed-unblockable, the deck's real-table
  edge), each can be swapped for a hand ninja at its REAL ninjutsu cost
  (Moon-Circuit/Mistblade 1, Deep Hours/Ingenious/Prosperous/Dokuchi/
  Silver-Fur 2, Naga 3, Fallen Shinobi/Thousand-Faced 4); the returned
  evader recasts post-combat for 1. Yuriko enters via commander ninjutsu
  {U}{B} off the first unblocked attacker. Deep Hours/Ingenious/Moon-Circuit
  hits draw +1 (capped 2/turn).

  COMBO — Thassa's Oracle ({U}{U}) + Demonic Consultation ({B}, name a card
  not in the 92-card rest -> library exiled) or Tainted Pact ({1}{B}, strict
  name-singleton holds incl. uniquely-named basics — verified Stage 2) =
  kill_all. Backups at +1 mana for a cantrip-draw: Jace WoM (4), Lab Maniac
  (3). Tutors: Mystical (1, to top -> next turn), Demonic (2), Wishclaw
  (cast 2 + {1} activate), Solve the Equation (3). Mana is the colour-blind
  lands+rocks floor (Sol Ring/Signets/Talisman/Lotus Petal banked 1).

OMITTED (conservative): Kaito, Sakashima's Student copying, Thousand-Faced
token, Mist-Syndicate copies, Fallen Shinobi free-casts, Lim-Dûl's Vault
stacking, snow/utility land minutiae, all counterspell protection.
OPTIMISTIC: every attacker is unblocked (printed evasion makes this the
deck's actual plan, but blockers/removal exist), mana colour-blind. Decap =
combat focus + drains; table = drains/combo. Trust shapes and deltas.

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

DECK = ROOT / "decks" / "considering" / "insider-trading-20260612.txt"
SEED = 20260612
TURNS = 12
SHOW = [3, 4, 5, 6, 7, 8, 9, 10, 12]

ROCKS = {"Sol Ring": (1, 2), "Arcane Signet": (2, 1), "Dimir Signet": (2, 1),
         "Talisman of Dominance": (2, 1)}
EVADERS = {"Changeling Outcast": 1, "Slither Blade": 1,
           "Triton Shorestalker": 1, "Mist-Cloaked Herald": 1,
           "Gingerbrute": 1, "Spectral Sailor": 1, "Faerie Seer": 1,
           "Wingcrafter": 1, "Mothdust Changeling": 1,
           "Universal Automaton": 1, "Looter il-Kor": 2,
           "Dimir Infiltrator": 2, "Baleful Strix": 2, "Tetsuko Umezawa, Fugitive": 2}
# ninja -> (ninjutsu cost, draws_on_hit)
NINJAS = {"Moon-Circuit Hacker": (1, 1), "Mistblade Shinobi": (1, 0),
          "Ninja of the Deep Hours": (2, 1), "Ingenious Infiltrator": (2, 1),
          "Prosperous Thief": (2, 0), "Dokuchi Silencer": (2, 0),
          "Silver-Fur Master": (2, 0), "Mist-Syndicate Naga": (3, 0),
          "Sakashima's Student": (2, 0), "Thousand-Faced Shadow": (4, 0),
          "Fallen Shinobi": (4, 0)}
ORACLES = {"Thassa's Oracle": 2, "Laboratory Maniac": 4,
           "Jace, Wielder of Mysteries": 5}     # +1 already folded for cantrip
EXILERS = {"Demonic Consultation": 1, "Tainted Pact": 2}
CANTRIPS = {"Brainstorm": 1, "Ponder": 1, "Preordain": 1, "Opt": 1,
            "Frantic Search": 3}


class Trial:
    def __init__(self, library, rng, powmap):
        self.g = slc.Goldfish(library, rng, rocks=ROCKS)
        self.tbl = slc.Table()
        self.powmap = powmap
        self.evaders = 0           # attackers from previous turns
        self.evaders_new = 0
        self.ninjas = []           # (name, power, draw) on bf
        self.yuriko = False
        self.scroll = False
        self.top = False
        self.pending_top = []
        self.petal = 0

    def combo_check(self, T):
        g = self.g
        for o, oc in ORACLES.items():
            if not g.has(o):
                continue
            for e, ec in EXILERS.items():
                if g.has(e) and g.avail + self.petal >= oc + ec:
                    spend = oc + ec - g.avail
                    if spend > 0:
                        self.petal -= spend
                        g.add_mana(spend)
                    g.cast(o, oc) and g.cast(e, ec)
                    self.tbl.kill_all(T)
                    return True
        return False

    def combo_tutor(self):
        g = self.g
        have_o = any(g.has(o) for o in ORACLES)
        have_e = any(g.has(e) for e in EXILERS)
        if have_o and have_e:
            return False
        tgt = "Thassa's Oracle" if not have_o else "Demonic Consultation"
        if not any(g.deck[i][0] == tgt for i in range(g.ptr, len(g.deck))):
            tgt = "Tainted Pact" if tgt == "Demonic Consultation" else tgt
        for tut, c, how in (("Mystical Tutor", 1, "top"),
                            ("Demonic Tutor", 2, "hand"),
                            ("Wishclaw Talisman", 3, "hand"),
                            ("Solve the Equation", 3, "hand")):
            if tut == "Mystical Tutor" and tgt == "Thassa's Oracle":
                continue                      # creature — Mystical can't
            if g.has(tut) and g.avail >= c \
                    and any(g.deck[i][0] == tgt
                            for i in range(g.ptr, len(g.deck))):
                g.cast(tut, c)
                if how == "top":
                    self.pending_top.append(tgt)
                else:
                    g.fetch(tgt)
                return True
        return False

    def stack_top(self):
        """Scroll Rack / Top: push the biggest reveal up front."""
        g = self.g
        if self.scroll and g.avail >= 1:
            i_best, mv_best = None, 4
            for i, (nm, rec) in enumerate(g.hand):
                if rec["cmc"] > mv_best and not ds.is_land(rec):
                    i_best, mv_best = i, rec["cmc"]
            if i_best is not None:
                g.avail -= 1
                g.deck.insert(g.ptr, g.hand.pop(i_best))
                return
        if self.top and g.ptr + 3 <= len(g.deck):
            window = g.deck[g.ptr:g.ptr + 3]
            best = max(range(3), key=lambda i: window[i][1]["cmc"])
            if best:
                g.deck[g.ptr], g.deck[g.ptr + best] = \
                    g.deck[g.ptr + best], g.deck[g.ptr]

    def turn(self, T):
        g = self.g
        self.evaders += self.evaders_new
        self.evaders_new = 0
        g.begin_turn(T)
        for nm in self.pending_top:
            g.fetch(nm)
        self.pending_top = []
        g.deploy_rocks()
        while g.has("Lotus Petal"):
            g.hand.pop(g.in_hand("Lotus Petal"))
            self.petal += 1

        if self.combo_check(T):
            return

        # ---- combat ----------------------------------------------------------
        attackers = self.evaders + len(self.ninjas) + (1 if self.yuriko else 0)
        free_evaders = self.evaders          # can carry a ninjutsu swap each
        hits = []                            # (power, draws) per connecting body
        # Yuriko via commander ninjutsu off the first evader
        if not self.yuriko and free_evaders >= 1 and g.avail >= 2:
            g.avail -= 2
            self.yuriko = True
            free_evaders -= 1
            self.evaders -= 1                # she replaces that attacker
            hits.append((1, 0))              # Yuriko 1/3 connects
        elif self.yuriko and attackers:
            hits.append((1, 0))
        # hand ninjas in via ninjutsu, cheap first
        for nm, (nc, dr) in sorted(NINJAS.items(), key=lambda x: x[1][0]):
            if free_evaders < 1:
                break
            if g.has(nm) and g.avail >= nc + 1:     # +1 to recast the evader
                g.avail -= nc + 1
                g.hand.pop(g.in_hand(nm))
                pw = self.powmap.get(nm.lower(), 1) or 1
                self.ninjas.append((nm, pw, dr))
                free_evaders -= 1
                hits.append((pw, dr))
        # every ninja on bf (incl. the ones that just flipped in) connects once
        ninja_hits = len(self.ninjas) + (1 if self.yuriko else 0)
        combat_pow = sum(p for _, p, _ in self.ninjas) \
            + free_evaders + (1 if self.yuriko else 0)
        draws = min(2, sum(d for _, _, d in self.ninjas))
        if self.yuriko and ninja_hits:
            self.stack_top()
            drained = 0
            for _ in range(ninja_hits):
                if g.ptr < len(g.deck):
                    drained += g.deck[g.ptr][1]["cmc"]
                    g.draw(1)
            if drained:
                self.tbl.hit_all(int(drained), T)
        if combat_pow:
            self.tbl.hit_focus(combat_pow, T)
        if draws:
            g.draw(draws)
        if self.tbl.done:
            return

        # ---- second main -----------------------------------------------------
        if self.combo_check(T):
            return
        progress = True
        while progress:
            progress = False
            for nm, c in EVADERS.items():
                if g.has(nm) and g.avail >= c:
                    g.cast(nm, c)
                    self.evaders_new += 1
                    if nm == "Baleful Strix":
                        g.draw(1)
                    progress = True
                    break
            for nm, c, attr in (("Scroll Rack", 2, "scroll"),
                                ("Sensei's Divining Top", 1, "top")):
                if not getattr(self, attr) and g.has(nm) and g.avail >= c:
                    g.cast(nm, c)
                    setattr(self, attr, True)
                    progress = True
            if self.combo_tutor():
                progress = True
            for nm, c in CANTRIPS.items():
                if g.has(nm) and g.avail >= c:
                    g.cast(nm, c)
                    g.draw(1)
                    progress = True
                    break
        if self.combo_check(T):
            return


def goldfish(library, trials, rng, powmap):
    out = []
    for _ in range(trials):
        tr = Trial(library, rng, powmap)
        for T in range(1, TURNS + 1):
            tr.turn(T)
            if tr.tbl.done:
                break
        out.append((tr.tbl.decap, tr.tbl.table))
    return out


def mode_clock(index, aliases, trials):
    print("=" * 72)
    print(f"CLOCK — Insider Trading (Yuriko) kill-turn goldfish "
          f"({trials} trials, seed {SEED})")
    print("=" * 72)
    rng = random.Random(SEED)
    library, commander = slc.load_parsed(DECK, index, aliases)
    names = [nm for nm, _ in library] + [commander]
    raw_pow = slc.load_powers(names)
    powmap = {k: (v if isinstance(v, int) else 1) for k, v in raw_pow.items()}
    print(f"  library {len(library)} + commander {commander}")
    print("  turns:".ljust(44) + "".join(f"{t:6d}" for t in SHOW))
    res = goldfish(library, trials, rng, powmap)
    print(slc.row("decap (one opponent, cum %)", slc.cum(res, 0, SHOW), SHOW))
    print(slc.row("table (all three, cum %)", slc.cum(res, 1, SHOW), SHOW))
    nv_d = 100.0 * sum(1 for d, _ in res if d is None) / trials
    nv_t = 100.0 * sum(1 for _, t in res if t is None) / trials
    print(f"\n  median decap {slc.median(res, 0)} / table {slc.median(res, 1)}"
          f"   ·   never-in-{TURNS}: decap {nv_d:.0f}% / table {nv_t:.0f}%")
    print("\n  GATE (proposal 2026-06-11): build requires ~T7 median. This is the gate.")


if __name__ == "__main__":
    slc.run_cli(__doc__, {"clock": mode_clock})
