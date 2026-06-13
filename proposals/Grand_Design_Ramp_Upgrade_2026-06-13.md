# The Grand Design — Ramp Upgrade (2026-06-13)

**Deck:** The Grand Design (`decks/the-grand-design-20260502.txt`), Atraxa, Grand Unifier — WUBG.
**Trigger:** the Atraxa-selection lever test (`Grand_Design_Speed_Curve_Analysis.md` addendum)
showed GD is **mana-gated, not finding-gated** — Atraxa's card-selection moves the clock ~0,
while **ramp is the dominant lever** (idealized +2 mana/turn collapsed decap T10→T7). This
proposal is the concrete, lab-validated ramp package. Companion to the separate finisher proposal
(`Grand_Design_Finisher_Upgrade_2026-06-08.md`, Craterhoof) — the two stack.

**Card text verified** via `card_lookup.py` for all adds + cuts; **GC checked** against
`REF_Game_Changers_List.md`; **availability** checked vs the Moxfield CSV + `grep decks/*.txt`.

---

## The swap (5-for-5, stays 100, stays 3/3 GCs)

GD is already at the **3-GC cap** (Cyclonic Rift, Force of Will, Rhystic Study) — so the ramp must
be **non-GC** (rules out Gaea's Cradle, Smothering Tithe). All five adds are non-GC and synergize
with the deck's flicker/reanimator/4-color shell.

| Out | In | Why |
|---|---|---|
| Carpet of Flowers | **Solemn Simulacrum** | conditional ramp (blank vs non-blue) → reliable ramp + draw + a flicker/reanimator ETB target |
| Veil of Summer | **Sakura-Tribe Elder** | narrow 1-of → cheap T2 ramp + chump + yard fuel for the reanimator |
| Flawless Maneuver | **Wood Elves** | situational protection → ramp/fixing (fetches a Forest-typed dual) + flicker target |
| Dovin's Veto | **Faeburrow Elder** | redundant counter (deck keeps Counterspell/Mana Drain/FoW/FoN/Swan Song) → explosive 4c dork (taps for up to WUBG) |
| Grand Abolisher *(flex — see note)* | **Coalition Relic** | anti-interaction tempo piece, marginal on a midrange value deck → 4c rock + charge-burst toward the 12-mana Finale turn |

GCs unchanged (no GC added or cut). 100 cards.

**Cut note:** the first four are clear (conditional/narrow/situational/redundant). The 5th —
**Grand Abolisher** — is the contested one (it's strong, but it protects a *combo* turn this
midrange value deck doesn't really have). If you'd rather keep it, swap the 5th cut for **Heroic
Intervention** (redundant protection) or a flicker value piece (Soulherder / Thassa) — the clock
is identical either way (the cut isn't a ramp/kill card).

## Lab result (`gd_clock_lab.py --mode ramp`, 20k, same kill model both sides)

| Build | T8 | decap median | never-in-12 |
|---|:--:|:--:|:--:|
| baseline GD | 21% | T10 | 11% |
| **+ ramp package** | **27%** | **T9** | **6%** |

**~1 turn faster (T10→T9) and the whiff rate halves (11%→6%).** Real and worthwhile, but short of
the idealized +2/turn ceiling (T7) — realistic ramp competes for early turns and several pieces
enter tapped (Solemn/Sakura/Cultivate fetch tapped lands). To push further you'd add *more* ramp
slots or fast untapped rocks (limited: the pod bans Mana Crypt).

**Stacks with the finisher proposal:** Craterhoof alone was also ~T10→T9 (a cheaper finisher than
the 12-mana Finale). Doing **both** ramp + Craterhoof should compound toward ~T8 — verify with a
combined run before committing if you want the exact number.

## Trade-off (honest)

This trades **4 interaction/protection pieces for ramp**. The deck drops from ~17 interaction to
~13 — still deep (Counterspell, Mana Drain, Force of Will, Force of Negation, Swan Song, Path,
Swords, Generous Gift, Assassin's Trophy, Cyclonic Rift, Toxic Deluge, Deadly Rollick, Heroic
Intervention). On-thesis: GD is mana-gated, so trading *marginal* interaction for speed +
consistency is the right exchange for a deck that out-grinds but is slow to close.

## Availability (CLAUDE.md cross-deck check)

| Add | Status |
|---|---|
| Solemn Simulacrum | owned 3 (2 in Earthbend/Eldrazi) → **free spare** |
| Sakura-Tribe Elder | owned 2 (1 in Eldrazi) → **free spare** |
| Coalition Relic | owned 2 (1 in Replication) → **free spare** |
| Wood Elves | owned 0 → **buy ~$1** |
| Faeburrow Elder | owned 1 (in Peace Offering) → pull or **buy 2nd ~$3–5** |

**~$5 total** (or $0 if pulling Faeburrow from Peace Offering). Prices unverified — confirm on
Cardmarket per the verify-prices rule.

## Status

**Proposal only — not applied.** The deployed `.txt` stays as-is. If applied: bump the dated
filename (`the-grand-design-<today>.txt`), archive the old list to `archive/old_decklists/`,
recount to 100, confirm 3/3 GCs. Lab: `gd_clock_lab.py --mode ramp`.
