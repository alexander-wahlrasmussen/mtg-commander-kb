# Pod Matchup Matrix — Roster vs. The Archenemy (combo decks + Ur-Dragon)

How each active deck matches up against the recurring pod combo opponent. This is
a **decision aid**, not a guarantee — it combines audited kill windows, the
interaction profile of each deck, and Monte Carlo consistency output from
`scripts/deck_sim.py`. State doc, not reference: re-derive when a deck's score,
clock, or interaction suite changes.

> **Two opponents, two models.** The main table races his **combo** decks (Acererak /
> Hidetsugu and Kairi / 5C tail) — a decap race. His **Ur-Dragon** deck is the odd one out:
> it's a *fair board deck*, not a combo, so there's no combo turn K to race and the decap
> model is the wrong shape. It gets its own **computed** section below — **"The other axis —
> vs his Ur-Dragon"** (`vs_dragon_roster_lab.py`, per-deck) — where the ranking largely
> **inverts**: the split is **board-independent kill** (goes over the flying wall — wins) vs
> **combat kill** (walled). Board-independent *damage* decks (Radiation, Genome, Lightning
> War) win **both** matchups; the **combat** decks near the top of the combo table get walled.

> **Rebuilt 2026-06-15 — the two-deck model (`--vs`).** The table now races each deck
> **separately vs his real decks** — Acererak (mono-B ETB), Hidetsugu and Kairi (UB death),
> and the 5C tail — then blends them by how often he brings each (`pod_gauntlet.py --matrix`
> emits the `--vs` rows). This replaces the old single generic-combo `P(win)` column and folds
> in two corrections: the **Grand Abolisher color-lock** (his two mains can't run the white
> Abolisher, so reactive decks recover) and **protect-own** (a deck's own counters / a counter-
> immune kill, which the flat model ignored). Biggest movers: **Replication Crisis → #2**,
> **Lightning War up**, **Grand Design re-cast as an anti-Acererak *controller*** (its Elesh
> Norn lock, `--vs-lock`). Clock medians stay lab-sourced; the verdicts remain judgment.

Last built: **2026-06-01**. Rebuilt **2026-06-05** — sim refreshed (20k trials/deck); all reskins now resolve, **zero unresolved cards** across the 16 active decks; Replication Crisis row updated for the pending Kiki swap. Rebuilt **2026-06-09** — **land-colour model fixed** (`deck_sim.py` previously scored sac-fetches and rainbow lands as zero-colour sources via empty `color_identity`; now uses `produced_mana` + fetch resolution — see `archive/proposals/Grand_Design_Mana_Fixing_Pass_2026-06-09.md`). All Colour-T6 figures re-derived; finding #2 and recommendation #2 retracted/rewritten. Replication Crisis clock re-derived **2026-06-09** via the `scripts/rc_speed_lab.py` goldfish combat lab (`analysis/Replication_Crisis_Speed_Curve_Analysis.md`). Exile's Return clock re-derived **2026-06-09** via `scripts/er_speed_lab.py` (`analysis/Exiles_Return_Speed_Curve_Analysis.md`) — Clock flag downgraded, verdict held on the disruption axis. **Reconciled 2026-06-13** — every Clock cell replaced with the kill-window sweep's lab-measured decap/table (`campaigns/Kill_Window_Lab_Sweep_2026-06-13.md`); the pre-sweep hand-estimates (the "T7–9" cluster) were systematically optimistic, mostly by conflating decap with table. **The Loam Cycle removed** (retired/dismantled 2026-06-08); **Zero-Sum Game added** (built 2026-06-11). Verdicts mostly held (they rest on the disruption axis, which the new clocks don't change) — the substantive shifts are Lightning War "✅ races" → chip/tempo-assisted (goldfish decap T9) and Calamity "T7–9" → T13 (oppression, not speed). **Audited & reordered 2026-06-14** — quantitative columns regenerated from the labs (`pod_gauntlet.py --matrix`) and **reordered by `P(win)`**; the narrated "Beats T6–7?" cells replaced with lab `P(decap ≤ 6/7)`; three clock drifts fixed (Earthbend table T12→T11, LW table ~T13→T14, GD/DR tables "T12+"→ median never-in-horizon); Lightning War's "disruption" reclassified as **protect-own** (race-protection, not combo-disruption). Companion **self-meta** ranking (roster as its own field): `campaigns/Self_Meta_Ranking.md`. **Measured disruption 2026-06-15** — the `P(win)` disruption term is now **delay_lab-measured for all 16** (was class-bucketed for 13); `analysis/delay_disruption.json` + writeup `analysis/Measured_Disruption_All16_2026-06-15.md`. Reorder: **Replication Crisis 4th→3rd** (under-bucketed "none" 15% → measured 50%), **Genome 1st→2nd** (over-bucketed; its rank is now a *race* rank, D 16%), Earthbend up (15→38%), Diminishing/Crystal down (over-bucketed). The `warn`/`none` bucket is retired. **Opponent model split 2026-06-15** — the generic single combo opponent is resolved into his two real decks (**Acererak** mono-B ETB loop / **Hidetsugu and Kairi** UB death-drain) + a 5C tail; see the rewritten "opponent" section and `pod_gauntlet.py --vs`. Load-bearing correction: **his two current decks are color-locked out of the white Grand Abolisher**, so the counterspells-are-dead premise applies only to the 5C tail — reactive decks recover value vs his current meta. **Matrix table rebuilt to the two-deck `--vs` model 2026-06-15** — per-opponent (Acererak / H&K / 5C-tail) columns + blend + a **protect-own** term (grep-verified counters + counter-immune kills) replace the single-opponent `P(win)`; **Replication Crisis → #2** (its counters/board-kill were under-rated), **Lightning War up** (counter-war + uncounterable Banefire), **Grand Design** re-cast as the anti-Acererak controller (30% race → 45%/59%-vs-Acererak with its Elesh Norn lock, `--vs-lock`). **Ur-Dragon axis added 2026-06-15** — his one *fair* deck gets its own inverted section ("The other axis"), since the decap-race model above is the wrong shape for a board deck. **First archetype-tiered, then COMPUTED per deck** (`scripts/vs_dragon_roster_lab.py`, 40k — a survival race: lab kill-clock + oracle-measured anti-dragon toolkit + a verified *over/combat* kill axis; priors swept; `analysis/vs_dragon_roster.json`). Doing the math **corrected two judgment calls** (Grand Design is the WORST here, 14% — combat kill walled by flyers; Genome 99% / Lightning War 83% are NOT walled — board-independent damage races over the wall). Cross-checked vs `scripts/vs_dragon_lab.py` (Glarb ~87% heads-up; deck packages +2–3pp marginal) and `analysis/Calamity_Tax_vs_Ur_Dragon_2026-06-15.md`. The real split is **board-independent vs combat kill** (not grind vs race); **Radiation Sickness (99% + #1 combo)** is the standout both-ways hedge.

---

## The opponent we're tuning against

From the pod profile (memory `project_pod_combo_opponent`, **updated 2026-06-15
from Alex's direct report — card text verified**). He is **not** a generic combo
pod; he has a small stable, and the two decks he actually brings now are:

- **Acererak the Archlich** ({2}{B}, **mono-B**) — *his favorite.* Engine is its
  **ETB trigger** (recast → venture, repeatedly); the kill is a damage/drain
  **loop** off the dungeon's "each player loses life" rooms — not a Thassa's
  Oracle deckout.
- **Hidetsugu and Kairi** ({2}{U}{U}{B}, **UB** — *one* commander, not the two
  the old profile mis-split into "Hidetsugu" + "Kairi, the Swirling Sky") — *the
  recent flood.* Engine is its **death trigger**: each death drains an opponent
  for the top card's mana value. Loops on a sac outlet + recursion.
- A legacy **5C tail** (Ur-Dragon / Kenrith / Kinnan) from the 2026-05-30
  profile — status unconfirmed in the current meta. **Note:** the 5C-tail *column*
  in the matrix below models the **combo** potential of these shells (Kenrith/Kinnan
  loops + the one place he can field the white Grand Abolisher). His **Ur-Dragon** build
  is a *fair board deck*, not a combo, and is handled separately in the
  **"The other axis — vs his Ur-Dragon"** section below — don't read the 5C-tail combo
  column as the Ur-Dragon matchup; they invert.

He **wins T6–7**. Bracket-4-in-spirit despite a low GC count.

### The correction that reframes this whole doc

The old "single most important fact" here was *their Grand Abolisher makes your
counterspells dead on the combo turn.* **That is now true only of the 5C tail.**
Grand Abolisher is **white**, and **Acererak (mono-B) and Hidetsugu and Kairi
(UB) are color-locked out of it.** So against his two *current* decks:

- **vs Acererak** — no Abolisher *and* no counterspells in mono-B. Your reactive
  answers (counters, instant removal) **almost all live**; the threats are his
  *speed* and proactive **discard** stripping your answer pre-combo.
- **vs Hidetsugu and Kairi** — no Abolisher, but a real **UB counter wall** (Force
  of Will / Swan Song / Fierce Guardianship / Mana Drain). Your answers fight
  theirs **1-for-1** — there is no blanket lock.
- **vs the 5C tail** — the original Abolisher logic still applies; only these
  shells can field it.

So the matchup is decided **per-deck**, by:

1. **Clock** — do you kill at or before T6–7?
2. **Interaction read against the *right* protection** — a counter wall (H&K) or
   discard+speed (Acererak), **not** a universal Abolisher lock. Reactive/counter
   decks are worth **more** vs his two mains than this doc previously assumed.
3. **The right static for the right loop** — and there is **no single one**,
   because his two mains loop through **different triggers**:

| static | Acererak (ETB) | H&K (death) | 5C tail |
|---|---|---|---|
| Torpor Orb / Hushwing Gryff | **hard lock** | **stone blank** | partial |
| Rule of Law (one spell/turn) | hits | hits | hits |
| Drannith Magistrate | soft (CZ recast only) | soft | soft |
| Cursed Totem | blank | weak | weak |

ETB-hate hard-locks Acererak and does **nothing** to H&K; only Rule of Law-class
+ exile-the-commander-on-sight + **racing** hit both. Damage-loop kills also mean
**lifegain is a trap** (infinite drain beats any life total) and Thoracle/tutor
hate (Mindcensor) is low value.

**Quantified:** `python scripts/pod_gauntlet.py --vs` races every roster deck vs
Acererak / H&K / 5C-tail separately and blended, with the per-deck interaction
term; the **Δ(Acrk−H&K)** column shows how much each matchup swings on which deck
he brings (reactive decks swing most: Lightning War +18, Replication +13). The
weights and interaction levels there are **priors, not measured** — tune freely.

> **The table below is the `--vs` two-deck model** — each deck raced per-opponent
> (Acererak / H&K / 5C-tail) + blended, with the colour-lock and protect-own
> corrections baked in. The per-row verdict is judgment layered on those numbers.

---

## The matrix

**Rows ordered by blended `P(win)`** from the two-deck model (`pod_gauntlet.py --vs`,
pasted by `--matrix`). Each deck is raced **separately vs Acererak, Hidetsugu and Kairi,
and the 5C tail**, then blended by how often he brings each (priors **0.45 / 0.40 / 0.15**):

- **Clock** = lab decap / table median (`analysis/pod_gauntlet_clocks.json`).
- **prot** = *protect-own* — P(this deck forces its kill THROUGH their reactive answer):
  its own counters (grep-verified count) + a **counter-immune kill** (board-state /
  uncounterable finisher). This is exactly what the old flat model ignored.
- **vs Acererak / H&K / 5C-tail** = `simulate_vs` per opponent; **BLEND** = the weighted avg.

> **Read the blend with its priors and biases.** (1) The clock is an **unblocked goldfish
> ceiling**, so fast decks read optimistically; (2) the **weights / answer / protect** values
> are PRIORS — tune as you log real games; (3) the blend is a **decap race**, so it
> **under-rates control decks that LOCK rather than race** — Grand Design reads 30% here but
> **45% blend / 59% vs Acererak** once its Elesh Norn ETB-lock is modelled (`--vs-lock`). Read
> the **per-opponent spread and the verdict**, not the blend alone. The roster-wide pattern:
> **everyone is strongest vs Acererak** (his favorite — mono-B, no counters) **and weakest vs
> Hidetsugu and Kairi** (the UB counter wall) — H&K is the table's real problem deck. Colour-T6
> floors (lands-only, `deck_sim`) are a uniform 88–99% and don't differentiate (dropped).

| # | Deck | Sc | Clock decap/table | prot | Acrk | H&K | tail | BLEND | Verdict vs pod |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Radiation Sickness | 18 | T7 / T10 | 55% | 73% | 68% | 67% | **70%** | **Bring — top + robust.** Counter-immune board kills (Simic Asc / Toxrill / rad) give H&K's wall nothing to target (Δ Acrk−H&K just +5). The default pick. |
| 2 | The Replication Crisis | 17 | T7 / T10 | 55% | 67% | 62% | 59% | **64%** | **Bring — #2.** 7 counters + combat/Kiki board kill, badly under-rated until protect-credited. Kiki swap adds an Abolisher-proof line. |
| 3 | The Genome Project | 15 | T7 / T8 | 5% | 65% | 58% | 57% | **61%** | **Race ceiling, not a lock.** 15/20 glass, combo-reliant, ~no protect — discount for the fragility the goldfish can't see. |
| 4 | Lightning War | 19 | T9 / T14 | 65% | 54% | 47% | 43% | **49%** | **Bring vs Acererak (54%).** Tempo + counter-war + uncounterable Banefire; fights H&K's wall rather than folding to it. |
| 5 | Ms. Bumbleflower | 15 | T8 / T11 | 15% | 53% | 43% | 40% | **47%** | **Soft.** decap T8 but the combat-only kill is goldfish-optimistic; thin protect. |
| 6 | The Exile's Return | 18 | T8 / T10 | 30% | 48% | 41% | 39% | **44%** | **Even–favoured.** Own Abolisher protects its turn; Drannith swap adds static; Kiki/combat kill. |
| 7 | Earthbend the Meta | 17 | T8 / T11 | 30% | 46% | 39% | 37% | **42%** | **Even.** REB/Pyroblast bite H&K's blue specifically; mid clock. |
| 8 | Lorehold Spirits | 18 | T8 / T10 | 0% | 42% | 36% | 35% | **39%** | **Even.** decap T8, combat; no counters or protect. |
| 9 | Curse of the Scarab | 17 | T8 / T11 | 40% | 41% | 37% | 36% | **39%** | **Even.** 5 counters + zombie-army board kill; mid clock. |
| 10 | Zero-Sum Game | — | T9 / T9 | 30% | 36% | 34% | 33% | **34%** | **Even (unaudited).** Board-independent, Abolisher-proof lifeloop kill. |
| 11 | The Grand Design | 19 | T10 / >T14 | 45% | 35% | 27% | 24% | **30%** | **Anti-Acererak CONTROLLER — the race number under-rates it.** →**45% blend / 59% vs Acererak** with its Elesh Norn ETB-lock (`--vs-lock`); best vs Acererak + the 5C tail (own Abolisher); weakest vs H&K (lock inert vs death). |
| 12 | The Dark Lord's Army | 19 | T9 / T12 | 45% | 28% | 24% | 23% | **26%** | **Underdog vs combo.** 7 counters but clock-bound T9; self-meta #1 (opponent-fed). |
| 13 | Eldrazi Stampede Chaos | 14 | T8 / T12 | 10% | 28% | 24% | 23% | **26%** | **Underdog.** combat kill, ~no protect. |
| 14 | The Calamity Tax | 18 | T10 / T10 | 35% | 26% | 20% | 18% | **22%** | **Re-roled → anti-fair / Ur-Dragon specialist (off the combo axis).** Deployed grind-fortress + fog/removal pkg; the realistic clock (T13→T10) lifts its combo-pod blend 5%→22%, but its JOB is the *fair* matchup: **~94% vs Ur-Dragon** (`scripts/vs_dragon_roster_lab.py`; ~87–89% on `vs_dragon_lab.py`) — see "The other axis." Not for his combo decks. |
| 15 | Diminishing Returns | 17 | T9 / >T14 | 10% | 19% | 15% | 14% | **17%** | **Underdog.** slow death-combo, no counters; self-meta strong. |
| 16 | Crystal Sickness | 17 | T11 / T13 | 30% | 9% | 8% | 8% | **9%** | **Underdog.** slow clock (T11). |

*(Peace Offering is off the active roster and excluded. Scores are the current
Conversion-Check audit. BLEND weights = Acererak 0.45 / Hidetsugu and Kairi 0.40 /
5C-tail 0.15, PRIORS; `prot` and the opponent `answer`/`disruption_a` levels are also
priors — tune as games are logged. Regenerate: `python scripts/pod_gauntlet.py --matrix`.)*

> **Reassessment note (2026-06-01, MEASURED 2026-06-09): Replication Crisis is
> not a race deck.** The 2026-06-01 draft argued this structurally; the
> `rc_speed_lab.py` goldfish combat lab (40k trials — token copies, energy
> keeps, Procession/Panharmonicon doubling, Brudiclad conversion, AA extra
> combats; see `analysis/Replication_Crisis_Speed_Curve_Analysis.md`) now
> quantifies it. Even with **every attacker unblocked and zero interaction**,
> the focused decapitation of one opponent lands by T6 only **16%** of the time
> (median T7); a defended-board proxy gives **6%** (median T8). The **table**
> kill is median T10–11 unblocked. The Sword+AA infinite decides ~1–3% of
> games (zero tutors), and Adeline's tokens are *spread* 1/opponent by printed
> text, not focused. The Summary's old "Goldfish T5–7" was a god-draw artifact
> (T5 = 2%) and has been corrected. This originally read as **even as a value deck,
> a loss as a race.** The two-deck `--vs` model now lifts it to **#2 (64% blend)**:
> the Grand Abolisher colour-lock means its 7 counters + board kill mostly **resolve**
> vs his two current mains (only the 5C tail blanks them), and the protect-own term
> credits exactly that. The Ur-Dragon-shell blocker problem still caps it as a pure
> race, but as a counter-heavy value/board deck it now rates a clear bring.

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

## The other axis — vs his Ur-Dragon (the *fair* deck): the matrix inverts

Everything above races his **combo** decks. His **Ur-Dragon** deck is a different
animal and **inverts every conclusion in the table**. Card text verified
(`card_lookup.py "The Ur-Dragon"`, `project_ur_dragon_matchup`): {4}{WUBRG} 10/10,
*Eminence* (dragon spells cost {1} less from the **command zone or battlefield** — the
discount survives the commander dying), and an **attack trigger** that draws + cheats a
permanent into play per attacking dragon. So it is a **combat-trigger BOARD deck** — a
snowballing dragon army a wrath **resets** and a fog **skips** — **not a combo with a
lethal turn K to race**. The decap-race model above is the wrong shape for it.

**The inversion (the headline).** Beating a fair board deck rewards the opposite traits
to racing a combo:

- The grind/wrath/over-the-top decks at the **bottom** of the combo table (Dark Lord,
  Calamity/Glarb, Diminishing, Grand Design) are the **right** decks here — wraths +
  card advantage + an over-the-top kill convert in a fair game.
- The race/glass decks at the **top** of the combo table (Replication's combat swarm,
  Genome's pings) get **walled** by flying blockers + incidental dragon lifegain; their
  table clock balloons.
- **Reactive interaction is LIVE** (only the 5C shell can field the white Grand Abolisher,
  and even then it's a fair deck), and the **sign-flips**: lifegain & fogs are **good**
  here; **don't burn removal on the 10/10** (eminence runs from the command zone) — sweep
  the board / kill the payoff dragons / tax the combat step / go over the top.

**Computed per deck (`scripts/vs_dragon_roster_lab.py`, 40k trials, 2026-06-15).** Not
archetype-judged — a Monte-Carlo SURVIVAL race for all 16. Three inputs: the deck's **kill
clock** (the lab CDFs, `pod_gauntlet_clocks.json` — decap, or the *table* clock for a deck
that only beats dragons via a slow drain); its **anti-dragon toolkit** (wraths / fogs /
combat-taxes / spot removal / maze / lifegain), classified from **oracle text** and printed
per deck for audit; and its **kill axis** — *over* (board-independent: drain/burn/ping/mill/
alt-win, or evasive combat → ignores blockers) vs *combat* (needs ground attackers → walled
by the flying board, with only a decaying pre-go-live / tapped-attacker window). Ur-Dragon's
go-live, damage curve, and mitigation magnitudes are PRIORS, **swept** — the over/combat
split and the ranking hold across the whole sweep. **`P(win)` is a HEADS-UP goldfish ceiling**
(1v1 vs the dragons; the real 4-pod number is lower, and the glass decks suffer most).

| Deck | vs Ur-Dragon | Combo blend (rank) | Kill axis | Anti-dragon toolkit (oracle-measured) |
|---|---|---|---|---|
| **The Genome Project** | **99%** | 61% (#3) | over | pings (direct dmg) + Exsanguinate; Blasphemous Act |
| **Radiation Sickness** | **99%** | 70% (#1) | over | rad-drain / Jarad / Mindcrank / **Toxrill**; 3 wraths |
| **The Calamity Tax (Glarb)** | **94%** | 22% (#14) | over | Torment / Gray Merchant; 3 wraths + 3 **fogs** + Maze |
| **The Dark Lord's Army** | **86%** | 26% (#12) | over | Gray Merchant + opp-fed amass-drain; 3 wraths + Propaganda |
| **Lightning War** | **83%** | 49% (#4) | over (race) | burn / X-spells; 1 wrath — but **lifegain-sensitive** (→56% if dragons gain life) |
| **Zero-Sum Game** | **70%** | 34% (#10) | over | Abolisher-proof lifeloop; 1 wrath + 4 spot |
| **Crystal Sickness** | **57%** | 9% (#16) | over | drain + Mirrodin-Besieged alt-win; slow (T11), 1 wrath |
| **The Replication Crisis** | **48%** | 64% (#2) | combat | token swarm — **walled**; 1 wrath, fast enough to sometimes race go-live |
| **Lorehold Spirits** | **39%** | 39% (#8) | combat | spirit combat — **walled**; 3 spot, no wrath |
| **Ms. Bumbleflower** | **38%** | 47% (#5) | combat | combat-steal — **walled**; 3 fogs survive but can't close |
| **The Exile's Return** | **37%** | 44% (#6) | combat | Kiki/combat — **walled**; 2 wraths + Abolisher survive, kill still must connect |
| **Curse of the Scarab** | **34%** | 39% (#9) | combat | zombie alpha — **walled**; 2 wraths |
| **Earthbend the Meta** | **34%** | 42% (#7) | combat | lands-as-creatures combat — **walled**; no wrath |
| **Eldrazi Stampede Chaos** | **29%** | 26% (#13) | combat | big-creature combat — **walled**; no wrath/over-line |
| **Diminishing Returns** | **23%** | 17% (#15) | over (slow) | death-drain is board-indep but the table clock is T12+; 3 wraths survive, drain too slow |
| **The Grand Design** | **14%** | 30/45% (#11) | combat | **"96% incremental COMBAT, almost no trample"** → survives (control + wraths) but can't close |

*(`P(win)` from `vs_dragon_roster_lab.py` → `analysis/vs_dragon_roster.json`; combo blend +
rank from the main table. Toolkit counts are oracle-classified and **printed by the lab for
audit** — Culling Ritual is excluded (MV≤2, misses dragons); a couple of reskin-named removal
spells under-resolve, so spot counts are floors. Cross-check: this model puts Glarb at 94%,
consistent with `vs_dragon_lab.py`'s ~87–89% on the same deck.)*

> **What the math changed (this is why we compute instead of judge).** Two of the
> archetype-tier guesses this section first carried were **wrong**, and the lab caught them:
> **(1) The Grand Design is the WORST deck here (14%), not a "Bring."** Its kill is
> *combat with almost no trample* (its own Summary: 96% of kills are incremental combat) —
> so vs a flying wall it **survives but can't close** (the can't-close-fortress pattern from
> `self_meta`). **(2) Genome (99%) and Lightning War (83%) are NOT walled** — pings and burn
> are *board-independent direct damage* that races over the wall; only the **combat** racers
> (Replication, Lorehold, Exile, Curse) get walled. "Race deck = walled" conflated combat
> with board-independent damage.
>
> **The decision.** The clean read isn't "grind vs race" — it's **board-independent kill vs
> combat kill**, and three decks are board-independent damage that beat *both* his archetypes:
> **Radiation Sickness (99% / #1 combo)** — the standout hedge, robust, not glass — plus
> **Genome (99% / #3)** and **Lightning War (83% / #4)** as the glassier both-ways options.
> **Glarb (94%) and Dark Lord (86%)** are the anti-fair *specialists* — top vs dragons, but
> bottom tier vs his combo (Glarb #14, Dark Lord #12), so they're a hard read: commit only
> when you're confident he's on Ur-Dragon. When the meta is unknown, **bring Radiation
> Sickness.**

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
   Full writeup: `archive/proposals/Grand_Design_Mana_Fixing_Pass_2026-06-09.md`.

---

## Recommendations

1. **Reactive answers are back on the menu — vs his two current mains.** The old
   "their Abolisher kills your counters" gap now holds **only for the 5C tail** (the
   colour-lock correction): Acererak is mono-B and Hidetsugu and Kairi is UB, so your
   counters/removal mostly **resolve** — which is exactly why the counter-heavy decks
   (RS, Replication, Lightning War) top the table once `protect` credits them. Static
   hatebears are still useful but are now **loop-typed, not universal**: ETB-hate
   (Torpor Orb / Elesh Norn) hard-locks Acererak and is a **blank** vs H&K's death
   trigger; only Rule of Law-class + exile-on-sight hit both. The **Kefka** (forced-draw
   burn on *your* turn) and **Exile's Return Drannith** swaps still point the right way,
   and GD's already-present **Elesh Norn** is the standout (`--vs-lock`).

2. ~~**Fix Grand Design's mana base.**~~ **RETRACTED 2026-06-09** — the 39% that
   motivated this was the model artifact above; the corrected floor is 89% and the
   hand-counted base is ≥16 sources per colour. No land changes needed. Grand
   Design's freed priority goes to the **single canonical upgrade**
   (`proposals/Grand_Design_Upgrade_2026-06-13.md`): a 7-for-7 ramp +
   diversified-finisher pass, lab-validated **decap T10→T9, whiff 11%→5%** — ramp
   (Solemn / Sakura-Tribe Elder / Wood Elves / Faeburrow / Coalition Relic) + a
   *tutorable* creature finisher (Craterhoof) + Rune-Scarred Demon to fetch the
   otherwise-untutorable Finale. Supersedes the older Finisher / ETB / Mana passes
   (now in `archive/proposals/`).

3. **The "too slow" tier (Dark Lord, Bumbleflower, Lorehold, Earthbend) is fine
   — just not the deck you bring to this pod.** Don't try to speed them up at the
   cost of their identity; pick a faster deck for this table. (Caveat: Dark Lord is
   *slow vs his combo* but a **top pick vs his Ur-Dragon** — see "The other axis.")

5. **Read his deck before you pick yours — and default to Radiation Sickness.** His
   combo decks and his Ur-Dragon deck largely want *opposite* answers (the tables invert),
   but the computed model (`vs_dragon_roster_lab.py`) shows the real axis is
   **board-independent kill vs combat kill**, not grind vs race. Three board-independent
   *damage* decks beat **both** archetypes: **Radiation Sickness (99% vs dragons / #1 combo)**
   — the robust hedge and default — plus **Genome (99% / #3)** and **Lightning War (83% / #4)**
   as glassier both-ways options. **Glarb (94%) and Dark Lord (86%)** are anti-fair
   *specialists* — bottom tier vs his combo, so commit them only on a confident Ur-Dragon
   read. Do **not** reach for The Grand Design here (14% — its combat kill is walled by the
   flying board) or Diminishing (23% — its drain is too slow).

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
- **Clock + the `--vs` blend are lab/gauntlet-sourced.** Clock medians come from
  `analysis/pod_gauntlet_clocks.json` (the `*_clock_lab.py` suite, harvested by
  `pod_gauntlet.py --refresh`); the per-opponent and BLEND columns from the two-deck
  race (`simulate_vs`). None are hand-typed — regenerate with `python
  scripts/pod_gauntlet.py --matrix`; `python scripts/clock_check.py` lints the Clock cells.
- **The blend is heuristic, with three known biases:** (1) the clock is an unblocked
  goldfish **ceiling** (over-rates fast decks); (2) the opponent **weights / `answer` /
  `disruption_a`** and each deck's **`prot`** are PRIORS (`OPPONENTS` / `PROTECT` in
  `pod_gauntlet.py`), not measured — tune as games are logged; (3) it's a **decap race**
  that under-rates lock/control decks (GD's persistent-lock line lives in `--vs-lock`,
  not the blend). Read the per-opponent spread and verdict, not the blend alone.
- **The verdict column is judgement**, anchored to the data above and the pod profile —
  not simulator output.
- Rebuild the sim numbers with: `python scripts/deck_sim.py --combos --json sim_results.json`
