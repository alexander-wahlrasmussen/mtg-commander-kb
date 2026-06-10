# The Grand Design — Speed-Curve Analysis: Pre-Swap vs. Post-Swap

**What this is:** the same before/after rigor we ran on Lightning War (`Lightning_War_Speed_Curve_Analysis.md`) and Calamity Tax (`Calamity_Tax_Speed_Curve_Analysis.md`), turned on **Atraxa, Grand Unifier (The Grand Design)**. It tests whether the **2026-05-02 6-for-6 replacement swaps** (`The_Grand_Design_Swaps_2026-05-02.md`) made the deck *kill sooner* and/or *more reliably* — or whether they only preserved the 19/20 while reshuffling which axis is strong.

**Date:** 2026-06-08
**Card text verified** against local Scryfall data (`card_lookup.py`) for every swapped card plus Finale, Defense of the Heart, Buried Alive, and the fat reanimation targets — not pattern-matched.
**Builds measured** (programmatically, so the only differences are the 6 swapped cards):
- **Pre-swap:** `archive/old_decklists/the-grand-design-20260402-100951.txt`
- **Post-swap (current):** `decks/the-grand-design-20260502.txt`

The 6-for-6 swap:

| OUT | IN |
|---|---|
| Beast Within | Assassin's Trophy |
| Boseiju, Who Endures | Bojuka Bog |
| Fierce Guardianship *(GC)* | **Force of Will** *(GC)* |
| Sakura-Tribe Elder | Bloom Tender |
| Seedborn Muse *(GC)* | Rhystic Study *(GC)* |
| Entomb | Grisly Salvage |

Both lists run through the canonical `scripts/deck_sim.py` engine (40k trials, seed 12345), plus grouped-availability and a reanimation-determinism model the stock fixed-piece sim can't express (`scripts/gd_speed_lab.py`).

> **Bottom line up front:** **No — the deck did not get faster, and "more reliable" is only half-true.** The land/mana curve is byte-for-byte identical (avg nonland CMC **2.983 → 2.983**, same 39 lands, same colour and keepable curves). The kill-line *availability* is essentially unchanged (same Finale, same Defense, same reanimation-piece counts). The swaps **genuinely improved interaction reliability and card-advantage reliability** — Force of Will now counters creatures and works without the commander, and Rhystic Study is a far more dependable engine than Seedborn — but they **measurably reduced reanimation reliability** (Entomb's deterministic bin → Grisly Salvage's ~15%-per-cast random bin) and shaved a hair off Finale-mana availability. This was a forced *substitution* to hold 19/20 under card-availability constraints, and on the speed/reliability axes it is a **reshape, not an upgrade**: +interaction coverage, +draw engine, −reanimation determinism, −one mana accelerant, ±0 speed.

---

## What the swaps were actually for

The swaps doc's own stated goal was **"6 cards physically unavailable... preserve the Conversion Check score of 19/20 and the Bracket-3 strict-3-GC design."** Speed and reliability were not the brief — this was a forced substitution because the originals were deployed in other decks. So the right question isn't "did the optimization work" but "did the forced subs incidentally help or hurt speed and reliability?" Answer below, axis by axis.

---

## 1. Setup / mana curve — identical (so: not faster)

The swaps touch one land (Boseiju → Bojuka Bog) and otherwise trade nonlands of equal cost. The sim confirms the curve does not move:

| metric (land base only) | Pre-swap | Post-swap |
|---|---|---|
| Keepable opening hand | 99.4% | 99.5% |
| Lands | 39 | 39 |
| **Avg nonland CMC** | **2.983** | **2.983** |
| Avg lands in play — T4 / T6 | 4 / 5 | 4 / 5 |
| All colours from lands — T4 / T6 | 22% / 39% | 22% / 39% |
| "Has a play" — T2 / T3+ | 91% / 100% | 92% / 100% |
| Creatures / instants / sorceries / enchantments | 20 / 20 / 11 / 5 | 19 / 20 / 11 / 6 |

> **Correction (2026-06-09):** the *level* of the all-colours row was a `deck_sim.py` model artifact — sac-fetches and rainbow lands (Command Tower, City of Brass, Exotic Orchard, Reflecting Pool) carry an empty `color_identity` and were scored as zero-colour sources. Under the corrected model both lists read **80% / 90%** (T4 / T6). The Pre = Post *equality* — the conclusion this table supports — is unaffected. See `Grand_Design_Mana_Fixing_Pass_2026-06-09.md`.

**Read:** the deck does not curve out faster, because nothing about the curve changed. The five swapped nonlands cost exactly as much as the five they replaced (the swap pairs net to identical total CMC), so average cost is unchanged to three decimals. The composition shifted by exactly one card (a creature → an enchantment: Seedborn/Sakura out as creatures, Bloom Tender in, Rhystic in), which is invisible at this resolution.

**The one land swap is a slight tempo *downgrade*, not an upgrade.** Boseiju is an **untapped {G}** source; **Bojuka Bog enters tapped** ({B}, exile a graveyard on ETB). Replacing an untapped land with a tapland costs you a fraction of a tempo on the turns you draw it — the opposite of "faster." It buys graveyard hate (relevant vs the Sauron/reanimator pod), which is a reasonable trade, but it is not a speed gain.

---

## 2. Kill-line availability — unchanged

`gd_speed_lab.py` grouped model: P(≥1 member of every named group in hand by turn T). "+tutors" treats Eladamri's Call / Chord / Birthing Pod as creature-finding wildcards. Ignores mana — an availability ceiling.

| availability by turn | T4 | **T6** | T8 | T10 |
|---|---|---|---|---|
| **Finale of Devastation** in hand (solo) — pre / post | 10 / 10 | **11 / 12** | 14 / 14 | 15 / 16 |
| **Defense of the Heart** in hand (solo) — pre / post | 10 / 10 | **12 / 12** | 14 / 14 | 16 / 16 |
| **Reanimation pair** (enabler + reanimate spell) drawn — pre / post | 13 / 13 | **18 / 18** | 23 / 23 | 28 / 28 |
| Reanimation pair, +tutors — pre / post | 27 / 27 | **36 / 36** | 44 / 44 | 52 / 52 |
| **Free counter** in hand (FG → FoW) — pre / post | 10 / 9 | **12 / 11** | 14 / 13 | 16 / 15 |
| Finale **+ a dedicated mana accelerant**, +tutors — pre / post | 22 / 21 | **29 / 27** | 36 / 34 | 42 / 41 |

Two takeaways:

1. **The two one-card wins (Finale, Defense) and the reanimation-piece counts are untouched** — all four are 1-ofs or same-size suites in both lists, so you *have* the kill pieces exactly as often as before. The swaps did not add or remove redundancy to any closer.
2. **Finale + mana-engine availability dropped ~2 points** (T6 29% → 27% with tutors). The post-swap list runs **one fewer dedicated accelerant**: it lost Seedborn Muse *and* Sakura-Tribe Elder (2) and gained only Bloom Tender (1). Small, but it is a reliability *loss* on the deck's flagship line, not a gain. (And see §3 — Seedborn was a dubious Finale-enabler to begin with.)

So the *availability* model says the swaps were close to neutral, tilting very slightly negative on the Finale line. The real reliability story is in the two places availability can't see: interaction *quality* (§4) and reanimation *determinism* (§3).

---

## 3. Reanimation reliability — measurably down (Entomb → Grisly Salvage)

This is the one swap that changes a reliability *quality* the availability model is blind to. **Entomb** ({B}, instant) searches your library and bins **exactly** Razaketh/Vilis/Elesh Norn — 100% success. **Grisly Salvage** ({B}{G}, instant) reveals the top 5 and you keep a creature/land; whether a *fat reanimation target* lands in the yard is **random**.

**Verified single-activation hit rate of Grisly Salvage** (≥1 of the 3 fat targets among a random top-5, ~90-card library): **14.8%.**

> **Correction to the Summary and the swaps doc:** both claim Grisly Salvage is "~50% to mill at least one of the 3 primary reanimation targets in 5 cards." That is wrong by ~3×. Hypergeometric and the sim agree it is **~15%**. Grisly is a fine *graveyard filler + card-selection* card (it always nets a creature/land to hand and bins 4 others), but as an *Entomb replacement for enabling a reanimation kill this turn* it is far less reliable than advertised.

The kill-setup model — P(a fat target actually in the yard via a resolved enabler **and** a reanimate spell in hand by turn T):

| build | T4 | **T6** | T8 | T10 | never |
|---|---|---|---|---|---|
| **Pre-swap** (full suite, **Entomb** det.) | 12 | **17** | 22 | 27 | 73% |
| **Post-swap** (full suite, **Grisly** rng.) | 9 | **13** | 17 | 21 | 79% |
| Pre-swap, **Buried Alive removed** (Entomb only) | 9 | **12** | 16 | 19 | 81% |
| Post-swap, **Buried Alive removed** (Grisly only) | 5 | **7** | 9 | 12 | 88% |

**Read:**
- With the full suite, the swap costs **~4 points at T6 / ~6 at T10**, and raises the "never assembled in 10 turns" rate **73% → 79%**. A real but **modest** reliability ding — because **Buried Alive (deterministic, bins up to 3 creatures) is in both lists** and does most of the heavy lifting, cushioning the loss of Entomb.
- Strip Buried Alive out and the swapped card stands naked: Entomb-only assembles ~**60% more often** than Grisly-only by T10 (19% vs 12%). That gap is the true cost of the swap; Buried Alive just hides most of it.

So reanimation got **less reliable**, not more. It is survivable (Buried Alive backbone), but the swaps doc's framing of Grisly as a near-equal Entomb stand-in overstates it.

---

## 4. The reliability the swaps *did* buy (and the sim can't score)

Two of the six swaps are genuine reliability upgrades — but on *quality/coverage*, not *availability*, so they don't show up as a number above (both pairs are 1-ofs with equal draw odds):

**Fierce Guardianship → Force of Will — the headline win.** Card text verified:
- Fierce Guardianship: free **only if you control a commander**, counters **noncreature** spells only.
- Force of Will: free **always** (pay 1 life, exile a blue card), counters **any** spell — including creatures — on any turn.

This directly closes the counter gap the Summary itself flagged ("creature spells / creature-based combos"), and it does so **board-state-independently** (no commander required). Against this pod specifically — the Grand Abolisher + Ur-Dragon / Kinnan / Hidetsugu *creature-combo* decks in [[project_pod_combo_opponent]] — a free counter that **stops a creature** is worth far more than one that can't. This is the clearest "more reliable" result in the whole swap, and it is exactly the kind of interaction the matchup needs. *(It does cost two cards of hand — the FoW plus the blue pitch — where FG cost one; in a deck this blue-dense, pitch fodder is rarely the constraint.)*

**Seedborn Muse → Rhystic Study — a more dependable engine.** Card text verified: Seedborn untaps your permanents **on each opponent's untap step** — it is an *instant-speed* mana engine (hold up counters *and* have mana), and it must survive a rotation to pay off. Rhystic Study is a passive draw engine that works the moment it resolves, refills your hand after a wipe, and doesn't care about your board. As **reliable resource generation**, Rhystic is the steadier card.

> **But kill the Summary's Finale claim.** The swaps doc and Summary both assert "Seedborn enabled a 12-mana Finale by untapping on 2–3 opponents' turns," and that Bloom Tender "compensates" for losing it. **Seedborn does not add mana to your own sorcery-speed turn** — mana empties between steps, and Finale is a sorcery you cast on your turn. Seedborn's value was *instant-speed* mana (Chord of Calling, holding counters), not a bigger Finale. So losing it barely touches the Finale line, and Bloom Tender "compensating for the Finale" is a fix for a problem that wasn't quite real. Bloom Tender's own caveat: **Vivid counts colors among permanents you control, and lands are colorless**, so a lone Bloom Tender taps for just **{G}** (it counts itself) and only reaches WUBG once **Atraxa** (a 7-drop) or a spread of colored permanents is on the board — the same board-conditionality flagged for Calamity Tax.

---

## 5. Verdict — faster? more reliable?

| axis | result | evidence |
|---|---|---|
| **Faster?** | **No.** | Identical avg nonland CMC (2.983), identical land/colour/keepable/has-a-play curves; the one land swap (Boseiju untapped → Bojuka tapped) is a marginal tempo *loss*; Finale+mana availability ↓2 pts; reanimation setup ↓4–6 pts. Nothing moved the clock earlier; a couple of things nudged it later. |
| **More reliable — interaction?** | **Yes (clear).** | Force of Will counters creatures and works without the commander; closes the documented creature-combo gap against this exact pod. |
| **More reliable — card advantage?** | **Yes.** | Rhystic Study is a board-independent, wipe-proof engine; Seedborn had to survive and only acted on opponents' turns. |
| **More reliable — reanimation?** | **No (modest).** | Entomb (100% bin) → Grisly (~15%/cast) costs ~4–6 pts of setup reliability; cushioned only because Buried Alive is in both lists. |
| **More reliable — mana / Finale?** | **Slightly no.** | One fewer dedicated accelerant; Bloom Tender is board-conditional (floors at {G}, needs Atraxa for WUBG). |
| **Conversion Check** | **19/20 held** | The swaps preserved the score and the 3-GC cap, which was their actual goal. |

**The honest summary:** the swaps were a **reliability reshape under a forced substitution**, not a speed or net-reliability upgrade. They traded *reanimation determinism + a mana accelerant* for *creature-counter coverage + a steadier draw engine* — and against this combo-heavy pod, that trade is **defensible and arguably correct** (interaction coverage > a third deterministic graveyard enabler when Buried Alive already exists). But "we made it faster and more reliable" is not what happened: it is **speed-neutral-to-slightly-slower**, and reliability went **up on interaction/draw, down on reanimation/mana**.

---

## 6. If the goal is actually faster / more reliable (levers, ≤3-GC, Bracket-3-legal)

The deck's kills are gated by **mana and setup** (Finale wants 12 mana; reanimation wants a fat target binned + a reanimate spell + a turn), not by *having the card*. So, like Calamity Tax, finisher redundancy isn't the lever — these are:

1. **Restore a deterministic graveyard enabler.** The cheapest way to undo the §3 reliability loss is to get **Entomb back** (it's only held elsewhere) or add a second deterministic binner. Grisly stays as filler; it doesn't have to be the *only* fast enabler.
2. **A front-loaded, board-independent mana source beats another conditional dork.** Bloom Tender needs Atraxa to shine. If the Finale line is the priority, an unconditional accelerant (a basic-fetching ramp spell or a rock) powers a 12-mana Finale more reliably than a dork that taps for {G} until turn 7.
3. **The genuine speed identity is the reanimation kill, not Finale.** Reanimating Razaketh for 1 mana and tutoring the win is the deck's *early* close; Finale-X≥10 is the *slow, mana-hungry* one. If "win the race vs the pod" is the goal (per [[feedback_bracket_4_in_spirit]]), invest in graveyard determinism and a second reanimate spell over the big-mana Finale package.
4. **Don't read Grisly as a kill enabler.** Treat it as card selection + yard fuel; rely on Buried Alive (and ideally Entomb) for "bin a fat target *now*."

None of these are needed to hold 19/20 — they're only relevant if the *next* pass is explicitly a speed/reliability optimization rather than a forced sub.

---

## Method caveats

- `deck_sim.py` is a **consistency** simulator, not a rules engine. Mana/colour are land-only floors; availability % ignore mana, the board, and whether Atraxa/Bloom Tender are online.
- The grouped model treats Eladamri's Call / Chord / Pod as generic creature-tutor wildcards — fair for Finale/Defense/creature-reanimation, slightly optimistic (they cost mana and can't fetch noncreatures).
- The reanimation-determinism model uses a land-floor + shared cheap rocks (Sol Ring/Signet/Birds) for enabler timing and counts only the 3 marquee fat targets as "success." Its absolute "never" rates are a floor (10 turns, no broader tutoring); the **OLD-vs-NEW delta** is the trustworthy output, and it is apples-to-apples.
- "19/20" and kill-window turns are structural estimates, not playtest data; this analysis measures *speed/reliability*, which the Conversion Check doesn't isolate.

---

Related: `The_Grand_Design_Summary.md` · `The_Grand_Design_Swaps_2026-05-02.md` · `Lightning_War_Speed_Curve_Analysis.md` · `Calamity_Tax_Speed_Curve_Analysis.md` · [[project_deck_sim_and_matchup_matrix]] · [[project_pod_combo_opponent]] · [[feedback_bracket_4_in_spirit]]
