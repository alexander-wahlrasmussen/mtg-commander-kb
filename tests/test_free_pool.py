"""Unit tests for free_pool pure helpers.

REGRESSION (2026-07-17): `--check` promised "the checked list is NOT counted as
deployed", but a list living inside decks/ was still counted against itself, so
every 1-of in the checked deck read as NOT-FREE (own 1, deployed 1). Surfaced by
checking mass-production-owned (in decks/) — the WoA session only ever checked
lists under decks/considering/, which the non-recursive glob never counts.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import free_pool as fp  # noqa: E402


def _mk(deck_dir, name, lines):
    p = deck_dir / name
    p.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return p


def test_checked_list_inside_deck_dir_is_excluded(tmp_path):
    checked = _mk(tmp_path, "mass-production.txt", ["1 Baylen, the Haymaker", "1 Sol Ring"])
    _mk(tmp_path, "other-deck.txt", ["1 Sol Ring"])

    dep = fp.deployed_from_decks(tmp_path, exclude=checked.resolve())
    assert dep["baylen, the haymaker"] == 0  # only in the checked list -> not deployed
    assert dep["sol ring"] == 1              # other deck still counts


def test_no_exclude_counts_everything():
    # default path (no --check): unchanged behavior, every decks/*.txt counts
    import inspect
    sig = inspect.signature(fp.deployed_from_decks)
    assert sig.parameters["exclude"].default is None


def test_exclude_outside_deck_dir_is_noop(tmp_path):
    deck_dir = tmp_path / "decks"
    deck_dir.mkdir()
    considering = tmp_path / "considering"
    considering.mkdir()
    _mk(deck_dir, "built.txt", ["1 Sol Ring"])
    candidate = _mk(considering, "candidate.txt", ["1 Sol Ring"])

    dep = fp.deployed_from_decks(deck_dir, exclude=candidate.resolve())
    assert dep["sol ring"] == 1
