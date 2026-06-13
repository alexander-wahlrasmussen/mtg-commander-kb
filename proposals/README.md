# proposals/ — index & status legend

**Forward-looking build proposals only**: new-deck candidates, per-deck upgrade/
direction docs, and external-build comparisons. The permanent lab evidence (clock
labs, speed-curve analyses) now lives in `../analysis/`; multi-session campaigns
(the kill-window sweep, the candidate bake-off, the framework doc) in `../campaigns/`.
**Not synced to the Claude Project** — local working material.

Status tags:

- **LIVE** — an active build decision or open bake-off candidate.
- **REFERENCE** — cited by path from an active deck Summary. **Moving it breaks that
  citation** (CLAUDE.md lab-citation rule) — rewrite the `proposals/<name>` reference
  in the Summary in the same change.
- **PIPELINE** — un-built candidate, linked from `Deck_Index.md` "Candidate new builds."

Spent docs (bake-off losers, superseded passes, built-deck readiness) live in
`../archive/proposals/`; superseded decklists in `../archive/old_decklists/`;
build scratch in `../archive/build_scratch/`.

## Pipeline candidates (un-built)

| File | Status | Note |
|---|---|---|
| `PROP_Berta_Wise_Extrapolator.md` | PIPELINE | Replaces Wise Mothman (Radiation Sickness); ceiling 15–16/20. |
| `PROP_Hashaton_Scarabs_Fist.md` | PIPELINE | Esper. |
| `PROP_Najeela_Blade_Blossom.md` | PIPELINE | 5C Warrior tribal, Bracket-4. |
| `PROP_The_Wandering_Minstrel.md` | PIPELINE | 5C Town tribal; **deferred** — Earthcraft contention with Najeela; not on the `Deck_Index` shortlist. |

## Bake-off candidates (the pick-one decision is in `../campaigns/`)

| File | Status | Note |
|---|---|---|
| `PROP_Yuriko_Insider_Trading.md` | LIVE | **Winner** → `decks/considering/insider-trading-20260612.txt`. Gated on pod approval of Thoracle+Consult. |
| `PROP_Kefka_Court_Mage.md` | LIVE | **Fallback** (internal Kefka-burn) → `decks/considering/forced-liquidation-20260612.txt`. No pod approval needed. |
| `PROP_Witherbloom_the_Balancer.md` | REFERENCE | Proposal-of-record for the **built** Zero-Sum Game (`decks/Zero_Sum_Game_Summary.md`). |
| `Witherbloom_External_Build_Comparison.md` | LIVE | Comparison-doc format the bake-off verdict mirrors. |

Verdict + evidence: `../campaigns/Candidate_Bakeoff_Verdict_2026-06-12.md` (+ tracker,
delay lab). Methodology: `../workflows/WF_Candidate_Bakeoff.md`.

## Cross-roster planning

| File | Status | Note |
|---|---|---|
| `Loam_Parts_Bin_Allocation_2026-06-13.md` | LIVE | Where the Loam + Peace Offering teardown cards go (ALLOCATED/PROPOSED/CANDIDATE/POOL/PARK); feeds the GD, RS, and Calamity upgrades. |

## Per-deck upgrade / direction (REFERENCE — cited by the deck's Summary, do not move)

| File | Cited by |
|---|---|
| `Grand_Design_Upgrade_2026-06-13.md` | `decks/The_Grand_Design_Summary.md` — the single canonical GD upgrade (ramp + diversified finisher, T10→T9; supersedes the Finisher/ETB/Mana passes now in `../archive/proposals/`). |
| `Radiation_Sickness_Upgrade_2026-06-13.md` | `decks/Radiation_Sickness_Summary.md` — GC-fix (resolves the 4-GC violation) + Loam synergy adds (Sylvan/Hedron Crab/Sidisi); lab: reliability not speed (decap T7 / table T9; front edge +5pp). |
| `Diminishing_Returns_B4_Pivot_2026-06-10.md` | `decks/Diminishing_Returns_Summary.md` |
| `Calamity_Tax_Direction_Glarb_Lists_2026-06-13.md` | `decks/The_Calamity_Tax_Summary.md` — chosen rebuild = 3-GC Thoracle hybrid (supersedes the retired swap proposals in `../archive/proposals/`). |

---

When the Yuriko/Kefka build is actually made, archive its `PROP_` here and the four
bake-off docs in `../campaigns/` to `../archive/proposals/`, and update both indexes.
