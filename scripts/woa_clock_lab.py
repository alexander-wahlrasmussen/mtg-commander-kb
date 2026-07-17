#!/usr/bin/env python3
"""woa_clock_lab.py — "War of Attrition" (Yahenni) kill-turn goldfish.

KILL SHAPE (confirmed 2026-07-17 via find_combos.py + card_lookup.py):
  This is a mono-black ARISTOCRATS/ATTRITION deck with two real kill axes and an
  optional bought combo. It is NOT a fast combo deck as built (free-pool only).

  1. VOLTRON — Yahenni, Undying Partisan {2}{B} 2/2 haste. "Whenever a creature an
     OPPONENT controls dies, put a +1/+1 counter on Yahenni." Lethal COMMANDER
     DAMAGE = 21 (NOT 40) — the threshold that actually kills first for a single
     source. Yahenni grows off OPPONENTS' creatures dying to our removal/edicts
     (Grave Pact, Dictate, Fleshbag/Merciless/Accursed/Gaius edicts, Toxic Deluge,
     Living Death…), plus equipment (Shadowspear +1/+1, Champion's Helm +2/+2, Nim
     Deathmantle +2/+2). [card_lookup on each]
  2. DRAIN — aristocrats chip: Al Bhed Salvagers / Marionette Apprentice / Nadier's
     Nightblade / Mirkwood Bats / Dreadhound / Sephiroth + Kokusho/Gray Merchant.
     Modelled only as a modest background hit_all once a drain is online.
  3. COMBO (ONLY in the +Ashnod variant) — Ashnod's Altar {3} "Sacrifice a creature:
     Add {C}{C}" + Nim Deathmantle {3} + Dread Drone {4} (ETB two 0/1 Eldrazi Spawn)
     = mana-positive infinite death loop; any drain in play → infinite lifeloss =
     table kill. All pieces except Ashnod's Altar (~EUR5 buy) are already in the free
     list. [card_lookup verified the loop is mana-positive]

MODES / options to compare:
  base    — owned free build, no buy (combo axis inert; Ashnod's not in list)
  ashnod  — build_lib(base) - 1 Swamp + Ashnod's Altar (unlocks the combo)
  combo   — combo-piece AVAILABILITY curve for the ashnod list (independent of voltron)
  sweep   — voltron counter-accrual SENSITIVITY (the dominant assumption) at 1.0/1.5/2.0

BIG OPTIMISM (state it, per the verification rule):
  * goldfish: combat is unblocked and Yahenni is assumed to connect (evasion via
    Rogue's Passage/Shizo/Shadowspear-trample abstracted away).
  * the COUNTER-ACCRUAL RATE is an assumption about the OPPONENTS' board — how many
    of their creatures our removal kills per turn. It is the single biggest lever;
    that is why `sweep` exists. Default 1.5/turn once Yahenni is down.
  * combo pieces are treated as castable the turn all are drawn + mana floor met;
    per-piece sequencing and commander tax on recast are omitted.
OMITTED: opponent interaction / removal on Yahenni, blocks, the drain axis as a full
  model (only a flat chip). So the VOLTRON clock is a ceiling; the real grind is slower
  and pod-dependent. decap and table are different clocks; both are reported.

Data: collection/oracle-cards.json (refresh via update_scryfall_data.py)
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
DECK = ROOT / "decks" / "considering" / "war-of-attrition-owned-20260717.txt"
SEED = 20260717
TURNS = 16
SHOW = [5, 6, 7, 8, 9, 10, 12, 14, 16]
ROCKS = {"Sol Ring": (1, 2), "Arcane Signet": (2, 1), "Mind Stone": (2, 1),
         "Fellwar Stone": (2, 1), "Coldsteel Heart": (2, 1)}

CMD_LETHAL = 21          # commander damage, not 40
DRAIN_CHIP = 2           # per-turn aristocrats background once a drain is online
EQUIP_CAP = 4            # cumulative +power from drawn/attached equipment

COMBO = ["Ashnod's Altar", "Nim Deathmantle", "Dread Drone"]
DRAINS = {"Al Bhed Salvagers", "Marionette Apprentice", "Nadier's Nightblade",
          "Mirkwood Bats", "Dreadhound", "Sephiroth, Fabled SOLDIER // Sephiroth, One-Winged Angel",
          "Kokusho, the Evening Star", "Gray Merchant of Asphodel"}
EQUIP = {"Shadowspear": 1, "Champion's Helm": 2, "Nim Deathmantle": 2,
         "Mask of Griselbrand": 1}


class VDTable:
    """3 opponents. Each has life (40) AND commander-damage-from-Yahenni (cdmg).
    A player dies at life<=0 OR cdmg>=21 — the commander-damage threshold the
    stock Table lacks. Focus-fire voltron leads; drains hit all; combo = kill_all."""

    def __init__(self, n=3, life=40):
        self.life = [life] * n
        self.cdmg = [0] * n
        self.decap = None
        self.table = None

    def _alive(self, i):
        return self.life[i] > 0 and self.cdmg[i] < CMD_LETHAL

    def _update(self, T):
        dead = sum(1 for i in range(len(self.life)) if not self._alive(i))
        if dead >= 1 and self.decap is None:
            self.decap = T
        if dead == len(self.life) and self.table is None:
            self.table = T

    def voltron(self, power, T):
        for i in range(len(self.life)):        # focus the lowest living opponent
            if self._alive(i):
                self.life[i] -= power
                self.cdmg[i] += power
                break
        self._update(T)

    def drain(self, x, T):
        for i in range(len(self.life)):
            if self._alive(i):
                self.life[i] -= x
        self._update(T)

    def kill_all(self, T):
        self.life = [0] * len(self.life)
        self._update(T)

    @property
    def done(self):
        return self.table is not None


class Trial:
    def __init__(self, library, rng, rate=1.5):
        self.g = slc.Goldfish(library, rng, rocks=ROCKS)
        self.tbl = VDTable()
        self.rate = rate
        self.yahenni = False
        self.since = None
        self.counters = 0.0
        self.seen = set()
        self.board = set()

    def _refresh_seen(self):
        self.seen |= {nm for nm, _ in self.g.hand}

    def _equip_bonus(self):
        return min(EQUIP_CAP, sum(EQUIP[n] for n in self.board if n in EQUIP))

    def _combo_ready(self):
        if not all(p in self.seen for p in COMBO):
            # one tutor (Increasing Ambition) can fetch a single missing piece
            missing = [p for p in COMBO if p not in self.seen]
            if not (len(missing) == 1 and "Increasing Ambition" in self.seen):
                return False
        return bool(self.seen & DRAINS) and self.g.avail >= 4

    def turn(self, T):
        g = self.g
        g.begin_turn(T)
        g.deploy_rocks()
        self._refresh_seen()

        # commander from the command zone (indestructible -> assume it sticks)
        if not self.yahenni and g.pay(3):
            self.yahenni, self.since = True, T

        # attach the cheap equipment we've drawn (cumulative power, capped)
        for nm in EQUIP:
            if nm not in self.board and g.has(nm) and g.avail >= 3:
                g.cast(nm, 3); self.board.add(nm)

        # COMBO (ashnod variant only — pieces just aren't in the base library)
        if self._combo_ready():
            self.tbl.kill_all(T); return

        # VOLTRON: 21 commander damage, growth = assumed opponent-deaths/turn + equip
        if self.yahenni:
            self.counters += self.rate
            power = 2 + self.counters + self._equip_bonus()
            self.tbl.voltron(power, T)

        # DRAIN: flat aristocrats chip once any drain is online
        if self.seen & DRAINS and self.yahenni:
            self.tbl.drain(DRAIN_CHIP, T)


CMDR = "Yahenni, Undying Partisan"


def load_base(index, aliases):
    """Base library WITHOUT the commander. parse_deck can't ID the commander of a
    non-registry candidate, so it leaves Yahenni in the 99 — strip it, since the
    model casts Yahenni from the command zone."""
    lib, _ = slc.load_parsed(DECK, index, aliases)
    return [t for t in lib if t[0] != CMDR]


def _run(library, rng, trials, rate=1.5):
    return slc.run_goldfish(lambda: Trial(library, rng, rate), trials, TURNS)


def mode_base(index, aliases, trials):
    print(f"\n### CLOCK — base free build (NO buy)   trials={trials} seed={SEED}")
    lib = load_base(index, aliases)
    print(f"  library {len(lib)} + Yahenni (command zone)   ·   counter-rate 1.5/turn")
    slc.report_clock(_run(lib, random.Random(SEED), trials), SHOW, TURNS, trials)


def mode_ashnod(index, aliases, trials):
    print(f"\n### CLOCK — +Ashnod's Altar (-1 Swamp, ~EUR5)   trials={trials} seed={SEED}")
    lib = slc.build_lib(load_base(index, aliases), index,
                        removes=["Swamp"], adds=["Ashnod's Altar"])
    print(f"  library {len(lib)} + Yahenni (command zone)   ·   combo axis LIVE")
    slc.report_clock(_run(lib, random.Random(SEED), trials), SHOW, TURNS, trials)


def mode_combo(index, aliases, trials):
    print(f"\n### COMBO AVAILABILITY — Ashnod line (independent of voltron)   trials={trials}")
    lib = slc.build_lib(load_base(index, aliases), index,
                        removes=["Swamp"], adds=["Ashnod's Altar"])
    groups = [["Ashnod's Altar"], ["Nim Deathmantle"], ["Dread Drone"], sorted(DRAINS)]
    drawn, with_t = slc.simulate_groups(lib, groups, ["Increasing Ambition"],
                                        trials, random.Random(SEED), TURNS)
    print(slc.row("all pieces drawn (cum %)", {t: drawn[t] for t in SHOW}, SHOW))
    print(slc.row("+ Increasing Ambition tutor (cum %)", {t: with_t[t] for t in SHOW}, SHOW))


def mode_sweep(index, aliases, trials):
    print(f"\n### SWEEP — voltron counter-accrual sensitivity (base build)   trials={trials}")
    lib = load_base(index, aliases)
    print(slc.row("rate", {t: t for t in SHOW}, SHOW).replace("  rate", "  (decap cum %)  rate"))
    for rate in (1.0, 1.5, 2.0):
        res = _run(lib, random.Random(SEED), trials, rate)
        print(slc.row(f"{rate:.1f} counters/turn", slc.cum(res, 0, SHOW), SHOW))


if __name__ == "__main__":
    slc.run_cli(__doc__, {"base": mode_base, "ashnod": mode_ashnod,
                          "combo": mode_combo, "sweep": mode_sweep},
                default_trials=40000)
