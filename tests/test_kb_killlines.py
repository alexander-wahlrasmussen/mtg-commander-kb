"""Regression tests for kb_content._kill_lines — the deck-page finisher parser.

The 2026-06-28 deck-page audit found 4 decks showing ZERO kill-lines not because the content
was missing but because the parser only recognised one heading/format. Each variant below is a
real Summary shape that produced 0 finishers; this pins them so the regression can't return.
Hermetic — feeds synthetic `sections` dicts straight to the pure parser, no Scryfall bulk.
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


def _sections(heading, body):
    return {heading.lower(): (heading, body)}


def test_canonical_kill_lines_still_parse():
    """The format that always worked (Radiation/Genome/Dark Lord) — guard against regressions."""
    body = ("**Line 1 — Counter Overload (primary, combat):** floods counters.\n"
            "**Line 2 — Simic Ascendancy (alternate win):** 20 growth counters.")
    out = kb._kill_lines(_sections("Kill Lines", body))
    assert [f["name"] for f in out] == ["Counter Overload", "Simic Ascendancy"]
    assert out[0]["tag"] == "primary, combat"


def test_closing_lines_heading_with_line_labels():
    """Exile's Return / Eldrazi: content under '## Closing Lines' (not 'Kill Lines')."""
    body = ("**Line 1 — Hellkite Charger + Firebending**\nWith Sozin's Comet up, swing for 20.\n"
            "**Line 2 — Commander Damage**\nPile counters on Zuko.")
    out = kb._kill_lines(_sections("Closing Lines", body))
    assert [f["name"] for f in out] == ["Hellkite Charger + Firebending", "Commander Damage"]


def test_letter_indexed_lines():
    """Zero-Sum: '**Line A —**' / '**Line B —**' letter indices, not digits."""
    body = ("**Line A — Exquisite Blood loop (primary).** Table dies at instant speed.\n"
            "**Line B — Affinity infinite.** Sprout Swarm under Witherbloom.")
    out = kb._kill_lines(_sections("Kill Lines", body))
    assert [f["name"] for f in out] == ["Exquisite Blood loop", "Affinity infinite"]
    assert out[0]["tag"] == "primary"


def test_numbered_bold_lead_fallback():
    """Forced Liquidation: 'N. **Card Name** *(tag)* — note' (bold is the name, not a label)."""
    body = ("1. **Notion Thief + Psychosis Crawler** *(marquee)* — one wheel kills the table.\n"
            "3. **Peer into the Abyss** *(single-target nuke)* — pointed at one opponent.\n"
            "4. **Displacer Kitten + Aether Channeler** *(backup combo)* — infinite ETB.")
    out = kb._kill_lines(_sections("Closing Lines", body))
    assert [f["name"] for f in out] == [
        "Notion Thief + Psychosis Crawler", "Peer into the Abyss",
        "Displacer Kitten + Aether Channeler"]
    assert out[0]["tag"] == "marquee"
    assert out[1]["note"].startswith("pointed at one opponent")


def test_line_labels_win_over_numbered_fallback():
    """If a section has BOTH '**Line N —**' items and stray bold bullets, the labels win
    (the numbered fallback only fires when no Line-labels are found)."""
    body = ("**Line 1 — Real Kill:** the line.\n- **Some Card** a mention, not a line.")
    out = kb._kill_lines(_sections("Kill Lines", body))
    assert [f["name"] for f in out] == ["Real Kill"]


def test_no_kill_section_returns_empty():
    assert kb._kill_lines(_sections("What the Deck Does", "It does things.")) == []
