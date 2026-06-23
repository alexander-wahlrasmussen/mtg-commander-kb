#!/usr/bin/env python3
"""pod_gauntlet.py — turn Pod_Matchup_Matrix.md from hand-judged into a
WIN-PROBABILITY per deck vs the recurring archenemy.

Backlog #1 (Backlog.md). The matrix says things like "Favoured — disruption-led,
not a race." This tool puts a number on it: P(we beat the pod combo opponent),
by RACING two already-measured quantities against the opponent profile —

  CLOCK       each deck's decap-clock distribution (the *_clock_lab.py suite).
              decap = the turn we can kill ONE opponent = the turn we can
              NEUTRALISE the combo player we are focusing.
  DISRUPTION  each deck's answer availability on the opponent's combo turn,
              GIVEN their Grand Abolisher (delay_lab.py). Abolisher zeroes
              REACTIVE answers on their turn, so only proactive hate (statics,
              own-turn removal, edicts) survives — exactly delay_lab's model.

THE OPPONENT (project_pod_combo_opponent + the matrix): Ur-Dragon ramp shell +
Hidetsugu/Kairi/Kenrith/Kinnan combo decks. Wins T6-7, typically behind Grand
Abolisher. We model their first combo-attempt turn K as a distribution (K_DIST)
and let them RETRY each later turn (disrupted attempts buy us a turn).

THE RACE (Monte Carlo, per deck):
  sample K  (their first combo turn) and  T_kill  (our decap turn, from the CDF)
  we are EARLIER in turn order, so our turn t precedes their turn t.
    * if T_kill <= K           -> WIN  (threat removed before their first attempt)
    * else each turn t = K,K+1,...: our turn t kills them if T_kill == t (WIN);
      otherwise they attempt on their turn t and WIN-FOR-THEM with prob 1-D
      (disrupted with prob D -> game continues). Undecided at the horizon = loss
      (they eventually combo through).

TWO NUMBERS, stated separately (same discipline as every lab — trust shapes and
the ranking, not the second decimal):
  PURE RACE   P(we decap the combo player at/before turn K), disruption IGNORED.
              Fully data-backed for all 16 decks (clock curves are simulated).
  P(WIN)      the race WITH the disruption overlay. Disruption is MEASURED
              (delay_lab) for the three decks delay_lab covers (Grand Design,
              Calamity Tax, Lightning War) and CLASS-BUCKETED from the matrix's
              "Through Abolisher?" column for the other 13. The bucket is the
              soft input; it is swept on P(Abolisher out) and exposed as a knob.

CAVEATS (load-bearing):
  * Clock curves are UNBLOCKED goldfish ceilings (no opposing interaction, no
    blockers). Real decap is slower — so PURE RACE is an optimistic front edge,
    not a promise. The pod's Ur-Dragon shell presents exactly the blockers the
    goldfish assumes away; read the numbers as "can this deck plausibly contest
    the race," not "wins this often."
  * decap (one opponent) is the headline; the game is not won until the TABLE
    is dead. A --strict run uses the table clock instead (much slower) — the
    "did we actually close" view. Most anti-pod value is removing the archenemy,
    so decap is the default.
  * Disruption AVAILABILITY != EFFECTIVENESS (delay_lab's caveat): a live answer
    doesn't model their second protection piece or a backup line.
  * This is a heuristic race model, not a rules engine.

Clock data: harvested 2026-06-14 from the *_clock_lab.py suite @8k trials (see
CLOCKS[].src per deck; Calamity is multi-variant so its slow curve is taken from
the 06-13 sweep median). Refresh with `--refresh` (re-runs the labs, reparses).
Disruption: delay_lab.py 2026-06-14 (MEASURED) + matrix classes (BUCKET).
Writeup: campaigns/Pod_Gauntlet_2026-06-14.md
"""
import argparse
import json
import random
import re
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).parent.parent

# Per-deck display name + clock-lab pointer are OWNED by deck_registry (the single source of
# truth). The CLOCKS harvest entries below mirror them and are guarded against drift at load;
# the curves themselves (grid/decap/table/med/never) are this file's own lab snapshot.
import importlib.util as _il
_rspec = _il.spec_from_file_location("deck_registry", Path(__file__).parent / "deck_registry.py")
deck_registry = _il.module_from_spec(_rspec)
_rspec.loader.exec_module(deck_registry)

for _s in (sys.stdout, sys.stderr):            # output uses →, Δ, §, 🔒, en-dashes
    if hasattr(_s, "reconfigure"):
        try:
            _s.reconfigure(encoding="utf-8", errors="replace")
        except (ValueError, OSError):
            pass

# --- opponent model --------------------------------------------------------
# Their first combo-attempt turn. Profile: "wins T6-7" with a god-draw tail at
# T5 and a slow tail past T7. Mean ~6.65. Tune with --pod-fast / --pod-slow.
K_DIST = {5: 0.10, 6: 0.35, 7: 0.35, 8: 0.15, 9: 0.05}
HORIZON = 16
A_BASE = 0.30                                  # baseline P(Abolisher out on the key turn)
A_SWEEP = [0.0, 0.15, 0.30, 0.50, 0.75]        # realistic band ~0.15-0.30 (delay_lab)

# --- the TWO REAL decks (2026-06-15) ---------------------------------------
# Split the generic single-opponent model above into his ACTUAL commanders
# (project_pod_combo_opponent, card text verified this session). run() keeps the
# generic model as the default; --vs races these instead.
#
# KEY MECHANICAL FACTS (verified oracle text), and why they change the race:
#  * Acererak the Archlich is mono-B and Hidetsugu and Kairi is UB -> NEITHER can run the
#    WHITE Grand Abolisher the matrix's whole disruption model is built around. So our
#    reactive answers are NOT dead-on-arrival vs his two current decks: vs Acererak (no
#    counters at all) almost all of them live; vs H&K they fight a UB counter wall 1-for-1.
#    Only the 5C tail (Ur-Dragon / Kenrith) can actually field Grand Abolisher.
#  * Their loops fire off DIFFERENT triggers: Acererak = ETB (recast -> venture),
#    H&K = a DEATH trigger (drain). No single static hoses both -> see LOCK_VS_LOOP.
#  * His kill is a damage/drain LOOP, not a Thassa's Oracle deckout -> lifegain is a trap,
#    Thoracle/tutor hate (Mindcensor) is low value. (Informs the catalog below, not the race.)
#
# disruption_a = the `a` we feed disruption() = fraction of our REACTIVE answers stopped on
# their key turn (Abolisher for the tail; a counter wall for H&K; ~nothing for Acererak).
# answer = P(THEY stop OUR kill on the stack) = their reactive instant interaction, color-keyed
# (Abolisher acts only on THEIR turn, so it does NOT answer our kill — counters/removal do).
# weight = how often he brings the deck (PRIOR: favorite + recent flood; --vs prints them; tune).
OPPONENTS = {
    "acererak": dict(
        name="Acererak (mono-B ETB)", ci="B", loop="etb", weight=0.45,
        disruption_a=0.05, answer=0.10,
        note="favorite; no Abolisher/counters -> our reactive answers live; ETB recast loop"),
    "hidetsugu_kairi": dict(
        name="Hidetsugu&Kairi (UB death)", ci="UB", loop="death", weight=0.40,
        disruption_a=0.30, answer=0.30,
        note="recent flood; UB counter wall (still no white Abolisher); death-trigger drain"),
    "five_color_tail": dict(
        name="5C tail (UrDrgn/Kenrith)", ci="WUBRG", loop="mixed", weight=0.15,
        disruption_a=0.45, answer=0.30,
        note="legacy profile; the ONLY shells that can run the white Grand Abolisher"),
}
ANSWER_DECAY = 0.5     # interaction is finite: each answer they spend halves the next P(answer)

# P(this deck FORCES ITS KILL THROUGH the opponent's reactive answer) on its kill turn — its own
# counter package winning the counter-war, PLUS a counter-immune kill (uncounterable finisher OR a
# board-state/combat win counterspells can't touch). The "protect-own" axis
# (feedback_interaction_role_protect_vs_disrupt): a deck's counters protect ITS kill, which the flat
# `answer` term ignores — so counter-heavy / board-kill decks read worse vs H&K than they play.
# Set roster-wide 2026-06-15 from a grep-VERIFIED counter count (Path/Swords are removal=disruption,
# not protect) + a judgment bump for counter-immune kills. PRIOR; tune freely. answer_eff *= (1-p).
PROTECT = {
    "lightning_war":       0.65,  # 8 counters (3 free) + Banefire X>=5 UNCOUNTERABLE finisher
    "radiation_sickness":  0.55,  # 5 counters + kills are BOARD-STATES (Simic Asc/Toxrill/rad) = counter-immune
    "replication_crisis":  0.55,  # 7 counters + combat/Kiki BOARD kill (counters don't stop it)
    "grand_design":        0.40,  # 5 counters (FoW free) + Glen Elendra recursion; Grand Abolisher CUT 2026-06-23; Finale/Craterhoof IS counterable
    "dark_lords_army":     0.45,  # 7 counters (reactive grind shell)
    "curse_of_the_scarab": 0.40,  # 5 counters + zombie-army board kill
    "calamity_tax":        0.35,  # 5 counters + Veil; X-drain kill is a counterable spell
    "crystal_sickness":    0.30,  # 4 counters
    "earthbend_the_meta":  0.30,  # 3 counters incl. REB/Pyroblast (anti-blue: extra bite vs H&K)
    "exiles_return":       0.30,  # 1 counter + its OWN Grand Abolisher (protect-own) + Kiki/combat kill
    "zero_sum_game":       0.30,  # board-independent, Abolisher-proof lifeloop kill + Veil
    "bumbleflower":        0.15,  # 1 counter, combat-steal kill
    "eldrazi_stampede":    0.10,  # combat kill (counter-immune) but no counters
    "diminishing_returns": 0.10,  # death-combo, no counters
    "genome_project":      0.05,  # BR burn/storm: kill is counterable spells, ~no counters
    # lorehold_spirits omitted = 0.0 (no counters; RW combat/spirits)
    # --- pending build candidates (priors; --pending) ---
    "kefka":               0.45,  # triggered-damage wheel kill (counter-immune, anti-Abolisher) + Grixis counters
    "hashaton":            0.40,  # instant Thoracle combo protected by counters, but glass (one fragile line)
}

# Which static actually stops which loop. STRUCTURE (which loop a piece hits) is VERIFIED from
# oracle text this session; magnitudes are judgment priors (e = P(stops the combo | the piece
# is live and the loop is the one named)). The headline is the ZEROES, not the decimals:
# ETB-hate hard-locks Acererak and is a stone blank on H&K's death trigger.
LOCK_VS_LOOP = {
    "Torpor Orb":          dict(etb=0.95, death=0.00, mixed=0.30),
    "Hushwing Gryff":      dict(etb=0.95, death=0.00, mixed=0.30),
    "Rule of Law":         dict(etb=0.70, death=0.70, mixed=0.60),
    "Drannith Magistrate": dict(etb=0.35, death=0.35, mixed=0.45),  # command-zone recast only
    "Cursed Totem":        dict(etb=0.05, death=0.15, mixed=0.20),  # activated abilities only
    "Aven Mindcensor":     dict(etb=0.10, death=0.10, mixed=0.40),  # tutor hate ~ irrelevant here
    "Elesh Norn, Mother of Machines": dict(etb=0.95, death=0.00, mixed=0.30),  # opp ETBs don't trigger
}

# Persistent opponent-combo locks each deck actually RUNS (verified from the list). These STOP
# the pod's combo on THEIR turn every turn until removed — NOT protect-own (Grand Abolisher /
# Teferi shield OUR turn and are excluded here and in lock_lab). Used by --vs-lock to overlay a
# loop-typed persistent lock on the two-deck race: e per opponent = LOCK_VS_LOOP[piece][opp loop],
# availability measured in-shell by lock_lab.
VS_LOCKS = {
    "grand_design": ["Elesh Norn, Mother of Machines"],   # ETB-lock: hard vs Acererak, inert vs H&K
}

# --- disruption: measured (delay_lab, drawn, composed P(disrupt their key turn))
# a-grid the measured arrays are sampled on. T6 / T7 rows; we pick by combo turn.
A_GRID = [0.0, 0.25, 0.50, 0.75, 1.0]
MEASURED = {
    "grand_design":  {6: [67, 55, 42, 30, 17], 7: [70, 58, 45, 33, 21]},
    "calamity_tax":  {6: [52, 41, 30, 19,  8], 7: [56, 45, 33, 21, 10]},
    "lightning_war": {6: [77, 63, 50, 37, 23], 7: [80, 67, 53, 40, 27]},
}
# 2026-06-15: overlay delay_lab-MEASURED disruption for ALL 16 decks (limitation #2 closed).
# delay_lab.py --emit-json writes analysis/delay_disruption.json from per-deck answer suites;
# we read it here so the 13 formerly class-bucketed decks are now measured too. The 3 baked
# rows above are the seed/fallback (the JSON reproduces them exactly). JSON keys are strings.
DJSON = ROOT / "analysis" / "delay_disruption.json"
if DJSON.exists():
    try:
        for _slug, _rows in json.loads(DJSON.read_text(encoding="utf-8")).items():
            MEASURED[_slug] = {int(_k): _v for _k, _v in _rows.items()}
    except (ValueError, OSError):
        pass
# class buckets — now only a FALLBACK for slugs absent from the JSON (e.g. the Kefka build
# clock). (D at a=0 "no Abolisher, reactive answers live", D at a=1 "Abolisher out, proactive
# only"). "warn"/"none" = the matrix "Through Abolisher?" mark read strictly as "can disrupt
# THEIR combo turn" (own-Abolisher / board-independent kill protect OUR clock, not disruption).
BUCKET = {"warn": (0.50, 0.14), "none": (0.20, 0.02)}

# --- clock data: cum P(decap <= turn T) and P(table <= T) over each lab's grid.
# Harvested 2026-06-14. grid/decap/table are %; medians/never echo the lab.
CLOCKS = {
    "genome_project": dict(
        name="The Genome Project", score="15", disrupt_class="warn",
        lab=("gp_clock_lab", "clock"), sel=("decap", "table"),
        grid=[4, 5, 6, 7, 8, 9, 10, 12],
        decap=[1, 8, 42, 82, 95, 98, 99, 99], table=[0, 2, 17, 49, 78, 92, 97, 99],
        med=("T7", "T8"), never=(0, 1), src="lab gp_clock_lab @8k"),
    "radiation_sickness": dict(
        name="Radiation Sickness", score="18", disrupt_class="warn",
        lab=("rs_clock_lab", "clock"), sel=("decap (one opponent", "table (all three)"),
        grid=[5, 6, 7, 8, 9, 10, 12, 14],
        decap=[6, 32, 75, 91, 95, 97, 99, 100], table=[0, 1, 4, 21, 49, 74, 95, 99],
        med=("T7", "T10"), never=(0, 1), src="lab rs_clock_lab @8k"),
    "replication_crisis": dict(
        name="The Replication Crisis", score="17", disrupt_class="none",
        lab=("rc_speed_lab", "clock"),
        sel=("ALL-IN: combo player dead", "ALL-IN: table dead"),
        grid=[3, 4, 5, 6, 7, 8, 10, 12],
        decap=[0, 0, 2, 17, 59, 81, 95, 99], table=[0, 0, 0, 1, 1, 4, 34, 80],
        med=("T7", "T10"), never=(1, 20),
        src="lab rc_speed_lab @8k (ALL-IN ceiling; SQUAD defended proxy ~1 turn slower)"),
    "lorehold_spirits": dict(
        name="Lorehold Spirits", score="18", disrupt_class="none",
        lab=("lor_clock_lab", "clock"), sel=("decap (one opponent", "table (all three)"),
        grid=[5, 6, 7, 8, 9, 10, 12, 14],
        decap=[4, 18, 47, 69, 82, 89, 96, 99], table=[0, 0, 4, 16, 40, 61, 85, 95],
        med=("T8", "T10"), never=(1, 5), src="lab lor_clock_lab @8k"),
    "earthbend_the_meta": dict(
        name="Earthbend the Meta", score="17", disrupt_class="none",
        lab=("ebm_clock_lab", "clock"), sel=("decap (one opponent", "table (all three)"),
        grid=[5, 6, 7, 8, 9, 10, 12, 14],
        decap=[2, 11, 36, 66, 83, 90, 96, 99], table=[0, 0, 1, 5, 15, 31, 71, 93],
        med=("T8", "T11"), never=(1, 7), src="lab ebm_clock_lab @8k"),
    "exiles_return": dict(
        name="The Exile's Return", score="18", disrupt_class="warn",
        lab=("er_speed_lab", "clock"),
        sel=("combo player dead (decap)", "table dead"),
        grid=[4, 5, 6, 7, 8, 10, 12],
        decap=[0, 1, 9, 39, 70, 94, 99], table=[0, 0, 1, 5, 15, 55, 83],
        med=("T8", "T10"), never=(1, 12), src="lab er_speed_lab @8k"),
    "zero_sum_game": dict(
        name="Zero-Sum Game", score="—", disrupt_class="none",
        lab=("wb_clock_lab", "clock"), sel=("combo kill decap", "combo kill table"),
        grid=[4, 5, 6, 7, 8, 9, 10, 12],
        decap=[3, 13, 25, 38, 48, 57, 64, 75], table=[3, 13, 25, 38, 48, 57, 64, 75],
        med=("T9", "T9"), never=(25, 25),
        src="lab wb_clock_lab @8k (combo lifeloop, board-independent -> converge)"),
    "curse_of_the_scarab": dict(
        name="Curse of the Scarab", score="17", disrupt_class="warn",
        lab=("cos_clock_lab", "clock"), sel=("decap (one opponent", "table (all three)"),
        grid=[5, 6, 7, 8, 9, 10, 12, 14],
        decap=[3, 13, 31, 56, 74, 86, 96, 99], table=[0, 1, 4, 12, 27, 46, 76, 91],
        med=("T8", "T11"), never=(1, 9), src="lab cos_clock_lab @8k"),
    "bumbleflower": dict(
        name="Ms. Bumbleflower", score="15", disrupt_class="warn",
        lab=("bmf_clock_lab", "clock"), sel=("decap (one opponent", "table (all three)"),
        grid=[5, 6, 7, 8, 9, 10, 12, 14],
        decap=[1, 7, 39, 82, 96, 99, 100, 100], table=[0, 0, 0, 0, 3, 17, 83, 98],
        med=("T8", "T11"), never=(0, 2), src="lab bmf_clock_lab @8k"),
    "eldrazi_stampede": dict(
        name="Eldrazi Stampede Chaos", score="14", disrupt_class="none",
        lab=("esc_clock_lab", "clock"), sel=("decap (one opponent", "table (all three)"),
        grid=[5, 6, 7, 8, 9, 10, 12, 14],
        decap=[3, 10, 27, 52, 74, 87, 96, 99], table=[0, 0, 1, 4, 11, 26, 67, 92],
        med=("T8", "T12"), never=(1, 8), src="lab esc_clock_lab @8k"),
    "dark_lords_army": dict(
        name="The Dark Lord's Army", score="19", disrupt_class="warn",
        lab=("dla_clock_lab", "pod"), sel=("MID pod", None),
        grid=[6, 7, 8, 9, 10, 12, 14, 16],
        decap=[4, 16, 37, 57, 69, 84, 93, 97], table=[0, 0, 1, 6, 19, 58, 78, 90],
        med=("T9", "T12"), never=(3, 10),
        src="lab dla_clock_lab @8k (MID pod tempo — engine is opponent-driven)"),
    "diminishing_returns": dict(
        name="Diminishing Returns", score="17", disrupt_class="warn",
        lab=("dr_clock_lab", "clock"), sel=("decap", "table"),
        grid=[4, 5, 6, 7, 8, 9, 10, 12],
        decap=[0, 0, 1, 11, 38, 66, 84, 96], table=[0, 0, 0, 0, 1, 4, 10, 30],
        med=("T9", ">T14"), never=(4, 70), src="lab dr_clock_lab @8k"),
    "lightning_war": dict(
        name="Lightning War", score="19", disrupt_class="warn",
        lab=("lw_clock_lab", "clock"), sel=("decap (one opponent", "table (all three)"),
        grid=[5, 6, 7, 8, 9, 10, 12, 14],
        decap=[0, 1, 10, 32, 58, 77, 93, 99], table=[0, 0, 0, 2, 5, 12, 33, 61],
        med=("T9", "T14"), never=(1, 39),
        src="lab lw_clock_lab @8k (strict goldfish; chip/reach not in decap)"),
    "grand_design": dict(
        name="The Grand Design", score="18", disrupt_class="warn",
        lab=("gd_clock_lab", "clock"), sel=("decap (one opponent", "table (all three)"),
        grid=[4, 5, 6, 7, 8, 9, 10, 12],
        decap=[0, 0, 3, 12, 33, 59, 79, 95], table=[0, 0, 0, 0, 2, 6, 13, 38],
        med=("T9", ">T12"), never=(5, 62),
        src="lab gd_clock_lab @40k (2026-06-23 ramp+Craterhoof swap; --refresh)"),
    "crystal_sickness": dict(
        name="Crystal Sickness", score="17", disrupt_class="warn",
        lab=("cs_clock_lab", "clock"), sel=("decap (one opponent", "table (all three)"),
        grid=[5, 6, 7, 8, 9, 10, 12, 14],
        decap=[0, 1, 7, 19, 35, 49, 68, 80], table=[0, 0, 1, 6, 15, 27, 50, 66],
        med=("T11", "T13"), never=(20, 34), src="lab cs_clock_lab @8k"),
    "calamity_tax": dict(
        name="The Calamity Tax", score="18", disrupt_class="warn",
        lab=None, sel=None,                       # multi-variant lab; base not printed
        grid=[5, 6, 7, 8, 9, 11, 13, 14],
        decap=[0, 0, 1, 3, 8, 30, 50, 58], table=[0, 0, 0, 1, 2, 12, 25, 33],
        med=("T13", ">T14"), never=(40, 60),
        src="matrix 06-13 sweep median (slow; curve reconstructed, race-irrelevant)"),
}

# Guard: the display name + lab pointer in each harvest entry must match the registry (the
# authority). A new deck adds its row there; if these mirrors ever drift, fail loudly here.
for _slug, _e in CLOCKS.items():
    _r = deck_registry.DECKS.get(_slug)
    if _r is not None:
        assert _e["name"] == _r["name"], f"pod_gauntlet name drift vs deck_registry: {_slug}"
        _elab = tuple(_e["lab"]) if _e["lab"] else None
        assert _elab == _r["lab"], f"pod_gauntlet lab drift vs deck_registry: {_slug}"


# --- pending swaps (Build_And_Swap_Tracker.md §2) --------------------------
# The --swapped view: where each deck's clock/disruption lands AFTER its planned
# swap. Clock curves are harvested from the lab mode that models the swap where
# one exists (rs --mode upgrade, gd --mode ramp); doc-sourced + flagged where it
# doesn't. gate="approval" = needs pod approval (the Kiki/B4 proposals); None =
# ungated (do it now). Most swaps barely move the clock — they buy reliability /
# resilience the goldfish can't score — so many entries carry only a note.
SWAP_BUCKET = {"static": (0.55, 0.30)}      # Exile's +Drannith: Abolisher-proof static floor

SWAPS = {
    "calamity_tax": dict(
        grid=[6, 7, 8, 9, 10, 12, 14], decap=[3, 16, 38, 63, 80, 96, 99],
        table=[3, 14, 32, 51, 67, 87, 96], gate=None,
        src="lab: ct_speed_lab.kill_turns on glarb-grind-fortress-20260614.txt (12k, 2026-06-14)",
        note="grind-fortress rebuild: decap T13→T9, table >T14→T9 (ungated, mostly owned)"),
    # grand_design ramp+Craterhoof swap APPLIED 2026-06-23 (now the committed list,
    # decks/the-grand-design-20260623.txt) — entry removed. Its baseline clock now comes
    # straight from --refresh (gd_clock_lab --mode clock points at the new list). The swap
    # moved BOTH clocks (decap T10→T9 AND table never ~82→~62%), so the old "decap-only/inert"
    # framing no longer applies; the table gain is harvested into the baseline like any other deck.
    # radiation_sickness GC-fix swap APPLIED 2026-06-15 (now the committed list) — entry removed
    "exiles_return": dict(
        disrupt_class="static", gate="approval",
        src="er pending-swap + Build_And_Swap §2",
        note="+Drannith static (Abolisher-proof) +Kiki; clock ~same, disruption ↑"),
    "replication_crisis": dict(
        gate="approval", src="rc pending-Kiki (−Bident)",
        note="+Kiki Satya-free Abolisher-proof line (rare ~5% in goldfish); clock ~same, resilience ↑"),
    "diminishing_returns": dict(
        gate="approval", src="dr Stage-1 (Build_And_Swap §2)",
        note="+Nim Deathmantle + Grave Titan combo; decap ~T9 same, table ↑ slightly"),
}


# --- CDF helpers -----------------------------------------------------------
def build_cdf(grid, cum):
    """Interpolate the lab's (turn -> cum %) onto every integer turn 1..HORIZON.
    0 below the first grid turn; linear between points; flat (= never plateau)
    after the last. Returns F[t] in [0,1] for t = 0..HORIZON."""
    F = [0.0] * (HORIZON + 1)
    pts = list(zip(grid, cum))
    for t in range(1, HORIZON + 1):
        if t <= pts[0][0]:
            F[t] = pts[0][1] / 100.0 if t == pts[0][0] else 0.0
        elif t >= pts[-1][0]:
            F[t] = pts[-1][1] / 100.0
        else:
            for (t0, c0), (t1, c1) in zip(pts, pts[1:]):
                if t0 <= t <= t1:
                    f = (t - t0) / (t1 - t0)
                    F[t] = (c0 + f * (c1 - c0)) / 100.0
                    break
    for t in range(1, HORIZON + 1):           # enforce monotone non-decreasing
        F[t] = max(F[t], F[t - 1])
    return F


CLOCKS_JSON = ROOT / "analysis" / "pod_gauntlet_clocks.json"


def merged_clocks():
    """Baked CLOCKS metadata overlaid with the canonical JSON curves (the lab
    harvest written by --refresh, default 40k). The JSON is the single source of
    truth for grid/decap/table/med/never; baked values are the seed/fallback when
    it's absent — so the gauntlet and clock_check.py read the same numbers."""
    out = {s: dict(c) for s, c in CLOCKS.items()}
    if CLOCKS_JSON.exists():
        try:
            J = json.loads(CLOCKS_JSON.read_text(encoding="utf-8"))
        except (ValueError, OSError):
            return out
        for s, c in out.items():
            for k in ("grid", "decap", "table", "med", "never"):
                if k in (J.get(s) or {}):
                    c[k] = J[s][k]
    return out


def disruption(slug, a, k, swapped=False):
    """P(we disrupt one combo attempt) at Abolisher-prob a, combo turn k."""
    if swapped and slug in SWAPS and "disrupt_class" in SWAPS[slug]:
        full, static = SWAP_BUCKET[SWAPS[slug]["disrupt_class"]]
        return full + a * (static - full)
    if slug in MEASURED:
        row = MEASURED[slug][6 if k <= 6 else 7]
        for (a0, v0), (a1, v1) in zip(zip(A_GRID, row), zip(A_GRID[1:], row[1:])):
            if a0 <= a <= a1:
                return (v0 + (a - a0) / (a1 - a0) * (v1 - v0)) / 100.0
        return row[-1] / 100.0
    meta = CLOCKS.get(slug) or BUILD_CLOCKS.get(slug, {})
    full, static = BUCKET[meta.get("disrupt_class", "none")]
    return full + a * (static - full)


def cdf_for(slug, which, swapped, clocks):
    """decap/table CDF for a deck, applying its pending swap when swapped=True."""
    s = SWAPS.get(slug)
    if swapped and s and s.get(which) is not None:
        return build_cdf(s["grid"], s[which])
    c = clocks[slug]
    return build_cdf(c["grid"], c[which])


def pod_kdist(args):
    d = dict(K_DIST)
    if args.pod_fast:
        d = {5: 0.20, 6: 0.40, 7: 0.28, 8: 0.10, 9: 0.02}
    if args.pod_slow:
        d = {5: 0.04, 6: 0.22, 7: 0.34, 8: 0.26, 9: 0.14}
    return d


# --- the race --------------------------------------------------------------
def pure_race(F, kdist):
    """P(decap turn <= combo turn K), disruption ignored. Closed form."""
    return sum(p * F[k] for k, p in kdist.items())


def sample_kill(F, rng):
    """Inverse-CDF sample of our decap turn; HORIZON+1 == 'never in horizon'."""
    u = rng.random()
    for t in range(1, HORIZON + 1):
        if u <= F[t]:
            return t
    return HORIZON + 1


def simulate(slug, F, a, kdist, trials, rng, swapped=False):
    """Monte Carlo P(win) with the disruption overlay. Returns (win, lose,
    grind) fractions; grind = undecided at horizon (counted as a loss in win)."""
    ks, kp = zip(*kdist.items())
    win = grind = 0
    for _ in range(trials):
        K = rng.choices(ks, weights=kp)[0]
        tkill = sample_kill(F, rng)
        if tkill <= K:
            win += 1
            continue
        D = disruption(slug, a, K, swapped)
        decided = False
        for t in range(K, HORIZON + 1):
            if tkill == t:                    # our turn t precedes their turn t
                win += 1
                decided = True
                break
            if rng.random() < (1 - D):        # their combo resolves
                decided = True
                break
        if not decided:
            grind += 1
    return win / trials, 1 - (win + grind) / trials, grind / trials


def simulate_vs(slug, F, opp, kdist, trials, rng):
    """P(win) vs ONE specific opponent deck (the --vs model). Differences from simulate():
      * disruption uses opp['disruption_a'] — NOT a global Abolisher. Acererak is mono-B
        (no Abolisher, no counters) so our reactive answers almost all live; H&K is UB (a
        counter wall ~ the old baseline tax); only the 5C tail fields the white Abolisher.
      * opp['answer'] = P(THEY stop OUR kill on the stack), rolled each kill attempt with
        finite, decaying interaction (they don't have infinite counters). An answered kill
        costs us a turn (reload) rather than ending the game — and Abolisher does NOT figure
        here, since it acts only on their turn while our kill is on ours. PROTECT[slug] (our own
        counter package / uncounterable finisher) reduces that answer: answer * (1 - protect)."""
    ks, kp = zip(*kdist.items())
    # PROTECT = our counter-war capability; it eases the SAME counter wall on both fronts —
    # our disruption of their combo (a) and our kill landing (answer). For Acererak (no counters)
    # the taxes are ~0 so this barely moves; vs H&K it's the whole counter-heavy-deck correction.
    a = opp["disruption_a"] * (1 - PROTECT.get(slug, 0.0))
    win = grind = 0
    for _ in range(trials):
        K = rng.choices(ks, weights=kp)[0]
        tkill = sample_kill(F, rng)
        D = disruption(slug, a, K)
        answer = opp["answer"] * (1 - PROTECT.get(slug, 0.0))   # our protect-own reduces their answer
        ready = tkill                              # earliest turn our kill is online
        decided = False
        for t in range(1, HORIZON + 1):
            if t >= ready:                         # our turn t (we precede their turn t)
                if rng.random() >= answer:         # our kill resolves
                    win += 1; decided = True; break
                ready = t + 1                      # answered -> reload next turn
                answer *= ANSWER_DECAY             # their interaction is finite
            if t >= K:                             # their combo attempt this turn
                if rng.random() < (1 - D):         # resolves -> we lose
                    decided = True; break
        if not decided:
            grind += 1
    return win / trials, grind / trials


def simulate_vs_lock(slug, F, opp, kdist, lock_cdf, e, r, trials, rng):
    """simulate_vs + a loop-typed PERSISTENT lock. lock_cdf = P(the lock is online by turn t)
    in this deck's shell (lock_lab); e = its effectiveness vs THIS opponent's loop
    (LOCK_VS_LOOP[piece][opp.loop]); r = pod's per-turn removal rate. Once live & effective the
    lock holds the pod's combo EVERY turn until removed. With e=0 (e.g. an ETB-lock vs H&K's
    death trigger) this reduces EXACTLY to simulate_vs — so those columns are provably unchanged."""
    ks, kp = zip(*kdist.items())
    a = opp["disruption_a"] * (1 - PROTECT.get(slug, 0.0))
    use_lock = lock_cdf is not None and e > 0
    win = grind = 0
    for _ in range(trials):
        K = rng.choices(ks, weights=kp)[0]
        tkill = sample_kill(F, rng)
        D = disruption(slug, a, K)
        answer = opp["answer"] * (1 - PROTECT.get(slug, 0.0))
        t_lock = sample_kill(lock_cdf, rng) if use_lock else HORIZON + 1
        lock_alive = t_lock <= HORIZON
        ready = tkill
        decided = False
        for t in range(1, HORIZON + 1):
            if t >= ready:                            # our kill attempt (precedes their turn t)
                if rng.random() >= answer:
                    win += 1; decided = True; break
                ready = t + 1; answer *= ANSWER_DECAY
            if t >= K:                                # their combo attempt
                if lock_alive and t >= t_lock and rng.random() < e:
                    if rng.random() < r:
                        lock_alive = False            # pod cleared it -> free next turn
                    continue                          # lock held this turn
                if rng.random() < (1 - D):
                    decided = True; break
        if not decided:
            grind += 1
    return win / trials, grind / trials


# --- lock-aware race (the opponent-clock-tax model, via PERSISTENT locks) ---
# A persistent hard-lock differs from the one-shot D above: once live & effective it
# stops the pod EVERY turn until they REMOVE it (rate r) — not re-rolled each turn. A
# mana-tax shifts the combo turn K out by tau/g (pod mana growth). With an EMPTY package
# this reduces EXACTLY to simulate() (lock never active, Delta=0) — so the lock-less decks
# are provably unchanged. Lock availability + e/tau come from lock_lab.py ->
# analysis/lock_availability.json (the same lab->JSON->gauntlet pattern as the clocks).
LOCK_JSON = ROOT / "analysis" / "lock_availability.json"
R_BASE = 0.25                                  # P(pod removes our lock each of their turns)
R_SWEEP = [0.0, 0.15, 0.25, 0.40, 0.60]
POD_MANA_GROWTH = 1.4                          # mana the Ur-Dragon shell adds per turn (tau->Delta)

# Build-candidate clocks (NOT active roster; lab-sourced). Used by the --lock view (Kefka,
# whose Cursed Totem is its anti-pod reason to exist) AND folded into --matrix / --vs under
# the --pending flag, so a deck being built can be placed in the matrix before it's sleeved.
# disrupt_class "warn" = it has a real one-shot counter suite; the lock (Kefka) is scored
# separately via lock_availability.json (no double-count).
BUILD_CLOCKS = {
    "kefka": dict(
        name="Kefka (Forced Liq., build)", score="~17", disrupt_class="warn",
        grid=[4, 5, 6, 7, 8, 9, 10, 12],
        decap=[1, 4, 14, 34, 58, 75, 86, 96], table=[0, 2, 7, 19, 39, 58, 72, 88],
        med=("T8", "T9"), never=(4, 12), src="lab kfk_clock_lab @4k 2026-06-15"),
    "hashaton": dict(
        name="Hashaton (Thoracle, build)", score="~17", disrupt_class="warn",
        grid=[3, 4, 5, 6, 7, 8, 9, 10, 12],
        decap=[5, 21, 44, 61, 72, 77, 82, 86, 91],
        table=[5, 21, 44, 61, 72, 77, 82, 86, 91],   # Thoracle: decap = table by construction
        med=("T6", "T6"), never=(9, 9), src="lab hsh_clock_lab @8k 2026-06-18"),
}


def load_lockdata():
    if not LOCK_JSON.exists():
        return {}
    try:
        return json.loads(LOCK_JSON.read_text(encoding="utf-8"))
    except (ValueError, OSError):
        return {}


def lock_race(slug, F, ld, a, r, kdist, trials, rng, g_mana=POD_MANA_GROWTH, use_tut=False):
    """P(win) with the persistent-lock overlay. ld = this deck's lock_availability entry
    (None/empty -> reduces to simulate's win rate). F = our decap CDF; slug feeds the
    one-shot disruption (unchanged); a = P(Abolisher out); r = pod removal rate of our lock."""
    grid = (ld or {}).get("grid")
    hl = (ld or {}).get("hl_tut" if use_tut else "hl_drawn")
    e = (ld or {}).get("e", 0.0) or 0.0
    tau_curve = (ld or {}).get("tau")
    hl_cdf = build_cdf(grid, hl) if (grid and hl and e > 0) else None
    ks, kp = zip(*kdist.items())
    win = 0
    for _ in range(trials):
        K0 = rng.choices(ks, weights=kp)[0]
        Delta = 0                              # mana-tax: push the combo turn out by tau/g
        if tau_curve and grid:
            tau_at = tau_curve[min(range(len(grid)), key=lambda i: abs(grid[i] - K0))]
            Delta = int(round(tau_at / g_mana))
        K = K0 + Delta
        tkill = sample_kill(F, rng)
        if tkill <= K:
            win += 1
            continue
        D = disruption(slug, a, K0)            # one-shot answers judged on the real combo turn
        t_lock = sample_kill(hl_cdf, rng) if hl_cdf else HORIZON + 1
        eff = (rng.random() < e) if hl_cdf else False
        lock_alive = t_lock <= HORIZON
        for t in range(K, HORIZON + 1):
            if tkill == t:                     # our turn t precedes their turn t
                win += 1
                break
            if lock_alive and eff and t >= t_lock:   # persistent lock holds this turn
                if rng.random() < r:
                    lock_alive = False         # pod cleared it -> free next turn
                continue
            if rng.random() < (1 - D):         # their combo resolves -> loss
                break
        # falling off the horizon undecided = loss (they grind through)
    return win / trials


# --- refresh (re-harvest clock curves from the labs) -----------------------
def parse_row(lines, selector, grid):
    """Find the row whose label contains `selector` and return its ints mapped
    to grid. The lab prints f'{v:6.0f}' per grid turn as the RIGHTMOST run on
    the line, so take the last len(grid) ints in 0..100 — this drops stray label
    numbers to their left ('decap (one opponent, 40)', 'MID pod (6 spells / 4
    draws)'). None if no qualifying row. The count guard rejects the 2-int
    'median decap T7 / table T8' summary line."""
    if selector is None:
        return None
    for ln in lines:
        if selector.lower() in ln.lower():
            ln = re.sub(r"\b[Tt]\d+\b", "", ln)        # drop 'med T8' / 'T9' median tags
            ints = [int(x) for x in re.findall(r"-?\d+", ln) if 0 <= int(x) <= 100]
            if len(ints) >= len(grid):
                return ints[-len(grid):]
    return None


def refresh(trials, out_path=None):
    out_path = Path(out_path).resolve() if out_path else CLOCKS_JSON
    print(f"# refresh — re-running the clock labs @ {trials} trials -> {out_path.name}\n")
    prior = {}
    if CLOCKS_JSON.exists():
        try:
            prior = json.loads(CLOCKS_JSON.read_text(encoding="utf-8"))
        except (ValueError, OSError):
            prior = {}
    updated = {}
    for slug, c in CLOCKS.items():
        if not c["lab"]:
            print(f"  {slug:22} SKIP (no single-deck clock mode; keep baked)")
            updated[slug] = c
            continue
        script, mode = c["lab"]
        try:
            out = subprocess.run(
                [sys.executable, str(ROOT / "scripts" / f"{script}.py"),
                 "--mode", mode, "--trials", str(trials)],
                capture_output=True, text=True, timeout=300, cwd=str(ROOT))
            lines = out.stdout.splitlines()
        except Exception as e:                                  # noqa: BLE001
            print(f"  {slug:22} ERROR running {script}: {e}; keep baked")
            updated[slug] = c
            continue
        dsel, tsel = c["sel"]
        dec = parse_row(lines, dsel, c["grid"])
        tab = parse_row(lines, tsel, c["grid"]) or c["table"]
        if dec is None:
            print(f"  {slug:22} PARSE-FAIL (decap sel {dsel!r}); keep baked")
            updated[slug] = c
            continue
        nc = dict(c)
        base = (prior.get(slug) or {}).get("decap", c["decap"])   # diff vs last JSON, not 8k seed
        flag = f"  <-- decap changed from {base}" if dec != base else ""
        nc["decap"], nc["table"] = dec, tab
        updated[slug] = nc
        print(f"  {slug:22} decap {dec}{flag}")
    out_path.write_text(json.dumps(
        {s: {k: v for k, v in c.items() if k in
             ("name", "grid", "decap", "table", "med", "never", "src")}
         for s, c in updated.items()}, indent=2), encoding="utf-8")
    rel = out_path.relative_to(ROOT) if out_path.is_relative_to(ROOT) else out_path
    print(f"\n  wrote {rel} (also feeds backlog #2)")


# --- report ----------------------------------------------------------------
def run(args):
    rng = random.Random(args.seed)
    kdist = pod_kdist(args)
    C = merged_clocks()
    cdfs = {s: build_cdf(c["grid"], c["decap"]) for s, c in C.items()}
    tdfs = {s: build_cdf(c["grid"], c["table"]) for s, c in C.items()}

    rows = []
    for slug, c in C.items():
        F = (tdfs if args.strict else cdfs)[slug]
        pr = pure_race(F, kdist)
        win, _, grind = simulate(slug, F, args.a, kdist, args.trials, rng)
        Db = disruption(slug, args.a, 7)
        band = [simulate(slug, F, a, kdist, args.trials // 2, rng)[0] for a in A_SWEEP]
        rows.append((slug, c, pr, win, Db, band))
    rows.sort(key=lambda r: -r[3])

    clk = "TABLE clock (did we actually close?)" if args.strict else "DECAP clock (neutralise the archenemy)"
    print(f"\n{'='*92}\nTHE POD GAUNTLET — P(beat the T6-7 combo pod)   [{clk}]")
    kd = " ".join(f"T{k}:{int(p*100)}%" for k, p in sorted(kdist.items()))
    print(f"  opponent combo turn K = {{{kd}}}   ·   Abolisher P(out)={args.a}   ·   "
          f"trials={args.trials}, seed={args.seed}")
    print(f"  PURE RACE = P(decap<=K), disruption ignored (fully simulated).  "
          f"P(WIN) folds in disruption (measured*/bucketed).\n")
    print(f"  {'deck':24}{'sc':>3}{'decap':>7}{'pure':>7}{'D@.3':>6}{'P(WIN)':>8}   P(win) vs P(Abolisher out)")
    print(f"  {'':24}{'':>3}{'med':>7}{'race':>7}{'':>6}{'':>8}   " +
          " ".join(f"a={a}" for a in A_SWEEP))
    for slug, c, pr, win, Db, band in rows:
        star = "*" if slug in MEASURED else " "
        print(f"  {c['name']:24}{c['score']:>3}{c['med'][0]:>7}{pr*100:>6.0f}%"
              f"{Db*100:>5.0f}%{star}{win*100:>6.0f}%   " +
              "  ".join(f"{b*100:>3.0f}" for b in band))
    print(f"\n  * disruption now MEASURED via delay_lab for ALL 16 decks "
          f"(analysis/delay_disruption.json; limitation #2 closed 2026-06-15).\n"
          f"    Regenerate: python scripts/delay_lab.py --emit-json. Buckets remain only as a "
          f"fallback for off-roster builds.")
    print(f"  Clock curves are UNBLOCKED goldfish ceilings — PURE RACE is an optimistic "
          f"front edge, not a win rate.")
    print(f"  Read the RANKING and the gap between PURE RACE and P(WIN) (= how much a "
          f"deck leans on disruption).\n")


def run_swapped(args):
    """Current vs after-the-pending-swaps P(win), per Build_And_Swap_Tracker §2."""
    rng = random.Random(args.seed)
    kdist = pod_kdist(args)
    which = "table" if args.strict else "decap"
    rows = []
    C = merged_clocks()
    for slug, c in C.items():
        cur = simulate(slug, cdf_for(slug, which, False, C), args.a, kdist, args.trials, rng)[0]
        sw = simulate(slug, cdf_for(slug, which, True, C), args.a, kdist, args.trials, rng,
                      swapped=True)[0]
        rows.append((slug, c, cur, sw, SWAPS.get(slug)))
    rows.sort(key=lambda r: -r[3])

    clk = "table" if args.strict else "decap"
    print(f"\n{'='*96}\nTHE POD GAUNTLET — current vs AFTER PENDING SWAPS   "
          f"[{clk} clock · Abolisher P(out)={args.a}]")
    print("  swaps from Build_And_Swap_Tracker §2. 🔒 = needs pod approval (else ungated).")
    print("  clocks: lab-harvested where a mode models the swap (rs upgrade / gd ramp), "
          "else doc-sourced.\n")
    print(f"  {'deck':24}{'now':>6}{'swap':>7}{'Δ':>6}  gate  swap")
    for slug, c, cur, sw, s in rows:
        if not s:
            continue
        d = (sw - cur) * 100
        gate = "🔒" if s.get("gate") == "approval" else " ·"
        print(f"  {c['name']:24}{cur*100:>5.0f}%{sw*100:>6.0f}%{d:>+6.0f}  {gate}   {s['note']}")
    print(f"\n  (the 10 decks with no §2 swap are unchanged and omitted.)")
    print("\n  HEADLINE: the swaps are mostly reliability/resilience upgrades the goldfish "
          "can't score —\n  the real clock movers are Calamity's ungated grind rebuild "
          "(T13→T9) and GD's ramp (T10→T9).\n  Exile's gains Abolisher-proof static "
          "(Drannith); the three 🔒 swaps need pod approval.")


def run_matrix(args):
    """Emit the --vs two-deck rows for Pod_Matchup_Matrix.md, sorted by BLENDED P(win).
    Lab-sourced (clock JSON) + gauntlet-computed — no narrated numbers. The matrix pastes
    these and adds its judgment verdict column. Per-opponent (Acererak / Hidetsugu&Kairi /
    5C-tail) + protect-own; the GD persistent-lock lift is a --vs-lock footnote, not a column."""
    rng = random.Random(args.seed)
    kd = pod_kdist(args)
    C = merged_clocks()
    if getattr(args, "pending", False):
        C = {**C, **BUILD_CLOCKS}                 # fold in build candidates (Kefka/Hashaton)
    okeys = list(OPPONENTS)
    rows = []
    for slug, c in C.items():
        F = cdf_for(slug, "decap", False, C)
        per = {k: simulate_vs(slug, F, OPPONENTS[k], kd, args.trials, rng)[0] for k in okeys}
        blend = sum(OPPONENTS[k]["weight"] * per[k] for k in okeys)
        rows.append((blend, c, slug, per))
    rows.sort(key=lambda r: -r[0])
    w = OPPONENTS
    print(f"\n# Pod_Matchup_Matrix --vs rows (two-deck model, trials={args.trials})\n")
    print("| # | Deck | Sc | Clock decap / table | prot | vs Acererak | vs H&K | vs 5C-tail | BLEND |")
    print("|---|---|---|---|---|---|---|---|---|")
    for i, (blend, c, slug, per) in enumerate(rows, 1):
        print(f"| {i} | {c['name']} | {c['score']} | {c['med'][0]} / {c['med'][1]} | "
              f"{PROTECT.get(slug,0)*100:.0f}% | {per['acererak']*100:.0f}% | "
              f"{per['hidetsugu_kairi']*100:.0f}% | {per['five_color_tail']*100:.0f}% | "
              f"**{blend*100:.0f}%** |")
    print(f"\nBLEND = weight-avg over his decks (Acererak {w['acererak']['weight']} / H&K "
          f"{w['hidetsugu_kairi']['weight']} / 5C-tail {w['five_color_tail']['weight']}, PRIORS). "
          f"prot = protect-own (counter-war + counter-immune kill). Clock = lab decap/table median. "
          f"GD also has a persistent-lock line (--vs-lock): 45% blend / 59% vs Acererak. "
          f"Regenerate: pod_gauntlet.py --matrix")


def print_hatebear_table():
    """The per-commander hatebear column, quantified: which static hits which loop."""
    loops = [("etb", "Acererak"), ("death", "H&K"), ("mixed", "5C-tail")]
    print(f"\n  HATEBEAR × LOOP — e = P(stops the combo | the piece is live). STRUCTURE verified")
    print(f"  from oracle text this session; magnitudes are priors. Read the ZEROES, not decimals.")
    print(f"  {'static':22}" + "".join(f"{lab:>10}" for _, lab in loops))
    for piece, row in LOCK_VS_LOOP.items():
        print(f"  {piece:22}" + "".join(f"{row[lk]*100:>9.0f}%" for lk, _ in loops))
    print(f"  Torpor Orb / Hushwing Gryff hard-lock Acererak (ETB) and are a STONE BLANK vs H&K")
    print(f"  (death trigger). Only Rule of Law-class + exile-the-commander-on-sight + RACING hit both.")


def run_vs(args):
    """Race each roster deck vs his TWO REAL decks separately, then blend by how often he
    brings each. Splits the generic opponent (run()) into Acererak / H&K / 5C-tail and adds
    the interaction-against-us term. The PER-OPPONENT columns are the payoff: they show where
    a deck's matchup swings on who he's piloting — reactive/counter decks recover vs Acererak
    (no Abolisher, no counters) and sag vs H&K (a UB counter wall)."""
    rng = random.Random(args.seed)
    C = merged_clocks()
    if getattr(args, "pending", False):
        C = {**C, **BUILD_CLOCKS}                 # fold in build candidates (Kefka/Hashaton)
    which = "table" if args.strict else "decap"
    kd = pod_kdist(args)
    okeys = list(OPPONENTS)
    rows = []
    for slug, c in C.items():
        F = build_cdf(c["grid"], c[which])
        per = {k: simulate_vs(slug, F, OPPONENTS[k], kd, args.trials, rng)[0] for k in okeys}
        blend = sum(OPPONENTS[k]["weight"] * per[k] for k in okeys)
        rows.append((slug, c, per, blend))
    rows.sort(key=lambda r: -r[3])

    clk = "TABLE clock (win the game)" if args.strict else "DECAP clock (neutralise the deck)"
    print(f"\n{'='*94}\nTHE POD GAUNTLET — vs HIS TWO REAL DECKS   [{clk}]")
    kds = " ".join(f"T{k}:{int(p*100)}%" for k, p in sorted(kd.items()))
    print(f"  combo turn K = {{{kds}}}   ·   trials={args.trials}, seed={args.seed}")
    print(f"  OUR disruption uses each deck's reactive-answer tax (a), NOT a global Abolisher — "
          f"Acererak & H&K\n  are color-locked out of the white Grand Abolisher; only the 5C tail "
          f"can field it. 'ans' = P(they\n  answer OUR kill on the stack).")
    for k in okeys:
        o = OPPONENTS[k]
        print(f"    {o['name']:26} w={o['weight']:.2f}  a={o['disruption_a']:.2f}  "
              f"ans={o['answer']:.2f}  [{o['loop']}]  — {o['note']}")
    print()
    print(f"  {'deck':24}{'sc':>3}{'clk':>6}{'prot':>6}{'Acrk':>7}{'H&K':>7}{'tail':>7}{'BLEND':>8}   Δ(Acrk−H&K)")
    for slug, c, per, blend in rows:
        d = (per['acererak'] - per['hidetsugu_kairi']) * 100
        print(f"  {c['name']:24}{c['score']:>3}{c['med'][0]:>6}{PROTECT.get(slug,0)*100:>5.0f}%"
              f"{per['acererak']*100:>6.0f}%{per['hidetsugu_kairi']*100:>6.0f}%"
              f"{per['five_color_tail']*100:>6.0f}%{blend*100:>7.0f}%   {d:>+6.0f}")
    print(f"\n  prot = P(this deck forces its kill THROUGH their answer) — own counters + uncounterable")
    print(f"  finisher (PROTECT, a verified-where-set prior). Δ(Acrk−H&K) = swing by which deck he brings.")
    print_hatebear_table()
    print(f"\n  Weights/answers are PRIORS (favorite + recent flood), not measured — tune in OPPONENTS.")
    print(f"  Clocks are unblocked goldfish ceilings; read the ranking and the per-opponent spread.")


def run_vs_lock(args):
    """--vs + a loop-typed PERSISTENT lock, for decks that RUN one (VS_LOCKS). Tests the axis the
    decap-race under-credits: a control deck that LOCKS the archenemy rather than out-races it.
    GD's Elesh Norn hard-stops Acererak (ETB) and is inert vs H&K (death) — exactly loop-typed.
    Availability is measured in the deck's real shell via lock_lab; clock = the deck's pending swap
    where it has one (so the lock stacks on the swap floor, not the unfixed clock)."""
    import importlib.util as _il
    spec = _il.spec_from_file_location("lock_lab", ROOT / "scripts" / "lock_lab.py")
    LL = _il.module_from_spec(spec); spec.loader.exec_module(LL)
    index = LL.ds.load_oracle_index(); aliases = LL.ds.load_reskin_aliases()
    C = merged_clocks(); kd = pod_kdist(args)
    which = "table" if args.strict else "decap"
    wb = lambda d: sum(OPPONENTS[k]["weight"] * d[k] for k in OPPONENTS)
    print(f"\n{'='*100}\nTHE POD GAUNTLET — vs HIS TWO DECKS + PERSISTENT LOCK   [{which} · r={args.r}]")
    print("  Overlays a loop-typed persistent lock (LOCK_VS_LOOP) on the --vs race for decks that RUN")
    print("  one (VS_LOCKS). e per opponent = its effect vs that deck's loop; availability measured")
    print("  in-shell by lock_lab (drawn floor / +tutors). Abolisher/Teferi are protect-own (PROTECT),")
    print("  not here. Clock = the deck's pending swap where it has one.\n")
    for slug, locks in VS_LOCKS.items():
        if slug not in C:
            continue
        piece, c = locks[0], C[slug]
        swapped = slug in SWAPS and SWAPS[slug].get(which) is not None
        F = cdf_for(slug, which, swapped, C)
        evec = LOCK_VS_LOOP.get(piece, {})
        lib = LL.load(slug, index, aliases)
        rec = index.get(piece.lower())
        cost = int(round((rec.get("cmc") if rec else None) or 5))
        pkg = {LL.HARDLOCK: [(piece, cost, max(evec.values(), default=0.5), "loop-typed")],
               LL.MANATAX: [], LL.EXCLUDED: []}
        d_av, _, _ = LL.measure(lib, pkg, args.trials, random.Random(LL.SEED))
        saved = LL.TUTORS                              # creature-tutor-aware ceiling (Elesh Norn IS a creature)
        LL.TUTORS = saved | {"Eladamri's Call", "Chord of Calling", "Fauna Shaman", "Birthing Pod",
                             "Razaketh, the Foulblooded", "Sidisi, Undead Vizier", "Defense of the Heart"}
        t_av, _, _ = LL.measure(lib, pkg, args.trials, random.Random(LL.SEED), use_tutors=True)
        LL.TUTORS = saved
        cdf_drawn = build_cdf(LL.GRID, [d_av[t] for t in LL.GRID])
        cdf_tut = build_cdf(LL.GRID, [t_av[t] for t in LL.GRID])
        clk = (SWAPS[slug].get("note", "swap").split(":")[0] if swapped else "current") + \
              f" clock ({'T9' if swapped else c['med'][0]})"
        print(f"  {c['name']} + {piece}")
        print(f"    {clk} · e[etb/death/mixed]={evec.get('etb',0):.2f}/{evec.get('death',0):.2f}/"
              f"{evec.get('mixed',0):.2f} · lock online by T6 {d_av[6]:.0f}% drawn ({t_av[6]:.0f}% +tut) / "
              f"T7 {d_av[7]:.0f}% ({t_av[7]:.0f}%)  [FLOOR: reanimation uncounted]\n")
        rng = random.Random(args.seed)
        per_base = {}; per_drawn = {}; per_tut = {}
        print(f"    {'opponent':22}{'base':>7}{'+lock drawn':>13}{'+lock tut':>11}")
        for okey, opp in OPPONENTS.items():
            e = evec.get(opp["loop"], 0.0)
            per_base[okey] = simulate_vs(slug, F, opp, kd, args.trials, rng)[0]
            per_drawn[okey] = simulate_vs_lock(slug, F, opp, kd, cdf_drawn, e, args.r, args.trials, rng)[0]
            per_tut[okey] = simulate_vs_lock(slug, F, opp, kd, cdf_tut, e, args.r, args.trials, rng)[0]
            print(f"    {opp['name'][:18]+' ['+opp['loop'][:3]+']':22}{per_base[okey]*100:>6.0f}%"
                  f"{per_drawn[okey]*100:>12.0f}%{per_tut[okey]*100:>10.0f}%")
        print(f"    {'BLEND':22}{wb(per_base)*100:>6.0f}%{wb(per_drawn)*100:>12.0f}%{wb(per_tut)*100:>10.0f}%")
        print(f"\n    BLEND vs pod-removal r:   " + "   ".join(f"r={rr}" for rr in R_SWEEP))
        for label, cdf in (("drawn", cdf_drawn), ("+tut", cdf_tut)):
            cells = []
            for rr in R_SWEEP:
                rng2 = random.Random(args.seed)
                d = {k: simulate_vs_lock(slug, F, OPPONENTS[k], kd, cdf,
                                         evec.get(OPPONENTS[k]["loop"], 0.0), rr, args.trials // 2, rng2)[0]
                     for k in OPPONENTS}
                cells.append(wb(d))
            print(f"      {label:6}" + "    ".join(f"{x*100:>4.0f}" for x in cells))
    print(f"\n  Only the Acererak column moves — the lock is provably inert vs H&K/tail (ETB-lock, e=0).")
    print(f"  Availability is a FLOOR (reanimation + the full creature-tutor suite uncounted), so the")
    print(f"  real lift runs higher. A lock removed on sight (high r) decays toward the no-lock --vs.")


def run_lock(args):
    """Current (one-shot disruption only) vs LOCK-AWARE P(win), per deck, sweeping the
    pod's removal rate r. Reads analysis/lock_availability.json (lock_lab.py)."""
    LD = load_lockdata()
    if not LD:
        print("  no analysis/lock_availability.json — run: python scripts/lock_lab.py")
        return
    rng = random.Random(args.seed)
    kdist = pod_kdist(args)
    C = {**merged_clocks(), **BUILD_CLOCKS}     # +Kefka build (lock view only)
    which = "table" if args.strict else "decap"
    rows = []
    for slug, c in C.items():
        F = build_cdf(c["grid"], c[which])
        cur = simulate(slug, F, args.a, kdist, args.trials, rng)[0]
        ld = LD.get(slug)
        lk = lock_race(slug, F, ld, args.a, args.r, kdist, args.trials, rng,
                       g_mana=args.pod_mana_growth, use_tut=args.use_lock_tutors)
        band = [lock_race(slug, F, ld, args.a, rr, kdist, args.trials // 2, rng,
                          g_mana=args.pod_mana_growth, use_tut=args.use_lock_tutors)
                for rr in R_SWEEP]
        rows.append((slug, c, cur, lk, (ld or {}).get("e", 0.0),
                     (ld or {}).get("tau_total", 0.0), band))
    rows.sort(key=lambda r: -r[3])
    clk = "TABLE" if args.strict else "DECAP"
    tut = "with-tutors" if args.use_lock_tutors else "drawn-only"
    print(f"\n{'='*100}\nTHE POD GAUNTLET — LOCK-AWARE   [{clk} clock · a={args.a} · "
          f"pod-removal r={args.r} · lock avail {tut}]")
    print("  'cur' = one-shot disruption only (the standing gauntlet). 'lock' = + the persistent-")
    print("  lock overlay (a live, effective lock holds every turn until the pod removes it at r).")
    print("  Empty-package decks are IDENTICAL by construction — the model only moves real locks.\n")
    print(f"  {'deck':24}{'e':>5}{'τ':>5}{'cur':>7}{'lock':>7}{'Δ':>6}   lock P(win) vs pod-removal r")
    print(f"  {'':24}{'':>5}{'':>5}{'':>7}{'':>7}{'':>6}   " +
          "  ".join(f"r={rr}" for rr in R_SWEEP))
    for slug, c, cur, lk, e, tau, band in rows:
        d = (lk - cur) * 100
        flag = "" if (e > 0 or tau > 0) else "   · no package"
        print(f"  {c['name']:24}{e:>5.2f}{tau:>5.1f}{cur*100:>6.0f}%{lk*100:>6.0f}%{d:>+6.0f}   "
              + "   ".join(f"{b*100:>3.0f}" for b in band) + flag)
    print(f"\n  lock data: analysis/lock_availability.json (lock_lab.py). e = P(lock stops THIS "
          f"pod | live), r swept.\n  A lock helps only if it is AVAILABLE (single copies are "
          f"~13% drawn by T6), EFFECTIVE (e), and STICKS (low r).\n  Read the gap cur→lock and "
          f"the r-sensitivity: a lock removed on sight (high r) buys almost nothing.")


def run_lock_add(args):
    """What-if: inject a catalog static into a deck, measure its availability in that
    shell (lock_lab), and race current vs with-the-add. args.add = 'slug=Piece Name'."""
    import importlib.util as _il
    spec = _il.spec_from_file_location("lock_lab", ROOT / "scripts" / "lock_lab.py")
    LL = _il.module_from_spec(spec); spec.loader.exec_module(LL)
    slug, _, piece = args.add.partition("=")
    slug, piece = slug.strip(), piece.strip()
    if slug not in LL.DECKS:
        print(f"  unknown deck slug {slug!r}; choices: {', '.join(LL.DECKS)}")
        return
    if piece not in LL.CATALOG:
        print(f"  {piece!r} not in the lock catalog; choices: {', '.join(LL.CATALOG)}")
        return
    index = LL.ds.load_oracle_index()
    aliases = LL.ds.load_reskin_aliases()
    rec = index.get(piece.lower())
    if rec is None:
        print(f"  {piece!r} not in the oracle data")
        return
    base = LL.load(slug, index, aliases)
    lib = base + [(piece, rec)]
    pkg = LL.inventory(lib)
    d_av, d_tau, _ = LL.measure(lib, pkg, args.trials, random.Random(LL.SEED))
    t_av, _tt, _ = LL.measure(lib, pkg, args.trials, random.Random(LL.SEED), use_tutors=True)
    ld = dict(grid=LL.GRID, hl_drawn=[d_av[t] for t in LL.GRID],
              hl_tut=[t_av[t] for t in LL.GRID], tau=[d_tau[t] for t in LL.GRID],
              e=LL.combined_e(pkg), tau_total=LL.total_tau(pkg))
    C = merged_clocks()
    if slug not in C:
        print(f"  {slug} has no clock curve in the gauntlet (build candidate); can't race it here")
        return
    c = C[slug]
    F = build_cdf(c["grid"], c["table" if args.strict else "decap"])
    rng = random.Random(args.seed)
    kdist = pod_kdist(args)
    cur = simulate(slug, F, args.a, kdist, args.trials, rng)[0]
    kind, cost, val, note = LL.CATALOG[piece]
    print(f"\n{'='*100}\nWHAT-IF — add {piece} to {c['name']}   [a={args.a}, "
          f"avail drawn (with-tutors)]")
    print(f"  {piece}: {kind} cost {cost} {'e' if kind=='hardlock' else 'τ'}={val} — {note}")
    print(f"  availability by their combo turn: T6 {d_av[6]:.0f}% ({t_av[6]:.0f}%)  ·  "
          f"T7 {d_av[7]:.0f}% ({t_av[7]:.0f}%)\n")
    print(f"  {'':20}{'cur':>7}" + "".join(f"   r={rr}" for rr in R_SWEEP))
    for tutflag, lab in ((False, "lock (drawn)"), (True, "lock (+tutors)")):
        band = [lock_race(slug, F, ld, args.a, rr, kdist, args.trials, rng,
                          g_mana=args.pod_mana_growth, use_tut=tutflag) for rr in R_SWEEP]
        print(f"  {lab:20}{cur*100:>6.0f}%" + "".join(f"{b*100:>6.0f}" for b in band))
    print(f"\n  cur = without the add. Columns = lock-aware P(win) across the pod's lock-removal "
          f"rate r.\n  The lift is real only at low r (lock sticks) AND when availability is high "
          f"(tutored / multiple copies).")


SWEEP_LOCKS = ["Cursed Totem", "Drannith Magistrate", "Rule of Law",
               "Linvala, Keeper of Silence", "Opposition Agent"]
SWEEP_ABBR = {"Cursed Totem": "CursTot", "Drannith Magistrate": "Drannith",
              "Rule of Law": "RuleLaw", "Linvala, Keeper of Silence": "Linvala",
              "Opposition Agent": "OppAgent"}


_LOCK_LAB = None


def _lock_lab():
    """Load lock_lab + the oracle index/aliases ONCE and cache (the index is 176MB; reloading
    it per call dominates a sweep, so this lets a bake / repeated server requests reuse it).
    Read-only in the sweep. Cached per process — restart to pick up decklist edits."""
    global _LOCK_LAB
    if _LOCK_LAB is None:
        import importlib.util as _il
        spec = _il.spec_from_file_location("lock_lab", ROOT / "scripts" / "lock_lab.py")
        LL = _il.module_from_spec(spec); spec.loader.exec_module(LL)
        _LOCK_LAB = (LL, LL.ds.load_oracle_index(), LL.ds.load_reskin_aliases())
    return _LOCK_LAB


def lock_sweep_rows(a, r, strict, trials, seed, pod_fast=False, pod_slow=False):
    """Structured deck × lock P(win)-lift matrix — the single source of truth shared by the
    CLI table (run_lock_sweep) and the dashboard endpoint. Returns (rows, meta):
      rows = [{slug, name, cur, cells:[{piece, lift, owned}]}]  sorted by cur desc
      meta = {which, trials, a, r, locks, abbr}
    Tutored-availability ceiling, baseline r; cells are P(win) lift in POINTS."""
    LL, index, aliases = _lock_lab()
    t = min(trials, 8000)                      # O(decks x locks) measurement; cap for runtime
    C = {**merged_clocks(), **BUILD_CLOCKS}
    kdist = pod_kdist(SimpleNamespace(pod_fast=pod_fast, pod_slow=pod_slow))
    which = "table" if strict else "decap"
    rows = []
    for slug in [s for s in LL.DECKS if s in C]:
        if not (ROOT / LL.DECKS[slug]).is_file():    # tolerate stale/missing deck paths
            continue
        base = LL.load(slug, index, aliases)
        have = {n for n, _ in base}
        c = C[slug]
        F = build_cdf(c["grid"], c[which])
        cur = simulate(slug, F, a, kdist, t, random.Random(seed))[0]
        cells = []
        for piece in SWEEP_LOCKS:
            rec = index.get(piece.lower())
            lib = base if piece in have else base + [(piece, rec)]
            pkg = LL.inventory(lib)
            av, tau, _ = LL.measure(lib, pkg, t, random.Random(LL.SEED), use_tutors=True)
            ld = dict(grid=LL.GRID, hl_drawn=[av[x] for x in LL.GRID],
                      hl_tut=[av[x] for x in LL.GRID], tau=[tau[x] for x in LL.GRID],
                      e=LL.combined_e(pkg), tau_total=LL.total_tau(pkg))
            lk = lock_race(slug, F, ld, a, r, kdist, t, random.Random(seed), use_tut=True)
            cells.append(dict(piece=piece, lift=(lk - cur) * 100, owned=(piece in have)))
        rows.append(dict(slug=slug, name=c["name"], cur=cur, cells=cells))
    rows.sort(key=lambda x: -x["cur"])
    return rows, dict(which=which, trials=t, a=a, r=r,
                      locks=list(SWEEP_LOCKS), abbr=dict(SWEEP_ABBR))


def run_lock_sweep(args):
    """Full deck x lock lift matrix: what each persistent lock buys each deck vs the pod
    (tutored availability ceiling, baseline r). Cells = P(win) lift in points; '·' = <0.5pp.
    Answers 'what every lock buys every deck' in one process (vs 85 --add calls)."""
    rows, meta = lock_sweep_rows(args.a, args.r, args.strict, args.trials, args.seed,
                                 args.pod_fast, args.pod_slow)
    which, t = meta["which"], meta["trials"]
    print(f"\n{'='*100}\nLOCK SWEEP — P(win) lift per deck × lock   "
          f"[{which} · a={args.a} · r={args.r} · tutored avail · trials={t}]")
    print("  cell = points added vs the no-lock baseline (one-shot disruption). "
          "* = deck already runs it.\n")
    print("  " + "deck".ljust(24) + "cur".rjust(5)
          + "".join(SWEEP_ABBR[p].rjust(9) for p in SWEEP_LOCKS))
    for row in rows:
        line = "  " + row["name"][:24].ljust(24) + f"{row['cur']*100:>4.0f}%"
        for cell in row["cells"]:
            d, owned = cell["lift"], cell["owned"]
            s = f"+{d:.0f}" if d >= 0.5 else ("·" if d > -0.5 else f"{d:.0f}")
            line += (s + ("*" if owned else "")).rjust(9)
        print(line)
    print("\n  * deck already runs that lock (cell = its current value, not an add).")
    print("  Mana-tax (Sphere/Trinisphere) omitted: ≈0 for the whole roster (pod mana growth).")
    print("  Creature-tutor fetch of creature locks (Drannith/Linvala) not modelled -> those")
    print("  columns are FLOORS. Read: fast decks don't need locks (they race); lifts concentrate")
    print("  in mid-clock grind decks, and even there a singleton is bounded by avail × e × r.")


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--a", type=float, default=A_BASE, help="P(Abolisher out) baseline")
    ap.add_argument("--trials", type=int, default=40000)
    ap.add_argument("--seed", type=int, default=20260614)
    ap.add_argument("--strict", action="store_true",
                    help="race the TABLE clock (win the game) not decap (remove the threat)")
    ap.add_argument("--pod-fast", action="store_true", help="faster pod (K mass on T5-6)")
    ap.add_argument("--pod-slow", action="store_true", help="slower pod (K mass on T7-8)")
    ap.add_argument("--swapped", action="store_true",
                    help="current vs after-pending-swaps P(win) (Build_And_Swap §2)")
    ap.add_argument("--matrix", action="store_true",
                    help="emit lab-sourced quantitative rows for Pod_Matchup_Matrix.md")
    ap.add_argument("--vs", action="store_true",
                    help="race his TWO REAL decks (Acererak / Hidetsugu&Kairi / 5C tail) "
                         "separately + blended, with the interaction-against-us term")
    ap.add_argument("--pending", action="store_true",
                    help="fold pending BUILD_CLOCKS candidates (Kefka / Hashaton) into the "
                         "--vs / --matrix run so they can be placed in the matrix")
    ap.add_argument("--vs-lock", dest="vs_lock", action="store_true",
                    help="--vs + a loop-typed PERSISTENT lock for decks that run one (VS_LOCKS); "
                         "e.g. GD's Elesh Norn vs Acererak's ETB loop")
    ap.add_argument("--refresh", action="store_true",
                    help="re-run the clock labs, reparse curves, write the JSON")
    ap.add_argument("--out", metavar="PATH",
                    help="refresh: write to PATH instead of the canonical clocks JSON "
                         "(e.g. a scratch file for the plan-keep harvest, leaving the snapshot intact)")
    ap.add_argument("--lock", action="store_true",
                    help="lock-aware race: current vs + persistent-lock overlay (lock_lab.py)")
    ap.add_argument("--add", metavar="SLUG=PIECE",
                    help="what-if: inject a catalog static into a deck and race the lift "
                         "(e.g. 'calamity_tax=Cursed Totem')")
    ap.add_argument("--lock-sweep", action="store_true",
                    help="full deck × lock lift matrix (what every lock buys every deck)")
    ap.add_argument("--r", type=float, default=R_BASE,
                    help="P(pod removes our lock each of their turns) baseline")
    ap.add_argument("--pod-mana-growth", type=float, default=POD_MANA_GROWTH,
                    help="pod mana/turn for the mana-tax tau->Delta conversion")
    ap.add_argument("--use-lock-tutors", action="store_true",
                    help="use the with-tutors lock-availability ceiling instead of drawn-only")
    args = ap.parse_args()
    if args.refresh:
        refresh(args.trials, args.out)   # default 40k -> canonical; --out for scratch harvests
        return
    if args.lock_sweep:
        run_lock_sweep(args)
        return
    if args.add:
        run_lock_add(args)
        return
    if args.lock:
        run_lock(args)
        return
    if args.swapped:
        run_swapped(args)
        return
    if args.matrix:
        run_matrix(args)
        return
    if args.vs:
        run_vs(args)
        return
    if args.vs_lock:
        run_vs_lock(args)
        return
    run(args)


if __name__ == "__main__":
    main()
