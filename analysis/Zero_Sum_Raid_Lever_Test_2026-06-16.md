# Zero-Sum Game — DR-Raid Lever Test (2026-06-16)

**Question (Alex).** Zero-Sum Game sits in no man's land — #10 vs his combo decks
(34% blend) and #6 vs his Ur-Dragon (70%). Can a raid of Diminishing Returns
(treated as a free donor; buying decided after) — Sephiroth + the black aristocrat
package + the infinite-combo pieces — push it into the both-ways top tier? **Model
all the candidate packages so we know which gives the payoff, not one committed list.**

**Verdict: No. On every axis the lab can measure, raiding DR is flat-to-worse.**
The lifeloop is already the deck's best line. The raid trades loop reliability for
board-independent kills that are too slow (T11–13) to convert within the horizon.

Lab: `scripts/wb_raid_lab.py` (40k trials, seed 20260616), derived from the
validated `scripts/wb_clock_lab.py` — `base` reproduces that lab's T9 exactly.

---

## Method

A lever test in the house style (cf. Lightning War §5, GD finisher sims): one
baseline + each candidate package **isolated**, on the same decap/table grid,
deltas attributed. Each package ADDS its cards and CUTS an equal number of the
weakest base slots (surplus dorks/tutors, the 7-MV Defiant Bloodlord, Corpse
Dance, etc.), so deck size — and draw odds — stay at 99.

The model credits **three new kill axes** beyond the base lifeloop, each card
oracle-verified 2026-06-16:

1. **Speed** — K'rrik (B pips → 2 life; loop repays) + reanimation.
2. **Aristocrat board-burn** — Syr Konrad / Nadier / Zulaport / Blood Artist fed
   by free sac outlets; accumulates as a grind + a one-shot hoarded-board alpha.
3. **Devotion / reanimator burst** — Gray Merchant (devotion drain) + Kokusho
   (death-drain), reanimated for repeats. Board-independent.
4. **(Her on-identity infinite)** — the Witherbloom Apprentice + Sprout Swarm
   affinity-storm (convoke-buyback loop → infinite magecraft drain), boosted by
   Professor Onyx (2nd drain payoff) + Sedgemoor Witch (Pest/convoke fuel).

Decap = table throughout, because the kills hit all opponents at once. The number
that matters is **never-kill % within 12 turns** (reliability).

---

## Lever test (open board, 40k)

| Variant | adds (−equal cuts) | median | never-kill % | vs base |
|---|---|---|---|---|
| **base** (lifeloop only) | — | **T9** | **25%** | — |
| base+ (raid model ON, same list) | credits existing aristocrats | T9 | 25% | flat |
| **speed** | +K'rrik +Reanimate +Victimize +Animate Dead | T9 | 26% | flat |
| **burst** | +Gray Merchant +Kokusho +Reanimate +Victimize +Animate Dead +Living Death | T9 | 27% | flat |
| **storm** | +Professor Onyx +Sedgemoor Witch | T9 | 27% | flat |
| **tokens** | +Slimefoot +Chatterfang +Scatter the Seeds | T9 | 26% | flat |
| **tokens+** | tokens +Professor Onyx +Sedgemoor Witch +Ophiomancer | T9 | 27% | flat |
| **burn** | +Syr Konrad +Nadier +Sephiroth +Priest +Yahenni +Woe Strider +Carrion Feeder +Morbid Opportunist | **T10** | **32%** | **worse** |
| **combined** | the full 10-card both-ways build | **T10** | **36%** | **worst** |

The `tokens` axis (added 2026-06-16 on Alex's "isn't the bottleneck bodies → infinite
tokens?" prompt) models the **Witherbloom + Sprout Swarm affinity infinite** as a real
kill (the deck tutors the last piece) + Chatterfang token-doubling + Slimefoot's
each-opponent Saproling-death drain. Flat — see Finding 7.

## Disruption / fair-wall (blocked board, no combat ignition, 40k)

The resilience proxy the race clock can't show: the lifeloop loses its easiest
igniter and must rely on non-combat ignition + the raid's board-independent kills.
This is also the Ur-Dragon "walled by flyers" scenario.

| Variant | table never-kill % |
|---|---|
| base | 42% |
| speed | 41% |
| burst | 41% |
| storm | 41% |
| tokens | 40% |
| tokens+ | 41% |
| burn | 43% |
| combined | **47%** |

Even here — exactly where a board-independent second kill *should* rescue games —
the raid is **flat** (41–43% vs 42%), and over-raiding (combined) is **worse**.

---

## Findings

1. **The lifeloop is already the fast line; you can't out-add it.** Every package
   displaces a loop enabler (a tutor, a dork, redundancy). The kills the raid
   brings are all slower than T9 — aristocrat grind ~T13, Gary/Kokusho bursts
   ~T11, the storm too conjunction-heavy to fire often — so they can't pull the
   median down, and thinning the loop pushes never-kill **up**. The more you raid,
   the worse it gets.

2. **K'rrik does nothing here.** The loop is *finding*-gated (drawing/tutoring the
   two halves), not mana-gated at the margin (+mana = flat). Consistent with the
   deck's own gcswap result, which kept the tutor suite over Mana Vault.

3. **The aristocrat board-burn (Sephiroth + Konrad + Nadier) is the *worst* race
   package** — the biggest enabler displacement (8 cuts) for the slowest payoff.
   This was the most intuitively "on-identity" add and it backfires on the clock.

4. **Burst (Gray Merchant + Kokusho) is the least-bad** — roughly flat clock and
   the only package with a genuinely board-independent Plan B. Its value is NOT in
   these numbers; see the caveat.

5. **Her on-identity affinity-storm is a cute bonus line, not a lever.** Even
   boosted (Onyx + Sedgemoor), it stays flat — the commander + magecraft payoff +
   Sprout Swarm + wide-green-board conjunction is too rare to move reliability.

6. **The "no man's land" is structural and not raid-fixable.** Zero-Sum is a
   2-piece BG combo (T9, 25% never) with **no access to counters** — capped below
   the counter-immune / counter-heavy top tier (Radiation Sickness, Replication)
   by colour, and below the T7 racers by clock. No DR card touches either limit.

7. **Infinite tokens is the wrong diagnosis for THIS deck (Alex's prompt).** The
   "bodies are the bottleneck" insight is correct — but it's *DR's* bottleneck. DR
   has **no fast combo, only the aristocrat grind**, so it is genuinely body-starved
   (tables T12+) and infinite tokens would fix it. Zero-Sum already has a **fast
   combo (the lifeloop, T9)**; its bottleneck is **assembling any combo at all**
   (commander + the right cards + mana). The Witherbloom + Sprout Swarm token-
   infinite is real, on-colour, and elegant — but it has the **same assembly cost
   as the lifeloop and shares its bottleneck**, so it's lateral: the ~26% whiff
   games are development/mana-screwed games where the token combo *also* can't
   assemble, and the cuts to fit it offset any gain. Even god-draw turns (T5–6) are
   identical to base. A second coequal combo doesn't rescue games where you can't
   cast your first. (NOT tested: a ground-up REBUILD around tokens as the *primary*
   plan — a different deck, not a raid; likely more fragile, since the token combo
   needs a board the lifeloop doesn't, so it dies to the wraths/flyers the board-
   independent lifeloop ignores.)

   *Lab bug fixed in passing:* **Marionette Apprentice** reads "each opponent loses
   1 life" (Brothers' War) — an each-table drain, not single-target as first coded.
   Corrected (now in `PER_EACH`). The deck has marginally more table-drain than
   credited; verdict unchanged.

---

## What the lab still can't price (the honest caveat)

The disruption proxy removes the *easiest igniter* (combat) but does **not** model
a combo half being **countered or exiled** — the real disruption a control deck
applies. Against *targeted* loop removal, `base` has no backup kill while `burst`
(Gary/Kokusho) does. So the burst package retains a real, **unmeasured** value:
insurance for "what do you do when they answer your combo," plus the Ur-Dragon
fair-board matchup (its own lab, `vs_dragon_roster_lab.py`, not this clock). But
note even there the backups are T11–13 — slow enough that they'd rarely close
before a developed pod kills you.

**Drain -> lifegain -> survival (Alex, 2026-06-16): a gap in ALL these one-way
goldfishes.** None of the kill-clock labs (this one OR `dr_clock_lab.py`) model
*incoming* damage -- we race a 40-life table and nobody attacks us. So the
survival value of the drains' lifegain (Gray Merchant gains devotion-worth ~18+,
Kokusho 5-15/death) is **unpriced everywhere**. `dr_clock_lab` at least tracks
our life as a *cost* resource (gates K'rrik / Dark Confidant / Reanimate;
`gain()` bumps it) but never as a buffer against an opponent clock; this lab
treats life as ~goldfish-free. The value **splits by opponent**: vs his
**infinite** combo decks lifegain is a **trap** (infinite drain beats any total
-- matrix-confirmed); vs **Ur-Dragon / aggro / burn** (non-infinite) it is a
**real survival buffer** that buys turns. Net: this *strengthens* the burst
package as an Ur-Dragon / fair hedge (a board-independent kill that ALSO gains a
wall of life) and changes nothing about the combo verdict. Quantifying it needs a
survival overlay (our life vs an incoming-clock prior) or the
`vs_dragon_roster_lab` run -- neither is this clock.

**Cross-check on the incremental-drain treatment (Alex, 2026-06-16):**
`dr_clock_lab.py` does NOT make the one-shot-only mistake an early draft of this
lab did -- it accumulates per-death drain every turn (`die()` -> `hit_all`,
`sac_phase` board-liquidation, Kokusho/Skullclamp/Gravecrawler loops). It found
DR's drain tables **T12+ even with Teysa's x2 doubling**. Zero-Sum has no doubler,
so the same pieces drain at half rate and would table >=T12 -- independently
confirming the raid grind cannot beat the lifeloop's T9.

---

## Follow-ups (Alex, 2026-06-16): vs Ur-Dragon + token rebuild

**#1 — burst/tokens through `vs_dragon_roster_lab` = flat at 70%.** The model credits
lifegain as a capped buffer (`nlife = min(sources, 6)`, +2 each, cap +12). Base
Zero-Sum already has **14 lifegain sources** (saturated) and an **over-axis** kill that
ignores the flying wall, so it is already a 70% anti-dragon deck (robust 65–73% across
the prior sweep). Burst/Tokens add *more* lifegain + *more* over-kills — both already
maxed — and no wraths, so they return ~70% unchanged. The lifegain instinct is right;
the deck already exploits it to the cap.

**#2 — token-combo + fog REBUILD = 73%, dominated by Glarb's 93%.**
`decks/considering/witherbloom-tokens-rebuild-20260616.txt` (two infinite-token engines —
Sprout Swarm + commander, and Earthcraft + Squirrel Nest — + Chatterfang doubling +
drain payoffs + a recurring green fog package). Raced via `scripts/wb_rebuild_vs_dragon.py`
(reusing zero_sum's over/decap clock for the ~T9 token over-kill):

| deck | fogs | wraths | P(win) | 
|---|---|---|---|
| base Zero-Sum | 0 | 1 | 70% |
| Zero-Sum + 3 fogs (lever isolated) | 3 | 1 | 72% |
| tokens-rebuild | 3 | 1 | **73%** |
| Glarb / Calamity | 3 | 3 + Maze | **93%** |

Findings: (a) the rebuild reaches only **73%** — the **+3pp is the FOG package, not the
token combo** (Zero-Sum + 3 fogs alone = 72%); the token engine is just a second
over-kill the deck didn't need vs dragons. (b) The dragon matchup is won by the
**survival fortress** (Glarb = 3 wraths + Maze + fogs + 1-card Torment over-kill), which
a combo deck can't carry. (c) The rebuild is **board-dependent** (loses the lifeloop's
board-independence) → *worse* vs the combo pod. Rock-paper-scissors trade is a net loss:
give up combo equity for +3pp vs dragons, landing at 73% when **Glarb already does that
job at 93%.** *Actionable nugget:* +Spore Frog (owned) / Constant Mists / Darkness on the
*current* list = 70→72% vs dragons with no rebuild — but those slots are dead vs combo,
so still dominated by bringing Glarb when dragons are expected.

## Recommendation (buying is Alex's call)

- **Buy nothing for speed.** No package makes Zero-Sum faster or more reliable on
  the clock. The lever that *would* help its combo matchup is tightening the LOOP
  (more half-redundancy / tutors to nudge T9→T8 and lower the 25% never) — and
  even that is marginal and doesn't touch the no-counters colour cap.
- **The only defensible spend is a *small* burst add** — Gray Merchant + Kokusho
  (+ maybe one reanimation) — as targeted-disruption insurance and an Ur-Dragon
  hedge, **not** a top-tier transformation. Validate it on
  `vs_dragon_roster_lab.py` (the fair matchup) before committing, since that's the
  axis where it could actually pay.
- **Do not run the full "combined" raid** — it is strictly worse on every measured
  axis (guts the loop).
- **Portfolio view:** Zero-Sum is a fine mid deck. For his combo pod bring
  Radiation Sickness / Replication (counter-immune / counter-heavy, T7); for his
  Ur-Dragon bring Calamity/Glarb (94%). Zero-Sum doesn't need to be either.

---

## Files

- Lab: `scripts/wb_raid_lab.py` (modes: `levers`, `disrupt`)
- Base clock (unchanged citation): `scripts/wb_clock_lab.py`, `decks/Zero_Sum_Game_Summary.md`
- Card text verified 2026-06-16: K'rrik, Gray Merchant, Kokusho, Gravecrawler,
  Sephiroth (both faces), Syr Konrad, Nadier's Nightblade, Witherbloom Apprentice,
  Sprout Swarm, Lab Rats, Priest of Forgotten Gods, Woe Strider, Professor Onyx,
  Sedgemoor Witch (all via `card_lookup.py`).
- Ownership cross-check: `collection/moxfield_haves_2026-06-07-1031Z.csv`.
