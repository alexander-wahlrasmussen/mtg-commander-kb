# Radiation Sickness — Kill-Turn Clock Lab (2026-06-13)

> ## ⚠ ERRATUM — re-audit 2026-06-23 (read first)
>
> This writeup's central claim is **wrong**. It says the table clock (T10) is "driven by
> rad drain + converge kills … creature-count-INDEPENDENT by construction" and that
> "blockers barely affect the table clock," and the addendum below uses that to justify
> leaving the omitted go-wide producers un-modelled. Instrumenting `goldfish_kill` to
> attribute every table-close (8k trials) shows the opposite:
>
> | branch closing the table | share |
> |---|---|
> | **COMBAT** (`hit_focus`, go-wide board) | **76%** |
> | kill_all (Mindcrank combo + Simic) | 14% |
> | Triumph poison | 6% |
> | **rad drain** (`hit_all`) | **3%** |
>
> Decap is the same: ~85% combat. So the table clock is an **unblocked, creature-count-
> DEPENDENT, fully-blockable combat ceiling** — the project's "speed greed" pattern, and the
> softest goldfish assumption — *not* the robust converge clock claimed below. Consequences:
> - The addendum's "producers only move the tail, not the median" reasoning is **backwards**:
>   the median rides on creature count, so Iridescent Hornbeetle / Walking Ballista / Hardened
>   Scales / Winding Constrictor *would* move it. The lab if anything **under**-counts go-wide.
> - The deck's strong `self_meta_lab` (#2) and `pod_gauntlet` (race-leader) standing rests on
>   this unblocked combat number, against an Ur-Dragon shell that is precisely the blockers the
>   goldfish assumes away. Read those rankings as an optimistic ceiling, not a win rate.
> - Two real code bugs fixed 2026-06-23 (both immaterial to the curve — board overshoots 40 long
>   before they matter): (1) Vorinclex's +1/+1 doubling was applied **twice** in `m_cre` (in
>   `vorx` *and* `n_mult`); (2) the Bloodchief quest accrual doubled its own rate (`*2 if
>   quest>=1`) with no card backing it. Re-run: table 74%→74% by T10, median T10 unchanged.
> - **Deck change (now on master):** −Vorinclex, Monstrous Raider / +Timeless Witness
>   (`radiation-sickness-20260622.txt`). The lab `DECK` was retargeted to it and the now-dead
>   Vorinclex modeling dropped. Vorinclex's membership is ~immaterial to the curve.
>
> Everything below is preserved as the original 2026-06-13 record. The CDF grid still holds; only
> the *interpretation* (why the table closes, and how robust/blocker-proof it is) was wrong.

**Deck 2 of 10** in the Kill-Window Lab Sweep (`campaigns/Kill_Window_Lab_Sweep_2026-06-13.md`).
Lab: `scripts/rs_clock_lab.py` (40k trials, seed 20260613), on `speed_lab_core.py`.
This is the **coarsest lab in the sweep** — the counter spiral is tracked as
expected-value floats, not enumerated. Read the caveats before trusting any single
number; trust the shape.

## Claim vs. measured

| | Claim (hand-estimate) | Measured (lab) |
|---|---|---|
| Goldfish | **T6–9** (single range) | **table (win) median T10** · decap median T7 |
| Front edge | T6 | table T6 = 1% · decap T6 = 32% |
| "T5–6 combo" | T5–6 | combo/Simic table kill ≈ 1% by T6, 4% by T7 (god-hand) |
| Never-in-14 | — | decap 0% / table 1% |

```
  P(kill <= turn T) %                        5     6     7     8     9    10    12    14
  decap (one opponent, 40)                   5    32    76    91    95    98    99   100
  table (all three)                          0     1     4    21    49    74    96    99
```

## Direction: optimistic on the clock that matters (the table win)

This deck's reliable kills — Mindcrank+Bloodchief combo, Simic Ascendancy at 20
growth, Triumph poison — all kill the **whole table at once**, so the win clock IS
the table clock. Measured table median is **T10**; "T6–9" is optimistic by roughly
a turn at the median and badly so at the front edge (T6 = 1%, and even T9 is only
49%). The "T5–6 combo" line is a **god-hand** (1–4% that early): from a singleton
deck the combo needs Mothman + Mindcrank + Bloodchief + a proliferate source + rad
ticking ≥2 life/turn, all online together — a five-piece assembly, not a T6 norm
(the bake-off "singleton combo density" trap exactly).

So the front edge is optimistic again (the project's recurring pattern), now scored
on the table clock since that's how this deck wins.

## The decap/table split (my prior was half-right)

Pre-registered prior: *"converge kills; front edge suspect."* The converge **kills**
do converge — but the deck's *fastest* clock isn't the marquee combo. It's the
**incidental combat decap** (countered creatures swing) plus the rad drain, which
push one opponent to 40 by median **T7** (76% by T7) while the table lags to T10.
So decap and table diverge ~3 turns here, like a combat deck — the kill-shape lens
correctly called the combo converge but missed that an engine deck's *first* kill is
often the side-effect beatdown, not the named win. Worth carrying forward: classify
the **fastest** line, not the marquee one.

Practically the T7 decap is not just vanity: against the archenemy combo deck,
pressuring/removing one threat by T7 (the pod's own bar) has real value — but it is
**pressure, not a win**; the deck closes the game at T10.

## Card text

No errors in the Summary (2026-05-13 audit holds). `card_lookup.py` confirmed the
load-bearing details: Bloodchief quest triggers on **an opponent** (not any player)
losing 2+; Vorinclex doubles counters you place on **permanents and players** (rad,
+1/+1, growth, quest all ×2); Doubling Season doubles only your-permanent counters
(not rad on opponents); Tekuthal proliferates twice; Triumph grants infect (10
poison = dead regardless of life).

## Modeling caveats (the coarsest lab — read these)

- Counters tracked as **expected-value floats**, not enumerated: rad per opponent
  (symmetric), growth, quest, board power. Opponent decks assumed 62% nonland, so a
  rad mill of R loses ~0.62R life and decays rad to ~0.38R. Mindcrank's self-mill
  loop folded into a ×1.8 life-loss factor. Mothman counter placement =
  min(ncre, nonland milled) per turn.
- Creature-counter multiplier m_cre = vorx · 2^min(3, #{Doubling Season, Branching,
  Corpsejack}); additive doublers (Hardened Scales, Winding Constrictor, Kami)
  ignored (conservative). Proliferate events/turn = perms online (×2 Tekuthal),
  capped at 6.
- **The decap front edge (32% T6) is the least certain number** — it rests on board
  growth, the most heuristic part. The **table clock (T10) is the robust finding**:
  it is driven by rad drain + converge kills, which depend on rad accumulation
  (more reliable than combo assembly) more than on board math.
- Damage/poison unblocked; no interaction/disruption model. The rad drain hits all
  opponents (Table.hit_all) — genuinely converge — so blockers barely affect the
  table clock (they slow only the combat-decap side).

## Verdict for the Summary

Replace `Goldfish: T6–9 (unverified)` with:
**`Clock: T10 table-win (median; T6 ≈ 1%, T9 ≈ 49%) / T7 decap one opponent (lab 2026-06-13, rs_clock_lab.py — coarse engine model) · Through interaction: slower (unverified)`**

Pod-bar read: the deck **decaps** one threat by T≤7 in 76% of games (useful vs the
archenemy), but its **win** is T10 — it does not race the table. This is consistent
with the deck's stated "incremental threat, not explosive / secondary target" pod
posture and does not challenge the 18/20 score (the rubric rewards its reliability
and interaction, which the slow-but-near-certain table clock — 1% never-in-14 —
corroborates). No card swaps (verification pass only).

---

## Addendum — producer re-check (2026-06-13)

Triggered by the bug-impact review (`campaigns/Kill_Window_Lab_Sweep_2026-06-13.md` session
log). This lab predates the lw/cs/cos "omitted-producer" lesson, so its inventory was
re-audited against the `.txt`. Omitted pieces (all oracle-verified), with direction:

- **Walking Ballista** — counter-scaling any-target ping; an un-modelled **alt-kill
  line** (especially with the deck's counter doublers).
- **Iridescent Hornbeetle** — a 1/1 per +1/+1 counter placed each turn; a go-wide
  inflator for the Triumph/combat lines.
- **Deepglow Skate** (one-shot counter doubler ETB), **Basking Broodscale** (Eldrazi
  Spawn on counter), **Hardened Scales / Winding Constrictor** (additive +1/+1 boosts
  the model's multiplicative `n_mult` doesn't capture).

**Decision: lab left UN-PATCHED, with reasoning.** The deck's median table clock (T10)
is the **rad-drain `hit_all`**, which is creature-count-INDEPENDENT by construction —
so none of the omitted producers can move it. They feed only the *secondary*
ncre-gated lines (Simic 20-growth, Triumph `board+ncre≥10`, combat decap) and the
Ballista alt-kill, all of which are god-hand/tail effects. The esc re-check the same
day confirmed empirically that singleton producers move the tail, not the median —
and here the median doesn't even use them. Re-modelling the sweep's coarsest EV lab to
chase a tail effect would add more imprecision than it removes. The decap-T7 / table-T10
clock and the 18/20 posture stand; **Walking Ballista is flagged as an un-modelled
alt-kill (residual upside, same slow-bias direction).**
