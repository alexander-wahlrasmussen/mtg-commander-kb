# Lightning War — Cross-Table Chip Model (2026-06-14)

Follow-up to `analysis/Lightning_War_Clock_Lab_2026-06-13.md`. That clock lab modelled
**our** chip (Guttersnipe 2 + Vivi 1 per noncreature cast, the creature board, Fated
Firepower amplification) but **held all three opponents at a static 40** and flagged the
gap explicitly: *"A real pod arrives at the finish already chipped from attacking each
other… Cross-table chip is real and unmodelled."* This closes that gap — and, in doing so,
corrects an over-optimistic pinger reading from this doc's own first pass (see Result 3).

Lab: `scripts/lw_clock_lab.py` — new `--mode chipsweep`, `--mode optimize`, `--mode avail`
(40k trials, seed 20260613, on `speed_lab_core.py`).

## What was added to the model

- **`chip_rate`** — life each opponent loses per *our* turn from the rest of the pod
  beating on each other, from `chip_start=3`. Implied avg opponent life at T6 = `40 − 4·rate`.
- **Capped non-lethal.** Cross-table chip drops an opponent no lower than 1 life, so the
  *table's own* beatdown never registers OUR decap/table clock. Conservative on purpose:
  chip never lands a kill even stacked with our pings, and aggression aimed at **us** is
  not subtracted from the opponents — so the **moderate band is the honest centre.**
- **Electrostatic Field** is now baked in as the deck's 3rd real pinger (the applied swap,
  below). `extra_pingers` = an **always-on pinger ceiling** (chips from T1, no draw/cast
  cost — optimistic). An injected **"Extra Pinger"** card (`_inject`, `--mode optimize`)
  is the **realistic** drawn-and-cast marginal pinger. The gap is the draw/cast tax.

## Result 1 — the table clock is the big mover (chip discounts the X-spell)

```
  P(kill <= turn T) %                          5     6     7     8     9    10    12    14   median  never
  no table chip  (@40 T6)   decap              0     1    10    32    58    77    94    99    T9      1%
                            table              0     0     0     2     5    11    34    61    T14    39%
  light 2/turn   (@32 T6)   decap              0     5    27    63    83    93    98   100    T8      0%
                            table              0     0     1     6    19    36    72    94    T11     6%
  moderate 3/turn(@28 T6)   decap              0     9    42    77    91    96    99   100    T8      0%
                            table              0     0     3    12    33    56    91    99    T10     1%
  heavy 5/turn   (@20 T6)   decap              2    24    76    91    96    98    99   100    T7      0%
                            table              0     2    12    43    73    95    99   100    T9      0%
```

The **decap** clock moves modestly (T9 → T8 → T7); the **table** (one-cast wipe) clock moves
*dramatically*: median T14 → **T10** at moderate chip, never-in-14 **39% → 1%**. The from-40
table sweep is 14-mana Crackle (`{X}{X}{X}{R}{R}`, X=4); cross-table chip is a *direct
discount on X* (from @28 the same fork is X≈3 = 11 mana; from @20, X≈2). **The deck's
"expensive" win is only expensive against a pod still at 40 on the back half — which nobody
plays.** This is the robust, model-independent headline.

## Result 2 — "T6–7" re-read honestly

So "T6–7" is right as the **decap front edge** of a chipped pod (41% by T7 / 76% by T8 at
moderate chip; decap median T7 at heavy chip), *not* as a from-40 table-sweep median. State
both clocks: **moderate-chip real-pod ≈ decap T7–8 / table T10**; strict from-40 goldfish
stays decap T9 / table T13. (decap and table are different clocks — don't conflate them.)

## Result 3 — the incremental-pinger lever is SATURATED (correcting this doc's first pass)

This doc originally claimed "+2 pingers lifts the by-T9 table wipe 33% → 76%" and recommended
adding a pinger. **That was wrong** — it used `extra_pingers`, which models a pinger that is
*always in play from turn 1 with no draw/cast cost*. A real singleton you must draw and then
cast is worth far less. Measured at moderate chip (`--mode optimize`, 40k):

```
  table wipe, P(<= T) %                 7     8     9    10    median
  current deck (3 pingers)              3    12    33    56    T10
  +1 REAL pinger (draw+cast)            3    14    36    59    T10     <- +3pp, median UNCHANGED
  +1 ALWAYS-ON pinger (ceiling)         6    25    54    80    T9      <- the +21pp mirage
```

The draw/cast tax is ~7×: a real added pinger buys **+3pp** on the table-by-T9, not the
+21pp the always-on abstraction implied. The deck **already runs three pingers** (Guttersnipe
2, Vivi 1, Electrostatic Field 1); together with cross-table chip they have **captured the
incremental-clock lever**. Adding a 4th pinger is not an optimization. (Lesson, logged:
never read an always-on flat bonus as the value of a real singleton — pay the draw+cast tax.)

## Result 4 — where the headroom actually is: finisher availability / conversion

`--mode avail` holds moderate chip and bounds each axis with an infinite-redundancy ceiling:

```
  table wipe, P(<= T) %                 7     8     9    10    median
  baseline (current deck)               3    12    33    56    T10
  +1 REAL pinger (draw+cast)            3    14    36    59    T10
  CEIL pinger always-on                 6    25    54    80    T9
  CEIL enabler always-on                7    21    44    65    T10
  CEIL finisher always-found           14    41    73    90    T9
  CEIL finisher+enabler both           30    57    82    92    T8
```

Two reads:
- **The enabler axis is slack.** Infinite enabler redundancy lifts table-by-T9 only 33→44%,
  because Comet Storm (instant) and Electrodominance (instant) already give enabler-free
  finishers — the enabler only unlocks Crackle's efficiency, which chip already de-prioritised.
  **The deck runs four enablers; that is redundancy to spare.**
- **Finisher availability is the binding axis** (33→73% as a ceiling — the most headroom).
  This is where the **copy package** earns its slot: Galvanic Iteration / Increasing Vengeance
  / Reiterate (and **Twinning Staff**, which adds +1 to *every* copy) **convert one finisher
  into a table-wide kill** and copy single-target Banefire/Electrodominance into a 2nd target.
  Twinning Staff also amplifies copied **cantrips (draw)**, **rituals (mana)**, and **Storm-Kiln
  Treasures** (Storm-Kiln triggers on cast *or copy*) — it is engine/finisher-conversion
  support on the deck's actual headroom axis, **not win-more.** But 73% is a *ceiling* (infinite
  redundancy); Result 5 measures what a single *real* card on this axis actually buys.

## Result 5 — even on the headroom axis, no single real card is a needle-mover

`--mode finlever` injects one drawable card per axis (must be drawn+cast) at moderate chip:

```
  table wipe, P(<= T) %             7     8     9    10    median   vs base (by T9)
  baseline (current deck)           3    12    33    56    T10       —
  +1 REAL converter/amp             3    14    35    56    T10      +2pp
  +1 REAL pinger (the bar)          3    14    36    59    T10      +3pp
  +1 REAL table finisher            3    15    38    61    T10      +5pp
  +1 REAL tutor                     4    16    40    62    T10      +7pp   <- best real add
  CEIL finisher always-found       14    41    73    90    T9      +40pp   <- uncapturable ceiling
```

- **Ranking: tutor > finisher > pinger > amp**, and it makes sense — a tutor is the most
  *flexible* redundancy (finds whichever finisher/enabler-path is missing), so it raises "have
  a table finisher castable in combat" the most per card. A dedicated finisher only helps when
  you'd have had none; a 5th copy-amp is weakest (the deck has 4, and an amp only matters when
  a finisher is *also* in the combat — conditional on conditional).
- **But every real single-card add is small (≤ +7pp, zero median movement), and the best
  captures only ~18% of the 73% ceiling.** The ceiling is the prize if the constraint *vanished*
  — not what one singleton in a 99 can buy; to approach it you'd have to *flood* the axis
  (several tutors/finishers), which costs the disruption / colour / curve the deck needs.

**So the optimization answer is: there is no exploitable single-card clock upgrade on any axis.**
The lab has now tested pingers, finishers, tutors, amps, and enablers at realistic draw+cast, and
none beats +7pp or moves the median — the deck is near its single-card consistency ceiling for a
99-singleton. Real further gains are **off-model**: disruption quality, Abolisher answers, and
politics — the axes the pod-loss history ([[pod_combo_opponent]]) says decide games and the
goldfish cannot score. If you ever *do* add finisher-axis redundancy, a **tutor is the best
single card**, not a pinger.

## The applied swap: −Vedalken Orrery / +Electrostatic Field (≈ clock-neutral)

Applied 2026-06-14 (`decks/lightning-war-20260614.txt`; old list archived). Rationale, honestly:
- **Cut Vedalken Orrery, not Twinning Staff.** The avail lab shows the *enabler* axis is the
  slack one, and Orrery is its most redundant member — a vanilla 4-mana "cast as though flash"
  with no body, no card, and no free-start, vs Leyline of Anticipation (free in opening hand),
  High Fae Trickster (a 4/2 flash flyer that advances the clock), and Borne Upon a Wind (cantrips).
  The user's challenge to keep Twinning Staff is correct and lab-supported (Result 4).
- **The add is marginal, by this lab's own corrected measure.** 2→3 pingers moved moderate-chip
  table-by-T9 by ~0pp and @40 never-wipe 40%→39%. Electrostatic Field's case is the **free cut**
  (redundant enabler) plus a **0/4 wall** — a sturdier body that blocks, survives wipes, and
  survives the very cross-table chip we modelled — **not** a measured speed gain.
- **GC-neutral**: both non-GCs; the 3/3 cap (Fierce Guardianship / Opposition Agent / Jeska's
  Will) is untouched. **Buy**: Electrostatic Field is unowned (~€0.25–1, bulk), not deployed
  elsewhere. **Keep-or-revert is a fair call** — it is a small resilience tweak, reversible in
  one step.

## Card text (re-verified `card_lookup.py` 2026-06-14)

Twinning Staff `{3}` "copy that many times **plus an additional time**"; its {7},{T} is a
spare copy outlet. Galvanic/Increasing Vengeance/Reiterate are the primary I/S copy effects.
**Electrodominance is a printed Instant** (no flash needed — corrects an earlier misread);
Comet Storm instant multikick; Crackle/Banefire are the enabler-gated sorceries. Firebrand
Archer 2/1 / Thermo-Alchemist 0/3 / Electrostatic Field 0/4 all = +1 to each opp per cast.
Storm-Kiln Artist makes a Treasure on cast **or copy**. No card-text errors.

## Verdict for the Summary

Clock line → **`Clock: T9 decap / T13 table strict-from-40 goldfish (lw_clock_lab.py, lab
2026-06-13). With realistic cross-table chip (moderate 3/turn, @28 by T6): decap T7–8 / table
T10, table never-wipe 40%→1% (chipsweep, 2026-06-14) — the from-40 sweep is the ceiling, the
chipped finish is the median. The deck's incremental-pinger lever is saturated (3 pingers);
its headroom axis is finisher availability, served by the copy package.`**

19/20 stands (verification pass; the swap is GC-neutral and clock-neutral).
