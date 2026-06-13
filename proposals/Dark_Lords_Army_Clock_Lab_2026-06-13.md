# The Dark Lord's Army — Kill-Window Clock Lab (2026-06-13)

Deck 10 of the Kill-Window Lab Sweep (`Kill_Window_Lab_Sweep_2026-06-13.md`) — the
**last row; the sweep is now complete.** Lab: `scripts/dla_clock_lab.py` (40 000 trials,
seed 20260613). Deck: `decks/the-dark-lords-army-20260417-211206.txt`. Commander: Sauron,
the Dark Lord (Grixis). Score: **19/20**.

---

## This deck cannot be goldfished like the others

Its entire engine is **opponent-driven** (verified Stage 0): Sauron amasses on *opponents'*
spells, and the drain (Sheoldred + Underworld Dreams + Orcish Bowmasters) punishes
*opponents'* draws; Wound Reflection doubles each opponent's loss. A self-contained goldfish
(no opponents) would show it killing ~never and grossly misrepresent it. So — like
`delay_lab.py` vs a pod combo turn — this lab models an explicit **pod-activity assumption**
(opponent spells/cycle feed amass, opponent draws/cycle feed the drain) and runs it at LOW /
MID / HIGH tempo. The clock is a *function of that assumption*, stated, not a single number.

## Claim vs measured (tempo-dependent)

| Pod tempo (opp spells / draws per cycle) | decap | table | table never-in-16 |
|---|---|---|---|
| LOW (3 / 3) — durdle pod | T10 | T15 | 29% |
| **MID (6 / 4) — typical Bracket-3** | **T9** | **T12** | 10% |
| HIGH (9 / 6) — spell-dense / cantrip pod | T8 | T11 | 6% |

Claim: "Goldfish T8–10 / through interaction T10–12."

**Verdict: among the best-corroborated claims in the sweep.** decap lands **T8–T10** across the
realistic tempo range — exactly the claimed window — and at typical (MID) tempo the **table is
T12**, squarely in the claimed T10–12 interaction window. The hand-estimate was good. The new
findings are (1) the clock is **uniquely tempo-dependent** — this deck kills *faster* the more
active the pod is (more spells = more amass, more draws = more drain), the opposite of every
other deck's goldfish — and (2) the usual decap/table split (decap leads the table by 2–3, more
vs a slow pod).

## Kill shape — MIXED, drain-dominant CONVERGE (prediction held)

- **table (the win)** set by the **drain web** (`hit_all`): per opponent draw, Sheoldred 2 +
  Underworld Dreams 1, doubled by Wound Reflection, plus Gray Merchant's ETB devotion drain.
  Symmetric across opponents → converge.
- **decap** led by the **Army voltron** (focus) — amass grows it on opponent spells, evasion
  makes it unblockable — plus Bowmasters' bonus-draw pings.

## Note on the documented pod

Against the archenemy (`project_pod_combo_opponent`: T6–7 combo behind Grand Abolisher — a
**spell-dense, high-tempo** pod), this deck is at its **fastest** (HIGH tempo: decap T8 / table
T11) *because* that pod feeds its amass+drain. But T8/T11 still doesn't out-race a T6–7 combo —
the deck's real plan there is its 15-piece interaction suite + oppression (Propaganda, the drain
tax) + Sauron's defensive Ring lifegain to survive and grind, which the 19/20 (Durability 5 /
Interaction 5) reflects. It out-grinds; it does not race.

## Engine modelled (oracle-verified, no card-text errors)

Self mana (lands + rocks) deploys the engine + the 6-mana commander; amass = SPELLS/cycle while
Sauron is out; drain per opp = (DRAWS/3) × (2·Sheoldred + 1·UD), `hit_all`, doubled by Wound
Reflection; Bowmasters bonus pings focus; Gray Merchant ETB = devotion (summed B pips of the
deployed black engine). **Omitted (conservative):** aristocrats grind (Dictate + Bombardment +
Plunderer forced sacs), graveyard-reset reanimation, Strionic copies, Barad-dûr self-amass,
Yawgmoth, redundant amass (Call of the Ring / Nazgûl ×4). **Optimistic:** steady assumed tempo,
rocks tap turn they land, no interaction with our engine.

## Disposition

No card swaps (verification pass only). 19/20 stands. The clock confirms the deck's grind-drain
identity and adds the key nuance the single number missed: **its kill turn scales with pod
activity** (decap T8–10 / table T11–15), and at typical tempo it lands decap T9 / table T12 —
matching the claim well.

### Summary Kill Window field → replace with

**`Clock (vs pod-activity — engine is opponent-driven): decap T8–10 / table T11–15 by pod tempo; typical (MID) decap T9 / table T12 (lab 2026-06-13, dla_clock_lab.py). Kills FASTER vs active pods (amass/drain feed on opponents' spells+draws). Claim T8–10 / interaction T10–12 corroborated.`**
