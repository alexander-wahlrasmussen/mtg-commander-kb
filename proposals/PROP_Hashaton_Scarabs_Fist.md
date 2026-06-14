# Proposal: Hashaton, Scarab's Fist

Status: **not built** (candidate). The original "Esper discard value" framing below is **superseded by the 2026-06-14 cEDH reframe + clock benchmark** in the addendum directly under this line.
Drafted: 2026-05-02. Revised 2026-05-03 — v1 was authored without local Scryfall data and rested on hallucinated commander text. Re-verified card text and rebuilt from scratch.

---

## 2026-06-14 — cEDH reframe + clock benchmark (the real engine)

User asked whether Hashaton's structure/engine is sound and to benchmark it vs the bake-off finalists. Scouted its actual cEDH presence (Moxfield/EDHREC/playingmtg) and **card_lookup-verified every piece** (Hashaton = the canonical hallucination card — text held this time). Finding: the competitive deck is **not the "fair value grind" framed below** — it's a **Thassa's Oracle + Demonic Consultation / Tainted Pact combo deck**, with Hashaton as a tutor/dig/resilience engine. Verified Hashaton-native lines:

- **Discard Thassa's Oracle → pay `{2}{U}` → 4/4 copy → ETB wins** on an empty library (devotion is irrelevant once library = 0). A counter-dodging way to deploy the win.
- **Discard Razaketh → copy → sac 4/4 Zombie tokens → tutor anything** (repeatable; tokens are Hashaton's own output).
- **Discard Hullbreaker Horror → copy for `{2}{U}`** (its cast-trigger bounce works while tapped) **+ a mana rock → infinite mana.**
- Free discard outlets: Tireless Tribe / Putrid Imp / Ghostly Pilferer / Skirge Familiar. **Beseech the Mirror** bargains a token → free-casts Consult/Oracle (MV ≤ 4).

**Benchmark** (`scripts/hsh_clock_lab.py` on the 3-GC-legal modelling list `decks/considering/hashaton-thoracle-20260614.txt` — GCs = Thassa's Oracle + Demonic Tutor + Vampiric Tutor; seed 20260612 / 20k, the same harness + seed as the bake-off, so the clocks are directly comparable):

| Deck | decap median | table median | by T7 (decap) | never-12 |
|---|---|---|---|---|
| **Hashaton (Thoracle)** | **T6** | **T6** (= decap) | **71%** | 9% |
| Yuriko (Insider Trading) | T7 | T8 | 57% | 7 / 9% |
| Kefka-burn (Forced Liquidation) | T8 | T9 | 35% | 4 / 11% |

**Verdict: the structure/engine is SOUND.** On the goldfish Hashaton is the **fastest of the three**, and decap = table (a Thoracle win ends the game for everyone at once, unlike the others' focus-fire combat tables). It out-assembles Yuriko's combo because it is a *dedicated* Thoracle deck (8 tutors + dig + the token-tutor engine) where Yuriko hedges into a ninja axis.

**Caveats (load-bearing):** (1) the goldfish **cannot score protection/resilience** — the exact blind spot that ranked faster Godo *below* Yuriko in the bake-off — so "fastest combo" ≠ "best deck"; (2) it's the **same wincon as the to-be-built Yuriko** and needs the **same Thoracle/Consult pod approval** (a redundant 2nd Thoracle deck?); (3) true cEDH wants 8–15 GCs — this is the 3-GC-legal floor. **Outlet variants** (looter/wheel/hybrid, `hsh_clock_lab.py --mode variants`): all median **T6 within ~2pp** — the discard-outlet flavour is a non-lever; the closer (Thoracle) is what moves the clock.

**Delay lab — resilience (`delay_lab.py`, 2026-06-14):** Hashaton **out-disrupts Yuriko at every Abolisher level** — their-T7 P(disrupt) ≈ **56/67%** (drawn/+tutors) at realistic P(Abolisher)≈0.25, vs Yuriko's **43/57%** — because the no-ninja-tax list runs a deeper suite (10 counters / 6 instant removal / 3 preempt + 8 tutors that double as answer-finders). **But it shares Yuriko's 0-static gap:** both collapse under a fully-resolved Abolisher (a=1: Hashaton 17%, Yuriko 8%), where **Kefka-burn's 1 static holds (23–33%) and stays the Abolisher-proof fallback.** The lab measures *disrupt-the-pod* only; Hashaton's *protect-own* resilience (counter-dodging discard-deploy of Thoracle, Razaketh recursion, redundant oracles) is additional and unmeasured — though so is Yuriko's genuinely independent second (combat) axis, which Hashaton lacks.

**Net verdict: on the measured axes (clock T6 vs T7–8 *and* disruption) Hashaton ≥ Yuriko — arguably the better Thoracle build — but the two are redundant** (same Thoracle wincon, same 6th-combo pod approval, same Abolisher weakness). It's build-*one*, not both; Hashaton has the stronger claim, Yuriko the more independent backup plan, Kefka the Abolisher resilience. *(Legality fix during the build: the modelling list had illegally run Veil of Summer — mono-green, not Esper — now Drown in the Loch.)*

*(Everything below is the pre-reframe "fair value" proposal, retained as the record.)*

---

## Commander

**Hashaton, Scarab's Fist** (UB). `{W}{B}`, Legendary Creature — Zombie Wizard, 1/3.

> Whenever you discard a creature card, you may pay `{2}{U}`. If you do, create a tapped token that's a copy of that card, except it's a 4/4 black Zombie.

**Color identity: WUB (Esper).** Despite a `{W}{B}` mana cost, the `{2}{U}` activation cost puts blue in identity. This is *not* a Dimir deck.

Owned: 3 copies (DRC, foil).

---

## Archetype framing

**Discard-trigger ETB-cheat engine.** The trigger is *you discard a creature card*; the payoff is a tapped 4/4 token copy of that card with all its other abilities. Implications:

- **Bodies don't matter.** The token is always 4/4. Cheating in Emrakul or Blightsteel as a 4/4 is wasted. Stat-based fatties are off-axis.
- **ETBs and static abilities are the entire point.** Targets are creatures whose value lives in *what they do when they enter or sit on the board*, not how big they are.
- **Token enters tapped.** ETB triggers fire fine, but attack/tap-trigger payoffs (e.g., Sheoldred, the Apocalypse's drain on combat damage; Sphinx of the Second Sun's combat trigger) are delayed a turn.
- **The engine wants creatures *in hand*, not in the graveyard.** Buried Alive / Entomb don't directly enable Hashaton. They support a *secondary* reanimation line. Primary fuel is tutors-to-hand + draw + wheels.
- **Discard outlets are the central infrastructure.** Self-discard creatures, looters, rummagers, wheels. This is the real construction puzzle.
- **Mana-intensive.** Each activation costs `{2}{U}` on top of however you discarded. Ramp matters more than in a typical reanimator shell.
- **Classic reanimation (Reanimate, Animate Dead, Necromancy) does *not* trigger Hashaton.** Useful as a parallel cheat-in line off the same yard fill, not as Hashaton synergy.

Right archetype label: *Esper discard-engine ETB-copy reanimator.*

---

## Distinctiveness check

Per `REF_Bracket_3_House_Rules.md`, archetype overlap with the existing roster is grounds for rejection. The roster has no other Esper deck, so the check runs against thematically adjacent decks regardless of color:

- **Curse of the Scarab (The Scarab God, Dimir).** Different lane. Scarab God is mill → pay-mana → tribal aggro with scry payoffs. Hashaton is discard → pay-mana → ETB-copy engine. Different play patterns despite both being "Dimir-coded zombie tokens."
- **Crystal Sickness (Golbez, Dimir).** Both end up with a big creature on board from a graveyard / yard-fill loop. But Golbez's engine is *Buried Alive → Animate*. Hashaton's engine is *tutor-to-hand → discard outlet → pay {2}{U}*. The construction is fundamentally different and white opens lanes Golbez can't touch.
- **Diminishing Returns (Teysa Karlov, Orzhov).** Both produce token bodies in WB. Teysa's tokens come from death triggers and Orzhov aristocrats; Hashaton's tokens come from discard activations. No real overlap.

**Verdict:** distinct. The Esper identity and discard-trigger engine give it clear daylight from anything currently in the roster. Easier distinctiveness story than the v1 framing claimed.

---

## Power ceiling from collection

**Likely 17+/20 elite range.** Owned staples that map onto this deck (verified before locking — quick spot list):

- **Discard outlets (Esper-legal):** Putrid Imp, Bone Miser (also a payoff), Liliana of the Veil, Forgotten Creation. *Need to inventory more — discard outlets are the construction bottleneck.*
- **Wheels / mass discard:** Windfall, Whispering Madness, Notion Thief (turn opponents' wheels into pure draw + their discards trigger Waste Not lines).
- **Tutors / draw:** Demonic Tutor, Vampiric Tutor, Mystical Tutor, Necropotence, Bolas's Citadel, Rhystic Study, Mystic Remora, Opposition Agent, Compulsive Research.
- **Removal / interaction:** Toxic Deluge, Cyclonic Rift, Force of Will, Mana Drain, Yawgmoth's Will. White additions: Swords to Plowshares, Path to Exile, Generous Gift, Anguished Unmaking, Teferi's Protection.
- **ETB-stacked targets to copy:** Sepulchral Primordial (verified — ETB pulls one creature card from each opponent's graveyard, even on the tapped token), Massacre Wurm, Grave Titan, Consecrated Sphinx (verified — opponent-draw trigger fires regardless of tapped), Sheoldred (both versions), Sphinx of the Second Sun, Agent of Treachery.
- **Reset / wrath:** Living Death (multiple).
- **Yard-fill (secondary reanimation line, not Hashaton trigger):** Buried Alive, Entomb, Victimize, Persist.

**Cuts from v1 list:**

- **Liliana, Dreadhorde General** — planeswalker, not a creature card. Cannot trigger Hashaton's discard ability and cannot be copied.
- **Faithless Looting / Wheel of Fortune / Anje Falkenrath / Magus of the Wheel / Cathartic Reunion / Burning Inquiry** — out of color identity (red). Esper has fewer cheap discard outlets than Rakdos; this is a real constraint.

**Caveat unchanged:** most of these staples are at zero surplus across the existing roster. Building Hashaton physical means cannibalizing 1–2 elite decks every play session. Proxy build is cheap; physical sleeve-up has real logistics cost.

---

## Construction direction (if/when built)

- **Discard outlet density is the central puzzle.** Need redundant ways to put a creature card from hand into the graveyard at instant speed or as a low-mana cost. Esper has fewer cheap looters than Rakdos — expect to lean on Putrid Imp, Liliana of the Veil, Forgotten Creation, and pricier options.
- **Tutor-to-hand bias.** Vampiric Tutor / Demonic Tutor / Mystical Tutor / Enlightened Tutor put the right creature in hand to discard. Yard-tutors (Entomb, Buried Alive) feed the secondary reanimation line, not Hashaton.
- **Ramp matters more than typical.** Each Hashaton activation is `{2}{U}` on top of the discard cost. Mox Diamond, Mana Crypt, Sol Ring, Talisman of Dominance, Talisman of Progress, Talisman of Hierarchy, Smothering Tithe (now in color), Esper Sentinel.
- **Wheel package as a bonus engine.** Windfall + Notion Thief + Bone Miser + Waste Not = wheels become draw, mana, tokens, and Hashaton triggers in parallel. Note Waste Not triggers only on opponent discards — symbiotic with wheels, not with Hashaton's own discards.
- **ETB-copy targets prioritized over fatties.** Value engines (Consecrated Sphinx, Grave Titan, Sepulchral Primordial, Agent of Treachery), not voltron threats.
- **Classic reanimation as a secondary line.** Reanimate / Animate Dead / Necromancy are still good cards in the shell — they just don't synergize with Hashaton specifically. Treat as parallel cheat-in.
- **Token-tapped timing awareness.** Build with the assumption that copies are tapped on entry. ETB payoffs are unaffected; combat-trigger payoffs lose a turn.

---

## Open questions for future build session

- **Game Changer slots: which 3?** Esper-legal candidates from owned pool — Cyclonic Rift, Mana Drain, Necropotence, Opposition Agent, Bolas's Citadel, Vampiric Tutor, Demonic Tutor, Force of Will, Yawgmoth's Will, Smothering Tithe. Cap is 3 hard. Verify against `REF_Game_Changers_List.md` at build time.
- **Discard outlet inventory.** Audit owned Esper-legal discard outlets specifically. This is the real build constraint and the most likely shopping-list driver.
- **Roster decision.** Both decks at 100% physical means a swap, not an addition. No obvious retire candidate — Esper distinctiveness is clean, so the question is purely "do we want a 17th elite slot or replace a Solid-tier deck."
- **Proxy-only path.** If kept as proxy build, no roster decision needed — but then it competes with the existing 35-card proxy backlog noted in `Deck_Index.md`.
- **Verify all candidate cards before locking.** This proposal lists cards directionally; every card going into the actual `.txt` decklist must be re-verified per `CLAUDE.md` hard rules.
