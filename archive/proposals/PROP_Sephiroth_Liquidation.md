# Proposal: Sephiroth Liquidation — the aristocrats rebuild (commander-drain variant + buys)

*Status: PIPELINE. Raised + lab-verified 2026-06-19. Supersedes `PROP_Yawgmoth_Liquidation.md`*
*as the lead aristocrats build (user picked Sephiroth + opened the budget to buy cards).*
*Decklist: `decks/considering/sephiroth-liquidation-20260619.txt` (100, parses clean, 3/3 GC).*
*Labs: `scripts/sephiroth_clock_lab.py` (+ diagnostic instrumentation of the Yawgmoth version).*

The "dismantle 3, build 1" line, v3. Same teardown (D-tier: Eldrazi Stampede, Crystal Sickness,
Diminishing Returns; Genome stays). Mono-black aristocrats, now **commander = Sephiroth**, with
7 targeted buys. Verdict-first, because the headline is a *diagnosis*, not a green light.

---

## Why Sephiroth (the user's call — and the diagnostic backs it)

Instrumenting the Yawgmoth build found the combo's gates were **piece redundancy**, not mana:
- **mana-gated: 0%** of stalled games (kills the "Coffers would fix it" theory).
- **Yawgmoth**: in play median T4, 100% (commander — never the problem).
- **Mikaeus** (sole undying-granter): median T9, **missing in 14%**.
- **Drain payoff** (only Zulaport + Syr Konrad): median T9, **missing in 25%**.

**Sephiroth, Fabled SOLDIER** (`{2}{B}`, mono-B, card_lookup 2026-06-19: *"Whenever another
creature dies, target opponent loses 1 life and you gain 1"*) puts the scarce **drain in the
command zone** — always available from T3, and on its 4th-death-per-turn transform it becomes a
**removal-proof emblem**. Yawgmoth drops into the 99 as the sac/-1/-1 engine.

## Targeted buys (7) — bought only where non-marginal

Per the diagnosis (redundancy, not mana), buys add undying + drain depth; **mana stays all-owned**
(0% mana-gated). All mono-B, color-verified:

| Buy | Role | Impact tier |
|---|---|---|
| **Geralf's Messenger** | undying **+** ETB drain 2 | **high** (combo piece *and* drain) |
| **Blood Artist** | drain (target) | **high** (grind + combo payoff) |
| **Bastion of Remembrance** | each-opp drain + a body | **high** (grind + combo payoff) |
| Vengeful Bloodwitch | drain (target), 2-drop | medium |
| Butcher Ghoul | cheap undying | marginal (combo only) |
| Putrid Goblin | persist undying | marginal (combo only) |
| Pawn of Ulamog | death→Scion fuel | marginal |

GC package (3/3): Necropotence · Bolas's Citadel · Demonic Tutor.

## Clock lab — the verdict that matters

`scripts/sephiroth_clock_lab.py`, 40k goldfish, combo-assembly (decap == table, infinite hit-all):

| line set | median kill | by T7 | never in 14 |
|---|--:|--:|--:|
| house-legal (3+ card lines) | **T12** | 5% | 33% |
| + pod-approved 2-card (Mikaeus+Ballista) | **T12–13** | 5% | 36% |

**The combo clock is ~T12 and STRUCTURAL.** It did not move for *any* lever tested:
- **Commander** (Yawgmoth-cmd ≈ Sephiroth-cmd, both ~T12) — each only frees ONE of the needed
  pieces; you still find the other 2.
- **The 7 buys** — they improve *consistency* (fewer whiffs) but not the median turn.
- **Tutors** — already 5; the diagnostic showed finding wasn't the single gate.
- **Unlocking the gated 2-card combo** — *no help*: Mikaeus + Ballista are two **unique
  singletons**, harder to assemble than the **redundant** 3-card lines.

Root cause: assembling ≥2–3 specific permanents in mono-B without fast mana is inherently
~T11–13 in goldfish — the same band as every other combo deck on the roster (Crystal T11,
Calamity T13). **You cannot make this a T6–7 combo racer by tuning.**

## What this deck actually is (and the unmeasured clock)

It is **not** a fast combo deck — it is a **resilient aristocrats GRIND deck whose combo is the
inevitability, not the race.** Its real clock is the **chip plan the combo lab does not model**:
Sephiroth (drain from T3) + Gray Merchant (devotion drain) + Geralf's (ETB 2) + Kokusho (5 on
death) + Syr Konrad + mass-sac value, into a wrath-proof board (Mikaeus). That out-grinds the
fair Ur-Dragon deck and out-resiliences the combo deck — the two halves of the pod — which is
exactly why Sephiroth (command-zone drain, removal-proof emblem) is the right commander for it.

**Bottom line:** a strict upgrade over Diminishing Returns (which was >T14 / 70%-never and
couldn't close), and a genuinely good *grind* answer to the pod — but it does **not** out-race
your existing T7 closers, and no amount of tuning makes the combo fast. Recommend the **3
high-impact buys** (Geralf's, Blood Artist, Bastion); the undying/fuel buys are marginal by the
"buy only if non-marginal" rule — use owned redundancy instead.

**Open next step:** build the **grind/chip clock** (incremental drain accumulation), since that —
not the ~T12 combo — is how this deck actually wins, and it's the only number still unmeasured.
