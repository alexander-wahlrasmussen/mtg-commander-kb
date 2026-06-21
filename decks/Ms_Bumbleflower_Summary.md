# Ms. Bumbleflower — This Bunny Goes to Market

## Quick Reference

| Field | Value |
|---|---|
| **Commander** | Ms. Bumbleflower ({1}{G}{W}{U}, 1/5 Legendary Creature — Rabbit Citizen, Vigilance) |
| **Colors** | Bant (GWU) |
| **Archetype** | Spellslinger / tempo-control (draw engine + counter/steal) |
| **Bracket** | 3 (0 Game Changers) |
| **Game Changers** | None — 0/3 used |
| **Conversion Check** | **15/20** (4/3/3/5) |
| **Kill Window** | **Clock: T8 decap** (median; goldfish **ceiling** — see caveat) **/ T11 table** **(board)** (lab 2026-06-13, `bmf_clock_lab.py`) · Through interaction: slower, T11–14 *(unverified — goldfish only)*. **Ceiling caveat:** the goldfish dumps the deck's ~15 interaction pieces proactively for Bumbleflower triggers; the real control deck holds them up and closes slower. Willbreaker theft is goldfish-invisible. See `analysis/Ms_Bumbleflower_Clock_Lab_2026-06-13.md`. |
| **Ramp** | 14 sources (1 burst / 13 repeatable) · 52 mana sources, 38 land · in band (`ramp_audit.py` 2026-06-21) |

-----

## Commander Rules Text

Ms. Bumbleflower is a {1}{G}{W}{U} 1/5 with vigilance and one triggered ability:

> **Whenever you cast a spell, target opponent draws a card. Put a +1/+1 counter on target creature. It gains flying until end of turn. If this is the second time this ability has resolved this turn, you draw two cards.**

Two independent targets each cast: **target opponent** (who draws) and **target creature** (which gets the counter and flying). The creature target can be *any* creature — yours or an opponent's.

Key rulings (verified via `card_lookup.py`):

- **The ability resolves before the spell that triggered it, and resolves even if that spell is countered.** You get the draw/counter/flying (and any Willbreaker steal) regardless of whether the spell that caused the trigger ever resolves.
- **The "draw two" rider keys off the *second resolution* of this ability each turn** — i.e., the second spell you cast (that this triggers on) each turn. Cheap and free spells (Gitaxian Probe, Snap, Frantic Search) reliably get you to the second trigger.
- **The counter and flying both go to the same target creature.** You choose where the counter lands every cast — onto your own evasive threat, onto a draw-payoff creature, or (with Willbreaker) onto an opponent's creature to steal it.
- The opponent-draw is a **symmetric cost**: every spell you cast hands a card to an opponent of your choice. The deck is built to monetize that (see Layer 2).

The commander is the hub that ties three separate payoff packages together, but it is not a hard combo piece — it generates incremental advantage, not an instant win.

-----

## What the Deck Does

Cast a high volume of cheap spells. Each cast triggers Bumbleflower, and the deck is built so that every part of that trigger feeds a payoff: the forced opponent-draw feeds "opponents drawing" payoffs, the second-resolution draw-two feeds "you drawing" payoffs, and the +1/+1 counter feeds "counters placed" payoffs — or steals a creature outright. The result is a tempo-control deck that buries the table in card advantage while picking apart their board, then closes slowly with an evasive, counter-pumped threat, a Jolrael alpha strike, or a stolen army.

### Layer 1 — Spell Fuel & Selection (~10 pieces)

Cheap card-selection that powers multi-spell turns (hitting the second Bumbleflower trigger) and digs to the pieces that matter:

- **Brainstorm, Consider, Opt** — one-mana cantrips.
- **Gitaxian Probe** — free (Phyrexian mana); a "free" Bumbleflower trigger.
- **Snap** — free to cast (untaps two lands); re-triggers Bumbleflower at no net mana.
- **Frantic Search** — free (untaps three lands); draw two, discard two.
- **Consult the Star Charts / Planar Genesis / Growth Spiral** — deeper dig and land/ramp selection.
- **Auroral Procession** — {G}{U} instant, returns any card from your graveyard (rebuy a counter, a removal spell, or a finisher).

These are the engine's intake. The free spells in particular are what reliably converts a turn into "two Bumbleflower resolutions → draw two."

### Layer 2 — Draw / Cast Payoffs (~10 pieces)

The machine that turns the commander's triggers into a runaway lead:

- **Willbreaker** — *the premium synergy.* Whenever an opponent's creature becomes the target of a spell or ability you control, you gain control of it for as long as Willbreaker survives. Bumbleflower's "+1/+1 counter on target creature" is a targeted ability you control — aim it at an opponent's creature and **you steal it every time you cast a spell.** Pongify, Path, Swords, Beast Within, Generous Gift, Ty Lee's tap, and Generous Patron's support also target opponents' creatures and trip Willbreaker (the removal ones destroy; use the non-destructive effects to steal).
- **Faerie Mastermind** — whenever an opponent draws their *second* card each turn, you draw. Bumbleflower's forced opponent-draws actively turn this on. Also a {1}{U} flash flyer.
- **Smuggler's Share** — each end step, draw per opponent who drew 2+ cards that turn (again, your commander forces this) and make a Treasure per opponent who had 2+ lands enter. Card advantage *and* ramp off the table's natural play.
- **Tataru Taru** — ETB draw; then a tapped Treasure whenever an opponent draws on a turn that isn't theirs (once/turn). Your spells make opponents draw on *your* turn → Treasure every turn.
- **Jolrael, Mwonvuli Recluse** — whenever you draw your *second* card each turn (Bumbleflower's draw-two, or any cantrip stack), make a 2/2 Cat. Her activated ability is a finisher (Layer 5).
- **Ledger Shredder** — connives whenever *any* player casts their second spell each turn; grows itself and filters.
- **Fathom Mage** — draws whenever a +1/+1 counter is placed on it (evolve + Bumbleflower's counter both qualify).
- **Dusk Legion Duelist** — draws when one or more +1/+1 counters are put on it (once/turn). A clean Bumbleflower counter-target that replaces itself with a card.
- **Generous Patron** — support 2 on ETB; draws whenever you put counters on a creature you *don't* control. Pairs with Willbreaker-style targeting: grow an opponent's creature (steal it) and draw.
- **Esper Sentinel** — taxes/draws off each opponent's first noncreature spell. Pure card advantage on a {W} body.

### Layer 3 — Tempo & Re-trigger Creatures (4 pieces)

- **Whitemane Lion / Shrieking Drake** — flash/cheap bodies that bounce a creature you control on ETB. Re-buy an ETB, save a creature from removal, or reset a stolen creature; each recast is another Bumbleflower trigger.
- **Brazen Borrower** — flash bounce (Petty Theft) plus a 3/1 flash flyer.
- **Snapcaster Mage** — flashback a counter, a removal spell, or a cantrip from the yard; another spell cast = another trigger.

### Layer 4 — Ramp (~9 pieces)

Low curve, but enough acceleration to land Bumbleflower on T3–4 and chain spells: **Sol Ring, Arcane Signet, Bender's Waterskin** (rock that untaps on every other player's untap, any color), **Paradise Chocobo** (= Birds of Paradise), **Incubation Druid, Hardbristle Bandit** (untaps when you commit a crime — trivial here), **Farseek, Nature's Lore, Three Visits, Growth Spiral, Freestrider Lookout** (crime → land onto the battlefield).

### Layer 5 — Finishers (3 routes)

- **Jolrael's activated ability** — {4}{G}{G}: your creatures' base P/T become X/X where X = cards in hand. After the draw engine fills your hand, this is an anthem to 8–12 across your board (Cats, payoff creatures, stolen bodies) — the most concrete kill.
- **Evasive counter beats** — pile Bumbleflower's per-cast +1/+1 counters and flying onto one threat (or the 1/5 commander herself) for a growing aerial clock.
- **Sin, Unending Cataclysm** — {5}{G}{U} 5/5 flying trample that enters having scooped counters off any number of permanents and doubling them onto itself; can vacuum your own accumulated +1/+1 counters (or strip opponents') into a single huge flyer, and reseeds its counters onto another creature when it dies.

### The Play Pattern

T1–2: cantrip and ramp; Esper Sentinel / a mana dork on curve. T3–4: Bumbleflower. From here every spell draws an opponent a card (pick the least threatening, or the one whose draw turns on Faerie Mastermind/Smuggler's Share), places a counter, and — on the second cast each turn — draws you two. T5+: deploy Willbreaker and start stealing creatures with each cast, or assemble the draw payoffs and bury the table in cards while holding up a deep interaction suite. Close with Jolrael's pump, an evasive counter-stacked threat, or by swinging with a stolen board.

-----

## Kill Lines

### Line 1 — Jolrael Alpha Strike (primary)
With a full hand (routine for this deck) and a board of Cats, payoff creatures, and/or stolen bodies, Jolrael's {4}{G}{G} sets your team to X/X where X = cards in hand. 8–12 power across several attackers, several of them flying from Bumbleflower, closes from a developed board. ~2–3 turns from a stocked hand + board; the activation itself is one turn.

### Line 2 — Willbreaker Theft, then Swing
With Willbreaker in play, aim Bumbleflower's counter at an opponent's creature each cast to steal it (and it gains flying that turn — can attack immediately). Empty the opponents' best threats onto your side, then swing with their own board, optionally pumped by Jolrael. Grindy but board-dominating; lethal over several turns and doubles as removal.

### Line 3 — Evasive Counter Beats
A single creature (commander or a payoff body) accumulates a +1/+1 counter and flying every cast. Stack counters across a few turns, optionally dump them into Sin, and fly over. Slowest line; one removal spell on the carrier resets it.

*All three lines are combat-based and relatively slow. The deck out-values the table long before it out-damages it — closing speed, not card advantage, is the limiting factor.*

-----

## Conversion Check Breakdown

### Core Loop: 4/5
The loop — "cast cheap spells → each cast triggers Bumbleflower (opponent draws, +1/+1 counter, flying; second cast draws two) → draw payoffs and the counter-target cascade into advantage or theft" — is supported by roughly 16–18 cards: ~10 selection/fuel cantrips and ~10 draw/cast payoffs (with overlap). The identity is recognizable with the commander covered: a spellslinger card-advantage shell (Ledger Shredder, Faerie Mastermind, Jolrael, Fathom Mage, Esper Sentinel, Willbreaker). Not a 5 because the loop generates advantage rather than winning on its own, and Bumbleflower is the hub that maximizes it — the payoffs still fire off secondary triggers without her, but at much lower frequency.

**Checkpoint:** Cover the commander. ~10 cantrips, Ledger Shredder, Faerie Mastermind, Jolrael, Fathom Mage, Dusk Legion Duelist, Generous Patron, Esper Sentinel, Willbreaker. The identity (spellslinger card advantage) is clear.

### Kill Reliability: 3/5
Three real closing lines (Jolrael pump, Willbreaker theft, evasive counter beats), but all are combat-based and slow (5+ turns from engine-online to a three-opponent kill), and the deck has no burn, no infinite, and no alternate win. This is the classic "out-values the table but converts slowly" profile — the defining weakness. It can absolutely win from a strong position, but it stalls between *dominating* and *finishing*.

**Checkpoint:** Name two kills — Jolrael X/X alpha and Willbreaker steal-then-swing. Both want a board and several turns; neither ends the game the turn the engine comes online.

### Durability: 3/5
The draw engine is highly redundant and self-healing: after a wipe the deck simply out-draws the table back into threats, and the protection/recovery suite is deep (Heroic Intervention, Galadriel's Dismissal phase-out, Comeuppance, Whitemane Lion to bounce a creature out of removal, Auroral Procession / Snapcaster to rebuy spells). Bumbleflower re-casts cheaply at {1}{G}{W}{U}. Held back from 4 by thin *finisher* redundancy (a wipe resets the slow clock to zero even when the engine rebuilds) and by the engine's reliance on the commander as its frequency hub.

**Checkpoint:** Cyclonic Rift on T7. Re-cast Bumbleflower next turn, the card engine refills the board in 2–3 turns — but the kill clock restarts from scratch.

### Interaction Profile: 5/5
The deck's standout axis. 12+ pieces, diverse and almost entirely instant-speed:
- **Counters (7):** Wild Rose Rebellion (= Counterspell), An Offer You Can't Refuse, Rewind, Unwind, Long River's Pull, Reprieve, plus Tishana's Tidebinder (counters an activated/triggered ability) and Dawn Charm's third mode (counter a spell targeting you).
- **Removal (8+):** Path to Exile, Swords to Plowshares, Pongify, Beast Within, Generous Gift, Fractured Identity, Tragic Arrogance (one-sided-leaning wipe), Witch Enchanter (artifact/enchantment), plus Brazen Borrower / Sink into Stupor bounce and Ty Lee tap-down.
- **Protection / fog:** Heroic Intervention, Comeuppance, Riot Control, Aetherize, Galadriel's Dismissal, Dress Down.

Coverage spans creatures, noncreature spells, abilities, artifacts/enchantments, and combat — and most of it is held up at instant speed while the engine keeps drawing. Comfortably a 5.

**Checkpoint:** Opponent goes for a win — you have a hard counter (Counterspell/Rewind/An Offer), an ability counter (Tishana's), and a damage-prevention shell (Comeuppance/Riot Control), nearly all instant-speed, while still developing.

### Total: 15/20 — Solid foundation with one exploitable weakness.
The lowest axis is **Kill Reliability (3)**: the deck dominates the board and the card-advantage game but lacks a fast or decisive closer. The interaction profile (5) and redundant draw engine (4) make it durable and obstructive; turning a winning position into a *win* is the skill ceiling and the build's clearest upgrade target.

-----

## Expected Kill Window

**Goldfish: T8–10.** Engine online ~T4–5 (commander T3–4, cantrips flowing). With no resistance, a Jolrael alpha or an evasive counter-stacked threat closes around T8–10 — the card advantage arrives turns before the lethal board does.

**Through interaction: T11–14 (can grind to time).** The deck's deep interaction and self-healing draw engine let it survive almost indefinitely, but the slow combat kill means contested games drag. Against a fast combo pod it must lean on its counters to stay alive long enough to assemble a lethal board.

-----

## Bracket 3 Compliance

**Game Changers (0 of 3 used):** None. The deck runs well under the cap — there is room to add up to three GCs (e.g., Rhystic Study, Smothering Tithe, Cyclonic Rift, a tutor) as an upgrade path, almost all of which would directly raise Kill Reliability or Durability.

**Notable non-GC power cards:** Willbreaker, Esper Sentinel, Snapcaster Mage, Faerie Mastermind, Ledger Shredder, Tishana's Tidebinder, Fractured Identity, Tragic Arrogance.

**Infinite combos:** None. Willbreaker + Bumbleflower is a strong repeatable theft engine but is bounded by spells cast per turn and requires Willbreaker to survive — not an infinite loop. No Rule 0 flag required.

**Extra turns:** None.

**Mass land denial:** None. (Demolition Field is single-target; Fabled Passage / fetches are self-only.)

-----

## Pod Fit

1. **Out-values, under-closes.** The deck wins the long game on cards but needs time to convert. Strong against grindy/midrange pods; pressured by fast combo.
2. **Heavy stack presence.** Seven-plus counters and an ability counter make it a credible answer to the table's combo player while it develops.
3. **The forced opponent-draw is a real cost.** Every spell gifts a card — choose the recipient to feed the least dangerous player and to trigger Faerie Mastermind / Smuggler's Share / Tataru Taru. Against a Nekusar-style "draw-matters" opponent, the gift can backfire.
4. **Willbreaker invites removal.** Once you start stealing creatures, Willbreaker becomes the table's priority target; protect it (Heroic Intervention, counters) or expect it to die.
5. **Low early profile.** A 1/5 vigilance Rabbit and a pile of cantrips look harmless until the card lead becomes insurmountable — but the slow clock means opponents who race can close before the deck does.

-----

## Differentiation From Other Decks

| | Ms. Bumbleflower | The Calamity Tax (Glarb) | The Replication Crisis (Satya) |
|---|---|---|---|
| Colors | Bant (GWU) | Sultai | Jeskai |
| Engine | Cast-triggered draw + counter/steal | Control / tax / card advantage | Copy / clone |
| Win axis | Slow combat (Jolrael / steal / evasion) | Incremental control | Token/copy combat |
| Interaction | Very high (counters + removal) | Very high | Moderate |
| Closing speed | Slow | Slow | Moderate |

Bumbleflower is the roster's only Bant deck and its only "spells-cast → forced-draw → counter/steal" engine. It shares the *control* texture of Glarb but lacks his Sultai graveyard plan and closes through creatures rather than incremental inevitability; it shares Bant's protection tools with no other deck. No engine overlap.

-----

## Known Weaknesses

- **Slow, combat-only kill.** No burn, no infinite, no alt-win. The deck regularly reaches a dominant board/card state without a fast way to end the game — its single clearest weakness and the reason it scores 15 rather than higher.
- **Commander-centric engine frequency.** Payoffs work without Bumbleflower but fire far less often; repeated commander removal slows the engine even though the deck doesn't fold.
- **The forced opponent-draw can feed the wrong player** in a draw-punisher or storm-adjacent pod.
- **Willbreaker is a removal magnet** and the steal plan collapses the moment it dies.

-----

## Changelog

- **2026-05-30:** First formal audit. Verified all FF/ATLA-flavored and unfamiliar cards via `card_lookup.py`; confirmed 100 cards and **0 Game Changers** against `REF_Game_Changers_List.md`. Scored 4/3/3/5 = **15/20**. Identified Willbreaker + Bumbleflower targeted-steal as the premium synergy and the slow combat-only kill as the defining weakness. Reskins in use: Wild Rose Rebellion = Counterspell (ATLA), Paradise Chocobo = Birds of Paradise (FF).
