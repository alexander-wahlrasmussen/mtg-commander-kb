#!/usr/bin/env python3
"""mp_clock_lab.py — Mass Production (Baylen, the Haymaker) KILL-TURN goldfish.

New-deck build (WF_New_Deck Stage 2 / WF_Kill_Window_Lab). The Summary's Kill Window
was flagged (unverified); this lab replaces it. Built on speed_lab_core.py.

KILL SHAPES (three lines; the lab models all three and reports which one fires):

  COMBO (decap = table)   Basking Broodscale + Rosie Cotton  OR  Basking Broodscale +
        Cathars' Crusade is a 2-card infinite: a +1/+1 counter on Broodscale makes an
        Eldrazi Spawn token; that token's creation (Rosie) / its ETB counter (Cathars')
        puts another counter on Broodscale -> loops. Infinite ETB. With Purphoros OR
        Impact Tremors also in play -> infinite damage to the table = kill_all.
        (find_combos.py 2026-07-11 confirms both pairings; CSB 2433-5641 / 2744-5641.)

  BURN (converge, decap ~ table)  Purphoros (2 dmg/opp per OTHER creature ETB) + Impact
        Tremors (1 dmg/opp per creature ETB), each DOUBLED to opponents by Twinflame
        Tyrant. Every token that enters pings the whole table -> a mass-token turn under
        a doubler burns everyone at once. hit_all, no combat needed.

  COMBAT (decap-fast / table via trample)  Go wide, then Craterhoof Behemoth (haste; on
        ETB all your creatures +X/+X and TRAMPLE, X = creatures) alpha-distributes across
        the table. Finale of Devastation for X>=8 tutors Craterhoof onto the battlefield
        (same alpha). Moonshaker Cavalry (+X/+X, FLYING not trample) focus-fires one
        opponent. Triumph of the Hordes gives the team +1/+1 + trample + INFECT (10-poison
        threshold, modelled as a parallel life-10 table). Standing board focus-fires.

THE PRODUCER AMPLIFIER (WF_Kill_Window_Lab Stage 1 — inventory every producer):
  Token DOUBLERS multiply every token batch, multiplicatively and per the oracle:
    Doubling Season / Anointed Procession / Parallel Lives / Elspeth, Storm Slayer = x2 each,
    Ojer Taq, Deepest Foundation = x3 (creature tokens). M = 2**doublers * (3 if Ojer).
  Omitting these would bias the clock SLOW and under-rate the race (the exact failure the WF
  warns about). M is applied to every TOKEN count (not to nontoken bodies), which also scales
  the Purphoros/Impact ETB pings. M capped at 12 and tokens/turn capped at 50 — documented
  optimism bounds so a doubler stack doesn't produce a fictional T3.

Oracle facts encoded (card_lookup.py 2026-07-11):
  * Baylen {R}{G}{W} 4/3: tap 2 tokens -> 1 mana (modelled as modest ramp, capped 3);
    tap 3 tokens -> draw (modelled as +1 card/turn once >=3 tokens). Tokens tapped this way
    can't attack; the model assumes token surplus and does NOT dock attackers (goldfish ceiling).
  * Purphoros {3}{R}: triggers on OTHER creatures entering, always (god or not); 2/opp.
  * Impact Tremors {1}{R}: 1/opp per creature ETB.  Twinflame Tyrant {3}{R}{R}: doubles all
    of our damage to opponents (burn AND combat) — applied as x2.
  * Craterhoof {5}{G}{G}{G} MV8 HASTE, +X/+X + trample, X = creatures.  Moonshaker {5}{W}{W}{W}
    MV8, +X/+X + flying (no trample -> focus).  Finale {X}{G}{G}: X>=8 fetches Craterhoof to
    the battlefield (its own +X/+X needs X>=10; the fetched Craterhoof alpha is the real kill).
  * Basking Broodscale {1}{G}: counter on it -> may make a 0/1 Spawn (Adapt {1}{G} seeds the
    first counter; Cathars' seeds it on any creature ETB).  Rosie {2}{W}: on any token created,
    +1/+1 counter on another creature (target Broodscale).  Cathars' {3}{W}{W}: creature ETB ->
    +1/+1 on each of your creatures.

HEURISTIC, not a rules engine (same caveats as every lab). Mana = lands + rocks/dorks +
land-ramp spells + a capped Baylen bump; damage unblocked; token counts are ceilings.
X-token spells (Awaken/Decree/Forth) scale with mana left after base cost. Trust shapes and
the front edge, not the second decimal. decap and table reported separately.

Data: collection/oracle-cards.json   ·   Writeup: proposals/Mass_Production_Clock_Lab_2026-07-11.md
"""
import importlib.util
import random
from pathlib import Path

ROOT = Path(__file__).parent.parent
_spec = importlib.util.spec_from_file_location("speed_lab_core", Path(__file__).parent / "speed_lab_core.py")
slc = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(slc)
ds = slc.ds

# The OWNED zero-contention list is the keeper (2026-07-11); the premium draft lives in
# archive/old_decklists/mass-production-20260711.txt and stays runnable via --deck <path>.
# 2026-07-17 Akroma swap (4 phantom-CSV cards: -Angel of Invention -Avenger of Zendikar
# -Birds of Paradise -Skyclave Apparition, +Akroma's Will +Akroma's Memorial +Ilysian
# Caryatid +Stroke of Midnight): medians held T7/T10 @20k; prior list archived.
DECK = ROOT / "decks" / "mass-production-owned-20260717.txt"
SEED = 20260711
TURNS = 14
SHOW = [5, 6, 7, 8, 9, 10, 12, 14]

# fixed mana producers + dorks the scaffold deploys greedily: name -> (cost, output)
ROCKS = {
    "Sol Ring": (1, 2), "Arcane Signet": (2, 1), "Fellwar Stone": (2, 1),
    "Birds of Paradise": (1, 1), "Llanowar Elves": (1, 1), "Elvish Mystic": (1, 1),
    "Gilded Goose": (1, 1),
}
# land-ramp spells: name -> (cost, lands added, taps this turn = conservative)
RAMP = {
    "Sakura-Tribe Elder": (2, 1), "Cultivate": (3, 1), "Kodama's Reach": (3, 1),
}
# token DOUBLERS: name -> multiplier factor
DOUBLERS = {"Doubling Season": 2, "Anointed Procession": 2, "Parallel Lives": 2,
            "Elspeth, Storm Slayer": 2, "Ojer Taq, Deepest Foundation": 3}
DOUBLER_COST = {"Doubling Season": 5, "Anointed Procession": 4, "Parallel Lives": 4,
                "Elspeth, Storm Slayer": 5, "Ojer Taq, Deepest Foundation": 6}

# burst token spells/ETBs: name -> (cost, base_token_count, token_power, haste)
# (covers BOTH the primary list and the owned/no-contention variant — run either via --deck)
BURST = {
    "Hop to It": (3, 3, 1, False),
    "Saproling Migration": (2, 2, 1, False),
    "Battle Screech": (4, 2, 1, False),
    "Hornet Queen": (7, 4, 1, False),
    "Siege-Gang Commander": (5, 3, 1, False),
    "Esika's Chariot": (4, 2, 2, False),
    "Decree of Justice": (0, 0, 1, False),   # X-spell, handled specially
    # --- owned/no-contention variant makers ---
    "Rally at the Hornburg": (2, 2, 1, True),      # Humans gain haste -> tokens attack now
    "Scurry of Gremlins": (4, 2, 1, False),        # 2 gremlins (+energy anthem, ignored)
    "Gather the White Lotus": (5, 4, 1, False),    # ~1 token per Plains (approx 4)
    "The Crystal's Chosen": (7, 4, 1, False),      # 4 heroes (+1/+1 to team, approx via anthem)
}
# per-turn engines once online: name -> (cost,)
ENGINES = ("Adeline, Resplendent Cathar", "Scute Swarm", "Avenger of Zendikar",
           "Rampaging Baloths", "Tendershoot Dryad", "Felidar Retreat", "Nesting Dragon",
           "God-Eternal Oketra", "Monastery Mentor", "Suki, Kyoshi Warrior",
           "Hanweir Garrison", "Oviya Pashiri, Sage Lifecrafter")
ENGINE_COST = {"Adeline, Resplendent Cathar": 3, "Scute Swarm": 3, "Avenger of Zendikar": 7,
               "Rampaging Baloths": 6, "Tendershoot Dryad": 5, "Felidar Retreat": 4,
               "Nesting Dragon": 5, "God-Eternal Oketra": 5, "Monastery Mentor": 3,
               "Suki, Kyoshi Warrior": 4, "Hanweir Garrison": 3,
               "Oviya Pashiri, Sage Lifecrafter": 1}
# owned-variant permanents (finishers / anthems / pingers): name -> (cost, own_power)
OWNED_PERMS = {
    "Elesh Norn, Grand Cenobite": (7, 4), "Angel of Invention": (5, 2),
    "Salvation Colossus": (8, 9), "Legion Loyalty": (8, 0), "Jazal Goldmane": (4, 4),
    "Blossoming Bogbeast": (5, 3), "Herald of the Host": (5, 4),
}

# +1/+1 COUNTER doublers (distinct from the token DOUBLERS above; Doubling Season is both).
# Only deployed/modelled when Walking Ballista is in the deck (the ballista A/B mode) so the
# baseline clock numbers stay byte-identical. Oracle (card_lookup 2026-07-11): all three are
# "twice that many +1/+1 counters" replacement effects; they apply to counters a permanent
# ENTERS with (Doubling Season ruling) — so Ballista cast for X enters with X*mult counters.
CTR_DOUBLERS = {"Doubling Season": 5, "Branching Evolution": 3, "The Earth Crystal": 4}
CTR_CAP = 8

M_CAP = 12
TOK_CAP = 50


def trample_distribute(tbl, P, T):
    remaining = P
    for i in range(len(tbl.dmg)):
        if remaining <= 0:
            break
        if tbl.dmg[i] < tbl.life:
            take = min(tbl.life - tbl.dmg[i], remaining)
            tbl.dmg[i] += take
            remaining -= take
    tbl._update(T)


def _survives_wipe(nm, index):
    """A creature board-wipe (Wrath/Blasphemous Act class) kills creatures only. Non-creature
    permanents (enchantment/artifact/planeswalker doublers, anthems, and Impact Tremors) stay;
    Purphoros is indestructible so it stays and keeps pinging on the rebuild."""
    if nm == "Baylen" or nm == "Purphoros, God of the Forge":
        return nm == "Purphoros, God of the Forge"
    rec = index.get(nm.lower())
    tl = (rec["type_line"].lower() if rec else "")
    return "creature" not in tl


def goldfish_kill(library, commander, index, rng, use_combo=True, wipe_turns=()):
    """One trial -> (decap, table, kind). wipe_turns = turns a creature board-wipe resolves
    (all our creatures destroyed at the start of that turn; non-creature permanents + the
    indestructible Purphoros survive) — the Durability checkpoint."""
    g = slc.Goldfish(library, rng, rocks=ROCKS)
    tbl = slc.Table()            # normal life-40
    inf = slc.Table(life=10)     # parallel infect table (Triumph of the Hordes)

    board_pow, ncre = 0, 0       # matured (can attack)
    new_pow, new_cre = 0, 0      # deployed this turn (sick, mature next turn)
    onb = set()                  # permanents on battlefield (by name)
    baylen = False
    kind = {"who": None}
    # Walking Ballista axis (only live when the variant list actually runs it)
    ballista_in_deck = any(nm == "Walking Ballista" for nm, _ in library)
    ballista_ctrs = 0

    def token_mult():
        f = 1
        for nm, mult in DOUBLERS.items():
            if nm in onb:
                f *= mult
        return min(f, M_CAP)

    def ctr_mult():
        f = 1
        for nm in CTR_DOUBLERS:
            if nm in onb:
                f *= 2
        return min(f, CTR_CAP)

    def note(who):
        if kind["who"] is None:
            kind["who"] = who

    def apply_burn(etb_count, T):
        """Purphoros/Impact pings on creature ETBs, x2 via Twinflame. hit_all (converge)."""
        if etb_count <= 0:
            return
        per = 0
        if "Purphoros, God of the Forge" in onb:
            per += 2 * etb_count
        if "Impact Tremors" in onb:
            per += 1 * etb_count
        if per <= 0:
            return
        if "Twinflame Tyrant" in onb:
            per *= 2
        before = tbl.decap
        tbl.hit_all(per, T)
        if tbl.decap is not None and before is None:
            note("burn")

    for T in range(1, TURNS + 1):
        if T in wipe_turns:                                   # board wipe resolves
            board_pow = ncre = new_pow = new_cre = 0
            onb = {n for n in onb if _survives_wipe(n, index)}
            baylen = False                                    # commander dies (recast not modelled)
            ballista_ctrs = 0                                 # Ballista is a creature — it dies too
        # matured: last turn's deploys attack now
        board_pow += new_pow; ncre += new_cre; new_pow = new_cre = 0
        land = g.begin_turn(T)
        g.deploy_rocks()
        lands_in = 1 if land else 0
        # land-ramp spells
        for rs, (cost, n) in RAMP.items():
            while g.has(rs) and g.avail >= cost:
                g.cast(rs, cost); g.lands += n; g.avail += n; lands_in += n
        # Baylen: commander, castable at 3. Modest token->mana ramp (cap 3) + a card/turn.
        if not baylen and g.avail >= 3:
            g.cast("Baylen, the Haymaker", 3); baylen = True; onb.add("Baylen")
            new_pow += 4; new_cre += 1
        if baylen and ncre >= 2:
            g.add_mana(min(3, ncre // 2))
        if baylen and ncre >= 3:
            g.draw(1)

        M = token_mult()
        etb = 0                  # creature ETBs this turn (for burn)
        haste_pow = haste_cre = 0
        toks_made = 0            # tokens created this turn (Rosie -> Ballista feed)

        def make_tokens(base, power, haste):
            nonlocal new_pow, new_cre, haste_pow, haste_cre, etb, toks_made
            n = min(base * token_mult(), TOK_CAP)
            etb += n
            toks_made += n
            if haste:
                haste_pow += power * n; haste_cre += n
            else:
                new_pow += power * n; new_cre += n

        # ---- DEVELOP: doublers -> pingers -> makers (order: doubler before makers) ----
        for dn in DOUBLERS:
            if dn not in onb and g.has(dn) and g.avail >= DOUBLER_COST[dn]:
                g.cast(dn, DOUBLER_COST[dn]); onb.add(dn)
                if dn == "Ojer Taq, Deepest Foundation":
                    new_pow += 6; new_cre += 1; etb += 1   # 6/6 body ETB
        # counter-doublers: only worth mana when the Ballista axis is live (keeps baseline identical)
        if ballista_in_deck:
            for dn, dc in CTR_DOUBLERS.items():
                if dn not in onb and g.has(dn) and g.avail >= dc:
                    g.cast(dn, dc); onb.add(dn)
        for pn, pc in (("Impact Tremors", 2), ("Purphoros, God of the Forge", 4),
                       ("Twinflame Tyrant", 5)):
            if pn not in onb and g.has(pn) and g.avail >= pc:
                g.cast(pn, pc); onb.add(pn)
                if pn == "Twinflame Tyrant":
                    new_pow += 3; new_cre += 1; etb += 1

        # combo pieces
        for cn, cc in (("Basking Broodscale", 2), ("Rosie Cotton of South Lane", 3),
                       ("Cathars' Crusade", 5)):
            if cn not in onb and g.has(cn) and g.avail >= cc:
                g.cast(cn, cc); onb.add(cn)
                if cn != "Cathars' Crusade":
                    new_pow += (2 if cn == "Basking Broodscale" else 1); new_cre += 1; etb += 1

        # burst makers (cheapest-first by cost)
        for nm, (cost, base, power, haste) in sorted(BURST.items(), key=lambda x: x[1][0]):
            if nm == "Decree of Justice":
                if g.has(nm) and g.avail >= 4:              # cycle {2}{W}=3, X soldiers
                    g.cast(nm, 3); make_tokens(max(0, g.avail), 1, False); g.avail = 0
                continue
            if g.has(nm) and g.avail >= cost:
                g.cast(nm, cost)
                make_tokens(base, power, haste)
                if nm in ("Hornet Queen", "Siege-Gang Commander"):
                    new_pow += 2; new_cre += 1; etb += 1    # the nontoken body
        # X-token spells that scale with leftover mana
        if g.has("Awaken the Woods") and g.avail >= 4:      # {X}{G}{G}: X dryad LANDS
            x = g.avail - 2; g.cast("Awaken the Woods", 2); g.avail = 0
            g.lands += min(x, 6)                            # they tap for mana next turns
            make_tokens(x, 1, False)
        if g.has("Forth Eorlingas!") and g.avail >= 4:      # {X}{R}{R}: X 2/2 haste trample
            x = g.avail - 2; g.cast("Forth Eorlingas!", 2); g.avail = 0
            make_tokens(x, 2, True)

        # per-turn engines (deploy if in hand; produce if already online)
        for en in ENGINES:
            if en not in onb and g.has(en) and g.avail >= ENGINE_COST[en]:
                g.cast(en, ENGINE_COST[en]); onb.add(en)
                if en == "Avenger of Zendikar":
                    new_pow += 5; new_cre += 1; etb += 1
                    make_tokens(g.lands, 0, False)          # a 0/1 plant per land
                elif en == "God-Eternal Oketra":
                    new_pow += 7; new_cre += 1; etb += 1
                else:
                    new_pow += 2; new_cre += 1; etb += 1
        # online engine production
        if "Adeline, Resplendent Cathar" in onb:
            make_tokens(3, 1, True)                         # 1/opp, tapped & attacking
        if "Suki, Kyoshi Warrior" in onb:
            make_tokens(1, 1, True)
        if "Hanweir Garrison" in onb:
            make_tokens(2, 1, True)                         # attack -> two 1/1 haste tokens
        if "Oviya Pashiri, Sage Lifecrafter" in onb:
            make_tokens(1, 1, False)                        # ~1 servo/turn
        if "Tendershoot Dryad" in onb:
            make_tokens(1, 1, False)
        if "God-Eternal Oketra" in onb:
            make_tokens(1, 4, False)                        # ~1 creature spell/turn
        if "Monastery Mentor" in onb:
            make_tokens(1, 1, False)                        # ~1 noncreature spell/turn
        if lands_in:
            if "Scute Swarm" in onb:
                make_tokens(2 if g.lands >= 6 else 1, 1, False)
            if "Rampaging Baloths" in onb:
                make_tokens(lands_in, 4, False)
            if "Felidar Retreat" in onb:
                make_tokens(lands_in, 2, False)
            if "Nesting Dragon" in onb:
                make_tokens(lands_in, 0, False)             # 0/2 egg: ETB only

        # owned-variant permanents (finishers / anthems)
        for pn, (pc, pw) in sorted(OWNED_PERMS.items(), key=lambda x: x[1][0]):
            if pn not in onb and g.has(pn) and g.avail >= pc:
                g.cast(pn, pc); onb.add(pn)
                if pw > 0:
                    new_pow += pw; new_cre += 1; etb += 1
                if pn == "Angel of Invention":
                    make_tokens(2, 1, False)                # fabricate: two 1/1 servos
        # Colossus of the Blood Age: ETB 3 to each opponent (owned-variant pinger)
        if "Colossus of the Blood Age" not in onb and g.has("Colossus of the Blood Age") \
                and g.avail >= 6:
            g.cast("Colossus of the Blood Age", 6); onb.add("Colossus of the Blood Age")
            new_pow += 6; new_cre += 1; etb += 1
            before = tbl.decap; tbl.hit_all(3 * (2 if "Twinflame Tyrant" in onb else 1), T)
            if tbl.decap is not None and before is None:
                note("burn")

        # ---- BURN axis (all ETBs this turn) ----
        apply_burn(etb, T)

        # ---- COMBO check ----
        combo_ready = ("Basking Broodscale" in onb
                       and ("Rosie Cotton of South Lane" in onb or "Cathars' Crusade" in onb)
                       and (etb > 0 or g.avail >= 2))          # a token made, or Adapt seed
        # Outlets: Purphoros/Impact (infinite ETB pings) or Walking Ballista — Broodscale+Rosie
        # makes infinite {C} (sac the Spawns) for {4}-activations, Broodscale+Cathars' puts the
        # per-ETB counters straight on Ballista. Either way: infinite pings.
        if use_combo and combo_ready and (
                "Purphoros, God of the Forge" in onb or "Impact Tremors" in onb
                or "Walking Ballista" in onb):
            note("combo"); tbl.kill_all(T); return tbl.decap, tbl.table, kind["who"]

        # ---- COMBAT step: Craterhoof/Finale alpha > Moonshaker focus > standing board ----
        cmult = 2 if "Twinflame Tyrant" in onb else 1
        atk_cre = ncre + haste_cre
        atk_pow = board_pow + haste_pow
        total_cre = ncre + new_cre + haste_cre               # X for pumps (incl. sick)
        fired = False

        def craterhoof_alpha():
            attackers = atk_cre + 1                           # +Craterhoof (haste)
            X = total_cre + 1
            swing = (atk_pow + 5) + X * attackers
            trample_distribute(tbl, swing * cmult, T)
            onb.add("Craterhoof Behemoth"); note("combat")

        # Finale {X}{G}{G} with X=8 (=10 mana) puts Craterhoof onto the battlefield (ETB alpha)
        if not fired and "Craterhoof Behemoth" not in onb and g.has("Finale of Devastation") \
                and g.avail >= 10 and g.fetch("Craterhoof Behemoth"):
            g.avail -= 10; g.cast("Craterhoof Behemoth", 0); craterhoof_alpha(); fired = True
        # Craterhoof hardcast for 8
        if not fired and g.has("Craterhoof Behemoth") and g.avail >= 8:
            g.cast("Craterhoof Behemoth", 8); craterhoof_alpha(); fired = True
        # Moonshaker: flying alpha but no trample -> focus-fire
        if not fired and g.has("Moonshaker Cavalry") and g.avail >= 8:
            g.cast("Moonshaker Cavalry", 8); onb.add("Moonshaker Cavalry")
            X = total_cre + 1
            swing = (atk_pow + 6) + X * (atk_cre + 1)
            before = tbl.decap; tbl.hit_focus(swing * cmult, T)
            if tbl.decap is not None and before is None:
                note("combat")
            fired = True
        # Triumph of the Hordes: +1/+1 + trample + infect -> parallel life-10 table
        if not fired and g.has("Triumph of the Hordes") and g.avail >= 4 and atk_cre > 0:
            g.cast("Triumph of the Hordes", 4)
            swing = (atk_pow + atk_cre)                       # +1/+1 to each attacker
            before = inf.decap; trample_distribute(inf, swing * cmult, T)
            if inf.decap is not None and before is None:
                note("combat-infect")
            fired = True
        # owned-variant finishers/anthems: flat team pump, trample, table-wide (Legion Loyalty),
        # Jazal activation. Cathars' Crusade is a static proxy (+2) for its accrued counters —
        # it lives in BOTH lists, so this also credits the primary list's previously-omitted anthem.
        team_plus = 0
        for a, amt in (("Elesh Norn, Grand Cenobite", 2), ("Intangible Virtue", 1),
                       ("Angel of Invention", 1), ("Cathars' Crusade", 2),
                       ("Salvation Colossus", 2), ("Blossoming Bogbeast", 2)):
            if a in onb:
                team_plus += amt
        trample = "Blossoming Bogbeast" in onb
        table_wide = "Legion Loyalty" in onb
        jazal = atk_cre if ("Jazal Goldmane" in onb and g.pay(5)) else 0
        if not fired and atk_cre > 0 and (team_plus or table_wide or trample or jazal):
            swing = (atk_pow + (team_plus + jazal) * atk_cre) * cmult
            before = tbl.decap
            if table_wide:
                tbl.hit_all(swing, T)                        # myriad -> a board-copy at each opp
            elif trample:
                trample_distribute(tbl, swing, T)
            else:
                tbl.hit_focus(swing, T)
            if tbl.decap is not None and before is None:
                note("combat")
            fired = True

        # standing board focus-fire
        if not fired and atk_pow > 0:
            before = tbl.decap; tbl.hit_focus(atk_pow * cmult, T)
            if tbl.decap is not None and before is None:
                note("combat")

        # ---- WALKING BALLISTA phase (post-combat, leftover mana = Baylen's battery) ----
        if ballista_in_deck:
            cm = ctr_mult()
            # cast with leftover mana: {X}{X}, enters with X*cm counters (doublers apply to
            # enter-with counters per the Doubling Season ruling)
            if "Walking Ballista" not in onb and g.has("Walking Ballista") and g.avail >= 4:
                x = g.avail // 2
                g.cast("Walking Ballista", 2 * x); onb.add("Walking Ballista")
                ballista_ctrs += x * cm
                # (its own ETB Purphoros ping not credited — fires after apply_burn; slow bias)
            if "Walking Ballista" in onb:
                # feeds: Cathars' (a counter per creature ETB), Rosie (per token created —
                # only targets Ballista when she isn't sustaining the Broodscale loop),
                # and {4}-activations off leftover mana
                if "Cathars' Crusade" in onb:
                    ballista_ctrs += etb * cm
                if "Rosie Cotton of South Lane" in onb and "Basking Broodscale" not in onb:
                    ballista_ctrs += toks_made * cm
                acts = g.avail // 4
                if acts:
                    g.pay(4 * acts); ballista_ctrs += acts * cm
                # ping: remove counters, 1 damage each, any target -> spread across the table.
                # Keep 1 counter (a 0/0 Ballista dies) unless dumping everything is lethal.
                remaining = sum(max(0, tbl.life - d) for d in tbl.dmg)
                spend = ballista_ctrs if ballista_ctrs >= remaining else max(0, ballista_ctrs - 1)
                if spend > 0:
                    ballista_ctrs -= spend
                    before = tbl.decap; trample_distribute(tbl, spend, T)
                    if tbl.decap is not None and before is None:
                        note("ping")

        # merge infect clocks into the reported decap/table (earliest across both)
        decap = min([d for d in (tbl.decap, inf.decap) if d is not None], default=None)
        table = min([d for d in (tbl.table, inf.table) if d is not None], default=None)
        if table is not None:
            return decap, table, kind["who"]

    decap = min([d for d in (tbl.decap, inf.decap) if d is not None], default=None)
    table = min([d for d in (tbl.table, inf.table) if d is not None], default=None)
    return decap, table, kind["who"]


def _run(index, aliases, trials, use_combo, title, deck=None):
    print(f"\n### CLOCK — Mass Production {title}   trials={trials} seed={SEED}")
    print("    decap = first opponent dead · table = all three · kinds: combo/burn/combat.")
    library, commander = slc.load_parsed(deck or DECK, index, aliases)
    rng = random.Random(SEED)
    raw = [goldfish_kill(library, commander, index, rng, use_combo=use_combo)
           for _ in range(trials)]
    res = [(d, t) for d, t, _ in raw]
    slc.report_clock(res, SHOW, TURNS, trials)
    kinds = {}
    for _, _, k in raw:
        kinds[k] = kinds.get(k, 0) + 1
    total = sum(kinds.values())
    mix = "  ".join(f"{k or 'none'} {100.0*v/total:.0f}%"
                    for k, v in sorted(kinds.items(), key=lambda x: -x[1]))
    print(f"  first-kill mixture: {mix}")


def mode_clock(index, aliases, trials, deck=None):
    _run(index, aliases, trials, use_combo=True, title="kill-turn goldfish (all lines)", deck=deck)
    print("\n  Primary claim 'T7/T10'; prior lists stay runnable via --deck archive/old_decklists/....")


def mode_nocombo(index, aliases, trials, deck=None):
    _run(index, aliases, trials, use_combo=False, title="FAIR (combo disabled)", deck=deck)
    print("\n  Fair-deck clock: combat + burn only, Broodscale infinite switched off.")


def mode_wipe(index, aliases, trials, deck=None):
    """DURABILITY: a creature board-wipe resolves on turn W; measure the kill clock AFTER it.
    The table-clock SLIP vs 'no wipe' is the recovery cost — the Conversion Check Durability
    checkpoint, measured per decklist (the goldfish clock can't see it)."""
    library, commander = slc.load_parsed(deck or DECK, index, aliases)
    print(f"\n### DURABILITY — Mass Production wipe-recovery   trials={trials} seed={SEED}")
    print(f"    deck: {(deck or DECK).name}   ·   wipe = creatures only (enchantment/artifact")
    print("    doublers, anthems, Impact Tremors, indestructible Purphoros survive).")
    base_tm = None
    for label, wt in (("no wipe", ()), ("wipe @ T6", (6,)), ("wipe @ T8", (8,)),
                      ("wipe @ T6 & T9", (6, 9))):
        rng = random.Random(SEED)
        raw = [goldfish_kill(library, commander, index, rng, use_combo=True, wipe_turns=wt)
               for _ in range(trials)]
        res = [(d, t) for d, t, _ in raw]
        dm, tm = slc.median(res, 0), slc.median(res, 1)
        nt = slc.never_pct(res, 1, trials)
        kinds = {}
        for _, _, k in raw:
            kinds[k] = kinds.get(k, 0) + 1
        tot = sum(kinds.values())
        mix = " ".join(f"{(k or 'none')}:{100*v/tot:.0f}"
                       for k, v in sorted(kinds.items(), key=lambda x: -x[1]))
        tnum = int(tm[1:]) if tm.startswith("T") else None
        if base_tm is None:
            base_tm = tnum
        slip = f"+{tnum-base_tm}" if (tnum is not None and base_tm is not None) else "—"
        print(f"  {label:16} decap {dm:>4}  table {tm:>4} (slip {slip})  never-table {nt:4.0f}%   [{mix}]")
    print("\n  Read: the table-clock SLIP after a wipe is the recovery cost. A list that keeps a")
    print("  board-independent axis (Purphoros/Impact burn, Broodscale combo) slips less.")


def mode_ballista(index, aliases, trials, deck=None):
    """LEVER TEST (WF_Kill_Window_Lab Stage 3): does swapping in Walking Ballista move the
    clock or the wipe recovery? A/B: baseline vs (-weakest flex slot +Walking Ballista).
    Pre-registered prior: median clock UNCHANGED (combat already carries T7/T10); the ping
    axis should show up as mixture share + a combo outlet, and wipe recovery should NOT
    improve (Ballista is a creature — it dies to the wrath). The lab is allowed to falsify."""
    library, commander = slc.load_parsed(deck or DECK, index, aliases)
    names = {nm for nm, _ in library}
    cut = "Battle Menu" if "Battle Menu" in names else "Harmonize"
    variant = slc.build_lib(library, index, [cut], ["Walking Ballista"])
    print(f"\n### LEVER — Walking Ballista A/B   deck={(deck or DECK).name}   "
          f"swap: -{cut} +Walking Ballista   trials={trials} seed={SEED}")
    for label, lib in (("baseline", library), ("+Ballista", variant)):
        for wlabel, wt in (("", ()), (" · wipe@T6", (6,))):
            rng = random.Random(SEED)
            raw = [goldfish_kill(lib, commander, index, rng, use_combo=True, wipe_turns=wt)
                   for _ in range(trials)]
            res = [(d, t) for d, t, _ in raw]
            dm, tm = slc.median(res, 0), slc.median(res, 1)
            nt = slc.never_pct(res, 1, trials)
            kinds = {}
            for _, _, k in raw:
                kinds[k] = kinds.get(k, 0) + 1
            tot = sum(kinds.values())
            mix = " ".join(f"{(k or 'none')}:{100*v/tot:.0f}"
                           for k, v in sorted(kinds.items(), key=lambda x: -x[1]))
            print(f"  {label+wlabel:22} decap {dm:>4}  table {tm:>4}  never-table {nt:4.0f}%   [{mix}]")
    print("\n  Read the DELTA rows (baseline vs +Ballista, with and without a T6 wrath).")


if __name__ == "__main__":
    slc.run_cli(__doc__, {"clock": mode_clock, "nocombo": mode_nocombo, "wipe": mode_wipe,
                          "ballista": mode_ballista},
                default_trials=40000)
