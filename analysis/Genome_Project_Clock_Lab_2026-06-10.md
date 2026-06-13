# Genome Project — Kill-Turn Lab & Clock-Upgrade Judgment (2026-06-10)

**Deck:** The Genome Project (Kuja, Genome Sorcerer — Rakdos wizard-token spellslinger)
**Lab:** `scripts/gp_clock_lab.py` (modes `clock`, `levers`; 20,000 trials, seed 12345)
**Decklist:** `decks/the-genome-project-20260510.txt`
**Question:** Verify the unverified "Goldfish T7–9" claim; judge whether the clock can be upgraded.

---

## Verdict

1. **The claimed window HOLDS — the first of seven labbed decks whose hand-estimate
   survives.** Goldfish: **decap median T7 (41% T6, 82% T7) / table median T8
   (49% T7, 78% T8)**. The Summary's "T7–9" sits exactly on the measured table
   clock. Five prior labs falsified five optimistic claims; this one was honest.
2. **The clock CANNOT be meaningfully upgraded by card swaps.** Four axes tested
   at 2 cards, two at 4 cards — every variant lands within +4 percentage points
   at T7 and ±0–1 on the median. The clock is structurally bound (see §4).
3. **Decap ≈ table is structural, and it's an asset.** Wizard pings hit every
   opponent simultaneously, so this deck's two clocks converge (T7/T8) instead
   of diverging 2–3 turns like the combat decks (e.g. Grand Design T10/T12+).
   Genome Project kills the *table* nearly as fast as it kills one player.
4. **Three card-text/rules errors found in the Summary** during oracle
   verification (§5) — one of them (Bonus Round) overstates a kill line.

---

## 1. Method

Kill-turn goldfish on the `speed_lab_core.py` harness, same conventions as
`gd_clock_lab.py` / `rc_speed_lab.py`: unblocked damage, 3 opponents @ 40,
mana = lands + rocks floor, London mulligan via `deck_sim.py`. Decap and table
reported separately per the verification rule.

Damage per noncreature cast, to each opponent (all multipliers oracle-verified
2026-06-10 via `card_lookup.py`):

```
(p1 + 2×BlackWaltz) × trig × trance2 × city3
  p1      = Kuja tokens + Coruscation Mage (+Offspring) + Rod Hero
  trig    = 1 + Harmonic Prodigy + Roaming Throne   (additive)
  trance2 = ×2 Trance Kuja (Wizard damage only)
  city3   = ×3 City on Fire (all damage from your sources; CONVOKE-discounted)
```

Turn model: main-phase chain → combat (focus-fire, sickness respected) → Neheb
postcombat {R} per opponent life lost this turn → second chain → end step
(Kuja token, transform at 4+ Wizards, Necropotence refill to 7).

**Modelled:** rocks/rituals/draw-2s as ping triggers, Underworld Breach escape
loop (escapes ARE casts), Mizzix's Mastery overload (copies ARE cast), Peer into
the Abyss, Exsanguinate (fires when it tables), Necropotence (replaces draw,
life floor 10), Jeska's Will (+5, draw 1), Mana Geyser (flat +8), fodder casts
once per-cast damage ≥ 4.
**Omitted (conservative):** Aetherflux Reservoir laser, Lindblum's Mage Siege
adventure, Electro's leave-trigger X, copy-effect value (Bonus Round / Cerberus
/ Primal Wellspring cast as ping fodder only), Circle's +1/+0 pump.
**Optimistic (noted):** rocks tap same turn, Ruby Medallion as 1-output rock,
no opposing interaction. Trust shapes and deltas, not second decimals.

## 2. Baseline clock

```
P(kill <= T) %            T4    T5    T6    T7    T8    T9   T10   T12
decap (one opponent)       1     8    41    82    95    98    99    99
table (all three)          0     3    18    49    78    92    97    99
median decap T7 / table T8 · never-in-12: 1%
```

**Canonical line:** `Clock: T7 decap / T8 table (lab 2026-06-10, gp_clock_lab.py)`

The engine sequence that produces it: Kuja T3–4 → one token per end step
(+ producers) → transform T5–6 → storm turn T6–8 at 8–16+ damage to each
opponent per cast.

## 3. Lever test — all axes flat

2-card packages cut the goldfish-weakest slots (Ensnared by the Mara, Dance
with Calamity); 4-card probes additionally cut Overmaster and Reanimate.
Tutor axis excluded: **Gamble is a current Game Changer** (list 2026-02-09)
and the deck is capped at 3/3.

| Variant (adds) | T6 table | T7 table | T8 table | median |
|---|---|---|---|---|
| BASE | 18 | 49 | 78 | T8 |
| +pingers (Guttersnipe, Kessig Flamebreather) | 18 | 49 | 78 | T8 |
| +fastmana (Pyretic Ritual, Seething Song) | 19 | 51 | 79 | T7* |
| +draw (Wrenn's Resolve, Reckless Impulse) | 20 | **53** | 81 | T7* |
| +wizards (Dreadhorde Arcanist, Ghitu Lavarunner) | 18 | 48 | 77 | T8 |
| +draw4 (also Thrill of Possibility, Tormenting Voice) | 19 | 53 | 81 | T7* |
| +mana4 (also Desperate Ritual, Rite of Flame) | 19 | 51 | 79 | T7* |

\* median flips on a 49→51–53% knife edge — nominal, not a real turn gained.

**Why flat, per axis:**
- **Pingers:** Guttersnipe/Kessig are Shamans, not Wizards — they miss Trance
  doubling and the transform count. Per-cast damage at storm time is already
  lethal-grade; the bottleneck is *when* the storm turn arrives, not its size.
  (Firebrand Archer — the Lightning War recommendation — is an **Archer**, not
  a Wizard; it misses every multiplier here. Does not transplant.)
- **Fast mana:** an earlier Kuja still waits on end-step token cadence; rituals
  compress the storm turn that was already happening.
- **Draw:** the deck already runs 11+ draw slots and Necropotence; two more
  draw-2s add +4pp at T7. The only axis with any signal, and it's marginal.
- **Wizard bodies:** transform arrives ~1 end step earlier but the extra bodies
  displace ping/draw value — net zero on the table clock.

## 4. Judgment: can the clock be upgraded?

**No — not within bracket constraints.** The clock is bound by two structural
facts no 99-slot swap changes:

1. **Token cadence is commander-fixed.** One Wizard per end step from Kuja;
   producers supplement but cost the same main-phase mana the chain wants.
   Transform realistically lands T5–6 in every variant tested.
2. **The deck already has critical chain density.** 11 draw slots +
   Necropotence + Birgi/Storm-Kiln rebates mean the storm turn fires the turn
   after transform with ~80% reliability. Feeding it more (draw, mana, pingers)
   moves single percentage points.

What WOULD move it sits outside the deck's constraints: GC fast mana (Mana
Vault/Chrome Mox — cap full at 3/3), GC tutors (Gamble/Demonic — same), or a
different commander. Within Bracket 3 as built, **T7 decap / T8 table is this
deck's natural speed.** It is already faster to the *table* kill than most of
the roster (GD table T12+, Lightning War table T6–7 only via its 1-of-4
finisher at 22%).

**Recommendation: make no speed-motivated swaps.** The only edit with any
measured signal is optional polish, not a clock change:
- − Ensnared by the Mara, − Dance with Calamity → + Thrill of Possibility
  (owned, undeployed) + Wrenn's Resolve (~€0.50 buy): +4pp at T7 table,
  never-in-12 1%→0%. Defensible as smoothing; do not expect a faster clock.
- Both cuts are goldfish-weak but have real-game table value (Ensnared is
  political/disruptive, Dance is a haymaker). Pilot's call, not a lab mandate.

## 5. Card-text corrections found during verification

1. **Bonus Round copies are NOT cast** (explicit oracle ruling: "The copy …
   is created on the stack, so it's not 'cast.' Abilities that trigger when a
   player casts a spell … won't trigger."). The Summary's Kill Line 3 claim
   "Each copy also triggers Wizard pings" is **wrong**. Bonus Round still
   doubles spell *effects* (rituals, draw, Exsanguinate X) and **does** trigger
   Storm-Kiln Artist (magecraft counts copies). Same applies to Summon: G.F.
   Cerberus chapters II–III and Primal Wellspring copies. Underworld Breach
   escapes and Mizzix's Mastery copies ARE cast — those lines stand.
2. **Stormsplitter copies are exiled at the beginning of the next end step**
   — the Summary's pilot note omits the exile clause. They can still be counted
   for Kuja's transform check (both triggers fire at your end step; you order
   yours: count, then exile) but they do NOT persist to the next turn.
3. **City on Fire has Convoke** — with 4–6 Wizards out it costs ~2–4 real mana,
   not 8. The Summary's multiplier table omits this; it materially changes when
   the ×3 comes down (same turn as the storm, tapping tokens that don't need
   to be untapped to ping).
4. *(Bonus, minor)* Storm-Kiln Artist is a **Shaman** — Harmonic Prodigy
   doubles its Treasure trigger. Urabrask pings a **single target** opponent
   (i/s only), not each opponent — he's a mana engine here, not a table pinger.

## 6. Ownership / availability notes

- Guttersnipe: owned (≥2 spare; 1 deployed in Lightning War). Pyretic Ritual,
  Seething Song (+ spare Blazing Firesinger), Desperate Ritual, Thrill of
  Possibility: owned, undeployed. Gamble: owned but GC-blocked.
- Not owned (no reskin alias): Kessig Flamebreather, Electrostatic Field,
  Firebrand Archer, Wrenn's Resolve, Reckless Impulse, Tormenting Voice,
  Thermo-Alchemist. All ≤€1 if ever wanted; none earn a buy on these numbers.
