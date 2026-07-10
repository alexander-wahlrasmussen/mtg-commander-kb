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
| `PROP_World_Shapers_Hearthhull.md` | PIPELINE | **Active candidate** — Creative Destruction (Hearthhull) lands/graveyard; queued awaiting the precon. Tuned list = Tier C #12 + 69% vs Ur-Dragon; see `../Build_And_Swap_Tracker.md`. |
| `PROP_The_Wandering_Minstrel.md` | PIPELINE | 5C Town tribal; **deferred** — Earthcraft contention with Najeela; not on the `Deck_Index` shortlist. |

### Dropped / shelved candidates (kept for record — see `../Deck_Index.md` "Candidate new builds")

| File | Status | Note |
|---|---|---|
| `PROP_Berta_Wise_Extrapolator.md` | SHELVED 2026-06-14 | Combo falsified for the 3-GC cap; a decisively worse Najeela (ceiling 15–16/20). |
| `PROP_Najeela_Blade_Blossom.md` | DROPPED 2026-06-14 | 5C Warrior tribal, B4; not falsified (median T10) but the round closed. |
| `PROP_Hashaton_Scarabs_Fist.md` | DROPPED 2026-06-27 | Sole Thoracle deck; user is not building Thoracle. Build slot went to Kefka / Forced Liquidation. |
| `PROP_Winota_Joiner_of_Forces.md` | CLOSED 2026-07-01 | Go-wide racer; a peer not an upgrade of the existing T6–7 racers. Lab `../scripts/winota_clock_lab.py`. |

## Bake-off candidates (the pick-one decision is in `../campaigns/`)

| File | Status | Note |
|---|---|---|
| `PROP_Yuriko_Insider_Trading.md` | LIVE | **Winner, un-built** → `decks/considering/insider-trading-20260612.txt`. Still gated on pod approval of Thoracle+Consult. |
| `../archive/proposals/PROP_Kefka_Court_Mage.md` | BUILT → archived | The no-approval **fallback**; built & physically assembled 2026-07-08 as **Forced Liquidation** (`decks/Forced_Liquidation_Summary.md`). Archived 2026-07-10. |
| `../archive/proposals/PROP_Witherbloom_the_Balancer.md` | BUILT → archived | Proposal-of-record for the built **Zero-Sum Game** (`decks/Zero_Sum_Game_Summary.md`). Archived 2026-07-10. |
| `Witherbloom_External_Build_Comparison.md` | LIVE | Comparison-doc format the bake-off verdict mirrors. |

Verdict + evidence: `../campaigns/Candidate_Bakeoff_Verdict_2026-06-12.md` (+ tracker,
delay lab). Methodology: `../workflows/WF_Candidate_Bakeoff.md`.

## Cross-roster planning

| File | Status | Note |
|---|---|---|
| `Loam_Parts_Bin_Allocation_2026-06-13.md` | LIVE | Where the Loam + Peace Offering teardown cards go (ALLOCATED/PROPOSED/CANDIDATE/POOL/PARK); feeds the GD, RS, and Calamity upgrades. |
| `Assembly_RS_GCfix_and_Calamity_Grind_2026-06-14.md` | LIVE | Per-card sourcing + cross-build contention for the two ungated gauntlet wins (RS GC-fix, Calamity grind-fortress); builds in `decks/considering/`, companion to `../campaigns/Pod_Gauntlet_2026-06-14.md`. |

## Per-deck upgrade / direction (REFERENCE — cited by the deck's Summary, do not move)

| File | Cited by |
|---|---|
| `Radiation_Sickness_Upgrade_2026-06-13.md` | `decks/Radiation_Sickness_Summary.md` — GC-fix (resolves the 4-GC violation) + Loam synergy adds (Sylvan/Hedron Crab/Sidisi); lab: reliability not speed (decap T7 / table T9; front edge +5pp). |
| `Calamity_Tax_Direction_Glarb_Lists_2026-06-13.md` | `decks/Croak_And_Dagger_Summary.md` — Calamity Tax was rebuilt into Croak and Dagger as a grind/lands deck. The Thoracle-hybrid direction this doc evaluated was **abandoned** (Thoracle dropped from the roster 2026-06-27); kept for record only. |

(`Diminishing_Returns_B4_Pivot_2026-06-10.md` archived to `../archive/proposals/` 2026-07-10 — Diminishing Returns dismantled 2026-07-08.)

---

Kefka (the fallback) and Witherbloom were built and their `PROP_` docs archived to
`../archive/proposals/` (2026-07-10); the campaigns bake-off docs are marked RESOLVED.
If **Yuriko / Insider Trading** (the pod-gated winner, still un-built) is ever built,
archive its `PROP_` here too and update both indexes.
