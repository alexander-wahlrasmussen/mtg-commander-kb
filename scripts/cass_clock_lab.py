#!/usr/bin/env python3
"""cass_clock_lab.py — COMBO-ASSEMBLY kill-turn goldfish for the external budget
"Cass, Hand of Vengeance" deck (decks/considering/cass-budget-combo-20260701.txt).

  >>> This REPLACES the original voltron model (2026-07-01, same day). That model
  >>> clocked the deck as a fair aura-beatdown (swing one carrier for 40, decap
  >>> median T13) and was measuring the WRONG DECK. The source video ("Reminder
  >>> Text — Nobody Plays This Deck, but it Wins on Turn 4 for $23", user-confirmed
  >>> 2026-07-01) presents an INFINITE-DAMAGE COMBO, not voltron. This lab models
  >>> that combo's ASSEMBLY turn instead. <<<

THE COMBO (every card card_lookup-verified 2026-07-01 — CLAUDE.md hard rule;
cross-checked vs Commander Spellbook via scripts/find_combos.py):

  Cass, Hand of Vengeance {2}{R}{W}, 4/4: "Whenever Cass or another creature you
  control dies, if it was enchanted or equipped, return any number of Aura cards
  attached to it from your graveyard to the battlefield attached to TARGET creature,
  then attach any Equipment that were attached to it to that creature."

  Loop = Cass in play + a TOKEN-ENGINE + a free SAC-PING outlet:
   1. A creature carries the token-engine aura + the sac-ping equipment.
   2. Sacrifice it to the ping for 1 damage.
   3. It died enchanted/equipped -> Cass returns the aura + re-attaches the equipment
      onto another creature; the token-engine spits out a fresh creature token (the
      body for the next iteration).
   4. Repeat -> infinite 1-damage pings -> the WHOLE TABLE dies at once.

  TOKEN-ENGINES (make a creature token each loop so it self-sustains):
    self-sufficient (an Aura that IS the token source):
      Griffin Guide {2}{W}   — "when enchanted creature dies, make a 2/2 Griffin"
      Murder Investigation {1}{W} — "...make X 1/1 Soldiers, X = its power" (needs the
        dying creature's power >=1; true after the first Griffin/real carrier — a
        documented minor optimism)
    needs a separate returnable Aura (a creature whose token triggers on enchantment ETB):
      Archon of Sun's Grace {2}{W}{W} — Constellation: enchantment ETB -> 2/2 Pegasus
      Ghostly Dancers {3}{W}{W}       — Eerie: enchantment ETB -> 3/1 Spirit
      (each loop Cass RE-ENTERS an aura, which is the enchantment-ETB that fires these)

  SAC-PING OUTLETS (free "Sacrifice ...: 1 damage" that also IS the payoff):
    Mask of Immolation {1}{R} — makes its own 1/1 Elemental on ETB (a ready carrier),
      "Equipped creature has 'Sacrifice this creature: 1 damage to any target.'"
    Mortarpod {2} — Living weapon (own 0/0 Germ carrier), same sac-ping.
    Cass re-attaches these Equipment each loop, so they are self-contained kills —
    the deck needs NO Goblin Bombardment / Ashnod's Altar (those are the video's
    "you could also add..." upgrades; measured in mode_levers).

  find_combos reports 0 COMPLETE combos only because CSB keys the Cass line on a
  dedicated free sac outlet (Goblin Bombardment/Blasting Station/Ashnod's Altar); the
  deck's Mask/Mortarpod build is the same loop via a card CSB doesn't index for Cass.
  The infinite is real and self-contained.

DIG (why it is fast for a no-ramp budget deck) — all verified:
  aura/equipment TUTORS: Heliod's Pilgrim {2}{W} (ETB->Aura to hand),
    Open the Armory {1}{W} (Aura OR Equipment to hand — the ONLY tutor that finds an
    outlet), Moon-Blessed Cleric {2}{W} (ETB->enchantment to TOP; next draw).
  cast-an-aura DRAW ENGINES (+1 card each, per qualifying cast): Kor Spiritdancer,
    Mesa Enchantress, Pearl-Ear (auras) · Sram, Armory Paladin (auras AND equipment).
    Pearl-Ear also gives enchantments AFFINITY FOR AURAS (each aura you control makes
    the next aura cost {1} less) — modelled as a discount.
  The deck is ~40% auras; casting cheap filler auras under a draw-engine digs toward
  the combo. Modelled generically: a "generic aura" (type_line has Aura, not a named
  engine) has no encoded effect EXCEPT triggering the verified draw engines — so no
  card text is invented.

MANA: colour-blind lands-only floor. This deck runs ZERO artifact ramp (budget), so
ROCKS = {} — the clock is gated by raw land count + finding the pieces, which is honest.

OPTIMISTIC (this is a CEILING, read as such): NO removal (one kill spell on Cass stops
the engine — the archetype's whole weakness, invisible here), NO counters, NO blockers;
a carrier creature is always assumed present (Cass + the outlet's own token guarantee it);
mana is colour-blind; Pearl-Ear/affinity discounts simplified. CONSERVATIVE / OMITTED:
only the 5 named draw engines + 3 tutors dig (the deck's cantrip auras Angelic Gift/
Feather of Flight/etc. draw on their own and are NOT modelled), and non-engine creatures
aren't cast — so the true assembly is, if anything, a touch faster than stated. Trust
shapes and deltas, not second decimals — same caveats as every lab in this repo.

Data: collection/oracle-cards.json (refresh via update_scryfall_data.py)
Run:  python scripts/cass_clock_lab.py --trials 40000
"""
import importlib.util
import random
from pathlib import Path

ROOT = Path(__file__).parent.parent
_spec = importlib.util.spec_from_file_location(
    "speed_lab_core", Path(__file__).parent / "speed_lab_core.py")
slc = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(slc)
ds = slc.ds

# --- spec ------------------------------------------------------------------
DECK = ROOT / "decks" / "considering" / "cass-budget-combo-20260701.txt"
SEED = 20260701
TURNS = 14
SHOW = [4, 5, 6, 7, 8, 9, 10, 12]
ROCKS = {}                     # no artifact ramp in the budget list — lands-only floor
CASS_COST = 4                  # {2}{R}{W} from the command zone

# token-engines: name -> cast cost. Self-engines are auras that ARE the token source;
# aura-engines are creatures that need a separate returnable aura (auras >= 1).
SELF_ENGINES = {"Griffin Guide": 3, "Murder Investigation": 2}
AURA_ENGINES = {"Archon of Sun's Grace": 4, "Ghostly Dancers": 5}
# free sac-ping outlets (self-contained kill). Goblin Bombardment/Blasting Station are
# inert unless build_lib adds them (mode_levers) — recognised here so the lever needs no
# code change; they never fire in the baseline because g.has() is false.
OUTLETS = {"Mask of Immolation": 2, "Mortarpod": 2,
           "Goblin Bombardment": 2, "Blasting Station": 3}
# tutors: name -> (cost, kinds it fetches, to_hand?)
TUTORS = {"Open the Armory": (2, {"aura", "equip"}, True),
          "Heliod's Pilgrim": (3, {"aura"}, True),
          "Moon-Blessed Cleric": (3, {"aura"}, False)}     # to TOP, not hand
# cast-an-aura(/equip) draw engines: name -> (cost, triggers-on-equip-too?)
DRAW_ENGINES = {"Kor Spiritdancer": (2, False), "Sram, Senior Edificer": (2, True),
                "Mesa Enchantress": (3, False), "Armory Paladin": (3, True),
                "Pearl-Ear, Imperial Advisor": (3, False)}
PEARL = "Pearl-Ear, Imperial Advisor"
# creatures we explicitly cast (for the "a carrier exists" gate). The deck's other
# bodies are ignored (conservative).
CREATURE_CARDS = set(AURA_ENGINES) | set(TUTORS) | set(DRAW_ENGINES)


def is_aura(rec):
    return "Aura" in rec.get("type_line", "")


class Trial:
    def __init__(self, library, rng):
        self.g = slc.Goldfish(library, rng, rocks=ROCKS)
        self.tbl = slc.Table()
        self.cass = False
        self.creatures = 0            # bodies actually put down (carrier gate)
        self.auras = 0                # auras in play (Pearl-Ear discount + aura-engine fuel)
        self.self_engine = False      # Griffin Guide / Murder Investigation attached
        self.aura_engine = False      # Archon / Ghostly Dancers in play
        self.outlet = False           # a sac-ping in play
        self.draw_on = set()          # draw engines online
        self.tutored_top = None       # Moon-Blessed Cleric put a piece on top -> next draw

    # -- helpers -------------------------------------------------------------
    def lib_has(self, nm):
        g = self.g
        return any(g.deck[i][0] == nm for i in range(g.ptr, len(g.deck)))

    def aura_cost(self, base):
        """Pearl-Ear affinity: each aura you control shaves {1} (floor 1)."""
        return max(1, base - self.auras) if PEARL in self.draw_on else base

    def trigger_draw(self, equip=False):
        """Cast-an-aura/equipment draw engines: +1 card per qualifying engine online.
        Every engine draws on an aura cast; only Sram/Armory Paladin draw on equipment."""
        n = sum(1 for e in self.draw_on if (not equip) or DRAW_ENGINES[e][1])
        if n:
            self.g.draw(n)

    def combo_ready(self):
        return (self.cass and self.outlet
                and (self.self_engine or (self.aura_engine and self.auras >= 1)))

    def cast_creature(self, nm, cost):
        if self.g.cast(nm, cost):
            self.creatures += 1
            return True
        return False

    def cast_aura(self, nm, base_cost):
        """Cast an aura (needs a creature to enchant); bumps aura count, fires engines."""
        if self.creatures < 1:
            return False
        if self.g.cast(nm, self.aura_cost(base_cost)):
            self.auras += 1
            self.trigger_draw(equip=False)
            return True
        return False

    def do_tutors(self):
        """Cast a tutor to fetch the most-needed missing piece (outlet before engine —
        it is the scarcer slot)."""
        g = self.g
        need_outlet = not self.outlet
        need_engine = not (self.self_engine or self.aura_engine)
        if not (need_outlet or need_engine):
            return False
        for nm, (cost, kinds, to_hand) in TUTORS.items():
            if not g.has(nm) or g.avail < cost:
                continue
            target = None
            if need_outlet and "equip" in kinds:
                target = next((o for o in OUTLETS if self.lib_has(o)), None)
            if target is None and need_engine and "aura" in kinds:
                target = next((e for e in SELF_ENGINES if self.lib_has(e)), None)
            if target is None:
                continue
            ok = self.cast_creature(nm, cost) if nm in CREATURE_CARDS else g.cast(nm, cost)
            if not ok:
                continue
            if to_hand:
                g.fetch(target)
            else:
                self.tutored_top = target       # on top; arrives next draw
            return True
        return False

    def turn(self, T):
        g = self.g
        g.begin_turn(T)
        if self.tutored_top:
            # Moon-Blessed put it on top last turn; this turn's draw is it. It is the top
            # of the undrawn library — fetch it to hand to represent that draw.
            g.fetch(self.tutored_top); self.tutored_top = None
        g.deploy_rocks()
        if self.combo_ready():
            self.tbl.kill_all(T); return

        progress = True
        while progress:
            progress = False
            # 1. Cass from the command zone
            if not self.cass and g.avail >= CASS_COST:
                g.avail -= CASS_COST; self.cass = True; self.creatures += 1; progress = True
            # 2. draw engines (dig backbone) — cheapest first
            for nm, (c, _) in sorted(DRAW_ENGINES.items(), key=lambda x: x[1][0]):
                if nm not in self.draw_on and g.has(nm) and g.avail >= c:
                    if self.cast_creature(nm, c):
                        self.draw_on.add(nm); progress = True; break
            # 3. token-engine (self-sufficient auras first, then the constellation creatures)
            if not (self.self_engine or self.aura_engine):
                for nm, c in SELF_ENGINES.items():
                    if g.has(nm) and self.creatures >= 1 and g.avail >= self.aura_cost(c):
                        if self.cast_aura(nm, c):
                            self.self_engine = True; progress = True; break
                if not progress:
                    for nm, c in AURA_ENGINES.items():
                        if g.has(nm) and g.avail >= c:
                            if self.cast_creature(nm, c):
                                self.aura_engine = True; progress = True; break
            # 4. sac-ping outlet
            if not self.outlet:
                for nm, c in OUTLETS.items():
                    if g.has(nm) and g.avail >= c:
                        if g.cast(nm, c):
                            self.outlet = True; self.creatures += 1   # its own token carrier
                            self.trigger_draw(equip=True); progress = True; break
            # 5. tutors
            if self.do_tutors():
                progress = True
            # 6. generic-aura dig: with a draw engine online, cast filler auras to dig
            if self.draw_on and self.creatures >= 1:
                for nm, rec in g.hand:
                    if nm in SELF_ENGINES or nm in AURA_ENGINES:
                        continue
                    if is_aura(rec) and g.avail >= self.aura_cost(rec["cmc"]):
                        if self.cast_aura(nm, rec["cmc"]):
                            progress = True; break
            if self.combo_ready():
                self.tbl.kill_all(T); return


def mode_clock(index, aliases, trials, deck=None):
    deck = deck or DECK
    print("=" * 72)
    print(f"CLOCK — Cass combo-assembly kill-turn goldfish ({trials} trials, seed {SEED})")
    print("=" * 72)
    rng = random.Random(SEED)
    library, commander = slc.load_parsed(deck, index, aliases)
    print(f"  library {len(library)} + commander {commander}   [{deck.name}]")
    res = slc.run_goldfish(lambda: Trial(library, rng), trials, TURNS)
    slc.report_clock(res, SHOW, TURNS, trials, single=True)   # infinite -> decap == table
    print("\n  kill = infinite-damage combo -> whole table at once (decap == table).")
    print("  Creator's clickbait ceiling is 'turn 4'; the median assembly is the honest read.")
    print("  CEILING: no removal/counters (kill Cass and the engine stops). This is a TABLE")
    print("  kill, not a decap — compare to the roster racers' decap clock accordingly.")


def mode_levers(index, aliases, trials, deck=None):
    """Does adding a dedicated free sac outlet (the video's 'you could also run Goblin
    Bombardment / Blasting Station') move the assembly clock? Both are ~$1 and Boros-legal.
    The base list has only 2 outlets (Mask/Mortarpod) and just ONE tutor (Open the Armory)
    that finds one — so the sac-ping is the scarce slot."""
    deck = deck or DECK
    print("=" * 72)
    print(f"LEVERS — extra free sac outlet on the Cass shell ({trials} trials, seed {SEED})")
    print("=" * 72)
    base, _ = slc.load_parsed(deck, index, aliases)
    VARIANTS = {
        "base (Mask + Mortarpod)":  ([], []),
        "+ Goblin Bombardment":     (["Ornithopter"], ["Goblin Bombardment"]),
        "+ Bombardment + Blasting Station":
                                    (["Ornithopter", "Momo, Playful Pet"],
                                     ["Goblin Bombardment", "Blasting Station"]),
    }
    print("  kill (decap = table, cum %)")
    print("  turns:".ljust(44) + "".join(f"{t:6d}" for t in SHOW))
    for name, (rm, ad) in VARIANTS.items():
        rng = random.Random(SEED)
        lib = slc.build_lib(base, index, rm, ad)
        res = slc.run_goldfish(lambda: Trial(lib, rng), trials, TURNS)
        nv = 100.0 * sum(1 for _, t in res if t is None) / trials
        print(slc.row(name, slc.cum(res, 1, SHOW), SHOW)
              + f"  med {slc.median(res, 1)} nv{nv:.0f}%")
    print("\n  Read: a cheap dedicated outlet adds redundancy to the deck's one scarce slot")
    print("  (the sac-ping); watch the front edge (T5-7) + never-in-14, not just the median.")


if __name__ == "__main__":
    slc.run_cli(__doc__, {"clock": mode_clock, "levers": mode_levers})
