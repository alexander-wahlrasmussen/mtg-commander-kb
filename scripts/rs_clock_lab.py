#!/usr/bin/env python3
"""rs_clock_lab.py — Radiation Sickness (The Wise Mothman) KILL-TURN goldfish.

Kill-Window Lab Sweep, deck 2 of 10 (proposals/Kill_Window_Lab_Sweep_2026-06-13.md).
Summary claims "Goldfish T6-9" with the front-edge T6 flagged suspect. Built on
speed_lab_core.py.

KILL SHAPE: RE-AUDITED 2026-06-23. The original framing below ("converge kills, table
driven by rad drain") was FALSIFIED by instrumenting which branch closes the table:
76% is incidental go-wide COMBAT (hit_focus, board), only ~14% the kill_all combo/Simic
and ~3% the rad drain. So decap (median T7) and table (median T10) do NOT converge — they
diverge ~3 turns like any combat deck, and the table clock is an UNBLOCKED creature-count-
DEPENDENT combat ceiling (fully blockable), not the robust converge clock once claimed. The
branch menu is still real; the *weighting* is combat-dominated. Branches:

  COMBO    Mindcrank + Bloodchief Ascension (active = 3 quest counters): any
           opponent life-loss -> Mindcrank mills -> cards to their graveyard ->
           Bloodchief drains 2 -> loops. kill_all when active.
  SIMIC    Simic Ascendancy: 20 growth counters at your upkeep = you win. kill_all.
  TRIUMPH  Triumph of the Hordes: your board gains +1/+1 + trample + INFECT;
           10 poison kills a player regardless of life. Wide board -> table.
  DRAIN    Rad counters tick every opponent's main phase (mill -> lose life per
           nonland), an all-opponent drain (Table.hit_all -> converge).
  COMBAT   Countered creatures swing (focus, decap-only fallback).

Engine spiral, oracle-verified (card_lookup.py 2026-06-13):
  * Mothman ({1}{B}{G}{U}, commander): ETB + attack -> each player a rad counter;
    each nonland-mill event -> +1/+1 on up to X creatures (X = nonland milled).
  * Bloodchief quest: +1 at an end step IF AN OPPONENT lost 2+ life that turn.
  * Tekuthal: proliferate twice. Doubling Season: counters on YOUR permanents x2
    (your +1/+1, growth, quest — NOT rad on players).
    (Vorinclex MR — the rad-on-players doubler — was cut 2026-06-22 for Timeless
    Witness, so vorx ≡ 1 below; its modeling was removed in the 06-23 retarget.)

HEURISTIC, not a rules engine — and the COARSEST lab in the sweep: the counter
spiral is tracked as expected-value floats (rad/growth/quest/board), opponent decks
assumed ~62% nonland (so milling R cards loses ~0.62R life and decays rad to ~0.38R),
Mindcrank's self-amplifying mill folded into a x1.8 life-loss factor, Mothman counter
placement = min(ncre, nonland milled) per turn. Mana = lands + rocks/dorks floor.
Proliferate events/turn = prolif perms online (x2 if Tekuthal), capped. Trust the
SHAPE and the front edge, not the second decimal. decap/table reported separately.

Data: collection/oracle-cards.json   ·   Writeup: proposals/Radiation_Sickness_Clock_Lab_2026-06-13.md
"""
import importlib.util
import random
from pathlib import Path

ROOT = Path(__file__).parent.parent
_spec = importlib.util.spec_from_file_location("speed_lab_core", Path(__file__).parent / "speed_lab_core.py")
slc = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(slc)
ds = slc.ds

DECK = ROOT / "decks" / "radiation-sickness-20260707.txt"   # retargeted 2026-07-07 (-Birds +Nightshade Dryad; fixing-neutral)
SEED = 20260613
TURNS = 14
SHOW = [5, 6, 7, 8, 9, 10, 12, 14]

NONLAND = 0.62          # opp deck nonland fraction (rad mills lose this much life, decay rest)
MINDCRANK_AMP = 1.8     # Mindcrank's self-mill loop multiplies opp life-loss

ROCKS = {"Sol Ring": (1, 2), "Arcane Signet": (2, 1), "Birds of Paradise": (1, 1),
         "Incubation Druid": (2, 1), "Bloom Tender": (2, 1)}
RAMP = {"Farseek": (2, 1), "Nature's Lore": (2, 1), "Three Visits": (2, 1)}
PROLIF_PERM = {"Inexorable Tide", "Evolution Sage", "Viral Drake", "Contagion Engine",
               "Sword of Truth and Justice"}
COMMANDER = "The Wise Mothman"


def _powmap(library, commander):
    names = [nm for nm, r in library if "creature" in r["type_line"].lower()]
    names.append(commander)
    raw = slc.load_powers(names)
    return {k: (v if isinstance(v, int) else 1) for k, v in raw.items()}


def poison_distribute(tbl, infect_total, T):
    """Triumph: 10 infect power kills one player (poison), regardless of life."""
    killable = int(infect_total // 10)
    for i in range(len(tbl.dmg)):
        if killable <= 0:
            break
        if tbl.dmg[i] < tbl.life:
            tbl.dmg[i] = tbl.life
            killable -= 1
    tbl._update(T)


def goldfish_kill(library, commander, index, powmap, rng, mills=False):
    def pw(nm):
        return powmap.get(nm.lower(), 1)

    g = slc.Goldfish(library, rng, rocks=ROCKS)
    tbl = slc.Table()
    mothman = tekuthal = doubling = seedborn = False
    mothman_turn = None              # turn Mothman entered; no haste, so it can't attack
    #                                  on its entry turn (gates the attack rad + combat power)
    simic = bloodchief = mindcrank = False
    ruin_crab = hedron_crab = altar = sidisi = False   # discrete mill producers (mills=True only)
    n_mult = 0                       # multiplicative creature-counter doublers (Branching/Corpsejack/DS)
    prolif = set()
    rad = 0.0                        # rad counters per opponent (symmetric)
    growth = quest = 0.0
    board = 0.0
    ncre = 0
    new_board = 0.0
    new_cre = 0

    def deploy(nm, rec):
        nonlocal tekuthal, doubling, seedborn, simic, bloodchief, mindcrank
        nonlocal n_mult, new_board, new_cre, rad
        nonlocal ruin_crab, hedron_crab, altar, sidisi
        low = nm
        if nm == "Tekuthal, Inquiry Dominus":
            tekuthal = True
        elif nm == "Doubling Season":
            doubling = True; n_mult_inc()
        elif nm in ("Branching Evolution", "Corpsejack Menace"):
            n_mult_inc()
        elif nm == "Seedborn Muse":
            seedborn = True
        elif nm == "Simic Ascendancy":
            simic = True
        elif nm == "Bloodchief Ascension":
            bloodchief = True
        elif nm == "Mindcrank":
            mindcrank = True
        elif nm in PROLIF_PERM:
            prolif.add(nm)
        elif nm == "Ruin Crab":
            ruin_crab = True
        elif nm == "Hedron Crab":
            hedron_crab = True
        elif nm == "Altar of the Brood":
            altar = True
        elif nm == "Sidisi, Brood Tyrant":
            sidisi = True
        if "creature" in rec["type_line"].lower():
            new_board += pw(nm); new_cre += 1

    def n_mult_inc():
        nonlocal n_mult
        n_mult += 1

    for T in range(1, TURNS + 1):
        board += new_board; ncre += new_cre; new_board = 0.0; new_cre = 0
        g.begin_turn(T)
        g.deploy_rocks()
        for rs, (cost, n) in RAMP.items():
            while g.has(rs) and g.avail >= cost:
                g.cast(rs, cost); g.lands += n; g.avail += n

        # commander: Mothman for 4 (ETB rad). No haste — it joins the board through
        # new_board/new_cre (online next turn) like every other creature here, so it
        # can't swing the turn it enters. The ETB rad still fires this turn.
        vorx = 1   # Vorinclex (rad/counter doubler) cut 2026-06-22 — no doubler left in deck
        if not mothman and g.avail >= 4:
            g.avail -= 4; mothman = True; mothman_turn = T
            new_board += 3; new_cre += 1
            rad += 1 * vorx
        # Vampiric Tutor: complete the combo or fetch Mothman-enabler
        if g.has("Vampiric Tutor") and g.avail >= 1:
            want = None
            if mindcrank and bloodchief:
                pass
            elif mindcrank and not bloodchief:
                want = "Bloodchief Ascension"
            elif bloodchief and not mindcrank:
                want = "Mindcrank"
            elif not simic:
                want = "Simic Ascendancy"
            if want and not g.has(want) and g.fetch(want):
                g.cast("Vampiric Tutor", 1)
        # deploy engine pieces / creatures cheapest-first
        more = True
        while more:
            more = False
            cands = sorted(((i, r["cmc"], nm) for i, (nm, r) in enumerate(g.hand)
                            if nm != "Vampiric Tutor" and nm not in ROCKS and nm not in RAMP
                            and not ds.is_land(r)
                            and (nm in PROLIF_PERM or "creature" in r["type_line"].lower()
                                 or nm in ("Doubling Season", "Branching Evolution",
                                           "Simic Ascendancy", "Bloodchief Ascension", "Mindcrank")
                                 or (mills and nm == "Altar of the Brood"))),
                           key=lambda x: x[1])
            for i, cmc, nm in cands:
                if g.avail >= cmc:
                    rec = g.hand[i][1]; g.hand.pop(i); g.avail -= cmc
                    deploy(nm, rec); more = True
                    break

        vorx = 1   # Vorinclex (rad/counter doubler) cut 2026-06-22 — no doubler left in deck
        m_perm = (2 if doubling else 1) * vorx
        m_cre = vorx * (2 ** min(3, n_mult)) if n_mult else vorx

        # Mothman attack rad — only once it can actually attack, i.e. it entered on a
        # PRIOR turn (no haste). The ETB rad already fired the turn it entered; the old
        # `T > 1` proxy let a freshly-cast Mothman swing the same turn (2026-06-29 audit).
        if mothman and mothman_turn is not None and T > mothman_turn:
            rad += 1 * vorx

        # proliferate step
        pevents = len(prolif)
        if tekuthal:
            pevents *= 2
        if seedborn:
            pevents += len(prolif & {"Viral Drake", "Contagion Engine"})
        pevents = min(pevents, 6)
        for _ in range(pevents):
            rad += vorx
            if growth >= 1 or (simic and ncre):
                growth += m_perm
            if bloodchief and quest >= 1:
                quest += m_perm
            if ncre:
                board += ncre * m_cre

        # Mothman mill->counter from opponents milling nonland this turn cycle
        life_each = rad * NONLAND
        if mindcrank and bloodchief:
            # MINDCRANK_AMP models the Mindcrank+Bloodchief Ascension feedback
            # (life loss -> mill -> yard -> Bloodchief drain -> more life loss).
            # Mindcrank ALONE only converts life loss to mill; it does not amplify
            # the life loss, so the amp requires both halves (2026-07-02 audit).
            life_each *= MINDCRANK_AMP
        nonland_milled = 3 * life_each
        if mothman and ncre:
            placed = min(ncre, nonland_milled)
            board += placed * m_cre
            if simic:
                growth += placed * m_perm
        # discrete mill producers -> extra Mothman counter-fuel (mills=True only).
        # These are separate mill EVENTS (your-turn landfall / ETB / attack), each its
        # own Mothman trigger, so not double-counting the rad mill above. Models the
        # un-modelled-producer caveat from the 2026-06-13 rs producer re-check.
        if mills and mothman and ncre:
            extra = 0.0
            if ruin_crab:          extra += 3        # landfall mill 3, ~1 land/turn
            if hedron_crab:        extra += 3        # landfall mill 3 (proposed add)
            if altar:              extra += 1.5      # ~perm-ETB/turn, mills each opp 1
            if sidisi and T > 1:   extra += 3        # ETB + attack self-mill 3 (proposed add)
            en = extra * NONLAND
            placed_x = min(ncre, en)
            board += placed_x * m_cre
            if simic:
                growth += placed_x * m_perm
            if sidisi and T > 1:                     # zombies off creature cards self-milled (~18%)
                board += 3 * 0.18 * m_cre
        # quest accrual: opponents losing 2+ life
        if bloodchief and life_each >= 2:
            quest += m_perm   # Bloodchief gains ONE quest counter / upkeep (×m_perm under
            #                   Doubling Season); the old `*2 if quest>=1` doubled the accrual
            #                   RATE with no card backing it (bug fix 2026-06-23)

        # opponent drain (rad life loss) — all-opponent, converge
        if life_each > 0:
            tbl.hit_all(life_each, T)
        rad *= (1 - NONLAND)        # nonland milled removes rad; lands persist

        # ---- KILL CHECKS (converge lines first) --------------------------------
        if mindcrank and bloodchief and quest >= 3:
            tbl.kill_all(T)
        elif simic and growth >= 20:
            tbl.kill_all(T)
        elif g.has("Triumph of the Hordes") and g.avail >= 4 and ncre >= 1 \
                and (board + ncre) >= 10:
            g.cast("Triumph of the Hordes", 4)
            poison_distribute(tbl, board + ncre, T)
        elif board >= 1:
            tbl.hit_focus(board, T)        # combat decap (rad already drained table)
        if tbl.done:
            return tbl.decap, tbl.table

    return tbl.decap, tbl.table


def mode_clock(index, aliases, trials):
    print(f"\n### CLOCK — Radiation Sickness kill-turn goldfish   trials={trials} seed={SEED}")
    print("    decap = first opponent dead (40) · table = all three. RE-AUDIT 2026-06-23:")
    print("    table close is ~76% go-wide COMBAT (board), only ~14% kill_all combo/Simic +")
    print("    ~3% rad drain — an UNBLOCKED, blockable combat ceiling, NOT a converge clock.\n")
    library, commander = slc.load_parsed(DECK, index, aliases)
    powmap = _powmap(library, commander)
    rng = random.Random(SEED)
    res = [goldfish_kill(library, commander, index, powmap, rng) for _ in range(trials)]

    slc.report_clock(res, SHOW, TURNS, trials)
    print("\n  Claimed in Summary: Goldfish T6-9. Front-edge T6 odds above are the test.")


# The 2026-06-13 GC-fix upgrade (−Survival/+Sylvan Library, −Generous Patron/+Hedron Crab,
# −Guardian Project/+Sidisi, Brood Tyrant) was APPLIED to the committed list 2026-06-15, so
# DECK above already IS the fixed deck — `mode_clock` now goldfishes it directly (Hedron Crab
# and Sidisi auto-activate via the mills=True producer flags). The former `--mode upgrade` A/B
# is retired; the original comparison lives in proposals/Radiation_Sickness_Upgrade_2026-06-13.md.


if __name__ == "__main__":
    slc.run_cli(__doc__, {"clock": mode_clock}, default_trials=40000)
