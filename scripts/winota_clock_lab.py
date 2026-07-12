#!/usr/bin/env python3
"""winota_clock_lab.py — Winota, Joiner of Forces KILL-TURN goldfish.

THE KILL (one engine, snowballing):
  Winota, Joiner of Forces (card_lookup verified 2026-06-18):
    "Whenever a NON-HUMAN creature you control attacks, look at the top six cards
     of your library. You may put a HUMAN creature card from among them onto the
     battlefield tapped and attacking. It gains indestructible until end of turn."
  So the clock = (# non-human attackers each combat) Winota triggers -> each digs 6
  and (with prob p_hit, set by Human density in library) floods a Human in ATTACKING.
  Floods add power THIS turn and bodies for next turn => the board compounds.

  Payoff multipliers encoded (all card_lookup verified 2026-06-18):
    * Erkenbrand, Lord of Westfold — "Whenever a Human you control enters, creatures
      you control get +1/+0 until EOT." Each Human that enters (flooded OR hardcast)
      pumps the WHOLE attacking team. The snowball term.
    * Adeline, Resplendent Cathar — power = creatures you control; on attack makes a
      1/1 Human attacking each opponent (extra bodies + extra Human-ETB events).
    * God-Eternal Oketra — each creature SPELL you cast makes a 4/4 non-human Zombie
      (a future Winota trigger). Hardcast only (flooded tokens aren't cast).
    * Siege-Gang (3 Goblins ETB) / Spawn-Gang (3 Eldrazi Spawn, 0-power but still
      attack => still trigger) / Blade Splicer (3/3 Golem) — non-human body banks.

  Damage is focus-fire (combat): decap leads, table follows as the wide board spills.

OPTIMISTIC (shared goldfish priors + this deck's):
  * Unblocked damage, no removal/wraths/interaction (the standard lab caveat). For a
    go-wide attacker that walks into blockers + sweepers, this is a real ceiling — the
    decap/table turns here are the BEST case, not the median pod outcome.
  * Erkenbrand pump assumes every attacker connects; flooded Human power fixed at 2
    (most Humans are p1-3). p_hit uses a running Human/library density estimate.
  * Mana = lands + rocks + Myr-dork floor (rock activation costs ignored, as every lab).
  * Haste (Goldspan/Ragavan/Hanweir Battlements/Rising of the Day) ignored => the few
    same-turn attacks are NOT counted (conservative on speed).
OMITTED: Monastery Mentor / Mirrex / Kavaron Harrier token trickles; Théoden /
  Lossarnach / Beregond / Odric / Iroas / Pianna / Flowering combat buffs; Mangara
  draw (so the real board is a touch stronger than modelled — the headline number is
  if anything conservative on payoff, optimistic on durability).
2026-07-12 list (-20260712): the 6 Mass-Production/Skullclamp-contended slots swapped
  for free-pool cards (Scurry/Kavaron/Pianna/Flowering/Mirrex/Mangara). Scurry's ETB
  gremlins modelled via ENCH_TOKEN_ETB; the rest land in the OMITTED bucket above.

Data: collection/oracle-cards.json (refresh via update_scryfall_data.py)
Run:  python scripts/winota_clock_lab.py --trials 40000
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
DECK = ROOT / "decks" / "considering" / "winota-joiner-of-forces-20260712.txt"
SEED = 20260618
TURNS = 14
SHOW = [4, 5, 6, 7, 8, 9, 10, 12]

WINOTA = "Winota, Joiner of Forces"
# artifact rocks: name -> (cost, net mana output) — the lands+rocks floor
ROCKS = {"Sol Ring": (1, 2), "Boros Signet": (2, 1), "Arcane Signet": (2, 1),
         "Talisman of Conviction": (2, 1), "Mind Stone": (2, 1)}
# Myr/Construct mana dorks: also NON-HUMAN creatures (so future Winota triggers)
DORKS = {"Plague Myr": 1, "Palladium Myr": 2, "Hedron Crawler": 1}
# non-human bodies created on cast/ETB: name -> (count, power) [become attackers next turn]
TOKEN_ETB = {"Siege-Gang Commander": (3, 1), "Spawn-Gang Commander": (3, 0),
             "Blade Splicer": (1, 3), "Angel of Invention": (2, 1)}
# noncreature spells that ETB non-human bodies (cast loop below is creatures-only):
#   Scurry of Gremlins — "When this enchantment enters, create two 1/1 red Gremlin
#   creature tokens." (card_lookup verified 2026-07-12; energy haste-pump NOT modelled)
ENCH_TOKEN_ETB = {"Scurry of Gremlins": (2, 1)}
OKETRA = "God-Eternal Oketra"            # +1 non-human 4/4 per creature cast
ERKENBRAND = "Erkenbrand, Lord of Westfold"   # +1/+0 team per Human ETB
ADELINE = "Adeline, Resplendent Cathar"
FLOOD_POW = 2                             # avg power of a flooded Human


def is_creature(rec): return "Creature" in rec.get("type_line", "")
def is_human(rec):
    tl = rec.get("type_line", "")
    return "Creature" in tl and "—" in tl and "Human" in tl.split("—")[1]
def power_of(rec):
    p = rec.get("power")
    try:
        return int(p)
    except (TypeError, ValueError):
        return max(1, int(rec.get("cmc", 2) or 2) - 1)   # '*'/None fallback


class Trial:
    def __init__(self, library, rng, haste=False):
        self.g = slc.Goldfish(library, rng, rocks=ROCKS)
        self.rng = rng
        self.haste = haste     # True = upper bound: this-turn creatures can attack
        self.tbl = slc.Table()
        self.board = []            # [(power, human)] — can attack (not sick)
        self.pending = []          # [(power, human)] — deployed this turn (sick)
        self.dork_out = 0
        self.winota = False
        self.oketra = False
        self.erkenbrand = False
        self.adeline = False
        self.humans_left = sum(1 for _, r in library if is_human(r))

    def _lib_left(self):
        return max(8, len(self.g.deck) - self.g.ptr)

    def _p_hit(self):
        frac = min(0.9, self.humans_left / self._lib_left())
        return 1.0 - (1.0 - frac) ** 6

    def turn(self, T):
        g = self.g
        # unsick last turn's deployments
        self.board += self.pending
        self.pending = []
        g.begin_turn(T)
        g.deploy_rocks()
        g.add_mana(self.dork_out)          # persistent dork mana floor

        # --- deploy the commander from the command zone, with priority ---------
        #   Winota is the COMMANDER (deck_sim loads only the 99-card library, so
        #   she is NEVER in g.hand — the old `nm == WINOTA` in-hand branch was dead
        #   code and self.winota stayed False, clocking the deck WITHOUT its engine).
        #   {2}{R}{W} = MV4, 4/4 Human Warrior (card_lookup verified 2026-06-18).
        #   No haste: she's summoning-sick the turn she lands (added to pending),
        #   but her trigger is a static "whenever a non-Human attacks" — so it works
        #   the turn she enters as long as other non-Humans are already attacking.
        if not self.winota and g.pay(4):
            self.winota = True
            self.pending.append((4, True))   # 4/4 Human body, sick this turn
            # NB: do NOT decrement humans_left — she's the commander, never in the
            # library, so she's not part of the flood pool _p_hit() draws from.

        # --- deploy creatures, cheapest first (maximise body/trigger count) ---
        #     (+ the token-ETB enchantments — bodies are bodies)
        while True:
            cands = sorted(
                ((i, nm, r) for i, (nm, r) in enumerate(g.hand)
                 if (is_creature(r) or nm in ENCH_TOKEN_ETB)
                 and (r.get("cmc", 0) or 0) <= g.avail),
                key=lambda x: x[2].get("cmc", 0) or 0)
            if not cands:
                break
            i, nm, r = cands[0]
            g.cast(nm)                      # pays cmc from avail
            if nm in ENCH_TOKEN_ETB:
                cnt, pw = ENCH_TOKEN_ETB[nm]
                self.pending += [(pw, False)] * cnt
                continue                    # enchantment: tokens only, no body/Human ETB
            if nm in DORKS:
                self.dork_out += DORKS[nm]
                g.add_mana(DORKS[nm])       # taps same turn
            hp = is_human(r)
            self.pending.append((power_of(r), hp))
            if hp:
                self.humans_left = max(0, self.humans_left - 1)
            if nm in TOKEN_ETB:
                cnt, pw = TOKEN_ETB[nm]
                self.pending += [(pw, False)] * cnt
            if self.oketra:
                self.pending.append((4, False))   # 4/4 zombie per creature cast
            if nm == OKETRA:
                self.oketra = True
            if nm == ERKENBRAND:
                self.erkenbrand = True
            if nm == ADELINE:
                self.adeline = True

        # --- combat ----------------------------------------------------------
        if self.haste:                      # upper bound: everything swings turn-of
            self.board += self.pending
            self.pending = []
        attackers = list(self.board)        # non-sick only
        if not attackers and not self.adeline:
            return
        nh = sum(1 for _, h in attackers if not h)
        base = sum(p for p, _ in attackers)
        humans_entered = 0
        flood_bodies = []

        # Adeline: power = creature count; +1 Human token attacking each opp (3)
        if self.adeline:
            ccount = len(self.board) + len(self.pending)
            base += ccount                  # her own */4 body swinging
            for _ in range(3):
                flood_bodies.append((1, True)); humans_entered += 1
            base += 3

        # Winota triggers: one dig per NON-HUMAN attacker
        if self.winota:
            ph = self._p_hit()
            for _ in range(nh):
                if self.humans_left <= 0:
                    break
                if self.rng.random() < ph:
                    base += FLOOD_POW
                    flood_bodies.append((FLOOD_POW, True))
                    humans_entered += 1
                    self.humans_left -= 1

        # Erkenbrand: +1/+0 to the whole attacking team per Human that entered
        if self.erkenbrand and humans_entered:
            n_attackers = len(attackers) + len(flood_bodies)
            base += n_attackers * humans_entered

        if base > 0:
            self.tbl.hit_focus(base, T)
        # flooded/Adeline bodies stick around for next turn
        self.board += flood_bodies


def _run(index, aliases, trials, haste, label):
    print(f"\n### CLOCK ({label}) — Winota kill-turn goldfish   trials={trials} seed={SEED}")
    rng = random.Random(SEED)
    library, commander = slc.load_parsed(DECK, index, aliases)
    print(f"  library {len(library)} + commander {commander}")
    res = slc.run_goldfish(lambda: Trial(library, rng, haste=haste), trials, TURNS)
    slc.report_clock(res, SHOW, TURNS, trials)


def mode_clock(index, aliases, trials):
    # no-haste = conservative floor; haste = upper bound (the truth brackets between).
    _run(index, aliases, trials, haste=False, label="floor / no-haste")
    _run(index, aliases, trials, haste=True, label="ceiling / all-haste")
    print("\n  decap vs table stated separately (verification rule). Truth brackets between.")


if __name__ == "__main__":
    slc.run_cli(__doc__, {"clock": mode_clock}, default_trials=40000)
