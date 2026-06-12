#!/usr/bin/env python3
"""kfx_clock_lab.py — Kefka, Court Mage (EXTERNAL $100 combo-control) KILL-TURN goldfish.

Stage 3 of the 2026-06-12 candidate bake-off. Deck:
decks/considering/kefka-external-20260612.txt (extracted verbatim from
proposals/Kefka_External_Build.md). Built on speed_lab_core.py. Same
commander as the internal burn build (kfk_clock_lab.py) — same-commander
head-to-head is a bake-off highlight.

THE KILL IS AN INFINITE COMBO (kill_all, decap = table). The three lines,
oracle-verified 2026-06-12 (all mechanically sound per Stage 0):

  A. DUALCASTER TOKENS — cast Twinflame {1}{R} (any creature you control as
     target -> needs >=1 body) or Electroduplicate {2}{R}, hold priority,
     flash Dualcaster Mage {1}{R}{R}: ETB copies the sorcery targeting DCM
     -> each token's ETB recopies -> infinite hasty 2/2s, swing out. 5-6
     mana, both pieces in hand, >=1 other creature.
  B. GHOSTLY FLICKER MANA — DCM + Ghostly Flicker (+ a land): each iteration
     re-ETBs the land untapped -> net +1 mana -> infinite mana + infinite
     DCM ETBs; with KEFKA on bf the flicker loop also strips hands / draws
     your library, then line A fires from hand (Twinflame/Electroduplicate
     must not BOTH be dead — singletons never die in this goldfish). 6 mana.
  C. RIONYA COMBATS — Rionya, Fire Dancer (5) + Combat Celebrant (3) or Fear
     of Missing Out (2, needs DELIRIUM — 4+ card types in yard, tracked) on
     the battlefield at your combat: Rionya copies the exerter with haste,
     each extra combat retriggers her -> infinite combats. Summoning
     sickness irrelevant (the copies have haste).

TUTORS (modelled at real costs/restrictions): Wishclaw Talisman (cast 2 +
{1},tap same turn = 3+1, ANY card), Splinter's Technique (4, any), Ringsight
(3, needs Kefka or another legendary on bf — colour-share approximated as
satisfied then), Demonic Counsel (2, ANY only with delirium), Shred Memory
transmute (3, MV2 exactly: Twinflame / FOMO / Harmonic Prodigy), Step
Through wizardcycle (2, a WIZARD: DCM or Rionya), Lively Dirge (5: tutor any
card to YARD + return DCM (MV3<=4) to the battlefield — modelled for DCM),
Lim-Dûl's Vault (2, to top -> next draw).

MANA: lands + rocks + BANKED one-shot mana (the deck's actual ramp texture):
Dark Ritual +2, Rite of Flame +1, Simian Spirit Guide +1 (from hand),
sac-bodies Basal Thrull / Blood Pet / Reckless Barbarian / Goldhound banked
at their net, Generator Servant net 0 but banked 2, Pentad Prism stores 2.
Banked mana pops only to complete a combo cast (wb-lab ritual convention).
Kefka cast at 5 when spare — his ETB/attack draw (+3/+2 modelled) is the
deck's velocity; opponents' discards ignored (no damage relevance).

OMITTED (conservative): Gogo as a second Celebrant-class piece, Harmonic
Prodigy doubling, Mayhem Devil post-combat burn, FOMO-without-delirium
half-combats, counterspell protection, Curse of Opulence gold, Azra
Oddsmaker draw. OPTIMISTIC: colour-blind mana, banked mana never wasted,
pieces never interacted with. Trust shapes and deltas.

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

DECK = ROOT / "decks" / "considering" / "kefka-external-20260612.txt"
SEED = 20260612
TURNS = 12
SHOW = [3, 4, 5, 6, 7, 8, 9, 10, 12]

ROCKS = {"Sol Ring": (1, 2), "Arcane Signet": (2, 1), "Fellwar Stone": (2, 1),
         "Talisman of Creativity": (2, 1), "Talisman of Dominance": (2, 1),
         "Talisman of Indulgence": (2, 1), "Springleaf Drum": (1, 0)}
BANKED = {"Dark Ritual": (1, 3), "Rite of Flame": (1, 2),
          "Simian Spirit Guide": (0, 1), "Basal Thrull": (2, 2),
          "Blood Pet": (1, 1), "Reckless Barbarian": (2, 2),
          "Goldhound": (1, 1), "Generator Servant": (2, 2),
          "Pentad Prism": (2, 2), "Strike It Rich": (1, 1)}
BODIES = {"Skirk Prospector": 1, "Goblin Chirurgeon": 1, "Hope of Ghirapur": 1,
          "Fugitive Droid": 1, "Phyrexian Revoker": 2, "Harmonic Prodigy": 2,
          "Siren Stormtamer": 1, "Nightscape Familiar": 2,
          "Malevolent Hermit": 2, "Hydroelectric Specimen": 3,
          "Mayhem Devil": 3, "Azra Oddsmaker": 3, "Gogo, Mysterious Mime": 4}


class Trial:
    def __init__(self, library, rng):
        self.g = slc.Goldfish(library, rng, rocks=ROCKS)
        self.tbl = slc.Table()
        self.bf = set()
        self.kefka = False
        self.bodies = 0            # creatures on bf (combo A needs >=1)
        self.bank = []             # one-shot mana (cost already paid)
        self.yard_types = set()
        self.pending_top = []

    # ---- mana ----------------------------------------------------------------
    def burst(self):
        return self.g.avail + sum(v for v in self.bank)

    def spend(self, n):
        while self.g.avail < n and self.bank:
            self.g.avail += self.bank.pop()
        self.g.avail -= n

    def delirium(self):
        return len(self.yard_types) >= 4

    def bin_card(self, rec):
        tl = rec["type_line"].lower()
        for t in ("creature", "instant", "sorcery", "artifact", "enchantment",
                  "land", "planeswalker"):
            if t in tl:
                self.yard_types.add(t)

    # ---- kill lines ------------------------------------------------------------
    def kill_check(self, T):
        g = self.g
        dcm_h = g.has("Dualcaster Mage")
        dcm_bf = "Dualcaster Mage" in self.bf
        # A: copy-spell + DCM from hand
        if dcm_h and self.bodies >= 1:
            if g.has("Twinflame") and self.burst() >= 5:
                self.spend(5); self.tbl.kill_all(T); return True
            if g.has("Electroduplicate") and self.burst() >= 6:
                self.spend(6); self.tbl.kill_all(T); return True
        # A': DCM already on bf (via Lively Dirge) — copy spell targets him
        if dcm_bf:
            if g.has("Twinflame") and self.burst() >= 2 and self.bodies >= 1:
                # need a second DCM ETB: Twinflame token of DCM copies nothing —
                # actual line: cast copy spell targeting DCM, flicker? Not
                # available. Honest: require Ghostly Flicker OR treat the
                # Twinflame token's ETB as a fresh DCM copying Twinflame —
                # rules-correct ONLY while Twinflame is still on the stack via
                # a second cast; NOT modelled. Fall through to B.
                pass
            if g.has("Ghostly Flicker") and self.kefka and self.burst() >= 3 \
                    and (g.has("Twinflame") or g.has("Electroduplicate")
                         or self._in_lib("Twinflame")
                         or self._in_lib("Electroduplicate")):
                self.spend(3); self.tbl.kill_all(T); return True
        # B: GF loop from hand
        if dcm_h and g.has("Ghostly Flicker") and self.kefka \
                and self.burst() >= 6 \
                and (g.has("Twinflame") or g.has("Electroduplicate")
                     or self._in_lib("Twinflame")
                     or self._in_lib("Electroduplicate")):
            self.spend(6); self.tbl.kill_all(T); return True
        # C: Rionya + exerter on bf at combat
        rionya = "Rionya, Fire Dancer" in self.bf
        exerter = "Combat Celebrant" in self.bf or (
            "Fear of Missing Out" in self.bf and self.delirium())
        if rionya and exerter:
            self.tbl.kill_all(T); return True
        return False

    def _in_lib(self, nm):
        g = self.g
        return any(g.deck[i][0] == nm for i in range(g.ptr, len(g.deck)))

    # ---- one turn ----------------------------------------------------------------
    def turn(self, T):
        g = self.g
        g.begin_turn(T)
        for nm in self.pending_top:
            g.fetch(nm)
        self.pending_top = []
        g.deploy_rocks()
        # bank one-shot mana sources from hand
        for nm, (cost, out) in BANKED.items():
            while g.has(nm) and (g.avail >= cost or cost == 0):
                if cost and not g.pay(cost):
                    break
                g.hand.pop(g.in_hand(nm))
                self.bank.append(out)
                if nm in ("Basal Thrull", "Blood Pet", "Reckless Barbarian",
                          "Goldhound", "Generator Servant"):
                    pass                      # they sac away — no lasting body

        if self.kill_check(T):
            return

        progress = True
        while progress:
            progress = False
            # combo permanents that want to PRE-DEPLOY: Rionya + exerters
            for nm, c in (("Combat Celebrant", 3), ("Rionya, Fire Dancer", 5),
                          ("Fear of Missing Out", 2)):
                if nm not in self.bf and g.has(nm) and g.avail >= c:
                    g.cast(nm, c)
                    self.bf.add(nm)
                    self.bodies += 1
                    progress = True
            # Kefka for velocity
            if not self.kefka and g.avail >= 5:
                g.avail -= 5
                self.kefka = True
                self.bodies += 1
                g.draw(3)
                progress = True
            # cheap bodies (combo A target + Kefka triggers)
            for nm, c in sorted(BODIES.items(), key=lambda x: x[1]):
                if nm not in self.bf and g.has(nm) and g.avail >= c:
                    g.cast(nm, c)
                    self.bf.add(nm)
                    self.bodies += 1
                    progress = True
                    break
            # tutors toward the closest missing piece
            tgt = self.missing_target()
            if tgt:
                if self.try_tutor(tgt):
                    progress = True
            if self.kill_check(T):
                return
        # Kefka attack draw
        if self.kefka:
            g.draw(2)
            self.tbl.hit_focus(4, T)

    def missing_target(self):
        g = self.g
        have_dcm = g.has("Dualcaster Mage") or "Dualcaster Mage" in self.bf
        have_copy = g.has("Twinflame") or g.has("Electroduplicate")
        if have_dcm and not have_copy:
            return "Twinflame"
        if not have_dcm and have_copy:
            return "Dualcaster Mage"
        if "Rionya, Fire Dancer" in self.bf \
                and not ("Combat Celebrant" in self.bf or g.has("Combat Celebrant")):
            return "Combat Celebrant"
        if not have_dcm:
            return "Dualcaster Mage"
        return None

    def try_tutor(self, tgt):
        g = self.g
        if not self._in_lib(tgt):
            return False
        opts = []
        if g.has("Wishclaw Talisman"):
            opts.append(("Wishclaw Talisman", 4))
        if g.has("Splinter's Technique"):
            opts.append(("Splinter's Technique", 4))
        if g.has("Ringsight") and self.kefka:
            opts.append(("Ringsight", 3))
        if g.has("Demonic Counsel") and self.delirium():
            opts.append(("Demonic Counsel", 2))
        if g.has("Shred Memory") and tgt in ("Twinflame", "Fear of Missing Out",
                                             "Harmonic Prodigy"):
            opts.append(("Shred Memory", 3))
        if g.has("Step Through") and tgt in ("Dualcaster Mage",
                                             "Rionya, Fire Dancer"):
            opts.append(("Step Through", 2))
        if g.has("Lim-Dûl's Vault"):
            opts.append(("Lim-Dûl's Vault", 2))
        if g.has("Lively Dirge") and tgt == "Dualcaster Mage":
            opts.append(("Lively Dirge", 5))
        for nm, cost in sorted(opts, key=lambda o: o[1]):
            if self.burst() >= cost:
                self.spend(cost)
                g.hand.pop(g.in_hand(nm))
                if nm == "Lim-Dûl's Vault":
                    self.pending_top.append(tgt)
                elif nm == "Lively Dirge":
                    g.fetch(tgt)
                    g.hand.pop(g.in_hand(tgt))
                    self.bf.add(tgt)
                    self.bodies += 1
                else:
                    g.fetch(tgt)
                self.yard_types.add("sorcery" if nm != "Lim-Dûl's Vault"
                                    else "instant")
                return True
        return False


def goldfish(library, trials, rng):
    out = []
    for _ in range(trials):
        tr = Trial(library, rng)
        for T in range(1, TURNS + 1):
            tr.turn(T)
            if tr.tbl.done:
                break
        out.append((tr.tbl.decap, tr.tbl.table))
    return out


def mode_clock(index, aliases, trials):
    print("=" * 72)
    print(f"CLOCK — Kefka (external combo-control) kill-turn goldfish "
          f"({trials} trials, seed {SEED})")
    print("=" * 72)
    rng = random.Random(SEED)
    library, commander = slc.load_parsed(DECK, index, aliases)
    print(f"  library {len(library)} + commander {commander}")
    print("  turns:".ljust(44) + "".join(f"{t:6d}" for t in SHOW))
    res = goldfish(library, trials, rng)
    print(slc.row("kill (decap = table, cum %)", slc.cum(res, 1, SHOW), SHOW))
    nv = 100.0 * sum(1 for _, t in res if t is None) / trials
    print(f"\n  median kill {slc.median(res, 1)}   ·   never-in-{TURNS}: {nv:.0f}%")
    print("\n  Primer self-declares 'NOT a turbo list... looks for a longer game'.")


if __name__ == "__main__":
    slc.run_cli(__doc__, {"clock": mode_clock})
