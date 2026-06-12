# Candidate Bake-Off — Pick-One Build Decision (2026-06-12)

**What this is:** the working tracker *and* method for choosing **ONE** deck to build from
**9 candidates** — 7 internal proposals + 2 external expert-built lists. This doc is
**resumable**: if usage/context runs out, restart from the Status table's "next action" column.

**Status (2026-06-12):** Planning complete. **Execution NOT started** — no card-text sweeps, GC
counts, builds, or labs have been run yet. Everything below the funnel is the plan, not results.
**Next action: Stage 0.**

**Owner model:** Opus 4.8 for the judgment that carries risk — card-text reads, lab kill-logic
design, Conversion Check, verdict. It is the lineup's *most capable* reasoning model and the
**documented author of the clock-lab falsifications** (every clock-lab commit carries
`Co-Authored-By: Claude Opus 4.8`, git trailers 2026-06-10; "Fable" appears nowhere in the repo
except card names). Sonnet subagents for mechanical fetch/run.
**Fable — open question (user, 2026-06-12):** the user rates Fable for catching optimistic clocks.
The git record attributes that work to Opus, but trailers only capture commit-time config, not every
reasoning step — unresolved. Since the labs are **deterministic Python**, the low-risk place to
actually test Fable is the *skeptical read of lab output* and *verdict prose*; **card-text reads and
lab kill-logic stay on Opus** (this repo's failure mode is hallucinated card text — not a place for a
hunch). My earlier "Fable is creative-tuned" was an inference from the name, not a citable fact.

---

## The brief (what every candidate is judged against)

- Reliable kill **~T6–7**; beat the recurring pod combo deck ([[project_pod_combo_opponent]]).
- Bracket-4 **in spirit**, hard **3-GC cap** for OUR builds. **Externals are exempt** from the cap
  (Witherbloom-comparison precedent) — count their GCs to set bracket, don't "flag and stop."
- **On-your-turn / Abolisher-proof kill preferred** — counterspell-based protection is illusory vs
  Grand Abolisher ([[feedback_grand_abolisher_blocks_counters]]); static hate + activated kills win.
- **Protected donors off-limits:** Lightning War, Calamity Tax, Grand Design, Genome Project,
  Zero-Sum Game. "Cheap" = *buys*, not pulls from these.

---

## The 8 candidates

| # | Candidate | Type | Archetype | Decklist exists? |
|---|---|---|---|---|
| 1 | Yuriko — *Insider Trading* | internal proposal | Dimir ninja-tempo + Thoracle/Consult | No (prose shell) |
| 2 | Godo — *Hostile Takeover* | internal proposal | mono-R Helm turbo (1-card combo) | No (prose shell) |
| 3 | Urza — *Planned Obsolescence* | internal proposal | artifact stax-combo | No (prose shell) |
| 4 | Kinnan — *Quantitative Easing* | internal proposal | Simic mana-combo → Ballista | No (prose shell) |
| 5 | Korvold — *Asset Stripping* | internal proposal | Jund treasure-combo | No (prose shell) |
| 6 | Thrasios+Tymna — *Mergers & Acquisitions* | internal proposal | throttled cEDH (4–5C) | No (prose shell) |
| 7 | **Clive, Ifrit's Dominant** | **external (built)** | mono-R devotion / wheel / discard payoff | **Yes — 100 cards** |
| 8 | **Kefka, Court Mage** *(external)* | **external (built)** | Grixis combo-control (budget $100) | **Yes — 100 cards** |
| 9 | **Kefka, Court Mage** *(internal)* | internal proposal | Grixis forced-draw **burn** (anti-Abolisher pod answer) | No (prose shell) |

> **Same-commander head-to-head (user, 2026-06-12):** both Kefka builds are in. #8 is the external
> *combo-control* list; #9 is our internal `PROP_Kefka_Court_Mage.md` (2026-05-31) — a Grixis
> *forced-draw burn* deck whose kill resolves on **your** turn (wheel + static punishers,
> Notion Thief + Psychosis one-wheel), explicitly designed as an *anti-Abolisher* answer. They share
> a commander and nothing else; keep them clearly separate in the verdict. Note #9 may actually
> **score well on brief-fit** (on-your-turn kill, static hate) where #8 scores poorly (self-declared
> non-turbo, Abolisher-illusory counters) — the comparison of the two is a highlight of this bake-off.

---

## Scope decision (user, 2026-06-12)

**The two external builds ride all the way to the lab — they are NOT eligible for a Stage-1 brief
cut.** Rationale: expert-crafted, already 100 cards, and their lab clocks calibrate what "good" looks
like and stress-test whether the brief's T6–7 bar is even right. They are still *scored* on brief-fit
(e.g. Kefka self-declares "NOT a turbo… longer game," and leans on Abolisher-illusory counters), but
a poor brief-fit does **not** remove them.

Consequence: labs needed = (internal Stage-1 survivors) **+ both externals**.

---

## The funnel (cheap → expensive; pick-one means triage, not 8 equal builds)

**Stage 0 — Normalize (ALL 8).** *Cheap, mandatory.*
- Card-text verify the two externals via `card_lookup.py` — dump **raw oracle verbatim**, no
  pattern-matching. Clive has the most unfamiliar/UB cards (PuPu UFO, Matzalantli, Brass's
  Tunnel-Grinder, Decaying Time Loop, Helm's Deep…); Kefka is FF/UB-heavy too.
- **Reskin-alias check** ([[feedback_read_card_first]], `REF_Reskin_Aliases.md`) before any
  unowned/buy line.
- **GC count** for all 8 against `REF_Game_Changers_List.md` *including the Removed section*. Sets
  bracket; for internals checks the 3-GC cap.
- Externals only: 100-card / duplicate / color-identity legality.

**Stage 1 — Brief screen (7 INTERNALS only; both externals auto-advance).** *Cheap, decisive.*
Score each internal on: brief-fit (does it try to race T6–7?), completability-from-collection
(buys vs *contested* pulls — protected donors are off-limits), Abolisher-resilience, structural
Conversion Check. Cut the weakest internals; keep ~3–4. (Internal Kefka #9 is an internal — it gets
screened here, and is the natural side-by-side with external Kefka #8.)

**Stage 2 — Build decklists (internal survivors).** *Medium.* Externals already built.
Resolve 99+1 from collection + buys; count to exactly 100; verify cross-deck availability
([[feedback_card_availability_check]]). Finalized builds → dated `.txt` under `decks/`, commander in
a **separate END block** (line-1 breaks the parser — ZSG finding).

**Stage 3 — Clock labs (internal finalists + BOTH externals).** *Expensive, mandatory for any
kill-window claim.* One `*_clock_lab.py` per finalist on `speed_lab_core.py`. Report **decap AND
table** turns separately. **Reuse the kill scaffold:** Godo & Clive share a mono-red combat/burn
goldfish core; Kinnan/Urza/Korvold/Thrasios share a "resolve engine → infinite → outlet" shape;
Kefka is combo-control; Yuriko is a ninja chip-clock. Commit the labs to `scripts/` (no `_tmp_`
throwaways — [[feedback_store_analysis_scripts]]).

**Stage 4 — Verdict doc.** *Cheap, the deliverable.* Head-to-head ranking → recommend ONE. Format
like `Witherbloom_External_Build_Comparison.md`: brief-fit, lab clock (decap/table cited),
Conversion Check, GC/bracket, completability/cost (prices unverified unless checked), pod matchup,
honest weaknesses.

---

## Model allocation

| Work | Model | Why |
|---|---|---|
| Brief-fit, Conversion Check, **lab kill-logic design**, verdict | **Opus 4.8 (inline)** | Where a misread card / conflated clock becomes a bad pick. |
| Card-text sweeps (raw oracle verbatim), GC cross-checks, availability greps, legality, **running labs + tabulating** | **Sonnet subagents** (sparingly, parallel) | Voluminous, verifiable; must return *raw* text so Opus interprets. |
| Skeptical read of lab output, verdict prose | Opus default; **Fable** candidate to A/B | Lab output is deterministic → low-risk place to test Fable's clock-skepticism (user-rated). |
| — | not Haiku (pattern-match risk on card text) | — |

---

## Wired-in guards (lessons that must not be re-learned)

1. **Don't trust the proposals' self-clocks.** 7 of 8 prior labs *falsified* hand-estimates, all
   optimistic ([[project_framework_clock_gap]]). The lab is the arbiter; **decap ≠ table**, state both.
2. **`color_identity` sim bug.** Never read `color_identity` as colours-produced — it scores
   fetches/rainbow lands as zero-colour ([[project_grand_design_mana_pass]]). Bites multicolor bases
   hardest → Korvold (Jund), Thrasios+Tymna (4–5C), Kefka (Grixis). Use `produced_mana` + FETCH_TYPED.
3. **Fast mana is often flat** in cheap-assembly combo decks ([[project_diminishing_returns_b4_pivot]]);
   don't let Urza/Korvold/Thrasios win on a "turbo" claim the lab won't support. Kinnan is the
   exception (gate genuinely is land-commander-then-artifact).
4. **Grand Abolisher kills counter-protection.** Strike against Kefka-external for this pod that a raw
   power ranking misses; favour on-your-turn activated kills + static hate.
5. **Externals exempt from the 3-GC cap** (count GCs, don't stop).
6. **Reskin-alias check before any unowned/buy line.**
7. **Prices in buy-lists are unverified** — flag or check ([[feedback_verify_prices]]).

---

## Status table (resumable — update as stages complete)

| # | Candidate | GC count | Brief-fit | Decklist | Lab | Clock (decap / table) | Stage | Next action |
|---|---|---|---|---|---|---|---|---|
| 1 | Yuriko | TBD | TBD | — | — | — | pre-0 | Stage 0 |
| 2 | Godo | TBD | TBD | — | — | — | pre-0 | Stage 0 |
| 3 | Urza | TBD | TBD | — | — | — | pre-0 | Stage 0 |
| 4 | Kinnan | TBD | TBD | — | — | — | pre-0 | Stage 0 |
| 5 | Korvold | TBD | TBD | — | — | — | pre-0 | Stage 0 |
| 6 | Thrasios+Tymna | TBD | TBD | — | — | — | pre-0 | Stage 0 |
| 7 | Clive (ext) | TBD | TBD | ✓ built | — | — | pre-0 | Stage 0 text+GC |
| 8 | Kefka (ext) | TBD | TBD | ✓ built | — | — | pre-0 | Stage 0 text+GC |
| 9 | Kefka (int, burn) | TBD | TBD | — | — | — | pre-0 | Stage 0 |

**Next action overall:** run **Stage 0** across all 9 (card-text verify the two externals, GC-count
all 8, legality-check the externals), then fill GC/legality columns and proceed to Stage 1 on the
internals.
