# Candidate Bake-Off — Pick-One Build Decision (2026-06-12)

**What this is:** the working tracker *and* method for choosing **ONE** deck to build from
**9 candidates** — 7 internal proposals + 2 external expert-built lists. This doc is
**resumable**: if usage/context runs out, restart from the Status table's "next action" column.

**Status (2026-06-12):** **Stage 0 complete. Stage 1 complete** — 5 survivors (Yuriko / Godo /
Kinnan / Kefka-burn / **Korvold**, kept by user override), 2 cuts (Urza / Thrasios+Tymna).
**Stage 2: COMPLETE (5 of 5)** — Yuriko (`insider-trading-20260612.txt`, fixed from 99→100 with
Temple of Deceit), Godo (`hostile-takeover-20260612.txt`, 100 ✓), Kinnan
(`quantitative-easing-20260612.txt`, 100 ✓ — GC slot 3 swapped Survival→**Worldly Tutor**; see
Stage 2 results for falsified free-claims + cost revision), Kefka-burn
(`forced-liquidation-20260612.txt`, 100 ✓ — Demonic Tutor now a BUY (ZSG took the last spare),
cost revised ~€140–190), Korvold (`asset-stripping-20260612.txt`, 100 ✓ — GC slot swapped
Survival→**Worldly Tutor**, ~€50 cost claim HOLDS, the only candidate whose estimate survived
the sweep). **Next action: Stage 3 clock labs** (refresh Scryfall data before Clive's).

**Owner model — REVISED 2026-06-12 (user flagged the original as compromised).** The first
version of this section was Opus-4.8-authored and the user reports it **hallucinated its claims
about Fable**. Specific failures, kept here so they aren't re-learned: (1) *circular
self-attribution* — its evidence for "Opus owns the risk work" was git trailers crediting Opus,
in a doc Opus wrote, while admitting trailers only capture commit-time config; (2) "Fable is
creative-tuned" was an admitted invention from the name, retracted — but the allocation derived
from it was kept; (3) "lineup's most capable reasoning model" was uncited self-assessment;
(4) "'Fable' appears nowhere in the repo" is now false — commits `479c9cc`/`f9acfff` (Stage 2,
2026-06-12) carry Fable 5 trailers, on **the card-text-read work Opus reserved for itself**, and
the discipline held (two SOS prepared-card traps, the Dictate/Ellie's-Rage proxy catch, 5+
falsified free-claims, clean GC caps and exact-100s).
**Stage 3 allocation (evidence-based):** **Fable 5, high effort**, for lab kill-logic design +
skeptical read of lab output + verdict (basis: the user's first-hand rating — Fable catches
optimistic clocks — plus the Stage 2 track record). **Sonnet subagents** for mechanical lab
runs/tabulation (deterministic, verifiable). **Opus 4.8 = optional controlled A/B arm**:
independently design ONE lab's kill logic and diff — settles attribution with data, not either
model's self-assessment. Not Haiku. *Symmetry caveat: this revision was written by Fable 5 —
same conflict-of-interest shape; basis is externally checkable (user observation + commits), and
the user arbitrates.*

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

*(Revised 2026-06-12 — see "Owner model" above for why the original Opus-authored split was
discarded.)*

| Work | Model | Why |
|---|---|---|
| **Lab kill-logic design**, skeptical read of lab output, Conversion Check, verdict | **Fable 5 (inline, high effort)** | User-rated for catching optimistic clocks; Stage 2 proved the card-text discipline on this repo's actual failure mode. |
| Card-text sweeps (raw oracle verbatim), GC cross-checks, availability greps, legality, **running labs + tabulating** | **Sonnet subagents** (sparingly, parallel) | Voluminous, verifiable, deterministic; must return *raw* text for the owner model to interpret. |
| Optional A/B arm: independently design ONE lab's kill logic, diff against Fable's | Opus 4.8 | Settles the Fable/Opus attribution question with a controlled comparison, not self-assessment. |
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

## Stage 0 results (2026-06-12)

**Method:** `card_lookup.py` (local Scryfall, snapshot dated **2026-06-01**) for raw oracle text;
GCs cross-checked against `REF_Game_Changers_List.md` (Feb 2026) *including* the Removed section;
delisted commanders confirmed still delisted; externals counted + duplicate-checked + color-identity
swept by script.

### GC counts — all 9

| # | Candidate | GCs | The cards | Verdict |
|---|---|---|---|---|
| 1 | Yuriko | **3/3** | Thassa's Oracle, Mystical Tutor, Demonic Tutor | cap-OK; Yuriko delisted 2025-10-21 = 0 |
| 2 | Godo | **3/3** | Mana Vault, Grim Monolith, Gamble | cap-OK; Godo never listed = 0 |
| 3 | Urza | **3/3** | Mana Vault, Grim Monolith, Chrome Mox | cap-OK; Urza delisted 2025-10-21 = 0 |
| 4 | Kinnan | **3/3** | Mana Vault, Grim Monolith, Survival of the Fittest | cap-OK; Kinnan delisted 2025-10-21 = 0 |
| 5 | Korvold | **3/3** | Survival of the Fittest, Gamble, Mana Vault | cap-OK; Korvold never listed = 0 |
| 6 | Thrasios+Tymna | **3/3** | Thassa's Oracle, Mystical Tutor, Drannith Magistrate | cap-OK; both partners non-GC = 0 |
| 7 | Clive (ext) | **3** | The One Ring, Underworld Breach, **Jeska's Will** (= "Storm's Will" reskin) | exempt; Wheel of Fortune & Sol Ring are NOT GCs |
| 8 | Kefka (ext) | **0** | — | exempt; self-declared 0 GCs, confirmed (nothing on list) |
| 9 | Kefka (int, burn) | **3/3** | Notion Thief, Demonic Tutor, Mana Vault | cap-OK |

All 10 distinct GC names across the internals are on the current list; none fell under the Removed
heading. No internal exceeds the 3-GC cap. **Bracket read:** externals exempt — Clive's **3 GCs**
(the Jeska's Will reskin counts) + fast-mana/Wheel suite read solidly **bracket 4**; Kefka-ext at
**0 GCs** is bracket-3-by-count but bracket-4-in-spirit by combo density (its own primer's claim,
and the brief's guard #4 stands).

### External legality

- **Clive — 100 cards ✓** (99 + commander). Only repeated card is **27× Mountain** (legal basic);
  no illegal duplicates. **Clive is a DFC** — "Ifrit, Warden of Inferno" is its *back face*
  (`{4}{R}{R}` 5/5 front, devotion-to-red wheel ETB), **not** a 100th card; the primer's separate
  "Ifrit" bullets describe the flip side. Color identity **R**. Five names raised flags at sweep
  time; **all RESOLVED 2026-06-12 via user-confirmed reskin aliases** (appended to
  `REF_Reskin_Aliases.md`):
  1. **Morgul-Knife = Shadowspear** (colorless equipment, +1/+1 trample/lifelink). The bare name
     fuzzy-matches a *different* real card, **Morgul-Knife Wound** (`{1}{B}` aura, CI B), which would
     be illegal mono-red — so this name must always be resolved via the alias, never the raw lookup.
  2. The four cards absent from the 2026-06-01 snapshot resolve to: **Storm's Will = Jeska's Will**
     (CI R, **and a Game Changer → Clive is 3 GCs**), **Helm's Deep = Shinka, the Bloodsoaked Keep**
     (red land), **Wakandan Skyscraper = Karn's Bastion** (colorless proliferate land), **Calliope's
     Song = Seething Song** (red ritual). *(Still run `update_scryfall_data.py` before the lab so the
     raw cards verify directly — but the targets are known and all red/colorless.)*
  3. **Net: Clive is 100% color-identity-legal mono-red, exactly 100 cards, 3 GCs — clean for Stage 3.**
- **Kefka (ext) — 100 cards ✓.** Only repeats are basics (3× Island, 4× Mountain, 2× Swamp); no
  illegal duplicates. Color identity **Grixis (BUR)** — every verified card sits within B/U/R or is
  colorless; no off-color leak. Commander text matches the internal proposal's verified read.
  **Combo pieces all verified real** (oracle-checked, loops mechanically sound): Dualcaster Mage +
  Electroduplicate/Twinflame → infinite hasty tokens; Dualcaster + Ghostly Flicker (+Kefka) → infinite
  mana/flicker; Rionya + Combat Celebrant / Fear of Missing Out → infinite combats; Harmonic Prodigy
  doubles Wizard/Shaman triggers (Kefka, Rionya, DCM). "________ Goblin" is a real card (Creature —
  Goblin Guest, CI R, legal). No hallucinated-card risk in this list.

---

## Stage 1 results (2026-06-12) — brief screen of the 7 internals

Scored **structurally**, not on the proposals' self-clocks (guard #1: 7/8 prior labs falsified
optimistic hand-estimates). Kill-*shape* lens from the lab record: a trigger that drains **all
opponents simultaneously** converges decap≈table (Genome shape — the only clock that ever held);
**combat** focus-fire diverges 2–3 turns; a **3-mana on-cast** combo is decap=table by definition.

| # | Candidate | Brief-fit (race T6–7? + kill shape) | Completability (buys / pulls) | Abolisher-resilience | Struct. CC (est, unverified) | Screen |
|---|---|---|---|---|---|---|
| 1 | **Yuriko** | **Strong** — dual clock: Yuriko's trigger drains **all opp** (Genome shape) **+** 3-mana Thoracle/Consult on-cast backup | ~€140–170 buys; ~0 protected-donor pulls (binder spares) | **Strong** (ninjutsu + triggers + own-turn Thoracle) | ~17–18 | **KEEP** |
| 2 | **Godo** | **Moderate** — 1-card combo, fastest *ceiling*; but **combat** (diverges) + glass mono-R, removal between land & swing = lost cycle | **Cheapest ~€45–60**; 3 GCs free; 0 pulls | Combo Abolisher-*irrelevant* but **no protection** (glassy) | ~15–16 | **KEEP** (speed/cost data point) |
| 3 | Urza | **Weak on speed** — explicitly "doesn't race"; stax delays pod, combo kills mid | ~€55–75 **+ mandatory pull of Urza from Crystal Sickness (17/20 Elite)**; stax politics | Strong (statics + own-turn combo) | ~15–17 | **CUT** |
| 4 | **Kinnan** | **Strong** — 2-card (1-from-99), turbo; ∞ mana → Ballista pings **all opp** (table kill); blue protection | ~€45; Basalt ×2 + 3 GCs free; contested pieces **bought not pulled** | **Strong** (activated ping, own turn + blue protection) | ~16–17 | **KEEP** |
| 5 | Korvold | **Weak on speed** — self-ID'd "resilient, grindy… not fastest," median ~T7–9 (the slow DR shape); 4-piece assembly | ~€50; 0 pulls | Strong | ~16–17 | **KEEP** (user override 2026-06-12 — grindy profile chosen deliberately) |
| 6 | Thrasios+Tymna | **Mixed** — cEDH ceiling fastest, but 3-GC throttle regresses median; **same Thoracle+Consult as Yuriko** | **Most expensive ~€140–180**; owns ~none; buys around protected donors | Strong (Drannith) but cap removes the free counters | ~18 ceiling / throttled lower | **CUT** |
| 9 | **Kefka (int, burn)** | **Strong** — purpose-built anti-Abolisher: wheel + **static** punishers fire *through* the lock; Notion Thief+Psychosis ≈28/opp one-wheel = table kill on **your** turn | ~$85–140 buys (premium wheels); commander free; Sauron donor (buy dupes; not protected) | **Strongest** (statics = the one axis Abolisher can't switch off) | ~17 (Durability 3/5 caps) | **KEEP** |

**CONFIRMED survivors (5, user 2026-06-12): Yuriko, Godo, Kinnan, Kefka-burn, Korvold.** The four
recommended span distinct shapes (tempo-chip+cheap-combo, mono-R 1-card combat turbo, Simic 2-card
mana→table-ping, anti-Abolisher static burn); **Korvold was kept by user override** — the grindy/
resilient profile (median ~T7–9 by its own proposal) was a deliberate choice, and its all-opponent
aristocrats drain is a genuinely different shape worth labbing. Its mechanical-distinctiveness vs.
DR/Genome/ZSG remains the open gate for the Stage-4 verdict.

**CONFIRMED cuts (2) and why:**
- **Urza** — weakest brief-fit on the *racing* ask (its thesis is the anti-race); requires the only
  **mandatory Elite-deck pull** of any candidate (its own commander out of Crystal Sickness, 17/20);
  stax carries table feel-bad. Kefka-burn already fills the "beat the pod by non-racing means" slot
  without a pull or stax politics.
- **Thrasios+Tymna** — **most expensive**, owns almost none of its core, and the **highest political
  risk** (the proposal itself: "if the pod is going to decline any candidate, it's this one"). Its win
  is the *same* Thoracle+Consult line Yuriko runs — but Yuriko does it cheaper, on a delisted-GC
  commander, behind a legitimate fair combat face. Redundant-but-worse against a kept candidate.

---

## Stage 2 results (2026-06-12) — builds + availability sweeps

**Method:** every card checked against `moxfield_haves_2026-06-07-1031Z.csv` (note: predates the
ZSG build, so ZSG-deployed cards can read owned:0) + all active `decks/*.txt`; reskin-alias check
run on every unowned name (no rescues — all genuine); card texts of combo-critical/unfamiliar
cards re-verified via `card_lookup.py`. Sibling-candidate claims (the other `considering/` builds)
do **not** block availability — pick-one means at most one gets built.

### Yuriko — `insider-trading-20260612.txt` (100 ✓)

- **Was 99 cards** (98+commander) as left by the prior session; fixed by adding **Temple of
  Deceit** (owned ×5, all spare; scry feeds the Yuriko reveal; uniquely named, so Tainted-Pact
  name-singleton discipline holds — the whole list is strict singleton incl. snow basics).
- Sweep confirms the proposal's cost shape: ~23 ninja/enabler cards + Thoracle/Consult/Pact all
  unowned; staples 0-spare (Demonic Tutor 4/4, Mana Drain 4/4, Polluted Delta 10/10, Sensei's Top,
  Baleful Strix). **~€140–170 buys claim stands (prices unverified).**

### Godo — `hostile-takeover-20260612.txt` (100 ✓)

- Sweep: **~30 unowned + ~12 zero-spare** incl. Helm of the Host, Hammer of Nazahn, Terror of the
  Peaks, Seasoned Pyromancer, Birgi — and the sole **Imperial Recruiter** copy is deployed.
  Mono-red support is cheap, but the **~€45–60 estimate looks light**; flag for Stage 4 re-cost
  (prices unverified). 3 GCs (Vault/Monolith/Gamble) genuinely free ✓ (Grim Monolith's 1 copy is
  claimed only by no other *active* deck).

### Kinnan — `quantitative-easing-20260612.txt` (100 ✓) — built this session

- **GC slot 3 swapped: Survival of the Fittest → Worldly Tutor** (owned ×1, undeployed = free).
  Survival's "owned, free" claim was **falsified** — its sole copy is IN
  `radiation-sickness-20260513-phaseC.txt`. GC count stays **3/3** (Mana Vault, Grim Monolith,
  Worldly Tutor). Card-text correction: **Worldly finds CREATURE cards only** — it fetches
  Ballista/dorks/Selvala, *not* Basalt (proposal said it could); artifact tutors
  (Whir/Fabricate/Reshape) cover Basalt.
- **⚠️ SIDE FINDING, outside bake-off scope: Radiation Sickness runs 4 GCs** (Survival of the
  Fittest + Seedborn Muse + Vampiric Tutor + Cyclonic Rift) — a standing 3-GC-cap violation,
  flagged to user 2026-06-12, unresolved.
- **Finale of Devastation = BUY**: proposal's "1 of 4 copies free" falsified — CSV shows 3 owned,
  and ZSG's build list marks its copy "(owned)" = it took the last binder spare (all 3 now in
  protected decks: Calamity / GD / ZSG).
- **Selvala = BUY**: "owned, free" falsified — sole copy deployed in Eldrazi Stampede (active,
  not protected; pulling is possible but defaulted to buy-don't-pull).
- Other falsified spares: Swiftfoot Boots ("×3 spares" → 0), Fellwar Stone (10/10 deployed);
  Bloom Tender 3rd copy + Walking Ballista 2nd copy confirmed as buys per proposal.
- **Budget swaps**: Nykthos, Lotus Field, Flooded Grove → basics (8 Forest / 5 Island). All three
  were unowned-or-locked buys with marginal synergy (Kinnan doesn't trigger on lands; only
  Vorinclex VoH cares). Lab/post-pick tuning can re-add.
- Combo math re-verified: Freed/Pemmin + Bloom Tender or Incubation Druid under Kinnan = infinite
  (pay {U}, net ≥+1); Staff/Mantle + Selvala needs board power ≥4; **Wall of Roots doesn't tap**
  (no Kinnan trigger, no aura combo — defensive ramp only). No protected-donor pulls; Elvish
  Mystic the only ZSG-overlap dork owned spare, rest of the dork package = cheap buys.
- **Cost revision: realistically ~€120–160 (unverified), NOT the proposal's ~€45.** The proposal
  assumed owned-free for Survival/Selvala/Finale/Boots and didn't enumerate ~35 unowned support
  cards (Spellseeker, Vorinclex VoH, Staff, Mantle, Sylvan Tutor, Botanical Sanctum…).
  **Kinnan is no longer tied-cheapest with Godo** — material for the Stage-4 verdict.

### Kefka-burn — `forced-liquidation-20260612.txt` (100 ✓) — built this session

*(Candidate #9 had no codename — filed as **Forced Liquidation**, in the proposal-codename theme;
rename trivially if disliked.)* Proposal's prose composition table summed to only ~90, so ~10 flex
slots were resolved per its own guidance (extra wheel/punisher redundancy, second sweeper).

- **GCs 3/3 unchanged** (Notion Thief / Demonic Tutor / Mana Vault — Stage 0 picks re-verified
  against the list incl. Removed section; **Deflecting Swat confirmed delisted** and added free,
  2 spares). But **Demonic Tutor is now a BUY**: owned 4 / deployed 4 (Calamity, Scarab, Sauron,
  **ZSG took the last spare**) — proposal's "multiple free copies" falsified. Kept as GC slot 2
  anyway (consistency is the deck's whole game; Yuriko's build buys it too).
- **Sheoldred = BUY.** The single binder spare exists (2 owned, 1 in Sauron) but the 2026-05-31
  Calamity Tax swap claims it — and that swap **was never applied to the ground-truth `.txt`**
  (deck file still dated 2026-04-05). Honored the prior paper claim; did not double-spend.
  Stage 4 can revisit if the CT swap is formally dropped.
- **Buy-don't-pull default held** for the Sauron raid (Underworld Dreams), Peace Offering
  (Psychosis Crawler), Genome (Peer into the Abyss), Lightning War (Past in Flames) — all BUYS.
- **Rock suite resolved 100% owned-free** by swapping five falsified "surplus" rocks (Fellwar
  10/10, Talisman of Indulgence 3/3, Talisman of Creativity −1, Jet Medallion → ZSG, Dark Ritual
  5/6) → Mind Stone / Thought Vessel (no-max-hand on-theme) / Commander's Sphere / Prismatic
  Lens / **Seething Song** (owned ×1 C21, free — the real ritual, not Clive's "Calliope's Song"
  alias; current oracle is an **instant**, adds {R}{R}{R}{R}{R}).
- **SOS find: `Naktamun Lorespinner // Wheel of Fortune` owned ×1, free** — per the SOS rule it
  is NOT Wheel of Fortune (3-mana 3/3 Jackal Wizard, prepares when a player has ≤1 cards in
  hand), but as an owned repeatable Wheel-copy caster it took a flex slot (displacing Pyroclasm,
  the weakest buy). Real Wheel of Fortune stays on the buy list as the marquee wheel.
- **Flex resolution (all texts verified):** punisher redundancy Ob Nixilis the Hate-Twisted /
  Kederekt Parasite / Glint-Horn Buccaneer (punishes *your* wheel-discards — hits each opponent) /
  **Bloodletter of Aclazotz** (doubles opponent life loss on your turn — turns a 2-punisher wheel
  ≈14/opp into ≈28 = table kill); wheel payoff Waste Not; static pod-hate **Cursed Totem** (shuts
  Kinnan/Hidetsugu/Kenrith activations; self-conflict with Magus of the Wheel sac + Glint-Horn
  draw flagged — deploy-order choice, ours to make); Dark Deal as 8th cheap wheel (with Notion
  Thief: opponents dump hands and redraw nothing). Wheel of Misfortune NOT added — proposal
  names it trim-first tier.
- **Genuinely free engine pieces confirmed:** Kefka (commander), Notion Thief, Mana Vault (2
  spare), Windfall, Magus of the Wheel, Deflecting Swat, Otawara, Reliquary Tower, Counterspell/
  Swan Song spares, Blasphemous Act, Lightning Greaves, Faithless Looting, Frantic Search,
  Thrill of Possibility.
- **Budget lands per Kinnan precedent:** 7 zero-spare/unowned duals (Spirebluff, Blackcleave,
  Darkslick, Dragonskull, Sulfurous Springs, Temple of Malice, Crumbling Necropolis) → basics;
  13 owned named lands + 23 basics. Niv-Mizzet Parun ({U}{U}{U}{R}{R}{R}) kept per proposal as
  flex/cut-first — the lean manabase strains it.
- **Alias check: no rescues** — all 38 unowned names are genuine buys. **Cost revision:
  realistically ~€140–190 (unverified), NOT the proposal's ~$85–140** — same failure shape as
  Kinnan/Godo: proposal under-counted deployed-elsewhere support (Demonic Tutor, Sheoldred,
  Boots, Chaos Warp, Go for the Throat, Ponder/Preordain, An Offer, Arcane Denial, Drown all
  0-spare) plus ~12 cheap unowned punisher/removal slots. Premium spend: Wheel of Fortune,
  Demonic Tutor, Sheoldred, Echo of Eons, Time Spiral, Bloodletter, Memory Jar.

### Korvold — `asset-stripping-20260612.txt` (100 ✓) — built this session

- **GC slot swapped: Survival of the Fittest → Worldly Tutor** (same falsification and same fix
  as Kinnan — Survival's sole copy is IN Radiation Sickness; Worldly owned ×1 undeployed = free,
  and arguably fits Korvold *better*: every payoff and engine creature is a creature card).
  GC tally **3/3: Worldly Tutor, Gamble (1 spare — 2 owned, 1 in Lorehold Spirit), Mana Vault.**
  The proposal's slot-3 lab A/B (Vault vs third tutor) stands for Stage 3.
- **~€50 cost claim HOLDS** — the only candidate whose Stage-1 estimate survived its sweep.
  13 buys ≈ €47 (unverified): Ashnod's Altar ~€15, Goblin Bombardment ~€10, Walking Ballista
  ~€8, Pitiless Plunderer / Sifter / Zulaport / Blood Artist / Viscera / Carrion / Deadly
  Dispute / Village Rites / Terminate / Bedevil ≈ €1–2 each. Zero land buys, zero pulls,
  no protected donor touched.
- **Proposal free-claims that held:** Korvold, Mayhem Devil, Marionette Master, Nadier's ×2,
  Reassembling Skeleton ×4, Gravecrawler spares — plus **Woe Strider turned out free** (2 owned,
  only 1 in DR; proposal had it as a buy). **Falsified:** Deadly Rollick "free" (6/6 deployed,
  ZSG took the last) — cut, not bought; Bitterblossom's free-add status (ZSG claimed it);
  Ashnod's "both copies" (CSV shows 1 owned — ZSG's is a post-CSV buy; the 2nd is a buy as
  proposed).
- **Dictate of Erebos ambiguity:** the CSV's only copy is **Proxy=True** and "Ellie's Rage"
  (its reskin, deployed in Sauron) has **no CSV row** — the proxy almost certainly IS Sauron's
  deployed copy. Not cleanly free → **Grave Pact (owned ×1, undeployed, unambiguous) took the
  slot.** Same effect, heavier pips.
- **Precision note on redundancy:** Sifter of Skulls' Scions make **{C} only** — it backs up
  the *value/draw* engine but can't pay Gravecrawler/Skeleton's {B}; only Pitiless Plunderer's
  Treasures make the loop fully self-sustaining. Payoff redundancy (5-wide) is real; *engine*
  redundancy is Plunderer-or-bust plus mana-assisted halves. Lab should model this.
- **Owned-spare flex haul** (~24 slots filled free): Meren, Mazirek, Tireless Tracker, Solemn,
  Burnished Hart, Whisper, Midnight Reaper, Dreadhorde Invasion, Victimize, Living Death,
  Eternal Witness, Professional Face-Breaker, Big Score, Pirate's Pillage, Curse of Opulence,
  Ichor Wellspring, Putrefy, Tear Asunder, Abrade, Feed the Swarm, Vandalblast, Heroic
  Intervention, Blasphemous Act, Greaves, Deflecting Swat, full ramp suite (Birds, STE, Three
  Visits, Farseek, Cultivate, Kodama's, Rampant, signets/talisman/Sphere/Mind Stone).
- **Lands:** 12 named owned-spare (incl. **Evolving Wilds / Terramorphic / Myriad Landscape —
  self-sacrificing fetches each trigger Korvold's draw**, actively on-plan) + 24 basics;
  Fabled Passage 6/6 deployed, Phyrexian Tower 0-spare — skipped, no land buys.

---

## Status table (resumable — update as stages complete)

| # | Candidate | GC count | Brief-fit | Decklist | Lab | Clock (decap / table) | Stage | Next action |
|---|---|---|---|---|---|---|---|---|
| 1 | Yuriko | 3/3 ✓ | **Strong** | ✓ 100 ✓ `insider-trading-20260612.txt` | — | — | 2 ✓ | Stage 3 lab (`yrk_clock_lab`) |
| 2 | Godo | 3/3 ✓ | **Moderate** | ✓ 100 ✓ `hostile-takeover-20260612.txt` | — | — | 2 ✓ | Stage 3 lab (`godo_clock_lab`) |
| 3 | Urza | 3/3 ✓ | Weak (anti-race) | — | — | — | **CUT** ✗ | eliminated (Stage 1, confirmed) |
| 4 | Kinnan | 3/3 ✓ (Worldly swap) | **Strong** | ✓ 100 ✓ `quantitative-easing-20260612.txt` | — | — | 2 ✓ | Stage 3 lab (`knn_clock_lab`) |
| 5 | Korvold | 3/3 ✓ (Worldly swap) | Weak (grindy T7–9) | ✓ 100 ✓ `asset-stripping-20260612.txt` | — | — | 2 ✓ | Stage 3 lab (`kvd_clock_lab`) |
| 6 | Thrasios+Tymna | 3/3 ✓ | Mixed (cost+politics) | — | — | — | **CUT** ✗ | eliminated (Stage 1, confirmed) |
| 7 | Clive (ext) | 3 (exempt) | auto-adv | ✓ 100 ✓ | — | — | 0 ✓ | Stage 3 lab (refresh data first) |
| 8 | Kefka (ext) | 0 (exempt) | auto-adv | ✓ 100 ✓ | — | — | 0 ✓ | Stage 3 lab |
| 9 | Kefka (int, burn) | 3/3 ✓ | **Strong** | ✓ 100 ✓ `forced-liquidation-20260612.txt` | — | — | 2 ✓ | Stage 3 lab (`kfk_clock_lab`) |

Clive flags all RESOLVED 2026-06-12 (user-confirmed reskin aliases → `REF_Reskin_Aliases.md`):
Morgul-Knife=Shadowspear, Storm's Will=**Jeska's Will (GC, → 3 GCs)**, Helm's Deep=Shinka,
Wakandan Skyscraper=Karn's Bastion, Calliope's Song=Seething Song. Still run
`update_scryfall_data.py` before the Clive lab.

**Next action overall:** **Stage 2 COMPLETE — all 5 internal survivors built** (Yuriko / Godo /
Kinnan / Kefka-burn / Korvold), swept, exactly 100 each, commanders in END blocks. Next →
**Stage 3 clock labs** for all 5 finalists + both externals (one `*_clock_lab.py` each on
`speed_lab_core.py`, decap AND table reported separately; reuse kill scaffolds per the funnel
notes); run `update_scryfall_data.py` before Clive's lab. Scratch drafts live in `_build/`
(untracked; `considering/` versions are canonical).
**Cost picture after all sweeps (all unverified):** Godo ~€45–60-but-light → Korvold ~€50
(claim held) → Kinnan ~€120–160 → Yuriko ~€140–170 → Kefka-burn ~€140–190.
**Open user decisions:** (a) Radiation Sickness 4-GC violation — how to resolve; (b) whether
Kinnan's ~€120–160 revised cost changes its Stage-1 "Strong" completability read; (c) Kefka-burn
filename — "Forced Liquidation" codename was coined at build time (candidate had none), rename if
disliked; (d) the 2026-05-31 Calamity Tax swap was never applied to its `.txt` — if it's dead,
the Sheoldred spare frees up and Kefka-burn's buy list shrinks by one premium card; (e) Korvold
pod approval + mechanical-distinctiveness sign-off vs DR/ZSG/Genome (the proposal's own gate).
