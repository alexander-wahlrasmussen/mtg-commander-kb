# London Mulligan Experiment — pricing the mulligan (2026-07-03)

Follow-through on `analysis/Mulligan_Strategy_Audit_2026-07-03.md` §8.1. The audit
established that every mulligan conclusion to date was bounded by the sim's free
mulligan (fresh 7, max 2, keeps a failing 3rd hand): digging had no cost, and
aggression (mull-to-5) was unrepresentable. This experiment adds both and asks the
user's question directly: **is there kill-clock speed hiding in mulligan strategy that
the free-mull model couldn't see?**

**Answer: no — the opposite.** Once mulligans cost cards, aggressive plan-mulliganing
never beats the plain land-count keep by more than noise, and on half the decks it is
actively slower. The remaining real upside in the mulligan system is **keep-spec
fidelity** (Grand Design's +5–6pp came from fixing its ramp bucket, not from mulling
harder) and **catching mis-tuned specs** (Forced Liquidation's plan keep measurably
fights its own clock — the Radiation-June-16 pattern, caught again).

## Design

`deck_sim.opening_hand` gained an opt-in London variant (`DECK_SIM_LONDON_MULLS=N`,
commit 3012b9c): up to N mulligans, each a fresh 7; the final keep bottoms one card per
mulligan taken. Bottoming policy: excess lands (4th+) first, then the most expensive
non-plan nonland, then plan cards; first 3 lands protected. Bottomed cards are never
drawn (exact for ≤14-turn goldfish horizons). Default path byte-identical (tier-1
tests; golden untouched).

Three arms per deck on its own clock lab (40k trials, the lab's fixed seed, so arms are
paired): **baseline** = land keep, free ×2 (the committed behaviour) · **plan** = plan
keep, free ×2 (fidelity-fixed buckets, commit d10f950) · **london3** = plan keep +
London, up to 3 mulls with real bottoming. Decks = the six with sharp keeps (the
mulligan_audit operating-room table: 14–40% keep-disagreement room); the other 11 have
degenerate keeps where no mulligan arm can express anything.

## Results — decap cumulative %, median, never-in-horizon

| deck (lab metric) | arm | T6 | T7 | T8 | T9 | med | never |
|---|---|--:|--:|--:|--:|---|--:|
| Zero-Sum (combo kill) | baseline | 25 | 37 | 48 | 56 | T9 | |
| | plan | **29** | **43** | **54** | **63** | **T8** | |
| | london3 | 22 | 34 | 45 | 54 | T9 | |
| Forced Liq. (burn axis) | baseline | 8 | 21 | 42 | 60 | T9 | 8% |
| | plan | 7 | 19 | 37 | 56 | T9 | 11% |
| | london3 | 5 | 14 | 31 | 49 | **T10** | 14% |
| Eldrazi Stampede | baseline | 10 | 28 | 52 | 73 | T8 | 1% |
| | plan | 11 | 30 | **56** | **77** | T8 | 0% |
| | london3 | 11 | 29 | 53 | 74 | T8 | 1% |
| Earthbend the Meta | baseline | 11 | 34 | 65 | 82 | T8 | 1% |
| | plan | 12 | **36** | 65 | 81 | T8 | 2% |
| | london3 | 10 | 30 | 59 | 78 | T8 | 2% |
| Grand Design | baseline | 3 | 12 | 33 | 59 | T9 | 5% |
| | plan | 3 | **14** | **38** | **65** | T9 | **3%** |
| | london3 | 3 | 13 | 34 | 60 | T9 | 4% |
| Croak (FULL assembly) | baseline | 9 | 24 | 41 | 55 | T9 | 10% |
| | plan | 10 | 25 | 41 | 55 | T9 | 9% |
| | london3 | 9 | 23 | 39 | 53 | T9 | 10% |

## Findings

1. **Pricing the mulligan kills the aggressive strategy.** london3 ≤ plan on every deck
   (mechanically necessary — same keep, added cost), and london3 ≤ baseline everywhere
   except GD/ESC at +1pp noise. On Zero-Sum (−3pp @T7), Earthbend (−4pp @T7), Forced
   Liquidation (−7pp @T8) and Croak (−1) it is *slower than not having a plan keep at
   all*. For redundancy-built 99-card decks, a card in hand beats a card of selection:
   the deck's own dig/tutor density converts raw cards into the plan faster than the
   mulligan can. Croak shows the cost on a second axis too: protection available by T4
   drops 66%→60% under london3 — bottomed interaction is real resilience lost.
2. **The free-mull plan-keep numbers were upper bounds, as documented — and even those
   cap at +6pp.** Zero-Sum is the best case for the *free* plan keep (+6pp @T7, median
   T9→T8): a true tutor-combo deck where "hold a tutor" genuinely is the plan. Grand
   Design's +5–6pp exists **only after the ramp-bucket fix** — the same keep measured
   +1pp with the broken bucket. Fidelity, not aggression, is where the lever lives.
3. **Forced Liquidation's spec is mis-tuned — the plan keep fights its own clock**
   (−2…−5pp even at free mulligans, never-in-12 8%→11%). Its FINDING keep digs for any
   single wheel/punisher/2-selection while shipping the curve-and-board hands its burn
   axis actually rides — the same single-axis over-dig that cost Radiation −9pp on
   2026-06-16. The audit predicted this class of failure (§6: lone-Windfall keeps, the
   inexpressible ≥2-punisher rule). Action: FL's judgment row needs re-tuning (union
   with BOARD, or the counted-bucket primitive) before its plan keep is used for
   anything.

## What this settles

The user's challenge — "we haven't nailed the mulligan strategy, so we can't conclude
it has no effect" — is now answered with the strategy space actually explored:

- **Smoothness:** the mulligan is not a smoothness lever (sweep, twice-verified).
- **Kill speed:** with real London costs, no tested mulligan strategy beats the plain
  land-count keep materially on any of the six sharp-keep decks. The free-mull model
  *overstates* mulligan upside, and even that ceiling was +6pp/one median step on one
  deck.
- **Where the system still pays:** keep-spec *fidelity*. Fixing one generated bucket
  moved GD +5pp; a mis-tuned spec costs FL −5pp. The keep specs' value is diagnostic
  and as deckbuilding lenses (`feedback_mulligan_is_deckbuilding_input`) — not as a
  speed dial.

## Limitations (honest bounds)

- Bottoming policy is heuristic (protect plan + first 3 lands). A cleverer policy
  narrows but cannot close the gap: london-N with any policy is dominated by free-N at
  equal keeps, and free-2 already measured ≈ flat vs baseline on most decks.
- Goldfish only: mulligan value **against interaction** (keeping protection for the
  combo turn, pace vs a known pod clock) is unmeasured — that lives in
  pod_gauntlet/delay_lab territory, per `feedback_goldfish_lab_blind_spots`.
- Binary keeps: no "good 7 vs redraw EV" ranking. Given london3's across-the-board
  losses, a ranking layer would have to overcome a negative baseline to matter.

*Files: deck_sim London variant (3012b9c) + tier-1 tests; raw arm outputs in the
session scratchpad (`london_experiment.txt`); companion docs
`Mulligan_Strategy_Audit_2026-07-03.md`, `Plan_Aware_Mulligan_2026-06-16.md`.*
