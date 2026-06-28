# Finisher Coverage Map — Backlog #11 "proper version" prerequisite (a)

**Date:** 2026-06-28
**Question:** Backlog #11's "proper version" (a finisher-mixture tournament) names two costs.
Cost **(a) roster-wide coverage**: *"only LW has a combo lab today; every deck's secondary
lines must be enumerated + labbed to the common schema, or the model degrades to race-only
unevenly and just relocates the bias."* This doc is that enumeration — the audit that decides
how much labbing the proper version actually needs.

**Verdict: cost (a) is already paid.** On inspection, **every active deck's harvested clock
already comes from a multi-line best-line goldfish** that takes the *earliest decap/table across
all of that deck's kill lines* (combat, combo, storm, drain) on **one correlated simulated game**
— the exact "min over correlated draws on one game, never over independent CDFs" discipline the
#11 brief demands. **Lightning War was the sole exception**, because its two lines lived in two
*separate* labs and only the burn lab was harvested; the #11 MVP (`lw_clock_lab --mode bestline`)
fixed it. There is **no roster-wide labbing gap** — no 15-secondary-lab build to do.

---

## How the question was framed (and why the obvious framing is wrong)

The wrong question is "which decks have a combo?" (7 of 16 do). The right question is the LW
pathology: **which decks' *harvested* lab models a SLOWER line than a FASTER line that lives in a
separate, un-harvested lab (or no lab at all)?** That — not "has a combo" — is what made LW's tier
wrong (D→S once fixed).

The clock labs were never naive combat races. Each was hand-authored deck-by-deck to model that
deck's *actual* kill lines and return the earliest. So the audit reduces to two checks:

1. **Combo-bearing decks** — does the deck's single clock lab fold the combo into its kill checks
   (so the harvested curve already takes the min over lines)? → verified by reading the lab.
2. **Decks with a *separate* lab file** beyond their one clock lab — is that separate line faster
   than the harvested clock, and un-harvested? (This is literally the LW shape.) Only **three**
   active decks have a separate secondary lab: LW, Grand Design, Zero-Sum.

---

## Per-deck audit

### Combo folded into the harvested clock (verified by lab inspection)

| Deck | Harvested lab (decap/table) | Combo / non-combat lines folded in? | Evidence |
|---|---|---|---|
| **Diminishing Returns** | `dr_clock_lab` T9 / >T14 | **Yes** — Gravecrawler + Phyrexian Altar infinite is a `kill_all` check, alongside drain-volume + combat. >T14 table = honest low assembly rate, *not* a missing line. | docstring "INFINITE: … ends the game (kill_all)"; the loop is one of the lab's kill checks |
| **Replication Crisis** | `rc_speed_lab` T7 / T10 | **Yes** — Satya+**Lightning Runner** infinite (`lr_infinite()` → `dmg=[40,40,40]`, energy bank), Sword+AA infinite combats, Brudiclad conversion, Adeline alpha — all in one goldfish. The 2026-06-22 fastest infinite (Lightning Runner) **is** in the clock mode, not just `avail`. | rc_speed_lab.py L219-230, 368-409, 448 |
| **Croak and Dagger** | `ct_speed_lab` T10 / T10 | **Yes** — X-drain (Torment/Exsanguinate), Rite-of-Replication copy on Gray/Kokusho, reanimator, Jarad, combat — all modelled together, earliest wins. | ct_speed_lab.py docstring "Kill lines modelled: X-DRAIN / COPY / REANIM / JARAD / COMBAT" |
| **Genome Project** | `gp_clock_lab` T7 / T8 | **Yes** — City-on-Fire ×3 oneshot multiplier + Trance + graveyard recast (Underworld Breach / Mizzix's Mastery) folded into the Wizard ping; decap/table converge by construction. | gp_clock_lab.py docstring damage model (`city3`) |
| **Radiation Sickness** | `rs_clock_lab` T7 / T10 | **Yes** — Mindcrank+Bloodchief infinite (`kill_all`) + Simic Ascendancy (`kill_all`) + go-wide combat + rad drain. Lab itself states *"76% incidental go-wide COMBAT, only ~14% the kill_all combo/Simic."* | rs_clock_lab.py L10, L16-19, L250-251 |
| **Lorehold Spirits** | `lor_clock_lab` T8 / T10 | **Yes** — Reveillark + Karmic Guide + Goblin Bombardment loop is a `kill_all` (`combo_ready`), alongside spirits/Quintorius board + Moonshaker. | lor_clock_lab.py L11-12, L73, L105-106 |
| **Lightning War** | `lw_clock_lab --mode bestline` T8 / T9 | **Yes — fixed by #11 MVP.** Burn race + Reiterate/Seething Song combo raced on ONE shared game (`bestline_kill`, `_goldfish_from`). | the MVP itself |
| **Forced Liquidation** | `kfk_clock_lab` T8 / T9 | **Yes (and the secondary is correctly excluded as irrelevant).** Harvested clock models the Notion Thief + Psychosis Crawler wheel kill; the Displacer Kitten + Aether Channeler backup combo is ~1% by T12 — never beats the burn, so folding it in would not move the curve. | deck_registry win_line + kfk_clock_lab |

### Pure combat / finisher — harvested clock IS the fastest line (no separate lab, no faster documented line)

Earthbend the Meta (`ebm`), The Exile's Return (`er`), Curse of the Scarab (`cos`),
Ms. Bumbleflower (`bmf`), Eldrazi Stampede (`esc`), The Dark Lord's Army (`dla`),
Crystal Sickness (`cs`). Each `win_line` is its combat/finisher line; none has a separate
combo/storm lab; none has a documented faster non-combat line. Covered by construction.

### Decks with a SEPARATE secondary lab — the only LW-shaped candidates, all resolved

| Deck | Separate lab | Resolved? |
|---|---|---|
| **Lightning War** | `lw_combo_lab` | **Unified** into `--mode bestline` (the #11 MVP). |
| **Grand Design** | `gd_combo_lab` | **Not a real line.** The lab evaluates a *proposed* board-independent drain combo (Karmic Guide + Reveillark + **Viscera Seer + Zulaport Cutthroat**). Viscera Seer and Zulaport are **not in the committed deck** (`the-grand-design-20260623.txt`); Karmic Guide + Reveillark alone don't loop without a free sac outlet. So the committed deck has **no** board-independent combo — the harvested `gd_clock_lab` (Finale + combat) is the real fastest line. `gd_combo_lab` is a proposal-evaluation lab, not a current-deck line. |
| **Zero-Sum Game** | `wb_storm_lab`, `wb_raid_lab` | **Harvested clock is already the fastest.** `wb_clock_lab` (harvested, T9/T9) models the **lifeloop** (Exquisite Blood + vito-half), which is the *fastest, commander-independent* line. `wb_storm_lab` isolates the **slower**, commander-*dependent* affinity-storm backup (a resilience axis), and `wb_raid_lab` was a falsified speed lever. The separate labs model *slower* lines by design. |

---

## What this means for Backlog #11's "proper version"

The backlog's honest prior said the proper version is gated on **(a) coverage** and **(b)
calibration**. This audit retires (a): the per-line MIN — "race every kill line, not just the
goldfish" — **already exists at the per-deck goldfish layer for all 16 decks.** The backlog's
worry ("only LW has a combo lab") conflated *"has a separate combo-lab file"* with *"models the
combo line"* — every clock lab models its deck's combo line inline.

So the genuine remaining delta of the "proper version" is **not** the per-line min (done). It is
the part the audit shows is still missing: making each line **first-class and switchable** so pod
state can selectively **disable** it — graveyard hate switches off a storm/recursion line, a
near-40 table switches off chip, counters tax the race but not the on-your-turn combo
([[feedback_interaction_role_protect_vs_disrupt]]). A single blended CDF (what the harvest emits
today) **cannot** be switched off component-wise; the labs would have to **emit their per-line
CDFs separately** for the tournament to disable one. That refactor + the enabler/disabler vector
is the real engineering, and it is gated on **(b) calibration** (real games, Backlog #10, log
currently holds 0) — adding switchable lines makes decks look faster/slower under different pod
states, only validated against logged outcomes. Per the honest prior: do not build the mixture as
a faster fiction; let logged games decide whether the per-line disabler vector earns its
complexity.

**Bottom line:** coverage-first is done. There is no labbing backlog. #11's remaining scope is the
disabler-vector refactor, which collapses into the same gate as #10.
