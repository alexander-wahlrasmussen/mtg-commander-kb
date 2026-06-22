# The Replication Crisis — Bracket-4 Swap (2026-06-01)

**Goal:** add a Satya-independent, deterministic kill so the deck stops folding
to commander removal / a blocked combat step. Pushes Replication Crisis from a
17/20 (5/4/4/4) combat-grind deck toward bracket-4-in-spirit
([[bracket-4-in-spirit]]) within the 3-GC cap.

**Status:** proposed. **Not yet applied to the `.txt`** — Kiki-Jiki is an
unowned buy and the line needs pod approval (see below). Decklist updates to a
new dated `.txt` once the card is acquired and approved.

Card text verified against local Scryfall data 2026-06-01 ([[feedback_read_card_first]]).

---

## The swap

| Out | In | Why |
|---|---|---|
| Bident of Thassa | **Kiki-Jiki, Mirror Breaker** *(buy ~€10–15)* | Bident is slow combat-damage card draw — no combo or protection role, and the deck is already deep on draw (One Ring, Mystic Remora, Esper Sentinel, Archivist, Cloudblazer). Kiki unlocks two Satya-independent infinites from pieces already in the deck. |

1-for-1. **Card count stays 99 + commander = 100.** **GC count stays 3/3**
(Fierce Guardianship, Cyclonic Rift, The One Ring) — neither Bident nor Kiki is a
Game Changer (verified against `REF_Game_Changers_List.md`).

---

## Why Kiki, and why it fixes the ceiling

The audit pins Kill Reliability and Durability at 4/5 for the *same* reason:
**every existing kill line needs Satya — a 4-mana 3/5 — to survive and connect in
combat.** Satya removal, two blockers, or a Torpor Orb / Ghostly Prison resets
the clock. The Sword+AA infinite is ~2% to assemble by draw (deck has no tutors;
see `deck_sim.py`), so the real kill is a slow grind.

Kiki adds a kill that **needs neither Satya nor a connecting attack** — it wins on
assembly. Both lines use creatures **already in the 99**:

### Line A — Kiki-Jiki + Zealous Conscripts (primary)
- **Kiki-Jiki, Mirror Breaker** `{2}{R}{R}{R}`, 2/2, **Haste**. `{T}: Create a token that's a copy of target nonlegendary creature you control, except it has haste. Sacrifice it at the beginning of the next end step.`
- **Zealous Conscripts** `{4}{R}`, 3/3 haste. `When this creature enters, gain control of target permanent until end of turn. Untap that permanent. It gains haste until end of turn.`
- Loop: tap Kiki → token copy of Conscripts → its ETB untaps **Kiki** → tap Kiki again → repeat. **Infinite hasty 3/3 attackers** (and you may steal/untap a permanent each iteration). Lethal alpha the same turn.

### Line B — Kiki-Jiki + Restoration Angel (redundant, same Kiki)
- **Restoration Angel** `{3}{W}`, 3/4 flash flying. `When this creature enters, you may exile target non-Angel creature you control, then return that card to the battlefield.`
- Loop: tap Kiki → token copy of Resto → its ETB blinks **Kiki** (non-Angel) → Kiki returns untapped → tap Kiki again → repeat. **Infinite 3/4 flying hasty bodies + infinite ETBs.**

Kiki's native haste means it combos the turn it lands if the partner is already
out. The deck's existing protection suite (Fierce Guardianship, Deflecting Swat,
Akroma's Will, Clever Concealment, Slip Out the Back, Lightning Greaves,
Swiftfoot Boots) shields the combo turn — no new protection needed.

---

## Pod approval required (2-card infinite)

`REF_Bracket_3_House_Rules.md` disallows 2-card infinites without explicit pod
approval. Kiki + Conscripts and Kiki + Resto are both 2-card (the commander is
not required), so this needs approval before tournament-grade play.

**This would be the 4th per-deck 2-card-infinite approval** (after Berta,
Witherbloom, Exile's Return — see [[project_exiles_return_bracket4_swaps]]). At
four standing exceptions it's worth **documenting the exception explicitly in
`REF_Bracket_3_House_Rules.md`** rather than tracking it per-deck. Flagging for a
decision — I won't edit the house-rules doc without being asked.

---

## Cross-deck contention (resolved by this plan)

Kiki-Jiki is **0 owned**; the Exile's Return bracket-4 pivot
([[project_exiles_return_bracket4_swaps]]) already plans to buy one for its own
Kiki + Felidar / Restoration combo. The chosen plan is a **dedicated second
Kiki for Replication**, so both decks run independently. The natural tutor for
it (Imperial Recruiter, which finds power-2 Kiki) is the single owned copy,
deployed in Exile's Return — see the optional follow-up below.

---

## Optional follow-up — combo consistency

Without a tutor, Kiki is found by draw + the deck's filtering (Ponder, Preordain,
One Ring, Mystic Remora). If the combo feels too inconsistent in play, the clean
non-GC add is a **second Imperial Recruiter** (`{2}{R}` 1/1, ETB tutor a
power-≤2 creature → fetches Kiki, and is itself a creature Satya can copy for a
repeatable tutor). Owned copy is in Exile's Return, so this is a ~€8–12 buy.
Not included in the core swap; hold until the combo's hit rate is felt.

---

## Score impact

- **Kill Reliability 4 → 5:** adds a deterministic kill independent of the
  combat step and of Satya. A 5 specifically required "kills that function
  independently of the combat step" (audit) — this delivers it.
- **Durability 4 → 5 (likely):** the deck is no longer dead to repeated Satya
  removal; the Kiki line closes from a board that doesn't include the commander.
- **Projected: 17 → 18–19/20.** Re-audit on application per
  `Deck_Index.md` rules (>3-card change is not triggered — this is 1 card — but
  the Core Loop description changes, which is a re-audit trigger).

---

## Decklist change (apply on acquisition)

When Kiki is acquired + pod-approved: copy the current `.txt`
(`the-replication-crisis-20260622.txt`) to `the-replication-crisis-<date>.txt`,
remove `1 Bident of Thassa`, add `1 Kiki-Jiki, Mirror Breaker`, verify 100 cards,
and move the old `.txt` to `archive/old_decklists/`. (Note: Kiki now stacks with
the Satya + Lightning Runner infinite added 2026-06-22 as a third, Satya-free
combo — see `The_Replication_Crisis_Swaps_2026-06-22.md`.)
