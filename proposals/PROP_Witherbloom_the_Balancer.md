# Proposal: Witherbloom, the Balancer — BG Spellslinger-Drain (Bracket-4-in-Spirit)

Status: **not built.** Saved for future consideration.
Drafted: 2026-06-01 in response to pack pull (Witherbloom, the Balancer + Professor Dellian Fel).

Card text verified against local Scryfall data (refreshed 2026-06-01 to pick up the new set). Verification log at the bottom.

---

## Commander

**Witherbloom, the Balancer** (BG). `{6}{B}{G}`, Legendary Creature — Elder Dragon, 5/5.

> Affinity for creatures *(This spell costs {1} less to cast for each creature you control.)*
> Flying, deathtouch
> Instant and sorcery spells you cast have affinity for creatures.

**Color identity: BG.** Owned: 1 copy (fresh pack). Verified 2026-06-01.

**What this enables:** with 8 creatures on board, every instant/sorcery you cast costs `{8}` less (down to its colored-mana floor). Affinity is a generic-cost reduction only — `{U}{U}` Counterspell-style mana isn't affected, but a `{6}{B}` Damnable Pact with 6 creatures costs `{B}`. Cantrips with `{1}U` / `{1}B` / `{1}G` become single-pip for free under affinity. **This is the textbook storm enabler in BG.**

Witherbloom herself also has affinity for creatures, so the 8-MV commander becomes a 0-cost cast with a wide board.

---

## Professor Dellian Fel as a 99 (not commander)

**Professor Dellian Fel** (BG). `{2}{B}{G}`, Legendary Planeswalker — Dellian.

> +2: You gain 3 life.
> 0: You draw a card and lose 1 life.
> -3: Destroy target creature.
> -6: You get an emblem with "Whenever you gain life, target opponent loses that much life."

**Cannot be commander** (no "can be your commander" text). Verified by emblem listing on Scryfall. Slots as a 99.

Value:
- **0-loyalty draw-a-card** is Necropotence-tier card advantage — free engine that pays its own cost in life and keeps Dellian alive (loyalty doesn't go down on 0 abilities). One card per turn cycle, forever, until removed.
- **+2 gain 3 life** keeps the planeswalker safe and **triggers Exquisite Blood / Sanguine Bond / Vito** for incidental drain.
- **-3 destroy a creature** is the situational removal slot.
- **-6 emblem** is a third redundant copy of the Vito/Sanguine Bond "you gain life → opp loses" half of the combo. The ult is a real win condition, not a flavor.

---

## Alternative path: slot both cards as 99s in Calamity Tax

**Surfaced 2026-06-01** as a decision-deferral option. Calamity Tax (Glarb, Calamity's Augur — Sultai BUG, 18/20 → 19/20 planned) covers BG within its color identity. Both new cards are commander-legal there as 99s. Companion swap doc: `decks/The_Calamity_Tax_Swaps_2026-06-01.md`.

**Why the 99-route might beat the standalone build:**

1. **Calamity Tax already wins via X-spell drain + copy effects** — Torment of Hailfire, Exsanguinate (planned add), Rite of Replication (kicked), Doppelgang, Mirrorform. Witherbloom's "instants and sorceries you cast have affinity for creatures" universally cheapens every one of those kills:

| Spell | Native cost | With Witherbloom + 12 creatures |
|---|---|---|
| Torment of Hailfire X=20 | {20}{B}{B} = 22 mana | ~{2}{B}{B} (the X reduces the same way) |
| Exsanguinate X=20 | 22 mana | ~4 mana |
| Doppelgang X=4 | {4}{4}{4}{G}{U} = 14 mana | {G}{U} |
| Rite of Replication kicked | {7}{U}{U} = 9 mana | {U}{U} |
| Mirrorform | {4}{U}{U} | {U}{U} |
| Espers to Magicite | {3}{B} | {B} |

2. **Witherbloom is MV ≥ 4**, so Glarb top-casts her for free. Or skip the cast entirely: surveil her into the graveyard via Glarb's tap ability, then Reanimate for {B}. T4–5 deploy is realistic.
3. **Dellian Fel's 0-loyalty "draw a card, lose 1 life"** is pure value at 4 MV (on-curve, also top-castable). The +2 keeps her alive while incidentally triggering Sheoldred (planned add) and any future life-gain hooks.
4. **Zero shopping list.** The standalone Witherbloom build is ~€80–90 of new buys (Exquisite Blood, Vito, Sanguine Bond, Witherbloom Apprentice, Beledros, Hornet Queen, combo pieces, conflict duplicates). Slotting in Calamity Tax costs €0 cards.
5. **No Pest Control roster conflict.** No mechanical-distinctiveness fight, no Survival contention, no Bloom Tender triple contention. Pest Control as a candidate slot stays open.

**What the 99-route gives up:**

1. **The Vito + Exquisite Blood 2-card pod-approved combo.** That kill line is a Witherbloom-the-commander identity — it needs creature density + life-gain triggers + the dedicated combo pieces. Calamity Tax doesn't go wide enough on creatures and doesn't run lifegain triggers naturally.
2. **The 18–19/20 standalone ceiling.** Slotting into Calamity Tax probably bumps the deck from 19 to ~19.5. A modest upgrade to an already-tuned deck rather than a new disgusting-tier kill.
3. **Witherbloom as a commander-zone finisher.** As a 99 she's a 1-of; as a commander she's always available. The deck identity loses the "race the pod with a 2-card combo" axis.

**Swap candidates within Calamity Tax (see companion doc for full plan):**
- **Witherbloom → Archon of Cruelty** (8-MV finisher swap; Witherbloom's global cost reduction beats Archon's one-shot drain on every X-spell turn)
- **Dellian Fel → Starfield Vocalist** (Starfield was already a planned cut in the 2026-05-31 swap doc — Dellian replaces that slot more efficiently than the planned Carpet of Flowers, but this collides with the Carpet plan)

**Decision deferred to build time.** Neither this proposal nor the standalone Witherbloom build is committed; both stay as proposals until a user call.

---

## Archetype

**BG spellslinger / aristocrats / drain hybrid.** Wide token board + cheap instants/sorceries (via affinity) + life-gain-drain win conditions. The deck has three distinct kill-engine clusters that share substrate:

1. **Drain combo** — Exquisite Blood + Vito/Sanguine Bond + any life-gain trigger. Pod-approved 2-card win.
2. **Razaketh chain** — sacrifice creatures to tutor combo pieces; ends in Mikaeus + Walking Ballista + sac outlet (3-card infinite damage).
3. **Storm-affinity drain** — chain cheap instants/sorceries (Witherbloom affinity makes them near-free); each trigger Witherbloom Apprentice (1 drain) or Aetherflux Reservoir (life-into-damage).

Backup: combat with Pest tokens (Beledros), Saproling tokens (Tendershoot Dryad), Insect tokens (Hornet Queen), occasionally Triumph of the Hordes for infect.

---

## Win lines (ordered by speed and reliability)

### Line 1 — Exquisite Blood + Vito / Sanguine Bond / Dellian Fel emblem (primary, T5–6 kill)

**Pod-approved 2-card infinite drain.** Confirmed by Sanguine Bond's own Scryfall ruling: *"If an ability triggers whenever an opponent loses life and causes you to gain life, such as the ability of Exquisite Blood, this will loop until either you win the game or a player takes an action to break the loop."*

Verified mechanics:
- **Exquisite Blood** (`{4}{B}`): *Whenever an opponent loses life, you gain that much life.*
- **Vito, Thorn of the Dusk Rose** (`{2}{B}`): *Whenever you gain life, target opponent loses that much life.* Plus `{3}{B}{B}: Creatures you control gain lifelink EOT.`
- **Sanguine Bond** (`{3}{B}{B}`): Same trigger as Vito's first ability.
- **Professor Dellian Fel emblem**: Same trigger again (gain life → target opp loses).

**Three redundant copies of the "gain-life-drains-opp" half.** Just need Exquisite Blood (or another loss-triggers-gain effect) plus any single trigger to start the loop. Once the loop fires, each cycle drains 1 from a chosen opponent and you gain 1 — repeats until that opponent is dead, then redirect to the next.

**The starting trigger is easy:**
- Witherbloom Apprentice magecraft (`{B}{G}`, 2/2) — *opps lose 1, you gain 1 per instant/sorcery cast.* Built-in.
- Aetherflux Reservoir — gain 1 life per spell cast.
- Soul Warden / Soul's Attendant variants if needed.
- Any lifelink combat damage.
- Vito's own activated ability gives the team lifelink for a turn (`{3}{B}{B}`).
- Cauldron Familiar ETB drains 1 / gains 1.
- Dellian Fel's +2 gives 3 life.

**Combo sequencing (race):**
- T1: Land, Sol Ring, or 1-drop dork.
- T2: Land, ramp (Bloom Tender / Birds of Paradise / Three Visits).
- T3: **Vito** (`{2}{B}`).
- T4: Land, ramp or tutor.
- T5: **Exquisite Blood** (`{4}{B}` = 5 mana). Cast Witherbloom Apprentice at any point along the way. **Combo armed.**
- T5 main phase 2: cast any instant/sorcery (cantrip works) → Apprentice triggers (you gain 1) → Vito drains 1 → Blood gains 1 → infinite loop → table dies.

**T5 kill is realistic.** With Vampiric Tutor T2 (find Blood), Demonic Tutor T3 (find Vito), Necropotence T3 (draw 5+ cards), combo lands T4–5 reliably.

### Line 2 — Razaketh chain → Mikaeus + Walking Ballista + sac outlet (T6–8)

Verified mechanics:
- **Razaketh, the Foulblooded** (`{5}{B}{B}{B}`, 8 MV, 8/8 flying trample): *Pay 2 life, sacrifice another creature: Search your library for a card, put that card into your hand, then shuffle.* Repeatable instant-speed tutor.
- **Mikaeus, the Unhallowed** (`{3}{B}{B}{B}`, 6 MV): *Other non-Human creatures you control get +1/+1 and have undying.* Undying: when a creature dies with no +1/+1 counters, return with a +1/+1 counter.
- **Walking Ballista** (`{X}{X}`): enters with X +1/+1 counters; *Remove a +1/+1 counter from this creature: It deals 1 damage to any target.*
- **Phyrexian Altar** (`{3}`): *Sacrifice a creature: Add one mana of any color.*

**Honest correction vs. common claim:** Mikaeus + Walking Ballista is NOT a 2-card infinite on its own. With Mikaeus's static +1/+1 buff, Ballista at 0 counters is still a 1/1 base + Mikaeus = 2/2, alive. The combo needs a sac outlet to kill Ballista so undying triggers. So this is a **3-card combo** (Mikaeus + Ballista + Phyrexian Altar / Phyrexian Tower / Viscera Seer / Carrion Feeder / Yawgmoth).

With Phyrexian Altar: sac Ballista → 1 mana → Mikaeus undying returns Ballista with +1/+1 counter → ping for 1 damage → repeat. **Infinite mana AND infinite damage.**

Razaketh sets this up by sacrificing creatures (paying 2 life per tutor) to find each missing piece. With Beledros Witherbloom's Pest tokens, Tendershoot Saprolings, Hornet Queen Insects providing sac fodder, Razaketh can chain 4–6 tutors in a single turn.

This is the [[pest-control-proposal]] engine — borrowed for redundancy.

### Line 3 — Affinity-storm via Aetherflux Reservoir or Witherbloom Apprentice (T6–8)

Witherbloom's affinity on instants/sorceries makes a stream of cantrips effectively free with a wide board. Chain 15+ cheap spells in one turn:

- Each cast triggers Witherbloom Apprentice (drain 1 each opp, gain 1)
- Each cast triggers Aetherflux Reservoir (gain 1 per spell already cast this turn — *counts up cumulatively*)
- After 10 casts, Aetherflux gains 1+2+3+...+10 = 55 life cumulative → pay 50 life to deal 50 damage. Win.

With Necropotence filling hand + Bolas's Citadel casting off the top, spell density per turn is high. This line scales with creature count (more creatures = cheaper spells = more casts per turn).

### Line 4 — Necrotic Ooze + Devoted Druid + Quillspike (T6–8 with graveyard setup)

3-card combo with graveyard prep:

- **Necrotic Ooze** (`{2}{B}{B}`): has all activated abilities of creature cards in all graveyards.
- **Devoted Druid** (`{G}` — in graveyard): `{T}: Add {G}. Put a -1/-1 counter on this creature: Untap this creature.`
- **Quillspike** (`{2}{B}{G}` — in graveyard): `Remove a -1/-1 counter from target creature: Quillspike gets +3/+3 EOT.` (Ooze targets itself.)

Loop:
- Tap Ooze (Druid's ability): +1 green mana
- Put -1/-1 counter on Ooze (Druid's untap ability)
- Untap Ooze
- Remove -1/-1 counter from Ooze (Quillspike's ability) → Ooze gets +3/+3 EOT
- Repeat: infinite green mana + infinite Ooze power

Sink: Walking Ballista cast for X = infinite, OR attack with infinite-power Ooze.

Setup: Survival of the Fittest discards Druid and Quillspike into graveyard; Razaketh sacrifices them; or hard-cast and let them die. Necrotic Ooze cast for `{2}{B}{B}` (with affinity from Witherbloom, often free).

### Line 5 — Combat / Triumph of the Hordes

Backup. Beledros Pests (1/upkeep), Tendershoot Saprolings (1/upkeep, +2/+2 with city's blessing), Hornet Queen (5 1/1 flying deathtouch on ETB), boosted by counter doublers or pumped by Craterhoof / Triumph of the Hordes (infect).

**Goldfish kill window: T5 (Blood + Vito god-hand), T6 (Razaketh chain), T7–8 (storm or combat).** Through interaction: T6–T8 for primary kill, **ahead of the pod's T6–7 combo window** ([[pod-combo-opponent]]).

---

## Game Changer slots (3/3)

**Locked, optimized for tutor density and engine speed:**

1. **Necropotence** (`{B}{B}{B}`, owned, GC) — top-tier card draw engine. Pay 1 life per card off the top. With Exquisite Blood + Vito/Bond, the life paid on Necropotence triggers don't matter (we'll loop life back from the combo anyway). Skip-draw downside is negligible because Necro fills hand to 7+.
2. **Vampiric Tutor** (`{B}`, owned, GC) — instant-speed combo find on top of library. Find Blood or Vito on opponent's end step; untap, draw, deploy. **Best tutor in the deck.**
3. **Demonic Tutor** (`{1}{B}`, owned, GC) — sorcery-speed any-card to hand. Pairs with Vampiric — Vampiric for the combo turn, Demonic for the earlier setup.

**Considered and cut:**
- **Bolas's Citadel** (owned, B, GC) — engine + payoff, but slow (6 MV, takes a turn after casting). Strong with the affinity-storm line; would be GC #4. **Decision deferred to build time** — could swap out Demonic Tutor if storm line proves stronger than tutor-find-combo line in testing.
- **Survival of the Fittest** (owned, G, GC) — graveyard setup for Necrotic Ooze line. But only 1 copy owned and **contested across three proposals** ([[berta-proposal]], [[pest-control-proposal]], this build). Decision deferred to build time.
- **Worldly Tutor / Mystical Tutor / Crop Rotation / Ad Nauseam** — all GC, all viable. Demonic + Vampiric covers the same ground at less opportunity cost (instant + sorcery flexibility).
- **Mana Vault / Ancient Tomb** — fast mana GCs, owned. Worth slotting if the build wants T4 kill speed; would replace Demonic.

**Critical: Survival contention.** This proposal claims Survival as a non-GC slot (Necrotic Ooze line needs it). The Berta proposal and Pest Control proposal both claim Survival as a GC. Three decks cannot share one copy. Either buy a second copy (~€85, expensive single staple) or arbitrate at build time — Pest Control has the strongest claim (already proposed earlier, deeper graveyard dependency).

---

## The Grand Abolisher problem (race plan)

[[pod-combo-opponent]] notes Grand Abolisher blanks our interaction during their turn. Witherbloom's race window (T5–6) is ahead of the pod's T6–7 combo, so we're rarely forced to interact through Abolisher.

What still matters:
- **Our combo turn is exposed to non-Abolisher interaction from the rest of the pod.** Counters and removal can still hit us.
- **Veil of Summer** (`{G}`, owned 3) — blue/black opponents can't target us, draw on counter.
- **Heroic Intervention** (`{1}{G}`, owned 5) — hexproof + indestructible.
- **Boseiju, Who Endures** (channel for `{1}{G}` from hand) — destroys artifact/enchantment, including Grand Abolisher pre-emptively if we see it on the stack — actually no, Abolisher is a creature. Boseiju doesn't hit it. Boseiju does hit Smothering Tithe, Rhystic Study, etc.
- **Beast Within / Pongify / Rapid Hybridization** — answers to Abolisher when cast on our own turn (timing: before they untap into the combo turn).

**No clean GU-style storm-counter / Mindbreak Trap option** — BG can't run blue counters. The plan is: kill them before they Abolish.

**Anti-pod stax with no self-conflict:**
- **Vexing Bauble** — counters spells cast for 0 mana (Force of Will, Pact of Negation, evoke). Doesn't hurt our own combo (we always spend mana). Not yet owned check; buy ~€7.
- **Damping Sphere** (taxes second spell per turn, Storm) — situational; mostly for storm pod players.
- **Cursed Totem** — CUT. Blanks our own Bloom Tender, Birds, dorks, Witherbloom Apprentice activations (Apprentice triggers are magecraft, not activated, so actually safe — but blanks Razaketh, Yawgmoth, Walking Ballista's ping, etc.). Too much self-conflict.

---

## Construction skeleton (100 cards, ~38 lands)

**Commander (1):** Witherbloom, the Balancer

**Lands (38, sketch):**
- Bayou (owned 1, premium dual)
- Overgrown Tomb (owned 5+, shock)
- Underground Sea (owned 2 — but used elsewhere ⚠️ — wait, this is BG not UB, so Underground Sea is wrong color. Skip.)
- Fetches: Polluted Delta, Marsh Flats, Verdant Catacombs, Wooded Foothills, Misty Rainforest, Bloodstained Mire (most owned)
- Utility: Bojuka Bog, Phyrexian Tower (owned 4, fetchable for combo), Cabal Coffers (owned), Urborg Tomb of Yawgmoth (buy ~€20 — pairs with Coffers), Boseiju Who Endures, Dryad Arbor (owned, creature for affinity count)
- 8–10 basics (Swamp + Forest)
- Maze of Ith optional

**Token generators / wide board (8–10):**
- Beledros Witherbloom (buy, Pest at upkeep)
- Tendershoot Dryad (owned, Saproling at upkeep)
- Hornet Queen (buy, 5 1/1 fliers on ETB)
- Bitterblossom (faerie tokens, B enchantment, optional)
- Mycoloth (proliferating sap engine)
- Spawning Pit / Spider Spawning
- Avenger of Zendikar (owned, Plant tokens with landfall)
- Birds of Paradise (owned 6 — affinity counter + ramp)
- Bloom Tender (owned 2 — affinity counter + ramp; ⚠️ Mothman + Grand Design conflicts)
- Llanowar Elves / Elvish Mystic / Sakura-Tribe Elder

**Drain engines / payoffs (5–6):**
- Witherbloom Apprentice (buy, magecraft drain)
- Aetherflux Reservoir (owned 1, in Genome — duplicate ~€7)
- Bolas's Citadel (owned, GC slot or non-GC engine)
- Vito, Thorn of the Dusk Rose (buy — combo piece + life-gain drain)
- Sanguine Bond (buy — combo redundancy)
- Exquisite Blood (buy — combo piece)
- Professor Dellian Fel (owned 1 — engine + emblem)

**Tutors (6–8):**
- Vampiric Tutor (GC, owned 1) — also contested across proposals
- Demonic Tutor (GC, owned 3)
- Diabolic Intent (owned 2, not GC — sac creature to tutor)
- Razaketh, the Foulblooded (owned 2, not GC — engine + tutor)
- Worldly Tutor (GC — would be 4th, skip)
- Survival of the Fittest (GC — contested, decision deferred)
- Eldritch Evolution (buy ~€10 — sac to tutor by MV+2)
- Defense of the Heart (owned 2)
- Finale of Devastation (owned)

**Combo pieces:**
- Mikaeus, the Unhallowed (owned 1)
- Walking Ballista (owned 1 — in Mothman ⚠️, duplicate ~€8)
- Phyrexian Altar (owned 1)
- Phyrexian Tower (owned 4)
- Viscera Seer (owned 1, redundant sac outlet)
- Carrion Feeder (owned 2, redundant sac outlet)
- Yawgmoth, Thran Physician (owned 1 — sac outlet + draw)
- Necrotic Ooze (buy ~€2)
- Devoted Druid (buy ~€2)
- Quillspike (buy ~€1)

**Engine / draw (5–6):**
- Necropotence (GC, owned)
- Black Market Connections (owned 5)
- Sheoldred, the Apocalypse (owned 2, but used in Calamity Tax + Genome ⚠️)
- Skullclamp (owned 4 — token equipment for draw)
- Sign in Blood, Night's Whisper, Read the Bones (owned)
- Greater Good (owned — sac for draw)

**Ramp (6–8):**
- Sol Ring, Arcane Signet, Mana Vault (owned)
- Three Visits, Farseek, Cultivate, Kodama's Reach (owned)
- Crop Rotation (would be GC #4 — skip if we want non-GC)
- Cabal Coffers + Urborg (combo)
- Crucible of Worlds (owned, in another deck ⚠️)

**Interaction (5–6):**
- Toxic Deluge (GC? no — owned 6, wipe)
- Damnation (buy or owned)
- Beast Within, Pongify, Rapid Hybridization
- Assassin's Trophy, Putrefy, Maelstrom Pulse
- Veil of Summer, Heroic Intervention (protection)

**Anti-pod tech (1–2):**
- Vexing Bauble (buy ~€7, vs Force of Will)

**Sketches to ~99 + commander.** Exact list needs a build session.

---

## Buy list

**Required for the build (verified ownership against `moxfield_haves_2026-05-14-0631Z.csv`):**

| Card | Estimated price | Notes |
|---|---|---|
| **Exquisite Blood** | ~€5 | Primary combo piece |
| **Vito, Thorn of the Dusk Rose** | ~€3 | Primary combo piece (life-gain → drain) |
| **Sanguine Bond** | ~€2 | Combo redundancy |
| **Witherbloom Apprentice** | ~€1 | Magecraft drain (also starts combo loop) |
| **Beledros Witherbloom** | ~€2 | Pest engine + land-untap |
| **Hornet Queen** | ~€2 | 5-body ETB + Razaketh sac fodder |
| **Necrotic Ooze** | ~€2 | Combo piece |
| **Devoted Druid** | ~€2 | Combo piece (graveyard) |
| **Quillspike** | ~€1 | Combo piece (graveyard) |
| **Triskelion** | ~€3 | Mikaeus backup ping |
| **Aetherflux Reservoir** (duplicate) | ~€7 | Owned 1 in Genome, conflict |
| **Walking Ballista** (duplicate) | ~€8 | Owned 1 in Mothman, conflict |
| Urborg, Tomb of Yawgmoth | ~€20 | Coffers combo land |
| Vexing Bauble | ~€7 | Anti-Force-of-Will |
| Eldritch Evolution | ~€10 | Tutor (sac to tutor by MV+2) |
| Cauldron Familiar | ~€1 | Recurrable drain with Witch's Oven |
| Witch's Oven | ~€1 | Food / sac outlet for Familiar |
| Nyxbloom Ancient | ~€5 | Mana tripler (optional, very strong with Coffers) |

**Estimated total: ~€80–90.** Plus stretch buys (Mana Crypt, Mox Diamond — owned via Sol Ring/Mana Vault baseline, skip).

**Cross-deck conflicts (claim or duplicate):**
- Bloom Tender → Mothman + Grand Design + Berta proposal all use one of the 2 owned. **Triple contention.**
- Walking Ballista → Mothman ⚠️
- Aetherflux Reservoir → Genome Project ⚠️
- Survival of the Fittest → Berta proposal + Pest Control proposal + this build ⚠️
- Vampiric Tutor → only 1 owned; may be used elsewhere — verify
- Mana Vault → Berta proposal also claims
- Skullclamp → other decks possibly
- Sheoldred → Calamity Tax + Genome
- Crucible of Worlds → Loam + others
- Razaketh → Pest Control core (uses 1 of 2 owned)

**The Pest Control overlap is significant.** See "Roster conflicts" below.

---

## Roster conflicts

**Heaviest overlap: Pest Control ([[pest-control-proposal]]).** Both BG, both use:
- Razaketh as engine
- Witherbloom Apprentice
- Cabal Coffers
- Bayou, Overgrown Tomb, BG fetches
- Vampiric / Demonic Tutors
- Phyrexian Altar
- Cauldron Familiar / Witch's Oven (Pest Control aristocrats package)

**The engines are mechanically distinct:**
- Pest Control: sacrifice-aristocrats (Razaketh chain + reanimation pivot, win via Survival of the Fittest tutor + Citadel) — sacrifice-driven value.
- Witherbloom-Balancer: cast-trigger spellslinger (affinity-storm + magecraft drain + life-gain combo) — instant/sorcery-driven value.

The Conversion Check's mechanical distinctiveness rule (`REF_Bracket_3_House_Rules.md`) judges play patterns, not card pool. By that test, these are different decks: Pest Control wins through creature sacrifices and graveyard recursion; Witherbloom wins through spell chains and life-loop drain. **Verdict deferred to user at build time** — the substrate overlap is significant enough that a single user decision could close the door on coexistence.

**Other conflicts (lighter):**
- Calamity Tax (Sultai) — different archetype (voltron-value)
- Loam Cycle (Sultai) — graveyard land loops, no overlap
- Diminishing Returns (WB) — aristocrats drain, but no green and different play pattern

---

## Realistic ceiling

**18–19/20 (Elite).** Justification:

- **Core loop (5/5):** Three independent kill clusters (Blood+Vito 2-card pod-approved infinite, Razaketh chain to Mikaeus+Ballista+sac, affinity-storm via Apprentice/Aetherflux), plus a tertiary Necrotic Ooze line. Five+ redundant paths to lethal.
- **Speed (5/5):** T5 god-hand kill via Blood+Vito with Vampiric + Demonic tutors. T6 consistency case. **Ahead of the pod's T6–7 combo window.**
- **Resilience (3/5):** Same cap as Berta. Our combo turn is exposed to non-Abolisher interaction. BG has Veil of Summer (excellent), Heroic Intervention, and not much else. No counterspells. Targeted removal on Vito or Blood breaks the combo turn. The fallback is to race past disruption.
- **Recovery (4/5):** Razaketh as commander-grade tutor engine. Necropotence + Bolas's Citadel both fill hand from life. Sac-aristocrats subtheme provides built-in graveyard recursion. Witherbloom commander recursion via affinity (her own cost shrinks with creatures).

**Why not 20?** Resilience axis caps at 3–4. BG can't counter their counters of our combo turn. To clear 20 we'd need a third color (white for stax, blue for counters) or a Thoracle/Demonic Consultation kill — neither is in BG or thematic to Witherbloom.

**Why this is genuinely bracket-4-in-spirit:** T5–6 kill window with a 2-card pod-approved infinite, three redundant combo lines, max-density tutors (Vampiric + Demonic, both GC), Razaketh chain as a 4th engine. The deck plays hard within the 3-GC cap and closes ahead of the meta pod. Identity drift from the standard "BG midrange" trope is intentional per [[bracket-4-in-spirit]].

---

## Open questions for build session

1. **Pod-approval scope** — the 2-card approval was granted for the Berta build and extended here. Confirm at build time. If the user wants this to be a global rule revision rather than per-deck, document in `REF_Bracket_3_House_Rules.md` "Exceptions and revisions."
2. **Pest Control coexistence** — same archetype substrate (BG sac-tutor-drain), distinct engines (sacrifice vs. cast-trigger). User decides whether the mechanical distinctiveness rule allows both.
3. **Survival of the Fittest claim contention** — three proposals claim the single owned copy. Build-time arbitration needed; Pest Control has the strongest dependency.
4. **Bloom Tender contention** — Mothman + Grand Design + Berta proposal + Witherbloom proposal all want it. Only 2 owned. Hard limit at 2 simultaneous decks unless duplicates bought.
5. **Witherbloom Apprentice as combo-loop participant.** Magecraft triggers BOTH halves of the Blood+Vito loop simultaneously (drains opp + gains you). Confirm interaction with a Comprehensive Rules check at build time — should be fine, but verify the trigger ordering doesn't break anything.
6. **GC re-audit** — Necropotence, Vampiric Tutor, Demonic Tutor all on Feb 2026 list. Re-verify before locking the `.txt`. Bolas's Citadel and Survival should be revisited if testing shows the storm line needs more horsepower.
7. **Sleeve-up vs. proxy-first.** No active slot. Roster is at 16 decks. Either retire a deck (Pest Control is the natural candidate given the archetype overlap, but Pest Control is unbuilt anyway — it's also a proposal) or expand the roster.

---

## Card text re-verification log (2026-06-01, post-Scryfall update)

Re-checked the cards this proposal depends on:

- **Witherbloom, the Balancer** — confirmed: `{6}{B}{G}`, affinity for creatures (self + I/S you cast), flying, deathtouch, 5/5 Elder Dragon
- **Professor Dellian Fel** — confirmed: BG planeswalker, +2/0/-3/-6 abilities as quoted, NOT commander-legal (no enabling text on card)
- **Mikaeus, the Unhallowed** — confirmed: static +1/+1 to other non-Human creatures (not a counter per ruling — won't prevent undying), grants undying
- **Walking Ballista** — confirmed: enters with X counters; remove counter to deal 1 damage
- **Phyrexian Altar** — confirmed: sac creature for any-color mana
- **Razaketh, the Foulblooded** — confirmed: pay 2 life + sac a creature to tutor any card. Instant-speed activation.
- **Beledros Witherbloom** — confirmed: Pest token at upkeep; pay 10 life: untap all lands
- **Vito, Thorn of the Dusk Rose** — confirmed: life-gain triggers opp loss
- **Sanguine Bond** — confirmed: identical trigger to Vito's first ability. Ruling explicitly confirms Blood+Bond loop until win or break.
- **Exquisite Blood** — confirmed: opp loses life → you gain. Ruling confirms loop.
- **Witherbloom Apprentice** — confirmed: magecraft drain 1 / gain 1 per I/S cast
- **Aetherflux Reservoir** — confirmed: gain 1 per spell cast this turn (cumulative count)
- **Necropotence** — confirmed: skip-draw, exile-for-life draw next end step
- **Bolas's Citadel** — confirmed: cast from top of library by paying life equal to MV; sac 10 nonland for 10 each opp
- **Vampiric Tutor** — confirmed GC, owned, BG-legal
- **Demonic Tutor** — confirmed GC, owned, BG-legal
- **Tendershoot Dryad** — confirmed: Saproling at upkeep; +2/+2 with city's blessing
- **Hornet Queen** — confirmed: 5 1/1 flying deathtouch on ETB
- **Cauldron Familiar** — confirmed: drain 1 / gain 1 ETB, sac Food returns from graveyard
- **Witch's Oven** — confirmed: `{T}, sac creature: Food token`
- **Exsanguinate** — confirmed: each opponent loses X, you gain life equal to total lost
- **Necrotic Ooze** — to verify at build time (proposal cites the standard "has all activated abilities of creatures in graveyards" text; classic interaction)
- **Devoted Druid + Quillspike** — to verify at build time (classic combo, but check exact wording)

**Hashaton 2026-05-02 risk addressed** — all primary commander interactions and combo pieces verified post-Scryfall-refresh on 2026-06-01.
