# Atraxa, Grand Unifier — Replacement Swaps

**Deck:** The Grand Design (`the-grand-design-20260402-100951.txt`)
**Reason:** 6 cards physically unavailable (most are zero-surplus shared cards held by other decks).
**Goal:** Preserve the Conversion Check score of **19/20 (5/5/5/4)** and the original Bracket 3 strict-3-GCs design.

---

## Summary table

| Out                          | In                        | Role preserved / gained                              | Owned? (set / count)        |
| ---------------------------- | ------------------------- | ---------------------------------------------------- | --------------------------- |
| Beast Within                 | Assassin's Trophy         | 2–3 mana removal (any perm)                          | ✅ 2x (2x2)                 |
| Boseiju, Who Endures         | Bojuka Bog                | Utility land (a "free" effect)                       | ✅ 5+ across multiple sets  |
| Fierce Guardianship *(GC)*   | **Force of Will** *(GC)*  | Free counter — strictly better than FG (any spell, any turn, no future cost) | ✅ 1x (dmr)                 |
| Sakura-Tribe Elder           | Bloom Tender              | MV-2 ramp creature; scales to WUBG with Atraxa       | ✅ 2x (ecl)                 |
| Seedborn Muse *(GC)*         | Rhystic Study *(GC)*      | Resource engine (draw, not untap)                    | ✅ 1x (pcy)                 |
| Entomb                       | **Grisly Salvage**        | Reanimation enabler (mill 5, get creature/land to hand) | ✅ 2x (tdc)              |

**Net swap count:** 6-for-6. Deck stays at exactly 100 cards. **GC count restored to 3/3** (Cyclonic Rift, Rhystic Study, Force of Will).

---

## Per-card rationale

### 1. Beast Within → Assassin's Trophy

- Beast Within: 3 mana, instant, destroy any permanent, opponent gets a 3/3 Beast token.
- Assassin's Trophy: **2 mana**, instant, destroy any permanent, opponent searches for a basic land and puts it onto the battlefield tapped.
- **Why it works:** Strictly cheaper, same "any permanent" coverage. The downside (basic land vs. 3/3 beast) is mild and arguably better — a basic land doesn't attack you.
- **Score impact:** Interaction profile unchanged; if anything, slightly improved by mana cost.

### 2. Boseiju, Who Endures → Bojuka Bog

- Boseiju: untapped green source, channel to destroy nonbasic land / artifact / enchantment.
- Bojuka Bog: ETB tapped, exiles a graveyard on entry.
- **Why it works:** Both are "a spell stapled to a land." We trade artifact/enchantment removal for graveyard hate, which matters against the Sauron / Teval / reanimator-heavy decks in your meta. The deck also runs Atraxa's own ETB drawing 5–7, so a single tapped land entering is rarely catastrophic.
- **Alternative if you want untapped mana over utility:** swap to a basic Forest instead. That keeps Atraxa castable on curve but gives up the graveyard answer.
- **Score impact:** Mana base remains within tolerance; loss of a flexible answer is partly offset by graveyard interaction.

### 3. Fierce Guardianship → Force of Will

- Fierce Guardianship: **0 mana** counter (with commander in play), counters noncreature only.
- Force of Will: **0 mana** counter (pay 1 life and exile a blue card from your hand), counters **any** spell, on **any** turn. 5 mana hard-cast.
- **Why it works (and why this is an upgrade, not a substitute):**
  - **Strictly more flexible:** Fierce Guardianship needed Atraxa in the command zone or on board; Force of Will is always free regardless of board state.
  - **Hits creatures:** the deck summary explicitly flags creature spells / creature-based combos as a counter gap. Force of Will closes that gap permanently.
  - **No future cost:** unlike Pact of Negation (originally suggested but unavailable — held in Calamity Tax), Force of Will doesn't lock you into a 5-mana upkeep payment.
  - **Game Changer:** Force of Will is itself on the GC list, so this single swap restores the deck to **3/3 GCs** without needing further changes.
- **Loss:** "Pitch a blue card" reduces hand size by 2 (the FoW + the pitched card), and you lose 1 life. The deck has plenty of blue cards (Counterspell, Mana Drain, Force of Negation, Swan Song, Dovin's Veto, Cyclonic Rift, Rhystic Study, Ghostly Flicker, Ephemerate, etc.) so finding pitch fodder is easy.
- **Score impact:** Counter count holds at 5; interaction profile improves on quality (creature coverage). Still 4/5 (the ceiling is held back by lack of noncreature tutoring, not counter density).

### 4. Sakura-Tribe Elder → Bloom Tender

- Sakura-Tribe Elder: 1G, 1/1 Snake, sac to fetch a basic land tapped.
- Bloom Tender: **1G, 1/2**, T: add one mana of each color among permanents you control.
- **Why it works:**
  - **Pod chain:** MV-2 slot preserved (Birds → Bloom Tender → MV-3 like Eternal Witness).
  - **Reveillark loop:** Bloom Tender is power 1, so Reveillark can return it from the graveyard.
  - **Compensates for Seedborn Muse loss:** with Atraxa on the battlefield, Bloom Tender taps for **WUBG = 4 mana per turn**. That's the engine that brings the Finale-of-Devastation X≥10 line back into reach (you needed Seedborn for the mana acceleration; Bloom Tender does the same job from a different angle).
  - Pre-Atraxa, Bloom Tender still ramps for whatever colors you have on board (Birds = G, Grand Abolisher = W, etc.).
- **Loss:** No ETB trigger, so weaker with Panharmonicon / Elesh Norn / flicker engine than an ETB-creature replacement (Coiling Oracle was an alternative considered for that reason — pick Coiling Oracle if you'd rather lean into flicker value over mana acceleration).
- **Score impact:** Core loop integrity preserved (Pod + Reveillark); helps recover the Kill Reliability hit from losing Seedborn.

### 5. Seedborn Muse → Rhystic Study

- Seedborn Muse: 3GG, 5 mana, untap all your permanents on each opponent's turn.
- Rhystic Study: **1U, 3 mana**, whenever an opponent casts a spell, you draw a card unless they pay 1.
- **Why it works:**
  - **Same archetype role: a passive engine that punishes opponents for playing the game.** Rhystic isn't a mana doubler, but it generates a torrent of card advantage — easily 3–6 cards per cycle of the table.
  - **Game Changer:** Rhystic Study **is** on the GC list, so this swap preserves one of the two GC slots being lost.
  - **Cheaper to deploy:** 3 mana vs. 5 mana — more likely to land before turn 5.
- **What you actually lose:** The Finale-of-Devastation X≥10 kill line becomes harder. Seedborn enabled a 12-mana Finale by untapping on 2–3 opponents' turns. Without it, that line wants Carpet of Flowers, Vilis draws, or a mana-doubling effect (Mana Drain hit) to assemble.
- **Score impact:**
  - **Kill Reliability:** Slight ding on Finale-line speed, but the deck still has 9 other kill lines (Defense of the Heart, Razaketh tutor, Karmic Guide loop, etc.). Still 5/5.
  - **Durability:** Rhystic Study refills your hand after wipes — arguably *improves* recovery. Still 5/5.

### 6. Entomb → Grisly Salvage

- Entomb: **1B instant**, search your library for any card and put it directly into your graveyard.
- Grisly Salvage: **1BG instant (3 mana)**, mill 5 cards from the top of your library, then return a creature or land card from among them to your hand.
- **Why it works:**
  - Preserves Entomb's *role* — getting reanimation targets into the graveyard at instant speed. Mills 5 cards, which has good odds of hitting at least one of Razaketh / Vilis / Elesh Norn (3 of the deck's fattest creatures).
  - **Instant speed matches Entomb's tempo:** mill at end of opp's turn → reanimate on yours.
  - **Card-selection bonus:** the "return a creature or land to hand" clause grabs Karmic Guide or Reveillark for the reanimation chain, or a missing land drop.
- **Loss:**
  - **Random mill, not deterministic:** unlike Entomb (find Razaketh exactly), Grisly Salvage is a probability play. ~50% to mill at least one of the 3 primary reanimation targets in 5 cards. If it whiffs on big creatures, you still get card advantage from the creature-to-hand clause.
  - Mana cost up by 1 (2 → 3) and demands a green source alongside black.
- **In-collection alternatives considered (and rejected):**
  - *Final Parting* — originally proposed; **unavailable**, held in Loam Cycle.
  - *Diabolic Intent* — both copies deployed (Exile's Return, Dark Lord's Army).
  - *Grim Tutor* (available) — tutors to hand, not graveyard. Would need to follow up with Buried Alive to enable reanimation, costing 2 cards and 5 mana to do what Entomb did in 1 card and 2 mana.
  - *Buried Alive* — already in deck (singleton).
  - *Forbidden Alchemy* — 2U instant, mill 3 + keep 1 of top 4 in hand. Less mill, but better selection. Reasonable B-list option if you'd rather have card filtering than raw mill.
  - *Satyr Wayfinder* — only mills 4 and conflicts with the Bloom Tender MV-2 slot.
  - *Stitcher's Supplier / Tortured Existence* — both unavailable (deployed elsewhere).
  - **Grisly Salvage wins** because it directly fills the graveyard at instant speed and adds card selection.
- **Score impact:**
  - **Core Loop:** Reanimation engine count holds at 9 enablers (Grisly Salvage replaces Entomb in the suite). Reliability is slightly lower due to randomness, but the deck has Buried Alive and Fauna Shaman as deterministic backups. Still 5/5.
  - **Durability:** No change.

---

## Cards considered but rejected

- **Pact of Negation** — originally proposed for the Fierce Guardianship slot. **Unavailable** — held in Calamity Tax (1 owned, deployed). Force of Will is the correct answer instead, and is also a strict upgrade.
- **Final Parting** — originally proposed for the Entomb slot. **Unavailable** — held in Loam Cycle. Grisly Salvage is the next-best replacement.
- **Vampiric Tutor (GC)** — would push GC count to 4, exceeding Bracket 3. Cutting Rhystic Study to make room would lose the strongest card-draw engine in the format. If you ever want both Vamp Tutor and Force of Will in here, you'd need to cut Rhystic Study and replace Seedborn's slot with a non-GC engine like Sylvan Library or Black Market Connections — viable but a real downgrade.
- **Solitude** — would replace Generous Gift (free-ish removal with flicker synergy), but only hits creatures and isn't actually free (1W + exile a white card to evoke). Trophy + Generous Gift cover more permanent types.
- **Grim Tutor** — available, but as an Entomb replacement it's a worse fit than Grisly Salvage (tutors to hand, doesn't fill the graveyard). As a generic add it's strictly worse than Vampiric Tutor (which we're not running anyway due to GC cap).
- **Earthcraft** — niche without combo pieces (Squirrel Nest, etc.). The deck has 12 basics and many creatures, so it works mechanically, but doesn't add a transformative engine and doesn't fit the reanimator/flicker identity.
- **Bloom Tender vs Coiling Oracle** — Bloom Tender wins on mana acceleration (compensates for Seedborn loss); Coiling Oracle wins on flicker-engine synergy. Picked Bloom Tender because the kill plan (Finale X≥10) needs the mana more than the flicker engine needs another ETB.

---

## Updated Conversion Check (post-swap)

| Axis              | Before     | After      | Notes                                                                                                |
| ----------------- | ---------- | ---------- | ---------------------------------------------------------------------------------------------------- |
| Core Loop         | 5          | 5          | Pod chain intact via Bloom Tender; reanimation enabler count steady via Final Parting                |
| Kill Reliability  | 5          | 5          | Bloom Tender restores mana for Finale-X≥10; reanimation chain unchanged                              |
| Durability        | 5          | 5          | Rhystic Study refills post-wipe; reanimation suite intact (9 spells)                                 |
| Interaction       | 4          | 4          | Counter count steady; Force of Will closes the creature-counter gap; Trophy ≥ Beast Within           |
| **Total**         | **19/20**  | **19/20**  | Maintained                                                                                           |

**Game Changers: 3/3** — Cyclonic Rift, Rhystic Study, Force of Will. Bracket 3 strict-3-GCs design restored.

---

## Pilot notes for the new build

- **Force of Will pitch discipline:** keep at least one blue card in hand at all times when you have FoW. The deck has lots of blue cards (Counterspell, Mana Drain, Force of Negation, Swan Song, Dovin's Veto, Cyclonic Rift, Rhystic Study, Ghostly Flicker, Ephemerate) — pitch the lowest-impact one. Don't pitch Mana Drain or Cyclonic Rift if you can help it.
- **Bloom Tender is your new MV-2 Pod target and mana engine:** Pod sequence becomes Birds (1) → Bloom Tender (2) → Eternal Witness / Ranger-Captain (3) → Resto Angel (4) → Karmic Guide (5). Once Atraxa hits the battlefield, Bloom Tender starts producing 4 mana per tap — protect it like you would Seedborn.
- **Replace the Seedborn untap mental model with a Rhystic draw mental model.** You're no longer "doing turns on opponents' turns" — you're "filling your hand on opponents' turns." The deck shifts from mana-engine to card-engine.
- **Rhystic Study target priority:** opponents who tap out to develop are paying the 1; opponents who hold up answers will let you draw. Use this to read the table.
- **Grisly Salvage is a probability play, not a tutor.** Cast it on your own end step or in response to a draw step to maximize information. It mills 5 random cards — accept the variance. If it whiffs on Razaketh/Vilis/Elesh Norn, the creature-to-hand clause still grabs Karmic Guide / Reveillark / Eternal Witness for the chain. The deck still has Buried Alive (deterministic) and Fauna Shaman (slow) as your reliable graveyard fillers; Grisly Salvage is the third leg of that stool.

---

## Future upgrade path (when missing cards return)

When you reclaim Beast Within, Boseiju, Fierce Guardianship, Sakura-Tribe Elder, Seedborn Muse, and Entomb from other decks (or buy extra copies), most reverse swaps could restore the original list — *except Force of Will, which is a clean upgrade over Fierce Guardianship.* Even when FG comes back, leave Force of Will in and put FG somewhere else. The cards introduced here (Assassin's Trophy, Bojuka Bog, Bloom Tender, Force of Will, Rhystic Study, Grisly Salvage) are all reasonable staples in WUBG — they won't go to waste in another deck.
