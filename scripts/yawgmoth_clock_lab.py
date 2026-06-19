#!/usr/bin/env python3
"""yawgmoth_clock_lab.py — Yawgmoth aristocrats KILL-TURN goldfish (combo-assembly clock).

THE KILL is a board-independent, own-turn, Abolisher-proof INFINITE DRAIN (decap == table).
Two house-legal (3+ card) lines, all pieces card_lookup-verified 2026-06-19:

  LINE A — Yawgmoth + Mikaeus + a drain (the engine):
    * Yawgmoth, Thran Physician: "Pay 1 life, Sacrifice another creature: put a -1/-1 counter
      on up to one target creature and draw a card." (free sac + card engine + counter reset)
    * Mikaeus, the Unhallowed: grants UNDYING to your non-Human creatures (mono-B has almost no
      printed undying — Mikaeus SUPPLIES it; this is what makes Yawgmoth's combo exist here).
    * Drain: Zulaport Cutthroat ("...another creature you control dies, each opponent loses 1")
      or Syr Konrad. Loop: sac body A (Yawg), put -1/-1 on body B; A undies (+1/+1); sac B,
      -1/-1 cancels A's +1/+1; repeat -> infinite deaths -> each opp loses infinite. Needs 2
      expendable non-Human bodies (deck floods them: Bitterblossom / Dreadhorde / Gisa / Endrek
      / Reassembling Skeleton / token banks) — assumed present once the 3 namepieces are.
  LINE B — Gravecrawler + Phyrexian Altar + a Zombie source + a drain:
    * Gravecrawler recast from yard (needs a Zombie) ; Phyrexian Altar "Sacrifice a creature:
      add one mana" pays for the recast -> infinite cast/die -> drain. (Mana-neutral loop.)

  Tutors can fetch the missing piece (Demonic Tutor, Grim Tutor, Diabolic Intent, Sidisi exploit,
  Razaketh). Yawgmoth is the COMMANDER — always available from the command zone at 4 mana, so
  Line A is only ever 2 cards short, not 3. That command-zone availability is the whole thesis
  vs Diminishing Returns (which had to DRAW both a sac outlet and a payoff).

OPTIMISTIC (shared goldfish priors): no interaction/wraths; mana is a lands+rocks floor;
  draw-engine acceleration modelled as a flat +1/turn per engine (Necropotence/Bolas's Citadel
  actually dig far harder). CONSERVATIVE / OMITTED: Cabal Coffers + Urborg big-mana NOT modelled
  (understates mana => understates speed); the Gray Merchant / Kokusho incremental-drain GRIND
  floor is NOT modelled (this lab measures the COMBO clock only, like the other combo labs);
  tutors fetch to hand (cast next turn unless mana spare). Trust shapes, not second decimals.
  decap == table by construction (infinite hit-all) so a single clock is reported.

Data: collection/oracle-cards.json (refresh via update_scryfall_data.py)
Run:  python scripts/yawgmoth_clock_lab.py --trials 40000
"""
import importlib.util
import random
from pathlib import Path

ROOT = Path(__file__).parent.parent
_spec = importlib.util.spec_from_file_location(
    "speed_lab_core", Path(__file__).parent / "speed_lab_core.py")
slc = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(slc)
ds = slc.ds

DECK = ROOT / "decks" / "considering" / "yawgmoth-liquidation-20260619.txt"
SEED = 20260619
TURNS = 14
SHOW = [4, 5, 6, 7, 8, 9, 10, 12]

COMMANDER = "Yawgmoth, Thran Physician"
ROCKS = {"Sol Ring": (1, 2), "Mind Stone": (2, 1), "Arcane Signet": (2, 1),
         "Fellwar Stone": (2, 1), "Bontu's Monument": (3, 1)}
DRAIN = {"Zulaport Cutthroat", "Syr Konrad, the Grim"}
ZOMBIE_SRC = {"Cryptbreaker", "Ghoulcaller Gisa", "Dreadhorde Invasion", "Carrier Thrall"}
TUTORS = {"Demonic Tutor", "Grim Tutor", "Diabolic Intent", "Sidisi, Undead Vizier",
          "Razaketh, the Foulblooded"}
DRAW_ENGINES = {"Necropotence", "Bolas's Citadel", "Phyrexian Arena", "Skullclamp",
                "Black Market Connections", "Vilis, Broker of Blood", "Midnight Reaper"}
# pieces the assembly cares about, with the line they serve
LINE_A = ["Mikaeus, the Unhallowed"]          # + commander Yawgmoth + any DRAIN
LINE_B = ["Gravecrawler", "Phyrexian Altar"]  # + any ZOMBIE_SRC + any DRAIN


STRONG = {"Necropotence", "Bolas's Citadel"}   # dig far harder than a cantrip


class Trial:
    def __init__(self, library, rng, dig=4):
        self.g = slc.Goldfish(library, rng, rocks=ROCKS)
        self.rng = rng
        self.dig = dig             # extra cards/turn per STRONG engine (Necro/Bolas)
        self.tbl = slc.Table()
        self.inplay = set()
        self.yawg = False          # commander resolved (recastable from command zone)
        self.draw_weight = 0       # accumulated per-turn bonus draws

    def _has_any(self, names):
        return any(n in self.inplay for n in names)

    def _combo_ready(self):
        a = self.yawg and ("Mikaeus, the Unhallowed" in self.inplay) and self._has_any(DRAIN)
        b = ("Gravecrawler" in self.inplay and "Phyrexian Altar" in self.inplay
             and self._has_any(ZOMBIE_SRC) and self._has_any(DRAIN))
        return a or b

    def _missing(self):
        # highest-value single piece to tutor for, given current board
        if self.yawg and self._has_any(DRAIN) and "Mikaeus, the Unhallowed" not in self.inplay:
            return "Mikaeus, the Unhallowed"
        if self.yawg and "Mikaeus, the Unhallowed" in self.inplay and not self._has_any(DRAIN):
            return "Zulaport Cutthroat"
        if not self.yawg and "Mikaeus, the Unhallowed" in self.inplay and self._has_any(DRAIN):
            return None        # just need to cast commander (mana), no tutor
        return "Mikaeus, the Unhallowed"

    def turn(self, T):
        g = self.g
        g.begin_turn(T)
        g.deploy_rocks()
        # Dark Ritual burst if held
        if g.has("Dark Ritual") and g.cast("Dark Ritual", 1):
            g.add_mana(3)
        # draw-engine acceleration (Necro/Bolas dig hard; cantrip-engines +1)
        g.draw(min(self.draw_weight, 8))

        progressed = True
        while progressed:
            progressed = False
            # 1) cast commander Yawgmoth from command zone (always available)
            if not self.yawg and g.avail >= 4:
                g.pay(4); self.yawg = True; progressed = True; continue
            # 2) cast any key/engine piece in hand we can afford (cheapest first)
            castable = sorted(
                ((i, nm, r) for i, (nm, r) in enumerate(g.hand)
                 if nm not in ROCKS and (r.get("cmc", 0) or 0) <= g.avail),
                key=lambda x: x[2].get("cmc", 0) or 0)
            for i, nm, r in castable:
                want = (nm in DRAIN or nm in ZOMBIE_SRC or nm in DRAW_ENGINES
                        or nm in LINE_A or nm in LINE_B or nm in TUTORS)
                if not want:
                    continue
                if not g.cast(nm):
                    continue
                if nm in DRAW_ENGINES:
                    self.draw_weight += self.dig if nm in STRONG else 1
                if nm in TUTORS:                 # fetch the missing piece to hand
                    miss = self._missing()
                    if miss:
                        g.fetch(miss)
                else:
                    self.inplay.add(nm)
                progressed = True
                break

        if self._combo_ready():
            self.tbl.kill_all(T)


def _run(index, aliases, trials, dig, label):
    print(f"\n### CLOCK ({label}) — Yawgmoth combo-assembly   trials={trials} seed={SEED}")
    rng = random.Random(SEED)
    library, commander = slc.load_parsed(DECK, index, aliases)
    print(f"  library {len(library)} + commander {commander}")
    res = slc.run_goldfish(lambda: Trial(library, rng, dig=dig), trials, TURNS)
    slc.report_clock(res, SHOW, TURNS, trials, single=True)   # infinite hit-all: decap == table


def mode_clock(index, aliases, trials):
    # floor = Necro/Bolas modelled as a cantrip (+1); realistic = they dig (+4). Coffers omitted
    # in BOTH (so both understate mana) and the Gray Merchant/Kokusho grind floor is unmodelled.
    _run(index, aliases, trials, dig=1, label="floor / engines as cantrips")
    _run(index, aliases, trials, dig=4, label="realistic / Necro+Bolas dig")
    print("\n  decap == table (infinite hit-all). Truth >= these (Coffers + grind plan omitted).")


if __name__ == "__main__":
    slc.run_cli(__doc__, {"clock": mode_clock}, default_trials=40000)
