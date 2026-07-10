# Zero-Sum Game — Badgermole Cub / Enduring Vitality / Pest Infestation eval

**Status:** LIVE · **Date:** 2026-06-30 · **Deck:** Zero-Sum Game (Witherbloom, the Balancer)
**Lab:** `scripts/wb_mana_engine_lab.py` · **Combo check:** `find_combos.py` vs Commander Spellbook, 2026-06-30

User asked whether three green cards had been considered for Zero-Sum, noting (correctly)
that **Badgermole Cub is synergistic with Enduring Vitality**. All three are color identity
**G** (legal in BG) and **none are Game Changers** — they don't touch the 3/3 GC cap.

Card text (card_lookup.py, 2026-06-30):

- **Badgermole Cub** `{1}{G}` 2/2 — "Whenever you tap a creature for mana, add an additional
  `{G}`." (+ earthbend 1 ETB.) Ruling: triggers only on a creature's `{T}` mana ability —
  fires on dorks **and** on Enduring Vitality's granted ability, **not** on convoke / "tap an
  untapped creature" costs (so it does **not** touch the Sprout Swarm or Lab Rats lines).
- **Enduring Vitality** `{1}{G}{G}` Enchantment Creature, Vigilance, 3/3 — "Creatures you
  control have '`{T}`: Add one mana of any color.'" Dies → returns as an enchantment (still
  granting mana). Turns the go-wide board into dorks; resilient to a wrath.
- **Pest Infestation** `{X}{X}{G}` sorcery — destroy up to X artifacts/enchantments; make 2X
  1/1 BG Pests with "when this dies, gain 1 life."

## Combo status — RAMP, not a new infinite

`find_combos.py` on the list **+ all three** returns **zero new COMPLETE combos** (14 → 14,
identical IDs). The EV × Badgermole pair is a CSB-confirmed *missing-1* away from an infinite:

- **Badgermole Cub + Enduring Vitality + Pili-Pala = infinite colored mana**
  ([combo 1247-6006-7008](https://commanderspellbook.com/combo/1247-6006-7008/)). Pili-Pala is
  not in the deck. With a board-scaling engine making 2 mana/creature, Pili-Pala untaps net-
  positive → infinite → dump into Finale of Devastation. A real 4th axis, but it needs a third,
  otherwise-dead card.

So as a **pair** EV × Badgermole is ramp. The user's instinct (a real synergy) is right; it
just isn't a wincon without Pili-Pala.

## Lab — does the ramp pair move the mana-gated axis?

The **primary lifeloop (T9)** is cheap (3–5 MV halves) and already known flat to fast mana
(`wb_clock_lab.py` gcswap: −Demonic +Mana Vault is flat-to-worse every turn). The one
**mana-gated** axis is **Line B**, the affinity magecraft infinite (8-MV commander + payoff +
Sprout Swarm + board≥4) — so that is where a board-scaling engine should bite.
`wb_mana_engine_lab.py`, 20k trials, models EV (non-dorks tap for 1) + Badgermole (+1`{G}` per
creature tapped), respecting summoning sickness via prev-turn board:

| Line B assembly (table-kill cum %) | T7 | T9 | T12 | never-in-14 |
|---|---|---|---|---|
| as-built (no engine) | 9 | 17 | 29 | **62%** |
| + Badgermole only | 10 | 18 | 31 | 61% |
| + Enduring Vitality only | 10 | 18 | 31 | 61% |
| **+ both (EV × Cub)** | **11** | **20** | **32** | **59%** |

The pair beats either alone (the synergy is real), but the whole effect is **~+3pp and a
62→59% never** — marginal. It does not move the headline kill (lifeloop, not mana-gated), and
the axis it helps is already the slow resilience line. Removes in the A/B (Toxic Deluge /
Pernicious Deed) are model-inert placeholders to hold library at 100, **not** a recommended cut.

## Verdict

- **Pest Infestation — the one worth a slot.** Different axis: it lifts **Interaction**
  (the deck's 2/5 soft spot, the stated highest-leverage upgrade) while making 2X bodies and
  seeding the lifeloop (Pests' death-lifegain = a built-in igniter). Not a mana card; this lab
  doesn't bear on it. **Buy candidate** — pending a cut + an Interaction-axis re-lab.
- **Enduring Vitality — resilience/mana-hunger include, not a clock upgrade.** Recurs through
  wraths; the external Glarb pilot called it "busted." But the lab says it does **not**
  measurably speed the kill. Include on feel for grindy games, low priority.
- **Badgermole Cub — owned** (spare beyond the `earthbend-the-meta` copy; ≈340 DKK / €46 foil,
  a real price not a data artifact). Weakest alone (+~1pp); only interesting *with* Enduring
  Vitality, and even paired the lift is marginal. Real ceiling = the Pili-Pala infinite.

**Bottom line:** the deck already carries three redundant infinite axes, so a 4th needing
EV + Badgermole + Pili-Pala is low priority. Of the three, **Pest Infestation is the only
measurable improvement** (it fixes the Interaction floor, not the clock). EV/Badgermole are a
defensible-but-marginal ramp/resilience pair here.

*(Per-roster question — does EV × Badgermole fit a greener, more creature-dense, mana-hungrier
deck than Zero-Sum? — tracked separately.)*
