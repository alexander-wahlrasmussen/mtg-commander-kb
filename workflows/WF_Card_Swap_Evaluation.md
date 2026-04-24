# Workflow: Card Swap Evaluation

Evaluating a proposed swap before endorsing it. This is the checklist that catches the "Aggravated Assault with firebending mana" class of error.

---

## Inputs

- Card(s) going out.
- Card(s) coming in.
- Current decklist and stated core loop.

---

## Steps

### 1. Read the card

**Non-negotiable.** If the proposed card is new, unfamiliar, or a UB reskin:

- Web-search the Oracle text on Scryfall.
- Check for: zone restrictions, timing restrictions (instant vs sorcery vs activated ability timing), cost structures (X costs, kicker, foretell), triggered vs activated abilities, and any keywords with non-obvious rules.
- UB-specific keywords with non-obvious rules: **firebending**, **waterbending**, **airbending**, **earthbending**. Check expiration timing.
- Check type line carefully. Legendary vs non-legendary matters for clone strategies.

Do not rely on pattern-matching from the card's name, art, or set.

### 2. Check the role

What slot is the outgoing card filling?

- Engine piece / payoff / ramp / draw / interaction / tutor / finisher / utility / flex?

Does the incoming card fill the same role?

- If yes: is it strictly better, contextually better, or a lateral move?
- If no: what role is being added, and what role is being reduced? Is the reduction acceptable?

### 3. Check the math

- **Engine piece count:** does the swap change it? Target is 15+ for a healthy Core Loop.
- **Interaction count:** does the swap change it? Floor is 8.
- **Game Changer count:** cross-reference `REF_Game_Changers_List.md`. Did the swap add or remove a GC?
- **Curve:** does the swap push the deck into a problematic mana profile?
- **Color requirements:** does the swap demand tighter color sources the mana base can't support?

### 4. Check the interactions

- Does the incoming card actually combine with the deck's core loop? (e.g., firebending mana can't fuel sorcery-speed activations after combat; verify timing before endorsing infinite-combat pieces.)
- Does it create a banned combo line with existing cards? (Early two-card infinite = pod approval needed.)
- Does it require support the deck doesn't currently run? (Anointed Procession with 3 token producers is dead.)
- Does it conflict with another card's legend rule? (Two Zukos can't share the battlefield.)
- Does it occupy the same slot as another card you'd expect to see? (e.g., two 4-mana sweepers may be redundant.)

### 5. Check the collection

- Is the card owned? Follow this order:
  1. Check the Full Card Matrix in `deck_safe_collection.xlsx` under the canonical name.
  2. If not found, check `REF_Reskin_Aliases.md` for a UB alias and re-search.
  3. Only after both checks, declare unowned.
- If unowned: what's the Cardmarket.eu price? Should it go on the shopping list or be proxied for testing?

### 6. Report

Structured output:

```
Swap: [Out] → [In]

Role: [same role / role shifted from X to Y / role added / role reduced]
Axis impact:
  Core Loop:   [+/0/-] — [reason]
  Kill:        [+/0/-] — [reason]
  Durability:  [+/0/-] — [reason]
  Interaction: [+/0/-] — [reason]

GC count: [old count] → [new count]
Ownership: [owned / need to buy €X / available for proxy]

Verdict: [endorse / endorse with caveat / decline]
Caveat (if any): [what needs to change to make this work]
```

---

## Do not

- Do not endorse a swap because the incoming card is popular, expensive, or well-reviewed generally.
- Do not endorse a swap without naming the role it fills.
- Do not assume card text. The cost of looking it up is 10 seconds; the cost of a wrong recommendation is a rebuild.
- Do not endorse a swap that pushes GC count above 3 without flagging it explicitly.
