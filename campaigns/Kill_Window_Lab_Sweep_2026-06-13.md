# Kill-Window Lab Sweep — tracker & ranking (opened 2026-06-13)

**Goal.** Give every active roster deck a lab-cited kill-turn clock, replacing the
hand-estimated Kill Windows that the `Framework_Clock_Gap_2026-06-09` evidence
showed are systematically optimistic. End state: a roster **ranked by measured
decap clock**, with the Conversion Check score alongside (the framework's finding
was that the two are uncorrelated in the 15–19/20 band — so we report both).

**This is a multi-session campaign.** This file is the durable store. Per-deck
procedure: `workflows/WF_Kill_Window_Lab.md`. Rule of record:
`REF_The_Conversion_Check.md` → Verification rule.

**Resume here each session:** read the Status board below, pick the top
`TODO`/`PARTIAL` row (priority-ordered), run the workflow, append to the Session
log, and update the Ranking. One deck per sitting is fine.

---

## The bar (what the ranking measures)

- **Decap clock = the race metric.** Pod-beating bar is **decap by T≤7** (the pod's
  combo decks win T6–7 behind Grand Abolisher — see `project_pod_combo_opponent`).
- **Table clock = the reliability metric**, not the race. Genome's T8 table is the
  roster benchmark for "reliable." Decap and table are stated separately, always.
- **Never-in-12** is the reliability tail.
- Score (NN/20) is judged on the Conversion Check; clock is measured. Reported
  together, never merged.

## Status legend

- ✅ **DONE** — kill-turn clock measured (decap + table), Summary cites it.
- ◐ **PARTIAL** — has a speed-curve / availability lab but **no kill-turn decap/table
  clock**. Needs a proper clock run for consistency.
- ❌ **TODO** — no lab; Kill Window is hand-estimated (`(unverified)` flagged).

---

## Status board — work queue (priority-ordered)

Priority rule (from `Framework_Clock_Gap` §5): **front-edge / low claims first** —
every front edge measured so far came back optimistic. Then the T7–9 cluster, then
the slow decks. Kill-shape prediction is the pre-registered prior (Stage 1 of the WF).

| # | Deck | Commander (colors) | Claim | Kill shape → prediction | Status |
|---|---|---|---|---|---|
| 1 | Eldrazi Stampede Chaos | Maelstrom Wanderer (Temur) | T6–8 | combat focus-fire → decap fast / table slow; **front edge suspect** | ✅ DONE — decap T8 / table T12 (`esc_clock_lab.py`, 2026-06-13); claim was optimistic front edge + decap/table conflation |
| 2 | Radiation Sickness | Wise Mothman (Sultai) | T6–9 | rad/toxic attrition + drain → likely converge; **front edge suspect** | ✅ DONE — table-win T10 / decap T7 (`rs_clock_lab.py`, 2026-06-13); claim optimistic on the win clock; coarse engine model |
| 3 | Lightning War | Fire Lord Azula (Grixis) | T6–7 | burn: single-target finishers + pingers → mixed; availability-verified, no kill-turn clock | ✅ DONE (v2) — decap T9 / table ~T13 strict goldfish (`lw_clock_lab.py`, 2026-06-13); from-40 sweep = 14-mana Crackle, so "T6–7" is the chip-/disruption-assisted clock; goldfish understates this tempo/disruption deck (v1's T11 was a model bug — fixed) |
| 4 | Crystal Sickness | Golbez (Dimir) | T7–9 | reanimate a fatty → combat focus-fire → diverge | ✅ DONE — decap T11 / table T13 (`cs_clock_lab.py`, 2026-06-13); claim optimistic ~2–4 turns; shape is MIXED (drain+Tezzeret converge / combat diverges), not the pure diverge predicted; engine = card draw |
| 5 | Curse of the Scarab | The Scarab God (Dimir) | T7–9 | zombies + Gray Merchant drain → mixed combat/drain | ✅ DONE — decap T8 / table T11 (`cos_clock_lab.py`, 2026-06-13); **decap claim HELD** (first in sweep), only correction is decap/table split; combat decaps, drain tables |
| 6 | Earthbend the Meta | Toph (Naya) | T7–9 | artifact stompy → combat focus-fire → diverge | ✅ DONE — decap T8 / table T12 (`ebm_clock_lab.py`, 2026-06-13); decap claim ~held (T7=34% front edge), correction is decap/table conflation; **diverge prediction held** (focused AWBO+combat outran the converge ping) |
| 7 | Lorehold Spirits | Quintorius (Boros) | T7–9 | Goblin Bombardment combo (ping) + spirits → combo converge / combat diverge | ✅ DONE — decap T8 / table T10 (`lor_clock_lab.py`, 2026-06-13); **decap claim held** (matches avg-T8, T7=46%), correction is decap/table split (2-turn gap); combo+Purphoros converge tightens it; Karmic Guide echo-not-persist text fixed |
| 8 | The Calamity Tax | Glarb (Sultai) | T7–9 | X-drain (Exsanguinate) + Kokusho reanimator → mana-gated; speed-curve done, no kill-turn clock | ✅ DONE — decap T13 / table rarely-in-14 (`ct_speed_lab.py`, 2026-06-13); **"T7–9" falsified, biggest miss** (hard mana-gated, strict floor excl. Seedborn); 4-version bake-off, none up to par → stay V1, different direction needed |
| 9 | Ms. Bumbleflower | Ms. Bumbleflower (Bant) | T8–10 | spellslinger tempo, evasive/Jolrael alpha → combat diverge | ✅ DONE — decap T8 ceiling / table T11 (`bmf_clock_lab.py`, 2026-06-13); decap claim corroborated but as a CEILING (goldfish dumps interaction proactively; real control deck slower); combat-diverge held; Willbreaker theft goldfish-invisible |
| 10 | The Dark Lord's Army | Sauron (Grixis) | T8–10 | go-wide tokens / The Ring → combat focus-fire → diverge | ✅ DONE — decap T8–10 / table T11–15 by pod tempo (typical T9/T12) (`dla_clock_lab.py`, 2026-06-13); **opponent-driven engine — modelled vs pod-activity, not goldfish**; claim well-corroborated; kills faster vs active pods; drain converge + Army focus |

**Scope note (2026-06-13):** rows 3 (Lightning War) and 8 (Calamity Tax) already
have *speed-curve* labs (`lw_speed_lab.py`, `ct_speed_lab.py`) but those measured
availability/levers, not a kill-turn decap/table distribution — CT's Summary says
so explicitly ("no kill-turn goldfish run"); LW's "T6–7" came from finisher
availability. They're in-scope as PARTIAL so the ranking rests on one consistent
metric. If the user wants them treated as already-done, drop them from the queue —
they don't block the 8 TODO decks.

---

## Already verified (baseline for the ranking)

These six already carry a kill-turn clock — no work, they seed the ranking.

| Deck | Commander | Score | Decap | Table | Lab | Date |
|---|---|---|---|---|---|---|
| The Genome Project | Kuja (Rakdos) | 15/20 | **T7** | T8 | `gp_clock_lab.py` | 2026-06-10 |
| The Replication Crisis | Satya (Jeskai) | 17/20 | **T7** (med) | T10+ | `rc_speed_lab.py` | 2026-06-09 |
| The Exile's Return | Zuko (Mardu) | 17/20 | **T8** (med) | T10 | `er_speed_lab.py` | 2026-06-09 |
| Diminishing Returns | Teysa (Orzhov) | 17/20 | **T9** | T12+ | `dr_clock_lab.py` | 2026-06-10 |
| Zero-Sum Game | Witherbloom (Golgari) | not audited | **T9** | T9 | `wb_clock_lab.py` | 2026-06-11 |
| The Grand Design | Atraxa (WUBG) | 19/20 | **T10** (med) | T12+ | `gd_clock_lab.py` | 2026-06-10 |

---

## Session log (append-only — newest at bottom)

Each entry: date · deck · what ran · result vs claim · direction · doc.

- **2026-06-13** — Sweep opened. Inventoried roster: 6 decks already clock-labbed
  (above), 8 fully unverified, 2 partial (speed-curve only). Built
  `workflows/WF_Kill_Window_Lab.md` and this tracker. No deck labbed yet — queue
  is ordered, ready to start at row 1 (Eldrazi Stampede Chaos).
- **2026-06-13** — **Deck 1: Eldrazi Stampede Chaos.** Ran `esc_clock_lab.py` (40k,
  seed 20260613). Claim "Goldfish T6–8" **falsified as a single number**: decap
  median **T8** (T6 = 10% god-hand), table median **T12**, never-in-14 table 11%.
  Optimistic front edge (7-for-7) + decap/table conflation; decap median in-band
  so a milder miss than Grand Design. Kill-shape prior held (8-for-8). No card-text
  errors. Wrote `analysis/Eldrazi_Stampede_Clock_Lab_2026-06-13.md`; updated
  Summary + Deck_Index. Pod bar: T≤7 decap only 26% — does not race. Next: row 2,
  Radiation Sickness.
- **2026-06-13** — **Deck 2: Radiation Sickness.** Ran `rs_clock_lab.py` (40k, seed
  20260613 — coarsest lab in the sweep, expected-value counter-engine model).
  Claim "Goldfish T6–9" **optimistic on the win clock**: table-win median **T10**
  (T6 ≈ 1%, T9 ≈ 49%), decap one opponent median T7. Marquee T5–6 combo is a
  five-piece god-hand (1–4% by T7). No card-text errors (2026-05-13 audit holds).
  **Kill-shape lens nuance learned:** the converge *kills* converged as predicted,
  but the deck's *fastest* clock was the incidental combat decap, not the marquee
  combo — classify the fastest line, not the named one. No swaps; 18/20 unchanged.
  Wrote `analysis/Radiation_Sickness_Clock_Lab_2026-06-13.md`; updated Summary +
  Deck_Index. Next: row 3, Lightning War (PARTIAL — has speed-curve, needs kill-turn clock).
- **2026-06-13** — **Deck 3: Lightning War** (was PARTIAL). Built `lw_clock_lab.py`
  — the kill-turn goldfish lw_speed_lab never ran. **v1 → v2 after user push-back.**
  v1 (decap T11 / table never) was too slow — a real model bug: it swung only Azula's
  4 power and omitted Vivi Ornitier (2nd pinger + ramp) and Fated Firepower (damage
  amplifier). **v2: decap median T9, table ~T13 (40% never).** The from-40 one-cast
  sweep is 14-mana Crackle (`{X}{X}{X}{R}{R}`; corroborated by lw_speed_lab's 20% T12
  / 70% never), so "T6–7" is the **chip-/disruption-assisted real-pod clock**, not a
  from-full goldfish median — NOT a clean falsification (goldfish models no disruption
  and a static-40 table; the deck's tempo/race identity is legitimate). 19/20 stands;
  corrected stale 18/20 in Deck_Index. **LESSON: inventory the full board + every
  pinger/amplifier before trusting a burn deck's clock — and goldfish strictness
  (static 40, no disruption) penalizes tempo/control decks; flag it, don't over-read.**
  No card-text errors. Wrote `analysis/Lightning_War_Clock_Lab_2026-06-13.md`. Next:
  row 4, Crystal Sickness.
- **2026-06-13** — **Deck 4: Crystal Sickness.** Built `cs_clock_lab.py`. Claim
  "Goldfish T7–9" **optimistic**: decap median **T11** (T7 = 7%), table median
  **T13**; never-in-14 decap 21% / table 34% (table tail is an UPPER bound — see
  below). **Same v1-class model bug as Lightning War, caught and fixed:** the first
  model had no card draw and flatlined at ~1 artifact/turn (killed never), because
  the deck's engine drivers are *non-artifact* permanents an artifact-only deploy
  loop skipped — Matoya (draw per surveil = per artifact ETB), Sai (creature),
  Efficient Construction / Mirrodin Besieged (enchantments), Forensic Gadgeteer /
  Mechanist (creatures). Adding the draw engine (Matoya + Thought Monitor/Thoughtcast/
  Skullclamp/Baubles/One Ring) made it run. **Two real bottlenecks** gate the kill:
  (a) reach 8 artifacts (~T8 median), (b) dig a drain BOMB to the yard — only 3 in
  99 (Dreadnought 12 / Master = arts / Troll 6), ~50% by T9, matching raw card-
  finding odds; the table then needs 3–4 drain cycles. **Kill-shape:** tracker's
  "combat focus-fire → diverge" was corrected at Stage 0 to MIXED (named primary
  drain + Tezzeret +2 = all-table converge; Urza Construct/Thopters = combat
  diverge). Measured mixed (decap T11 / table T13, ~2-turn gap). **Lesson: the
  shape lens held (9-for-9 on the pattern) but my corrected absolute prior (decap
  ~T8) was itself 3 turns optimistic — the lens predicts the pattern, not the turn.**
  No card-text errors (2026-05-06 re-audit held; reconfirmed Master-CDA-in-yard,
  Golbez-returns-to-hand re-bin, Tezzeret-no-self-affinity). Pod bar: decap T≤7 only
  7% — does NOT race; the deck interacts/grinds (5 counters) rather than out-speeds.
  No swaps; 17/20 stands. Caveat: model captures the primary drain + Tezzeret +
  combat but OMITS the slower redundant closers (Mirrodin Phyrexian 15-yard alt-win,
  Cruel Captain emblem, Urza mana→hardcast), so 34% table-never is an upper bound on
  the tail, not the front edge. Wrote `analysis/Crystal_Sickness_Clock_Lab_2026-06-13.md`;
  updated Summary + Deck_Index + README reference table (added ESC/RS/LW/CS rows).
  Next: row 5, Curse of the Scarab.
- **2026-06-13** — **Deck 5: Curse of the Scarab.** Built `cos_clock_lab.py`. Claim
  "Goldfish T7–9" is the **most accurate hand-estimate in the sweep** — decap median
  **T8** (T7 = 32%, a healthy front edge, NOT a god-hand), squarely in-band. **First
  deck whose front edge did not come back optimistic.** Only correction: the single
  number conflated decap with table — table median **T11** (never-in-14 9%). **Two
  engines drive the two clocks:** lord-pumped **combat** focus-fires the decap (~T8);
  the **all-table Scarab/Gary drain** is modest per turn (~4–5 Zombies median at T7–9)
  so it *tables* at T11 — i.e. the deck's named primary (Scarab upkeep) is the table
  clock, the combat is the decap clock (opposite of the Summary's framing). Soultrader
  loop kill_all assembles only ~1% by T12. **Two model bugs caught:** (1) devotion
  zeroed because parsed records carry no `mana_cost` field → Gary drained 0 (fixed via
  oracle pip map); (2) zombie engine under-counted (~3 at T7) until I added the token
  generators I'd omitted — Grave Titan attack tokens, Liliana DM +1, Cryptbreaker, Rot
  Hulk ETB, Living Death/Agadeem's mass dump (cs/lw lesson, 3rd time). Model still
  OMITS deaths-based token engines (Gisa, Wilhelt, Crowded Crypt) so T11 table is a
  CONSERVATIVE (slow) edge — real table likely T10–11. No card-text errors (2026-05-05
  re-audit held; reconfirmed Scarab-is-a-God-not-Zombie, Gary=devotion, loop=kill_all).
  Pod bar: decap T≤7 = 32% (highest in sweep) — can pressure early via combat, but the
  *win* clock is T11 and the real pod plan is interaction + inevitability, not a race.
  No swaps; 17/20 stands. Wrote `analysis/Curse_of_the_Scarab_Clock_Lab_2026-06-13.md`;
  updated Summary + Deck_Index + README. Next: row 6, Earthbend the Meta.
- **2026-06-13** — **Bug-impact review + producer re-check (before resuming at row 6).**
  Audited every prior lab against the bugs surfaced so far. **Clean:** (a) the
  `color_identity` mana bug (2026-06-09) is walled off from all clock labs — the clock
  mana model is a generic lands+rocks count and the mulligan keeps on a colourless land
  count; the buggy code feeds only `deck_sim`'s `all_colors_by_turn`, which no clock lab
  calls; `rc/er_speed_lab` don't reference colour at all. (b) The devotion / "records
  carry no `mana_cost`" gotcha (caught at cos) never touched dr/ct — both hardcode `PIPS`
  dicts — and cos fixed its own copy before publishing. (c) Stale `sim_profiles.json` is
  `deck_sim --combos`-only; no clock lab reads it. **The one real, systematic risk** is
  omitted token/producer/amplifier modelling (lw/cs/cos, "3rd time"), which always biases
  a body/damage-race clock SLOWER → false-negative on the T≤7 pod bar. Exposed set =
  esc + rs (labbed rows 1–2, before the lesson). **wb is structurally immune** (closed
  loop; one igniter body is enough) and **dr got the scrutiny** (engine generates tokens;
  its whole finding was "death VOLUME"). **esc re-checked with the two omitted amplifiers
  modelled** (`esc_clock_lab.py` v2: Berserkers' Onslaught = combat ×2 double strike;
  Warstorm Surge = per-creature-ETB burn distributed to the table; both oracle-verified):
  medians **UNCHANGED at decap T8 / table T12**, only the reliability tail moved
  (never-in-14 table 11%→9%) — singleton amplifiers shift the tail, not the median.
  **rs left un-patched** (documented): its median table clock T10 is the rad-drain
  `hit_all`, creature-count-INDEPENDENT by construction, so the omitted go-wide pieces
  (Walking Ballista alt-kill, Iridescent Hornbeetle tokens, Deepglow Skate counter-double)
  feed only the secondary Simic/Triumph/combat lines and the tail; re-modelling the
  sweep's coarsest EV lab would add more imprecision than it removes. **Net: no published
  decap/table median changes; all sweep verdicts stand.** Codified the lesson as a
  producer-inventory step + Do-not in `WF_Kill_Window_Lab.md`. Residual upside flagged in
  both writeups (esc: Etali/Kodama-East/Tireless still un-modelled; rs: Ballista line).
  Next: resume row 6, Earthbend the Meta — **apply the producer inventory** (Toph artifact
  stompy is a combat/body race → exposed shape).
- **2026-06-13** — **Deck 6: Earthbend the Meta** (first lab under the new producer-inventory
  step; most producer-dense deck in the sweep). Built `ebm_clock_lab.py`. Claim "Goldfish
  T7–9 (fastest T6)" is **essentially the DECAP window** — decap median **T8** (T7 = 34%
  healthy front edge, T6 = 11%, T5 = 2%), in-band; 2nd deck after CoS whose front edge did
  NOT come back optimistic. Correction = the usual decap/table conflation: **table median
  T12** (never-in-14 decap 1% / table 8%). **Shape lesson:** tracker predicted "combat
  focus-fire → diverge"; at Stage 0 I over-corrected to "converge-dominant" (seeing the
  Purphoros/Impact Tremors `hit_all` ping) — but measured **DIVERGE** (4-turn gap): the
  focused AWBO counter-burn + combat decap outran the hit-all ping. A hit_all axis does NOT
  converge the shape if a focused axis kills one player faster; the *original* prediction
  held. **Two v1-class model bugs caught & fixed** (4th/5th of the sweep): (1) commander
  not in library → `g.cast` failed, `self.toph` never flipped, whole engine dead (decap 88%
  never) — fixed via mana-gate cast (rs/cos pattern); (2) end-step earthbend counters
  powering the SAME turn's combat (decap T7) — fixed by ordering begin-combat EB (Kyoshi) →
  combat → end-step EB, decap → T8. No card-text errors (all kill cards verified Stage 0;
  Annie doubles only legendary-creature earthbend triggers, NOT Purphoros/Tremors/amps).
  Producer inventory applied (Scute exponential + Felidar/Springheart/Field/Awaken/Tannuk/
  Cathars modelled); conservative omissions (Evolution Sage proliferate, Ozolith, Bumi
  pumps, Zuran+Amulet recursion) all slow-bias → true clock if anything slightly faster.
  Pod bar: decap T≤7 = 34% — pressures (≈CoS) but does not race; pod plan is snowball +
  interaction. No swaps; 17/20 stands. Wrote `analysis/Earthbend_the_Meta_Clock_Lab_2026-06-13.md`;
  updated Summary + Deck_Index. Next: row 7, Lorehold Spirits.
- **2026-06-13** — **Deck 7: Lorehold Spirits.** Built `lor_clock_lab.py` (commander is a
  PW → mana-gate cast, the ebm gotcha applied up front). Claim "T7–9 (fastest T6, avg T8)"
  is **accurate as a DECAP window** — decap median **T8** (matches "avg T8" exactly; T7 = 46%
  strong front edge, T6 = 18%); 3rd deck after CoS/Earthbend with a non-optimistic front
  edge. Correction = decap/table conflation, but the **tightest gap yet (2 turns): table
  median T10** (never-in-14 decap 1% / table 5%). **Shape:** MIXED, both predictions held —
  focused combat (Quintorius −4 + anthems) + Balefire chip set decap; Purphoros `hit_all`
  + GB combo `kill_all` pull the table to only +2 (vs esc's +4). The carried prior worked.
  **Card-text correction (Stage 0):** Summary's Line-6 combo said Karmic Guide "persist
  returns it" — KG has **Echo, not persist**; loop runs off Reveillark's leave-trigger +
  KG's ETB (unbounded, no model impact); fixed in the Summary. **Model correction (consistency
  omission, slow-bias):** v1 omitted Quintorius +1 (draw 2/turn) → decap T9 / 35% never-table;
  adding the +1 dig → decap T8 / 5% never-table — same class as ebm/cs/lw under-modeling, the
  +1 is a verified ability so faithful. Pod bar: decap T≤7 = **46%** — highest pressure of the
  mixed decks, nearly races. No swaps; 18/20 stands. Wrote
  `analysis/Lorehold_Spirits_Clock_Lab_2026-06-13.md`; updated Summary + Deck_Index. Next:
  row 8, The Calamity Tax (PARTIAL — speed-curve done, needs kill-turn clock).
- **2026-06-13** — **Deck 8: The Calamity Tax** (last PARTIAL) + **version bake-off.** Discovered
  `ct_speed_lab.py` was ALREADY a kill-turn clock lab (built 2026-06-10) that never ran — it
  crashed on a Windows cp1252 `◐` print, so its referenced writeup never existed and the row
  stayed PARTIAL. Fixed the glyph, added the missing V3 (06-01 Witherbloom) variant + affinity
  model, ran it. **"T7–9" is the biggest falsification in the sweep:** V1 committed decap median
  **T13 / table never-in-14** (47% killed). The deck is hard **mana-gated** (X-drain wants ~16
  mana); reanimator's "T5–6 fast line" also falsified (god-hand). CONVERGE shape (hit-all drain).
  **Caveat:** strict floor EXCLUDES Seedborn Muse (the deck's mana multiplier) + flash — so T13 is
  a conservative floor (à la LW); real clock faster but decisively not T7–9, and cannot out-race
  the T6–7 pod. **4-version bake-off:** V1 47% / V2 49% / V3 50% / V4 56% killed-in-14 — swaps move
  the kill RATE not the TURN (all T12–13). **Ownership reality decisive:** collection holds 1 of
  every relevant card (prior "owned spare" claims stale); **V3 impractical** (Witherbloom is now
  Zero-Sum's commander), **V4 mostly Loam-freed but Scarab=Curse commander locked** (~$15–30).
  **User decision: none up to par — stay on committed V1, no version applied; a DIFFERENT
  improvement direction needed (not these swaps), deferred to a later session.** No card-text errors.
  Wrote `analysis/Calamity_Tax_Kill_Turn_Lab_2026-06-13.md`; updated Summary + Deck_Index. **Sweep
  TODO/PARTIAL now: 2 left (Ms. Bumbleflower, The Dark Lord's Army).**
- **2026-06-13** — **Deck 9: Ms. Bumbleflower.** Built `bmf_clock_lab.py`. Claim "T8–10" decap
  **corroborated but as a CEILING** — decap median **T8** (T7 = 38%), in-band, front edge ~holds
  (4th non-optimistic front edge). **table median T11** (3-turn diverge = the deck's "out-values,
  under-closes" identity). **Inverse-of-LW caveat:** the goldfish *over-credits* this control deck
  by dumping its ~15 interaction pieces proactively for Bumbleflower triggers (counters/Cats/Jolrael
  hand-size); real play holds them up → slower than T8. Jolrael alpha ({4}{G}{G}, board → X/X, X =
  hand, Reliquary Tower = big hand) is the decap; Willbreaker theft is goldfish-invisible (no opp
  board). Combat-diverge prediction held. No card-text errors. No swaps; 15/20 stands. Wrote
  `analysis/Ms_Bumbleflower_Clock_Lab_2026-06-13.md`; updated Summary + Deck_Index. Next: row 10,
  The Dark Lord's Army (last).
- **2026-06-13** — **Deck 10: The Dark Lord's Army — SWEEP COMPLETE.** Built `dla_clock_lab.py`.
  **Unique: the engine is OPPONENT-DRIVEN** (Sauron amasses on opp spells; Sheoldred/Underworld
  Dreams/Bowmasters drain on opp draws; Wound Reflection doubles their loss) — a self-contained
  goldfish would show "never" and misrepresent it, so modelled vs an explicit **pod-activity
  assumption** (like `delay_lab.py`), at LOW/MID/HIGH tempo. **decap T8–10 / table T11–15 by
  tempo** (typical MID: decap T9 / table T12). **Claim "T8–10 / interaction T10–12" well-
  corroborated** — among the LEAST-falsified in the sweep; new finding is the tempo-dependence
  (kills FASTER vs active pods — the amass/drain feed on opponents) + the decap/table split.
  Drain hit_all (converge, the win) + Army voltron focus (decap). vs the documented spell-dense
  Abolisher pod it's at its fastest (T8/T11) but still out-grinds rather than races (19/20 = its
  Durability/Interaction). No card-text errors; no swaps; 19/20 stands. Wrote
  `analysis/Dark_Lords_Army_Clock_Lab_2026-06-13.md`; updated Summary + Deck_Index.

**SWEEP COMPLETE — all active roster decks carry a measured kill-turn clock.** See the RANKING +
closing note below.

---

## RANKING — roster by measured decap clock

Fills in as the sweep completes. Sorted fastest decap first; ties broken by table
clock then never-in-12. `—` = not yet measured. Final deliverable of the campaign.

| Rank | Deck | Decap | Table | Never-in-12 (table) | Score | Kill shape |
|---:|---|---|---|---|---|---|
| 1 | The Genome Project | T7 | T8 | — | 15/20 | drain/ping (converge) |
| 2 | Radiation Sickness | T7 decap | T10 | 1% | 18/20 | counter-engine (combo/Simic/Triumph converge; combat decap leads) |
| 3 | The Replication Crisis | T7 (med) | T10+ | — | 17/20 | combat focus-fire |
| 4 | The Exile's Return | T8 (med) | T10 | — | 17/20 | combat focus-fire |
| 5 | Lorehold Spirits | T8 | T10 | 15% | 18/20 | MIXED: Quintorius−4+anthem combat & Balefire focus decap / Purphoros hit-all + GB combo kill_all table (+2 gap) |
| 6 | Curse of the Scarab | T8 | T11 | 9% | 17/20 | combat decaps / Scarab+Gary drain tables (mixed; **decap claim held**) |
| 7 | Ms. Bumbleflower | T8 | T11 | 18% | 15/20 | combat focus (Jolrael alpha) — **decap a goldfish ceiling** (proactive interaction dump); Willbreaker theft invisible |
| 8 | Earthbend the Meta | T8 | T12 | ~30% | 17/20 | MIXED→diverge: AWBO+combat focus decap / Purphoros+Tremors hit-all ping tables (snowball) |
| 9 | Eldrazi Stampede Chaos | T8 | T12 | 33% (v2) | 14/20 | combat focus-fire / Craterhoof alpha (amplifiers: tail only) |
| 10 | Zero-Sum Game | T9 | T9 | — | n/a | lifeloop (converge) |
| 11 | The Dark Lord's Army | T9 | T12 | 42% | 19/20 | **opponent-driven** — drain hit-all (converge) + Army focus; tempo-dependent (decap T8–10 / table T11–15; kills faster vs active pods) |
| 12 | Diminishing Returns | T9 | T12+ | — | 17/20 | aristocrat drain |
| 13 | Lightning War | T9 | ~T13 | 40% | 19/20 | burn chip + X-spell fork (**strict goldfish; tempo/disruption understated — real clock faster**) |
| 14 | The Grand Design | T10 (med) | T12+ | — | 19/20 | combat (96%) |
| 15 | Crystal Sickness | T11 | T13 | 34% (upper bd) | 17/20 | artifact drain + Tezzeret (converge) / combat decap (mixed) |
| 16 | The Calamity Tax | T13 | never (>T14) | ~69% | 18/20 | mana-gated converge drain (**strict floor; 2026-06-13 dig test found this UNDER-modeled Glarb's selection — realistic ~T8–10, not T13; see Calamity direction doc**) |

**Reading the ranking — the framework's thesis confirmed.** The clock order and the Score
column disagree, and the disagreement is systematic:

- **Only 3 decks clear the decap-T≤7 pod bar** — Genome (15/20), Radiation (18/20),
  Replication (17/20) — and **not one is a top-score (19/20) deck.** The fastest racers are
  mid-scored; the highest-scored decks are the slowest.
- **The four 19/20 decks all sit in the slow half:** Lightning War (T9/~T13), Dark Lord's Army
  (T9/T12), The Grand Design (T10/T12+), and the 18/20 Calamity Tax is dead last (T13/never).
  These are the **high-score / slow-clock fortresses** — the signature gap. They score on
  Durability + Interaction (grind/inevitability), which the Conversion Check rewards, but they
  do **not** race.
- **No deck both races (decap T≤7) and scores 19/20.** Speed and Conversion-Check score are
  anti-correlated at the top: the rubric's "best" decks win by out-grinding, not out-racing —
  which is precisely why a T6–7 combo pod behind Grand Abolisher is the roster's hard matchup
  (nothing out-races it, and even the fast decap decks table at T10+). The framework's founding
  claim — score and clock are uncorrelated in the 15–19 band — is borne out: a 14/20 (Eldrazi)
  and an 18/20 (Lorehold) share the same T8 decap, while 19/20s span T9–T13.
- **Read the caveats, not just the column:** Lightning War + Calamity Tax are penalized by
  strict-goldfish floors (no Seedborn/disruption modelled → real clocks faster); Dark Lord's
  Army is tempo-dependent (faster vs active pods); Bumbleflower's decap is a proactive-cast
  ceiling. The order is by **decap median**; the Kill shape column carries the real texture.

**Sweep complete (2026-06-13):** 16 active decks, all clock-labbed. 7 of the 8 hand-estimated
windows tested came back optimistic on the *single number* (the recurring decap/table
conflation), but the *decap* front edge held for CoS / Earthbend / Lorehold / Bumbleflower /
Dark Lord's Army (5 of the last 6) — the optimism is concentrated in conflating decap with table
and in true outliers (Calamity Tax "T7–9" → T13). Process wins banked: the producer-inventory
WF step, the commander-mana-gate gotcha, and the "hit_all doesn't converge if a focused axis
leads" shape rule.

---

## Related

- `workflows/WF_Kill_Window_Lab.md` — the per-deck procedure.
- `campaigns/Framework_Clock_Gap_2026-06-09.md` — why the sweep exists; the rule.
- `REF_The_Conversion_Check.md` — Verification rule + Clock annotation format.
- `Pod_Matchup_Matrix.md` — the Race/Disrupt/Both verdicts the clock feeds.
- `project_pod_combo_opponent` (memory) — the T6–7 pod the bar is set against.
