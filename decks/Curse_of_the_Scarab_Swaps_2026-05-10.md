# Curse of the Scarab — Swap Proposal 2026-05-10

**Status:** Proposal, not yet applied. `.txt` unchanged pending confirmation.

## Context

Earlier today (2026-05-10) Champion of the Perished was promoted from sideboard to main and **Lost Monarch of Ifnir** was moved to the sideboard to make room. The summary justified the cut as "the slowest payoff in the deck" — a framing that undersells what Lost Monarch actually does (army-wide afflict 3) and overstates what the cut card was offering. On second look, **Corpse Augur is the more redundant 4-drop** and a cleaner cut for the same Champion-promotion swap.

This proposal does **not** unwind the Champion promotion. It revisits which 4-drop should have been the cut.

## Proposed swap

| Out (main → sideboard) | In (sideboard → main) | Net |
|---|---|---|
| Corpse Augur | Lost Monarch of Ifnir | Same CMC slot (4), zombie-for-zombie, no GC change |

## Card text (verified via card_lookup.py)

- **Corpse Augur** — {3}{B}, 4/2 Zombie Wizard. *When this creature dies, you draw X cards and you lose X life, where X is the number of creature cards in target player's graveyard.*
- **Lost Monarch of Ifnir** — {3}{B}, 4/4 Zombie Noble. *Afflict 3. Other Zombies you control have afflict 3. At the beginning of your second main phase, if a player was dealt combat damage by a Zombie this turn, mill three cards, then you may return a creature card from your graveyard to your hand.*

## Rationale

### Why Corpse Augur is the stronger cut

- **Redundant draw axis.** The deck already runs Kindred Discovery, Graveborn Muse, Black Market Connections, Bone Miser, Skullclamp, Wilhelt's end-step sac-to-draw, Undead Augur, and Midnight Reaper — eight on-rate draw engines. Corpse Augur is a ninth, gated on a stocked target graveyard and on the Augur itself dying. Marginal in a deck that is rarely card-starved once the engine is running.
- **Variance-dependent payoff.** X = creature cards in *target player's* graveyard. Early-game it's 0–2. It only spikes to "real draw" mid-late game, and at that point Demonic Tutor / Kindred Discovery / Graveborn Muse / Black Market Connections are usually already shaping the hand.
- **Stat line is poor.** 4/2 for {3}{B} dies to most chip removal and trades down in combat. Lost Monarch's 4/4 is durable, attacks profitably, and survives a lot more incidental damage.

### Why Lost Monarch deserves the main slot

- **Army-wide afflict 3 is a damage multiplier on the wide-combat kill plan.** Kill Line 3 swings a wide lord-pumped board behind Cyclonic Rift. With four blocked attackers, that's 12 life across the table *regardless of combat math* — independent of whether your tokens are hit by Toxic Deluge, Wrath of God, or chump blockers.
- **Anthem applies to tokens too.** Necroduality copies, Diregraf Colossus tokens, Wilhelt 2/2s, Crowded Crypt's decayed wave — every disposable body becomes a 3-life threat on block. This is exactly the deck's bottleneck (tokens are individually small without lord support); afflict adds a second damage axis that bypasses lord-stacking entirely.
- **Mill+recur trigger is value upside, not the main reason to run it.** The summary fixated on this and missed the anthem. Even if the second-main trigger never fires, the card earns its slot on afflict alone.

### What the swap costs

- **Lost a death-trigger draw spell.** The deck loses Corpse Augur's variance-dependent draw burst. Mitigated by the eight other draw engines and the fact that Demonic Tutor can find any of them.
- **Loss is more pronounced in long grindy games** where graveyards bloat and Corpse Augur becomes a 6–10-card draw. In faster pods (T7–9 goldfish), Augur often dies with X=2–4, well below its ceiling.

## Honest counterargument (why you might leave it)

Corpse Augur has a real combo with the deck's free sac outlets — Carrion Feeder or Warren Soultrader can pop it on the same turn it enters, converting it into an instant-speed draw spell timed to a stocked graveyard. That's a play pattern Lost Monarch can't replicate. If your meta runs creature-heavy decks (Najeela, Ghave, token strategies), Augur's X-value scales hard with opponent graveyards. If your meta is light on blockers (control, combo), Lost Monarch's afflict goes uncast — opponents simply don't block — and the value collapses to a 4/4 vanilla.

**Decision lever:** if your pod has lots of bodies hitting graveyards (Sauron-style, Teysa-style, token strategies), keep Corpse Augur. If your pod is wide-combat-friendly (control, midrange, decks that block to defend), Lost Monarch is the better main.

## Verification

- **Card text:** verified for both via `card_lookup.py`.
- **Cross-deck availability:** both cards exist only in this deck (`grep decks/*.txt` confirms). No collision with other decks.
- **Game Changer status:** neither card is on `REF_Game_Changers_List.md`. GC count remains 3/3 (Cyclonic Rift, Demonic Tutor, Fierce Guardianship).
- **Bracket 3 compliance:** unchanged. No new infinite combo enabled.
- **Card count:** 99 + 1 commander before and after.

## If applied — file changes

- New: `decks/curse-of-the-scarab-20260510-<HHMMSS>.txt` (today is 2026-05-10, so a timestamped suffix is needed to avoid collision with the existing dated file)
- Archived: `archive/old_decklists/curse-of-the-scarab-20260510.txt`
- Summary update: append a 2026-05-10 second-swap entry to the score-history paragraph; update the Maybeboard table (Lost Monarch role-tag changes; Corpse Augur added).
