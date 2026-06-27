# Raffine "Grave Conspiracy" — Connive-Reanimator Clock Lab (2026-06-24)

**Candidate:** `decks/considering/grave-conspiracy-20260624.txt` — Raffine, Scheming Seer,
Esper connive-reanimator aristocrats. 3-GC-legal (Demonic Tutor + Vampiric Tutor +
Cyclonic Rift). Every card text card_lookup-verified 2026-06-24.

**Lab:** `scripts/raf_clock_lab.py` (modes: `clock`, `hate`, `fix`). Same harness
(`speed_lab_core.py`) and seed family (20260612) as hsh/yrk/kfk, so the clock is
directly comparable. Goldfish ceiling — unblocked, no opponent interaction.

## The intended kill (Line A)

Board-independent aristocrats infinite: **Reveillark + Karmic Guide + a free sac
outlet (Viscera Seer / Carrion Feeder) + a drain payoff (Blood Artist / Zulaport /
Bastion of Remembrance)** → infinite deaths → table drains out. Connive (Raffine +
Ledger Shredder) and dedicated binners (Buried Alive, Entomb) bury the loop creatures;
cheap reanimation (Reanimate/Animate Dead/Victimize) cheats them back. Razaketh
(sac → tutor) is the support engine.

> **Legality correction (2026-06-24):** the first draft ran **Griselbrand** as the
> draw engine — it is **BANNED in Commander** (my miss: I verified its text but not
> its legality). Replaced with **Kokusho, the Evening Star** (legal, owned, a
> death-drain grind closer). A full-decklist legality scan now confirms the other 99
> are all legal. Removing Griselbrand moved the clock 17%→16% by T12 — i.e. it was
> never the deck's saving grace, and its loss *removes the deck's only draw engine*,
> sharpening the verdict below.

## Result — `clock` (8000 trials, seed 20260612)

```
P(kill <= turn T) %        2   3   4   5   6   7   8   9  10  12
kill (decap = table)       0   0   0   1   3   4   6   8  11  16
median kill: never in 12   ·   never-in-12: 84%
```

**The infinite assembles only ~16% of the time by T12; median game never assembles it.**
Benchmark: Hashaton (Esper Thoracle) is T6 decap=table. This is not in the same league.

### Why (instrumented)

- The only infinite funnels through **two specific singletons** (Reveillark + Karmic
  Guide) with **no backup pair**. Seeing one specific card by T12 is ~18%; seeing both,
  even with tutors that are themselves singletons, is rare. Component availability by
  T12: payoff 81% / sac outlet 56% / Reveillark 48% / **Karmic Guide 31%** (the choke).
- **No draw-to-win payoff.** With Griselbrand (banned) gone, the deck has no engine
  that converts a big draw into a win. Razaketh tutors, but to *hand* — and the kill
  wants the loop creatures in the *yard*. The hand→yard bridge (connive / Frantic
  Search) moves ~1 card/turn, so assembly is mana-and-sequencing-gated across multiple
  turns. This is exactly the gap Thassa's Oracle closes for the Hashaton build (draw
  deck → instant win); this deck deliberately omits it.

## Result — `hate` (graveyard hate, 6000 trials)

```
P(kill <= T) %         5   6   7   8  10  12   never
clean                  1   3   4   6  11  16    84%
RIP/Leyline @T3        0   0   0   1   1   2    98%
RIP/Leyline @T5        0   0   0   0   1   1    99%
```

A single resolved Rest in Peace / Leyline of the Void **craters the clock to ~2%**
(must hardcast Line A — ~13 mana). The pod (Acererak mono-B, Hidetsugu & Kairi UB) is
the exact color pair that runs graveyard hate. **Decisive Pod-Fit failure.**

## Result — `fix` (does redundancy help? 8000 trials)

Adds a 2nd, compact infinite — **Mikaeus, the Unhallowed + Walking Ballista** (Mikaeus
gives the Construct undying → remove last counter to ping → dies → returns with a +1/+1
counter → infinite ping; Mikaeus already in the 99, Ballista owned) — plus two
bin-tutors (Final Parting owned, Corpse Connoisseur ~$1), cutting three weak cards.

```
P(kill <= T) %                 5   6   7   8  10  12   never
as-drafted (Line A only)       1   3   4   6  11  16    84%
+ 2nd infinite + bin-tutors    1   3   5   7  11  16    84%
```

**Flat.** Adding combo *count* does not move the clock — confirming the bottleneck is
not "too few combos" but the structural lack of a fast draw-to-win payoff plus the
mana/sequencing cost of deploying any multi-piece board kill, all under gy-hate risk.

## Verdict

The as-drafted "Grave Conspiracy" is an honest **Bracket-3 grind/value reanimator**, not
an upper-tier racer. Its combo is a low-frequency side line (cf. the repo already tags
the identical Reveillark+Karmic loop as a *side line* for Lorehold Spirits, not a primary
clock). Against a T6–7 combo pod it loses the race and folds to routine graveyard hate.

**Paths to actually make Raffine pod-tier (each needs its own re-lab):**
1. **Add the draw-to-win payoff** (Thassa's Oracle + Consultation). Converts Griselbrand
   from "draw a big hand" to "win on the spot" and makes the reanimator genuinely fast —
   but it is the same wincon the user rejected as "boring" (and overlaps Hashaton).
2. **Accept it as a B3 grind deck** — fun, mostly-owned, but not a pod racer; pick it for
   flavor, not to beat the combo pod.
3. **Different commander.** If the goal is "upper tier in this pod," a dedicated combo
   commander beats bending Raffine, whose connive identity pulls toward fair value.

Clock claims for any Summary must cite this lab. As-drafted descriptor:
`Clock: combo assembles ~16% by T12 / median never (lab 2026-06-24); folds to gy hate (spell)`.
