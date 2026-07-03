"""TAGGER_REGRESSION (tier-1, synthetic cards — no oracle load): pins the two
framework_bakeoff.tag_card fixes from the 2026-07-03 mulligan audit (§7):

1. Braceless mana producers ("Add one mana of any color") are ramp — Birds of
   Paradise / Arcane Signet class was invisible to the `add \\{` pattern, so the
   MANA keeps false-rejected hands whose only accel was a dork/Signet.
2. Draw PAYOFFS ("whenever you draw a card, <effect>") are not draw SOURCES —
   Sheoldred / Psychosis Crawler were tagged 'draw', so keep_spec's selection
   bucket counted punishers as dig (Forced Liquidation's >=2-selection clause).
   Niv-Mizzet, Parun is the pinned survivor: its payoff clause is stripped but
   its genuine engine clause ("whenever a player casts ... you draw") keeps it.

Same bug class as deck_sim._draw_profile's payoff fix (tests/test_deck_sim.py);
that fix lived only in the flow model — this one covers the tag layer feeding
keep_spec buckets and the bake-off counts.
"""
import framework_bakeoff as fb


def _card(text, type_line="Creature"):
    return {"type_line": type_line, "oracle_text": text}


# --- fix 1: braceless mana producers are ramp --------------------------------

def test_braceless_any_color_dork_is_ramp():
    birds = _card("Flying\n{T}: Add one mana of any color.")
    assert "ramp" in fb.tag_card(birds)


def test_braceless_commander_identity_rock_is_ramp():
    signet = _card("{T}: Add one mana of any color in your commander's color identity.",
                   type_line="Artifact")
    assert "ramp" in fb.tag_card(signet)


def test_braced_producer_still_ramp():
    sol_ring = _card("{T}: Add {C}{C}.", type_line="Artifact")
    assert "ramp" in fb.tag_card(sol_ring)


def test_no_mana_text_not_ramp():
    bear = _card("Vigilance")
    assert "ramp" not in fb.tag_card(bear)


def test_opponent_treasure_reminder_text_is_not_ramp():
    # The braceless pattern must not match the Treasure REMINDER text — An Offer
    # You Can't Refuse gives the Treasures to the countered spell's controller.
    offer = _card("Counter target noncreature spell. Its controller creates two "
                  "Treasure tokens. (They're artifacts with \"{T}, Sacrifice this "
                  "token: Add one mana of any color.\")", type_line="Instant")
    assert "ramp" not in fb.tag_card(offer)


# --- fix 2: draw payoffs are not draw sources ---------------------------------

def test_sheoldred_payoff_is_not_draw():
    sheoldred = _card("Deathtouch\nWhenever you draw a card, you gain 2 life.\n"
                      "Whenever an opponent draws a card, they lose 2 life.")
    assert "draw" not in fb.tag_card(sheoldred)


def test_psychosis_crawler_payoff_is_not_draw():
    crawler = _card("Psychosis Crawler's power and toughness are each equal to the "
                    "number of cards in your hand.\n"
                    "Whenever you draw a card, each opponent loses 1 life.",
                    type_line="Artifact Creature")
    assert "draw" not in fb.tag_card(crawler)


def test_niv_mizzet_engine_survives_payoff_strip():
    niv = _card("Flying\nWhenever you draw a card, Niv-Mizzet, Parun deals 1 damage "
                "to any target.\n"
                "Whenever a player casts an instant or sorcery spell, you draw a card.")
    assert "draw" in fb.tag_card(niv)


def test_plain_draw_spell_still_draw():
    whisper = _card("You draw two cards and you lose 2 life.", type_line="Sorcery")
    assert "draw" in fb.tag_card(whisper)


def test_upkeep_draw_engine_still_draw():
    arena = _card("At the beginning of your upkeep, you draw a card and you lose 1 life.",
                  type_line="Enchantment")
    assert "draw" in fb.tag_card(arena)
