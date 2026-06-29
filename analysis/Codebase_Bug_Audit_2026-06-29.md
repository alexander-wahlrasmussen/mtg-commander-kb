
# Codebase Bug Audit — MTG Commander KB

**Date:** 2026-06-29
**Method:** 23 reviewer agents (one per file cluster, all ~80 scripts + tests). Each
finding independently reproduced by a verifier running the actual code (refute-by-default),
then a completeness critic. **38 bugs confirmed, 17 rejected as false positives.**
Baseline: 0 syntax errors, 119/119 fast tests green.

Two themes dominate: a **critical sim that models a deck without its commander**, and a
**stale-identifier sweep** from the Calamity→Croak rename and the Hashaton-Thoracle drop.

**Status (2026-06-29):** ✅ **COMPLETE.** All 38 confirmed bugs are resolved or consciously
deferred (2 escalated rules-nits documented-accepted in-code; 1 flagged item resolved as
intended; 1 maintainer-call left as-is). Worked in four tiers across the session — safe cluster
(crashes/stale-config/tooling), cascading clock fixes (each re-labbed + Summary/JSON re-derived),
the stale-roster oracle cluster (re-harvested + roster guards), and the 🟢 latent tier (a
7-cluster parallel sweep). Every fix earned a `*_REGRESSION` test; fast gate green (200), golden
tier green (38). The authoritative per-item checklist is **"Fix status"** at the bottom.

---

## 🔴 Critical

| File | Bug | Impact |
|---|---|---|
| `winota_clock_lab.py:108-150` | Clone of its sibling labs that **lost the command-zone deploy step**. Winota is the commander, so `deck_sim` pulls her from the library; the only code setting `self.winota=True` checks `nm == WINOTA` in hand — dead code. Verified True in **0/3000 trials**. | The entire Winota flood/Erkenbrand snowball never fires — it clocks a Winota deck *without Winota*. Headline clock wrong (too slow); ranking decisions off it are invalid. Fix: add `if not self.winota and g.avail>=4` deploy block. |

## 🟠 Stale-identifier cluster (Calamity→Croak rename + Hashaton drop)

Three labs crash on launch; several tools silently produce wrong/missing results.

| File | Symptom | Class |
|---|---|---|
| `vs_dragon_roster_lab.py:83` | Crashes `KeyError: 'calamity_tax'` at import | crash |
| `ext_glarb_vs_calamity_lab.py:43,255` | Crashes `FileNotFoundError` (+ stale keep-spec key) | crash |
| `glarb_iso_clock_lab.py:56` | Crashes `FileNotFoundError` on V1 baseline | crash |
| `wb_rebuild_vs_dragon.py:56,64-65` | Crashes on load; `PROTECT.get('calamity_tax')` silently → 0.0 | crash / silent-wrong |
| `game_log.py:79-84` | Can't log 2 active decks (croak, forced_liquidation); accepts retired calamity_tax | data-capture dead |
| `framework_bakeoff.py:81-122` | Oracles silently drop 2 current decks; `--power` uses stale roster | silent wrong-coverage |
| `clock_check.py:52-69` | Maps slug to a deleted Summary file → silently `[SKIP]`s drift for 3 decks | silent skip |
| `self_meta_lab.py:71` → `interaction_meta_lab.py:176` | Δrank broken for 2 newest decks; anchored to a dead one | silent wrong |
| `unlock_optimizer.py:50` | "What to buy" recommends cards for the dropped Hashaton build | wrong output |
| `delay_lab.py:640` | Still loads the dropped Hashaton considering-list as live config | stale config |

> **Recurrence fix:** derive these rosters from `deck_registry.fb_decks()` (single source of
> truth) instead of hand-maintained literals; a one-line invariant test would have caught all.
> Fixing `framework_bakeoff`/`clock_check`/`self_meta` properly also requires re-running
> pod_gauntlet/self_meta/interaction to get real oracle numbers for the 2 new decks.

## 🟡 Simulation-correctness bugs that bias published clocks

| File | Bug | Direction |
|---|---|---|
| `ct_speed_lab.py:279` | `dig` knob is raw card DRAW, not Glarb's selection; lab's own "flat ⇒ mana-gated" conclusion is false (T13→T8 swing); realistic modes hardcode fictional +2 cards/turn | clock too fast |
| `er_speed_lab.py:115` | Fire Lord Zuko hardcoded `MV=4`; actual cost is `{R}{W}{B}` = 3 | clock too slow |
| `lw_speed_lab.py:273-277` | Pre-chip lethal-mana ignores Crackle's X≥3 targeting floor (offers 5-mana wipe that costs 11) | clock too fast |
| `pod_gauntlet.py:550` | `simulate_vs_lock` re-rolls lock effectiveness `e` every turn → P(hold n turns) ≈ eⁿ (sibling `lock_race` is correct) | understates locks |
| `urza_clock_lab.py:107-117` | Urza's +2 artifact mana regranted on every `spend()`, not once/turn | mana overstated |
| `pod_championship.py:102-113` | Hardcoded 16-deck bracket drops the 17th seed (or malformed 5-seat pod with `--snake`) | corrupted field |
| **Systemic — even-median** | `vals[len(vals)//2]` (upper middle) in `speed_lab_core.py:382`, `calibrate.py:176`, `er_speed_lab.py:639`, `gd_clock_lab.py:501`, `lock_lab.py:253` | clocks ~1 turn slow at boundaries |

## 🟡 Tooling correctness (non-clock)

| File | Bug |
|---|---|
| `card_lookup.py:103` | Vanilla creatures (~345 cards) lose type line, mana cost, P/T — `is_multi_face` fires on any empty `oracle_text`. This is the tool CLAUDE.md mandates before recommending a card. Fix: gate on `card.get("card_faces")`. |
| `deck_doctor.py:904-911` | `--footprint` (and `--all`) crashes `AttributeError` on any deck with an unresolved card — the WIP decks the doctor exists to diagnose. Make `_all_text` None-safe. |
| `kb_content.py:592,634` | Kill-line notes silently dropped for 5/17 decks whose Summaries put the description on the line after `**Line N…**` (radiation, replication, earthbend, exiles, diminishing) |
| `update_scryfall_data.py:47-83` | Non-atomic overwrite — interrupted download corrupts the only copy of the 168 MB bulk before verification. Stream to `.part`, verify, then `replace`. |
| `sync_to_project.py:120-136` | `--since` runs the collision guard only over changed files — clash with an unchanged file isn't caught; guard only protects `--all` |

## 🟢 Lower-impact / latent

- **Reproducibility:** `deck_sim.py:642` threads one RNG across all decks (`--deck X` ≠ batch row);
  `esc_clock_lab.py:210` iterates a `set` (PYTHONHASHSEED-dependent); `deck_registry.py:606`
  same-date tie-break inverted (dormant).
- **gd-family copy-paste:** `gd_ramp_lab.py:79`, `gd_combo_lab.py:120`, `gd_speed_lab.py:204` all
  refund the spell's mana cost in the land-ramp loop (A/B deltas preserved, so conclusions hold).
- **Rules nits (secondary lines):** `dr_clock_lab.py` Living Death over-returns board + Zulaport
  over-credits life; `cos_clock_lab.py` Diregraf Colossus self-triggers; `rs_clock_lab.py` Mothman
  attacks while summoning-sick; `berta_clock_lab.py` combo fires turn the dork enters;
  `sephiroth_clock_lab.py` Mikaeus counts Humans (dead `is_human()`); `ebm_clock_lab.py` Scute
  Swarm exponential engine is inert (never seeded); `urza_clock_lab.py:185` & `lw_clock_lab.py:203`
  don't reserve tutor mana.
- **Latent traps:** `er_speed_lab.py`/`rc_speed_lab.py` `build_lib` silently ignores a missing
  remove-target (shared core guards this; copies don't); `lw_speed_lab.py:97` stale date label;
  `test_bakeoff_real_oracle.py:48` reimplements prod logic instead of calling it.

## Flagged for review (not confirmed)

- `pod_gauntlet.py` `simulate()`/`simulate_vs()` re-roll disruption/answer every turn — same
  shape as the confirmed lock bug, but per-turn combo re-attempts may be intended. Check vs intent.

---

## Fix status (2026-06-29)

### ✅ Resolved this session — safe cluster (implemented + regression-tested + committed)

| File | Fix |
|---|---|
| `vs_dragon_roster_lab.py` | dropped stale `calamity_tax`, renamed `KILL` key → `croak_and_dagger`, added load-time `assert set(DECKS)==set(KILL)` guard |
| `wb_rebuild_vs_dragon.py` | → `croak_and_dagger` (now runs; Glarb/Croak scores 93% ≈ the 94% reference) |
| `ext_glarb_vs_calamity_lab.py` | resolve current deck via `deck_registry.resolve_deck`, fixed keep-spec key, updated stale display labels |
| `glarb_iso_clock_lab.py` | V1 baseline → `archive/old_decklists/…` |
| `game_log.py` | `DECKS` derived from `deck_registry.fb_decks()` (single source of truth) |
| `unlock_optimizer.py` | `DEFAULT_BUILDS = []` (Hashaton dropped, Forced Liquidation graduated) |
| `card_lookup.py` | `is_multi_face` keys on `card_faces`, not empty `oracle_text` (vanilla creatures render) |
| `deck_doctor.py` | `_all_text` None-safe (footprint / `--all` no longer crash on unresolved cards) |
| `update_scryfall_data.py` | atomic `.part` write → verify → `replace` |
| `sync_to_project.py` | collision guard runs over the full namespace before the `--since` filter |

Tests added: `test_stale_slug_regression.py`, `test_card_lookup.py`, `test_update_scryfall.py`,
`test_sync_to_project.py`, + an `_all_text` None case in `test_deck_doctor.py`.

### ✅ Resolved 2026-06-29 (cont.) — cascading tier (implemented + regression-tested + re-derived)

| File | Fix | Clock impact |
|---|---|---|
| 🔴 `winota_clock_lab.py` | deploy the commander from the command zone (`g.pay(4)`); removed the dead `nm == WINOTA` in-hand branch; do NOT decrement `humans_left` for her (not in the library flood pool) | engine now fires (was 0/3000): decap **T8–9 → T6–7**, table **T13–14 → T9–10**, never-table **26–43% → ~1%**. `PROP_Winota_Joiner_of_Forces.md` verdict **reversed** (mid-speed/can't-close → genuine racer), `project_dismantle3_build1` memory corrected. Not in the golden snapshot (considering/ deck), so no `--update`. Regression: `test_winota_regression.py` (3 tests, hermetic). |
| 🟡 **even-median ×5** (`speed_lab_core.py`, `calibrate.py`, `er_speed_lab._median`, `gd_clock_lab.py`, `lock_lab.med_online`) | `vals[len//2]` (upper-middle) → `vals[(len-1)//2]` (lower-middle = lowest turn with cum ≥ 50%, matching `curve_median`). Identical for odd N (existing test stays green). | **Scope was narrower than the audit implied: print-only.** The harvested clocks come from the cum *curves* (`parse_row`/`curve_median`), NOT the `median()` line — so NO Summary moved and the **golden suite passes bit-for-bit** (38 green, proving no curve changed). The fix just makes each lab's printed "median Tx" line agree with the harvested clock. Regression: `test_median_even_length_is_lower_middle` + a `curve_median`-agreement property test. |
| 🟡 `kb_content.py` dropped notes | B1 loop now looks ahead for the description when it sits on the line AFTER `**Line N —**` (group(2) empty) — all 5 decks' real shape. Added a `--content` flag to `dashboard_export.py` (content-only re-bake, manifest-merge) and re-baked the 5 deck pages. | **Non-clock (content display).** radiation 8/8, exiles 4/4, diminishing 5/5, replication 6/6, earthbend 6/6 finishers now carry notes (were empty). 12 other deck pages byte-identical; no sim grid touched. Regression: existing test now asserts notes + 2 new shape tests. |
| 🟡 `er_speed_lab.py` Zuko MV | `ZUKO_MV = 4 → 3` (Fire Lord Zuko {R}{W}{B}, card_lookup verified). | **Median HOLDS** (decap T8 / table T10) — only the front edge shifts (T7 decap 39→48%, T8 70→76%). Updated the harvested curve (`pod_gauntlet_clocks.json` exiles + in-source `CLOCKS` mirror), golden snapshot (`--update`, exiles-only), and the Summary's "T6≈9%/70% by T8" prose → 11%/76%. Golden 38 green. Regression: `test_er_zuko_mv_is_three`. Dashboard deck-page + clocks.json + gauntlet/tier-list grid re-bake **batched for the end** (with the ct croak change). |
| 🟡 `pod_gauntlet.py` lock re-roll | `simulate_vs_lock` now samples effectiveness ONCE per trial (mirrors the verified-correct `lock_race`) — holds until removed, instead of re-rolling Bernoulli(e) each turn (P(hold n)≈eⁿ). | **Lock SUB-REPORT only** (`--vs-lock`; VS_LOCKS = grand_design only) — NOT the main gauntlet/tier-list/golden. Numbers barely move (`e=0.95` → tiny per-turn leak): GD ~45% blend / ~58–59% vs Acererak HOLD within MC noise. Added a dated provenance note to the GD Summary + matrix. Regression: `test_simulate_vs_lock_is_persistent` (grind≈e under an isolated persistence probe). |
| 🟡 `pod_championship.py` 16-deck cap | `draw_groups` `range(4)` → `range(0, len(seeds), 4)` — deals the remainder pot round-robin so a 17-deck field makes a 5-seat Pod A and drops NO seed (snake already placed all 17). Display strings → dynamic count (lab header, docstrings, dashboard comment, Championship.tsx). | Was silently dropping seed #17 (Diminishing Returns) from every drawn bracket. NOT golden/tier-list. `championship.json` re-bake **batched** for the end; the dated 2026-06-15 analysis writeups (16-deck era, pre-FL) need a fresh dated run, not in-place edits. Champion unchanged in practice (dropped seed is the weakest). Regression: `test_championship_brackets_place_every_seed` (N∈{15..21}, both builders). |
| 🟡 `urza_clock_lab.py` per-spend mana | Urza's +2 artifact mana (`mana()`/`spend()`) was recomputed from the `self.urza` boolean on every `spend()` → refreshed per-spend (unbounded/turn). Now a per-turn pool (`urza_pool`) that depletes and refreshes once/turn (+ on deploy). | **CLAIM changes** but NOT golden/dashboard (Urza is a `considering/` candidate). Clock **T6–7 → T7–8** (cons median T8/49% by T7/8% never; gen median T7/57%/2%). Re-derived the lab docstring, `Urza_Planned_Obsolescence_Clock_2026-06-25.md`, and the `project_urza_planned_obsolescence` memory ("upper-tier racer" → "pod-competitive, a touch behind the racer ceiling"). Regression: `test_urza_artifact_mana_is_once_per_turn`. |
| 🟡 `lw_speed_lab.py` Crackle floor | Pre-chip lethal-mana ignored Crackle's X≥3 targeting floor (a 3-opponent wipe is ≥11 mana at any life ≤45); the sensitivity offered 5/8-mana "wipes". Replaced the literals with `crackle_lethal_mana(life, copies)` enforcing the floor. | **NOT golden** (analysis lab; LW's published clock is `lw_clock_lab`, correctly floored — Summary T11 unaffected). Magnitude only: 40→30 +4pts at T10 (was +12), 40→20 T10 ~4%→25% / never 86%→51% — chip still the dominant lever (conclusion stands). Corrected the `project_lightning_war_speed_analysis` memory + a note in the archived Speed-Curve analysis. Comet Storm's separate @20 rounding slip flagged, not bundled. Regression: `test_crackle_lethal_mana_respects_targeting_floor`. |
| 🔴 **`ct_speed_lab.py` dig** | The `dig` knob modelled Glarb's SELECTION (surveil-2 / play-from-top, net-zero on card count — already in the baseline) as fictional RAW DRAW (`g.draw(dig)`). The "realistic" modes passed dig=2/3; corrected to dig=0 (honest), relabeled dig>0 as a raw-draw upper bound, fixed the false "dig-flat ⇒ mana-gated" conclusion + docstring. | **Biggest live-clock change.** Croak decap **~T10 → ~T13**, table **~T10/T11 → never-in-horizon** (~40% killed by T14). Re-baked the croak harvest (`pod_gauntlet_clocks.json`, also fixed stale name "The Calamity Tax"→"Croak and Dagger"); now matches the in-source fallback. Re-derived the Croak Summary (Kill Window + weakness + flagged the dig=2 A/B sub-notes), the `feedback_selection_vs_mana_gated` methodology memory ("model selection AS selection, not raw draw"), `project_calamity_lands_graveyard_swap`, and the MEMORY.md hook. Regression: `test_croak_published_clock_is_the_honest_grind`. Gauntlet P(beat pod) + tier-list + dashboard re-bake in the final batch. |

### ✅ Resolved 2026-06-29 (cont.) — final batch re-bake + stale-roster oracle cluster

| Item | Fix | Commit |
|---|---|---|
| **Final batch re-bake** | One `dashboard_export.py` run propagated the er (exiles decap T8 / table T10), ct (croak decap T13 / table >T14), and championship (17-seat) source changes into every baked view: clocks.json, gauntlet, championship, tier-list, locks, home, roster, manifest + the croak/exiles deck pages. Only the two re-clocked deck pages move; the rest is aggregate re-derivation. Mirrored to `ui/public/data`. | `5a4afbd` |
| 🟡 `framework_bakeoff.py` | `RICHER_ORACLE` + `INTERACTION_ORACLE` **re-harvested for all 17** (pod_gauntlet @20k a=0.3, self_meta @20k, interaction @120k tax=0.6) — the 06-16 snapshot was stale beyond the rename (Lightning War's chip-model table collapse T14→T9 lifted its self_meta **5→49** / interaction **7→52**; Exiles' Zuko fix; Replication's 06-22 opt). Dropped dead `calamity_tax`, added croak/forced_liquidation, + a `set(RICHER)==set(DECKS)==set(INTERACTION)` guard. Bakeoff now correlates over 17 (was silently 15). | `b236f70` |
| 🟡 `clock_check.py` | `SUMMARY` → `croak_and_dagger` + `forced_liquidation` (was `calamity_tax`→deleted file), `set(SUMMARY)==fb_decks()` guard. Also fixed the parser blind spot it surfaced: a header-format clock line (`Score … · Clock: T8 decap / T9 table`) was cut at the leading `·` → UNPARSED on FL's correct cite; `cited_turns` now re-cuts at the lab marker when the `·` cut left no clock keyword. **Roster 17/17 [OK], 0 DRIFT, 0 UNPARS.** | `b236f70` |
| 🟡 `self_meta_lab.py` + `interaction_meta_lab.py` | `JUDGMENT` Δrank anchor → `croak_and_dagger:7` (inherits the renamed deck's tier; model now ranks it #15, Δ−8). `forced_liquidation` left unranked (doc predates it → honest "—", not a fabricated judgment). `set(JUDGMENT)<=ROSTER` guard. interaction_meta_lab fixed transitively (imports `sm.JUDGMENT`). Synced `campaigns/Self_Meta_Ranking.md` with a dated note. | `b236f70` |

Regression: 4 new hermetic guards (`test_stale_slug_regression.py` clock_check/framework_bakeoff/self_meta + `test_sim_cluster_regression.py` header-format parse). Full fast gate green (155).

### ✅ Resolved 2026-06-29 (cont.) — 🟢 lower-impact / latent tier (7-cluster parallel sweep)

Fanned out one agent per disjoint file-cluster, each held to **clock-neutral-or-escalate**
(re-run the lab; keep only if the published median holds, else revert + flag). Per-cluster
hermetic regression test in `tests/test_green_*.py`. Commit `e1a394c`.

| Cluster | Fix | Outcome |
|---|---|---|
| gd-ramp-refund | `gd_ramp_lab`/`gd_combo_lab`: drop the `g.avail = g.lands + g.rock_out` reset (cast() already pays; it refunded the spell + counted the tapped land same-turn). `gd_speed_lab` had no such loop (audit line ref inaccurate). | Clock-neutral; ramp-saturation conclusion holds (deltas flatter). |
| reproducibility | `deck_sim` per-deck str-seeded RNG (single-run == batch row); `esc_clock_lab` granter set→ordered tuple (PYTHONHASHSEED-independent); `deck_registry` version-key tie-break (same-day timestamped re-cut wins). | Clock-neutral (esc golden bit-identical under both hash orders). |
| latent-traps | `er`/`rc_speed_lab` `build_lib` raises on a missing remove-target; `lw_speed_lab` stale date label; `test_bakeoff_real_oracle` calls prod `framework_values`. | Clock-neutral (guards/labels/test-wiring). |
| rules-dr-cos | Zulaport-class gain credited per-death not per-opponent; Living Death returns only the pre-existing yard; Diregraf Colossus no self-token. | DR bit-identical; CoS median T8/T11 holds (~1pp curve). |
| rules-rs-berta | The Wise Mothman (commander, no haste) can't attack/feed combat its entry turn; Berta combo gated on an unsick board. | Median holds (RS T7/T10), but RS front edge slows — see cascade below. |
| rules-seph-ebm | **ESCALATED** (comment-only): the correct Mikaeus non-Human-fodder gate moved Sephiroth's median **T12→T13**, so reverted + documented for a coordinated proposal-clock pass; EBM Scute Swarm exponential left intentionally unmodeled (wiring it flips EBM's table median). | Clocks preserved; 2 fixes deferred as documented-accepted. |
| rules-tutor-mana | `lw_clock_lab` reserves the tutor's mana before the fetched finisher; `urza` already correct post per-spend fix (comment only). | LW median T8/T9 holds. |

**Curve cascade (medians held, front edges moved):** the rs/cos/lw fixes shifted bit-exact
@800 curves → regenerated the golden snapshot under py3.14 (`1c6ee0d`). The **Radiation front-edge
correction is material**: removing Mothman's illegal entry-turn swing dropped its goldfish
decap-by-T7 ~76→63%, so its **pod P(win) 69→60 — Genome (66) is now the roster's top racer.**
Re-harvested the 3 affected curves into `pod_gauntlet_clocks.json`, re-baked the dashboard, and
re-harvested the `framework_bakeoff` oracles (RS pod 69→60 / self_meta 35→31 / interaction 39→33;
the rest ≤±1 shared-pool noise). Published Summary clocks all unchanged (medians held).

- **Left as-is:** `delay_lab.py` Hashaton load — inside a historical bake-off function, `try/except`-guarded, non-crashing; maintainer call.
- **Flagged → RESOLVED (intended):** `pod_gauntlet.py` `simulate()`/`simulate_vs()` per-turn re-roll is correct — reactive disruption/combo IS a fresh per-turn attempt; persistent locks use the separate `simulate_vs_lock`/`lock_race` path (the one that *was* buggy). Not a bug.
- **Deferred (escalated):** the Sephiroth non-Human-fodder gate (median T12→T13) and EBM Scute Swarm exponential wiring (flips table median) — both need a coordinated proposal/clock re-derivation; currently documented-accepted in-code with change-detector tests.

**All 38 confirmed bugs resolved or consciously deferred.** Per repo convention, each fix earned a `*_REGRESSION` test; full fast gate green (200), golden tier green (38).

> Two items (`clock_check.py`, `wb_rebuild_vs_dragon.py`) were surfaced by the completeness
> critic rather than the per-cluster pass, but both were independently grep-confirmed.