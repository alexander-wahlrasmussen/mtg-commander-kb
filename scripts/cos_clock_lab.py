#!/usr/bin/env python3
"""cos_clock_lab.py — Curse of the Scarab (The Scarab God) KILL-TURN goldfish.

Kill-Window Lab Sweep, deck 5 of 10 (proposals/Kill_Window_Lab_Sweep_2026-06-13.md).
Summary claims "Goldfish T7-9". Built on speed_lab_core.py.

KILL SHAPE: drain-led CONVERGE with a combat focus-fire side (mixed, but the fast
lines converge — like Genome/Radiation/Crystal Sickness, not a pure combat deck):

  DRAIN  (hit_all, CONVERGE):
    * Scarab God upkeep: each opponent loses X = Zombies you control, every upkeep
      (no mana/attack). The PRIMARY clock. (Scarab is a God, not a Zombie — it does
      NOT count itself and lords do NOT pump it.)
    * Gray Merchant of Asphodel ETB: each opponent loses X = your devotion to black;
      recurrable via the reanimation suite (Reanimate/Necromancy/Living Death).
    * Shepherd of Rot {T}: each player (you too) loses 1 per Zombie on the battlefield.
    * Plague Belcher: each opponent loses 1 per OTHER Zombie death (with a sac outlet).
  COMBO  (kill_all): Warren Soultrader + Gravecrawler + Plague Belcher — sac Gravecrawler
    to Soultrader (Treasure, lose 1), recast for {B}, Plague Belcher pings each
    opponent 1 per loop; ~39 loops at 40 life => whole table. Assembled = kill_all.
  COMBAT (hit_focus, DIVERGE): lord-pumped Zombies (Death Baron/Warchief/etc.) swing;
    decap accelerant. Unblocked goldfish convention.

THE ENGINE IS ZOMBIE COUNT + DRAW (the cs lesson). Zombie count drives the Scarab
drain; token generators multiply it and draw refills the hand to keep deploying:
  * Diregraf Colossus: each Zombie SPELL cast -> a tapped 2/2 token.
  * Necroduality: each NONTOKEN Zombie ETB -> a token copy.
  * Grave Titan (a Giant, not a Zombie): ETB + each attack -> two 2/2 Zombie tokens.
  * Wilhelt: a Zombie death -> a 2/2 decayed token (folded into the loop/combat).
  * Kindred Discovery (Zombie): every Zombie ETB OR attack -> draw (incl tokens).
  * Rooftop Storm: Zombie creature spells cost {0} (Scarab God is NOT a Zombie spell).
  * Reanimation (Entomb/Buried Alive -> Reanimate/Necromancy/Living Death) cheats
    Gray Merchant / Grave Titan onto the board early and recurs Gary's drain.

HEURISTIC, not a rules engine — coarse like rs_clock_lab. Zombie count is an integer
engine variable; token multipliers are flags; devotion is summed black pips of black
permanents deployed (oracle mana_cost). Mana = lands + rocks. Draw is capped/turn to
bound the loop. Goldfish damage unblocked, no opposing interaction, no removal of the
Scarab God. Trust the SHAPE and front edge, not the second decimal. decap/table split.

Data: collection/oracle-cards.json   ·   Writeup: proposals/Curse_of_the_Scarab_Clock_Lab_2026-06-13.md
"""
import importlib.util
import json
import random
from pathlib import Path

ROOT = Path(__file__).parent.parent
_spec = importlib.util.spec_from_file_location("speed_lab_core", Path(__file__).parent / "speed_lab_core.py")
slc = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(slc)
ds = slc.ds

DECK = ROOT / "decks" / "curse-of-the-scarab-20260510-215526.txt"
SEED = 20260613
TURNS = 14
SHOW = [5, 6, 7, 8, 9, 10, 12, 14]
DRAW_CAP = 14

ROCKS = {"Sol Ring": (1, 2), "Arcane Signet": (2, 1), "Dimir Signet": (2, 1),
         "Fellwar Stone": (2, 1), "Mind Stone": (2, 1), "Talisman of Dominance": (2, 1)}
# per-Zombie power bonus from lords/anthems (Mikaeus pumps all non-Humans incl Zombies)
LORDS = {"Death Baron": 1, "Lord of the Accursed": 1, "Undead Warchief": 2,
         "Cemetery Reaper": 1, "Narfi, Betrayer King": 1, "Mikaeus, the Unhallowed": 1}
KINDRED = "Kindred Discovery"
COLOSSUS = "Diregraf Colossus"
NECRODUALITY = "Necroduality"
GRAVE_TITAN = "Grave Titan"
GARY = "Gray Merchant of Asphodel"
SHEPHERD = "Shepherd of Rot"
GRAVEBORN = "Graveborn Muse"
ROOFTOP = "Rooftop Storm"
SCARAB = "The Scarab God"
REANIMATE_TARGETS = {GARY, GRAVE_TITAN}        # what we cheat in early
REANIMATORS = {"Reanimate": 1, "Necromancy": 3, "Dread Return": 4, "Victimize": 3}
LOOP_PIECES = {"Warren Soultrader", "Gravecrawler", "Plague Belcher"}


def load_black_pips(names):
    """name(lower) -> count of black pips in mana_cost (incl hybrid/Phyrexian)."""
    with (ROOT / "collection" / "oracle-cards.json").open(encoding="utf-8") as f:
        cards = json.load(f)
    want = {n.lower() for n in names}
    out = {}
    def pips(mc):
        return mc.count("B") if mc else 0      # counts {B}, {W/B}, {B/P} ... any B
    for c in cards:
        nm = c.get("name", "").lower()
        if nm in want and nm not in out:
            mc = c.get("mana_cost") or ""
            if not mc and c.get("card_faces"):
                mc = c["card_faces"][0].get("mana_cost", "")
            out[nm] = pips(mc)
    return out


def is_zombie(rec):
    return "zombie" in rec["type_line"].lower()


class Trial:
    def __init__(self, library, rng, index, pips):
        self.g = slc.Goldfish(library, rng, rocks={})
        self.tbl = slc.Table()
        self.index = index
        self.pips = pips
        self.z = 0                  # matured Zombies you control (count at upkeep)
        self.new_z = 0              # entered this turn (count next upkeep)
        self.scarab = False
        self.devotion = 0           # summed black pips on your permanents
        self.lord_pow = 0           # per-Zombie power bonus
        self.colossus = False
        self.necro = False
        self.kindred = False
        self.graveborn = False
        self.rooftop = False
        self.shepherd = False
        self.gary_yard = False      # Gary reanimatable
        self.titan_yard = False
        self.titan_bf = False       # Grave Titan on bf -> +2 tokens per attack
        self.lili = False           # Liliana DM +1: a 2/2 token + mill each turn
        self.cryptbreaker = False   # tap+discard -> a 2/2 token each turn
        self.yard_z = 0             # Zombie cards in yard (mass-reanimation fuel)
        self.loop = set()           # LOOP_PIECES in play
        self.draws = 0

    def gdraw(self, k):
        k = max(0, min(k, DRAW_CAP - self.draws))
        if k:
            self.g.draw(k); self.draws += k

    def zombie_etb(self, n=1, nontoken=False, base=2):
        """A Zombie (or n tokens) enters: count, Kindred draw, token multipliers."""
        total = n
        if nontoken and self.necro:
            total += 1                       # Necroduality token copy
        self.new_z += total
        if self.kindred:
            self.gdraw(total)                # draw per Zombie ETB (tokens included)

    def cast_zombie_spell(self, rec, base=2, colossus_active=None):
        """Casting a Zombie creature spell: its ETB + Colossus's cast-trigger
        token. Colossus's "whenever you cast a Zombie spell" only triggers when
        Colossus is ALREADY on the battlefield — it does NOT trigger off its own
        casting (card_lookup ruling 2026-06-29), so pass the colossus flag as it
        stood BEFORE this card resolved."""
        self.zombie_etb(1, nontoken=True, base=base)
        active = self.colossus if colossus_active is None else colossus_active
        if active:
            self.zombie_etb(1, nontoken=False)   # tapped 2/2, a token


def goldfish_kill(library, index, pips, rng):
    t = Trial(library, rng, index, pips)
    g, tbl = t.g, t.tbl
    gary_casts = 0

    def pip(nm):
        return pips.get(nm.lower(), 0)

    for T in range(1, TURNS + 1):
        t.z += t.new_z; t.new_z = 0; t.draws = 0
        # ---- UPKEEP drains (converge) ----
        if t.scarab and t.z:
            tbl.hit_all(t.z, T)
        if t.graveborn and t.z:
            t.gdraw(t.z)
        if tbl.done:
            return tbl.decap, tbl.table

        g.begin_turn(T)
        # mana rocks (devotion via pip map; records carry no mana_cost field)
        changed = True
        while changed:
            changed = False
            for nm, (cost, out) in sorted(ROCKS.items(), key=lambda x: x[1][0]):
                if g.has(nm) and g.avail >= cost:
                    g.cast(nm, cost); g.rock_out += out; g.add_mana(out)
                    t.devotion += pip(nm)
                    changed = True; break

        # reanimation setup + payoff: Entomb/Buried Alive to bin Gary/Titan, then
        # Reanimate/Necromancy to deploy. Bin first.
        if g.has("Entomb") and g.avail >= 1 and not (t.gary_yard or t.titan_yard):
            g.cast("Entomb", 1)
            if g.fetch(GARY):
                g.discard(GARY); t.gary_yard = True; t.yard_z += 1
            elif g.fetch(GRAVE_TITAN):
                g.discard(GRAVE_TITAN); t.titan_yard = True
        if g.has("Buried Alive") and g.avail >= 2 and not (t.gary_yard or t.titan_yard):
            g.cast("Buried Alive", 2)
            if g.fetch(GARY):
                g.discard(GARY); t.gary_yard = True
            if g.fetch(GRAVE_TITAN):
                g.discard(GRAVE_TITAN); t.titan_yard = True
            t.yard_z += 2                            # Buried Alive bins 3 creatures (~zombies)
        # commander
        if not t.scarab and g.avail >= 5:
            g.cast(SCARAB, 5); t.scarab = True; t.devotion += pip(SCARAB)

        # high-value engines first: Kindred / Necroduality / Rooftop
        for nm, flag in [(KINDRED, "kindred"), (NECRODUALITY, "necro"),
                         (ROOFTOP, "rooftop")]:
            rec = index.get(nm.lower())
            if g.has(nm) and not getattr(t, flag) and rec and g.avail >= rec["cmc"]:
                g.cast(nm, rec["cmc"]); setattr(t, flag, True); t.devotion += pip(nm)

        # reanimate Gary / Titan from yard (drain / tokens), cheapest reanimator
        for rz, rc in sorted(REANIMATORS.items(), key=lambda x: x[1]):
            if g.has(rz) and g.avail >= rc and (t.gary_yard or t.titan_yard):
                if t.gary_yard:
                    g.cast(rz, rc); t.gary_yard = False
                    t.devotion += pip(GARY); tbl.hit_all(t.devotion, T)
                    t.zombie_etb(1, nontoken=True)
                elif t.titan_yard:
                    g.cast(rz, rc); t.titan_yard = False
                    t.titan_bf = True; t.zombie_etb(2)   # Giant body (not Zombie) + 2 tokens
                break

        # deploy creatures/enchantments cheapest-first (Rooftop zeroes Zombie spells)
        progress = True
        while progress:
            progress = False
            best = None
            for i, (nm, rec) in enumerate(g.hand):
                if ds.is_land(rec) or nm in ROCKS or nm == SCARAB:
                    continue
                tl = rec["type_line"].lower()
                if "creature" not in tl and "enchantment" not in tl and "planeswalker" not in tl:
                    continue
                zcre = "creature" in tl and is_zombie(rec)
                cost = 0 if (zcre and t.rooftop) else rec["cmc"]
                if cost <= g.avail and (best is None or cost < best[0]):
                    best = (cost, i, nm, rec, zcre, tl)
            if best is None:
                break
            cost, i, nm, rec, zcre, tl = best
            g.hand.pop(i); g.avail -= cost
            progress = True
            # Colossus's cast-trigger only sees Zombie spells cast while it is
            # ALREADY in play; capture its state BEFORE this card sets the flag
            # so it never tokens off its own casting.
            colossus_active = t.colossus
            t.devotion += pip(nm)
            if nm in LORDS:
                t.lord_pow += LORDS[nm]
            if nm == KINDRED: t.kindred = True
            if nm == NECRODUALITY: t.necro = True
            if nm == COLOSSUS: t.colossus = True
            if nm == ROOFTOP: t.rooftop = True
            if nm == GRAVEBORN: t.graveborn = True
            if nm == SHEPHERD: t.shepherd = True
            if nm == "Liliana, Death's Majesty": t.lili = True
            if nm == "Cryptbreaker": t.cryptbreaker = True
            if nm == "Stitcher's Supplier": t.yard_z += 1   # mill 3 ~ 1 zombie
            if nm in LOOP_PIECES: t.loop.add(nm)
            if nm == GARY:
                gary_casts += 1
                tbl.hit_all(t.devotion, T)            # ETB drain (devotion incl Gary's 2)
                t.zombie_etb(1, nontoken=True)
            elif nm == GRAVE_TITAN:
                t.titan_bf = True; t.zombie_etb(2)    # Giant body (not a Zombie) + 2 tokens
            elif nm == "Rot Hulk":
                t.zombie_etb(1, nontoken=True)        # Rot Hulk is itself a Zombie
                back = min(3, t.yard_z); t.yard_z -= back
                t.zombie_etb(back)                    # ETB: return up to 3 Zombies (X=opps)
            elif nm in ("Living Death", "Agadeem's Awakening"):
                t.zombie_etb(t.yard_z); t.yard_z = 0  # mass reanimation dump
            elif zcre:
                t.cast_zombie_spell(rec, colossus_active=colossus_active)

        # steady token engines (count next upkeep / attack next turn)
        if t.titan_bf:
            t.zombie_etb(2)                           # Grave Titan attack tokens
        if t.lili:
            t.zombie_etb(1); t.yard_z += 1            # +1 token + mill 2 (~1 zombie)
        if t.cryptbreaker and len(g.hand) > 1:
            t.zombie_etb(1)                           # tap + discard -> a 2/2 token

        # Shepherd of Rot: tap -> each player loses 1 per Zombie on bf (converge)
        if t.shepherd and t.z:
            tbl.hit_all(t.z, T)

        # Rule-0 loop assembled -> table kill
        if LOOP_PIECES <= t.loop and t.z >= 1:
            tbl.kill_all(T)
        if tbl.done:
            return tbl.decap, tbl.table

        # ---- COMBAT (focus-fire) ----
        if t.z >= 1:
            tbl.hit_focus(t.z * (2 + t.lord_pow), T)
        if tbl.done:
            return tbl.decap, tbl.table

    return tbl.decap, tbl.table


def mode_clock(index, aliases, trials):
    print(f"\n### CLOCK — Curse of the Scarab kill-turn goldfish   trials={trials} seed={SEED}")
    print("    Scarab upkeep + Gary + Shepherd hit ALL opponents (converge); combat")
    print("    focus-fires; the Soultrader loop is a table kill. decap / table split.\n")
    library, commander = slc.load_parsed(DECK, index, aliases)
    pips = load_black_pips([nm for nm, _ in library] + [commander])
    rng = random.Random(SEED)
    res = [goldfish_kill(library, index, pips, rng) for _ in range(trials)]

    slc.report_clock(res, SHOW, TURNS, trials)
    print("\n  Claimed in Summary: Goldfish T7-9. Front-edge T7 odds above are the test.")


if __name__ == "__main__":
    slc.run_cli(__doc__, {"clock": mode_clock}, default_trials=40000)
