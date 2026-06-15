# Self-Meta, Quantified — the long-game model

**2026-06-15.** `campaigns/Self_Meta_Ranking.md` ranks the roster against *itself* ("if a
4-player pod were drawn from my own decks, which wins?") as **explicit judgment** — "there
is no multiplayer rules-engine sim ... I won't fake one." This lab quantifies the part that
**is** measurable (the table-close race) and **decomposes** how much of the ranking rests on
the unmeasured rest — the long-game analog of how the Pod Gauntlet split anti-pod into a
measured race + a soft disruption overlay. Tool: `scripts/self_meta_lab.py`.

> Two numbers, stated separately (gauntlet discipline). **CLOSE** = lab-measured table-clock
> race. **WIN** = CLOSE + a soft durability overlay. Trust the *decomposition* and the
> *sweep*, not the second decimal.

## The model

Random 4-seat pods from the 16 active decks; each seat samples a **table-close turn** from
its lab table CDF (`pod_gauntlet_clocks.json`). Two readouts:

- **CLOSE-RACE (measured):** the earliest table-close wins (converge — a hit-all kill closes a
  3-seat table; the self-meta doc's metric). Pure lab clocks, no judgment.
- **WIN (+ overlay):** if *someone* closes by `T_grind`, the race decides; if the field
  **stalls** (no close by `T_grind`), the most **DURABLE** seat outlasts and wins. Durability
  is a soft index = `0.50·(1−table_never%) + 0.35·min(1, R+P answers / 8) + 0.15·opp_fed`,
  where defense counts come from the delay_lab roster suites (oracle-verified 2026-06-15) and
  `opp_fed` flags the one clear opponent-fed engine (Dark Lord's Sauron shell). `T_grind` and
  the weights are documented, **swept**.

## The ranking (T_grind=10, 80k pods)

```
 #  deck                  table never def dura  CLOSE  WIN   judg  Δrank
 1  The Genome Project      T8    1%   3  0.63   81%   81%    #3    +2
 2  Zero-Sum Game           T9   25%   5  0.59   54%   53%    #5    +3
 3  Radiation Sickness     T10    1%   6  0.76   44%   45%    #2    -1
 4  The Exile's Return     T10   12%   8  0.79   33%   38%   #11    +7
 5  Lorehold Spirits       T10    5%   3  0.61   36%   33%    #8    +3
 6  Curse of the Scarab    T11    9%   5  0.67   28%   27%   #10    +4
 7  The Dark Lord's Army   T12   10%   6  0.86   13%   26%    #1    -6
 8  The Replication Crisis T10   20%   7  0.71   22%   21%   #13    +5
 9  Earthbend the Meta     T11    7%   6  0.73   19%   20%   #12    +3
10  Ms. Bumbleflower       T11    2%   6  0.75   14%   17%   #15    +5
11  Crystal Sickness       T13   34%   1  0.37   16%   13%   #16    +5
12  Eldrazi Stampede       T12    8%   2  0.55   17%   11%   #14    +2
13  Lightning War          T14   39%  13  0.66    8%    7%    #4    -9
14  Diminishing Returns   >T14   70%   7  0.46    6%    4%    #9    -5
15  The Calamity Tax      >T14   60%  10  0.55    4%    3%    #7    -8
16  The Grand Design      >T14   82%   8  0.44    3%    1%    #6   -10
```

## What it found

**1. The ranking pivots on one assumption — how grindy is the field (`T_grind`).** This is the
load-bearing knob the judgment hid:

| `T_grind` | meaning | who wins |
|---|---|---|
| **8** (field reliably stalls — the judgment's stated premise) | most pods are grinds → durability decides | **Dark Lord #2 (62%)**, Exile's/Bumbleflower lift; Genome still #1 |
| 10 (baseline) | mixed | Genome / Zero-Sum / Radiation, Dark Lord #7 |
| **13** (someone usually closes fast) | ≈ pure close-race | converge closers sweep; **Dark Lord crashes to #12** |

So the judgment's **Dark Lord #1 is defensible — but only under its own premise that the field
reliably grinds past ~T8–10**, exactly where Sauron's opponent-fed durability dominates. The
model doesn't refute the judgment; it **exposes the assumption and prices it.**

**2. The "can't-close fortresses" are over-rated by the judgment — robustly, at every
`T_grind`.** Grand Design (#6→#16), Calamity Tax (#7→#15), Diminishing Returns (#9→#14) sit
bottom-four no matter the grind level. Their lab **table-never% is 60–82%** — they rarely close
the table *even goldfishing, unopposed*. The judgment's "win by inevitability if they survive"
is **not lab-supported**: surviving ≠ closing ≠ winning. A fortress that can't close doesn't win
the grind, it *draws* it — and the durability overlay (mid, because inevitability = 1−never% is
low for them) can't rescue a deck that never closes. This is the self-meta twin of the gauntlet's
"PURE RACE over-rates goldfish ceilings" caveat, pointed the other way.

**3. Lightning War is the cleanest judgment miss (#4→#13).** Its pingers *decap*/chip, but the
**table** clock (T14, never 39%) says it closes three seats slowly. The judgment rated its
self-meta on chip-everyone; the table clock says it doesn't convert that into a table-close.

**4. Genome is #1 at every `T_grind` — with the gauntlet's exact caveat.** Fastest table (T8,
never 1%), so it wins the measured race outright. But the model **cannot see fragility or focus
fire** — the judgment's reason for #3 (15/20 glass, draws the removal). Read Genome's #1 as a
*closing-speed ceiling*, discounted for the targeting the model ignores.

## Limitations (load-bearing — the symmetry with the gauntlet)

1. **Static table clocks miss opponent-fed acceleration.** Dark Lord's lab clock is goldfish
   (T12); the `dla_clock_lab` measured it **closes ~1 turn faster against an active pod** (table
   T11 high-tempo). A self-meta field is the most active pod possible, so the *measured* CLOSE
   (13%) **under-rates** Dark Lord — its true rank sits above the static-clock race, between the
   model's #7 and the judgment's #1. This is the exact dual of the gauntlet's "no opponent-clock
   tax" blind spot.
2. **Genome / fast glass are over-rated** — no fragility or focus-fire targeting (ceiling).
3. **"Most durable outlasts" is an abstraction** — no politics, no targeting, no 4-body combat
   math (the doc's stated reasons for staying judgment). The grind path is a tiebreak, not a sim.
4. **Durability and `T_grind` are documented judgment, swept** — only the table-close race is
   measured.

## Bottom line

The self-meta ranking is **not one ranking — it's a function of how grindy the field is.** The
lab measures the table-close race (converge decks win it) and prices the grind premise the
judgment leaned on (Dark Lord's #1 needs a reliably-stalling field). The durable verdict shift:
**the can't-close fortresses (GD / Calamity / Diminishing / Lightning War) are weaker in the
self-meta than the judgment said** — the table never% refutes their "inevitability," at every
`T_grind`. Run `python scripts/self_meta_lab.py --t-grind {8,10,13}` to see the crossover.
