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

**Dashboard integration — 4-deck pilot (shipped 2026-06-28).** The 4 encoded kill trees
(radiation/diminishing/genome/replication) now render on their dashboard deck pages as a
hand-rolled cheapest-first LADDER (no mermaid/diagram dep — the lean-SVG ethos): `kb_content
._kill_tree` bakes the structured `KILL_TREES` registry data (reg_slug-keyed) into each deck
JSON; `DeckPage.tsx`'s `KillTree` component renders lines coloured by kind (combo/table/
combat/enabler) with the lab clock on each rung + the always-on background lane + the stall
note. Guard: `tests/test_kb_killlines.py` (hermetic shape tests). Decks without an encoded
tree simply hide the section.

**Roster completion — all 17 decks encoded (shipped 2026-06-28).** Encoded the remaining 13 trees from
each deck's `*_clock_lab.py` KILL CHECKS + its Summary's verified Kill Lines (gathered by 4 parallel
evidence-extraction agents returning verbatim lab/Summary quotes; authored from the quotes, not memory —
the read-the-card rule). Verified all 13 commanders' oracle text via the bulk first (fixed roots:
Quintorius is a planeswalker, Golbez returns-to-hand-then-drains, Sauron amasses on opp *spells* while
the punishers drain on *draws*). Sanitized mana-cost braces (`{5}{R}{R}` → `5RR`) that break Mermaid's
rhombus parser; validated representative trees (incl. the `MV<8` and `≥`/`×` ones) via the Mermaid Chart
tool = valid. Harvested decap/table medians used for the primary line, never the optimistic Summary edges.
`kill_tree.py --all` regenerates all 17 `.mmd`; the README embeds all 17 as GitHub-native blocks;
`tests/test_kb_killlines.py` now asserts 17/17 resolve with valid kinds.

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

**Spin-off — mulligan TRAINER (shipped 2026-06-28).** `scripts/mulligan_trainer.py` turns the
keep-spec into a keep/mull DRILL: deals raw 7-card hands from a chosen deck (no auto-mull — you
call it), then reveals what the plan-keep model would do + WHY (land band, which axis fired,
present key/tutor/ramp/dig cards) and scores session agreement + over-keep/over-mull coaching.
The verdict is `deck_sim.keep_hand` with the spec installed — the SAME heuristic the sim
mulligans on, so the drill can never disagree with the sim it trains against
(`tests/test_mulligan_trainer.py` pins that invariant over a 400-hand battery). Motive: it's the
one thing that turns "Layer C is blocked on real games (#10)" into *getting better at the games
I'll log* — rep on the most frequent in-game decision, needing zero games. Interactive for a human
terminal; `--auto` for non-interactive demo/CI. NOT an oracle — a documented plan-progress
heuristic ([[feedback_mulligan_is_deckbuilding_input]]); colours / on-the-play / the specific pod
are still the pilot's call.

**Dashboard drill (shipped 2026-06-28).** Brought the trainer to the static dashboard with NO
backend: `mulligan_trainer.bake_hands(slug)` bakes N=40 opening hands per deck WITH their
authoritative `keep_hand` verdict + reasons into each deck JSON (in `dashboard_export`, kept
out of the live per-request `compute_deck` path — it loads the bulk + sims). `DeckPage.tsx`'s
`MulliganDrill` deals from the baked pool, takes a keep/mull guess, reveals the model's call +
why + a running agreement score. **No client-side keep_hand re-impl → no drift** (the verdicts
are the Python authority's, baked). Guards: `tests/test_mulligan_trainer.py` adds bulk-gated
`bake_hands` shape + seed-reproducibility tests. Side-fix: regenerating `keep_specs.json` for
the bake de-staled it — it was keyed on the OLD `calamity-tax` stem (now `croak-and-dagger`) and
missing `forced-liquidation`; the CLI trainer for that deck was silently broken too. Now 17/17
decks have a drill. Note: the drill shows in the BUILT/static site (`npm run preview`); the live
dev API server intentionally skips the heavy mulligan bake (kill trees still show there).

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

## 8. Deck Doctor extensions — #1-#7 SHIPPED 2026-06-26; only #8 (CI gate) open

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
3. ~~**Consistency vitals**~~ ✅ SHIPPED 2026-06-26 — `--vitals` (opt-in, ~5s). Chains
   `deck_sim.simulate` (keepable% @8k, fixed seed) + `need_source_set`/`simulate_need` for ramp
   (BDD ~12 by T3) and draw (~8 by T6) count-by-turn. Framed as consistency not power (keepable%
   informs HOW to build, doesn't grade). `--deep` turns it on with #4. Matched deck_sim's own 98.9%.
4. ~~**Combo audit**~~ ✅ SHIPPED 2026-06-26 — `--combos` (opt-in, network). (a) network-free intended
   kill-line check vs the registry `win_line` (fuzzy-aware); (b) `find_combos.query_deck` (CSB) for
   complete + one-away combos. House-rules gate: a combo producing repeatable **extra turns** = ERROR;
   other infinites pod-accepted ([[project_infinites_ok_in_pod]]). Refactored find_combos to expose a
   reusable `query_deck`. Validated: Genome kill line present + 0 combos; Replication 2 infinite → bracket 4.
5. ~~**Bracket estimate**~~ ✅ SHIPPED 2026-06-26 — default `bracket / house rules` section. Estimates
   WotC bracket from GC + MLD + 2-card-infinite (when `--combos` ran) + fast-mana density + extra-turns,
   AND enforces the pod house rules: **MLD = ERROR** (hard exclusion, curated set + "destroy all lands"
   text backstop), >1 extra-turn = WARN (0-1 allowance, no chains). Added `MLD` + `brk` columns to `--all`
   (so the dashboard now catches a house-banned card). Caught Time Warp's "take**s** an extra turn" wording.

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
8. ~~**Pre-commit / CI gate**~~ ✅ SHIPPED 2026-06-27 — committed git hook (`hooks/pre-commit`, activated
   by `scripts/install_hooks.py` via `core.hooksPath`, NOT the heavy pre-commit framework). Targeted +
   fast: only works when relevant files are staged. Staged active `decks/*.txt` -> `deck_doctor <file>
   --no-build` per file (size · legality · colour-id · GC · singleton · MLD/house-rule) PLUS
   `validate.py --no-oracle` for the repo-wide filename-collision sweep a single-deck pass can't see;
   staged `scripts|tests/*.py` -> `pytest` (the Tier-1 suite, #9). Degrades gracefully without the
   Scryfall bulk (size+GC+collision still gate; full legality is the CI backstop). `.gitattributes`
   pins the hook to LF so it runs on macOS. Verified: blocks a 41-card decklist, passes a clean tree,
   instant-skips a docs-only commit. Bypass once with `git commit --no-verify`; CI (`repo-health.yml`)
   re-runs the same tools regardless.

**Status:** ~~#1-#8~~ **all shipped.** #1-#7 (2026-06-26): singleton, buildability/buy-€, `--all`
dashboard, `--diff` swap inspector, consistency `--vitals`, combo `--combos`, bracket/house-rule gate.
#8 (2026-06-27): the pre-commit hook — "run it when you remember" is now "can't forget" locally, with
CI as the hard backstop. The Deck Doctor extension track is complete; further testing work lives in #9.

---

## 9. Test discipline — calibrate the instruments (Tiers 1–3 SHIPPED 2026-06-27; mutation deferred by design)

The whole analytical edifice (clock labs, `deck_sim`, `deck_doctor`, the bake-off) emits numbers we
make real buy/build decisions on — but until now **zero** tests guarded the code that produces them.
That's the asymmetry: we have strict discipline for the *card-level* inputs (read-the-card, cite-the-lab,
verify-prices) and none for the *code*. And it has already failed: the colour-divide retraction, Grand
Design's "39%→89%" fetch bug, the singleton sideboard over-count were all the **same** failure — a false
red/green from an uncalibrated instrument (in TDD terms, a bug in the test framework itself). Our clock
labs *are* test-first deckbuilding; this extends the same epistemics down to the simulator.

Framing: **two layers.** Layer A = test the instrument (ordinary software testing — the gap). Layer B =
the labs themselves (deck-acceptance tests — mostly need *formalising*, not inventing). Can't trust B
until A exists. (Layer C — calibration vs real games — is out of scope; `game_log.py` → `calibrate.py`,
the L2 frontier, deliberately excluded.)

### NOW — Tier 1 (✅ SHIPPED 2026-06-27)
- `tests/` (pytest + Hypothesis), hermetic (synthetic card records, NO Scryfall bulk, no network) — 48
  tests, ~1.3s. Covers the three cores every consumer imports: `deck_sim`, `speed_lab_core`,
  `deck_registry`. Three kinds: unit, **property** (`@given` — land band, cum-monotonicity, parse
  round-trip), and **REGRESSION** (one per retracted finding: the produced-mana colour bug, the
  fetch-resolution bug, the sideboard over-count).
- Pinned `requirements.txt` (runtime) + `requirements-dev.txt` (pytest/hypothesis) — a fixed seed only
  reproduces if the libraries underneath don't move.
- New `tests` job in `repo-health.yml` (alongside link-lint + Deck Doctor). Fast gate — no bulk fetch.
- **The rule** (`tests/README.md`): every retraction earns a regression test — the code equivalent of
  `REF_Domain_Principles.md` for card-text gotchas. Stop thinking "coverage"; think "this bug is red
  forever."

### NEXT — Tier 2 (the labs as characterization tests) — ✅ SHIPPED 2026-06-27
- ~~**Golden / snapshot tests**~~ ✅ `tests/test_clock_golden.py` + `tests/golden/clock_snapshot.json`.
  Re-runs each of the 15 single-deck clock labs at its fixed module seed + a small pinned trial count
  and pins the curves **two-tier**, exactly as specced: **EXACT** — bit-for-bit vs the snapshot (the
  labs are deterministic at (seed, trials); verified hash-seed- and OS-insensitive but NOT guaranteed
  across CPython minors, so the snapshot records `_meta.python` and EXACT auto-skips on a mismatch);
  **TOLERANCE** — snapshot median within ±1 turn of the committed `analysis/pod_gauntlet_clocks.json`
  (cross-version robust), tying the cheap artifact to the numbers the Summaries cite. DRY: reuses
  `pod_gauntlet.CLOCKS` + `parse_row` (the `--refresh` machinery). `golden`-marked, needs the bulk →
  auto-skips on bulk-free machines; runs in CI's bulk-having `decks` job (pinned to py3.14 to keep EXACT
  live). Regenerate: `python tests/test_clock_golden.py --update`.
- ~~**Formalise the null-reduction differentials**~~ ✅ `tests/test_null_reduction.py`. `interaction_meta_lab
  --tax 0` reproduces `self_meta_lab`'s per-deck WIN bit-for-bit (Backlog #6, now a CI test, not a manual
  check) + asserts the overlay's own Δ is +0 everywhere. Hermetic (both labs race table CDFs, no bulk) →
  runs in the fast `tests` job. The pattern for every future overlay's null reduction.
- ~~**Contract tests** for the external APIs (CSB `find_combos`, Scryfall) with record/replay~~ ✅
  `tests/test_contract_csb.py` + `tests/fixtures/csb_find_my_combos.json`. Replays a recorded (real,
  trimmed, page-split) CSB response by monkeypatching `find_combos._post`, asserting `find_my_combos`
  parses/paginates/aggregates the four result lists correctly — offline, `contract`-marked. `--record`
  re-hits the live API so drift surfaces as a reviewable fixture diff. Scryfall's "contract" is the
  oracle-index record shape, already pinned by `helpers.py` + `test_deck_sim` (Tier 1) — not re-done here.

### THEN — Tier 3 (metamorphic + meta-check) — ✅ SHIPPED 2026-06-27 (mutation deferred by design)
- ~~**Metamorphic suite**~~ ✅ `tests/test_metamorphic.py` (hermetic, 7 relations MR-1..6 + a DST check).
  The answer to the oracle problem: assert how output must *change*, not its value. **All four named
  relations, plus more:** reorder decklist → identical (MR-1: exact at the parser, statistical-in-aggregate
  at the sim); swap a reskin alias → identical sim result (MR-2: exact); double the trials → estimate
  concentrates / CI narrows (MR-5); add a Sol Ring → clock not slower (MR-6). Added two beyond the list:
  source-set monotonicity (MR-3: A⊆B ⇒ availability ≥, exact) and add-source-copies → not slower (MR-4).
  **Layering note:** MR-6 lives at the `speed_lab_core` goldfish — the only layer that models a rock as
  *mana* (deck_sim's core treats it as a cheap spell), so that's where "Sol Ring → faster" is testable.
  A *separate bulk-gated lab* metamorphic file was considered and **dropped**: the four relations are
  calibrated hermetically on the cores every lab imports, the Tier-2 golden snapshot already pins each
  real lab's exact output, and a lab-transform harness would be invasive (labs hard-code their `DECK`
  path) and flaky (the repo's own "levers are within MC noise" finding).
- ~~**Deterministic simulation testing (DST)**~~ ✅ formalised the property, **rejected the global-seed
  refactor.** Threading one seed through every lab would churn every committed number (the labs carry
  distinct fixed seeds whose outputs are already pinned in the golden snapshot + `pod_gauntlet_clocks.json`)
  for zero replay benefit — per-component injected rng + per-lab fixed seed already make every failure
  replay exactly (git-bisectable). Pinned the invariant that makes that sufficient: `test_metamorphic.py`
  `test_goldfish_is_deterministic_for_a_fixed_seed` (same seed → same run, and the seed actually matters),
  the `speed_lab_core` companion to deck_sim's determinism test in Tier 1.
- **Mutation testing** (mutmut/cosmic-ray) — **deferred on purpose** (the backlog always flagged it
  *later*). It's the meta-check ("are the tests any good?"), not a gate. mutmut 3.x dropped native-Windows
  support (needs WSL/Linux), so rather than commit an unverified config, the turnkey how-to is documented
  in `tests/README.md` (run on demand on Linux/WSL/CI, scoped to the cores + `-m "not golden"`); no dep
  is pinned and it is intentionally NOT wired into CI. Run it when hardening a core, act on survivors.

**Out of scope / anti-goals:** no coverage-% target; do NOT unit-test the one-off `analysis/` scripts
(disposable, not load-bearing); real-game calibration stays Layer C (excluded here). Overlaps #8 — both
are CI gates; the `tests` job and the (still-open) `deck_doctor`/`validate` pre-commit hook are
complementary, not duplicates.

---

## 10. Layer C — the grading instrument (`calibrate.py` SHIPPED 2026-06-28; awaiting real games)

The frontier every prior tier deferred: nothing has back-tested the LABS against real games. The
capture end (`game_log.py` → `analysis/game_results.jsonl`) already existed; this builds the
**grading end**. `scripts/calibrate.py` reads the game log and grades, per deck and per oracle:
**CLOCK** (observed mean table/decap turn vs the lab medians → signed Δ + MAE in turns) and
**WIN-RATE** (observed win% vs ANTI-POD / SELF / INTER P(win) → tie-aware Spearman, reusing
`framework_bakeoff.spearman`). DRY: predictions come straight from the `tier_list.py` axes (the
same oracles the v2 tier list ranks on); heavy oracle loads are lazy so the pure aggregation
helpers stay hermetically unit-tested (`tests/test_calibrate.py`, 10 tests, + a synthetic
`tests/fixtures/calibrate_synthetic.jsonl`). Honest by construction: every per-deck stat carries
its `n`; decks below `--min-games` are shown but excluded from MAE/Spearman; Spearman needs n≥3
decks. **It is the same question as the Framework Bake-Off — does the number predict the result? —
but graded against REALITY instead of the sim's own outcome oracle.**

**Wired into the bake-off too:** `framework_bakeoff.py --bakeoff` now grades every framework
(Conversion Check, Disciple, BDD, WotC, pure-clock) against a **seventh oracle — REAL** (observed
win% via `real_win_oracle`, reusing `calibrate.observed_stats`), alongside the six sim oracles. It's
the only oracle NOT semi-circular with the clock, so it's the true framework test. `--real-min N`
sets the per-deck floor, `--real-log` points at an alternate log; '—' until ≥3 decks clear the
floor. Guarded by `tests/test_bakeoff_real_oracle.py` (hermetic — bakeoff loads the 168 MB index
lazily). This finally lets the Bake-Off answer *does the number predict the result?* against
**reality**, not just the sim's own outcome oracle.

**The logging target (`calibrate.py --power`):** a Monte-Carlo power analysis that needs **no games**
— it takes the committed ANTI-POD oracle as the assumed truth and asks how many i.i.d. games/deck
until the observed-win% ranking recovers it. Answer at detect ρ≥0.5: **~5 games/deck (~80 total)**
gets ≥80% recovery; below that the REAL column is small-sample noise (the 3-deck fixture hitting
ρ=±1 is exactly that). An OPTIMISTIC floor — pilot variance / meta drift push it up. So the concrete
ask is "log ~5+ games per deck," not "log a couple and trust the number."

**Status: the instruments are built, tested, and ARMED — but Layer C itself is NOT closed.** The log
holds **0 games**; with an empty log `calibrate.py` and the bake-off's REAL column both print the
armed-but-ungraded loop. The work that remains is *playing and logging* — the first real pod games
are what finally grade the [v2 tier list](analysis/Definitive_Tier_List_2026-06-28.md), every
framework, and the whole tower. This is the one open frontier the test-discipline anti-goals (#9)
explicitly fenced off as Layer C.

**Capture friction removed (2026-07-01).** The reason an armed loop sat at 0 games was *capture
friction* (details fade before you're at the desk) + *no payoff on game #1* (`calibrate` needs
n≥3/deck). Both closed, so the only thing left really is playing: (1) `game_log.py quick` — a
one-line, non-interactive shorthand (`quick "genome W T9 d8 combo | ur_dragon L | kinnan L"`,
prefix-matched decks) typeable straight from a scorecard; (2) an **instant grade card** printed
after *every* append (`log`/`add`/`quick`) — grades this one game's table/decap clock against the
harvested lab median for the deck, from game one, with the FAST/SLOW sign read; (3)
`workflows/WF_Game_Logging.md` — the pocket scorecard + grammar + the `--power` target (~5
games/deck ≈ 80). Side-win: `tests/test_game_log.py` (25 hermetic tests) closes the gap where the
Layer-C *capture* end had no tests despite being the source of every number `calibrate` grades.

---

## 11. All-finishers clock — race every kill line, not just the goldfish (raised 2026-06-28)

**The gap.** Every tournament instrument (`pod_gauntlet.py`, `pod_championship.py`, `self_meta_lab.py`,
and the dashboard via `dashboard_server.compute_*`) represents each deck as **one** harvested curve —
a single `decap` CDF + a single `table` CDF in `pod_gauntlet.CLOCK`, with `--strict` just toggling which
of the two is read. That curve is the deck's *strict-goldfish race* from 40 life. A deck's other kill
lines — combo, cross-table chip, graveyard storm — are flattened out *before* they reach the sim. The
canonical casualty is **Lightning War**: its primary/fastest table kill is the Reiterate + Seething Song
infinite (`lw_combo_lab.py`, CAST median ~T9), but the gauntlet only sees `lw_clock_lab`'s race goldfish
(`table >T14`). The harvested oracle even tags it: `pod_gauntlet_clocks.json` LW `src` reads
"strict goldfish; **chip/combo not in this clock**." So LW's tier (C→D, anti-pod 49→33) is scored on the
one axis it's worst at, and its real fastest line is invisible to the whole tower. This affects any deck
whose fastest line isn't a combat race (LW today; latent for Diminishing/Replication/Croak combo lines).

**The subtle trap (read before building).** The naive "sample each line's kill turn independently, take
the earliest" is **wrong** and would inflate every deck — the lines are not independent draws, they share
one opening hand and one library. Min-over-N-independent-CDFs is keeping the best of N god-draws, i.e. the
exact optimistic-clock disease the kill-window sweep already falsified five times ([[project_framework_clock_gap]],
[[project_kill_window_lab_sweep]]). The correct combination takes the min over lines **on the same simulated
game**, not across independent labs.

### MVP — "best-line" harvest, tournament untouched (~the 80%) — ✅ SHIPPED 2026-06-28
Push the min **down into the per-deck goldfish**: have each deck's `speed_lab` / `*_clock_lab` track every
kill line it knows on the *same* simulated game (LW already runs both a race and a combo lab — unify them so
the min is taken on correlated draws) and report "earliest decap/table by **any** surviving line." Then the
harvest into `pod_gauntlet_clocks.json` still emits **one** `(decap, table)` pair per deck — but it now means
"fastest of all lines" instead of "race only." **Nothing in `pod_gauntlet` / `championship` / the dashboard
changes** — they keep consuming one curve; the curve just stops lying. Result: LW's ~T9 combo finally shows
up in the gauntlet and the tier list. Cost: unify LW's two labs + re-harvest; bounded, days not weeks.
Guard: a golden snapshot delta (#9 Tier-2) so the re-harvest is reviewable, and the per-line CDFs stay
lab-backed (never hand-assumed — the cite-the-lab rule).

**Built:** `lw_clock_lab.py --mode bestline` — races the burn goldfish (`goldfish_kill`) AND the
Reiterate/Seething Song combo (`lw_combo_lab.assembly_turn`) on **one** shuffled game (a shared pre-rolled
opening hand + library injected into both via a new `g=` param) and reports the earliest decap/table by
either line. The min is over **correlated draws on one game**, never over two labs' independent CDFs — the
optimistic-clock trap the brief flagged (a brick hand bricks the min). Repointed the harvest pointer
(`deck_registry` + `pod_gauntlet.CLOCKS` lightning_war `lab` → `bestline`) and re-harvested LW @8k:
**decap T10→T8, table >T14→T9** (`pod_gauntlet_clocks.json`). Side-fix: `lw_combo_lab`'s tutor picks were
iterating a *set* (PYTHONHASHSEED-dependent) — sorted them so the lab is reproducible and the golden EXACT
tier holds across hash seeds. Guards green: golden snapshot regenerated (LW-only delta, EXACT+TOLERANCE pass
under two hash seeds), `clock_check` + `deck_doctor lightning_war` OK, fast test gate (101) + full golden (33)
pass. Propagated to the LW Summary Kill Window + the matrix LW row. **Effect:** the live gauntlet ranks LW #4
(was bottom on the race axis) and `tier_list.py` lifts it to **S-tier #2** (was ~11–12) — exactly the
LW-shaped distortion the brief named.

**Follow-up (NOT in this MVP, own commit) — ✅ DONE 2026-06-28 (`399ca4c`):** re-baked the *committed*
`analysis/Definitive_Tier_List_2026-06-28.md` writeup (LW D #14 → S #2; LW reframed as the cautionary
score⊥results FLIP — the race-only clock lied, not CC) + the baked dashboard JSON (`dashboard_export.py` →
both `dashboard/data` + `ui/public/data`) so they match the live tools. Guard: `tests/test_tier_list.py`
contract green; baked tierlist matches live `tier_list.py` (LW S #2, COMP 75).

### Proper version — a finisher-mixture tournament (the rest)
Make "all finishers" first-class. Each deck carries a **list** of finisher records
`{line_id, kind (combo/race/chip/storm), decap_cdf, table_cdf, enablers, disablers}` instead of one curve;
the sim resolves a game by applying pod state to each line and taking the earliest *viable* close. This is
where the lines that the goldfish can't see get to count *and* get to be switched off: graveyard hate
disables the storm line, a near-40 table disables chip, counters tax the race but not the on-your-turn combo
([[feedback_interaction_role_protect_vs_disrupt]]). It reuses the disruption/lock layer the gauntlet already
has — the new part is the per-line enabler/disabler vector. Two real costs: (a) **roster-wide coverage** —
only LW has a combo lab today; every deck's secondary lines must be enumerated + labbed to the common schema,
with card text verified first (the read-the-card rule), or the model degrades to race-only *unevenly* and
just relocates the bias; (b) **calibration** — adding lines makes every deck look faster, so it's only real
if back-tested via `calibrate.py` against logged games (#10) + golden tests so a re-bake can't drift silently.

**Honest prior:** the MVP is mostly correct and cheap and fixes the LW-shaped distortion now; the proper
version is the principled answer but is gated on the same thing as #10 — the per-line labs and real games
to prove the mixture isn't just a faster fiction. Do the MVP first; let logged games decide whether the
mixture earns its complexity.

**Coverage audit — cost (a) is already paid (2026-06-28, `analysis/Finisher_Coverage_Map_2026-06-28.md`).**
"Coverage first" turned up a clean **negative result**: every active deck's harvested clock already comes
from a **multi-line best-line goldfish** that takes the earliest decap/table across all of that deck's kill
lines on ONE correlated game — the exact "min over correlated draws, never independent CDFs" discipline this
brief demands. The backlog's worry ("only LW has a combo lab") conflated *has a separate combo-lab file* with
*models the combo line*: every clock lab folds its deck's combo/storm/drain lines into its kill checks
(verified by lab inspection — `dr` Gravecrawler `kill_all`, `rc` Lightning Runner `lr_infinite`, `ct`
X-drain/Rite/reanim, `rs` Mindcrank+Bloodchief `kill_all`, `lor` Reveillark loop `kill_all`, `gp` City-on-Fire
×3, `wb` lifeloop). **LW was the sole true gap** (two *separate* labs, one harvested) — fixed by the MVP. The
only other active decks with a separate secondary lab resolve cleanly: **Grand Design** `gd_combo_lab` evaluates
a *proposed* combo whose pieces (Viscera Seer + Zulaport) are **not in the committed deck**, so there is no
board-independent line to miss; **Zero-Sum** `wb_storm_lab`/`wb_raid_lab` model *slower* backup axes, while the
harvested `wb_clock_lab` already models the fastest (lifeloop). So there is **no roster-wide labbing gap and no
common-schema build to do** — the per-line MIN already exists per-deck. The genuine remaining delta of the
proper version is **only** the part the audit shows is still missing: making each line **first-class and
switchable** (the enabler/**disabler** vector) so pod state can disable a line — which requires the labs to
**emit per-line CDFs separately** (today they collapse to one blended curve that can't be switched off
component-wise). That refactor collapses into the **same gate as cost (b)/#10**: it only earns its complexity
once logged real games can validate the switched mixture. Net: #11's remaining scope = the disabler-vector
refactor, gated on #10 (0 games logged) — not a coverage build.

**Disabler-vector pilot — SHIPPED 2026-06-28 (`analysis/Finisher_Mixture_Pilot_2026-06-28.md`).**
Built the switchable-line capability the audit isolated as the one genuinely-missing piece. (1)
`lw_clock_lab.perline_kill` — the per-line primitive: races LW's burn + combo lines on ONE shared
game and returns each line's `(decap,table)` separately; `bestline_kill` is now the min wrapper, so
the harvested curve + golden snapshot are **byte-identical** (golden EXACT/tolerance green). (2)
`scripts/finisher_mixture.py` + `analysis/finisher_lines.json` (schema: per deck `{grid, split,
lines:[{line_id,kind,decap,table,med,never,disablers,note}], bestline_check}`) — reads lines
separately, applies a pod-state **disabler vector**, reports the earliest VIABLE close over the
surviving lines. **Load-bearing safety property: the vector only ever REMOVES lines, so the mixture
is bounded ABOVE by the harvested best-line curve** — degradation, never a faster fiction (defuses
the "every deck looks faster" worry by construction). **Null reduction (exact):** mixture{} ==
harvested curve bit-for-bit (LW `bestline_check` @8k == `pod_gauntlet_clocks.json` LW). LW demo, all
card-grounded: `{}`→T8/T9; `{graveyard_hate}`→**unchanged** (both LW lines assemble from hand);
`{rule_of_law}`→**never** (one-noncreature-spell lock kills both multi-spell lines). Guards:
`tests/test_finisher_mixture.py` (hermetic engine tests in the fast gate + golden real-LW null
reduction); fast gate (108) + golden (33) + clock_check (0 DRIFT) + deck_doctor LW all green. **NOT
baked into tier list / gauntlet** — a separate consumer, exactly as the MVP left the tournament
untouched. Only LW is `split`; every other deck is a single pass-through line. UNCALIBRATED: the
disabler tags are oracle-grounded but not back-tested on win-rate. **Roster-wide split + calibration
remain gated on #10** (priority gy-dependent decks to split next: Genome / Diminishing / Radiation).

---

## ~~12. Lab `--deck` override — variant comparison as first-class~~ ✅ DONE 2026-07-01

**The gap (surfaced closing Winota 2026-07-01).** Each `*_clock_lab.py` hard-pins one dated
decklist in its `DECK` constant (correct — the pin is the version record, see
[[project_lab_decklist_staleness_audit]]), but there was **no way to run the same kill model against a
variant** (owned vs no-new-purchase vs external baseline) without monkeypatching `mod.DECK` in a
throwaway `python -c` driver — which is exactly what the 3-way Winota comparison needed.

**Shipped:** `speed_lab_core.run_cli` now takes `--deck PATH|stem` (resolved by
`resolve_deck_arg` — a path, or a fuzzy stem matched newest under `decks/**`, so
`decks/considering/` variants resolve). A mode **opts in** by declaring a `deck=None` parameter and
using `deck or DECK`; run_cli passes the override only to such modes (signature introspection) and
**errors loudly** if `--deck` is handed to a mode without it — no silent no-op. Backward compatible:
every existing lab's modes lack the param, so the old call path is untouched and golden snapshots are
byte-identical. Wired into `cass_clock_lab` (both modes) as the worked example;
`clock_lab_template.py` documents the pattern (step 5). Other labs opt in trivially when a variant
comparison comes up. Fast + golden gates green.

---

## 13. Measure the pod — the last hand-estimated clock (Phase 0 SHIPPED 2026-07-02)

Every ANTI-POD number races `pod_gauntlet.K_DIST` ("wins T6-7", mean T6.70) — a
**hand-assumed** distribution, in a repo whose deepest learning is that hand-estimated kill
windows were falsified 7-of-8 times when labbed. We applied read-the-card/lab-the-clock
discipline to all 17 of our decks and never to the four decks everything races against.
Phased, lab-before-building style: **(0)** sensitivity sweep — does the assumption even
matter? **(1)** reconstruct the pod's decks from observed cards (hard constraints) +
archetype-typical fill, every card verified, flagged PROXY — never citation-grade. **(2)**
clock-lab the reconstructions on the same harness → replace the point assumption with a
measured distribution (median, variance, god-draw tail) + honest uncertainty bands.

**Phase 0 — ✅ SHIPPED 2026-07-02** (`scripts/pod_clock_sensitivity.py` +
`analysis/Pod_Clock_Sensitivity_2026-07-02.md` + hermetic tests). Sweeps K_DIST δ∈{−2…+2}
(mean T4.7→T8.7) + the two preset shapes; ONLY the anti-pod axis moves (INTER/SELF are
pod-profile-independent, held at baseline → attribution by construction); min-max norm
cancels uniform shifts so tier flips are real differential sensitivity. Noise yardstick
0.4pp. **Finding: 11 ROBUST · 2 EDGE · 4 SENSITIVE of 17.** The S-tier picks and D floor
survive any plausible pod clock; the load-bearing region is the middle band (Exile's A needs
the pod NOT faster than assumed; Lorehold's B flips on the fast *shape* alone; Bumbleflower
underrated if slower; DLA drops to D if faster) — and ALL absolute P(beat pod) levels
(Genome 15→94% across the sweep; ranking ρ≥0.975 but the *levels* inherit the full
uncertainty). **Verdict: Phases 1–2 justified, targeted at the middle band + absolute
levels.** Caveat carried: disruption rows clamp outside K∈{6,7} → measured sensitivity is a
mild floor.

**Phase 1 — ✅ DONE 2026-07-02.** Recon (`scripts/fetch_archidekt.py` → `opponents/`, merge
5d82dbd): H&K found ("You get a clone", real 2023 list), Ur-Dragon 72/100 + Henzie 67/100
(lands-only PROXY fills, cbaff2a), Acererak fully reconstructed from user testimony +
verified mechanics (1aa5755, rev 2 28ca343 promoted the infinite to OBSERVED). Observed
rotation (user): Ur-Dragon + Acererak EVERY meetup, H&K occasional (stomps), Henzie once.

**Phase 2 — ✅ LAB SWEEP DONE 2026-07-02 (4/4)** (`scripts/opponent_labs/`, running doc
`analysis/Opponent_Clock_Labs_2026-07-02.md`; merges 3e3959d/62fb7d7/7b6d269). Measured
decap medians: Acererak infinite >T14 (nv70%, LEAN 94..FAT 47 band) · Ur-Dragon T8
(unblocked ceiling, never 1%) · H&K T8 (real T5-6 edge) · Henzie T11. **Assumed K_DIST
(mean T6.70) is ~1-1.5 turns too fast for the stable, and the Abolisher framing is wrong
for BOTH current combo decks (mono-B + UB can't cast it).**

**Phase 2.5 — ✅ DONE 2026-07-02: Acererak lab (v2 → v3 correction).** v2 all-lines on the
mid-power reconstruction measured Acererak as slow (nv59%) — but the USER PUSHED BACK ("his
Acererak is NOT slow") and was RIGHT. `find_combos` on that list showed it one card short of ~a
dozen aristocrats infinites (it already ran the sac+drain shell). **v3 CORRECTION**: re-tuned the
reconstruction to a real combo deck (REV3: +Gravecrawler/Reassembling Skeleton/Mikaeus/Nim
Deathmantle, +Heartless Summoning→Acererak={B}, +tutors; 18 CSB complete infinites) + added a
first-class ARISTOCRATS sac-loop kill line to `opp_acererak_lab` → **decap median T12, nv28%, real
T6-8 front edge** (was >T14). NOT slow — a combo deck; T12 is a FLOOR (goldfish keeps on lands).
LESSON: a "mid-power to match the felt clock" reconstruction is CIRCULAR — always `find_combos` an
opponent reconstruction before trusting its clock. Writeup: `Opponent_Clock_Labs_2026-07-02.md` §1
v3 CORRECTION. Original spec (provenance):

**Phase 2.5 spec: Acererak lab v2, all-lines best-line (the user's challenge: "his
version is stronger" — and our own #11 discipline agrees).** The v1 lab measures ONLY the
tight net-0 infinite; that is the SAME single-line distortion that mis-tiered Lightning War
(race-only clock, combo invisible — see #11). Four real kill axes are invisible in v1, and
the "conservative" mana omissions are NOT second-order for this deck:
  (a) BIG-MANA DRAIN TURNS — Cabal Coffers + Urborg + Crypt Ghast + Dark Ritual; with
      Bontu's Monument out, casts/turn = floor(B-mana / reduced cost) drains EACH opponent
      per cast: table −12ish per turn with NO Colossus/Altar/net-0 needed. Model Coffers/
      Urborg/Ghast as swamp-scaling mana, count drains — the infinite becomes the limit case.
  (b) X-BURSTS — Torment of Hailfire / Gray Merchant devotion off the same big mana.
  (c) SHEPHERD OF ROT — table −(zombie count) per tap once Colossus tokens accumulate.
  (d) GRAVECRAWLER LEVER — excluded as unobserved, but Gravecrawler+Colossus+Phyrexian
      Altar is a famous 3-piece infinite needing ZERO reducers; "repeat casting & saccing"
      eyewitness matches it. ASK the user / watch for it next meetup; run as a lever.
  Build: race attrition + bursts + infinite on ONE correlated game (min over lines on the
  same draws — the #11 MVP rule, never independent CDFs). Expect the front edge to pull in
  toward the felt T6-7; if it still doesn't reach, the felt clock is memory-bias — one real
  observation settles it. Keep v1's bottleneck census (kill-on-sight list stays valid).

**Phase 3 — ✅ DONE 2026-07-02: the K_DIST rebuild.** Shipped: `pg.set_profile(True)` /
`--measured` / `POD_MEASURED_PROFILE=1` swaps in the four measured opponents (Acererak v2 /
Ur-Dragon / H&K / Henzie), each with its own lab-derived kdist (`opp_kdist`, never-mass on a
`NEVER_K` sentinel), user-confirmed rotation weights (.40/.30/.20/.10), and no-Abolisher
disruption; 5C-tail retired. Default byte-identical (null-reduction: `tests/test_pod_measured_
profile.py`); goldens untouched. `pod_clock_sensitivity.py` prints "AT THE MEASURED PROFILE":
**ρ=0.973, 7/17 tiers move** (middle band lifts: FL B→A, Bumbleflower/CoS/EBM C→B, GD/Eldrazi
D→C; Zero-Sum A→B). Ur-Dragon uses unblocked decap T8 directly (user's call). Housekeeping: the
committed tier-list doc refreshed to live (Croak D→A, FL A→B); dashboard tierlist.json verified
already-current. **The blend HIDES H&K** — play to beat H&K, not the Acererak mirage. Writeup:
`analysis/Pod_Measured_Profile_2026-07-02.md`. Measured profile is OPT-IN (PROXY + Acererak
memory-bias flagged), not the committed default. Original spec (provenance):

**Phase 3 spec: the K_DIST rebuild.** Fold the measured curves into `pod_gauntlet` as an OPT-IN
measured profile; default path byte-identical (null-reduction test, the finisher_mixture pattern):
  1. PER-OPPONENT kdists — replace the single global K_DIST: each OPPONENTS entry carries
     its own measured attempt curve (Acererak: v2 best-line; H&K: decap; Ur-Dragon: decap
     with an explicit unblocked-ceiling caveat — decide whether to haircut via vs_dragon's
     defended view, or model UD as pressure-not-K; Henzie: decap). Sample K per-opponent.
  2. WEIGHTS from the observed rotation (UD + Acererak every meetup ≫ H&K ≫ Henzie);
     retire/demote the 5C-tail entry (Kenrith/Kinnan unseen); user confirms splits.
  3. disruption_a stays per-opponent and gets BETTER: no current deck can cast Abolisher —
     the a≈0.15-0.30 sweep may be obsolete vs this stable; re-derive from the lists.
  4. Guards: fast gate + a null-reduction test (measured-profile OFF ⇒ bit-identical);
     goldens untouched (opponent labs are outside the harvest chain by design).
  5. Re-run `pod_clock_sensitivity.py` AT the measured profile → which middle-band tiers
     move (expect lifts per the +1/+2 sweep columns); write up + update the tier list.
  6. Housekeeping folded in: the committed `Definitive_Tier_List_2026-06-28.md` + dashboard
     are STALE vs HEAD (Croak promotion, FL A→B, RS fixes) — one rebake after (5).
  Standing refinement: log his actual kill/attempt turns at the next meetup (pocket
  scorecard next to `game_log.py quick`) — real observations grade all four PROXY clocks.
