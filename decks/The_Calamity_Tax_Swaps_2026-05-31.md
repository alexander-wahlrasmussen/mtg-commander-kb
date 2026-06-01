# Glarb, Calamity's Augur — Pod-Targeted Swaps (2026-05-31)

**Deck:** The Calamity Tax (`calamity-tax-20260405-061741.txt`)
**Trigger:** 2026-05-30 pod session — recurring archenemy wins T6–7 with Ur-Dragon + Hidetsugu / Kairi / Kenrith / Kinnan-creatures behind Grand Abolisher. See `project_pod_combo_opponent.md`.
**Goal:** Lift the deck from **18/20 (5/4/4/5)** to **19/20** by raising Kill Reliability and shifting interaction toward Abolisher-resilient, blue-meta-targeted pressure — without adding a 4th Game Changer.
**Net:** 5-for-5. Stays at 100 cards. No GC change (holds 3/3: Seedborn Muse, Fierce Guardianship, Demonic Tutor).
**Axis:** Oppressive + faster close, ~4:1 over raw speed. See reasoning below — the deck is *ramp-saturated*, so generic acceleration floods; only front-loaded mana earns a slot.

---

## Summary table

| Out | In | Role gained | Owned? |
|---|---|---|---|
| Savvy Trader | **Exsanguinate** | 2nd X-drain finisher; Kill Reliability 4→5 | ⚠️ in own sideboard; both physical copies in Loam + Genome — buy 3rd (~$5) or pull |
| Flash Photography | **Sheoldred, the Apocalypse** | Abolisher-proof static drain; blue-meta hoser; 4/5 deathtouch wall | ✅ spare owned (2nd copy in Dark Lord's Army) |
| Druid of Purification | **Mystic Remora** | Abolisher-proof tax on their spell-dense turns + card draw | ⚠️ single copy in Replication Crisis — buy 2nd (~$2–5) or pull |
| High Fae Trickster | **Bloom Tender** | Front-loaded acceleration (3 mana off a T2 body in BUG) | ⚠️ both copies in Radiation Sickness + Grand Design — buy 3rd (~$8–15) or pull |
| Starfield Vocalist | **Carpet of Flowers** | Anti-blue ramp (pod-specific flex slot) | ✅ spare owned (2nd copy in Grand Design) |

Prices unverified per [[verify-prices]] — confirm on Cardmarket before buying. All adds are non-GC (verified against `REF_Game_Changers_List.md`), so the deck stays at 3/3.

---

## Why this axis (and not raw speed)

The deck runs **39 lands + ~20 ramp pieces** (12 land tutors, Lotus Cobra, Nissa, Exploration, Azusa, Oracle, Icetill, Coffers, Lumra, Tortoise, Sol Ring). It does **not** have a mana-quantity problem — it has a *timing* problem (engine-online ~T7 vs a T6–7 opponent) and an Abolisher problem.

Consequence: adding generic mana rocks (Signets, Talismans) just floods an already-saturated curve — the marginal 3rd/4th rock is a near-dead draw. Only **front-loaded** acceleration moves the online-turn, and only one card clears that bar universally: **Bloom Tender** (T2 body that taps for {B}{G}{U}). Carpet of Flowers is the meta-specific second (great vs this blue table, blank vs non-blue). Past those two, every remaining slot is worth more spent on the deck's genuinely under-served axes: Kill Reliability (sat at 4) and Abolisher-resilient interaction. Hence ~4 oppression : 1 speed, not a 50/50 hybrid.

**The one scenario this build is wrong:** if the pod games were never close on the clock — they combo through dead interaction regardless of your turn — then Bloom Tender buys nothing and slots 4–5 should both go to oppression/resilience. That hinges on a read only the pilot has.

---

## Why the 3/3 GCs stay put

- **Seedborn Muse** — the entire "hold interaction up on every opponent's turn" thesis. Untaps Glarb + all lands each opponent's untap; without it the deck is a once-per-turn engine.
- **Fierce Guardianship** — the only free counter. Dead during an Abolisher turn, but covers everything cast outside it.
- **Demonic Tutor** — finds whichever finisher (now Torment *or* Exsanguinate) the board calls for. Redundant finishers + an unrestricted tutor is the core of the Kill Reliability bump.

The cleanest oppressive draw-taxers — Narset, Notion Thief, Consecrated Sphinx, Rhystic Study — are **all Game Changers**, so they're locked out under the cap. The oppression here is built from the non-GC tier on purpose.

---

## Per-card rationale

### 1. Savvy Trader → Exsanguinate

- **Out:** value creature; loots/recurs but serves no kill line (the summary's own stated cut candidate on the Path to 19).
- **In:** {X}{B}{B} sorcery — each opponent loses X, you gain that much total.
- **Why:** the deck's primary kill (Torment of Hailfire) is a single point of failure for the closing plan. A second X-drain doubles the odds of drawing *a* finisher and gives Demonic Tutor a choice: Torment to strip boards/hands, Exsanguinate for pure reach. Glarb casts it from the top at X≥2. This is the single highest-leverage add — Kill Reliability 4→5.
- **Note:** already sits in this deck's sideboard, so it's an intended inclusion; the constraint is physical (both owned copies are in Loam and Genome).

### 2. Flash Photography → Sheoldred, the Apocalypse

- **Out:** {3} copy-a-permanent (flashback 6). Weakest of five copy effects — single copy, no board-state requirement met early.
- **In:** {2}{B}{B}, 4/5 deathtouch. "Whenever an opponent draws a card, they lose 2 life."
- **Why:** the drain is a **static ability**, so it keeps ticking *through* a Grand Abolisher turn — it's interaction the lock can't switch off. It taxes exactly what the Kairi/Kinnan card-spew chains do, and the 4/5 deathtouch body walls Ur-Dragon and combat. Blue-meta hoser in a blue-heavy pod.

### 3. Druid of Purification → Mystic Remora

- **Out:** {3}{G}{G} ETB where *each* player removes an artifact/enchantment — symmetric and slow; helps opponents as often as you.
- **In:** {U} enchantment, cumulative upkeep {1}. "Whenever an opponent casts a noncreature spell, you may draw a card unless they pay {4}."
- **Why:** against a spell-dense combo pod this is brutal — every cheap noncreature spell in their chain either taxes them {4} or draws you a card, and it works *during their turn* (triggered, survives Abolisher). On T1–3 off a single {U} it commonly nets 3–5 cards before you let it lapse. Proactive disruption that doubles as card advantage.

### 4. High Fae Trickster → Bloom Tender

- **Out:** flash enabler — but the deck keeps **Valley Floodcaller AND Alchemist's Refuge**, so flash redundancy is untouched.
- **In:** {1}{G} 1/1 Elf Druid. {T}: add one mana of each color among permanents you control — with Glarb (BUG) out, that's 3 mana from a 2-drop.
- **Why:** the only accelerant that beats flooding in a 39-land deck. Turn-2 Tender → turn-3 you're a full turn ahead on the Coffers/Torment clock, and unlike a rock it scales with the board and isn't a dead late draw.

### 5. Starfield Vocalist → Carpet of Flowers

- **Out:** ETB-doubler — win-more once the deck leans on X-drains over copy kills.
- **In:** {G} enchantment — each main phase, add X mana of one color where X = Islands an opponent controls.
- **Why (flex slot):** the pod is blue-heavy (Kinnan, Kairi, Ur-Dragon), so this taxes their Islands into 2–4 of your mana per turn — front-loaded acceleration that's *also* meta-punishing. The honest caveat: it's a blank against a non-blue table. This is the most swappable slot; a 4th oppression piece goes here instead if the meta shifts.

---

## What didn't make the cut and why

- **Generic mana rocks (Signets, Talismans, Fellwar, Coalition Relic)** — all owned, but they flood a ramp-saturated deck and don't ride Glarb's MV4+ top-cast or trigger landfall. Net-negative includes.
- **Narset / Notion Thief / Consecrated Sphinx / Rhystic Study** — the best oppressive taxers, but all Game Changers. Would break the 3/3 cap.
- **Submerge (kept)** — free interaction vs the green decks' Forests; survives as a window answer. Retained over a 5th cut.
- **Cursed Totem / Linvala-type lockdowns** — shut off Glarb's own surveil tap. Self-damaging.
- **Pithing Needle / Tormod's Crypt** — viable Abolisher-proof permanents, but the oppression package addresses the matchup more proactively. Hold as future tech if the build still loses to graveyard combo.

---

## Updated Conversion Check: 18/20 → 19/20 (5/5/4/5)

| Axis | Before | After | Notes |
|---|---|---|---|
| Core Loop | 5/5 | 5/5 | Bloom Tender/Carpet accelerate; cut flash enabler is fully redundant |
| Kill Reliability | 4/5 | **5/5** | 2nd X-drain (Exsanguinate) + Demonic Tutor choice; no longer single-points on Torment |
| Durability | 4/5 | 4/5 | Unchanged; Sheoldred adds a deathtouch wall but finisher pool still exile-vulnerable |
| Interaction | 5/5 | 5/5 | Same score, **better quality vs this pod** — Sheoldred + Remora survive Abolisher; cut the symmetric Druid |

---

## Pilot notes (cost-free, biggest single impact)

1. **Don't tap out.** Seedborn Muse is the whole point — hold counters up on their turns while developing via Glarb top-casts. Tapping out to durdle is how you die to T6 Abolisher-into-combo.
2. **Hold Otawara in hand, not on the battlefield.** Its channel ({2}{U} with Glarb out) is a *land* ability that survives Abolisher — your only stack-relevant answer on the lock turn. It bounces Abolisher itself or the combo creature. A played-out Otawara is useless here.
3. **Spend interaction in the windows, not on the lock turn.** If they cast Abolisher a turn early, that's your opening — counter/bounce/kill it on your turn or an end step, when your counters still work.
4. **Land Mystic Remora early and let it lapse.** T1–3 it taxes/draws hardest; pay cumulative upkeep only while the card flow justifies it.
5. **Don't telegraph the Torment/Exsanguinate turn.** A visible 12+ land count with Coffers signals the kill — manage threat perception.

---

## Shopping list

| Card | Status | Price (unverified) |
|---|---|---|
| Sheoldred, the Apocalypse | Owned spare (2nd in Dark Lord's Army) | $0 |
| Carpet of Flowers | Owned spare (2nd in Grand Design) | $0 |
| Exsanguinate | Buy 3rd or pull from Loam/Genome | ~$5 |
| Mystic Remora | Buy 2nd or pull from Replication Crisis | ~$2–5 |
| Bloom Tender | Buy 3rd or pull from Radiation Sickness/Grand Design | ~$8–15 |
| **Total (buy route)** | | **~$15–25** |

Verify on Cardmarket per [[verify-prices]]. If pulling instead of buying, none of the donor decks (Loam, Genome, Radiation, Grand Design, Replication Crisis, Dark Lord's Army) were in the 2026-05-30 pod rotation — pilot's call which to raid.

---

## Changelog

- **2026-05-31:** Companion swap file created in response to 2026-05-30 pod session. Axis chosen = oppressive + faster close (~4:1 over raw speed) after the user pushed on hybrid-vs-focused reasoning; conclusion held because the deck is ramp-saturated (only front-loaded acceleration earns a slot) while Kill Reliability (4) and Abolisher-resilient interaction were under-served. All five adds card-text-verified via `card_lookup.py`; GC status checked against `REF_Game_Changers_List.md` (all non-GC). Cross-deck availability checked via `moxfield_haves_2026-05-14-0631Z.csv` + grep of `decks/*.txt`: Sheoldred/Carpet have owned spares; Exsanguinate/Bloom Tender/Mystic Remora are deployed elsewhere and require a buy or a pull.
