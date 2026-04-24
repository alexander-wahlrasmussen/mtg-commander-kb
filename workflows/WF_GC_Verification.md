# Workflow: Game Changer Verification

Confirming a deck's GC count is legal under the Bracket 3 cap of 3.

---

## Steps

### 1. Load the authoritative list

Read `REF_Game_Changers_List.md`. **Do not verify from memory.** The list changes — Deflecting Swat was removed in October 2025, and other cards may have shifted since. If the local list looks stale, re-verify against WotC's current published list before trusting it.

### 2. Resolve reskin aliases

Before grepping, translate every UB card in the decklist through `REF_Reskin_Aliases.md`. GC checks apply to the *original* MTG name:

- Aang's Shelter → Teferi's Protection (GC ✓)
- Wild Rose Rebellion → Counterspell (not a GC)
- Dawn Warriors' Legacy → Mizzix's Mastery (verify)

A reskin of a GC is still a GC.

### 3. Grep the decklist

Use `grep -iE` with a pipe-delimited pattern across canonical GC names. Example:

```bash
grep -iE "teferi's protection|jeska's will|smothering tithe|enlightened tutor|gamble|mana drain|cyclonic rift|fierce guardianship|rhystic study|mystic remora|drannith magistrate|aang's shelter|wild rose rebellion" decklist.txt
```

Include every GC candidate you suspect. Grep is cheap; misses are expensive. Iterate once if unsure.

For reskins that map to GCs, include *both* the reskin name and the original in the pattern so the grep catches whichever form the decklist uses.

### 4. Count and classify

- Each matched card is one GC slot, even if the decklist uses the reskin name.
- If a card matched twice (once under reskin name, once under original), deduplicate — it's one card.
- Report count: X/3.

### 5. Handle overage

If the count is above 3:

- **Stop.** Do not unilaterally decide which to cut.
- Report the overage and identify which GCs are load-bearing for the deck's core loop and which are swappable.
- Propose candidate cuts with replacements in the same role (see `WF_Card_Swap_Evaluation.md`).
- Ask the player to confirm the cut.

### 6. Report

Standard format:

```
GC slots: X/3
  1. [Card A]  [(reskin: Reskin Name)]
  2. [Card B]
  3. [Card C]

Flagged (commonly assumed to be GCs but aren't): [list, if any]
```

---

## Common false positives

Cards that are frequently assumed to be GCs but are not currently on the list:

- **Doubling Season** — not a GC.
- **Deflecting Swat** — removed October 2025.

Cards that are often missed because they've been on the list only recently:

- *(Add as identified.)*

---

## Do not

- Do not verify against memory. The list changes.
- Do not skip alias resolution — a decklist using reskin names will produce a false zero count.
- Do not count a card twice when both the reskin name and the original appear in your grep pattern (deduplicate).
- Do not finalize a deck with GC count above 3. The cap is a hard rule, not a guideline.
