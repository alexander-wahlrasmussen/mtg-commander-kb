# Backlog — tooling & analysis ideas

Forward-looking ideas we want to try but haven't started. Captured 2026-06-14 (after the
`validate.py` + clock-lab-harness session). Not a commitment or a spec — a "don't forget"
list. When one is picked up it graduates to a `scripts/` tool + (if it's a clock/analysis)
an `analysis/` write-up, and its row moves to Done.

---

## ~~1. The Pod Gauntlet — simulate the matrix verdicts~~ ✅ DONE 2026-06-14

Built: `scripts/pod_gauntlet.py` + `analysis/pod_gauntlet_clocks.json` +
`campaigns/Pod_Gauntlet_2026-06-14.md`. Races each deck's measured decap clock
(harvested from the `*_clock_lab.py` suite) + disruption (`delay_lab.py` measured for
GD/Calamity/LW, matrix-class-bucketed for the rest, Abolisher swept) into `P(beat the
pod)`, with PURE RACE (fully simulated) and P(WIN) (+ disruption overlay) stated
separately. Findings: separates the race-vs-disruption axes the matrix collapsed;
race leaders are Genome/Radiation/Replication (goldfish ceilings); GD/LW swing hard on
P(Abolisher out); **flags Calamity's "Favoured" as least supported**. `--refresh`
re-harvests the curves (also seeds #2). Matrix + campaigns README updated.

## ~~2. Close the clock-claim loop — verify, don't just cite~~ ✅ DONE 2026-06-14

Built: `scripts/clock_check.py`. Reads the lab decap/table medians from
`analysis/pod_gauntlet_clocks.json` (the aggregated `{deck,decap,table,never}` JSON that
`pod_gauntlet.py --refresh` harvests from every `*_clock_lab` — the practical form of "labs
emit JSON"), parses each Summary's canonical `Kill Window / Clock:` line (clause-split on
`/`/`;`, head-cut before the citation, `(one player)` decap synonym, `(median Tn)` / open
markers), and flags any decap/table median that drifted ≥2 turns. Validated: 16/16 current
Summaries match; fabricated stale lines flag DRIFT. A WARN-level lint (`--strict` to gate);
complements `validate.py` check #4 (citation EXISTS → this checks it's TRUE), cross-linked
both ways.

## ~~3. The "one-purchase unlock" optimizer~~ ✅ DONE 2026-06-14

Built: `scripts/unlock_optimizer.py`. Automates `Build_And_Swap_Tracker.md` §4: counts demand
across the 16 active decklists + the live builds (default Hashaton + Kefka; `--build` /
`--all-considering` to change), nets out owned **+ proxy** copies (this is a proxy-friendly
collection — `--no-proxy` for real-only), and prints two reports: **over-committed** owned
cards ranked by copy deficit (reproduces §4 — Demonic Tutor short 2, Vampiric Tutor
over-committed) and **one-purchase unlock** = build-needed cards owned 0-real, shared buys
first (Go for the Throat serves both builds). Resolves reskin aliases on both sides, flags GC
contention. Limitation: pending per-deck swaps not yet in a `.txt` (the Kiki swap) aren't seen.

## ~~4. Kill-tree diagrams (the fun one)~~ ✅ DONE 2026-06-14

Built: `scripts/kill_tree.py` + `analysis/kill_trees/` (README embeds the rendered trees as
GitHub-native ` ```mermaid ` blocks; `.mmd` files alongside). Renders a deck's kill lines as a
cheapest-first decision ladder (try the fastest line; if its pieces aren't up, fall to the
next), leaves coloured combo / table-drain / combat-decap / enabler, with an always-on
background-clock lane and the lab-measured clock on every leaf. Encoded **Radiation Sickness**
and **Diminishing Returns** (5 distinct lines each); both validated+rendered via the Mermaid
Chart tool. Add a deck by encoding its lab's KILL CHECKS into `DECKS`.

---

*Source: 2026-06-14 brainstorm. Order ≈ value; #1 was the recommended first build.*
**All four shipped 2026-06-14** in one top-down grind. ✅✅✅✅

---

## 5. Plan-aware (per-deck) mulligan + front-edge oracle — TODO (raised 2026-06-16)

From the Framework Bake-Off mulligan robustness check (`analysis/Framework_Bakeoff_2026-06-16.md`,
commit f48cf26). The sim mulligan keeps on **land count only**; the 2026-06-16 "smart keep"
(`deck_sim.DECK_SIM_SMART_KEEP=1`) added a generic *"has a CMC≤3 play"* requirement and **0/16
decap/table medians moved**. User's correct critique: that's a generic proxy, not *"does the hand
advance THIS DECK'S plan."* A real mulligan is deck-specific — a combo deck keeps a piece or a
tutor; a finding-gated deck (Crystal) keeps toward its drain bomb; a ramp deck keeps lands+ramp+payoff.

**The build:** give `deck_sim`'s keep rule a per-deck **keep predicate** (key cards / enabler tags /
"progress toward the win line"). Reuse what already encodes "the plan": the `WIN_LINE` dict in
`framework_bakeoff.py` and each clock lab's KILL CHECKS / `kill_tree.py` specs. Then re-harvest the
16 clocks and re-run the bake-off.

**Do it WITH the front-edge oracle, not alone.** A plan-aware mulligan moves the **front edge**
(T5–7 assembly), not the **median** — and the bake-off scored medians, so the 2026-06-16 test was
structurally insensitive to it. But the pod's real bar is `decap by T≤7` (front edge). So pair the
plan-aware mulligan with a **front-edge oracle** (e.g. P(decap by T7) from the clock curves, which
`pod_gauntlet_clocks.json` already stores) — that's where finding-gated/combo decks and the
consistency frameworks (Disciple, BDD-consistency) could finally show signal the median oracle hides.

**Honest prior:** likely a *fidelity* upgrade that lifts finding-gated decks + maybe Disciple a bit,
**not** a verdict reversal — because it doesn't touch the bigger leak (the oracle is a solitaire
goldfish: no interaction/durability modelling → half the Conversion Check scores 0 regardless). That
interaction-overlay oracle is the deeper, separate frontier.
