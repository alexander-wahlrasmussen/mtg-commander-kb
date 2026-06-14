# The Pod Gauntlet — win-probability vs the archenemy

**2026-06-14.** Backlog #1. `Pod_Matchup_Matrix.md` answers "does each deck beat
the recurring combo pod?" in **words** ("Favoured — disruption-led, not a race").
This puts a **number** on it by racing two already-measured quantities against
the opponent profile. Tool: `scripts/pod_gauntlet.py`. Clock data:
`analysis/pod_gauntlet_clocks.json` (harvested from the `*_clock_lab.py` suite).

> **This is a heuristic race model, not a rules engine — and it is built on
> goldfish ceilings.** Trust the *ranking* and the *shape of the two axes*, not
> the second decimal. Read "How to read this" before quoting any cell.

---

## The opponent (from `project_pod_combo_opponent` + the matrix)

Ur-Dragon ramp shell + Hidetsugu / Kairi / Kenrith / Kinnan combo decks. **Wins
T6–7**, typically **behind Grand Abolisher**. We model their first combo-attempt
turn `K` as a distribution (default `T5:10 / T6:35 / T7:35 / T8:15 / T9:5`) and
let them **retry every later turn** — a disrupted attempt just buys us a turn.

The one mechanical fact that shapes everything (`feedback_grand_abolisher_blocks_counters`):
on **their** turn, Grand Abolisher stops all our spells, so **counterspells are
dead on the combo turn**. Only proactive hate that is already in play — statics,
own-turn removal cast before they untap, edicts — survives. That is exactly what
`delay_lab.py` measures, and it is the disruption input here.

## The model

Two clocks race, per deck, Monte-Carlo (we are earlier in turn order, so our
turn *t* precedes their turn *t*):

- **CLOCK** — `decap` = the turn we can kill **one** opponent = the turn we can
  **neutralise the combo player we focus**. From each deck's `*_clock_lab.py`.
- **DISRUPTION `D`** — P(we stop one combo attempt | their Abolisher), from
  `delay_lab.py` where it exists, else class-bucketed (below).

```
sample K (their first combo turn) and T_kill (our decap turn, from the CDF)
  T_kill <= K            -> WIN   (threat removed before their first attempt)
  else each turn t=K,K+1,…: our turn t kills them if T_kill==t (WIN);
       otherwise their turn t combos and WINS-FOR-THEM with prob 1−D
       (disrupted with prob D -> continue). Undecided at the horizon = loss.
```

Two numbers, stated separately:

- **PURE RACE** = P(decap ≤ K), disruption ignored. **Fully simulated** for all
  16 decks (the clock curves are real lab output).
- **P(WIN)** = the race **with** the disruption overlay. `D` is **measured**
  (`delay_lab`, drawn) for the three decks delay_lab covers — Grand Design,
  Calamity Tax, Lightning War — and **class-bucketed** from the matrix
  "Through Abolisher?" column for the other 13 (`warn`/`none` → `(D@a=0,
  D@a=1)` = `(0.50, 0.14)` / `(0.20, 0.02)`, calibrated to bracket the measured
  trio). `a` = P(Abolisher out) is **swept**; baseline `a=0.30`.

## The gauntlet (decap clock, `a=0.30`)

`P(win)` is sorted; the right block is `P(win)` across the Abolisher sweep.
`*` = disruption measured, not bucketed.

```
deck                     sc  decap  pure  D@.3  P(WIN)   a=0.0  .15  .30  .50  .75
The Genome Project       15    T7    63%   39%    74%      77   76   74   72   69
Radiation Sickness       18    T7    56%   39%    68%      71   70   68   66   63
Ms. Bumbleflower         15    T8    33%   39%    49%      55   52   49   45   41
The Replication Crisis   17    T7    43%   15%    47%      49   48   47   46   45
The Exile's Return       18    T8    32%   39%    45%      51   48   45   41   38
Lorehold Spirits         18    T8    38%   15%    41%      43   42   41   40   39
Curse of the Scarab      17    T8    28%   39%    40%      44   42   39   36   33
Lightning War            19    T9    12%   64%*   37%      56   46   37   29   23
Zero-Sum Game             —    T9    33%   15%    35%      36   35   36   35   34
Earthbend the Meta       17    T8    31%   15%    34%      37   35   34   34   32
Eldrazi Stampede Chaos   14    T8    25%   15%    28%      29   29   28   27   26
Diminishing Returns      17    T9    13%   39%    26%      32   28   25   22   19
The Dark Lord's Army     19    T9    15%   39%    25%      31   28   25   23   19
The Grand Design         19   T10     8%   55%*   25%      36   30   24   19   14
Crystal Sickness         17   T11     7%   39%    14%      18   16   14   12   11
The Calamity Tax         18   T13     1%   43%*    4%       7    5    4    3    2
```

---

## What it found

**1. The matrix collapsed two axes into one verdict; the gauntlet separates
them.** A deck beats the pod either by **out-racing** (kill the combo player
before T6–7) or by **disrupting** (stop the combo turn through Abolisher). These
are different decks:

| | Race leaders (high PURE RACE) | Disruption leaders (high `D`, low race) |
|---|---|---|
| Decks | Genome 63%, Radiation 56%, Replication 43%, Zero-Sum 33% | Lightning War 64%\*, Grand Design 55%\*, Calamity 43%\* |
| Plan | kill the archenemy first | answer the combo turn, grind |
| Weakness | fragile / unblocked-ceiling (below) | **Abolisher-sensitive** (below) |

**2. The race leaders are not the matrix's favourites — and the gap is the
caveat.** The matrix rates Genome/Radiation "underdog/even — fast but fragile";
the gauntlet's PURE RACE rates them **highest**. Both are right: the race numbers
are **unblocked goldfish ceilings** with **no model of the deck's own
fragility** (Genome is combo-reliant; the pod's Ur-Dragon shell brings exactly
the blockers the goldfish assumes away). So their P(WIN) is a *ceiling* — read it
as "**can contest the race on paper**," then discount for fragility the model
doesn't see. This is the single most important reading caveat.

**3. The disruption leaders' verdicts hinge on one swept number.** Lightning War
goes **56% → 23%** and Grand Design **36% → 14%** across the Abolisher sweep
(`a=0 → 0.75`). Their whole anti-pod case is "how often is Abolisher actually
out?" The realistic band is `a≈0.15–0.30` (delay_lab), where both sit ~25–45% —
**even, not favoured**. The matrix's confident "Favoured" for Grand Design is
true *only* at low Abolisher density.

**4. Almost nothing actually *closes* by T6–7 — the matrix's core thesis,
quantified.** `--strict` races the **table** clock (win the game) instead of
decap (remove the threat). Everything collapses except **Genome 53%** and
**Zero-Sum 35%** (both hit-all kills that converge decap≈table). Every other deck
is a *remove-the-archenemy-and-grind* plan, not a *win-the-game-by-T7* plan. This
is why the matrix is right that this is "disruption-led, not a race" for most of
the roster — they can't close even when they decap.

**5. The model challenges Calamity Tax's "Favoured" verdict.** Under a uniform
combo-turn distribution Calamity is the **worst** deck here (4%): a T13 clock
can't out-race, and **43%/turn disruption is not a lock** — held over the 6 turns
from T7 to T13 it leaks (`0.43⁶ ≈ 0.7%`), so they combo through long before the
X-drain lands. Calamity's matrix-Favoured case rests on an assumption the race
model does **not** credit: that its tax **pushes the pod's clock from T6–7 out to
T10+**. Read its `--pod-slow` number against that claim — it climbs to ~6%, still
weak, because even a slowed pod out-combos a T13 kill behind leaky disruption.
**Action: Calamity's "grind/oppress = Favoured" verdict is the least supported on
the board** and deserves a real-game check — does it *beat* the pod, or just
*not-lose* for a long time? (See limitation 1.)

---

## How to read this

- **Rank, don't quote.** The ordering and the **pure-race-vs-`D` gap** (how much
  a deck leans on disruption) are the signal. The cells are ceilings.
- **PURE RACE is an optimistic front edge**, not a win rate: unblocked goldfish,
  no interaction against us, no model of our own combo fragility.
- **decap, not table, is the headline** — removing the archenemy is the goal in a
  4-player pod. `--strict` is the stricter "did we actually close" view.
- **The Abolisher sweep is the disruption decks' real verdict.** A single
  baseline number hides their sensitivity; quote the band.

## Limitations (load-bearing)

1. **No opponent-clock tax.** Every deck races the *same* `K` distribution. Decks
   whose plan is to **slow the pod** (Calamity, Diminishing, the stax shells) are
   systematically **underrated** — their real edge is making `K=10+`. Approximate
   it with `--pod-slow`; do not read their baseline cell as their ceiling.
2. **Disruption is bucketed for 13 of 16 decks** from the matrix's qualitative
   "Through Abolisher?" mark (measured only for GD / Calamity / LW). The bucket is
   the soft input; it is swept, but a per-deck `delay_lab` spec (hand-classified
   answer suite) would replace it with measurement.
3. **Availability ≠ effectiveness** (delay_lab's caveat): a live answer doesn't
   model their backup line or a second protection piece. One disruption of a
   *fragile* combo can also set them back multiple turns — not modelled either, so
   the leak rate in finding 5 is, if anything, pessimistic for true lock pieces.
4. **decap = "fastest single kill"** mapped to "kill the combo player"; assumes we
   always get to aim at the archenemy. Optimistic.

## Run it

```bash
python scripts/pod_gauntlet.py                 # decap gauntlet, a=0.30
python scripts/pod_gauntlet.py --strict        # table clock (did we actually close?)
python scripts/pod_gauntlet.py --a 0.15        # lower Abolisher density
python scripts/pod_gauntlet.py --pod-slow      # a pod the tax decks have slowed
python scripts/pod_gauntlet.py --refresh       # re-run the labs, reparse curves, rewrite the JSON
```

`--refresh` re-harvests every clock curve from the `*_clock_lab.py` suite and
writes `analysis/pod_gauntlet_clocks.json` (which also seeds backlog #2, the
clock-claim verifier). Calamity is the one deck kept from the matrix median (its
lab is multi-variant and never prints the base list); it is slow enough that the
curve shape doesn't change the verdict.
