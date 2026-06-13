# Calamity Tax — "Different Direction" Evaluation: 5 External Glarb Lists (2026-06-13)

Follow-up to `Calamity_Tax_Kill_Turn_Lab_2026-06-13.md` (sweep row 8), whose verdict was:
our V1–V4 are mana-gated grinders that kill ~T13 and can't race the T6–7 Abolisher pod —
the deck needs a *different direction*, not the 05-31/06-01/reanimator swaps. The user
brought five online Glarb (Calamity's Augur) lists to evaluate on four axes: how **scary**,
how **quick**, how often it **has an answer**, how **smooth**.

Ownership ignored per the user. Win-cons card-text-verified via `card_lookup.py`. Lists
saved at `decks/considering/glarb-*-20260613.txt`. Labs: `glarb_compare_lab.py` (cross-deck
availability) + `glarb_hybrid_clock_lab.py` (real combo kill-turn with Glarb's dig modelled).

---

## The lists split into two philosophies

- **Out-grind harder** — #1 Glarbland, #3 Strong Glarb: bigger mana (Coffers/Nyxbloom/
  Beledros) into Doppelgang/Finale/Rite + Field of the Dead. Same DNA as our deck.
- **Out-race with a combo** — #2 Dead Man's Hand (storm/draw-burn), #4 Mastermind (Hermit
  Druid + Thassa's Oracle/Jace, zero basics), #5 Croak & Dagger (Isochron+Dramatic Reversal
  → Aetherflux/Citadel; full cEDH, **bracket 4**).

The sweep already proved out-grinding can't beat the pod, so the combo philosophy is the one
that addresses our actual weakness.

## Cross-deck availability (glarb_compare_lab.py, 40k) — with a critical caveat

| List | win@T6 | answer@T6 | keepable |
|---|:--:|:--:|:--:|
| #3 Strong Glarb | 54%* | 74% | 99% |
| #4 Mastermind | 9%† | 54% | 100% |
| Hybrid | 14%† | 73% | 99% |
| #5 Croak & Dagger | 21%† | 76% | 98% |

\* **mirage** — "payoff in hand" ≠ castable; the kill is mana-gated to ~T13 (cf. our Calamity).
† **floor** — this model draws + a few tutors but does **NOT model Glarb's selection engine**
(surveil 2, MV4+ top-casts, Sylvan/Top/fetch filtering). For Glarb that guts the core plan, so
the combo numbers are a severe undercount. (User correctly flagged this — hence the second lab.)

Read it right: the grind's high number is a ceiling it never reaches; the combos' low numbers
are floors they blow past once they dig. **True speed: #5 ≈ #4 (turbo) > Hybrid > #3 (slowest).**
**Answer:** #3/Hybrid/#5 dense (~73–76%), #4 light (54%); #5's are *free* (best vs Abolisher).
**Smooth:** all keepable 98–100%.

## The Hybrid, with Glarb's dig modelled (glarb_hybrid_clock_lab.py, 40k)

Hybrid = #3's explosive-mana/tutor shell − {Starfield Vocalist, Savvy Trader, Druid of
Purification} + {Thassa's Oracle, Demonic Consultation, Demonic Tutor} — i.e. bolt a fast,
low-mana, board-independent Thoracle finish (Consult names a nonexistent card → exiles your
library → Thoracle ETB wins, ~3 mana) onto the grind shell. Dig modelled = draw + Glarb
surveil 2 + Sylvan 2 + Top 1, filtering toward pieces; tutors (Vampiric/Demonic/GSZ/Chord/
Finale) fetch the missing piece.

| Variant | combo win@T6 | median | never-in-12 |
|---|:--:|:--:|:--:|
| no-dig floor (compare-lab) | 14% | — | — |
| **BASE** (Consult + Thoracle) | 38% | **T8** | 24% |
| **REDUNDANT** (+Tainted Pact +Jace, −Submerge −Make an Example) | **46%** | **T7** | **15%** |

Modelling the dig moves the combo from a 14% mirage to **median T7–8** — a genuine fast kill
vs the deployed deck's **T13** grind. The user's "trade interaction for redundancy/speed" is
**measurably correct**: REDUNDANT is a full turn faster and cuts the whiff rate 24%→15% (2nd
enabler + 2nd finisher). Protection, however, is thin: ~55% to hold *any* answer by T6, all
**soft** (no free hard counter).

## Recommendation

**Adopt the REDUNDANT Hybrid as the Calamity rebuild direction** — it's the only option that
fixes "quick" (T7 combo) while keeping the Glarb shell's smoothness (99% keepable) and a grind
backup (Doppelgang/Finale off the big mana). It directly fills the "lower-mana board-independent
kill" gap the row-8 lab identified.

**Required adjustment (don't just cut interaction — re-aim it):** convert ~2–3 of the soft
answers into **free** counters (Force of Will, Force of Negation, Fierce Guardianship, Pact of
Negation). A 2-card combo into a T6–7 Abolisher pod dies to one counterspell on the combo turn;
free protection is what makes the fast kill *resolve*. This is a different cut than "lose
interaction" — it's losing *mana-committed soft* interaction for *free combo protection*.

**Bracket:** the 2-card Thoracle line is **bracket-4-in-spirit** → pod approval, same path as the
Yuriko/Insider Trading proposal (house-rule exception for 3+/2-card combos). #5 Croak & Dagger is
the cEDH ceiling (Isochron+Dramatic infinite mana, free counters, full tutors) — out of the
pod's bracket, kept as the reference for where these ideas top out. Pass on #1 (too slow) and #2
(scary but clunky/answer-light).

## Caveats

- The dig model is a near-**ceiling** (assumes surveil/Sylvan/Top filter cleanly toward pieces;
  real surveil whiffs / bins needed cards). T7–8 is the optimistic edge; real is a touch slower —
  but the order of magnitude (and the BASE-vs-REDUNDANT delta) is solid, and it is vastly faster
  than the no-dig floor and the V1 grind.
- Combo decap = table by construction (it wins the game outright).
- "Scary" is qualitative; all win-cons verified. Next step if pursued: lock the exact 99 (with the
  free-counter swap), then a full clock-lab pass + pod Rule-0 conversation.

---

## Follow-up (2026-06-13): finished build + dig-FAIR comparison — a correction

The user asked to clock-lab the finished hybrid AND run the *same dig treatment* on the
original (V1) and reanimator (V4), since "we'd not have modeled the strategy there either."
This corrected a claim I made above.

**Finished hybrid** = REDUNDANT + free combo protection (`glarb-hybrid-final-20260613.txt`):
−Submerge −Make an Example −Blasphemous Edict −We Want…A SHRUBBERY! −Shadow of the Second Sun;
+Tainted Pact +Jace, Wielder of Mysteries +Force of Will +Force of Negation +Pact of Negation.
Result (`glarb_hybrid_clock_lab.py`): **combo median T7**, 45% by T6, 15% never-in-12 (combo
speed unchanged from REDUNDANT — the protection swap doesn't touch it, as intended). Protection
availability **55% → 70% by T6** (the free counters do their job).

**The correction (I was wrong).** Earlier I asserted V1/V4 were "mana-gated, so more dig won't
help." A dig-sensitivity test (`ct_speed_lab.py --mode digtest`) **falsified that**:

| Build | dig=0 (baseline sweep model) | dig=3 (realistic Glarb) | dig=6 (ceiling) |
|---|:--:|:--:|:--:|
| V1 committed | T13 | **T9** | T8 |
| V4 reanimator | T12 | **T9** | T8 |

Modeling Glarb's selection speeds V1/V4 from T13 to ~T9 — the dig finds ramp + Coffers + the
payoff faster, so the bottleneck was drawing into the engine, not pure mana. **The sweep's
Calamity "T13 / never" UNDER-modeled Glarb's dig** (same blind spot the combo-availability lab
had); realistic V1/V4 land **~T8–T10**, not T13.

**Updated verdict.** Finished hybrid ~T7 vs dig-fair V1/V4 ~T9 — a **~2-turn edge, not ~6.**
The real case for the hybrid is therefore **resilience, not raw speed**:
- board-independent kill (~3 mana, no 16-mana Coffers setup needed) → survives mana denial,
  slow draws, and board wipes far better than the grind;
- a real floor (doesn't brick to T13 on a mana-light hand);
- now defensible (free counters, 70% protection by T6).

Still the recommended direction — for those reasons, not a speed blowout.

**Caveat (cross-lab):** the dig knobs differ — `ct_speed_lab` adds raw extra draws; the hybrid
lab models targeted surveil-filtering toward a small piece set. So the exact T7-vs-T9 gap is
approximate. A fully-unified single-engine lab would tighten it; the robust conclusions
(V1/V4 ≈ T8–10 once dig is modeled; hybrid edges them on speed AND wins on resilience) hold.

**Build-it flags (when/if it becomes the roster deck):** GC count needs an audit — the hybrid
carries Demonic Tutor + Field of the Dead (+ possibly others) and must stay ≤3 for the pod;
and the 2-card Thoracle combo needs the pod Rule-0 nod.

---

## Follow-up (2026-06-13): UNIFIED-engine gap + GC-ceiling check + game plans

### 1. Exact gap — one engine, same dig (ct_speed_lab.py --mode unified)
All three builds run through the SAME mana model + the SAME Glarb dig knob (dig=3 = realistic).

| Build (dig=3) | T6 | median decap | dig 2/3/4 sensitivity |
|---|:--:|:--:|---|
| Original (V1) | 3% | **T9** | T10 / T9 / T9 |
| Reanimator (V4) | 3% | **T9** | T9 / T9 / T9 |
| Hybrid (final) | **41%** | **T7** | T8 / T7 / T7 |

**The gap is ~2 turns at the median (T7 vs T9)** — and the hybrid's T7 here matches the
independent `glarb_hybrid_clock_lab.py` (cross-validated). The bigger story is the **front
edge**: the hybrid threatens a kill by T6 in **41%** of games vs **3%** for the grind — it can
actually *race*; the grind essentially never does that early. **V1 ≈ V4** — the reanimator
swaps don't move the clock once Glarb's dig is modelled fairly.

### 2. GC-ceiling check — FAIL (flag, per CLAUDE.md; not silently cut)
The finished hybrid carries **6 Game Changers** vs the bracket-3 cap of 3 (checked against
`REF_Game_Changers_List.md`): **Crop Rotation, Demonic Tutor, Field of the Dead, Force of Will,
Thassa's Oracle, Vampiric Tutor**. (V1 deployed is at 3/3: Demonic Tutor, Fierce Guardianship,
Seedborn Muse.) **Thassa's Oracle is itself a GC**, so the combo finisher alone is +1.

Consequence: the hybrid as tested is a genuine **bracket-4** deck — which is consistent with it
already being a 2-card-combo (bracket-4-in-spirit) build. Two honest paths:
- **Play it bracket 4** (keep all 6 GCs; bracket 4 has no GC cap). The combo + free counters +
  full tutors are a coherent bracket-4 deck. Needs the pod's bracket-4 nod.
- **Force it into bracket 3 (≤3 GCs)** — keep Thassa's Oracle + 2 of {Vampiric, Demonic, Force
  of Will}; cut Crop Rotation + Field of the Dead + one tutor/counter. This **slows + de-risks
  the combo** (fewer tutors to find it, less free protection) — the T7/41%-by-T6 figures are for
  the 6-GC build; a 3-GC-legal trim would be measurably slower/less consistent. **User decision —
  not applied.**

### 3. How the game plans differ
- **V1/V4 (grind, one axis):** ramp to a huge mana pool (Coffers + Urborg, Nyxbloom/Beledros in
  #3), then spend it on a board-wide drain — Torment of Hailfire at lethal X, Doppelgang/Rite on
  Gray/Kokusho, Gray Merchant devotion. You win by *out-resourcing*: survive with Glarb value +
  interaction, assemble ~16 mana, end the game in one big mana-sink turn (~T9). Inevitability,
  not a race. Resilient to spot removal (the kill is board-light) but **loses the race to a T6-7
  pod** and **folds if the mana engine (Coffers) is disrupted** — no Coffers, no kill.
- **Hybrid (combo, two axes):** the same Glarb shell *digs toward a cheap 2-card combo* (Consult/
  Pact + Thoracle/Jace) that wins on ~3 mana **regardless of board or mana count** (~T7, races at
  T5-6 in ~40% of games), protected by free counters; the **grind is the backup** (Doppelgang/
  Rite/Gray off the big mana) when the combo is hated. You win by *assembling + protecting a
  compact combo, fast*. Independent of the 16-mana setup, so it has a real floor (doesn't brick to
  T13 on a slow draw) and survives mana denial/wipes. Costs: **bracket-4-in-spirit + 6 GCs** (see
  above) and folds to graveyard/exile hate on the combo turn (mitigated by the grind backup).

The core swap: **mana-gated inevitability → finding-gated speed + a backup**. The hybrid is
~2 turns faster on median, dramatically faster at the front edge, and far more resilient to a
slow/disrupted draw — at the price of moving up a bracket.
