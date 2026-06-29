"""REGRESSION (2026-06-29 codebase audit): the Calamity->Croak rename and the
Hashaton-Thoracle drop left stale slugs in hand-maintained config that silently
dropped/blocked active decks or pointed tools at retired builds. These pin the
roster-derived configs to the single source of truth (deck_registry) so the drift
can't recur.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))


def test_game_log_roster_matches_registry():
    import game_log
    import deck_registry
    assert set(game_log.DECKS) == set(deck_registry.fb_decks())
    assert "calamity_tax" not in game_log.DECKS          # retired -> Croak
    assert {"croak_and_dagger", "forced_liquidation"} <= set(game_log.DECKS)


def test_unlock_optimizer_no_dead_default_build():
    import unlock_optimizer
    joined = " ".join(unlock_optimizer.DEFAULT_BUILDS)
    assert "hashaton" not in joined                      # dropped build
    assert "forced-liquidation" not in joined            # graduated to an active .txt


def test_vs_dragon_roster_decks_match_kill():
    # Importing the module also runs its load-time `assert set(DECKS) == set(KILL)`;
    # this re-asserts it explicitly and pins the rename.
    import vs_dragon_roster_lab as V
    assert set(V.DECKS) == set(V.KILL)
    assert "calamity_tax" not in V.KILL
    assert "croak_and_dagger" in V.KILL


def test_clock_check_summary_covers_active_roster():
    # clock_check.SUMMARY pointed calamity_tax at a deleted file and silently [SKIP]ped
    # croak_and_dagger / forced_liquidation (2026-06-29 audit). Importing runs its load-time
    # roster guard; re-assert the mapping == the active roster and pin the rename.
    import importlib.util
    from pathlib import Path
    spec = importlib.util.spec_from_file_location(
        "clock_check", Path(__file__).resolve().parent.parent / "scripts" / "clock_check.py")
    cc = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cc)
    import deck_registry
    assert set(cc.SUMMARY) == set(deck_registry.fb_decks())
    assert "calamity_tax" not in cc.SUMMARY
    assert {"croak_and_dagger", "forced_liquidation"} <= set(cc.SUMMARY)


def test_framework_bakeoff_oracles_cover_full_roster():
    # The SIM oracles are computable for EVERY deck, so a missing slug silently drops it from
    # every Spearman (falls through to None) and a stale slug (calamity_tax) is dead weight that's
    # never queried — the bakeoff was correlating over 15 decks, not 17. Importing runs the
    # load-time `assert set(RICHER)==set(DECKS)==set(INTERACTION)`; re-assert + pin the rename.
    import framework_bakeoff as fb
    import deck_registry
    roster = set(deck_registry.fb_decks())
    assert set(fb.RICHER_ORACLE) == roster
    assert set(fb.INTERACTION_ORACLE) == roster
    assert "calamity_tax" not in fb.RICHER_ORACLE and "calamity_tax" not in fb.INTERACTION_ORACLE
    assert {"croak_and_dagger", "forced_liquidation"} <= set(fb.RICHER_ORACLE)


def test_self_meta_judgment_has_no_dead_anchor():
    # The Δrank comparison column anchors on a hand-kept judgment ranking. The Calamity->Croak
    # rename left "calamity_tax" pointing at a deck no longer simmed (a dead anchor). JUDGMENT may
    # be a SUBSET (new decks unranked -> "—"), but must never name a retired slug. Importing runs
    # its load-time `assert set(JUDGMENT) <= delay_lab.ROSTER`.
    import self_meta_lab as sm
    import deck_registry
    roster = set(deck_registry.fb_decks())
    assert set(sm.JUDGMENT) <= roster                 # subset of the live roster, no dead anchors
    assert "calamity_tax" not in sm.JUDGMENT
    assert sm.JUDGMENT.get("croak_and_dagger") == 7   # inherited the renamed deck's tier
