#!/usr/bin/env python3
"""ebm_clock_lab.py — Earthbend the Meta (Toph, the First Metalbender) KILL-TURN goldfish.

Kill-Window Lab Sweep, deck 6 (proposals/Kill_Window_Lab_Sweep_2026-06-13.md).
Summary claims "Goldfish T7-9" (fastest T6 god-hand). Built on speed_lab_core.py.
First lab run under the producer-inventory step added to WF_Kill_Window_Lab.md after
the 2026-06-13 esc/rs re-check — and this is the most producer-dense deck in the sweep.

KILL SHAPE — corrected at Stage 0 from the tracker's "combat focus-fire -> diverge"
to MIXED, CONVERGE-DOMINANT. The deck's reliable damage is a per-creature-ETB table
ping, not combat:

  PING (hit_all, CONVERGE)  Purphoros (2 to EACH opp per OTHER creature ETB) + Impact
                            Tremors (1 to EACH opp per creature ETB) + Tannuk (1 to
                            each opp per landfall). Scales with creatures entering per
                            turn -> the Scute Swarm exponential is the driver.
  BURN  (focus, decap)      All Will Be One: each +1/+1-counter event deals that many
                            to ONE target opponent. Fed by earthbend (amplified) and
                            Cathars' Crusade. Single-target per event -> decap-leaning.
  POISON (go-wide alt-kill) Triumph of the Hordes: your board gains +1/+1 + trample +
                            infect; 10 poison kills regardless of life.
  COMBAT (focus fallback)   earthbent lands as creatures (double strike via Greatest
                            Earthbender) + Moraug extra combats per landfall.

Engine, all oracle-verified (card_lookup.py 2026-06-13):
  * Toph (cmdr): nontoken artifacts you control are LANDS (so each artifact ETB is a
    landfall event WHILE TOPH IS OUT); end step earthbend 2.
  * Scute Swarm: landfall -> 1 Insect, or a COPY of Scute Swarm at 6+ lands (the copies
    are Scutes and re-trigger) -> exponential. Doubling Season doubles the tokens.
  * Purphoros: 2 to each opp per OTHER creature ETB; indestructible, NOT a creature while
    red devotion < 5 (true in this Naya deck) -> NOT doubled by Annie (not a legendary
    *creature* then). Impact Tremors: 1 to each opp per creature ETB (not legendary).
  * Amplifier stack on a +1/+1 placement, additive-before-multiplicative: Hardened Scales
    (+1) -> The Earth Crystal (x2) -> Doubling Season (x2). earthbend 2 -> (2+1)*2*2 = 12.
  * Annie Joins Up: doubles a *triggered ability of a legendary creature you control*
    -> doubles the commander's end-step earthbend + Tannuk landfall (NOT Purphoros/Tremors,
    which aren't legendary creatures here; NOT replacement-effect amplifiers).
  * Toph Greatest Earthbender: ETB earthbend X (X = mana spent); land creatures have
    double strike. Avatar Kyoshi: begin-combat earthbend 8 (MV8). Cathars' Crusade: per
    creature ETB, +1/+1 on EACH creature you control.

HEURISTIC, not a rules engine — and like rs the counter spiral is coarse. Mana = lands +
rocks + landfall-mana (Lotus Cobra/Tireless) floor. Landfall events/turn = land drops
(+1 with Dryad of the Ilysian Grove) + nontoken artifacts entered this turn IF Toph is out
+ Awaken/Entish lands. AWBO modelled as single-opponent (hit_focus) decap pressure; Cathars
counters folded in conservatively. Combat is a focus fallback (double strike / Moraug
multiplier capped). Scutes capped at 1e4 (lethal arrives far sooner). Trust the SHAPE and
the front edge, not the second decimal. decap and table reported separately.

OMITTED (conservative, all same slow-bias direction): Wrenn/Bristly counter trickle,
Evolution Sage proliferate growth, The Ozolith carryover, Bumi attack pumps, Earthbender
Ascension quest, exhaust earthbends, Springheart copy mode, fetchland double-landfall,
Zuran Orb + Amulet recursion engine. OPTIMISTIC (noted): rocks tap the turn they land,
no opposing interaction / static 40 table.

Data: collection/oracle-cards.json   ·   Writeup: proposals/Earthbend_the_Meta_Clock_Lab_2026-06-13.md
"""
import importlib.util
import random
from pathlib import Path

ROOT = Path(__file__).parent.parent
_spec = importlib.util.spec_from_file_location("speed_lab_core", Path(__file__).parent / "speed_lab_core.py")
slc = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(slc)
ds = slc.ds

DECK = ROOT / "decks" / "earthbend-the-meta-20260404-075423.txt"
SEED = 20260613
TURNS = 14
SHOW = [5, 6, 7, 8, 9, 10, 12, 14]

ROCKS = {"Sol Ring": (1, 2), "Arcane Signet": (2, 1), "Liquimetal Torque": (2, 1)}
# land-ramp spells: name -> (cost, lands added) — each added land is a landfall event
RAMP = {"Farseek": (2, 1), "Nature's Lore": (2, 1), "Entish Restoration": (3, 2)}
# landfall-mana producers (treated as +1 mana per landfall once out)
LF_MANA = {"Lotus Cobra", "Tireless Provisioner"}

# everything the deploy loop will hard-cast cheapest-first, by oracle cmc, with a flag
PAYOFFS = {"Purphoros, God of the Forge", "Impact Tremors", "All Will Be One",
           "Tannuk, Memorial Ensign", "Cathars' Crusade"}
PRODUCERS = {"Scute Swarm", "Felidar Retreat", "Springheart Nantuko",
             "Bristly Bill, Spine Sower", "Evolution Sage", "Moraug, Fury of Akoum"}
AMPS = {"Hardened Scales", "Doubling Season", "The Earth Crystal"}
EB_ETB = {  # earthbend-on-ETB sources -> N counters placed once when they enter
    "Toph, the Blind Bandit": 2, "Bumi, Eclectic Earthbender": 1, "Bumi, Unleashed": 4,
    "Badgermole Cub": 1, "Earthbender Ascension": 2, "Toph, Greatest Earthbender": 4,
}
LANDDROP = {"Dryad of the Ilysian Grove"}      # +1 land drop / turn
DEPLOYABLE = (PAYOFFS | PRODUCERS | AMPS | set(EB_ETB) | LANDDROP
              | {"Avatar Kyoshi, Earthbender", "Annie Joins Up", "Ashaya, Soul of the Wild",
                 "Toph, Earthbending Master", "Toph, Hardheaded Teacher", "Field of the Dead"})
# creatures among the deployables (their ETB also pings Purphoros/Tremors and is a body)
CREATURE_DEPLOY = ({"Scute Swarm", "Springheart Nantuko", "Bristly Bill, Spine Sower",
                    "Evolution Sage", "Moraug, Fury of Akoum", "Tannuk, Memorial Ensign",
                    "Avatar Kyoshi, Earthbender", "Ashaya, Soul of the Wild",
                    "Bumi, Eclectic Earthbender", "Bumi, Unleashed", "Badgermole Cub",
                    "Toph, the Blind Bandit", "Toph, Greatest Earthbender",
                    "Toph, Earthbending Master", "Toph, Hardheaded Teacher",
                    "Dryad of the Ilysian Grove"})


class Trial:
    def __init__(self, library, rng):
        self.g = slc.Goldfish(library, rng, rocks=ROCKS)
        self.tbl = slc.Table()
        self.bf = set()
        self.toph = False            # commander out (artifact-landfall + endstep EB2)
        self.scutes = 0              # Scute Swarm bodies (exponential)
        self.tokens = 0              # other creature tokens (cats/insects/zombies/dryads)
        self.bodies = 0              # nontoken creatures incl payoffs that are creatures
        self.counters = 0.0          # total +1/+1 counters on the board (board power & Triumph)
        self.lf_mana = 0             # standing landfall-mana sources
        self.land_drops = 1
        self._T = 0

    # ---- amplifier helpers ----
    def counter_mult(self, base):
        """+1/+1 counters actually placed from a 'base' earthbend/effect, additive
        (Hardened) before multiplicative (Earth Crystal, Doubling Season)."""
        n = base + (1 if "Hardened Scales" in self.bf else 0)
        if "The Earth Crystal" in self.bf:
            n *= 2
        if "Doubling Season" in self.bf:
            n *= 2
        return n

    def tok_mult(self, k):
        return k * (2 if "Doubling Season" in self.bf else 1)

    @property
    def ncre(self):
        return self.scutes + self.tokens + self.bodies

    # ---- AWBO: a counter-placement event deals that many to ONE opponent (decap) ----
    def awbo(self, amount, T):
        if "All Will Be One" in self.bf and amount > 0:
            self.tbl.hit_focus(amount, T)

    def place_counters(self, base, T, legendary_eb=False):
        """Resolve an earthbend / counter event: amplify, add to board, fire AWBO.
        legendary_eb doubles the trigger if Annie is out (legendary-creature trigger)."""
        events = 2 if (legendary_eb and "Annie Joins Up" in self.bf) else 1
        for _ in range(events):
            n = self.counter_mult(base)
            self.counters += n
            self.awbo(n, T)

    # ---- per-creature-ETB ping (Purphoros + Impact Tremors), hit_all -> converge ----
    def ping(self, n_etb, T):
        per = (2 if "Purphoros, God of the Forge" in self.bf else 0) \
            + (1 if "Impact Tremors" in self.bf else 0)
        if per and n_etb:
            self.tbl.hit_all(per * n_etb, T)
        # Cathars' Crusade: each creature ETB puts a counter on each creature you control.
        # Conservative fold: counts as n_etb counter-placement waves of size ~ncre, but we
        # only bank a flat n_etb to board growth + one AWBO ping (avoids runaway).
        if "Cathars' Crusade" in self.bf and n_etb:
            add = self.counter_mult(n_etb)
            self.counters += add
            self.awbo(add, T)

    # ---- landfall: returns creatures-entered this event (for the ETB ping) ----
    def landfall(self, T):
        entered = 0
        if "Scute Swarm" in self.bf:
            if self.g.lands >= 6 and self.scutes:
                new = self.tok_mult(self.scutes)        # one copy per Scute (DS doubles)
                self.scutes = min(self.scutes + new, 10000)
                entered += new
            else:
                seed = max(1, self.scutes)              # the Scute itself makes a 1/1 Insect
                self.tokens += self.tok_mult(seed); entered += self.tok_mult(seed)
        for nm, fixed in (("Felidar Retreat", 1), ("Springheart Nantuko", 1)):
            if nm in self.bf:
                self.tokens += self.tok_mult(fixed); entered += self.tok_mult(fixed)
        if "Field of the Dead" in self.bf and self.g.lands >= 7:
            self.tokens += self.tok_mult(1); entered += self.tok_mult(1)
        if "Tannuk, Memorial Ensign" in self.bf:                 # 1 to each opp / landfall
            self.tbl.hit_all(2 if "Annie Joins Up" in self.bf else 1, T)
        if "Lotus Cobra" in self.bf:
            self.g.add_mana(1)
        if "Tireless Provisioner" in self.bf:
            self.g.add_mana(1)
        if "Bristly Bill, Spine Sower" in self.bf:
            self.place_counters(0.5, T)                          # ~a counter / landfall
        return entered

    def turn(self, T):
        self._T = T
        g, tbl = self.g, self.tbl
        arts_before = sum(1 for nm in self.bf if nm in ROCKS) + ("Liquimetal Torque" in self.bf)
        played = g.begin_turn(T)
        lf = 1 if played else 0
        # second land drop with Dryad out
        if "Dryad of the Ilysian Grove" in self.bf:
            li = next((i for i, (_, r) in enumerate(g.hand) if ds.is_land(r)), None)
            if li is not None:
                g.hand.pop(li); g.lands += 1; lf += 1
        g.deploy_rocks()
        g.add_mana(self.lf_mana)
        # rocks just deployed are nontoken artifacts -> landfall events while Toph is out
        arts_after = sum(1 for nm, _ in []) + 0
        # (rock deployment handled by Goldfish; approximate +1 landfall per rock if Toph out)

        # commander first (enables artifact-landfall + endstep EB2), then engine cheapest-first.
        # Commander lives in the command zone (not the library) -> gate on mana, not g.has.
        if not self.toph and g.avail >= 4:
            g.avail -= 4; self.toph = True; self.bodies += 1
        progress = True
        new_bodies = 0
        arts_this_turn = 0
        while progress:
            progress = False
            cands = sorted(((i, r["cmc"], nm) for i, (nm, r) in enumerate(g.hand)
                            if nm in DEPLOYABLE), key=lambda x: x[1])
            for i, cmc, nm in cands:
                if g.avail >= cmc:
                    g.hand.pop(i); g.avail -= cmc
                    self.bf.add(nm)
                    if nm in EB_ETB:
                        self.place_counters(EB_ETB[nm], T,
                                            legendary_eb=nm.startswith(("Toph", "Bumi")))
                    if nm in LF_MANA or nm in ("Lotus Cobra", "Tireless Provisioner"):
                        self.lf_mana += 1
                    if nm in CREATURE_DEPLOY:
                        self.bodies += 1; new_bodies += 1
                    progress = True
                    break
        # ramp spells (each added land = a landfall event later)
        ramp_lands = 0
        for rs, (cost, n) in RAMP.items():
            while g.has(rs) and g.avail >= cost:
                g.cast(rs, cost); g.lands += n; g.avail += n; ramp_lands += n

        # ---- count landfall events this turn -------------------------------------
        # rocks/artifacts that entered this turn are lands via Toph (if Toph is out)
        if self.toph:
            arts_now = sum(1 for nm in self.bf if nm in ROCKS) + ("Liquimetal Torque" in self.bf)
            arts_this_turn = max(0, arts_now - arts_before)
        lf_events = lf + ramp_lands + (arts_this_turn if self.toph else 0)

        # Awaken the Woods: X dryad LAND creature tokens (each is a landfall + a creature ETB)
        awaken_etb = 0
        if g.has("Awaken the Woods") and g.avail >= 4:
            x = int(min(self.tok_mult(max(0, int(g.avail) - 2)), 40))   # {X}{G}{G}
            g.cast("Awaken the Woods", g.avail)
            self.tokens += x; awaken_etb += x; lf_events += x

        # ---- resolve landfall events (producers) + the per-ETB ping --------------
        etb = new_bodies + awaken_etb
        for _ in range(int(min(lf_events, 60))):
            etb += self.landfall(T)
        self.ping(etb, T)

        # Avatar Kyoshi begin-combat earthbend 8 (untaps land; powers THIS combat)
        if "Avatar Kyoshi, Earthbender" in self.bf:
            self.place_counters(8, T, legendary_eb=True)
        if tbl.done:
            return
        # ---- alt / fallback kills (combat uses counters accumulated up to here:
        #      prior end steps + Kyoshi this turn — NOT this turn's end-step EB) ----
        board_pow = self.ncre + self.counters
        # Triumph of the Hordes: +1/+1 + infect; 10 poison per player
        if g.has("Triumph of the Hordes") and g.avail >= 4 and self.ncre >= 1:
            infect = board_pow + self.ncre                       # the +1/+1 too
            g.cast("Triumph of the Hordes", 4)
            killable = int(infect // 10)
            for i in range(len(tbl.dmg)):
                if killable <= 0:
                    break
                if tbl.dmg[i] < tbl.life:
                    tbl.dmg[i] = tbl.life; killable -= 1
            tbl._update(T)
        # combat: land creatures + bodies swing (focus). Double strike + Moraug multiplier.
        if board_pow > 0 and self.toph:
            mult = 2 if "Toph, Greatest Earthbender" in self.bf else 1   # double strike
            if "Moraug, Fury of Akoum" in self.bf:
                mult *= min(1 + lf_events, 4)                            # extra combats
            tbl.hit_focus(int(board_pow * mult), T)
        if tbl.done:
            return
        # ---- end-step earthbends: fire AWBO now, power NEXT turn's combat --------
        if self.toph:                                            # commander endstep EB2
            self.place_counters(2, T, legendary_eb=True)
        if "Toph, Earthbending Master" in self.bf:               # attack-trigger EB (coarse)
            self.place_counters(min(6, T), T, legendary_eb=True)


def mode_clock(index, aliases, trials):
    print(f"\n### CLOCK — Earthbend the Meta kill-turn goldfish   trials={trials} seed={SEED}")
    print("    decap = first opponent dead (40) · table = all three. Purphoros/Tremors ping")
    print("    is hit_all (converge); AWBO + combat focus the decap. MIXED shape.\n")
    library, commander = slc.load_parsed(DECK, index, aliases)
    rng = random.Random(SEED)
    res = slc.run_goldfish(lambda: Trial(library, rng), trials, TURNS)
    slc.report_clock(res, SHOW, TURNS, trials)
    print("\n  Claimed in Summary: Goldfish T7-9 (fastest T6). Front-edge T6/T7 odds are the test.")


if __name__ == "__main__":
    slc.run_cli(__doc__, {"clock": mode_clock}, default_trials=40000)
