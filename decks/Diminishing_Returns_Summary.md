# Diminishing Returns — Teysa Karlov

## Quick Reference

| Field | Value |
|---|---|
| **Commander** | Teysa Karlov ({2}{W}{B}, 2/4 Legendary Creature — Human Advisor) |
| **Colors** | Orzhov (WB) |
| **Archetype** | Aristocrats / Sacrifice-Drain |
| **Bracket** | 3 (3 Game Changers used; no early two-card infinites; no MLD; no extra turns) |
| **Game Changers** | Farewell, Smothering Tithe, Teferi's Protection (3 of 3 slots used) |
| **Conversion Check** | **17/20** (5/4/4/4) |
| **Kill Window** | Clock: T9 decap / T12+ table (lab 2026-06-10, `dr_clock_lab.py`) · Through interaction: slower *(unverified — goldfish lab only; no interaction model)*. The old "Goldfish T7–9" claim was falsified: it held only as the back edge of the decap clock and conflated the two clocks — the board swing decapitates T9, the drain engine tables T12+. |
| **Ramp** | 12 sources (1 burst / 11 repeatable) · 48 mana sources, 36 land · in band (`ramp_audit.py` 2026-06-21) |

-----

## Commander Rules Text

Teysa Karlov has two abilities:

1. **Death trigger doubling:** If a creature dying causes a triggered ability of a permanent you control to trigger, that ability triggers an additional time.
2. **Token keyword granting:** Creature tokens you control have vigilance and lifelink.

Key rulings: Teysa doubles the number of triggers, not the effect of each trigger. She doubles triggers from any permanent you control, not just your own creatures dying. Tokens with lifelink and vigilance are relevant for stabilizing after drain chains or blocking while attacking with an aristocrats board.

-----

## What the Deck Does

The deck converts creatures into damage through a three-part engine:

**Layer 1 — Sacrifice Outlets (8 permanents + 1 land):** Viscera Seer (free, scry), Carrion Feeder (free, grows), Yahenni (free, indestructible), Woe Strider (free, scry — also ETBs a Goat token), Ashnod's Altar (free, {C}{C}), Phyrexian Altar (free, any color), Altar of Dementia (free, mill), Priest of Forgotten Gods ({T} + sac 2, draws + mana + edict), Phyrexian Tower (land, sac for {B}{B}). Skullclamp and Soldevi Adnate also function as pseudo-sac outlets (Adnate is {T} + sac black/artifact creature → {B} equal to its mana value; once per turn unless untapped). Razaketh tutors (pay 2 life + sac another creature). Sephiroth front face is a once-per-ETB and once-per-attack sac outlet that also draws a card. Endrek Sahr generates Thrull tokens that become sac fodder (X 1/1s per creature spell cast, where X is the spell's mana value); Teysa grants those tokens vigilance and lifelink. *Endrek self-limit:* state trigger sacrifices Endrek when you control 7+ Thrulls — flips from feature to liability if you can't sink them faster than you make them, but in this deck the death payoffs are happy to consume both Thrulls and Endrek himself.

**Layer 2 — Death-Triggered Payoffs (doubled by Teysa):**
- **Zulaport Cutthroat** — each opponent loses 1 per creature you control dying. Pure death trigger; doubled.
- **Elas il-Kor, Sadistic Pilgrim** — {W}{B} 2/2 Deathtouch. Death trigger: each opponent loses 1 per other creature you control dying. Stacks with Zulaport — both Teysa-doubled, so every creature death drains each opponent for 4. Also gains 1 life per other creature ETB (not doubled by Teysa, but pads the K'rrik life bill).
- **The Meathook Massacre** — {X}{B}{B} legendary Enchantment. ETB: every creature gets -X/-X (flexible board wipe / pinpoint removal). Plus *two* death triggers, both doubled by Teysa: a creature you control dying drains each opponent for 1; a creature an opponent controls dying gains you 1. With Teysa: 2 drain on yours dying, 2 lifegain on theirs.
- **Nadier's Nightblade** — each opponent loses 1 whenever a *token* you control leaves the battlefield. Doubled by Teysa when the token leaves *by dying* (per Teysa rulings, "leaves the battlefield" triggers are doubled if caused by a creature dying).
- **Agent of the Iron Throne** — *an Enchantment (Background), not a creature.* Grants Teysa the trigger "whenever an artifact or creature you control is put into a graveyard from the battlefield, each opponent loses 1 life." The granted ability *is* on Teysa, so when a creature dies, Teysa's own ability triggers and is then doubled by Teysa.
- **Midnight Reaper** — 1 damage to you, draw a card on each *nontoken* creature you control dying. Doubled. Note: Endrek's Thrull tokens dying does NOT trigger Reaper.
- **Syr Konrad** — 1 damage to each opponent. Death-on-battlefield half is doubled. The other clauses (creature card entering graveyard from non-battlefield zones; creature card leaving your graveyard) are not death triggers and are not doubled.
- **Vindictive Lich** — modal death trigger; with Teysa, two separate triggers, each picking 1+ modes, each constrained to different players within that trigger. You can pick "lose 5" twice on different (or same) opponents.
- **Kokusho, the Evening Star** — death trigger drain 5 / gain 15. Doubled to 10 / 30.
- **Sephiroth, Fabled SOLDIER** — *Front face ({2}{B}, 3/3):* Two abilities. **(1)** "Whenever Sephiroth enters or attacks, you may sacrifice another creature. If you do, draw a card." → Sephiroth doubles as a sac outlet AND a draw engine on ETB and on each of his attacks. **(2)** "Whenever another creature dies, target opponent loses 1 life and you gain 1 life. If this is the fourth time this ability has resolved this turn, transform Sephiroth." → Single-target drain (not each opponent), doubled by Teysa to 2 resolutions per death. **2 creature deaths with Teysa out = 4 trigger resolutions = transform.** *Back face — Sephiroth, One-Winged Angel (5/5 flying):* Emblem: "Whenever a creature dies, target opponent loses 1 life and you gain 1 life." The emblem is **not** doubled by Teysa (emblems aren't permanents) but persists indefinitely if Sephiroth is later removed — meaningful durability. Attack ability: "Whenever Sephiroth attacks, you may sacrifice any number of other creatures. If you do, draw that many cards." → high-volume draw engine.

**Layer 2b — Engine Pieces NOT Doubled by Teysa:**
- **Gray Merchant of Asphodel** — *ETB trigger*, not death. Sacrificing and reanimating Gary triggers the drain on each ETB but Teysa does not double it. With K'rrik (3 devotion from {B/P}{B/P}{B/P}), Teysa (1 from {W}{B}), Gary himself (2 from {B}{B}), devotion is 6 minimum: each opponent loses 6, you gain 18.
- **Mirkwood Bats** — triggers on creating *or sacrificing* a token. Token creation triggers are not death triggers; sacrifice triggers are not death triggers per Teysa rulings. Not doubled. Note that *non-token* creature deaths (Gravecrawler, Gary, Kokusho) do not trigger Mirkwood Bats at all.
- **Morbid Opportunist** — death trigger, but capped at "only once each turn." Teysa's doubling effectively does nothing.
- **Desecrated Tomb** — triggers on creature cards leaving your graveyard, which is not a creature dying.

**Layer 3 — Recursive Creatures and Reanimation:** Gravecrawler recasts from graveyard for {B} if you control a Zombie. On-board Zombies in the 99: Gravecrawler itself, Gray Merchant, Midnight Reaper, Stitcher's Supplier. Reanimate, Animate Dead, Necromancy, Victimize, and Living Death recycle high-value creatures. K'rrik converts each {B} pip in any cost to 2 life (he changes how you pay {B}, not what generic costs), enabling explosive starts where Dark Ritual costs 2 life and yields {B}{B}{B}.

**The play pattern:** Deploy a sac outlet and a drain payoff in the early game. Land Teysa to double the death-triggered payoffs. Sacrifice creatures, drain the table, draw cards off the deaths, replay creatures from graveyard or via reanimation. Razaketh tutors any missing piece. K'rrik lets you pay life instead of black mana, and the drain triggers pay the life back with interest.

-----

## Kill Lines

**Line 1 — Gravecrawler Loop**
Gravecrawler + Phyrexian Altar + any Zombie on the battlefield + any drain payoff. Sacrifice Gravecrawler to Phyrexian Altar for {B}. Recast Gravecrawler for {B}. Each cycle triggers drain payoffs, doubled by Teysa. Repeat until all opponents are dead. This is mana-neutral and deterministic once assembled. Requires 4 pieces (Gravecrawler, Phyrexian Altar, a Zombie, a drain piece), but Razaketh can tutor all of them.

**Line 2 — Gray Merchant Recursion**
Gray Merchant's drain is an ETB trigger, so Teysa does *not* double it. Each ETB still drains for devotion. With K'rrik ({B/P}{B/P}{B/P} = 3 devotion), Teysa ({W}{B} = 1), and Gary himself ({B}{B} = 2), devotion is 6 minimum: each opponent loses 6, you gain 18. Sacrifice Gary, reanimate him with Animate Dead / Necromancy / Victimize, drain again. Two ETBs in a 4-player pod = 36 life off the table; three usually closes once Teysa-doubled deaths from Gary triggering Zulaport / Agent / Sephiroth / Lich are added on top.

**Line 3 — Kokusho Drain Chain**
Kokusho dies → each opponent loses 5, you gain 15. Teysa doubles: each opponent loses 10, you gain 30. Sacrifice and reanimate repeatedly. Two Kokusho deaths (doubled) = 60 life drained from the table.

**Line 4 — Living Death Reset**
Stock the graveyard through self-mill (Stitcher's Supplier, Altar of Dementia), looting, and natural play. Living Death sacrifices all creatures on the battlefield (triggering all your death payoffs, doubled by Teysa) and returns everything from your graveyard. Your graveyard is stacked with Gray Merchant, Kokusho, Razaketh, Sephiroth, and drain creatures. Opponents' graveyards are usually worse.

**Line 5 — Razaketh Tutor Chain**
Razaketh pays 2 life + sacrifices a creature to tutor any card. With token generators (Endrek Sahr Thrulls, Desecrated Tomb bats from graveyard recursion, Woe Strider goat ETB token), Razaketh finds the exact combination needed to close. Typical line: tutor Gravecrawler + Phyrexian Altar + drain piece for Line 1.

-----

## K'rrik Integration (MH3 Upgrade)

K'rrik, Son of Yawgmoth converts every {B} in any mana cost to 2 life. This transforms the deck's speed:

| Card | Normal Cost | With K'rrik |
|---|---|---|
| Dark Ritual | {B} → {B}{B}{B} | 2 life → {B}{B}{B} |
| Reanimate | {B} + life | 2 life + creature MV life |
| Animate Dead | {1}{B} | {1} + 2 life |
| Necromancy | {2}{B} | {2} + 2 life |
| Living Death | {3}{B}{B} | {3} + 4 life |
| Gray Merchant | {3}{B}{B} | {3} + 4 life (drain ~6+ per ETB; Gary is *not* Teysa-doubled — ETB trigger) |
| Kokusho | {4}{B}{B} | {4} + 4 life (Teysa-doubled death: drain 30 from the table per resolution) |
| Gravecrawler | {B} | 2 life (free with Phyrexian Altar) |
| Victimize | {2}{B} + sac | {2} + 2 life + sac |

K'rrik also contributes 3 devotion to black ({B/P}{B/P}{B/P} counts toward devotion), boosting Gray Merchant ETB drains. He has lifelink, partially offsetting life payments. He enables turn 3–4 explosive starts (Dark Ritual for 2 life → chain into reanimation) that the deck previously couldn't achieve until turn 5–6.

The life cost is a non-issue in this deck. Every drain trigger gains life. A single Gary ETB or Teysa-doubled Kokusho death repays any life K'rrik spent.

-----

## Conversion Check Breakdown

### Core Loop: 5/5

The loop is "sacrifice creatures → Teysa-doubled death triggers (Layer 2) plus untoubled engine pieces (Layer 2b) → drain opponents, draw cards, generate tokens → sacrifice again." 26+ cards directly serve this loop across three layers (9 sac outlets counting Phyrexian Tower, 8 death-triggered payoffs, 4 engine pieces not doubled, 5 reanimation spells, plus Gravecrawler, K'rrik, Dark Ritual, and card-draw creatures). The loop is immediately identifiable from the decklist. Teysa is a powerful accelerant (doubling death triggers is massive on Kokusho, Sephiroth, Lich, Zulaport) but the deck still functions without her — sacrificing creatures to drain is the plan regardless.

**Checkpoint:** Cover the commander. The 99 screams aristocrats sacrifice — sac outlets, drain payoffs, recursive creatures, reanimation. Unmistakable.

### Kill Reliability: 4/5

Five distinct closing lines, including one deterministic loop (Gravecrawler + Phyrexian Altar). Razaketh tutors any missing piece directly. Gray Merchant and Kokusho each threaten lethal in 1–2 sacrifice/reanimate cycles with Teysa out. Estimated 2–3 turns from engine-online to kill. K'rrik accelerates the clock by reducing the mana needed for each reanimation cycle.

Doesn't reach 5 because the deterministic loop requires 4 specific pieces. The non-loop lines (Gary recursion, Kokusho chain) are strong but require reanimation spells in hand and a turn cycle between each iteration. No single-card "I win" equivalent to Tooth and Nail.

**Checkpoint:** Gravecrawler loop kills deterministically. Gary recursion kills in 2 cycles. Both achievable within 2–3 turns of engine-online.

### Durability: 4/5

Five reanimation spells recover key creatures. Gravecrawler self-recurs from the graveyard. Living Death is a full-board reset that favors the deck with the fullest graveyard. Teferi's Protection and Flawless Maneuver dodge board wipes entirely. Phyrexian Tower lets you sacrifice in response to removal for value. K'rrik enables fast rebuilds by converting life into mana.

After a board wipe: reanimate a key creature for 1–3 mana, or cast Living Death to rebuild everything at once. Threatening again in 1–2 turns. Teysa is an accelerant, not a dependency — her removal doesn't stop the sacrifice plan, just halves the trigger output.

Doesn't reach 5 because the deck fundamentally needs creatures on the battlefield to function. Repeated wraths with no reanimation in hand is a real vulnerability. Graveyard exile (Bojuka Bog, Rest in Peace) shuts off Gravecrawler recursion and Living Death simultaneously.

**Checkpoint:** Cyclonic Rift on turn 7. Reanimate Razaketh (1 mana + 8 life, or just 10 life with K'rrik), sacrifice any creature to tutor the next reanimation target or Gravecrawler. Threatening again in 1–2 turns.

### Interaction: 4/5

12 interaction pieces across multiple types:

- **Targeted removal (5):** Swords to Plowshares, Path to Exile, Generous Gift, Feed the Swarm, Cathar Commando
- **Edict effects (2):** Merciless Executioner, Plaguecrafter — these are *ETB* triggers, not death triggers, so Teysa does **not** double them. Each still forces every opponent to sacrifice once. (Fleshbag Marauder is in the maybeboard, not the maindeck.)
- **Board wipes (2):** Toxic Deluge, Farewell
- **Protection (5):** Teferi's Protection, Flawless Maneuver, Selfless Spirit, Grand Abolisher, Lightning Greaves
- **Creature protection (2):** Giver of Runes, Mother of Runes

The edict creatures double as sacrifice fodder — they interact with the table AND feed the engine. Grand Abolisher protects combo turns. Teferi's Protection is a hard reset button.

Doesn't reach 5 because the deck has zero counterspells. Orzhov can't counter spells, so a combo that resolves on the stack can't be stopped — only prevented proactively (Grand Abolisher on your turn) or punished afterward (Fleshbag effects). Against the pod's combo player, this is a meaningful gap compared to blue decks.

### Total: 17/20 — Structurally excellent. Pilot skill is the main variable.

The MH3 upgrades (K'rrik, Phyrexian Tower) don't change the total score but meaningfully improve the deck's speed and consistency within the existing framework. K'rrik accelerates kill lines by 1–2 turns. Phyrexian Tower adds a sac outlet on a land slot.

-----

## Bracket 3 Compliance

- **Game Changers:** Farewell, Smothering Tithe, Teferi's Protection (3 of 3 slots used). All three GC slots are occupied — no further Game Changers can be added without a swap.
- **Infinite combos:** The Gravecrawler loop is technically infinite but requires 4 pieces (Gravecrawler + Phyrexian Altar + Zombie + drain payoff) and does not consistently assemble before turn 6. Compliant with B3's "no early two-card infinite combos" restriction.
- **Extra turns:** None.
- **Mass land denial:** None.

-----

## Pod Fit

The aristocrats archetype has natural pod advantages:

1. **Hard to interact with.** Drain triggers don't target. Sacrifice triggers can't be countered. The damage comes from multiple small sources, not one big spell.
2. **Punishes removal.** Opponents removing your creatures triggers your payoffs. A board wipe against this deck often deals more damage to the table than it prevents.
3. **Grinds through stax.** The deck operates on small mana increments (1–3 mana per action) and recursive creatures. Tax effects like Rhystic Study or Thalia don't meaningfully slow it.
4. **Weak to graveyard hate.** Rest in Peace, Dauthi Voidwalker, and Bojuka Bog all shut off key lines. The deck has limited answers to enchantments (Feed the Swarm, Generous Gift, Cathar Commando only).
5. **Weak to combo without blue.** No counterspells means the combo player can resolve their win condition if the deck doesn't have Grand Abolisher or a sacrifice-based answer available.

-----

## Differentiation From Other Decks

| | Teysa (Diminishing Returns) | Scarab God (Curse of the Scarab) |
|---|---|---|
| Engine | Sacrifice + death triggers | Zombie tribal + drain |
| Token role | Sacrifice fodder | Persistent army |
| Commander role | Passive doubler | Active reanimator + scry |
| Win speed | Fast (2–3 turns from engine) | Moderate (3–4 turns) |
| Color access | WB (removal + protection) | UB (counters + card draw) |
| Graveyard dependency | High (Gravecrawler, reanimation) | Moderate (Scarab God exiles from GY) |

No overlap in engine pieces. The decks share only generic staples (Sol Ring, lands).

-----

## Decklist (100 cards)

### Commander (1)

1 Teysa Karlov

### Sacrifice Outlets (8)

1 Viscera Seer
1 Carrion Feeder
1 Yahenni, Undying Partisan
1 Woe Strider
1 Ashnod's Altar
1 Phyrexian Altar
1 Altar of Dementia
1 Priest of Forgotten Gods

### Death-Triggered Payoffs — Teysa-doubled (9)

1 Zulaport Cutthroat
1 Elas il-Kor, Sadistic Pilgrim
1 The Meathook Massacre
1 Nadier's Nightblade
1 Agent of the Iron Throne
1 Syr Konrad, the Grim
1 Midnight Reaper
1 Kokusho, the Evening Star
1 Sephiroth, Fabled SOLDIER

### Engine Pieces — Not Teysa-doubled (4)

1 Gray Merchant of Asphodel
1 Mirkwood Bats
1 Morbid Opportunist
1 Desecrated Tomb

### Token Generator (1)

1 Endrek Sahr, Master Breeder

### Mana Acceleration (2)

1 K'rrik, Son of Yawgmoth
1 Dark Ritual

### Edict Creatures (2)

1 Merciless Executioner
1 Plaguecrafter

### Reanimation (5)

1 Reanimate
1 Animate Dead
1 Necromancy
1 Victimize
1 Living Death

### Tutor / Death-Trigger Payoff (2)

1 Razaketh, the Foulblooded
1 Vindictive Lich

### Recursive Creatures (2)

1 Gravecrawler
1 Stitcher's Supplier

### Card Draw (3)

1 Dark Confidant
1 Skullclamp
1 Soldevi Adnate

### Commander Protection (5)

1 Lightning Greaves
1 Giver of Runes
1 Mother of Runes
1 Selfless Spirit
1 Skrelv, Defector Mite

### Board Protection (3)

1 Teferi's Protection
1 Flawless Maneuver
1 Grand Abolisher

### Targeted Removal (4)

1 Swords to Plowshares
1 Path to Exile
1 Generous Gift
1 Feed the Swarm

### Flexible Removal (2)

1 Cathar Commando
1 Recruiter of the Guard

### Board Wipes (2)

1 Toxic Deluge
1 Farewell

### Ramp Artifacts (6)

1 Sol Ring
1 Arcane Signet
1 Fellwar Stone
1 Mind Stone
1 Thought Vessel
1 Wayfarer's Bauble

### Equipment (1)

1 Swiftfoot Boots

### Tax Effects (2)

1 Esper Sentinel
1 Smothering Tithe

### MDFC Land/Spell (1)

1 Malakir Rebirth

### Lands (35 + Malakir Rebirth above = 36 total mana sources)

1 Command Tower
1 Exotic Orchard
1 Phyrexian Tower
1 Urborg, Tomb of Yawgmoth
1 Urza's Saga
1 Bojuka Bog
1 Takenuma, Abandoned Mire
1 Eiganjo, Seat of the Empire
1 Castle Shimura
1 Demolition Field
1 Vault of Champions
1 Concealed Courtyard
1 Caves of Koilos
1 Fabled Passage
1 Prismatic Vista
1 Polluted Delta
1 Verdant Catacombs
1 Desolate Mire
1 Gemstone Caverns
8 Plains
8 Swamp

### Maybeboard

1 Fleshbag Marauder — third edict effect, currently held out of the main 99

-----

## Audit Log

### 2026-05-13 — Formal Conversion Check audit

**Score holds at 17/20 (5/4/4/4).** Decklist `diminishing-returns-20260505.txt` verified: 99 main + 1 commander = 100 cards. GC count 3/3 (Farewell, Smothering Tithe, Teferi's Protection) — cross-checked against `REF_Game_Changers_List.md`. Bracket 3 compliant: the Gravecrawler loop is a 4-piece infinite (Gravecrawler + free sac outlet + other Zombie + drain payoff) that doesn't reliably assemble before turn 6; no extra turns; no MLD.

**Card text re-verified against local Scryfall data:** Teysa Karlov, Sephiroth (front + back face), Agent of the Iron Throne (it's a Background Enchantment that grants the death trigger to commander creatures you own — i.e., to Teysa), K'rrik, Mirkwood Bats, Nadier's Nightblade, Vindictive Lich, Endrek Sahr, Razaketh, Gravecrawler, Kokusho, Gray Merchant, Zulaport Cutthroat, Carrion Feeder, Midnight Reaper, Syr Konrad, The Meathook Massacre, Elas il-Kor, Soldevi Adnate, Phyrexian Altar, Woe Strider, Desecrated Tomb, Morbid Opportunist.

**Axis-by-axis:**
- **Core Loop 5/5** — 26+ engine pieces (9 sac outlets, 9 Teysa-doubled death payoffs, 4 non-doubled engine pieces, 5 reanimation spells, plus Gravecrawler, K'rrik, Dark Ritual, recursive creatures, card-draw creatures). The aristocrats loop is unmistakable from the decklist.
- **Kill Reliability 4/5** — 5 distinct lines (Gravecrawler loop, Gary recursion, Kokusho chain, Living Death reset, Razaketh tutor). One deterministic loop. K'rrik accelerates the clock by 1–2 turns. Held under 5 because the deterministic loop needs 4 pieces and no single-card "I win" exists.
- **Durability 4/5** — 5 reanimation spells, Gravecrawler self-recurs, Living Death full reset, Teferi's Protection + Flawless Maneuver dodge wipes, Phyrexian Tower for sac-to-protect, K'rrik enables fast rebuilds. Sephiroth's back-face emblem adds a passive drain that persists through removal once transformed. Held under 5 because graveyard hate (RIP, Bojuka Bog, Dauthi Voidwalker) shuts off both Gravecrawler recursion and Living Death simultaneously.
- **Interaction 4/5** — 12 pieces (5 targeted removal + 2 edict + 2 board wipes + 3 board protection including Grand Abolisher). Two free protection spells (Teferi's, Flawless). Held under 5 because Orzhov can't counter — combos that resolve on the stack are unanswerable.

**Errors corrected during the audit (documentation only, no card swaps):**
1. **Sephiroth was massively underdescribed.** Prior summary captured only the death-trigger drain (and even that with errors — said "1 to a single target opponent" but missed the lifegain clause, and said "transforms after 2 creature deaths" without explaining the 4-trigger-resolution mechanism behind that number). Missed entirely: front-face "Whenever Sephiroth enters or attacks, you may sacrifice another creature. If you do, draw a card." (Sephiroth is also a sac outlet AND a draw engine, not just a death-drain piece). Back-face Sephiroth, One-Winged Angel (5/5 flying), its emblem death-drain (not doubled by Teysa since emblems aren't permanents but persists through Sephiroth's removal), and the back-face attack ability (sac any number → draw that many) — all missing. Full rewrite applied to the Sephiroth entry in Layer 2.
2. **"Sephiroth tokens" in Razaketh kill line** — Sephiroth doesn't create tokens. Razaketh's token fuel is Endrek Sahr Thrulls, Desecrated Tomb bats, and Woe Strider's ETB Goat. Corrected.
3. **Endrek Sahr 7-Thrull self-sacrifice clause** — added to the Layer 1 description as a feature-not-bug note (Endrek dying triggers all death payoffs anyway).
4. **Soldevi Adnate tap cost** — Adnate requires {T} so he's once per turn unless untapped. Clarified.
5. **Woe Strider ETB Goat token** — wasn't surfaced before. Noted as part of the Razaketh fuel and Layer 1 description.

The Sephiroth correction is the most consequential. The deck's actual durability is slightly higher than the prior summary suggested (emblem persists through removal once you transform), and Sephiroth's draw output is meaningfully larger (he draws on every ETB, every attack, and every back-face attack lets you cash in your whole board). None of this changes the axis scoring — Durability stays at 4/5 because graveyard hate remains the structural ceiling, and the emblem alone doesn't tilt that.

No card swaps applied during this audit.

### 2026-06-10 — Kill-turn lab: "Goldfish T7–9" falsified

**`scripts/dr_clock_lab.py` (12k trials): decap median T9 (11% T7, 37% T8, 66% T9) / table median beyond T12 (30% by T12).** Kill Window field updated to the lab citation. Key findings (full writeup: `analysis/Diminishing_Returns_Clock_Lab_2026-06-10.md`):

1. **The two clocks diverge.** The wide board swing decapitates like a combat deck (T9); the drain engine is the table clock and its volume is low (~5 deaths/game in goldfish). The old claim conflated them.
2. **Death volume, not multipliers, is the bottleneck.** Once Teysa + payoffs assemble, each death drains 4–8 from every opponent — the deck just doesn't produce enough deaths. Lever test: +drains / +deathmana / +tutors all flat; only +tokens (Bitterblossom + Ophiomancer) moved the table clock (+7pp by T12, never-kill 70→63%). No variant moved the decap median.
3. **The Gravecrawler infinite fires in ~3% of goldfish games** — a 4-piece assembly with only Razaketh as a true tutor. That rarity is the Bracket 3 compliance argument, quantified.
4. **No card-text errors found** — the 2026-05-13 oracle pass holds.
5. Optional polish (pilot's call, NOT a lab mandate): −Mother of Runes −Skrelv +Bitterblossom (owned, undeployed, $0) +Ophiomancer (~€3). The cuts cost real Teysa protection the goldfish can't price. Minimal version: Bitterblossom in, Skrelv out.

No card swaps applied. Scores unchanged (17/20) — the lab measures the clock, not the axes; the deck's identity is Disrupt, not Race, and the matchup framing should treat it as such.

### 2026-06-10 — Bracket-4-in-spirit pivot proposed (pending pod approval)

Follow-up lab (`dr_clock_lab.py --mode b4`, 12k trials) answered "more drain infinites or faster mana?": **combos, decisively — fast mana tested *below* baseline** (its cuts cost bodies; even goldfish-dead protection creatures contribute corpses here). Staged proposal in `proposals/Diminishing_Returns_B4_Pivot_2026-06-10.md`:

- Compact 2-card kills: **Leonin Relic-Warder + in-deck Animate Dead/Necromancy** (Recruiter tutors LRW), **Nim Deathmantle + Grave Titan + in-deck Ashnod's Altar (both owned, $0)**, Exquisite Blood + Vito (~€30, prices checked 2026-06-10).
- Best measured build (full package + GC reallocation: −Smothering Tithe −Farewell +Demonic +Vampiric, still 3/3): table kill 30→41% by T12, never-kill 70→59%, **21% of games end via combo (T8–12)**. Decap stays T9 in all variants — this is a kill-reliability upgrade, not a race upgrade.
- **Bracket consequence:** LRW+aura is an early-capable 2-card infinite → breaks the B3 letter; pod approval required before any swap. Decklist unchanged.

## Don't-Miss Rulings

- **Teysa doubles DEATH triggers only.** She does **NOT** double Gray Merchant (ETB), Mirkwood Bats (token create/sac), or Morbid Opportunist (capped once/turn). She doubles the *number of triggers*, not each effect.
- **Agent of the Iron Throne is a Background enchantment**, not a creature — it grants Teysa a death-drain ability, which Teysa then doubles.
- **Sephiroth front face is a sac outlet + draw engine + single-target drain** (not each opponent). After **4 trigger-resolutions = 2 deaths with Teysa**, he transforms. The back-face emblem drain is **not** doubled but **persists if Sephiroth is later removed** — real durability.
- **K'rrik converts each {B} pip to 2 life** (changes how you pay coloured, not generic) and adds 3 devotion for Gary. Drain triggers pay the life back with interest.
- **Edict creatures (Merciless Executioner, Plaguecrafter) are ETB edicts**, not death triggers — not doubled, but they double as fodder.
- **Endrek Sahr self-sacrifices at 7+ Thrulls** — fine here, since the death payoffs happily eat both the Thrulls and Endrek.

## Piloting Notes (for borrowers)

**Mulligan.** Looking for: **a sac outlet + a drain payoff + lands**, ideally with Teysa or a reanimation spell behind it.

- **Keep:** sac outlet + drain piece; or ramp + Teysa + something to sacrifice; or a fast K'rrik/Dark Ritual start.
- **Toss:** no-creature hands; all-payoff with nothing to sacrifice; no-land hands.
- You **don't** need the full loop in your opener — the deck grinds and draws off its own deaths.

**Threats & timing.**

- **Hard to interact with.** Drains don't target, sac triggers can't be countered, damage comes from many small sources.
- **Punishes removal and board wipes.** Killing your creatures triggers your payoffs — a wrath often does more damage to the table than to you.
- **Grinds through stax.** Small mana increments and recursive creatures shrug off Rhystic Study / Thalia-style taxes.
- **Weak to graveyard hate.** Rest in Peace, Dauthi Voidwalker, and Bojuka Bog shut off Gravecrawler recursion and Living Death at once — the structural ceiling.
- **No counterspells (Orzhov).** A resolving combo can't be stopped on the stack — prevent it proactively with Grand Abolisher on your turn, or punish with edicts. Lean on Teferi's Protection / Flawless Maneuver to survive.
