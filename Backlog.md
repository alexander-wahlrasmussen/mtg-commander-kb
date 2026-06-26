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

## ~~5. Plan-aware (per-deck) mulligan + front-edge oracle~~ ✅ DONE 2026-06-16

Built: `scripts/keep_spec.py` → `analysis/keep_specs.json` (per-deck "good hand" = bottleneck
class FINDING/MANA/BOARD + land band [hand-curated, user-reviewed] + key/tutor/ramp/selection
buckets [generated from `WIN_LINE` + the bake-off tagger]); `deck_sim` plan-aware `keep_hand`
(opt-in `DECK_SIM_PLAN_KEEP=1`, installed per deck at parse; default path byte-identical);
front-edge oracle `front_edge()` + `framework_bakeoff --frontedge` / `front7` column (reads the
decap CURVE, so unlike baked `med` it's sensitive to the mulligan); `pod_gauntlet --refresh --out`
for non-destructive scratch harvests. Verified Azula/Satya text (→ reclassified Lightning War
MANA→BOARD, Replication "attack not connect"; fixed kill_tree).
**Finding:** the plan-aware mulligan is a *diagnostic*, not a speed-up. Where the tagged bottleneck
is the deck's fast line it helps the front edge (Zero-Sum +6, Dark Lord/Eldrazi +3); where it's the
WRONG line it HURTS (Radiation −9, Lorehold −4 — both dug for a *side* combo line over their real
counter-board / spirits clock). Re-tagging those two FINDING→BOARD erased the harm exactly
(Radiation 67→76 = default). Framework `front7` ρ's barely moved (≤0.03) — a fidelity upgrade, NOT a
verdict reversal (honest prior held; solitaire-goldfish leak untouched). Caveat: the sim's London
mulligan is FREE (no bottoming), so +Δ's are an upper bound. Kept plan-keep opt-in; did NOT replace
the committed harvest. Writeup: `analysis/Plan_Aware_Mulligan_2026-06-16.md`.

### (original note) Plan-aware (per-deck) mulligan + front-edge oracle — raised 2026-06-16

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

---

## ~~6. Interaction / durability overlay oracle~~ ✅ DONE 2026-06-16

The "deeper, separate frontier" #5 named — the bigger bake-off leak. The oracle was a **solitaire
goldfish**, so Interaction + Durability (half the Conversion Check, all of Disciple's `I` term) scored
**0** and no quality framework could correlate. Built the **overlay** version (user-chosen over an actual
multiplayer rules engine, which the repo's discipline forbids — "I won't fake one").

Built: `scripts/interaction_meta_lab.py` — self_meta's 4-seat roster-pod race, but a closing seat must
push its win **through the rest of the table's available answers**:
`P(stopped) = TAX · (table holds a live answer) · (1 − protect-own)`, slip a turn + decay on a stop;
earliest *effective* close wins, durability still takes the grind tail. Substrate all MEASURED + imported
(`interact` = `pg.MEASURED` delay-lab disruption; `PROTECT`, clocks, durability from
`pod_gauntlet`/`self_meta_lab`); only the **swept** `TAX` is new — no new card claims. **Null reduction
verified:** `--tax 0` reproduces `self_meta_lab` bit-for-bit. Wired a sixth oracle (`oracle_interactive`,
snapshot @ TAX=0.6) into `framework_bakeoff.py --bakeoff`.

**Finding (honest prior held to the decimal):** modelling interaction **halves CC's anti-correlation but
doesn't reverse it** — CC −0.061 (self_meta) → **−0.034** (interaction oracle), monotone toward zero
across the tax sweep (−0.065 → −0.011), while pure-clock's lead erodes (+0.426 → +0.405); the two
converge. Mechanism: the overlay **sinks the glass cannon** (Genome 15/20, the anti-CC #3 outlier, −14)
and **lifts** interaction-dense/durable high-CC decks (Dark Lord +13, Calamity/Radiation/Exiles +5–6) —
but the two **highest** CC decks (Lightning War / Grand Design, 19/20) are T14 fortresses interaction
can't make *fast*, which caps the gain. So ~half of "score ⊥ results" was the goldfish artifact; the
rest is genuine. Writeup: `analysis/Interaction_Oracle_2026-06-16.md`.

**Still open (Layer 2):** real games via `game_log.py` → `calibrate.py` to validate the tower against
reality. Everything above is Layer 1 (predicting the *simulated* outcome).

---

## ~~7. Bridge to a real rules engine~~ — EVALUATED & DECLINED 2026-06-17

The "deeper frontier" #6 named (model the judgment the solitaire goldfish can't). Use-case reframe was
sound: a learning builder's real games (L2) confound *deck quality* with *pilot skill*, so a fixed-AI
engine could decouple them — strength / play-difficulty / card-A/B independent of who's driving. Scoped a
three-instrument design (Power / Difficulty / Inclusion) on Forge, then **checked Forge — and declined.**
Coverage is NOT the blocker (Commander **99.8% incl. UB**, `sim` runs headless multiplayer AI-vs-AI); the
wall is the **AI pilot** — heuristic/untrained, competent at aggro/midrange but **weak at combo *and*
control**, i.e. this roster's core. So the tool is competent **only where you don't need it** — and for the
hard (combo/control) decks the hand-scripted `*_clock_lab.py` goldfish already beats it. An engine imports a
*weaker* judgment, not the missing one. Full record + verified Forge facts + the "if reopened" baseline:
`reference/REF_Simulation_Fidelity.md` §3–§4 (which also stands as the durable fidelity-ladder reference).

---

## 8. Deck Doctor extensions — #1 + #2 + #6 + #7 SHIPPED 2026-06-26; rest open

Forward ideas for `scripts/deck_doctor.py` (built 2026-06-25 — the one-command per-deck
health check: size · banlist · colour-identity · GC · unresolved · clock-drift · CC datum
· `--run-lab`; see `workflows/WF_Deck_Doctor.md` + [[project_deck_doctor_tool]]). Proven on
the 22-candidate sweep: caught Berta's `Hengegate Pathway` ({WU} in a {GU} deck) and
filtered the benchmark/superseded noise. The frame for every extension: **plug into the
chain without duplicating a tool we already have** (note the tool each leans on, stay DRY).

**A. New checks that drop into the per-deck pass**
1. ~~**Singleton-rule check**~~ ✅ SHIPPED 2026-06-26 — `singleton` section. `parse_deck`
   does NOT collapse dupes (it expands `qty`), and crucially it EXCLUDES the `SIDEBOARD:`
   block, so the check derives quantities from the parsed main deck (`canon_quantities`), not a
   raw re-read (which over-counted Radiation's 2 sideboard cards). Honours the two exemption
   shapes from the card's own text: "any number of cards named …" (→ ∞) and "up to N cards
   named …" (Nazgûl 9, Seven Dwarves 7 — limit enforced). First pass false-flagged 4× Nazgûl
   until the "up to N" wording was added — a worked example of read-the-card-text.
2. ~~**Ownership / buildability + buy cost**~~ ✅ SHIPPED 2026-06-26 — `buildability` section.
   Reuses `unlock_optimizer.load_owned` (alias-resolved real vs proxy) and joins on the ORACLE
   canonical name (so `Morgul-Knife`→`Shadowspear` and `Wise Mothman`→`The Wise Mothman` match —
   validated live on Radiation). Reports own N/100 (basics assumed owned), the buy list, and
   INDICATIVE dated Scryfall € (flagged, never a quote; 82% eur coverage). Contention (free vs
   locked elsewhere) explicitly deferred to `availability_check.py` — pointed to, not re-derived.
   Candidate value proven: planned-obsolescence = own 74/100, buy 26 cards ≈ €96.
3. **Consistency vitals** — chain `deck_sim.py`: keepable-hand % + the BDD `--need ramp/draw`
   count-by-target-turn ("12 ramp by T3?"). Adds the "is it consistent" axis, not just "is it legal".
4. **Combo audit** — chain `find_combos.py` (Commander Spellbook): confirm the *intended* kill line
   is present + flag **accidental** infinites. Doubles as a house-rules gate (infinites OK per
   [[project_infinites_ok_in_pod]] since 2026-06-19, but MLD / repeatable extra-turns still out).
5. **Bracket estimate** — beyond GC count, score the broader WotC-bracket signals (MLD, extra-turns,
   2-card infinites, fast-mana density). GC ≤3 is one input; this is the fuller bracket read.

**B. New modes / uses**
6. ~~**`--all` batch dashboard**~~ ✅ SHIPPED 2026-06-26 — `--all` (+ `--candidates`). Runs the
   SAME checks in quiet mode (no second code path: `Report(quiet)` suppresses prints but still
   tallies + fills a `facts` dict) and prints one `size·sing·ill·off·GC·owned/100·buy€` row per
   deck, FAIL/WARN floated up. 16-deck roster all PASS/WARN; the 38-deck `--candidates` sweep
   re-caught Berta's off-colour + the external lists' GC-cap violations.
7. ~~**`--diff old.txt new.txt`**~~ ✅ SHIPPED 2026-06-26 — swap inspector. Cards out/in (added cards
   annotated GC / off-colour / BANNED), then a boundary check off the two quiet-doctor `facts` dicts
   (size, GC>cap, newly illegal/off-colour/singleton) shown `old -> new` with NEWLY/fixed flags; verdict
   `OLD-tag -> NEW-tag`, exit 1 on any crossing. Canon-keyed (a reskin reprint isn't read as a swap; a
   commander change is called out). Clock movement is NOT inferred from two static lists (medians are
   per-slug) — prints the `--run-lab` command instead (kill-window-needs-a-lab). Validated on the real
   Replication Crisis 0504->0622 optimization (5-out/5-in, all boundaries clean) + a crafted off-colour
   swap (WARN->FAIL). **Perf:** this pass also `lru_cache`d `deck_sim.load_oracle_index` +
   `deck_doctor.load_full_index` (the 176 MB bulk was re-read per deck) — `--all` 32s -> 2.6s, helping
   every batch tool (pod_gauntlet, labs).

**C. Integration**
8. **Pre-commit / CI gate** — wire it into a hook (the docstring already advertises this) so a decklist
   edit that breaks size/legality/CI/GC can't be committed. Turns "run it when you remember" into
   "can't forget".

**Recommended first pick:** ~~#1 + #2 + #6 + #7~~ — all four shipped 2026-06-26 (singleton,
buildability/buy-€, `--all` dashboard, `--diff` swap inspector). **Still open:** #3 consistency vitals
(chain `deck_sim`), #4 combo audit (chain `find_combos`), #5 bracket estimate, #8 pre-commit/CI gate.
Next natural pick: #8 (CI gate) — wire `deck_doctor`/`validate` into a hook so a decklist edit that
breaks size/legality/singleton/GC can't be committed; or #3/#4 to add the "is it consistent / does the
intended combo line exist" axes the doctor still lacks.
