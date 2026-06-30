#!/usr/bin/env python3
"""rc_speed_lab.py — The Replication Crisis (Satya, Aetherflux Genius) race lab.

Tests the question the Pod Matchup Matrix row left open: can this deck actually
BEAT THE POD COMBO OPPONENT ON THE CLOCK (their kill: T6-7 behind Grand
Abolisher), or is the "T5-7 goldfish" window in the Summary a god-draw floor?

Two modes, both built on deck_sim.py's engine + oracle index:

  avail   Kill-package availability: P(every piece of >=1 complete kill package
          seen by turn T), drawn only — the deck has NO tutor that finds any
          piece (Ranger-Captain of Eos fetches MV<=1 creatures; no package piece
          qualifies). Packages: Satya + Lightning Runner infinite (commander + 1
          card, so availability == P(draw Lightning Runner)) / Sword+AA infinite /
          Adeline+Procession alpha / Brudiclad conversion. Also prints the LEGACY
          pre-LR 99 (the before/after for the 2026-06-22 swap) and the KIKI
          stack-on variant (+Kiki, -Strionic Resonator as an illustrative donor;
          The_Replication_Crisis_Swaps_2026-06-01.md — note Bident, that doc's
          original donor, is already cut as of 2026-06-22) where Kiki + (Conscripts
          or Resto) is a Satya-free assembly win that would stack as a 3rd infinite.

  clock   Goldfish kill-turn Monte Carlo. Unlike the availability model it
          tracks mana (lands + the 10 rocks), casts the board out greedily, and
          plays Satya combat turn by turn: attack trigger token = copy of the
          best nontoken creature in play (power + Inferno Titan's 3-damage
          enters/attacks trigger), doubled by Anointed Procession; ETB-trigger
          doubling (Panharmonicon / Elesh Norn) doubles the Titan token's enters
          damage; energy bank (+2/attack) keeps tokens whose MV it covers;
          Brudiclad converts the kept-token pile at begin-combat; Aggravated
          Assault buys extra combats at 5 mana; Sword-equipped Satya connecting
          with AA in play and >=5 lands = infinite combats = table kill;
          Akroma's Will doubles one combat's damage when it turns a 2-turn kill
          into a 1-turn kill. Reports, per variant:

            ALL-IN    every unsick creature attacks the focused opponent
                      (pure goldfish ceiling — assumes zero blockers)
            SQUAD     only Satya + her tokens attack; Adeline still triggers
                      (proxy for a defended board where ground crew stays home)

          ...the turn the FOCUSED opponent (= the combo player, 40 life) dies
          and the turn the TABLE (3 opponents) dies, plus the infinite-combat
          subset, plus the pending-Kiki assembly clock (Kiki + Conscripts/Resto
          in play = table kill that turn: infinite hasty bodies overwhelm
          blockers, no Satya needed).

HEURISTIC, NOT a rules engine. Known simplifications (all goldfish-FAVOURABLE
unless marked): attackers are never blocked (Satya only has menace — vs a real
board this is very generous); no opponent interaction/removal; Adeline tokens
spread 1/opponent (2 w/ Procession) per her printed text; Strionic Resonator,
Phelia/Resto flicker value, Goldspan Treasures and The One Ring draw are NOT
modelled (conservative, all small); Ponder/Preordain modelled as dig-2;
Cloudblazer/Wall of Omens ETB draw counted on cast. Trust the shape of the
curves and the variant gap, not the second decimal.

Card text verified via card_lookup.py 2026-06-09: Satya, Sword of F&F,
Aggravated Assault, Adeline, Anointed Procession, Brudiclad, Inferno Titan,
Kiki-Jiki, Zealous Conscripts, Restoration Angel, Strionic Resonator.

Writeup: proposals/Replication_Crisis_Speed_Curve_Analysis.md
Data: collection/oracle-cards.json (refresh via update_scryfall_data.py)
"""
import argparse
import importlib.util
import json
import random
from pathlib import Path

ROOT = Path(__file__).parent.parent
_spec = importlib.util.spec_from_file_location("deck_sim", Path(__file__).parent / "deck_sim.py")
ds = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(ds)

# Frozen pre-swap baseline for the 2026-06-30 Imperial Recruiter decision: this
# lab is the before/after that justified -Strionic Resonator +Imperial Recruiter,
# now APPLIED in decks/the-replication-crisis-20260630.txt. The "CURRENT deck"
# rows below are the pre-swap 99 (Strionic in, no Recruiter); the IMPERIAL
# RECRUITER variant rows are the now-live deck. Kept pinned to the archived list
# so the comparison stays reproducible (re-point to the live .txt only if you
# rebuild the variant logic to model the reverse swap).
DECK = ROOT / "archive" / "old_decklists" / "the-replication-crisis-20260622.txt"
SEED = 12345
TURNS = 12
SHOW = [3, 4, 5, 6, 7, 8, 10, 12]

# ---- card sets (exact decklist names) ------------------------------------
SWORD = "Sword of Feast and Famine"
AA = "Aggravated Assault"
ADELINE = "Adeline, Resplendent Cathar"
PROCESSION = "Anointed Procession"
BRUDICLAD = "Brudiclad, Telchor Engineer"
TITAN = "Inferno Titan"
KIKI = "Kiki-Jiki, Mirror Breaker"
KIKI_PARTNERS = ["Zealous Conscripts", "Restoration Angel"]
RECRUITER = "Imperial Recruiter"   # {2}{R} 1/1, ETB tutor a creature power<=2 to hand
SATYA_MV = 4

PACKAGES = {                       # slot-sets; a package is live when every slot is seen
    "INF   Sword+AA": [[SWORD], [AA]],
    "ALPHA Adeline+Procession": [[ADELINE], [PROCESSION]],
    "BRUD  Brudiclad": [[BRUDICLAD]],
}
KIKI_PACKAGE = {"KIKI  Kiki + Conscripts/Resto": [[KIKI], KIKI_PARTNERS]}

# --- Satya + Lightning Runner infinite (applied 2026-06-22) --------------------
# Applied swap (-Goldspan Dragon/-Ponder/-Preordain, +Lightning Runner/+Sleight of
# Hand/+Opt): the three cuts were each deployed in another physical deck (so the
# RC slots were free), and Lightning Runner gives an owned commander + 1-card
# infinite. Lightning Runner: "Whenever this attacks, you get {E}{E}, then you may
# pay 8{E}: untap all creatures + an additional combat phase." Satya makes a token
# copy of it each attack; once those token Runners are untapped they attack in the
# NEXT combat and trigger too, so per-combat energy = 2*(Satya + #Runners). At >=3
# Runners that is >=8/combat = self-sustaining => infinite combats/energy/tokens/
# damage. CSB combo db lists this complete (Satya + Lightning Runner) — text
# verified 2026-06-22. The LEGACY_* sets reconstruct the pre-swap 99 for the
# before/after comparison the report prints.
LRUNNER = "Lightning Runner"
LR_PACKAGE = {"INF   Satya + Lightning Runner": [[LRUNNER]]}   # Satya is the cmdr => 1-card avail
LEGACY_RM = [LRUNNER, "Sleight of Hand", "Opt"]
LEGACY_ADD = ["Goldspan Dragon", "Ponder", "Preordain"]

ROCKS = {"Sol Ring": (1, 2), "Arcane Signet": (2, 1), "Fellwar Stone": (2, 1),
         "Mind Stone": (2, 1), "Azorius Signet": (2, 1), "Boros Signet": (2, 1),
         "Izzet Signet": (2, 1), "Talisman of Conviction": (2, 1),
         "Talisman of Creativity": (2, 1), "Talisman of Progress": (2, 1)}
DIG = {"Ponder": (1, 2), "Preordain": (1, 2),          # (cost, gross cards)
       "Sleight of Hand": (1, 2), "Opt": (1, 1)}        # proposed-variant cantrips
ETB_DRAW = {"Cloudblazer": 2, "Wall of Omens": 1}      # drawn when cast
HASTE = {"Goldspan Dragon", "Zealous Conscripts", KIKI, LRUNNER}
PAN = {"Panharmonicon", "Elesh Norn, Mother of Machines"}   # double the token's ETB
WILL = "Akroma's Will"


# ==========================================================================
# avail — union package availability (no tutors apply)
# ==========================================================================
def simulate_packages(library, packages, trials, rng, tutors=None):
    """{package: curve} + 'ANY' curve: P(all slots of the package seen <= T).

    tutors: optional {tutor_name: {findable_piece_name, ...}}. When the tutor is
    among the seen cards, its findable pieces count as seen too — the drawn-only
    abstraction of "a tutor fetches its target to hand." Mana and the one-fetch-
    per-cast limit are NOT modelled here (that realism is the clock mode's job);
    for a tutor whose only combo-relevant target is a single piece (Imperial
    Recruiter -> Lightning Runner), the one-fetch limit doesn't distort the line."""
    n = len(library)
    pk = {name: [{s.lower() for s in slot} for slot in slots]
          for name, slots in packages.items()}
    tut = {k.lower(): {v.lower() for v in vs} for k, vs in (tutors or {}).items()}
    hits = {name: [0] * (TURNS + 1) for name in pk}
    any_hits = [0] * (TURNS + 1)
    for _ in range(trials):
        deck = library[:]
        hand, _ = ds.opening_hand(deck, rng)
        seen = {nm.lower() for nm, _ in hand}
        ptr = 7
        for t in range(1, TURNS + 1):
            if t > 1 and ptr < n:
                seen.add(deck[ptr][0].lower()); ptr += 1
            eff = seen
            if tut and any(tn in seen for tn in tut):
                eff = set(seen)
                for tname, targets in tut.items():
                    if tname in seen:
                        eff |= targets
            got_any = False
            for name, slots in pk.items():
                if all(slot & eff for slot in slots):
                    hits[name][t] += 1; got_any = True
            if got_any:
                any_hits[t] += 1
    curve = lambda h: {t: 100.0 * h[t] / trials for t in range(1, TURNS + 1)}
    return {name: curve(h) for name, h in hits.items()}, curve(any_hits)


def build_lib(base, index, removes, adds):
    rm = list(removes)
    lib = []
    for t in base:
        if t[0] in rm:
            rm.remove(t[0]); continue
        lib.append(t)
    if rm:                                  # mirror speed_lab_core: a typo'd cut is a loud error,
        raise SystemExit(f"remove not in library: {rm}")   # never a silent no-op
    for nm in adds:
        rec = index.get(nm.lower())
        if rec is None:
            raise SystemExit(f"add not in oracle: {nm}")
        lib.append((nm, rec))
    return lib


def _row(label, d):
    return "  " + label.ljust(34) + "".join(f"{d[t]:6.0f}" for t in SHOW)


def mode_avail(index, aliases, trials):
    print(f"\n### AVAIL — P(complete kill package seen <= turn T) %   trials={trials} seed={SEED}")
    print("    drawn only — no tutor in the 99 finds any package piece.\n")
    library, commander, diag = ds.parse_deck(DECK, index, aliases)
    if diag["unresolved"]:
        print(f"  UNRESOLVED: {diag['unresolved']}")
    print("  package".ljust(36) + "".join(f"{t:>6}" for t in SHOW))
    print("  CURRENT deck (with Satya + Lightning Runner):")
    rng = random.Random(SEED)
    per, any_c = simulate_packages(library, {**PACKAGES, **LR_PACKAGE}, trials, rng)
    for name, d in per.items():
        print(_row(name, d))
    print(_row("ANY of the four", any_c))
    print("  --- legacy (pre-LR: -Lightning Runner/Sleight/Opt +Goldspan/Ponder/Preordain) ---")
    legacy_lib = build_lib(library, index, LEGACY_RM, LEGACY_ADD)
    rng = random.Random(SEED)
    per, any_c = simulate_packages(legacy_lib, PACKAGES, trials, rng)
    print(_row("ANY of the three (no LR)", any_c))
    print("  --- KIKI stack-on variant (+Kiki-Jiki, -Strionic Resonator illustrative donor) ---")
    kiki_lib = build_lib(library, index, ["Strionic Resonator"], [KIKI])
    rng = random.Random(SEED)
    per, any_c = simulate_packages(kiki_lib, {**PACKAGES, **LR_PACKAGE, **KIKI_PACKAGE}, trials, rng)
    print(_row(next(iter(KIKI_PACKAGE)), per[next(iter(KIKI_PACKAGE))]))
    print("  --- IMPERIAL RECRUITER variant (+Imperial Recruiter, -Strionic Resonator donor) ---")
    print("      Recruiter ETB tutors a creature power<=2 -> fetches Lightning Runner (2/2).")
    print("      Modelled as: Recruiter seen => LR accessible (same drawn-only abstraction).")
    print("      Donor is Strionic Resonator (in no kill package), so ALL four lines stay live")
    print("      -- including Sword+AA. The LR-line lift is donor-independent.")
    rec_lib = build_lib(library, index, ["Strionic Resonator"], [RECRUITER])
    rng = random.Random(SEED)
    per, any_c = simulate_packages(rec_lib, {**PACKAGES, **LR_PACKAGE}, trials, rng,
                                   tutors={RECRUITER: {LRUNNER}})
    print(_row("INF   Satya + LR (draw LR or Recruiter)", per["INF   Satya + Lightning Runner"]))
    print(_row("ANY of the four (Sword+AA kept; -Strionic donor)", any_c))


# ==========================================================================
# clock — goldfish kill-turn model
# ==========================================================================
def load_powers(names):
    """name(lower) -> int power from the raw oracle file ('*' -> None=dynamic)."""
    with (ROOT / "collection" / "oracle-cards.json").open(encoding="utf-8") as f:
        cards = json.load(f)
    want = {n.lower() for n in names}
    out = {}
    for c in cards:
        k = c.get("name", "").lower()
        if k in want and k not in out:
            p = c.get("power")
            if p is None and c.get("card_faces"):
                p = c["card_faces"][0].get("power")
            try:
                out[k] = int(p)
            except (TypeError, ValueError):
                out[k] = None          # '*' (Adeline) or no power
    return out


def lr_infinite(energy, proc):
    """True if a banked-energy + Satya + Lightning Runner board goes infinite.

    Cascade each combat: bodies (Satya + all Lightning Runners) generate 2{E}
    each; pay 8{E} for one extra combat; Satya makes `growth` token Runners
    (2 with Anointed Procession, else 1) that attack next combat. Self-sustaining
    once #Runners >= 3 (gen 2*(1+3) = 8 >= cost). Returns True iff the starting
    bank survives the bootstrap (>=6 energy, >=4 with Procession)."""
    e, runners, growth = energy, 1, (2 if proc else 1)
    for _ in range(40):
        e += 2 * (1 + runners)         # Satya + every Runner attacks
        if e < 8:
            return False               # can't buy the extra combat -> fizzles
        e -= 8
        runners += growth
        if 2 * (1 + runners) >= 8:      # next combat generates >= cost -> runaway
            return True
    return False


def kill_turns(library, powers, rng, squad_only, with_kiki=False, with_lr=False):
    """One trial. Returns (first_opp_dead_turn, table_dead_turn, via_infinite,
    kiki_online_turn) — turns are None if not reached by TURNS.

    Greedy goldfish: land/turn, rocks tap same turn, cast priority Satya >
    Sword/equip > AA > Procession > doubler > Brudiclad > best copy-target
    creature; reserve 5 for one AA activation once AA is down. 3 opponents at
    40; all damage focused on one opponent until dead, then the next (Adeline's
    spread tokens chip the others per her text). Unblocked throughout."""
    deck = library[:]
    hand, _ = ds.opening_hand(deck, rng)
    hand = list(hand); ptr = 7

    def draw(k=1):
        nonlocal ptr
        for _ in range(k):
            if ptr < len(deck):
                hand.append(deck[ptr]); ptr += 1

    def in_hand(nm):
        return next((i for i, (h, _) in enumerate(hand) if h == nm), None)

    lands = rock_out = 0
    satya = False
    sword_cast = sword_on = aa = proc = pan = brud = lr_in_play = False
    will_used = False
    creatures = []                  # (name, power-or-None, cmc, cast_turn)
    kept = []                       # surviving token values (attack damage each)
    myr = 0
    energy = 0
    dmg = [0, 0, 0]
    focus = 0
    first_dead = table_dead = None
    via_inf = False
    kiki_partner = kiki_out = False
    kiki_online = None

    def n_creatures():
        return len(creatures) + len(kept) + myr + (1 if satya else 0)

    def pw(name, p):
        return n_creatures() if p is None and name == ADELINE else (p or 0)

    def copy_targets():
        return [(nm, pw(nm, p) + (3 if nm == TITAN else 0)) for nm, p, _, _ in creatures]

    for T in range(1, TURNS + 1):
        if T > 1:
            draw()
        li = next((i for i, (_, r) in enumerate(hand) if ds.is_pure_land(r)), None)
        if li is None:
            li = next((i for i, (_, r) in enumerate(hand) if ds.is_land(r)), None)
        if li is not None:
            hand.pop(li); lands += 1
        avail = lands + rock_out
        changed = True
        while changed:                                       # rocks, cheapest first
            changed = False
            cand = sorted(((i, ROCKS[nm]) for i, (nm, _) in enumerate(hand) if nm in ROCKS),
                          key=lambda x: x[1][0])
            for i, (cost, out) in cand:
                if avail >= cost:
                    hand.pop(i); avail += out - cost; rock_out += out; changed = True
                    break
        for nm, (cost, k) in DIG.items():                    # cantrip dig
            i = in_hand(nm)
            if i is not None and avail >= cost:
                hand.pop(i); avail -= cost; draw(k)

        def cast(nm, cost):
            nonlocal avail
            i = in_hand(nm)
            if i is not None and avail >= cost:
                hand.pop(i); avail -= cost
                return True
            return False

        if with_kiki:                                        # Kiki race takes priority
            for p_nm in KIKI_PARTNERS:
                if not kiki_partner:
                    rec_i = in_hand(p_nm)
                    if rec_i is not None:
                        c = hand[rec_i][1]["cmc"]
                        if avail >= c:
                            hand.pop(rec_i); avail -= c; kiki_partner = True
                            creatures.append((p_nm, powers.get(p_nm.lower()), c, T))
            if not kiki_out and kiki_partner and cast(KIKI, 5):
                kiki_out = True
            if kiki_out and kiki_partner and kiki_online is None:
                kiki_online = T                              # infinite hasty bodies
        if not satya and avail >= SATYA_MV:
            satya = True; avail -= SATYA_MV                  # haste: attacks now
        if satya and not sword_cast and cast(SWORD, 3):
            sword_cast = True
        if satya and sword_cast and not sword_on and avail >= 2:
            avail -= 2; sword_on = True
        if not aa and cast(AA, 3):
            aa = True
        if not proc and cast(PROCESSION, 4):
            proc = True
        if not pan:
            for d_nm, d_cost in (("Panharmonicon", 4), ("Elesh Norn, Mother of Machines", 7)):
                if cast(d_nm, d_cost):
                    pan = True; break
        if not brud and cast(BRUDICLAD, 6):
            brud = True
        if with_lr and satya and not lr_in_play and cast(LRUNNER, 5):
            lr_in_play = True
            creatures.append((LRUNNER, powers.get(LRUNNER.lower()), 5, T))
        reserve = 5 if (aa and satya) else 0
        while True:                                          # best copy-target creature
            best_i, best_v = None, 0
            for i, (nm, rec) in enumerate(hand):
                if "Creature" not in rec["type_line"] or nm in ROCKS:
                    continue
                p = powers.get(nm.lower())
                v = (p or 2) + (3 if nm == TITAN else 0)
                if rec["cmc"] <= avail - reserve and v > best_v:
                    best_i, best_v = i, v
            if best_i is None:
                break
            nm, rec = hand.pop(best_i)
            avail -= rec["cmc"]
            creatures.append((nm, powers.get(nm.lower()), rec["cmc"], T))
            if nm in ETB_DRAW:
                draw(ETB_DRAW[nm])

        # ---- combat ------------------------------------------------------
        if satya:
            if with_lr and lr_in_play and lr_infinite(energy, proc):
                dmg = [40, 40, 40]                            # infinite combats/damage
                first_dead = first_dead or T
                return first_dead, T, True, kiki_online
            if brud:                                         # begin combat: Myr + convert
                myr += 2 if proc else 1
                tv = max([v for _, v in copy_targets()] or [0])
                if tv > 2 and (kept or myr):
                    kept = [tv] * (len(kept) + myr); myr = 0
            new_tokens = []
            combats = 1
            while combats:
                combats -= 1
                D = 0
                satya_p = 5 if sword_on else 3
                D += satya_p
                energy += 2
                if with_lr and lr_in_play:
                    energy += 2                              # real Lightning Runner's attack energy
                tgts = copy_targets()
                if tgts:
                    nm_t, v = max(tgts, key=lambda x: x[1])
                    n_tok = 2 if proc else 1
                    enter_v = v + (3 if (nm_t == TITAN and pan) else 0)
                    D += n_tok * enter_v
                    rec_t = next(c for c in creatures if c[0] == nm_t)
                    new_tokens += [(v, rec_t[2])] * n_tok
                if any(nm == ADELINE for nm, _, _, _ in creatures):
                    chip = 2 if proc else 1                  # 1/1s spread, 1 per opponent
                    for o in range(3):
                        if dmg[o] < 40:
                            dmg[o] += chip
                D += sum(kept)
                D += 2 * myr
                if not squad_only:
                    for nm, p, _, ct in creatures:
                        if ct < T or nm in HASTE:
                            D += pw(nm, p) + (3 if nm == TITAN else 0)
                if (not will_used and avail >= 4 and D < 40 - dmg[focus] <= 2 * D
                        and in_hand(WILL) is not None):
                    hand.pop(in_hand(WILL)); avail -= 4; will_used = True
                    D *= 2
                if sword_on and aa and lands >= 5:           # infinite combats
                    dmg = [40, 40, 40]
                    first_dead = first_dead or T
                    return first_dead, T, True, kiki_online
                dmg[focus] += D
                while focus < 3 and dmg[focus] >= 40:
                    if first_dead is None:
                        first_dead = T
                    focus += 1
                    if focus == 3:
                        return first_dead, T, via_inf, kiki_online
                if aa and avail >= 5:                        # buy an extra combat
                    avail -= 5; combats += 1
            if not (with_lr and lr_in_play):                 # else bank energy for the LR combo
                keepable = sorted(new_tokens, key=lambda x: -x[0])
                for v, mv in keepable:                        # pay energy to keep
                    if energy >= mv > 0:
                        energy -= mv; kept.append(v)
        if kiki_online is not None and table_dead is None:
            dmg = [40, 40, 40]                               # overwhelm: table dies
            return first_dead or kiki_online, kiki_online, via_inf, kiki_online
    return first_dead, table_dead, via_inf, kiki_online


def _cum(results, idx):
    n = len(results)
    return {t: 100.0 * sum(1 for r in results if r[idx] is not None and r[idx] <= t) / n
            for t in SHOW}


def mode_clock(index, aliases, trials):
    print(f"\n### CLOCK — goldfish kill-turn Monte Carlo   trials={trials} seed={SEED}")
    print("    3 opponents @40, all damage focused on one (the combo player) until dead.")
    print("    ALL-IN = every unsick creature attacks (zero-blocker ceiling);")
    print("    SQUAD  = only Satya + tokens attack (defended-board proxy).\n")
    library, commander, diag = ds.parse_deck(DECK, index, aliases)
    names = [nm for nm, _ in library] + [KIKI]
    powers = load_powers(names)
    print("  metric".ljust(36) + "".join(f"{t:>6}" for t in SHOW))
    print("  CURRENT deck (Satya + Lightning Runner infinite modelled):")
    for tag, squad in [("ALL-IN", False), ("SQUAD", True)]:
        rng = random.Random(SEED)
        res = [kill_turns(library, powers, rng, squad, with_lr=True) for _ in range(trials)]
        print(_row(f"{tag}: combo player dead", _cum(res, 0)))
        print(_row(f"{tag}: table dead", _cum(res, 1)))
        if not squad:
            inf = [(r[1] if r[2] else None,) for r in res]
            print(_row("      (via an infinite: LR or Sword+AA)", _cum(inf, 0)))
    print("  --- legacy (pre-LR: -Lightning Runner/Sleight/Opt +Goldspan/Ponder/Preordain) ---")
    legacy_lib = build_lib(library, index, LEGACY_RM, LEGACY_ADD)
    for tag, squad in [("ALL-IN", False), ("SQUAD", True)]:
        rng = random.Random(SEED)
        res = [kill_turns(legacy_lib, powers, rng, squad) for _ in range(trials)]
        print(_row(f"{tag}: combo player dead", _cum(res, 0)))
        print(_row(f"{tag}: table dead", _cum(res, 1)))
        if not squad:
            inf = [(r[1] if r[2] else None,) for r in res]
            print(_row("      (via Sword+AA infinite)", _cum(inf, 0)))
    print("  --- KIKI stack-on variant (+Kiki, -Strionic Resonator donor): Satya-free assembly kill ---")
    kiki_lib = build_lib(library, index, ["Strionic Resonator"], [KIKI])
    rng = random.Random(SEED)
    res = [kill_turns(kiki_lib, powers, rng, True, with_kiki=True) for _ in range(trials)]
    kk = [(r[3],) for r in res]
    print(_row("KIKI line online (mana-aware)", _cum(kk, 0)))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--mode", choices=["avail", "clock", "both"], default="both")
    ap.add_argument("--trials", type=int, default=40000)
    args = ap.parse_args()
    index = ds.load_oracle_index()
    aliases = ds.load_reskin_aliases()
    if args.mode in ("avail", "both"):
        mode_avail(index, aliases, args.trials)
    if args.mode in ("clock", "both"):
        mode_clock(index, aliases, args.trials)


if __name__ == "__main__":
    main()
