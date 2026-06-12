# Candidate Bake-Off — Stage 4 Verdict (2026-06-12)

**What this is:** the Stage 4 deliverable of the pick-one bake-off
(`Candidate_Bakeoff_2026-06-12.md`): head-to-head ranking of the 7 labbed finalists and a
recommendation of **ONE** deck to build. Format per `Witherbloom_External_Build_Comparison.md`.

**Method:** clocks are lab-measured (`scripts/*_clock_lab.py` on `speed_lab_core.py`, 20 000
trials, seed 20260612, 2026-06-12 — decap and table cited separately). Conversion Checks are
full-pass structural scores from the finalized 100-card lists for the three contenders, band
estimates for the eliminated. All prices **unverified** unless stated.

---

## THE VERDICT: build Yuriko — *Insider Trading*

**`insider-trading-20260612.txt` is the pick**, conditional on one gate: **pod approval of
Thassa's Oracle + Demonic Consultation/Tainted Pact** (the 6th two-card-combo request to this
pod). **If the pod declines, build Kefka-burn (*Forced Liquidation*) instead** — it is the
strongest candidate that needs no approval at all.

| Rank | Candidate | Clock (decap / table) | Never-in-12 | CC | Cost (unverified) | One-line verdict |
|---|---|---|---|---|---|---|
| **1** | **Yuriko (int)** | **T7 / T8** | **9%** | **17/20** (5/4/4/4) | ~€140–170 | Best clock×reliability product; only pre-registered gate that passed; evasion makes its goldfish honest |
| 2 | Kefka-burn (int) | T8 / T9 | 11% | 16/20 (4/4/3/5) | ~€140–190 | Best Abolisher answer + best interaction suite; loses the race by ~1 turn; no pod approval needed |
| 3 | Godo (int) | **T6 / T6** | 5% | 13/20 (4/4/**2**/3) | ~€45–60 *(flagged light)* | Fastest on paper; the margin lives entirely in the goldfish's blind spot; Durability 2 = rubric red flag |
| 4 | Kefka-ext | T9 / T9 | 19% | ~15–16 (band) | n/a (scouting) | Honest non-turbo; loses the same-commander head-to-head on clock AND brief-fit |
| 5 | Kinnan (int) | T11 / T11 | 42% | ~14–15 (band) | ~€120–160 | "Strong turbo" falsified by lab; singleton combo density is the bottleneck |
| 6 | Clive (ext) | T9 / >T12 | 58% | ~15 (band) | n/a (scouting) | Expert engine, not a racer; calibrated the brief's bar |
| 7 | Korvold (int) | T9 / >T12 | 72% | ~15 (band) | ~€50 (held) | Grindy as self-declared; table kill rarely arrives inside the game |

---

## Why Yuriko over Godo (the clock leader)

Godo's lab clock (median **T6 table**, 5% never) is genuinely the only number inside the brief's
T6–7 bar, and it is the cheapest build. The verdict still goes against it, for three reasons that
compound:

1. **The goldfish flatters the two decks unequally.** The lab convention is *every attacker
   unblocked, no opposing interaction*. For Yuriko that assumption is close to literal — the list
   runs 4 printed-unblockable one-drops (Slither Blade, Changeling Outcast, Triton Shorestalker,
   Mist-Cloaked Herald), a flier package, and Tetsuko (power ≤1 can't be blocked). For Godo it is
   false: samurai tokens are ground attackers, and the pod it has to beat is an **Ur-Dragon
   deck** — the table is full of large flying blockers. The same convention measures Yuriko's
   real line and Godo's best case. Godo's one-turn edge does not survive this correction.
2. **Durability 2 is the framework's catastrophic-gap flag.** "No single axis compensates for a
   catastrophic gap in another." Godo is cast-dependent (commander tax compounds — ninjutsu-
   Yuriko's doesn't), its combo cycle loses a full turn to any instant-speed removal between ETB
   and combat (Stage-1 caveat, still true), protection is 4 thin slots, and wipe recovery is
   topdeck-dependent. The pods this deck must win in are exactly the pods that punish that.
3. **It cannot interact with the pod threat.** The recurring combo opponent wins T6–7 on their
   own turn behind Grand Abolisher. Godo's plan against that is strictly "win first, every game,
   through removal." Mono-red has no real stack answer (Pyroblast is narrow) and the deck has no
   static hate. A T6 racer that loses the die roll or eats one removal spell has no game B.

Godo stays interesting as the cheap/fast data point, but as the *one* build it is a coin-flip
deck: ahead on the goldfish, structurally behind everywhere the goldfish can't see.

## Why Yuriko over Kefka-burn (the brief-fit leader)

Kefka-burn is the best answer to the Abolisher axis (symmetric static damage needs no stack and
no combat; Bloodletter doubles it on our turn; Cursed Totem switches off Kinnan/Kenrith/Hidetsugu
activations on sight) and carries the deepest interaction suite of any candidate (16 pieces,
mechanism-diverse, scored 5). It is also a clean second on reliability (11% never).

But the brief's first clause is the race, and Kefka-burn loses it: **decap T8** arrives *after*
the pod deck's T6–7 window, so against the deck this bake-off was aimed at, Kefka-burn is
betting entirely on its disruption holding for a turn or two — real, but unmeasured by any lab.
Yuriko's **decap T7** races that window to a coin flip *and* keeps a 3-mana, on-your-turn,
Abolisher-proof combo kill (Thoracle/Consult/Pact, with Jace + Lab Man as redundant oracles and
6+ ways to tutor the pieces) as the second axis. Yuriko also matches or beats it on cost.

Kefka-burn's decisive advantage is political: **it needs no pod approval**. That makes it the
designated fallback, not the pick.

## Why the rest are out

- **Kinnan** — the Stage-1 "Strong turbo" read was **falsified by its own lab** (median T11/T11,
  42% never-in-12): the combo is 2-card in name but its halves are 1–2 singleton copies in 99,
  and assembly odds are governed by copies-in-deck, not piece count. Cost also tripled on sweep
  (~€120–160 vs the claimed ~€45). Wrong on both axes that made it attractive.
- **Korvold** — kept by user override to test the grindy shape; the lab confirms the shape and
  its cost (decap T9, **table >T12 in 72% of games**, ~€50 claim held — the only estimate that
  survived). It is what it says it is: a resilient attrition deck that does not close inside the
  game this pod plays. Also the least mechanically distinct from DR/ZSG/Genome (aristocrats
  drain), which was its own proposal's open gate.
- **Kefka-ext** — matches its self-declaration ("NOT a turbo"); T9/T9 with a counter-heavy suite
  that Grand Abolisher switches off on the only turn that matters. Loses the same-commander
  head-to-head to the internal burn build by ~1 turn AND on brief-fit. Its real lesson is below
  (Learnings #6).
- **Clive (ext)** — T9 decap / >T12 table, 58% never. An expert devotion/wheel engine whose value
  is calibration: even a tuned external doesn't table-kill T6–7. (Lab omitted Underworld Breach
  storm and The One Ring, so its true late ceiling is higher — immaterial to a racing brief.)

---

## Conversion Check — the three contenders (full pass)

### Yuriko — 17/20 (5/4/4/4) · Clock: T7 decap / T8 table (lab 2026-06-12)

| Axis | Score | Rationale |
|---|---|---|
| Core Loop | **5** | The loop is the deck: ~23 ninjas/enablers + ~10 topdeck manipulators (Top, Scroll Rack, Brainstorm, Lim-Dûl's Vault…) + high-MV reveal bombs (Draco, Blinkmoth Infusion, the Cruise/Dig delve suite) all serve one engine. Immediately recognizable. |
| Kill Reliability | **4** | Two genuinely independent lines: the Yuriko drain (hits **all** opponents — the only kill shape that has ever held a clock claim) and a 3-mana on-cast Thoracle/Consult with 3 oracles × 2 consults + 6 tutors. Lab: 61% table by T8. |
| Durability | **4** | Commander ninjutsu dodges the tax — removal costs tempo, not escalating mana. Cheap redundant bodies rebuild after a wipe in 1–2 turns. Not 5: the loop is commander-routed and the bodies are 1-toughness. |
| Interaction | **4** | ~12 pieces: 6–7 counters + 4 instant-speed removal + Dokuchi Silencer. Counter-heavy is the known Abolisher weakness (see Pod fit), but the removal half can kill Abolisher on sight to turn the counters back on. |

### Kefka-burn — 16/20 (4/4/3/5) · Clock: T8 decap / T9 table (lab 2026-06-12)

| Axis | Score | Rationale |
|---|---|---|
| Core Loop | **4** | ~20-card wheel × static-punisher matrix (10 wheel effects × 10 punishers + Bloodletter doubling). Lethality is a conjunction (wheel + 2 punishers), which keeps it off 5. |
| Kill Reliability | **4** | Notion Thief + any wheel ≈ one-wheel table kill with a punisher out; the shared dependency is a card *class* (10 wheels), not a card, so the lines stay independent. Convergence thesis held in the lab (1-turn decap/table gap). |
| Durability | **3** | Punishers are cheap permanents that die to sweepers and the deck has little recursion — but every wheel is also a full-hand recovery, so rebuilds are fast. The proposal's own 3 stands. |
| Interaction | **5** | 16 pieces, mechanism-diverse: 8 removal + 6 counters + Cursed Totem (static) + Deflecting Swat. The only suite in the bake-off that keeps working through Grand Abolisher. |

### Godo — 13/20 (4/4/2/3) · Clock: T6 decap / T6 table (lab 2026-06-12)

| Axis | Score | Rationale |
|---|---|---|
| Core Loop | **4** | ~15-card extra-combat/equipment engine around a 1-card commander combo (Godo fetches Helm; Hammer auto-attach protects the equip step). Clear identity. |
| Kill Reliability | **4** | Once Godo connects it's a table kill in one turn (lab: kill_all, decap = table). Backup combat-extension lines (Aggravated Assault + Neheb, Port Razer, Moraug) are real. |
| Durability | **2** | Cast-dependent commander with compounding tax (Command Beacon mitigates once); one instant-speed removal spell costs a full cycle; thin protection; topdeck-dependent wipe recovery. The rubric's "two in a row is fatal" describes it exactly. |
| Interaction | **3** | ~10 pieces but mono-red coverage: burn + artifact removal; nothing for enchantments or resolved combos; Pyroblast is the only stack answer. |

*Stage-1 estimated Godo at ~15–16; the full pass corrects this downward (Witherbloom-comparison
precedent: screens estimate, full passes correct). Kinnan's band likewise drops from ~16–17 to
~14–15 — Kill Reliability cannot survive a measured 42% never-in-12.*

---

## Pod fit — the pick vs. [[project_pod_combo_opponent]]

The recurring opponent: Ur-Dragon + Hidetsugu/Kairi/Kenrith/Kinnan combo shells, **T6–7 wins on
their own turn behind Grand Abolisher**.

- **The race:** Yuriko decap median T7 makes the matchup a genuine race — and "decap" here means
  the combo player specifically; ninjas choose their target. Kefka-burn (T8) and every other
  candidate except Godo concede the race outright.
- **Under Abolisher:** the counter suite is half-dead on their key turn — known, priced in. The
  plan is race-first; removal (Go for the Throat, Fatal Push, Bloodchief's Thirst, Murderous
  Cut, Dokuchi Silencer) kills Abolisher on sight on *our* turn to re-enable the counters.
  Thoracle/Consult resolves on our turn, where Abolisher never applies.
- **As secondary target:** ninjutsu's tax-dodge + 9% never-in-12 means focused removal slows
  but doesn't shut off the deck — the exact axis where Godo folds.
- **Social role:** Thoracle/Consult carries table stigma; this is precisely why the pod-approval
  gate is non-negotiable and asked *before* purchase, not after.

## Honest weaknesses of the pick

1. **The goldfish is still a ceiling.** T7/T8 assumes average draws and no wraths; a sweeper-
   heavy table pushes the chip plan out 1–2 turns (1-toughness bodies). Through-interaction
   estimate: **T8–10 (unverified, judgment)**.
2. **Counter-heavy interaction** is the wrong shape for this specific pod (Abolisher); the deck
   leans on its removal minority and the race. If pod games show the counters consistently dead,
   the post-build tune should swap 2–3 counters toward static hate — respecting the next point.
3. **Tainted Pact locks the build into name-singleton forever** — every future swap must keep
   all 100 names unique (snow-basic discipline already in the list). This constrains tuning in
   perpetuity and is easy to forget in a casual edit. Flagged in the Summary when written.
4. **~€140–170 is the second-most expensive candidate** (prices unverified; verify at purchase
   — [[feedback_verify_prices]]), and ~23 ninja/enabler slots plus the combo are all buys.
5. **6th two-card-combo approval request.** The political account is being drawn down
   (Kiki ×2, ZSG, DR pending, Replication Crisis pending). If this matters to the pod, the
   fallback exists for a reason.

---

## Learnings (bake-off retrospective)

1. **Pre-registered gates pass; adjectives fail.** The only clock claim that survived its lab
   unmodified was Yuriko's — the one stated in advance as a falsifiable gate ("~T7 median or no
   build"). "Strong turbo" (Kinnan) and "median T7–9" (Korvold, which silently meant decap)
   were the casualties. Kinnan is the **8th** optimistic hand-estimate falsified by a lab.
   Claims survive when they are (a) pre-registered and (b) decap/table-split.
2. **The kill-shape lens is now validated.** Stage 1's structural screen — all-opponent
   simultaneous damage converges decap≈table; combat focus-fire diverges 2–3 turns; a 3-mana
   on-cast combo is decap=table by definition — predicted the convergence pattern of **all
   seven** labs. It is a legitimate pre-lab ranking tool; use it to order future candidates
   before paying for labs.
3. **Cost estimates fail exactly the way clock estimates fail** — optimistic by default, and
   for one root cause: *owned ≠ free*. 3 of 5 internal estimates revised upward on sweep
   (Kinnan ~3×; Kefka-burn and Godo materially); only Korvold's held, because it had enumerated
   its buys. Proposed rule (mirrors the 2026-06-09 lab-citation rule, needs user sign-off since
   it touches `REF_The_Conversion_Check.md`): **a cost claim must cite an availability sweep
   (CSV + deployed-deck grep, dated) or carry an explicit (unverified) flag.**
4. **Singleton combo density beats combo elegance.** A "2-card combo" whose halves are 1–2
   copies in 99 assembles like a 4-card combo (Kinnan: T11, 42% never). Count copies-in-deck
   per role, not pieces-in-combo — same finding as the Witherbloom external's 3×2×4 redundancy
   matrix beating our leaner 2-card line.
5. **The T6–7 brief bar is a decap bar.** Both calibrating externals (expert lists) sit at
   T9/>T12 table; only a glass 1-card-combo deck tables by T6. The pod-beating condition was
   never "kill the table by T7" — it is "kill or outpace **the combo player** by their T6–7
   window." Future briefs should say "decap T≤7" and treat table clock as the reliability
   metric (Genome's T8 table remains the roster benchmark).
6. **Goldfish conventions are not deck-neutral.** "Every attacker unblocked" is nearly literal
   for an evasion deck (Yuriko) and pure fiction for a ground-token deck facing a dragon pod
   (Godo). When *comparing across decks*, state which candidates the shared convention flatters
   — a 1-turn lab edge can be smaller than the convention asymmetry.
7. **Purpose-built beats expert-built on brief-fit.** The same-commander head-to-head (internal
   Kefka-burn vs external Kefka combo-control) went to the internal on clock AND fit. Expert
   provenance signals card quality, not fit to *your* pod's failure mode.
8. **Labs double as decklist linters.** Wiring the parsers caught two ground-truth `.txt`
   errors (a nonexistent "Consuming Tides", Lim-Dûl's Vault mis-spelt). A deck that has never
   been machine-parsed has unverified spelling.
9. **Process guards earned their keep again:** the SOS prepared-card rule caught Naktamun
   Lorespinner // Wheel of Fortune (and turned it into a free flex add); the reskin-alias table
   rescued Clive's legality (raw "Morgul-Knife" fuzzy-resolves to an illegal mono-black card);
   the Dictate-of-Erebos proxy ambiguity was resolved by preferring the unambiguous owned copy
   (Grave Pact) rather than adjudicating a proxy row.

---

## What happens next (user gates)

1. **Take Yuriko to the pod**: Thoracle/Consult/Pact approval (6th two-card request).
   - **Approved** → verify prices on the ~€140–170 buy list → purchase → move
     `insider-trading-20260612.txt` from `considering/` to `decks/` → write
     `Insider_Trading_Summary.md` carrying `17/20 · Clock: T7 decap / T8 table (lab 2026-06-12)`
     and the Tainted-Pact name-singleton warning.
   - **Declined** → build **Kefka-burn** (no approval needed). Then resolve: the codename
     ("Forced Liquidation" was coined at build time — rename if disliked) and the stale
     2026-05-31 Calamity Tax Sheoldred claim (if formally dropped, the buy list shrinks by one
     premium card).
2. **Standing items surfaced by the bake-off, outside its scope:**
   - **Radiation Sickness runs 4 GCs** (Survival + Seedborn + Vampiric Tutor + Cyclonic Rift) —
     open 3-GC-cap violation, needs a resolution decision.
   - Rule-codification proposal in Learnings #3 (cost-claim sweep citation) — needs explicit
     user approval to touch `REF_The_Conversion_Check.md`.
   - The losing candidates' builds stay in `decks/considering/` as priced, labbed, ready
     options; Godo in particular is a ~€50 weekend build if a fast-glass slot ever opens.

Related: `Candidate_Bakeoff_2026-06-12.md` (tracker, Stages 0–3 evidence) ·
[[project_yuriko_insider_trading]] · [[project_kefka_proposal]] · [[project_pod_combo_opponent]]
