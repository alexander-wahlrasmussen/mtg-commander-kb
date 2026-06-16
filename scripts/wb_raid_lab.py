#!/usr/bin/env python3
"""wb_raid_lab.py — Zero-Sum Game (Witherbloom) DR-RAID LEVER TEST.

Question (Alex, 2026-06-16): Zero-Sum sits in no man's land (#10 vs combo,
34%; #6 vs Ur-Dragon, 70%). Can a raid of Diminishing Returns (treated as a
free donor — all cards available for modelling, buying decided after) push it
into the both-ways top tier? Model ALL the candidate packages so we see which
one actually moves the clock, not just one committed list.

This is a LEVER TEST in the house style (cf. Lightning War §5, GD finisher
sims): one baseline + each candidate package isolated, reported on the same
decap/table grid, deltas attributed.

DERIVED FROM scripts/wb_clock_lab.py — the validated lifeloop model is copied
faithfully so the `base` variant reproduces that lab's T9 (the Summary
citation). The raid axes are NEW and gated behind self.raid, so they touch
nothing the base measures. wb_clock_lab.py is left intact (it backs the
Summary).

THREE KILL AXES the raid can add (all oracle-verified 2026-06-16):
  1. SPEED — K'rrik, Son of Yawgmoth ({B} payable as 2 life; the loop repays
     it). Modelled as +2 mana/turn while K'rrik is out (life is goldfish-free
     in this lab, per the base model's Necropotence convention) — conservative
     vs the real black-pip discount. Reanimation (Reanimate/Animate Dead/
     Victimize) cheats Gary/Kokusho/Razaketh out early and rebuilds post-wrath.
  2. ARISTOCRAT BOARD-BURN (on-identity) — sacrifice the wide token board that
     ALREADY powers Witherbloom's affinity, into "1 to EACH opponent per
     creature death" payoffs: Syr Konrad (dmg) + Zulaport (loss) + Nadier's
     Nightblade (tokens) + single-target Blood Artist / Marionette. Board-
     independent of blockers, Abolisher-proof (triggers, not casts), and an
     igniter for the lifeloop. Free repeatable outlets dump the whole board at
     once: Ashnod's/Phyrexian Altar, Viscera Seer, Carrion Feeder, Yahenni,
     Woe Strider.
  3. DEVOTION / REANIMATOR BURST (board-independent insurance) — Gray Merchant
     (each opp loses devotion-to-black; ~6+ and reanimate for a 2nd) + Kokusho
     (death: each opp loses 5; sac+reanimate to repeat). A kill that needs no
     board at all — the hedge vs wraths / a flying wall.

RAID ALPHA is an UNBLOCKED ONE-SHOT CEILING (the same convention as every lab
here): each turn it computes the max alpha if you dumped the board + bursts,
and records the first turn it crosses 40 (decap = onto one opponent; table =
to each). It does NOT mutate the board (assumes tokens regrow), so the table
clock via repeated focus-alpha is OPTIMISTIC — trust the decap shape and the
cross-variant deltas, not the second decimal. The lifeloop path is unchanged
from the base model and still kill_all's on assembly+ignition.

Variants (each ADDS a package and CUTS an equal number of the weakest base
slots, so deck size — and draw odds — stay at 99):
  base     — current decks/zero-sum-game-20260611.txt, raid model OFF.
  base+    — same list, raid model ON (credits the board-burn the base list
             can ALREADY do via Zulaport/Blood Artist/Marionette — isolates
             how much is new cards vs just crediting the existing aristocrats).
  speed    — +K'rrik +Reanimate +Victimize +Animate Dead
  burn     — +Syr Konrad +Nadier +Sephiroth +Priest +Yahenni +Woe Strider
             +Carrion Feeder +Morbid Opportunist
  burst    — +Gray Merchant +Kokusho +Reanimate +Victimize +Animate Dead
             +Living Death
  combined — the curated both-ways build (speed + burn + burst, 10 cards)

Data: collection/oracle-cards.json. Writeup: analysis/ (this run).
"""
import importlib.util
import random
from pathlib import Path

ROOT = Path(__file__).parent.parent
_spec = importlib.util.spec_from_file_location(
    "speed_lab_core", Path(__file__).parent / "speed_lab_core.py")
slc = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(slc)
ds = slc.ds

DECK = ROOT / "decks" / "zero-sum-game-20260611.txt"
SEED = 20260616
TURNS = 12
SHOW = [4, 5, 6, 7, 8, 9, 10, 12]

ROCKS = {"Sol Ring": (1, 2), "Arcane Signet": (2, 1), "Jet Medallion": (2, 1)}

DORKS = {"Birds of Paradise", "Llanowar Elves", "Elvish Mystic",
         "Fyndhorn Elves", "Boreal Druid", "Arbor Elf",
         "Elves of Deep Shadow", "Deathrite Shaman", "Delighted Halfling"}

BLOOD_HALF = {"Exquisite Blood": 5, "Bloodthirsty Conqueror": 5}
VITO_HALF = {"Vito, Thorn of the Dusk Rose": 3, "Sanguine Bond": 5,
             "Enduring Tenacity": 4, "Defiant Bloodlord": 7}
SELF_IGNITERS = {"Professor Dellian Fel": 4}
DEATH_IGNITERS = {"Blood Artist": 2, "Zulaport Cutthroat": 2,
                  "Marionette Apprentice": 2}
OUTLETS = {"Viscera Seer": 1, "Witch's Oven": 1, "Warren Soultrader": 3,
           "Ashnod's Altar": 3, "Phyrexian Altar": 3}
TOKEN_MAKERS = {"Bitterblossom": (2, 1, 0),
                "Tendershoot Dryad": (5, 1, 0),
                "Saproling Migration": (2, 0, 2),
                "Hornet Queen": (7, 0, 5),
                "Scatter the Seeds": (2, 0, 3),   # convoke, affinity-cheapened
                "Ophiomancer": (3, 1, 0)}         # a Snake each upkeep
CREATURE_TARGETS = {"Bloodthirsty Conqueror": 5,
                    "Vito, Thorn of the Dusk Rose": 3,
                    "Enduring Tenacity": 4, "Defiant Bloodlord": 7,
                    "Witherbloom Apprentice": 2, "Cauldron Familiar": 1,
                    "Blood Artist": 2, "Marionette Apprentice": 2,
                    "Zulaport Cutthroat": 2}
CHEAP_IS = {"Lab Rats": 1, "Sprout Swarm": 2, "Dark Ritual": 1,
            "Abrupt Decay": 2, "Assassin's Trophy": 2, "Veil of Summer": 1,
            "Night's Whisper": 2, "Corpse Dance": 3}
IS_CARDS = {"Vampiric Tutor", "Demonic Tutor", "Beseech the Queen",
            "Increasing Ambition", "Dark Petition", "Diabolic Intent",
            "Chord of Calling", "Finale of Devastation", "Nature's Rhythm",
            "Dark Ritual", "Cabal Ritual"} | set(CHEAP_IS)

# ---- RAID axis card sets (new) -------------------------------------------
KRRIK = "K'rrik, Son of Yawgmoth"
GARY = "Gray Merchant of Asphodel"
KOKUSHO = "Kokusho, the Evening Star"
# each opp / death — Marionette Apprentice reads "each opponent loses 1 life"
# (Brothers' War), an each-opponent payoff, NOT single-target (lab bug fixed)
PER_EACH = {"Syr Konrad, the Grim", "Zulaport Cutthroat", "Marionette Apprentice"}
TOKEN_PER_EACH = {"Nadier's Nightblade", "Mirkwood Bats"}    # each opp / token
# each opp per SAPROLING/token death specifically (live with the token engine)
SAPROLING_PAYOFF = {"Slimefoot, the Stowaway"}
SINGLE = {"Blood Artist"}                                    # one opp / death
FREE_OUTLETS = {"Ashnod's Altar", "Phyrexian Altar", "Viscera Seer",
                "Carrion Feeder", "Yahenni, Undying Partisan", "Woe Strider"}
REANIM = {"Reanimate", "Animate Dead", "Victimize", "Necromancy",
          "Living Death"}
# magecraft payoffs that drive her on-identity affinity-storm infinite
MAGECRAFT_PAYOFF = {"Witherbloom Apprentice", "Professor Onyx",
                    "Sedgemoor Witch"}
CHATTERFANG = "Chatterfang, Squirrel General"   # token doubler
# raid bodies that get deployed for the burn/burst axes (name -> deploy cost)
RAID_BODIES = {KRRIK: 4, "Syr Konrad, the Grim": 5, GARY: 5, KOKUSHO: 6,
               "Nadier's Nightblade": 3, "Sephiroth, Fabled SOLDIER": 3,
               "Priest of Forgotten Gods": 2, "Yahenni, Undying Partisan": 2,
               "Woe Strider": 3, "Carrion Feeder": 1, "Morbid Opportunist": 3,
               "Slimefoot, the Stowaway": 3, CHATTERFANG: 3}


class Trial:
    def __init__(self, library, rng, raid=False):
        self.g = slc.Goldfish(library, rng, rocks=ROCKS)
        self.tbl = slc.Table()
        self.bf = set()
        self.entered = {}
        self.dork_out = 0
        self.dork_new = 0
        self.tokens = 0
        self.bodies = 0
        self.token_rate = 0
        self.commander = False
        self.life = 40
        self.cast_is_this_turn = False
        self.pending_top = []
        self.is_in_yard = 0
        self.rituals_held = []
        self.prev_creatures = 0
        self.combat_ign = True
        self.raid = raid

    @property
    def creatures(self):
        return self.bodies + self.tokens

    @property
    def tmult(self):
        """Chatterfang: tokens created come with an equal number of Squirrels."""
        return 2 if self.raid and CHATTERFANG in self.bf else 1

    def aff(self, generic):
        return min(generic, self.creatures) if self.commander else 0

    def missing(self):
        m = []
        if not (self.bf & set(BLOOD_HALF)):
            m.append("blood")
        if not (self.bf & set(VITO_HALF)):
            m.append("vito")
        if not self.igniter_live(future=True):
            m.append("igniter")
        return m

    def igniter_live(self, future=False):
        g = self.g
        if self.combat_ign and (self.prev_creatures >= 1 or future):
            return True
        if "Professor Dellian Fel" in self.bf:
            return True
        if "Cauldron Familiar" in self.bf and "Witch's Oven" in self.bf:
            return True
        if (self.bf & set(DEATH_IGNITERS)) and (self.bf & set(OUTLETS)) \
                and self.tokens >= 1:
            return True
        # raid payoffs that produce a life event with a free outlet are igniters
        if self.raid and (self.bf & FREE_OUTLETS) and (
                self.bf & (PER_EACH | SINGLE)) and self.creatures >= 1:
            return True
        if self.raid and (self.bf & TOKEN_PER_EACH) and self.tokens >= 1 \
                and (self.bf & FREE_OUTLETS):
            return True
        if "Gilded Goose" in self.bf and (future or g.avail >= 2):
            return True
        if "Witch's Oven" in self.bf and self.tokens >= 1 \
                and (future or g.avail >= 2):
            return True
        if "Witherbloom Apprentice" in self.bf:
            if future or self.cast_is_this_turn:
                return True
            for nm, c in CHEAP_IS.items():
                cost = max(0, c - self.aff(max(0, c - 1)))
                if g.has(nm) and g.avail >= cost:
                    return True
        if not future and self.entered.get("Cauldron Familiar") == self._T:
            return True
        return False

    def ritual_boost(self, needed):
        while self.g.avail < needed and self.rituals_held:
            nm = self.rituals_held.pop()
            if nm == "Dark Ritual":
                self.g.add_mana(2)
            else:
                self.g.add_mana(3 if self.is_in_yard >= 7 else 1)
            self.cast_is_this_turn = True
            self.is_in_yard += 1

    def deploy(self, nm, cost, body=False):
        self.ritual_boost(cost)
        if not self.g.cast(nm, cost):
            return False
        self.bf.add(nm)
        self.entered[nm] = self._T
        if body:
            self.bodies += 1
        return True

    def fetch_for(self, slot):
        if slot == "blood":
            return "Exquisite Blood" if not self.g.has("Exquisite Blood") \
                and not self.g.has("Bloodthirsty Conqueror") else None
        if slot == "vito":
            for nm in VITO_HALF:
                if self.g.has(nm):
                    return None
            return "Vito, Thorn of the Dusk Rose"
        for nm in ("Witherbloom Apprentice", "Cauldron Familiar",
                   "Professor Dellian Fel"):
            if self.g.has(nm):
                return None
        return "Witherbloom Apprentice"

    def turn(self, T):
        self._T = T
        g = self.g
        self.cast_is_this_turn = False
        self.dork_out += self.dork_new
        self.dork_new = 0
        self.tokens += self.token_rate * self.tmult
        played = g.begin_turn(T)
        if played == "Khalni Garden":
            self.tokens += 1
        if played == "Dryad Arbor":
            self.bodies += 1
        g.add_mana(self.dork_out)
        g.deploy_rocks()
        if self.raid and KRRIK in self.bf:        # life-funded black pips
            g.add_mana(2)
        if "Necropotence" in self.bf and self.entered["Necropotence"] < T:
            g.draw(3)
        for nm in self.pending_top:
            g.fetch(nm)
        self.pending_top = []
        for r in ("Dark Ritual", "Cabal Ritual"):
            while g.has(r):
                g.hand.pop(g.in_hand(r))
                self.rituals_held.append(r)
        if "Razaketh, the Foulblooded" in self.bf:
            for slot in self.missing():
                tgt = self.fetch_for(slot)
                if tgt and self.tokens >= 1 and self.life > 8:
                    if g.fetch(tgt):
                        self.tokens -= 1
                        self.life -= 2

        progress = True
        while progress:
            progress = False
            for nm, c in list(BLOOD_HALF.items()) + list(VITO_HALF.items()):
                if nm not in self.bf and g.has(nm) and not (
                        self.bf & set(BLOOD_HALF) and nm in BLOOD_HALF) and not (
                        self.bf & set(VITO_HALF) and nm in VITO_HALF):
                    self.ritual_boost(c)
                    if g.avail >= c and self.deploy(
                            nm, c, body=nm != "Exquisite Blood" and nm != "Sanguine Bond"):
                        progress = True
            if "igniter" in self.missing() or not self.igniter_live(future=True):
                for nm, c in [("Witherbloom Apprentice", 2),
                              ("Cauldron Familiar", 1), ("Witch's Oven", 1),
                              ("Professor Dellian Fel", 4)] + \
                             list(DEATH_IGNITERS.items()):
                    if nm not in self.bf and g.has(nm) and g.avail >= c:
                        self.deploy(nm, c, body=nm in ("Witherbloom Apprentice",
                                                       "Cauldron Familiar",
                                                       *DEATH_IGNITERS))
                        progress = True
                        break
            miss = self.missing()
            if miss:
                slot = miss[0]
                tgt = self.fetch_for(slot)
                if tgt:
                    if self.cast_any_tutor(tgt):
                        progress = True
            if not self.commander:
                c = max(2, 8 - self.creatures)
                if g.cast("Witherbloom, the Balancer", c):
                    self.commander = True
                    self.bodies += 1
                    progress = True
            if "Necropotence" not in self.bf and g.has("Necropotence") \
                    and g.avail >= 3:
                self.deploy("Necropotence", 3)
                progress = True
            for nm, (c, rate, burst) in TOKEN_MAKERS.items():
                if nm not in self.bf and g.has(nm) and g.avail >= c:
                    self.deploy(nm, c, body=nm in ("Tendershoot Dryad",
                                                   "Hornet Queen"))
                    self.token_rate += rate
                    self.tokens += burst * self.tmult
                    progress = True
            for nm in list(DORKS) + ["Gilded Goose"]:
                if g.has(nm) and g.avail >= 1:
                    g.cast(nm, 1)
                    self.bodies += 1
                    if nm != "Gilded Goose":
                        self.dork_new += 1
                    progress = True
            if "Razaketh, the Foulblooded" not in self.bf \
                    and g.has("Razaketh, the Foulblooded") and g.avail >= 8:
                self.deploy("Razaketh, the Foulblooded", 8, body=True)
                progress = True
            # raid bodies (payoffs / outlets / bursts / K'rrik)
            if self.raid:
                # tutor the last piece of the token-infinite when it's one away
                outlet_ok = (bool(self.bf & FREE_OUTLETS)
                             or "Witch's Oven" in self.bf)
                payoff_ok = (bool(self.bf & {"Witherbloom Apprentice",
                                             "Professor Onyx"})
                             or (outlet_ok and self.bf & (
                                 PER_EACH | TOKEN_PER_EACH | SAPROLING_PAYOFF)))
                if (self.commander and self.creatures >= 4 and self.tokens >= 1
                        and payoff_ok and not g.has("Sprout Swarm")
                        and "Sprout Swarm" not in self.bf):
                    if self.cast_any_tutor("Sprout Swarm"):
                        progress = True
                # pursue her affinity-storm: deploy a magecraft payoff
                for nm, c, bd in [("Witherbloom Apprentice", 2, True),
                                  ("Sedgemoor Witch", 3, True),
                                  ("Professor Onyx", 5, False)]:
                    if nm not in self.bf and g.has(nm) and g.avail >= c:
                        self.deploy(nm, c, body=bd)
                        progress = True
                        break
                # ensure a free sac outlet is online for the burn axis
                if not ((self.bf & FREE_OUTLETS) or "Witch's Oven" in self.bf):
                    for nm, c, bd in [("Viscera Seer", 1, True),
                                      ("Witch's Oven", 1, False),
                                      ("Ashnod's Altar", 3, False),
                                      ("Phyrexian Altar", 3, False)]:
                        if nm not in self.bf and g.has(nm) and g.avail >= c:
                            self.deploy(nm, c, body=bd)
                            progress = True
                            break
                for nm, c in sorted(RAID_BODIES.items(), key=lambda kv: kv[1]):
                    if nm not in self.bf and g.has(nm) and g.avail >= c:
                        self.deploy(nm, c, body=True)
                        progress = True
                        break

        # win check — lifeloop (unchanged from base), then her on-identity
        # affinity-storm, then the raid aristocrat/burst alpha
        if (self.bf & set(BLOOD_HALF)) and (self.bf & set(VITO_HALF)) \
                and self.igniter_live():
            self.tbl.kill_all(T)
        elif self.raid and self.storm_ready():
            self.tbl.kill_all(T)
        elif self.raid:
            self.raid_alpha(T)
        self.prev_creatures = self.creatures

    def storm_ready(self):
        """The on-identity infinite: commander's affinity zeroes Sprout Swarm's
        generic, convoke pays the {G} by tapping the green Saproling the last
        cast made, buyback returns it — infinite casts, each a magecraft drain.
        Needs: commander out (affinity), a magecraft payoff (Witherbloom
        Apprentice / Professor Onyx / Sedgemoor Witch), Sprout Swarm in hand,
        >=4 creatures for affinity, and a green token to bootstrap convoke.
        (Lab Rats does NOT loop — its Rat is black, can't convoke the {G}.)"""
        if not self.commander or self.tokens < 1 or self.creatures < 4:
            return False
        if not self.g.has("Sprout Swarm"):
            return False
        if self.bf & {"Witherbloom Apprentice", "Professor Onyx"}:
            return True                      # magecraft: infinite drain, no sac
        # else convert infinite Saprolings via a free outlet + each-opp payoff
        outlet = bool(self.bf & FREE_OUTLETS) or "Witch's Oven" in self.bf
        payoff = bool(self.bf & (PER_EACH | TOKEN_PER_EACH | SAPROLING_PAYOFF))
        return outlet and payoff

    def raid_alpha(self, T):
        """Aristocrat-burn / burst kill, modelled as a GRIND that ACCUMULATES in
        the Table plus a one-shot hoarded-board alpha. Two components:

          recurring (FLOW) — the tokens you feed an outlet each turn die: each
            death pings the per-each payoffs (Konrad/Zulaport) and, for tokens,
            the token-leave payoffs (Nadier/Mirkwood); single-target payoffs
            (Blood Artist/Marionette) pile onto one. Plus repeatable board-
            independent bursts (Gary re-ETB / Kokusho sac via reanimation).
            Applied as hit_all/hit_focus EVERY turn the engine is online, so the
            table clock reflects the grind.
          one-shot (STOCK) — dump the whole hoarded board at once; kills if
            board x payoffs >= 40.

        Optimism (flagged): unblocked, no interaction, tokens regrow (stock not
        mutated), reanimation loops are mana-light. Trust shapes + deltas."""
        bf = self.bf
        pe = len(bf & PER_EACH)
        tpe = len(bf & TOKEN_PER_EACH)
        sg = len(bf & SINGLE)
        outlet = bool(bf & FREE_OUTLETS) or "Witch's Oven" in bf
        reanim = any(self.g.has(r) or self.g.in_yard(r) for r in REANIM)
        dev = 4 + (2 if KRRIK in bf else 0)

        # repeatable board-independent bursts (need no board)
        burst_each = 0
        if GARY in bf and self.entered.get(GARY) == T:      # ETB this turn
            burst_each += dev
        if GARY in bf and reanim and self.g.avail >= 1:     # reanimate, re-ETB
            burst_each += dev
        if KOKUSHO in bf and outlet:                        # sac drain
            burst_each += 5 * (2 if reanim else 1)

        # recurring aristocrat drain — only with a free outlet to convert bodies
        if outlet and (pe or tpe or sg):
            deaths = self.token_rate + (1 if self.creatures >= 1 else 0)
            each = self.token_rate * (pe + tpe) + (deaths - self.token_rate) * pe
            focus_extra = deaths * sg
        else:
            each = focus_extra = 0
        each += burst_each
        if each:
            self.tbl.hit_all(each, T)
        if focus_extra:
            self.tbl.hit_focus(focus_extra, T)

        # one-shot hoarded-board alpha
        if outlet:
            stock_each = self.creatures * pe + self.tokens * tpe
            stock_focus = self.creatures * (pe + sg) + self.tokens * tpe
            if stock_each >= self.tbl.life:
                self.tbl.kill_all(T)
            elif stock_focus >= self.tbl.life:
                self.tbl.hit_focus(self.tbl.life, T)

    def cast_any_tutor(self, tgt):
        g = self.g
        if not any(g.deck[i][0] == tgt for i in range(g.ptr, len(g.deck))):
            return False
        tgt_cmc = {**BLOOD_HALF, **VITO_HALF,
                   "Witherbloom Apprentice": 2}.get(tgt, 3)
        if tgt in CREATURE_TARGETS:
            for nm, base in (("Nature's Rhythm", 2), ("Finale of Devastation", 2)):
                cost = max(2, tgt_cmc + base - self.aff(tgt_cmc))
                if g.has(nm):
                    self.ritual_boost(cost)
                    if g.cast(nm, cost):
                        self.bf.add(tgt)
                        self.entered[tgt] = self._T
                        self.bodies += 1
                        self._note_is()
                        g.fetch(tgt) and g.hand.pop(g.in_hand(tgt))
                        return True
            if g.has("Chord of Calling"):
                cost = max(0, tgt_cmc + 3 - self.creatures)
                self.ritual_boost(cost)
                if g.cast("Chord of Calling", cost):
                    self.bf.add(tgt)
                    self.entered[tgt] = self._T
                    self.bodies += 1
                    self._note_is()
                    g.fetch(tgt) and g.hand.pop(g.in_hand(tgt))
                    return True
        opts = []
        if g.has("Demonic Tutor"):
            opts.append(("Demonic Tutor", max(1, 2 - self.aff(1)), False))
        if g.has("Dark Petition"):
            net = 2 if self.is_in_yard >= 2 else max(2, 5 - self.aff(3))
            opts.append(("Dark Petition", net, False))
        if g.has("Increasing Ambition"):
            opts.append(("Increasing Ambition", max(1, 5 - self.aff(4)), False))
        if g.has("Beseech the Queen") and tgt_cmc <= self.g.lands:
            opts.append(("Beseech the Queen",
                         min(3, max(0, 6 - self.aff(6))), False))
        if g.has("Diabolic Intent") and self.creatures >= 1:
            opts.append(("Diabolic Intent", max(1, 2 - self.aff(1)), True))
        if g.has("Vampiric Tutor"):
            opts.append(("Vampiric Tutor", 1, "top"))
        for nm, cost, sac in sorted(opts, key=lambda o: o[1]):
            self.ritual_boost(cost)
            if g.cast(nm, cost):
                self._note_is()
                if sac == "top":
                    self.pending_top.append(tgt)
                else:
                    if sac:
                        if self.tokens:
                            self.tokens -= 1
                        else:
                            self.bodies = max(0, self.bodies - 1)
                    g.fetch(tgt)
                return True
        return False

    def _note_is(self):
        self.cast_is_this_turn = True
        self.is_in_yard += 1


# ---------------------------------------------------------------------------
# variants
# ---------------------------------------------------------------------------
CUTSET = ["Defiant Bloodlord", "Corpse Dance", "Springheart Nantuko",
          "Gilded Goose", "Boreal Druid", "Fyndhorn Elves", "Jet Medallion",
          "Beseech the Queen", "Black Market Connections", "Increasing Ambition",
          "Elves of Deep Shadow", "Delighted Halfling"]

PACKAGES = {
    "speed":  ["K'rrik, Son of Yawgmoth", "Reanimate", "Victimize",
               "Animate Dead"],
    "burn":   ["Syr Konrad, the Grim", "Nadier's Nightblade",
               "Sephiroth, Fabled SOLDIER", "Priest of Forgotten Gods",
               "Yahenni, Undying Partisan", "Woe Strider", "Carrion Feeder",
               "Morbid Opportunist"],
    "burst":  ["Gray Merchant of Asphodel", "Kokusho, the Evening Star",
               "Reanimate", "Victimize", "Animate Dead", "Living Death"],
    "storm":  ["Professor Onyx", "Sedgemoor Witch"],
    "tokens": ["Slimefoot, the Stowaway", "Chatterfang, Squirrel General",
               "Scatter the Seeds"],
    "tokens+": ["Slimefoot, the Stowaway", "Chatterfang, Squirrel General",
                "Scatter the Seeds", "Professor Onyx", "Sedgemoor Witch",
                "Ophiomancer"],
    "combined": ["K'rrik, Son of Yawgmoth", "Syr Konrad, the Grim",
                 "Nadier's Nightblade", "Sephiroth, Fabled SOLDIER",
                 "Gray Merchant of Asphodel", "Kokusho, the Evening Star",
                 "Priest of Forgotten Gods", "Yahenni, Undying Partisan",
                 "Reanimate", "Victimize"],
}


def run_variant(library, trials, raid, combat_ign=True):
    rng = random.Random(SEED)

    def make():
        tr = Trial(library, rng, raid=raid)
        tr.combat_ign = combat_ign
        return tr
    return slc.run_goldfish(make, trials, TURNS)


def report(label, res, trials):
    dec = slc.cum(res, 0, SHOW)
    tab = slc.cum(res, 1, SHOW)
    print(slc.row(f"{label} decap", dec, SHOW))
    print(slc.row(f"{label} table", tab, SHOW))
    nd = slc.never_pct(res, 0, trials)
    nt = slc.never_pct(res, 1, trials)
    print(f"      median decap {slc.median(res, 0)} / table "
          f"{slc.median(res, 1)}  ·  never decap {nd:.0f}% / table {nt:.0f}%")


def mode_levers(index, aliases, trials):
    print("=" * 78)
    print(f"RAID LEVER TEST — Zero-Sum Game ({trials} trials, seed {SEED})")
    print("=" * 78)
    base, _ = slc.load_parsed(DECK, index, aliases)
    print(f"  base library {len(base)} cards")
    print("  turns:".ljust(46) + "".join(f"{t:6d}" for t in SHOW))

    print("\n-- base (raid model OFF; reproduces wb_clock_lab) --")
    report("base", run_variant(base, trials, raid=False), trials)

    print("\n-- base+ (same list, raid model ON: credits existing aristocrats) --")
    report("base+", run_variant(base, trials, raid=True), trials)

    for name, adds in PACKAGES.items():
        cuts = CUTSET[:len(adds)]
        lib = slc.build_lib(base, index, cuts, adds)
        print(f"\n-- {name}: +{len(adds)} / -{len(cuts)} "
              f"(adds: {', '.join(a.split(',')[0] for a in adds)}) --")
        report(name, run_variant(lib, trials, raid=True), trials)


def mode_disrupt(index, aliases, trials):
    """Resilience proxy the race clock can't show: BLOCKED-OUT board (no combat
    ignition) — the lifeloop loses its easiest igniter and must rely on non-
    combat ignition + the raid's board-independent kills. This is also the
    Ur-Dragon 'walled by flyers' scenario. Lower never-kill% = more resilient /
    better both-ways. Reported as P(table kill <= T) + never%."""
    print("=" * 78)
    print(f"DISRUPTION / FAIR-WALL — blocked board, no combat ignition "
          f"({trials} trials)")
    print("=" * 78)
    base, _ = slc.load_parsed(DECK, index, aliases)
    print("  turns:".ljust(46) + "".join(f"{t:6d}" for t in SHOW))

    def line(label, lib, raid):
        res = run_variant(lib, trials, raid=raid, combat_ign=False)
        nt = slc.never_pct(res, 1, trials)
        print(slc.row(f"{label} table", slc.cum(res, 1, SHOW), SHOW)
              + f"   never {nt:.0f}%")

    line("base  ", base, False)
    for name, adds in PACKAGES.items():
        cuts = CUTSET[:len(adds)]
        line(f"{name:6}", slc.build_lib(base, index, cuts, adds), True)


if __name__ == "__main__":
    slc.run_cli(__doc__, {"levers": mode_levers, "disrupt": mode_disrupt})
