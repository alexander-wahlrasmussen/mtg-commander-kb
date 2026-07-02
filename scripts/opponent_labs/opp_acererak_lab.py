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
    slc.run_cli(__doc__, {"clock": mode_clock, "levers": mode_levers})
