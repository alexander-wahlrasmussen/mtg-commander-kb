#!/usr/bin/env python3
"""lor_clock_lab.py — Lorehold Spirits (Quintorius, History Chaser) KILL-TURN goldfish.

Kill-Window Lab Sweep, deck 7 (proposals/Kill_Window_Lab_Sweep_2026-06-13.md).
Summary claims "Goldfish T7-9 (fastest T6, avg T8)". Built on speed_lab_core.py.
Commander is a PLANESWALKER (mana-gate the cast, not g.has — the ebm gotcha).

KILL SHAPE — MIXED. Per the carried prior: predict decap off the focused/combo axis,
let the hit_all ping set the (slower) table:

  COMBO  (kill_all)   Reveillark + Karmic Guide + Goblin Bombardment + a power<=2
                      creature in yard = unbounded sac loop (arbitrary GB damage +
                      arbitrary Spirit tokens). Decap=table by construction WHEN it
                      lands, but a 3-singleton assembly so it's a minority/late line.
  COMBAT (focus)      Quintorius -4 (Spirits gain double strike + vigilance) + anthems
                      (Patchwork / Balefire / Hofri / Field Historian) + Moonshaker
                      Cavalry / Akroma's Will. Focus-fires one player -> decap leads.
  PING   (hit_all)    Purphoros (2 to EACH opp per Spirit/creature ETB), scaling with
                      recursion events/turn x Anointed Procession. Converge, slower.
  CHIP   (focus)      Balefire Liege 3 to one opp per RED spell cast; Boros Charm 4.

Engine, oracle-verified (card_lookup.py 2026-06-13):
  * Quintorius HC (PW): static "whenever one or more cards LEAVE your graveyard, make
    a 3/2 Spirit" — ONE token per event regardless of how many cards leave. +1 fills
    yard (discard, draw 2, mill); -4 gives Spirits double strike+vig (loyalty starts 3,
    so -4 is available the turn after a +1: modelled as ult-ready once out >=1 turn).
  * Each recursion piece returning a card from yard = 1 static event = 1 Spirit (x2 w/
    Anointed Procession). Quintorius Field Historian is a 2nd static (events make 2).
  * Purphoros: 2 to each opp per OTHER creature ETB; indestructible non-creature at red
    devotion < 5 (usual here) so it pings but does not attack.
  * Combo loop is unbounded with GB; CORRECTION to the Summary's Line 6 text — Karmic
    Guide has ECHO, not persist; the loop runs off Reveillark's leave-trigger returning
    KG + a <=2 creature and KG's ETB returning Reveillark, not a persist counter.

HEURISTIC, not a rules engine. Mana = lands + rocks (+Smothering Tithe ~+1/turn) floor.
recursion events/turn ~= repeatable engines online + one-shot pulses, capped (assumes the
+1 keeps the yard fuelled). Spirit power = 3 + anthems (Patchwork +1, Balefire +2 [red&
white], Hofri +1, Field Historian +1). Combat focus, doubled under -4 / Akroma double
strike; Moonshaker adds +ncre/+ncre. Combo fires kill_all when its 3 pieces are on the
battlefield with a body for fodder. Trust SHAPE + front edge, not the 2nd decimal.

OMITTED (conservative, slow-bias): Hofri death-token copies, Staff/Tocasia draw, Venerable
combat-damage recursion chains, Emeria/Mistveil/Sun-Titan-attack extra recursions, Teshar
historic chains, Balefire white-cast lifegain. OPTIMISTIC: rocks tap turn they land; no
interaction / static-40 table; recursion always has yard fuel.

Data: collection/oracle-cards.json   ·   Writeup: proposals/Lorehold_Spirits_Clock_Lab_2026-06-13.md
"""
import importlib.util
import random
from pathlib import Path

ROOT = Path(__file__).parent.parent
_spec = importlib.util.spec_from_file_location("speed_lab_core", Path(__file__).parent / "speed_lab_core.py")
slc = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(slc)
ds = slc.ds

DECK = ROOT / "decks" / "lorehold-spirit-20260503-154449.txt"
SEED = 20260613
TURNS = 14
SHOW = [5, 6, 7, 8, 9, 10, 12, 14]

ROCKS = {"Sol Ring": (1, 2), "Arcane Signet": (2, 1), "Mind Stone": (2, 1),
         "Fellwar Stone": (2, 1), "Mox Amber": (0, 1), "Patchwork Banner": (3, 1)}

REPEAT_RECUR = {"Sun Titan", "Serra Paragon", "Teshar, Ancestor's Apostle",
                "Venerable Warsinger"}                 # ~1 recursion event/turn each
ONESHOT_RECUR = {"Karmic Guide", "Reveillark", "Sevinne's Reclamation",
                 "Angel of Indemnity", "Relic Retriever", "Advanced Reconstruction"}
PAYOFFS = {"Purphoros, God of the Forge", "Anointed Procession", "Balefire Liege",
           "Hofri Ghostforge", "Quintorius, Field Historian", "Staff of the Storyteller",
           "Tocasia's Welcome"}
COMBO = {"Reveillark", "Karmic Guide", "Goblin Bombardment"}
ANTHEMS = {"Patchwork Banner": 1, "Balefire Liege": 2, "Hofri Ghostforge": 1,
           "Quintorius, Field Historian": 1}
DEPLOYABLE = REPEAT_RECUR | ONESHOT_RECUR | PAYOFFS | COMBO | {
    "Moonshaker Cavalry", "Goblin Bombardment", "Patchwork Banner"}


class Trial:
    def __init__(self, library, rng):
        self.g = slc.Goldfish(library, rng, rocks=ROCKS)
        self.tbl = slc.Table()
        self.bf = set()
        self.quint = False           # commander PW on battlefield
        self.quint_turn = None       # turn it landed (for -4 loyalty timing)
        self.spirits = 0             # 3/2 Spirit tokens
        self.bodies = 0              # nontoken creatures (recursion engines etc.)
        self.tithe = False           # Smothering Tithe -> ~+1 mana/turn
        self._T = 0

    @property
    def statics(self):
        return (1 if self.quint else 0) + (1 if "Quintorius, Field Historian" in self.bf else 0)

    @property
    def anthem(self):
        return sum(v for nm, v in ANTHEMS.items() if nm in self.bf)

    @property
    def ncre(self):
        return self.spirits + self.bodies

    @property
    def combo_ready(self):
        return COMBO <= self.bf and self.ncre >= 1     # need a creature as fodder

    def recur_events(self, T):
        """Graveyard-leaving events this turn = repeatable engines online + one-shots
        deployed this turn (tracked via _oneshot_pulse). +1 keeps the yard fuelled."""
        rep = sum(1 for nm in REPEAT_RECUR if nm in self.bf)
        return min(rep + self._oneshot_pulse, 6)

    def turn(self, T):
        self._T = T
        g, tbl = self.g, self.tbl
        self._oneshot_pulse = 0
        g.begin_turn(T)
        g.deploy_rocks()
        if self.tithe:
            g.add_mana(1)
        # commander first (PW: mana-gate, not g.has), then engine cheapest-first
        if not self.quint and g.avail >= 4:
            g.avail -= 4; self.quint = True; self.quint_turn = T
        # Quintorius +1 (discard 1, draw 2, mill 1): the deck's dig engine — net a card
        # AND fuels the yard for recursion. Models the consistency that finds pieces.
        # (+1 and -4 are exclusive; on the actual kill turn the draw is harmless.)
        if self.quint:
            g.draw(2)
        progress = True
        while progress:
            progress = False
            cands = sorted(((i, r["cmc"], nm) for i, (nm, r) in enumerate(g.hand)
                            if nm in DEPLOYABLE or nm == "Smothering Tithe"),
                           key=lambda x: x[1])
            for i, cmc, nm in cands:
                if g.avail >= cmc:
                    g.hand.pop(i); g.avail -= cmc; self.bf.add(nm)
                    if nm == "Smothering Tithe":
                        self.tithe = True
                    if nm in ONESHOT_RECUR:
                        self._oneshot_pulse += 1
                    # nontoken creature bodies (recursion engines + combo creatures)
                    if nm in (REPEAT_RECUR | {"Karmic Guide", "Reveillark",
                              "Angel of Indemnity", "Quintorius, Field Historian",
                              "Hofri Ghostforge", "Balefire Liege"}):
                        self.bodies += 1
                    progress = True
                    break

        # ---- token production: recursion events -> static triggers -> Spirits ----
        events = self.recur_events(T)
        mult = 2 if "Anointed Procession" in self.bf else 1
        spirits_new = events * self.statics * mult if self.quint else 0
        self.spirits += spirits_new
        # Purphoros: 2 to each opp per creature ETB (Spirits + returned bodies), hit_all
        if "Purphoros, God of the Forge" in self.bf:
            tbl.hit_all(2 * (spirits_new + events), T)        # events ~ returned creatures
        # Balefire chip: ~1 red spell cast/turn -> 3 to one opp
        if "Balefire Liege" in self.bf:
            tbl.hit_focus(3, T)
        if tbl.done:
            return

        # ---- combo: unbounded GB loop -> kill_all -------------------------------
        if self.combo_ready:
            tbl.kill_all(T)
            return

        # ---- combat (focus): Spirits x power, doubled under -4 / Akroma ----------
        if self.quint and self.ncre >= 1:
            spow = 3 + self.anthem
            board_pow = self.spirits * spow + self.bodies * 2
            # Moonshaker Cavalry ETB: +ncre/+ncre to all (cast this turn for the alpha)
            if g.has("Moonshaker Cavalry") and g.avail >= 8:
                g.cast("Moonshaker Cavalry", 8)
                self.bodies += 1
                board_pow += (self.ncre) * self.ncre + 6      # +X/+X on all + the 6/6
            # double strike: Quintorius -4 (loyalty ready ~1 turn after landing) or Akroma
            ds_on = (self.quint_turn is not None and T > self.quint_turn)
            if g.has("Akroma's Will") and g.avail >= 4:
                g.cast("Akroma's Will", 4); ds_on = True
            if ds_on:
                board_pow *= 2
            tbl.hit_focus(board_pow, T)
        if tbl.done:
            return
        # Boros Charm 4-damage finisher (focus)
        if g.has("Boros Charm") and g.avail >= 2:
            g.cast("Boros Charm", 2); tbl.hit_focus(4, T)


def mode_clock(index, aliases, trials):
    print(f"\n### CLOCK — Lorehold Spirits kill-turn goldfish   trials={trials} seed={SEED}")
    print("    decap = first opponent dead (40) · table = all three. Combo=kill_all (converge),")
    print("    combat+Balefire focus the decap, Purphoros ping is hit_all. MIXED shape.\n")
    library, commander = slc.load_parsed(DECK, index, aliases)
    rng = random.Random(SEED)
    res = slc.run_goldfish(lambda: Trial(library, rng), trials, TURNS)
    slc.report_clock(res, SHOW, TURNS, trials)
    print("\n  Claimed in Summary: Goldfish T7-9 (fastest T6, avg T8). Front-edge odds are the test.")


if __name__ == "__main__":
    slc.run_cli(__doc__, {"clock": mode_clock}, default_trials=40000)
