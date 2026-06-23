#!/usr/bin/env python3
"""gd_clock_lab.py — The Grand Design (Atraxa) KILL-TURN goldfish.

Closes the gap flagged in proposals/Framework_Clock_Gap_2026-06-09.md §5: the
Summary's "Goldfish T6-8" was never goldfished. gd_speed_lab.py measured kill-piece
*availability* (P(Finale drawn by T)), the Speed-Curve analysis measured the mana
curve — neither measured *what turn the deck actually kills*. This does, the same
way rc/er_speed_lab did for their combat decks: a per-trial goldfish that develops
a board and records the decap turn (first opponent dead) and table turn (all three).

Built on speed_lab_core.py (the shared harness extracted 2026-06-10). The deck's
two real kill axes, verified against card_lookup.py oracle text:

  FINALE   Finale of Devastation {X}{G}{G}. ONLY a finisher at X>=10 (= 12 mana):
           creatures you control get +X/+X and gain haste. It is a SORCERY, so the
           creature-tutor suite cannot fetch it — modelled DRAWN-ONLY. The burst
           is checked while mana is still unspent (the optimal line holds up 12).

  BOARD    Reanimator/combat beatdown. Buried Alive deterministically bins the fat
           targets (Razaketh/Vilis, P8); a reanimate spell + a fat in yard cheats
           ~8 power onto the board for 1-3 mana. Atraxa (P7, ETB draws 5) and the
           rest of the creature suite are hard-cast cheapest-first. Unblocked
           goldfish (same convention as rc/er): decap at 40 power, table at 120.

Each turn the deck takes whichever kill (Finale burst or combat) lands first.

HEURISTIC, not a rules engine. Mana = lands + rocks/dorks + land-ramp spells (a
floor; Bloom Tender counted optimistically at 1, board-conditionality ignored).
Damage is unblocked. Buried Alive's binned fats are tracked as reanimation fuel
without being pulled from the library (a small double-count optimism). Trust the
shape and the front edge, not the second decimal. Per the verification rule, decap
and table are reported separately.

Data: collection/oracle-cards.json (refresh via update_scryfall_data.py)
Writeup: proposals/Grand_Design_Speed_Curve_Analysis.md (clock addendum)
"""
import importlib.util
import random
from pathlib import Path

ROOT = Path(__file__).parent.parent
_spec = importlib.util.spec_from_file_location("speed_lab_core", Path(__file__).parent / "speed_lab_core.py")
slc = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(slc)
ds = slc.ds

# LIVE = the current committed deck (mode_clock — this is what pod_gauntlet --refresh harvests).
# BASELINE = the pre-swap list (archived 2026-06-23); the swap-comparison / sensitivity modes
# (ramp / userpkg / levers / video) build their variants ON it, so it must stay reachable.
LIVE = ROOT / "decks" / "the-grand-design-20260623.txt"
BASELINE = ROOT / "archive" / "old_decklists" / "the-grand-design-20260502.txt"
SEED = 12345
TURNS = 12
SHOW = [4, 5, 6, 7, 8, 9, 10, 12]

DECAP, TABLE = 40, 120          # unblocked thresholds: one player / whole table

# fixed mana producers the scaffold deploys as rocks: name -> (cost, output)
ROCKS = {"Sol Ring": (1, 2), "Arcane Signet": (2, 1), "Birds of Paradise": (1, 1),
         # ramp-upgrade package (variant only): 4c rock + 4c dork (Faeburrow ~3 in WUBG)
         "Coalition Relic": (3, 1), "Faeburrow Elder": (3, 2)}
# Bloom Tender is handled manually: it taps for one mana PER COLOUR among your
# permanents, so it floors at ~2 (Birds + a coloured creature) and jumps to 4
# once Atraxa (WUBG) is out — the single biggest swing toward a 12-mana Finale.
# land-ramp spells: cost -> +1 untapped land (taps this turn; conservative)
RAMP = {"Nature's Lore": 2, "Three Visits": 2, "Farseek": 2,
        # ramp-upgrade package (only present in the --mode ramp/userpkg variant libraries):
        "Sakura-Tribe Elder": 2, "Wood Elves": 3, "Cultivate": 3, "Solemn Simulacrum": 4,
        # Kodama's Reach: fetch-2-basics, modelled like Cultivate (+1 land @3). CONSERVATIVE
        # -- the real card also puts a 2nd land to HAND (anti-flood / land-drop insurance),
        # which this +1 model does NOT credit, so Kodama's true value is >= what it shows.
        "Kodama's Reach": 3,
        # Springbloom Druid {2}{G}: sac a land, fetch 2 basics -> net +1 land (tapped). Owned
        # substitute for Wood Elves; same +1 @3. Model can't see tapped-entry / sac-a-land /
        # basics-vs-duals -- all marginal, all slightly favour Wood Elves. Parity check below.
        "Springbloom Druid": 3}
# reanimate spells (cheapest first): cheat a fat creature from yard onto the board
REANIM = [("Reanimate", 1), ("Animate Dead", 2), ("Persist", 2), ("Necromancy", 3),
          ("Victimize", 3), ("Dread Return", 4), ("Living Death", 5)]
FAT = ["Razaketh, the Foulblooded", "Vilis, Broker of Blood"]   # Buried Alive bins these


def _powmap(library, commander):
    names = [nm for nm, r in library if "creature" in r["type_line"].lower()]
    names.append(commander)
    raw = slc.load_powers(names)
    return {k: (v if isinstance(v, int) else 1) for k, v in raw.items()}


# ---------------------------------------------------------------------------
# Atraxa selection model (the 2026-06-13 sensitivity, per the Glarb dig lesson)
# ---------------------------------------------------------------------------
# Real Atraxa: reveal top 10, take the best card of EACH card type into hand,
# bottom the rest. The base lab modelled this as a flat one-time g.draw(5). This
# adds: (1) best-per-type SELECTION, (2) REPEAT ETBs via the deck's flicker shell
# (Restoration Angel / Ghostly Flicker / Soulherder / Thassa / Ephemerate /
# Displacer Kitten), (3) Panharmonicon DOUBLING each ETB.
TYPES = ("creature", "sorcery", "instant", "enchantment", "artifact",
         "planeswalker", "land", "battle")
FLICKER = {"Restoration Angel", "Ghostly Flicker", "Soulherder",
           "Thassa, Deep-Dwelling", "Ephemerate", "Displacer Kitten"}
ATRAXA_PRI = {  # kill-relevance for "take the best of each type"
    "Finale of Devastation": 100, "Craterhoof Behemoth": 100,
    "Reanimate": 95, "Animate Dead": 92, "Necromancy": 90, "Victimize": 88,
    "Persist": 88, "Dread Return": 85, "Living Death": 84, "Buried Alive": 91,
    "Grisly Salvage": 80, "Razaketh, the Foulblooded": 86,
    "Vilis, Broker of Blood": 86, "Sol Ring": 80, "Bloom Tender": 76,
    "Birds of Paradise": 72, "Nature's Lore": 66, "Three Visits": 66,
    "Farseek": 66, "Arcane Signet": 60, "Panharmonicon": 82,
    "Restoration Angel": 74, "Ghostly Flicker": 72, "Soulherder": 70,
    "Thassa, Deep-Dwelling": 70, "Ephemerate": 68, "Displacer Kitten": 68,
}


def _ctypes(rec):
    tl = rec["type_line"].lower()
    return {t for t in TYPES if t in tl}


def _pri(nm, rec, powmap):
    if nm in ATRAXA_PRI:
        return ATRAXA_PRI[nm]
    if "creature" in rec["type_line"].lower():
        return 35 + powmap.get(nm.lower(), 1)
    if "land" in rec["type_line"].lower():
        return 10
    return 25


def _atraxa_etb(g, powmap, doublings):
    """Reveal top 10, take the best card of each type to hand, bottom the rest.
    doublings>1 = Panharmonicon (repeat the reveal-and-take that many times)."""
    for _ in range(doublings):
        window = g.deck[g.ptr:g.ptr + 10]
        if not window:
            return
        del g.deck[g.ptr:g.ptr + 10]
        covered, chosen = set(), []
        for nm, rec in sorted(window, key=lambda x: -_pri(x[0], x[1], powmap)):
            ts = _ctypes(rec)
            if ts and (ts - covered):
                chosen.append((nm, rec)); covered |= ts
        for c in chosen:
            g.hand.append(c)
        g.deck.extend(c for c in window if c not in chosen)   # bottom the rest


def _cantrip(g, powmap):
    """Ponder / Preordain proxy (the BDD / Surf City 'smoothener'): look at the top 3,
    draw the most kill-relevant one (same _pri ranking Atraxa uses) to hand, leave the
    other two on top. Card-neutral (the cantrip replaced itself) — it does NOT add card
    advantage; it digs toward ramp / Atraxa / a finisher. Mana-gated decks should barely
    move; finding-gated decks should tighten. That contrast is the whole test."""
    window = list(enumerate(g.deck[g.ptr:g.ptr + 3]))
    if not window:
        return
    i_rel, best = max(window, key=lambda iv: _pri(iv[1][0], iv[1][1], powmap))
    del g.deck[g.ptr + i_rel]
    g.hand.append(best)


def goldfish_kill(library, commander, index, powmap, rng, cfg=None):
    """One trial -> (decap, table). cfg toggles the Atraxa-selection sensitivity +
    build levers; cfg=None reproduces the original published model (flat draw-5)."""
    cfg = cfg or {}
    select = cfg.get("select", False)        # Atraxa reveal-10 best-per-type
    repeat = cfg.get("repeat", False)        # flicker re-triggers Atraxa each turn
    hand_cap = cfg.get("hand_cap", None)     # None = no max hand size (current default)
    extra_ramp = cfg.get("extra_ramp", 0)    # +N mana/turn (more-ramp lever)
    crater = cfg.get("craterhoof", False)    # creature finisher present (library swap)

    def pw(nm):
        return powmap.get(nm.lower(), 1)

    g = slc.Goldfish(library, rng, rocks=ROCKS)
    tbl = slc.Table()
    board = ncre = 0
    yard_fat = []
    atraxa = bloom = fanatic = have_big = False   # have_big = a power-4+ creature is in play
    protect_set = cfg.get("protect_set")     # names of "your-turn lock" protection pieces
    protect_turn = None                      # earliest turn one is in hand (pre-development)

    for T in range(1, TURNS + 1):
        g.begin_turn(T)
        g.deploy_rocks()
        if extra_ramp:
            g.add_mana(extra_ramp)
        for rs, cost in RAMP.items():
            while g.has(rs) and g.avail >= cost:
                g.cast(rs, cost); g.lands += 1; g.avail += 1
        if not bloom and g.has("Bloom Tender") and g.avail >= 2:
            g.cast("Bloom Tender", 2); bloom = True
        if bloom:
            g.avail += 4 if atraxa else 2
        # Fanatic of Rhonas {1}{G}: taps for G, or GGGG with a power-4+ creature out
        # (Atraxa / any reanimated fat turns Ferocious on). GREEN-only -- the generic-mana
        # model can't see that fixing limit; flag it in the writeup, not the number. Modelled
        # parallel to Bloom (taps the turn it lands, same optimism as every dork here).
        if not fanatic and g.has("Fanatic of Rhonas") and g.avail >= 2:
            g.cast("Fanatic of Rhonas", 2); fanatic = True; ncre += 1; board += 1
        if fanatic:
            g.avail += 4 if have_big else 1

        # cheap selection (Ponder/Preordain) — pay 1 to dig the best of the top 3 toward
        # ramp/Atraxa/finisher. cfg-gated (other modes unaffected). Competes with early
        # development for mana, so the tempo cost is modelled, not just the dig upside.
        if cfg.get("cantrips"):
            for cn in ("Ponder", "Preordain"):
                while g.has(cn) and g.avail >= 1:
                    g.cast(cn, 1)
                    _cantrip(g, powmap)

        # repeat Atraxa ETB via flicker (once Atraxa is out) — Panharmonicon doubles
        if atraxa and repeat and g.avail >= 2 and (FLICKER & {nm for nm, _ in g.hand}):
            g.avail -= 2
            _atraxa_etb(g, powmap, 2 if g.has("Panharmonicon") else 1)

        # protect-the-kill: record the first turn a your-turn lock is in hand at the start
        # of the turn (after draw/cantrip/repeat-ETB, before development). Conservative by
        # ~1 turn for a lock grabbed via Atraxa's FIRST ETB this same turn (that fires in
        # development below). Availability only — it ignores mana to cast it (see mode_video).
        if protect_set and protect_turn is None and (protect_set & {nm for nm, _ in g.hand}):
            protect_turn = T

        # --- attack step: Finale / Craterhoof alpha, else standing board swings ---
        fired = False
        if g.has("Finale of Devastation") and g.avail >= 12 and ncre >= 1:
            X = g.avail - 2
            if X >= 10:
                tbl.hit_focus(board + (ncre + 1) * X + 8, T)
                board += 8; ncre += 1; fired = True
        if not fired and crater and g.has("Craterhoof Behemoth") and g.avail >= 8 and ncre >= 1:
            atk = ncre + 1                              # haste; everyone +ncre+1/+ncre+1
            tbl.hit_focus(board + 5 + (ncre + 1) * atk, T)   # base + Craterhoof 5 + pump
            board += 5; ncre += 1; fired = True; have_big = True
        if not fired and board > 0:
            tbl.hit_focus(board, T)
        if tbl.done:
            if protect_set is not None:
                cfg.setdefault("protect_out", []).append(protect_turn)
            return tbl.decap, tbl.table

        # --- develop ---
        if not fired:
            if g.has("Buried Alive") and g.avail >= 3:
                g.cast("Buried Alive", 3); yard_fat += [8, 8]
            if g.has("Grisly Salvage") and g.avail >= 2:
                g.cast("Grisly Salvage", 2)
                for nm in g.mill(5):
                    rec = index.get(nm.lower())
                    if rec and "creature" in rec["type_line"].lower():
                        yard_fat.append(pw(nm))
            for rn, cost in REANIM:
                while yard_fat and g.has(rn) and g.avail >= cost:
                    g.cast(rn, cost)
                    board += max(yard_fat); ncre += 1; yard_fat.remove(max(yard_fat))
                    have_big = True                      # fats are power 8 -> Ferocious on
            if not atraxa and g.avail >= 7:
                board += pw(commander); ncre += 1; atraxa = True; have_big = True
                g.avail -= 7
                if select:
                    _atraxa_etb(g, powmap, 2 if g.has("Panharmonicon") else 1)
                else:
                    g.draw(5)                            # original flat model
            # Rune-Scarred Demon: ETB tutor ANY card -> grab the biggest finisher you
            # lack (incl. Finale, which creature-tutors can't get). A 6/6 body too.
            if cfg.get("rune") and g.has("Rune-Scarred Demon") and g.avail >= 7:
                g.cast("Rune-Scarred Demon", 7); board += pw("Rune-Scarred Demon"); ncre += 1
                have_big = True
                for want in ("Finale of Devastation", "Craterhoof Behemoth"):
                    if not g.has(want) and g.fetch(want):
                        break
            # Grim Tutor {1}{B}{B}: find ANY card -> hand at 3 mana (vs Rune's 7). Grabs the
            # finisher you lack so the crater/Finale line is guaranteed; no body (the trade vs
            # Rune). Prefer Craterhoof (8-mana, deployable sooner than 12-mana Finale).
            if cfg.get("grim") and g.has("Grim Tutor") and g.avail >= 3:
                g.cast("Grim Tutor", 3)
                for want in ("Craterhoof Behemoth", "Finale of Devastation"):
                    if not g.has(want) and g.fetch(want):
                        break
            more = True
            while more:
                more = False
                cands = sorted(((i, r["cmc"], nm) for i, (nm, r) in enumerate(g.hand)
                                if "creature" in r["type_line"].lower()), key=lambda x: x[1])
                for i, cmc, nm in cands:
                    if g.avail >= cmc:
                        g.cast(nm, cmc); board += pw(nm); ncre += 1; more = True
                        if pw(nm) >= 4:
                            have_big = True
                        break

        # --- end of turn: discard to hand size (None = no max). Discarded fats
        #     fall to the yard = reanimation fuel (so the cap isn't pure downside). ---
        if hand_cap is not None and len(g.hand) > hand_cap:
            ranked = sorted(range(len(g.hand)),
                            key=lambda i: _pri(g.hand[i][0], g.hand[i][1], powmap))
            for i in ranked[:len(g.hand) - hand_cap]:
                nm, rec = g.hand[i]
                if "creature" in rec["type_line"].lower() and pw(nm) >= 5:
                    yard_fat.append(pw(nm))
            keep = set(ranked[len(g.hand) - hand_cap:])
            g.hand = [g.hand[i] for i in sorted(keep)]

    if protect_set is not None:
        cfg.setdefault("protect_out", []).append(protect_turn)
    return tbl.decap, tbl.table


def _run(library, commander, index, powmap, trials, cfg):
    rng = random.Random(SEED)
    return [goldfish_kill(library, commander, index, powmap, rng, cfg) for _ in range(trials)]


def mode_clock(index, aliases, trials):
    print(f"\n### CLOCK — Grand Design kill-turn goldfish   trials={trials} seed={SEED}")
    print("    decap = first opponent dead (40) · table = all three (120), unblocked.")
    print("    Finale burst (X>=10, drawn-only) vs reanimator/combat board, earliest wins.")
    print("    LIVE deck (2026-06-23 swap applied): Craterhoof is in, so the crater finisher is ON.\n")
    library, commander = slc.load_parsed(LIVE, index, aliases)
    powmap = _powmap(library, commander)
    res = _run(library, commander, index, powmap, trials, {"craterhoof": True})
    slc.report_clock(res, SHOW, TURNS, trials)


def mode_levers(index, aliases, trials):
    print(f"\n### LEVERS — Atraxa-selection sensitivity + build levers   trials={trials} seed={SEED}")
    print("    Tests whether modelling Atraxa's reveal-10 selection (the Glarb lesson) +")
    print("    build levers move GD's clock. decap = first opp dead.\n")
    library, commander = slc.load_parsed(BASELINE, index, aliases)
    powmap = _powmap(library, commander)
    crater_lib = slc.build_lib(library, index, ["Finale of Devastation"], ["Craterhoof Behemoth"])
    full = {"select": True, "repeat": True}
    rows = [
        ("baseline (flat draw-5, no cap)", library, None),
        ("+Atraxa select-10 (best/type)", library, {"select": True}),
        ("+repeat ETBs (flicker/Panharm)", library, full),
        ("  ^ + hand cap 7 (realistic)", library, {**full, "hand_cap": 7}),
        ("  ^ + MORE RAMP (+2 mana/turn)", library, {**full, "extra_ramp": 2}),
        ("  ^ + CRATERHOOF (-Finale)", crater_lib, {**full, "craterhoof": True}),
    ]
    print("  variant".ljust(38) + "".join(f"{t:>6}" for t in SHOW) + "   median   never12")
    for tag, lib, cfg in rows:
        res = _run(lib, commander, index, powmap, trials, cfg)
        nd = 100.0 * sum(1 for d, _ in res if d is None) / trials
        print(slc.row(tag, slc.cum(res, 0, SHOW), SHOW)
              + f"   {slc.median(res, 0):>5}   {nd:4.0f}%")
    print("\n  Read: baseline vs +select/+repeat = the Atraxa under-model cost; the indented")
    print("  rows are levers ON the full Atraxa model (hand-cap delta = value of no-max-hand).")


RAMP_CUTS = ["Carpet of Flowers", "Veil of Summer", "Flawless Maneuver",
             "Dovin's Veto", "Grand Abolisher"]
RAMP_ADDS = ["Solemn Simulacrum", "Sakura-Tribe Elder", "Wood Elves",
             "Faeburrow Elder", "Coalition Relic"]


def mode_ramp(index, aliases, trials):
    print(f"\n### RAMP — proposed 5-for-5 ramp upgrade vs baseline   trials={trials} seed={SEED}")
    print("    Same kill model for both (cfg=None) so the delta is purely the ramp package.")
    print(f"    OUT: {', '.join(RAMP_CUTS)}")
    print(f"    IN : {', '.join(RAMP_ADDS)}\n")
    base, commander = slc.load_parsed(BASELINE, index, aliases)
    ramp_lib = slc.build_lib(base, index, RAMP_CUTS, RAMP_ADDS)
    # combined: ramp package + Craterhoof (cut Displacer Kitten for it; Finale STAYS,
    # so the deck has two finisher types — the fragility fix the lever test motivates).
    combo_lib = slc.build_lib(base, index, RAMP_CUTS + ["Displacer Kitten"],
                              RAMP_ADDS + ["Craterhoof Behemoth"])
    rune_lib = slc.build_lib(base, index, RAMP_CUTS + ["Displacer Kitten", "Heroic Intervention"],
                             RAMP_ADDS + ["Craterhoof Behemoth", "Rune-Scarred Demon"])
    print("  build".ljust(38) + "".join(f"{t:>6}" for t in SHOW) + "   median   never12")
    for tag, lib, cfg in (("baseline GD", base, None),
                          ("+ramp package (5-for-5)", ramp_lib, None),
                          ("+ramp +Craterhoof (keep Finale)", combo_lib, {"craterhoof": True}),
                          ("  ^ +Rune-Scarred (tutor finisher)", rune_lib,
                           {"craterhoof": True, "rune": True})):
        powmap = _powmap(lib, commander)
        res = _run(lib, commander, index, powmap, trials, cfg)
        nd = 100.0 * sum(1 for d, _ in res if d is None) / trials
        print(slc.row(tag, slc.cum(res, 0, SHOW), SHOW)
              + f"   {slc.median(res, 0):>5}   {nd:4.0f}%")
    print("\n  (ramp adds modelled: Sakura/Wood Elves/Cultivate/Solemn = +1 land; Coalition")
    print("   Relic = rock(3,1); Faeburrow Elder = 4c dork(3,2). Tapped-land entry optimism noted.)")


# ---------------------------------------------------------------------------
# mode_userpkg — 2026-06-23 follow-up: the user accepted the proposal's direction
# but asked whether the 7th-slot picks are the best AVAILABLE. Two edits to the
# canonical 7-for-7 (same 7 cuts):
#   (i)  Faeburrow Elder -> "more ramp": Kodama's Reach (reliable, wrath-proof,
#        owned x5) vs Fanatic of Rhonas (conditional GGGG dork, owned x1) -- both
#        tested for the ramp slot.
#   (ii) Rune-Scarred Demon (7-mana, ~1pp in mode_ramp) -> Grim Tutor (3-mana
#        any-card tutor, owned $0) for the finisher-insurance slot.
# Writeup: proposals/Grand_Design_Upgrade_2026-06-13.md
# ---------------------------------------------------------------------------
USER_CUTS = RAMP_CUTS + ["Displacer Kitten", "Heroic Intervention"]   # the proposal's 7 cuts
USER_COMMON = ["Solemn Simulacrum", "Sakura-Tribe Elder", "Wood Elves",
               "Coalition Relic", "Craterhoof Behemoth", "Grim Tutor"]  # 6 shared adds


def mode_userpkg(index, aliases, trials):
    print(f"\n### USERPKG — 'more ramp + Grim Tutor' vs the full proposal   trials={trials} seed={SEED}")
    print("    Same 7 cuts in every variant. 7th slot under test (ramp) + Rune->Grim.")
    print(f"    cuts: {', '.join(USER_CUTS)}")
    print("    full proposal IN : ...Faeburrow Elder + Rune-Scarred Demon")
    print("    Kodama's   IN    : ...Kodama's Reach   + Grim Tutor")
    print("    Fanatic    IN    : ...Fanatic of Rhonas + Grim Tutor\n")
    base, commander = slc.load_parsed(BASELINE, index, aliases)
    full_lib = slc.build_lib(base, index, USER_CUTS,
                             RAMP_ADDS + ["Craterhoof Behemoth", "Rune-Scarred Demon"])
    kod_lib = slc.build_lib(base, index, USER_CUTS, USER_COMMON + ["Kodama's Reach"])
    fan_lib = slc.build_lib(base, index, USER_CUTS, USER_COMMON + ["Fanatic of Rhonas"])
    # CHOSEN 2026-06-23 (7-for-7): BOTH ramp pieces, no Grim (-> kept for a combo deck).
    # Craterhoof is the tutorable finisher, so Finale's un-tutorability stops mattering;
    # Grim's finisher-insurance is redundant. No 7th-slot tutor at all.
    chosen_lib = slc.build_lib(base, index, USER_CUTS,
                               ["Solemn Simulacrum", "Sakura-Tribe Elder", "Wood Elves",
                                "Coalition Relic", "Craterhoof Behemoth",
                                "Kodama's Reach", "Fanatic of Rhonas"])
    # 2026-06-23: keep the build 100% owned -> Wood Elves ($1 buy) -> Springbloom Druid
    # (owned x2, free). Same ETB-land-fetch creature role, modelled identically (+1 @3).
    spring_lib = slc.build_lib(base, index, USER_CUTS,
                               ["Solemn Simulacrum", "Sakura-Tribe Elder", "Springbloom Druid",
                                "Coalition Relic", "Craterhoof Behemoth",
                                "Kodama's Reach", "Fanatic of Rhonas"])
    print("  build".ljust(40) + "".join(f"{t:>6}" for t in SHOW) + "   median   never12")
    for tag, lib, cfg in (
            ("baseline GD", base, None),
            ("full proposal (Faeburrow + Rune)", full_lib, {"craterhoof": True, "rune": True}),
            ("more-ramp Kodama's + Grim", kod_lib, {"craterhoof": True, "grim": True}),
            ("Fanatic of Rhonas + Grim", fan_lib, {"craterhoof": True, "grim": True}),
            ("CHOSEN: w/ Wood Elves ($1)", chosen_lib, {"craterhoof": True}),
            ("CHOSEN: w/ Springbloom (all owned)", spring_lib, {"craterhoof": True})):
        powmap = _powmap(lib, commander)
        res = _run(lib, commander, index, powmap, trials, cfg)
        nd = 100.0 * sum(1 for d, _ in res if d is None) / trials
        print(slc.row(tag, slc.cum(res, 0, SHOW), SHOW)
              + f"   {slc.median(res, 0):>5}   {nd:4.0f}%")
    print("\n  Caveats: mana is GENERIC here, so Fanatic's green-only output and Kodama's basic-")
    print("  fixing are both invisible (helps Fanatic, hurts Kodama's -> read fixing off-model).")
    print("  Kodama's 2nd land (to hand) is uncredited. Grim/Rune both guarantee a finisher; the")
    print("  gap is cost (3 vs 7 mana) + Rune's 6/6 body. Trust the shape, not the 2nd decimal.")


# ---------------------------------------------------------------------------
# mode_video — the two levers the Surf City "Atraxa Coaching #12" deck suggests:
#   (A) cantrip "smootheners" (Ponder/Preordain) — does cheap selection move a
#       deck our prior labs called MANA-gated, not finding-gated?
#   (B) Tidal Barracuda as a your-turn lock — protection AVAILABILITY by the kill
#       turn (the only Barracuda question a goldfish can honestly answer).
# Writeup: analysis/Surf_City_Atraxa_Coaching_vs_Grand_Design_2026-06-19.md
# ---------------------------------------------------------------------------
CANTRIP_CUTS = ["Dovin's Veto", "Swan Song"]            # cheap counters the kill-goldfish ignores
LOCK_BASE = ["Grand Abolisher", "Teferi, Time Raveler"]  # your-turn locks GD already runs


def _whiff(res, trials):
    return 100.0 * sum(1 for d, _ in res if d is None) / trials


def mode_video(index, aliases, trials):
    print(f"\n### VIDEO - Surf City 'Atraxa Coaching #12' levers on GD   trials={trials} seed={SEED}")
    print("    (A) cantrip smootheners (Ponder/Preordain): do they move a MANA-gated clock?")
    print("    (B) Tidal Barracuda your-turn lock: protection AVAILABILITY by the decap turn.\n")
    library, commander = slc.load_parsed(BASELINE, index, aliases)
    full = {"select": True, "repeat": True}

    # (A) SMOOTHING: decap clock + whiff, full Atraxa model both rows --------
    print("  (A) SMOOTHING: decap clock + whiff (full Atraxa select+repeat model both rows)")
    smooth_lib = slc.build_lib(library, index, CANTRIP_CUTS, ["Ponder", "Preordain"])
    print("  " + "build".ljust(44) + "".join(f"{t:>6}" for t in SHOW) + "  median  never12")
    for tag, lib, cfg in (("baseline GD", library, full),
                          ("-Dovin's Veto -Swan Song +Ponder +Preordain", smooth_lib,
                           {**full, "cantrips": True})):
        pm = _powmap(lib, commander)
        res = _run(lib, commander, index, pm, trials, cfg)
        print(slc.row(tag, slc.cum(res, 0, SHOW), SHOW, width=44)
              + f"   {slc.median(res, 0):>5}  {_whiff(res, trials):5.0f}%")
    print("    (The two cuts are interaction the kill-goldfish can't see, so the delta isolates")
    print("     the dig; in a real game you also lose two counters - a cost this clock can't score.)")

    # (B) PROTECT-THE-KILL: lock availability by decap turn ------------------
    print("\n  (B) PROTECT-THE-KILL: P(a your-turn lock in hand by the decap turn)")
    swap_lib = slc.build_lib(library, index, ["Grand Abolisher"], ["Tidal Barracuda"])  # 2 locks
    add_lib = slc.build_lib(library, index, ["Dovin's Veto"], ["Tidal Barracuda"])       # 3 locks
    print("  " + "lock suite".ljust(42) + "by-decap  by-T12  median-avail")
    for tag, lib, locks in (
            ("current  (GA + Teferi) = 2 locks", library, LOCK_BASE),
            ("SWAP  GA -> Barracuda (+Teferi) = 2", swap_lib,
             ["Tidal Barracuda", "Teferi, Time Raveler"]),
            ("ADD   +Barracuda (GA+Teferi+Barra) = 3", add_lib,
             LOCK_BASE + ["Tidal Barracuda"])):
        pm = _powmap(lib, commander)
        cfg = {**full, "protect_set": set(locks), "protect_out": []}
        res = _run(lib, commander, index, pm, trials, cfg)
        prot = cfg["protect_out"]
        decapped = [(d, pt) for (d, _), pt in zip(res, prot) if d is not None]
        by_decap = 100.0 * sum(1 for d, pt in decapped if pt is not None and pt <= d) / max(1, len(decapped))
        by12 = 100.0 * sum(1 for pt in prot if pt is not None) / trials
        avail = sorted(pt for pt in prot if pt is not None)
        med = f"T{avail[len(avail) // 2]}" if avail else "-"
        print("  " + tag.ljust(42) + f"{by_decap:6.0f}% {by12:6.0f}%   {med:>6}")
    print("    SWAP is ~1-for-1 -> availability ~FLAT (it's a QUALITY change, not quantity).")
    print("    ADD raises a lock to hand by the kill turn (GD only has it ~half the time at 2 locks)")
    print("    - the real lever vs the Abolisher pod is lock COUNT, not which lock. The goldfish")
    print("    still can't score Barracuda's edges (stops creature spells/flash, end-step-Chord")
    print("    line) or its 4-vs-2 cost on a tight kill turn: delay_lab / interaction, not clock.")


if __name__ == "__main__":
    slc.run_cli(__doc__, {"clock": mode_clock, "levers": mode_levers, "ramp": mode_ramp,
                          "userpkg": mode_userpkg, "video": mode_video}, default_trials=40000)
