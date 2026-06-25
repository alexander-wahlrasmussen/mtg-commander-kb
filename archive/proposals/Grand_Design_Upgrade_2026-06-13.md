# The Grand Design — Upgrade (2026-06-13, APPLIED 2026-06-23)

**THE single canonical Grand Design upgrade proposal.** Consolidates and supersedes the prior
GD proposals (Finisher Upgrade, ETB Disruption Pass, Mana-Fixing Pass — now in
`archive/proposals/`). Standing evidence: `Grand_Design_Speed_Curve_Analysis.md` (clock + the
Atraxa-selection lever test) and `gd_clock_lab.py` (`--mode ramp`, `--mode userpkg`).

**Deck:** The Grand Design (`decks/the-grand-design-20260623.txt`), Atraxa, Grand Unifier — WUBG.
**Thesis (lab-derived):** GD is **mana-gated, not finding-gated** — modelling Atraxa's reveal-10
selection moved the clock ~0, while ramp is the dominant lever. And every kill line funnels
through Finale of Devastation (an untutorable sorcery) — a single point of failure. So this
upgrade does two things: **ramp (speed)** + **a second, *tutorable* finisher (resilience).**

Card text verified via `card_lookup.py` (all adds + cuts); GC checked vs `REF_Game_Changers_List.md`;
availability vs the Moxfield CSV + `grep decks/*.txt`.

---

## The swap — 7-for-7 (stays 100 cards, stays 3/3 GCs)

GD is at the 3-GC cap (Cyclonic Rift, Force of Will, Rhystic Study) — all adds are **non-GC**.

| # | Out | In | Role |
|---|---|---|---|
| 1 | Carpet of Flowers | **Solemn Simulacrum** | ramp + draw + flicker/reanimator ETB target |
| 2 | Veil of Summer | **Sakura-Tribe Elder** | T2 ramp + chump + yard fuel |
| 3 | Flawless Maneuver | **Springbloom Druid** | ramp/fixing (sac a land → 2 basics) + flicker/Pod/reanimate ETB target |
| 4 | Dovin's Veto | **Kodama's Reach** | reliable, wrath-proof land-ramp + fixing (2nd land to hand) |
| 5 | Grand Abolisher | **Coalition Relic** | 4c rock + charge-burst toward the kill turn (colorless body survives sweepers) |
| 6 | Displacer Kitten | **Craterhoof Behemoth** | **2nd finisher TYPE** — a *tutorable* creature finisher (Finale can't be) |
| 7 | Heroic Intervention | **Fanatic of Rhonas** | explosive green burst ({G}{G}{G}{G} with a power-4+ creature) → funds Craterhoof/Finale |

**Keep Finale of Devastation** — the point is *two* independent finisher lines (the big X≥10
sorcery AND the cheaper tutorable creature), not replacing one fragile line with another.

### 2026-06-23 revision (what changed from the original draft, and why)

The original 2026-06-13 draft used **Faeburrow Elder** (slot 4) and **Rune-Scarred Demon** (slot 7).
A follow-up review ("are we really picking the best of what's *available*?") replaced both:

- **Faeburrow Elder → Kodama's Reach + Fanatic of Rhonas (two slots).** Faeburrow's verified text
  counts colors among permanents — its floor is **{G}{W} = 2 mana** on cast, the same board-
  conditionality the speed analysis dinged Bloom Tender for, and it dies to the sweepers this deck
  itself runs (Toxic Deluge / Cyclonic Rift). For a *mana-gated* deck, ramp **reliability** is the
  point. So it became two pieces doing different jobs: **Kodama's** raises the floor (wrath-proof,
  fixes colors, owned ×5), **Fanatic** raises the ceiling (the GGGG burst lands exactly on the
  green finishers it funds — Craterhoof {5}{G}{G}{G} / Finale {X}{G}{G}).
- **Rune-Scarred Demon → (nothing — Craterhoof is the fix).** Rune-Scarred was ~1pp in the lab and
  a 7-mana body competing for the mana this deck is short on. Its job — "a tutor that can finally
  find a finisher" — is already done by **Craterhoof**, which the whole creature-tutor suite (Pod /
  Chord / Eladamri's / Defense / Razaketh) *can* fetch. Finale just rides as the un-tutorable
  backup. Grim Tutor was considered for the slot but kept in the pool for a combo deck instead;
  freeing the slot for the 2nd ramp piece is the stronger, on-thesis use.
- **Wood Elves → Springbloom Druid.** Same ETB-land-fetch creature role, modelled identically
  (+1 land @3), but **owned ×2 (free)** instead of a ~$1 buy — so the whole build is $0.

## Lab results (`gd_clock_lab.py --mode userpkg`, 40k, seed 12345, decap clock)

| Build | T6 | T7 | T8 | T9 | T10 | decap median | never-12 |
|---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| baseline GD | 1 | 6 | 20 | 44 | 66 | T10 | 10% |
| original draft (Faeburrow + Rune-Scarred) | 2 | 11 | 32 | 58 | 78 | T9 | 5% |
| **APPLIED (Kodama's + Fanatic, no tutor)** | **3** | **12** | **33** | **60** | **79** | **T9** | **5%** |

(Wood Elves vs Springbloom Druid was a parity check — identical to the second decimal.)

**What each lever does (measured, honest):**
- **Ramp (slots 1–5): the speed fix** — median T10→T9, whiff 10%→5%. Two reliable land-ramp pieces
  (Kodama's + Springbloom) + Solemn + Coalition Relic + Sakura raise both floor and reliability.
- **Craterhoof (6): the fragility fix + a sharper front edge** — a cheaper 8-mana finisher closes
  fast games more than 12-mana Finale, and (the value the goldfish can't score) it's a 2nd finisher
  the *creature-tutor suite can fetch*. Reanimatable / Pod-able / Defense-able / Finale-fetchable.
- **Fanatic of Rhonas (7): the front-edge sharpener** — the GGGG burst (once Atraxa or a reanimated
  fat is out) is the only lever that beat the original draft on the front edge (T9 60% vs 58%).
  Off-model caveat: it produces **green only** (no fixing for the WUB half) and is a conditional
  creature — but its payoff is the green finishers, so the acceleration is largely real.

**Bottom line:** decap **T10 → T9**, whiff **10% → 5%**, a sharper T7–9 front edge than the original
draft, two independent finisher lines, and a deck that no longer dies if Finale is countered/exiled/
unseen — built entirely from owned cards.

> **Model caveats (the comparison is conservative for the applied build).** Mana is GENERIC in the
> lab, so Kodama's basic-fixing and its 2nd-land-to-hand are *uncredited* (its true value ≥ shown),
> while the original draft's Faeburrow was *over*-credited (unconditional 2 mana/turn). So the
> applied build's real-world edge over the draft is larger than the ~+2pp the table shows. Trust the
> shape and the front edge, not the second decimal.

## Trade-off (honest)

Trades interaction/protection density for ramp + finishers. Interaction drops from ~17 to ~13 —
still deep (Counterspell, Mana Drain, Force of Will, Force of Negation, Swan Song, Path, Swords,
Generous Gift, Assassin's Trophy, Cyclonic Rift, Toxic Deluge, Deadly Rollick). Two cuts are
"contested" if you value them: **Grand Abolisher** (anti-interaction tempo, but this is a midrange
value deck, not a combo deck protecting a turn) and **Displacer Kitten** (a flicker engine — but
the lever test showed flicker doesn't move the clock; 5 flicker outlets remain). The other cuts are
the deck's softest interaction (Veil of Summer, Flawless Maneuver, Dovin's Veto, Heroic
Intervention) and a conditional ramp piece (Carpet of Flowers, only ramps vs blue).

## Availability (CLAUDE.md cross-deck check)

Every card is an **owned, undeployed spare** — **$0 total, no buys.**

| Add | Status |
|---|---|
| Solemn Simulacrum | owned ×4 (2 deployed) → free spare |
| Sakura-Tribe Elder | owned ×2 (1 deployed) → free spare |
| Springbloom Druid | owned ×2, in 0 decks → free |
| Kodama's Reach | owned ×5 (1 deployed) → free spare |
| Coalition Relic | owned ×2 (1 deployed) → free spare |
| Craterhoof Behemoth | owned ×2, in 0 decks → free |
| Fanatic of Rhonas | owned ×1, in 0 decks → free |

## Status

**APPLIED 2026-06-23.** New decklist: `decks/the-grand-design-20260623.txt` (100 cards, 3/3 GC
verified). Old list archived to `archive/old_decklists/the-grand-design-20260502.txt`. DeckSafe
spreadsheet re-run. Summary's finisher/kill-line section updated (Craterhoof = tutorable primary,
Finale = un-tutorable backup). Lab: `gd_clock_lab.py --mode userpkg`.
