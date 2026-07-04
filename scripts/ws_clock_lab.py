#!/usr/bin/env python3
"""ws_clock_lab.py — KILL-TURN goldfish for the World Shapers precon (EOC, Hearthhull,
the Worldseed) and its owned-only 19-swap upgrade (2026-07-04 evaluation:
"if I buy the precon, can free collection cards make it pod-competitive?").

DECKS (both parse via deck_registry EXTRA_COMMANDERS):
  stock    decks/considering/world-shapers-precon-20260704.txt    (the box, as sold)
  upgraded decks/considering/world-shapers-upgraded-20260704.txt  (19 swaps, all cards
           verified FREE = owned minus deployed > 0 on moxfield_haves_2026-06-25; GCs
           exactly 3/3: Natural Order, Gamble, Mana Vault)

KILL SHAPE (find_combos 2026-07-04 + every encoded card card_lookup-verified — the
CLAUDE.md hard rule; Hearthhull's station-gating verified off the printed card image):

  PRIMARY (upgraded only) — the Mazirek loop [CSB 317-5641, COMPLETE in the list]:
    Mazirek, Kraul Death Priest ("whenever a player sacrifices ANOTHER permanent, put a
    +1/+1 counter on each creature you control") + Basking Broodscale ("whenever one or
    more +1/+1 counters are put on this creature, you may create a 0/1 Eldrazi Spawn
    token with 'Sacrifice this token: Add {C}'").
    IGNITION = the first counter on Broodscale: any sacrifice while both are out (fetch
    crack, Hearthhull's land-sac draw, Woe Strider's free outlet, Korvold's attack sac)
    or, failing those, Broodscale's own adapt {1}{G} (legal only while counterless).
    Loop: sac Spawn -> {C} + Mazirek counter -> new Spawn. Infinite colorless mana,
    infinite sac triggers, infinite +1/+1 counters (CSB agrees).
    CONVERTERS to a table kill the same turn:
      Mayhem Devil on board  (1 dmg per sacrifice -> infinite pings)
      Jarad, Golgari Lich Lord on board ({1}{B}{G}, sac a loop-pumped creature: each
        opponent loses its power — activation paid from loop mana, colour-blind waiver)
      Exsanguinate in hand   ({X}{B}{B} with X from the infinite {C})
      Worldsoul's Rage in hand = DECAP only (X to ONE target); table follows next combat.
    No converter -> the loop still leaves arbitrarily many pumped Spawn tokens: the
    NEXT turn's unblocked combat tables (kill_all at T+1).

  FLOOR (both lists) — landfall/battlecruiser combat, the precon's native plan:
    creatures cast biggest-first attack unblocked (ceiling); Omnath, Locus of Rage
    (5/5 per landfall) / Rampaging Baloths (4/4, stock) / Titania (5/3 per land DEATH) /
    Ob Nixilis, the Fallen (target player loses 3 per landfall, upgraded) / Moraug
    (one extra combat per land entering on our main phase — damage x(1+lands_in)) /
    Baloth Prime (stock; enters w/ 6 stun counters, land-sacs untap it + make 4/4s) /
    Mayhem Devil pings each sacrifice. Splendid Reclamation / Aftermath Analyst return
    the whole land graveyard (mass landfall). Hearthhull: 2+ station = {1},T, sac a
    land: draw 2 + extra land play (the engine); the "sacrifice a land -> each opponent
    loses 2" drain sits INSIDE the 8+ box (printed-card check 2026-07-04 — it is NOT
    always-on), so it only ticks once the ship stations to 8, modelled as spending one
    whole combat step's worth of untapped power (>=8) to station.

DIG / RECURSION MODELLED: Hearthhull draw engine, Night's Whisper, Satyr Wayfinder,
Aftermath Analyst mill, Gitrog draw-per-land-binned-event, Korvold draw-per-sacrifice,
Life from the Loam (yard lands -> hand), Crucible/Ramunap/Conduit/Icetill single land
replay, extra land drops (Gitrog/Oracle/Icetill), ramp suite (Farseek, Nature's Lore,
Cultivate, Skyshroud Claim, Harrow, Roiling Regrowth, Springbloom Druid), tutors
(Natural Order -> Mazirek only — Broodscale is DEVOID, not a green card; Gamble -> any
missing combo bit, with the honest random-discard risk; Victimize -> both pieces from
the yard, needing a body to sac).

OPTIMISTIC (ceiling, as every lab): unblocked combat, no opposing interaction, colour-
blind mana (lands+rocks floor; Jarad/Exsanguinate colour costs waived vs loop {C}),
fetches crack instantly (tapped-land timing ignored), Moraug multiplier is
1+lands-entered, station-8 costs one skipped combat rather than exact tap math.
OMITTED (conservative): Escape to the Wilds, Valakut Exploration, Augur/Oracle top-play,
Braids, Tireless Tracker clues, Wrenn and Six, Meren end-step recursion, Szarel counters,
Exploration Broodship, Loam dredge, Woe Strider escape, all removal (goldfish-inert),
Veil of Summer (protection — matters in pods, invisible here). Trust shapes and deltas.

Run:  python scripts/ws_clock_lab.py --trials 40000
      --mode clock   upgraded list (the primary question)
      --mode stock   the box as sold (baseline)
      --mode levers  upgrade decomposition (combo package vs GC tutors vs full)
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
DECK_UP = ROOT / "decks" / "considering" / "world-shapers-upgraded-20260704.txt"
DECK_ST = ROOT / "decks" / "considering" / "world-shapers-precon-20260704.txt"
SEED = 20260704
TURNS = 16
SHOW = [5, 6, 7, 8, 9, 10, 12, 14, 16]

ROCKS = {"Sol Ring": (1, 2), "Arcane Signet": (2, 1), "Mana Vault": (1, 3)}

# lands that sacrifice themselves to fetch (crack-on-sight model: +1 net land,
# 2 landfall events, 1 land-sacrifice event, the shell to the yard)
FETCHES = {"Evolving Wilds", "Fabled Passage", "Terramorphic Expanse", "Mountain Valley",
           "Rocky Tar Pit", "Myriad Landscape", "Escape Tunnel",
           "Cabaretti Courtyard", "Maestros Theater", "Riveteers Overlook"}

RAMP = {  # name -> (cost, lands_gained, untapped_mana_now, sacs_a_land_first)
    "Farseek": (2, 1, 0, False), "Nature's Lore": (2, 1, 1, False),
    "Cultivate": (3, 1, 0, False), "Skyshroud Claim": (4, 2, 2, False),
    "Harrow": (3, 2, 2, True), "Roiling Regrowth": (3, 2, 0, True),
}
EXTRA_DROP = {"The Gitrog Monster", "Oracle of Mul Daya", "Icetill Explorer"}
GY_LAND_ENGINE = {"Crucible of Worlds", "Ramunap Excavator", "Conduit of Worlds",
                  "Icetill Explorer"}
COMBO = {"Mazirek, Kraul Death Priest": 5, "Basking Broodscale": 2}
CONVERTER_BD = {"Mayhem Devil": 3, "Jarad, Golgari Lich Lord": 4}
# cheap GREEN bodies (card colour, not identity) a pilot would feed Natural Order,
# plus the green token names this model creates. Broodscale is devoid -> illegal.
GREEN_FODDER = {"Satyr Wayfinder", "Springbloom Druid", "Aftermath Analyst",
                "Augur of Autumn", "Icetill Explorer", "Tireless Tracker",
                "Groundskeeper", "Centaur Vinecrasher", "Elemental", "Beast"}
DYN_POWER = {"Multani, Yavimaya's Avatar", "Uurg, Spawn of Turg"}


class Trial:
    def __init__(self, library, rng, powers, no_combat=False, free_drain=False):
        self.g = slc.Goldfish(library, rng, rocks=ROCKS)
        self.rng = rng
        self.tbl = slc.Table()
        self.powers = powers
        self.no_combat = no_combat  # True = measure the spell kills only (combo /
                                    # Ob Nixilis / Devil pings / station-8 drain)
        self.free_drain = free_drain  # COUNTERFACTUAL: drain live from the moment
                                      # Hearthhull is cast (as if not 8+-gated)
        self.station8_turn = None   # when the 8+ station actually happened
        self.drain_events = 0       # land sacs that drained the table
        self.board = []            # [name, power, ready]
        self.flags = set()         # named permanents on board
        self.hearthhull = False
        self.charge2 = False       # stationed to 2+ (draw engine live)
        self.charge8 = False       # stationed to 8+ (drain live, 6/7 attacker)
        self.baloth_stun = None    # stock: Baloth Prime stun counters left
        self.sac_this_turn = False
        self.lands_in = 0          # lands entered this turn (Moraug / landfall count)
        self.pumped_at = None      # loop ran w/o converter -> combat tables next turn
        self.kill_src = None       # what actually ended the game (mixture instrument)
        self.done_whisper = False

    # -- helpers ---------------------------------------------------------------
    def bd(self, nm):
        return nm in self.flags

    def yard_lands(self):
        return sum(1 for _, r in self.g.yard if ds.is_land(r))

    def power_of(self, nm):
        if nm == "Multani, Yavimaya's Avatar":
            return self.g.lands + self.yard_lands()
        if nm == "Uurg, Spawn of Turg":
            return self.yard_lands()
        return self.powers.get(nm.lower()) or 0

    # -- events ------------------------------------------------------------------
    def land_to_yard(self):
        self.g.yard.append(("Binned Land",
                            {"cmc": 0, "type_line": "Land", "face_types": ["Land"],
                             "color_identity": (), "produced_mana": ()}))
        if self.bd("The Gitrog Monster"):
            self.g.draw(1)

    def after_mill(self, milled_names):
        """Gitrog sees mills that contained a land (one draw per event)."""
        if self.bd("The Gitrog Monster") and any(
                ds.is_land(r) for n, r in self.g.yard if n in milled_names):
            self.g.draw(1)

    def sacrifice(self, is_land):
        """One sacrifice event of ours resolves."""
        self.sac_this_turn = True
        if self.bd("Mayhem Devil"):
            self.tbl.hit_focus(1, self.T)
        if self.bd("Korvold, Fae-Cursed King"):
            self.g.draw(1)
        if is_land:
            if self.bd("Titania, Protector of Argoth"):
                self.board.append(["Elemental", 5, False])
            if self.baloth_stun is not None:
                self.board.append(["Beast", 4, False])
                self.baloth_stun -= 1
            if self.charge8 or (self.free_drain and self.hearthhull):
                self.tbl.hit_all(2, self.T)
                self.drain_events += 1
        self.try_combo(ignited=True)

    def landfall(self, n=1):
        self.lands_in += n
        for _ in range(n):
            if self.bd("Omnath, Locus of Rage"):
                self.board.append(["Elemental", 5, False])
            if self.bd("Rampaging Baloths"):
                self.board.append(["Beast", 4, False])
            if self.bd("Ob Nixilis, the Fallen"):
                self.tbl.hit_focus(3, self.T)

    def play_land(self, name):
        """Effects of a land hitting play (the land count is already bumped)."""
        if name in FETCHES:
            self.landfall(2)                    # the fetch + the basic it grabs
            self.land_to_yard()                 # the shell
            self.sacrifice(is_land=True)
        else:
            self.landfall(1)

    def extra_land_drop(self):
        g = self.g
        li = next((i for i, (_, r) in enumerate(g.hand) if ds.is_pure_land(r)), None)
        if li is None:
            li = next((i for i, (_, r) in enumerate(g.hand) if ds.is_land(r)), None)
        if li is None:
            return False
        nm, _ = g.hand.pop(li)
        g.lands += 1
        self.play_land(nm)
        return True

    # -- the combo -----------------------------------------------------------------
    def try_combo(self, ignited=False):
        """ignited=True only when called from a sacrifice event resolving WHILE both
        pieces are on board (Mazirek must see the sac to counter Broodscale) —
        a sac from earlier in the turn does not carry over."""
        if self.tbl.done or self.pumped_at is not None:
            return
        if not (self.bd("Mazirek, Kraul Death Priest") and self.bd("Basking Broodscale")):
            return
        # ignition: this sacrifice, a free outlet on board, or pay adapt {1}{G}
        if not (ignited or self.bd("Woe Strider")):
            if not self.g.pay(2):
                return
        # loop live: infinite {C}, infinite sac triggers, infinite counters
        if (self.bd("Mayhem Devil") or self.bd("Jarad, Golgari Lich Lord")
                or self.g.has("Exsanguinate")):
            self.kill_src = "combo+converter"
            self.tbl.kill_all(self.T)
            return
        # no converter: every creature (and as many Spawn tokens as we like) is
        # arbitrarily pumped. Ready bodies swing THIS combat; else next turn.
        ready = sum(1 for c in self.board if c[2])
        if self.g.has("Worldsoul's Rage") or ready >= 1:
            self.tbl.hit_focus(999, self.T)     # decap now (Rage or one pumped swing)
        if ready >= 3:
            self.kill_src = "combo pumped swing"
            self.tbl.kill_all(self.T)
        else:
            self.kill_src = "combo pumped (next turn)"
            self.pumped_at = self.T             # Spawn army connects next turn

    # -- creatures --------------------------------------------------------------------
    def cast_creature(self, nm, cost=None):
        if not self.g.cast(nm, cost):
            return False
        self.flags.add(nm)
        if nm == "Baloth Prime":
            self.baloth_stun = 6
        self.board.append([nm, self.power_of(nm), False])
        if nm == "Satyr Wayfinder":
            milled = self.g.mill(4)
            li = next((i for i, (n2, r2) in enumerate(self.g.yard)
                       if n2 in milled and ds.is_land(r2)), None)
            if li is not None:
                self.g.hand.append(self.g.yard.pop(li))
            self.after_mill(milled)
        if nm == "Aftermath Analyst":
            self.after_mill(self.g.mill(3))
        self.try_combo()
        return True

    def remove_body(self, entry):
        self.board.remove(entry)
        self.flags.discard(entry[0])

    def mass_reclaim(self):
        """All yard lands to the battlefield tapped (Reclamation / Analyst sac)."""
        keep, n = [], 0
        for item in self.g.yard:
            if ds.is_land(item[1]):
                n += 1
            else:
                keep.append(item)
        self.g.yard[:] = keep
        self.g.lands += n
        self.landfall(n)

    # -- one turn -------------------------------------------------------------------
    def turn(self, T):
        self.T = T
        g = self.g
        self.sac_this_turn = False
        self.lands_in = 0
        for c in self.board:                    # summoning sickness wears off
            c[2] = True
        if self.baloth_stun is not None and self.baloth_stun >= 0:
            self.baloth_stun -= 1               # untap step chips a stun counter
        played = g.begin_turn(T)
        if self.pumped_at is not None and T > self.pumped_at:
            self.tbl.kill_all(T)                # arbitrarily pumped Spawn army connects
            return
        g.deploy_rocks()
        if played:
            self.play_land(played)

        # Hearthhull draw engine (2+ box): {1}, T, sac a land: draw 2 + extra land play
        if self.charge2 and g.avail >= 1 and (
                g.lands >= 4 or (self.flags & GY_LAND_ENGINE and g.lands >= 2)):
            g.pay(1)
            g.lands -= 1
            self.land_to_yard()
            self.sacrifice(is_land=True)
            g.draw(2)
            if not self.extra_land_drop() and (self.flags & GY_LAND_ENGINE
                                               and self.yard_lands() >= 1):
                li = next(i for i, (_, r) in enumerate(g.yard) if ds.is_land(r))
                g.yard.pop(li)                  # replay the sacrificed land (Crucible)
                g.lands += 1
                self.landfall(1)

        progress = True
        while progress and not self.tbl.done and self.pumped_at is None:
            progress = False
            # 1. combo pieces (absent from the stock list -> these simply never fire)
            for nm, cost in COMBO.items():
                if not self.bd(nm) and g.has(nm) and g.avail >= cost:
                    if self.cast_creature(nm, cost):
                        progress = True
            # 2. Natural Order: sac a green body, put Mazirek onto the battlefield
            if (not self.bd("Mazirek, Kraul Death Priest") and g.has("Natural Order")
                    and g.avail >= 4):
                fodder = min((c for c in self.board if c[0] in GREEN_FODDER and c[2]),
                             key=lambda c: c[1], default=None)
                if fodder is not None:
                    got = g.fetch("Mazirek, Kraul Death Priest") or g.has(
                        "Mazirek, Kraul Death Priest")
                    if got:
                        g.cast("Natural Order", 4)
                        self.remove_body(fodder)
                        self.sacrifice(is_land=False)
                        g.hand.pop(g.in_hand("Mazirek, Kraul Death Priest"))
                        self.flags.add("Mazirek, Kraul Death Priest")
                        self.board.append(["Mazirek, Kraul Death Priest", 2, False])
                        self.try_combo()
                        progress = True
            # 3. Gamble for the missing combo half (honest random discard)
            if g.has("Gamble") and g.avail >= 1:
                missing = next((nm for nm in COMBO
                                if not self.bd(nm) and not g.has(nm)
                                and not g.in_yard(nm)), None)
                if missing and g.fetch(missing):
                    g.cast("Gamble", 1)
                    if g.hand:
                        self.g.yard.append(g.hand.pop(self.rng.randrange(len(g.hand))))
                    progress = True
            # 4. Victimize: both halves in the yard -> battlefield (needs a body)
            if (g.has("Victimize") and g.avail >= 3
                    and g.in_yard("Mazirek, Kraul Death Priest")
                    and g.in_yard("Basking Broodscale")):
                fodder = min((c for c in self.board
                              if c[2] and c[0] not in CONVERTER_BD),
                             key=lambda c: c[1], default=None)
                if fodder is not None:
                    g.cast("Victimize", 3)
                    self.remove_body(fodder)
                    self.sacrifice(is_land=False)
                    for nm in COMBO:
                        g.take_yard(nm)
                        self.flags.add(nm)
                        self.board.append([nm, self.power_of(nm), False])
                    self.try_combo()
                    progress = True
            # 5. the commander (engine): cast, then station the 2+ box
            if not self.hearthhull and g.avail >= 4:
                g.pay(4)
                self.hearthhull = True
                progress = True
            if self.hearthhull and not self.charge2 and any(
                    c[2] and c[1] >= 2 for c in self.board):
                self.charge2 = True             # tap a 2-power body once (sorcery)
                progress = True
            # 6. converters / ramp / draw / recursion
            for nm, cost in CONVERTER_BD.items():
                if not self.bd(nm) and g.has(nm) and g.avail >= cost:
                    if self.cast_creature(nm, cost):
                        progress = True
            for nm, (cost, gained, now, sacs) in RAMP.items():
                if g.has(nm) and g.avail >= cost:
                    g.cast(nm, cost)
                    if sacs and g.lands >= 1:
                        g.lands -= 1
                        self.land_to_yard()
                        self.sacrifice(is_land=True)
                    g.lands += gained
                    g.add_mana(now)
                    self.landfall(gained)
                    progress = True
            if g.has("Springbloom Druid") and g.avail >= 3 and g.lands >= 1:
                self.cast_creature("Springbloom Druid", 3)
                g.lands -= 1
                self.land_to_yard()
                self.sacrifice(is_land=True)
                g.lands += 2
                self.landfall(2)
                progress = True
            if not self.done_whisper and g.has("Night's Whisper") and g.avail >= 2:
                g.cast("Night's Whisper", 2)
                g.draw(2)
                self.done_whisper = True
                progress = True
            if g.has("Life from the Loam") and g.avail >= 2 and self.yard_lands() >= 2:
                g.cast("Life from the Loam", 2)
                for _ in range(3):
                    li = next((i for i, (_, r) in enumerate(g.yard)
                               if ds.is_land(r)), None)
                    if li is not None:
                        g.hand.append(g.yard.pop(li))
                progress = True
            # 7. mass reclamation when it is a real burst
            payoff = (self.bd("Omnath, Locus of Rage")
                      or self.bd("Titania, Protector of Argoth")
                      or self.bd("Ob Nixilis, the Fallen")
                      or self.bd("Moraug, Fury of Akoum"))
            if g.has("Splendid Reclamation") and g.avail >= 4 and (
                    self.yard_lands() >= (4 if payoff else 6)):
                g.cast("Splendid Reclamation", 4)
                self.mass_reclaim()
                progress = True
            if (self.bd("Aftermath Analyst") and g.avail >= 4
                    and self.yard_lands() >= (4 if payoff else 6)):
                g.pay(4)                        # {3}{G} + sac itself
                self.remove_body(next(c for c in self.board
                                      if c[0] == "Aftermath Analyst"))
                self.sacrifice(is_land=False)
                self.mass_reclaim()
                progress = True
            # 8. extra land drops from static permits
            if (self.lands_in >= 1 and (self.flags & EXTRA_DROP)
                    and self.extra_land_drop()):
                progress = True
            # 9. combat-floor bodies, biggest printed power first
            castable = sorted(((nm, rec) for nm, rec in g.hand
                               if "Creature" in rec.get("type_line", "")
                               and rec["cmc"] <= g.avail and nm not in COMBO),
                              key=lambda x: -(self.powers.get(x[0].lower()) or 0))
            if castable and self.cast_creature(castable[0][0], castable[0][1]["cmc"]):
                progress = True

        if self.tbl.done or self.pumped_at is not None:
            return
        # combat: all ready bodies, unblocked; Moraug grants an extra combat per land
        ready = sum((self.power_of(c[0]) if c[0] in DYN_POWER else c[1])
                    for c in self.board
                    if c[2] and not (c[0] == "Baloth Prime" and self.baloth_stun >= 0))
        if self.charge8:
            ready += 6                          # Hearthhull 6/7, vigilance + haste
        if self.hearthhull and not self.charge8 and 8 <= ready < 25:
            self.charge8 = True                 # spend this combat step stationing
            self.station8_turn = self.T
            return
        if ready and not self.no_combat:
            if self.bd("Korvold, Fae-Cursed King"):
                self.sacrifice(is_land=False)   # attack trigger saccing a spare token
            combats = 1 + (self.lands_in if self.bd("Moraug, Fury of Akoum") else 0)
            for _ in range(combats):
                self.tbl.hit_focus(ready, self.T)
            if self.tbl.done and self.kill_src is None:
                self.kill_src = "combat"


def _run(deck, index, aliases, trials, no_combat=False):
    rng = random.Random(SEED)
    library, commander = slc.load_parsed(deck, index, aliases)
    powers = slc.load_powers([nm for nm, r in library
                              if "Creature" in r.get("type_line", "")])
    print(f"  library {len(library)} + commander {commander}   [{deck.name}]")
    res, mix = [], {}
    for _ in range(trials):
        tr = Trial(library, rng, powers, no_combat=no_combat)
        for T in range(1, TURNS + 1):
            tr.turn(T)
            if tr.tbl.done:
                break
        res.append((tr.tbl.decap, tr.tbl.table))
        src = tr.kill_src or ("combat" if tr.tbl.decap else "none in horizon")
        mix[src] = mix.get(src, 0) + 1
    slc.report_clock(res, SHOW, TURNS, trials)
    print("  kill mixture: " + ", ".join(
        f"{k} {100.0 * v / trials:.0f}%"
        for k, v in sorted(mix.items(), key=lambda x: -x[1])))
    return res


def mode_clock(index, aliases, trials, deck=None):
    print("=" * 72)
    print(f"CLOCK — World Shapers UPGRADED (owned-only swaps)   trials={trials} seed={SEED}")
    print("=" * 72)
    _run(deck or DECK_UP, index, aliases, trials)
    print("\n  Primary = Mazirek+Broodscale infinite (converter same turn, else pumped")
    print("  army tables next turn). CEILING: no interaction; the loop is two creatures")
    print("  (a wipe/spot removal turns it off) — pod resilience is NOT measured here.")


def mode_comboclock(index, aliases, trials, deck=None):
    """The SPELL-KILL clock: plain combat switched off, so a kill = the Mazirek loop
    (incl. its pumped-army finish), Ob Nixilis / Devil pings, or station-8 drain.
    This is the interaction-resistant clock the pod actually has to answer on the
    stack — the honest counterpart to the flattering unblocked-combat ceiling."""
    print("=" * 72)
    print(f"COMBO CLOCK — upgraded, plain combat OFF   trials={trials} seed={SEED}")
    print("=" * 72)
    _run(deck or DECK_UP, index, aliases, trials, no_combat=True)
    print("\n  Read: when the loop (or a non-combat drain) actually ends the game if")
    print("  combat damage is fully answered. Pumped-army finishes still count as combo.")


def mode_stock(index, aliases, trials, deck=None):
    print("=" * 72)
    print(f"CLOCK — World Shapers STOCK precon (the box)   trials={trials} seed={SEED}")
    print("=" * 72)
    _run(deck or DECK_ST, index, aliases, trials)
    print("\n  Stock kill = landfall combat + late station-8 drain. No combo in the box.")


def mode_drain(index, aliases, trials, deck=None):
    """How much does the 8+ gate on the drain actually cost? Counterfactual A/B:
    the real card (drain only once stationed to 8, one combat step spent stationing)
    vs an imaginary always-on drain live from the turn Hearthhull is cast. Also
    reports when station-8 actually happens in-sim and how much the drain chips."""
    print("=" * 72)
    print(f"DRAIN GATE — station-8 counterfactual   trials={trials} seed={SEED}")
    print("=" * 72)
    for label, dpath in (("stock", DECK_ST), ("upgraded", DECK_UP)):
        library, _ = slc.load_parsed(deck or dpath, index, aliases)
        powers = slc.load_powers([nm for nm, r in library
                                  if "Creature" in r.get("type_line", "")])
        for tag, free in ((f"{label}: real card (8+ gated)", False),
                          (f"{label}: IF drain were always-on", True)):
            rng = random.Random(SEED)
            res, st8, drains = [], [], 0
            for _ in range(trials):
                tr = Trial(library, rng, powers, free_drain=free)
                for T in range(1, TURNS + 1):
                    tr.turn(T)
                    if tr.tbl.done:
                        break
                res.append((tr.tbl.decap, tr.tbl.table))
                if tr.station8_turn:
                    st8.append(tr.station8_turn)
                drains += tr.drain_events
            extra = (f"  station-8 in {100.0 * len(st8) / trials:.0f}% of games"
                     f" (median T{sorted(st8)[len(st8) // 2]})" if st8 and not free
                     else "")
            print(slc.row(tag + " — decap", slc.cum(res, 0, SHOW), SHOW, width=44)
                  + f"  med {slc.median(res, 0)}")
            print(slc.row("    ... table", slc.cum(res, 1, SHOW), SHOW, width=44)
                  + f"  med {slc.median(res, 1)}"
                  + f"   drain sacs/game {drains / trials:.1f}" + extra)
    print("\n  Read: the always-on arm is the UPPER BOUND of what un-gating could buy.")
    print("  The drain rate is 2 x (land sacs/turn) — the gate matters less than the rate.")


def mode_levers(index, aliases, trials, deck=None):
    """Decomposition: which slice of the 19 swaps buys the speed? Variants built from
    the STOCK list via build_lib, so each package is measured against the same base."""
    print("=" * 72)
    print(f"LEVERS — upgrade decomposition   trials={trials} seed={SEED}")
    print("=" * 72)
    base, _ = slc.load_parsed(DECK_ST, index, aliases)
    up, _ = slc.load_parsed(DECK_UP, index, aliases)
    powers = slc.load_powers(sorted({nm for nm, r in base + up
                                     if "Creature" in r.get("type_line", "")}))
    COMBO_PKG = (["Sprouting Goblin", "Groundskeeper", "Centaur Vinecrasher",
                  "Scouring Swarm", "Eumidian Wastewaker", "Formless Genesis"],
                 ["Basking Broodscale", "Exsanguinate", "Jarad, Golgari Lich Lord",
                  "Victimize", "Woe Strider", "Life from the Loam"])
    TUTOR_PKG = (["Horizon Explorer", "Evendo Brushrazer", "Soul of Windgrace"],
                 ["Natural Order", "Gamble", "Mana Vault"])
    VARIANTS = {
        "stock (the box)": base,
        "stock + combo package (no GCs)": slc.build_lib(base, index, *COMBO_PKG),
        "stock + combo + GC tutors/Vault": slc.build_lib(
            slc.build_lib(base, index, *COMBO_PKG), index, *TUTOR_PKG),
        "full 19-swap upgrade": up,
    }
    print("  P(kill <= T) %".ljust(46) + "".join(f"{t:6d}" for t in SHOW))
    for name, lib in VARIANTS.items():
        rng = random.Random(SEED)
        res = slc.run_goldfish(lambda: Trial(lib, rng, powers), trials, TURNS)
        print(slc.row(name + " — decap", slc.cum(res, 0, SHOW), SHOW, width=44)
              + f"  med {slc.median(res, 0)}")
        print(slc.row("    ... table", slc.cum(res, 1, SHOW), SHOW, width=44)
              + f"  med {slc.median(res, 1)}")
    print("\n  Read: combo package = the kill; the GC slice = assembly speed.")
    print("  Deltas over decimals, as ever.")


if __name__ == "__main__":
    slc.run_cli(__doc__, {"clock": mode_clock, "comboclock": mode_comboclock,
                          "stock": mode_stock, "levers": mode_levers,
                          "drain": mode_drain})
