# Workflow: Deck Audit

Scoring an existing deck against The Conversion Check.

---

## Inputs

- Current decklist (the `.txt` file is ground truth — not the summary).
- Commander.
- Core loop description from the player, if available.

---

## Steps

### 1. Sanity check the list

- Confirm 99 + 1 commander. If the count is off, stop and ask.
- Identify the commander's color identity. Confirm all cards are in-identity.
- Verify GC count using `WF_GC_Verification.md`. If above 3, stop and report.

### 2. Identify the Core Loop

Extract or ask:

- What resource does this deck exploit?
- How is that resource converted into advantage?
- What is the repeatable *machine* (not the payoff — the engine)?

Count the cards that **directly serve the loop**. Payoffs, staples, mana, and flex slots don't count. Only engine pieces.

### 3. Score each axis (1–5)

Apply the rubric in `REF_The_Conversion_Check.md`. Every score anchors to a count:

- **Core Loop:** engine pieces. 15–18 = 4. 18+ with redundancy = 5. Below 10 = 2.
- **Kill Reliability:** name the closing lines. Two minimum. Estimate turns from engine-online to lethal.
- **Durability:** count redundant engine pieces. Mentally resolve a Cyclonic Rift on turn 7 and count turns to threat re-establishment.
- **Interaction:** count removal + counters + targeted disruption. Below 8 = gamble = 2.

If a score can't be anchored to a count or a named line, it's a guess. Ask for more info before scoring.

### 4. Apply archetype notes

From the Conversion Check framework:

- **Aggro / Swarm:** Core Loop and Kill Reliability often overlap. Expect Durability and Interaction to be weaker.
- **Control:** Kill Reliability legitimately low. Compensated by Durability + Interaction.
- **Stax / Prison:** Pressure = denial. Kill Reliability low; Interaction carries.
- **Combo:** Kill Reliability binary. Score Durability on post-failed-combo recovery.
- **Goodstuff:** May score low on Core Loop honestly. That's the trade.

A deck's total can be lower than 17 and still be structurally honest for its archetype.

### 5. Report

Structured output:

```
Deck: [Name]
Commander: [Name] ([colors])
Archetype: [type]

Score: CoreLoop / Kill / Durability / Interaction = Total/20
       X       / X    / X          / X           = XX/20

Core Loop: [one sentence]
Closing lines:
  1. [name] — [turns from engine-online]
  2. [name] — [turns from engine-online]

Kill Window:
  Goldfish: T[X]–[Y]
  Through Interaction: T[X]–[Y]

Lowest axis: [name] — [what's driving it]
Cut candidates if tightening: [list]
Add candidates if strengthening the low axis: [list]

Game Changer slots: X/3 — [list with aliases]
```

---

## Do not

- Do not inflate scores to match the player's enthusiasm for the deck.
- Do not score axes that weren't measurable from the list — ask first.
- Do not treat the commander's flavor or tribal identity as part of the Core Loop unless the engine actually runs on the commander.
- Do not round up. A deck at 16 is a 16, not a 17.
