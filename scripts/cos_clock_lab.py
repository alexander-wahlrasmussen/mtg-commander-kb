#!/usr/bin/env python3
"""cos_clock_lab.py — Curse of the Scarab (The Scarab God) KILL-TURN goldfish.

Kill-Window Lab Sweep, deck 5 of 10 (proposals/Kill_Window_Lab_Sweep_2026-06-13.md).
Summary claims "Goldfish T7-9". Built on speed_lab_core.py.

KILL SHAPE: drain-led CONVERGE with a combat focus-fire side (mixed, but the fast
lines converge — like Genome/Radiation/Crystal Sickness, not a pure combat deck):

  DRAIN  (hit_all, CONVERGE):
    * Scarab God upkeep: each opponent loses X = Zombies you control, every upkeep
      (no mana/attack). The PRIMARY clock. (Scarab is a God, not a Zombie — it does
      NOT count itself and lords do NOT pump it.)
    * Gray Merchant of Asphodel ETB: each opponent loses X = your devotion to black;
      recurrable via the reanimation suite (Reanimate/Necromancy/Living Death).
    * Shepherd of Rot {T}: each player (you too) loses 1 per Zombie on the battlefield.
    * Plague Belcher: each opponent loses 1 per OTHER Zombie death (with a sac outlet).
  COMBO  (kill_all): Warren Soultrader + Gravecrawler + Plague Belcher — sac Gravecrawler
    to Soultrader (Treasure, lose 1), recast for {B}, Plague Belcher pings each
    opponent 1 per loop; ~39 loops at 40 life => whole table. Assembled = kill_all.
  COMBAT (hit_focus, DIVERGE): lord-pumped Zombies (Death Baron/Warchief/etc.) swing;
    decap accelerant. Unblocked goldfish convention.

THE ENGINE IS ZOMBIE COUNT + DRAW (the cs lesson). Zombie count drives the Scarab
drain; token generators multiply it and draw refills the hand to keep deploying:
  * Diregraf Colossus: each Zombie SPELL cast -> a tapped 2/2 token.
  * Necroduality: each NONTOKEN Zombie ETB -> a token copy.
  * Grave Titan (a Giant, not a Zombie): ETB + each attack -> two 2/2 Zombie tokens.
  * Wilhelt: a Zombie death -> a 2/2 decayed token (folded into the loop/combat).
  * Kindred Discovery (Zombie): every Zombie ETB OR attack -> draw (incl tokens).
  * Rooftop Storm: Zombie creature spells cost {0} (Scarab God is NOT a Zombie spell).
  * Reanimation (Entomb/Buried Alive -> Reanimate/Necromancy/Living Death) cheats
    Gray Merchant / Grave Titan onto the board early and recurs Gary's drain.

HEURISTIC, not a rules engine — coarse like rs_clock_lab. Zombie count is an integer
engine variable; token multipliers are flags; devotion is summed black pips of black
permanents deployed (oracle mana_cost). Mana = lands + rocks. Draw is capped/turn to
bound the loop. Goldfish damage unblocked, no opposing interaction, no removal of the
Scarab God. Trust the SHAPE and front edge, not the second decimal. decap/table split.

Data: collection/oracle-cards.json   ·   Writeup: proposals/Curse_of_the_Scarab_Clock_Lab_2026-06-13.md
"""
import importlib.util
import json
import random
from pathlib import Path

ROOT = Path(__file__).parent.parent
_spec = importlib.util.spec_from_file_location("speed_lab_core", Path(__file__).parent / "speed_lab_core.py")
slc = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(slc)
ds = slc.ds

DECK = ROOT / "decks" / "curse-of-the-scarab-20260510-215526.txt"
SEED = 20260613
TURNS = 14
SHOW = [5, 6, 7, 8, 9, 10, 12, 14]
DRAW_CAP = 14

ROCKS = {"Sol Ring": (1, 2), "Arcane Signet": (2, 1), "Dimir Signet": (2, 1),
         "Fellwar Stone": (2, 1), "Mind Stone": (2, 1), "Talisman of Dominance": (2, 1)}
# per-Zombie power bonus from lords/anthems (Mikaeus pumps all non-Humans incl Zombies)
LORDS = {"Death Baron": 1, "Lord of the Accursed": 1, "Undead Warchief": 2,
         "Cemetery Reaper": 1, "Narfi, Betrayer King": 1, "Mikaeus, the Unhallowed": 1}
KINDRED = "Kindred Discovery"
COLOSSUS = "Diregraf Colossus"
NECRODUALITY = "Necroduality"
GRAVE_TITAN = "Grave Titan"
GARY = "Gray Merchant of Asphodel"
SHEPHERD = "Shepherd of Rot"
GRAVEBORN = "Graveborn Muse"
ROOFTOP = "Rooftop Storm"
SCARAB = "The Scarab God"
REANIMATE_TARGETS = {GARY, GRAVE_TITAN}        # what we cheat in early
REANIMATORS = {"Reanimate": 1, "Necromancy": 3, "Dread Return": 4, "Victimize": 3}
LOOP_PIECES = {"Warren Soultrader", "Gravecrawler", "Plague Belcher"}

# --- extended combo model (mode 'combo') ------------------------------------
# The default 'clock' mode's kill check is the ONE documented Warren line
# (LOOP_PIECES). But find_combos shows the deck actually holds redundant infinite
# assemblies routing through Carrion Feeder (a free, no-mana sac outlet) + a
# death-drain payoff. The 'combo' mode models that as ENGINE + PAYOFF, read from
# the library so a variant .txt with a 2nd payoff (via --deck) auto-enables it:
#   ENGINE : Warren Soultrader + Gravecrawler   (mana-neutral, life-capped ~39)
#          | Rooftop Storm + Carrion Feeder + Gravecrawler   (free, truly infinite)
#   PAYOFF : Plague Belcher   (the deck's only maindeck each-opp death drain)
#          | a 2nd payoff — Zulaport Cutthroat / Bastion of Remembrance / Blood Artist
# Traced against oracle text 2026-07-03; all card-grounded, none assumed.
#
# FINDING (2026-07-03, --mode combo @8k): the combo is a ~2-3% FRINGE line — it
# assembles by T14 in only ~2% of goldfish games (no tutoring modeled = a floor).
# The deck's real clock (decap T8 / table T11) is entirely drain+combat; the combo
# is a rare backup, NOT the kill. A 2nd payoff (Gempalm->Zulaport variant) moved the
# table clock by NOTHING (T11->T11) and combo assembly by ~+1pp (2%->3%) — a FLAT
# lever, not a speed upgrade (feedback_lab_before_proposing). It also confirmed the
# 'clock' mode was NOT under-modeling the combo (the Carrion engine doesn't fire
# earlier). The only unmodeled merit of a 2nd payoff is incidental aristocrats drain
# on every creature death in normal play (goldfish-blind); if ever added, prefer the
# wipe-proof enchantment Bastion of Remembrance over the 1/1 Zulaport in this
# wipe-inviting deck. Committed deck left as-is.
CARRION = "Carrion Feeder"
PAYOFF2 = {"Zulaport Cutthroat", "Bastion of Remembrance", "Blood Artist"}
COMBO_TRACK = LOOP_PIECES | {CARRION, ROOFTOP} | PAYOFF2


def combo_ready(t):
    """Extended predicate: an ENGINE (mana-neutral sac loop) + a PAYOFF
    (each-opponent death drain) + a Zombie on board => table kill this turn."""
    have = t.have
    g = "Gravecrawler" in have
    engine = (("Warren Soultrader" in have) and g) or (t.rooftop and (CARRION in have) and g)
    payoff = ("Plague Belcher" in have) or any(p in have for p in PAYOFF2)
    return engine and payoff and t.z >= 1


def load_black_pips(names):
    """name(lower) -> count of black pips in mana_cost (incl hybrid/Phyrexian)."""
    with (ROOT / "collection" / "oracle-cards.json").open(encoding="utf-8") as f:
        cards = json.load(f)
    want = {n.lower() for n in names}
    out = {}
    def pips(mc):
        return mc.count("B") if mc else 0      # counts {B}, {W/B}, {B/P} ... any B
    for c in cards:
        nm = c.get("name", "").lower()
        if nm in want and nm not in out:
            mc = c.get("mana_cost") or ""
            if not mc and c.get("card_faces"):
                mc = c["card_faces"][0].get("mana_cost", "")
            out[nm] = pips(mc)
    return out


def is_zombie(rec):
    return "zombie" in rec["type_line"].lower()


class Trial:
    def __init__(self, library, rng, index, pips, combo_extended=False):
        self.combo_extended = combo_extended
        self.have = set()           # COMBO_TRACK pieces deployed (extended model)
        self.combo_turn = None      # first turn the combo assembles (either model)
        self.nontoken_bf = 0        # matured NONTOKEN zombie bodies (yard fuel / undying survivors on a wipe)
        self.new_nontoken = 0       # nontoken zombies entered this turn (mature next upkeep)
        self.mikaeus = False        # Mikaeus on battlefield -> undying saves the nontoken board through 1 wipe
        self.wiped_at = None        # turn a modelled board wipe hit ('recover' mode)
        self.recover_delay = None   # turns after the wipe to rebuild a threatening board
        self.g = slc.Goldfish(library, rng, rocks={})
        self.tbl = slc.Table()
        self.index = index
        self.pips = pips
        self.z = 0                  # matured Zombies you control (count at upkeep)
        self.new_z = 0              # entered this turn (count next upkeep)
        self.scarab = False
        self.devotion = 0           # summed black pips on your permanents
        self.lord_pow = 0           # per-Zombie power bonus
        self.colossus = False
        self.necro = False
        self.kindred = False
        self.graveborn = False
        self.rooftop = False
        self.shepherd = False
        self.gary_yard = False      # Gary reanimatable
        self.titan_yard = False
        self.titan_bf = False       # Grave Titan on bf -> +2 tokens per attack
        self.lili = False           # Liliana DM +1: a 2/2 token + mill each turn
        self.cryptbreaker = False   # tap+discard -> a 2/2 token each turn
        self.yard_z = 0             # Zombie cards in yard (mass-reanimation fuel)
        self.loop = set()           # LOOP_PIECES in play
        self.draws = 0

    def gdraw(self, k):
        k = max(0, min(k, DRAW_CAP - self.draws))
        if k:
            self.g.draw(k); self.draws += k

    def zombie_etb(self, n=1, nontoken=False, base=2):
        """A Zombie (or n tokens) enters: count, Kindred draw, token multipliers."""
        total = n
        if nontoken and self.necro:
            total += 1                       # Necroduality token copy (a TOKEN — no yard/undying)
        self.new_z += total
        if nontoken:
            self.new_nontoken += n           # only the real card stocks the yard / gets undying
        if self.kindred:
            self.gdraw(total)                # draw per Zombie ETB (tokens included)

    def cast_zombie_spell(self, rec, base=2, colossus_active=None):
        """Casting a Zombie creature spell: its ETB + Colossus's cast-trigger
        token. Colossus's "whenever you cast a Zombie spell" only triggers when
        Colossus is ALREADY on the battlefield — it does NOT trigger off its own
        casting (card_lookup ruling 2026-06-29), so pass the colossus flag as it
        stood BEFORE this card resolved."""
        self.zombie_etb(1, nontoken=True, base=base)
        active = self.colossus if colossus_active is None else colossus_active
        if active:
            self.zombie_etb(1, nontoken=False)   # tapped 2/2, a token


RECOVER_THREAT = 6      # zombies that will drain next upkeep = a real Scarab clock again


def apply_wipe(t, T):
    """One-shot creature board wipe (Wrath / Toxic Deluge / Blasphemous Act class)
    hitting the deck's board as it stands at the start of turn T. Modelled effects,
    all card-grounded:
      * tokens vanish (the bulk of a go-wide zombie board);
      * NONTOKEN zombies stock the graveyard (reanimation fuel) — UNLESS Mikaeus,
        the Unhallowed is out, in which case undying returns them and the nontoken
        board SURVIVES the first wipe (Mikaeus himself has no self-undying -> yard);
      * enchantment / planeswalker engines persist (Kindred Discovery, Necroduality,
        Rooftop Storm, Liliana); creature-based engines (Colossus / Cryptbreaker /
        Graveborn / Shepherd) die unless Mikaeus's undying saved their bodies;
      * Grave Titan (nontoken, non-Human) survives via Mikaeus, else -> yard;
      * The Scarab God returns to HAND on death (no tax) -> recast next turn.
    Coarse — a heuristic on a heuristic. Trust the shape, not the decimal."""
    mik = t.mikaeus
    t.wiped_at = T
    t.scarab = False                        # Scarab dies -> hand -> recast for 5
    t.new_z = 0; t.new_nontoken = 0
    if mik:
        t.z = t.nontoken_bf                 # undying returns the nontoken zombies (board survives)
        t.yard_z += 1                       # Mikaeus himself -> yard (a reanimatable zombie)
        t.mikaeus = False                   # a 2nd wipe now finishes the (countered) board
    else:
        t.yard_z += t.nontoken_bf           # nontoken zombies -> reanimation fuel
        t.z = 0; t.nontoken_bf = 0
        t.colossus = t.cryptbreaker = t.graveborn = t.shepherd = False
        if t.titan_bf:
            t.titan_bf = False; t.titan_yard = True


def goldfish_kill(library, index, pips, rng, combo_extended=False, wipe=None):
    t = Trial(library, rng, index, pips, combo_extended=combo_extended)
    g, tbl = t.g, t.tbl
    gary_casts = 0

    def pip(nm):
        return pips.get(nm.lower(), 0)

    for T in range(1, TURNS + 1):
        t.z += t.new_z; t.new_z = 0; t.draws = 0
        t.nontoken_bf += t.new_nontoken; t.new_nontoken = 0
        if wipe and T == wipe:
            apply_wipe(t, T)                # 'recover' mode: opponent wiped before your turn
        # ---- UPKEEP drains (converge) ----
        if t.scarab and t.z:
            tbl.hit_all(t.z, T)
        if t.graveborn and t.z:
            t.gdraw(t.z)
        if tbl.done:
            return tbl.decap, tbl.table, t.combo_turn, t.recover_delay

        g.begin_turn(T)
        # mana rocks (devotion via pip map; records carry no mana_cost field)
        changed = True
        while changed:
            changed = False
            for nm, (cost, out) in sorted(ROCKS.items(), key=lambda x: x[1][0]):
                if g.has(nm) and g.avail >= cost:
                    g.cast(nm, cost); g.rock_out += out; g.add_mana(out)
                    t.devotion += pip(nm)
                    changed = True; break

        # reanimation setup + payoff: Entomb/Buried Alive to bin Gary/Titan, then
        # Reanimate/Necromancy to deploy. Bin first.
        if g.has("Entomb") and g.avail >= 1 and not (t.gary_yard or t.titan_yard):
            g.cast("Entomb", 1)
            if g.fetch(GARY):
                g.discard(GARY); t.gary_yard = True; t.yard_z += 1
            elif g.fetch(GRAVE_TITAN):
                g.discard(GRAVE_TITAN); t.titan_yard = True
        if g.has("Buried Alive") and g.avail >= 2 and not (t.gary_yard or t.titan_yard):
            g.cast("Buried Alive", 2)
            if g.fetch(GARY):
                g.discard(GARY); t.gary_yard = True
            if g.fetch(GRAVE_TITAN):
                g.discard(GRAVE_TITAN); t.titan_yard = True
            t.yard_z += 2                            # Buried Alive bins 3 creatures (~zombies)
        # commander
        if not t.scarab and g.avail >= 5:
            g.cast(SCARAB, 5); t.scarab = True; t.devotion += pip(SCARAB)

        # high-value engines first: Kindred / Necroduality / Rooftop
        for nm, flag in [(KINDRED, "kindred"), (NECRODUALITY, "necro"),
                         (ROOFTOP, "rooftop")]:
            rec = index.get(nm.lower())
            if g.has(nm) and not getattr(t, flag) and rec and g.avail >= rec["cmc"]:
                g.cast(nm, rec["cmc"]); setattr(t, flag, True); t.devotion += pip(nm)

        # reanimate Gary / Titan from yard (drain / tokens), cheapest reanimator
        for rz, rc in sorted(REANIMATORS.items(), key=lambda x: x[1]):
            if g.has(rz) and g.avail >= rc and (t.gary_yard or t.titan_yard):
                if t.gary_yard:
                    g.cast(rz, rc); t.gary_yard = False
                    t.devotion += pip(GARY); tbl.hit_all(t.devotion, T)
                    t.zombie_etb(1, nontoken=True)
                elif t.titan_yard:
                    g.cast(rz, rc); t.titan_yard = False
                    t.titan_bf = True; t.zombie_etb(2)   # Giant body (not Zombie) + 2 tokens
                break

        # deploy creatures/enchantments cheapest-first (Rooftop zeroes Zombie spells)
        progress = True
        while progress:
            progress = False
            best = None
            for i, (nm, rec) in enumerate(g.hand):
                if ds.is_land(rec) or nm in ROCKS or nm == SCARAB:
                    continue
                tl = rec["type_line"].lower()
                if "creature" not in tl and "enchantment" not in tl and "planeswalker" not in tl:
                    continue
                zcre = "creature" in tl and is_zombie(rec)
                cost = 0 if (zcre and t.rooftop) else rec["cmc"]
                if cost <= g.avail and (best is None or cost < best[0]):
                    best = (cost, i, nm, rec, zcre, tl)
            if best is None:
                break
            cost, i, nm, rec, zcre, tl = best
            g.hand.pop(i); g.avail -= cost
            progress = True
            # Colossus's cast-trigger only sees Zombie spells cast while it is
            # ALREADY in play; capture its state BEFORE this card sets the flag
            # so it never tokens off its own casting.
            colossus_active = t.colossus
            t.devotion += pip(nm)
            if nm in LORDS:
                t.lord_pow += LORDS[nm]
            if nm == KINDRED: t.kindred = True
            if nm == NECRODUALITY: t.necro = True
            if nm == COLOSSUS: t.colossus = True
            if nm == ROOFTOP: t.rooftop = True
            if nm == GRAVEBORN: t.graveborn = True
            if nm == SHEPHERD: t.shepherd = True
            if nm == "Liliana, Death's Majesty": t.lili = True
            if nm == "Mikaeus, the Unhallowed": t.mikaeus = True   # undying blanket (wipe survival)
            if nm == "Cryptbreaker": t.cryptbreaker = True
            if nm == "Stitcher's Supplier": t.yard_z += 1   # mill 3 ~ 1 zombie
            if nm in LOOP_PIECES: t.loop.add(nm)
            if nm in COMBO_TRACK: t.have.add(nm)
            if nm == GARY:
                gary_casts += 1
                tbl.hit_all(t.devotion, T)            # ETB drain (devotion incl Gary's 2)
                t.zombie_etb(1, nontoken=True)
            elif nm == GRAVE_TITAN:
                t.titan_bf = True; t.zombie_etb(2)    # Giant body (not a Zombie) + 2 tokens
            elif nm == "Rot Hulk":
                t.zombie_etb(1, nontoken=True)        # Rot Hulk is itself a Zombie
                back = min(3, t.yard_z); t.yard_z -= back
                t.zombie_etb(back)                    # ETB: return up to 3 Zombies (X=opps)
            elif nm in ("Living Death", "Agadeem's Awakening"):
                t.zombie_etb(t.yard_z); t.yard_z = 0  # mass reanimation dump
            elif zcre:
                t.cast_zombie_spell(rec, colossus_active=colossus_active)

        # steady token engines (count next upkeep / attack next turn)
        if t.titan_bf:
            t.zombie_etb(2)                           # Grave Titan attack tokens
        if t.lili:
            t.zombie_etb(1); t.yard_z += 1            # +1 token + mill 2 (~1 zombie)
        if t.cryptbreaker and len(g.hand) > 1:
            t.zombie_etb(1)                           # tap + discard -> a 2/2 token

        # Shepherd of Rot: tap -> each player loses 1 per Zombie on bf (converge)
        if t.shepherd and t.z:
            tbl.hit_all(t.z, T)

        # combo assembled -> table kill. Default 'clock' mode: the one documented
        # Warren line (LOOP_PIECES), golden-stable. 'combo' mode: the extended
        # data-driven engine+payoff predicate.
        assembled = combo_ready(t) if t.combo_extended else (LOOP_PIECES <= t.loop and t.z >= 1)
        if assembled:
            if t.combo_turn is None:
                t.combo_turn = T
            tbl.kill_all(T)
        if tbl.done:
            return tbl.decap, tbl.table, t.combo_turn, t.recover_delay

        # ---- COMBAT (focus-fire) ----
        if t.z >= 1:
            tbl.hit_focus(t.z * (2 + t.lord_pow), T)
        if tbl.done:
            return tbl.decap, tbl.table, t.combo_turn, t.recover_delay

        # post-wipe recovery: turns until the board that drains next upkeep
        # (matured + entered-this-turn) is threatening again ('recover' mode)
        if t.wiped_at is not None and t.recover_delay is None and (t.z + t.new_z) >= RECOVER_THREAT:
            t.recover_delay = T - t.wiped_at

    return tbl.decap, tbl.table, t.combo_turn, t.recover_delay


def mode_clock(index, aliases, trials):
    print(f"\n### CLOCK — Curse of the Scarab kill-turn goldfish   trials={trials} seed={SEED}")
    print("    Scarab upkeep + Gary + Shepherd hit ALL opponents (converge); combat")
    print("    focus-fires; the Soultrader loop is a table kill. decap / table split.\n")
    library, commander = slc.load_parsed(DECK, index, aliases)
    pips = load_black_pips([nm for nm, _ in library] + [commander])
    rng = random.Random(SEED)
    res = [goldfish_kill(library, index, pips, rng) for _ in range(trials)]

    slc.report_clock(res, SHOW, TURNS, trials)
    print("\n  Claimed in Summary: Goldfish T7-9. Front-edge T7 odds above are the test.")


def mode_combo(index, aliases, trials, deck=None):
    """Extended combo model: race the deck's redundant infinite assemblies
    (engine + payoff, data-driven from the library) instead of only the one
    documented Warren line. Reports the same decap/table clock PLUS a combo-
    assembly curve. Point at a variant with --deck to measure a 2nd-payoff add.
    The 'clock' mode is untouched (golden-stable); this is a separate consumer."""
    path = deck or DECK
    library, commander = slc.load_parsed(path, index, aliases)
    pips = load_black_pips([nm for nm, _ in library] + [commander])
    p2 = sorted(PAYOFF2 & {nm for nm, _ in library})
    print(f"\n### COMBO MODEL — Curse of the Scarab   trials={trials} seed={SEED}")
    print(f"    deck: {Path(path).name}")
    print("    engine = Warren+Gravecrawler | Rooftop+CarrionFeeder+Gravecrawler")
    print("    payoff = Plague Belcher" +
          ("".join(" | " + p for p in p2) if p2 else "  (ONLY — single payoff, bottleneck)"))
    print()
    rng = random.Random(SEED)
    res = [goldfish_kill(library, index, pips, rng, combo_extended=True) for _ in range(trials)]
    slc.report_clock(res, SHOW, TURNS, trials)
    print(slc.row("combo assembled (cum %)", slc.cum(res, 2, SHOW), SHOW))
    print(f"  median combo assembly {slc.median(res, 2)}"
          f"   ·   never-in-{TURNS}: {slc.never_pct(res, 2, trials):.0f}%")


def _mednum(res, idx, cap=99):
    """Numeric lower-median of a turn-or-None field (same rule as slc.median)."""
    vals = sorted((r[idx] if r[idx] is not None else cap) for r in res)
    return vals[(len(vals) - 1) // 2]


def mode_recover(index, aliases, trials):
    """Post-wipe INEVITABILITY: how much does a creature board wipe actually set
    this grinder back, and how fast does it rebuild? Injects a one-shot wipe at
    turn W (see apply_wipe) on the SAME shuffles as the no-wipe baseline (paired),
    and reports the wipe TAX (table-clock delta) + the recovery clock. This is the
    grind/recursion resilience the goldfish 'clock' mode can't see — measured, not
    narrated. Coarse heuristic; trust the shape."""
    print(f"\n### RECOVER — Curse of the Scarab post-wipe inevitability   trials={trials} seed={SEED}")
    print("    One-shot creature wipe at turn W: tokens vanish; nontoken zombies -> yard")
    print("    (reanim fuel) OR survive via Mikaeus undying; enchantment/PW engines + mana")
    print("    persist; Scarab -> hand. Same shuffles as baseline (paired). 'recovered' =")
    print(f"    board draining >= {RECOVER_THREAT} next upkeep again.\n")
    library, commander = slc.load_parsed(DECK, index, aliases)
    pips = load_black_pips([nm for nm, _ in library] + [commander])

    rng = random.Random(SEED)
    base = [goldfish_kill(library, index, pips, rng) for _ in range(trials)]
    bd, btb = _mednum(base, 0), _mednum(base, 1)
    print(f"  baseline (no wipe):   median decap T{bd} / table T{btb}\n")
    print("  wipe@W   decap  table   table-tax    survived   recover(med)  <=2t  <=3t  never")
    print("  " + "-" * 74)
    for W in (6, 8, 10):
        rng = random.Random(SEED)               # identical games; only the wipe differs
        res = [goldfish_kill(library, index, pips, rng, wipe=W) for _ in range(trials)]
        d, tb = _mednum(res, 0), _mednum(res, 1)
        tax = tb - btb
        rec = [r[3] for r in res]               # recover_delay (turns after wipe), None = never
        got = sorted(x for x in rec if x is not None)
        survived = 100 * sum(1 for x in rec if x == 0) / trials     # board never dropped below threat
        medrec = got[(len(got) - 1) // 2] if got else None
        p2 = 100 * sum(1 for x in got if x <= 2) / trials
        p3 = 100 * sum(1 for x in got if x <= 3) / trials
        never = 100 * sum(1 for x in rec if x is None) / trials
        mr = f"+{medrec}t" if medrec is not None else "  —"
        print(f"    T{W:<4} T{d:<5} T{tb:<5}   {'+' if tax >= 0 else ''}{tax} turn{'s' if abs(tax)!=1 else ''}"
              f"{'':4} {survived:4.0f}%{'':6} {mr:>5}{'':6} {p2:3.0f}% {p3:4.0f}% {never:4.0f}%")
    print("\n  table-tax = wiped table median - baseline (turns the wipe costs).")
    print("  survived  = board stayed >= threat through the wipe (mostly Mikaeus undying).")
    print("  recover   = turns AFTER the wipe to a threatening board again; never = not within horizon.")


if __name__ == "__main__":
    slc.run_cli(__doc__,
                {"clock": mode_clock, "combo": mode_combo, "recover": mode_recover},
                default_trials=40000)
