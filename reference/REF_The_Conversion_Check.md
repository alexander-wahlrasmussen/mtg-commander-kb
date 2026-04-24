# The Conversion Check

A deckbuilding and piloting framework for Commander.

---

## Purpose

Build decks that convert advantage into wins. Evaluate them honestly. Pilot them deliberately.

This framework separates three things most deckbuilding tools blur together: the deck as an object, the table it sits in, and the player running it. Each layer has its own evaluation. Mixing them creates false diagnoses — a piloting failure looks like a deckbuilding flaw, a pod mismatch looks like a structural weakness. The Conversion Check keeps them apart.

---

## Part 1 — The Deck

These are properties of the 99 and the commander. They can be evaluated from a decklist without shuffling up.

Four axes. Each scored 1–5.

---

### Axis 1: Core Loop

*In one sentence, what resource does this deck exploit, and how does it turn that resource into advantage?*

This is the deck's mechanical identity. Not its flavor, not its theme — its engine. A deck's identity is its engine in practice. A deck that feels like something but doesn't do anything has flavor, not identity.

Ask:

- What is the repeatable loop? Not the payoff — the machine.
- How many cards in the deck directly serve this loop? Target: 15–20.
- Can the deck find or rebuild the loop after disruption?
- Does the commander enable the loop, or is the loop independent?

Checkpoint: If someone fans out the deck and covers the commander, can they identify the core loop from the cards alone?

---

### Axis 2: Kill Reliability

*Once this deck is online, how fast and reliably does it end the game, and how many distinct paths can it take to get there?*

This axis measures the full arc from threatening to winning. How quickly does the engine become lethal? How many ways can the deck close? Can it finish through disruption, or does a single answer shut it down?

A deck that pressures without closing has a slow kill clock. A deck that stalls between threatening and winning has unreliable conversion. A deck that lacks real finishers has no closing lines. All three problems show up here.

Ask:

- How many turns from engine-online to game-over?
- How many distinct closing lines does the deck support? Minimum two real ones.
- Can the deck close through common disruption — a wipe, a counterspell, targeted removal?
- Does the deck draw disproportionate hate before it can actually close?

Checkpoint: Name two different ways this deck ends the game and estimate how many turns each takes from engine-online.

---

### Axis 3: Durability

*What happens to this deck after a board wipe, commander removal, or targeted hate?*

A deck that cannot survive disruption cannot win real games. Durability measures both redundancy (enough backup pieces to restart the loop) and resilience (the ability to recover quickly after a reset).

Ask:

- How many redundant engine pieces exist? Can the loop restart after losing a key card?
- How many turns does recovery take after a full reset?
- Does the deck fold to common hate cards in its meta?
- Is the commander a critical dependency, a strong accelerant, or functionally optional?

Checkpoint: Mentally resolve a Cyclonic Rift against the deck on turn 7. How many turns before it's threatening again?

---

### Axis 4: Interaction Profile

*Can this deck stop the scariest thing at the table, and can it do so without derailing its own plan?*

Interaction density and quality determine whether a deck participates in the real game or merely goldfishes alongside it. A deck with no answers is gambling that nobody else will try to win first.

Ask:

- How many interaction pieces does the deck run? Count removal, counterspells, stax effects, targeted disruption.
- Does the interaction hit the threats that matter in the expected meta?
- Is the interaction efficient enough to use without falling behind on tempo?
- Can the deck interact at instant speed or only sorcery speed?

Checkpoint: The player across from you is about to win. Do you have an answer in your 99, and can you realistically have it in hand?

---

## Part 2 — The Table

This is not a property of the deck alone. It is a relationship between the deck and the pod. It changes every time the pod changes. It is not scored — it is checked.

### Pod Fit Checklist

Answer yes or no. If more than one answer is no, the deck may need adjustment for this specific pod.

- Does the deck match the pod's stated or implied power level?
- Can the deck survive until its engine is online against the fastest deck at the table?
- Does the deck have answers that hit the most common win conditions in the pod?
- Can the deck function if it becomes the table's secondary target?
- Is the pilot comfortable with the social role this deck creates?

Revisit this checklist every time the pod changes. It is not a permanent property of the deck.

---

## Part 3 — The Pilot

Separated from deck evaluation. A low score on Kill Reliability might mean the deck can't close — or it might mean the pilot doesn't know when to go. These are different problems. The deck axes measure the object. This section measures the decisions.

### Pre-Game

- What is my plan A for this pod?
- Which opponent is most likely to win if I don't interact with them?
- What's the fastest I can close in this specific game?
- Do I need to play politically or assertively?

### In-Game

- Am I still setting up, or should I be pressing?
- Am I pressuring for a reason, or just painting a target on myself?
- If I tap out this turn, who wins?
- Am I interacting with the player who annoyed me, or the player who's actually ahead?
- What am I holding back to survive the clapback?
- If someone wraths right now, where does that leave me relative to the table?

### Post-Game

- When did I lose the game? Was it a deckbuilding failure or a piloting failure?
- Did I convert when I should have, or did I wait too long?
- Did I die to something my deck could have answered if I'd built or played differently?

Post-game review is where the conversion question does its best work. "Did I convert?" is a retrospective piloting question, not a prospective deckbuilding one. Ask it here.

---

## Part 4 — Functional Baseline

A checklist, not scored. Either the deck meets baseline requirements or it doesn't.

- Mana base: Enough sources, acceptable color distribution, lands enter untapped when it matters.
- Ramp: Enough acceleration for the deck's speed requirements.
- Card draw / selection: Enough to find engine pieces and recover from disruption.
- Protection: Ways to protect key pieces or the commander if commander-dependent.
- Recursion: Ways to retrieve key cards if relevant to the strategy.
- Utility: Flex slots that serve multiple roles.

House preference: Prefer cards that serve more than one function.

---

## Scoring Rubric

Four axes. Each 1–5. Total range: 4–20.

### 1. Core Loop

| Score | Description |
|-------|-------------|
| 1 | No identifiable repeatable loop, or the loop is incoherent. |
| 2 | A loop exists conceptually but is supported by fewer than 8 cards. Unreliable. |
| 3 | Real loop with moderate density (10–14 supporting cards). Sometimes comes together, sometimes doesn't. |
| 4 | Well-supported loop (15–18 cards). Consistently online by mid-game. Clear mechanical identity. |
| 5 | The loop is the deck. 18+ cards serve it. Immediately recognizable, highly redundant, hard to fully disrupt. |

Anchor: Count the cards. If you can't identify which cards are engine pieces versus payoffs versus staples, the loop is probably a 2.

### 2. Kill Reliability

| Score | Description |
|-------|-------------|
| 1 | The deck generates value but has no clear plan to end the game. |
| 2 | One fragile closing line exists. Impressive boards that don't translate into wins. |
| 3 | Two closing lines exist. Can win from a strong position, but the window is narrow or slow (5+ turns from engine-online to kill). |
| 4 | Two or more closing lines, at least one fast (2–4 turns from engine-online). Can close through light disruption. |
| 5 | Multiple fast, resilient closing lines. Strong positions regularly become decisive ones. |

Anchor: Estimate the turn count from engine-online to game-over. If you can't estimate this, the kill plan is probably a 2.

### 3. Durability

| Score | Description |
|-------|-------------|
| 1 | A single board wipe or commander removal effectively ends the deck's game. |
| 2 | Can recover from one disruption event, but two in a row is fatal. Commander-dependent with no backup. |
| 3 | Has redundant engine pieces and some recovery tools. Rebuilds after a wipe in 2–3 turns. Doesn't fold to common hate. |
| 4 | Meaningfully resilient. Multiple redundant engine copies, recovery built into the strategy. Commander is an accelerant, not a dependency. |
| 5 | Disruption-resistant by design. Recovers faster than opponents can re-deploy hate. |

Anchor: Count redundant engine pieces. If you have 2 or fewer backups for key loop cards, you're probably a 2.

### 4. Interaction Profile

| Score | Description |
|-------|-------------|
| 1 | Fewer than 5 interaction pieces, or interaction doesn't hit relevant threats. |
| 2 | 5–7 interaction pieces, narrow or expensive. Can sometimes stop a win attempt. |
| 3 | 8–10 interaction pieces with reasonable coverage. Handles most common threats. |
| 4 | 10–12 pieces, well-targeted for the expected meta. Includes instant-speed answers. Can stop a combo turn while continuing to develop. |
| 5 | 12+ pieces, diverse in type and timing. Can credibly threaten to stop any win attempt while maintaining its own game plan. |

Anchor: Count every card that can remove, counter, or prevent an opponent's threat. Below 8 is a gamble.

### Reading the Score

| Total | Assessment |
|-------|------------|
| 17–20 | Structurally excellent. Pilot skill is the main variable. |
| 13–16 | Solid foundation with at least one exploitable weakness. Identify the lowest axis and address it. |
| 9–12 | The deck has a plan but can't execute it reliably. Likely needs a significant rebuild in one or two axes. |
| 4–8 | The deck doesn't yet hold together. Revisit the Core Loop first. |

**No single axis compensates for a catastrophic gap in another.** A deck at 5/5/5/1 will lose games it should win. Minimum viable score in every axis is 2.

---

## Expected Kill Window

*Not scored. Stated as a descriptor on each deck's quick reference.*

The four axes measure structural quality — whether the deck *can* convert. The Kill Window measures *when* it typically converts, expressed as a turn range.

Two estimates per deck:

**Goldfish** — Uncontested. No interaction from opponents, average draws. When does the deck threaten lethal if left completely alone?

**Through Interaction** — Realistic pod. One board wipe, one piece of targeted removal, and occasional counterspells from the table. When does the deck close under normal pressure?

Guidelines for estimating:

- Count backwards from the kill line. What mana/board state does it require? What turn does the deck reliably reach that state?
- "Engine-online" is not "kill." The gap between them is already captured by Kill Reliability. The Kill Window captures the full arc from turn 1 to game-over.
- Goldfish estimates below T5 should be rare at Bracket 3. If your goldfish is T4, double-check that the line doesn't violate early combo restrictions.
- Through-interaction estimates more than 4 turns slower than goldfish suggest a Durability or Interaction problem — the deck can't protect its plan.

The Kill Window is not a quality judgment. A T10–12 control deck that scores 18/20 is not worse than a T6–8 aggro deck that scores 14/20. Use it for pod selection and threat assessment, not deck evaluation.

---

## Archetype Notes

Different strategies manifest these axes differently. The framework accounts for this — a low score in one axis is not always a problem if the deck's archetype compensates elsewhere.

**Aggro / Swarm** — Core Loop and Kill Reliability often overlap (the engine IS the kill). Score both honestly. Expect the total to be driven by Durability and Interaction, where aggro is typically weakest.

**Control / Draw-Go** — Core Loop is "answer threats efficiently, accumulate incremental advantage." Kill Reliability may be low by design. Acceptable if Durability and Interaction are high. A control deck at 2/2/5/5 = 14 is structurally coherent.

**Stax / Prison** — Core Loop is "deny opponents resources." Pressure manifests as denial, not aggression. Kill Reliability may be low. A stax deck at 3/2/4/5 = 14 is honest — the Interaction Profile carries the weight.

**Combo** — Core Loop is "assemble the combo." Kill Reliability is binary. Score Durability on recovery after a failed combo attempt, Interaction on whether the deck can protect the combo turn.

**Goodstuff / Value Piles** — May score low on Core Loop (no repeatable machine, just high card quality). That's an honest reflection. The framework names what these decks trade away for raw power. A pile at 2/4/4/3 = 13 is functional but structurally opportunistic.

**Politics / Group Hug** — Win conditions are often social, not mechanical. Score what's scorable. The Pilot section and Pod Fit Checklist matter more than the rubric for these archetypes.

---

## Build Rules

1. **Define the loop before choosing staples.** If a card doesn't serve the Core Loop, it needs a strong reason to exist in the deck.
2. **Count your engine pieces.** Fewer than 12 cards directly serving the loop means the deck is undergassed.
3. **Count your interaction.** Fewer than 8 interaction pieces means you're hoping opponents won't try to win.
4. **Name your closing lines.** Write them down. If you can't name two, the deck can't reliably end games.
5. **Test recovery mentally.** Board wipe on turn 7. How many turns until you're threatening again? More than 3 means you need more redundancy or recursion.
6. **Prefer dual-role cards.** Every slot that serves two functions compresses the deck and raises the floor.
7. **Don't confuse spectacle with lethality.** A scary board that can't close is a political liability, not a win condition.
8. **Be honest about the pod.** Fill out the Pod Fit Checklist before you sleeve up.

---

## The Core Test

A successful deck is not one that merely looks strong.

It is one that runs on a real loop, closes games reliably, survives disruption, interacts with the table, fits its pod, and is piloted with intention.

Value is not inevitability. Spectacle is not lethality. Looking dangerous is not the same as being decisive.

That is The Conversion Check.
