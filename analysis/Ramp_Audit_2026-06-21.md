# Ramp Audit — does each deck's ramp match its plan? (2026-06-21)

Tool: `scripts/ramp_audit.py` (committed). Source of the framework:
`reference_bdd_ramp_framework` memory / BDD "You're Probably Ramping Wrong"
(youtube.com/watch?v=upqHyQqN3WU). Every classification is read off oracle text +
type_line + produced_mana (`collection/oracle-cards.json`) — no card-name
pattern-matching (CLAUDE.md hard rule). Run `--cards` to eyeball the per-card calls.

**Two questions:** (a) BAND — count mana sources vs BDD's fair-deck band (~12 ramp /
~36-38 lands / ~48-50 sources); (b) TYPE vs ROLE — does the burst/repeatable split
match the deck's kill SHAPE (one-shot combo → burst OK; deploy-each-turn → repeatable),
where the role is read from each deck's measured clock (`pod_gauntlet_clocks.json`).

## Active roster

```
deck                 role lnd flx rock dork lrmp rit tre cr RAMP   b/r  src top avgC
The Genome Project   COMBO 31   6    5    3    0   3   6  1   18  6/11   54   4 2.98
Radiation Sickness   INCR  35   0    2    6    4   0   1  0   13  1/12   48   4 2.78
The Replication Cri. INCR  36   0   10    0    1   0   4  0   15  2/13   51   3 2.83
Lorehold Spirits     INCR  37   0    6    0    2   0   4  1   13  2/10   49   3 3.23
Earthbend the Meta   GRIND 32   2    4    3    6   0   3  1   17  1/15   50   4 2.91
The Exile's Return   INCR  36   1    7    1    0   2   3  0   13  2/11   50   3 2.98
Zero-Sum Game        GRIND 36   0    4    9    0   3   2  1   19  4/14   54   5 2.68
Curse of the Scarab  GRIND 35   1    7    1    0   0   3  1   12   2/9   47   6 3.16
Ms. Bumbleflower     GRIND 35   3    4    3    4   0   3  0   14  1/13   52   1 2.46
Eldrazi Stampede     GRIND 37   0    6    5    8   1   1  2   23  1/20   58  26 5.23
The Dark Lord's Army GRIND 35   1    6    0    0   1   3  0   10   3/7   46   3 2.76
Diminishing Returns  GRIND 35   1    7    2    1   1   1  0   12  1/11   48   4 2.68
Lightning War        GRIND 30   6    5    1    0   4   3  2   15   5/8   49   1 2.40
The Grand Design     GRIND 39   0    3    2    3   0   0  0    8   0/8   47   3 2.98
Crystal Sickness     GRIND 30   0   14    1    0   0   2  3   20  3/14   47   5 2.52
The Calamity Tax     MID   38   1    1    5   12   1   0  0   19  1/18   58   5 3.10
```
`src` includes MDFC flex lands (playable as lands) + mana-producing ramp; cost reducers
counted in RAMP but not in `src`. `top` = nonland payoffs cmc≥6.

## Findings

1. **Ramp TYPE already matches ROLE everywhere — zero mismatches.** Every grind/
   incremental deck is repeatable-heavy (rocks/dorks/land-ramp); the one one-shot-combo-
   shaped deck (Genome) carries burst (6 treasure + 3 ritual). No deck deploys a threat
   each turn while leaning on one-shot rituals, and no combo deck is burst-starved. BDD's
   central rule — match ramp type to kill shape — the roster already obeys. *Validation,
   not a fix list.*

2. **No deck is under-resourced.** Counting MDFC flex lands as sources, the floor is
   46-47 (Dark Lord's / Crystal / Grand Design) — in band. The first-pass "Lightning War
   under-resourced" alarm was a flex-counting bug (now fixed: LW = 30 pure + 6 MDFC + 13
   ramp = 49). Lesson baked into the tool: **MDFC flex lands are mana sources.**

3. **Four decks over-resourced (>52) — all explained by payoff profile, none is the BDD
   "over-ramped into nothing":**
   - **Eldrazi 58** — 26 payoffs cmc≥6, avg 5.23. A big-mana deck *should* run this much.
   - **Genome 54** — its "ramp" is 6 treasure + 3 ritual: storm fuel for the Kuja ping
     engine, not standing sources. Mana IS the payoff. (Clock is lever-flat anyway —
     `project_genome_project_clock_lab` — so more ramp wouldn't move it.)
   - **Zero-Sum 54** — 9 dorks feeding the lifeloop combo; redundancy. Deck near-optimal.
   - **Calamity Tax 58 / 19 ramp / 12 land-ramp** — the one that looks like over-ramp, but
     its kill (Torment of Hailfire X≥12, ~14 mana) genuinely consumes the mana AND Glarb's
     lands-matter identity makes land-ramp double as synergy. Its real problem is the clock
     (mana-gated, can't close — `project_calamity_tax_speed_analysis`), not the ramp count.

4. **The BDD "ramping toward nothing" failure mode is ABSENT.** Our low-curve decks
   (Genome 2.98, LW 2.4, Bumbleflower 2.46) ramp toward combos / X-spells / cast-chains /
   engines — targets a naive "count cmc≥6 payoffs" audit cannot see. **Methodological
   lesson: a ramp audit must read the WIN LINE, not just the curve.** The cmc≥6 proxy cried
   wolf on exactly the decks whose ramp target is an engine, so that flag was demoted to a
   data column; only the source-band and type/role flags are auto-raised.

5. **Archetype fingerprints are clean** (classifier sanity): lands-matter Glarb = land-ramp-
   heavy (Calamity 12; Glarb variants 8-12); artifact decks = rock-heavy (Crystal 14);
   elf/dork decks = dork-heavy (Zero-Sum 9, Berta 9); storm = treasure/ritual burst (Genome).

6. **Candidate-deck validation (`--considering`):** Hashaton-Thoracle, the fastest combo
   benchmark, is the LEANEST on mana (11 ramp / 41 sources / avg 2.33) — BDD's "combo decks
   build to one turn, run leaner." The framework predicts our own benchmark.

## Bottom line

The roster is well-ramped — it already follows BDD's type-matches-plan rule, and the only
"over-resourced" reads are payoff-justified. The durable output is the **method**, not a
swap list: (1) count sources vs the band with `ramp_audit.py`; (2) match ramp TYPE to kill
shape; (3) answer "ramp toward WHAT, by which turn" from the **win line**, not the curve.
Codification proposed into `REF_The_Conversion_Check.md` (Functional Baseline + a Build Rule)
and `REF_Domain_Principles.md` (the read-the-win-line lesson).
