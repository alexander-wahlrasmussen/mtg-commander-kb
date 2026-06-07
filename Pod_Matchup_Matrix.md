# Pod Matchup Matrix — Roster vs. The Combo Opponent

How each active deck matches up against the recurring pod combo opponent. This is
a **decision aid**, not a guarantee — it combines audited kill windows, the
interaction profile of each deck, and Monte Carlo consistency output from
`scripts/deck_sim.py`. State doc, not reference: re-derive when a deck's score,
clock, or interaction suite changes.

Last built: **2026-06-01**. Rebuilt **2026-06-05** — sim refreshed (20k trials/deck); all reskins now resolve, **zero unresolved cards** across the 16 active decks; Replication Crisis row updated for the pending Kiki swap.

---

## The opponent we're tuning against

From the pod profile (see memory `project_pod_combo_opponent`): an Ur-Dragon
ramp shell plus Hidetsugu / Kairi / Kenrith / Kinnan combo decks. **Wins T6–7**,
typically **behind Grand Abolisher**. Bracket-4-in-spirit despite a low GC count.

The single most important mechanical fact (memory
`grand_abolisher_blocks_counters`):

> On **their** turn, their Grand Abolisher stops you from casting spells or
> activating artifact/creature/enchantment abilities. **Your counterspells are
> dead on their combo turn.** What still works: anything *static and already in
> play* (Rule of Law, Cursed Totem, Drannith Magistrate, Mindcensor), triggered
> abilities, land/mana abilities, and **removal cast before they untap** (kill
> the Abolisher on sight, or pre-empt the combo).

So the matchup is **not** decided by counterspell count. It's decided by:

1. **Clock** — do you kill at or before their T6–7?
2. **Disruption that survives Abolisher** — static stax/hatebears in play, an
   oppressive tax that slows their setup, your own proactive lock to protect
   your kill turn, or removal held for their Abolisher.

---

## The matrix

Clock = audited goldfish kill window. "Through Abolisher?" = can the deck
meaningfully disrupt the combo turn *given* a resolved enemy Abolisher.
"Colour T6" = Monte Carlo probability all colours are available from **lands
only** by turn 6 (a floor — rocks/dorks raise it); low values flag a deck that
needs its fixing rocks to come online to function on curve.

| Deck | Score | Clock (goldfish) | Beats T6–7? | Through Abolisher? | Colour T6 (lands) | Verdict vs pod |
|---|---|---|---|---|---|---|
| The Replication Crisis | 17 → 18–19 | T6–8 (T5 god-draw) | ⚠ only on a god-draw | ❌ counter-reliant (dead under Abolisher); every line needs Satya to connect | 77% | **Even — overrated as a race** (pending Kiki swap; see note) |
| The Calamity Tax | 18→19 | T7–9 | ⚠ slower | ✅ static tax + stax slows their mana; Seedborn keeps you live | 48% ⚠ | **Favoured — grind/oppress** |
| The Exile's Return | 17→18 | T6–8 | ✅ | ✅ own Grand Abolisher protects your turn; 9 spot-removal for theirs | 79% | **Favoured** |
| The Grand Design | 19 | T6–8 | ✅ | ✅ own Grand Abolisher + Teferi T.R. (sorcery-lock) + FoW pre-Abolisher | 39% ⚠⚠ | **Favoured (if it hits colours)** |
| Lightning War | 18 | T6–8 | ✅ races | ⚠ counter-reliant; burn can finish through a lock | 67% | **Even–favoured — outrace** |
| The Loam Cycle | 19 | T6–8 | ✅ | ⚠ FG + Counterspell only (dead under Abolisher); no static hate | 71% | **Even** |
| Diminishing Returns | 17 | T7–9 | ⚠ | ✅ own Grand Abolisher + edicts punish post-combo; no counters | 82% | **Even** |
| Radiation Sickness | 18 | T6–9 | ⚠ | ⚠ counters + Force of Negation (off-turn, pre-Abolisher only) | 69% | **Even** |
| Curse of the Scarab | 17 | T7–9 | ❌ | ⚠ FG counter; otherwise reactive | 87% | **Even–underdog** |
| Crystal Sickness | 17 | T7–9 | ❌ | ⚠ FG counter; reanimator is slow to disrupt | 88% | **Underdog** |
| The Genome Project | 15 | T7–9 | ❌ | ⚠ some counters; combo-reliant itself | 88% | **Underdog** |
| Lorehold Spirits | 18 | T7–9 | ❌ | ❌ no counters; Teferi's Protection only survives, doesn't stop | 95% | **Underdog** |
| Earthbend the Meta | 17 | T7–9 | ❌ | ❌ no counters; slow; fixing-dependent | 40% ⚠⚠ | **Underdog** |
| The Dark Lord's Army | 19 | T8–10 | ❌ | ⚠ 15 interaction but slow clock loses the race | 67% | **Underdog — too slow** |
| Ms. Bumbleflower | 15 | T8–10 | ❌ | ⚠ 5/5 interaction but combat-only kill is far too slow | 77% | **Underdog — too slow** |
| Eldrazi Stampede Chaos | 14 | T6–8 | ✅ clock only | ❌ no counters, no lock; "cannot stop a combo turn" (audit) | 66% | **Underdog — no disruption** |

*(Peace Offering is off the active roster and excluded.)*

> **Reassessment note (2026-06-01): Replication Crisis is not the fast race the
> first draft implied.** Its summary lists goldfish T5–7, but that's the
> god-draw floor: the deck has **zero tutors**, so the Sword+AA infinite is ~1–2%
> to assemble by draw (sim), and *every* kill line requires Satya — a 4-mana 3/5
> commander — to survive and connect in combat. The summary's own play pattern
> says "Goal turns 6–8." Against a T6–7 combo pod whose Abolisher also blanks
> Replication's counter-based protection, this is an even matchup, not a
> favoured outrace. Treat the audited "goldfish" numbers as optimistic floors
> throughout this table, not expected kill turns.

> **Pending fix — the Kiki swap closes the Satya-dependence (proposed 2026-06-01,
> not yet applied).** `decks/The_Replication_Crisis_Swaps_2026-06-01.md` proposes
> **+Kiki-Jiki, Mirror Breaker / −Bident of Thassa** (1-for-1, stays 99+1 and 3/3
> GCs). Kiki-Jiki + Zealous Conscripts and Kiki-Jiki + Restoration Angel — **both
> partners are already in the 99** (verified 2026-06-05) — are infinites that win
> on *assembly*, needing **neither Satya nor a connecting attack**, which is
> exactly the weakness that pins this row. Projected **18–19/20**. Three caveats
> keep the *current* verdict Even: the swap is **not applied to the `.txt`**
> (Kiki is an unowned ~€10–15 buy), it needs **pod approval** (a 4th standing
> 2-card-infinite exception — see [[REF_Bracket_3_House_Rules]]), and as a 2-card
> combo it's still only ~2% to draw naturally (sim) — it raises the deck's
> *resilience and ceiling*, not its expected clock against a T6–7 pod. Once Kiki
> lands, add the two Kiki lines to `sim_profiles.json` and re-derive this row.

---

## What the simulation actually told us

Two findings from `scripts/deck_sim.py` (20k trials/deck), separate from the audits:

1. **Fixed 2-card combos are ~2% to draw naturally by T10.** Replication's
   Sword+AA, Lightning War's AA+Ozai, Diminishing's Gravecrawler+Altar all sit
   near 1–2% drawn, ~2–6% with their lone tutor. This is *correct* maths for two
   singletons in 99 cards — and it confirms these decks' real speed comes from
   **redundancy, alternative lines, and tutor packages**, not from drawing the
   named combo. It also quietly argues for the Conversion Check's new
   "independent closing lines" axis: a deck leaning on one fragile pair is slow
   and stoppable. **Decks that win by racing the pod need redundant kill density,
   not a prettier two-card combo.**

2. **Colour-fixing is the real consistency divide, and it's invisible in the
   land count.** Land counts are near-uniform (~4.6–4.8 lands by T6 everywhere),
   but all-colours-from-lands ranges from 95% (Lorehold, Boros) down to **39%
   (Grand Design, WUBG) and 40% (Earthbend, Naya)**. Those two decks are
   *structurally dependent on mana rocks* to cast on curve — a real fragility the
   audits don't surface. Worth a fixing pass (more dual lands / fewer
   colour-screw keeps) on Grand Design especially, given it's a 19/20 we lean on
   against the pod.

---

## Recommendations

1. **The roster's anti-pod plan is "outrace or oppress," and it's thin on the
   third option: static disruption.** Almost every "Through Abolisher?" ⚠ is the
   same gap — the deck's interaction is *reactive* (counters/removal) and dies on
   their combo turn. The decks that beat the pod do it by being faster
   (Lightning War's burn race, which can finish through blockers) or by
   taxing/locking proactively (Calamity Tax, the three Grand-Abolisher decks). **The highest-leverage upgrade across the
   roster is cheap static hatebears** — Rule of Law, Cursed Totem, Drannith
   Magistrate, Mindcensor — that keep working under their Abolisher. This is
   exactly what the **Kefka** (forced-draw burn that resolves on *your* turn) and
   **Exile's Return Drannith** swaps target; both are pointed the right way.

2. **Fix Grand Design's mana base.** A 19/20 deck we want against the pod that
   only assembles all four colours from lands 39% of the time by T6 is one bad
   keep from doing nothing. Add fixing or tighten the curve.

3. **The "too slow" tier (Dark Lord, Bumbleflower, Lorehold, Earthbend) is fine
   — just not the deck you bring to this pod.** Don't try to speed them up at the
   cost of their identity; pick a faster deck for this table.

4. **Alias resolution is now clean (was: Bayo outstanding).** As of the
   2026-06-05 rebuild, `deck_sim.py` resolves every UB reskin through
   `REF_Reskin_Aliases.md` — **zero unresolved cards across all 16 active decks**.
   The previously-flagged exception, **Bayo, Irritable Instructor** (Genome
   Project), was corrected in the alias table to point at the printed card
   `Electro, Assaulting Battery`, so Genome's colour figure (88%) and
   Diminishing's (80% → 82%, as Castle Shimura → Eiganjo Castle now counts as a
   white source) are computed on fully-resolved lists. No outstanding data gaps.

---

## Method & limits

- **Source of truth:** each deck's `.txt` (contents) and `collection/oracle-cards.json`
  (cmc, type line, colour identity). Kill windows and interaction scores are from
  the audited `*_Summary.md` files.
- **`deck_sim.py` is not a rules engine.** It models opening-hand keepability
  (London mulligan, 2–5 land keep), land drops, colour availability from lands,
  and combo-piece draw. It does **not** model casting, the stack, mana from
  rocks/dorks, or actual play. Treat mana/colour figures as **floors**.
- **The matchup verdicts are judgement**, anchored to the data above and the pod
  profile — not simulator output. Two decks didn't play; this estimates who's
  favoured and why.
- Rebuild the sim numbers with: `python scripts/deck_sim.py --combos --json sim_results.json`
