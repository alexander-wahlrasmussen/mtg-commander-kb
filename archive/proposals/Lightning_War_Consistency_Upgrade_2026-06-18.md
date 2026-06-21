# Lightning War — Combo axis, the consistency swap, and a BDD benchmark

**Date:** 2026-06-18 (rev. 2026-06-19 — fast pkg, GC swap, focus, recursion, color, pod_gauntlet) · **Status:** COMMITTED — race build; pod_gauntlet P(WIN) 38%→64% (§13). Ready to apply.
**Deck:** Fire Lord Azula (Lightning War), `decks/lightning-war-20260614.txt`
**Lab:** `scripts/lw_combo_lab.py` (combo-assembly clock, deck-agnostic), 40k trials, seed 20260618
**Inputs:** BDD's lists `decks/considering/bdd-azula-{expensive,budget}-20260618.txt`; reviews [[reference-bdd-azula-b4-combo]], [[reference-maldhound-azula-review]].

---

## 1. The two combos our deck already contains — and the asymmetry vs BDD

- **Combo A — draw the deck.** Narset's Reversal + (Frantic Search *or* Turnabout), Azula attacking.
  All halves are **instants** → every instant-tutor reaches them, and a copyable instant-tutor
  (Mystical/Waterlogged Teachings) cast in Azula's combat is **itself copied**, fetching *both*
  pieces from one card (BDD's core accelerant). We have Narset's + Frantic Search; **no Turnabout**.
- **Combo B — infinite red mana.** Reiterate + a Seething Song *source* → Comet Storm/Crackle.
  **Here is our handicap:** we have **no standalone Seething Song**. Our only source is the
  **Blazing Firesinger** creature half — it must be *cast into play* first, and a **creature is
  reachable by only an any-card tutor** (our single Emeritus of Woe // Demonic Tutor), not by the
  three instant-tutors. BDD runs Seething Song as a free-floating instant that all ~10 of his
  tutors can grab.

**Verified vs commanderspellbook.com (2026-06-19):** Combo A (Azula + Narset's Reversal + Frantic
Search) is a catalogued variant — exact match. Combo B (Azula + Reiterate + Seething Song) isn't
listed for Azula yet (new card), but CSB catalogues **Reiterate + Seething Song** as a combo family
that needs a copy/cost enabler (Bonus Round, Storm-Kiln Artist, Birgi, …) — **Azula is that enabler**
(she copies each I/S in her combat, identical to the listed Bonus Round variant; net +4 R/loop).
Bonus: CSB also confirms a **third** line we run — **Azula + Narset's Reversal + Storm-Kiln Artist →
infinite mana** (prereq: a spare cheap instant/sorcery in hand). The post-rebuild deck has all three.

## 2. Density: ours vs BDD (the root cause)

| | Tutors | Cheap selection | Mana rocks (incl. fast mana) | Seething Song |
|---|---|---|---|---|
| **Lightning War (ours)** | **4** | ~4 | **4** (no Sol Ring / Vault / Mox) | creature-gated (Blazing Firesinger) |
| **BDD expensive (B4)** | ~9–10 | ~9 | ~11 (Sol Ring, Mana Vault, Moxen, Ancient Tomb) | standalone instant |
| **BDD budget (B4)** | ~9–10 | ~13 | ~11 (treasures + signets) | standalone instant |

Our 4 tutors are: Emeritus of Woe (any), Mystical Teachings, Waterlogged Teachings, Sanar // Wild
Idea (the last three instant/sorcery-only — **none reach Blazing Firesinger**).

## 3. Lab — how fast does each deck assemble a combo? (40k, SEEN=pieces accessible, CAST=+mana)

```
P(combo CAST-live <= turn T) %        4    5    6    7    8    9   10   12   median
Lightning War (ours)                  0    5   13   17   21   24   27   32   never-in-14
BDD expensive (B4 combo)             10   28   47   55   61   66   70   77   T7
BDD budget   (B4 combo)               5   24   45   55   61   66   70   77   T7
```

**Answer to "how quick are his decks, per our labs": his combo goes off at median T7**, with a
fast tail (~10% T4 / ~28% T5 on the expensive list) — squarely consistent with the T4–6 kills he
shows on screen. **Ours reaches ~13% by T6 and never crosses 50% in the 14-turn horizon.** His
deck assembles **~3–4× more often** at every turn. (Caveat: the rock model is mildly *generous* to
fast mana, so if anything his numbers flatter him slightly; this is the combo clock, his only plan.)

**Why ours looks "so slow" is an archetype confusion, not a defect.** Our deck's real kill clock is
the **burn race** (`lw_clock_lab`: **decap T8 / table T10**), not the combo. The combo is a
*secondary, low-frequency bonus* (~once every 3–4 games by T10). BDD's deck has **no race** — the
combo *is* the deck, fed by 2.5× the tutors, 2–3× the selection, and fast mana we don't run.

## 4. The swap, bracketed (our deck) — does cheap selection help?

```
P(combo CAST <= T) %                  5    6    7    8    9   10   12
current, dig OFF (raw draw + tutors)  5   12   17   20   24   27   32
current, dig ON  (own selection)      5   13   17   21   24   27   32   ← ~identical
PROPOSED (+Brainstorm/Ponder/Pre.)    6   14   19   22   26   29   34   ← +~2pp
```
**Race regression** (`lw_clock_lab.goldfish_kill`, moderate chip): current **decap T8 / table T10**;
proposed **decap T8 / table T10**, front edge ~3–5pp lower (table T10 55%→50%) from cutting Fated
Firepower. Medians unchanged.

## 5. Verdict & recommendation

1. **The combo is tutor-gated, not dig-gated.** Cheap selection moves combo assembly by ~0 (current)
   to +2pp (proposed). Cantrips can't reliably find a *specific* 2-card combo; **tutors** do. The
   selection thesis is falsified ([[feedback_selection_vs_mana_gated]] run honestly).
2. **The proposed 3-swap is marginal-to-slightly-negative** — no combo gain, a small race-front-edge
   loss. **Do not apply as-is.** If you want the hand-feel nudge only, the zero-cost slice is
   **−Necromancy / +Ponder** (Necromancy is irrelevant to the race clock); keep Fated Firepower.
3. **If you actually want BDD-like combo speed (T6–7),** the levers the bench identifies are, in order:
   (a) **add a standalone Seething Song** — un-gates Combo B so all three instant-tutors reach it
   (today only Emeritus can); (b) **more tutors**, especially any-card ones; (c) **fast mana**
   (Sol Ring etc.). That is a deliberate move toward a B4 combo deck and away from our B3 race
   identity — a real choice, not a free upgrade.
4. **Independent doc fix:** the Summary's "Infinite combo: None / Reiterate is finite" is wrong —
   both combos are live (user-blessed 2026-06-18). Reframe as a combo-race hybrid whose combo is a
   ~T10, once-in-3–4-games bonus, with the race (decap T8 / table T10) as the primary plan.

## 6. The GC-neutral "fast" direction (`--mode fast`) — RECOMMENDED over the cantrip swap

All three combo-speed levers can be pulled **without touching the 3/3 GC cap**: Sol Ring, Seething
Song, Solve the Equation and Merchant Scroll are **none of them Game Changers** (the premium tutors —
Demonic/Vampiric/Mystical Tutor, Imperial Seal, Gifts, Intuition — and fast mana — Mana Vault, Moxen,
Grim Monolith — all *are*, which is the wall). The clean package, **all owned spares deployed in zero
other decks**:

> **fast3 (GC-neutral, 3/3 held, 99→99):**
> **−Fated Firepower −Necromancy −Leyline Tyrant  +Seething Song +Solve the Equation +Merchant Scroll**
> Un-gates Combo B (a standalone instant Seething Song the instant-tutors can fetch) and takes tutors
> **4 → 6**.

```
COMBO go-off  P(CAST <= T) %   4    5    6    7    8    9   10   12   median
current                       0    5   13   17   21   24   27   32   never-in-14
fast3 (GC-neutral)            1    6   16   23   28   33   37   45   T14
fast4 (+Sol Ring, -E.Field)   2    7   18   24   29   33   37   45   T14
BDD expensive (reference)    10   28   47   55   61   66   70   77   T7

RACE clock                    decap / table medians
current                       T8 / T10   (table-by-T10 55%)
fast3                         T8 / T10   (table-by-T10 50%)   ← same small cost as dropping Fated Firepower
fast4                         T8 / T11   (cutting a pinger nudges the table clock out)
```

**Findings:**
1. **fast3 lifts the combo ~+37% in frequency** (by-T10 27%→37%; by-T12 32%→45%; median never→T14) for a
   negligible race cost (table front edge −5pp, medians held) — and it's **GC-neutral with owned spares**.
2. **fast4 / Sol Ring is not worth it.** Sol Ring barely moves the combo (+1–2pp — the line is
   tutor-gated, not mana-gated, confirmed again), and trading a pinger for it nudges the table clock to
   T11. **Drop Sol Ring; ship fast3.**
3. **The GC cap is the ceiling.** Even maxed GC-neutral we reach ~half BDD's combo frequency (37% vs
   70% by T10; median T14 vs T7). Closing the rest *requires* GC tutors + GC fast mana — i.e. abandoning
   the 3-GC B3 cap. So "BDD-fast without more GCs" buys a **meaningful but bounded** lift: the combo goes
   from a once-in-3–4-games bonus to roughly a coin-flip by T12, while the **race stays the primary plan**.

**Recommendation:** ship **fast3** as the Lightning War combo-direction upgrade (replaces the §1–§5
cantrip swap, which the lab killed). It's the most combo speed obtainable inside the 3-GC cap, costs
almost nothing on the race, and uses only owned, uncontested spares — and see §7, which makes it
race-neutral *and* faster by re-spending the weakest GC slot.

## 7. Is Jeska's Will the best GC? (`--mode gc`) — no; swap it for Mystical Tutor

The three current GCs are **Fierce Guardianship** (free protection — keep), **Opposition Agent**
(flash tutor-theft, aimed at the pod's tutor-combo decks — keep), and **Jeska's Will** (ritual +
impulse-3 — pure value, no disruption/protection). Since the lab shows the combo is **tutor-gated**,
the Jeska's Will *GC slot* is better spent on a GC tutor (GC count stays 3/3). On the fast3 base:

```
COMBO go-off  P(CAST <= T) %    6    8   10   12   median   RACE table by-T10 / median
fast3 (keep Jeska's Will)      16   28   37   45    T14      50% / T10
fast3, Jeska's -> Demonic       18   32   41   50    T13      49% / T11   (sorcery eats kill-turn mana)
fast3, Jeska's -> Mystical      17   31   41   50    T13      55% / T10   (cheap instant, race improves)
fast3, Jeska's -> Vampiric      18   32   41   50    T13      55% / T10
```

- Any GC tutor lifts the combo ~+4–5pp (median T14→T13). A **cheap instant** tutor (Mystical/Vampiric,
  {U}/{B}) also *improves the race front edge* (by-T10 50%→55%) by finding a finisher without competing
  for kill-turn mana; **Demonic Tutor** (sorcery) does the opposite and tips the race to T11.
- **Pick Mystical Tutor.** It's an **uncontested owned spare**, was previously in this very deck (cut
  for GC budget per the GC list), improves both clocks, and fast3's standalone Seething Song removes
  its only flaw (I/S-only can now reach Combo B). Vampiric Tutor is the more flexible alt (any-card,
  reaches the creature) but is contended and costs 2 life.

### FINAL recommended build — `fast3 + (Jeska's Will → Mystical Tutor)`
`−Fated Firepower −Necromancy −Leyline Tyrant −Jeska's Will / +Seething Song +Solve the Equation
+Merchant Scroll +Mystical Tutor` · 99 held · **GC 3/3** (Fierce Guardianship, Opposition Agent,
Mystical Tutor) · tutors **4 → 7** · almost all owned spares.

- **Combo by T10: 27% → 41%** (~+50% relative); median never-in-horizon → T13.
- **Race unchanged:** table by-T10 back to **55%** (Mystical Tutor repays the front edge that cutting
  Fated Firepower cost), decap T8 / table T10.
- Disruption identity intact (FG + Opposition Agent kept). Honest cost: Jeska's Will's high-roll
  mana/draw burst (a ceiling the goldfish flattens) — on the medians the tutor's consistency wins.

## 8. Also swap Opposition Agent? (`--mode gc2`) — yes IF the pod is low-tutor

User read: the pod doesn't run many tutors, so Opposition Agent (whose value is *opponents searching
their libraries*) is often a vanilla 3/2. If so, its GC slot is better spent on a **second** tutor.
On the §7 base (fast3 + Jeska's→Mystical), dropping Opposition Agent for a 2nd GC tutor (GC stays 3/3
= Fierce Guardianship + 2 tutors):

```
COMBO go-off  P(CAST <= T) %    6    8   10   12   median   RACE table by-T10 / median
base: keep Opposition Agent    17   31   41   50    T13      55% / T10
Opp.Agent -> Demonic Tutor      19   35   46   55    T11      55% / T10
Opp.Agent -> Vampiric Tutor     19   35   46   55    T11      60% / T10
Opp.Agent -> Gifts Ungiven(buy) 22   39   50   59    T11      60% / T10
```

**⚠ The labs cannot see Opposition Agent's disruption** (stealing an opponent's tutor can win/stop a
game outright); the "free upside" above is a goldfish artefact. The trade is only sound on the
**low-tutor pod read** — a real-world judgement, not a lab output.

- The 2nd tutor adds ~+5pp combo (by-T10 41%→46%, median T13→T11). **Gifts Ungiven** (a buy) is best
  (+9pp, by-T10 50%) — it's the *copyable* assembly tutor Azula doubles, BDD's engine. Among owned,
  **Vampiric Tutor** edges Demonic (any-card complement to Mystical's I/S-only; cheap instant; nudges
  the race up).

### FINAL build (combo-lean) — `fast3 + Jeska's→Mystical + Opposition Agent→[Vampiric | Gifts]`
`−Fated Firepower −Necromancy −Leyline Tyrant −Jeska's Will −Opposition Agent / +Seething Song
+Solve the Equation +Merchant Scroll +Mystical Tutor +[Vampiric Tutor (owned) | Gifts Ungiven (buy)]`
· 99 held · **GC 3/3** (Fierce Guardianship + 2 tutors) · tutors **4 → 8**.
- **Combo by T10: 27% → 46% (Vampiric) / 50% (Gifts)** — ~doubled vs current.
- **Race:** unchanged-to-better (table by-T10 55–60%).
- **Identity shift:** "disruption race" → "**protected combo that races as backup**" (Fierce
  Guardianship is now the sole disruption GC, protecting the kill). Justified by the low-tutor pod.

## 9. Focus pass — "cut the fat" (BDD lesson #1), applied in two tiers

The combo lab can't score situational cards, so this is a judgement pass: does each card *advance the
combo*, *protect the kill*, or *carry the backup race*? If it only answers the board or runs a third
axis, it's fat. **Tier 1** = clear fat; **Tier 2** = lean-dependent (cut when committing to combo).

| Cut | Tier | Why it's fat | Fill |
|---|---|---|---|
| Vandalblast | 1 | artifact-only hate, dead vs non-artifact pods | Ponder |
| V.A.T.S. | 1 | 4-mana board removal; combo doesn't clear boards | Preordain |
| Snap | 1 | low-impact bounce/tempo | Brainstorm |
| High Fae Trickster | 1 | redundant 3rd flash enabler (2 cover the sorcery finishers) | Spell Pierce |
| Toxic Deluge | 2 | board wipe a combo rarely wants (burn still answers Abolisher) | Sol Ring |
| Past in Flames | 2 | redundant yard-recursion (Yawgmoth's Will + 8 tutors remain) | Dispel |
| Ozai, the Phoenix King | 2 | 6-mana tertiary retention body; combo makes its own mana | Opt |

Kept as core (NOT fat): Twinning Staff (amplifies the combo copies too), Galvanic Iteration /
Increasing Vengeance, Yawgmoth's Will (the one yard-recursion), the counter suite, the 3 pingers.

## 10. FINAL consolidated build (12-for-12) — kept as PROPOSAL (not applied)

```
CUT (12)                          ADD (12)
A combo-lean  Fated Firepower      Seething Song
              Necromancy           Solve the Equation
              Leyline Tyrant       Merchant Scroll
              Jeska's Will   (GC)   Mystical Tutor      (GC)
              Opposition Agent(GC)  Gifts Ungiven       (GC, BUY)
B Tier-1      Vandalblast          Ponder
              V.A.T.S.             Preordain
              Snap                 Brainstorm
              High Fae Trickster   Spell Pierce
C Tier-2      Toxic Deluge         Sol Ring
              Past in Flames       Dispel              (BUY)
              Ozai                 Opt
```
- **99 held · GC 3/3** = Fierce Guardianship, Gifts Ungiven, Mystical Tutor (−Jeska's Will −Opposition
  Agent +Mystical +Gifts). **Buys: Gifts Ungiven + Dispel (~$4)**; other 10 adds owned.
- **Clocks (40k):** combo by-T10 **27%→54%** (median never→T10); race decap **T8→T7**, table T10
  (front edge 55%→67%). Layer A is ~90% of the lift; B+C tighten + add unmeasured hand-quality/focus.
- **Identity:** protected combo (combo ~doubled) racing as backup; Fierce Guardianship guards the kill.

**Status: proposal of record — not applied to `lightning-war-20260614.txt` or the Summary.** When
applied: bump `.txt` to today, archive the old, recount to 100, and rewrite the Summary's
combo/Bracket/GC sections (and fix the false "no infinite combo" line).

## 11. Mana-base color audit (the labs are color-blind — verify by hand)

The labs model total CMC/mana (so the curve affects the clocks) but **not colored pips**. The full
build quietly flips the deck **red-primary → blue-primary**:

```
nonland colored pips   U     B     R        curve avg CMC
CURRENT               30    10    35        2.23   (red-primary)
FULL build            38     5    29        2.02   (BLUE-primary, LOWER curve)
land color sources     U:18  B:20  R:19  (unchanged; ~20/33 access blue incl. Polluted Delta/Scalding Tarn fetches)
```

Curve is fine (it dropped). The watch-item is **blue is now most-demanded (38 pips) but tied-fewest
sourced**, and you can't ritual/Firebend into blue (BDD's explicit warning). Black is now massively
over-served (5 pips / 20 sources) — that's the slack to spend. Mild tension, not a crisis — but it is
the one dimension the labs structurally cannot check. **Finalized fix (blue +2 / black −2, both owned):**
- **−Bloodstained Mire → +Misty Rainforest** (owned ×3): a blue fetch — grabs Island / Watery Grave /
  Steam Vents and keeps Brainstorm/Ponder shuffle support that Bloodstained Mire's B/R fetch wasted.
- **−Shizo, Death's Storehouse → +Fiery Islet** (owned spare, **zero contention**): a U/R horizon land
  (verified produces {U}/{R}); adds a blue source on-color and cantrips late.

## 12. Graveyard recursion — REVERSE the Past in Flames cut + add Invoke Calamity

The §9 focus pass cut Past in Flames as "redundant," but that was wrong in the same build that **adds
Gifts Ungiven**, whose power *is* recasting the opponent-binned half from the yard (BDD's line). The
deck already runs **Snapcaster Mage + Past in Flames + Yawgmoth's Will** — a real Grixis spell-
recursion suite that also rebuys combo pieces lost to Frantic Search / Faithless Looting / Brainstorm.

- **Keep Past in Flames** (un-cut; drop the Dispel that replaced it).
- **Add Invoke Calamity** (owned, non-GC): an **instant** → Azula copies it → cast up to **four** I/S
  spells free from yard/hand. The best Gifts-enabler/combo-recursion piece for this deck; BDD runs it.
  Brought in for **Opt** (weakest grease).

Recursion suite → Snapcaster + Yawgmoth's Will + Past in Flames + Invoke Calamity; **GC still 3/3**.

**Lab built to see it (`--mode recur`, 40k):** the combo sim now models a yard (an I/S piece is
castable while a recursion enabler is in hand) and Gifts binning the pieces you need. Result:

```
COMBO go-off  P(CAST <= T) %                    6    8   10   12   median
FINAL build, recursion modeled OFF (old)       25   41   50   58    T10
FINAL build, recursion modeled ON              25   42   52   60    T10
  vs w/o Past in Flames + Invoke Calamity, ON   25   42   52   59    T10
```

**Honest read: recursion barely moves the goldfish clock (~+2pp), and the recursion *cards* add ~0 to
combo SPEED** — in a disruption-free goldfish you rarely *lose* pieces. Recursion's job (recover from
counters/discard/mill, make Gifts' adversarially-binned pile live) is **resilience, not speed**. Unlike
opponent disruption — which the resilience labs DO measure (§13) — graveyard-recursion-as-reassembly
isn't captured even by delay_lab (it says so explicitly), so it stays a hand call like the colors (§11).
Keep it for reliability + Gifts-enabling. Graveyard-hate (RiP / Leyline of the Void) is the exposure,
but the primary combos don't need the yard, so this is redundancy, not dependence.

## 13. Resilience IS measurable — delay_lab on the build (the Opposition Agent cost)

Correction to §8/§9's "labs can't see disruption": the goldfish can't, but `pod_gauntlet` /
`delay_lab` / `interaction_meta` do. pod_gauntlet scores current LW **disruption-LED** (PURE RACE 12%
→ P(WIN) 37%). Re-running delay_lab on the new answer suite (−Opposition Agent −V.A.T.S. −Snap
−Toxic Deluge, +Spell Pierce + 3 tutors) — composed P(disrupt their T6), across P(Abolisher out):

```
P(Abolisher out)            0%   25%   50%   75%  100%
CURRENT (8 ctr, 1 static)   81   67    52    38    23
NEW build (9 ctr, 0 stat)   83   66    48    31    14
```

- **No Abolisher:** new build disrupts *slightly better* (more counters + tutors find them).
- **Behind Abolisher:** new build is **−4 to −9pp** — cutting Opposition Agent leaves **0 statics**,
  the only answer class that survives Abolisher. Since the pod combos behind Abolisher, this is real.

**But the compensation is Abolisher-immune:** our combo kills on OUR turn (Abolisher only stops us on
THEIRS) and Banefire X≥5 is uncounterable under Fierce Guardianship. So the build trades Abolisher-
proof *disruption* for an Abolisher-proof, faster *combo* — exactly the deck's founding "race, don't
lock" thesis, flipping it from disruption-led to race-led.

**pod_gauntlet net (CLOSED 2026-06-19, user committed to the race).** Fed the new combined (combo ∪
race) decap clock + the measured new disruption into `pod_gauntlet.simulate`:

```
P(WIN vs pod)                     a=0   .25  .30   .50  .75  1.0   pure_race
CURRENT LW                         55   40   38   30   22   17       12%
NEW build (conservative combine)   74   65   64   58   52   48       44%
NEW build (optimistic combine)     81   74   73   68   64   60       56%
decompose @a=.3:  new clock + OLD disrupt = 68% (+30) · OLD clock + new disrupt = 32% (-6)
```

**The clock gain (+30pp) dwarfs the disruption loss (−6pp) → net +26pp P(WIN), ~38% → ~64%**, and the
build wins even with Abolisher always out (17%→48%) because the kill is on our turn. Caveat: most of
the clock gain is the *race* speeding up (6 tutors + Sol Ring; the race lab credits tutors generously),
so trust the **direction + decomposition** over the absolute; even combo-only lifts pure-race 12%→~30%.
**Decision: COMMIT to the race build (final, 0 statics).** The −6pp static loss is the measured,
accepted cost; the deck is now decisively race-led, as its founding thesis intended.

### Revised consolidated changes vs §10
- **Un-cut:** Past in Flames stays (was a Tier-2 cut). **−Dispel** (its replacement) from the add list.
- **Swap:** −Opt **+Invoke Calamity** (recursion over grease).
- **Lands (+2 blue / −2 black):** −Bloodstained Mire, −Shizo (or a BR dual) → +blue fetch/dual ×2.
- Net still **GC 3/3** (Fierce Guardianship, Gifts Ungiven, Mystical Tutor); buys unchanged
  (Gifts Ungiven + the blue land(s) if not owned).
