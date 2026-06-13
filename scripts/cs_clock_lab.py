#!/usr/bin/env python3
"""cs_clock_lab.py — Crystal Sickness (Golbez, Crystal Collector) KILL-TURN goldfish.

Kill-Window Lab Sweep, deck 4 of 10 (proposals/Kill_Window_Lab_Sweep_2026-06-13.md).
Summary claims "Goldfish T7-9". Built on speed_lab_core.py.

KILL SHAPE: MIXED (the tracker's first-pass "combat focus-fire -> diverge" prior is
only half right). The deck's NAMED primary kills are all-table DRAINS (converge);
its incidental combat is focus-fire (diverge). The net is a mild divergence.

  DRAIN  (hit_all, CONVERGE) — the real clock:
    * Golbez end step: with 4+ artifacts return a creature from yard to hand; with
      8+ artifacts EACH opponent loses life = that card's power. Drain bombs:
        Phyrexian Dreadnought  12 (fixed). Cast for {1} -> ETB self-sacrifice ->
            lands in yard; recast for {1} each turn to re-bin = repeatable 12 drain.
        Master of Etherium     = artifacts you control (CDA works in ALL zones incl
            graveyard, ruling-verified) — scales with the same board it gates on.
        Troll of Khazad-dum    6. Swampcycle {1} pitches it to yard early.
    * Tezzeret, Master of the Bridge +2: X damage to EACH opponent, X = artifacts,
      every turn (he himself does NOT have affinity -> flat {4}{U}{B}=6 to cast).
  COMBAT (hit_focus, DIVERGE) — the decap accelerant:
    * Urza's 0/0 Construct = artifacts you control; Thopter/Myr tokens (+1/+1 each
      from Master of Etherium on bf, Thopters +1/+1 from Stridehangar). Unblocked
      goldfish swing, focus-fire one player -> pulls decap ahead of the drain table.

THE ENGINE IS CARD DRAW (the v1 lesson, again): the deck's clock is not the curve,
it is how fast the hand refills to keep deploying artifacts so the token generators
multiply the count to 8 and feed a fatty to the yard. Draw modelled (oracle-verified
card_lookup.py 2026-06-13):
  * Matoya, Archon Elder: draw on EVERY surveil. Golbez surveils per artifact ENTER
    (tokens included) -> with Matoya out, every artifact entering also draws.
  * Thought Monitor (ETB draw 2, affinity), Thoughtcast (draw 2, affinity),
    Cryogen Relic / Mishra's & Urza's Bauble (cantrips), The One Ring (escalating),
    Skullclamp (sac a token Thopter -> draw 2, loops with the token makers),
    Riddlesmith / Underworld Cookbook (loot -> folded into the fatty dig).
  * Token generators trigger on CAST not ETB (Sai / Efficient Construction / Mirran
    Mirrodin Besieged -> token per artifact spell; Forensic Gadgeteer / Mechanist ->
    Clue; Stridehangar -> +1 bonus Thopter per token-creation event). Mirrodin is in
    MIRRAN mode; its Phyrexian 15-cards-in-yard alt-win is a SLOWER unmodelled line.
  * Etherium Sculptor / Cloud Key: artifact spells cost {1} less (floor 0).
  * Urza taps artifacts for {U} (extra mana, capped) and makes the Construct.

HEURISTIC, not a rules engine. Mana = lands + rocks (+ capped Urza tap-mana); draws
capped per turn to bound the loop. Fatties reach the yard via a dig proxy (surveil/
loot/self-sac/swampcycle are dense and cheap) scaled by artifacts entered that turn;
Dreadnought re-bins for {1} so its drain repeats, others repeat only with a loot
outlet online. Goldfish damage is unblocked; no opposing interaction. Trust the
SHAPE and front edge, not the second decimal. decap and table reported separately.

Data: collection/oracle-cards.json   ·   Writeup: proposals/Crystal_Sickness_Clock_Lab_2026-06-13.md
"""
import importlib.util
import random
from pathlib import Path

ROOT = Path(__file__).parent.parent
_spec = importlib.util.spec_from_file_location("speed_lab_core", Path(__file__).parent / "speed_lab_core.py")
slc = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(slc)
ds = slc.ds

DECK = ROOT / "decks" / "crystal-sickness-20260322-152311.txt"
SEED = 20260613
TURNS = 14
SHOW = [5, 6, 7, 8, 9, 10, 12, 14]
DRAW_CAP = 16            # max engine draws per turn (bounds the Matoya/Skullclamp loop)

# mana artifacts: name -> (cost, output). All also count toward the artifact total.
ROCKS = {
    "Sol Ring": (1, 2), "Arcane Signet": (2, 1), "Dimir Signet": (2, 1),
    "Talisman of Dominance": (2, 1), "Fellwar Stone": (2, 1),
    "Liquimetal Torque": (2, 1), "Springleaf Drum": (1, 1),
    "Mox Amber": (0, 1), "Mox Opal": (0, 1), "Chrome Mox": (0, 1),
    "Lotus Petal": (0, 1), "The Mightstone and Weakstone": (5, 2),
}
REDUCERS = {"Etherium Sculptor", "Cloud Key"}            # artifact spells cost {1} less
GEN_TOKEN = {"Sai, Master Thopterist", "Efficient Construction",
             "Mirrodin Besieged"}                        # cast -> Thopter/Myr (creature)
GEN_CLUE = {"Forensic Gadgeteer", "The Mechanist, Aerial Artisan"}  # cast -> Clue (artifact)
STRIDE = "Stridehangar Automaton"                        # token event -> +1 Thopter
# non-artifact engine permanents the deploy loop must ALSO cast (Golbez doesn't
# surveil off these entering — they aren't artifacts — but they drive the engine).
# name -> (cmc, body power for combat)
ENGINE_NONART = {
    "Sai, Master Thopterist": (3, 1), "Efficient Construction": (4, 0),
    "Mirrodin Besieged": (3, 0), "Forensic Gadgeteer": (3, 1),
    "The Mechanist, Aerial Artisan": (3, 1), "Matoya, Archon Elder": (3, 1),
    "Riddlesmith": (2, 1), "Basim Ibn Ishaq": (2, 2),
}
LOOT = {"Riddlesmith", "The Underworld Cookbook"}        # repeat-drain enabler for non-Dread fatties
CANTRIP_ART = {"Mishra's Bauble", "Urza's Bauble", "Cryogen Relic"}  # +1 card on/around ETB
# noncreature non-artifact draw spells: name -> (mana floor, cards)
DRAW_SPELL = {"Thoughtcast": (1, 2), "Ponder": (1, 1), "Preordain": (1, 1),
              "Lórien Revealed": (1, 1)}
FATTIES = {"Phyrexian Dreadnought": 12, "Troll of Khazad-dûm": 6}  # Master handled separately


def is_artifact(rec):
    return "artifact" in rec["type_line"].lower()


def is_artifact_land(rec):
    tl = rec["type_line"].lower()
    return "artifact" in tl and "land" in tl


class Trial:
    def __init__(self, library, rng, index):
        self.g = slc.Goldfish(library, rng, rocks={})   # we deploy artifacts ourselves
        self.tbl = slc.Table()
        self.index = index
        self.arts = 0                # artifacts you control (the engine variable)
        self.golbez = False
        self.urza = False            # Urza in play (Construct + tap-mana)
        self.tezz = False            # Tezzeret, Master of the Bridge in play
        self.master_bf = False       # Master of Etherium on battlefield (pumps, body)
        self.matoya = False          # draw on every surveil (= every artifact enter)
        self.basim = False           # +1 draw on first historic cast each turn
        self.bodies = 0              # non-Construct creature power (matured), focus-fire
        self.new_bodies = 0
        self.onering = False
        self.ring_burden = 0
        self.skullclamp = False
        self.reducers = 0
        self.gen_token = 0           # # of token-on-cast generators online
        self.gen_clue = 0
        self.stride = False
        self.loot = False
        self.dread_yard = False
        self.troll_yard = False
        self.master_yard = False
        self.tok_cre = 0             # Thopter/Myr/bonus token creatures (matured)
        self.new_tok = 0             # created this turn (summoning sick)
        self.entered = 0             # artifacts entered this turn (surveil/dig depth)
        self.cum_entered = 0         # ALL artifacts entered so far (compound-dig depth)
        self.draws = 0               # engine draws this turn (capped)

    # -- draw / artifact entry ----------------------------------------------
    def gdraw(self, k):
        k = max(0, min(k, DRAW_CAP - self.draws))
        if k:
            self.g.draw(k); self.draws += k

    def art_enter(self, n=1, token=False):
        """An artifact enters: count it, fire Golbez surveil (-> Matoya draws)."""
        self.arts += n
        self.entered += n
        if token:
            self.new_tok += n
        if self.matoya:
            self.gdraw(n)            # one surveil -> one Matoya draw per artifact

    def on_cast_artifact(self):
        """An artifact SPELL resolved: fire the cast-triggered token/Clue makers."""
        made_token = 0
        if self.gen_token:
            made_token += self.gen_token            # 1 Thopter/Myr per generator
        if self.stride and made_token:
            made_token += 1                         # one bonus Thopter per creation event
        if made_token:
            self.art_enter(made_token, token=True)
        if self.gen_clue:
            self.art_enter(self.gen_clue)           # Clues: artifacts, not creatures

    def dig_for_fatty(self, dig="current"):
        """Surveil/loot/self-sac proxy: scan a window scaled by artifacts entered;
        pull a drain bomb into the yard. More artifacts -> more surveil -> more digs.

        dig sensitivity regimes (2026-06-13 test of the surveil-modelling hunch):
          off      — no surveil/loot dig at all; bombs reach yard ONLY via the
                     explicit hand-seed lines (Dreadnought self-sac / Troll
                     swampcycle drawn to HAND). Lower bound = "selection unmodelled".
          current  — PUBLISHED model: per-turn window of (entered+1) cards from the
                     top, NON-compounding (resets each turn). What the T11/T13 used.
          compound — surveil-binning compounds: every dud you've ever binned is gone
                     from the top, so the effective dig depth is CUMULATIVE surveils.
                     Upper bound = "you aggressively bin to dig and never reset"."""
        g = self.g
        if dig == "off":
            return
        if dig == "compound":
            self.cum_entered += self.entered
            depth = min(self.cum_entered + 1, 24)
        else:
            depth = min(self.entered + 1, 12)
        i = g.ptr
        end = min(len(g.deck), g.ptr + depth)
        while i < end:
            nm = g.deck[i][0]
            if nm == "Phyrexian Dreadnought" and not self.dread_yard:
                self.dread_yard = True; g.deck.pop(i); end -= 1; continue
            if nm == "Master of Etherium" and not self.master_yard and not self.master_bf:
                self.master_yard = True; g.deck.pop(i); end -= 1; continue
            if nm == "Troll of Khazad-dûm" and not self.troll_yard:
                self.troll_yard = True; g.deck.pop(i); end -= 1; continue
            i += 1

    def drain_power(self):
        """Best repeatable Golbez drain available this end step -> (power, repeats?)."""
        best, repeats = 0, False
        if self.dread_yard:                       # recast for {1} -> always repeats
            best, repeats = 12, True
        if self.master_yard and self.arts > best:
            best, repeats = self.arts, self.loot
        if self.troll_yard and 6 > best:
            best, repeats = 6, self.loot
        return best, repeats


def goldfish_kill(library, index, rng, dig="current"):
    t = Trial(library, rng, index)
    g, tbl = t.g, t.tbl
    drained_once = False

    def cast_artifact(i, nm, rec, cost):
        g.hand.pop(i); g.avail -= cost
        if nm in ROCKS:
            out = ROCKS[nm][1]; g.rock_out += out; g.add_mana(out)
        t.art_enter(1)                              # the spell itself enters
        t.on_cast_artifact()                        # cast-triggered token/Clue makers
        if nm in CANTRIP_ART:
            t.gdraw(1)
        if nm == "Thought Monitor":
            t.gdraw(2)
        if nm in REDUCERS:
            t.reducers += 1
        if nm in GEN_TOKEN:
            t.gen_token += 1
        if nm in GEN_CLUE:
            t.gen_clue += 1
        if nm == STRIDE:
            t.stride = True
        if nm == "Matoya, Archon Elder":
            t.matoya = True
        if nm == "Skullclamp":
            t.skullclamp = True
        if nm == "Master of Etherium":
            t.master_bf = True
        if nm in LOOT:
            t.loot = True

    def cast_engine(nm, cost, power):
        g.cast(nm, cost)
        if power:
            t.new_bodies += power
        if nm in GEN_TOKEN:
            t.gen_token += 1
        if nm in GEN_CLUE:
            t.gen_clue += 1
        if nm == "Matoya, Archon Elder":
            t.matoya = True
        if nm == "Riddlesmith":
            t.loot = True
        if nm == "Basim Ibn Ishaq":
            t.basim = True

    for T in range(1, TURNS + 1):
        t.tok_cre += t.new_tok; t.new_tok = 0       # tokens mature
        t.bodies += t.new_bodies; t.new_bodies = 0
        t.entered = 0; t.draws = 0
        land = g.begin_turn(T)
        if land is not None:
            rec = index.get(land.lower())
            if rec and is_artifact_land(rec):
                t.art_enter(1)
        if t.urza:
            g.add_mana(min(t.arts, 8))              # tap artifacts for {U}, capped
        if t.onering:                               # escalating draw, once per turn
            t.ring_burden += 1; t.gdraw(t.ring_burden)
        if t.basim:                                 # historic cast every turn -> +1
            t.gdraw(1)

        if not t.golbez and g.avail >= 2:           # commander down T2 (flat {U}{B})
            g.avail -= 2; t.golbez = True

        # seed the yard cheaply: swampcycle Troll / self-sac Dreadnought
        if not t.troll_yard and g.has("Troll of Khazad-dûm") and g.avail >= 1:
            g.discard("Troll of Khazad-dûm"); g.avail -= 1; t.troll_yard = True
        if not t.dread_yard and g.has("Phyrexian Dreadnought") and g.avail >= 1:
            g.discard("Phyrexian Dreadnought"); g.avail -= 1; t.dread_yard = True
            t.entered += 1

        # high-value plays FIRST (a pilot finishes/engines over chaff): One Ring
        # (draw), Urza (Construct + tap-mana), Tezzeret (repeating all-table +2).
        if not t.onering and g.has("The One Ring") and g.avail >= 4:
            g.cast("The One Ring", 4); t.onering = True; t.art_enter(1)
            t.ring_burden = 1; t.gdraw(1)
        if not t.urza and g.has("Urza, Lord High Artificer") and g.avail >= 4:
            g.cast("Urza, Lord High Artificer", 4); t.urza = True
            t.new_tok += 1                           # the 0/0 Construct (scales = arts)
        if not t.tezz and g.has("Tezzeret, Master of the Bridge") and g.avail >= 6:
            g.cast("Tezzeret, Master of the Bridge", 6); t.tezz = True

        # deploy + draw engine: keep acting while anything is affordable
        progress = True
        while progress:
            progress = False
            # 1. cheapest affordable artifact OR non-artifact engine piece
            best = None                              # (cost, i, nm, rec, kind)
            for i, (nm, rec) in enumerate(g.hand):
                if ds.is_land(rec):
                    continue
                if nm in ENGINE_NONART:
                    cost, kind = ENGINE_NONART[nm][0], "engine"
                elif nm in ROCKS:
                    cost, kind = ROCKS[nm][0], "art"
                elif is_artifact(rec):
                    cost, kind = max(0, rec["cmc"] - t.reducers), "art"
                else:
                    continue                         # draw spells handled below
                if cost <= g.avail and (best is None or cost < best[0]):
                    best = (cost, i, nm, rec, kind)
            if best is not None:
                cost, i, nm, rec, kind = best
                if kind == "engine":
                    cast_engine(nm, cost, ENGINE_NONART[nm][1])
                else:
                    cast_artifact(i, nm, rec, cost)
                progress = True
                continue
            # 2. draw spells (incl affinity Thoughtcast)
            for nm, (floor, nd) in DRAW_SPELL.items():
                if not g.has(nm):
                    continue
                cost = max(1, 5 - t.arts) if nm == "Thoughtcast" else floor
                if g.avail >= cost:
                    g.cast(nm, cost); t.gdraw(nd); progress = True
                    break
            if progress:
                continue
            # 3. Skullclamp: sac a Thopter -> draw 2 (loops with token makers)
            if t.skullclamp and t.tok_cre >= 1 and g.avail >= 1 and t.draws < DRAW_CAP:
                g.avail -= 1; t.tok_cre -= 1; t.arts -= 1      # token dies
                t.gdraw(2)
                progress = True
                continue

        t.dig_for_fatty(dig)

        # ---- COMBAT (focus-fire, decap accelerant) -----------------------------
        thop = 1 + (1 if t.master_bf else 0) + (1 if t.stride else 0)
        combat = t.tok_cre * thop + t.bodies
        if t.urza:
            combat += t.arts                         # Construct = artifacts you control
        if t.master_bf:
            combat += t.arts                         # Master body
        if combat > 0:
            tbl.hit_focus(combat, T)
        if tbl.done:
            return tbl.decap, tbl.table

        # ---- DRAIN (hit_all, converge) -----------------------------------------
        if t.tezz and t.arts >= 1:                   # Tezzeret +2: X = arts to each opp
            tbl.hit_all(t.arts, T)
        if t.golbez and t.arts >= 8:                 # Golbez end-step drain
            power, repeats = t.drain_power()
            if power > 0 and (repeats or not drained_once):
                tbl.hit_all(power, T)
                drained_once = True
        if tbl.done:
            return tbl.decap, tbl.table

    return tbl.decap, tbl.table


def mode_clock(index, aliases, trials):
    print(f"\n### CLOCK — Crystal Sickness kill-turn goldfish   trials={trials} seed={SEED}")
    print("    Golbez drain + Tezzeret +2 hit ALL opponents (converge); Urza Construct")
    print("    + Thopters focus-fire (diverge). decap = first dead / table = all three.\n")
    library, commander = slc.load_parsed(DECK, index, aliases)
    rng = random.Random(SEED)
    res = [goldfish_kill(library, index, rng) for _ in range(trials)]

    print("  P(kill <= turn T) %".ljust(40) + "".join(f"{t:>6}" for t in SHOW))
    print(slc.row("decap (one opponent, 40)", slc.cum(res, 0, SHOW), SHOW))
    print(slc.row("table (all three)", slc.cum(res, 1, SHOW), SHOW))
    never_d = 100.0 * sum(1 for d, _ in res if d is None) / trials
    never_t = 100.0 * sum(1 for _, x in res if x is None) / trials
    print(f"\n  median decap {slc.median(res, 0)}   median table {slc.median(res, 1)}"
          f"   ·   never-in-{TURNS}: decap {never_d:.0f}% / table {never_t:.0f}%")
    print("\n  Claimed in Summary: Goldfish T7-9. Front-edge T7 odds above are the test.")


def mode_digtest(index, aliases, trials):
    """Sensitivity of the clock to how Golbez's SURVEIL dig is modelled.
    Brackets the published 'current' regime between dig OFF (selection unmodelled,
    the Glarb-lab failure mode) and dig COMPOUND (surveil-binning compounds). If
    off ~= current ~= compound, the deck is development-gated and selection is a
    Grand-Design-style red herring; if the spread is wide, the clock is sensitive
    to the surveil model and the published number is fragile."""
    print(f"\n### DIGTEST — Crystal Sickness surveil-dig sensitivity   trials={trials} seed={SEED}")
    print("    Does modelling Golbez's surveil harder move the clock, or is the deck")
    print("    development-gated (8 artifacts) so selection is a red herring?\n")
    library, commander = slc.load_parsed(DECK, index, aliases)
    print("  regime".ljust(14) + "  decap   table   |  T<=7 decap  T<=7 table  never-table")
    for dig in ("off", "current", "compound"):
        rng = random.Random(SEED)
        res = [goldfish_kill(library, index, rng, dig=dig) for _ in range(trials)]
        d7 = 100.0 * sum(1 for d, _ in res if d is not None and d <= 7) / trials
        t7 = 100.0 * sum(1 for _, x in res if x is not None and x <= 7) / trials
        nt = 100.0 * sum(1 for _, x in res if x is None) / trials
        md = slc.median(res, 0).replace(" (never in horizon)", "")
        mt = slc.median(res, 1).replace(" (never in horizon)", "")
        tag = " (PUBLISHED)" if dig == "current" else ""
        print(f"  {dig.ljust(12)}  {md:>5}   {mt:>5}   |  {d7:8.0f}%  {t7:9.0f}%  {nt:9.0f}%{tag}")
    print("\n  Read: if 'current' sits near 'off', surveil isn't the bottleneck "
          "(development-gated);\n  if 'compound' is much faster than 'current', the "
          "published clock under-credits the dig.")


if __name__ == "__main__":
    slc.run_cli(__doc__, {"clock": mode_clock, "digtest": mode_digtest}, default_trials=40000)
