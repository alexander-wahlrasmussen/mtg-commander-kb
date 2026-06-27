"""Shared test setup.

Puts scripts/ on sys.path (the repo's cross-module idiom is path-based, not a
package) and resets deck_sim's process-global keep-spec around every test so a
plan-aware test can't leak its installed spec into the next one.
"""
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import pytest  # noqa: E402


@pytest.fixture(autouse=True)
def _reset_keep_spec():
    """deck_sim.keep_hand consults a module-global keep-spec. Default it to None
    (the land-count rule) before AND after each test so order can't matter."""
    import deck_sim
    deck_sim.set_keep_spec(None)
    yield
    deck_sim.set_keep_spec(None)
