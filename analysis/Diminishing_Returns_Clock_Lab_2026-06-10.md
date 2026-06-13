# Diminishing Returns — Kill-Turn Lab & Clock-Upgrade Judgment (2026-06-10)

**Deck:** Diminishing Returns (Teysa Karlov — Orzhov aristocrats / sacrifice-drain)
**Lab:** `scripts/dr_clock_lab.py` (modes `clock`, `levers`; 12,000 trials, seed 12345)
**Decklist:** `decks/diminishing-returns-20260505.txt`
**Question:** Verify the unverified "Goldfish T7–9" claim; judge whether the clock can be upgraded.

---

## Verdict

1. **The claimed window is FALSIFIED — optimistic, like 6 of the 7 prior
   falsifications (running tally now 7 of 8).** Goldfish: **decap median T9
   (11% T7, 37% T8, 66% T9) / table median beyond T12 (30% by T12)**. Read as
   a decap claim, "T7–9" sits at its own back edge; read as a table claim it
   is 3+ turns optimistic.
2. **Decap and table DIVERGE here (unlike the Genome Project).** The decap
   clock is the wide aristocrats board swing (focus-fire); the table clock is
   the drain engine, and its volume is low. This deck decapitates like a
   combat deck and tables like a grinder.
3. **The bottleneck is death VOLUME, not multipliers.** Once Teysa + payoffs
   assemble, each death drains 4–8 from every opponent — but the deck only
   produces ~5 deaths per game in goldfish. Multiplier, mana, and tutor levers
   are all flat; only the token axis (more bodies) shows any signal.
4. **No card-text errors found.** The 2026-05-13 audit's oracle pass holds —
   every modelled piece re-verified clean against `card_lookup.py`.

---

## 1. Method

Kill-turn goldfish on the `speed_lab_core.py` harness, conventions per
`gp_clock_lab.py` / `gd_clock_lab.py`: 3 opponents @ 40, unblocked combat,
mana = lands + rocks floor, London mulligan via `deck_sim.py`. Decap and
table reported separately per the verification rule.

Per creature death, to EACH opponent (all oracle-verified 2026-06-10):

```
nontoken: (Zulaport + Elas + Meathook + Konrad + Agent*) x teysa2
token:    + Nadier x teysa2, + Mirkwood (sac trigger — NOT doubled)
Kokusho:  + 5 x teysa2        Vindictive Lich: 5 single-target x teysa2
* Agent of the Iron Throne grants its trigger TO Teysa — dead without her.
```

**Modelled:** Teysa doubling (death triggers of permanents only — activated
abilities and ETBs excluded per her ruling), board liquidation once the
multiplier is set, Skullclamp loops (Teysa-doubled to draw 4 per mana; the
Gravecrawler+Zombie clamp cycle), Kokusho sac-reanimate cycles, Gray Merchant
devotion ETBs (live pip count), Living Death bursts, Razaketh fetching the
missing combo piece, K'rrik pip-for-life payment, Endrek Thrulls, Urza's Saga
(Constructs + fetch Skullclamp), full-board attacks, and the **Gravecrawler +
Phyrexian Altar + Zombie + payoff infinite as an immediate table kill**.
**Omitted (conservative):** Esper Sentinel + Smothering Tithe (opponent
behaviour), scry/selection from Seer/Strider, Phyrexian Tower, Sephiroth's
ETB sac-draw, Soldevi Adnate ramp.
**Optimistic (noted):** colour-blind mana, same-turn rocks, whole board
swings every turn, Endrek's 7-Thrull cap ignored, no opposing interaction.

## 2. Baseline clock

```
P(kill <= T) %             T4    T5    T6    T7    T8    T9   T10   T12
decap (one opponent)        0     0     1    11    37    66    84    96
table (all three)           0     0     0     0     2     4    10    30
median decap T9 / table >T12 · never-in-12: 70% (table)
```

**Canonical line:** `Clock: T9 decap / T12+ table (lab 2026-06-10, dr_clock_lab.py)`

The shape: engine assembly T5–7 (Teysa + outlet + payoff), then the board
swing decapitates the focus opponent around T8–10 while drains chip the other
two. The infinite (Line 1) fires in ~3% of games inside the horizon — it is a
4-piece assembly with no in-deck tutor redundancy beyond Razaketh.

Reconciliation with the Summary's Kill Reliability text ("2–3 turns from
engine-online"): that holds for DECAP (engine T6–7 → first kill T9). The
header's "Goldfish T7–9" was the optimistic compression of it.

## 3. Lever test — death volume is the only axis with signal

2-card packages cut the goldfish-deadest slots (Mother of Runes, Skrelv);
the 4-card probe also cuts Generous Gift and Swiftfoot Boots. Demonic /
Vampiric tutor axis EXCLUDED (GCs; deck capped 3/3 — verified current list).

| Variant (adds) | T8 table | T10 table | T12 table | never-12 |
|---|---|---|---|---|
| BASE | 2 | 10 | 30 | 70% |
| +drains (Bastion of Remembrance, Cruel Celebrant) | 2 | 12 | 31 | 69% |
| **+tokens (Bitterblossom, Ophiomancer)** | 2 | **14** | **37** | **63%** |
| +deathmana (Pitiless Plunderer, Pawn of Ulamog) | 2 | 11 | 29 | 71% |
| +tutors (Buried Alive, Diabolic Intent) | 2 | 12 | 32 | 68% |
| +best4 (Bastion+Celebrant+Plunderer+Bitterblossom) | 3 | 16 | 40 | 60% |

Decap is flat in every variant (T9 median, ±2pp). No variant moves the table
median inside the 12-turn horizon.

**Why flat, per axis:**
- **+drains:** the multiplier is already 4–8 per death when assembled; adding
  payoff #5–6 multiplies deaths that aren't happening.
- **+deathmana:** mana is not the gate — the deck floats spare mana most
  turns once liquidation play patterns are available.
- **+tutors:** the infinite needs 4 pieces; one tutor finds one. Buried Alive
  feeds reanimation but the reanimation targets weren't the bottleneck.
- **+tokens:** the only axis pointed at the real constraint (bodies to kill).
  Bitterblossom/Ophiomancer add a recurring death per turn through every
  multiplier, plus Skullclamp fuel, plus attackers. +7pp at T12 and the
  biggest never-kill reduction — real, but incremental, not a clock change.

## 4. Judgment: can the clock be upgraded?

**Not meaningfully, within the deck's identity.** Two structural facts:

1. **Death volume is commander-external.** Teysa doubles triggers but makes
   no bodies. Every body is a card; recursion (Gravecrawler, reanimation) is
   piece-dependent. The deck's ~15 interaction/protection slots — its actual
   pod value as the attrition deck — are goldfish-dead, and a goldfish lab
   punishes exactly that composition. Converting them to token generators
   wholesale would change the deck's role, not polish it.
2. **The infinite is the only fast table kill and it's a 4-piece assembly**
   (Gravecrawler + Phyrexian Altar + Zombie + payoff) with Razaketh as the
   only true tutor. That is by design — Bracket 3 compliance ("does not
   consistently assemble before turn 6"). Making it consistent means tutors,
   and the GC tutors are cap-blocked.

This deck is the roster's **Disrupt** archetype, not a racer: it decapitates
on schedule (T9) and grinds the rest. The honest clock annotation reflects
that split.

**Recommendation — one optional polish swap, pilot's call:**
- − Mother of Runes, − Skrelv, Defector Mite → **+ Bitterblossom (owned,
  undeployed — $0)** + Ophiomancer (~€3, unowned, no reskin alias): +7pp
  table by T12, never-kill 70→63%, decap unchanged. The cuts cost real
  protection for Teysa — the lab cannot see that value, so this is explicitly
  NOT a lab mandate. If only one slot moves: **Bitterblossom in, Skrelv out**
  is the free, lowest-regret version.
- Bastion of Remembrance / Cruel Celebrant / Pitiless Plunderer / Pawn of
  Ulamog: none earn a slot on these numbers (Plunderer also deployed in The
  Dark Lord's Army; Buried Alive ×2 and Diabolic Intent ×2 owned but all
  deployed elsewhere — contested, and flat here anyway).

## 5. Ownership / availability notes

- **Bitterblossom: owned (SPG), undeployed** — the standout.
- Buried Alive: owned ×2, both deployed (Curse of the Scarab, Grand Design).
- Diabolic Intent: owned ×2, both deployed (Dark Lord's Army, Exile's Return).
- Pitiless Plunderer: owned, deployed (Dark Lord's Army).
- Not owned (reskin aliases checked — none): Bastion of Remembrance, Cruel
  Celebrant, Pawn of Ulamog, Ophiomancer, Blood Artist, Falkenrath Noble.
  All ≤€4; none earn a buy on these numbers except optionally Ophiomancer.
- Blood Artist / Falkenrath Noble were screened and rejected before the lab:
  both are "target player" single-drains, not Zulaport-class each-opponent.

## 6. Framework note

Tally update: **7 of 8 labbed decks falsified their hand-estimated kill
windows, all optimistic.** The Genome Project remains the only survivor.
This deck adds a new failure mode to the record: the claim wasn't just
shifted — it conflated the two clocks. Decap-vs-table divergence (T9 vs
T12+) is the largest measured so far alongside Grand Design (T10/T12+).
