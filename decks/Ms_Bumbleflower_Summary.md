# Ms. Bumbleflower — This Bunny Goes to Market

## Quick Reference

| Field | Value |
|---|---|
| **Commander** | Ms. Bumbleflower ({1}{G}{W}{U}, 1/5 Legendary Creature — Rabbit Citizen, Vigilance) |
| **Colors** | Bant (GWU) |
| **Archetype** | Spellslinger / tempo-control (draw engine + counter/steal) |
| **Bracket** | 3 by GC count (0 Game Changers); ~4 in spirit (infinite line, pod-accepted 2026-06-19) |
| **Game Changers** | None — 0/3 used |
| **Conversion Check** | **16/20** (4/4/3/5) — Kill Reliability 3→4, 2026-07-03 quiet-exits package |
| **Kill Window** | **Clock: T8 decap** (median; goldfish **ceiling** — see caveat) **/ T11 table** (lab 2026-07-03, `bmf_clock_lab.py` @40k, all-lines) · Table front edge: **T9 15% / T10 35%** (was 3%/17% pre-package) · Close-mixture: **60% combat / 32% Approach / 8% Alarm** · Through interaction: slower *(unverified — goldfish only)*. **Ceiling caveat:** the goldfish dumps the deck's interaction proactively for Bumbleflower triggers; the real control deck holds it up and closes slower — but the Approach/Alarm exits are exactly the lines that *don't* need the dump. Willbreaker theft is goldfish-invisible. See `analysis/Ms_Bumbleflower_FeelsGreat_Rebuild_2026-07-03.md`. |
| **Ramp** | 13 sources (Misleading Signpost cut 2026-07-03; was 14, in band per `ramp_audit.py` 2026-06-21) · 38 land |

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

Cast a high volume of cheap spells. Each cast triggers Bumbleflower, and the deck is built so that every part of that trigger feeds a payoff: the forced opponent-draw feeds "opponents drawing" payoffs, the second-resolution draw-two feeds "you drawing" payoffs, and the +1/+1 counter feeds "counters placed" payoffs — or steals a creature outright. The result is a tempo-control deck that buries the table in card advantage while picking apart their board, then closes through whichever of its **quiet exits** the game hands it: a Jolrael alpha, a stolen army, a protected Approach of the Second Sun, or the Intruder Alarm bounce-loop. None of the exits is tutored — the 2026-07-03 lab measured the close-mixture at 60% combat / 32% Approach / 8% Alarm, so different games genuinely end differently.

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

### Layer 5 — Finishers (5 routes, none tutored — the 2026-07-03 "quiet exits" package)

- **Jolrael's activated ability** — {4}{G}{G}: your creatures' base P/T become X/X where X = cards in hand. After the draw engine fills your hand, this is an anthem to 8–12 across your board (Cats, payoff creatures, stolen bodies) — the most frequent kill (60% of goldfish closes).
- **Approach of the Second Sun** — the second cast *from hand* wins the game outright. The engine redraws it naturally (it goes 7th from top; the deck draws 2–4/turn), and **Reprieve** is a shortcut: the win checks that the first copy was *cast*, not that it resolved (ruling-verified), so bouncing your own first cast back to hand with Reprieve sets up the winning cast a turn later — 9 mana, then 7. Wipe-proof, combat-free, and protected by the counter suite. 32% of goldfish closes.
- **Intruder Alarm loop** — Alarm + Shrieking Drake or Whitemane Lion (self-bounce on ETB) + any repeatable dork: every recast is a creature entering (untap all creatures → retap the dork → recast, mana-neutral off a single dork) and a Bumbleflower trigger. "Target opponent draws a card," iterated without bound, draws the whole table out — they lose drawing from an empty library. With the Lion this happens at **instant speed**. 8% of goldfish closes; every piece except Alarm is a card the deck plays for value anyway.
- **Wizard Class lvl 3 + Fathom Mage** (enabler) — every draw puts a +1/+1 counter on a creature you control; aimed at Fathom Mage ("whenever a counter is put on this, you *may* draw"), it draws the library at will. Not a kill itself: it makes Jolrael's X enormous and puts whichever exit you need in hand. Levels 1–2 are honest value (no max hand size; draw two).
- **Evasive counter beats** — pile Bumbleflower's per-cast +1/+1 counters and flying onto one threat (or the 1/5 commander herself) for a growing aerial clock. The fallback.

### The Play Pattern

T1–2: cantrip and ramp; Esper Sentinel / a mana dork on curve. T3–4: Bumbleflower. From here every spell draws an opponent a card (pick the least threatening, or the one whose draw turns on Faerie Mastermind/Smuggler's Share), places a counter, and — on the second cast each turn — draws you two. T5+: deploy Willbreaker and start stealing creatures with each cast, or assemble the draw payoffs and bury the table in cards while holding up a deep interaction suite. Close with whichever exit the game dealt you: Jolrael's pump, a stolen board, a counter-protected Approach, or the Alarm loop.

-----

## Kill Lines

### Line 1 — Jolrael Alpha Strike (most frequent, 60% of goldfish closes)
With a full hand (routine for this deck) and a board of Cats, payoff creatures, and/or stolen bodies, Jolrael's {4}{G}{G} sets your team to X/X where X = cards in hand. 8–12 power across several attackers, several of them flying from Bumbleflower, closes from a developed board. ~2–3 turns from a stocked hand + board; the activation itself is one turn.

### Line 2 — Approach of the Second Sun (32% of goldfish closes; combat-free, wipe-proof)
Cast Approach ({6}{W}); it goes 7th from the top and the engine redraws it in ~2 turns (the deck draws 2–4/turn — Brainstorm/Consult dig it back faster). Cast it again *from hand* → **win the game**. The Reprieve shortcut (ruling-verified 2026-07-03: the win checks the first copy was **cast**, not resolved): with 9 mana, cast Approach and bounce your own cast back to hand with Reprieve — the winning second cast needs only 7 mana next turn, with the counter suite held up to protect it. This exit ignores board wipes, blockers, and creature removal entirely.

### Line 3 — Intruder Alarm Loop (8% of goldfish closes; table kill on the spot)
Alarm + Shrieking Drake (or Whitemane Lion, at instant speed) + any repeatable dork + the commander: each self-bounce recast unlocks the dork again (Alarm untaps all creatures on every ETB), so the loop is mana-neutral — and every iteration is a Bumbleflower trigger forcing an opponent to draw. Iterated without bound, all three opponents draw out and lose. Drake/Lion/dorks are value cards the deck already plays; only Alarm is combo-specific.

### Line 4 — Willbreaker Theft, then Swing
With Willbreaker in play, aim Bumbleflower's counter at an opponent's creature each cast to steal it (and it gains flying that turn — can attack immediately). Empty the opponents' best threats onto your side, then swing with their own board, optionally pumped by Jolrael. Grindy but board-dominating; goldfish-invisible, real in pods.

### Line 5 — Evasive Counter Beats (fallback)
A single creature (commander or a payoff body) accumulates a +1/+1 counter and flying every cast. Stack counters across a few turns and fly over. Slowest line; one removal spell on the carrier resets it.

*The close-mixture (which line actually tables the goldfish: 60/32/8) is the measured answer to "does it always win the same way?" — it doesn't, and nothing is tutored. Enabler: Wizard Class lvl 3 + Fathom Mage draws the library at will and feeds every line above.*

-----

## Conversion Check — 16/20

### Core Loop: 4/5
The loop — "cast cheap spells → each cast triggers Bumbleflower (opponent draws, +1/+1 counter, flying; second cast draws two) → draw payoffs and the counter-target cascade into advantage or theft" — is supported by roughly 16–18 cards: ~10 selection/fuel cantrips and ~10 draw/cast payoffs (with overlap). The identity is recognizable with the commander covered: a spellslinger card-advantage shell (Ledger Shredder, Faerie Mastermind, Jolrael, Fathom Mage, Esper Sentinel, Willbreaker). Not a 5 because the loop generates advantage rather than winning on its own, and Bumbleflower is the hub that maximizes it — the payoffs still fire off secondary triggers without her, but at much lower frequency.

**Checkpoint:** Cover the commander. ~10 cantrips, Ledger Shredder, Faerie Mastermind, Jolrael, Fathom Mage, Dusk Legion Duelist, Generous Patron, Esper Sentinel, Willbreaker. The identity (spellslinger card advantage) is clear.

### Kill Reliability: 4/5 (3→4, 2026-07-03 quiet-exits package)
Five closing lines, and the two new ones fix the old profile's defining hole: **Approach of the Second Sun** is an alternate win that ignores combat, wipes, and blockers (with the Reprieve cast-check shortcut and 6 counterspells to protect the winning cast), and the **Intruder Alarm loop** is an infinite that tables everyone on the spot from cards the deck already plays. The lab's close-mixture (60% combat / 32% Approach / 8% Alarm @40k) shows the exits genuinely fire, and the table clock's front edge doubled (P(table ≤ T10) 17%→35%). Not a 5: the exits are un-tutored by design (the deck finds them by drawing, which is what it does, but a dedicated combo deck this is not), and the median table close is still T11.

**Checkpoint:** Name two kills — Jolrael X/X alpha and a protected Approach. One ends the game through a board wipe; the other doesn't need the game to go long.

### Durability: 3/5
The draw engine is highly redundant and self-healing: after a wipe the deck simply out-draws the table back into threats, and the protection/recovery suite is deep (Heroic Intervention, Galadriel's Dismissal phase-out, Comeuppance, Whitemane Lion to bounce a creature out of removal, Auroral Procession / Snapcaster to rebuy spells). Bumbleflower re-casts cheaply at {1}{G}{W}{U}. Held back from 4 by thin *finisher* redundancy (a wipe resets the slow clock to zero even when the engine rebuilds) and by the engine's reliance on the commander as its frequency hub.

**Checkpoint:** Cyclonic Rift on T7. Re-cast Bumbleflower next turn, the card engine refills the board in 2–3 turns — but the kill clock restarts from scratch.

### Interaction Profile: 5/5
The deck's standout axis. 12+ pieces, diverse and almost entirely instant-speed:
- **Counters (6):** Wild Rose Rebellion (= Counterspell), An Offer You Can't Refuse, Unwind, Long River's Pull, Reprieve, plus Tishana's Tidebinder (counters an activated/triggered ability) and Dawn Charm's third mode (counter a spell targeting you). (Rewind cut 2026-07-03 — the clunkiest of the seven; Reprieve now double-duties as the Approach shortcut, so spend it reactively only when the Approach line isn't live.)
- **Removal (8+):** Path to Exile, Swords to Plowshares, Pongify, Beast Within, Generous Gift, Fractured Identity, Tragic Arrogance (one-sided-leaning wipe), Witch Enchanter (artifact/enchantment), plus Brazen Borrower / Sink into Stupor bounce and Ty Lee tap-down.
- **Protection / fog:** Heroic Intervention, Comeuppance, Riot Control, Aetherize, Galadriel's Dismissal, Dress Down.

Coverage spans creatures, noncreature spells, abilities, artifacts/enchantments, and combat — and most of it is held up at instant speed while the engine keeps drawing. Comfortably a 5.

**Checkpoint:** Opponent goes for a win — you have a hard counter (Counterspell/An Offer/Unwind), an ability counter (Tishana's), and a damage-prevention shell (Comeuppance/Riot Control), nearly all instant-speed, while still developing.

### Total: 16/20 — Solid, one point off elite.
The 2026-07-03 package raised the old lowest axis (Kill Reliability 3→4): the deck now converts dominance into wins through plural, non-telegraphed exits instead of stalling on combat math. The remaining soft axis is **Durability (3)** — the engine still leans on the commander as its frequency hub, and the combat lines still reset on a wipe (Approach doesn't, which is precisely why it was added).

-----

## Expected Kill Window

**Goldfish (lab 2026-07-03, @40k):** decap **T8** median (ceiling caveat applies) / table **T11** median, with the front edge at T9 15% / T10 35% — roughly double the pre-package odds of tabling by T10. Engine online ~T4–5 (commander T3–4, cantrips flowing).

**Through interaction: slower (unverified — goldfish only), but the exits change the texture.** The combat lines still slow down against blockers and wipes; Approach doesn't care about either, and casting it into open counter-mana *with your own counters held* is the play pattern the deck was missing. Against a fast combo pod, lean on the counter suite to survive, then close with Approach rather than trying to race on board.

-----

## Bracket 3 Compliance

**Game Changers (0 of 3 used):** None — deliberately. The 2026-07-03 upgrade chose exits that stay off the GC list and off the archenemy radar (no Rhystic/Tithe-class salience spikes). The 3-GC budget remains fully in reserve.

**Notable non-GC power cards:** Willbreaker, Esper Sentinel, Snapcaster Mage, Faerie Mastermind, Ledger Shredder, Tishana's Tidebinder, Fractured Identity, Tragic Arrogance, Approach of the Second Sun.

**Infinite combos:** One — **Intruder Alarm + Shrieking Drake/Whitemane Lion + a repeatable dork + the commander** (infinite casts / infinite forced opponent draws → table decks out). Pod-accepted per the 2026-06-19 house-rule revision (infinites OK; no MLD, no extra-turn chains — this is neither). Willbreaker + Bumbleflower remains a bounded, non-infinite theft engine.

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

- **The exits are found, not fetched.** No tutors by design (that's the "not the same combo every game" feature) — so in the ~60% of games where neither Approach nor Alarm shows up in time, the close is still slowish combat. Median table T11.
- **Commander-centric engine frequency.** Payoffs work without Bumbleflower but fire far less often; repeated commander removal slows the engine even though the deck doesn't fold.
- **The forced opponent-draw can feed the wrong player** in a draw-punisher or storm-adjacent pod.
- **Willbreaker is a removal magnet** and the steal plan collapses the moment it dies.
- **Approach telegraphs for one turn.** After the first cast, a table that's seen the card knows the second is coming — hold counters for the winning cast (it's a sorcery: both casts happen on your own turns, so plan the protection mana in advance). The Reprieve-split at least keeps the winning copy in hand instead of advertising a library dig.

-----

## Changelog

- **2026-07-03: The "quiet exits" package (feels-great rebuild).** −Misleading Signpost / −Sin, Unending Cataclysm / −Rewind → +**Intruder Alarm** / +**Approach of the Second Sun** / +**Wizard Class** (same-slot swaps: 3-drop rock→3-drop engine, 7-drop finisher→7-drop finisher, 4-mana counter→1-mana staged enchantment). Design target: fix "stalls between dominating and finishing" *without* raising archenemy salience (still 0 GCs, no tutors) or hurting smoothness. Measured (`bmf_clock_lab.py` @40k, all-lines on correlated draws; flow A/B @8k paired): table front edge T9 3→15% / T10 17→35% (median T11 holds); close-mixture 60% combat / 32% Approach / 8% Alarm; dead turns 0.609→**0.566**, hellbent@T8 18.2→**16.4%** (the Wizard-Class-for-Rewind trade *improved* flow). All three adds oracle-verified via `card_lookup.py` (incl. the Approach "cast, not resolved" ruling that legalises the Reprieve shortcut); GC list checked (none are GCs); aliases checked; Intruder Alarm confirmed undeployed (only in the shelved Berta candidate list); buy = Alarm + Approach ≈ €6 indicative. Kill Reliability 3→4 = **16/20**. Writeup: `analysis/Ms_Bumbleflower_FeelsGreat_Rebuild_2026-07-03.md`.
- **2026-05-30:** First formal audit. Verified all FF/ATLA-flavored and unfamiliar cards via `card_lookup.py`; confirmed 100 cards and **0 Game Changers** against `REF_Game_Changers_List.md`. Scored 4/3/3/5 = **15/20**. Identified Willbreaker + Bumbleflower targeted-steal as the premium synergy and the slow combat-only kill as the defining weakness. Reskins in use: Wild Rose Rebellion = Counterspell (ATLA), Paradise Chocobo = Birds of Paradise (FF).

## Decklist (100 cards)

### Commander (1)
1 Ms. Bumbleflower

### Steal & Combat Payoffs (5)
1 Willbreaker
1 Jolrael, Mwonvuli Recluse
1 Ty Lee, Chi Blocker
1 Generous Patron
1 Duelist's Heritage

### Card-Draw Engine & Tax (8)
1 Faerie Mastermind
1 Smuggler's Share
1 Tataru Taru
1 Esper Sentinel
1 Ledger Shredder
1 Dusk Legion Duelist
1 Fathom Mage
1 Freestrider Lookout

### Cantrips / Free Spells (7)
1 Gitaxian Probe
1 Snap
1 Frantic Search
1 Brainstorm
1 Consider
1 Opt
1 Consult the Star Charts

### Counterspells (8)
1 An Offer You Can't Refuse
1 Wild Rose Rebellion
1 Long River's Pull
1 Reprieve
1 Unwind
1 Tishana's Tidebinder
1 Dawn Charm
1 Sink into Stupor

### Spot Removal (8)
1 Path to Exile
1 Swords to Plowshares
1 Pongify
1 Beast Within
1 Generous Gift
1 Brazen Borrower
1 Witch Enchanter
1 Fractured Identity

### Mass Removal (3)
1 Promise of Loyalty
1 Tragic Arrogance
1 Aetherize

### Protection & Utility (7)
1 Comeuppance
1 Riot Control
1 Heroic Intervention
1 Galadriel's Dismissal
1 Hydroelectric Specimen
1 Dress Down
1 Lion Sash

### Bounce-to-Reuse (2)
1 Shrieking Drake
1 Whitemane Lion

### Quiet Exits — 2026-07-03 package (3)
1 Approach of the Second Sun
1 Intruder Alarm
1 Wizard Class

### Recursion (2)
1 Snapcaster Mage
1 Auroral Procession

### Mana Dorks (3)
1 Hardbristle Bandit
1 Incubation Druid
1 Paradise Chocobo

### Mana Rocks (3)
1 Sol Ring
1 Arcane Signet
1 Bender's Waterskin

### Ramp Spells (5)
1 Farseek
1 Nature's Lore
1 Three Visits
1 Growth Spiral
1 Planar Genesis

### Lands (35)
1 Adarkar Wastes
1 Branchloft Pathway
1 Breeding Pool
1 Brushland
1 Command Tower
1 Demolition Field
1 Deserted Beach
1 Dreamroot Cascade
1 Eiganjo, Seat of the Empire
1 Exotic Orchard
1 Fabled Passage
1 Flooded Strand
1 Floodfarm Verge
2 Forest
1 Glacial Fortress
1 Hallowed Fountain
1 Hengegate Pathway
1 Hinterland Harbor
1 Hushwood Verge
4 Island
1 Misty Rainforest
1 Overgrown Farmland
2 Plains
1 Reliquary Tower
1 Spara's Headquarters
1 Sunpetal Grove
1 Temple Garden
1 Windswept Heath
1 Yavimaya Coast
1 Yavimaya, Cradle of Growth

## Don't-Miss Rulings

- **Bumbleflower's ability resolves BEFORE the spell that triggered it, and resolves even if that spell is countered.** The draw / counter / steal happens first — so a Willbreaker steal off your spell goes through even if the spell itself gets countered.
- **The "draw two" is on the *second resolution* each turn** — cast at least two spells you trigger on. Free spells (Probe, Snap, Frantic Search) are how you reliably get there.
- **The counter and flying go to the same target creature; you pick it every cast.** Aim it at: (a) your evasive threat, (b) **Dusk Legion Duelist / Fathom Mage** to draw a card, or (c) an opponent's creature **with Willbreaker out** to steal it. You keep stolen creatures only while Willbreaker lives.
- **Willbreaker triggers on *any* of your targeted effects hitting an opponent's creature** — Bumbleflower's counter, Ty Lee's tap, Generous Patron's support. Pongify/Path/Swords also target, but they destroy; use the non-lethal effects to steal.
- **The forced opponent-draw is a real cost — but you choose who.** Feed the least threatening player, or feed someone to turn on **Faerie Mastermind** (you draw on their 2nd draw), **Smuggler's Share** (draw per opponent who drew 2+), and **Tataru Taru** (Treasure when an opponent draws on your turn). Don't gift a draw-punisher (Nekusar) for free.
- **Jolrael's pump sets *base* P/T to cards-in-hand and overwrites** — play it as a finisher with a full hand. Her Cat tokens come from your *second* draw each turn (which the commander's draw-two enables).
- **Dress Down turns off ALL creature abilities, including yours** — use it to blank an opponent's engine/combo, not while you're relying on your own creatures; it sacrifices itself at end step.
- **Generous Gift / Beast Within hand the target's controller a token** — fine as removal, just count the body you're giving back.
- **Approach of the Second Sun wins if the first copy was CAST, not resolved** (ruling-verified). So Reprieve targeting your *own* Approach on the stack returns it to hand with the cast already banked — the next cast from hand wins. Both casts are sorcery-speed (your turn); the second can be countered, so hold protection for it.
- **The Intruder Alarm loop needs only one repeatable dork** — Drake costs {U}, Chocobo makes 1 any; Incubation Druid with a Bumbleflower counter makes 3 by itself (fuels the Lion loop alone). Alarm's untap is symmetric: opponents' creatures untap too, so don't deploy it early as a value card — it's a combo turn card (or instant-speed with Lion on the end step before yours).
- **Wizard Class levels are activated abilities, not casts** — no Bumbleflower trigger from leveling. Lvl 3 aimed at Fathom Mage: each draw is "may", so you draw exactly as deep as you want.

## Piloting Notes (for borrowers)

**Mulligan.** Looking for: **lands + ramp + a couple of cheap spells, with Bumbleflower reachable by T3–4.** An all-interaction hand with no payoff and no route to the commander is a toss, however pretty the curve — the engine only pays once Bumbleflower plus a payoff are converting the cheap spells into cards and bodies.

- **Keep:** ramp + cantrips + a payoff (Willbreaker, Faerie Mastermind, Esper Sentinel) or the commander.
- **Toss:** no-land hands; all-payoff with no cantrips to fuel the triggers; all-interaction with no engine.

**Threats & timing.**

- **How you lose:** **the race.** The kill is still slow-median; fast combo pods can win before you assemble lethal. Lean on your counters to buy time — and know that your fastest honest outs against a racing table are a Reprieve-split Approach (9 mana, then 7 with counter backup) or an end-step Lion into the Alarm loop.
- **Willbreaker is a removal magnet** — once you're stealing creatures, the table targets it; protect it (Heroic Intervention, hold a counter) or the steal plan collapses.
- **Interaction:** very deep — 12+ pieces, mostly instant-speed. 7+ counters (Wild Rose Rebellion = Counterspell, An Offer, Rewind, Unwind, Long River's Pull, Reprieve, Tishana's Tidebinder, Dawn Charm), 8+ removal (Path, Swords, Pongify, Beast Within, Generous Gift, Fractured Identity, Tragic Arrogance, Witch Enchanter), plus a fog/protection shell (Heroic Intervention, Comeuppance, Riot Control, Aetherize, Galadriel's Dismissal phase-out). You can hold up answers and keep drawing.
- **Low early profile** — a 1/5 Rabbit and cantrips look harmless until the card lead is insurmountable. You out-value the table long before you out-damage it; the skill is knowing when to stop drawing and start killing.

## Reskins (for borrowers)

| On the card | Really is | What it does |
|---|---|---|
| Wild Rose Rebellion | Counterspell | {U}{U} instant; counter target spell. |
| Paradise Chocobo | Birds of Paradise | {G} 0/1 flyer; {T}: add one mana of any color. |

*The deck also runs cards under official Universes Beyond names (Tataru Taru, Sin Unending Cataclysm, Ty Lee Chi Blocker, Bender's Waterskin, Galadriel's Dismissal, Long River's Pull, Hydroelectric Specimen, Witch Enchanter) — these are real printed cards with their own readable text, not aliases.*
