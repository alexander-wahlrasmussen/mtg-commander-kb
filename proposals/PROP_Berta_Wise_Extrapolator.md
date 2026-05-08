# Proposal: Berta, Wise Extrapolator

Status: **not built.** Saved for future consideration.
Drafted: 2026-05-08.

Card text verified against local Scryfall data per `CLAUDE.md` hard rules. The Hashaton 2026-05-02 incident is the canonical reason proposals must verify before drafting.

---

## Commander

**Berta, Wise Extrapolator** (GU). `{2}{G}{U}`, Legendary Creature — Frog Druid, 1/4.

> **Increment** — Whenever you cast a spell, if the amount of mana you spent is greater than this creature's power or toughness, put a +1/+1 counter on this creature.
>
> Whenever one or more +1/+1 counters are put on Berta, add one mana of any color.
>
> `{X}, {T}`: Create a 0/0 green and blue Fractal creature token and put X +1/+1 counters on it.

**Color identity: GU (Simic).** Strict 2-color — no black tools.

Owned: 1 copy (SOS).

**Threshold mechanics for Increment.** "Greater than power or toughness" reads as the disjunction (mana > power OR mana > toughness), so the trigger fires when mana spent exceeds the *lower* of the two. Berta's power is always lower than her toughness as she grows from her own counters (P = 1+n, T = 4+n), so **the threshold tracks her power**: at 1/4 she triggers off any 2+ MV spell, at 2/5 off 3+, etc. The threshold ratchets up — sustaining the engine requires either bigger spells over time or external counter sources that don't push power higher than payoffs justify.

---

## Replacement context

This proposal **replaces Wise Mothman (Radiation Sickness)** in the roster slot, not adds alongside it. Two reasons:

1. **Archetype overlap is total.** Both decks live on +1/+1 counters and proliferate. The mechanical-distinctiveness house rule (`REF_Bracket_3_House_Rules.md`) would reject coexistence.
2. **The Mothman shell physically transfers.** Roughly 35–40 cards move directly from Mothman into Berta with no shopping required. Building Berta as a new deck while keeping Mothman would mean buying duplicates of Bloom Tender, Champion of Lambholt, Walking Ballista, Karn's Bastion, etc. — economically wasteful for a deck that will replace the worse one anyway.

Mothman is currently the lowest-scoring active deck (14/20). Berta is the natural upgrade lane, not a sideways add.

---

## Archetype framing

**Big-mana Simic ramp with Fractal-token finishers, not proliferate-as-engine.** Mothman's identity is *proliferate spreads rad counters to drain opponents*. Berta's identity is different even though the substrate overlaps:

- **Engine = mana refund per spell.** Each Increment trigger refunds one any-color mana. Cast a 6-MV spell, get back 1 mana of any color — Berta is effectively a 2-color 4-CMC mana rock that grows. This is *Animar-style cost reduction by a different mechanism*, not Mothman-style player-counter manipulation.
- **X-spells are the natural payoff.** `{X}{G}{U}` Hydroid Krasis pays back life and cards; Pull from Tomorrow draws X; Finale of Devastation at X≥10 wins on board; Stroke of Genius mills. Each X-spell triggers Increment because the threshold is in the X cost.
- **Fractal tokens are a built-in finisher.** `{X},{T}` makes an X/X every turn (and on every opponent's turn with Seedborn Muse). With counter doublers in play, that's 2X/2X.
- **Proliferate is supplementary, not central.** Cap the proliferate count well below Mothman's 12. Inexorable Tide and Tezzeret's Gambit earn slots; Viral Drake / Flux Channeler / Thrummingbird probably don't.

Right archetype label: *Simic big-mana / X-spell ramp with counter-payoff finishers.*

---

## Distinctiveness check

Replacing Mothman makes this trivially clean. Cross-check against the rest of the roster:

- **Loam Cycle (Teval, Sultai).** Different lane — Loam is graveyard recursion / land loops. Shared Simic ramp staples, no engine overlap.
- **Eldrazi Stampede Chaos (Maelstrom Wanderer, Temur).** Both run Avenger / Craterhoof / Selvala's Stampede as ramp-into-fatties. Wanderer's identity is cascade-into-haymaker; Berta's is X-spell value with token finisher. Different play patterns.
- **Earthbend the Meta (Toph, Naya).** Toph is artifact stompy with counters as a side note. Counter doubler overlap (Hardened Scales, Doubling Season, The Ozolith) is shared substrate, not shared engine.

**Verdict: distinct.** No conflict once Mothman retires.

---

## Power ceiling from collection

**Realistic ceiling: 15–16/20 (high Solid).** **17+ (Elite) is a stretch and requires structural additions, not just buys.**

Why the ceiling sits where it does:

- **Commander dependency is high.** Berta is a 4-CMC 1/4. Repeated removal taxes tempo the same way it taxed Mothman. Lightning Greaves / Heroic Intervention / Inspiring Call partially answer this.
- **2-color is a strict downgrade vs. Sultai.** Lose Toxic Deluge, Drown in the Loch, Assassin's Trophy, the Mindcrank+Bloodchief combo. Gain Doubling Season, X-spells, Selvala+Mantle line. Net: roughly even.
- **Counter strategies wrath poorly.** The Ozolith and Heroic Intervention are partial answers. A turn-7 Cyclonic Rift still costs 2–3 turns of rebuild.
- **Single combo line + combat is exactly the structure that scored 14 for Mothman.** The kill-reliability axis is the binding constraint.

### Owned shell that maps onto Berta

Verified ownership against `collection/moxfield_haves_2026-05-02-2113Z.csv`. ⚠️ = currently deployed in another active deck.

**Counter doublers:** Hardened Scales, Branching Evolution, Kalonian Hydra, Forgotten Ancient, Doubling Season, Kami of Whispered Hopes ⚠️ (Mothman). Vorinclex MR is the highest-impact buy — it doubles *your* counters, halves *opponents'* counters and proliferate (verified 2026-05-08), so it's a counter doubler AND a proliferate doubler AND political asymmetric in one card.

**Counter / token payoffs:** Walking Ballista ⚠️, Simic Ascendancy, Basking Broodscale, Iridescent Hornbeetle ⚠️, Champion of Lambholt ⚠️, Herd Baloth ⚠️, Ouroboroid ⚠️, Kodama of the West Tree ⚠️, The Ozolith ⚠️ (Toph + Mothman both use one).

**Big-mana ramp:** Sol Ring, Arcane Signet, Mana Vault ⚠️, Birds of Paradise, Bloom Tender ⚠️ (Mothman + Grand Design), Carpet of Flowers ⚠️, Exploration ⚠️, Azusa ⚠️, Oracle of Mul Daya ⚠️, Farseek, Three Visits, Cultivate, Kodama's Reach, Skyshroud Claim, Sakura-Tribe Elder, Springbloom Druid, Crucible of Worlds, Defense of the Heart ⚠️, Selvala's Stampede.

**X-spells / draw / finishers:** Finale of Devastation, Pull from Tomorrow, Selvala Heart of the Wilds ⚠️ (Eldrazi Stampede), Tatyova Benthic Druid, Garruk's Uprising, Sylvan Library ⚠️ (Loam + Calamity Tax), Avenger of Zendikar ⚠️, Craterhoof Behemoth ⚠️, Tooth and Nail ⚠️.

**Tutors:** Worldly Tutor, Mystical Tutor, Survival of the Fittest, Defense of the Heart ⚠️, Green Sun's Zenith ⚠️, Crop Rotation ⚠️.

**Interaction:** Counterspell, Mana Drain ⚠️ (Calamity Tax + Crystal Sickness + Dark Lord all use one of four owned), Swan Song (7 owned, 7 deployed — zero surplus), Force of Will ⚠️ (Grand Design), Fierce Guardianship, Cyclonic Rift, Beast Within, Pongify, Heroic Intervention, Reclamation Sage, Boseiju Who Endures, Krosan Grip (not owned), Inspiring Call ⚠️.

**Aetherflux Reservoir** (owned, 1 copy, deployed in Genome Project) is a soft alternate finisher — Berta's mana refund makes spell-storm turns realistic. Worth considering as a 4th-line wincon if a 2nd copy is acquired.

### Game Changer slots

**3/3 (locked):**
1. **Seedborn Muse** — non-negotiable. Untaps Berta on every opponent's turn, generating three additional Fractal tokens per cycle and three additional any-color mana via the counter trigger. Highest-impact GC for this commander specifically. Owned (2 copies, one deployed in Calamity Tax — surplus available).
2. **Fierce Guardianship** — free counterspell with commander in play, protects Berta directly. Surplus available (5+ owned).
3. **Cyclonic Rift** — only legal asymmetric reset in GU. Critical for a counter deck that loses to its own board state being wiped. Surplus available (5 owned).

**Not selected, considered:**
- **Force of Will** — second free counter, but the only owned copy is in Grand Design. Buying a duplicate (~€80) is the cost of admission. If the budget allows, swap Cyclonic Rift → Force of Will and accept a less robust answer to opposing board states.
- **Mystical Tutor / Worldly Tutor** — combo finders, but Fierce Guardianship's free-counter slot earns more in this shell. Run them as non-GC tutors instead.
- **Survival of the Fittest** — extremely strong creature tutor, owned, not deployed. Strong case for slotting it over Cyclonic Rift if combo speed matters more than wrath defense.

Verify against `REF_Game_Changers_List.md` at build time.

---

## Closing lines

1. **Combat (primary).** Avenger of Zendikar's Plant tokens grow with landfall + Doubling Season; Craterhoof Behemoth ETB pumps team +X/+X with trample. Fractal tokens add board width. Goldfish T8–10. Mothman parity.
2. **Finale of Devastation X≥10.** Tutors a creature, gives team +X/+X and haste. Game-ending swing once mana doublers are online (Mana Reflection, multi-untap from Seedborn Muse). Goldfish T7–9.
3. **Selvala + Umbral Mantle + 5+ power creature.** Verified mechanics:
   - Selvala: `{G},{T}: Add X mana in any combination of colors, where X is the greatest power among creatures you control.`
   - Umbral Mantle (current text, verified): `Equipped creature has "{3}, {Q}: This creature gets +2/+2 until end of turn."` `{Q}` is the untap symbol — paying it untaps the equipped creature as a cost.
   - Per cycle: tap Selvala (cost `{G}` + tap) for X mana, then activate Mantle (cost `{3}` + untap Selvala). Net = X − 4 mana per cycle. **Need X ≥ 5 for net positive infinite mana.** A 5-power creature is reachable through Berta with 4 counters, Forgotten Ancient with stored counters, or any Avenger Plant with 5+ lands.
   - Win sink: Walking Ballista (already in shell) for arbitrary damage, or Hydroid Krasis cast for X = drawn-deck for instant win-on-cast (uncounterable trigger gives life and cards even if Krasis itself is countered, verified 2026-05-08).
   - 3 components for the combo + 1 finisher = 4 cards. **House-rule legal** (>2 cards, late assembly).
4. **Simic Ascendancy.** Counter doublers + Vorinclex MR + Berta's own counter generation can hit 20 growth counters in 2–3 turns. Telegraphed but real.

**Kill window:** Goldfish T7–10. Through interaction T9–13.

---

## Path to Elite (17+)

The kill-reliability axis is the binding constraint. To clear 17, Berta needs **two redundant deterministic combo lines** rather than one. Three options, ordered by archetype fit:

### Option A — Marwyn + Staff of Domination (elf subtheme)

Verified mechanics:
- Marwyn: `{T}: Add an amount of {G} equal to Marwyn's power.` `Whenever another Elf you control enters, put a +1/+1 counter on Marwyn.`
- Staff of Domination: `{1}: Untap this artifact.` `{3}, {T}: Untap target creature.` Plus `{5}, {T}: Draw a card.`
- Per cycle: tap Marwyn for X green; pay `{3}, {T}` Staff to untap Marwyn; pay `{1}` to untap Staff. Net = X − 4 green mana per cycle. **Need Marwyn at 5+ power for infinite usable green.**
- Marwyn starts 1/1 and grows only on Elf ETBs — committing to this line means adding an elf package (Llanowar Elves, Elvish Mystic, Joraga Treespeaker, Quirion Beastcaller, etc.). That bend is *off-axis* with the X-spell core. Real cost: probably 6–8 elf slots, displacing X-spell density.

**Verdict: works, but bends the deck toward Marwyn-elves and weakens the X-spell identity.** Acceptable if elite tier matters more than thematic coherence; not recommended as the default path.

### Option B — Aetherflux Reservoir storm finisher

- Verified: gain 1 life per spell cast this turn, on each spell. `Pay 50 life: deal 50 damage to any target.`
- Berta's mana refund + Mana Reflection + multiple cantrips and X-spells can realistically hit 50 life and a one-shot kill in a single explosive turn.
- Not deterministic, but consistent if the deck is built with cheap-spell density. Adds a 4th closing line without shifting archetype.
- Cost: ~€7 for a second Aetherflux (existing one is in Genome Project). Possibly Mind's Desire-style payoffs if pushing further.

**Verdict: lowest-cost path to a meaningful 4th line. Doesn't push to 17 alone, but combined with the Selvala combo it shores up the kill-reliability axis.**

### Option C — Bloom Tender + Pemmin's Aura

Standard combo: Bloom Tender taps for one of each color among permanents you control; Pemmin's Aura `{U}: untap enchanted creature`. With 3+ colors among permanents, infinite mana of those colors.

**Doesn't work in 2-color GU.** No clean way to add a third color among permanents (Beast Within / Pongify tokens are colorless; treasure tokens are colorless; no GU multicolor permanents that aren't off-axis). Skip.

### Recommendation

**Build to 15–16/20 with the existing shell + a small buy package. Don't chase 17 with an elf bend.** Slot the Selvala+Mantle line and Aetherflux as a soft secondary, accept that the deck sits at "high Solid" rather than Elite. If 17+ becomes a hard requirement later, revisit the Marwyn-elf bend as a structural rebuild, not a tweak.

---

## Construction direction (if/when built)

- **Cap proliferate at 4–5 sources.** Inexorable Tide, Tezzeret's Gambit, Vorinclex MR, Karn's Bastion. Drop the rest of the Mothman proliferate package — Viral Drake, Flux Channeler, Thrummingbird, Contagion Engine, Contagion Clasp. Their slots go to X-spells and big mana.
- **X-spell density: 5–7 cards.** Hydroid Krasis (buy), Pull from Tomorrow, Finale of Devastation, Stroke of Genius (buy), Genesis Wave (buy or substitute Selvala's Stampede), Walking Ballista. These are the cards Berta's engine is built to support.
- **Mana doubler is the highest-impact single buy.** Mana Reflection (~€10) doubles all permanent-tapped mana. Stacks multiplicatively. Turns Berta into a turbo-mana engine when paired with Seedborn Muse.
- **Tribute to the World Tree (verified 2026-05-08).** `Whenever a creature you control enters, draw a card if its power is 3 or greater. Otherwise, put two +1/+1 counters on it.` No mana cost per trigger. Berta's Fractal tokens with X≥3 counters draw a card; smaller ones get +2/+2. Pure value enchantment. ~€3 buy.
- **Combo tutor density.** Defense of the Heart (find Selvala + finisher), Eldritch Evolution (sac Bloom Tender → Selvala), Worldly Tutor, Survival of the Fittest, Green Sun's Zenith. Five tutors that can find Selvala is enough redundancy.
- **Equipment for Berta protection.** Lightning Greaves or Swiftfoot Boots — Berta is the engine, must survive.
- **Land base: drop the BUG fetches and triomes from Mothman.** Polluted Delta, Verdant Catacombs, Zagoth Triome, Hedge Maze are wrong colors. Replace with Flooded Strand / Scalding Tarn / Botanical Sanctum / Yavimaya Coast. The Mothman summary's land buy list is partially relevant here.

---

## Buy list summary

**Required buys** (from non-owned cards needed for the build):
- Hydroid Krasis (~€2) — auto-include X-spell
- Mana Reflection (~€10) — highest-impact mana doubler in the shell
- Vorinclex, Monstrous Raider (~€5) — counter doubler + proliferate doubler + political
- Umbral Mantle (~€3) — combo piece
- Tribute to the World Tree (~€3) — value engine
- Eldritch Evolution (~€10) — combo tutor
- Stroke of Genius / Genesis Wave (~€5) — additional X-spell
- Krosan Grip (~€2) — split-second artifact/enchantment removal

**Total ~€40 in non-owned cards.**

**Cross-deck conflicts requiring duplicates or swaps** (only buy these if unwilling to swap between Mothman→Berta and the other deck):
- Selvala, Heart of the Wilds (~€3) — Eldrazi Stampede uses the only copy
- Walking Ballista (~€8) — Mothman's copy transfers cleanly if Mothman retires
- Most other ⚠️-flagged cards transfer cleanly when Mothman retires

If Mothman retires, **most ⚠️ flags resolve themselves** — the conflict is between Mothman and Berta on the same shell. Cards used by *other* active decks (Selvala in Eldrazi, Force of Will in Grand Design, Sylvan Library in Loam) remain real conflicts.

---

## Open questions for future build session

- **Confirm Mothman retirement.** This proposal assumes the slot swap. If Mothman stays in rotation, the build becomes a different (and weaker) deck — see the alternate framing in the deferred build session.
- **Re-verify all candidate cards before locking the `.txt`.** This proposal lists cards directionally; every card in the actual decklist must be re-verified per `CLAUDE.md` hard rules. Re-running `python scripts/update_scryfall_data.py` is a good first step at build time.
- **Decide on Selvala+Mantle as primary combo or relegate it to backup.** If primary, increase tutor density. If backup, the deck leans more on combat and the 15/20 ceiling is firm.
- **Game Changer cap audit.** Verify Seedborn Muse, Fierce Guardianship, Cyclonic Rift remain on the GC list at build time. The list has shifted twice in the last year (Oct 2025, Feb 2026).
- **Sleeve-up vs. proxy-first.** The roster is at 16 active decks; this is a 1-for-1 swap, so no slot expansion. But Mothman has physical cards deployed — sleeving Berta means physically dismantling Mothman, not a parallel build.
- **Re-verify Berta's Increment threshold interpretation.** This proposal assumes "greater than power or toughness" reads as the disjunction (mana > min(P, T)). Confirm with a current Comprehensive Rules check or a Scryfall ruling at build time. If the actual interpretation is "greater than max(P, T)", the engine is significantly weaker and the X-spell density needs to compensate harder.
