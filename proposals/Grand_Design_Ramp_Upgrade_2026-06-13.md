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

**Stacks with the finisher proposal:** Craterhoof alone was also ~T10→T9. Combined ramp + Craterhoof
was run — median stays **T9** (same mana gate) but the front edge sharpens (T8 21%→31%, T7 6%→11%).
See the verified follow-up section below; the bigger payoff there is *resilience*, not the clock.

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

---

## Combined ramp + Craterhoof (verified) + the fragility fix (2026-06-13 follow-up)

Ran the combined build (`gd_clock_lab.py --mode ramp`): ramp package **+ Craterhoof, keeping
Finale** (cut Displacer Kitten for Craterhoof's slot → 6-for-6 if done with the ramp 5-for-5).

| Build | T7 | T8 | decap median | never-12 |
|---|:--:|:--:|:--:|:--:|
| baseline GD | — | 21% | T10 | 11% |
| + ramp package | 7% | 27% | T9 | 6% |
| **+ ramp + Craterhoof** | **11%** | **31%** | **T9** | 6% |

Craterhoof doesn't push the **median** past T9 (same mana gate), but it **sharpens the front edge**
(T8 21%→31%, T7 6%→11%) — a cheaper 8-mana finisher closes the fast games more often than the
12-mana Finale.

**The real win is resilience, not the clock — and the goldfish can't show it.** The user's concern
("all lines rely on Finale of Devastation") is the single-point-of-failure problem:
- **Craterhoof** adds a *second finisher type* (creature). Unlike Finale (an untutorable sorcery),
  it's fetchable by the deck's creature-tutor suite (Chord / Eladamri's Call / Fauna Shaman /
  Sidisi / Defense of the Heart) and findable off Atraxa / Rune-Scarred. **Keep Finale** so the
  deck has two independent finisher lines.
- **Rune-Scarred Demon** ({5}{B}{B} 6/6 flyer, ETB tutor ANY card) — a recurrable tutor in the
  flicker shell (Restoration Angel / Ghostly Flicker / Soulherder / Ephemerate / Displacer Kitten /
  Karmic Guide re-trigger its ETB) that *reliably assembles a finisher*. **But it is clock-neutral:**
  the Atraxa-selection test already proved finding doesn't move GD's mana-gated clock (we ran the
  strongest finder possible — reveal-10-take-5, repeated — for ~0). Rune-Scarred is a weaker finder,
  so its value is **resilience/consistency, not speed** — which is exactly the fragility fix wanted.
  Cost: a 7th cut + ~$3–5 (owned 0).

**Net recommendation.** Two complementary upgrades:
1. **Ramp 5-for-5** → the speed fix (T10→T9, whiff 11%→6%).
2. **+ Craterhoof (keep Finale; cut Displacer Kitten)** → the fragility fix (2nd finisher type,
   tutorable) + a sharper T7–8 front edge. ~$0 (Craterhoof has a free spare).
3. **Optional + Rune-Scarred Demon** (7th cut, ~$3–5) → further fragility insurance (recurrable
   finisher-tutor) — resilience only, clock-neutral.

Combined #1+#2 = a ~6-for-6, stays 100, stays 3/3 GCs. Proposal only — not applied.
