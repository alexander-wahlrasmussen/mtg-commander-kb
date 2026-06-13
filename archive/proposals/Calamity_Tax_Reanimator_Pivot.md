# The Calamity Tax — Reanimator Lean (build-direction proposal)

**Deck:** The Calamity Tax (`decks/calamity-tax-20260405-061741.txt`), Glarb, Calamity's Augur — Sultai (BUG)
**Date:** 2026-06-08
**Trigger:** The speed-curve analysis (`Calamity_Tax_Speed_Curve_Analysis.md`) showed the 31-May/01-June swaps made the deck more *reliable + oppressive* but **did not move the kill turn** — the X-drain kill is mana-gated at ~T7–9 and nothing front-loaded it. User asked whether to change build direction toward the deck's *fast* kill (the copy/reanimator line), and whether the cards exist — especially with **The Loam Cycle being dismantled** (Craterhoof → Grand Design), freeing its BUG graveyard package.
**Card text verified** via `card_lookup.py` for every add and the new cut (Mirrorform); GC status checked against `REF_Game_Changers_List.md`; ownership checked against `collection/moxfield_haves_2026-06-07-1031Z.csv` and `grep decks/*.txt`.

> **Recommendation: lean, don't pivot.** Add a focused reanimator/copy package as a **second, faster, board-independent kill axis**, keep the X-drains (incl. the cheap 2nd one, Exsanguinate) as the resilient backbone. This is the only change in the whole project that actually moves the realized kill **earlier** (fast line is ~10 mana vs ~15–25), and the sim confirms it lifts fast-kill availability **33% → 42% by T6 (49% → 59% by T10)** while leaving the X-drain backbone untouched. **Zero buy** — all six adds come from the Loam teardown + CT's own sideboard.

---

## The decision this answers

| | Stick with X-drain (V1/V2) | **Reanimator lean (V4 — proposed)** |
|---|---|---|
| Primary kill | X-drain (Torment/Exsanguinate), mana-gated ~15–25 mana | **Two axes:** fast reanimator ~10 mana **+** X-drain backup |
| Realized kill turn | T7–9 (Coffers online) | **T5–6 fast line** / T7–9 backup |
| Board/yard dependence | none (resilient) | fast line needs the yard (hedged by Scarab God) |
| Vs the Abolisher combo pod | out-grind (V2 adds Sheoldred/Remora) | **out-race** (no new oppression) |
| Cost | ~$15–25 (V2) | **$0** (Loam teardown + CT sideboard) |

The reanimator lean trades the 31-May oppression adds (Sheoldred/Mystic Remora/Bloom/Carpet) for *speed*. It keeps Exsanguinate — the one 31-May add that strengthens the **kept** X-drain axis and is essentially free.

---

## The swap (6-for-6, stays 100, GCs untouched 3/3)

| Out | In | Role gained | Source (owned) |
|---|---|---|---|
| Savvy Trader | **Exsanguinate** | 2nd X-drain (keeps the resilient backbone strong) | Loam frees 1 (also CT SB); 2 owned, 1 in Genome |
| Flash Photography | **The Scarab God** | **Resilient** reanimator payoff — eats *any* yard, recurs itself on death | CT SB / Loam frees the spare (2 owned; **1 is the Curse of the Scarab commander — do not pull that one**) |
| Starfield Vocalist | **Final Parting** | The enabler — bins Kokusho to yard **and** grabs Reanimate/Rite in one card | Loam (1 owned) |
| High Fae Trickster | **Jarad, Golgari Lich Lord** | Sac outlet + combo finisher | Loam (2 owned) |
| Druid of Purification | **Lord of Extinction** | Combo finisher (Jarad sac = 20–40/opp) + sac fodder | Loam (2 owned) |
| Mirrorform | **Victimize** | Cheap 2-for-1 reanimation | Loam frees 1 (5 owned) |

GCs unchanged: Seedborn Muse, Fierce Guardianship, Demonic Tutor (3/3). All six adds verified **non-GC**.

**Do NOT pull these from Loam** (Game Changers — CT is capped): Crop Rotation, Field of the Dead. (Fierce Guardianship is the GC you already share.) *Tooth and Nail is **not** a GC — it was removed from the list 2025-10-21 — so it's a legal pull, just not part of this package.*

---

## The two kill axes after the lean

Both are now live and roughly co-equal in availability by T6 — but they fail to *different* hate, which is the point.

**Axis 1 — Fast reanimator (the new speed):** get a death-drainer onto the battlefield cheaply, then multiply or sac it.
- **Reanimate (1 mana) → Kokusho on battlefield → kicked Rite of Replication (9) = 25/opp.** ~10 mana, board-independent, lands ~T5–6.
- **Final Parting** sets it up in one card: bin Kokusho to the yard, put Reanimate (or Rite) in hand.
- **The Scarab God** is the resilient version — it exiles creatures from *any* graveyard (so it works even after your own yard is hated, feeding off opponents'), drains on upkeep per Zombie, and **returns to hand when it dies** instead of being answered.

**Axis 2 — Explosive combo (the ceiling):** **Jarad + Lord of Extinction.** Sacrifice Lord (power = all cards in all graveyards, realistically 20–40 in this deck) to Jarad's `{1}{B}{G}` ability → each opponent loses that much = table kill from two cards. Finite (bracket-3-legal), board-independent once both are down.

**Axis 3 — Resilient backbone (unchanged):** Torment of Hailfire + Exsanguinate, mana-gated, immune to board/yard hate. The insurance when Axis 1/2 get hated out.

### Sim — fast-kill availability (40k trials, seed 12345)

`deck_sim.py` grouped model: "a copy/reanimation spell **and** a death-drainer available by turn T," creature tutors + Demonic + Final Parting as wildcards. Card-availability ceiling — ignores mana, but also a **conservative floor for this deck** because it counts the drainer only when *drawn to hand*; in reality Glarb's surveil, Stitcher's-type mill, and Final Parting put it in the **yard**, which is where the reanimation line wants it.

| availability by turn | T2 | T4 | **T6** | T8 | T10 |
|---|---|---|---|---|---|
| X-drain finisher, +Demonic — **V1** | 15% | 18% | **22%** | 26% | 29% |
| X-drain finisher, +Demonic — **V2 / V4** | 21% | 27% | **31%** | 36% | 41% |
| Reanimator fast-kill, +tutors — **V1 / V2** | 17% | 25% | **33%** | 41% | 49% |
| **Reanimator fast-kill, +tutors — V4** | 22% | 32% | **42%** | 51% | **59%** |
| Jarad + Lord combo, +tutors — **V4** | 9% | 13% | **19%** | 25% | 30% |

**Read:** V4 keeps the X-drain line exactly where V2 put it (31% by T6 — Exsanguinate retained), and **adds ~9 points of fast-kill availability on top** (33%→42% by T6, 49%→59% by T10) plus a 19%-by-T6 explosive backup. The deck now has *two* independent ways to be holding a kill by T6, one of which costs half the mana and lands a turn or two sooner. The setup curve is unchanged (keepable 99.5%, colours/has-a-play within noise) — the swaps are all nonland-for-nonland.

---

## Card-text catches (verified, and they matter)

- **Unmarked Grave can't fetch Kokusho** — it searches for a *nonlegendary* card only. Use **Final Parting** (no restriction) as the Kokusho-to-yard tutor. (This is why Final Parting, not the cheaper Unmarked Grave, is in the build.)
- **Jarad + Lord is finite, not infinite** — one big drain, bracket-3-legal. It *is* a 2-card combo (bracket-4-in-spirit, which you've okayed).
- **Living Death (a bench option) is symmetric** — it refills opponents' yards too; only run it if you want a board-reset finish, not as default reanimation.
- **The Scarab God eats opponents' graveyards** — it's the one reanimator payoff that survives your *own* yard being hated, and a soft answer to the pod's recursion. It's the resilience anchor of the package.

---

## Why these six cuts

The five non-Mirrorform cuts are the deck's universally-agreed weakest cards — the *same five* the 31-May oppression swap cut, so this is a clean A/B (same cuts, reanimator adds instead of oppression adds):
- **Savvy Trader** — value creature, serves no kill line (the Summary's own stated cut).
- **Flash Photography** — weakest of five copy effects (single copy, needs a board).
- **Starfield Vocalist** — win-more ETB doubler.
- **High Fae Trickster** — redundant flash enabler (Valley Floodcaller + Alchemist's Refuge remain).
- **Druid of Purification** — symmetric, slow; helps opponents as often as you.
- **Mirrorform** (new 6th cut) — `{4}{U}{U}` instant copy. Redundant with kicked Rite for the Kokusho line and needs an existing board; the dedicated reanimation package replaces it. Espers to Magicite is **kept** (graveyard hate vs the pod's recursion). *Alternative:* if you'd rather keep all copy effects, cut a marginal ramp piece instead (e.g. Sowing Mycospawn) — the deck is ramp-saturated and the fast line needs less mana, so a ramp trim is defensible.

The X-drain backbone, all ramp, and the other copy effects (Rite, Doppelgang, Espers) stay intact — this deepens an existing sub-theme, it doesn't gut the engine.

---

## The honest trade vs the 31-May oppression build

This is genuinely either/or for the flex slots:

- **V4 gives up the Abolisher-resilient oppression** (Sheoldred's static drain, Mystic Remora's spell-tax) that V2 added. Against the specific "combo behind Grand Abolisher" problem, V4's plan is **out-race**, not **out-grind**.
- **V4 raises graveyard-hate exposure.** The fast line folds to Rest in Peace / Leyline of the Void / a timely Bojuka Bog. Mitigations: The Scarab God (eats any yard), the X-drain backbone (yard-independent), and the deck's existing Force of Vigor / Boseiju / Veil of Summer to answer the hate piece.

Per [[bracket-4-in-spirit]] (close games, race the pod), out-racing is the on-identity choice — but if the read is "they combo through dead interaction regardless of our clock," the V2 oppression package is the better answer and this lean is wrong. That's a pilot/meta read.

---

## Conversion Check: 18/20 → 19/20 (5/**5**/4/5)

| Axis | Before | After | Notes |
|---|---|---|---|
| Core Loop | 5/5 | 5/5 | Unchanged; Final Parting/Scarab feed the same engine |
| **Kill Reliability** | 4/5 | **5/5** | **Two independent kill axes** (fast reanimator ~10 mana **+** redundant X-drain), better-earned than V2's X-drain-only redundancy — the fast axis is 42% available by T6 and lands earlier |
| Durability | 4/5 | 4/5 | Holds; **but** graveyard-hate is now a bigger swing (more yard-dependent) — Scarab God + the X-drain backbone hedge it |
| Interaction | 5/5 | 5/5 | 19 pieces (lost Druid of Purification); 3 free counters + 4 free removal intact. **Quality note:** unlike V2 this adds **no** Abolisher-resilient oppression |

Not 20: still no deterministic 1-card kill, and the fast axis is exile-vulnerable. Same cap as every prior version.

---

## Bench / deeper-pivot options (all owned, from Loam or CT sideboard)

If the lean tests well and you want to push further (each competes for ramp/interaction slots):
- **Dread Return** (Loam) — reanimation with a sac-3 flashback that pairs with token/legend deaths.
- **Stitcher's Supplier** (Loam) — `{B}` mill-3 on ETB/death; cheap yard velocity + sac fodder for Jarad.
- **Vein Ripper** (CT SB) — 6/5 flyer, drains 2 on *any* creature death; payoff for the legend-rule/sac lines.
- **Sidisi, Brood Tyrant** (Loam) — self-mill + Zombie tokens (the tokens also feed Scarab God's drain).
- **Coiling Rebirth / Breach the Multiverse** (CT SB) — owned reanimation already in the maybeboard.
- **Meren of Clan Nel Toth** (Loam) — a full recursion engine if you want the grind-reanimator identity.

---

## Ownership / shopping — **$0**

All six adds are owned and free once Loam is dismantled. Two are tight:
- **The Scarab God** — you own **2**; one is the **Curse of the Scarab commander (locked)**, the other is the Loam/CT-sideboard copy that frees up. Exactly one spare — don't raid the Curse deck.
- **Exsanguinate** — you own **2**; one is in Genome Project, the other frees from Loam. One spare.
- Victimize (5 owned), Jarad (2), Lord of Extinction (2), Final Parting (1, only in Loam) — all clear.

No Cardmarket purchase required. (Optional future tech: **Entomb**, the 1-mana yard tutor, ~€3–5 — not owned, not needed given Final Parting + Glarb surveil.)

---

## Pilot notes

1. **Surveil is your Entomb.** Use Glarb's `{T}: Surveil 2` to bin Kokusho/a fatty into the yard for Reanimate — you usually don't need to draw the drainer, which is why the 42% sim figure understates the real line.
2. **Lead with Scarab God into a hated table.** If you see graveyard hate, Scarab is the payoff that still works (eats their yards) and dodges spot removal (returns to hand on death).
3. **Hold the X-drain as the closer they can't interact with.** If they pack the yard hate, you still have Torment/Exsanguinate off the Coffers turn — don't over-commit the graveyard plan into obvious hate.
4. **Jarad line: sac in response to exile.** If Lord (or Kokusho) is about to be exiled, sac it to Jarap first — you keep the drain.
5. **Don't telegraph.** Same as the X-drain build — a stocked yard + Reanimate up reads as a kill; manage threat perception.

---

## If applied to the `.txt`

Per CLAUDE.md: bump the dated filename (`calamity-tax-<today>.txt`), archive the old list to `archive/old_decklists/`, recount to 100, and **update `scripts/sim_profiles.json`** — the canonical `calamity-tax` profile currently models the committed V1 Rite+Kokusho line; after the lean it should add the reanimation enablers (Reanimate/Victimize/Scarab) and Final Parting as a tutor, and optionally a second combo entry for Jarad+Lord. Not applied yet — this is a proposal.

---

## Changelog

- **2026-06-08:** Created in response to the speed-curve finding + the user's build-direction question and the Loam Cycle teardown. Six adds card-text-verified via `card_lookup.py`; GC status checked (all non-GC, 3/3 holds); cross-deck availability + owned counts checked against `moxfield_haves_2026-06-07-1031Z.csv` (zero-buy; Scarab/Exsanguinate each have exactly one free spare). Fast-kill curve measured via a throwaway `deck_sim.py` wrapper (40k, seed 12345), then deleted. Companion to `Calamity_Tax_Speed_Curve_Analysis.md`, `The_Calamity_Tax_Swaps_2026-05-31.md`, `The_Calamity_Tax_Swaps_2026-06-01.md`.
