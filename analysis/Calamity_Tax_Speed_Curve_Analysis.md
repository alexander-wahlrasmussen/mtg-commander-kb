# The Calamity Tax — Speed-Curve Analysis: Original vs. 31-May vs. 01-June

**What this is:** the same before/after rigor we ran on Lightning War (`Lightning_War_Speed_Curve_Analysis.md`) and the Witherbloom builds, turned on **Glarb, Calamity's Augur**. It tests whether the two proposed swap rounds actually make the deck *kill sooner* — or whether they make it more *reliable / oppressive* without moving the clock.

**Date:** 2026-06-08
**Card text verified** against local Scryfall data (`card_lookup.py`) for the commander, both X-drains, Bloom Tender, Carpet, Witherbloom, Dellian Fel, Sheoldred, Mystic Remora — not pattern-matched.
**Variants measured** (built programmatically from the committed list so the only differences are the swapped cards):
- **V1 — original:** `decks/calamity-tax-20260405-061741.txt` (the committed deck)
- **V2 — 31-May swap:** `The_Calamity_Tax_Swaps_2026-05-31.md` (−Savvy Trader, −Flash Photography, −Druid of Purification, −High Fae Trickster, −Starfield Vocalist; +Exsanguinate, +Sheoldred, +Mystic Remora, +Bloom Tender, +Carpet of Flowers)
- **V3 — 01-June swap:** `The_Calamity_Tax_Swaps_2026-06-01.md` (V2 minus Carpet, minus Archon of Cruelty; +Witherbloom the Balancer, +Professor Dellian Fel — Carpet's slot goes to Dellian)

Both run through the canonical `scripts/deck_sim.py` engine (40k trials, seed 12345) plus grouped-availability models the stock fixed-piece sim can't express.

> **Bottom line up front:** **No — the deck has not been sped up.** The 31-May swap made it more *consistent at having a closer* (a second X-drain roughly **doubles** finisher availability, 11%→22% by T6) and more *oppressive/resilient* (Sheoldred, Remora) — which is exactly what that doc set out to do (it was ~4:1 oppression over speed by its own framing). But the **kill turn did not move**: the land curve is byte-for-byte identical across all three variants, only one *board-conditional* mana dork (Bloom Tender) was added to a ramp-saturated deck, and the binding constraint — **lethal-X mana** — is untouched. The 01-June variant adds the project's only genuine speed lever (Witherbloom's affinity cost-reduction on every X-spell) but it is MV8, board-conditional, sim-invisible, and it **weakens the deck's actual *fastest* kill** by cutting Archon. The reliable kill is still "Cabal Coffers online + a finisher," ~T7–9, before and after.

---

## Why this deck is different from Lightning War

Lightning War's kill is a finisher cast **behind a free commander** — the gate was *having the card*, so finisher availability *was* the speed curve. **Calamity Tax's kill is mana-gated.** Both primary finishers (Torment of Hailfire, Exsanguinate) are single-card X-drains that do nothing until you have ~15–25 mana to pump X. So for this deck "speed" is two separate questions the sim must answer separately:

1. **Do we *have* a closer sooner?** (finisher availability — what the 31-May swap targeted)
2. **Can we *pay* for a lethal closer sooner?** (the mana curve to a lethal X — the part that actually gates the kill)

The swaps moved (1). They did almost nothing to (2).

---

## 1. Setup / land curve — identical across all three

None of the swaps touch a single land, and the sim confirms the obvious: the three columns are the same deck on every land-based metric.

| metric (land base only) | V1 original | V2 31-May | V3 01-June |
|---|---|---|---|
| Keepable opening hand | 99.5% | 99.5% | 99.5% |
| Avg lands in play — T4 / T6 | 3.6 / 4.8 | 3.6 / 4.8 | 3.6 / 4.8 |
| All colours from lands — T4 / T6 | 32% / 48% | 31% / 46% | 31% / 47% |
| "Has a play" — T3 | 94% | 97% | 96% |

The only flicker is "has a play" at T3 (94%→96–97%): the V2/V3 adds (Mystic Remora {U}, Carpet {G}, Bloom Tender {1}{G}) are cheaper than the cards they replace, so a castable early play appears slightly more often. That is a *castability* nudge, not a *kill-speed* one. **The mana curve to the kill is unchanged.**

---

## 2. Finisher availability — the real (and only sizable) improvement

`deck_sim.py` grouped model. "Drawn" = X-drain seen by natural draw; "+Demonic" treats Demonic Tutor as a wildcard that can fetch one. Ignores mana — a **card-availability ceiling**, read next to §3.

| ≥1 X-drain in hand by turn | T2 | T4 | **T6** | T8 | T10 |
|---|---|---|---|---|---|
| **V1** — Torment only, drawn | 7% | 9% | **11%** | 13% | 15% |
| **V1** — Torment only, +Demonic | 15% | 18% | **22%** | 26% | 29% |
| **V2 / V3** — Torment **or** Exsanguinate, drawn | 14% | 18% | **22%** | 25% | 29% |
| **V2 / V3** — +Demonic | 21% | 26% | **31–32%** | 36% | 40% |

**This is the one axis the swaps genuinely improved.** Adding Exsanguinate as a second copy of "a 1-of-99 X-drain" roughly **doubles** the natural-draw odds (11%→22% by T6) and lifts the tutored line 22%→31%. That is the Kill Reliability 4→5 the 31-May doc claimed, and the sim backs it.

**But read what it is and isn't.** This is *availability*, not a kill turn. The deck was already ~22% to have *a* finisher in hand by T6 once you count Demonic Tutor; the swap moves "have a closer" from decent to good. It does **not** move when that closer becomes *lethal*, because that is a mana question (§3). V3 ≈ V2 here — Exsanguinate is retained in both.

---

## 3. The part the sim ignores — lethal-X mana (the actual gate)

"X-drain in hand" ≠ "table is dead." Both finishers are `{X}{B}{B}`; lethal X against a 3-opponent, 40-life pod:

- **Exsanguinate** — pure life loss, X to *each* opponent. A clean from-full table kill is **X=40 → 42 mana**. Realistic use is reach/finishing a chipped table (X=15 → 17 mana to close opponents already near 15). No board-strip; just damage.
- **Torment of Hailfire** — each of X iterations is "lose 3 **or** sac a nonland **or** discard." Opponents *dodge* life loss with chaff, so the worst-case lethal X against healthy boards is high (~X=20+ for a true one-shot), but it simultaneously **strips every board and hand**, and opponents routinely take life over sacrificing key permanents — so X=12–15 is usually crippling-to-lethal in practice. (The Summary's "X=12 = table kill" is optimistic but directionally right as "back-breaking.")

Either way the kill turn is **"Cabal Coffers + Urborg + ~12 lands online,"** which one tap turns into ~12–20 black mana. The Summary already pegs that at **T7–9**, and **nothing in V2 or V3 moves it earlier:**

- **Bloom Tender (V2/V3) is board-conditional, not front-loaded.** Its Vivid taps for "one mana of each color *among permanents you control*" — and **lands are colorless**. A T2 Bloom Tender with only lands out produces *nothing*; it needs Glarb (3 mana, so T3+ at the earliest) or another colored permanent already down. So it is not the T2→T3 jump the swap doc implied; it comes online about when the deck's other ramp does. The grouped model shows the marginal effect: P(≥1 of a 6-card front-loaded accelerant set in hand) rises only **+5 points** when Bloom Tender is added (T2 39%→44%, T6 54%→59%) — a small bump from a 7th dork into a deck already drowning in ramp.
- **Witherbloom, the Balancer (V3) is the project's only structural mana-threshold lever** — and it's conditional. *"Instant and sorcery spells you cast have affinity for creatures"* reduces the **generic** part of every X-spell by your creature count. Torment/Exsanguinate are `{X}{B}{B}`, so affinity-N lets you cast effective-X=K for `{K−N}{B}{B}`. With a realistic mid-game **6 creatures**, a "lethal-feel" Torment of X≈18 costs **14 mana instead of 20** — roughly one turn earlier. The swap doc's "X=20 for ~4 mana" needs **12+ creatures**, which this creature-light lands deck rarely fields. So Witherbloom is real acceleration, but (a) she's MV8, (b) she's board-conditional, and (c) the sim can't see her — she does not show up in any column above.

**Net: the gate is mana, the swaps barely touched mana, so the kill turn barely moved.**

---

## 4. The swaps neglected — and V3 *weakened* — the deck's actual fastest kill

The X-drains are the **slow** kill (15–25 mana). The deck's **fast** kill is the copy/reanimator line: a kicked **Rite of Replication** (or **Doppelgang**) on **Kokusho** = five legends die to the legend rule = **25 damage per opponent** for ~**10 mana** (Reanimate Kokusho for {B} from the surveil-fed yard, kicked Rite for 9). That closes 2–4 turns before a lethal Torment.

Grouped model, "copy spell **and** a death-drain creature together in hand" (creature tutors GSZ/Chord/Finale + Demonic as wildcards, since Glarb mills the creature):

| copy-kill assembled by turn | T4 | **T6** | T8 | T10 |
|---|---|---|---|---|
| **V1** — drawn / +tutors | 4% / 19% | **6% / 25%** | 9% / 33% | 11% / 40% |
| **V2** — drawn / +tutors | 4% / 19% | **7% / 26%** | 9% / 33% | 11% / 40% |
| **V3** — drawn / +tutors | 3% / 16% | **4% / 22%** | 6% / 28% | 8% / 35% |

(The canonical `sim_profiles.json` entry models the strict 2-piece Rite+Kokusho version: ~15% +tutors by T6, 24% by T10 — a tighter floor than the broad "any copy spell + any drainer" group above.)

**V1→V2 leaves this line flat. V3 *cuts* it** — removing Archon of Cruelty shrinks the death-drain creature pool from three to two (Kokusho, Gray Merchant), dropping copy-kill availability ~3 points across the board, and **Witherbloom is a poor backfill** (she's one big flyer, not a copy-the-death-trigger body). So the 01-June swap, judged purely on *speed*, trades the deck's fastest kill line down for an 8-mana conditional cost-reducer.

---

## 5. Kill window — before vs after

| | V1 original | V2 31-May | V3 01-June |
|---|---|---|---|
| Reliable kill turn (Coffers + finisher) | **T7–9** | **T7–9** | **T7–9** (faster *only* if Witherbloom + a creature board are live) |
| ≥1 X-drain available by T6 (+Demonic) | 22% | **31%** | 32% |
| Fast copy-kill available by T6 (+tutors) | 25% | 26% | **22%** ↓ |
| Front-loaded accelerant by T2 | 39% | 44% | 43% |
| What actually changed | baseline | **+reliability, +oppression** (Sheoldred/Remora/Exsanguinate); kill turn unchanged | as V2, **+conditional mana-threshold cut** (Witherbloom), **−fast-kill** (Archon) |

---

## Verdict

**The deck got more reliable and more oppressive, not faster.** The 31-May swap did exactly what it said — second X-drain doubles finisher availability (Kill Reliability 4→5, confirmed), and Sheoldred/Mystic Remora are Abolisher-proof pressure — but it was a **~4:1 oppression-over-speed** swap by its own admission, and the sim confirms the speed component is marginal: identical land curve, one board-conditional dork, untouched lethal-X mana. The 01-June swap's Witherbloom is the only true acceleration in the whole project, but it's conditional and sim-invisible, and it costs the deck its fastest kill (Archon → copy-kill pool).

So if the goal was "stop losing the race to the T6–7 combo pod," **these swaps don't deliver it** — they make you better at grinding and at *eventually* closing, on the same T7–9 clock you already had.

---

## What we can actually do about it (if the goal is a faster kill turn)

The binding constraint is **lethal-X mana**, and the deck is ramp-*saturated* — so "add more ramp" mostly floods (the 31-May doc's own correct conclusion). The levers that move the *kill turn* rather than the *ramp count*:

1. **Lean into the copy/reanimator fast-kill — it is the deck's real early kill and the swaps neglected it.** Kokusho + kicked Rite is lethal at ~10 mana, board-independent, 3–4 turns ahead of a lethal Torment, but only ~25% available with tutors by T6 — under-supported. Cheapest upgrades: a graveyard enabler so the line doesn't wait on Glarb's surveil to bin Kokusho (**Entomb** / **Buried Alive** / **Jarad's Orders**), and/or a second reanimation spell. And for speed specifically, **don't cut Archon** (the V3 trade). This raises a *low-mana, board-independent* kill — the only kind that's genuinely "faster."

2. **If you keep Witherbloom (V3), make her pay off — add cheap creatures.** Her affinity only accelerates if you have bodies; this is a creature-light lands deck, so mid-game she often reduces cost by only 4–6. Either commit to enough cheap creatures that affinity is real, or accept she's an 8-mana 5/5 that does little the turn she lands.

3. **For *speed*, Carpet of Flowers > Dellian Fel against this blue pod.** Carpet is a T1 {G} enchantment that taps their Islands for 2–4 unconditional mana every turn — genuinely front-loaded acceleration vs Kinnan/Kairi/Ur-Dragon. The 01-June doc picked Dellian Fel for *universal value*; that's the right call for grind, the wrong one for *clock*. If the read is "we are losing the race," Carpet earns the slot back.

4. **The literal speed button the deck already owns: Nyxbloom Ancient (maybeboard).** Tripling mana turns a T6 Coffers tap into the lethal-X turn a full turn early. It's flagged "win-more," but it is the single most direct "kill sooner" card in the BUG pool and it sidesteps the ramp-saturation objection (it's a multiplier, not another source).

5. **The honest structural point.** An X-drain ramp deck is an inherently slow closer — its kill is gated on a big-mana turn no amount of finisher redundancy front-loads. If "win the race" is the real goal (per the [[bracket-4-in-spirit]] / [[pod-combo-opponent]] thread), the faster identity is the **reanimator/copy kill emphasized over the X-drains**, not a fourth way to find Torment. That's a build-direction call, not a swap.

---

## Method caveats

- `deck_sim.py` is a **consistency** simulator, not a rules engine. Mana/colour are land-only floors; availability % ignore mana, the board, and whether Coffers/Witherbloom are online.
- The "front-loaded accelerant" group is a defined 6-card set (Sol Ring, Lotus Cobra, Exploration, Farseek, Nature's Lore, Three Visits) + Bloom Tender for V2/V3 — a proxy for "an early mana play exists," not a mana total.
- The copy-kill grouped model treats GSZ/Chord/Finale/Demonic as generic wildcards; the creature tutors really *can* fetch the drainer and Demonic either half, so it's a fair-to-slightly-optimistic ceiling. The canonical `sim_profiles.json` Rite+Kokusho entry is the stricter floor.
- Lethal-X and "T7–9" are structural estimates and card-text math, not playtest data. Conversion Check scores (18→19) are unchanged by this analysis — it measures *speed*, which the Conversion Check doesn't isolate.

Related: `The_Calamity_Tax_Summary.md` · `The_Calamity_Tax_Swaps_2026-05-31.md` · `The_Calamity_Tax_Swaps_2026-06-01.md` · `Lightning_War_Speed_Curve_Analysis.md` · [[project_deck_sim_and_matchup_matrix]] · [[2026-05-31-pod-swaps]]
