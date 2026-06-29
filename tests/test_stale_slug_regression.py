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
