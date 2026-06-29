"""Regression test for kb_content._summary_buckets — the decklist role grouping.

REGRESSION (2026-06-29): the bucket parser only recognised NUMBERED card lines
("1 Card Name"), so Summaries that BULLET their decklist ("- Card Name" —
Lightning War and several others) parsed zero cards per bucket. Every .txt card
then fell to the catch-all "Other" group and the deck page's "By role" view was
a single undifferentiated block. This pins both list styles. Hermetic — feeds
synthetic Summary markdown to the pure parser, no Scryfall bulk.
"""
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def _load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


kb = _load("kb_content")

_BULLET = """\
## Decklist (100 cards)

### Commander (1)
- Fire Lord Azula

### Infinite Combo & Copy-Doublers (2)
- Twinning Staff
- Expansion // Explosion

### Lands (1)
- Steam Vents
"""

_NUMBERED = """\
## Decklist (100 cards)

### Ramp (2)
1 Sol Ring
1 Arcane Signet
"""


def test_summary_buckets_parses_bulleted_cards(tmp_path):
    p = tmp_path / "X_Summary.md"
    p.write_text(_BULLET, encoding="utf-8")
    buckets = {name: cards for name, cards in kb._summary_buckets(p)}
    # the command-zone bucket is dropped; functional buckets carry their cards
    assert "Commander" not in buckets
    assert buckets["Infinite Combo & Copy-Doublers"] == ["Twinning Staff", "Expansion // Explosion"]
    assert buckets["Lands"] == ["Steam Vents"]


def test_summary_buckets_parses_numbered_cards(tmp_path):
    p = tmp_path / "Y_Summary.md"
    p.write_text(_NUMBERED, encoding="utf-8")
    buckets = {name: cards for name, cards in kb._summary_buckets(p)}
    assert buckets["Ramp"] == ["Sol Ring", "Arcane Signet"]
