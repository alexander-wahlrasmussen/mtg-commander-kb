# The Interaction Oracle — does modelling interaction rescue the Conversion Check?

**2026-06-16 · Backlog #6 · `scripts/interaction_meta_lab.py` + `framework_bakeoff.py --bakeoff`**

**Verdict.** Teaching the outcome oracle to model interaction/durability **shrinks the
Conversion Check's anti-correlation by about half but does not reverse it.** Against the new
interaction oracle the Conversion Check scores **−0.034** (vs −0.061 against plain self_meta
and −0.264 against the table clock) — the least-negative number CC posts against any of the
six oracles, and it slides monotonically toward zero as the interaction tax rises (−0.065 →
−0.011 across the sweep). Meanwhile pure-clock's lead **erodes** (+0.426 → +0.405; sweep
+0.423 → +0.391). The two move *toward* each other — exactly what you expect if interaction is
a **real but secondary** predictor. But CC never turns positive and the clock still leads:
roughly half of "score ⊥ results" was the goldfish artifact (interaction worth zero), and the
other half is genuine — the Conversion Check's top decks (Lightning War / Grand Design, 19/20)
are slow grind fortresses no interaction model can make *fast*.

---

## The question

The Framework Bake-Off (`Framework_Bakeoff_2026-06-16.md`) found no deck-quality framework
predicts winning, and diagnosed the cause: every oracle is a **solitaire goldfish**, so
Interaction and Durability — two of the Conversion Check's four axes, and Disciple's whole `I`
term — score **0**, and a framework that rewards them *cannot* correlate. The writeup flagged
the fix as "a real multiplayer interaction model … the rules engine the project deliberately
never built." Backlog #6 builds the tractable version of that — an **overlay, not a rules
engine** — and asks the direct question: *once interaction is worth something, does the
Conversion Check correlate?*

## The model (overlay, not a rules engine)

`interaction_meta_lab.py` extends `self_meta_lab`'s 4-seat random roster pod with one rule: a
closing seat must push its win **through the rest of the table's available answers.**

Per pod, reusing self_meta's pod draw + table-clock CDFs unchanged:
1. Sample each seat's **raw** table-close turn from its table CDF (identical draw to self_meta).
2. **Interaction tax.** For each seat, starting at its raw close turn `t`:
   `P(stopped) = TAX · pressure(others,t) · (1 − PROTECT[seat])`, where
   `pressure = 1 − Π_other (1 − interact[other])` (≥1 opponent holds a live answer). If
   stopped, the close slips a turn and the table's answers **decay** (finite interaction);
   else that's the effective close.
3. Winner = **earliest effective close**; if none by `T_grind`, the **most durable** seat
   outlasts (self_meta's grind fallback, untouched).

This finally pays the missing axes: **protect-own / counter-immune** decks (high `PROTECT`)
keep their clock; **interaction-dense** decks (high `interact`) tax opponents; **glass cannons**
(fast clock, low protect, low interact) get delayed and lose races they used to goldfish;
**durable fortresses** still take the grind tail.

**All inputs are already measured + oracle-verified, imported not re-derived:** `interact` =
each deck's measured P(hold a live answer on T6/T7) from `delay_lab --emit-json`
(`pg.MEASURED`); `PROTECT` = protect-own from `pod_gauntlet`; clocks/durability from
`pod_gauntlet` + `self_meta_lab`. The only new parameters are the **swept** tax magnitude and
the reused decay — no new card claims.

**Null reduction (the correctness gate).** With `TAX=0`, `P(stopped)≡0`, so effective close =
raw close and the output is **bit-identical to `self_meta_lab`** (verified: the `WIN(sm)` column
reproduces self_meta deck-for-deck, Δ=0 everywhere). The overlay only ever *adds* the tax.

## Result — the bake-off with the interaction oracle

Spearman ρ, every framework oriented so higher = "should win" (`framework_bakeoff.py --bakeoff`):

| Framework | gauntlet | selfmeta | **intract** | TABLE | decap | front7 | N |
|---|---:|---:|---:|---:|---:|---:|---:|
| **Conversion Check** | −0.259 | −0.061 | **−0.034** | −0.264 | −0.448 | −0.396 | 15 |
| BDD mana-budget | +0.139 | +0.019 | +0.019 | −0.034 | +0.085 | +0.124 | 16 |
| Disciple of the Vault | −0.448 | −0.374 | −0.358 | −0.419 | −0.376 | −0.433 | 16 |
| BDD consistency | +0.258 | −0.200 | −0.189 | +0.008 | +0.408 | +0.321 | 16 |
| WotC bracket 1–5 | −0.253 | +0.168 | +0.140 | +0.029 | −0.116 | −0.140 | 16 |
| **Pure clock (null)** | +0.903 | +0.426 | **+0.405** | +0.561 | +1.000 | +0.899 | 16 |

`intract` is `selfmeta` plus the interaction overlay, so the **selfmeta → intract** column pair
isolates the effect of interaction alone. CC: **−0.061 → −0.034** (negative nearly halved).
pure-clock: **+0.426 → +0.405** (lead eroded). They converge.

### Robustness — the shift is monotone across the tax sweep

ρ vs the interaction oracle at each tax level (TAX=0 is the self_meta null; 80k trials):

| TAX | CC ρ | Disciple ρ | pure-clock ρ |
|---:|---:|---:|---:|
| 0.0 | −0.065 | −0.400 | +0.423 |
| 0.3 | −0.037 | −0.397 | +0.408 |
| 0.6 | −0.034 | −0.358 | +0.405 |
| 0.9 | −0.011 | −0.321 | +0.391 |

The CC shift toward zero is **monotone** — not an artifact of the TAX=0.6 snapshot. Disciple's
negative also shrinks (its `I` term rewards interaction, which now matters) but stays robustly
backwards. Pure-clock erodes monotonically: the more interaction predicts winning, the less
pure speed does. Exactly the signature of a real-but-secondary factor.

### Who interaction lifts vs sinks (TAX sweep Δ, high − null)

| lifted (resist tax / tax others) | Δ | sunk (fast-but-answerable) | Δ |
|---|---:|---|---:|
| The Dark Lord's Army (19/20, dura .86) | +13 | The Genome Project (15/20, prot 5%) | −14 |
| The Calamity Tax (18/20) | +6 | Lorehold Spirits (18/20, prot 0%) | −11 |
| Radiation Sickness (18/20) | +5 | Eldrazi Stampede (14/20) | −4 |
| The Exile's Return (17/20) | +5 | Zero-Sum Game | −3 |

The pull on CC is legible: the overlay **drops Genome** — the 15/20 glass cannon that was
self_meta's #3 and the single biggest CC counter-example — by up to 14 points, and **lifts**
the interaction-dense / durable high-CC decks (Dark Lord, Calamity, Radiation, Exiles). That is
the entire mechanism by which CC's anti-correlation shrinks. The cap on the gain is also
legible: the two **highest** CC decks, Lightning War and Grand Design (both 19/20), have huge
`interact`/`PROTECT` yet barely move (+2 / −0) because their clocks are T14 / >T14 — interaction
can't make a fortress fast, and self_meta already credited their durability.

## What it means

1. **About half of "score ⊥ results" was the goldfish artifact.** Modelling interaction
   nearly halves CC's negative (−0.061 → −0.034) and the effect is monotone in the tax. A
   real chunk of the bake-off's damning verdict was the oracle scoring two of CC's four axes at
   zero, not the framework being wrong.
2. **The other half is genuine.** CC never crosses positive, and pure-clock still leads even
   with interaction fully turned on. The Conversion Check's best decks are slow by design (it
   *explicitly* holds the clock out as "not a fifth axis"); an interaction model can reward
   their resilience but cannot make them close faster, which is still what wins.
3. **Interaction is a real but secondary predictor.** It erodes pure-clock's edge (+0.426 →
   +0.405) without overtaking it. On *this* roster, when you want to know which deck wins, the
   clock is first and interaction is a correction — not the other way round.
4. **The honest prior held exactly.** The pre-registered guess (`project_framework_bakeoff`)
   was "a fidelity upgrade that shrinks CC's negative, not a verdict reversal." That is what the
   data shows, to the decimal.

## Limitations — read before quoting a ρ

- **An overlay, not a rules engine.** No targeting, stack, politics, combat, or shared-answer
  accounting (each closing seat faces a "fresh" table; the decay models one seat's contest, not
  a global answer pool). It is a heuristic race correction whose *job* is to make interaction
  worth more than zero — deliberately the tractable version the repo's discipline allows
  ("I won't fake a rules engine"), not the full thing.
- **`interact` and `PROTECT` are priors.** `interact` is delay_lab-measured (oracle-verified
  2026-06-15) but at the a=0 column (reactive answers live) and only at T6/T7 — it over-credits
  interaction at very early closes (less mana than T6 assumes) and flat-extends the late game.
  `PROTECT` is a verified-where-set judgment prior. Trust the **direction and decomposition**,
  not the second decimal.
- **N = 16 (CC = 15).** Per the bake-off, |ρ| ≈ 0.50 is the significance bar, so none of these
  individual ρ's clears it; the robust claim is the **monotone cross-tax pattern**, not any one
  cell. The snapshot oracle is 120k trials; the bake-off's older P(win) snapshots are 20k, so
  the selfmeta cell wobbles ±0.01 between the table and the sweep (−0.061 vs −0.065) — noise.
- **Still Layer 1.** This predicts the *simulated* outcome with a richer model, not real games.
  Layer 2 (`game_log.py` → `calibrate.py`) is the only thing that can validate the tower.

## Reproduce

```
python scripts/interaction_meta_lab.py --tax 0           # null check: reproduces self_meta_lab
python scripts/interaction_meta_lab.py --tax 0.6         # the overlay (per-deck CLOSE→WIN→INTER)
python scripts/interaction_meta_lab.py --sweep           # INTERACTIVE P(win) across the tax grid
python scripts/framework_bakeoff.py --bakeoff            # the six-oracle correlation table
```

## Related

- `analysis/Framework_Bakeoff_2026-06-16.md` — the verdict this answers (the goldfish-leak diagnosis).
- `scripts/self_meta_lab.py` · `scripts/pod_gauntlet.py` · `scripts/delay_lab.py` — the measured substrate reused.
- `campaigns/Self_Meta_Ranking.md` · `campaigns/Kill_Window_Lab_Sweep_2026-06-13.md` — the "score ⊥ clock" thesis.
- memory `project_framework_bakeoff` — project log (the honest prior this confirms).
