# Candidate Clock Labs — Berta & Najeela (2026-06-13)

Kill-turn goldfish clocks for the two un-built "Candidate new builds" (`Deck_Index.md`),
requested after the Loam-teardown / RS-upgrade round. Both are **combo decks**, so the kill
shape is *closed-loop → decap = table by construction* (`kill_all`). Labs:
`scripts/berta_clock_lab.py`, `scripts/naj_clock_lab.py` (20k trials, seed 20260613), on
`speed_lab_core.py`. Modelling builds: `decks/considering/berta-wise-extrapolator-20260613.txt`,
`decks/considering/najeela-blade-blossom-20260613.txt` (both **GC-verified to the 3-cap** — see
GC corrections below).

The pod bar (`project_pod_combo_opponent`): **decap by T≤7.**

## Results

```
  P(kill <= T) %            T3   T4   T5   T6   T7   T8   T9  T10  T12   median  never-12
  Berta  (GU)                0    1    2    3    6   10   13   17   25   >T12      75%
  Najeela (5C)               0    0    5   12   23   36   46   54   66    T10      34%
```

## Berta — the "T3–5, ahead of the pod" thesis is falsified hard

PROP claim: *"T3 god-hand, T4–5 consistency, T6 worst case… ahead of the pod's T6–7."*
**Measured: median kill never lands in 12 turns (75% never-in-12); 3% by T6, 25% by T12.**

The diagnosis is structural, not a tuning miss: **every Berta win line is gated on a
singleton, un-tutorable enabler.**
- Tender + **Freed/Pemmin's** (the auras) → the creature half (Bloom Tender) is tutorable;
  the aura half is **not** (no enchantment tutor survives the GC cap — see below).
- Selvala + **Umbral Mantle / Staff of Domination** → the untapper half is an artifact, **not**
  tutorable by the deck's green creature-tutors.
- Berta + **Simic Ascendancy** + a doubler → the Ascendancy is an enchantment, **not** tutorable.

GU, once the Game-Changer tutors are removed, has **no way to tutor an enchantment or
artifact** — so each line must *draw* its specific 1–2-copy enabler. That is the "singleton
combo density" trap (a 2-card combo of singletons assembles like a 4-card combo) compounded
by un-tutorability. The lab models the deck *generously* — full card-draw engines (Tatyova,
Garruk's Uprising, X-draw digs) and smart creature-tutoring toward whichever line's enabler
was drawn — and it still whiffs three games in four. The pod-approved 2-card infinite is a
**glass cannon that never assembles**, not a race.

Conservative omissions (would lift the front edge *somewhat*, not the verdict): Aetherflux
storm, the combat backup (Avenger/Craterhoof/Triumph), Berta's own Fractal finisher, Mana
Reflection/Sapphire Medallion mana, aggressive mulligan-to-combo.

## Najeela — reliable, but a T10 deck, not a T6–7 racer

PROP framing: *"deterministic and tutorable… ceiling 18–19/20."* The **deterministic +
tutorable** half holds — Najeela lands far more often than Berta (66% by T12 vs 25%) because
the enablers (Druids' Repository, Bear Umbra, Sword) **are** tutorable (Demonic/Vampiric/Idyllic
Tutor + Diabolic Intent/Grim Tutor/Wishclaw), and there are 3 redundant loop lines. **But the
clock is median T10**, with 34% never-in-12 and only 12–23% by the pod's T6–7. It does **not**
race the pod.

The gates are exactly the ones the proposal flagged: **5-colour mana** (the loop costs WUBRG
every combat) and **commander dependence** (Najeela is {2}{R}, 3/2 — every line funnels through
her; recast tax compounds). You also need a creature board (≥5 attackers for the self-funding
Repository line). The clock is a *reliability* clock (assembles by ~T10 most games), not a
*race* clock.

Conservative omissions: Cryptolith Rite / Earthcraft as ramp-to-loop, fair Warrior beats, the
mana-funding of the Repository line at board<5. Optimistic (documented): rocks repeat,
colour-blind mana floor, Najeela survives to activate (her real glass jaw).

## Head-to-head

Najeela dominates Berta on both axes (median T10 vs never; 66% vs 25% by T12). If the question
is "which of these two would you build," it's **Najeela** without contest. But against the
*actual* brief — out-race or disrupt the T6–7 combo pod — **neither qualifies as a racer**;
both are ~T8–T10 combo decks that would have to win the *disruption/protection* game to survive
to their kill turn, which is the same gap the kill-window sweep found across the roster.

## GC corrections found while building (important for any real build)

Both proposals mis-counted Game Changers against the Feb-2026 list:
- **Berta:** the PROP calls **Cyclonic Rift, Mystical Tutor, Worldly Tutor** "non-GC" — **all
  three are GCs** (#11, #33, #53). The modelling build runs the legal trio **Seedborn Muse /
  Survival of the Fittest / Mana Vault** and cuts those three. Losing Mystical/Enlightened/
  Worldly is *why* the enchantment/artifact halves are un-tutorable — i.e. the GC cap is part
  of what makes Berta's combo so slow.
- **Najeela:** the PROP plans a **Bracket-4 "unlimited GC"** list (8–10 GCs) — this repo's hard
  rule is **max 3**. Its **Smothering Tithe / Chrome Mox / Cyclonic Rift** are GCs too. The
  modelling build runs the legal trio **Demonic Tutor / Vampiric Tutor / Mana Vault**.

## Bottom line

- **Berta:** do **not** build on the current plan. The 2-card-infinite thesis collapses under
  GU's tutor poverty + the 3-GC cap; median never-in-12. Would need a colour splash (for
  enchantment/artifact tutors or a Thoracle line) to be a real combo deck — outside GU/budget.
- **Najeela:** a genuine, reliable combo deck (median T10) and clearly the better of the two,
  but **not** a pod-racer; build it for the *combo + interaction* plan, not to out-speed T6–7.
- Both clocks are now **lab-cited** (replacing the proposals' unverified windows). Exact
  percentages are soft (goldfish: no interaction, no combo-mulligan); the **direction** —
  Berta whiffs, Najeela ~T10 — is robust.

---

## Addendum — Berta real-engine re-lab (2026-06-14)

User dropped Najeela, asked *"what would it take for Berta to compete,"* and shared three
external Berta lists. Reviewing them surfaced a real gap in the 06-13 run: **the modelling
build omitted the engine those lists are built on.** Most importantly it had no **Intruder
Alarm**, which combos with **Berta's own `{X},{T}` Fractal + any unsick mana dork for infinite
mana** (activate for X=0 → Fractal ETB → Alarm untaps all creatures → re-tap the dork for net
mana, re-tap Berta, loop → Ballista/Finale). The 06-13 lab therefore **never tested Berta's own
best line** — it only had Tender+Freed (which doesn't even need Berta).

Re-lab is an A/B on the same harness/seed (`berta_clock_lab.py` extended): 06-13 build vs a
real-engine build (`decks/considering/berta-wise-extrapolator-20260614.txt`, same legal 3-GC
frame, −4 weak combat/value cards +Intruder Alarm / Kami of Whispered Hopes / Lyla + Pensive
Professor dig), with win-line attribution. Dig-engine assembly via creature tutors enabled
(both halves are creatures — a real pilot would).

```
  P(kill <= T) %            T3  T4  T5  T6  T7  T8  T9 T10 T12   median  never-12
  Berta 06-13 (pre-engine)   0   1   2   3   6  10  13  17  25   never     75%
  Berta 06-14 (real engine)  0   1   4   7  10  15  20  26  36   never     64%
```

**The 06-13 row reproduces exactly** (regression check passed → paired comparison is sound).
The real engine lifts the clock **+11pp by T12 (25→36%), −11pp never (75→64%), T7 6→10%** — so
the prior verdict *understated* Berta. But:

- **Median kill is still never-in-12.** It whiffs ~64% of games and clears the pod's T7 bar
  only ~10% of the time.
- **Almost the entire lift is the Intruder Alarm line alone** (24–26% of all wins). Kami (a
  6th dork) and the Lyla+Pensive draw loop add only ~3pp *even with* tutor-assembly — because
  dorks and raw draw were never the bottleneck. **Drawing the singleton, un-tutorable ENABLERS
  is** (Freed / Pemmin's / Intruder Alarm / Ascendancy), and the 3-GC cap leaves that unchanged.

**Verdict holds: within 3 GC, Berta does not compete — still a decisively worse Najeela (36%
vs 66% by T12; median never vs T10).** Two durable takeaways:
1. **Intruder Alarm belongs in *any* Berta build** (it's her own combo, ~¼ of all wins); the
   PROP and the 06-13 considering list wrongly omitted it.
2. The external lists' GC counts: **#1 Fun Teacher = 7** (the only one built to race — fast mana
   + free counters + The One Ring/Rhystic dig), **#2 crazy frog = 3** (legal under our cap),
   **#3 Poison Dart = 0** (casual). The path to "Berta competes" is essentially **#1 — i.e.
   waiving the 3-GC house rule.** Caveat: a goldfish clock can't credit the *protection* that
   shell buys, which is most of why #1 is a real deck; that axis is a separate (delay-lab) question.
