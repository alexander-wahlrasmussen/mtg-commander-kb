# Urza "Planned Obsolescence" — Mono-U Artifact Combo Clock Lab (2026-06-25)

**Candidate:** `decks/considering/planned-obsolescence-20260625.txt` — Urza, Lord High
Artificer, mono-U artifact combo-control. The pod-racer chosen after the Raffine
reanimator was lab-falsified (see `Raffine_Grave_Conspiracy_Clock_2026-06-24.md`).

**Lab:** `scripts/urza_clock_lab.py` (modes `clock`, `lines`). Same harness
(`speed_lab_core.py`) and seed (20260612) as hsh/raf, so the clock is directly comparable.

**Verification done before labbing** (the four gates — text / legality / color-identity /
GC, per [[check-card-legality]] + the GC scan): all 99 card_lookup-verified; full-list
legality scan clean; color-identity scan caught **Thopter Foundry (BUW)** and **Tezzeret,
Agent of Bolas (BU)** as off-color for mono-U → cut (Thopter-Sword combo dropped, → Voltaic
Key). GC scan caught 5 → cut Gifts Ungiven + Thassa's Oracle → **exactly 3 GCs** (Mana Vault
+ The One Ring + Cyclonic Rift). 100 cards, library 99.

## The kill

Assemble any of **three redundant, GC-free 2-card infinite-mana combos**, then Urza's
`{5}` ability (no tap symbol → repeatable with infinite mana) digs to a payoff and casts it:

- **A — Isochron Scepter (imprint Dramatic Reversal) + nonland mana** → untap-all loop.
- **B — Grand Architect + Pili-Pala** → infinite colored mana.
- **C — Power Artifact on Basalt Monolith** → {C}{C}{C}, untap {3}→{1} = +2/cycle.
- **Payoff:** Walking Ballista (X = ∞ → ping the table) or Blue Sun's Zenith (deck the
  table out). Both fed by infinite mana; Urza digs one if not in hand.

Consistency engine (what Raffine lacked): Urza's `{5}` dig + 9 tutors (artifact tutors
Whir/Fabricate/Reshape/Tribute/Trinket/Trophy/Tezzeret; blue Merchant Scroll/Spellseeker/
Muddle). Plus a deep mono-U counter suite to protect the turn and Winter Orb / Back to
Basics / Static Orb soft-locks (Urza floats on artifact mana through them).

## Result — `clock` (8000 trials, seed 20260612)

Bracketed by the Urza-`{5}`-dig proxy (`DIG_DRAW` = cards seen per activation):

```
                 T4   T5   T6   T7   T8   T10  T12   median  never
DIG_DRAW=1 (cons) 16   28   45   59   72   90   97    T7     3%
DIG_DRAW=2 (gen)  11   32   54   71   85   97  100    T6     0%
```

**≈ T6–7 decap = table, ~60–71% by T7, ≤3% never.** Pod-competitive (decap T≤7) and
reliable — squarely in the Hashaton (Esper Thoracle, T6 / 71% by T7) neighborhood, and a
different axis from it (artifact infinite-mana → damage/mill, not a {U}{U}+{B} deckout).
Contrast Raffine: ~16% by T12, median never.

## Result — `lines` (which combo carries the kill)

```
Isochron + Reversal   77% of kills
Architect + Pili      18%
Power Artifact+Basalt   5%
```

Combo A is the workhorse (both halves tutorable); B and C are real but draw-dependent
(Grand Architect / Power Artifact have no artifact tutor). Honest read: the "three combos"
are one highly-tutorable primary + two drawn backups — still far more redundant than
Raffine's single 4-piece line, and the backups raise the floor.

## Caveats (the ceiling)

- **No opponent interaction modeled** — this is the goldfish ceiling. The "through
  interaction" clock is slower, but mono-U is the *best* color at fighting the pod's UB
  counter wall, and its protection/stax is upside the goldfish can't score (unlike a glass
  cannon, where the goldfish flatters).
- **Build cost:** mostly a buy (Isochron Scepter / Grand Architect / Pili-Pala / Power
  Artifact / blue duals unowned; you own Urza + Basalt Monolith ×2 + The One Ring ×3 +
  Mana Vault ×2 + Cyclonic Rift ×3 + Thran Dynamo ×6). Combo pieces are cheap commons/
  uncommons; the spend is the rocks + manabase. Run `availability_check.py` for full sourcing.
- **Pod approval:** the deck wins via an infinite combo — pod-accepted as of 2026-06-19
  ([[infinites-ok-in-pod]]). No MLD, no repeatable extra-turns (Time Sieve deliberately
  excluded).

**Verdict: a genuine upper-tier pod racer.** Descriptor:
`Clock: T6–7 decap = table (spell, ~60–71% by T7, lab 2026-06-25); mono-U counters + stax as protection`.
Next: `availability_check.py` sourcing, then a Summary if the user commits to building it.
