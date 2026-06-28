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

**Status: the instrument is built, tested, and ARMED — but Layer C itself is NOT closed.** The log
holds **0 games**; with an empty log `calibrate.py` prints the armed-but-ungraded loop and exits 0.
The work that remains is *playing and logging* — the first real pod games are what finally grade
the [v2 tier list](analysis/Definitive_Tier_List_2026-06-28.md) and the whole tower. This is the
one open frontier the test-discipline anti-goals (#9) explicitly fenced off as Layer C.
