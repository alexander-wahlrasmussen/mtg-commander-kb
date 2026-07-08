#!/usr/bin/env python3
"""dr_clock_lab.py — Diminishing Returns (Teysa Karlov) KILL-TURN goldfish + levers.

Closes the unverified clock flagged 2026-06-10: the Summary's "Goldfish T7-9"
was hand-estimated, never goldfished. Built on speed_lab_core.py.

THE CLOCK HAS TWO COMPONENTS that the lab found do NOT converge: the drain
engine (Zulaport class, hits ALL opponents — the table clock) and the wide
aristocrats board swing (focus-fire — the decap clock). Drain volume =
deaths-per-turn x drain-per-death; deaths are the bottleneck, not multipliers.
Accelerants: Teysa doubling (x2 on death triggers of permanents you control),
Kokusho cycles (5 each, doubled to 10), Gravecrawler loops, Living Death
bursts, and board liquidation once the multiplier is set.

Damage model per creature death, to EACH opponent (oracle-verified 2026-06-10):

    nontoken death: (Zulaport + Elas + Meathook + Konrad + Agent*) x teysa2
    token death:    same + Nadier x teysa2, + Mirkwood (sac trigger, NOT doubled)
    Kokusho death:  + 5 x teysa2
    * Agent of the Iron Throne grants the trigger TO TEYSA (Background) — it is
      live only while Teysa is on the battlefield, and is then doubled by her.

    single-target extras (hit_focus): Sephiroth front face 1 x teysa2 per other
    death, transforming after 4 resolutions in a turn; the back-face EMBLEM
    (1 per death) is NOT doubled (emblems aren't permanents) but persists.

RULES FACTS the model encodes (each checked against card_lookup.py):
  * Teysa doubles death TRIGGERS of permanents you control. Activated abilities
    (Priest of Forgotten Gods, the altars) and ETB triggers (Gray Merchant,
    edicts, Elas's lifegain) are NOT doubled.
  * "Whenever you sacrifice" (Mirkwood Bats) triggers ONCE per Teysa's own
    ruling — sacrificing is not a death trigger.
  * Skullclamp's "equipped creature dies: draw two" IS a death trigger of a
    permanent you control -> Teysa-doubled to draw 4 per 1 mana.
  * Midnight Reaper is MANDATORY (1 damage + draw, doubled), nontoken only.
  * Carrion Feeder and Midnight Reaper are ZOMBIES — either satisfies
    Gravecrawler's recast condition.
  * Gravecrawler recast from the graveyard is a creature SPELL — it feeds
    Endrek Sahr Thrulls and Desecrated Tomb Bats (card leaves the graveyard).
  * INFINITE: Gravecrawler + Phyrexian Altar + another Zombie + >=1 drain
    payoff is mana-neutral and ends the game (kill_all). Pitiless Plunderer
    (lever variant) substitutes for the Altar: death -> Treasure (doubled).
  * K'rrik: each {B} pip payable with 2 life. Modelled as a per-cast discount
    (PIPS table) used only when mana is short and life stays >= 12.
  * Gray Merchant drains devotion to black (ETB, not doubled) — devotion is
    counted live from black pips on the battlefield (PIPS).
  * Vindictive Lich: modes within ONE trigger must target different players,
    so lose-5 fires once per trigger; Teysa's second trigger may pick the
    same or another opponent -> modelled as 5 (x2 with Teysa), focus-fire.
  * Endrek Sahr: X Thrulls per creature spell (X = MV). His 7-Thrull
    self-sacrifice is IGNORED (optimistic: outlets eat Thrulls continuously;
    his own death would trigger the payoffs anyway).

MODELLED PLAY POLICY (the part that took tuning — naive policies deadlock):
greedy engine casts, generic creature cards become clamp/sac fodder, board
LIQUIDATION once Teysa + a payoff are set (cash every non-engine body),
Skullclamp loops (tokens, fodder, the Gravecrawler+Zombie cycle, one engine
body when the hand is empty), Kokusho sac-reanimate cycles, Living Death on a
stocked yard, Razaketh fetching the missing infinite piece, full-board attack
every turn (unblocked; Teysa's tokens have vigilance so there is no defensive
cost in goldfish), Urza's Saga -> 2 Constructs + fetch Skullclamp/Sol Ring.

OMITTED (conservative): Smothering Tithe / Esper Sentinel mana+draw (opponent
behaviour), Phyrexian Tower's {B}{B}, Yahenni indestructibility, Soldevi
Adnate ramp, scry/selection value from Seer / Strider, Morbid beyond 1/turn,
Sephiroth's ETB sac-draw, edict hits on opponents' boards, Constructs above
1 power.
OPTIMISTIC (noted): rocks tap the turn they land, Wayfarer's Bauble as a
3-cost rock, mana is colour-blind (lands+rocks floor), Endrek 7-Thrull cap
ignored, the whole board swings every turn including Teysa, no opposing
interaction. Trust shapes and deltas, not second decimals.

Modes:
  clock   — baseline kill-turn goldfish vs the claimed T7-9.
  levers  — +drains / +tokens / +deathmana / +tutors swap variants (2 cuts
            each: Mother of Runes, Skrelv — the goldfish-deadest slots).
            Demonic/Vampiric tutor axis EXCLUDED: GCs, deck capped 3/3.
  b4      — Bracket-4-in-spirit packages (2026-06-10 follow-up; identity
            change away from Disrupt approved). Adds COMPACT 2-card kills,
            all oracle-verified + GC-screened (none are GCs):
              * Leonin Relic-Warder + Animate Dead/Necromancy (aura already
                in deck): LRW ETB exiles the aura -> aura leaves -> LRW dies
                -> LRW leave-trigger returns the aura -> aura reanimates LRW.
                Infinite ETB/death loop, no mana, no outlet needed once the
                aura targets LRW in the yard. Recruiter fetches LRW (tgh 2).
              * Nim Deathmantle + Grave Titan + Ashnod's Altar (Altar already
                in deck): sac Titan (+CC), pay 4 to Mantle, Titan returns
                with 2 Zombies; sac the Zombies (+CCCC) -> mana-positive
                infinite nontoken deaths. Mantle + 2 spare Titans OWNED, $0.
              * Exquisite Blood + Vito/Sanguine Bond: gain->lose + lose->gain
                closed loop; in THIS deck any Zulaport-class death gain
                starts it. Vito alone converts every gain into single-target
                drain (Kokusho death w/ Teysa = gain 30 -> 30 to a face).
            Plus tutor support (Grim Tutor owned-free, Wishclaw Talisman,
            Final Parting contested-by-Calamity) and a fast-mana control
            axis (Cabal Ritual, Culling the Weak, Jet Medallion owned-free,
            Crypt Ghast). Burnt Offering EXCLUDED: BR identity, not Orzhov.

Data: collection/oracle-cards.json (refresh via update_scryfall_data.py)
Writeup: proposals/Diminishing_Returns_Clock_Lab_2026-06-10.md
"""
import importlib.util
import random
from pathlib import Path

ROOT = Path(__file__).parent.parent
_spec = importlib.util.spec_from_file_location(
    "speed_lab_core", Path(__file__).parent / "speed_lab_core.py")
slc = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(slc)
ds = slc.ds

# Diminishing Returns dismantled 2026-07-08 — decklist archived; this lab is a historical artifact.
DECK = ROOT / "archive" / "old_decklists" / "diminishing-returns-20260505.txt"
SEED = 12345
TURNS = 12
SHOW = [4, 5, 6, 7, 8, 9, 10, 12]

ROCKS = {"Sol Ring": (1, 2), "Arcane Signet": (2, 1), "Fellwar Stone": (2, 1),
         "Mind Stone": (2, 1), "Thought Vessel": (2, 1),
         "Wayfarer's Bauble": (3, 1),
         # b4 variants: Medallion approximated as a rock (deck is ~all black)
         "Jet Medallion": (2, 1)}

# black pips for devotion + K'rrik discounts (battlefield permanents only)
PIPS = {"Teysa Karlov": 1, "Zulaport Cutthroat": 1, "Elas il-Kor, Sadistic Pilgrim": 1,
        "The Meathook Massacre": 2, "Nadier's Nightblade": 1, "Syr Konrad, the Grim": 2,
        "Midnight Reaper": 1, "Kokusho, the Evening Star": 2, "Vindictive Lich": 1,
        "Sephiroth, Fabled SOLDIER": 1, "Agent of the Iron Throne": 1,
        "Gray Merchant of Asphodel": 2, "Razaketh, the Foulblooded": 3,
        "K'rrik, Son of Yawgmoth": 3, "Endrek Sahr, Master Breeder": 1,
        "Gravecrawler": 1, "Stitcher's Supplier": 1, "Carrion Feeder": 1,
        "Viscera Seer": 1, "Yahenni, Undying Partisan": 1, "Woe Strider": 1,
        "Priest of Forgotten Gods": 1, "Mirkwood Bats": 1, "Morbid Opportunist": 1,
        "Plaguecrafter": 1, "Merciless Executioner": 1, "Dark Confidant": 1,
        "Soldevi Adnate": 1,
        "Bastion of Remembrance": 1, "Cruel Celebrant": 1, "Bitterblossom": 1,
        "Ophiomancer": 1, "Pitiless Plunderer": 1, "Pawn of Ulamog": 2,
        "Vito, Thorn of the Dusk Rose": 1, "Exquisite Blood": 1,
        "Sanguine Bond": 2, "Grave Titan": 2, "Crypt Ghast": 1}

ZOMBIES = {"Gravecrawler", "Gray Merchant of Asphodel", "Midnight Reaper",
           "Stitcher's Supplier", "Carrion Feeder"}
# battlefield names that are NOT creatures (survive Living Death's sac)
NONCREATURE_BF = {"The Meathook Massacre", "Agent of the Iron Throne",
                  "Bitterblossom", "Bastion of Remembrance", "Skullclamp",
                  "Phyrexian Altar", "Ashnod's Altar", "Altar of Dementia",
                  "Desecrated Tomb", "Exquisite Blood", "Sanguine Bond",
                  "Nim Deathmantle", "Wishclaw Talisman"}
FREE_OUTLETS = {"Viscera Seer", "Carrion Feeder", "Yahenni, Undying Partisan",
                "Woe Strider", "Altar of Dementia", "Ashnod's Altar",
                "Phyrexian Altar"}
# each-opponent drain payoffs, all Teysa-doubled (Agent gated on Teysa in code)
PAYOFFS = {"Zulaport Cutthroat", "Elas il-Kor, Sadistic Pilgrim",
           "The Meathook Massacre", "Syr Konrad, the Grim",
           "Bastion of Remembrance", "Cruel Celebrant"}
# subset of PAYOFFS that ALSO gain YOU life on your own creature's death — the
# only cards that feed the Vito/Sanguine-Bond/Exquisite-Blood lifegain loop.
# Verified vs card_lookup 2026-06-29: Zulaport / Cruel Celebrant / Bastion read
# "each opponent loses 1 AND you gain 1" (gain 1 TOTAL, not per opponent). Elas's
# lifegain is on ETB not death, Meathook gains only when an OPPONENT's creature
# dies, and Syr Konrad / Agent deal loss/damage with no lifegain — so the per-
# death drain (`d`) must NOT be re-credited wholesale as life (it over-credited).
GAIN_PAYOFFS = {"Zulaport Cutthroat", "Cruel Celebrant", "Bastion of Remembrance"}
EXPENDABLE = {"Stitcher's Supplier", "Plaguecrafter", "Merciless Executioner",
              "Gravecrawler"}          # nontokens we sac freely once spent
REANIMATE_ORDER = ["Kokusho, the Evening Star", "Gray Merchant of Asphodel",
                   "Grave Titan", "Razaketh, the Foulblooded",
                   "Sephiroth, Fabled SOLDIER", "Endrek Sahr, Master Breeder"]
# printed power for the full-board swing (goldfish: unblocked, vigilance
# tokens mean no defensive cost; verified vs oracle 2026-06-10)
ATTACK_POWER = {"Kokusho, the Evening Star": 5, "Razaketh, the Foulblooded": 8,
                "Sephiroth, Fabled SOLDIER": 3, "Gravecrawler": 2,
                "Syr Konrad, the Grim": 5, "Midnight Reaper": 3,
                "Woe Strider": 3, "Elas il-Kor, Sadistic Pilgrim": 2,
                "Vindictive Lich": 4, "Plaguecrafter": 3,
                "Merciless Executioner": 3, "Yahenni, Undying Partisan": 2,
                "Zulaport Cutthroat": 1, "Endrek Sahr, Master Breeder": 2,
                "Gray Merchant of Asphodel": 2, "K'rrik, Son of Yawgmoth": 2,
                "Dark Confidant": 2, "Mirkwood Bats": 2,
                "Nadier's Nightblade": 1, "Morbid Opportunist": 1,
                "Carrion Feeder": 1, "Viscera Seer": 1,
                "Stitcher's Supplier": 1, "Priest of Forgotten Gods": 1,
                "Recruiter of the Guard": 1, "Soldevi Adnate": 1,
                "Cruel Celebrant": 1, "Ophiomancer": 2,
                "Pitiless Plunderer": 1, "Pawn of Ulamog": 2,
                "Grave Titan": 6, "Leonin Relic-Warder": 2,
                "Vito, Thorn of the Dusk Rose": 1, "Crypt Ghast": 2}

# kept back during board liquidation (the drain/draw engine itself)
LIQUIDATE_KEEP = PAYOFFS | {"Midnight Reaper", "Sephiroth, Fabled SOLDIER",
                            "K'rrik, Son of Yawgmoth", "Razaketh, the Foulblooded",
                            "Mirkwood Bats", "Nadier's Nightblade",
                            "Morbid Opportunist", "Endrek Sahr, Master Breeder"}

# cast priority: (name, cost) — effects wired by name in the chain
CASTS = [
    ("Viscera Seer", 1), ("Carrion Feeder", 1), ("Skullclamp", 1),
    ("Gravecrawler", 1), ("Stitcher's Supplier", 1),
    ("Zulaport Cutthroat", 2), ("Elas il-Kor, Sadistic Pilgrim", 2),
    ("The Meathook Massacre", 2),                  # X=0, pure enchant drains
    ("Cruel Celebrant", 2), ("Bitterblossom", 2),
    ("Altar of Dementia", 2), ("Priest of Forgotten Gods", 2),
    ("Sephiroth, Fabled SOLDIER", 3), ("Agent of the Iron Throne", 3),
    ("Midnight Reaper", 3), ("Nadier's Nightblade", 3),
    ("Bastion of Remembrance", 3), ("Ophiomancer", 3), ("Pawn of Ulamog", 3),
    ("Woe Strider", 3), ("Yahenni, Undying Partisan", 3),
    ("Phyrexian Altar", 3), ("Ashnod's Altar", 3),
    ("Recruiter of the Guard", 3), ("Desecrated Tomb", 3),
    ("Plaguecrafter", 3), ("Merciless Executioner", 3),
    ("Mirkwood Bats", 4), ("Pitiless Plunderer", 4),
    ("Morbid Opportunist", 3), ("Dark Confidant", 2),
    # b4-mode pieces (absent from the base library = never cast)
    ("Leonin Relic-Warder", 2), ("Vito, Thorn of the Dusk Rose", 3),
    ("Nim Deathmantle", 2), ("Wishclaw Talisman", 2), ("Crypt Ghast", 4),
    ("Exquisite Blood", 5), ("Sanguine Bond", 5),
    ("Syr Konrad, the Grim", 5), ("Endrek Sahr, Master Breeder", 5),
    ("Gray Merchant of Asphodel", 5), ("Kokusho, the Evening Star", 6),
    ("Grave Titan", 6),
    ("Razaketh, the Foulblooded", 8),
]
COST = dict(CASTS)


class Trial:
    def __init__(self, library, rng):
        self.g = slc.Goldfish(library, rng, rocks=ROCKS)
        self.tbl = slc.Table()
        self.bf = set()                 # nontoken permanents on the battlefield
        self.entered = {}               # name -> turn (summoning sickness)
        self.dead = []                  # creature names in the graveyard
        self.tok_ready = 0
        self.tok_new = 0
        self.life = 40
        self.teysa = False
        self.sephi_back = False         # transformed; emblem live
        self.sephi_res = 0              # front-face resolutions this turn
        self.morbid_drawn = False
        self.fodder = 0                 # generic nontoken bodies (clamp/sac fuel)
        self._T = 1

    # -- drain math -----------------------------------------------------------
    @property
    def mult(self):
        return 2 if self.teysa else 1

    def per_death(self, token):
        base = sum(1 for p in PAYOFFS if p in self.bf)
        if "Agent of the Iron Throne" in self.bf and self.teysa:
            base += 1
        d = base * self.mult
        if token:
            d += (self.mult if "Nadier's Nightblade" in self.bf else 0)
            d += (1 if "Mirkwood Bats" in self.bf else 0)   # sac trig, undoubled
        return d

    def per_death_gain(self, token):
        """Life YOU gain per creature death — Zulaport-class lifegain ONLY,
        Teysa-doubled. NOT the per-opponent drain: "each opponent loses 1 and
        you gain 1" gains 1 TOTAL, not 1 per opponent, so the gain tallies the
        GAIN_PAYOFFS count, not the (larger) drain count `d`."""
        g = sum(1 for p in GAIN_PAYOFFS if p in self.bf) * self.mult
        if token and "Nadier's Nightblade" in self.bf:
            g += self.mult       # "a token you control leaves" -> you gain 1
        return g

    def gain(self, x, T):
        """Lifegain event: Vito / Sanguine Bond convert it to single-target
        drain; Exquisite Blood + either closes the loop = table kill."""
        if x <= 0:
            return
        self.life += x
        bond = ("Vito, Thorn of the Dusk Rose" in self.bf
                or "Sanguine Bond" in self.bf)
        if bond:
            self.tbl.hit_focus(x, T)
            if "Exquisite Blood" in self.bf:
                self.tbl.kill_all(T)

    def make_tokens(self, k):
        self.tok_new += k
        if k and "Mirkwood Bats" in self.bf:    # creation trigger, conservative:
            self.tbl.hit_all(1, self._T)        # 1 per event, not per token

    def spend_token(self):
        if self.tok_new:
            self.tok_new -= 1
            return True
        if self.tok_ready:
            self.tok_ready -= 1
            return True
        return False

    def spend_body(self, T):
        """Sacrifice any expendable body (token first, then generic fodder).
        Applies the death triggers; returns True if something died."""
        if self.spend_token():
            self.die(1, True, T)
            return True
        if self.fodder:
            self.fodder -= 1
            self.die(1, False, T)
            return True
        return False

    def die(self, k, token, T, names=()):
        """k creature deaths (all token or all nontoken). Applies drains,
        Sephiroth, Reaper draws, death-mana. names -> graveyard."""
        if k <= 0:
            return
        d = self.per_death(token) * k
        if d:
            self.tbl.hit_all(d, T)
        gained = self.per_death_gain(token) * k             # Zulaport-class gain only
        if gained:
            self.gain(gained, T)
        # Sephiroth: front face single-target, doubled; 4 resolutions = flip
        if "Sephiroth, Fabled SOLDIER" in self.bf:
            if not self.sephi_back:
                r = k * self.mult
                self.tbl.hit_focus(r, T)
                self.sephi_res += r
                if self.sephi_res >= 4:
                    self.sephi_back = True
            else:
                self.tbl.hit_focus(k, T)                    # emblem, undoubled
        if not token:
            if "Midnight Reaper" in self.bf and self.life > 8:
                n = min(k * self.mult, self.life - 8)
                self.g.draw(n); self.life -= n
            if "Pawn of Ulamog" in self.bf:
                self.g.add_mana(k * self.mult)
        if "Pitiless Plunderer" in self.bf:
            self.g.add_mana(k * self.mult)
        if "Morbid Opportunist" in self.bf and not self.morbid_drawn:
            self.g.draw(1); self.morbid_drawn = True
        if "Altar of Dementia" in self.bf:      # self-mill stocks the yard
            for mn in self.g.mill(k):
                if mn in REANIMATE_ORDER or mn == "Gravecrawler":
                    self.dead.append(mn)
        for nm in names:
            self.bf.discard(nm)
            self.dead.append(nm)
            if nm == "Vindictive Lich":   # lose-5 mode, once per trigger
                self.tbl.hit_focus(5, T)
                if self.mult == 2:
                    self.tbl.hit_focus(5, T)
            elif nm == "Kokusho, the Evening Star":
                self.tbl.hit_all(5 * self.mult, T)
                self.gain(15 * self.mult, T)

    def resolve_living_death(self, T):
        """Resolve a cast Living Death: sacrifice all YOUR creatures (the death
        burst drains), then return ONLY the creature cards that were already in
        YOUR graveyard when it resolved. Per the oracle + ruling (card_lookup
        2026-06-29), Living Death exiles graveyard creatures FIRST, THEN
        sacrifices the board, so the board sacrificed here does NOT come back —
        the returnable set is snapshotted BEFORE die(creatures_bf) dumps the
        board into self.dead, else it over-returns the whole board. Returns the
        names put back onto the battlefield. (Goldfish models only your side.)"""
        creatures_bf = [n for n in self.bf if n not in NONCREATURE_BF]
        returnable = list(self.dead)                 # snapshot: yard at resolution
        ntok = self.tok_ready + self.tok_new
        self.die(ntok, True, T)
        self.tok_ready = self.tok_new = 0
        self.die(len(creatures_bf), False, T, names=creatures_bf)
        for nm in returnable:
            self.dead.remove(nm); self.bf.add(nm); self.entered[nm] = T
            if nm == "Grave Titan":
                self.make_tokens(2)
            if nm == "Gray Merchant of Asphodel":
                x = self.devotion()
                self.tbl.hit_all(x, T); self.gain(3 * x, T)
        return returnable

    # -- helpers ----------------------------------------------------------------
    def devotion(self):
        return sum(PIPS.get(n, 0) for n in self.bf) + (1 if self.teysa else 0)

    def outlet(self):
        return any(o in self.bf for o in FREE_OUTLETS)

    def zombie_support(self):
        return any(z in self.bf for z in ZOMBIES if z != "Gravecrawler")

    def kcost(self, nm, cost):
        """Effective cost after K'rrik pips, and the life it would burn."""
        if "K'rrik, Son of Yawgmoth" not in self.bf:
            return cost, 0
        use = min(PIPS.get(nm, 0), max(0, cost - self.g.avail))
        if self.life - 2 * use < 12:
            use = 0
        return cost - use, 2 * use

    def cast_named(self, nm, cost, T):
        c, lf = self.kcost(nm, cost)
        i = self.g.in_hand(nm)
        if i is None or self.g.avail < c:
            return False
        is_creature = "creature" in self.g.hand[i][1]["type_line"].lower()
        self.g.cast(nm, c)
        self.life -= lf
        self.bf.add(nm)
        if is_creature:
            self.entered[nm] = T
            if ("Endrek Sahr, Master Breeder" in self.bf
                    and nm != "Endrek Sahr, Master Breeder"):
                self.make_tokens(int(COST.get(nm, 1)))
        return True


DEBUG_STATS = None      # set to a list to collect per-trial end-state dicts


def goldfish_kill(library, rng, index):
    t = Trial(library, rng)
    g, tbl = t.g, t.tbl

    def infinite_ready():
        if t.per_death(False) < 1:
            return False
        # b4: Nim Deathmantle + Grave Titan + Ashnod's Altar, 4 mana to start
        if ({"Nim Deathmantle", "Grave Titan", "Ashnod's Altar"} <= t.bf
                and g.avail >= 4):
            return True
        # b4: Leonin Relic-Warder + Animate Dead/Necromancy loop
        for a, c in (("Animate Dead", 2), ("Necromancy", 3)):
            if g.in_hand(a) is None:
                continue
            if "Leonin Relic-Warder" in t.dead and g.avail >= c:
                return True
            if ("Leonin Relic-Warder" in t.bf and t.outlet()
                    and g.avail >= c):
                return True
            if (g.in_hand("Leonin Relic-Warder") is not None and t.outlet()
                    and g.avail >= c + 2):
                return True
        # Gravecrawler + Phyrexian Altar (or Plunderer) + Zombie
        gc = "Gravecrawler" in t.bf or "Gravecrawler" in t.dead
        if not (gc and t.zombie_support()):
            return False
        if "Phyrexian Altar" in t.bf:
            return True
        if "Pitiless Plunderer" in t.bf and t.outlet():
            return True                                      # Treasure pays {B}
        return False

    def combo_want():
        """Best single fetch targets, most game-winning first."""
        w = []
        aura_held = (g.in_hand("Animate Dead") is not None
                     or g.in_hand("Necromancy") is not None)
        lrw_near = ("Leonin Relic-Warder" in t.dead
                    or "Leonin Relic-Warder" in t.bf
                    or g.in_hand("Leonin Relic-Warder") is not None)
        if aura_held and not lrw_near:
            w.append("Leonin Relic-Warder")
        if lrw_near and not aura_held:
            w += ["Animate Dead", "Necromancy"]
        if {"Grave Titan", "Ashnod's Altar"} <= t.bf:
            w.append("Nim Deathmantle")
        if {"Nim Deathmantle", "Ashnod's Altar"} <= t.bf:
            w.append("Grave Titan")
        if "Exquisite Blood" in t.bf:
            w += ["Vito, Thorn of the Dusk Rose", "Sanguine Bond"]
        if ("Vito, Thorn of the Dusk Rose" in t.bf
                or "Sanguine Bond" in t.bf):
            w.append("Exquisite Blood")
        if (("Gravecrawler" in t.bf or "Gravecrawler" in t.dead)
                and t.zombie_support()):
            w.append("Phyrexian Altar")
        w += ["Leonin Relic-Warder", "Exquisite Blood",
              "Vito, Thorn of the Dusk Rose", "Nim Deathmantle",
              "Grave Titan", "Kokusho, the Evening Star",
              "Phyrexian Altar", "Skullclamp", "Zulaport Cutthroat"]
        return w

    def fetch_best():
        for w in combo_want():
            if (w not in t.bf and g.in_hand(w) is None
                    and w not in t.dead and g.fetch(w)):
                return w
        return None

    def reanimate(T):
        """One reanimation spell from hand onto the best dead target."""
        for sp, cost in (("Reanimate", 1), ("Animate Dead", 2),
                         ("Necromancy", 3), ("Victimize", 3)):
            if g.in_hand(sp) is None:
                continue
            if (sp in ("Animate Dead", "Necromancy")
                    and "Leonin Relic-Warder" in t.dead
                    and t.per_death(False) >= 1):
                continue                  # hold the aura: it IS the win
            targets = [n for n in REANIMATE_ORDER if n in t.dead]
            if not targets:
                return False
            if sp == "Victimize":
                if t.tok_ready + t.tok_new + t.fodder < 1 or len(targets) < 2:
                    continue
                c, lf = t.kcost(sp, cost)
                if g.avail < c:
                    continue
                g.cast(sp, c); t.life -= lf
                t.spend_body(T)
                for nm in targets[:2]:
                    t.dead.remove(nm); t.bf.add(nm); t.entered[nm] = T
                    if nm == "Grave Titan":
                        t.make_tokens(2)
                    if nm == "Gray Merchant of Asphodel":
                        x = t.devotion()
                        tbl.hit_all(x, T); t.gain(3 * x, T)
                return True
            c, lf = t.kcost(sp, cost)
            if g.avail < c:
                continue
            nm = targets[0]
            g.cast(sp, c); t.life -= lf
            if sp == "Reanimate":
                t.life -= int(COST.get(nm, 3))
            t.dead.remove(nm); t.bf.add(nm); t.entered[nm] = T
            if nm == "Grave Titan":
                t.make_tokens(2)
            if nm == "Gray Merchant of Asphodel":
                x = t.devotion()
                tbl.hit_all(x, T); t.gain(3 * x, T)
            return True
        return False

    def chain(T):
        acted = True
        while acted and not tbl.done:
            acted = False
            g.deploy_rocks()
            # commander once an outlet or payoff exists (or by T5 regardless)
            if not t.teysa and g.avail >= 4 and (
                    t.outlet() or t.per_death(False) > 0 or T >= 5):
                g.pay(4); t.teysa = True
                if "Endrek Sahr, Master Breeder" in t.bf:
                    t.make_tokens(4)
                acted = True; continue
            # K'rrik off raw mana + 6 life
            if ("K'rrik, Son of Yawgmoth" not in t.bf
                    and g.in_hand("K'rrik, Son of Yawgmoth") is not None
                    and g.avail >= 4 and t.life >= 22):
                g.cast("K'rrik, Son of Yawgmoth", 4); t.life -= 6
                t.bf.add("K'rrik, Son of Yawgmoth")
                t.entered["K'rrik, Son of Yawgmoth"] = T
                if "Endrek Sahr, Master Breeder" in t.bf:
                    t.make_tokens(7)
                acted = True; continue
            # Dark Ritual when it unlocks anything
            if g.in_hand("Dark Ritual") is not None and g.avail >= 1:
                g.cast("Dark Ritual", 1); g.add_mana(3)
                acted = True; continue
            # priority cast table
            for nm, cost in CASTS:
                if nm in t.bf or g.in_hand(nm) is None:
                    continue
                if t.cast_named(nm, cost, T):
                    if nm == "Woe Strider":
                        t.make_tokens(1)
                    elif nm == "Stitcher's Supplier":
                        for mn in g.mill(3):
                            if mn in REANIMATE_ORDER or mn == "Gravecrawler":
                                t.dead.append(mn)
                    elif nm == "Bastion of Remembrance":
                        t.make_tokens(1)
                    elif nm == "Grave Titan":
                        t.make_tokens(2)
                    elif nm == "Gray Merchant of Asphodel":
                        x = t.devotion()
                        tbl.hit_all(x, T); t.gain(3 * x, T)
                    elif nm == "Recruiter of the Guard":
                        aura_held = (g.in_hand("Animate Dead") is not None
                                     or g.in_hand("Necromancy") is not None)
                        wants = (("Leonin Relic-Warder",) if aura_held else ()) + (
                            "Viscera Seer", "Zulaport Cutthroat",
                            "Gravecrawler", "Carrion Feeder",
                            "Stitcher's Supplier")
                        for w in wants:
                            if w not in t.bf and g.in_hand(w) is None:
                                if g.fetch(w):
                                    break
                    acted = True
                    break
            if acted:
                continue
            # Buried Alive (lever variant): stock the yard
            if g.in_hand("Buried Alive") is not None and g.avail >= 3:
                g.cast("Buried Alive", 3)
                got = 0
                for w in ("Kokusho, the Evening Star", "Gray Merchant of Asphodel",
                          "Gravecrawler", "Razaketh, the Foulblooded"):
                    if got >= 3:
                        break
                    if w not in t.bf and w not in t.dead and g.fetch(w):
                        i = g.in_hand(w)
                        g.yard.append(g.hand.pop(i))
                        t.dead.append(w); got += 1
                acted = True; continue
            # Diabolic Intent (lever variant): sac a token, tutor a combo piece
            if (g.in_hand("Diabolic Intent") is not None and g.avail >= 2
                    and t.tok_ready + t.tok_new + t.fodder >= 1):
                g.cast("Diabolic Intent", 2)
                t.spend_body(T)
                for w in ("Phyrexian Altar", "Kokusho, the Evening Star",
                          "Zulaport Cutthroat", "Gravecrawler", "Skullclamp"):
                    if w not in t.bf and g.in_hand(w) is None and w not in t.dead:
                        if g.fetch(w):
                            break
                acted = True; continue
            # compact tutors (b4 variants): fetch the missing combo piece
            tutored = False
            for tn, tc, tl in (("Vampiric Tutor", 1, 2), ("Demonic Tutor", 2, 0),
                               ("Grim Tutor", 3, 3), ("Wishclaw Talisman", 3, 0)):
                if g.in_hand(tn) is not None and g.avail >= tc:
                    g.cast(tn, tc)
                    t.life -= tl
                    fetch_best()      # Vampiric: to-top modelled as to-hand
                    tutored = True
                    break
            if tutored:
                acted = True; continue
            # Final Parting: one to hand, one to the yard
            if g.in_hand("Final Parting") is not None and g.avail >= 5:
                g.cast("Final Parting", 5)
                fetch_best()
                for w in REANIMATE_ORDER:
                    if w not in t.bf and w not in t.dead and g.fetch(w):
                        i = g.in_hand(w)
                        g.yard.append(g.hand.pop(i))
                        t.dead.append(w)
                        break
                acted = True; continue
            # rituals (b4 variants)
            if g.in_hand("Cabal Ritual") is not None and g.avail >= 2:
                thr = 5 if (len(g.yard) + len(t.dead)) >= 7 else 3
                g.cast("Cabal Ritual", 2); g.add_mana(thr)
                acted = True; continue
            if (g.in_hand("Culling the Weak") is not None and g.avail >= 1
                    and t.tok_ready + t.tok_new + t.fodder >= 1):
                g.cast("Culling the Weak", 1)
                t.spend_body(T)           # the sac IS a death trigger
                g.add_mana(4)
                acted = True; continue
            # reanimation
            if reanimate(T):
                acted = True; continue
            # Living Death: mass rebirth when the yard is stocked (the mass
            # death of your own board is itself a drain burst)
            ld_targets = [n for n in t.dead if n in REANIMATE_ORDER]
            if (g.in_hand("Living Death") is not None
                    and (len(ld_targets) >= 2 or len(t.dead) >= 4)):
                c, lf = t.kcost("Living Death", 5)
                if g.avail >= c:
                    g.cast("Living Death", c); t.life -= lf
                    t.resolve_living_death(T)
                    acted = True; continue
            # Vindictive Lich as a body late (death value not modelled)
            if t.per_death(False) >= 2 and g.in_hand("Vindictive Lich") is not None:
                if t.cast_named("Vindictive Lich", 4, T):
                    acted = True; continue
            # generic fodder: any remaining creature card becomes clamp/sac
            # fuel (Mother of Runes, Selfless Spirit etc. are real bodies)
            cands = sorted(
                ((i, nm, rec) for i, (nm, rec) in enumerate(g.hand)
                 if "creature" in rec["type_line"].lower()
                 and rec["cmc"] <= g.avail),
                key=lambda x: x[2]["cmc"])
            if cands:
                i, nm, rec = cands[0]
                g.hand.pop(i)
                g.pay(rec["cmc"])
                t.fodder += 1
                if "Endrek Sahr, Master Breeder" in t.bf:
                    t.make_tokens(max(1, int(rec["cmc"])))
                acted = True; continue

    def sac_phase(T):
        # Kokusho cycle: sac for 5 x mult each, as often as reanimation allows
        while ("Kokusho, the Evening Star" in t.bf and t.outlet()
               and not tbl.done):
            t.die(1, False, T, names=["Kokusho, the Evening Star"])
            if not reanimate(T):
                break
        if tbl.done:
            return
        # Priest of Forgotten Gods, once
        if ("Priest of Forgotten Gods" in t.bf
                and t.entered.get("Priest of Forgotten Gods", T) < T
                and t.tok_ready + t.tok_new >= 2):
            t.spend_token(); t.spend_token()
            tbl.hit_all(2, T)
            t.die(2, True, T)
            g.add_mana(2); g.draw(1)
        # Gravecrawler loop: finite (mana- or life-bounded)
        if (("Gravecrawler" in t.bf or "Gravecrawler" in t.dead)
                and t.zombie_support() and t.outlet()
                and t.per_death(False) >= 1):
            if "Gravecrawler" in t.bf:
                t.die(1, False, T, names=["Gravecrawler"])
            loops = int(g.avail)
            if "K'rrik, Son of Yawgmoth" in t.bf:
                loops += max(0, int(t.life - 16) // 2)
            for _ in range(min(loops, 30)):
                if tbl.done:
                    break
                if g.avail >= 1:
                    g.pay(1)
                else:
                    t.life -= 2
                t.dead.remove("Gravecrawler")
                if "Endrek Sahr, Master Breeder" in t.bf:
                    t.make_tokens(1)
                if "Desecrated Tomb" in t.bf:
                    t.make_tokens(1)
                t.die(1, False, T, names=["Gravecrawler"])
        if tbl.done:
            return
        # Razaketh: convert spare fodder into the missing combo pieces
        if "Razaketh, the Foulblooded" in t.bf:
            for _ in range(3):
                if tbl.done or t.life <= 12:
                    break
                if t.tok_ready + t.tok_new + t.fodder < 1:
                    break
                if not t.spend_body(T):
                    break
                t.life -= 2
                fetch_best()
        # Skullclamp: bodies -> cards (death trigger of a permanent you
        # control -> Teysa-doubled: draw 4 per 1 mana)
        if "Skullclamp" in t.bf:
            while (g.avail >= 1 and t.tok_ready + t.tok_new >= 1
                   and len(g.hand) < 7 and not tbl.done):
                g.pay(1)
                t.spend_token()
                t.die(1, True, T)
                g.draw(2 * t.mult)
            while (g.avail >= 1 and t.fodder >= 1
                   and len(g.hand) < 7 and not tbl.done):
                g.pay(1)
                t.fodder -= 1
                t.die(1, False, T)
                g.draw(2 * t.mult)
            # hand empty: clamp one engine body (it rebuys via recursion)
            if not g.hand and g.avail >= 1 and not tbl.done:
                victim = next((n for n in t.bf if n in ATTACK_POWER
                               and n not in PAYOFFS), None)
                if victim is not None:
                    g.pay(1)
                    t.die(1, False, T, names=[victim])
                    g.draw(2 * t.mult)
            # Gravecrawler clamp cycle: {B} recast + {1} equip per draw
            if (("Gravecrawler" in t.bf or "Gravecrawler" in t.dead)
                    and t.zombie_support()):
                while g.avail >= 2 and len(g.hand) < 7 and not tbl.done:
                    if "Gravecrawler" in t.bf:
                        t.bf.discard("Gravecrawler")
                    else:
                        t.dead.remove("Gravecrawler")
                        if "Endrek Sahr, Master Breeder" in t.bf:
                            t.make_tokens(1)
                        if "Desecrated Tomb" in t.bf:
                            t.make_tokens(1)
                    g.pay(2)
                    t.die(1, False, T, names=["Gravecrawler"])
                    g.draw(2 * t.mult)
        # mass token sac once each death drains
        if t.outlet() and t.per_death(True) >= 1 and not tbl.done:
            k = t.tok_ready + t.tok_new
            t.tok_ready = t.tok_new = 0
            t.die(k, True, T)
        # expendable nontokens + generic fodder
        if t.outlet() and t.per_death(False) >= 1 and not tbl.done:
            spent = [n for n in t.bf if n in EXPENDABLE
                     and not (n == "Gravecrawler" and not t.zombie_support())]
            t.die(len(spent), False, T, names=spent)
            t.die(t.fodder, False, T)
            t.fodder = 0
        # board liquidation: once Teysa + a payoff are set (>=2 per death),
        # cash every non-engine body into the outlet — aristocrats endgame
        if t.outlet() and t.per_death(False) >= 2 and not tbl.done:
            cash = [n for n in t.bf if n not in LIQUIDATE_KEEP
                    and n not in NONCREATURE_BF]
            t.die(len(cash), False, T, names=cash)

    saga_turn = None
    for T in range(1, TURNS + 1):
        t._T = T
        played = g.begin_turn(T)
        if played == "Urza's Saga":
            saga_turn = T
        if saga_turn is not None and T == saga_turn + 2:
            # chapter III: 2 Construct tokens landed (ch. I-II), fetch a
            # 0/1-cost artifact, Saga sacrifices itself
            t.make_tokens(2)
            g.lands -= 1
            for w in ("Skullclamp", "Sol Ring"):
                if w not in t.bf and g.in_hand(w) is None and g.fetch(w):
                    break
            saga_turn = None
        t.morbid_drawn = False
        t.sephi_res = 0
        if "Dark Confidant" in t.bf and t.entered.get("Dark Confidant", T) < T:
            g.draw(1); t.life -= 3
        if "Bitterblossom" in t.bf:
            t.make_tokens(1); t.life -= 1
        if "Ophiomancer" in t.bf:
            t.make_tokens(1)
        if "Crypt Ghast" in t.bf and t.entered.get("Crypt Ghast", T) < T:
            g.add_mana(2)                 # ~half the lands are Swamps
        g.deploy_rocks()
        chain(T)
        if infinite_ready():
            tbl.kill_all(T)
        if tbl.done:
            break
        # combat: tokens + the whole board, unblocked focus-fire
        atk = t.tok_ready + min(t.fodder, 3)
        for nm in t.bf:
            if nm in ATTACK_POWER and t.entered.get(nm, T) < T:
                p = ATTACK_POWER[nm]
                atk += 5 if (nm.startswith("Sephiroth") and t.sephi_back) else p
        if t.teysa:
            atk += 2                       # Teysa herself, 2/4 vigilant board
        # Sephiroth attack trigger: sac 1, draw 1
        if ("Sephiroth, Fabled SOLDIER" in t.bf
                and t.entered.get("Sephiroth, Fabled SOLDIER", T) < T
                and t.tok_ready >= 1):
            t.tok_ready -= 1
            t.die(1, True, T)
            g.draw(1)
        if atk:
            tbl.hit_focus(atk, T)
        if tbl.done:
            break
        sac_phase(T)
        if infinite_ready():
            tbl.kill_all(T)
        if tbl.done:
            break
        chain(T)                       # spend death-mana / drawn cards
        if infinite_ready():
            tbl.kill_all(T)
        if tbl.done:
            break
        t.tok_ready += t.tok_new
        t.tok_new = 0

    if DEBUG_STATS is not None:
        DEBUG_STATS.append(dict(
            teysa=t.teysa, lands=g.lands, bf=sorted(t.bf),
            payoffs=sum(1 for p in PAYOFFS if p in t.bf),
            outlet=t.outlet(), dmg=tbl.dmg, life=t.life,
            tokens=t.tok_ready + t.tok_new, dead=len(t.dead)))
    return tbl.decap, tbl.table


VARIANTS = {
    "BASE (current list)": ([], []),
    "+drains  (-Mother of Runes -Skrelv +Bastion of Remembrance +Cruel Celebrant)":
        (["Mother of Runes", "Skrelv, Defector Mite"],
         ["Bastion of Remembrance", "Cruel Celebrant"]),
    "+tokens  (-Mother -Skrelv +Bitterblossom +Ophiomancer)":
        (["Mother of Runes", "Skrelv, Defector Mite"],
         ["Bitterblossom", "Ophiomancer"]),
    "+deathmana (-Mother -Skrelv +Pitiless Plunderer +Pawn of Ulamog)":
        (["Mother of Runes", "Skrelv, Defector Mite"],
         ["Pitiless Plunderer", "Pawn of Ulamog"]),
    "+tutors  (-Mother -Skrelv +Buried Alive +Diabolic Intent)":
        (["Mother of Runes", "Skrelv, Defector Mite"],
         ["Buried Alive", "Diabolic Intent"]),
    "+best4   (-also Generous Gift, Swiftfoot Boots; best two axes combined)":
        (["Mother of Runes", "Skrelv, Defector Mite",
          "Generous Gift", "Swiftfoot Boots"],
         ["Bastion of Remembrance", "Cruel Celebrant",
          "Pitiless Plunderer", "Bitterblossom"]),
}

# Bracket-4-in-spirit packages. Cuts come from the protection/removal shell
# (identity change away from Disrupt approved 2026-06-10).
CUTS6 = ["Mother of Runes", "Giver of Runes", "Skrelv, Defector Mite",
         "Selfless Spirit", "Generous Gift", "Swiftfoot Boots"]
CUTS10 = CUTS6 + ["Cathar Commando", "Morbid Opportunist",
                  "Wayfarer's Bauble", "Vindictive Lich"]
VARIANTS_B4 = {
    "BASE (current list)": ([], []),
    "b4-combo6 (+LRW +Vito +ExquisiteBlood +GraveTitan +Deathmantle +GrimTutor)":
        (CUTS6, ["Leonin Relic-Warder", "Vito, Thorn of the Dusk Rose",
                 "Exquisite Blood", "Grave Titan", "Nim Deathmantle",
                 "Grim Tutor"]),
    "b4-mana4  (+Cabal Ritual +Culling the Weak +Jet Medallion +Crypt Ghast)":
        (CUTS6[:4], ["Cabal Ritual", "Culling the Weak", "Jet Medallion",
                     "Crypt Ghast"]),
    "b4-tutor3 (+Grim Tutor +Wishclaw +Final Parting; no new combos)":
        (CUTS6[:3], ["Grim Tutor", "Wishclaw Talisman", "Final Parting"]),
    "b4-full10 (combo6 + Wishclaw + SanguineBond + CabalRit + Culling)":
        (CUTS10, ["Leonin Relic-Warder", "Vito, Thorn of the Dusk Rose",
                  "Exquisite Blood", "Grave Titan", "Nim Deathmantle",
                  "Grim Tutor", "Wishclaw Talisman", "Sanguine Bond",
                  "Cabal Ritual", "Culling the Weak"]),
    # GC slot reallocation: defensive GCs out, tutor GCs in (still 3/3 with
    # Teferi's Protection). Demonic x3 / Vampiric x1 owned but ALL deployed.
    "b4-gcswap (full10, also -SmotheringTithe -Farewell +Demonic +Vampiric)":
        (CUTS10 + ["Smothering Tithe", "Farewell"],
         ["Leonin Relic-Warder", "Vito, Thorn of the Dusk Rose",
          "Exquisite Blood", "Grave Titan", "Nim Deathmantle",
          "Grim Tutor", "Wishclaw Talisman", "Sanguine Bond",
          "Cabal Ritual", "Culling the Weak",
          "Demonic Tutor", "Vampiric Tutor"]),
}


def _run(library, index, trials, label):
    rng = random.Random(SEED)
    res = [goldfish_kill(library, rng, index) for _ in range(trials)]
    print(slc.row(label + "  decap", slc.cum(res, 0, SHOW), SHOW, width=70))
    print(slc.row(label + "  table", slc.cum(res, 1, SHOW), SHOW, width=70))
    print(f"    median decap {slc.median(res, 0)} / table {slc.median(res, 1)}"
          f" · never-in-{TURNS}: "
          f"{100.0 * sum(1 for _, x in res if x is None) / trials:.0f}% (table)")
    return res


def mode_clock(index, aliases, trials):
    print(f"\n### CLOCK — Diminishing Returns kill-turn goldfish   trials={trials} seed={SEED}")
    print("    Combat focus-fire drives decap; the drain engine is the table clock.")
    print("    Claimed in Summary (unverified): Goldfish T7-9.\n")
    library, commander = slc.load_parsed(DECK, index, aliases)
    print("  P(kill <= turn T) %".ljust(76) + "".join(f"{t:>6}" for t in SHOW))
    _run(library, index, trials, "")


def mode_b4(index, aliases, trials):
    print(f"\n### B4 — bracket-4-in-spirit packages   trials={trials} seed={SEED}")
    print("    Compact 2-card kills + tutors + fast-mana control axis.")
    print("    GC slots untouched (3/3); all adds GC-screened clean.\n")
    base, commander = slc.load_parsed(DECK, index, aliases)
    print("  P(kill <= turn T) %".ljust(76) + "".join(f"{t:>6}" for t in SHOW))
    for label, (rm, add) in VARIANTS_B4.items():
        lib = slc.build_lib(base, index, rm, add)
        _run(lib, index, trials, label[:62])
        print()


def mode_levers(index, aliases, trials):
    print(f"\n### LEVERS — axis swaps, 2-card packages   trials={trials} seed={SEED}")
    print("    Tutor axis limited to non-GC tutors (Demonic/Vampiric blocked: 3/3).\n")
    base, commander = slc.load_parsed(DECK, index, aliases)
    print("  P(kill <= turn T) %".ljust(76) + "".join(f"{t:>6}" for t in SHOW))
    for label, (rm, add) in VARIANTS.items():
        lib = slc.build_lib(base, index, rm, add)
        _run(lib, index, trials, label[:62])
        print()


if __name__ == "__main__":
    slc.run_cli(__doc__, {"clock": mode_clock, "levers": mode_levers,
                          "b4": mode_b4},
                default_trials=20000)
