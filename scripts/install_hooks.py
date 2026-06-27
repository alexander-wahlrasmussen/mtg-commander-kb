#!/usr/bin/env python3
"""install_hooks.py — activate the committed git hooks (one-time, per clone).

Points git at the version-controlled hooks/ directory via core.hooksPath (so the
hook ships with the repo instead of living untracked in .git/hooks). Re-run after
a fresh clone. Bypass a single commit with `git commit --no-verify`.

    python scripts/install_hooks.py
"""
import stat
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HOOK = ROOT / "hooks" / "pre-commit"


def main():
    if not HOOK.exists():
        sys.exit(f"ERROR: {HOOK} not found — nothing to install.")

    # Mark executable (required by git on macOS/Linux; a no-op on Windows, where
    # Git Bash runs the hook via its shebang regardless).
    HOOK.chmod(HOOK.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

    subprocess.run(["git", "config", "core.hooksPath", "hooks"], cwd=ROOT, check=True)

    # Best-effort: record the executable bit in the index if the hook is tracked,
    # so other clones (and Unix committers) get it too. Silent if not yet added.
    subprocess.run(["git", "update-index", "--chmod=+x", "hooks/pre-commit"],
                   cwd=ROOT, capture_output=True)

    print("Installed: core.hooksPath -> hooks/")
    print("  pre-commit now gates staged decklists (Deck Doctor + validate) and runs")
    print("  pytest when scripts/ or tests/ change. Bypass once: git commit --no-verify")


if __name__ == "__main__":
    main()
