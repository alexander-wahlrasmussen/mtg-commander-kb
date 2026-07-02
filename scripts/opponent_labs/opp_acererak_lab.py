#!/usr/bin/env python3
"""opp_acererak_lab.py — COMBO-ASSEMBLY kill-turn goldfish for the archenemy's Acererak
deck (opponents/acererak-reconstruction-PROXY-20260702.txt — a RECONSTRUCTION; this is a
PROXY clock, never citation-grade; see scripts/opponent_labs/README.md).

WHY THIS EXISTS: pod_gauntlet races our decks against a hand-assumed K_DIST ("wins T6-7").
This lab measures the assumed number for his FAVORITE deck (seen every meetup). Kill shape
verified BEFORE modelling (feedback_verify_kill_shape_before_labbing): user testimony
2026-07-02 says the deck "most certainly runs" an Acererak infinite whose damage comes from
venturing — a COMBO-ASSEMBLY clock, not attrition.

THE LOOP (every card card_lookup-verified 2026-07-02; traced per-iteration):
  Acererak the Archlich {2}{B}: ETB "if you haven't completed Tomb of Annihilation, return
  Acererak to its owner's hand and venture" -> tax-free recasts from HAND, forever, as long
  as ToA is never completed. The infinite laps LOST MINE (Dark Pool: each opponent loses 1)
  — completing ToA would END the bounce, which is why the damage dungeon is another one.
    cost   = max(1, 3 - #reducers)   reducers: Undead Warchief / Jet Medallion / Bontu's
             Monument ("Zombie/Black creature spells cost {1} less"; colored pip floor {B})
    income = Phyrexian Altar (sac the token -> 1 any) + Pitiless Plunderer (token dies ->
             Treasure; needs the token to DIE, i.e. Altar or a free outlet)
    token  = Diregraf Colossus ("whenever you cast a Zombie spell, create a tapped 2/2")
  READY when: Colossus + an outlet (Altar, or Carrion Feeder/Viscera Seer for the Plunderer
  path) + income >= cost + cost mana available to prime the first cast. Then infinite
  ventures -> Dark Pool kills all three opponents the same turn (decap == table); Bontu's
  Monument alternatively drains 1/cast with no dungeon at all. -> tbl.kill_all(T).

DIG: Demonic Tutor (hand) / Vampiric Tutor (top -> next draw) fetch the scarcest missing
piece; Night's Whisper / Read the Bones draw; Deadly Dispute / Village Rites draw off spare
fodder; Phyrexian Arena +1/turn. AND THE COMMANDER HIMSELF: spare-mana Acererak casts (cost
reduced by the reducers — he is a Zombie creature spell) each walk one Lost Mine room:
Goblin Lair token (fodder) / Mine Tunnels Treasure / Dark Pool chip (each opp -1, a real
slow second kill axis alongside Bontu's Monument 1/cast) / Temple of Dumathoin draw. The
scry room is unmodelled (conservative).

OPTIMISTIC (ceiling, same class as every lab): no removal/counters/blockers — one Colossus
or Altar kill stops the engine and is invisible here; mana is a colour-blind lands+rocks
floor. CONSERVATIVE / OMITTED: Dark Ritual burst, Crypt Ghast/Cabal Coffers swamp ramp,
Skullport Merchant draw, Cave Entrance scry, the ToA symmetric-attrition opener + zombie
combat. Net read: trust the shape, not second decimals. The PROXY list itself is the
dominant uncertainty; the levers mode brackets it LEAN (bare-minimum enablers) to FAT
(colorless-reducer build: Semblance Anvil / Cloud Key — how tuned mono-B Acererak lists
actually reach net-0). Cite the clock as the LEAN..FAT band.

Data: collection/oracle-cards.json · Run: python scripts/opponent_labs/opp_acererak_lab.py
"""
import importlib.util
import random
from pathlib import Path

ROOT = Path(__file__).parents[2]
_spec = importlib.util.spec_from_file_location(
    "speed_lab_core", ROOT / "scripts" / "speed_lab_core.py")
slc = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(slc)
ds = slc.ds

# --- spec ------------------------------------------------------------------
DECK = ROOT / "opponents" / "acererak-reconstruction-PROXY-20260702.txt"
COMMANDER = "Acererak the Archlich"
SEED = 20260702
TURNS = 14
SHOW = [4, 5, 6, 7, 8, 9, 10, 12]
ROCKS = {"Sol Ring": (1, 2), "Arcane Signet": (2, 1),
         "Mind Stone": (2, 1), "Fellwar Stone": (2, 1)}

# name -> (cast cost, reduction). Anvil/Cloud Key are COLORLESS reducers real mono-B
# Acererak builds use to hit net-0 without blue — absent from the committed PROXY,
# reachable via the FAT lever (Anvil imprint simplification: exiles-a-card cost ignored).
REDUCERS = {"Undead Warchief": (4, 1), "Jet Medallion": (2, 1), "Bontu's Monument": (3, 1),
            "Semblance Anvil": (3, 2), "Cloud Key": (3, 1)}
COLOSSUS, PLUNDERER = "Diregraf Colossus", "Pitiless Plunderer"
# Altar-class = sac-for-mana; Ashnod's {C}{C}-only pip caveat simplified to 1 generic
# income (documented optimism, only reachable via the FAT lever variant).
ALTARS = {"Phyrexian Altar": 3, "Ashnod's Altar": 3}
PIECES = {COLOSSUS: 3, PLUNDERER: 4, **ALTARS}
FREE_OUTLETS = {"Carrion Feeder": 1, "Viscera Seer": 1}
TUTORS = {"Vampiric Tutor": (1, False), "Demonic Tutor": (2, True)}   # (cost, to_hand)
DRAW2 = {"Night's Whisper": 2, "Read the Bones": 3}
SAC_DRAW = {"Village Rites": 1, "Deadly Dispute": 2}                  # need spare fodder
ARENA = "Phyrexian Arena"


def pull_commander(library, name):
    """Opponent decks aren't in deck_sim.COMMANDERS — extract the commander here."""
    for i, (nm, _rec) in enumerate(library):
        if nm.lower() == name.lower():
            return library[:i] + library[i + 1:]
    raise SystemExit(f"commander {name!r} not in parsed list")


class Trial:
    def __init__(self, library, rng):
        self.g = slc.Goldfish(library, rng, rocks=ROCKS)
        self.tbl = slc.Table()
        self.board = set()
        self.fodder = 0                  # zombie tokens (Colossus per-cast + Goblin Lair)
        self.arena = False
        self.top = None                  # Vampiric Tutor target arriving on next draw
        self.step = 0                    # Lost Mine venture pointer (4 rooms per lap)

    # -- combo state ----------------------------------------------------------
    def cost(self):
        red = sum(REDUCERS[r][1] for r in self.board if r in REDUCERS)
        return max(1, 3 - red)

    def income(self):
        altar = any(a in self.board for a in ALTARS)
        outlet = altar or any(o in self.board for o in FREE_OUTLETS)
        return (1 if altar else 0) + (1 if PLUNDERER in self.board and outlet else 0)

    def wants(self):
        """EVERY piece that still advances the loop (cast whichever is in hand —
        fixating on one target gated assembly on draw order, the v1 bug)."""
        out = []
        if COLOSSUS not in self.board:
            out.append(COLOSSUS)
        if not any(a in self.board for a in ALTARS):
            out += [a for a in ALTARS]
        if self.income() < self.cost():
            if PLUNDERER not in self.board:
                out.append(PLUNDERER)
            out += [r for r in REDUCERS if r not in self.board]
        return out

    def missing(self):
        """The single scarcest gap, for tutor targeting + the bottleneck census."""
        w = self.wants()
        return w[0] if w else None

    def ready(self):
        outlet = (any(a in self.board for a in ALTARS)
                  or any(o in self.board for o in FREE_OUTLETS))
        return (COLOSSUS in self.board and outlet
                and self.income() >= self.cost() and self.g.avail >= self.cost())

    # -- turn ------------------------------------------------------------------
    def lib_has(self, nm):
        g = self.g
        return any(g.deck[i][0] == nm for i in range(g.ptr, len(g.deck)))

    def turn(self, T):
        g = self.g
        g.begin_turn(T)
        if self.top:                     # Vampiric put it on top; this draw is it
            g.fetch(self.top); self.top = None
        if self.arena:
            g.draw(1)
        g.deploy_rocks()
        if self.ready():
            self.tbl.kill_all(T); return

        progress = True
        while progress:
            progress = False
            # 1. combo pieces — cast ANY advancing piece we hold, cheapest first
            costs = PIECES | {n: c for n, (c, _r) in REDUCERS.items()}
            for nm in sorted(self.wants(), key=lambda n: costs[n]):
                if g.has(nm) and g.avail >= costs[nm] and g.cast(nm, costs[nm]):
                    self.board.add(nm); progress = True; break
            # 2. a free outlet for the Plunderer path (cheap, grab when spare)
            if not any(o in self.board for o in FREE_OUTLETS):
                for nm, c in FREE_OUTLETS.items():
                    if g.has(nm) and g.avail >= c and g.cast(nm, c):
                        self.board.add(nm); progress = True; break
            # 3. tutors -> the scarcest missing piece
            want = self.missing()
            if want:
                for nm, (c, to_hand) in TUTORS.items():
                    if g.has(nm) and g.avail >= c and self.lib_has(want):
                        if g.cast(nm, c):
                            if to_hand:
                                g.fetch(want)
                            else:
                                self.top = want
                            progress = True; break
            # 4. draw
            if not self.arena and g.has(ARENA) and g.avail >= 3 and g.cast(ARENA, 3):
                self.arena = True; progress = True
            for nm, c in DRAW2.items():
                if g.has(nm) and g.avail >= c and g.cast(nm, c):
                    g.draw(2); progress = True; break
            for nm, c in SAC_DRAW.items():
                if self.fodder >= 1 and g.has(nm) and g.avail >= c and g.cast(nm, c):
                    self.fodder -= 1; g.draw(2); progress = True; break
            # 5. spare-mana Acererak casts: HE IS THE DIG ENGINE. Cost is reduced by
            #    the reducers (he's a Zombie creature spell — verified); each cast =
            #    Colossus token (if out) + Monument chip (if out) + ONE Lost Mine room:
            #    Cave Entrance scry (unmodelled) -> Goblin Lair token / Mine Tunnels
            #    treasure -> Dark Pool (each opp -1) -> Temple (draw 1), lap repeats.
            if g.avail >= self.cost():
                g.avail -= self.cost()
                if COLOSSUS in self.board:
                    self.fodder += 1
                if "Bontu's Monument" in self.board:
                    self.tbl.hit_all(1, T)
                if self.step == 1:                     # Goblin Lair or Mine Tunnels
                    if self.fodder:
                        g.add_mana(1)                  # Treasure
                    else:
                        self.fodder += 1               # Goblin token
                elif self.step == 2:
                    self.tbl.hit_all(1, T)             # Dark Pool
                elif self.step == 3:
                    g.draw(1)                          # Temple of Dumathoin
                self.step = (self.step + 1) % 4
                progress = True
            if self.tbl.done:
                return
            if self.ready():
                self.tbl.kill_all(T); return


# ===========================================================================
# v2 — ALL-LINES best-line (Backlog #13 Phase 2.5)
#
# v1 (Trial, above) measures ONLY the tight net-0 recast infinite -> nv70%. The USER
# CHALLENGED "his version is stronger" and our own #11 discipline agrees: the single-line
# distortion is exactly what mis-tiered Lightning War (race-only clock, combo invisible).
# AllLines races the deck's OTHER kill axes on the SAME correlated game (min over lines on
# one set of draws, the #11 MVP rule — never independent CDFs), so a brick hand bricks every
# line together:
#   infinite   v1's ready() -> kill_all (the ceiling; still gated on the 3 one-ofs).
#   monument   Bontu's Monument: each CREATURE cast (Acererak recasts + zombies) drains 1 to
#              every opponent (verified: triggers on creature spells only, black creatures -{1}).
#   shepherd   Shepherd of Rot {T}: each player loses 1 / Zombie (SYMMETRIC, verified) — table
#              -(zombie count) per turn once it's untapped; scales with Colossus/Army tokens.
#   gary       Gray Merchant ETB: each opponent loses devotion-to-black (verified; tokens add 0
#              devotion — only cast permanents' {B} pips count).
#   torment    Torment of Hailfire X-burst off BIG MANA — the axis v1 omitted "conservative"
#              but which is NOT second-order here: Cabal Coffers ({2}: +B/Swamp) + Urborg (all
#              lands are Swamps) + Crypt Ghast (+B per Swamp tapped) + Dark Ritual is a known
#              degenerate mono-B engine (~3L-2 mana). Torment forces 3/iteration UNLESS the
#              opponent sacs a nonland/discards -> modelled with a resource BUFFER they exhaust
#              first (documented optimism cuts both ways: no responses, but a real buffer).
#   venture    v1's Dark Pool / Lost Mine chip off spare-mana Acererak casts (kept).
#   gravecrawler  LEVER (off by default): Gravecrawler + Phyrexian Altar + a death-drain
#              (Zulaport/Blood Artist/Bastion/Vengeful Dead) + any Zombie = a ZERO-reducer
#              infinite drain. EXCLUDED from the committed list (unobserved) — "repeat casting
#              & saccing" eyewitness matches it. ASK the user / watch next meetup; run as a lever.
#
# All axes feed ONE Table; whichever crosses 40 first sets the clock. Acererak's kill is a
# symmetric DRAIN (no focus-fire modelled) so decap == table by construction (single=True),
# same as v1. Big mana is a documented, curated model (records carry no mana_cost/oracle_text
# -> devotion via a small PIP table, default 1 per black permanent). PROXY: trust the SHAPE,
# not second decimals; Black Market ramp + combat token-makers (Death Tyrant) omitted conservative.
# ===========================================================================

PIP = {"Gray Merchant of Asphodel": 2, "Endless Ranks of the Dead": 2, "Black Market": 2,
       "Liliana's Mastery": 2, "Bastion of Remembrance": 1}   # devotion pips; default 1 per black perm
# Non-creature token / payoff permanents the cheap-creature loop never touches (Army is a sorcery;
# the rest are enchantments) but which materially feed Shepherd's zombie count + the Gravecrawler
# lever's death-drain: name -> (effect, amount). Casting them adds devotion (PIP) but NOT a
# Monument trigger (only CREATURE spells trigger it — verified).
ATTRITION_NONCRE = {"Army of the Damned": ("zombies", 13), "Liliana's Mastery": ("zombies", 2),
                    "Endless Ranks of the Dead": ("board", 0), "Bastion of Remembrance": ("board", 0),
                    "Black Market": ("board", 0)}
DEATH_DRAINS = {"Zulaport Cutthroat", "Blood Artist", "Bastion of Remembrance", "Vengeful Dead"}
REDUCE_CRE = ("Undead Warchief", "Jet Medallion", "Bontu's Monument")   # black-creature cost -{1} each
TORMENT_BUFFER = 8      # nonland perms / cards an opponent sacs-or-discards before Torment bites
TORMENT_MIN_X = 6       # smallest X worth firing Torment at
DEFAULT_LINES = ("infinite", "monument", "shepherd", "gary", "torment", "venture")


class AllLines(Trial):
    """v2 all-lines engine. Inherits v1's combo detection (cost/income/wants/ready) and adds the
    attrition + burst + big-mana axes, gated by `enabled` so a per-line decomposition runs the
    SAME play pattern with one axis's damage switched on (the disabler-vector discipline: the
    engine only ever REMOVES damage, so any single-line curve is bounded above by all-lines)."""

    def __init__(self, library, rng, enabled=DEFAULT_LINES, gravecrawler=False):
        super().__init__(library, rng)
        self.enabled = set(enabled) | ({"gravecrawler"} if gravecrawler else set())
        self.recs = {nm: rec for nm, rec in library}
        self.zombies = 0
        self.devotion = 0
        self.shepherd_turn = None
        self.swamp_lands = 0
        self.lands_played = set()
        self.gary_cast = False
        self.torment_cast = False
        self._T = 0

    # -- mana ------------------------------------------------------------------
    def _play_land(self):
        g = self.g
        idx = None
        for want in ("Urborg, Tomb of Yawgmoth", "Cabal Coffers"):   # the big-mana enablers first
            if want not in self.lands_played:
                j = g.in_hand(want)
                if j is not None:
                    idx = j
                    break
        if idx is None:
            idx = next((i for i, (_, r) in enumerate(g.hand) if ds.is_pure_land(r)), None)
        if idx is None:
            idx = next((i for i, (_, r) in enumerate(g.hand) if ds.is_land(r)), None)
        if idx is not None:
            nm, rec = g.hand.pop(idx)
            g.lands += 1
            self.lands_played.add(nm)
            if "swamp" in rec["type_line"].lower():
                self.swamp_lands += 1

    def _big_mana(self):
        g = self.g
        urborg = "Urborg, Tomb of Yawgmoth" in self.lands_played
        swamps = g.lands if urborg else self.swamp_lands
        bonus = 0
        if "Crypt Ghast" in self.board:            # +B per Swamp tapped for mana
            bonus += swamps
        if "Cabal Coffers" in self.lands_played and (g.avail + bonus) >= 2:
            bonus += max(0, swamps - 2)            # {2}: +B per Swamp (net swamps-2)
        if bonus:
            g.add_mana(bonus)

    # -- cost / cast -----------------------------------------------------------
    def _cost_of(self, nm):
        if nm == COMMANDER:
            return self.cost()                     # Acererak recast (v1 reducer-aware)
        if nm in PIECES:
            return PIECES[nm]
        if nm in REDUCERS:
            return REDUCERS[nm][0]
        rec = self.recs.get(nm)
        if rec is None:
            return 99
        cmc = int(rec["cmc"])
        tl = rec["type_line"].lower()
        if "creature" in tl and "B" in rec["color_identity"]:
            red = sum(1 for r in REDUCE_CRE if r in self.board)
            return max(1, cmc - red)
        return cmc

    def _try_cast(self, nm):
        g = self.g
        i = g.in_hand(nm)
        if i is None:
            return False
        c = self._cost_of(nm)
        if g.avail < c:
            return False
        rec = g.hand[i][1]
        g.hand.pop(i)
        g.avail -= c
        self._on_cast(nm, rec)
        return True

    def _on_cast(self, nm, rec):
        g, T = self.g, self._T
        tl = rec["type_line"].lower()
        is_cre = "creature" in tl
        is_zom = "zombie" in tl
        black = "B" in rec["color_identity"]
        colossus_out = COLOSSUS in self.board and nm != COLOSSUS
        self.board.add(nm)
        if is_cre:
            if black:
                self.devotion += PIP.get(nm, 1)
            if "Bontu's Monument" in self.board and "monument" in self.enabled:
                self.tbl.hit_all(1, T)             # per-creature-cast drain
            if is_zom:
                self.zombies += 1
                if colossus_out:
                    self.zombies += 1              # Diregraf Colossus token (a Zombie; not re-cast)
            if nm == "Shepherd of Rot" and self.shepherd_turn is None:
                self.shepherd_turn = T
        if nm == "Gray Merchant of Asphodel" and not self.gary_cast:
            self.gary_cast = True
            if "gary" in self.enabled:
                self.tbl.hit_all(self.devotion, T)      # devotion incl. Gary's own {B}{B}
        elif nm == "Army of the Damned":
            self.zombies += 13
        elif nm == "Skullport Merchant":
            g.add_mana(1)                          # Treasure token

    # -- kill checks -----------------------------------------------------------
    def _grave_ready(self):
        g = self.g
        have_gc = (g.has("Gravecrawler") or "Gravecrawler" in self.board
                   or g.in_yard("Gravecrawler"))
        return (have_gc and "Phyrexian Altar" in self.board
                and any(p in self.board for p in DEATH_DRAINS) and self.zombies >= 1)

    def _ready_any(self, T):
        if "infinite" in self.enabled and self.ready():
            self.tbl.kill_all(T)
            return True
        if "gravecrawler" in self.enabled and self._grave_ready():
            self.tbl.kill_all(T)
            return True
        return False

    # -- turn ------------------------------------------------------------------
    def turn(self, T):
        g = self.g
        self._T = T
        if T > 1:
            g.draw()
        if self.top:
            g.fetch(self.top)
            self.top = None
        if self.arena:
            g.draw(1)
        self._play_land()
        g.avail = g.lands + g.rock_out
        g.deploy_rocks()
        self._big_mana()
        if "Endless Ranks of the Dead" in self.board:      # upkeep: +half your zombies
            self.zombies += self.zombies // 2
        if (self.shepherd_turn is not None and T > self.shepherd_turn
                and self.zombies and "shepherd" in self.enabled):
            self.tbl.hit_all(self.zombies, T)              # symmetric tap, table -(zombies)
        if self.tbl.done or self._ready_any(T):
            return

        progress = True
        while progress:
            progress = False
            # 1. combo pieces (advance the infinite), cheapest first
            for nm in sorted(self.wants(), key=self._cost_of):
                if self._try_cast(nm):
                    progress = True
                    break
            # 2. a free sac outlet for the Plunderer path (cheap)
            if not any(o in self.board for o in FREE_OUTLETS):
                for nm in FREE_OUTLETS:
                    if self._try_cast(nm):
                        progress = True
                        break
            # 3. tutors -> the scarcest missing piece
            want = self.missing()
            if want:
                for nm, (c, to_hand) in TUTORS.items():
                    if g.has(nm) and g.avail >= c and self.lib_has(want):
                        if g.cast(nm, c):
                            if to_hand:
                                g.fetch(want)
                            else:
                                self.top = want
                            progress = True
                            break
            # 4. ramp / draw (Dark Ritual first — it boosts a same-turn finisher)
            if g.has("Dark Ritual") and g.avail >= 1 and g.cast("Dark Ritual", 1):
                g.add_mana(3)
                progress = True
            if not self.arena and g.has(ARENA) and g.avail >= 3 and g.cast(ARENA, 3):
                self.arena = True
                progress = True
            for nm, c in DRAW2.items():
                if g.has(nm) and g.avail >= c and g.cast(nm, c):
                    g.draw(2)
                    progress = True
                    break
            # 5. Gray Merchant (drain) then any cheap creature (Monument/Shepherd/devotion chip)
            if g.has("Gray Merchant of Asphodel") and self._try_cast("Gray Merchant of Asphodel"):
                progress = True
            cres = sorted(((i, nm, r) for i, (nm, r) in enumerate(g.hand)
                           if "creature" in r["type_line"].lower()),
                          key=lambda x: self._cost_of(x[1]))
            for i, nm, r in cres:
                if g.avail >= self._cost_of(nm):
                    g.hand.pop(i)
                    g.avail -= self._cost_of(nm)
                    self._on_cast(nm, r)
                    progress = True
                    break
            # 5b. non-creature token / payoff engines (Army 13 zombies, Endless Ranks, Bastion...)
            for nm, (eff, amt) in sorted(ATTRITION_NONCRE.items(),
                                         key=lambda kv: self._cost_of(kv[0])):
                if nm not in self.board and g.has(nm) and g.avail >= self._cost_of(nm):
                    if g.cast(nm, self._cost_of(nm)):
                        self.board.add(nm)
                        if "B" in (self.recs.get(nm, {}).get("color_identity") or ()):
                            self.devotion += PIP.get(nm, 1)
                        if eff == "zombies":
                            self.zombies += amt
                        progress = True
                        break
            # 6. Torment of Hailfire — dump remaining mana as a burst
            if ("torment" in self.enabled and not self.torment_cast
                    and g.has("Torment of Hailfire") and g.avail - 2 >= TORMENT_MIN_X):
                x = g.avail - 2
                if g.cast("Torment of Hailfire", g.avail):
                    self.torment_cast = True
                    dmg = 3 * max(0, x - TORMENT_BUFFER)
                    if dmg:
                        self.tbl.hit_all(dmg, T)
                    progress = True
            # 7. spare-mana Acererak casts: the dig engine + a Lost Mine venture (Dark Pool chip)
            if g.avail >= self.cost():
                g.avail -= self.cost()
                if COLOSSUS in self.board:
                    self.zombies += 1
                if "Bontu's Monument" in self.board and "monument" in self.enabled:
                    self.tbl.hit_all(1, T)
                if self.step == 1:
                    self.zombies += 1                  # Goblin Lair token (fodder)
                elif self.step == 2 and "venture" in self.enabled:
                    self.tbl.hit_all(1, T)             # Dark Pool: each opp -1
                elif self.step == 3:
                    g.draw(1)                          # Temple of Dumathoin
                self.step = (self.step + 1) % 4
                progress = True
            if self.tbl.done or self._ready_any(T):
                return


def run_alllines(make_trial, trials, turns):
    """run_goldfish + a bottleneck census over the trials the infinite never assembled in."""
    out, misses = [], {}
    for _ in range(trials):
        tr = make_trial()
        for T in range(1, turns + 1):
            tr.turn(T)
            if tr.tbl.done:
                break
        out.append((tr.tbl.decap, tr.tbl.table))
        if not tr.ready():
            m = tr.missing() or "mana (pieces down, income short)"
            misses[m] = misses.get(m, 0) + 1
    return out, misses


def mode_bestline(index, aliases, trials, deck=None):
    """The v2 headline: ALL lines raced on one game, earliest close. Compare its front edge to
    the felt 'wins T6-7' and to v1's infinite-only nv70% floor."""
    deck = deck or DECK
    print("=" * 74)
    print(f"OPP CLOCK v2 — Acererak ALL-LINES best-line ({trials} trials, seed {SEED})")
    print("=" * 74)
    print("  lines: infinite + Monument drain + Shepherd + Gray Merchant + Torment(big-mana)")
    print("  + venture; Gravecrawler lever OFF. min over lines on ONE game (#11 MVP rule).")
    rng = random.Random(SEED)
    library, _ = slc.load_parsed(deck, index, aliases)
    library = pull_commander(library, COMMANDER)
    print(f"  library {len(library)} + commander {COMMANDER}   [{deck.name}]")
    res, misses = run_alllines(lambda: AllLines(library, rng), trials, TURNS)
    slc.report_clock(res, SHOW, TURNS, trials, single=True)
    if misses:
        tot = sum(misses.values())
        print(f"\n  infinite-bottleneck census over the {tot} trials it never assembled in "
              f"(kill-on-sight; the OTHER lines may still have closed):")
        for nm, n in sorted(misses.items(), key=lambda kv: -kv[1])[:6]:
            print(f"    {nm:38} {100.0 * n / tot:5.1f}%")
    print("\n  Read: this is his earliest KILL turn by ANY line (K in pod_gauntlet terms), an")
    print("  unblocked ceiling. Front edge vs the felt T6-7 is the whole question of Phase 2.5.")


def mode_lines(index, aliases, trials, deck=None):
    """Per-line decomposition + the Gravecrawler lever. Same play pattern, one axis's damage on
    at a time (disabler-vector: each single-line curve is bounded ABOVE by all-lines)."""
    deck = deck or DECK
    print("=" * 74)
    print(f"LINES — per-axis kill clock on ONE game ({trials} trials, seed {SEED})")
    print("=" * 74)
    library, _ = slc.load_parsed(deck, index, aliases)
    library = pull_commander(library, COMMANDER)
    print(f"  library {len(library)} + commander {COMMANDER}   [{deck.name}]")
    variants = [("infinite only", ("infinite",), False),
                ("monument only", ("monument",), False),
                ("shepherd only", ("shepherd",), False),
                ("gary only", ("gary",), False),
                ("torment only", ("torment",), False),
                ("attrition (mon+shep+gary+vent)", ("monument", "shepherd", "gary", "venture"), False),
                ("ALL (best-line)", DEFAULT_LINES, False),
                ("ALL + Gravecrawler lever", DEFAULT_LINES, True)]
    print("  kill (decap = table, cum %)")
    print("  " + "line".ljust(34) + "".join(f"{t:6d}" for t in SHOW))
    for name, en, gc in variants:
        rng = random.Random(SEED)
        lib = library
        if gc:                                     # add the Gravecrawler the reconstruction excludes
            rec = index.get("gravecrawler")
            lib = library + [("Gravecrawler", rec)] if rec else library
        res = slc.run_goldfish(lambda: AllLines(lib, rng, enabled=en, gravecrawler=gc), trials, TURNS)
        nv = 100.0 * sum(1 for _, t in res if t is None) / trials
        print(slc.row(name, slc.cum(res, 1, SHOW), SHOW)
              + f"  med {slc.median(res, 1)} nv{nv:.0f}%")
    print("\n  Read: which axis drives the front edge. The Gravecrawler lever is the user's")
    print("  'his version is stronger' hypothesis — a zero-reducer infinite; ask/watch next meetup.")


def census(make_trial, trials, turns):
    """run_goldfish + a bottleneck census over the failed trials."""
    out, misses = [], {}
    for _ in range(trials):
        tr = make_trial()
        for T in range(1, turns + 1):
            tr.turn(T)
            if tr.tbl.done:
                break
        out.append((tr.tbl.decap, tr.tbl.table))
        if not tr.tbl.done:
            m = tr.missing() or "mana (pieces down, income short)"
            misses[m] = misses.get(m, 0) + 1
    return out, misses


def mode_clock(index, aliases, trials, deck=None):
    deck = deck or DECK
    print("=" * 74)
    print(f"OPP CLOCK — Acererak combo-assembly goldfish ({trials} trials, seed {SEED})")
    print("=" * 74)
    print("  PROXY clock: reconstructed list, evidence tiers in the .txt header.")
    rng = random.Random(SEED)
    library, _ = slc.load_parsed(deck, index, aliases)
    library = pull_commander(library, COMMANDER)
    print(f"  library {len(library)} + commander {COMMANDER}   [{deck.name}]")
    res, misses = census(lambda: Trial(library, rng), trials, TURNS)
    slc.report_clock(res, SHOW, TURNS, trials, single=True)   # infinite -> decap == table
    if misses:
        tot = sum(misses.values())
        top = sorted(misses.items(), key=lambda kv: -kv[1])
        print(f"\n  bottleneck census over the {tot} failed trials "
              f"(the piece to kill on sight):")
        for nm, n in top:
            print(f"    {nm:38} {100.0 * n / tot:5.1f}%")
    print("\n  Read: this is his first combo-ATTEMPT turn (K in pod_gauntlet terms), an")
    print("  unblocked ceiling. The K_DIST comparison is vs the assumed {T5:10 T6:35 T7:35")
    print("  T8:15 T9:5} — the whole point of the lab.")


def mode_levers(index, aliases, trials, deck=None):
    """Bracket the reconstruction's biggest guess: HOW MANY redundant enablers he runs.
    LEAN removes Plunderer + Monument (loop needs Warchief+Medallion+Colossus+Altar
    exactly); FAT adds Ashnod's Altar as a 2nd sac-mana rock... (income any-colour
    simplification, noted). If the clock barely moves, the reconstruction risk is low."""
    deck = deck or DECK
    print("=" * 74)
    print(f"LEVERS — enabler-count bracket on the PROXY list ({trials} trials, seed {SEED})")
    print("=" * 74)
    base, _ = slc.load_parsed(deck, index, aliases)
    base = pull_commander(base, COMMANDER)
    VARIANTS = {
        "reconstruction as committed": ([], []),
        "LEAN (-Plunderer -Monument)": (["Pitiless Plunderer", "Bontu's Monument"],
                                        ["Swamp", "Swamp"]),
        "FAT  (+Anvil +Cloud Key +2nd Altar)": (
            ["Liliana's Mastery", "Army of the Damned", "Endless Ranks of the Dead"],
            ["Semblance Anvil", "Cloud Key", "Ashnod's Altar"]),
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
    print("\n  Read: the spread between LEAN and FAT is the reconstruction uncertainty band")
    print("  on the enabler count — cite the clock as a band, not a point.")


if __name__ == "__main__":
    slc.run_cli(__doc__, {"clock": mode_clock, "levers": mode_levers,
                          "bestline": mode_bestline, "lines": mode_lines})
