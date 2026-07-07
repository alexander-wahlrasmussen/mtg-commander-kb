#!/usr/bin/env python3
"""wb_clock_lab.py — Zero-Sum Game (Witherbloom, the Balancer) KILL-TURN goldfish.

First lab for the NEW deck (decks/zero-sum-game-20260619.txt, built 2026-06-11
from proposals/witherbloom-balancer-v2b-20260607.txt minus Bayou/Coffers/Urborg).
Converts the proposal's 2026-06-07 ad-hoc deployment model ("33% T6 / 46% T7 /
56% T8 deployable") into a harness-cited clock per the verification rule.
Built on speed_lab_core.py.

THE KILL IS A CLOSED LOOP, so decap and table CONVERGE by construction: once a
blood-half (opponent-loses->you-gain) and a vito-half (you-gain->opponent-loses)
are both on the battlefield, any single life event drains the whole table out
one player at a time with you gaining through every step. kill_all on the turn
the loop closes with an igniter live.

COMBO SLOTS (all oracle-verified 2026-06-01/07/11):
  blood-half: Exquisite Blood (5), Bloodthirsty Conqueror (5)
  vito-half:  Vito (3), Sanguine Bond (5), Enduring Tenacity (4),
              Defiant Bloodlord (7)
  igniter:    Witherbloom Apprentice (2; magecraft - needs ANY I/S cast that
              turn), Cauldron Familiar (1; ETB turn, or every turn with
              Witch's Oven out), Professor Dellian Fel (4; +2 gains 3 every
              turn), Blood Artist / Zulaport Cutthroat / Marionette Apprentice
              (2; need a sac outlet + a body)

RULES FACTS the model encodes (each checked against card_lookup.py):
  * Witherbloom grants I/S "affinity for creatures" = GENERIC cost reduction
    only; coloured pips untouched. Commander herself costs 8 - creatures
    (floor {B}{G} = 2). Affinity applies to tutors/rituals, NOT to the combo
    permanents themselves.
  * Beseech the Queen {2/B}{2/B}{2/B}: payable {B}{B}{B}=3 or generically,
    so with the commander out its cost is min(3, 6 - creatures); its target
    must have MV <= lands you control (Blood @5 needs 5 lands).
  * Increasing Ambition is {4}{B} (CMC 5; 4 generic shrinks under affinity).
  * Dark Petition {3}{B}{B}; spell mastery (2+ I/S in yard) refunds {B}{B}{B}
    -> net 2.
  * Nature's Rhythm / Finale of Devastation put the creature ONTO THE
    BATTLEFIELD ({X} generic shrinks under affinity); Chord of Calling
    convokes (each creature taps for 1). Creature tutors can fetch the
    Conqueror and every vito-half EXCEPT Sanguine Bond (enchantment) —
    Enduring Tenacity is an enchantment CREATURE and is fetchable.
  * Vampiric Tutor puts the card on TOP: it reaches hand on the NEXT draw
    (modelled as a pending fetch, +1 turn).
  * Diabolic Intent needs a creature to sacrifice.
  * Gilded Goose makes mana only by eating Food — modelled as a body, not a
    dork. Delighted Halfling modelled as a full dork (optimistic: its
    coloured mode is legendary-only).
  * Cauldron Familiar + Witch's Oven loop = a drain trigger EVERY turn.
  * Razaketh: pay 2 life + sac another creature -> any card to hand,
    repeatable at instant speed; fed by tokens.
  * Dryad Arbor is a creature land (affinity body on the land drop);
    Khalni Garden ETBs with a Plant token.

MODELLED PLAY POLICY: greedy combo-first — cast/blitz missing combo halves,
then igniters, then spend any-card tutors on the highest missing slot
(blood > vito > igniter), creature tutors straight to the battlefield,
commander when affordable (she is a tutor-discount engine here, NOT a combo
piece — the line is commander-independent), dorks/token-makers with spare
mana. Rituals (Dark +2 net, Cabal +1/+3 net on threshold) pop only when they
complete a cast that turn. Necropotence = +3 draws at the start of each
following turn (life is goldfish-free).

OMITTED (conservative): Skullclamp / Black Market Connections / Night's
Whisper draw, Sprout Swarm + Lab Rats buyback token engines (counted only as
cheap I/S for the magecraft igniter), Corpse Dance recursion, Deathrite
drain mode, the affinity-storm and combat backup lines entirely (tokens stay
home as fodder; a token-beats decap would be T12+, irrelevant next to the
combo clock). OPTIMISTIC (noted): rocks tap the turn they land, Jet Medallion
approximated as a rock, mana is colour-blind (lands+rocks+dorks floor), no
opposing interaction. Trust shapes and deltas, not second decimals.

Modes:
  clock   — baseline kill-turn goldfish (the Summary citation).
  gcswap  — GC suite A/B: -Demonic Tutor +Mana Vault (rock (1,3), optimistic:
            ignores the untap tax). Answers "is the 3rd GC better as fast
            mana than as a tutor?" — kill is mana-gated per the 06-07 model.
  avail   — simulate_groups cross-check of the two combo halves vs the
            2026-06-07 deployment-model availability numbers.

Data: collection/oracle-cards.json (refresh via update_scryfall_data.py)
Writeup: decks/Zero_Sum_Game_Summary.md
"""
import importlib.util
import random
from pathlib import Path

ROOT = Path(__file__).parent.parent
_spec = importlib.util.spec_from_file_location(
    "speed_lab_core", Path(__file__).parent / "speed_lab_core.py")
slc = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(slc)
ds = slc.ds

DECK = ROOT / "decks" / "zero-sum-game-20260707.txt"
SEED = 20260611
TURNS = 12
SHOW = [4, 5, 6, 7, 8, 9, 10, 12]

ROCKS = {"Sol Ring": (1, 2), "Arcane Signet": (2, 1), "Jet Medallion": (2, 1),
         # gcswap variant only (absent from base library)
         "Mana Vault": (1, 3)}

DORKS = {"Birds of Paradise", "Llanowar Elves", "Elvish Mystic",
         "Fyndhorn Elves", "Boreal Druid", "Arbor Elf",
         "Elves of Deep Shadow", "Deathrite Shaman", "Delighted Halfling"}

BLOOD_HALF = {"Exquisite Blood": 5, "Bloodthirsty Conqueror": 5}
VITO_HALF = {"Vito, Thorn of the Dusk Rose": 3, "Sanguine Bond": 5,
             "Enduring Tenacity": 4, "Defiant Bloodlord": 7}
# igniters that fire by themselves every turn once down
SELF_IGNITERS = {"Professor Dellian Fel": 4}
DEATH_IGNITERS = {"Blood Artist": 2, "Zulaport Cutthroat": 2,
                  "Marionette Apprentice": 2}
OUTLETS = {"Viscera Seer": 1, "Witch's Oven": 1, "Warren Soultrader": 3,
           "Ashnod's Altar": 3, "Phyrexian Altar": 3}
TOKEN_MAKERS = {"Bitterblossom": (2, 1, 0),       # (cost, per-turn, on-cast)
                "Tendershoot Dryad": (5, 1, 0),
                "Saproling Migration": (2, 0, 2),
                "Hornet Queen": (7, 0, 5)}
# creatures fetchable by Chord / Finale / Nature's Rhythm (name -> MV)
CREATURE_TARGETS = {"Bloodthirsty Conqueror": 5,
                    "Vito, Thorn of the Dusk Rose": 3,
                    "Enduring Tenacity": 4, "Defiant Bloodlord": 7,
                    "Witherbloom Apprentice": 2, "Cauldron Familiar": 1,
                    "Blood Artist": 2, "Marionette Apprentice": 2,
                    "Zulaport Cutthroat": 2}
CHEAP_IS = {"Lab Rats": 1, "Sprout Swarm": 2, "Dark Ritual": 1,
            "Abrupt Decay": 2, "Assassin's Trophy": 2, "Veil of Summer": 1,
            "Night's Whisper": 2, "Corpse Dance": 3}   # magecraft fuel

IS_CARDS = {"Vampiric Tutor", "Demonic Tutor", "Beseech the Queen",
            "Increasing Ambition", "Dark Petition", "Diabolic Intent",
            "Chord of Calling", "Finale of Devastation", "Nature's Rhythm",
            "Dark Ritual", "Cabal Ritual"} | set(CHEAP_IS)


class Trial:
    def __init__(self, library, rng):
        self.g = slc.Goldfish(library, rng, rocks=ROCKS)
        self.tbl = slc.Table()
        self.bf = set()
        self.entered = {}
        self.dork_out = 0          # mana from dorks deployed BEFORE this turn
        self.dork_new = 0
        self.tokens = 0
        self.bodies = 0            # nontoken creatures on bf (incl. commander)
        self.token_rate = 0
        self.commander = False
        self.life = 40
        self.cast_is_this_turn = False
        self.pending_top = []      # Vampiric targets, arrive next turn
        self.is_in_yard = 0        # for Dark Petition mastery / Cabal threshold
        self.rituals_held = []
        self.prev_creatures = 0    # non-sick bodies+tokens (attack ignition)
        self.combat_ign = True

    # ---- derived ----
    @property
    def creatures(self):
        return self.bodies + self.tokens

    def aff(self, generic):
        """Affinity discount on an I/S generic portion (commander out)."""
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
        """Can a loop-starting life event happen this turn (or any later turn
        with the current board, if future=True)?

        Combat ignition: with the blood-half down, ANY unblocked combat damage
        is an opponent life loss that closes the loop — one non-sick body is
        an igniter under the goldfish unblocked convention. The stricter
        no-combat rows model a blocked-out board (Abolisher does NOT stop
        this either way — triggers aren't cast spells or activations)."""
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
        # Food = "{2}, Sacrifice: gain 3 life" — Goose ETBs with one and makes
        # more; Oven turns any spare body into one. Eating it starts the loop.
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

    # ---- casting helpers ----
    def ritual_boost(self, needed):
        """Pop held rituals to cover a shortfall on a kill-relevant cast."""
        while self.g.avail < needed and self.rituals_held:
            nm = self.rituals_held.pop()
            if nm == "Dark Ritual":
                self.g.add_mana(2)
            else:  # Cabal Ritual
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
        """Name worth tutoring for the given missing slot."""
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

    # ---- one turn ----
    def turn(self, T):
        self._T = T
        g = self.g
        self.cast_is_this_turn = False
        self.dork_out += self.dork_new
        self.dork_new = 0
        self.tokens += self.token_rate
        played = g.begin_turn(T)
        if played == "Khalni Garden":
            self.tokens += 1
        if played == "Dryad Arbor":
            self.bodies += 1
        g.add_mana(self.dork_out)
        g.deploy_rocks()
        if "Necropotence" in self.bf and self.entered["Necropotence"] < T:
            g.draw(3)
        # Vampiric pending arrives
        for nm in self.pending_top:
            g.fetch(nm)
        self.pending_top = []
        # bank rituals from hand (held until a cast needs them)
        for r in ("Dark Ritual", "Cabal Ritual"):
            while g.has(r):
                g.hand.pop(g.in_hand(r))
                self.rituals_held.append(r)
        # Razaketh chains: 2 life + a token per fetch
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
            # 1. combo halves from hand
            for nm, c in list(BLOOD_HALF.items()) + list(VITO_HALF.items()):
                if nm not in self.bf and g.has(nm) and not (
                        self.bf & set(BLOOD_HALF) and nm in BLOOD_HALF) and not (
                        self.bf & set(VITO_HALF) and nm in VITO_HALF):
                    self.ritual_boost(c)
                    if g.avail >= c and self.deploy(
                            nm, c, body=nm != "Exquisite Blood" and nm != "Sanguine Bond"):
                        progress = True
            # 2. igniters
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
            # 3. tutors -> highest missing slot
            miss = self.missing()
            if miss:
                slot = miss[0]
                tgt = self.fetch_for(slot)
                if tgt:
                    if self.cast_any_tutor(tgt):
                        progress = True
            # 4. commander
            if not self.commander:
                c = max(2, 8 - self.creatures)
                if g.cast("Witherbloom, the Balancer", c):
                    self.commander = True
                    self.bodies += 1
                    progress = True
            # 5. engines: Necropotence, Razaketh, outlets, token makers, dorks
            if "Necropotence" not in self.bf and g.has("Necropotence") \
                    and g.avail >= 3:
                self.deploy("Necropotence", 3)
                progress = True
            for nm, (c, rate, burst) in TOKEN_MAKERS.items():
                if nm not in self.bf and g.has(nm) and g.avail >= c:
                    self.deploy(nm, c, body=nm in ("Tendershoot Dryad",
                                                   "Hornet Queen"))
                    self.token_rate += rate
                    self.tokens += burst
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

        # win check
        if (self.bf & set(BLOOD_HALF)) and (self.bf & set(VITO_HALF)) \
                and self.igniter_live():
            self.tbl.kill_all(T)
        self.prev_creatures = self.creatures

    def cast_any_tutor(self, tgt):
        g = self.g
        if not any(g.deck[i][0] == tgt for i in range(g.ptr, len(g.deck))):
            return False
        tgt_cmc = {**BLOOD_HALF, **VITO_HALF,
                   "Witherbloom Apprentice": 2}.get(tgt, 3)
        # creature tutors put it straight onto the battlefield
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
                        # remove fetched card from library
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
        # to-hand tutors
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


def goldfish(library, trials, rng, combat_ign=True):
    out = []
    for _ in range(trials):
        tr = Trial(library, rng)
        tr.combat_ign = combat_ign
        for T in range(1, TURNS + 1):
            tr.turn(T)
            if tr.tbl.done:
                break
        out.append((tr.tbl.decap, tr.tbl.table))
    return out


def report(label, res):
    dec, tab = slc.cum(res, 0, SHOW), slc.cum(res, 1, SHOW)
    print(slc.row(f"{label} decap (cum %)", dec, SHOW))
    print(slc.row(f"{label} table (cum %)", tab, SHOW))
    print(f"    median decap {slc.median(res, 0)} / table {slc.median(res, 1)}")


def mode_clock(index, aliases, trials):
    print("=" * 72)
    print("CLOCK — Zero-Sum Game baseline goldfish "
          f"({trials} trials, seed {SEED})")
    print("=" * 72)
    rng = random.Random(SEED)
    library, commander = slc.load_parsed(DECK, index, aliases)
    print(f"  library {len(library)} + commander "
          f"{commander[0] if commander else '?'}")
    print("  turns:".ljust(44) + "".join(f"{t:6d}" for t in SHOW))
    report("combo kill", goldfish(library, trials, rng))
    rng2 = random.Random(SEED + 1)
    report("no-combat ignition", goldfish(library, trials, rng2,
                                          combat_ign=False))


def mode_gcswap(index, aliases, trials):
    print("=" * 72)
    print("GCSWAP — 3rd GC as fast mana: -Demonic Tutor +Mana Vault")
    print("=" * 72)
    rng = random.Random(SEED)
    library, _ = slc.load_parsed(DECK, index, aliases, warn=False)
    lib = slc.build_lib(library, index, ["Demonic Tutor"], ["Mana Vault"])
    print("  turns:".ljust(44) + "".join(f"{t:6d}" for t in SHOW))
    report("gcswap kill", goldfish(lib, trials, rng))


def mode_avail(index, aliases, trials):
    print("=" * 72)
    print("AVAIL — combo-half availability cross-check vs 2026-06-07 model")
    print("=" * 72)
    rng = random.Random(SEED)
    library, _ = slc.load_parsed(DECK, index, aliases, warn=False)
    groups = [list(BLOOD_HALF), list(VITO_HALF)]
    tutors = ["Demonic Tutor", "Vampiric Tutor", "Beseech the Queen",
              "Increasing Ambition", "Dark Petition", "Diabolic Intent",
              "Chord of Calling", "Finale of Devastation", "Nature's Rhythm",
              "Razaketh, the Foulblooded"]
    drawn, with_t = slc.simulate_groups(library, groups, tutors,
                                        trials, rng, TURNS)
    show = {t: drawn[t] for t in SHOW}
    showt = {t: with_t[t] for t in SHOW}
    print("  turns:".ljust(44) + "".join(f"{t:6d}" for t in SHOW))
    print(slc.row("both halves drawn (%)", show, SHOW))
    print(slc.row("both halves +tutor wildcards (%)", showt, SHOW))


if __name__ == "__main__":
    slc.run_cli(__doc__, {"clock": mode_clock, "gcswap": mode_gcswap,
                          "avail": mode_avail})
