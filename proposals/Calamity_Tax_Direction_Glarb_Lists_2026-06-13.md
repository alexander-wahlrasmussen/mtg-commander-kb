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
