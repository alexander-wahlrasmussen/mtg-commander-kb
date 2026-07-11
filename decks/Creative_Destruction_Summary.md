# Creative Destruction — Hearthhull, the Worldseed

## Quick Reference

| Field | Value |
|---|---|
| **Commander** | Hearthhull, the Worldseed ({1}{B}{R}{G}, Legendary Artifact — Spacecraft, 6/7) |
| **Colors** | Jund (BRG) |
| **Archetype** | Land-sacrifice ramp / value + combo (Schumpeter: tear your own lands down, rebuild them bigger) |
| **Bracket** | 3 by GC count (3/3). Pod-legal 2-card infinite (blessed under the 2026-06-19 pod combo OK). |
| **Game Changers** | Crop Rotation, Gamble, Natural Order (3 of 3) |
| **Conversion Check** | **15/20 (4/3/4/4)** · judged 2026-07-04 (list-built + promoted 2026-07-11) |
| **Kill Window** | Clock: **T10 decap / T11 table** (lab `ws_clock_lab.py`, 2026-07-11) |
| **Status** | **Built & physically assembled 2026-07-11** — ground-truth `decks/creative-destruction-20260711.txt` (100% owned; precon + free pool + Earthbend the Meta retirement pool) |

-----

## Commander Rules Text

**Hearthhull, the Worldseed** ({1}{B}{R}{G}, Legendary Artifact — Spacecraft, 6/7). Verified via `card_lookup.py` 2026-07-11.

- **Station** (Tap another creature you control: put charge counters equal to its power on Hearthhull; sorcery speed only; it becomes an artifact creature at 8+). *— the ship charges from the side; it is a **noncreature artifact** until stationed to 8, so it dodges creature wipes while charging.*
- **2+ |** {1}, {T}, Sacrifice a land: Draw two cards. You may play an additional land this turn. *— the always-on engine: turn excess lands into cards + extra drops; the "play an additional land" is **cumulative** with Icetill Explorer / Oracle of Mul Daya (a ruling: with Icetill out you get three land plays that turn).*
- **8+ |** Flying, vigilance, haste — **and** "Whenever you sacrifice a land, each opponent loses 2 life." *— the drain is **inside the 8+ box** (printed-card check): until the ship is stationed to 8, it is a draw engine only.*

Hearthhull is an accelerant, not a linchpin — every kill line works without it. It just makes the fair plan (land sacs → drain + cards) inevitable.

-----

## What the Deck Does

A Jund land-sacrifice value engine: it treats its own lands as a renewable resource, sacrificing them for cards, mana, tokens, and drain, then returning them to the battlefield bigger with Splendid Reclamation / Crucible / Ramunap / Life from the Loam. The fair plan is a battlecruiser grind — landfall payoffs (Titania, Scute Swarm, Tannuk, Ob Nixilis, Valakut Exploration) plus a stationed Hearthhull that drains 2 from each opponent per land sacrificed. Behind that fair shell sits an Abolisher-proof, wipe-proof 2-card infinite — Mazirek, Kraul Death Priest + Basking Broodscale — that converts to a table kill through Exsanguinate / Jarad / Mayhem Devil / All Will Be One. The deck is not a racer (median decap T10); it out-grinds the pod and closes from a board- and stack-independent combo when the window opens.

-----

## Kill Lines

**Line 1 — Mazirek + Basking Broodscale infinite (primary, combo):** Mazirek (any player sacrificing *another* permanent puts a +1/+1 counter on each of your creatures) + Basking Broodscale (a +1/+1 counter on it makes a 0/1 Eldrazi Spawn that sacs for {C}). Sacrifice the Spawn → {C} floats + Mazirek counters Broodscale → new Spawn. **Infinite {C}, infinite sac/death triggers, infinite +1/+1 counters.** Convert with Exsanguinate (X = huge, drains the table), Jarad (sac an infinitely-pumped body, each opp loses its power), Mayhem Devil (ping per sac), or All Will Be One (counter → damage). Ignition = any sacrifice while both are out. *Two singleton pieces + only three tutors (Natural Order → Mazirek only, Gamble → either, Victimize → both from yard) — the window is narrow until tutored.*

**Line 2 — Stationed land-sac drain (table):** Hearthhull at 8+ → every land you sacrifice makes each opponent lose 2; the landfall slugs (Tannuk, Sabotender, Ob Nixilis) chip alongside on the refetch wave. Splendid Reclamation / Zuran Orb / Harrow feed the sac→rebuy loop.

**Line 3 — Springheart landfall (combo):** Springheart Nantuko enchanting a Lotus Cobra / Tireless Provisioner, with Ashaya or Badgermole making lands into creatures → infinite landfall → infinite tokens / mana / drain triggers.

**Line 4 — Battlecruiser combat (fallback):** Titania / Scute Swarm / land-token board + Purphoros / All Will Be One counter-pings → focus one opponent; the deck's decap floor.

**Line 5 — Gitrog + Dakmor Salvage (enabler):** bottomless discard-loop self-mill + draw that fills the yard for Splendid Reclamation (not a standalone win — no Thassa's Oracle).

-----

## Kill Window

- **Goldfish:** Clock **decap T10 / table T11** (lab `scripts/ws_clock_lab.py --mode creative`, 40k, 2026-07-11). Kill mixture: land-sac drain 32% / combat 27% / Mazirek combo (+ converters / pumped swing) ~23% / landfall slug 8% / All Will Be One + Purphoros ~10%.
- **Through interaction:** slower *(unverified — goldfish ceiling; no opposing interaction / wipes modelled)*. The deck **cannot race** the measured T6–7 pod combo — but its removal works *before* the Abolisher turn and its combo kill works *through* one.

-----

## Conversion Check — 15/20 (audited 2026-07-04)

Scored from the list per `reference/REF_The_Conversion_Check.md`. Four judged axes; the clock is measured.

| Axis | Score | Rationale |
|---|---|---|
| **Core Loop** | **4/5** | Land-sac / recursion engine, 18+ serving cards, commander-boosted but commander-independent. |
| **Kill Reliability** | **3/5** | Two genuinely independent lines (combat overrun; the Mazirek loop with four converter exits), but the fast line is two specific singletons — the window is narrow until tutored (only three tutors). |
| **Durability** | **4/5** | Life from the Loam / Crucible / Ramunap / Splendid Reclamation / Victimize rebuild from a wipe in 2–3 turns; the commander is an accelerant, not a dependency. |
| **Interaction** | **4/5** | 11 instant-heavy, mechanism-diverse pieces (targeted / sweeper / GY-hate / anti-counter). |

**Reading:** upper-middle of the roster (the Diminishing Returns / Curse-of-the-Scarab band), **not** the racer half. Limiting axis is Kill Reliability — combo assembly is the binding constraint, not fat.

-----

## Durability

Board wipes feed the plan rather than break it: sacrificed and killed lands recur via Life from the Loam (dredge), Crucible of Worlds / Ramunap Excavator (play from yard), and Splendid Reclamation (return **all** yard lands tapped, at once). Victimize and Jarad rebuy the combo creatures from the graveyard; the commander re-casts cheaply and dodges creature wipes while charging (it's a noncreature artifact under 8 charge). Two-to-three turns to re-threaten after a T7 wipe.

-----

## Interaction Package

**11 pieces total.** Removal: 8 — Abrade, Infernal Grasp, Bitter Triumph, Putrefy, Beast Within, Tear Asunder, Murderous Rider, Windgrace's Judgment. Sweepers: 2 — Blasphemous Act, The Meathook Massacre. Protection / redirect / anti-counter: Deflecting Swat, Veil of Summer. Counters: 0 (Jund — the answers are removal, not permission). Instant speed: ~55%.

-----

## Known Weaknesses

- **Slow decap (median T10).** It cannot win a race — against the T6–7 pod it must survive to grind, leaning heavily on its removal + the Abolisher-proof combo (pure-race P(decap) is only ~8%; measured P(win) 23% rides its disruption).
- **Combo is two singletons + only three tutors.** No redundancy in the Broodscale slot; Natural Order can't fetch the devoid half. A well-timed graveyard-hate piece also slows the Splendid Reclamation recursion the fair plan leans on.
- **Station gate on the drain.** Until Hearthhull reaches 8 charge (median T8–9), the commander is a draw engine only — the drain is not a fast clock, it's an accelerant.

-----

## Don't-Miss Rulings

Card text verified via `card_lookup.py` 2026-07-11 (read the card + rulings; no writing from memory).

- **Hearthhull, the Worldseed** — the "each opponent loses 2 per land sac" drain sits **inside the 8+ box**; it does nothing until the ship is stationed to 8 (sorcery-speed only). Station taps *another* creature for its power in charge. The 2+ "play an additional land" is **cumulative** — with Icetill Explorer / Oracle of Mul Daya out you get three land plays that turn.
- **Mazirek, Kraul Death Priest** — triggers on a player sacrificing **another** permanent, so Mazirek sacrificing *itself* doesn't fire it, but he counts **every other** sac by **any** player (yours or an opponent's). This is what powers the Broodscale loop (each Spawn sac is "another permanent").
- **Basking Broodscale** — **devoid** (colorless). Natural Order fetches a *green* creature, so it can grab Mazirek but **cannot** fetch Broodscale; Gamble finds either half, Victimize returns both from the yard. The token trigger is "one or more +1/+1 counters," so one Mazirek trigger = one Spawn per counter event.
- **Splendid Reclamation** — returns **all** land cards from your graveyard to the battlefield **tapped**, simultaneously; a big pile of sacrificed lands returns as one landfall wave (each is a Titania/Tannuk/Valakut trigger).
- **Basking Broodscale / Mazirek is Abolisher-proof** — the loop's payoffs (Exsanguinate cast aside, Jarad/Mayhem Devil are activated/triggered *abilities*, All Will Be One is a static) fire through Grand Abolisher and don't use the stack in a way a single counter answers.

-----

## Decklist (100 cards)

*The dated `.txt` (`decks/creative-destruction-20260711.txt`) is ground truth; these functional buckets are labels only.*

### Commander (1)
- Hearthhull, the Worldseed

### Combo pieces + converters (9)
- Mazirek, Kraul Death Priest · Basking Broodscale · Springheart Nantuko
- Exsanguinate · Jarad, Golgari Lich Lord · Mayhem Devil · All Will Be One · Purphoros, God of the Forge · Ashaya, Soul of the Wild

### Tutors (3)
- Crop Rotation *(GC)* · Gamble *(GC)* · Natural Order *(GC)*

### Landfall / land-sac payoffs (8)
- Titania, Protector of Argoth · Scute Swarm · Tannuk, Memorial Ensign · Sabotender · Ob Nixilis, the Fallen · Valakut Exploration · Szarel, Genesis Shepherd · Korvold, Fae-Cursed King

### Ramp / mana (11)
- Sol Ring · Arcane Signet · Lotus Cobra · Tireless Provisioner · Orcish Lumberjack · Farseek · Nature's Lore · Cultivate · Skyshroud Claim · Harrow · Roiling Regrowth · Entish Restoration

### Land engine / recursion + sac outlets (11)
- Crucible of Worlds · Ramunap Excavator · Life from the Loam · Splendid Reclamation · Aftermath Analyst · Icetill Explorer · Oracle of Mul Daya · The Gitrog Monster · Victimize · Zuran Orb · Sylvan Safekeeper · Woe Strider · Evolution Sage · Badgermole Cub

### Card advantage (2)
- Night's Whisper · Pest Infestation

### Interaction (12)
- Abrade · Infernal Grasp · Bitter Triumph · Putrefy · Beast Within · Tear Asunder · Murderous Rider · Windgrace's Judgment · Blasphemous Act · The Meathook Massacre · Deflecting Swat · Veil of Summer

### Lands (38)
- 2 Forest · 2 Swamp · Mountain · Command Tower · Command Beacon · Yavimaya, Cradle of Growth · Boseiju, Who Endures · Urza's Saga · Lotus Field · Ba Sing Se · Eumidian Hatchery · Takenuma, Abandoned Mire · Dakmor Salvage · Bojuka Bog · Myriad Landscape · Maestros Theater · Riveteers Overlook · Cabaretti Courtyard
- **Duals/shocks/fetches:** Badlands · Taiga · Blood Crypt · Stomping Ground · Overgrown Tomb · Karplusan Forest · Llanowar Wastes · Sulfurous Springs · Twilight Mire · Woodland Cemetery · Arid Mesa · Bloodstained Mire · Prismatic Vista · Scalding Tarn · Verdant Catacombs · Windswept Heath · Wooded Foothills · Fabled Passage

-----

## Piloting Notes (for borrowers)

- **Mulligan for mana + a land engine**, not for the combo (MANA keep). A hand that ramps and sacrifices lands for value plays itself; the combo assembles off the tutors + card advantage. Keep 2–5 lands with ramp or a recursion piece; the combo is upside, not the plan.
- **Don't over-commit into a wipe** — the recursion means you rebuild, so hold Splendid Reclamation until you have lands in the yard worth returning.
- **Kill Grand Abolisher / graveyard hate on sight** with the removal suite; the combo works through Abolisher but the fair recursion plan does not love graveyard hate.
- **Station Hearthhull only when the drain matters** — pre-8 it's a draw engine; don't tap your board to charge it if that costs you the turn's tempo.

-----

## Changelog

- **2026-07-11:** Built and promoted to the active roster from `world-shapers-tuned-20260709.txt` (precon + free pool + Earthbend the Meta retirement pool; zero further buys). Named *Creative Destruction* 2026-07-05. Registered in `deck_registry` (lab `ws_clock_lab.py --mode creative`). Clock harvested decap T10 / table T11.
