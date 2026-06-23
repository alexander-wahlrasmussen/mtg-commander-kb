# Pod Matchup Matrix — Roster vs. The Combo Opponent

How each active deck matches up against the recurring pod combo opponent — a
**decision aid**, not a guarantee. It combines lab-measured kill clocks, each
deck's interaction profile, and the two-deck race model in
`scripts/pod_gauntlet.py`. State doc: re-derive when a deck's score, clock, or
interaction suite changes.

**Last run: 2026-06-15.** Regenerate with `python scripts/pod_gauntlet.py --matrix`
(clock cells linted by `python scripts/clock_check.py`).

The table races each deck **separately vs his real decks** — Acererak (mono-B
ETB), Hidetsugu and Kairi (UB death), and the 5C tail — then blends them by how
often he brings each. It bakes in two corrections a flat single-opponent model
misses: the **Grand Abolisher colour-lock** (his two mains can't run white
Abolisher, so reactive decks recover value) and **protect-own** (a deck's own
counters / a counter-immune kill).

---

## The opponent we're tuning against

From `project_pod_combo_opponent` (card text verified). He is **not** a generic
combo pod — he has a small stable, and the two decks he actually brings now are:

- **Acererak the Archlich** ({2}{B}, **mono-B**) — *his favorite.* Engine is the
  **ETB trigger** (recast → venture, repeatedly); the kill is a damage/drain
  **loop** off the dungeon's "each player loses life" rooms.
- **Hidetsugu and Kairi** ({2}{U}{U}{B}, **UB** — one commander). Engine is the
  **death trigger**: each death drains an opponent for the top card's mana value.
  Loops on a sac outlet + recursion.
- A legacy **5C tail** (Ur-Dragon / Kenrith / Kinnan) — status unconfirmed in the
  current meta.

He **wins T6–7**. Bracket-4-in-spirit despite a low GC count.

**Grand Abolisher is white, so Acererak (mono-B) and H&K (UB) are colour-locked
out of it.** Against his two *current* decks your reactive answers mostly live:

- **vs Acererak** — no Abolisher *and* no counters in mono-B; your answers almost
  all resolve. The threat is his *speed* + proactive **discard** stripping your
  answer pre-combo.
- **vs H&K** — no Abolisher, but a real **UB counter wall** (FoW / Swan Song /
  Fierce Guardianship / Mana Drain). You fight 1-for-1; no blanket lock.
- **vs the 5C tail** — the original Abolisher logic still applies; only these
  shells can field it.

So the matchup is decided **per-deck**, by clock (do you kill by T6–7?),
interaction read against the *right* protection (counter wall vs discard+speed,
not a universal lock), and the right static for the right loop — and there is
**no single static**, because his two mains loop through different triggers:

| static | Acererak (ETB) | H&K (death) | 5C tail |
|---|---|---|---|
| Torpor Orb / Hushwing Gryff | **hard lock** | **stone blank** | partial |
| Rule of Law (one spell/turn) | hits | hits | hits |
| Drannith Magistrate | soft (CZ recast only) | soft | soft |
| Cursed Totem | blank | weak | weak |

ETB-hate hard-locks Acererak and does **nothing** to H&K; only Rule of Law-class
+ exile-the-commander-on-sight + **racing** hit both. Damage-loop kills also mean
**lifegain is a trap** (infinite drain beats any life total) and Thoracle/tutor
hate (Mindcensor) is low value.

---

## The matrix

Rows ordered by blended **P(win)**. Each deck raced separately vs Acererak / H&K /
5C-tail (priors **0.45 / 0.40 / 0.15**), then blended.

- **Clock** = lab decap / table median (`analysis/pod_gauntlet_clocks.json`).
- **prot** = *protect-own* — P(this deck forces its kill through their reactive
  answer): own counters (grep-verified count) + a counter-immune kill.
- **vs Acrk / H&K / tail** = `simulate_vs` per opponent; **BLEND** = weighted avg.

> **Read with its biases:** (1) the clock is an **unblocked goldfish ceiling**, so
> fast decks read optimistically; (2) weights / answer / `prot` values are
> **priors** — tune as you log real games; (3) the blend is a **decap race**, so it
> under-rates control decks that LOCK rather than race (Grand Design reads 30% here
> but **45% blend / 59% vs Acererak** with its Elesh Norn lock, `--vs-lock`). Read
> the per-opponent spread + verdict, not the blend alone. Roster-wide: **everyone
> is strongest vs Acererak** (mono-B, no counters) **and weakest vs H&K** (the UB
> counter wall) — H&K is the table's real problem deck.

| # | Deck | Sc | Clock decap/table | prot | Acrk | H&K | tail | BLEND | Verdict vs pod |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Radiation Sickness | 18 | T7 / T10 | 55% | 73% | 68% | 67% | **70%** | **Bring — top + robust.** Counter-immune board kills (Simic Asc / Toxrill / rad) give H&K's wall nothing to target (Δ Acrk−H&K just +5). The default pick. |
| 2 | The Replication Crisis | 17 | T7 / T10 | 55% | 67% | 62% | 59% | **64%** | **Bring — #2.** 7 counters + combat/Kiki board kill, badly under-rated until protect-credited. Kiki swap adds an Abolisher-proof line. |
| 3 | The Genome Project | 15 | T7 / T8 | 5% | 65% | 58% | 57% | **61%** | **Race ceiling, not a lock.** 15/20 glass, combo-reliant, ~no protect — discount for the fragility the goldfish can't see. |
| 4 | Lightning War | 19 | T9 / T14 | 65% | 54% | 47% | 43% | **49%** | **Bring vs Acererak (54%).** Tempo + counter-war + uncounterable Banefire; fights H&K's wall rather than folding to it. |
| 5 | Ms. Bumbleflower | 15 | T8 / T11 | 15% | 53% | 43% | 40% | **47%** | **Soft.** decap T8 but the combat-only kill is goldfish-optimistic; thin protect. |
| 6 | The Exile's Return | 18 | T8 / T10 | 30% | 48% | 41% | 39% | **44%** | **Even–favoured.** Own Abolisher protects its turn; Drannith swap adds static; Kiki/combat kill. |
| 7 | Earthbend the Meta | 17 | T8 / T11 | 30% | 46% | 39% | 37% | **42%** | **Even.** REB/Pyroblast bite H&K's blue specifically; mid clock. |
| 8 | Lorehold Spirits | 18 | T8 / T10 | 0% | 42% | 36% | 35% | **39%** | **Even.** decap T8, combat; no counters or protect. |
| 9 | Curse of the Scarab | 17 | T8 / T11 | 40% | 41% | 37% | 36% | **39%** | **Even.** 5 counters + zombie-army board kill; mid clock. |
| 10 | Zero-Sum Game | — | T9 / T9 | 30% | 36% | 34% | 33% | **34%** | **Even (unaudited).** Board-independent, Abolisher-proof lifeloop kill. |
| 11 | The Grand Design | 19 | T10 / >T14 | 45% | 35% | 27% | 24% | **30%** | **Anti-Acererak CONTROLLER — the race number under-rates it.** →**45% blend / 59% vs Acererak** with its Elesh Norn ETB-lock (`--vs-lock`); best vs Acererak + the 5C tail (own Abolisher); weakest vs H&K (lock inert vs death). |
| 12 | The Dark Lord's Army | 19 | T9 / T12 | 45% | 28% | 24% | 23% | **26%** | **Underdog vs combo.** 7 counters but clock-bound T9; self-meta #1 (opponent-fed). |
| 13 | Eldrazi Stampede Chaos | 14 | T8 / T12 | 10% | 28% | 24% | 23% | **26%** | **Underdog.** combat kill, ~no protect. |
| 14 | Diminishing Returns | 17 | T9 / >T14 | 10% | 19% | 15% | 14% | **17%** | **Underdog.** slow death-combo, no counters; self-meta strong. |
| 15 | Crystal Sickness | 17 | T11 / T13 | 30% | 9% | 8% | 8% | **9%** | **Underdog.** slow clock (T11). |
| 16 | Croak and Dagger | 18 | T13 / >T14 | 35% | 6% | 5% | 3% | **5%** | **Don't bring as built;** the grind-fortress rebuild → 27% (`--swapped`). |

*(Peace Offering is off the active roster and excluded. Scores are the current
Conversion-Check audit. BLEND weights and the `prot` / opponent `answer` /
`disruption_a` levels are PRIORS — tune as real games are logged.)*

---

## Pending / build candidates

Decks being built or considered, raced through the **same model** as the active
matrix — `python scripts/pod_gauntlet.py --matrix --pending` (run 2026-06-18). Kept
out of the active table above because the builds aren't finalized/audited; clocks are
lab-sourced (`kfk_clock_lab` / `hsh_clock_lab`), `prot` values are priors.

| Deck | Clock decap/table | prot | Acrk | H&K | tail | BLEND | Would slot |
|---|---|---|---|---|---|---|---|
| Hashaton (Thoracle) | T6 / T6 | 40% | 72% | 69% | 68% | **71%** | **above Radiation** (new #1) |
| Kefka (Forced Liquidation) | T8 / T9 | 45% | 45% | 41% | 39% | **42%** | between Exile's Return (#6) and Earthbend (#7) |
| Zero-Sum Game | T9 / T9 | 30% | 36% | 34% | 33% | **35%** | already active (row 10) |

- **Hashaton would top the matrix — but as a *race ceiling*, not a lock** (the Genome
  caveat, #4): a glass one-line Thassa's Oracle combo whose fragility the goldfish
  clock can't see. Its 40% `prot` (counters guarding the combo turn) makes it less
  glassy than Genome's 5%, but **Radiation stays the safer real-games pick** —
  counter-immune board kills vs a single combo line.
- **Kefka reads mid-pack here**, capped by its T8 clock — and this base race **does
  not credit its anti-pod reason to exist**: the Cursed Totem lock + the on-your-turn
  *triggered-damage* (anti-Abolisher) kill. That value lives in the `--lock` view, not
  the blend. Its pitch is resilience vs the lock pod, not race speed.
- **Zero-Sum** is already in the active table (built, cards on order); listed here only
  to confirm ~35% is unchanged under `--pending`.

Build status / sourcing: `Build_And_Swap_Tracker.md`.

---

## What the sim adds

One standing finding from `scripts/deck_sim.py` (consistency Monte Carlo, 20k
trials/deck), separate from the labs: **fixed 2-card combos are ~2% to draw
naturally by T10** (~2–6% with their lone tutor) — correct maths for two
singletons in 99 cards. These decks' real speed comes from **redundancy,
alternative lines, and tutor packages**, not from drawing the named pair. Decks
that race the pod need redundant kill density, not a prettier two-card combo.

Colour-T6 floors are a uniform **88–99%** across the roster (lands-only model) and
don't differentiate decks — dropped from the table.

---

## Recommendations

1. **Reactive answers are on the menu vs his two current mains.** The "their
   Abolisher kills your counters" gap holds **only for the 5C tail** — Acererak
   (mono-B) and H&K (UB) can't field it, so counters/removal mostly **resolve**.
   That's why the counter-heavy decks (Radiation, Replication, Lightning War) top
   the table once `prot` credits them. Static hatebears are **loop-typed, not
   universal**: ETB-hate hard-locks Acererak but **blanks** H&K; only Rule of
   Law-class + exile-on-sight hit both. GD's already-present **Elesh Norn** is the
   standout (`--vs-lock`).
2. **The "too slow" tier (Dark Lord, Bumbleflower, Lorehold, Earthbend) is fine —
   just not the deck you bring to *this* pod.** Don't speed them up at the cost of
   their identity; pick a faster deck for this table.

---

## Method & limits

- **Source of truth:** each deck's `.txt` + `collection/oracle-cards.json`; kill
  windows and interaction scores from the audited `*_Summary.md` files.
- **`deck_sim.py` is not a rules engine** — it models opening-hand keepability
  (London mulligan, 2–5 land keep), land drops, colour from lands, and
  combo-piece draw. It does **not** model casting, the stack, or mana from
  rocks/dorks. Treat mana/colour figures as **floors**.
- **Clock + the `--vs` blend are lab/gauntlet-sourced** — clock medians from
  `analysis/pod_gauntlet_clocks.json` (the `*_clock_lab.py` suite, harvested by
  `pod_gauntlet.py --refresh`); the per-opponent and BLEND columns from the
  two-deck race (`simulate_vs`). Regenerate with `python scripts/pod_gauntlet.py --matrix`.
- **The blend is heuristic, with three known biases:** the clock is an unblocked
  goldfish **ceiling** (over-rates fast decks); the opponent weights / `answer` /
  `disruption_a` and each deck's `prot` are **priors**, not measured; it's a
  **decap race** that under-rates lock/control decks (GD's persistent-lock line
  lives in `--vs-lock`, not the blend). Read the per-opponent spread + verdict.
- **The verdict column is judgement**, anchored to the data above and the pod
  profile — not simulator output.
