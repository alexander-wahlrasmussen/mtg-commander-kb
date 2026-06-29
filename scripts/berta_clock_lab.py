#!/usr/bin/env python3
"""berta_clock_lab.py — Berta, Wise Extrapolator (GU) candidate KILL-TURN goldfish.

Lab run requested 2026-06-13 (after the Loam teardown / RS upgrade round). Berta is
an UN-BUILT candidate (proposals/PROP_Berta_Wise_Extrapolator.md); the list labbed
here is a GC-verified modelling build at decks/considering/berta-wise-extrapolator-
20260613.txt (3 GCs: Seedborn Muse, Survival of the Fittest, Mana Vault — the
proposal's "non-GC" Cyclonic Rift/Mystical Tutor/Worldly Tutor are ALL GCs and were
cut). Built on speed_lab_core.py; structure follows knn_clock_lab.py (Berta's combo
substrate is a subset of Kinnan's). Kill shape: closed-loop combo -> Walking Ballista
pings ALL opponents, so decap = table by construction (kill_all).

KILL LINES (oracle-verified; PROP log 2026-06-01 + knn lab 2026-06-12):
  A. INFINITE MANA -> BALLISTA (fast, deterministic, pod-approved 2-card):
     - Bloom Tender + (Freed from the Real | Pemmin's Aura): tap GU=2, untap {U} ->
       net coloured, infinite.
     - OR Selvala, Heart of the Wilds + (Umbral Mantle | Staff of Domination) with a
       >=4-power creature on board: tap X, untap {3}, net positive + grows.
     Outlet (infinite coloured mana finds/fires Ballista): Walking Ballista in
     hand/bf, OR Finale of Devastation / Green Sun's Zenith (X=huge -> Ballista to bf),
     OR Hydroid Krasis (cast huge -> draw deck -> Ballista). kill_all.
  B. SIMIC ASCENDANCY (slower alt-win): Berta + Simic Ascendancy + >=1 counter doubler
     on bf -> ~3 qualifying spell casts to 20 growth (2 turns with >=2 doublers). Modelled
     as kill_all at assembly_turn + (2 if >=2 doublers else 3).

MANA: lands + rocks + dorks floor, + ~1/turn while Berta is on bf (her cast-refund,
modelled conservatively at +1, not per-spell). Bloom Tender taps for 2 (GU). OMITTED
(conservative): Sapphire Medallion cost-reduction, Mana Reflection doubling, the
combat/Aetherflux/storm backups, Defense of the Heart (dead in a goldfish — needs an
opponent with 3+ creatures). OPTIMISTIC (documented, knn/wb convention): rocks repeat
(Mana Vault untap tax ignored), mana colour-blind, auras never fizzle. Trust shapes.

RE-LAB 2026-06-14 (user asked "what would it take for Berta to compete," shared 3
external lists): the 06-13 modelling build OMITTED the engine those lists are built
on. This run is an A/B of that build vs a real-engine build (decks/considering/
berta-wise-extrapolator-20260614.txt, same legal 3-GC frame, -4 weak combat/value
cards +4 engine pieces). Three lines added to the model:
  C. BERTA + INTRUDER ALARM + any unsick mana dork = INFINITE MANA (commander-central):
     Berta {0},{T} makes a 0/0 Fractal -> Fractal ETB -> Intruder Alarm untaps ALL
     creatures (Berta + dork) -> re-tap dork for net >=1 mana, re-tap Berta, loop.
     Outlet as in A. This is the line the 06-13 build couldn't make (no Alarm) -> the
     lab never tested Berta's OWN best combo. Intruder Alarm is a 3rd untap enabler
     (Freed/Pemmin's/Alarm) and pairs with ANY of ~6 dorks, not a specific one.
  D. KAMI OF WHISPERED HOPES — a 6th dork (taps for its power; modelled flat at 1,
     conservative) + counter doubler (not credited to Ascendancy here, conservative).
  E. LYLA + PENSIVE PROFESSOR — controllable ~infinite draw loop (Pensive: counters->
     draw; Lyla: draw->counter; point them at each other). Modelled as a one-time
     dig of 10 + ongoing +1 draw/turn when BOTH are on bf. NOT tutored for (both are
     creatures, so Survival/GSZ COULD assemble it — omitted = conservative). This is
     how a tutor-poor GU deck reaches its un-tutorable enchantment halves: draw to them.
Win-line attribution added so we can see WHICH line carries the new build.

Data: collection/oracle-cards.json   ·   Proposal: proposals/PROP_Berta_Wise_Extrapolator.md
"""
import importlib.util
import random
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).parent.parent
_spec = importlib.util.spec_from_file_location(
    "speed_lab_core", Path(__file__).parent / "speed_lab_core.py")
slc = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(slc)
ds = slc.ds

DECK_OLD = ROOT / "decks" / "considering" / "berta-wise-extrapolator-20260613.txt"
DECK_NEW = ROOT / "decks" / "considering" / "berta-wise-extrapolator-20260614.txt"
DECKS = [("06-13 (pre-engine)", DECK_OLD), ("06-14 (real engine)", DECK_NEW)]
SEED = 20260613
TURNS = 12
SHOW = [3, 4, 5, 6, 7, 8, 9, 10, 12]
COMMANDER = "Berta, Wise Extrapolator"

ROCKS = {"Sol Ring": (1, 2), "Mana Vault": (1, 3), "Arcane Signet": (2, 1)}
DORK_OUT = {"Birds of Paradise": 1, "Llanowar Elves": 1, "Elvish Mystic": 1,
            "Joraga Treespeaker": 1, "Incubation Druid": 1, "Bloom Tender": 2,
            "Kami of Whispered Hopes": 1}
DORK_COST = {"Birds of Paradise": 1, "Llanowar Elves": 1, "Elvish Mystic": 1,
             "Joraga Treespeaker": 1, "Incubation Druid": 2, "Bloom Tender": 2,
             "Kami of Whispered Hopes": 3,
             "Selvala, Heart of the Wilds": 3, "Marwyn, the Nurturer": 2}
RAMP = {"Three Visits": (2, 1), "Farseek": (2, 1), "Sakura-Tribe Elder": (2, 1),
        "Cultivate": (3, 1), "Kodama's Reach": (3, 1), "Skyshroud Claim": (4, 2)}
AURAS = {"Freed from the Real": 3, "Pemmin's Aura": 3}
UNTAPPERS = {"Umbral Mantle": 3, "Staff of Domination": 3}
DOUBLERS = {"Hardened Scales", "Branching Evolution", "Doubling Season",
            "Vorinclex, Monstrous Raider"}
OUTLETS = {"Walking Ballista", "Finale of Devastation", "Green Sun's Zenith",
           "Hydroid Krasis"}
# creature combo pieces / payoffs to deploy from hand (name -> cost)
PIECES = {"Bloom Tender": 2, "Selvala, Heart of the Wilds": 3, "Simic Ascendancy": 2,
          "Kalonian Hydra": 5, "Craterhoof Behemoth": 8, "Walking Ballista": 2,
          "Hardened Scales": 1, "Branching Evolution": 3, "Doubling Season": 5,
          "Vorinclex, Monstrous Raider": 6, "Forgotten Ancient": 4,
          "Champion of Lambholt": 3, "Avenger of Zendikar": 7,
          "Intruder Alarm": 3, "Lyla, Holographic Assistant": 4,
          "Pensive Professor": 3}
CREATURE_TUTORS = {"Survival of the Fittest": 1, "Green Sun's Zenith": 4,
                   "Finale of Devastation": 4, "Eldritch Evolution": 3}


class Trial:
    def __init__(self, library, rng, powmap):
        self.g = slc.Goldfish(library, rng, rocks=ROCKS)
        self.tbl = slc.Table()
        self.powmap = powmap
        self.bf = set()
        self.unsick = set()     # permanents on board since before this turn (no summoning
        #                         sickness): the only ones that may TAP for a combo this turn
        self.berta = False
        self.dork_out = 0
        self.dork_new = 0
        self.maxpow = 0
        self.simic_turn = None
        self.draw_rate = 0      # Tatyova / Garruk's Uprising landfall/ETB draw
        self.digs = set()       # one-shot X-draw spells already fired
        self.dig_fired = False  # Lyla + Pensive controllable infinite-draw loop
        self.line = None        # which kill line fired (attribution)

    def pw(self, nm):
        return self.powmap.get(nm.lower(), 0) or 0

    def outlet(self):
        g = self.g
        return any(o in self.bf or g.has(o) for o in OUTLETS) \
            or "Survival of the Fittest" in self.bf

    def infinite(self, T):
        g = self.g
        got = False
        line = None
        # Every line below taps a creature ({T}/{Q} mana ability) — Bloom Tender's
        # Vivid, Selvala's {G}{T}, Berta's {X}{T}. None has haste, so the creature
        # must have entered on a PRIOR turn (be in self.unsick). The aura/untapper
        # half CAN be cast this turn (enchantments/equipment have no sickness). Gating
        # on self.bf let a dork combo the turn it entered (2026-06-29 audit).
        if "Bloom Tender" in self.unsick:
            for a, c in AURAS.items():
                if a in self.bf or (g.has(a) and g.avail >= c and g.cast(a, c)):
                    self.bf.add(a); got = True; line = "Tender+aura"; break
        if not got and "Selvala, Heart of the Wilds" in self.unsick and self.maxpow >= 4:
            for u, c in UNTAPPERS.items():
                if u in self.bf or (g.has(u) and g.avail >= c and g.cast(u, c)):
                    self.bf.add(u); got = True; line = "Selvala+untap"; break
        # Berta + Intruder Alarm + any unsick dork = infinite mana (commander-central).
        # Berta herself taps to make the Fractal, so she must be unsick too; the dork is
        # gated by dork_out (this-turn dorks live in dork_new, not dork_out).
        if not got and COMMANDER in self.unsick and "Intruder Alarm" in self.bf \
                and self.dork_out >= 1:
            got = True; line = "Berta+Alarm"
        if got and self.outlet():
            self.line = line
            self.tbl.kill_all(T)
            return True
        return False

    def ndoublers(self):
        return len(self.bf & DOUBLERS)

    def tutor_target(self):
        """Creature half of whichever combo line we've drawn the (un-tutorable)
        enabler for; else default to Bloom Tender (most flexible)."""
        g = self.g
        have_aura = any(a in self.bf or g.has(a) for a in AURAS)
        have_untap = any(u in self.bf or g.has(u) for u in UNTAPPERS)
        absent = lambda nm: nm not in self.bf and not g.has(nm)
        if have_aura and absent("Bloom Tender"):
            return "Bloom Tender"
        if have_untap:
            if absent("Selvala, Heart of the Wilds"):
                return "Selvala, Heart of the Wilds"
            if self.maxpow < 4 and absent("Kalonian Hydra"):
                return "Kalonian Hydra"
        ready = (("Bloom Tender" in self.bf and have_aura)
                 or ("Selvala, Heart of the Wilds" in self.bf
                     and self.maxpow >= 4 and have_untap)
                 or (self.berta and "Intruder Alarm" in self.bf and self.dork_out >= 1))
        if ready and not self.outlet():
            return "Walking Ballista"
        # assemble the Lyla+Pensive dig engine if we hold exactly one half (both are
        # creatures -> Survival/GSZ/Finale/Eldritch fetch them) and no line is closer
        dig = ["Pensive Professor", "Lyla, Holographic Assistant"]
        present = [d for d in dig if d in self.bf or g.has(d)]
        if not self.dig_fired and len(present) == 1 and not have_aura and not have_untap:
            other = dig[1] if present[0] == dig[0] else dig[0]
            if absent(other):
                return other
        if absent("Bloom Tender"):
            return "Bloom Tender"
        return None

    def turn(self, T):
        g = self.g
        # Snapshot the board BEFORE anything is cast this turn: these permanents have
        # been under control since before the turn began, so they alone may tap for a
        # combo (no summoning sickness). Anything deployed below is sick until next turn.
        self.unsick = set(self.bf)
        self.dork_out += self.dork_new
        self.dork_new = 0
        g.begin_turn(T)
        g.draw(self.draw_rate)
        g.deploy_rocks()
        g.add_mana(self.dork_out)
        if self.berta:
            g.add_mana(1)                       # Berta cast-refund (conservative)

        # ramp spells (grow the land count)
        for rs, (cost, n) in RAMP.items():
            while g.has(rs) and g.avail >= cost:
                g.cast(rs, cost); g.lands += n; g.add_mana(n)

        # commander: Berta {2}{G}{U} = 4 (GU permanent + refund engine)
        if not self.berta and g.avail >= 4:
            g.avail -= 4; self.berta = True
            self.bf.add(COMMANDER); self.maxpow = max(self.maxpow, 1)

        if self.infinite(T):
            return

        progress = True
        while progress:
            progress = False
            # dorks
            for nm, c in DORK_COST.items():
                if nm not in self.bf and g.has(nm) and g.avail >= c:
                    g.cast(nm, c); self.bf.add(nm)
                    self.dork_new += DORK_OUT.get(nm, 0)
                    self.maxpow = max(self.maxpow, self.pw(nm))
                    progress = True; break
            # combo pieces / doublers / payoffs cheapest-first
            cands = sorted(((c, nm) for nm, c in PIECES.items()
                            if nm not in self.bf and g.has(nm) and g.avail >= c),
                           key=lambda x: x[0])
            for c, nm in cands:
                cost = 2 if nm == "Walking Ballista" else c   # X=1, survives
                if g.avail >= cost:
                    g.cast(nm, cost); self.bf.add(nm)
                    self.maxpow = max(self.maxpow, self.pw(nm))
                    progress = True; break
            # card-draw engines + one-shot X-draw digs (find the un-tutorable halves)
            for nm, c in (("Tatyova, Benthic Druid", 5), ("Garruk's Uprising", 4)):
                if nm not in self.bf and g.has(nm) and g.avail >= c:
                    g.cast(nm, c); self.bf.add(nm); self.draw_rate += 1
                    self.maxpow = max(self.maxpow, self.pw(nm))
                    progress = True; break
            for nm in ("Pull from Tomorrow", "Stroke of Genius"):
                if nm not in self.digs and g.has(nm) and g.avail >= 6:
                    g.cast(nm, 5); g.draw(3); self.digs.add(nm)
                    progress = True; break
            # Lyla + Pensive Professor: controllable ~infinite draw -> dig to enablers
            if (not self.dig_fired and "Lyla, Holographic Assistant" in self.bf
                    and "Pensive Professor" in self.bf):
                g.draw(10); self.draw_rate += 1; self.dig_fired = True
                progress = True
            # tutor the creature half of whichever line is closest to online
            tgt = self.tutor_target()
            if tgt:
                for tut, c in CREATURE_TUTORS.items():
                    if g.has(tut) and g.avail >= c and g.fetch(tgt):
                        g.cast(tut, c)
                        if tut != "Survival of the Fittest":   # GSZ/Finale/Eldritch -> bf
                            g.hand.pop(g.in_hand(tgt))
                            self.bf.add(tgt)
                            self.maxpow = max(self.maxpow, self.pw(tgt))
                            if tgt == "Bloom Tender":
                                self.dork_new += 2
                        progress = True; break
            if self.infinite(T):
                return

        # Simic Ascendancy alt-win bookkeeping
        if (self.berta and "Simic Ascendancy" in self.bf and self.ndoublers() >= 1
                and self.simic_turn is None):
            self.simic_turn = T
        if self.simic_turn is not None:
            lag = 2 if self.ndoublers() >= 2 else 3
            if T >= self.simic_turn + lag:
                if self.line is None:
                    self.line = "Ascendancy"
                self.tbl.kill_all(T)


def goldfish(library, trials, rng, powmap):
    out, lines = [], []
    for _ in range(trials):
        tr = Trial(library, rng, powmap)
        for T in range(1, TURNS + 1):
            tr.turn(T)
            if tr.tbl.done:
                break
        out.append((tr.tbl.decap, tr.tbl.table))
        if tr.tbl.table is not None:
            lines.append(tr.line or "?")
    return out, lines


def mode_clock(index, aliases, trials):
    print("=" * 72)
    print(f"CLOCK A/B — Berta, Wise Extrapolator candidate kill-turn goldfish "
          f"({trials} trials, seed {SEED})")
    print("=" * 72)
    print("  06-13 (pre-engine, the labbed build) vs 06-14 (+Intruder Alarm combo /"
          " Kami / Lyla+Pensive dig)")
    print("  kill (decap = table, cum %)")
    print("  turns:".ljust(44) + "".join(f"{t:6d}" for t in SHOW))
    for label, deckpath in DECKS:
        rng = random.Random(SEED)
        library, commander = slc.load_parsed(deckpath, index, aliases)
        names = [nm for nm, _ in library] + [commander]
        raw = slc.load_powers(names)
        powmap = {k: (v if isinstance(v, int) else 0) for k, v in raw.items()}
        res, lines = goldfish(library, trials, rng, powmap)
        print(slc.row(label, slc.cum(res, 1, SHOW), SHOW))
        nv = 100.0 * sum(1 for _, t in res if t is None) / trials
        dist = ", ".join(f"{k} {100.0 * v / max(1, len(lines)):.0f}%"
                         for k, v in Counter(lines).most_common())
        print(f"      median {slc.median(res, 1)} · never-{TURNS} {nv:.0f}%"
              f" · of the wins: {dist or '(none)'}")
    print("\n  PROP claim: 'T3 god-hand, T4-5 consistency, T6 worst case; ahead of the"
          " pod's T6-7'.\n  06-13 is the falsification; 06-14 re-tests with the real"
          " engine. Pod bar: decap T<=7.")


if __name__ == "__main__":
    slc.run_cli(__doc__, {"clock": mode_clock})
