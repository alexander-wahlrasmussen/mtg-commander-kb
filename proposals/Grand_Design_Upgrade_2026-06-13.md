# The Grand Design — Upgrade (2026-06-13)

**THE single canonical Grand Design upgrade proposal.** Consolidates and supersedes the prior
GD proposals (Finisher Upgrade, ETB Disruption Pass, Mana-Fixing Pass — now in
`archive/proposals/`). Standing evidence: `Grand_Design_Speed_Curve_Analysis.md` (clock + the
Atraxa-selection lever test) and `gd_clock_lab.py`.

**Deck:** The Grand Design (`decks/the-grand-design-20260502.txt`), Atraxa, Grand Unifier — WUBG.
**Thesis (lab-derived):** GD is **mana-gated, not finding-gated** — modelling Atraxa's reveal-10
selection moved the clock ~0, while ramp is the dominant lever. And every kill line funnels
through Finale of Devastation (an untutorable sorcery) — a single point of failure. So this
upgrade does two things: **ramp (speed)** + **a second, tutorable finisher (resilience).**

Card text verified via `card_lookup.py` (all adds + cuts); GC checked vs `REF_Game_Changers_List.md`;
availability vs the Moxfield CSV + `grep decks/*.txt`.

---

## The swap — 7-for-7 (stays 100 cards, stays 3/3 GCs)

GD is at the 3-GC cap (Cyclonic Rift, Force of Will, Rhystic Study) — all adds are **non-GC**.

| # | Out | In | Role |
|---|---|---|---|
| 1 | Carpet of Flowers | **Solemn Simulacrum** | ramp + draw + flicker/reanimator ETB target |
| 2 | Veil of Summer | **Sakura-Tribe Elder** | T2 ramp + chump + yard fuel |
| 3 | Flawless Maneuver | **Wood Elves** | ramp/fixing (fetches a Forest dual) + flicker target |
| 4 | Dovin's Veto | **Faeburrow Elder** | explosive 4-color dork (taps for up to WUBG) |
| 5 | Grand Abolisher | **Coalition Relic** | 4c rock + charge-burst toward the kill turn |
| 6 | Displacer Kitten | **Craterhoof Behemoth** | **2nd finisher TYPE** — a *tutorable* creature finisher (Finale can't be) |
| 7 | Heroic Intervention | **Rune-Scarred Demon** | recurrable ETB "tutor ANY card" (incl. Finale) — finisher insurance + a 6/6 |

**Keep Finale of Devastation** — the point is *two* independent finisher lines (the big X≥10
sorcery AND the cheaper tutorable creature), not replacing one fragile line with another.

## Lab results (`gd_clock_lab.py --mode ramp`, 20k, same kill model)

| Build | T7 | T8 | decap median | never-in-12 |
|---|:--:|:--:|:--:|:--:|
| baseline GD | — | 21% | T10 | 11% |
| + ramp (1–5) | 7% | 27% | T9 | 6% |
| + ramp + Craterhoof (6) | 11% | 31% | T9 | 6% |
| **+ all 7 (incl. Rune-Scarred)** | **11%** | **32%** | **T9** | **5%** |

**What each lever does (measured, honest):**
- **Ramp (1–5): the speed fix** — median T10→T9, whiff rate 11%→6%. (Short of the idealized
  +2-mana/turn ceiling of T7: real ramp competes for early turns and enters tapped.)
- **Craterhoof (6): the fragility fix + a sharper front edge** — median stays T9 (same mana gate),
  but T8 21%→31% / T7 6%→11% (a cheaper 8-mana finisher closes fast games more than 12-mana
  Finale). Its bigger value is *resilience the goldfish can't score*: a 2nd finisher the creature-
  tutor suite (Chord / Eladamri's Call / Fauna Shaman / Sidisi / Defense of the Heart) can fetch.
- **Rune-Scarred (7): top-end consistency** — it *can* tutor Finale (any card), so it tightens the
  tail (never-12 6%→5%, T12 94%→95%), median flat. A ~1pp dial in the goldfish (GD is mana-gated +
  already finisher-redundant), but the modelled single ETB undersells a recurrable any-card tutor
  in the flicker shell (Restoration Angel / Ghostly Flicker / Karmic Guide re-trigger it). Genuine
  resilience/flexibility, concentrated at the top end; not a speed lever.

**Bottom line:** decap **T10 → T9**, whiff **11% → 5%**, a much sharper T7–8 front edge, and the
deck no longer dies if Finale is countered/exiled/unseen. Speed + resilience, on-thesis for a
mana-gated deck that out-grinds but was slow and fragile to close.

## Trade-off (honest)

Trades interaction/protection density for ramp + finishers. Interaction drops from ~17 to ~13 —
still deep (Counterspell, Mana Drain, Force of Will, Force of Negation, Swan Song, Path, Swords,
Generous Gift, Assassin's Trophy, Cyclonic Rift, Toxic Deluge, Deadly Rollick). Two cuts are
"contested" if you value them: **Grand Abolisher** (anti-interaction tempo, but this is a midrange
value deck, not a combo deck protecting a turn) and **Displacer Kitten** (a flicker engine — but
the lever test showed flicker doesn't move the clock). Swap either for another redundant counter
if preferred; the clock is unchanged (neither is a ramp/kill card).

## Availability (CLAUDE.md cross-deck check)

| Add | Status |
|---|---|
| Solemn Simulacrum / Sakura-Tribe Elder / Coalition Relic / Craterhoof Behemoth | **free owned spare** each |
| Wood Elves | buy ~$1 (owned 0) |
| Faeburrow Elder | owned 1 (in Peace Offering) → pull or buy ~$3–5 |
| Rune-Scarred Demon | buy ~$3–5 (owned 0) |

**~$7–11 total** (less if pulling Faeburrow). Prices unverified — confirm on Cardmarket.

## Status

**Proposal only — not applied.** Deployed `.txt` unchanged. To apply: bump the dated filename
(`the-grand-design-<today>.txt`), archive the old list to `archive/old_decklists/`, recount to 100,
confirm 3/3 GCs. Lab: `gd_clock_lab.py --mode ramp` (baseline → +ramp → +Craterhoof → +Rune-Scarred).
