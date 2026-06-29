#!/usr/bin/env python3
"""er_speed_lab.py — The Exile's Return (Fire Lord Zuko) kill-window lab.

Verifies the Summary's claimed goldfish kill window (T6-8) and runs a
Lightning-War-style lever test: which single-card adds actually move the
clock? Three modes, built on deck_sim.py's engine + oracle index:

  avail   Kill-package availability with HONEST tutor mapping:
            - Hellkite Charger + Sozin's Comet (the L1 one-turn table kill):
              ONLY Diabolic Intent reaches either piece. Enlightened Tutor is
              artifact/enchantment ONLY (Sozin's Comet is a SORCERY — the
              Summary's claim that ET finds it is wrong); Imperial Recruiter
              (power<=2) and Recruiter of the Guard (toughness<=2) both miss
              the 5/5 Hellkite.
            - >=2 exile engines online (the L2 Zuko counter-stack floor).
            - pending-swap variant (+Kiki -Night's Whisper, +Drannith -Light
              Up the Stage): Kiki + Felidar Guardian, where Imperial finds
              BOTH halves (Kiki 2/2, Felidar 1/4) and RotG finds Kiki.

  clock   Goldfish kill-turn Monte Carlo. Mana-aware (lands + rocks + Dark
          Ritual), greedy casts, and the two real kill axes:
            - +1/+1-counter accrual: every cast-from-exile and every
              permanent-entering-from-exile puts a counter on EACH creature
              (Panharmonicon doubles only the enters-from-exile events caused
              by a creature/artifact entering — cast triggers are not ETBs).
              Engine events are split pre-combat (flickers, impulse plays,
              foretold Sozin) vs post-combat (Norin/Circle/Prosper end-step
              loops) so counters land on the honest side of the attack.
            - firebending mana: Zuko X (X = his power), Sozin's Comet
              (firebending 5 to every creature), Zuko EP 3, Avatar Roku 4,
              Fire Nation Palace's 4-grant. Hellkite Charger's untap trigger
              is an ATTACK trigger, so firebending income CAN pay its
              {5}{R}{R}: income >= 7 in a combat = infinite combats = table
              kill. NOTE the asymmetry verified 2026-06-09: Aggravated
              Assault activates "only as a sorcery" (main phase) and
              firebending mana dies at end of combat, so in THIS deck (no
              Sword of Feast and Famine) AA buys one extra combat per 5 REAL
              mana and can never go infinite. Zuko at power >= 7 attacking
              alongside Hellkite is itself an infinite, no Sozin needed.
          Reports the turn the FOCUSED opponent dies (decapitation of the
          combo player: 40 life or 21 commander damage from Zuko) and the
          turn the TABLE (3 opponents) dies, plus infinite/commander-damage
          subsets.

  levers  One-card swap-ins through a fixed flex slot (-Imp's Mischief,
          goldfish-dead interaction) so every lever is measured on identical
          footing, same seed. Levers: Combat Celebrant (free exerted extra
          combat, RotG-tutorable at 4/1), Aggravated Assault (5-real-mana
          extra combats, Enlightened-Tutor-tutorable enchantment), Sarkhan's
          Triumph (instant Dragon tutor -> Hellkite), Port Razer, Moraug,
          Scourge of the Throne, Lotus Petal, Wrenn's Resolve (impulse
          velocity = counters + cards), Outpost Siege (owned, sideboard),
          Cathars' Crusade (owned, sideboard: a second counters-on-each
          engine keyed to creature ETBs, double-dips with every flicker,
          Panharmonicon-doubled), plus the pending Kiki+Felidar swap as a
          package variant.

HEURISTIC, NOT a rules engine. Known simplifications (goldfish-favourable
unless marked): attackers are never blocked; no opponent interaction; Prosper/
Light Up the Stage/Jeska's Will impulse plays modelled as a flat +1 cast-from-
exile event (conservative: real turns can chain several); Eldrazi Displacer's
{C} assumed available (generous); Monk Gyatso, Windbrisk Heights, Dualcaster-
copying-Sozin, Reconnaissance, Karmic Guide/Sun Titan recursion and all
removal/protection spells NOT modelled (conservative dilution); Black Market
Connections = flat draw 1/turn; Appa allies = 1 token per cast-from-exile
event while out. Trust curve shapes and lever ordering, not second decimals.

Card text verified via card_lookup.py 2026-06-09: Fire Lord Zuko, Hellkite
Charger, Sozin's Comet, Aggravated Assault, Enlightened Tutor, Imperial
Recruiter, Recruiter of the Guard, Diabolic Intent, Laelia, Prosper, Norin,
Teleportation Circle, Airbender Ascension, Appa, The Legend of Roku, Zuko EP,
Fire Nation Palace, Panharmonicon, Combat Celebrant, Sarkhan's Triumph,
Moraug, Port Razer, Scourge of the Throne, Wrenn's Resolve, Lotus Petal,
Outpost Siege, Kiki-Jiki, Felidar Guardian, flicker suite.

Writeup: proposals/Exiles_Return_Speed_Curve_Analysis.md
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

DECK = ROOT / "decks" / "the-exiles-return-20260417-194010.txt"
SEED = 12345
TURNS = 12
SHOW = [4, 5, 6, 7, 8, 10, 12]

# ---- card names (exact decklist spellings) --------------------------------
HELLKITE = "Hellkite Charger"
SOZIN = "Sozin's Comet"
DI = "Diabolic Intent"
ET = "Enlightened Tutor"
IMPERIAL = "Imperial Recruiter"
ROTG = "Recruiter of the Guard"
KIKI = "Kiki-Jiki, Mirror Breaker"
FELIDAR = "Felidar Guardian"
AA = "Aggravated Assault"
CELEBRANT = "Combat Celebrant"
SARKHAN = "Sarkhan's Triumph"
PETAL = "Lotus Petal"
RESOLVE = "Wrenn's Resolve"
SIEGE = "Outpost Siege"
RAZER = "Port Razer"
MORAUG = "Moraug, Fury of Akoum"
SCOURGE = "Scourge of the Throne"
CRUSADE = "Cathars' Crusade"        # owned, in the deck's own sideboard ($0)
FLEX_CUT = "Imp's Mischief"          # goldfish-dead interaction: lever flex slot

ZUKO_MV = 3                          # Fire Lord Zuko {R}{W}{B} = MV3 (card_lookup), base power 2
ROCKS = {"Sol Ring": (1, 2), "Arcane Signet": (2, 1), "Boros Signet": (2, 1),
         "Rakdos Signet": (2, 1), "Fellwar Stone": (2, 1),
         "Talisman of Conviction": (2, 1), "Talisman of Indulgence": (2, 1)}
HASTE = {HELLKITE, "Laelia, the Blade Reforged", KIKI}

# exile-event engines: name -> (cost, kind)
#   kind: 'cast' = ~1 cast-from-exile event/turn (pre-combat)
#         'post' = ~1 enters-from-exile event/turn at end step (post-combat)
ENGINES = {
    "Laelia, the Blade Reforged": (3, "cast"),     # attack impulse, plays it
    "Prosper, Tome-Bound": (4, "cast"),            # end-step exile, played next turn
    "Zuko, Exiled Prince": (4, "cast"),            # {3}: impulse (cost folded in)
    "Professional Face-Breaker": (3, "cast"),      # treasure -> impulse on connect
    "Norin the Wary": (1, "post"),                 # self-loops, never attacks
    "Teleportation Circle": (4, "post"),           # end-step flicker
    "Airbender Ascension": (2, "post"),            # end-step flicker once questy
    SIEGE: (4, "cast"),                            # lever/SB: upkeep impulse
}
# one-shot flicker spells: name -> (cost, enters_events, body_power-or-None)
FLICKERS = {
    "Cloudshift": (1, 1, None),
    "Ephemerate": (1, 1, None),                    # rebound: 2nd event next turn
    "Charming Prince": (3, 1, 2),
    "Flickerwisp": (3, 1, 3),
    "Eerie Interlude": (3, -1, None),              # -1 = all other creatures
    "Semester's End": (4, -1, None),               # + an extra counter each (ignored)
    FELIDAR: (4, 1, 1),
    "Restoration Angel": (4, 1, 3),
}
DRAW = {"Night's Whisper": (2, 2, 0),              # (cost, cards, cast_events)
        "Light Up the Stage": (3, 2, 1),           # impulse 2: ~1 cast from exile
        RESOLVE: (2, 2, 1)}                        # lever
JESKA = "Jeska's Will"                             # both modes w/ commander
BMC = "Black Market Connections"
PAN = "Panharmonicon"
ROKU = "The Legend of Roku"
APPA = "Appa, Steadfast Guardian"
GREAVES = "Lightning Greaves"
FNP = "Fire Nation Palace"
RITUAL = "Dark Ritual"


# ==========================================================================
# avail — package availability with per-slot tutor wildcards
# ==========================================================================
# package: list of slots; slot = (member-names, tutor-names that fetch it)
PKG_L1 = [({HELLKITE}, {DI}), ({SOZIN}, {DI})]
PKG_KIKI = [({KIKI}, {DI, IMPERIAL, ROTG}), ({FELIDAR}, {DI, IMPERIAL})]


def slot_complete(slots, seen):
    """Greedy/brute bipartite: members satisfy slots; each seen tutor fills <=1."""
    missing = [tut for mem, tut in slots if not (mem & seen)]
    if not missing:
        return True
    tutors_seen = list(set().union(*(t for t in missing)) & seen)
    if len(tutors_seen) < len(missing):
        return False
    # <=2 slots in every package: brute-force assignment
    if len(missing) == 1:
        return bool(missing[0] & seen)
    a, b = missing
    for t in tutors_seen:
        if t in a and (set(tutors_seen) - {t}) & b:
            return True
    return False


def simulate_avail(library, packages, trials, rng, engine_names=None):
    """{label: curve}; optional '>=2 engines' curve from engine_names."""
    n = len(library)
    pk = {name: [({m.lower() for m in mem}, {t.lower() for t in tut}) for mem, tut in slots]
          for name, slots in packages.items()}
    hits = {name: [0] * (TURNS + 1) for name in pk}
    eng = {e.lower() for e in (engine_names or [])}
    eng_hits = [0] * (TURNS + 1)
    for _ in range(trials):
        deck = library[:]
        hand, _ = ds.opening_hand(deck, rng)
        seen = {nm.lower() for nm, _ in hand}
        ptr = 7
        for t in range(1, TURNS + 1):
            if t > 1 and ptr < n:
                seen.add(deck[ptr][0].lower()); ptr += 1
            for name, slots in pk.items():
                if slot_complete(slots, seen):
                    hits[name][t] += 1
            if len(eng & seen) >= 2:
                eng_hits[t] += 1
    curve = lambda h: {t: 100.0 * h[t] / trials for t in range(1, TURNS + 1)}
    out = {name: curve(h) for name, h in hits.items()}
    if engine_names:
        out[">=2 exile engines seen"] = curve(eng_hits)
    return out


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
    return "  " + label.ljust(40) + "".join(f"{d[t]:6.0f}" for t in SHOW)


def mode_avail(index, aliases, trials):
    print(f"\n### AVAIL — P(kill package reachable <= turn T) %   trials={trials} seed={SEED}")
    print("    tutor map (text-verified): Diabolic Intent -> anything;")
    print("    Enlightened Tutor CANNOT find Sozin's Comet (sorcery); neither")
    print("    recruiter finds the 5/5 Hellkite Charger.\n")
    library, commander, diag = ds.parse_deck(DECK, index, aliases)
    if diag["unresolved"]:
        print(f"  UNRESOLVED: {diag['unresolved']}")
    print("  package".ljust(42) + "".join(f"{t:>6}" for t in SHOW))
    rng = random.Random(SEED)
    pkgs = {"L1 Hellkite+Sozin (drawn only)": [(m, set()) for m, _ in PKG_L1],
            "L1 Hellkite+Sozin (+tutors)": PKG_L1}
    eng = [e for e in ENGINES if e != SIEGE]
    for name, d in simulate_avail(library, pkgs, trials, rng, engine_names=eng).items():
        print(_row(name, d))
    print("  --- lever effect on L1 reach ---")
    lever_lib = build_lib(library, index, [FLEX_CUT], [SARKHAN])
    pk2 = {"+Sarkhan's Triumph (Dragon tutor)":
           [({HELLKITE}, {DI, SARKHAN}), ({SOZIN}, {DI})]}
    rng = random.Random(SEED)
    for name, d in simulate_avail(lever_lib, pk2, trials, rng).items():
        print(_row(name, d))
    print("  --- pending-swap variant (+Kiki -Night's Whisper, +Drannith -LUtS) ---")
    kiki_lib = build_lib(library, index,
                         ["Night's Whisper", "Light Up the Stage"],
                         [KIKI, "Drannith Magistrate"])
    pk3 = {"KIKI Kiki+Felidar (drawn only)": [(m, set()) for m, _ in PKG_KIKI],
           "KIKI Kiki+Felidar (+tutors)": PKG_KIKI}
    rng = random.Random(SEED)
    for name, d in simulate_avail(kiki_lib, pk3, trials, rng).items():
        print(_row(name, d))


# ==========================================================================
# clock — goldfish kill-turn model
# ==========================================================================
def load_powers(names):
    """name(lower) -> int power from the raw oracle file (None = no/dynamic)."""
    with (ROOT / "collection" / "oracle-cards.json").open(encoding="utf-8") as f:
        cards = json.load(f)
    want = {n.lower() for n in names}
    out = {}
    def put(k, p):
        if k in want and k not in out:
            try:
                out[k] = int(p)
            except (TypeError, ValueError):
                out[k] = None
    for c in cards:
        put(c.get("name", "").lower(), c.get("power"))
        for face in c.get("card_faces") or []:           # e.g. Avatar Roku (back face)
            put(face.get("name", "").lower(), face.get("power"))
    return out


def kill_turns(library, powers, rng, levers=frozenset(), with_kiki=False):
    """One trial. Returns (decap_turn, table_turn, via_infinite, via_commander,
    kiki_online). Greedy goldfish, 3 opponents @40, focus-fire until dead."""
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

    def fetch(nm):
        """Tutor: move named card from the undrawn library into hand."""
        nonlocal ptr
        for i in range(ptr, len(deck)):
            if deck[i][0] == nm:
                hand.append(deck[i])
                deck[i] = deck[len(deck) - 1]
                deck.pop()
                return True
        return False

    lands = rock_out = 0
    fnp = pan = appa = bmc = greaves = aa = False
    zuko_on = False; zuko_turn = 0; zuko_ctr = 0
    creatures = []                 # [name, base_power, cast_turn, counters]
    engines = set()                # engine names in play
    ascension_quest = 0
    roku_cast_turn = None; roku_avatar = False
    sozin_foretold = sozin_used = False
    ephemerate_rebound = False
    celebrant_in = razer_in = moraug_in = scourge_in = crusade_in = False
    kiki_in = felidar_in = False; kiki_online = None
    dmg = [0, 0, 0]; cmd = [0, 0, 0]
    focus = 0
    decap = table = None
    via_inf = via_cmd = False

    creature_adds = 0              # creature ETBs this turn (Cathars' Crusade)

    def creatures_entered(n=1):
        nonlocal ascension_quest, creature_adds
        ascension_quest += n
        creature_adds += n

    def add_creature(nm, T):
        p = powers.get(nm.lower())
        creatures.append([nm, 0 if p is None else p, T, 0])
        creatures_entered()

    def apply_counters(n):
        nonlocal zuko_ctr
        if n <= 0:
            return
        zuko_ctr += n if zuko_on else 0
        for c in creatures:
            c[3] += n

    for T in range(1, TURNS + 1):
        creature_adds = 0
        if T > 1:
            draw()
        if bmc:
            draw()
        # land drop
        lands_played = 0
        li = next((i for i, (_, r) in enumerate(hand) if ds.is_pure_land(r)), None)
        if li is None:
            li = next((i for i, (_, r) in enumerate(hand) if ds.is_land(r)), None)
        if li is not None:
            nm = hand[li][0]
            hand.pop(li); lands += 1; lands_played = 1
            if nm == FNP:
                fnp = True
        avail = lands + rock_out
        # rocks / rituals, cheapest first
        changed = True
        while changed:
            changed = False
            cand = sorted(((i, ROCKS[nm]) for i, (nm, _) in enumerate(hand) if nm in ROCKS),
                          key=lambda x: x[1][0])
            for i, (cost, out) in cand:
                if avail >= cost:
                    hand.pop(i); avail += out - cost; rock_out += out; changed = True
                    break
        i = in_hand(RITUAL)
        if i is not None and avail >= 1:
            hand.pop(i); avail += 2                      # B -> BBB one-shot
        i = in_hand(PETAL)
        if i is not None:
            hand.pop(i); avail += 1                      # lever: one-shot

        def cast(nm, cost):
            nonlocal avail
            j = in_hand(nm)
            if j is not None and avail >= cost:
                hand.pop(j); avail -= cost
                return True
            return False

        pre_cast_ev = 0          # cast-from-exile events before combat
        pre_ent_ev = 0           # enters-from-exile events before combat
        post_cast_ev = 0
        post_ent_ev = 0

        # ---- tutors (cheap, before threats) -------------------------------
        if cast(SARKHAN, 3):                              # lever: Dragon -> Hellkite
            if not fetch(HELLKITE):
                fetch(SCOURGE)
        if in_hand(ET) is not None and avail >= 1:        # artifact/enchantment ONLY
            # priority: AA/Crusade (levers) > Panharmonicon > Teleportation Circle
            for want in ([AA] if not aa else []) \
                    + ([CRUSADE] if CRUSADE in levers and not crusade_in else []) \
                    + ([PAN] if not pan else []) \
                    + (["Teleportation Circle"] if "Teleportation Circle" not in engines else []):
                if in_hand(want) is None and fetch(want):
                    hand.pop(in_hand(ET)); avail -= 1
                    break
        sac_ok = [j for j, c in enumerate(creatures) if c[0] not in (HELLKITE, KIKI, FELIDAR)]
        if in_hand(DI) is not None and avail >= 2 and sac_ok:
            seen_hk = HELLKITE in [c[0] for c in creatures] or in_hand(HELLKITE) is not None
            seen_sz = sozin_foretold or in_hand(SOZIN) is not None
            want = None
            if with_kiki and not (kiki_in or in_hand(KIKI) is not None):
                want = KIKI
            elif seen_hk and not seen_sz:
                want = SOZIN
            elif seen_sz and not seen_hk:
                want = HELLKITE
            elif not seen_hk:
                want = HELLKITE
            if want and fetch(want):
                hand.pop(in_hand(DI)); avail -= 2
                creatures.pop(min(sac_ok, key=lambda j: creatures[j][1] + creatures[j][3]))
        for rec_nm in (IMPERIAL, ROTG):                   # recruiters as bodies+tutor
            j = in_hand(rec_nm)
            if j is not None and avail >= 3:
                hand.pop(j); avail -= 3
                add_creature(rec_nm, T)
                if with_kiki and rec_nm == IMPERIAL and not kiki_in and in_hand(KIKI) is None:
                    fetch(KIKI)                           # Kiki 2/2: power <= 2
                elif with_kiki and rec_nm == IMPERIAL and not felidar_in and in_hand(FELIDAR) is None:
                    fetch(FELIDAR)                        # Felidar 1/4: power <= 2
                elif with_kiki and rec_nm == ROTG and not kiki_in and in_hand(KIKI) is None:
                    fetch(KIKI)                           # Kiki 2/2: toughness <= 2
                elif rec_nm == ROTG and CELEBRANT in levers and not celebrant_in and in_hand(CELEBRANT) is None:
                    fetch(CELEBRANT)                      # Celebrant 4/1: toughness <= 2
                else:
                    fetch("Laelia, the Blade Reforged") or fetch("Norin the Wary")

        # ---- commander ----------------------------------------------------
        if not zuko_on and avail >= ZUKO_MV:
            zuko_on = True; zuko_turn = T; avail -= ZUKO_MV

        # ---- kiki combo (pending-swap variant) ----------------------------
        if with_kiki:
            if not felidar_in and cast(FELIDAR, 4):
                felidar_in = True; add_creature(FELIDAR, T); pre_ent_ev += 1
            if not kiki_in and cast(KIKI, 5):
                kiki_in = True; add_creature(KIKI, T)
            if kiki_in and felidar_in and kiki_online is None:
                kiki_online = T                           # infinite hasty Felidars

        # ---- threats / engines / draw -------------------------------------
        if HELLKITE not in [c[0] for c in creatures] and cast(HELLKITE, 6):
            add_creature(HELLKITE, T)
        zuko_power = (2 + zuko_ctr) if zuko_on else 0
        hk_ready = any(c[0] == HELLKITE for c in creatures)
        combo_now = hk_ready and (sozin_foretold and avail >= 3 or in_hand(SOZIN) is not None and avail >= 5)
        sozin_active = False
        if combo_now and not sozin_used:
            if sozin_foretold and avail >= 3:
                avail -= 3; sozin_foretold = False; sozin_used = True
                sozin_active = True; pre_cast_ev += 1     # cast from exile
            elif cast(SOZIN, 5):
                sozin_used = True; sozin_active = True
        elif not sozin_used and not sozin_foretold and in_hand(SOZIN) is not None and avail >= 2:
            j = in_hand(SOZIN); hand.pop(j); avail -= 2; sozin_foretold = True
        if not pan and cast(PAN, 4):
            pan = True
        if not aa and cast(AA, 3):                        # lever
            aa = True
        if CRUSADE in levers and not crusade_in and cast(CRUSADE, 5):
            crusade_in = True                             # lever (owned, SB)
        for e_nm, (e_cost, _) in ENGINES.items():
            if e_nm not in engines and cast(e_nm, e_cost):
                engines.add(e_nm)
                if e_nm in ("Laelia, the Blade Reforged", "Prosper, Tome-Bound",
                            "Zuko, Exiled Prince", "Professional Face-Breaker",
                            "Norin the Wary"):
                    add_creature(e_nm, T)
        if roku_cast_turn is None and cast(ROKU, 4):
            roku_cast_turn = T; pre_cast_ev += 1          # ch I impulse play
        if roku_cast_turn is not None and not roku_avatar and T >= roku_cast_turn + 2:
            roku_avatar = True
            add_creature("Avatar Roku", T)                # enters from exile, transformed
            pre_ent_ev += 1
        if not appa and cast(APPA, 4):
            appa = True; add_creature(APPA, T)
        if not bmc and cast(BMC, 3):
            bmc = True
        if not greaves and cast(GREAVES, 1):
            greaves = True
        for nm, (cost, cards, ev) in DRAW.items():
            if cast(nm, cost):
                draw(cards); pre_cast_ev += ev
        if zuko_on and cast(JESKA, 3):
            avail += 4; draw(2); pre_cast_ev += 1         # both modes
        # levers: extra-combat creatures
        for lv_nm, lv_cost in ((CELEBRANT, 3), (RAZER, 5), (MORAUG, 6), (SCOURGE, 6)):
            if lv_nm in levers and cast(lv_nm, lv_cost):
                add_creature(lv_nm, T)
                celebrant_in |= lv_nm == CELEBRANT
                razer_in |= lv_nm == RAZER
                moraug_in |= lv_nm == MORAUG
                scourge_in |= lv_nm == SCOURGE
        # one-shot flickers (need a creature to flicker; don't flicker Zuko)
        if ephemerate_rebound:
            ephemerate_rebound = False
            if creatures:
                pre_ent_ev += 1
        for f_nm, (f_cost, f_ev, f_pow) in FLICKERS.items():
            j = in_hand(f_nm)
            if j is None or avail < f_cost:
                continue
            n_others = len(creatures)
            if f_pow is None and n_others == 0:
                continue                                  # nothing to flicker
            hand.pop(j); avail -= f_cost
            if f_pow is not None:
                add_creature(f_nm, T)
            ev_n = n_others if f_ev == -1 else f_ev
            if f_pow is not None and n_others == 0 and f_nm != FELIDAR:
                ev_n = 0                                  # body but nothing to flicker
            pre_ent_ev += max(ev_n, 0)
            if f_nm == "Ephemerate":
                ephemerate_rebound = True
        # generic bodies (anything castable left, biggest first)
        while True:
            best_j, best_p = None, -1
            for j, (nm, rec) in enumerate(hand):
                if "Creature" not in rec.get("type_line", "") or nm in ROCKS:
                    continue
                p = powers.get(nm.lower()) or 0
                if rec["cmc"] <= avail and p > best_p:
                    best_j, best_p = j, p
            if best_j is None:
                break
            nm, rec = hand.pop(best_j)
            avail -= rec["cmc"]
            add_creature(nm, T)

        # ---- repeatable engine events --------------------------------------
        for e_nm in engines:
            cost, kind = ENGINES[e_nm]
            if e_nm == "Zuko, Exiled Prince":
                if avail >= 3:
                    avail -= 3; pre_cast_ev += 1
            elif e_nm == "Airbender Ascension":
                if ascension_quest >= 4 and creatures:
                    post_ent_ev += 1
            elif kind == "cast":
                pre_cast_ev += 1
            else:
                post_ent_ev += 1

        # ---- counters land pre-combat ---------------------------------------
        mult = 2 if pan else 1
        if appa:
            for _ in range(pre_cast_ev):
                creatures.append(["Ally", 1, T, 0])
                creatures_entered()
        crusade_pre = (creature_adds + pre_ent_ev) * mult if crusade_in else 0
        apply_counters(pre_cast_ev + pre_ent_ev * mult + crusade_pre)
        zuko_power = (2 + zuko_ctr) if zuko_on else 0

        # ---- combat ---------------------------------------------------------
        attackers = [c for c in creatures
                     if (c[2] < T or greaves or c[0] in HASTE)
                     and c[0] not in ("Norin the Wary",)]
        zuko_attacks = zuko_on and (zuko_turn < T or greaves)
        if attackers or zuko_attacks:
            K = len(attackers) + (1 if zuko_attacks else 0)
            D = sum(p + ctr for _, p, _, ctr in attackers) + (zuko_power if zuko_attacks else 0)
            hk_atk = any(c[0] == HELLKITE for c in attackers)
            celebrant_pow = next((p + ctr for nm, p, _, ctr in attackers if nm == CELEBRANT), None)
            scourge_pow = next((p + ctr for nm, p, _, ctr in attackers if nm == SCOURGE), None)
            combats = [D]
            if moraug_in and lands_played:
                combats += [D] * lands_played             # pre-combat landfall combats
            if hk_atk:
                income = (5 * K if sozin_active else 0)
                income += zuko_power if zuko_attacks else 0
                income += 4 if any(c[0] == "Avatar Roku" for c in attackers) else 0
                income += 3 if any(c[0] == "Zuko, Exiled Prince" for c in attackers) else 0
                if fnp and avail >= 2:
                    avail -= 2; income += 4
                if income >= 7:                           # infinite combats
                    via_inf = True
                    decap = decap or T
                    return decap, T, True, via_cmd, kiki_online
                while avail >= 7 - income:
                    avail -= 7 - income
                    combats.append(D)
                    if len(combats) > 12:
                        break
            if celebrant_in and celebrant_pow is not None:
                combats.append(D - celebrant_pow)         # exert: once per turn
            if razer_in and any(c[0] == RAZER for c in attackers):
                combats.append(D)                         # connect -> extra combat
            if scourge_in and scourge_pow is not None:
                combats.append(D - scourge_pow)           # Scourge must hit high-life
            while aa and avail >= 5:                      # real mana only (verified)
                avail -= 5
                combats.append(D)
                if len(combats) > 12:
                    break
            for D_i in combats:
                if focus > 2:
                    break
                dmg[focus] += D_i
                if zuko_attacks:
                    cmd[focus] += zuko_power
                while focus < 3 and (dmg[focus] >= 40 or cmd[focus] >= 21):
                    if decap is None:
                        decap = T
                        via_cmd = cmd[focus] >= 21 and dmg[focus] < 40
                    focus += 1
                    if focus == 3:
                        return decap, T, via_inf, via_cmd, kiki_online

        # ---- post-combat / end-step events ----------------------------------
        crusade_post = post_ent_ev * mult if crusade_in else 0
        apply_counters(post_cast_ev + post_ent_ev * mult + crusade_post)
        if kiki_online is not None:
            decap = decap or kiki_online
            return decap, kiki_online, via_inf, via_cmd, kiki_online
    return decap, table, via_inf, via_cmd, kiki_online


def _cum(results, idx):
    n = len(results)
    return {t: 100.0 * sum(1 for r in results if r[idx] is not None and r[idx] <= t) / n
            for t in SHOW}


def _median(results, idx):
    vals = sorted((r[idx] if r[idx] is not None else 99) for r in results)
    m = vals[(len(vals) - 1) // 2]      # lower-middle (see speed_lab_core.median)
    return f"T{m}" if m < 99 else ">T12"


def run_clock(library, powers, trials, levers=frozenset(), with_kiki=False):
    rng = random.Random(SEED)
    return [kill_turns(library, powers, rng, levers, with_kiki) for _ in range(trials)]


def mode_clock(index, aliases, trials):
    print(f"\n### CLOCK — goldfish kill-turn Monte Carlo   trials={trials} seed={SEED}")
    print("    3 opponents @40 (21 Zuko commander damage also kills), focus-fire,")
    print("    every creature unblocked: a CEILING, real games are slower.\n")
    library, commander, diag = ds.parse_deck(DECK, index, aliases)
    names = [nm for nm, _ in library] + [KIKI, CELEBRANT, SCOURGE, RAZER, MORAUG, "Avatar Roku"]
    powers = load_powers(names)
    print("  metric".ljust(42) + "".join(f"{t:>6}" for t in SHOW))
    res = run_clock(library, powers, trials)
    print(_row("combo player dead (decap)", _cum(res, 0)) + f"   med {_median(res, 0)}")
    print(_row("table dead", _cum(res, 1)) + f"   med {_median(res, 1)}")
    inf = [(r[1] if r[2] else None,) for r in res]
    print(_row("  (table via Hellkite infinite)", _cum(inf, 0)))
    cmdk = [(r[0] if r[3] else None,) for r in res]
    print(_row("  (decap via 21 commander dmg)", _cum(cmdk, 0)))


def mode_levers(index, aliases, trials):
    print(f"\n### LEVERS — one-card swap-ins through the flex slot (-{FLEX_CUT})")
    print(f"    trials={trials} seed={SEED}; identical model, identical seed.\n")
    library, commander, diag = ds.parse_deck(DECK, index, aliases)
    names = [nm for nm, _ in library] + [KIKI, FELIDAR, CELEBRANT, SCOURGE, RAZER,
                                         MORAUG, SARKHAN, PETAL, RESOLVE, SIEGE,
                                         AA, "Avatar Roku", "Drannith Magistrate"]
    powers = load_powers(names)
    base = run_clock(library, powers, trials)
    hdr = "  lever".ljust(42) + "".join(f"{t:>6}" for t in SHOW)
    print(hdr + "   median")
    print(_row("BASELINE decap", _cum(base, 0)) + f"   {_median(base, 0)}")
    print(_row("BASELINE table", _cum(base, 1)) + f"   {_median(base, 1)}")
    levers = [CRUSADE, CELEBRANT, AA, SARKHAN, RAZER, MORAUG, SCOURGE, PETAL, RESOLVE, SIEGE]
    for lv in levers:
        lib = build_lib(library, index, [FLEX_CUT], [lv])
        res = run_clock(lib, powers, trials, levers=frozenset([lv]))
        print(_row(f"+{lv}  decap", _cum(res, 0)) + f"   {_median(res, 0)}")
        print(_row(" " * (len(lv) + 1) + "  table", _cum(res, 1)) + f"   {_median(res, 1)}")
    print("  --- pending-swap variant (+Kiki -Night's Whisper, +Drannith -LUtS) ---")
    kiki_lib = build_lib(library, index,
                         ["Night's Whisper", "Light Up the Stage"],
                         [KIKI, "Drannith Magistrate"])
    res = run_clock(kiki_lib, powers, trials, with_kiki=True)
    print(_row("KIKI variant  decap", _cum(res, 0)) + f"   {_median(res, 0)}")
    print(_row("              table", _cum(res, 1)) + f"   {_median(res, 1)}")
    kk = [(r[4],) for r in res]
    print(_row("  (Kiki+Felidar online, mana-aware)", _cum(kk, 0)))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--mode", choices=["avail", "clock", "levers", "all"], default="all")
    ap.add_argument("--trials", type=int, default=40000)
    args = ap.parse_args()
    index = ds.load_oracle_index()
    aliases = ds.load_reskin_aliases()
    if args.mode in ("avail", "all"):
        mode_avail(index, aliases, args.trials)
    if args.mode in ("clock", "all"):
        mode_clock(index, aliases, args.trials)
    if args.mode in ("levers", "all"):
        mode_levers(index, aliases, args.trials)


if __name__ == "__main__":
    main()
