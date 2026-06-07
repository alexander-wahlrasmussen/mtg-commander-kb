# Analysis: External Witherbloom, the Balancer Build vs. Our Proposal

**What this is:** a Conversion Check + `deck_sim.py` evaluation of an external 100-card *Witherbloom, the Balancer* build the user supplied for comparison against our own `PROP_Witherbloom_the_Balancer.md`. Same commander, different combo route.

**Date:** 2026-06-07
**Card text verified** against local Scryfall data (`card_lookup.py`). Loops, GC count, and legality checked programmatically — not pattern-matched.

> Not a build proposal. This is a scouting/comparison document. The deck is **not** on our roster and is **not** subject to our 3-GC house cap (it is a Bracket-4 list).

---

## The external deck at a glance

- **100 cards, legal, no duplicates, ~35 lands.** (An earlier paste mixed in the maybeboard — that combined pile was 275 cards with 2 illegal dupes and 11 GCs. Those are maybeboard artifacts; the *mainboard* is clean.)
- **6 Game Changers** → **Bracket 4** (double our house cap): Ad Nauseam, Demonic Tutor, Natural Order, Opposition Agent, Orcish Bowmasters, Vampiric Tutor. (Tooth and Nail *was* a GC; delisted Oct 2025, no longer counts.)
- **Archetype:** BG Saproling/tokens go-wide + aristocrat drain, with the kill **powered by the commander's affinity**.

---

## The engine (verified loops)

Witherbloom's *"instants and sorceries you cast have affinity for creatures"* floors the buyback token/recursion spells to a single colored pip on a wide board. A mana-producing sac outlet refunds that pip, and a drain payoff closes the loop.

**Loop A — token-maker + Mirkwood Bats.** Sprout Swarm (`{4}{G}` w/ buyback → `{G}` at 4 creatures) makes a Saproling → Mirkwood Bats: each opp loses 1. Sac the Saproling to Phyrexian Altar → `{G}` → Mirkwood Bats again: opp loses 1. Recast for `{G}`. Mana-neutral, ~2 drain/cycle → infinite. Lab Rats does the same in black.

**Loop B — Corpse Dance + an aristocrat.** Corpse Dance (`{4}{B}` w/ buyback → `{B}`) reanimates the top creature of the yard → sac it to Phyrexian Altar for `{B}` → Blood Artist / Zulaport / Marionette: opp loses 1 → creature is back on top of the yard → recast for `{B}`. Infinite drain.

**Redundancy:** loop-starters {Sprout Swarm, Lab Rats, Corpse Dance} × mana sac outlets {Phyrexian Altar, Warren Soultrader} × payoffs {Mirkwood Bats, Blood Artist, Zulaport, Marionette}.

**Two structural weaknesses, both confirmed by the sim:**
1. **Commander-dependent.** Kill Witherbloom and every loop-starter snaps back to `{4}{X}`; one Phyrexian Altar activation can't refund that. The commander-*independent* enablers (Earthcraft, Cryptolith Rite, Enduring Vitality, the four token doublers, Ashnod's Altar) are all in the **maybeboard**.
2. **Phyrexian Altar is a soft single point.** It is the only mainboard free sac outlet that *makes mana*. Warren Soultrader backs it up (costs 1 life/loop), and only the 4 unrestricted tutors can fetch the artifact.

**Plan B (commander-independent):** Finale of Devastation for X≥10 = team +X/+X + haste overrun. Protean Hulk / entwined Tooth and Nail currently have **no win-pile in the main** (no Hulk-combo creatures, no Craterhoof) — they fetch value, not a kill. Those slots are underperforming until given a target.

---

## Conversion Check — 15/20 (4 / 4 / 3 / 4)

> Corrects an earlier off-the-cuff "16–18" estimate. On a full pass it lands at 15; Durability is what pulls it down.

| Axis | Score | Rationale |
|---|---|---|
| **Core Loop** | **4** | ~19 cards serve the affinity-drain loop; redundant starters/outlets/payoffs + 8 token makers + 11 dorks. Clear identity. Not 5: loop is commander-dependent, and a non-integrated Hulk/T&N/big-green-spell package dilutes it. |
| **Kill Reliability** | **4** | Two independent lines — infinite affinity-drain loop (instant once online) and Finale X≥10 overrun (needs neither commander-affinity nor the Altar). At least one fast; combo turn protectable (Dosan, Veil, free Deadly Rollick). Not 5: the primary leans on a commander + sac-outlet chokepoint. |
| **Durability** | **3** | Deep redundancy in token makers/dorks/draw, rebuilds in 2–3 turns, and a commander-independent Plan B. But the *primary* loop is commander-dependent (8-MV recast tax) and the mana-sac-outlet redundancy is thin (sim: 23%→14% at T6 without Warren). Fails the "commander is an accelerant, not a dependency" bar for 4. |
| **Interaction** | **4** | ~10 pieces, mechanism-diverse (removal: Trophy, Beast Within, free Deadly Rollick, Lethal Scheme, Pile On, Alpha Deathclaw; stax/hate: Dosan, Opposition Agent; protection: Veil, Sylvan Safekeeper; disruption: Dauthi, Bowmasters). Instant-speed, *not* monotype — survives Grand Abolisher better than a counter wall. Not 5: <12 pieces, mostly single-target, no maindeck wipe. |

**Read:** 13–16 band — "solid foundation with at least one exploitable weakness." The weakness is **Durability/commander-dependence**.

**Kill window:** Goldfish **T5–6** (commander ~T4–5 on dork ramp; combo assembles T5–6). Through interaction **T7–9** (commander removal sets the primary plan back a full recast).

---

## deck_sim.py results

Driven through the canonical `scripts/deck_sim.py` engine (40k trials, seed 12345). Mana/colour are **land-base floors** — the 11 dorks are excluded, so real mana is higher; the 8-MV commander is the true gate. Combo assembly is a **card-availability ceiling** (ignores mana, board, and the commander being in play).

**Consistency (land base only):**

| turn | 2 | 3 | 4 | 5 | 6 | 8 | 10 |
|---|---|---|---|---|---|---|---|
| avg lands | 2.0 | 2.8 | 3.5 | 4.1 | 4.5 | 5.3 | 6.0 |
| all colours (land) | 52% | 68% | 77% | 82% | 85% | 90% | 93% |
| has a play | 98% | 100% | 100% | 100% | 100% | 100% | 100% |

Keepable opening hand: **98.8%**. BG fixing is a non-issue; dorks push the real colour/mana floor well above these numbers.

**Combo assembly — [1 of L] + [1 of S] + [1 of P]:**

| turn | 2 | 3 | 4 | 5 | 6 | 8 | 10 |
|---|---|---|---|---|---|---|---|
| pieces drawn (no tutors) | 1% | 1% | 1% | 2% | 2% | 3% | 5% |
| with tutors | 8% | 11% | 15% | **19%** | **23%** | 32% | 42% |
| *sensitivity: Warren gone (Altar only)* | 4% | 6% | 8% | 11% | **14%** | 20% | 26% |

Tutor model respects card type: only the 4 unrestricted tutors (Vampiric, Demonic, Beseech, Increasing Ambition) can fetch the noncreature loop-starters and the Phyrexian Altar; the 4 creature-tutors (Chord, Nature's Rhythm, Finale, Tooth and Nail) can grab Warren or a payoff. GSZ/Natural Order are green-only and can't fetch the black combo pieces, so they don't count as combo tutors here. The model **undercounts** real assembly because it ignores the deck's heavy draw/dig (Ad Nauseam, Rishkar's Expertise, Return of the Wildspeaker, etc.).

---

## Head-to-head vs. `PROP_Witherbloom_the_Balancer`

Proposal combo modeled with the same engine (deck not built): single Exquisite Blood + (Vito | Sanguine Bond) + abundant trigger, 4 broad tutors.

| | External build (measured) | Our proposal (modeled) |
|---|---|---|
| Bracket | **Bracket 4** (6 GC) | Bracket-3 legal / bracket-4-*in-spirit* (3-GC cap) |
| Kill | 3-piece affinity loop, **commander-dependent** | **2-card** Blood + Vito, commander-*independent* |
| Combo assembly w/ tutors **T6** | **23%** | 18% |
| same **T10** | **42%** | 29% |
| Plan B | Finale X≥10 overrun (independent) | affinity-storm, Razaketh→Mikaeus+Ballista, Necrotic Ooze |
| Combo-turn protection | **Stronger** (Dosan, Veil, Dauthi, Sylvan Safekeeper, Opposition Agent) | Weaker (Veil + Heroic, no counters) |
| Conversion Check | **15/20** (4/4/3/4) | projected 18–19/20 |

**Verdict.** As built they are genuine peers, and the external build is "more" by bracket (6 GC vs our hard 3) with a faster dork base and better combo-turn protection. Its combo also **assembles more reliably** (deeper redundancy: 3×2×4 piece combinations vs the proposal's single-Exquisite-Blood bottleneck — 23% vs 18% at T6, 42% vs 29% at T10). But on two axes the proposal is tighter: its kill is a **2-card** combo and it **survives commander removal**, where the external build folds if Witherbloom or Phyrexian Altar is answered — which is exactly why the proposal projects higher on the Conversion Check (18–19 vs 15) despite the external build's raw bracket edge.

**The real ceiling is latent in the maybeboard.** Pull Earthcraft + a token doubler + Cryptolith Rite/Enduring Vitality + Ashnod's Altar into the main and the loops become commander-independent and redundant; the waiting GCs (Gaea's Cradle, Necropotence, Survival, Imperial Seal, Biorhythm) push the count toward 9–11. That version (true cEDH-adjacent) leaves a 3-GC-capped build behind decisively. As currently mainboarded, it does not.

---

## Pod fit (vs. our [[project_pod_combo_opponent]])

Favourable-to-even: out-powers the Bracket-3 roster, races the pod's T6–7 window, and its removal works on its own turn under Grand Abolisher (Dosan-style soft lock + free Deadly Rollick). Main risk is being the table's archenemy at Bracket 4 and losing the commander-dependent loop to focused removal.

---

## Method caveats

- `deck_sim.py` is a consistency simulator, **not** a rules engine. Mana/colour figures are land-only floors; combo assembly ignores mana, board state, and whether the commander is in play.
- The proposal numbers are a **structural model** of its combo (the deck is not built), not a measurement of a real list.
- Conversion Check is a structural estimate from the decklist, not playtest data.

Related: [[witherbloom-balancer-proposal]] · `PROP_Witherbloom_the_Balancer.md`
