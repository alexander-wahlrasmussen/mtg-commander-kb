#!/usr/bin/env python3
"""gp_clock_lab.py — The Genome Project (Kuja) KILL-TURN goldfish + lever test.

Closes the unverified clock flagged 2026-06-10: the Summary's "Goldfish T7-9"
was hand-estimated, never goldfished. Built on speed_lab_core.py.

THE DECK'S CLOCK IS STRUCTURALLY DIFFERENT from the combat decks labbed so far:
Kuja's Wizard tokens ping EVERY opponent on each noncreature cast, so decap and
table converge instead of diverging 2-3 turns. The two real bottlenecks are
(a) transform timing — Trance Kuja (x2 all Wizard damage) needs 4 Wizards at
your end step, and (b) spells-per-turn throughput once transformed.

Damage model per noncreature cast, to EACH opponent (oracle-verified 2026-06-10):

    (p1 + 2*BlackWaltz) * trig * trance2 * city3        [Wizard sources]
  + Kessig 1 * (1+Prodigy) * city3                       [Shaman, noncreature]
  + Guttersnipe 2 * (1+Prodigy) * city3   [Shaman, i/s only — lever variants]
  + ElectrostaticField/FirebrandArcher 1 * city3         [no tribe, variants]

  p1     = Kuja tokens + Coruscation Mage (+Offspring) + Rod Hero (all Wizards)
  trig   = 1 + Harmonic Prodigy + Roaming Throne (additive trigger doublers)
  trance2= x2 while Trance Kuja (replacement, Wizard damage only)
  city3  = x3 while City on Fire (ALL damage from sources you control)

RULES FACTS the model encodes (each checked against card_lookup.py rulings):
  * Bonus Round / Cerberus / Primal Wellspring COPIES ARE NOT CAST — they do
    not trigger pings (explicit Bonus Round ruling). The Summary's Line 3 claim
    is wrong; these cards are modelled as ping-fodder casts only (conservative:
    their copy value on draw/ritual effects is ignored).
  * Underworld Breach escapes and Mizzix's Mastery copies ARE cast — full pings.
  * Storm-Kiln Artist is a SHAMAN — Harmonic Prodigy doubles its Treasures.
  * City on Fire has CONVOKE — cost modelled as max(8 - creatures, 2).
  * Urabrask pings TARGET opponent (single), i/s only, and adds {R} per i/s.
  * Neheb converts the turn's total opponent life loss into {R} postcombat —
    the turn is modelled as chain / combat / Neheb mana / second chain.
  * Stormsplitter copies exile at end step — only the original persists.
  * Necropotence replaces the draw step: refill to 7 at end step, life floor 10.

OMITTED (conservative): Aetherflux Reservoir laser, Lindblum's Mage Siege
adventure, Electro's leave-the-battlefield X, copy-effect value, Circle's +1/+0.
OPTIMISTIC (noted): rocks tap the turn they land (harness convention), Ruby
Medallion modelled as a 1-output rock, Mana Geyser flat +8, Jeska's Will flat
+5 and draw 1, no opposing interaction. Trust shapes and deltas.

Modes:
  clock   — baseline kill-turn goldfish vs the claimed T7-9.
  levers  — +pingers / +fast-mana / +draw swap variants (2 cuts each:
            Ensnared by the Mara, Dance with Calamity — the goldfish-weakest
            slots). Gamble (tutor axis) is EXCLUDED: it is a current GC and
            the deck is capped at 3/3.

Data: collection/oracle-cards.json (refresh via update_scryfall_data.py)
Writeup: proposals/Genome_Project_Clock_Lab_2026-06-10.md
"""
import importlib.util
import random
from pathlib import Path

ROOT = Path(__file__).parent.parent
_spec = importlib.util.spec_from_file_location(
    "speed_lab_core", Path(__file__).parent / "speed_lab_core.py")
slc = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(slc)
ds = slc.ds

DECK = ROOT / "decks" / "the-genome-project-20260510.txt"
SEED = 12345
TURNS = 12
SHOW = [4, 5, 6, 7, 8, 9, 10, 12]

ROCKS = {"Sol Ring": (1, 2), "Arcane Signet": (2, 1), "Fellwar Stone": (2, 1),
         "Rakdos Signet": (2, 1), "Talisman of Indulgence": (2, 1),
         "Ruby Medallion": (2, 1)}

# creature engines: name -> (cost, state_key, power, is_wizard)
ENGINES = [
    ("Harmonic Prodigy", 2, "prodigy", 1, True),
    ("Birgi, God of Storytelling", 3, "birgi", 3, False),
    ("Bayo, Irritable Instructor", 3, "electro", 2, False),   # Electro reskin
    ("Storm-Kiln Artist", 4, "stormkiln", 2, False),
    ("Black Waltz No. 3", 4, "waltz", 2, True),
    ("Urabrask", 4, "urabrask", 4, False),
    ("Roaming Throne", 4, "throne", 4, False),
    ("Neheb, the Eternal", 5, "neheb", 4, False),
    ("Stormsplitter", 4, "splitter", 1, True),
    # lever-variant pingers (absent from baseline library = never cast)
    ("Kessig Flamebreather", 2, "kessig", 1, False),
    ("Guttersnipe", 3, "snipe", 2, False),
    ("Electrostatic Field", 2, "field", 0, False),
    ("Firebrand Archer", 2, "archer", 2, False),
    # lever-variant Wizard bodies (transform acceleration axis)
    ("Dreadhorde Arcanist", 2, "arcanist", 1, True),
    ("Ghitu Lavarunner", 1, "lavarunner", 1, True),
]

DRAW2 = {  # name -> (cost, needs_discard) — all instant/sorcery draw-2s
    "Night's Whisper": (2, False), "Sign in Blood": (2, False),
    "Demand Answers": (2, True), "Highway Robbery": (2, True),
    "Deadly Dispute": (2, False),          # sac cost paid with a Treasure/rock
    "Valakut Awakening": (3, False),
    "Big Score": (2, True), "Unexpected Windfall": (2, True),  # 4 - 2 Treasures
    "Wrenn's Resolve": (2, False), "Reckless Impulse": (2, False),  # variants
    "Thrill of Possibility": (2, True), "Tormenting Voice": (2, True),
}
RITUALS = {"Dark Ritual": (1, 3), "Pyretic Ritual": (2, 3), "Seething Song": (3, 5),
           "Desperate Ritual": (2, 3), "Rite of Flame": (1, 2)}
# (name, cost, counts-as-instant/sorcery) — Rod is an artifact: pings, no magecraft
PRODUCERS = [("Vivi's Persistence", 2, True), ("Black Mage's Rod", 2, False),
             ("Cornered by Black Mages", 3, True), ("Circle of Power", 4, True)]


class Trial:
    def __init__(self, library, rng):
        self.g = slc.Goldfish(library, rng, rocks={})
        self.tbl = slc.Table()
        self.s = dict.fromkeys([k for _, _, k, _, _ in ENGINES], False)
        self.s.update(kuja=False, trance=False, city=False, necro=False)
        self.p1 = 0                      # Wizard 1-dmg-each-opponent pingers
        self.wizards = 0                 # transform threshold count
        self.board = []                  # (power, is_wizard, turn_cast)
        self.lost_turn = 0               # opponent life lost this turn (Neheb)
        self.spells_turn = 0
        self.life = 40

    # -- damage -------------------------------------------------------------
    def per_cast(self):
        s, c3 = self.s, 3 if self.s["city"] else 1
        trig = 1 + (1 if s["prodigy"] else 0) + (1 if s["throne"] else 0)
        tr2 = 2 if s["trance"] else 1
        d = (self.p1 + 2 * (1 if s["waltz"] else 0)) * trig * tr2 * c3
        if s["kessig"]:
            d += 1 * (2 if s["prodigy"] else 1) * c3
        if s["archer"]:
            d += 1 * c3
        return d

    def per_cast_is(self):               # extra, instant/sorcery casts only
        s, c3 = self.s, 3 if self.s["city"] else 1
        d = 0
        if s["snipe"]:
            d += 2 * (2 if s["prodigy"] else 1) * c3
        if s["field"]:
            d += 1 * c3
        return d

    def ping(self, T, is_spell):
        """One noncreature cast: token pings + per-cast mana refunds."""
        s, g = self.s, self.g
        self.spells_turn += 1
        living = sum(1 for d in self.tbl.dmg if d < self.tbl.life)
        d = self.per_cast() + (self.per_cast_is() if is_spell else 0)
        if d and living:
            self.tbl.hit_all(d, T)
            self.lost_turn += d * living
        if is_spell:
            if s["stormkiln"]:
                g.add_mana(2 if s["prodigy"] else 1)   # Shaman: Prodigy doubles
            if s["electro"]:
                g.add_mana(1)
            if s["urabrask"]:
                g.add_mana(1)
                c3 = 3 if s["city"] else 1
                self.tbl.hit_focus(1 * c3, T)
                self.lost_turn += 1 * c3
        if s["birgi"]:
            g.add_mana(1)

    # -- helpers ------------------------------------------------------------
    def discard_worst(self):
        g = self.g
        li = next((i for i, (_, r) in enumerate(g.hand) if ds.is_land(r)), None)
        if li is not None and sum(1 for _, r in g.hand if ds.is_land(r)) > 1:
            g.yard.append(g.hand.pop(li)); return
        if g.hand:
            i = max(range(len(g.hand)), key=lambda i: g.hand[i][1]["cmc"])
            g.yard.append(g.hand.pop(i))

    def is_spell_rec(self, rec):
        tl = rec["type_line"].lower()
        return "instant" in tl or "sorcery" in tl


def goldfish_kill(library, rng, index):
    """One trial. Returns (decap_turn, table_turn)."""
    t = Trial(library, rng)
    g, s, tbl = t.g, t.s, t.tbl

    def chain(T):
        """Greedy main-phase storm. Casts until nothing improves."""
        acted = True
        while acted and not tbl.done:
            acted = False
            # 1. rocks (artifact casts ping)
            for nm, (cost, out) in ROCKS.items():
                if g.has(nm) and g.avail >= cost:
                    g.cast(nm, cost); g.rock_out += out; g.add_mana(out)
                    t.ping(T, False); acted = True; break
            if acted:
                continue
            # 2. commander
            if not s["kuja"] and g.avail >= 4:
                s["kuja"] = True; t.wizards += 1
                t.board.append((3, True, T)); g.add_mana(-4)
                if s["birgi"]:
                    g.add_mana(1)
                acted = True; continue
            # 3. Necropotence (refill engine; BBB floor'd as 3 generic)
            if not s["necro"] and g.has("Necropotence") and g.avail >= 3:
                g.cast("Necropotence", 3); s["necro"] = True
                t.ping(T, False); acted = True; continue
            # 4. creature engines, cheapest first
            for nm, cost, key, pw, wiz in ENGINES:
                if not s[key] and g.has(nm) and g.avail >= cost:
                    g.cast(nm, cost); s[key] = True
                    t.board.append((pw, wiz, T))
                    if wiz:
                        t.wizards += 1
                    if s["birgi"]:
                        g.add_mana(1)
                    acted = True; break
            if acted:
                continue
            # 4b. Coruscation Mage (+Offspring when flush)
            if g.has("Coruscation Mage"):
                if g.avail >= 4:
                    g.cast("Coruscation Mage", 4); t.p1 += 2; t.wizards += 2
                    t.board.append((2, True, T)); t.board.append((1, True, T))
                    acted = True; continue
                if g.avail >= 2:
                    g.cast("Coruscation Mage", 2); t.p1 += 1; t.wizards += 1
                    t.board.append((2, True, T)); acted = True; continue
            # 5. Wizard producers (noncreature casts: ping + add pinger)
            for nm, cost, isp in PRODUCERS:
                if g.has(nm) and g.avail >= cost:
                    g.cast(nm, cost); t.ping(T, isp)
                    t.p1 += 1; t.wizards += 1
                    if nm == "Circle of Power":
                        g.draw(2)
                    acted = True; break
            if acted:
                continue
            # 6. City on Fire at convoke discount once a board exists
            if not s["city"] and g.has("City on Fire"):
                ncre = len(t.board) + t.p1
                cost = max(8 - ncre, 2)
                if g.avail >= cost and t.wizards >= 3:
                    g.cast("City on Fire", cost); s["city"] = True
                    t.ping(T, False); acted = True; continue
            # 7. draw-2 package
            for nm, (cost, disc) in DRAW2.items():
                if g.has(nm) and g.avail >= cost and len(g.hand) > (1 if disc else 0):
                    g.cast(nm, cost)
                    if disc:
                        t.discard_worst()
                    t.ping(T, True); g.draw(2); acted = True; break
            if acted:
                continue
            # 7b. cheap card flow
            if g.has("Faithless Looting") and g.avail >= 1:
                g.cast("Faithless Looting", 1); t.ping(T, True)
                g.draw(2); t.discard_worst(); t.discard_worst()
                acted = True; continue
            if g.has("Overmaster") and g.avail >= 1:
                g.cast("Overmaster", 1); t.ping(T, True); g.draw(1)
                acted = True; continue
            if g.has("Light Up the Stage") and g.avail >= (1 if t.lost_turn else 3):
                g.cast("Light Up the Stage", 1 if t.lost_turn else 3)
                t.ping(T, True); g.draw(2); acted = True; continue
            # 8. rituals — when pings flow or they enable a bigger cast
            for nm, (cost, out) in RITUALS.items():
                if g.has(nm) and g.avail >= cost and (
                        t.per_cast() >= 3 or any(
                            g.has(x) and cost - out + g.avail >= c
                            for x, c in [("Peer into the Abyss", 7),
                                         ("Mana Geyser", 5)])):
                    g.cast(nm, cost); g.add_mana(out); t.ping(T, True)
                    acted = True; break
            if acted:
                continue
            if g.has("Jeska's Will") and g.avail >= 3:
                g.cast("Jeska's Will", 3); g.add_mana(5); g.draw(1)
                t.ping(T, True); acted = True; continue
            if g.has("Mana Geyser") and g.avail >= 5 and t.per_cast() >= 3:
                g.cast("Mana Geyser", 5); g.add_mana(8); t.ping(T, True)
                acted = True; continue
            # 9. capstones
            if g.has("Peer into the Abyss") and g.avail >= 7:
                g.cast("Peer into the Abyss", 7); t.ping(T, True)
                g.draw(min(15, max(0, (len(g.deck) - g.ptr) // 2)))
                t.life -= t.life // 2
                acted = True; continue
            nonland_yard = [y for y in g.yard if not ds.is_land(y[1])]
            if (g.has("Dawn Warriors' Legacy") and g.avail >= 8
                    and sum(1 for y in nonland_yard if t.is_spell_rec(y[1])) >= 3):
                g.cast("Dawn Warriors' Legacy", 8); t.ping(T, True)
                for nm, rec in list(g.yard):          # copies of yard i/s ARE cast
                    if not t.is_spell_rec(rec):
                        continue
                    t.ping(T, True)
                    if nm in RITUALS:
                        g.add_mana(RITUALS[nm][1])
                    elif nm in DRAW2:
                        g.draw(2)
                    g.yard.remove((nm, rec))
                acted = True; continue
            if (g.has("Underworld Breach") and g.avail >= 2
                    and len(nonland_yard) >= 4):
                g.cast("Underworld Breach", 2); t.ping(T, False)
                while not tbl.done:                    # escape loop
                    cands = sorted(
                        ((nm, rec) for nm, rec in g.yard
                         if t.is_spell_rec(rec) and rec["cmc"] <= g.avail),
                        key=lambda x: x[1]["cmc"])
                    if not cands or len(g.yard) < 4:
                        break
                    nm, rec = cands[0]
                    g.yard.remove((nm, rec)); g.pay(rec["cmc"])
                    fuel = [y for y in g.yard if (y[0], y[1]) != (nm, rec)][:3]
                    if len(fuel) < 3:
                        break
                    for f in fuel:
                        g.yard.remove(f)
                    t.ping(T, True)
                    if nm in RITUALS:
                        g.add_mana(RITUALS[nm][1])
                    elif nm in DRAW2:
                        g.draw(2)
                acted = True; continue
            # 10. fodder casts once each cast is worth real damage
            if t.per_cast() >= 4:
                cands = sorted(
                    ((i, nm, rec) for i, (nm, rec) in enumerate(g.hand)
                     if not ds.is_land(rec) and "creature" not in
                     rec["type_line"].lower() and rec["cmc"] <= g.avail
                     and nm != "Exsanguinate"),
                    key=lambda x: x[2]["cmc"])
                if cands:
                    i, nm, rec = cands[0]
                    g.hand.pop(i); g.pay(rec["cmc"])
                    g.yard.append((nm, rec))
                    t.ping(T, t.is_spell_rec(rec)); acted = True; continue
            # 11. Exsanguinate when it tables (or as a huge chunk)
            if g.has("Exsanguinate") and g.avail >= 3:
                rem = [tbl.life - d for d in tbl.dmg if d < tbl.life]
                X = g.avail - 2
                if rem and (X >= max(rem) or X >= 20):
                    g.cast("Exsanguinate", g.avail)
                    t.ping(T, True)
                    tbl.hit_all(X, T); t.lost_turn += X * len(rem)
                    acted = True; continue

    for T in range(1, TURNS + 1):
        if s["necro"]:                    # Necropotence replaces the draw step
            g.begin_turn(1 if T > 1 else T)   # suppress draw, keep land drop
        else:
            g.begin_turn(T)
        t.lost_turn = 0
        t.spells_turn = 0
        chain(T)
        if tbl.done:
            break
        # combat: prior-turn creatures swing unblocked, focus-fire
        c3 = 3 if s["city"] else 1
        atk = sum(p * (2 if (wiz and s["trance"]) else 1) * c3
                  for p, wiz, tc in t.board if tc < T and p)
        if s["kuja"] and s["trance"]:
            # board already counts Kuja at 3 power x2 trance; true value is
            # Trance Kuja 4 power x2 = 8, so top up the difference (8 - 6)
            atk += 2 * c3
        if atk:
            tbl.hit_focus(atk, T)
            t.lost_turn += min(atk, tbl.life)
        # Dreadhorde Arcanist attack trigger: recast a cmc<=1 i/s from the yard
        # (a real cast: full pings; exiled after). Power-1 base, no pump modelled.
        if s["arcanist"] and atk:
            y = next((y for y in g.yard if t.is_spell_rec(y[1])
                      and y[1]["cmc"] <= 1), None)
            if y is not None:
                g.yard.remove(y)
                t.ping(T, True)
                if y[0] in RITUALS:
                    g.add_mana(RITUALS[y[0]][1])
        if tbl.done:
            break
        if s["neheb"] and t.lost_turn:    # postcombat main: {R} per life lost
            g.add_mana(t.lost_turn)
            chain(T)
            if tbl.done:
                break
        # end step: Kuja token, transform check, Necropotence refill
        if s["kuja"]:
            t.p1 += 1; t.wizards += 1
        if t.wizards >= 4 and s["kuja"]:
            s["trance"] = True
        if s["necro"]:
            n = min(max(0, 7 - len(g.hand)), max(0, t.life - 10))
            g.draw(n); t.life -= n

    return tbl.decap, tbl.table


VARIANTS = {
    "BASE (current list)": ([], []),
    "+pingers  (-Ensnared -Dance +Guttersnipe +Kessig Flamebreather)":
        (["Ensnared by the Mara", "Dance with Calamity"],
         ["Guttersnipe", "Kessig Flamebreather"]),
    "+fastmana (-Ensnared -Dance +Pyretic Ritual +Seething Song)":
        (["Ensnared by the Mara", "Dance with Calamity"],
         ["Pyretic Ritual", "Seething Song"]),
    "+draw     (-Ensnared -Dance +Wrenn's Resolve +Reckless Impulse)":
        (["Ensnared by the Mara", "Dance with Calamity"],
         ["Wrenn's Resolve", "Reckless Impulse"]),
    "+wizards  (-Ensnared -Dance +Dreadhorde Arcanist +Ghitu Lavarunner)":
        (["Ensnared by the Mara", "Dance with Calamity"],
         ["Dreadhorde Arcanist", "Ghitu Lavarunner"]),
    # 4-card ceiling probes on the two axes with any 2-card signal
    "+draw4    (also -Overmaster -Reanimate +Thrill +Tormenting Voice)":
        (["Ensnared by the Mara", "Dance with Calamity", "Overmaster", "Reanimate"],
         ["Wrenn's Resolve", "Reckless Impulse",
          "Thrill of Possibility", "Tormenting Voice"]),
    "+mana4    (also -Overmaster -Reanimate +Desperate Rit +Rite of Flame)":
        (["Ensnared by the Mara", "Dance with Calamity", "Overmaster", "Reanimate"],
         ["Pyretic Ritual", "Seething Song",
          "Desperate Ritual", "Rite of Flame"]),
}


def _run(library, index, trials, label):
    rng = random.Random(SEED)
    res = [goldfish_kill(library, rng, index) for _ in range(trials)]
    print(slc.row(label + "  decap", slc.cum(res, 0, SHOW), SHOW, width=66))
    print(slc.row(label + "  table", slc.cum(res, 1, SHOW), SHOW, width=66))
    print(f"    median decap {slc.median(res, 0)} / table {slc.median(res, 1)}"
          f" · never-in-{TURNS}: "
          f"{100.0 * sum(1 for _, x in res if x is None) / trials:.0f}% (table)")
    return res


def mode_clock(index, aliases, trials):
    print(f"\n### CLOCK — Genome Project kill-turn goldfish   trials={trials} seed={SEED}")
    print("    Pings hit ALL opponents -> decap and table converge (vs combat decks).")
    print("    Claimed in Summary (unverified): Goldfish T7-9.\n")
    library, commander = slc.load_parsed(DECK, index, aliases)
    print("  P(kill <= turn T) %".ljust(72) + "".join(f"{t:>6}" for t in SHOW))
    _run(library, index, trials, "")


def mode_levers(index, aliases, trials):
    print(f"\n### LEVERS — axis swaps, 2-card packages   trials={trials} seed={SEED}")
    print("    Tutor axis (Gamble) excluded: current GC, deck capped 3/3.\n")
    base, commander = slc.load_parsed(DECK, index, aliases)
    print("  P(kill <= turn T) %".ljust(72) + "".join(f"{t:>6}" for t in SHOW))
    for label, (rm, add) in VARIANTS.items():
        lib = slc.build_lib(base, index, rm, add)
        _run(lib, index, trials, label[:58])
        print()


if __name__ == "__main__":
    slc.run_cli(__doc__, {"clock": mode_clock, "levers": mode_levers},
                default_trials=20000)
