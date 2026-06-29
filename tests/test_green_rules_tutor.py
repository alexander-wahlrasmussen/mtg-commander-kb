"""REGRESSION (2026-06-29 codebase audit — 🟢 rules nit: tutor mana reservation).

Two clock labs let a piece be TUTORED and CAST on the same turn while only paying
the fetched card's mana — the tutor's own cost was never reserved (double-spend on
the assembly path):

  * lw_clock_lab.goldfish_kill — `castable(fin)` was true via a held tutor, but the
    `cm >= finisher_cost` check used the FULL mana pool. A tutored finisher must cost
    tutor_cost + finisher_cost. Fix: fin_cm() reserves the cheapest held tutor's mana
    when the finisher is not already in hand (Mystical Teachings {3}{U}=4 / Emeritus
    of Woe {3}{B}=4 / Sanar–Wild Idea {U}{R}=2, card_lookup 2026-06-29).
  * urza_clock_lab — tutor_missing() already pays spend(tc) before combo_check pays
    the combo cost; the 2026-06-29 per-spend fix made spend() drain a FINITE per-turn
    urza_pool, so the tutor and the combo can't both re-claim Urza's +2 tap bonus.
    This pins that reservation (the bug would let the bonus pay for both).

Hermetic: synthetic records (helpers.rec) + controlled Goldfish state, no Scryfall
bulk. Each lab is exercised as a pure deterministic function (g is injected, so no
rng / opening-hand variance). Boundary shape: a turn with EXACTLY tutor+piece mana
closes; one mana short cannot close that turn.
"""
import importlib.util
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "tests"))

from helpers import rec


def _load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


LW = _load("lw_clock_lab")
URZA = _load("urza_clock_lab")


# --------------------------------------------------------------------------
# Lightning War — a tutored finisher must reserve the tutor's mana too.
#
# Controlled goldfish: empty undrawn library + a fixed `lands` floor (avail is
# constant every turn). Azula auto-deploys at avail>=4 and swings opp 0 only, so
# opponents 1 & 2 stay at 40 -> the TABLE finisher's need_each is a constant 40.
# With no amps (inst=2): Comet needs X=20, cost = X + 2 + (living-1) = 24 at the
# first combat turn (T2). cm = lands + 2 (Azula's +2 combat mana). The kill lands
# on T2 iff the mana left to CAST the finisher covers 24.
# --------------------------------------------------------------------------
def _lw_goldfish(lands, hand):
    g = LW.slc.Goldfish.__new__(LW.slc.Goldfish)
    g.deck = []
    g.hand = list(hand)
    g.ptr = 0
    g.yard = []
    g.lands = lands
    g.rock_out = 0
    g.rocks = {}
    g.avail = 0
    return g


def _lw_table_turn(lands, hand):
    g = _lw_goldfish(lands, hand)
    _decap, table = LW.goldfish_kill([], "Azula", None, {}, random.Random(0), g=g)
    return table


_MYSTICAL = ("Mystical Teachings",
             rec(cmc=4, type_line="Instant", face_types=["Instant"], color_identity=("U",)))
_COMET = ("Comet Storm",
          rec(cmc=2, type_line="Instant", face_types=["Instant"], color_identity=("R",)))

# the Comet table-kill at T2 with no amps: X=20, cost = 20 + 2 + (3-1)
_FINISHER_COST = 24
_TUTOR_COST = 4                              # Mystical Teachings {3}{U}


def test_lw_in_hand_finisher_pays_only_its_own_cost():
    """A finisher already in HAND is taxed nothing extra: cm = its own cost closes
    the table on the first combat turn; one mana short slips to a later turn."""
    # cm = lands + 2 ; need cm >= 24  -> lands >= 22
    assert _lw_table_turn(_FINISHER_COST - 2, [_COMET]) == 2
    assert _lw_table_turn(_FINISHER_COST - 3, [_COMET]) > 2


def test_lw_tutored_finisher_reserves_tutor_mana():
    """A finisher supplied by a held tutor must pay tutor_cost + finisher_cost. The
    boundary moves up by exactly the tutor's mana: cm >= tutor+finisher closes on T2,
    one short cannot (under the bug, cm >= finisher_cost alone closed it — the
    double-spend this guards)."""
    # cm = lands + 2 ; need cm - tutor_cost >= 24  -> lands >= 26
    exact = _FINISHER_COST + _TUTOR_COST - 2          # lands for cm == tutor+finisher
    assert _lw_table_turn(exact, [_MYSTICAL]) == 2     # exactly enough -> kills T2
    assert _lw_table_turn(exact - 1, [_MYSTICAL]) > 2  # one mana short -> delayed


def test_lw_tutor_tax_equals_tutor_cost():
    """The extra mana a tutored finisher needs over an in-hand one is exactly the
    held tutor's cost (4), not a free find."""
    # smallest land count that closes T2 for each route
    in_hand = next(n for n in range(60) if _lw_table_turn(n, [_COMET]) == 2)
    tutored = next(n for n in range(60) if _lw_table_turn(n, [_MYSTICAL]) == 2)
    assert tutored - in_hand == _TUTOR_COST


# --------------------------------------------------------------------------
# Urza — tutor-into-combo reserves both the tutor and the combo cost.
# --------------------------------------------------------------------------
def _urza_trial(lands, urza_pool=2):
    tr = URZA.Trial.__new__(URZA.Trial)
    g = URZA.slc.Goldfish.__new__(URZA.slc.Goldfish)
    g.deck = [("Dramatic Reversal",
               rec(cmc=2, type_line="Instant", face_types=["Instant"]))]
    g.hand = [("Isochron Scepter", rec(cmc=2, type_line="Artifact", face_types=["Artifact"])),
              ("Merchant Scroll", rec(cmc=2, type_line="Sorcery", face_types=["Sorcery"])),
              ("Walking Ballista",
               rec(cmc=0, type_line="Artifact Creature", face_types=["Artifact Creature"]))]
    g.ptr = 0
    g.yard = []
    g.lands = lands
    g.rock_out = 0
    g.rocks = {}
    g.avail = 0
    tr.g = g
    tr.tbl = URZA.slc.Table()
    tr.bf = set()
    tr.urza = True
    tr.petal = 0
    tr.used = set()
    tr.urza_pool = urza_pool
    return tr


def test_urza_tutor_into_combo_reserves_both():
    """Isochron+Reversal combo = 4 mana; Merchant Scroll tutor = 2; Urza's pool = +2.
    Tutor Reversal then fire the combo needs 6 total. On T1 (no draw): lands 4 -> mana
    6 closes; lands 3 (one short) cannot. The bug regranted Urza's +2 to BOTH the tutor
    and the combo, so 5 mana sufficed."""
    tr_ok = _urza_trial(4)
    tr_ok.turn(1)
    assert tr_ok.tbl.table == 1

    tr_short = _urza_trial(3)
    tr_short.turn(1)
    assert tr_short.tbl.table is None


def test_urza_spend_uses_tap_bonus_once():
    """spend() draws the finite urza_pool down across consecutive spends — the tutor
    then the fetched card. Two spends totalling 7 deduct 7 from (pool + avail); the
    per-spend-regrant bug deducted only 3 (the 2-mana bonus 'paid' twice)."""
    tr = _urza_trial(0, urza_pool=2)
    tr.g.lands = 10
    tr.g.avail = 10
    start = tr.mana()                 # 10 + 2
    tr.spend(3)                       # tutor cost
    tr.spend(4)                       # fetched-card cost
    assert tr.mana() == start - 7
