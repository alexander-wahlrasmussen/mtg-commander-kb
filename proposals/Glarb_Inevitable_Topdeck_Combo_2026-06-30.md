# Glarb "Inevitable" — Topdeck-Combo Rebuild (2026-06-30)

> **✅ PROMOTED to the roster 2026-07-01** as **Croak and Dagger** →
> `decks/croak-and-dagger-20260701.txt` (the candidate was reconciled to a legal 100 by restoring
> Tempt with Discovery — the Out list below is 13, but the candidate had over-cut it to 99). The old
> grind list and the candidate file are archived under `archive/old_decklists/`. The T9 clock now
> lives in `CLOCKS["croak_and_dagger"]`; the lab was repointed to the roster `.txt`. Summary,
> Deck_Index, Pod_Matchup_Matrix, tier-list + dashboard all re-baked. **Outstanding:** refresh the
> Moxfield ownership CSV (it predates the 8 buys + 2nd Aetherflux) and pick the DLA 1-card backfill
> (deferred) if Sensei's Top physically comes out of that deck.

Candidate (promoted): `archive/old_decklists/glarb-inevitable-20260630.txt` → `decks/croak-and-dagger-20260701.txt`
Lab: `scripts/glarb_inevitable_lab.py` · Harvest: `scripts/pod_gauntlet.py --matrix`

## The problem this fixes

The deployed **Croak and Dagger** (Glarb grind fortress) wins with a single
mana-gated **Torment of Hailfire**: honest clock **~T13 decap / table never-in-horizon**
(`ct_speed_lab`, dig=0). Two structural weaknesses, confirmed across the 2026-06-30
session:

1. **Fragile win-con** — one telegraphed, counterable, ~14-mana haymaker; no inevitability.
2. **Loses to the combo pod** — `pod_gauntlet` P(beat pod) ≈ **7–8%**; the deck can't
   race a T6–7 kill and can't out-grind a deck that wins on the spot.

The grind externals (Strong Glarb, the 06-16 reanimator) are *bigger* versions of the
same problem — the old "54%@T6" was the `dig` mirage (the bug corrected 2026-06-29).
Only the **combo** externals are actually inevitable.

## The direction: GLARB4EVA's redundant "Topdeck Matters" loop

From the user-supplied **GLARB4EVA primer** (a deliberately **Bracket-3** list, verified
3/3 GC on our list: Bolas's Citadel + Field of the Dead + Seedborn Muse). Inevitability
comes from **redundancy**, not one combo:

- **Loop core:** Sensei's Divining Top (`{T}: draw, put Top on top`).
- **Enablers (cast Top off the top, no MV restriction) — any one:** Bolas's Citadel /
  One with the Multiverse / Fortune Teller's Talent (lvl 2) / The Reality Chip.
- **Payoffs — any one:** Aetherflux Reservoir ("pay 50: deal 50", an *ability* = counter-immune)
  / Ancient Cellarspawn (drain on under-costed casts). Both also gain/needn't-gain life,
  addressing the burn worry.
- **Setup:** non-GC topdeck tutors (Insidious Dreams, Emergent Ultimatum, Scheming Symmetry)
  stack pieces on top for Glarb/Citadel; GSZ/Chord/Finale fetch the creature pieces.
- **Protection:** Tidal Barracuda (one-sided Abolisher on our turn) + the retained free counters.

Two cards' evaluation **flips** vs the grind shell: **Sensei's Top** and **Bolas's Citadel**
go from marginal/negative to core — context-dependent, as flagged throughout.

## The build (vs current Croak)

100 cards, **3/3 GC** — the *only* GC change is **Demonic Tutor → Bolas's Citadel**
(its tutoring role moves to non-GC topdeck tutors, which are *better* here). Land base
(38) unchanged.

**Out (13):** Demonic Tutor, Gray Merchant, Kokusho, Rite of Replication, Submerge,
V.A.T.S., Crucible of Worlds, Life from the Loam, Splendid Reclamation, Ramunap Excavator,
Titania's Command, Spore Frog, Blossoming Tortoise.

**In (13):** Bolas's Citadel, Sensei's Divining Top, Aetherflux Reservoir, Ancient
Cellarspawn, One with the Multiverse, Fortune Teller's Talent, The Reality Chip, Savvy
Trader, Emergent Ultimatum, Insidious Dreams, Tidal Barracuda, **Tatyova, Benthic Druid**,
Scheming Symmetry. *(Sheoldred → Tatyova, 2026-06-30 — contention fix, see Acquisition.)*

Kept on-theme from the old shell: Seedborn Muse, Valley Floodcaller, Coffers+Urborg+Yavimaya,
Sylvan Library, Shifting Woodland, Exploration/Oracle/Azusa/Aesi, GSZ/Chord/Finale, Noxious
Revival, Muldrotha, **Torment of Hailfire** (retained as a mana-sink grind-out backup).

## Results

### Assembly clock — `glarb_inevitable_lab.py` (20k, honest dig = selection)

| Build | T6 | T7 | T8 | T9 | T10 | T12 | median | never-in-14 |
|---|--:|--:|--:|--:|--:|--:|:--:|--:|
| **FULL** (4 enablers · 2 payoffs · tutors) | 9% | 24% | 41% | 55% | 66% | 82% | **T9** | 10% |
| **LEAN** (only Citadel+Top+Aetherflux) | 3% | 6% | 10% | 14% | 19% | 30% | **never** | 58% |

- **Redundancy is the win, not speed:** the exact 3-card line never assembles 58% of the
  time; the redundant build is T9 / 90% in horizon.
- **Protection available** ≈ 76% by T7 (→87% by T12) — the combo turn is defensible
  (Fierce Guardianship / Force of Negation / Pact / Swan Song / Mana Drain / Veil / Tidal Barracuda).
- **Dig sweep:** median T12→T8 across dig −1..+2 (robust, monotonic).
- **Conservative:** Cabal Coffers is *not* modelled → the real clock is a touch faster.

### Pod matchup — `pod_gauntlet --matrix --pending`

Harvested the FULL curve into `BUILD_CLOCKS["glarb_inevitable"]` (disrupt_class `warn` =
Croak's counter suite retained):

| | current grind (T13) | inevitable combo (T9) |
|---|--:|--:|
| Pure race (P decap ≤ pod K) | 3% | **21%** |
| **P(beat pod)** | **~7–8%** | **~27–31%** |

≈ **4× improvement** — from near-bottom of the roster to a **fair table share (~25–31%)**.
Still mid-pack, *not* a top-tier pod-crusher (kept Bracket-3 + protection-heavy for our
Abolisher meta).

### Trade-off — vs Ur-Dragon (`vs_dragon_lab`)

**~88% → ~78%** with the combo clock + grind defense. A deliberate trade: against a *fair*
deck, near-certain *eventual* kill matters more than speed, and the combo bricks ~10%.
The **78% under-credits the retained Torment** grind-out (kept for exactly those brick
games), so the true number is likely **~83–85%**. Net: a sliver of the *best* matchup
spent to fix the *worst* one.

## Acquisition (contention resolved 2026-06-30)

`deck_doctor` buy list — **8 cards ≈ €32** (indicative, Scryfall): Insidious Dreams (€7.34),
Tidal Barracuda (€7.20), Scheming Symmetry (€5.86), Ancient Cellarspawn (€5.40), The Reality
Chip (€2.48), One with the Multiverse (€2.00), Fortune Teller's Talent (€0.68), Emergent
Ultimatum (€0.55).

**Contention resolution** (the three owned-but-locked cards, after reading the donor decks):
- **Sheoldred** (a *redundant* punisher in FL, a drain/cushion piece in DLA; ~€80 card) →
  **substituted OUT** of this build for **Tatyova, Benthic Druid** (owned, free, on-theme
  landfall lifegain + draw). **Clock-neutral** (median T9, never 9%), arguably better in
  reality (Tatyova's draw digs toward pieces). Leaves FL **and** DLA untouched.
- **Aetherflux Reservoir** (a *backup* line in S-tier Genome) → **buy a 2nd copy (~€2–5)**;
  not worth disturbing Genome.
- **Sensei's Divining Top** → **pulled from The Dark Lord's Army** (one of ~7 redundant draw
  pieces there; negligible loss). DLA needs a 1-card backfill — **TBD** (deferred per user
  2026-06-30; DLA `.txt` left at 100 until the replacement is chosen).

**Total to build ≈ €34–37** (the 8 buys + a 2nd Aetherflux) plus the free Sensei's Top pull —
vs ~€80 had we bought a 3rd Sheoldred.

## Bracket / Rule-0

3-card combo → **Bracket-4-in-spirit**. The pod has accepted infinites/combos since
2026-06-19, so this should be a quick Rule-0 nod (same path as past combo proposals).
Stays **Bracket-3 by GC count** (3/3).

## Caveats (honest)

- The assembly clock + pod numbers rest on **judgment priors** in a heuristic model
  (dig rate, deploy costs, K-distribution). Swept where possible; trust the **shape +
  deltas** (T13→T9, 8%→~30%, FULL≫LEAN), not the second decimal.
- Goldfish: no opposing interaction in the assembly clock (protection reported separately).
- This is an **identity shift** (grind fortress → combo-control) and a real ~13-card swap.

## Next steps

1. Pod Rule-0 nod.
2. Resolve the 3-card contention (substitute search for DLA / Genome / Forced Liquidation)
   + acquire the 8 buys.
3. On build: promote to a dated roster `.txt`, write the Summary, refresh tier-list/memory.

Files: candidate (promoted → archived) `archive/old_decklists/glarb-inevitable-20260630.txt` · lab
`scripts/glarb_inevitable_lab.py` · wiring `pod_gauntlet.py BUILD_CLOCKS/PROTECT["glarb_inevitable"]`
· guard `tests/test_glarb_inevitable_regression.py`.
