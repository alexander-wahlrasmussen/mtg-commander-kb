# The Replication Crisis — Lightning Runner Swap (2026-06-22)

**Goal:** optimize the deck with **owned cards only**, now that infinite combos
are pod-accepted ([[infinites_ok_in_pod]], 2026-06-19). The physical deck was 3
cards short (Goldspan Dragon, Ponder, Preordain — each physically deployed in
another deck), so those slots were already free. The core fix turns the empty
slots into the deck's most-available infinite; a follow-up pass (part **b**)
swapped two more contended/weak cards for better-available interaction.

**Status:** **APPLIED.** New `.txt`: `the-replication-crisis-20260622.txt`; old
`…-20260504-202914.txt` moved to `archive/old_decklists/`. No purchase required.

Card text verified against local Scryfall data 2026-06-22 ([[feedback_read_card_first]]):
Satya, Lightning Runner, Sleight of Hand, Opt, Sublime Epiphany, Winds of Abandon.

---

## The swap (5-for-5, all owned)

**Part a — the Lightning Runner infinite (fills the 3 empty slots):**

| Out | In | Why |
|---|---|---|
| Goldspan Dragon | **Lightning Runner** | Goldspan is 1-owned and physically in Lightning War → the RC slot was empty. Lightning Runner completes the **Satya + Lightning Runner** infinite. |
| Ponder | **Sleight of Hand** | Ponder is a 1-of shared across 4 decks (physically elsewhere). Sleight of Hand (dig-2) is owned + unallocated. |
| Preordain | **Opt** | Same contention. Opt (2 owned, 1 free) replaces the selection 1-for-1. |

**Part b — interaction tune (2026-06-22 follow-up):**

| Out | In | Why |
|---|---|---|
| Expansion // Explosion | **Sublime Epiphany** | E // E was needed in Lightning War (contended). Sublime Epiphany ({2}{U}{U} instant, 2 owned + unallocated) is a strictly more flexible modal answer — counter spell/ability, bounce, **copy a creature you control** (ETB synergy), or draw. |
| Bident of Thassa | **Winds of Abandon** | Bident = the prior Kiki proposal's earmarked weakest card (redundant with One Ring / Remora / Esper / Archivist / Cloudblazer). Winds (overload {4}{W}{W}) is the deck's **second mass answer** — a one-sided creature wipe, which a go-wide deck wants over a symmetric wrath. 1 owned + unallocated. |

**Card count 99 + commander = 100** (verified). **GC count 3/3 unchanged**
(Fierce Guardianship, Cyclonic Rift, The One Ring; none of the five added cards
is a Game Changer — checked against `REF_Game_Changers_List.md`).

**Score:** Conversion Check **17 → 18/20**. Kill Reliability stays 4 (LR still
needs Satya to connect). **Interaction 4 → 5** — part b retires both reasons the
axis was capped (no 2nd wipe; weak flexible counter), caveat that Winds is a soft
6-mana sweeper that ramps opponents. Removing E // E also drops the Narset's
Reversal + E // E "infinite magecraft" near-combo (no payoff here, no loss).

---

## The combo (text-verified, CSB [4918-5658])

- **Satya, Aetherflux Genius** — `{1}{U}{R}{W}`, menace/haste. "Whenever Satya
  attacks, create a tapped and attacking token copy of up to one other target
  nontoken creature you control. You get {E}{E}. At the next end step sacrifice
  that token unless you pay {E} equal to its mana value."
- **Lightning Runner** — `{3}{R}{R}`, 2/2, double strike, haste. "Whenever this
  creature attacks, you get {E}{E}, then you may pay eight {E}. If you pay, untap
  all creatures you control, and after this phase, there is an additional combat
  phase."

**Loop.** Both real Satya and real Lightning Runner attack → +2{E} each. Satya
makes a **token copy of Lightning Runner** (it enters tapped + attacking, so its
own "whenever attacks" does **not** fire that combat — same ruling as
Adeline/Phelia copies). Pay 8{E} on the real Runner → untap all creatures + an
extra combat. In the **next** combat the token Runner is untapped and **declared**
as an attacker, so it triggers too. Per-combat energy = `2 × (Satya + every
Lightning Runner attacking)`:

| Combat | Runners attacking | Energy generated | Net after paying 8 |
|---|---|---|---|
| 1 | 1 | 4 | −4 |
| 2 | 2 | 6 | −2 |
| 3 | 3 | 8 | 0 (self-sustaining) |
| 4+ | 4+ | 10+ | +2, +4, … (runs away) |

So it goes infinite once the **bank survives to combat 3** — needs ~6 banked
energy (4 with Anointed Procession, which doubles the token Runners so you reach
3 Runners a combat sooner). Satya banks 2{E} every attack, so a turn or two of
prior Satya attacks covers the bootstrap. Tokens persist through the loop (the
end step never arrives). Lethal regardless of blockers: copy **Inferno Titan**
for infinite ETB pings, or just swing with the infinitely-growing double-strike
Runner pile.

This is **not** infinite turns and **not** mass land denial — it is infinite
combat *phases*, the same category as the deck's existing Sword + AA line, which
is pod-accepted.

---

## Why it's the right add (lab benchmark)

`scripts/rc_speed_lab.py` (40k trials, seed 12345) — extended 2026-06-22 to model
the LR cascade (avail + a goldfish clock); prints CURRENT (with LR) vs LEGACY
(pre-LR 99) so the before/after is one command. Reproduce: `python
scripts/rc_speed_lab.py --trials 40000`.

### Availability — P(a complete infinite is in hand/play ≤ T), drawn, no tutors

| | T6 | T8 | T12 |
|---|---|---|---|
| LEGACY: Sword + AA (only infinite) | 1% | 2% | 3% |
| CURRENT: Satya + Lightning Runner | **12%** | **14%** | **18%** |
| CURRENT: ANY kill package | **24%** | **28%** | **37%** |
| (legacy ANY kill package) | 14% | 16% | 22% |

The jump is structural: one combo half is the commander, so availability is just
P(draw a single card) instead of P(draw a specific pair).

### Clock — P(kill ≤ T), goldfish, mana-aware

| | T6 | T8 | T10 | T12 |
|---|---|---|---|---|
| Table dead **via an infinite** — LEGACY | 1% | 1% | 2% | 3% |
| Table dead **via an infinite** — CURRENT | **5%** | **12%** | **16%** | **18%** |
| SQUAD (defended board) table dead — LEGACY | 1% | 2% | 16% | 47% |
| SQUAD (defended board) table dead — CURRENT | **5%** | **12%** | **28%** | **56%** |
| Decap (combo player dead), ALL-IN — LEGACY | 14% | 78% | 94% | 98% |
| Decap (combo player dead), ALL-IN — CURRENT | 18% | 80% | 94% | 99% |

**Read:** the realistic (defended-board) table-closing rate roughly doubles and
the win-via-infinite rate rises 4–6×, while the **decapitation clock is
essentially unchanged**. This is a reliability/closing upgrade, **not** a speed
one — the deck still isn't a T6–7 racer, so the 2026-06-09 speed-curve verdict
stands (don't bring it to out-race the combo pod; bring it as a flexible value
engine that can now actually close).

---

## Relation to the pending Kiki swap (`…_Swaps_2026-06-01.md`)

Lightning Runner is the **better-value resilience add** and it's **free**:

| | Satya + Lightning Runner (this swap) | Kiki + Conscripts/Resto (pending) |
|---|---|---|
| Owned? | **Yes** (was in the sideboard) | No — ~€10–15 buy |
| Availability T6 / T12 | **12% / 18%** | 2% / 6% |
| Needs the commander? | Yes (Satya must attack) | **No** (combat-step-independent) |
| Pod approval | Not needed (infinites OK 2026-06-19) | Was flagged (2-card infinite) |

The one thing Kiki does that LR doesn't is win **without** Satya / without a
combat step — that's why Kill Reliability stays 4/5 here (a 5 needs a
combat-independent kill). If a Kiki is ever acquired it stacks with this (a third
infinite, Satya-free); until then LR is the owned, higher-hit-rate closer.

**Note:** part b cut **Bident of Thassa**, which was that pending Kiki swap's
donor (−Bident +Kiki). So if Kiki is later acquired it now needs a *different*
donor (Strionic Resonator is the lab's illustrative choice). Tracked in
`…_Swaps_2026-06-01.md`.

---

## Available bench after the swap (owned, not deployed elsewhere)

Bident of Thassa (just benched), Combat Celebrant (one-shot extra combat — flex
for more clock), Inspiring Overseer, Coalition Relic, Reprieve, a 2nd Sleight of
Hand. **Not** available: Goldspan Dragon / Ponder / Preordain / Expansion //
Explosion (each physically in another deck), Arcane Denial (1 owned, in three
other decks' mains).
