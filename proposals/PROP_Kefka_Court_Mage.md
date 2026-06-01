# Proposal: Kefka, Court Mage

Status: **not built.** Saved for future consideration.
Drafted: 2026-05-31.

Built as a pod answer to the recurring archenemy who wins T6–7 with Ur-Dragon + Hidetsugu / Kairi / Kenrith / Kinnan behind **Grand Abolisher** (see `project_pod_combo_opponent.md`). The whole thesis is that a forced-draw burn kill resolves on *your* turn and through *static* triggers, which is the one damage axis Abolisher cannot switch off.

Card text verified against local Scryfall data via `python scripts/card_lookup.py` per `CLAUDE.md` hard rules (Final Fantasy is Universes Beyond → strict verification). Every card named in the kill math below was Scryfall-checked at draft time. Re-verify at build time.

---

## Commander

**Kefka, Court Mage // Kefka, Ruler of Ruin** — `{2}{U}{B}{R}`, Legendary Creature — Human Wizard, 4/5. **Color identity: BRU (Grixis).**

> **Front (Court Mage):** Whenever Kefka enters or attacks, each player discards a card. Then you draw a card for each card type among cards discarded this way.
> `{8}`: Each opponent sacrifices a permanent of their choice. Transform Kefka. Activate only as a sorcery.
>
> **Back (Ruler of Ruin):** Flying, 5/7. Whenever an opponent loses life during your turn, you draw that many cards.

**Owned: YES — 1 copy, free.** Listed in `collection/moxfield_haves_2026-05-14-0631Z.csv` under its full DFC name `"Kefka, Court Mage // Kefka, Ruler of Ruin"` (FF set, acquired 2026-04-14); not deployed in any `decks/*.txt`. (Initial draft wrongly reported it unowned — a grep-pattern error that anchored a closing quote after "Mage"; corrected 2026-05-31.)

**Engine reading (the design steer this is built around).** The front side is the engine; the back side is a late-game overrun we mostly ignore. Two clauses, two jobs:

- **The draw is asymmetric** — *only you* draw. This is the entire reason Kefka beats Nekusar for this pod: Nekusar forces *every* player to draw extra, which fills the combo player's hand and accelerates their kill. Kefka refuels you alone.
- **The draw scales on card-*type* diversity, not count** — "for each card type **among cards discarded this way**" counts distinct types across the *whole* discarded pile (creature / land / instant / sorcery / artifact / enchantment / planeswalker), not per player. Realistic yield 2–4, ceiling ~7.
- **The discard is one card per trigger** ("each player discards *a* card") — disruption-lite, a steady chip, not a hand-empty. The *wheels* empty hands; Kefka chips and digs.
- **The attack trigger fires on *declaration*** — Kefka needs to *survive to attack*, not connect. Support = protection, not evasion.

---

## Why this is the right pod answer (and the others aren't)

Every other deck in the roster fights the Abolisher problem with counters that go dead on the lock turn. Kefka sidesteps it structurally:

1. **The kill is a wheel + static draw-punishers.** A wheel makes opponents draw seven; static punishers (Sheoldred, Underworld Dreams, Fate Unraveler) convert each of those draws to damage. Statics keep firing through a Grand Abolisher turn — they're not "casting a spell" or "activating an ability," so the lock can't touch them.
2. **It resolves on *your* turn.** Grand Abolisher only locks *opponents* on *its controller's* turn. When you cast your wheel on your own turn, you are unaffected regardless of who has an Abolisher out.
3. **It races the clock from the other direction.** Instead of trying to out-grind a T6 combo, you assemble a one-cast table-wide burn that closes the same turn it comes online.

---

## Engine architecture: division of labor

**Front-side Kefka = value engine + light disruption.** Assembles and protects the kill; not the kill itself, and explicitly *not* a combo piece you must keep alive (see constraint #2 below).

**Wheel + punisher shell = the Abolisher-proof finish.** Functions with Kefka dead in the command zone.

Two punisher axes, fed simultaneously by every wheel:

| Axis | Triggers on | Cards | Note |
|---|---|---|---|
| **Opponent-draw** | each opponent's 7 wheel-draws | Sheoldred (−2 life/draw), Underworld Dreams (1 dmg/draw), Fate Unraveler (1 dmg/draw), [Orcish Bowmasters] | dormant under Notion Thief (opponents draw nothing) |
| **Your-draw** | *your* 7 wheel-draws (guaranteed) | Psychosis Crawler (each opp −1/your draw), Niv-Mizzet Parun (1 dmg any target/your draw) | the *reliable* half — you always draw your own 7 |
| **Discard** | each player's hand dumped to the wheel | Megrim (2 dmg/discard), Liliana's Caress (−2 life/discard) | early value with Kefka; gravy on the wheel |

A single wheel triggers all three axes at once.

---

## Kill lines (verified math)

### Line 1 — Notion Thief + Psychosis Crawler + any wheel (marquee, near-deterministic)

- **Notion Thief** (`{2}{U}{B}`, GC, verified): "If an opponent would draw a card except the first one they draw in each of their draw steps, instead that player skips that draw and **you** draw a card."
- **Psychosis Crawler** (`{5}` colorless, verified): "Whenever **you** draw a card, each opponent loses 1 life." (Ruling: multi-draw effects trigger it that many times.)

With both out, cast any wheel: each opponent's seven draws are redirected to you. You draw your own 7 plus ~21 from three opponents = **~28 draws → Psychosis Crawler fires ~28 times → each opponent loses ~28 life.** Table dead from one wheel, and opponents draw *nothing* — the refuel problem is erased. Niv-Mizzet, Parun is the redundant version (you draw ~28 → 28 damage you aim anywhere).

### Line 2 — Multi-punisher wheel (the default burn)

With **2+ opponent-draw punishers down**, cast a wheel (each opponent draws 7):

- 1 punisher = 7 each → **don't do this**, it's the refuel trap (you hand them 7 fresh cards to deal 7).
- 2 punishers (Underworld Dreams + Fate Unraveler) = 14 each.
- 3 punishers (+ Sheoldred's 2-life/draw) = 7 + 7 damage + 14 life ≈ **28 each per wheel.** From 40, one wheel → ~12; a second wheel, Kefka's drip, or a Peer finishes.

Add Psychosis Crawler (your-draw axis, guaranteed 7) on top of any of the above and the numbers climb regardless of opponent responses.

### Line 3 — Peer into the Abyss (hand-size-independent single-target nuke)

**Peer into the Abyss** (`{4}{B}{B}{B}`, verified): target player draws half their library (round up) and loses half their life. Pointed at one opponent with a single draw-punisher out, they draw ~15+ cards (→ 15+ damage) *and* lose half their life. Kills one player outright, and refuels only that player instead of the table. The answer to a stalled board where wheels are too symmetric.

---

## The two honest constraints (discussed and agreed with the pilot)

**1. Lethal-or-bust.** A non-lethal wheel refuels the combo player. The deck must have **2+ draw-punishers online before it ever spins** (3 to actually kill a healthy table), or a Notion Thief out to deny the refuel. This is why the wheel count is high (redundancy) and why the deck wants tutors and acceleration — it has to *reliably* assemble two pieces before the opponent's T6.

**2. Kefka is a removal magnet, and that's fine.** A 4/5 value engine in three colors gets pointed at. The build survives this because **the win doesn't depend on Kefka surviving**:
- The ETB is guaranteed value *per cast* — even a Kefka that dies instantly gave you one table-wide discard + a draw.
- Commander recastability means you can never be permanently denied it; the cost is the +2 tax grind (4 → 6 → 8), which is the real price, not a dead engine.
- Kefka is a lightning rod — every removal spell spent on him is one not spent on Sheoldred / Underworld Dreams, the pieces that actually kill.

Plan: cast Kefka, take the ETB, *don't over-invest* protecting him, let him bait removal, recast once if cheap — win off the shell. The deck's resilience is punisher/wheel redundancy, not Kefka's longevity.

---

## Composition (100 cards, 3/3 Game Changers)

| Category | Count | Key cards (verified) |
|---|---|---|
| Commander | 1 | Kefka, Court Mage |
| Lands | 36 | Grixis duals/shocks/fastlands, Command Tower, **Otawara, Soaring City** (channel bounce — Abolisher-proof), **Reliquary Tower** (no max hand for big wheel draws), a few basics |
| Mana rocks / ramp / cost-reducers | 11 | Sol Ring, Arcane Signet, Dimir/Rakdos/Izzet Signets, Talismans (Dominance/Indulgence/Creativity), Fellwar Stone, Dark Ritual, **Jet Medallion + Ruby Medallion**, **Mana Vault** (GC) |
| Wheels + Peer | 8 | Wheel of Fortune, Windfall, Echo of Eons, Reforge the Soul, Magus of the Wheel, Time Spiral, Memory Jar, Peer into the Abyss |
| Punishers (draw + your-draw + discard) | 7 | Sheoldred, Underworld Dreams, Fate Unraveler, Psychosis Crawler, Niv-Mizzet Parun, Megrim, Liliana's Caress |
| Notion Thief (GC) | 1 | Notion Thief |
| Tutors | 3 | **Demonic Tutor** (GC) + 2 non-GC (Diabolic Tutor / Mastermind's Acquisition) |
| Kefka protection | 2 | Lightning Greaves, Swiftfoot Boots |
| Interaction — removal | 7 | Bedevil, Terminate, Go for the Throat, Bloodchief's Thirst, + 3 cheap instant-speed (kill Abolisher / combo pieces on sight) |
| Interaction — counters | 6 | Counterspell, + 5 (for non-Abolisher windows — counters blank on the lock turn) |
| Card filtering / graveyard fuel | 4 | Faithless Looting, Frantic Search, + 2 |
| Flex / role-players | 4 | extra wheel/punisher redundancy, a second sweeper, etc. |

**GC tally = 3/3:** Notion Thief, Demonic Tutor, Mana Vault. Verified against `REF_Game_Changers_List.md`. Everything else in the list is confirmed non-GC.

---

## Game Changer plan (the 3-cap forces one real choice)

The deck is *swimming* in strong Grixis GCs, so the cap is the binding constraint. The two locks:

- **Notion Thief** — unique effect, combos with Psychosis Crawler/Niv for a one-wheel kill, and single-handedly solves the refuel problem. Non-negotiable.
- **Demonic Tutor** — a lethal-or-bust deck needs to *find* its second punisher / a wheel / Notion Thief. Consistency is the whole game.

The **third slot** is a genuine toss-up; pick to taste:

| 3rd GC | Buys you | Cost |
|---|---|---|
| **Mana Vault** *(default)* | raw speed — deploy 2 punishers + a wheel ahead of their T6, the deck's measured weakness | no extra interaction/resilience |
| **Orcish Bowmasters** | a flash punisher + body that *also* pings their own draw-heavy combo turns; proactive interaction | slower; an opponent-draw punisher (dormant under Notion Thief) |
| **The One Ring** | a protective turn (protection from everything) + a draw engine that feeds Psychosis Crawler / Niv | no acceleration; burden-counter life drain |

Default recommendation: **Mana Vault**, because the deck's documented loss condition is *losing the race to T6* — speed is the axis that's actually short. Swap to Bowmasters if the pilot wants more interaction; to The One Ring if durability is the bigger problem in practice.

**Anti-synergy flagged:** Narset, Parter of Veils and (in burn mode) Orcish Bowmasters/Notion Thief all suppress opponent draws — great for *denial*, but they turn off the opponent-draw punishers. Notion Thief earns its slot anyway because it pairs with the *your-draw* axis (Psychosis/Niv). Don't stack all the draw-deniers and expect the burn axis to still fire.

---

## Owned shell vs. buys

Verified against `collection/moxfield_haves_2026-05-14-0631Z.csv` and `decks/*.txt`. ⚠️ = owned but currently deployed in another active deck (owning ≠ free).

### Owned and free
| Card | Owned | Notes |
|---|---|---|
| Notion Thief | 1 | undeployed — **free** |
| Demonic Tutor | 4 | multiple free copies |
| Mana Vault | 3 | 1 in Eldrazi Stampede → **2 free** |
| The One Ring | 4 | 2 in Crystal Sickness + Replication Crisis → **2 free** (if chosen) |
| Windfall | 1 | undeployed — **free** (grep matched "Unexpected Windfall" in Genome, a *different* card) |
| Magus of the Wheel | 1 | undeployed — **free** |
| Kefka, Court Mage *(commander)* | 1 | undeployed — **free** (listed under full DFC name) |
| Lightning Greaves / Swiftfoot Boots | 9 / 6 | free |
| Counterspell, Dark Ritual, Faithless Looting, Frantic Search, Go for the Throat | many | free |
| Sol Ring, Arcane Signet, Command Tower, Blood Crypt, Jet/Ruby Medallion | surplus | Grixis manabase + rocks well-stocked |

### Owned but contested (buy a duplicate or pull from donor)
| Card | Owned | Deployed in | Note |
|---|---|---|---|
| Sheoldred, the Apocalypse | 2 | 1 in The Dark Lord's Army → 1 "free" | **but the 2026-05-31 Calamity Tax swap also claims this spare** — see cross-proposal note |
| Underworld Dreams | 1 | The Dark Lord's Army | buy 2nd or pull |
| Psychosis Crawler | 1 | Peace Offering | buy 2nd or pull |
| Peer into the Abyss | 1 | The Genome Project | buy 2nd or pull |
| Orcish Bowmasters | 1 | The Dark Lord's Army | only if chosen as 3rd GC |

### Unowned — required buys
Wheel of Fortune, Echo of Eons, Reforge the Soul, Time Spiral, Memory Jar, Fate Unraveler, Megrim, Liliana's Caress, Niv-Mizzet Parun, Bedevil, Terminate, Bloodchief's Thirst. *(Commander is owned — see above.)*

---

## Cross-deck contention

- **The Dark Lord's Army (Sauron) is the big donor.** It already runs **Orcish Bowmasters, Sheoldred, and Underworld Dreams** — three of Kefka's punisher staples, because it's a black drain/aristocrats deck. Building Kefka raids Sauron's core unless you buy duplicates. This is the single largest deckbuilding decision in the proposal: are you willing to gut Sauron, or buy ~3 duplicates (~$15–25 total)?
- **Cross-proposal conflict — Sheoldred.** The same-session Calamity Tax swap (`The_Calamity_Tax_Swaps_2026-05-31.md`) also allocates the single free Sheoldred. **Only one of the two decks can have it.** If both get built, buy a 3rd Sheoldred. Flagged so the two proposals don't silently double-spend the same card.
- Peace Offering (Psychosis Crawler) and Genome Project (Peer into the Abyss) are lower-impact donors; neither was in the 2026-05-30 pod rotation.

---

## Projected Conversion Check: ~17/20 ceiling (5 / 4–5 / 3 / 4)

| Axis | Projected | Reasoning |
|---|---|---|
| Core Loop | 5/5 | Kefka value engine + 8 wheel-effects + redundant punishers; tutors find the missing piece |
| Kill Reliability | 4–5/5 | multiple Abolisher-proof axes + the Notion Thief/Psychosis one-wheel kill + Demonic Tutor; bounded by lethal-or-bust (needs 2+ pieces) |
| **Durability** | **3/5** | **the limiting axis** — Grixis has no green/white; commander is a magnet; punishers are enchantments/creatures vulnerable to wraths; relies on racing |
| Interaction | 4/5 | strong cheap removal + counters, but counters still blank on the Abolisher turn → same "kill Abolisher on sight" pilot demand |

A pure-power version ceilings higher, but Durability caps a Grixis racing deck at ~17 realistically. That still clears the pod bar — the point isn't to grind, it's to assemble the burn before they combo.

---

## Shopping list (prices unverified per `verify-prices` — confirm on Cardmarket)

| Card | Status | Est. (unverified) |
|---|---|---|
| Kefka, Court Mage *(commander)* | **owned — free** | $0 |
| Wheel of Fortune | buy | ~$30–50 |
| Echo of Eons | buy | ~$10–20 |
| Time Spiral | buy | ~$8–15 |
| Memory Jar | buy | ~$5–10 |
| Niv-Mizzet, Parun | buy (flex) | ~$5–10 |
| Reforge the Soul / Fate Unraveler / Megrim / Liliana's Caress | buy | ~$1–5 each |
| Bedevil / Terminate / Bloodchief's Thirst | buy | ~$1–3 each |
| Sheoldred / Underworld Dreams / Psychosis Crawler / Peer (duplicates to avoid raids) | buy or pull | ~$15–25 total |
| **Estimated buy-route total** | | **~$85–140** |

Most of the engine — the commander, the GCs, protection, counters, filtering, rocks, and manabase — is already owned in surplus. The spend is concentrated in the premium wheels (Wheel of Fortune, Echo of Eons, Time Spiral, Memory Jar) and avoiding cross-deck raids.

---

## Open questions for the build session

- **Donor decision on The Dark Lord's Army.** Raid Sauron for Bowmasters/Sheoldred/Underworld Dreams, or buy duplicates? This gates the punisher core.
- **Resolve the Sheoldred conflict with the Calamity Tax swap** before either is sleeved.
- **Lock the 3rd GC** (Mana Vault vs. Bowmasters vs. The One Ring) — default Mana Vault for speed; confirm against the pilot's read of *why* games are being lost (clock vs. resilience).
- **Tune the wheel count.** 8 wheel-effects is aggressive; if early-game consistency suffers, trim the weakest (Wheel of Misfortune-tier) for more rocks/interaction.
- **Niv-Mizzet, Parun** — `{U}{U}{U}{R}{R}{R}` is hard on a 3-color base. Keep as flex; cut first if the manabase strains.
- **Re-verify all GC slots at build time** — the list updated twice in the last year (Oct 2025, Feb 2026).
- **Re-verify Kefka's text and color identity at build time** (UB card; strict rule).
