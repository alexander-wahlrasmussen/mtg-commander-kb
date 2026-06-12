#!/usr/bin/env python3
"""knn_clock_lab.py — Quantitative Easing (Kinnan, Bonder Prodigy) KILL-TURN goldfish.

Stage 3 of the 2026-06-12 candidate bake-off. Deck:
decks/considering/quantitative-easing-20260612.txt. Built on speed_lab_core.py.
Kill shape: resolve engine -> infinite mana -> Walking Ballista pings ALL
opponents, so decap = table by construction (kill_all).

THE THREE INFINITE LINES (oracle-verified via card_lookup.py 2026-06-12):

  A. COLORLESS — Kinnan + Basalt Monolith: tap for {C}{C}{C} (+1 Kinnan) = 4,
     untap {3} -> net +1 per cycle. Infinite COLORLESS only, so Kinnan's
     {5}{G}{U} dig is NOT payable: the line needs Walking Ballista itself
     (hand/bf, castable X=0) or an artifact tutor with colored mana left:
     Whir X=0 ({U}{U}{U}~3), Reshape X=0 ({U}{U}~2, sac a spare rock),
     Fabricate (3, to hand).
  B. AURA — Kinnan + (Freed from the Real | Pemmin's Aura, 3) on Bloom Tender
     (>=2 colours incl. the blue aura itself -> 2 (+1 Kinnan) = 3/tap, untap
     {U} = net +2 coloured) or Incubation Druid (any type a land could
     produce, x2 with Kinnan, untap {U} = net +1 coloured). Infinite COLOURED
     -> Kinnan's {5}{G}{U} dig repeatedly: Ballista is a non-Human Construct,
     dig until found -> kill.
  C. SELVALA — Selvala (X = greatest power) + Umbral Mantle (untap {3},
     +2/+2) or Staff of Domination (untap 3+1): net positive once the best
     power on board >= 4 (Mantle grows it each cycle). Coloured ("any
     combination of colors") -> dig/outlet as line B. Power requirement
     tracked from real printed powers.

  Kinnan's dig is modelled HONESTLY: peek the next 5 library cards, take a
  needed non-Human creature to the battlefield, bottom the rest (repeatable
  with infinite coloured mana = guaranteed Ballista eventually -> kill_all).

TUTORS: Worldly/Sylvan Tutor (1, creature -> TOP, arrives next draw; CAN
fetch Ballista — artifact creature), Chord of Calling (X+3, instant, to bf;
NEVER fetches Ballista — X=0 would enter as a 0/0 and die), Eldritch
Evolution (3 + sac dork, MV<=sac+2), Whir/Fabricate/Reshape (artifact suite),
Spellseeker (3, fetches an I/S MV<=2: Worldly/Sylvan/Reshape), Fierce Empath
(only Vorinclex, ignored). Finale of Devastation: creature to bf, X = MV.

MANA: lands + rocks + dorks; with Kinnan on bf every nonland mana source
taps for +1 (his whole turbo thesis) — modelled as +1 per deployed dork/rock
tapped. Castle Garenbrig ignored (colour-blind floor). OMITTED: Ballista as
a slow mana sink, Blue Sun's Zenith chains, Temur Sabertooth loops, Genesis
Wave, counterspell protection. OPTIMISTIC: rocks repeat (Mana Vault/Grim
Monolith untap tax ignored, wb-lab convention), colour-blind mana floor,
auras never fizzle. Trust shapes and deltas.

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

DECK = ROOT / "decks" / "considering" / "quantitative-easing-20260612.txt"
SEED = 20260612
TURNS = 12
SHOW = [3, 4, 5, 6, 7, 8, 9, 10, 12]

ROCKS = {"Sol Ring": (1, 2), "Mana Vault": (1, 3), "Grim Monolith": (2, 3),
         "Arcane Signet": (2, 1), "Simic Signet": (2, 1),
         "Fellwar Stone": (2, 1), "Talisman of Curiosity": (2, 1),
         "Mind Stone": (2, 1)}
DORKS = {"Birds of Paradise": 1, "Llanowar Elves": 1, "Elvish Mystic": 1,
         "Fyndhorn Elves": 1, "Arbor Elf": 1, "Boreal Druid": 1,
         "Paradise Druid": 1, "Wall of Roots": 1, "Devoted Druid": 1,
         "Priest of Titania": 1, "Incubation Druid": 1, "Bloom Tender": 2}
DORK_COST = {"Birds of Paradise": 1, "Llanowar Elves": 1, "Elvish Mystic": 1,
             "Fyndhorn Elves": 1, "Arbor Elf": 1, "Boreal Druid": 1,
             "Paradise Druid": 2, "Wall of Roots": 2, "Devoted Druid": 2,
             "Priest of Titania": 2, "Incubation Druid": 2, "Bloom Tender": 2,
             "Selvala, Heart of the Wilds": 3}
AURAS = {"Freed from the Real": 3, "Pemmin's Aura": 3}
AURA_HOSTS = {"Bloom Tender", "Incubation Druid"}
UNTAPPERS = {"Umbral Mantle": 3, "Staff of Domination": 3}
# non-Human creatures Kinnan's dig may put in (combo-relevant ones)
DIG_HITS = {"Walking Ballista", "Bloom Tender", "Incubation Druid",
            "Selvala, Heart of the Wilds"}
# value bodies: name -> (cost, draws_on_etb, lands_on_etb) — power from oracle
BODIES = {"Coiling Oracle": (2, 1, 0), "Sakura-Tribe Elder": (2, 0, 1),
          "Wood Elves": (3, 0, 1), "Eternal Witness": (3, 0, 0),
          "Trygon Predator": (3, 0, 0), "Spellseeker": (3, 0, 0),
          "Fierce Empath": (3, 0, 0), "Temur Sabertooth": (4, 0, 0),
          "Frilled Mystic": (4, 0, 0), "Mystic Snake": (4, 0, 0),
          "Tatyova, Benthic Druid": (5, 0, 0),
          "Vorinclex, Voice of Hunger": (8, 0, 0)}
CANTRIPS = {"Brainstorm": 1, "Ponder": 1, "Preordain": 1}


class Trial:
    def __init__(self, library, rng, powmap):
        self.g = slc.Goldfish(library, rng, rocks=ROCKS)
        self.tbl = slc.Table()
        self.powmap = powmap
        self.bf = set()
        self.kinnan = False
        self.dork_out = 0          # mana from dorks deployed before this turn
        self.dork_new = 0
        self.dorks_n = 0           # count deployed (for Kinnan +1 each)
        self.dorks_n_new = 0
        self.maxpow = 0            # best printed power on bf
        self.pending_top = []      # Worldly/Sylvan targets
        self.colorless_online = False   # Kinnan+Basalt up, hunting Ballista
        self.draw_rate = 0         # Sylvan Library / Mystic Remora / Tatyova

    def kinnan_dig(self, want):
        """{5}{G}{U}: peek 5, put a wanted non-Human creature onto bf.
        Misses are BOTTOMED (moved to the end of the library), not lost —
        sustained digging eventually cycles back to them."""
        g = self.g
        window = g.deck[g.ptr:g.ptr + 5]
        hit = next((t for t in window if t[0] in want), None)
        rest = [t for t in window if t is not hit]
        del g.deck[g.ptr:g.ptr + 5]
        g.deck.extend(rest)
        if hit:
            self.bf.add(hit[0])
            return hit[0]
        return None

    def infinite_check(self, T):
        g = self.g
        # line B: aura on a host
        host = self.bf & AURA_HOSTS
        if self.kinnan and host:
            for a, c in AURAS.items():
                if g.has(a) and g.avail >= c:
                    g.cast(a, c)
                    self.tbl.kill_all(T)        # coloured infinite -> dig -> Ballista
                    return True
        # line C: Selvala + untapper, best power >= 4
        if "Selvala, Heart of the Wilds" in self.bf and self.maxpow >= 4:
            for u, c in UNTAPPERS.items():
                if u in self.bf or (g.has(u) and g.avail >= c and g.cast(u, c)):
                    if self.kinnan or "Walking Ballista" in self.bf \
                            or g.has("Walking Ballista") \
                            or g.has("Blue Sun's Zenith"):
                        self.tbl.kill_all(T)
                        return True
        # line A: Kinnan + Basalt -> colourless infinite, needs Ballista access
        if self.kinnan and "Basalt Monolith" in self.bf:
            if "Walking Ballista" in self.bf or g.has("Walking Ballista"):
                self.tbl.kill_all(T)
                return True
            for tut, c in (("Reshape", 2), ("Whir of Invention", 3),
                           ("Fabricate", 3)):
                if g.has(tut) and g.avail >= c:
                    g.cast(tut, c)
                    self.tbl.kill_all(T)
                    return True
            # engine online without an outlet yet: infinite {C} pays the {5}
            # of Kinnan's dig, lands cover {G}{U} ~twice a turn -> dig for
            # Ballista (non-Human Construct) until found.
            self.colorless_online = True
        return False

    def missing_piece(self):
        """What to tutor toward, in priority order."""
        g = self.g
        if self.kinnan:
            if not (self.bf & AURA_HOSTS) and not g.has("Bloom Tender") \
                    and not g.has("Incubation Druid"):
                return "Bloom Tender"
            if (self.bf & AURA_HOSTS) and not any(g.has(a) for a in AURAS):
                return None                    # auras have no tutor here
            if "Basalt Monolith" not in self.bf and not g.has("Basalt Monolith"):
                return "Basalt Monolith"
        if not g.has("Walking Ballista") and "Walking Ballista" not in self.bf:
            return "Walking Ballista"
        return None

    def turn(self, T):
        g = self.g
        self.dork_out += self.dork_new
        self.dorks_n += self.dorks_n_new
        self.dork_new = self.dorks_n_new = 0
        g.begin_turn(T)
        g.draw(self.draw_rate)
        for nm in self.pending_top:
            g.fetch(nm)
        self.pending_top = []
        g.deploy_rocks()
        rocks_n = sum(1 for v in (g.rocks,) for _ in ())  # placeholder, unused
        g.add_mana(self.dork_out)
        if self.kinnan:
            # +1 per nonland source tapped: dorks + deployed rocks
            g.add_mana(self.dorks_n + (g.rock_out > 0) * max(1, g.rock_out // 2))

        # commander first — he IS the engine
        if not self.kinnan and g.avail >= 2:
            g.avail -= 2
            self.kinnan = True
            self.bf.add("Kinnan, Bonder Prodigy")
            self.maxpow = max(self.maxpow, 2)

        if self.infinite_check(T):
            return
        if self.colorless_online:
            for _ in range(2):                  # two {G}{U} digs off real lands
                if self.kinnan_dig({"Walking Ballista"}):
                    self.tbl.kill_all(T)
                    return

        progress = True
        while progress:
            progress = False
            # combo permanents from hand
            for nm, c in (("Basalt Monolith", 3), ("Walking Ballista", 2),
                          ("Selvala, Heart of the Wilds", 3)):
                if nm not in self.bf and g.has(nm) and g.avail >= c:
                    if nm == "Walking Ballista":
                        g.cast(nm, 2)          # X=1, survives
                        self.bf.add(nm)
                    else:
                        g.cast(nm, c)
                        self.bf.add(nm)
                        if nm == "Basalt Monolith":
                            g.rock_out += 3
                            g.add_mana(3)
                    self.maxpow = max(self.maxpow,
                                      self.powmap.get(nm.lower(), 0) or 0)
                    progress = True
            # dorks
            for nm, c in DORK_COST.items():
                if nm not in self.bf and g.has(nm) and g.avail >= c:
                    g.cast(nm, c)
                    self.bf.add(nm)
                    self.dork_new += DORKS.get(nm, 0)
                    self.dorks_n_new += 1
                    self.maxpow = max(self.maxpow,
                                      self.powmap.get(nm.lower(), 0) or 0)
                    progress = True
                    break
            # draw engines and cantrips
            for nm, c, rate in (("Mystic Remora", 1, 1),
                                ("Sylvan Library", 2, 1),
                                ("Guardian Project", 4, 0)):
                if nm not in self.bf and g.has(nm) and g.avail >= c:
                    g.cast(nm, c)
                    self.bf.add(nm)
                    self.draw_rate += rate
                    progress = True
            for nm, c in CANTRIPS.items():
                if g.has(nm) and g.avail >= c:
                    g.cast(nm, c)
                    g.draw(1)
                    progress = True
            # value bodies (raise Selvala's X, draw, ramp)
            for nm, (c, dr, ld) in BODIES.items():
                if nm not in self.bf and g.has(nm) and g.avail >= c:
                    g.cast(nm, c)
                    self.bf.add(nm)
                    self.maxpow = max(self.maxpow,
                                      self.powmap.get(nm.lower(), 0) or 0)
                    if "Guardian Project" in self.bf:
                        g.draw(1)
                    if dr:
                        g.draw(dr)
                    if ld:
                        g.lands += 1
                    if nm == "Spellseeker" and not g.has("Worldly Tutor"):
                        g.fetch("Worldly Tutor")
                    if nm == "Tatyova, Benthic Druid":
                        self.draw_rate += 1
                    progress = True
                    break
            # tutors toward the missing piece
            tgt = self.missing_piece()
            if tgt:
                fetched = False
                for tut, c, how in (("Worldly Tutor", 1, "top"),
                                    ("Sylvan Tutor", 1, "top"),
                                    ("Fabricate", 3, "hand"),
                                    ("Chord of Calling", None, "bf"),
                                    ("Eldritch Evolution", 3, "bf"),
                                    ("Finale of Devastation", None, "bf"),
                                    ("Whir of Invention", None, "bf"),
                                    ("Reshape", None, "bf")):
                    rec = None
                    artifact_tgt = tgt in ("Basalt Monolith", "Walking Ballista")
                    creature_tgt = tgt != "Basalt Monolith"
                    if tut in ("Worldly Tutor", "Sylvan Tutor") and not creature_tgt:
                        continue
                    if tut in ("Fabricate", "Whir of Invention", "Reshape") \
                            and not artifact_tgt:
                        continue
                    if tut in ("Chord of Calling", "Eldritch Evolution",
                               "Finale of Devastation") and (
                            not creature_tgt or tgt == "Walking Ballista"):
                        continue              # X=0 Ballista dies; Finale X=0 ok? no
                    cost = {"Worldly Tutor": 1, "Sylvan Tutor": 1,
                            "Fabricate": 3, "Eldritch Evolution": 3,
                            "Chord of Calling": 3 + 2,
                            "Finale of Devastation": 2 + 2,
                            "Whir of Invention": 3 + 3,
                            "Reshape": 2 + 3}[tut]
                    if g.has(tut) and g.avail >= cost:
                        if how == "top":
                            if any(g.deck[i][0] == tgt
                                   for i in range(g.ptr, len(g.deck))):
                                g.cast(tut, cost)
                                self.pending_top.append(tgt)
                                fetched = True
                        else:
                            if g.fetch(tgt):
                                g.cast(tut, cost)
                                if how == "bf":
                                    g.hand.pop(g.in_hand(tgt))
                                    self.bf.add(tgt)
                                    if tgt == "Basalt Monolith":
                                        g.rock_out += 3
                                fetched = True
                        if fetched:
                            progress = True
                            break
            # Kinnan's own dig with spare mana
            if self.kinnan and g.avail >= 7:
                want = {n for n in DIG_HITS
                        if n not in self.bf and not g.has(n)}
                if want:
                    g.avail -= 7
                    got = self.kinnan_dig(want)
                    if got:
                        self.maxpow = max(self.maxpow,
                                          self.powmap.get(got.lower(), 0) or 0)
                    progress = True
            if self.infinite_check(T):
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
    print(f"CLOCK — Quantitative Easing (Kinnan) kill-turn goldfish "
          f"({trials} trials, seed {SEED})")
    print("=" * 72)
    rng = random.Random(SEED)
    library, commander = slc.load_parsed(DECK, index, aliases)
    names = [nm for nm, _ in library] + [commander]
    raw_pow = slc.load_powers(names)
    powmap = {k: (v if isinstance(v, int) else 0) for k, v in raw_pow.items()}
    print(f"  library {len(library)} + commander {commander}")
    print("  turns:".ljust(44) + "".join(f"{t:6d}" for t in SHOW))
    res = goldfish(library, trials, rng, powmap)
    print(slc.row("kill (decap = table, cum %)", slc.cum(res, 1, SHOW), SHOW))
    nv = 100.0 * sum(1 for _, t in res if t is None) / trials
    print(f"\n  median kill {slc.median(res, 1)}   ·   never-in-{TURNS}: {nv:.0f}%")
    print("\n  Stage 1 screened Kinnan 'Strong — 2-card turbo'. The rows above are the test.")


if __name__ == "__main__":
    slc.run_cli(__doc__, {"clock": mode_clock})
