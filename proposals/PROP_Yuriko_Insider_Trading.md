# Proposal: "Insider Trading" — Yuriko, the Tiger's Shadow (Dimir Ninja Tempo + Consultation Finish)

Status: **proposal — not built.** Drafted 2026-06-11 on a clean-sheet brief: brand-new deck
(not a shelf proposal), reliable T6–7 finish, beats the pod combo opponent, bracket-4 in
spirit, hard 3-GC cap. Donor restrictions: no cards from Lightning War, Calamity Tax
(post-swap), Grand Design (post-swap), Genome Project, Zero Sum Game.

All card texts quoted below verified via `python scripts/card_lookup.py` on 2026-06-11
(Yuriko, Thassa's Oracle, Demonic Consultation, Tainted Pact, Jace Wielder of Mysteries,
Laboratory Maniac, Emet-Selch and the other commander candidates). GC statuses checked
against `REF_Game_Changers_List.md` (Feb 2026, incl. the Removed section).

---

## Commander

**Yuriko, the Tiger's Shadow** — `{1}{U}{B}`, 1/3 Legendary Creature — Human Ninja. **Owned, undeployed, free.**

> Commander ninjutsu {U}{B} ({U}{B}, Return an unblocked attacker you control to hand: Put
> this card onto the battlefield from your hand or the command zone tapped and attacking.)
> Whenever a Ninja you control deals combat damage to a player, reveal the top card of your
> library and put that card into your hand. Each opponent loses life equal to that card's
> mana value.

**The load-bearing fact: Yuriko was REMOVED from the Game Changers list on 2025-10-21**
(`REF_Game_Changers_List.md` §Cards Removed). She costs **0 of 3 GC slots**. This is the
purest bracket-4-in-spirit, bracket-3-by-the-letter commander available — a card WotC
considered GC-grade five months ago, now legal for free.

---

## Why this architecture wins the brief

The lab series (8 decks, 2026-06-08 → 06-11) produced two empirical design rules:

1. **The only clock that held its claimed window was Genome Project's** — trigger-based,
   hits **each opponent**, so decap and table converge (decap T7 / table T8). Combat
   focus-fire decks diverge 2–3 turns (decap T7–9, table T10–12). **Yuriko's trigger is
   the GP architecture with bigger numbers**: every ninja connection drains all three
   opponents for the revealed card's mana value. Two connections a turn revealing MV 4–6
   off a stacked top = 8–12 to the whole table per turn cycle from ~T3–4.
2. **Zero-Sum Game (the tuned 2-card-combo deck) medians T9** because its combo costs
   8–13 mana to find-and-deploy. The cost structure is the clock. The cheapest legal
   table-kill is **Thassa's Oracle + Demonic Consultation: 3 total mana**, win on
   resolution, decap = table by definition.

This deck runs **both clocks independently**:

- **Clock A — the chip (T5–8 table, primary):** ninjas + unblockable 1-drops + top-of-library
  stacking. Abolisher-irrelevant (triggered ability), counterspell-resistant (the trigger
  isn't a spell), and Yuriko herself enters via **ninjutsu — an activated ability**: she can
  never be countered and never pays commander tax.
- **Clock B — the button (T4–6 when needed, closer):** Thassa's Oracle / Jace, Wielder of
  Mysteries / Laboratory Maniac + Demonic Consultation / Tainted Pact. Resolves on our
  turn; Grand Abolisher never gets a say. Against the pod's T6–7 combo, this is the
  pre-emptive strike — and the chip clock means we often don't even need it.

The two clocks share substrate: Consultation/Pact are *instants* (flashed end-of-turn),
the win-bodies are cheap blue creatures (devotion is trivial), and the top-stacking suite
(Brainstorm/Ponder/Scroll Rack/Sensei's Top/Lim-Dul's Vault) serves Yuriko reveals AND
combo assembly simultaneously. No dead halves.

**Why the pod combo deck specifically loses to this:**
- Their Abolisher locks our *spells on their turn* — it touches neither ninjutsu, nor the
  Yuriko trigger, nor a main-phase Thoracle.
- Their T6–7 goldfish is now racing a deck that has dealt 15–25 table damage by T6 AND
  holds a 3-mana instant-win behind Counterspell/Mana Drain backup.
- Our interaction (counters) is live on *every other player's* turn and on our own — the
  documented "counters blank on the lock turn" problem only applies to the Abolisher
  player's own combo turn, which we pre-empt by clock instead.

---

## Verified rules facts the design rests on

- **Thassa's Oracle** ETB: "If X [devotion to blue] is **greater than or equal to** the
  number of cards in your library, you win the game." Empty library: X=0 ≥ 0 — wins with
  zero devotion. Her own {U}{U} provides devotion 2 regardless.
- **Demonic Consultation** ({B}, instant): name a card not in the deck → exiles the entire
  library. Thoracle ETB after = win. No targets; nothing for opponents to respond to except
  the spells themselves.
- **Tainted Pact** ({1}{B}, instant): exiles until two cards **share a name** — the deck
  must be effectively true-singleton: **max 1 Island, 1 Swamp, 1 Snow-Covered Island,
  1 Snow-Covered Swamp**, everything else nonbasic. Collection supports this (see mana).
- **Jace, Wielder of Mysteries** / **Laboratory Maniac**: redundant win-bodies; both
  non-GC. Lab Man needs a draw after the exile (Frantic Search ×4 owned, free).
- **Yuriko reveal**: {X} in a revealed mana cost counts as 0; MDFC reveals use the front
  face value. Reveal goes to HAND (card advantage on every trigger).
- **Commander ninjutsu**: activation, not a cast — no tax accumulation, no counter window
  (ruling on card).

---

## Game Changer plan (3/3)

| Slot | Card | Status |
|---|---|---|
| 1 | **Thassa's Oracle** | GC (Win Conditions category). Buy ~€12 *(unverified)* |
| 2 | **Mystical Tutor** | GC. **Owned, undeployed — free.** Finds Consultation/Pact/counter at instant speed |
| 3 | **Demonic Tutor** | GC. All 3 physical copies deployed (1 locked in Calamity), proxy claimed by ZSG → **buy a copy** |

- Yuriko: **0 slots** (delisted Oct 2025). Mana Drain, Counterspell, Snapcaster, Scroll
  Rack, Sensei's Top, Lim-Dul's Vault, Commandeer: all confirmed non-GC.
- A/B candidate for the lab: swap Demonic Tutor → **Mana Vault** (2 free copies). Both the
  DR and ZSG labs found fast mana flat-to-worse vs tutors in combo shells; expected verdict
  is "keep Demonic," but this deck's combo is only 3 mana, so the lab should test it
  honestly. Force of Will (unowned, €€€) and Fierce Guardianship (1 physical copy,
  location ambiguous across 5 decks) considered and passed over.

---

## Construction skeleton (~100)

**Commander:** Yuriko (ninjutsu — she starts in the zone, not the 99).

| Package | ~Count | Cards (owned-free in **bold**) |
|---|---|---|
| Win-bodies | 3 | Thassa's Oracle (buy), Jace WoM (buy), **Laboratory Maniac** (owned ×2) |
| Library-exilers | 2 | Demonic Consultation (buy), Tainted Pact (buy) |
| Ninjas | 8–9 | Ingenious Infiltrator, Fallen Shinobi, Silver-Fur Master, Prosperous Thief, Moon-Circuit Hacker, Mistblade Shinobi, Sakashima's Student, Ninja of the Deep Hours, Thousand-Faced Shadow (all buy, ~€1–5 each) |
| Evasive enablers | 10–12 | Changeling Outcast, Slither Blade, Triton Shorestalker, Mist-Syndicate Naga, Spectral Sailor, Faerie Seer, Siren Stormtamer, Gingerbrute, Wingcrafter (buy, ~€0.5–2) + **Tetsuko Umezawa, Fugitive** (owned — makes the whole 1-power board unblockable) |
| Top-stack / dig | 8–9 | **Brainstorm, Ponder, Preordain** (owned spares), **Scroll Rack** (owned free), Sensei's Divining Top (owned — in Dark Lord's Army, donor call), Lim-Dul's Vault (buy), **Mystical Tutor** (GC), **Frantic Search** (owned) |
| Tutors | 3–4 | Demonic Tutor (GC, buy), Solve the Equation (buy — finds Consult/Pact/counters), **Merchant Scroll** (owned — finds Brainstorm/counters), Wishclaw Talisman (buy, optional) |
| Counters / protection | 8 | **Counterspell** (spare), **Mana Drain ×2** (spares — non-GC), **Swan Song** (spare), **Force of Negation** (spare, location check), **Commandeer** (owned free — pitch-cast AND an MV-7 reveal), Siren Stormtamer (above), 1–2 buys (e.g. An Offer You Can't Refuse) |
| Yuriko bombs (big-MV reveals that aren't dead cards) | 6–7 | **Commandeer** (7), **Agadeem's Awakening** (7, MDFC land — 2 owned, location check), Sea Gate Restoration (7, MDFC land, buy), Consuming Tides (6, buy), Curtains' Call (6, buy), Draco (16!, buy ~€2), Blinkmoth Infusion (14, buy ~€1) |
| Removal | 3–4 | **Go for the Throat** (owned), Bloodchief's Thirst-class cheap buys |
| Rocks | 4–5 | **Sol Ring, Arcane Signet, Dimir Signet, Talisman of Dominance** (all spares), **Lotus Petal** (spare check) |
| Lands | ~29–30 | **Underground Sea** (1 free), **Watery Grave / Sunken Hollow ×7 / Underground River / Drowned Catacomb / Morphic Pool / Mystic Sanctuary** (spares), 1 Island + 1 Swamp + 1 Snow-Covered each (Pact rule), **Evolving Wilds / Terramorphic / Fabled Passage** spares (shuffle away dead tops), low-curve deck = 29–30 lands |

Curve: ~1.8 avg MV outside the bomb slot. The bombs are the only cards above MV 4, and
five of seven are lands/free-spells/interaction on their face.

---

## Clock projection — *(unverified — lab required before any Summary claim)*

Structural estimate, NOT a citation: Clock A alone should resemble Genome Project's shape
(converging decap/table) with onset ~T4–5; Clock B alone is a 5–7 mana total assembly
(pieces + protection) with ~10 effective tutors/redundant copies — materially cheaper than
ZSG's 8–13 mana assembly that labbed at median T9. Target: **median table kill T7, with
meaningful T5–6 tails on either axis.** Per the verification rule this gets a dedicated
`yrk_clock_lab.py` (on `speed_lab_core.py`, modeling both clocks + the interaction between
them) BEFORE the decklist is finalized — if the lab says T8+, the proposal's premise is
falsified and we say so.

---

## Buy list (prices **unverified** — Cardmarket check at order time)

| Tier | Cards | Est. |
|---|---|---|
| Combo core (critical) | Thassa's Oracle ~€12, Demonic Consultation ~€8, Tainted Pact ~€25, Jace WoM ~€4, Lim-Dul's Vault ~€8, Solve the Equation ~€1 | ~€58 |
| GC tutor | Demonic Tutor (cheapest printing) | ~€25–40 |
| Ninja package (critical — it IS the strategy) | 9 ninjas + 9 enabler buys | ~€25–40 |
| Bombs | Sea Gate Restoration, Consuming Tides, Curtains' Call, Draco, Blinkmoth Infusion | ~€20 |
| Misc (removal, 1–2 counters, snow basics) | | ~€10 |
| **Total** | | **~€140–170** |

Heavier than ZSG's list because the tribal core is unowned — but every tier-1 card is
strategy-critical per the brief. Proxy-first remains an option for Tainted Pact and
Demonic Tutor (the two big tickets).

---

## Roster fit & politics

- **Mechanical distinctiveness:** no tempo, ninja, topdeck-matters, or library-exile deck
  exists in the roster. Closest neighbours (Curse of the Scarab: zombie reanimator;
  Crystal Sickness: artifact reanimator) share colors only. Clean pass.
- **Donor impact: near zero.** The build uses binder spares almost exclusively; the only
  donor calls are Sensei's Top (Dark Lord's Army) and the Agadeem's Awakening /
  Hullbreaker Horror location ambiguities (DeckSafe pass at build time). No GC leaves any
  deck.
- **Pod approval required (the big one):** Thoracle + Consultation is a 2-card instant win
  — this would be the roster's 6th 2-card exception request, and it's the most
  cEDH-coded line yet. Mitigations to offer the pod: it's the *backup* clock in a combat
  deck, the deck runs zero free counterspells and zero fast-mana GCs, and the chip clock
  is fully interactable (blockers, removal, wraths all work). If the pod declines,
  **Plan B: cut Thoracle/Consult/Pact/Jace for 4 more tempo pieces** — the deck stays a
  legitimate GP-architecture T6–8 table clock with Yuriko's delisted-GC power level, and
  the lab will quantify exactly what the combo is worth.
- ZSG overlap: none mechanically (lifeloop vs tempo); both want Demonic Tutor copies —
  both resolved by buying.

---

## Open questions for the build session

1. **Pod approval** for the Consultation line (or Plan B tempo-only).
2. **3rd-GC A/B** in the lab: Demonic Tutor vs Mana Vault (2 free).
3. **Bomb suite depth** — every bomb raises average reveal but is a mulligan risk; lab
   should sweep 4/6/8 bombs for the chip-clock optimum.
4. **Snow basics + Pact audit** — final list must be name-singleton; automate the check.
5. **Sensei's Top pull** from Dark Lord's Army vs buy (~€30 — pricey; Scroll Rack covers).
6. DeckSafe pass to locate Agadeem's Awakening ×2, Force of Negation, Hullbreaker Horror
   physical copies.
