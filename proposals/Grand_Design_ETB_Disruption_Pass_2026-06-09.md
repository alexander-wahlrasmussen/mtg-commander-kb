# The Grand Design — ETB Disruption / ETB-Tutor Optimization Pass

**Date:** 2026-06-09
**Ask:** Add **creatures that trigger on ETB — tutoring or control** — to disrupt the arch-enemy's plan *while* we build ours. The clock is what it is; trading a slot for proactive disruption is acceptable if it's engine-findable.
**Card text verified** via `card_lookup.py` for every add and cut. **GC checked** (`REF_Game_Changers_List.md`): all adds are non-GC; deck stays **3/3** (Force of Will, Rhystic Study, Cyclonic Rift). **Ownership / cross-deck** checked against `moxfield_haves_2026-06-07-1031Z.csv` + `decks/*.txt`. **Reskin check**: none of the adds are UB reskins. **Count:** 4-for-4 → 100 held.

> **Bottom line:** Your instinct is the *same structural insight* behind the pending finisher pass, generalized. Atraxa's deck is an ETB-payoff machine — Panharmonicon + Elesh Norn double every ETB, 6 flicker outlets re-fire them, and Pod/Chord/Eladamri's/Defense/Razaketh all fetch creatures. It currently spends that infrastructure almost entirely on *value*, not *disruption*. Adding ETB **removal-on-a-stick** (Skyclave Apparition, Noxious Gearhulk) and ETB **tutors** (Spellseeker, Fierce Empath) turns the engine into repeatable, proactive interaction that **survives the pod's Grand Abolisher** (you deploy it on *your* turn / via Pod / via reanimate, pre-empting their combo turn). The recommended $0-core + $3 package is **4-for-4, stays 3/3 GC and 100 cards**, and the sim says it **does not worsen the deck's thin colour floor**.

---

## 1. Why ETB creatures are the right axis for *this* deck

The deck already runs the most expensive half of an ETB-abuse engine and underuses it:

- **Doublers:** Panharmonicon + Elesh Norn → each ETB fires up to 3×.
- **6 flicker outlets** (Ephemerate, Thassa, Soulherder, Panharmonicon, Restoration Angel, Displacer Kitten) re-trigger any ETB.
- **5 creature-tutors** (Birthing Pod, Chord of Calling, Eladamri's Call, Defense of the Heart, Razaketh) + the 5–7 cards Atraxa draws on entry — every one of them points at *creatures*.
- **5 reanimation spells + Karmic Guide** recur creatures from the bin.

Today that machine fetches/flickers/reanimates *value* (Eternal Witness, Sun Titan) and *bombs* (Razaketh, Vilis). It has **almost no flickerable/reanimatable ETB disruption**, and — per the Summary's own 4/5 Interaction note — **cannot tutor for its noncreature interaction at all**. ETB creatures fix both: a removal-on-a-stick becomes *repeatable removal*; a tutor-on-a-stick becomes a *repeatable tutor*; both are findable by the engine you already paid for.

### Why this beats "more counterspells" against the pod

Per `project_pod_combo_opponent` + `feedback_grand_abolisher_blocks_counters`: the arch-enemy wins T6–7 **behind Grand Abolisher**, which blanks every counterspell and instant on their combo turn. What survives is **static-already-in-play, triggered abilities, and removal cast before they untap.** ETB removal you deploy on *your* turn (or via Pod's activated ability, or by reanimating onto the battlefield) is exactly that — it kills the Abolisher / their mana rock / their combo permanent **pre-emptively**, and it doesn't care that counters are dead.

---

## 2. The candidate pool (all text-verified)

WUBG-legal, **non-GC** (Opposition Agent, Drannith Magistrate, Notion Thief are GCs — deliberately excluded to hold 3/3). Owned = free copies after current deployments.

### Control / disruption ETBs

| Card | Cost | MV | ETB effect (verified) | Owned (free) | Anti-pod value |
|---|---|---|---|---|---|
| **Skyclave Apparition** | {1}{W}{W} | 3 | Exile up to one **nonland, nontoken permanent you don't control, MV ≤ 4**. (LTB: owner makes an X/X Illusion = exiled MV.) | **1 free ($0)** | ★ Hits **Grand Abolisher (2), Sol Ring/Signet, Kinnan (3), Rhystic, planeswalkers, combo enchant/artifacts**. Can't touch Ur-Dragon (MV 9). Pod MV3, reanimatable, flickerable. |
| **Noxious Gearhulk** | {4}{B}{B} | 6 | May destroy **another target creature** (any colour); gain life = its toughness. | **2 free ($0)** | Unrestricted creature kill + lifegain. **Pod MV6 → bridges to Atraxa/Elesh Norn.** Reanimatable. |
| **Shriekmaw** | {4}{B}, evoke {1}{B} | 5 | Destroy target **nonblack, nonartifact** creature. | buy ~$1 | Cheap evoke removal; misses black/artifact combo creatures. Lower colour strain than Noxious. |
| **Agent of Treachery** | {5}{U}{U} | 7 | **Gain control of target permanent** (indefinite). Draw 3 each end step if you control 3+ stolen permanents. | buy ~$2 | ★ Steal their **Abolisher / mana rock / combo piece** and keep it. Flicker = re-steal. Pod MV7, reanimatable. |
| **Plague Engineer** | {2}{B} | 3 | Choose a creature type; **opponents'** creatures of that type get −1/−1 (**static, deathtouch body**). | buy ~$4 | Survives Abolisher (already static). Wrecks **Ur-Dragon (Dragons)** and go-wide/token Kinnan; narrow vs pure combo (Hidetsugu/Kairi). Meta call. |
| **Venser, Shaper Savant** | {2}{U}{U} | 4 | Flash. Return target **spell or permanent** to hand — *works even on uncounterable spells*. | 1 (in Calamity Tax) → buy ~$8 | Bounces a combo finisher off the stack or a permanent; legendary. Flash-cast is dead under their Abolisher, but on your turn / flickered it's flexible. |
| **Solitude** | {3}{W}{W}, evoke (pitch a white card) | 5 | Flash, lifelink. Exile up to one other creature (controller gains life = its power). | 2 (both deployed) → buy ~$35 | Premium free removal; flickerable/reanimatable to keep it. Expensive + fully spoken-for. |

### Tutor ETBs

| Card | Cost | MV | ETB effect (verified) | Owned (free) | Role |
|---|---|---|---|---|---|
| **Spellseeker** | {2}{U} | 3 | Search an **instant/sorcery MV ≤ 2** to hand. | buy ~$3 | ★ **Closes the 4/5 Interaction ceiling.** Fetches Counterspell, Mana Drain, Swan Song, Dovin's Veto, Path, Swords, Veil, Assassin's Trophy, *or* Reanimate/Animate Dead/Nature's Lore/Farseek. A **creature** that finds noncreature answers → itself Pod/Chord/Recruiter-able and repeatable on flicker. |
| **Fierce Empath** | {2}{G} | 3 | Search a **creature MV ≥ 6** to hand. | **1 free ($0)** | Finds Razaketh / Vilis / Elesh Norn / Atraxa / Noxious (/ Craterhoof). Consistency for the reanimator targets and bombs. Pod MV3, flickerable. |
| **Recruiter of the Guard** | {2}{W} | 3 | Search a creature **toughness ≤ 2** to hand. | 2 (both deployed) → buy ~$2 | Toolbox: fetch **Grand Abolisher / Glen Elendra / Skyclave / Spellseeker / Birds / Fauna**. Note: **can't** grab Ranger-Captain (3/3) or the big bombs. Repeatable on flicker. |

---

## 3. Recommended package — balanced 2-control + 2-tutor (4-for-4)

Exactly what you asked for: two **control** ETBs and two **tutor** ETBs, all engine-findable. **$3 total** (Spellseeker buy); the other three are owned and free. Stays **100 cards, 3/3 GC**.

| OUT | IN | Cost | Role |
|---|---|---|---|
| Grisly Salvage | **Skyclave Apparition** | $0 (1 free) | Flagship ETB disruptor — exiles Abolisher/rock/Kinnan/combo permanents MV≤4; the single best anti-pod ETB. |
| Ghostly Flicker | **Spellseeker** | ~$3 (buy) | ETB interaction-tutor — makes the deck's noncreature answers *tutorable* for the first time; repeatable on flicker. |
| Dread Return | **Noxious Gearhulk** | $0 (2 free) | ETB removal + lifegain (any creature); Pod MV6 bridge; reanimatable. |
| Persist | **Fierce Empath** | $0 (1 free) | ETB tutor for the MV≥6 bombs; feeds the reanimator. |

**Cut rationale (all spells — no colour source lost; verified):**
- *Grisly Salvage* ({B}{G} instant) — the ~15%-per-cast random binner the speed analysis already flagged; Buried Alive (deterministic) + Fauna Shaman remain as graveyard fill.
- *Ghostly Flicker* ({2}{U} instant) — narrowest flicker (needs **two** targets, can't blink a lone creature); 5 flicker outlets remain to re-fire every new ETB.
- *Dread Return* ({2}{B}{B} sorcery) + *Persist* ({1}{B} sorcery) — the two weakest reanimation spells. Reanimators go 7→5 (Reanimate, Animate Dead, Necromancy, Victimize, Living Death) + Karmic Guide; Persist's nonlegendary-only restriction made it the thinnest, Dread Return's 3-creature flashback the clunkiest. The new ETB creatures give the *remaining* reanimates better targets.

**Net effect:** creatures 19 → 23 (more Pod fuel, more Chord/Recruiter targets, more reanimation payoffs); flicker outlets 7 → 6; reanimation spells 7 → 5. All three pools stay healthy.

### Simulation (`gd_speed_lab.py --mode etb`, 40k trials)

**Risk — colour floor is unchanged (the swap is land-neutral):**

| | nonland avg CMC | all-colours-from-lands T6 | "has a play" T2 |
|---|---|---|---|
| CURRENT | 2.983 | 90% | 92% |
| PROPOSED | 3.050 | **90% (identical)** | 90% |

> **Correction (2026-06-09, later same day):** this section originally read 39% — a `deck_sim.py` measurement artifact (sac-fetches and rainbow lands scored as zero-colour). The model was fixed and the table above shows corrected values; the *land-neutral* verdict is unchanged. The deck's mana base is healthy — see `Grand_Design_Mana_Fixing_Pass_2026-06-09.md`.

The colour floor is **not made worse** — no lands change, and avg CMC ticks up only +0.07. (Caveat: the sim measures *land* colour sources; the two double-pip adds, WW + BB, do raise the *board* colour requirement to hardcast — but both are designed to be **cheated in** via Pod/reanimate, not hardcast. See §6.)

**Gain — a brand-new proactive-removal axis the current deck lacks:**

| P(≥1 of Skyclave/Noxious available) | T4 | **T6** | T8 |
|---|---|---|---|
| drawn | 18 | 22 | 25 |
| **+ creature-tutors (Pod/Chord/Eladamri's)** | 40 | **47** | 53 |

≈**47% by T6** you can deploy — then flicker/reanimate — a removal-on-a-stick aimed at the Abolisher or a combo piece. (Defense of the Heart and Razaketh, not counted here, add more.) This mirrors the finisher pass's Craterhoof figure: same engine, same ~4× leverage.

**Gain — the 4/5 Interaction ceiling, addressed:** the Summary caps Interaction at 4/5 because *no tutor can find noncreature interaction*. Spellseeker is the creature-shaped fix — **~40% by T6** to have it online via the engine, and because it's a creature, flicker re-fires the tutor. (The deck still usually *draws* an answer — ~65% by T6 — so the win here is **specificity + repeatability**: digging to the *right* answer on demand, not raw count.)

---

## 4. Optional upgrades / meta calls (beyond the core)

Swap these in over a core pick or a remaining weak card, per taste and budget:

- **Agent of Treachery (~$2)** — the highest-impact *control* add. Steal their engine and keep it; flicker re-steals. Best as a Pod-MV7 / reanimate target. **Swap idea:** over *Vilis, Broker of Blood* — both are top-end reanimator payoffs, but Agent *disrupts* (steal a permanent + draw) where Vilis only draws. Trade-off: loses the Vilis draw-engine / no-max-hand-size synergy.
- **Plague Engineer (~$4)** — bring it **specifically for the Ur-Dragon (Dragons)** night, or token/go-wide Kinnan. Static → survives Abolisher. Narrow vs Hidetsugu/Kairi. Sideboard-style meta call, not a default.
- **Recruiter of the Guard (~$2)** — if you want a *toolbox* tutor that fetches Grand Abolisher / Skyclave / Glen Elendra on demand (toughness ≤2 only). Repeatable on flicker.
- **Venser, Shaper Savant (~$8, contended w/ Calamity Tax)** — flexible flash bounce (even uncounterable spells). Buy a 2nd if you want it in both.
- **Solitude (~$35, fully deployed)** — premium, but expensive and already spoken-for across Exile's Return + Replication Crisis. Only if you're buying a third copy.

---

## 5. Reconciliation with the pending Finisher pass — *you can't fully do both*

The finisher pass (`Grand_Design_Finisher_Upgrade_2026-06-08.md`) and this pass **compete for the same ~5 cuttable slots**:

- **Finisher OUT:** Ghostly Flicker, Bloom Tender, Grisly Salvage → **IN:** Craterhoof, Pathbreaker Ibex, Grim Tutor
- **ETB OUT:** Grisly Salvage, Ghostly Flicker, Dread Return, Persist → **IN:** Skyclave, Spellseeker, Noxious, Fierce Empath

They overlap on **Ghostly Flicker + Grisly Salvage**. The deck only has ~5–6 genuinely cuttable cards, so applying both *in full* = 7 adds / 5 unique cuts = **breaks 100**. You must prioritize or merge.

**Recommended merged build (best of both, 4-for-4, $0+$3, holds 100 / 3/3 GC)** — note **Craterhoof is itself an ETB creature**, so it belongs to this same axis:

| OUT | IN | Why |
|---|---|---|
| Grisly Salvage | **Craterhoof Behemoth** ($0) | Fixes the single-finisher SPOF; ETB overrun the engine can finally fetch. |
| Ghostly Flicker | **Skyclave Apparition** ($0) | Anti-pod ETB disruptor. |
| Dread Return | **Spellseeker** (~$3) | Makes noncreature interaction tutorable. |
| Persist | **Noxious Gearhulk** ($0) | ETB removal + Pod MV6 bridge. |

This keeps Bloom Tender (the deck's best non-land colour fixer + ramp), banks the highest-leverage card from each pass, and adds **four ETB payoffs** (one finisher, one disruptor, one interaction-tutor, one removal). Fierce Empath / Pathbreaker Ibex / Grim Tutor become the next-tier options if you later free a slot.

---

## 6. Honest caveats

1. **This does not speed the clock.** Per `Grand_Design_Speed_Curve_Analysis.md`, the deck's kills are mana/setup-gated; nothing here changes avg CMC meaningfully (+0.07). This pass buys **disruption + reliability of having the right answer**, exactly the "disrupt their plan while building ours" trade you asked for — not a faster goldfish.
2. **Double-pip board cost.** WW (Skyclave) and BB (Noxious) raise the *hardcast* colour requirement. The sim shows the *land* floor is unchanged (90% T6 both builds, corrected model), and the real mitigation is that **both are meant to be Pod'd / reanimated / flickered in, not hardcast.** *(The "fixing pass is higher priority" line that originally stood here is withdrawn — the mana-fixing pass closed 2026-06-09 with no changes needed; the 39% that motivated it was a model artifact. See `Grand_Design_Mana_Fixing_Pass_2026-06-09.md`.)*
3. **Skyclave caps at MV ≤ 4** — it cannot exile Ur-Dragon (MV 9) or other fat threats; it's a *combo-permanent / hatebear / rock* answer, not a catch-all. Noxious covers the big creatures.
4. **Under an enemy Abolisher, the *cast* lines are still dead** (Solitude/Shriekmaw evoke, Venser flash, hardcasting any of them on their turn). The value is **pre-emptive deployment + the activated/triggered engine** (Pod, reanimate-on-your-turn, flicker), which is what survives. Kill the Abolisher on *your* turn before they combo.
5. `gd_speed_lab.py --mode etb` is a **card-availability model** — it ignores mana and the board. "Available" ≠ "resolved removal that turn." Trust the deltas, not the second decimal.

---

## 7. Next step

Not applied to the `.txt` — proposal only. On approval: pick **the §3 ETB package** *or* **the §5 merged build**, apply the 4-for-4, bump the dated filename (`the-grand-design-<today>.txt`), archive the old list, recount to 100, and update the Summary (add the ETB toolbox to the interaction section; if merged, fold Craterhoof in as co-primary finisher per the finisher pass).

---

Related: `Grand_Design_Finisher_Upgrade_2026-06-08.md` (shared cut slots — §5) · `Grand_Design_Speed_Curve_Analysis.md` (clock is mana-gated) · `Pod_Matchup_Matrix.md` (fix the mana base first) · [[project_pod_combo_opponent]] · [[feedback_grand_abolisher_blocks_counters]] · [[feedback_bracket_4_in_spirit]]
