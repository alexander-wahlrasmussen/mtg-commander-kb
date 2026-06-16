# External "Yd Freehold" Glarb vs The Calamity Tax — head-to-head (2026-06-16)

*Experiment (branch `experiment/external-glarb-vs-calamity`). Ranks the external budget
Glarb list the user added (`proposals/External Glarb.md`, the "Yd Freehold" / Palladium
Reef primer) against our own Glarb deck, **The Calamity Tax**. Same commander, same
archetype — a clean apples-to-apples.*

- **Lab:** `scripts/ext_glarb_vs_calamity_lab.py` (reuses `speed_lab_core`), 40k trials, seed 20260616.
- **External list as a sim deck:** `decks/considering/glarb-external-ext-20260616.txt` (registered `glarb-external-ext` → Glarb in `deck_sim.COMMANDERS`).
- **Card text** for every win/answer/combo card verified via `card_lookup.py` 2026-06-16.

---

## Setup notes (data + faithfulness)

- Two external land names are absent from our (stale) Scryfall snapshot. Per the user they
  resolve to **Barrow-Downs → Bojuka Bog** and **Henneth Annûn → Reflecting Pool**; patched
  in the lab so the external land count / keepable% is honest.
- **The pasted decklist is already the post-pivot "explosive" version.** The primer's headline
  3-card combo needs **Bloodthirsty Conqueror**, which the 6/13 changelog cut and which is **not
  in the 99**. So the list as written wins by grind/value, not the combo.
- **Two card-name flags in the external list:**
  - `Sheoldred` resolves to the {3}{B}{B} Praetor (ETB edict, flips to *The True Scriptures*) —
    consistent with the primer ("Sheoldred ETB"). OK.
  - The decklist lists **`Teferi, Master of Time`** (4-MV planeswalker), but the *entire primer*
    discusses **`Teferi, Mage of Zhalfir`** (5-MV flash-lock creature). The roles don't match;
    likely a transcription slip. Treated as a value/protection slot; flagged for the user.

---

## Results

```
                                              T3    T4    T5    T6    T7    T8   T10
The Calamity Tax (ours)   keepable 99%  | FREE-int 7 | TOTAL-int 14
  (smooth) has a play by T               98   100   100   100   100   100   100
  ANSWER: >=1 FREE interaction in hand   48    52    56    59    63    66    71
  ANSWER: >=1 ANY  interaction in hand   74    78    82    84    87    89    92
  FINISH: payoff in hand (mana-gated)    43    47    50    54    57    60    65

External Glarb (Yd Freehold)  keepable 100% | FREE-int 4 | TOTAL-int 16
  (smooth) has a play by T               96   100   100   100   100   100   100
  ANSWER: >=1 FREE interaction in hand   31    34    37    40    43    46    51
  ANSWER: >=1 ANY  interaction in hand   80    84    87    89    91    93    95
  FINISH: payoff in hand (mana-gated)    58    62    66    69    72    75    80

External + combo re-armed (+Bloodthirsty Conqueror / -Teferi MoT)
  COMBO: Cistern+Doom+Conqueror assembled  1     1     2     2     3     4     6
```

| Axis | Calamity Tax | External | Read |
|---|:--:|:--:|---|
| **SMOOTH** (keepable / play-by-T) | 99% / 98%@T3 | 100% / 96%@T3 | **Tie.** Both are exceptionally consistent Glarb piles. |
| **FREE interaction @T6** | **59%** | 40% | **Ours, decisively.** Our pitch/0-mana suite (FoN, Force of Vigor, Fierce Guardianship, Pact, Deadly Rollick, Swan Song, Veil) lets us develop *and* hold up answers. The external author himself flags "holding up 3 mana for interaction has felt awkward." |
| **ANY interaction @T6** | 84% | **89%** | External slightly higher by raw count (16 vs 14) — but most is **mana-gated** (Counterspell, Ertai, Counterbalance, sorcery removal). |
| **FINISH ceiling @T8** | 60% | **75%** | **Misleading — counts bodies, not lethality.** External has 6 candidate payoffs (Gary, Syr Konrad, Doom, Archon, Breach, Oculus) vs our 3, so "a payoff is in hand" fires more often. But its payoffs are **incremental/value** (pings, 2/2s, a fat beater, a one-shot swing); **ours are scalable table-enders** (Torment of Hailfire-X / Finale-X off the Cabal Coffers + Urborg engine). The ceiling can't see SCALE — it understates our edge. |
| **Headline combo** | n/a | **2%@T6, 6%@T10** even re-armed | And that's the *optimistic* ceiling ignoring mana/life/library-size gating. The combo is a once-in-a-blue-moon win — exactly why the author cut it. |

---

## Verdict — where the external deck ranks

Both decks are the **same thing**: a Sultai Glarb grind-fortress whose kill is a mana-gated
drain, not a race. On the roster's "Definitive Tier List" (2026-06-15) our **Calamity Tax = Tier B,
composite 44** (Power 18, Self-meta 36%, **Anti-pod 22% = roster-worst**, table T10).

**The external list lands in the same band, a notch BELOW our Calamity Tax — low-B / high-C.**
The three drivers, by the composite's own weights (Anti-pod 0.40 / Self-meta 0.35 / Power 0.25):

1. **Anti-pod (the heaviest axis): external is *worse* than our already-worst 22%.** Thinner free
   interaction (40 vs 59 @T6) + a slower real clock (author-reported **T8–10, often T10–11**, vs our
   T10) mean it can neither race nor reliably interrupt the recurring T6–7 combo opponent. Its slightly
   higher *total* interaction doesn't help when it has to tap out to develop.
2. **Power: lower.** A budget, **0-GC, ~$750** Bracket-3 build. Well-built for that bracket, but no
   Cabal Coffers/Urborg payoff engine, no Mana Drain/Force free-counter suite, no Seedborn Muse — so
   the X-drains it does have are smaller. Estimate ~14–16/20 vs our 18.
3. **Self-meta: roughly comparable to slightly below.** A grind fortress *survives* a pod of grind
   decks (the Dark Lord paradox), but its weaker finish + slower clock shade it under our 36%.

**Important fairness caveat:** the external deck is a self-described *moderately strong Bracket-3*
deck with a **real, logged 26–18 win rate** in its intended meta. Our Anti-pod axis grades against a
faster (cEDH-ish T6–7 combo) pod than this deck targets. **On its own B3 terms it is a genuinely
strong, consistent, winning build.** It loses this head-to-head because our Calamity Tax is the same
archetype tuned harder (premium mana, a scalable table-ender, a dense free-interaction suite) for a
harsher pod.

---

## The "suggested improvement" — Maldhound's review (transcript pulled)

Transcript fetched via `youtube-transcript-api` (the video, `J2G-tO88YoU`, is Maldhound's "deck
review" series; auto-captions). His read is unambiguous and it **reframes the whole question**:

> *"The deck's very good… If anything, we have to make it worse… I have no interest in making this
> deck better… you're winning more than half your games [22–16]… this is peak bracket three
> heinously strong good-stuff pile… There's nothing you need to cut here, there's nothing you need
> to add here."*

His thesis: the deck's only flaw is **dissatisfaction**, not weakness — it wins slow wars of attrition
("nickel-and-dime," "the accounting department") rather than big explosive turns. So every suggestion
is **explicitly power-neutral-to-negative**, aimed at making wins *feel* bigger:

> *"I would be taking out anything that provides incremental value for something that provides a huge
> amount of value in one turn… It's going to be worse than what you currently do, but I'm going to
> try to make you feel something."*

**Specific cards he names (all card-text-verified 2026-06-16):**
- **Rite of Replication, kicked** (over The Scarab God) — five Archons of Cruelty = a concise win. *(Already in the pasted 99.)*
- **Gogo, Master of Mimicry** ({2}{U}; copy a triggered/activated ability X times) — a mana-sink finisher: copy the Archon of Cruelty / Gray Merchant trigger X times to "win the game outright." *(MV3 → not castable off Glarb's top, as he notes.)*
- **Doomsday** ({B}{B}{B}) — affirms a Sultai Doomsday line is Bracket-3-doable (non-Thoracle); "tell people that's your win condition."
- **The Gitrog, Ravenous Ride** ({3}{B}{G}) — churn to reach big reanimation sooner *(floated, hedged on power)*.
- **Jumbo Cactuar** ({5}{G}{G}) and **Lord of the Void** ({4}{B}{B}{B}) — floated then **rejected** ("even slower" / "already not concise").
- **Trim candidates:** Teferi (Mage of Zhalfir) + High Fae Trickster (flash-package math); one-for-one wincon swaps generally.

### What this does to the ranking

By Maldhound's own framing the "improved" deck is **weaker, not stronger** — so it does **not** leapfrog
our Calamity Tax, and on our consistency-rewarding self-meta/smooth axes it is a lateral-to-slightly-down
move (most of his ideas are win-more or slower).

**The real nuance:** a *subset* of his concise-kill ideas — **kicked Rite of Replication, a Doomsday
line, Gogo copying the Archon/Gary trigger** — attack the exact axis our whole lab stack says a Glarb
grind-fortress is weakest on (**closing**; "closing > building"). On *our* results-oriented yardstick
those are the closest thing to a genuine ranking-relevant *upgrade*, even though Maldhound sells them as
"making it worse." We optimise for closing vs a fast T6–7 pod; he optimises for B3 win-rate (where
grinding wins). The catch: a real Doomsday/combo line would shed the **fair, 0-GC B3 identity** that made
the deck a >50% sleeper in the first place — so it's a lever that trades identity for closing power, the
same trade our own Calamity Tax already made.

---

### Scored: the concise-kill variant (`--mode closing`, plan-aware mulligan)

Built Maldhound's concise-kill subset by swap (`build_lib`): **−The Scarab God, −High Fae Trickster,
−Teferi (MoT); +Gogo, Master of Mimicry, +Bloodthirsty Conqueror, +Doomsday** (kicked Rite already
in). Scored the **board-independent 2-card kills** it adds (Gogo copying the Gary/Archon trigger; kicked
Rite on a fat creature), and — per the user's steer — ran it under the **plan-aware mulligan**
machinery (`set_keep_spec`, a FINDING keep that mulligans toward the kill) vs the naive land-count keep.
Reference bar = our Calamity Tax's *real* keep-spec (MANA) and its scalable X-drain finish.

| Line | keepable | CONCISE-kill @T6 | @T8 |
|---|:--:|:--:|:--:|
| **Calamity Tax — FINISH (scalable X-drain)** *[bar]* | 84% | **53%** | **59%** |
| External as-is (MANA keep) | 85% | 11% | 15% |
| Maldhound variant — default land keep | 100% | 29% | 37% |
| **Maldhound variant — FINDING keep (mulligan toward kill)** | 91% | **37%** | **45%** |

**It moves the closing number substantially toward our Calamity — but converges to, not past, it.**
The discrete-kill availability gap to the bar shrinks from **11→53 (42pp)** for the as-is list to
**37→53 (16pp)** for the plan-aware variant — a **~60% gap closure**. Two clean reads:

- **The variant ~triples the as-is deck's concise-kill availability** (11%→29% at T6 before mulligans),
  and the **plan-aware mulligan adds a real, robust ~+8pp** (29%→37%) at a modest keepable cost
  (100%→91%, still 100% "has a play" by T4) — the mulligan work *verifies* the lift is not a keep
  artifact.
- **It plateaus below the bar by design.** Traced mechanically, Maldhound's explosive adds (Gogo
  copying a Gary drain X times; kicked Rite = five Garys/Archons) are **the same scalable,
  mana-hungry, board-independent X-drain kill our Calamity Tax already wins with.** The variant
  *adopts our win condition* — so it converges toward our number, then stalls, because it lacks our
  Cabal Coffers/Urborg mana engine to power those X-kills and our free-interaction suite to protect
  them. All four curves are mana-blind ceilings; the real kills are gated the same way, so the
  *character* of the remaining gap is real, not an artifact.

**Net:** Maldhound's "make it worse (more fun)" subset is, on our results yardstick, a genuine upgrade
to the deck's weakest axis (closing) — it lifts the external from "no discrete closer" toward Calamity's
level and would nudge it up within Tier B. It does **not** overtake our Calamity Tax, and it does so by
becoming a budget version of the same scalable-drain deck (shedding the fair-B3 identity Maldhound
prized). The ranking holds: **ours ≥ Maldhound-improved external > external as-is**, all in the same
grind-fortress band.

## Upgrade pass — steal the external's best ideas into our Calamity Tax (`--mode upgrade`)

Swap (`build_lib`, all card text verified; none are GCs → stays **3/3 GC**, 100 cards):
**−Submerge −Open the Way −Spore Frog / +Counterbalance +Wan Shi Tong +Abhorrent Oculus.**

| | keepable | FREE-int @T6 | ANY-int @T6 | FINISH @T8 |
|---|:--:|:--:|:--:|:--:|
| Calamity Tax — current | 99% | 59% | 84% | 60% |
| Calamity Tax — upgraded | 100% | 60% | **85%** | 60% |

**Verdict: neutral on every axis this lab scores** — and that's expected. No free counter or finisher
was added, so FREE-int and FINISH are flat by construction; ANY-int moves +1pp (Counterbalance). The
real value is in axes an availability sim cannot measure — the **Glarb + Counterbalance** soft-lock
(we control/know our top card → near-deterministic counters), Wan Shi Tong card flow, Abhorrent Oculus
board-grind/dig. Same lesson as every prior upgrade pass in this repo: *adds move the unmeasured axes,
not the median.* So the lab can't *validate* the upgrade — it can only confirm it costs nothing
measurable (keepable/finish/smooth all hold).

**Ownership / recommendation (Moxfield CSV 2026-06-07; no reskin aliases):**
- **Wan Shi Tong, Librarian — OWNED, $0, in no deck.** Lowest-risk; a clean draw-engine-over-redundant-ramp swap. **Take it now.**
- **Counterbalance — BUY.** Highest synergy with Glarb, but a deploy-2 enchantment that telegraphs and eats removal; value real but unmeasured. Worth a cheap pickup if pursuing.
- **Abhorrent Oculus — BUY, most speculative.** Wants a 6-card graveyard as an additional cost — slower for us than the external's Doom Whisperer mill shell; its value is board-grind the lab can't score. Hold unless proxying.

*(Considered & passed: Prismatic Undercurrents / Carpet of Flowers — strong in the budget list, weak
for us: few basics, and we already run Exploration + Azusa for extra land drops.)*

**Not applied to the deployed `calamity-tax-20260615.txt`** — two of three adds are buys and the
measurable impact is neutral, so this stays an experiment-branch proposal pending the user's call on
the purchases. Applying would need the usual protocol (date-bump the filename, archive the old `.txt`,
update the Summary; clock citation unchanged — finish curve flat).
