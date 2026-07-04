#!/usr/bin/env python3
"""ws_clock_lab.py — KILL-TURN goldfish for the World Shapers precon (EOC, Hearthhull,
the Worldseed), its owned-only 19-swap upgrade, and the external $1400 primer build
(2026-07-04 evaluation: "if I buy the precon, can it be made pod-competitive?").

DECKS (all parse via deck_registry EXTRA_COMMANDERS):
  stock    decks/considering/world-shapers-precon-20260704.txt    (the box, as sold)
  upgraded decks/considering/world-shapers-upgraded-20260704.txt  (19 swaps, all cards
           verified FREE = owned minus deployed > 0 on moxfield_haves_2026-06-25; GCs
           exactly 3/3: Natural Order, Gamble, Mana Vault)
  external decks/considering/world-shapers-external-20260704.txt  (community primer
           list; GCs 3/3: Crop Rotation, Field of the Dead, Glacial Chasm; four
           alt-name printings resolve via REF_Reskin_Aliases — Fangorn Forest =
           Yavimaya, La abuela = Tireless Provisioner, Master Emerald Shrine =
           Command Tower, Newfound Adventure = Farseek)

KILL SHAPES (find_combos 2026-07-04 + every encoded card card_lookup-verified — the
CLAUDE.md hard rule; Hearthhull's station-gating verified off the printed card image):

  UPGRADED primary — the Mazirek loop [CSB 317-5641, COMPLETE]:
    Mazirek + Basking Broodscale -> infinite {C} / sac triggers / counters; converters
    Mayhem Devil / Jarad / Exsanguinate / Worldsoul's Rage (decap) / pumped Spawn army
    next combat. Ignition = any sacrifice while both are out, or adapt {1}{G}.
    Tutors: Natural Order (Mazirek only — Broodscale is devoid, not green), Gamble
    (either half, honest random discard), Victimize (both from yard, needs a body).

  EXTERNAL primary — stationed slug + MASS LAND SACRIFICE (the primer's Plan A):
    station 8+ turns every land sac into "each opponent loses 2"; landfall slug
    statics (Tannuk 1-each-opp per landfall + draw on 2nd resolve; Sabotender
    1-each-opp; Iridescent Vinelasher 1-target; Retreat to Hagra 1-each drain mode;
    Traveling Chocobo doubling Tannuk) chip alongside; then a burst:
      Scapeshift (sac ALL lands -> 2/each per sac -> refetch that many -> full
      landfall wave), or a Zuran Orb / Squandered Resources / Sylvan Safekeeper
      full dump fired only when 2 x lands tables the remaining life,
      with Lumra, Bellow of the Woods (mill 4, return ALL yard lands) as the rebuild.
    Mana engines: Lotus Cobra / Tireless Provisioner / Nissa Resurgent (1 per
    landfall), Squandered Resources; Horn of Greed draws per land played; Field of
    the Dead zombies at 7+ lands; Scute Swarm tokens; Green Sun's Zenith / Nature's
    Rhythm fetch Lumra (stocked yard) or Lotus Cobra.
    NOT modelled (conservative): the deck's 32 CSB infinites (Springheart lines,
    Quirion/Ashaya, Shifting Woodland+Analyst), earthbend, Windgrace, Rydia,
    Formidable Speaker, Famished Worldsire, Urza's Saga, Glacial Chasm / Constant
    Mists fog locks (defense — goldfish-inert). The external clock is therefore a
    floor for a pilot who also plays the combo lines.

  FLOOR (all lists) — landfall/battlecruiser combat, unblocked ceiling; Omnath /
    Rampaging Baloths / Titania / Ob Nixilis / Moraug multipliers; Splendid
    Reclamation / Aftermath Analyst mass returns; Hearthhull 2+ draw engine; the
    8+ drain modelled as spending one combat step's worth of untapped power (>=8)
    to station (drain is INSIDE the 8+ box — printed-card check 2026-07-04).

OPTIMISTIC (ceiling, as every lab): unblocked combat, no opposing interaction,
colour-blind mana, fetches crack instantly, Moraug x(1+lands), station-8 = one
skipped combat, Scapeshift always finds lands. OMITTED (conservative): see each
deck's list above + Escape to the Wilds, Valakut Exploration, Braids, Wrenn and Six,
Meren, Szarel, Woe Strider escape, removal, Veil of Summer. Trust shapes and deltas.

Run:  python scripts/ws_clock_lab.py --trials 40000
      --mode clock      upgraded list        --mode external  the primer build
      --mode stock      the box as sold      --mode comboclock upgraded, combat off
      --mode levers     upgrade decomposition
      --mode drain      station-8 gate counterfactual
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
DECK_EX = ROOT / "decks" / "considering" / "world-shapers-external-20260704.txt"
DECK_MG = ROOT / "decks" / "considering" / "world-shapers-merged-20260704.txt"
SEED = 20260704
TURNS = 16
SHOW = [5, 6, 7, 8, 9, 10, 12, 14, 16]

ROCKS = {"Sol Ring": (1, 2), "Arcane Signet": (2, 1), "Mana Vault": (1, 3)}

# lands that sacrifice themselves to fetch (crack-on-sight model: +1 net land,
# 2 landfall events, 1 land-sacrifice event, the shell to the yard)
FETCHES = {"Evolving Wilds", "Fabled Passage", "Terramorphic Expanse", "Mountain Valley",
           "Rocky Tar Pit", "Myriad Landscape", "Escape Tunnel",
           "Cabaretti Courtyard", "Maestros Theater", "Riveteers Overlook",
           "Arid Mesa", "Bloodstained Mire", "Marsh Flats", "Misty Rainforest",
           "Polluted Delta", "Prismatic Vista", "Scalding Tarn", "Verdant Catacombs",
           "Windswept Heath", "Wooded Foothills"}

RAMP = {  # name -> (cost, lands_gained, untapped_mana_now, sacs_a_land_first)
    "Farseek": (2, 1, 0, False), "Nature's Lore": (2, 1, 1, False),
    "Cultivate": (3, 1, 0, False), "Skyshroud Claim": (4, 2, 2, False),
    "Harrow": (3, 2, 2, True), "Roiling Regrowth": (3, 2, 0, True),
    "Explore": (2, 0, 0, False),            # modelled as draw+extra drop below
    "Entish Restoration": (3, 2, 0, True),
    "Sakura-Tribe Elder": (2, 1, 0, False), # body ignored: it chumps IRL anyway
}
EXTRA_DROP = {"The Gitrog Monster", "Oracle of Mul Daya", "Icetill Explorer",
              "Exploration"}
GY_LAND_ENGINE = {"Crucible of Worlds", "Ramunap Excavator", "Conduit of Worlds",
                  "Icetill Explorer", "Walk-In Closet/Forgotten Cellar"}
COMBO = {"Mazirek, Kraul Death Priest": 5, "Basking Broodscale": 2}
CONVERTER_BD = {"Mayhem Devil": 3, "Jarad, Golgari Lich Lord": 4}
GREEN_FODDER = {"Satyr Wayfinder", "Springbloom Druid", "Aftermath Analyst",
                "Augur of Autumn", "Icetill Explorer", "Tireless Tracker",
                "Groundskeeper", "Centaur Vinecrasher", "Elemental", "Beast"}
DYN_POWER = {"Multani, Yavimaya's Avatar", "Uurg, Spawn of Turg",
             "Lumra, Bellow of the Woods", "Ashaya, Soul of the Wild"}
# external-list engines (inert for lists that lack the names)
MANA_LANDFALL = {"Lotus Cobra", "Tireless Provisioner", "Nissa, Resurgent Animist"}
SLUG_EACH = {"Sabotender", "Retreat to Hagra"}          # 1 to each opponent/landfall
MASS_OUTLETS = {"Zuran Orb", "Squandered Resources", "Sylvan Safekeeper"}
CAST_OTHER = {  # noncreature engine permanents worth deploying
    "Zuran Orb": 0, "Squandered Resources": 2, "Exploration": 1,
    "Horn of Greed": 3, "Retreat to Hagra": 3, "Crucible of Worlds": 3,
    "Conduit of Worlds": 4, "Walk-In Closet/Forgotten Cellar": 3,
    "All Will Be One": 5, "Purphoros, God of the Forge": 4,
    "Doubling Season": 5, "The Earth Crystal": 4, "Impact Tremors": 2,
}


class Trial:
    def __init__(self, library, rng, powers, no_combat=False, free_drain=False):
        self.g = slc.Goldfish(library, rng, rocks=ROCKS)
        self.rng = rng
        self.tbl = slc.Table()
        self.powers = powers
        self.no_combat = no_combat
        self.free_drain = free_drain  # COUNTERFACTUAL: drain live from cast
        self.station8_turn = None
        self.drain_events = 0
        self.board = []            # [name, power, ready]
        self.flags = set()         # named permanents on board
        self.hearthhull = False
        self.charge2 = False
        self.charge8 = False
        self.baloth_stun = None
        self.sac_this_turn = False
        self.lands_in = 0
        self.tannuk_today = 0
        self.extra_drops_used = 0
        self.sage_charge = 0
        self.pumped_at = None
        self.kill_src = None
        self.done_whisper = False

    # -- helpers ---------------------------------------------------------------
    def bd(self, nm):
        return nm in self.flags

    def yard_lands(self):
        return sum(1 for _, r in self.g.yard if ds.is_land(r))

    def power_of(self, nm):
        if nm in ("Multani, Yavimaya's Avatar",):
            return self.g.lands + self.yard_lands()
        if nm in ("Lumra, Bellow of the Woods", "Ashaya, Soul of the Wild"):
            return self.g.lands
        if nm == "Uurg, Spawn of Turg":
            return self.yard_lands()
        return self.powers.get(nm.lower()) or 0

    def tag(self, src):
        if self.tbl.done and self.kill_src is None:
            self.kill_src = src

    def dfactor(self):
        """Counter/token multiplier from Doubling Season + The Earth Crystal (each
        doubles +1/+1 counters; Doubling Season also doubles tokens). Stacks."""
        f = 1
        if self.bd("Doubling Season"):
            f *= 2
        if self.bd("The Earth Crystal"):
            f *= 2
        return f

    def awbo(self, n):
        """All Will Be One: n counters placed -> n damage to ONE opponent (decap).
        This is the non-tutor, non-combat, Abolisher-proof decap lever."""
        if self.bd("All Will Be One") and n > 0:
            self.tbl.hit_focus(n, self.T)
            self.tag("All Will Be One (counters)")

    def make_body(self, name, power, ready=False):
        """All token/creature arrivals route here so Purphoros / Impact Tremors see
        them; Doubling Season doubles TOKEN arrivals (named tokens, not hardcast)."""
        copies = 2 if (self.bd("Doubling Season") and name in
                       ("Elemental", "Beast", "Insect", "Zombie", "Bear")) else 1
        for _ in range(copies):
            self.board.append([name, power, ready])
            if self.bd("Purphoros, God of the Forge"):
                self.tbl.hit_all(2, self.T)
                self.tag("Purphoros slug")
            if self.bd("Impact Tremors"):
                self.tbl.hit_all(1, self.T)
                self.tag("Impact Tremors slug")

    # -- events ------------------------------------------------------------------
    def land_to_yard(self):
        self.g.yard.append(("Binned Land",
                            {"cmc": 0, "type_line": "Land", "face_types": ["Land"],
                             "color_identity": (), "produced_mana": ()}))
        if self.bd("The Gitrog Monster"):
            self.g.draw(1)

    def after_mill(self, milled_names):
        if self.bd("The Gitrog Monster") and any(
                ds.is_land(r) for n, r in self.g.yard if n in milled_names):
            self.g.draw(1)

    def sacrifice(self, is_land):
        self.sac_this_turn = True
        if self.bd("Mayhem Devil"):
            self.tbl.hit_focus(1, self.T)
            self.tag("land-sac drain")
        if self.bd("Korvold, Fae-Cursed King"):
            self.g.draw(1)
        if self.bd("All Will Be One") and self.bd("Mazirek, Kraul Death Priest"):
            self.awbo(max(1, len(self.board)) * self.dfactor())   # a counter per creature
        if is_land:
            if self.bd("Titania, Protector of Argoth"):
                self.make_body("Elemental", 5)
            if self.baloth_stun is not None:
                self.make_body("Beast", 4)
                self.baloth_stun -= 1
            if self.charge8 or (self.free_drain and self.hearthhull):
                self.tbl.hit_all(2, self.T)
                self.drain_events += 1
                self.tag("land-sac drain")
        self.try_combo(ignited=True)

    def landfall(self, n=1):
        g = self.g
        self.lands_in += n
        for _ in range(n):
            if self.bd("Evolution Sage") and self.charge2 and not self.charge8:
                self.sage_charge += 1 * (2 if self.bd("Doubling Season") else 1)
                self.awbo(1 * self.dfactor())         # proliferate ticks a +1/+1 too
                if self.sage_charge >= 6:             # 2 -> 8 without tapping a board
                    self.charge8 = True
                    self.station8_turn = self.T
            if self.bd("Bristly Bill, Spine Sower"):
                self.awbo(1 * self.dfactor())         # landfall -> +1/+1 counter -> AWBO
            if self.bd("Omnath, Locus of Rage"):
                self.make_body("Elemental", 5)
            if self.bd("Rampaging Baloths"):
                self.make_body("Beast", 4)
            if self.bd("Scute Swarm"):
                self.make_body("Insect", 1)
            if self.bd("Field of the Dead") and g.lands >= 7:
                self.make_body("Zombie", 2)
            if self.bd("Ob Nixilis, the Fallen"):
                self.tbl.hit_focus(3, self.T)
                self.tag("landfall slug")
            if self.bd("Tannuk, Memorial Ensign"):
                x = 2 if self.bd("Traveling Chocobo") else 1
                self.tbl.hit_all(x, self.T)
                self.tannuk_today += 1
                if self.tannuk_today == 2:
                    g.draw(1)
                self.tag("landfall slug")
            for nm in SLUG_EACH:
                if self.bd(nm):
                    self.tbl.hit_all(1, self.T)
                    self.tag("landfall slug")
            if self.bd("Iridescent Vinelasher"):
                self.tbl.hit_focus(1, self.T)
                self.tag("landfall slug")
            for nm in MANA_LANDFALL:
                if self.bd(nm):
                    g.add_mana(1)

    def play_land(self, name):
        if self.bd("Horn of Greed"):
            self.g.draw(1)
        if name == "Field of the Dead":
            self.flags.add(name)
        if name in FETCHES:
            self.landfall(2)
            self.land_to_yard()
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

    # -- the combo (upgraded list) -------------------------------------------------
    def try_combo(self, ignited=False):
        if self.tbl.done or self.pumped_at is not None:
            return
        if not (self.bd("Mazirek, Kraul Death Priest") and self.bd("Basking Broodscale")):
            return
        if not (ignited or self.bd("Woe Strider")):
            if not self.g.pay(2):
                return
        if (self.bd("Mayhem Devil") or self.bd("Jarad, Golgari Lich Lord")
                or self.bd("All Will Be One") or self.g.has("Exsanguinate")):
            self.kill_src = "combo+converter"
            self.tbl.kill_all(self.T)
            return
        ready = sum(1 for c in self.board if c[2])
        if self.g.has("Worldsoul's Rage") or ready >= 1:
            self.tbl.hit_focus(999, self.T)
        if ready >= 3:
            self.kill_src = "combo pumped swing"
            self.tbl.kill_all(self.T)
        else:
            self.kill_src = "combo pumped (next turn)"
            self.pumped_at = self.T

    # -- creatures --------------------------------------------------------------------
    def cast_creature(self, nm, cost=None):
        if not self.g.cast(nm, cost):
            return False
        self.enters_creature(nm)
        return True

    def enters_creature(self, nm):
        self.flags.add(nm)
        if nm == "Baloth Prime":
            self.baloth_stun = 6
        self.make_body(nm, self.power_of(nm))
        if nm == "The Earth King":
            self.make_body("Bear", 4)
        if nm == "Satyr Wayfinder":
            milled = self.g.mill(4)
            li = next((i for i, (n2, r2) in enumerate(self.g.yard)
                       if n2 in milled and ds.is_land(r2)), None)
            if li is not None:
                self.g.hand.append(self.g.yard.pop(li))
            self.after_mill(milled)
        if nm == "Aftermath Analyst":
            self.after_mill(self.g.mill(3))
        if nm == "Lumra, Bellow of the Woods":
            self.after_mill(self.g.mill(4))
            self.mass_reclaim()
            for c in self.board:            # power = lands, set after the return
                if c[0] == nm:
                    c[1] = self.power_of(nm)
        self.try_combo()

    def remove_body(self, entry):
        self.board.remove(entry)
        self.flags.discard(entry[0])

    def mass_reclaim(self):
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
        self.tannuk_today = 0
        self.extra_drops_used = 0
        for c in self.board:
            c[2] = True
        if self.baloth_stun is not None and self.baloth_stun >= 0:
            self.baloth_stun -= 1
        played = g.begin_turn(T)
        if self.pumped_at is not None and T > self.pumped_at:
            self.tbl.kill_all(T)
            return
        g.deploy_rocks()
        if played:
            self.play_land(played)

        # Hearthhull draw engine (2+ box)
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
                g.yard.pop(li)
                g.lands += 1
                self.landfall(1)

        progress = True
        while progress and not self.tbl.done and self.pumped_at is None:
            progress = False
            # 1. combo pieces (upgraded list)
            for nm, cost in COMBO.items():
                if not self.bd(nm) and g.has(nm) and g.avail >= cost:
                    if self.cast_creature(nm, cost):
                        progress = True
            # 2. Natural Order -> Mazirek
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
                        self.make_body("Mazirek, Kraul Death Priest", 2)
                        self.try_combo()
                        progress = True
            # 3. Gamble for the missing combo half
            if g.has("Gamble") and g.avail >= 1:
                missing = next((nm for nm in COMBO
                                if not self.bd(nm) and not g.has(nm)
                                and not g.in_yard(nm)), None)
                if missing and g.fetch(missing):
                    g.cast("Gamble", 1)
                    if g.hand:
                        self.g.yard.append(g.hand.pop(self.rng.randrange(len(g.hand))))
                    progress = True
            # 4. Victimize both halves from the yard
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
                        self.make_body(nm, self.power_of(nm))
                    self.try_combo()
                    progress = True
            # 5. the commander, then the 2+ station
            if not self.hearthhull and g.avail >= 4:
                g.pay(4)
                self.hearthhull = True
                progress = True
            if self.hearthhull and not self.charge2 and any(
                    c[2] and c[1] >= 2 for c in self.board):
                self.charge2 = True
                progress = True
            # 6. engine permanents: converters, slug statics, mana engines, rooms
            for nm, cost in CONVERTER_BD.items():
                if not self.bd(nm) and g.has(nm) and g.avail >= cost:
                    if self.cast_creature(nm, cost):
                        progress = True
            for nm in ("Lotus Cobra", "Tireless Provisioner", "Nissa, Resurgent Animist",
                       "Tannuk, Memorial Ensign", "Sabotender", "Iridescent Vinelasher",
                       "Scute Swarm", "Traveling Chocobo", "The Earth King",
                       "Evolution Sage", "Orcish Lumberjack", "Bristly Bill, Spine Sower"):
                if not self.bd(nm) and g.has(nm):
                    rec = g.hand[g.in_hand(nm)][1]
                    if g.avail >= rec["cmc"] and self.cast_creature(nm, rec["cmc"]):
                        progress = True
            for nm, cost in CAST_OTHER.items():
                if not self.bd(nm) and g.has(nm) and g.avail >= cost:
                    if g.cast(nm, cost):
                        self.flags.add(nm)
                        progress = True
            # 7. green creature tutors (external): Lumra when stocked, else a Cobra
            for tut, base in (("Green Sun's Zenith", 1), ("Nature's Rhythm", 2)):
                if not g.has(tut):
                    continue
                if (self.yard_lands() >= 4 and g.avail >= base + 6
                        and not self.bd("Lumra, Bellow of the Woods")
                        and g.fetch("Lumra, Bellow of the Woods")):
                    g.cast(tut, base)
                    g.pay(6)
                    g.hand.pop(g.in_hand("Lumra, Bellow of the Woods"))
                    self.enters_creature("Lumra, Bellow of the Woods")
                    progress = True
                elif (not (self.flags & MANA_LANDFALL) and g.avail >= base + 2
                        and g.fetch("Lotus Cobra")):
                    g.cast(tut, base)
                    g.pay(2)
                    g.hand.pop(g.in_hand("Lotus Cobra"))
                    self.enters_creature("Lotus Cobra")
                    progress = True
            # 8. ramp / draw / recursion
            for nm, (cost, gained, now, sacs) in RAMP.items():
                if g.has(nm) and g.avail >= cost:
                    g.cast(nm, cost)
                    if nm == "Explore":
                        g.draw(1)
                        self.extra_land_drop()
                        progress = True
                        continue
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
            # 9. mass reclamation as a burst
            payoff = (self.bd("Omnath, Locus of Rage")
                      or self.bd("Titania, Protector of Argoth")
                      or self.bd("Ob Nixilis, the Fallen")
                      or self.bd("Moraug, Fury of Akoum")
                      or self.bd("Tannuk, Memorial Ensign"))
            if g.has("Splendid Reclamation") and g.avail >= 4 and (
                    self.yard_lands() >= (4 if payoff else 6)):
                g.cast("Splendid Reclamation", 4)
                self.mass_reclaim()
                progress = True
            if (self.bd("Aftermath Analyst") and g.avail >= 4
                    and self.yard_lands() >= (4 if payoff else 6)):
                g.pay(4)
                self.remove_body(next(c for c in self.board
                                      if c[0] == "Aftermath Analyst"))
                self.sacrifice(is_land=False)
                self.mass_reclaim()
                progress = True
            # 10. Lumra hardcast when the yard is stocked
            if (g.has("Lumra, Bellow of the Woods") and g.avail >= 6
                    and self.yard_lands() >= 3):
                if self.cast_creature("Lumra, Bellow of the Woods", 6):
                    progress = True
            # 11. extra land drops from static permits (one per permit per turn)
            if (self.lands_in >= 1
                    and self.extra_drops_used < len(self.flags & EXTRA_DROP)
                    and self.extra_land_drop()):
                self.extra_drops_used += 1
                progress = True
            # 12. combat-floor bodies, biggest printed power first
            castable = sorted(((nm, rec) for nm, rec in g.hand
                               if "Creature" in rec.get("type_line", "")
                               and rec["cmc"] <= g.avail and nm not in COMBO),
                              key=lambda x: -(self.powers.get(x[0].lower()) or 0))
            if castable and self.cast_creature(castable[0][0], castable[0][1]["cmc"]):
                progress = True

        if self.tbl.done or self.pumped_at is not None:
            return

        # stationed mass-sacrifice bursts (the external list's primary close)
        if self.charge8:
            if g.has("Scapeshift") and g.avail >= 4 and g.lands >= 5:
                n = g.lands
                g.cast("Scapeshift", 4)
                g.lands = 0
                for _ in range(n):
                    self.land_to_yard()
                    self.sacrifice(is_land=True)
                g.lands = n                     # refetch that many (33-land deck)
                self.landfall(n)
                self.tag("Scapeshift wave")
            if not self.tbl.done and (self.flags & MASS_OUTLETS) and g.lands >= 6:
                need = self.tbl.life - min(self.tbl.dmg)
                if 2 * g.lands >= need:
                    n = g.lands
                    g.lands = 0
                    for _ in range(n):
                        self.land_to_yard()
                        self.sacrifice(is_land=True)
                    self.tag("mass land dump")
        if self.tbl.done:
            return

        # combat: all ready bodies, unblocked; Moraug: extra combat per land
        ready = sum((self.power_of(c[0]) if c[0] in DYN_POWER else c[1])
                    for c in self.board
                    if c[2] and not (c[0] == "Baloth Prime" and self.baloth_stun >= 0))
        if self.charge8:
            ready += 6
        if self.hearthhull and not self.charge8 and 8 <= ready < 25:
            self.charge8 = True
            self.station8_turn = self.T
            return
        if ready and not self.no_combat:
            if self.bd("Korvold, Fae-Cursed King"):
                self.sacrifice(is_land=False)
            combats = 1 + (self.lands_in if self.bd("Moraug, Fury of Akoum") else 0)
            for _ in range(combats):
                self.tbl.hit_focus(ready, self.T)
            self.tag("combat")


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
    print("\n  Primary = Mazirek+Broodscale infinite. CEILING: no interaction; the loop")
    print("  is two creatures — pod resilience is NOT measured here.")


def mode_external(index, aliases, trials, deck=None):
    print("=" * 72)
    print(f"CLOCK — World Shapers EXTERNAL primer build   trials={trials} seed={SEED}")
    print("=" * 72)
    _run(deck or DECK_EX, index, aliases, trials)
    print("\n  Primary = stationed slug + mass land sacrifice (primer Plan A). The 32")
    print("  CSB infinites (Springheart / Quirion+Ashaya / Shifting Woodland lines) are")
    print("  NOT modelled — this clock is a floor for a pilot who also plays them.")


def mode_comboclock(index, aliases, trials, deck=None):
    print("=" * 72)
    print(f"COMBO CLOCK — upgraded, plain combat OFF   trials={trials} seed={SEED}")
    print("=" * 72)
    _run(deck or DECK_UP, index, aliases, trials, no_combat=True)
    print("\n  Read: when the loop (or a non-combat drain) actually ends the game if")
    print("  combat damage is fully answered.")


def mode_stock(index, aliases, trials, deck=None):
    print("=" * 72)
    print(f"CLOCK — World Shapers STOCK precon (the box)   trials={trials} seed={SEED}")
    print("=" * 72)
    _run(deck or DECK_ST, index, aliases, trials)
    print("\n  Stock kill = landfall combat + late station-8 drain. No combo in the box.")


def mode_drain(index, aliases, trials, deck=None):
    """How much does the 8+ gate on the drain actually cost? Counterfactual A/B."""
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


def mode_mergedlevers(index, aliases, trials, deck=None):
    """Can the merged build move UP the tier without tutors? Tests the non-combat,
    Abolisher-proof 'counters -> All Will Be One -> single-target DECAP' axis, fed by
    counter-generators from the Earthbend retirement pool (all Jund-legal, free):
      Bristly Bill (landfall -> +1/+1 -> AWBO ping an opponent each land drop),
      Doubling Season (2x charge = faster station-8, 2x tokens, 2x every AWBO ping),
      The Earth Crystal (2x counters + green cost cut), Impact Tremors (2nd Purphoros).
    Cuts fair-value slots that don't drive decap. Watch the DECAP front edge (T6-8)."""
    base, _ = slc.load_parsed(DECK_MG, index, aliases)
    powers = slc.load_powers(sorted({nm for nm, r in base
                                     if "Creature" in r.get("type_line", "")}
                                    | {"Bristly Bill, Spine Sower"}))
    CUTS = ["Escape to the Wilds", "Augur of Autumn", "Tireless Tracker"]
    ADD3 = ["Bristly Bill, Spine Sower", "Doubling Season", "Impact Tremors"]
    VARIANTS = {
        "merged base": base,
        "+ Bristly Bill only": slc.build_lib(base, index, ["Escape to the Wilds"],
                                             ["Bristly Bill, Spine Sower"]),
        "+ counter pkg (3)": slc.build_lib(base, index, CUTS, ADD3),
        "+ counter pkg (4, -Roiling)":
            slc.build_lib(base, index, CUTS + ["Roiling Regrowth"],
                          ADD3 + ["The Earth Crystal"]),
    }
    print("=" * 72)
    print(f"MERGED LEVERS — non-tutor 'counters->AWBO->decap' axis   trials={trials}")
    print("=" * 72)
    print("  P(kill <= T) %".ljust(46) + "".join(f"{t:6d}" for t in SHOW))
    for name, lib in VARIANTS.items():
        rng = random.Random(SEED)
        res, mix = [], {}
        for _ in range(trials):
            tr = Trial(lib, rng, powers)
            for T in range(1, TURNS + 1):
                tr.turn(T)
                if tr.tbl.done:
                    break
            res.append((tr.tbl.decap, tr.tbl.table))
            src = tr.kill_src or "combat"
            mix[src] = mix.get(src, 0) + 1
        print(slc.row(name + " — decap", slc.cum(res, 0, SHOW), SHOW, width=44)
              + f"  med {slc.median(res, 0)}")
        print(slc.row("    ... table", slc.cum(res, 1, SHOW), SHOW, width=44)
              + f"  med {slc.median(res, 1)}")
        awbo = 100.0 * mix.get("All Will Be One (counters)", 0) / trials
        print(f"      AWBO-decap share {awbo:.0f}%")
    print("\n  Read: the tier axis is the DECAP front edge (T6-8). A flat delta = the")
    print("  counters axis doesn't race either -> keep it a resilience/self-meta case.")


def mode_levers(index, aliases, trials, deck=None):
    """Decomposition: which slice of the 19 swaps buys the speed?"""
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


if __name__ == "__main__":
    slc.run_cli(__doc__, {"clock": mode_clock, "external": mode_external,
                          "comboclock": mode_comboclock, "stock": mode_stock,
                          "levers": mode_levers, "drain": mode_drain,
                          "mergedlevers": mode_mergedlevers})
