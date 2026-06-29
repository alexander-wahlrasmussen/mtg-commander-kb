"""REGRESSION (2026-06-29 audit): in --since mode sync_to_project ran collision
detection only over the git-changed subset, so a changed file whose basename
collides with an UNCHANGED doc slipped past the guard and would overwrite it in the
flattened Claude Project namespace. Fix checks collisions over the full candidate
set before the --since filter.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import sync_to_project as s  # noqa: E402


def test_since_collision_detected_against_unchanged_file(monkeypatch, capsys):
    root = s.REPO_ROOT
    changed = root / "decks" / "Foo_Summary.md"        # the one git says changed
    unchanged = root / "collection" / "Foo_Summary.md"  # same basename, NOT changed

    monkeypatch.setattr(s, "collect_candidate_files", lambda: [changed, unchanged])
    monkeypatch.setattr(s, "filter_by_git_changes", lambda files, since: [changed])
    monkeypatch.setattr(sys, "argv", ["sync_to_project.py", "--since", "HEAD~1"])

    rc = s.main()
    assert rc == 2                                       # collision must abort the sync
    assert "collision" in capsys.readouterr().err.lower()


def test_no_collision_when_basenames_unique(monkeypatch):
    root = s.REPO_ROOT
    a = root / "decks" / "A_Summary.md"
    b = root / "collection" / "B_Summary.md"
    monkeypatch.setattr(s, "collect_candidate_files", lambda: [a, b])
    monkeypatch.setattr(s, "filter_by_git_changes", lambda files, since: [a])
    monkeypatch.setattr(sys, "argv", ["sync_to_project.py", "--since", "HEAD~1", "--dry-run"])
    rc = s.main()
    assert rc == 0                                       # unique names -> proceeds
