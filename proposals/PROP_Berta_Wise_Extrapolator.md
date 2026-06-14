# Proposal: Berta, Wise Extrapolator — Standalone Bracket-4-in-Spirit Build

Status: **SHELVED 2026-06-14** (user decision after the real-engine re-lab cited below). Within the 3-GC cap Berta does not compete — best clock ~36% by T12, median never-in-12, a worse Najeela. **Do not build on this document.** Revisit only if (a) the 3-GC house rule is waived for her — then build toward external "Deck #1" (7 GCs: Ancient Tomb + free counters + The One Ring/Rhystic dig) — or (b) GU gains an enchantment/artifact tutor or a Thassa's-Oracle-style line. Retained below as the worked record.
Drafted: 2026-05-08. **Rewritten 2026-06-01** as a standalone (no longer a Mothman replacement) and recast through the bracket-4-in-spirit lens. Updated same day with **pod approval for 2-card infinites** — primary kill line shifted to Bloom Tender + Freed from the Real, ceiling raised to 18–19/20.

Card text verified against local Scryfall data per `CLAUDE.md` hard rules. Re-verification log at the bottom.

> ⚠️ **LAB CORRECTION (2026-06-13) — the kill-window claims below are falsified.** `scripts/berta_clock_lab.py` (20k, GC-legal modelling build `decks/considering/berta-wise-extrapolator-20260613.txt`) measures **median kill never-in-12 (75% never; 3% by T6, 25% by T12)** — NOT the claimed "T3–5, ahead of the pod's T6–7." Every win line is gated on a **singleton, un-tutorable** enabler (Freed/Pemmin's auras, Umbral Mantle/Staff, Simic Ascendancy), and **GU has no enchantment/artifact tutor** — worse, the GCs this PROP lists as "non-GC" (**Cyclonic Rift, Mystical Tutor, Worldly Tutor**) are *all Game Changers*, so they can't legally backfill that gap under the 3-GC cap. **Do not build on this plan.** Full writeup: `analysis/Candidate_Clock_Labs_Berta_Najeela_2026-06-13.md`.
>
> **RE-LAB 2026-06-14 (addendum to that doc).** This plan also *omitted Berta's own best combo:* **Intruder Alarm + Berta's `{X},{T}` Fractal + any dork = infinite mana** (Fractal ETB → Alarm untaps all → re-tap dork → loop). Adding it + a Lyla/Pensive dig engine (the real-engine build `decks/considering/berta-wise-extrapolator-20260614.txt`) lifts the clock to **36% by T12 / 64% never / T7 10%** — better, but **median still never-in-12, still a worse Najeela.** Intruder Alarm should be in any Berta list. Within the 3-GC cap Berta is not a pod-racer; "competes" requires waiving the cap (external Deck #1 = 7 GCs).

---

## Why this proposal changed

The 2026-05-08 draft framed Berta as a Mothman swap with a 15–16/20 ceiling. Two things invalidated that frame:

1. **Mothman is now 17/20** (Radiation Sickness audit, 2026-05-13). Replacement math no longer holds; a 15/20 Berta is a downgrade.
2. **The pod meta now demands bracket-4-in-spirit power** ([[pod-combo-opponent]], [[bracket-4-in-spirit]]). The T6–7 combo pod requires fry-the-table speed within the 3-GC cap, not Solid-tier value.

This rewrite assumes Berta is built **as a roster addition (or new slot replacing a different deck)**, optimized for kill reliability rather than thematic coherence, and targeting **17–18/20**.

---

## Commander

**Berta, Wise Extrapolator** (GU). `{2}{G}{U}`, Legendary Creature — Frog Druid, 1/4.

> **Increment** — Whenever you cast a spell, if the amount of mana you spent is greater than this creature's power or toughness, put a +1/+1 counter on this creature.
>
> Whenever one or more +1/+1 counters are put on Berta, add one mana of any color.
>
> `{X}, {T}`: Create a 0/0 green and blue Fractal creature token and put X +1/+1 counters on it.

**Color identity: GU.** Owned: 1 copy (SOS). Verified 2026-06-01.

**Increment threshold tracks Berta's power** (always lower than toughness as she grows: P = 1+n, T = 4+n). So at 1/4 she triggers off any 2+ MV spell, at 2/5 off 3+, etc. The mana refund is **one mana per triggering event, not per counter** — counter doublers don't multiply the refund. They DO multiply the growth, which is what feeds the win lines.

---

## Pod-approved 2-card infinite (the engine)

`REF_Bracket_3_House_Rules.md` normally disallows 2-card infinites without pod approval. **User granted approval 2026-06-01** for this build. That unlocks the cleanest GU engine and makes the deck legitimately faster than the pod's T6–7 combo window.

The approval is **scoped to this deck**, not a global rule revision. Future builds default back to the 3+ card requirement unless renewed.

---

## Win lines (ordered by speed and resilience)

### Line 1 — Bloom Tender + Freed from the Real → Walking Ballista (primary, T3–5 kill)

**2-card infinite mana, pod-approved.**

Verified mechanics:
- Bloom Tender: `{T}: For each color among permanents you control, add one mana of that color.` Rulings confirm: with G and U among permanents, tap = `{G}{U}` = 2 mana.
- Freed from the Real: `{U}: Untap enchanted creature.` (Also `{U}: Tap enchanted creature` — irrelevant for combo.)
- Cycle: tap Bloom Tender for `{G}{U}` → pay `{U}` to untap. Net `{G}` per cycle. **Infinite green mana** (and infinite untap of Tender, breakeven blue).

GU among permanents is trivial — any Forest + any Island, or Berta herself, or any GU permanent. With Berta on the field, the threshold is auto-satisfied.

**Sink:** Walking Ballista already on board OR in hand → cast for X = infinite → ping each opponent for 40. Win.

**Backup sinks if Ballista isn't in hand:**
- Finale of Devastation X = very large → tutor Ballista directly to battlefield
- Hydroid Krasis cast for X = very large → draw deck, gain infinite life (uncounterable trigger), then Ballista or any sink from drawn cards
- Berta's own `{X}, {T}` → make 1 Fractal token with (very large) +1/+1 counters, kill via combat next turn (Doubling Season makes it 2 tokens with double the counters; trample via Garruk's Uprising)
- Helix Pinnacle (buy ~€2) — gain 100+ tower counters → win on next upkeep. Slower but has shroud, so harder to remove.

**Cast-on-curve speed:**

| Turn | Setup |
|---|---|
| T1 | Sol Ring + Forest. Mana floats. |
| T2 | Land (Island) + Bloom Tender (`{1}{G}`). Spare mana for a 1-drop dork if available. |
| T3 | Land + cast Freed from the Real (`{2}{U}`) on Bloom Tender. **Combo online if Walking Ballista is in hand.** With Sol Ring + 3 lands + Bloom Tender's tap, T3 mana pool is 5+ — enough to combo and ping for kill. |
| T4 | If Ballista wasn't in hand T3, Survival of the Fittest finds it. Kill T4. |

**T3 kill is real with perfect hand. T4–5 kill is the consistency case** given a tutor (Survival, Worldly, Mystical, Spellseeker, Defense of the Heart, Eldritch Evolution, Finale of Devastation).

**Berta is not strictly required for this line** — Tender + Freed kills with any GU mana base + Ballista. Berta is the resilience hedge (mana refund engine + Fractal alt-finisher + commander recursion).

### Line 2 — Bloom Tender + Pemmin's Aura → Walking Ballista (redundant Line 1)

Pemmin's Aura: `{U}: Untap enchanted creature.` Plus four other modes (shroud, flying, +1/-1) on the enchanted creature — irrelevant for combo but flavorful.

Same combo as Freed, second copy effect. **Both should be in the deck for redundancy** (~€3 buy, not owned). Tutor density (Mystical Tutor, Spellseeker for 2-MV enchantment? No, Pemmin's Aura is 3 MV — Spellseeker doesn't find it. Mystical Tutor and Worldly Tutor both miss Pemmin's. Survival doesn't find enchantments. Defense of the Heart only finds creatures.) — only Idyllic Tutor / Enlightened Tutor would find Pemmin's, and those aren't in CI. So Pemmin's is **backup-in-hand only**, not tutorable. Freed is the primary; Pemmin's is the second draw.

### Line 3 — Simic Ascendancy alt-win

**Cards in play required: Berta + Simic Ascendancy + at least one counter doubler.** Three cards.

Verified mechanics (2026-06-01):
- Simic Ascendancy (`{G}{U}`): *Whenever one or more +1/+1 counters are put on a creature you control, put that many growth counters on this enchantment. At the beginning of your upkeep, if this enchantment has twenty or more growth counters on it, you win the game.*
- Doubling Season: *If an effect would put one or more counters on a permanent you control, it puts twice that many of those counters on that permanent instead.* Affects growth counters too (growth counters are counters on a permanent you control).
- Hardened Scales: *If one or more +1/+1 counters would be put on a creature you control, that many plus one +1/+1 counters are put on it instead.* Only +1/+1 counters.
- Branching Evolution: Same as Hardened Scales (worded identically per Scryfall).

Math, with combo stacked (controller chooses replacement order):

| Setup | Growth per Berta trigger | Spells to lethal (20 growth) |
|---|---|---|
| Ascendancy + Berta (no doubler) | 1 | 20 |
| + Doubling Season | 4 | **5** |
| + Doubling Season + Hardened Scales | 8 | **3** |
| + DS + HS + Branching Evolution | 12 | **2** |
| + DS + HS + BE + Vorinclex MR | 24 | **1** (next upkeep wins) |

Walkthrough at DS + HS: Berta's trigger would put 1 counter → Hardened Scales replaces to 2 → Doubling Season doubles to 4 → Ascendancy triggers with "4 counters were put" → puts 4 growth counters → Doubling Season replaces to 8 growth.

**This wins on next upkeep after 3 qualifying spell casts** with two cheap doublers. The doublers are cheap (DS aside) and double as combat enablers, so they aren't dead cards before the combo lands. **This is the primary kill.**

Note: Ascendancy triggers on +1/+1 counters on **any** creature you control — Berta isn't the only source. Avenger of Zendikar's Plant tokens entering with landfall counters, Champion of Lambholt growing on each creature ETB, Fractal token activations all feed Ascendancy.

### Line 4 — Selvala + Umbral Mantle + 5-power creature → Walking Ballista

Verified mechanics:
- Selvala HotW: `{G}, {T}: Add X mana in any combination of colors, where X is the greatest power among creatures you control.` (Mana ability, doesn't use stack — uncounterable.)
- Umbral Mantle: `{3}, {Q}`: +2/+2 EOT. `{Q}` is untap symbol (paid as cost, untaps Selvala).
- Net per cycle: X − 4 mana. Need 5+ power creature for infinite positive mana.

4 cards (Selvala + Mantle + 5-power + Ballista). House-rule legal.

5-power creatures in shell:
- Berta with 4 counters (3 spells in)
- Forgotten Ancient with stored counters
- Kalonian Hydra (5/5 base)
- Avenger of Zendikar's Plants with 5+ lands
- Craterhoof Behemoth (5/5)
- Champion of Lambholt at 4 ETBs

Backup sink if Ballista is countered: Hydroid Krasis cast for huge X — `When you cast this spell, you gain half X life and draw half X cards` resolves before counterspells (verified). So even a countered Krasis empties the deck.

### Line 5 — Marwyn + Staff of Domination (elf bend, optional)

Verified mechanics:
- Marwyn the Nurturer: `{T}: Add an amount of {G} equal to Marwyn's power. Whenever another Elf you control enters, put a +1/+1 counter on Marwyn.`
- Staff of Domination: `{3}, {T}: Untap target creature. {5}, {T}: Draw a card.` Plus `{1}: Untap this artifact.`
- Cycle: tap Marwyn for X green → pay `{3}, {T}` Staff to untap Marwyn → pay `{1}` to untap Staff. Net X − 4 green per cycle. Need Marwyn at 5+ power.

This needs an Elf package (Llanowar Elves, Elvish Mystic, Joraga Treespeaker, Quirion Beastcaller) to grow Marwyn — minimum ~4 elf slots displacing X-spell/counter-doubler slots. The original proposal flagged this bend as off-axis and refused it; under the bracket-4-in-spirit lens, **it earns its slots as a third infinite-mana redundancy**. Recommended: include, sized to 4–5 elf slots, not 8.

### Line 6 — Aetherflux Reservoir storm

Verified: `Whenever you cast a spell, you gain 1 life for each spell you've cast this turn. Pay 50 life: this artifact deals 50 damage to any target.` Counts the triggering spell. Berta's mana refund stacks with Sapphire Medallion, Mana Reflection, and Seedborn Muse cycles for big-storm turns. Owned (1 copy, currently in Genome Project — duplicate ~€7).

Natural multi-card line — no combo-rule issue.

### Line 7 — Combat (Avenger / Craterhoof / Triumph of the Hordes)

Backup. All owned (Triumph in plst). Doubling Season makes Plants enter with 2 counters; Craterhoof ETB pumps team. Multi-card by construction.

**Goldfish kill window: T3–4 (Tender + Freed god-hand), T5 consistency case (with one tutor activation), T6 (Ascendancy with DS + HS), T7 (Selvala+Mantle), T8 (combat or storm).** Through interaction: T5–T7 for primary kill.

**This is now ahead of the pod's T6–7 combo window** ([[pod-combo-opponent]]).

---

## Game Changer slots (3/3)

**Locked, optimized for race speed vs. T6–7 combo pod:**

1. **Seedborn Muse** — non-negotiable. Doubles Berta's effective tempo (X-spell activation every turn cycle, Fractal pump every turn cycle, Aetherflux trigger fuel). Owned (2 copies, surplus). Mothman currently runs one — if both decks stay active, buy a second physical copy (~€5) or proxy.
2. **Survival of the Fittest** — best tutor in green. Finds Selvala, Bloom Tender, Marwyn, Walking Ballista (creature), Avenger, Craterhoof on demand at instant-ish speed. Owned. Verified GC status 2026-06-01.
3. **Mana Vault** — the bracket-4-in-spirit pick over Cyclonic Rift / Fierce Guardianship. T2 Mana Vault → T3 Berta is a real line that compresses the kill window by one full turn. Owned (3 copies, currently 1 deployed elsewhere). Verified GC.

**Considered and cut:**
- **Cyclonic Rift** — defensive. Doesn't speed up kills; bracket-4-in-spirit prioritizes offense.
- **Fierce Guardianship** — protects Berta but doesn't function against Grand Abolisher on the pod's combo turn (Abolisher locks our castable interaction during their turn — counters don't fire). Worth running as non-GC for non-pod matchups.
- **Worldly / Mystical Tutor** — both run as non-GC tutors, but Survival earns the slot over either.
- **Force of Will** — same Abolisher blank-out as Fierce Guardianship. Skip.
- **Crop Rotation** — no Gaea's Cradle to find (Cradle would be GC #4). Skip.

---

## The Grand Abolisher problem (mostly solved by racing)

**Grand Abolisher reads:** *Your opponents can't cast spells or activate abilities of artifacts, creatures, or enchantments during your turn.* GU cannot interact at instant speed during the Abolisher controller's turn — Counterspell, Pongify, Beast Within, Krosan Grip all blocked.

**With the Tender + Freed line on the table, this matters far less.** Our combo turn is T3–5, the pod's combo turn is T6–7. We close before Abolisher resolves.

What still matters:
- **Protection on our own combo turn.** Opponents can still cast spells during *our* turn (Abolisher only locks *their* turn). Mana Drain, Swan Song, Force of Will, Pongify on our Bloom Tender all still fire.
- **Veil of Summer** (`{G}`, owned 3) — blue/black opponents can't target us or our spells, draw on counter. Best protection in CI.
- **Heroic Intervention** (`{1}{G}`, owned 5) — hexproof + indestructible all permanents. Beats targeted removal on Bloom Tender or Freed.
- **Swan Song** (`{U}`, owned 7+) — counters non-creature spells. Cheap, holdable.
- **Counterspell / Mana Drain** as backup, knowing they may be blanked under Abolisher.

**Anti-pod stax tech that doesn't conflict with our combo:**
- **Vexing Bauble** (owned) — counters spells cast with no mana. Blanks Force of Will, Misdirection, Pact of Negation, free evoke. **No conflict** with our Tender combo because we always spend mana.
- **Cursed Totem CUT.** Blanks our own Bloom Tender, Selvala, Marwyn — too much self-conflict for a build that races through Tender. Replaced by Vexing Bauble as the primary anti-free-spell silver bullet.

The race plan is now realistic, not aspirational.

---

## Construction skeleton (100 cards, 38 lands)

**Commander (1):** Berta, Wise Extrapolator

**Lands (38, sketch):**
- 12 basics (6 Forest, 6 Island roughly — Tribute to the World Tree wants basics)
- Fetches/duals: Misty Rainforest, Scalding Tarn, Flooded Strand (if unowned, sub Yavimaya Coast / Botanical Sanctum / Hinterland Harbor / Breeding Pool)
- Utility: Boseiju Who Endures, Otawara, Soaring City, Karn's Bastion, Reliquary Tower, Oran-Rief, the Vastwood
- Ramp lands: Yavimaya, Cryptic Caves; one or two fast-mana lands if owned

**Counter doublers (5–6):** Hardened Scales, Branching Evolution, Doubling Season, Vorinclex MR (buy), The Ozolith, Kalonian Hydra (also a 5/5 finisher for Selvala line)

**Win cards (6–7):** Bloom Tender (combo + ramp, owned), **Freed from the Real (buy, primary combo)**, **Pemmin's Aura (buy, combo redundancy)**, Simic Ascendancy, Walking Ballista, Hydroid Krasis (buy), Aetherflux Reservoir (buy duplicate), Umbral Mantle (buy), Helix Pinnacle (buy, backup sink, optional)

**Mana / engine (10–12):** Sol Ring, Arcane Signet, Mana Vault (GC), Sapphire Medallion, Bloom Tender, Birds of Paradise, Mana Reflection (buy), Seedborn Muse (GC), Selvala HotW (buy duplicate or claim from Eldrazi Stampede), Marwyn the Nurturer (buy), Staff of Domination (buy)

**Elf package for Marwyn line (4–5):** Llanowar Elves, Elvish Mystic, Joraga Treespeaker, Quirion Beastcaller, Bloom Tender (already counted)

**Ramp (6–7):** Birds of Paradise, Three Visits, Farseek, Cultivate, Kodama's Reach, Skyshroud Claim, Sakura-Tribe Elder, Springbloom Druid, Crucible of Worlds, Exploration (owned)

**Tutors (8):** Survival of the Fittest (GC), Worldly Tutor, Mystical Tutor, Spellseeker (buy), Defense of the Heart, Eldritch Evolution (buy), Tooth and Nail, Finale of Devastation, Green Sun's Zenith — pick 6–8 from this list

**X-spells / draw (5–6):** Hydroid Krasis, Pull from Tomorrow, Stroke of Genius, Genesis Wave / Selvala's Stampede, Tatyova Benthic Druid, Garruk's Uprising, Tribute to the World Tree (buy)

**Counter / token payoffs (4–5):** Forgotten Ancient, Champion of Lambholt, Iridescent Hornbeetle, Avenger of Zendikar, Craterhoof Behemoth, Triumph of the Hordes

**Interaction (6–7):** Counterspell, Mana Drain (owned 4, conflicts with Calamity Tax / Crystal Sickness / Dark Lord — claim one or proxy), Swan Song, Veil of Summer, Heroic Intervention, Beast Within, Pongify, Rapid Hybridization, Krosan Grip (buy), Cyclonic Rift (non-GC slot), Boseiju Who Endures channel

**Anti-pod stax (1):** Vexing Bauble (owned, vs Force of Will / free spells). Cursed Totem **cut** — blanks own Tender combo.

**Protection for Berta (2):** Lightning Greaves, Swiftfoot Boots, Inspiring Call (also draws on doubler-out turns)

This sketches to ~99 + commander. Exact list requires a build session and a card-by-card cut pass.

---

## Buy list

**Required for the build (verified ownership against `moxfield_haves_2026-05-14-0631Z.csv` on 2026-06-01):**

| Card | Estimated price | Notes |
|---|---|---|
| Umbral Mantle | ~€3 | Combo piece, Selvala line |
| Hydroid Krasis | ~€2 | X-spell sink + uncounterable trigger |
| Mana Reflection | ~€10 | Highest-impact mana doubler |
| Vorinclex, Monstrous Raider | **VERIFY before buying** | Memory [[verify-prices]] flagged a €5→€30+ Cardmarket gap. Could be the single most expensive card on this list. |
| Marwyn the Nurturer | ~€3 | Combo piece, elf bend |
| Staff of Domination | ~€10 | Combo piece, elf bend |
| Spellseeker | ~€3 | Tutor for instants/sorceries ≤2 |
| Tribute to the World Tree | ~€3 | Value enchantment |
| **Freed from the Real** | ~€2 | **Primary combo piece with Bloom Tender** |
| **Pemmin's Aura** | ~€3 | **Redundant Bloom Tender untapper** |
| Helix Pinnacle | ~€2 | Backup infinite-mana sink with shroud (optional) |
| Krosan Grip | ~€2 | Split-second artifact/enchantment removal |
| Eldritch Evolution | ~€10 | Combo tutor (sac Bloom Tender → Selvala; risky — only after combo lands) |
| Selvala HotW *or* claim from Eldrazi Stampede | ~€3 | One in collection (foil, CMM), deployed in Eldrazi |
| Walking Ballista *or* claim from Mothman | ~€8 | One owned (proxy, FIC), deployed in Mothman |
| Aetherflux Reservoir *or* claim from Genome | ~€7 | One owned (foil, PKLD), deployed in Genome |

**Estimated total before Vorinclex verification: ~€80. With Vorinclex at €30: ~€105.** Re-verify all prices at Cardmarket before pulling the trigger per [[verify-prices]].

**Cross-deck conflicts (claim or duplicate):** Selvala (Eldrazi Stampede), Walking Ballista (Mothman), Aetherflux (Genome), Bloom Tender (Mothman + Grand Design), Forgotten Ancient (Mothman), Champion of Lambholt (Mothman), Kami of Whispered Hopes (Mothman), Inspiring Call (Mothman), Crop Rotation (Loam), Sylvan Library (Loam + Calamity), Mana Drain (Calamity Tax + Crystal Sickness + Dark Lord), Earthcraft (Najeela).

The biggest conflict is **Mothman**. If both decks are active, ~6–7 cards need duplicating (~€40 in shared staples). If Mothman retires after all, this proposal becomes ~€60 net.

---

## Realistic ceiling

**18–19/20 (Elite).** Justification:

- **Core loop (5/5):** Primary 2-card infinite (Tender + Freed, pod-approved) + 2-card redundancy (Tender + Pemmin's) + Ascendancy alt-win + Selvala+Mantle + Marwyn+Staff. **Five redundant kill lines**, with the primary winning T3–5.
- **Speed (5/5):** T3 god-hand, T4–5 consistency, T6 worst case. Sol Ring + Mana Vault + Bloom Tender on curve. **Ahead of the pod's T6–7 combo window.** This is the biggest improvement vs. the original 15–16 framing.
- **Resilience (3/5):** Still the binding constraint, but for a different reason. We no longer need to interact through Abolisher because we race past it. The cap on this axis now comes from: (a) our own combo turn being exposed to counterspells from the rest of the pod (mitigated by Veil of Summer, Heroic Intervention, Swan Song), (b) targeted removal on Bloom Tender before T3 (mitigated by Survival, Lightning Greaves, the redundant Pemmin's slot, and the secondary Ascendancy line).
- **Recovery (4/5):** Survival + Worldly + Spellseeker + Defense of the Heart + Eldritch Evolution + Finale of Devastation + Mystical Tutor = ~7 tutor density. Berta as commander gives reliable engine recursion through command tax.

**Why not 20?** Resilience axis caps at 3–4. Our combo turn is still exposed to the rest of the pod's interaction, and Bloom Tender dies to a `{1}` Pongify on the wrong turn. To clear 20 we'd need to splash a third color for stronger protection (Veil of Summer is the best we have) or run a Thoracle/Demonic Consultation line — neither of those is in GU/in budget.

**Why is this a real bracket-4-in-spirit deck?** T3–5 kill window with a 2-card infinite is the textbook bracket-4 play pattern. The deck plays hard within the 3-GC cap and wins on its own turn ahead of the pod's combo. Identity drift from the original "X-spell value commander" framing is intentional and embraced per [[bracket-4-in-spirit]] — the user's note that *identity matters less than just being able to fry our opponents* applies here.

---

## Open questions for build session

1. **Mothman coexistence.** Mechanical distinctiveness rule (`REF_Bracket_3_House_Rules.md`) — both decks share +1/+1 counter substrate. Berta's primary line (Tender + Freed → Ballista) is mechanically distinct from Mothman's rad-proliferate-drain plan, but the *shared substrate* of counter doublers and Bloom Tender could read as overlap. **Verdict needed at build time from the user, not unilaterally.**
2. **Pod-approval scope.** The 2-card infinite approval was granted for Berta specifically. Confirm this isn't a global rule revision; future builds should default back to 3+ card requirement unless explicitly renewed. Consider documenting in `REF_Bracket_3_House_Rules.md` under "Exceptions and revisions" if this becomes a pattern.
3. **Selvala+Mantle / Marwyn+Staff retention.** With Tender + Freed as primary, are the 3–4 card backup lines still worth their slots? Default: yes — they hedge against Tender removal and add power without conflicting with the engine. The Marwyn elf bend is the most expendable (4–5 elf slots could become more X-spells or interaction).
4. **Increment interpretation.** Confirmed reading: "greater than power or toughness" is disjunctive — threshold is min(P, T) = power. Re-verify with a current Comprehensive Rules check or Scryfall ruling at build time.
5. **GC re-audit.** Mana Vault, Seedborn Muse, Survival of the Fittest all on the Feb 2026 list. Re-verify before locking the `.txt`. List has shifted twice in the last year.
6. **Sleeve-up.** No active slot for Berta currently. Either retire a deck (Mothman is the historical candidate, but 17/20 now — a Berta at 18–19 ceiling could justify the swap), expand the roster, or proxy-test in a parallel build.

---

## Card text re-verification log (2026-06-01)

Re-checked the cards this rewrite depends on, against local Scryfall data:

- Berta, Wise Extrapolator — unchanged
- Bloom Tender — confirmed: *for each color among permanents you control, add one mana of that color* (rulings confirm GU = `{G}{U}` = 2 mana)
- Freed from the Real — confirmed: `{U}: untap enchanted creature` (PRIMARY COMBO PIECE under pod approval)
- Pemmin's Aura — confirmed: `{U}: untap enchanted creature` (REDUNDANT combo piece)
- Helix Pinnacle — confirmed: shroud, `{X}: put X tower counters`, win on upkeep with 100+ tower counters (intervening-if clause)
- Selvala, Heart of the Wilds — confirmed, mana ability
- Umbral Mantle — confirmed, `{3}, {Q}` for +2/+2 EOT
- Walking Ballista — confirmed (X X cost, ping)
- Hydroid Krasis — confirmed, cast trigger resolves before counters
- Aetherflux Reservoir — confirmed, counts the triggering spell
- Mana Reflection — confirmed, doubles only when *you* tap permanents for mana
- Survival of the Fittest — confirmed (current GC, Feb 2026 list)
- Cursed Totem — confirmed: stops creature mana abilities (Bloom Tender, Selvala, Marwyn affected too)
- Vexing Bauble — confirmed: counters spells cast with no mana spent
- Simic Ascendancy — confirmed: 20 growth = win on upkeep, growth counters subject to Doubling Season
- Hardened Scales — confirmed: +1/+1 only, controller picks replacement order
- Doubling Season — confirmed: doubles tokens AND counters on permanents (growth counters included)
- Vorinclex, Monstrous Raider — confirmed: doubles your counters of all kinds
- Marwyn the Nurturer — confirmed: mana ability, taps for power-equal green
- Staff of Domination — confirmed: 6 modes including `{1}: untap this`
- Spellseeker — confirmed: ETB tutors instant/sorcery ≤2 MV
- Tribute to the World Tree — confirmed: draw on 3+ power ETB, otherwise 2 counters (no mana cost)
- Finale of Devastation — confirmed: X≥10 gives team +X/+X and haste

All combo lines verified mechanically. Hashaton 2026-05-02 risk addressed.
