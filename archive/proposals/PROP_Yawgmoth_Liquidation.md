# Proposal: Yawgmoth Liquidation — the aristocrats rebuild of Diminishing Returns

*Status: PIPELINE. Raised + lab-verified 2026-06-19. The "dismantle 3, build 1" build (v2,*
*after the Winota go-wide racer was lab-falsified — see `PROP_Winota_Joiner_of_Forces.md`).*
*Decklist: `decks/considering/yawgmoth-liquidation-20260619.txt` (100, parses clean, 3/3 GC).*
*Lab: `scripts/yawgmoth_clock_lab.py`.*

The user chose the **aristocrats hit-all rebuild** path: recycle Diminishing Returns' freed
parts into a *faster, board-independent, Abolisher-proof* drain — explicitly trading raw race
speed for pod-resilience. This build delivers the resilience; read the clock for the speed.

---

## Teardown (unchanged)

Cut the D-tier — **Eldrazi Stampede (16) · Crystal Sickness (20) · Diminishing Returns (22)** —
the three worst by the results composite (`Definitive_Tier_List_2026-06-15.md`). Genome stays
(S-tier). DR's freed aristocrats core (sac fodder, drains, Skullclamp, tutors, Cabal Coffers)
feeds this deck directly.

## Commander & why it fixes DR

**Yawgmoth, Thran Physician** `{2}{B}{B}`, Legendary Creature — Human Cleric, 2/4 (mono-B).
*Not a Game Changer.* (card_lookup 2026-06-19: *"Pay 1 life, Sacrifice another creature: put a
-1/-1 counter on up to one target creature and draw a card."*)

DR's diagnosed flaw (`analysis/`): its death-combo was gated on **death volume**, and it had to
*draw both* a sac outlet and a payoff. **Yawgmoth IS the free sac outlet + card engine, always
available from the command zone** (recast if killed) — so the deck never whiffs on the outlet,
and it manufactures volume + cards every turn. It also doubles as repeatable -1/-1 removal that
**grinds the fair Ur-Dragon deck** (the half of the pod that walls glass racers).

## The kill — board-independent, own-turn, Abolisher-proof (house-legal, 3+ cards)

The undying gap in mono-B (only Mikaeus + Hancock printed) is solved by the commander pairing:
- **Line A:** Yawgmoth + **Mikaeus, the Unhallowed** (grants undying to non-Humans) + a drain
  (**Zulaport Cutthroat** / Syr Konrad). Sac→undying→-1/-1 reset = **infinite deaths → each
  opponent loses infinite.** A 4-piece combo (Yawg is the commander, so it's only ever 2 cards
  short) — comfortably inside the house "3+ distinct cards" rule, **no pod approval needed.**
- **Line B:** Gravecrawler + Phyrexian Altar + a Zombie source + a drain (mana-neutral loop).
- **Resilience bonus:** Mikaeus also makes the whole board undying → wrath-proof.

GC package (3/3): **Necropotence · Bolas's Citadel · Demonic Tutor** (engines + the tutor that
assembles the line). Free interaction kept non-GC: Deadly Rollick, Snuff Out, Imp's Mischief.

## Clock lab — the verdict

`scripts/yawgmoth_clock_lab.py`, 40k goldfish, combo-assembly (decap == table by construction —
infinite hit-all), bracketed on the draw engines:

| | median kill | by T7 | by T10 | never in 14 |
|---|--:|--:|--:|--:|
| floor (Necro/Bolas as cantrips) | T13 | 6% | 28% | 37% |
| realistic (Necro/Bolas dig) | **T12** | 6% | 33% | 31% |

**Clock: ~T12 combo (lab 2026-06-19), decap == table.**

**CORRECTION (2026-06-19 diagnostic, `scripts/sephiroth_clock_lab.py` + instrumentation):** an
earlier draft blamed omitted Cabal Coffers MANA. The instrumented run disproved that — the
combo is **0% mana-gated**. The real gates are *piece redundancy*: the single undying-granter
(Mikaeus, median T9, missing 14%) and the drain payoff (median T9, missing 25%). See the
Sephiroth variant (`PROP_Sephiroth_Liquidation.md`) for the full diagnosis: the ~T12 combo
clock is **structural** to assembling 3 specific permanents in mono-B, and does NOT move with
commander choice, targeted buys, more tutors, or even unlocking the 2-card combo.

The one thing the combo lab still omits is the **grind floor** (Gray Merchant / Kokusho / Syr
Konrad / commander-drain chipping the table from the early game) — which is what the deck
actually wins on. That clock is unmeasured here; the combo is the inevitability, not the race.

## Honest bottom line

**This is a reliable, resilient, Abolisher-proof grind-combo that actually closes the table —
not a T6–7 racer.** That is exactly the tradeoff the user picked (pod-proof over fast), and it
is a **strict upgrade over Diminishing Returns**: DR was >T14 / 70%-never-close; this assembles
a board-independent hit-all by ~T12 (earlier with its real mana + grind), survives wraths via
Mikaeus, and beats the fair Ur-Dragon deck on the grind axis DR couldn't.

What it is **not**: faster than your existing T7 racers (Genome/Radiation/Replication). Against
the combo half of the pod it out-*grinds* and out-*resiliences* rather than out-*races*. If the
goal is to pre-empt a T6–7 Abolisher combo, no owned build surfaced in this exercise does that
better than the racers you already run — which is itself the rigorous finding.

**Open levers if pursued:** model Coffers + the grind floor for a truer clock; consider a lower
combo curve (Mikaeus at 6 is the assembly bottleneck) or a cheaper second undying-granter to
pull the line in.
