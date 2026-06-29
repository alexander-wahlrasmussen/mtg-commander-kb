"""REGRESSION (2026-06-29 audit): card_lookup blanked the mana cost, type line and
P/T of any single-faced card with empty oracle_text (~345 vanilla creatures),
because is_multi_face keyed on `not oracle_text`. CLAUDE.md mandates this tool
before recommending a card, so a missing body/cost is exactly the misread the
hard rules exist to prevent. Fix keys on the presence of card_faces.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import card_lookup as cl  # noqa: E402


def test_vanilla_creature_shows_cost_type_and_pt():
    card = {
        "name": "Grizzly Bears", "layout": "normal", "mana_cost": "{1}{G}",
        "cmc": 2.0, "type_line": "Creature — Bear", "oracle_text": "",
        "power": "2", "toughness": "2", "color_identity": ["G"],
    }
    out = cl.format_card(card, rulings_index={})
    assert "{1}{G}" in out
    assert "Creature — Bear" in out
    assert "P/T: 2/2" in out


def test_dfc_with_card_faces_still_renders_both_faces():
    card = {
        "name": "Front // Back", "layout": "modal_dfc", "oracle_text": "",
        "cmc": 1.0, "type_line": "Creature — Elf // Land", "color_identity": ["G"],
        "card_faces": [
            {"name": "Front", "mana_cost": "{G}", "type_line": "Creature — Elf",
             "oracle_text": "Front rules.", "power": "1", "toughness": "1"},
            {"name": "Back", "mana_cost": "", "type_line": "Land",
             "oracle_text": "Back rules."},
        ],
    }
    out = cl.format_card(card, rulings_index={})
    assert "Front rules." in out and "Back rules." in out
