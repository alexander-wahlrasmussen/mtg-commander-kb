# The Replication Crisis — Imperial Recruiter swap (2026-06-30)

**Goal:** improve the *availability* of the deck's primary win condition — the
Satya + **Lightning Runner** energy-combat infinite (applied 2026-06-22) — by
adding a second findable path to Lightning Runner. This is the "tutor the
primary line" lever flagged when the [[project_replication_crisis_b4_swap]]
Kiki-Jiki *third infinite* was declined the same day: a goldfish lab can't
score Satya-removal insurance, but it *can* score how often the kill is online,
and a tutor for the existing line beats a rare extra combo.

**Status: APPROVED 2026-06-30 — buying a 2nd copy. `.txt` NOT yet bumped.**
The single owned Imperial Recruiter is physically deployed in **Exile's Return**
(`the-exiles-return-20260417-194010.txt`), so this requires a second copy rather
than a free reallocation. Apply the swap to a new dated `.txt`
(`the-replication-crisis-<arrival-date>.txt`, old version → `archive/old_decklists/`)
once the card is in hand. Tracked as on-order in [[project_build_swap_tracker]].

Card text verified against local Scryfall data 2026-06-30
([[feedback_read_card_first]], [[feedback_check_card_legality]]).

---

## The swap

| Out | In | Why |
|---|---|---|
| Strionic Resonator | **Imperial Recruiter** *(buy 2nd copy — price unverified; budget-reprinted, confirm before ordering)* | Strionic is a generic "copy a triggered ability" value artifact — it is **not a piece of any of the deck's four kill packages**, so cutting it costs no kill line (Sword+AA stays live). Imperial Recruiter ({2}{R}, ETB: search a creature **power ≤ 2** → hand) fetches **Lightning Runner** (a 2/2), giving the deck a *second* way to assemble its primary infinite — draw LR **or** draw the tutor. |

1-for-1. **Card count stays 99 + commander = 100** (deck_doctor-verified at 100,
3/3 GC: Cyclonic Rift, Fierce Guardianship, The One Ring). **GC count stays 3/3**
— neither Strionic nor Imperial Recruiter is a Game Changer (Recruiter checked
unanchored against `REF_Game_Changers_List.md`, [[feedback_gc_list_removed_section]]).

---

## Lab evidence — `rc_speed_lab.py --mode avail` (40k, seed 12345, 2026-06-30)

Recruiter is modelled as: *Recruiter seen ⇒ Lightning Runner accessible* — the
same drawn-only abstraction the lab already uses for "a tutor fetches its target
to hand." Because Recruiter's only combo-relevant target is the single card LR,
the one-fetch-per-cast limit doesn't distort the line. Donor is Strionic (in no
package), so **all four kill lines stay live**.

| Line | T6 | T12 |
|---|---|---|
| Satya + Lightning Runner (current — draw LR only) | 11% | 18% |
| **Satya + LR (draw LR *or* Recruiter)** | **22%** | **32%** |
| ANY of the four kill lines (current) | 24% | 36% |
| **ANY of the four (−Strionic +Recruiter)** | **33%** | **48%** |

Recruiter roughly **doubles** how often the primary infinite is online and lifts
the deck's overall kill-availability by ~9–12 pp. For contrast, the declined
Kiki *third infinite* assembled only ~6% by T12 — Recruiter is the better buy
because it is **on-axis** (the primary line) rather than a rare backup, and it is
a commander-independent *find* rather than a 2-card stack.

---

## The honest caveat

This is a **reliability** upgrade, not a **speed** one. The decap and table
*clocks do not move* — Recruiter changes how *often* the kill is assembled by a
given turn, not the earliest turn it can happen
([[feedback_selection_vs_mana_gated]]: Replication Crisis is a finding-gated
deck, so availability is the right lever). Replication Crisis still **cannot
out-race a T6–7 pod** ([[project_replication_crisis_speed_analysis]]); its decap
is ~T7 / table ~T10+. The swap raises the floor (kill is online more often,
survives a Satya-light board better), it does not turn the deck into a racer.

The Kill Reliability score (currently 4/5) is the dimension this targets; whether
it tips to 5/5 is a post-swap audit question once games are played — not claimed
here ([[feedback_lab_before_proposing]]).
