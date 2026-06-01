# Teval, the Balanced Scale — Pod-Targeted Swaps (2026-05-31)

**Deck:** The Loam Cycle (`the-loam-cycle-20260404-074432.txt`)
**Trigger:** 2026-05-30 pod session — five Alex-decks lost to a combo opponent running Hidetsugu / Kairi / Kenrith / Kinnan (Kinnan-creatures variant, Marwyn-style mana flood) behind Grand Abolisher protection. See `project_pod_combo_opponent.md`.
**Goal:** Preserve **19/20 (5/5/5/4)** Conversion Check and the existing **3/3 GC** (Fierce Guardianship, Crop Rotation, Field of the Dead). Improve matchup against Abolisher-protected combo without adding a fourth Game Changer.
**Net:** 3-for-3. Stays at 100 cards. No GC change.

---

## Summary table

| Out | In | Role preserved / gained | Owned? |
|---|---|---|---|
| An Offer You Can't Refuse | **Pithing Needle** | Targeted permanent-based lock; survives Grand Abolisher | ❌ buy (~$2-5, unverified) |
| Heroic Intervention | **Endurance** | Free anti-graveyard hate + 3/4 reach body | ❌ buy (~$30-50, unverified) |
| Wonder | **Subtlety** | Free creature/PW soft counter (hits Grand Abolisher cast); 3/3 flier hardcast | ❌ buy (~$15-30, unverified) |

Prices flagged per [[verify-prices]] — confirm on Cardmarket before purchase. Endurance especially has bounced through reprint cycles.

---

## Why the 3/3 GCs stay put

All three Game Changers are engine-critical and color-pie irreplaceable:

- **Fierce Guardianship** is the only free counter in the deck. It can't hit Grand Abolisher (noncreature-only), but it covers everything *else* the combo player casts — Tendrils-class spells, Aetherflux, win-loop enchantments, removal on Teval.
- **Crop Rotation** tutors Field of the Dead, Bojuka Bog (proactive yard hate), Cephalid Coliseum (threshold self-mill), or any colored basic — instant-speed engine fix.
- **Field of the Dead** is the secondary Zombie engine; the manabase is built around its 7-uniquely-named-lands threshold (every fetch/dual is a different name).

Cutting any of these to add Drannith Magistrate or Force of Will would degrade the engine. The interesting deckbuilding constraint is fixing the matchup *without* breaking the GC budget.

---

## Per-card rationale

### 1. An Offer You Can't Refuse → Pithing Needle

- **Out:** {U} instant, counter noncreature spell, **its controller creates two Treasure tokens.**
- **In:** {1} colorless artifact, "Activated abilities of sources with the chosen name can't be activated unless they're mana abilities."
- **Why it works:**
  - An Offer You Can't Refuse is the **worst counter in the deck for this matchup specifically** — countering a combo piece while handing the combo player 2 fast-mana Treasures is the textbook "you spent a card to help them win" trade. Against Hidetsugu/Kairi/Kenrith, two Treasures often *complete* the combo turn.
  - Pithing Needle is the only piece on either side of this swap that **survives a resolved Grand Abolisher** — it's a static effect on a permanent already in play. Once Needle resolves, it remains live through Abolisher's lock-out window.
  - Naming priorities by opponent: Worldgorger Dragon (Kairi-Worldgorger combo), Walking Ballista (Kenrith-Heliod-Ballista), Basalt Monolith if seen (Kinnan artifact line — less relevant since this Kinnan pilot runs creatures, but worth knowing), or the combo's named centerpiece if you scout it.
  - Cost-efficient — castable T1-2, gives a turn-2 lock if you scout early.
- **Score impact:** Counter count drops from 4 → 3, but the cut counter was actively harmful in this matchup. Net interaction quality improves. Core Loop and Kill Reliability unchanged.

### 2. Heroic Intervention → Endurance

- **Out:** {1}{G} instant, your permanents gain hexproof and indestructible until end of turn.
- **In:** {1}{G}{G} creature (3/4 reach, flash); ETB shuffles target player's graveyard back into library. **Evoke: pitch a green card.**
- **Why it works:**
  - **The summary explicitly states board wipes feed the engine** — "Wipes often make the deck stronger." Heroic Intervention is anti-wipe; it actively *prevents* the engine's preferred recovery vector. Low-value card in this deck's archetype.
  - The pod's combo decks don't wipe — they combo. Heroic Intervention rarely activates in this matchup.
  - Endurance is **free interaction** (pitch a green card you'd otherwise discard to hand size — Loam decks always have green cards to spare). Shuffles Hidetsugu/Kairi/Kenrith yard back to library, fizzling reanimation combos at the moment the yard trigger fires.
  - **3/4 reach body sticks around** as a static threat once cast — survives Abolisher because it's already on the battlefield. The body alone is good in a deck running Living Death asymmetry (one more creature for the swing).
  - Hand-pitch fodder for nut draws when you don't need to flash it.
- **Loss:** No more hexproof/indestructible blanket protection. Acceptable — the deck's resilience comes from graveyard recursion, not battlefield protection.
- **Score impact:** Durability stays 5/5 (engine resilience source unchanged). Interaction shape against combo improves materially.

### 3. Wonder → Subtlety

- **Out:** {2}{U} creature, 2/2, gives all your creatures flying as long as Wonder is in your graveyard and you control an Island.
- **In:** {2}{U}{U} creature (3/3 flash, flying); ETB puts target creature spell or PW spell on top or bottom of owner's library. **Evoke: pitch a blue card.**
- **Why it works:**
  - Wonder enables exactly **one** of six kill lines (Line 3 — Living Death asymmetry with flying alpha strike). The other five kill lines (Tooth and Nail / Craterhoof trample, Jarad lifeloss, Exsanguinate damage, Unmarked Grave reanimate, Living Death without flying) close fine without evasion. Wonder is the most expendable single piece in the kill suite.
  - Subtlety is **the only piece in your colors that can answer Grand Abolisher's cast on the stack**. Fierce Guardianship, Swan Song, An Offer, and Counterspell either miss creatures (the first three) or cost mana (the last) — Subtlety is the free creature-spell answer. Pitch a blue card, put Abolisher on the bottom of their library. Hard counter shaped as a bounce.
  - Doubles as removal on Hidetsugu/Kairi/Kenrith/Kinnan **commanders post-resolution** — bounce any commander to the bottom of library for free, costing them an extra 2-tax + a turn to re-deploy.
  - 3/3 flying body when hardcast (4 mana). Cleanly fills the evasion-attacker role Wonder vacated, just on a different chassis.
- **Loss:** No more on-demand flying for the whole team via Living Death. Hardcast Subtlety is 4 mana vs. Wonder's free evasion grant. The Living Death + Wonder alpha strike now needs Craterhoof or trample to break through ground blockers.
- **Score impact:** Kill Reliability stays 5/5 (Lines 1, 2, 4, 5, 6 all unaffected; Line 3 loses evasion but the asymmetry still wins from raw board volume). Interaction picks up the only free Abolisher-counter the deck can run.

---

## What didn't make the cut and why

- **Ethersworn Canonist** — white card (color identity W). Sultai (BUG) cannot run it. This was my original first instinct and required a mid-audit correction.
- **Cursed Totem** — too much self-damage. Shuts off Jarad activation (Kill Line 2), Scarab God activation (zombie engine), Wight of the Reliquary's land tutor, Sakura-Tribe Elder's ramp sac. Self-cost outweighs Kinnan-creatures answer (Toxic Deluge already covers that).
- **Drannith Magistrate** — Game Changer. Adding would push to 4/3 GCs and break the cap.
- **Force of Negation** — already in 6 other decks (zero surplus). Also noncreature-only, can't counter Abolisher anyway. Would create a 7th shared-card pressure for marginal benefit.
- **Damping Sphere** — anti-storm; doesn't really hit Kinnan-creatures (no storm-style chains). Marginal.
- **Mindbreak Trap** — looks free, but it's a *cast*. Dies to Abolisher just like every other counter. Useful only on non-Abolisher combo turns.

---

## Updated Conversion Check: 19/20 (5/5/5/4)

| Axis | Before | After | Notes |
|---|---|---|---|
| Core Loop | 5/5 | 5/5 | Engine pieces untouched |
| Kill Reliability | 5/5 | 5/5 | Wonder cut affects 1 of 6 lines; trample covers most |
| Durability | 5/5 | 5/5 | Heroic Intervention was anti-wipe; wipes fuel the engine |
| Interaction | 4/5 | 4/5 | Same axis score, *materially better matchup quality vs combo*. Ceiling still capped by no unrestricted tutor for answers. |

Score holds. Matchup against this pod improves disproportionately to the score change.

---

## Pilot notes (cost-free, biggest single impact)

1. **Kill Grand Abolisher on sight.** You have ~3 opponent-turn windows between their T5 Abolisher cast and their T6 combo untap. Burn instant-speed removal — Beast Within, Assassin's Trophy, Tear Asunder kicked, Otawara channel, Boseiju channel. Six options. Don't save them.
2. **Don't tap out into open combo mana.** If a known combo opponent has 5+ untapped on your turn, hold up Counterspell or Subtlety-pitch instead of casting Splendid Reclamation / Tooth and Nail / Living Death.
3. **Pithing Needle name selection is up-front.** Name the moment you cast — don't save the name slot for "when it matters." Common picks: Worldgorger Dragon (Kairi), Walking Ballista (Kenrith), or the combo enabler you scouted in conversation.
4. **Endurance flash timing.** Pitch and shuffle in response to their first yard trigger of the combo turn — don't wait for the full chain. One graveyard reset usually fizzles the whole sequence.

---

## Shopping list

| Card | Price (unverified) | Source |
|---|---|---|
| Pithing Needle | ~$2-5 | New buy |
| Endurance | ~$30-50 | New buy (high variance — verify on Cardmarket) |
| Subtlety | ~$15-30 | New buy |
| **Total** | **~$47-85** | **All three** |

Verify on Cardmarket before purchase per [[verify-prices]] — these are memory-rounded estimates, not live quotes. Endurance has bounced 2-3x through reprint cycles.

**Tiered fallback if budget-constrained:**
- Pithing Needle only (~$2-5): Minimum viable Abolisher-survivor.
- Pithing Needle + Endurance (~$32-55): Adds the strongest free anti-graveyard piece; the Subtlety / Abolisher-counter hole stays open.

---

## Changelog

- **2026-05-31:** Companion swap file created in response to 2026-05-30 pod session loss. Audit pass identified An Offer You Can't Refuse, Heroic Intervention, and Wonder as the lowest-value slots in the matchup. Adds chosen to preserve 3/3 GC cap while shifting interaction shape toward Abolisher-survival and graveyard hate. Cross-deck conflicts checked: none. Ownership verified via `collection/moxfield_haves_2026-05-14-0631Z.csv` — all three adds require purchase.
