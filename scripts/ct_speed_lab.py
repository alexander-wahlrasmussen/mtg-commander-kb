#!/usr/bin/env python3
"""ct_speed_lab.py — The Calamity Tax (Glarb, Calamity's Augur) kill-turn lab.

The missing piece of proposals/Calamity_Tax_Speed_Curve_Analysis.md (2026-06-08):
that analysis measured finisher AVAILABILITY and showed the kill is mana-gated,
but the Summary's "T7-9 goldfish" was only corroborated, never goldfished
(status ◐ in proposals/Framework_Clock_Gap_2026-06-09.md). This lab runs the
actual kill-turn Monte Carlo for three variants:

  V1  committed list        decks/calamity-tax-20260405-061741.txt
  V2  31-May oppression     -Savvy Trader -Flash Photography -Druid of
                            Purification -High Fae Trickster -Starfield
                            Vocalist  +Exsanguinate +Sheoldred +Mystic Remora
                            +Bloom Tender +Carpet of Flowers
  V4  reanimator lean       same five cuts + -Mirrorform; +Exsanguinate
                            +The Scarab God +Final Parting +Jarad +Lord of
                            Extinction +Victimize
                            (proposals/Calamity_Tax_Reanimator_Pivot.md —
                            claims the fast line lands "~T5-6")

Built on scripts/speed_lab_core.py (first lab on the shared harness). Goldfish
clock, 3 opponents @ 40, sorcery speed. Kill lines modelled:

  X-DRAIN  Torment of Hailfire / Exsanguinate. Goldfish dummies hold no
           permanents and no cards, so Torment is forced 3-life-per-iteration
           (ceiling — real opponents dodge with chaff; text verified).
           Lethal-only casting unless both X-drains are held (then the spare
           chips at X>=5). Mana engine: lands + Sol Ring + ramp spells
           (Farseek/Nature's Lore/Three Visits +1 land, Skyshroud Claim +2,
           Hour of Promise +2 with Coffers+Urborg fetch priority, Tempt with
           Discovery +1 any land), Azusa/Exploration/Oracle extra drops,
           Lotus Cobra/Nissa landfall mana, Cabal Coffers+Urborg = lands-2
           extra black each turn, Glarb top-of-library land plays and MV>=4
           casts, Sylvan Library +1 card/turn. V2 adds Bloom Tender (3 mana
           with Glarb out per Vivid, else 1) and Carpet of Flowers (+2/turn —
           POD-META assumption: the matchup matrix pod is islands-heavy;
           strict goldfish would be 0).

  COPY     kicked Rite of Replication (9) / Doppelgang (X=2, 8) on a board
           death-drainer. On Gray Merchant: 5 token ETBs, each draining
           devotion-to-black counted AFTER all five enter (+10 pips) — the
           ~60-per-opponent table kill. On Kokusho (legendary): 5 tokens die
           to the legend rule = 25/opponent. On Archon: 5 ETBs x 3 to one
           target. Devotion counts only modelled permanents' B pips
           (conservative).

  REANIM   Glarb's {T}: Surveil 2 bins fat targets (the only V1/V2 enabler);
           V4 adds Final Parting (bin Gray/Kokusho AND fetch Reanimate/Rite),
           Victimize (sac fodder, return 2 fats tapped — ETBs still fire),
           The Scarab God (upkeep drain = Zombies; {2}{U}{B}: eternalize a
           binned Gray as a 4/4 Zombie — ETB drain fires, mana cost copied).
           Agadeem's Awakening mass-reanimates distinct MVs. Reanimate {B}.

  JARAD    V4: Jarad + Lord of Extinction; {1}{B}{G} sac Lord = each opponent
           loses Lord's power = cards in OUR graveyard only (goldfish dummies
           have empty yards — conservative, real tables 2-3x bigger).

  COMBAT   all modelled creatures attack the focused opponent from their
           second turn (Glarb stays back to surveil); Archon adds its attack
           trigger. Unblocked throughout — pure ceiling.

HEURISTIC, NOT a rules engine. Not modelled (all real, all small or
goldfish-dead): Seedborn Muse (kill is sorcery-speed), counterspell suite,
Meathook/Toxic/Culling sweepers, Mystic Remora draws (opponents cast nothing
in goldfish — the point of the V2 comparison), Sheoldred's drain-on-their-draw,
Noxious Revival, Timeless Witness, Mirrorform/Flash Photography copies,
Valley Floodcaller, V.A.T.S. Trust curve shapes and variant deltas.

Card text verified via card_lookup.py 2026-06-10: Glarb, Torment, Exsanguinate,
Rite of Replication, Doppelgang, Kokusho, Gray Merchant, Archon of Cruelty,
Reanimate, Agadeem's Awakening, Final Parting, Victimize, Jarad, Lord of
Extinction, The Scarab God, Cabal Coffers, Urborg, Bloom Tender, Sheoldred,
Carpet of Flowers, Mystic Remora, ramp suite, GSZ/Chord/Finale, sweepers.

Writeup: proposals/Calamity_Tax_Kill_Turn_Lab_2026-06-10.md
Data: collection/oracle-cards.json (refresh via update_scryfall_data.py)
"""
import importlib.util
import random
from pathlib import Path

_spec = importlib.util.spec_from_file_location(
    "speed_lab_core", Path(__file__).parent / "speed_lab_core.py")
core = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(core)
ds = core.ds

ROOT = Path(__file__).parent.parent
DECK = ROOT / "decks" / "calamity-tax-20260405-061741.txt"
SEED = 12345
TURNS = 14
SHOW = [4, 5, 6, 7, 8, 9, 10, 12, 14]

V2_OUT = ["Savvy Trader", "Flash Photography", "Druid of Purification",
          "High Fae Trickster", "Starfield Vocalist"]
V2_IN = ["Exsanguinate", "Sheoldred, the Apocalypse", "Mystic Remora",
         "Bloom Tender", "Carpet of Flowers"]
V4_OUT = V2_OUT + ["Mirrorform"]
V4_IN = ["Exsanguinate", "The Scarab God", "Final Parting",
         "Jarad, Golgari Lich Lord", "Lord of Extinction", "Victimize"]

# ---- card names ------------------------------------------------------------
TORMENT = "Torment of Hailfire"
EXSANG = "Exsanguinate"
RITE = "Rite of Replication"
DOPPEL = "Doppelgang"
GRAY = "Gray Merchant of Asphodel"
KOKUSHO = "Kokusho, the Evening Star"
ARCHON = "Archon of Cruelty"
REANIMATE = "Reanimate"
AGADEEM = "Agadeem's Awakening"
PARTING = "Final Parting"
VICTIMIZE = "Victimize"
JARAD = "Jarad, Golgari Lich Lord"
LORD = "Lord of Extinction"
SCARAB = "The Scarab God"
COFFERS = "Cabal Coffers"
URBORG = "Urborg, Tomb of Yawgmoth"
DEMONIC = "Demonic Tutor"
SYLVAN = "Sylvan Library"
TENDER = "Bloom Tender"
CARPET = "Carpet of Flowers"

ROCKS = {"Sol Ring": (1, 2)}
RAMP1 = {"Farseek": 2, "Nature's Lore": 2, "Three Visits": 2}   # +1 land
RAMP2 = {"Skyshroud Claim": 4}                                  # +2 lands
EXTRA_DROP = {"Azusa, Lost but Seeking": (3, 2), "Exploration": (1, 1),
              "Oracle of Mul Daya": (4, 1)}                     # (cost, drops)
LANDFALL = {"Lotus Cobra": 2, "Nissa, Resurgent Animist": 3}    # +1/land
FATS = {GRAY: 5, KOKUSHO: 6, ARCHON: 8}                          # name -> MV
# B-pips of modelled permanents (devotion for Gray's drain)
PIPS = {GRAY: 2, KOKUSHO: 2, ARCHON: 2, "Sheoldred, the Apocalypse": 2,
        JARAD: 2, LORD: 1, SCARAB: 1, "Glarb, Calamity's Augur": 1}
POWER = {GRAY: 2, KOKUSHO: 5, ARCHON: 6, "Sheoldred, the Apocalypse": 4,
         SCARAB: 5, "Lotus Cobra": 2, "Nissa, Resurgent Animist": 3,
         TENDER: 1, "Azusa, Lost but Seeking": 1, "Oracle of Mul Daya": 2}
CREATURE_TUTORS = {"Chord of Calling": 8, "Finale of Devastation": 7}  # -> Gray


def kill_turns(library, rng, v4=False):
    """One trial. Returns (decap, table, via). via in
    {'xdrain','copy','jarad','drain','combat',None}."""
    g = core.Goldfish(library, rng, rocks=ROCKS)
    tb = core.Table()
    glarb = False
    coffers = urborg = False
    sylvan = carpet = False
    extra_drops = 0                # standing extra land drops
    landfall_mana = 0              # standing +mana per land entering
    board = []                     # names of modelled permanents in play
    cast_turn = {}                 # name -> turn it entered
    zombies = 0                    # Scarab upkeep count (Gray + tokens)
    gray_tokens = 0
    chip_used = False
    lands_in_play_names = set()

    def devotion():
        return sum(PIPS.get(n, 0) for n in board) + 2 * gray_tokens

    def enter(nm, T):
        board.append(nm)
        cast_turn[nm] = T

    def gray_etb(k, T):
        """k Gray ETBs entering together (tokens already counted)."""
        tb.hit_all(k * devotion(), T)

    def land_entered(n=1):
        nonlocal landfall_mana
        g.lands += n
        g.add_mana(landfall_mana * n)

    for T in range(1, TURNS + 1):
        played = g.begin_turn(T)
        if played:
            lands_in_play_names.add(played)
            g.add_mana(landfall_mana)
        # Coffers + Urborg: one tap, lands-2 black (counted off begin-of-turn lands)
        if coffers and urborg:
            g.add_mana(max(0, g.lands - 2))
        if carpet:
            g.add_mana(2)          # pod-meta assumption, see module docstring
        if TENDER in board and cast_turn[TENDER] < T:
            g.add_mana(3 if glarb else 1)
        if sylvan:
            g.draw(1)
        # Scarab upkeep drain
        if SCARAB in board and cast_turn[SCARAB] < T and zombies:
            tb.hit_all(zombies, T)
            if tb.done:
                return tb.decap, tb.table, "drain"

        # extra land drops from hand
        for _ in range(extra_drops):
            extra = g.begin_turn.__self__  # noqa - readability: reuse pure-land pref
            li = next((i for i, (_, r) in enumerate(g.hand) if ds.is_pure_land(r)), None)
            if li is None:
                li = next((i for i, (_, r) in enumerate(g.hand) if ds.is_land(r)), None)
            if li is None:
                break
            lands_in_play_names.add(g.hand[li][0])
            g.hand.pop(li)
            land_entered()
            g.add_mana(1)          # entered untapped this turn

        g.deploy_rocks()

        # ---- Glarb: surveil 2 (bin fats), then top-of-library velocity ------
        if glarb:
            for _ in range(2):     # surveil 2: bin fat reanimation targets
                if g.ptr < len(g.deck):
                    nm = g.deck[g.ptr][0]
                    if nm in FATS or (v4 and nm == LORD):
                        g.yard.append(g.deck[g.ptr]); g.ptr += 1
                    # non-fats stay on top (drawn normally)
                    else:
                        break
            moved = True
            while moved and g.ptr < len(g.deck):
                moved = False
                nm, rec = g.deck[g.ptr]
                if ds.is_pure_land(rec) and extra_drops == 0 and played is None:
                    g.ptr += 1
                    lands_in_play_names.add(nm)
                    land_entered(); g.add_mana(1)
                    played = nm
                    moved = True
                elif rec["cmc"] >= 4 and not ds.is_land(rec) and g.avail >= rec["cmc"]:
                    g.hand.append((nm, rec)); g.ptr += 1
                    moved = True

        # ---- ramp spells -----------------------------------------------------
        for nm, cost in RAMP1.items():
            if g.cast(nm, cost):
                land_entered()
        if g.cast("Skyshroud Claim", 4):
            land_entered(2)
        if g.cast("Hour of Promise", 5):     # fetch Coffers/Urborg first
            for want in (COFFERS, URBORG):
                if want not in lands_in_play_names and g.fetch(want):
                    i = g.in_hand(want)
                    g.hand.pop(i)
                    lands_in_play_names.add(want)
            land_entered(2)
        if g.cast("Tempt with Discovery", 4):
            for want in (COFFERS, URBORG, None):
                if want is None:
                    land_entered()
                    break
                if want not in lands_in_play_names and g.fetch(want):
                    i = g.in_hand(want)
                    g.hand.pop(i)
                    lands_in_play_names.add(want)
                    land_entered()
                    break
        coffers = COFFERS in lands_in_play_names
        urborg = URBORG in lands_in_play_names
        for nm, (cost, drops) in EXTRA_DROP.items():
            if nm not in board and g.cast(nm, cost):
                enter(nm, T)
                extra_drops += drops
        for nm, cost in LANDFALL.items():
            if nm not in board and g.cast(nm, cost):
                enter(nm, T)
                landfall_mana += 1

        # ---- commander / value ----------------------------------------------
        if not glarb and g.pay(3):
            glarb = True
            enter("Glarb, Calamity's Augur", T)
        if not sylvan and g.cast(SYLVAN, 2):
            sylvan = True
        if not carpet and g.cast(CARPET, 1):
            carpet = True
        if TENDER not in board and g.cast(TENDER, 2):
            enter(TENDER, T)
        if g.cast("Sheoldred, the Apocalypse", 4):
            enter("Sheoldred, the Apocalypse", T)

        # ---- Demonic Tutor decision ------------------------------------------
        if g.has(DEMONIC) and g.avail >= 2:
            want = None
            if GRAY in board and not g.has(RITE):
                want = RITE
            elif any(g.in_yard(f) for f in FATS) and not g.has(REANIMATE):
                want = REANIMATE
            elif not (g.has(TORMENT) or g.has(EXSANG)):
                want = TORMENT if any(nm == TORMENT for nm, _ in g.deck[g.ptr:]) else EXSANG
            if want and g.fetch(want):
                g.hand.pop(g.in_hand(DEMONIC))
                g.avail -= 2

        # ---- reanimator package ----------------------------------------------
        if v4 and g.cast(PARTING, 5):        # bin Gray, fetch Rite (or Reanimate)
            target = GRAY if not (GRAY in board or g.in_yard(GRAY)) else KOKUSHO
            if g.fetch(target):
                g.yard.append(g.hand.pop(g.in_hand(target)))
            grab = RITE if not g.has(RITE) else REANIMATE
            g.fetch(grab)
        if g.has(REANIMATE) and g.avail >= 1:
            for f in (GRAY, KOKUSHO, ARCHON):
                if g.in_yard(f):
                    g.hand.pop(g.in_hand(REANIMATE)); g.avail -= 1
                    g.take_yard(f)
                    enter(f, T)
                    if f == GRAY:
                        zombies += 1
                        gray_etb(1, T)
                    elif f == ARCHON:
                        tb.hit_focus(3, T); g.draw(1)
                    break
        if v4 and g.has(VICTIMIZE) and g.avail >= 3:
            in_yard_fats = [f for f in (GRAY, KOKUSHO, ARCHON, LORD) if g.in_yard(f)]
            fodder = [n for n in board if n in LANDFALL or n == TENDER]
            if len(in_yard_fats) >= 2 and fodder:
                g.hand.pop(g.in_hand(VICTIMIZE)); g.avail -= 3
                board.remove(fodder[0])
                if fodder[0] in LANDFALL:
                    landfall_mana -= 1
                for f in in_yard_fats[:2]:
                    g.take_yard(f)
                    enter(f, T)
                    if f == GRAY:
                        zombies += 1
                        gray_etb(1, T)
                    elif f == ARCHON:
                        tb.hit_focus(3, T); g.draw(1)
        if g.has(AGADEEM):                    # X+BBB mass reanimate, distinct MVs
            in_yard_fats = sorted({FATS[f] for f in FATS if g.in_yard(f)})
            if len(in_yard_fats) >= 2:
                cost = 3 + max(in_yard_fats)
                if g.avail >= cost:
                    g.hand.pop(g.in_hand(AGADEEM)); g.avail -= cost
                    for f in (GRAY, KOKUSHO, ARCHON):
                        if g.in_yard(f):
                            g.take_yard(f)
                            enter(f, T)
                            if f == GRAY:
                                zombies += 1
                                gray_etb(1, T)
                            elif f == ARCHON:
                                tb.hit_focus(3, T); g.draw(1)
        # creature tutors put Gray on the battlefield directly
        for nm, cost in CREATURE_TUTORS.items():
            if GRAY not in board and g.has(nm) and g.avail >= cost:
                if g.fetch(GRAY):
                    g.hand.pop(g.in_hand(nm)); g.avail -= cost
                    g.hand.pop(g.in_hand(GRAY))
                    enter(GRAY, T)
                    zombies += 1
                    gray_etb(1, T)
                    break

        # ---- hardcast fats ----------------------------------------------------
        for f, mv in FATS.items():
            if f not in board and g.cast(f, mv):
                enter(f, T)
                if f == GRAY:
                    zombies += 1
                    gray_etb(1, T)
                elif f == ARCHON:
                    tb.hit_focus(3, T); g.draw(1)
        if v4:
            if JARAD not in board and g.cast(JARAD, 4):
                enter(JARAD, T)
            if LORD not in board and g.cast(LORD, 5):
                enter(LORD, T)
            if SCARAB not in board and g.cast(SCARAB, 5):
                enter(SCARAB, T)
            # GSZ can fetch Lord (green)
            if LORD not in board and g.has("Green Sun's Zenith") and g.avail >= 6:
                if g.fetch(LORD):
                    g.hand.pop(g.in_hand("Green Sun's Zenith")); g.avail -= 6
                    g.hand.pop(g.in_hand(LORD))
                    enter(LORD, T)

        # ---- copy kills --------------------------------------------------------
        if GRAY in board and g.cast(RITE, 9):
            gray_tokens += 5
            zombies += 5
            gray_etb(5, T)                       # devotion counted after entry
            if tb.done:
                return tb.decap, tb.table, "copy"
        elif KOKUSHO in board and g.cast(RITE, 9):
            tb.hit_all(25, T)                    # 5 legend-rule deaths
            if tb.done:
                return tb.decap, tb.table, "copy"
        elif ARCHON in board and g.cast(RITE, 9):
            tb.hit_focus(15, T); g.draw(5)
            if tb.done:
                return tb.decap, tb.table, "copy"
        if GRAY in board and g.cast(DOPPEL, 8):  # X=2 on Gray
            gray_tokens += 2
            zombies += 2
            gray_etb(2, T)
            if tb.done:
                return tb.decap, tb.table, "copy"
        # Scarab eternalize a binned Gray
        if SCARAB in board and g.in_yard(GRAY) and g.avail >= 4:
            g.avail -= 4
            g.take_yard(GRAY)
            gray_tokens += 1
            zombies += 1
            gray_etb(1, T)
            if tb.done:
                return tb.decap, tb.table, "drain"
        # Jarad + Lord
        if v4 and JARAD in board and LORD in board and g.avail >= 3:
            g.avail -= 3
            board.remove(LORD)
            yard_n = len(g.yard) + 1             # Lord joins the yard it counts
            tb.hit_all(yard_n, T)
            g.yard.append((LORD, {}))
            if tb.done:
                return tb.decap, tb.table, "jarad"

        # ---- X-drain ------------------------------------------------------------
        alive = [d for d in tb.dmg if d < tb.life]
        worst = max((tb.life - d for d in tb.dmg if d < tb.life), default=0)
        for nm, per in ((TORMENT, 3), (EXSANG, 1)):
            if not g.has(nm) or not alive:
                continue
            lethal_x = -(-worst // per)
            if g.avail >= lethal_x + 2:
                g.hand.pop(g.in_hand(nm)); g.avail -= lethal_x + 2
                tb.kill_all(T)
                return tb.decap, tb.table, "xdrain"
            both = g.has(TORMENT) and g.has(EXSANG)
            if both and not chip_used and g.avail >= 7 and per == 3:
                x = g.avail - 2
                g.hand.pop(g.in_hand(nm)); g.avail = 0
                chip_used = True
                tb.hit_all(x * per, T)
                if tb.done:
                    return tb.decap, tb.table, "xdrain"

        # ---- combat ---------------------------------------------------------------
        atk = sum(POWER.get(n, 0) for n in board
                  if cast_turn[n] < T and n != "Glarb, Calamity's Augur")
        atk += 2 * gray_tokens
        if v4 and JARAD in board and cast_turn[JARAD] < T:
            atk += 2 + sum(1 for _, r in g.yard if "Creature" in r.get("type_line", ""))
        if v4 and LORD in board and cast_turn[LORD] < T:
            atk += len(g.yard)
        if ARCHON in board and cast_turn[ARCHON] < T:
            tb.hit_focus(3, T); g.draw(1)        # attack trigger
        if atk:
            tb.hit_focus(atk, T)
            if tb.done:
                return tb.decap, tb.table, "combat"
    return tb.decap, tb.table, None


def mode_clock(index, aliases, trials):
    print(f"\n### CLOCK — goldfish kill-turn Monte Carlo   trials={trials} seed={SEED}")
    print("    3 opponents @40. Drains hit all; combat/Archon focus-fire. Unblocked")
    print("    ceiling. Summary claim under test: 'Goldfish T7-9' (status ◐).")
    print("    V4 claim under test: fast reanimator line lands '~T5-6'.\n")
    base, commander = core.load_parsed(DECK, index, aliases)
    variants = [
        ("V1 committed", base, False),
        ("V2 31-May oppression", core.build_lib(base, index, V2_OUT, V2_IN), False),
        ("V4 reanimator lean", core.build_lib(base, index, V4_OUT, V4_IN), True),
    ]
    print("  metric".ljust(42) + "".join(f"{t:>6}" for t in SHOW) + "   median")
    for tag, lib, v4 in variants:
        rng = random.Random(SEED)
        res = [kill_turns(lib, rng, v4) for _ in range(trials)]
        print(core.row(f"{tag}  decap", core.cum(res, 0, SHOW), SHOW)
              + f"   {core.median(res, 0)}")
        print(core.row(" " * len(tag) + "  table", core.cum(res, 1, SHOW), SHOW)
              + f"   {core.median(res, 1)}")
        n = len(res)
        via = {}
        for r in res:
            if r[1] is not None:
                via[r[2]] = via.get(r[2], 0) + 1
        kills = sum(via.values())
        if kills:
            parts = ", ".join(f"{k} {100.0 * v / kills:.0f}%"
                              for k, v in sorted(via.items(), key=lambda x: -x[1]))
            print(f"    table kills by line: {parts}   (killed {100.0 * kills / n:.0f}% of trials in {TURNS}T)")
    print()


def main():
    core.run_cli(__doc__, {"clock": mode_clock})


if __name__ == "__main__":
    main()
