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


# --- gamePlan selection (the same audit's second parser gap) ------------------
def test_game_plan_prefers_what_the_deck_prose():
    secs = _sections("What the Deck Does", "It builds a wide Wizard board and pings the table.")
    assert kb._game_plan(secs, "fallback").startswith("It builds a wide")


def test_game_plan_matches_heading_variant_by_prefix():
    """Lightning War uses '## What the Deck Is Trying to Do' — must still match (was falling
    through to the terse win-line)."""
    secs = {"what the deck is trying to do":
            ("What the Deck Is Trying to Do", "Dictate tempo, then end on an X-burn finisher.")}
    assert kb._game_plan(secs, "fallback") == "Dictate tempo, then end on an X-burn finisher."


def test_game_plan_skips_empty_table_section():
    """Eldrazi stalled on 'Quick Reference' (a table → empty first paragraph) and never reached
    its prose 'Core Loop'. Skip empties and fall through."""
    secs = {
        "quick reference": ("Quick Reference", "| Archetype | Eldrazi ramp |\n| Clock | T8 |"),
        "core loop": ("Core Loop", "The deck ramps hard into Maelstrom Wanderer and Craterhoof."),
    }
    assert kb._game_plan(secs, "fallback").startswith("The deck ramps hard")


def test_game_plan_falls_back_to_win_line():
    assert kb._game_plan({"commander rules text": ("Commander Rules Text", "x")}, "WL") == "WL"


# --- _kill_tree: structured kill-ladder for the deck page (hermetic registry transform) ---
_KIND = {"combo", "table", "combat", "enabler"}


def test_kill_tree_none_for_unencoded_deck():
    """Only 4 decks are encoded; the rest return None and the dashboard hides the ladder."""
    assert kb._kill_tree("lightning_war") is None
    assert kb._kill_tree("not_a_real_slug") is None


def test_kill_tree_shape_for_an_encoded_deck():
    kt = kb._kill_tree("radiation_sickness")
    assert kt is not None
    assert set(kt) >= {"title", "root", "stall", "src", "background", "lines"}
    assert kt["lines"] and all(
        set(l) == {"id", "need", "kill", "clock", "kind"} and l["kind"] in _KIND
        for l in kt["lines"])
    # Radiation has an always-on background drain; its kind is valid too.
    assert kt["background"] is not None and kt["background"]["kind"] in _KIND


def test_kill_tree_all_four_encoded_decks_resolve():
    """Every reg_slug in KILL_TREES round-trips through _kill_tree with valid line kinds."""
    encoded = [sp["reg_slug"] for sp in kb.deck_registry.KILL_TREES.values()]
    assert len(encoded) == 4
    for slug in encoded:
        kt = kb._kill_tree(slug)
        assert kt and kt["lines"]
        assert all(l["kind"] in _KIND for l in kt["lines"])
