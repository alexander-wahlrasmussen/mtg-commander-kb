# Pod Matchup Matrix — Roster vs. The Combo Opponent

How each active deck matches up against the recurring pod combo opponent. This is
a **decision aid**, not a guarantee — it combines audited kill windows, the
interaction profile of each deck, and Monte Carlo consistency output from
`scripts/deck_sim.py`. State doc, not reference: re-derive when a deck's score,
clock, or interaction suite changes.

Last built: **2026-06-01**. Rebuilt **2026-06-05** — sim refreshed (20k trials/deck); all reskins now resolve, **zero unresolved cards** across the 16 active decks; Replication Crisis row updated for the pending Kiki swap. Rebuilt **2026-06-09** — **land-colour model fixed** (`deck_sim.py` previously scored sac-fetches and rainbow lands as zero-colour sources via empty `color_identity`; now uses `produced_mana` + fetch resolution — see `proposals/Grand_Design_Mana_Fixing_Pass_2026-06-09.md`). All Colour-T6 figures re-derived; finding #2 and recommendation #2 retracted/rewritten. Replication Crisis clock re-derived **2026-06-09** via the `scripts/rc_speed_lab.py` goldfish combat lab (`proposals/Replication_Crisis_Speed_Curve_Analysis.md`). Exile's Return clock re-derived **2026-06-09** via `scripts/er_speed_lab.py` (`proposals/Exiles_Return_Speed_Curve_Analysis.md`) — Clock flag downgraded, verdict held on the disruption axis.

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
| The Replication Crisis | 17 → 18–19 | T7–8 decap · T10+ table (lab) | ❌ 16% by T6 even unblocked | ❌ counter-reliant (dead under Abolisher); every line needs Satya to connect | 90% | **Even — race measured & rejected** (pending Kiki swap; see note) |
| The Calamity Tax | 18→19 | T7–9 | ⚠ slower | ✅ static tax + stax slows their mana; Seedborn keeps you live | 96% | **Favoured — grind/oppress** |
| The Exile's Return | 17→18 | T7–8 decap · T10 table (lab) | ⚠ 9% by T6 / 39% by T7 even unblocked | ✅ own Grand Abolisher protects your turn; 9 spot-removal for theirs; pending Drannith swap adds static hate | 94% | **Favoured — disruption-led, not a race** |
| The Grand Design | 19 | decap T10 · table T12+ (lab) | ❌ 1% by T6 / 20% by T8 | ✅ own Grand Abolisher + Teferi T.R. (sorcery-lock) + FoW pre-Abolisher | 89% | **Favoured — disruption-led, not a race** |
| Lightning War | 18 | T6–8 | ✅ races | ⚠ counter-reliant; burn can finish through a lock | 97% | **Even–favoured — outrace** |
| The Loam Cycle | 19 | T6–8 | ✅ | ⚠ FG + Counterspell only (dead under Abolisher); no static hate | 91% | **Even** |
| Diminishing Returns | 17 | T7–9 | ⚠ | ✅ own Grand Abolisher + edicts punish post-combo; no counters | 95% | **Even** |
| Radiation Sickness | 18 | T6–9 | ⚠ | ⚠ counters + Force of Negation (off-turn, pre-Abolisher only) | 90% | **Even** |
| Curse of the Scarab | 17 | T7–9 | ❌ | ⚠ FG counter; otherwise reactive | 96% | **Even–underdog** |
| Crystal Sickness | 17 | T7–9 | ❌ | ⚠ FG counter; reanimator is slow to disrupt | 94% | **Underdog** |
| The Genome Project | 15 | T7–9 | ❌ | ⚠ some counters; combo-reliant itself | 98% | **Underdog** |
| Lorehold Spirits | 18 | T7–9 | ❌ | ❌ no counters; Teferi's Protection only survives, doesn't stop | 99% | **Underdog** |
| Earthbend the Meta | 17 | T7–9 | ❌ | ❌ no counters; slow | 90% | **Underdog** |
| The Dark Lord's Army | 19 | T8–10 | ❌ | ⚠ 15 interaction but slow clock loses the race | 89% | **Underdog — too slow** |
| Ms. Bumbleflower | 15 | T8–10 | ❌ | ⚠ 5/5 interaction but combat-only kill is far too slow | 93% | **Underdog — too slow** |
| Eldrazi Stampede Chaos | 14 | T6–8 | ✅ clock only | ❌ no counters, no lock; "cannot stop a combo turn" (audit) | 88% | **Underdog — no disruption** |

*(Peace Offering is off the active roster and excluded.)*

> **Reassessment note (2026-06-01, MEASURED 2026-06-09): Replication Crisis is
> not a race deck.** The 2026-06-01 draft argued this structurally; the
> `rc_speed_lab.py` goldfish combat lab (40k trials — token copies, energy
> keeps, Procession/Panharmonicon doubling, Brudiclad conversion, AA extra
> combats; see `proposals/Replication_Crisis_Speed_Curve_Analysis.md`) now
> quantifies it. Even with **every attacker unblocked and zero interaction**,
> the focused decapitation of one opponent lands by T6 only **16%** of the time
> (median T7); a defended-board proxy gives **6%** (median T8). The **table**
> kill is median T10–11 unblocked. The Sword+AA infinite decides ~1–3% of
> games (zero tutors), and Adeline's tokens are *spread* 1/opponent by printed
> text, not focused. The Summary's old "Goldfish T5–7" was a god-draw artifact
> (T5 = 2%) and has been corrected. Against a T6–7 combo pod whose Abolisher
> also blanks Replication's counter-based protection — and whose Ur-Dragon
> shell presents exactly the blockers the model assumes away — this is an even
> matchup as a value deck, and a clear loss as a race.

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

2. ~~**Colour-fixing is the real consistency divide.**~~ **RETRACTED 2026-06-09 —
   measurement artifact.** The old land-colour model scored a land by its Scryfall
   `color_identity`, which is **empty for sac-fetches and rainbow lands** (Command
   Tower, City of Brass, Exotic Orchard, Reflecting Pool). It therefore counted a
   deck's *best fixers as zero-colour sources* and punished exactly the bases built
   for fixing: Grand Design read 39% with 11 of its 39 lands deleted from the
   colour count. Under the corrected model (`produced_mana` + fetch resolution)
   the roster's T6 floors compress to **88–99%** — Grand Design 89%, Earthbend
   90% — and no active deck is structurally rock-dependent. The surviving, smaller
   truth: basics-light 4-colour bases pay at T2–3 (GD reads 49/68% there), which
   is normal 4C variance handled by dorks/rocks and mulligans, not land swaps.
   Full writeup: `proposals/Grand_Design_Mana_Fixing_Pass_2026-06-09.md`.

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

2. ~~**Fix Grand Design's mana base.**~~ **RETRACTED 2026-06-09** — the 39% that
   motivated this was the model artifact above; the corrected floor is 89% and the
   hand-counted base is ≥16 sources per colour. No land changes needed. Grand
   Design's freed priority goes to the **merged ETB/finisher build**
   (`Grand_Design_ETB_Disruption_Pass_2026-06-09.md` §5): a creature finisher the
   engine can tutor (Craterhoof) + ETB disruption that pre-empts the Abolisher
   turn (Skyclave Apparition, Noxious Gearhulk) + a tutor for noncreature
   interaction (Spellseeker).

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
