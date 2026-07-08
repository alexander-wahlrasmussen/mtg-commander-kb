# Diminishing Returns — Swap Log 2026-05-05

## Context

Audit of the Teysa Karlov aristocrats deck on 2026-05-05 surfaced engine-math errors in the prior summary (Gray Merchant ETB not Teysa-doubled, edict creatures ETB not doubled, Mirkwood Bats sac/create not doubled) and one decklist mismatch (Phyrexian Tower documented but not present, fixed earlier the same day). After correcting the documentation, two upgrades were swapped in from the DeckSafe collection.

## Swaps

| Out | In | Rationale |
|---|---|---|
| Black Market Connections | The Meathook Massacre | BMC is a slow 3-mana incremental value engine. Meathook is a 2-death-trigger drain payoff (both doubled by Teysa) plus a flexible {X}{B}{B} board wipe / pinpoint removal on ETB. Faster, scales harder, doubles as a removal slot. |
| Welcoming Vampire | Elas il-Kor, Sadistic Pilgrim | Welcoming Vampire is a narrow draw-on-small-ETB piece that doesn't leverage the death-trigger axis. Elas is a {W}{B} 2/2 deathtouch with a Teysa-doubled drain on creature death (stacks with Zulaport — every death drains each opponent for 4 with both online), plus ETB lifegain that pads K'rrik life payments. |

## Verification notes

- Both adds verified in collection: Meathook Massacre (DeckSafe surplus 1, owned 2, prior copy in Calamity Tax); Elas il-Kor (Moxfield CSV line 1101, DMU set, 1 owned). Elas was absent from the DeckSafe Full Card Matrix because that sheet is demand-driven (only includes cards currently in deck demand) — the underlying CSV is the source of truth for ownership.
- Both cuts confirmed safe: BMC is in 5 decks but owned 5, so cutting from DR returns the copy to the shared pool with no shortage. Welcoming Vampire is only in DR (3 owned, surplus 2 already), so cutting strands no other deck.
- Game Changer count unchanged at 3/3 (Farewell, Smothering Tithe, Teferi's Protection). Neither add is a Game Changer.
- Bracket 3 compliance unchanged. No new infinite combo enabled.
- Card text verified via card_lookup.py before applying.

## Engine math after swap

With Teysa + Zulaport + Elas + Meathook all online, every creature *you* control dying triggers six death events (Zulaport×2, Elas×2, Meathook×2 = drain 6 per opponent per death) on top of any other Layer 2 triggers (Sephiroth, Lich, Agent, etc.) doubled simultaneously. Meathook's opponent-side death trigger also gains you 2 life per opponent creature death, swinging removal-heavy turns hard in your favor.

## Decklist files

- New: `decks/diminishing-returns-20260505.txt`
- Archived: `archive/old_decklists/diminishing-returns-20260405-195326.txt` (the Phyrexian Tower fix), `archive/old_decklists/diminishing-returns-20260404-073759.txt` (original)
