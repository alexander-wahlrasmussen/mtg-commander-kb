# Vs-Dragon Roster Lab — P(win vs the Ur-Dragon fair-board deck), all 16 decks

**2026-06-15.** Computes **P(win vs the archenemy's Ur-Dragon deck) for every active
deck**, replacing the archetype-tiered *judgment* the Pod Matchup Matrix used to carry on
this axis. Lab: `scripts/vs_dragon_roster_lab.py` (40k trials/deck). Data:
`analysis/vs_dragon_roster.json`. Relates [[project_ur_dragon_matchup]],
[[project_pod_gauntlet_findings]], [[project_self_meta_quantified]]; the single-deck Glarb
study is `analysis/Calamity_Tax_vs_Ur_Dragon_2026-06-15.md`.

## Why this lab exists

`vs_dragon_lab.py` answered one question — does **Glarb's** anti-dragon package help (A/B,
~87–89% archetype, +2–3pp package). The matrix then carried an *archetype-tiered* read of
the **rest** of the roster ("grind = bring, race = walled"). That tier table was judgment,
and the repo's #1 lesson is that un-modelled judgments drift (7 of 8 hand-estimated clocks
were falsified). This lab does the math **per deck**, and it caught two wrong guesses (below).

## The matchup (card text verified — `project_ur_dragon_matchup`)

The Ur-Dragon is `{4}{WUBRG}` 10/10 with **Eminence** (dragon spells cost `{1}` less from
the **command zone or battlefield** — discount survives the commander dying) and an
**attack trigger** that draws + cheats a permanent into play per attacking dragon. So it is
a **combat-trigger BOARD deck** — a snowballing flying army a wrath **resets** and a fog
**skips** — **not a combo with a lethal turn K to race**. Beating it is a **survival race**:
stay alive until our kill lands, and the kill must get **through a flying wall**. This
**inverts** the combo matrix.

## What's measured vs judged (same discipline as every lab)

- **MEASURED** — each deck's **kill-clock CDF** (`analysis/pod_gauntlet_clocks.json`, the
  `*_clock_lab` suite; decap, or the *table* clock for a deck that only beats dragons via a
  slow drain — Diminishing Returns); each deck's **anti-dragon toolkit** counts (wraths /
  fogs / combat-taxes / spot removal / maze / lifegain), classified from **oracle text**
  (`collection/oracle-cards.json`) and **printed per deck for audit**.
- **JUDGED** — the **kill-axis** tag (`over` = board-independent or evasive → ignores
  blockers; `combat` = needs ground attackers → walled), one verified line per deck from its
  Summary's kill line; and the Ur-Dragon **go-live / damage curve / mitigation magnitudes**
  — priors, **every one swept**.

Heuristic, not a rules engine — trust the shape and the order, not the second decimal.
`P(win)` is a **HEADS-UP goldfish ceiling** (1v1 vs the dragons; the real 4-pod number is
lower, and the glass decks suffer most).

## Result — the ranking (baseline: G={T6 20 / T7 35 / T8 30 / T9 15}, dmg 16+7/turn)

| Rank | Deck | vs Ur-Dragon | Kill axis | Why |
|---|---|---:|---|---|
| 1 | The Genome Project | **99%** | over | Wizard-token pings = direct damage; Exsanguinate |
| 2 | Radiation Sickness | **99%** | over | rad-drain / Jarad / Mindcrank / **Toxrill**; 3 wraths |
| 3 | The Calamity Tax (Glarb) | **94%** | over | Torment / Gray Merchant; 3 wraths + 3 fogs + Maze |
| 4 | The Dark Lord's Army | **86%** | over | Gray Merchant + opp-fed amass-drain; 3 wraths + Propaganda |
| 5 | Lightning War | **83%** | over (race) | burn / X-spells; **lifegain-sensitive** (→56% if dragons gain life) |
| 6 | Zero-Sum Game | **70%** | over | Abolisher-proof lifeloop; 1 wrath + 4 spot |
| 7 | Crystal Sickness | **57%** | over | drain + Mirrodin-Besieged alt-win; slow (T11) |
| 8 | The Replication Crisis | **48%** | combat | token swarm **walled**; fast enough to sometimes race go-live |
| 9 | Lorehold Spirits | **39%** | combat | spirit combat **walled**; no wrath |
| 10 | Ms. Bumbleflower | **38%** | combat | combat-steal **walled**; 3 fogs survive, can't close |
| 11 | The Exile's Return | **37%** | combat | Kiki/combat **walled**; kill must still connect |
| 12 | Curse of the Scarab | **34%** | combat | zombie alpha **walled** |
| 13 | Earthbend the Meta | **34%** | combat | lands-as-creatures combat **walled** |
| 14 | Eldrazi Stampede Chaos | **29%** | combat | big-creature combat **walled** |
| 15 | Diminishing Returns | **23%** | over (slow) | death-drain board-indep but table clock T12+ |
| 16 | The Grand Design | **14%** | combat | "96% incremental combat, ~no trample" → survives, can't close |

Numbers reproduce `analysis/vs_dragon_roster.json` exactly on re-run.

## Robustness — the ranking holds across the sweep

P(win) was swept across 9 scenarios (go-live fast/slow, hyper-aggro 22+9, grindy 12+5,
combat-thru-wall .15/.45, we-brick draw .45, dragons-gain-life race+2). The **over/combat
split and the ordering survive the whole sweep.** The one signal swing worth naming:
**Lightning War craters 83%→56% when dragons gain life** (it chases a single total), where
the drain/ping decks above it don't — a race-vs-non-race distinction, not a noise artifact.
Slow go-live lifts every combat deck (they get a longer pre-go-live window) but never enough
to cross the over decks.

## What the math changed (this is why we compute instead of judge)

Two archetype-tier guesses the matrix first carried were **wrong**, and the lab caught both:

1. **The Grand Design is the WORST deck here (14%), not a "Bring."** Its kill is *combat
   with almost no trample* (its own Summary: 96% of kills are incremental combat) — vs a
   flying wall it **survives but can't close** (the can't-close-fortress pattern from
   `self_meta`).
2. **Genome (99%) and Lightning War (83%) are NOT walled.** Pings and burn are
   *board-independent direct damage* that race **over** the wall; only the **combat** racers
   (Replication, Lorehold, Exile, Curse) get walled. "Race deck = walled" had conflated
   combat with board-independent damage.

The clean axis isn't "grind vs race" — it's **board-independent kill vs combat kill**.

## The decision

Three decks are board-independent damage that beat **both** his archetypes:

- **Radiation Sickness (99% vs dragons / #1 combo)** — the standout hedge: robust, not
  glass, top of both tables. **When the meta is unknown, bring Radiation Sickness.**
- **Genome (99% / #3)** and **Lightning War (83% / #4)** — glassier both-ways options.

**Glarb (94%) and Dark Lord (86%)** are the anti-fair **specialists** — top vs dragons but
bottom tier vs his combo (Glarb #14, Dark Lord #12). Commit them only when you're confident
he's on Ur-Dragon; they're the *worst* read if he sits down with a combo deck.

## Addendum 2026-07-05 — classifier fix, pin refresh, candidate injection

- **Oracle-index bug fixed**: textless "X // X" printings (art-series-style entries)
  could shadow the real card via the face-name index path — `otext("Infernal Grasp")`
  returned whitespace, silently deflating spot counts roster-wide (this, not reskins,
  was the main reason the counts ran low). `SPOT_RE` also widened to catch
  "destroy target permanent" / "destroy target artifact or creature" (Beast Within,
  Putrefy — both hit a dragon). Regression tests: `tests/test_vs_dragon_toolkit.py`.
- **Stale decklist pins fixed in `lock_lab.py`** (this lab imports its DECKS map):
  Replication Crisis → 20260630, Dark Lord's Army → 20260630, Croak → 20260701.
- `analysis/vs_dragon_roster.json` re-baked @40k. **The ranking and the over/combat
  split are unchanged.** Notable drift vs the table above (updated decklists, not the
  model): Lightning War 83→73% (and 56→47% under dragon-lifegain), Exile 37→42%,
  Bumbleflower 38→39%, Curse 34→32%, GD 14→20%, Earthbend 34→33%.
- **Candidate injection**: `ws_place.py --dragon` ranks the merged World Shapers
  build in this model using its COMBAT-OFF clock (axis=over) — it lands **58%, #7,
  between Zero-Sum and Crystal Sickness**, vs 33% for the Earthbend seat it retires;
  the gap holds across the full sweep. See PROP_World_Shapers_Hearthhull.md.

## Audit caveats (load-bearing)

- Toolkit counts are oracle-classified and **printed by the lab** — verify the matches.
  Culling Ritual is **excluded** (MV≤2, misses fat dragons); a couple of reskin-named
  removal spells under-resolve, so **spot counts are floors**.
- The kill-axis tag is judged per deck (from verified Summary kill lines); the dragon priors
  are judgment, swept. The kill CLOCK and the toolkit COUNTS are measured.
- Cross-check: this roster model puts Glarb at **94%**, consistent with `vs_dragon_lab.py`'s
  ~87–89% on the same deck (the standalone study).
