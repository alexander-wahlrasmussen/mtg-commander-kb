# The Opponent-Clock Lock Model — closing pod_gauntlet limitation #1

**2026-06-15.** `pod_gauntlet.py`'s load-bearing **limitation #1** was *"no opponent-clock
tax: every deck races the same fixed combo turn `K`, so decks that **slow the pod** are
systematically underrated — their real edge is making `K=10+`."* The intended fix was a
**mana-tax** (Sphere/Thalia) accumulator that pushes `K` out. This iteration set out to
build it — and found the premise mostly false, so it built the **honest** form instead.

> **Trust the ranking, the gap, and the direction — not the second decimal.** A heuristic
> race model on goldfish clocks, now with a persistent-lock overlay. `e/r/g` are documented
> judgment (the `delay_lab` convention), printed and swept.

Tools: `scripts/lock_lab.py` (availability lab) + `pod_gauntlet.py --lock` / `--add`
(lock-aware race + what-if). Data: `analysis/lock_availability.json`.

---

## 1. The audit: the roster has no clock-tax to model

Before modelling tax pieces, I checked which decks run them — grep of all 16 active lists +
**full read** of both Calamity lists + **oracle verification** of every candidate
(`card_lookup.py` / the oracle dump, per the read-the-card rule). The result reframed the
whole iteration:

- **No mana-tax stax anywhere.** Zero Sphere of Resistance / Thalia / Trinisphere /
  Lodestone / Rule of Law across the roster. Grep hits were false positives (`Aven`→Graven
  Cairns, `Tax`→Gi**tax**ian Probe) or non-taxes (Esper Sentinel = draw-tax, Propaganda =
  attack-tax, Smothering Tithe = ramps *you*).
- **Calamity Tax — the deck this was meant to rescue — runs no tax or lock at all.** Its
  "Tax" is the **Torment of Hailfire** life-drain, not a Sphere. Its disruption is *entirely
  one-shot*: counters (Mana Drain, Pact, FoN, Fierce Guardianship, Swan Song) + removal
  (Deadly Rollick, Toxic Deluge, Meathook, Massacre Wurm). Nothing pushes the pod's `K` out.
- **What little persistent disruption exists is thin and elsewhere:** Cursed Totem (Kefka),
  Opposition Agent (Lightning War), Teferi Time Raveler (Grand Design — and it doesn't even
  count, below).

**Verdict on limitation #1: real in principle, moot in practice.** A τ-accumulator would
model stax pieces nobody plays. The roster contests the pod by **racing** (decap clock) and
**answering one attempt** (the one-shot `D` already modelled) — not by taxing its clock.

### The classification (oracle text verified 2026-06-15)

| Piece | Where | Kind | `e` / `τ` | Why |
|---|---|---|---|---|
| **Cursed Totem** | Kefka | hard-lock | e 0.50 | creature activated abilities can't be activated → stops Kenrith/Hidetsugu creature-activation; partial Kinnan (artifact mana); nil Kairi (spells). Symmetric, but free for Kefka's spell/trigger kill |
| **Opposition Agent** | Lightning War | hard-lock (soft) | e 0.40 | flash; hijacks their library searches → taxes tutor-reliant assembly; removable body, pre-assembled lines dodge |
| **Esper Sentinel** | DR, Earthbend, Replication, Bumbleflower | mana-tax | τ 0.3 | first noncreature spell/turn only, ~1 mana, payable → **negligible** (Δ=0); it's really a draw engine |
| Teferi, Time Raveler | Grand Design | **excluded** | 0 | sorcery-speed lock protects *our* interaction; does **not** stop a main-phase combo |
| Grand Abolisher | Exile's/DR/GD | **excluded** | 0 | *"during your turn"* = protect-own; the pod combos on **their** turn |
| Notion Thief | Kefka | **excluded** | 0 | draw-replacement punisher — anti-wheel value, not a combo stop |

Everything else: **empty package**.

---

## 2. The model: persistent lock vs one-shot answer

The honest content of limitation #1 is **locks, not mana-tax**. `delay_lab` and the gauntlet
treat disruption as **one-shot**: an answer stops one attempt and is *re-rolled* next turn
(so a deck holds `n` turns with prob `Dⁿ` — leaky; this is the "Calamity leaks 0.43⁶ ≈ 0.7%"
finding). A **persistent lock** is different: once it's **live and effective**, it holds
**every turn until the pod removes it**. That is exactly "making `K=10+`."

The lock-aware race (`pod_gauntlet.lock_race`), per trial:

```
sample K0 (pod's natural combo turn) ; mana-tax shifts it: K = K0 + round(τ/g)
sample t_kill (our decap turn) ; if t_kill <= K -> WIN
sample t_lock (turn our hard-lock is live, from the availability CDF; ∞ if never)
sample eff ~ Bernoulli(e)            # does the lock stop THIS pod's line?
for t = K .. horizon:
    if t_kill == t: WIN                                  # our turn precedes theirs
    if lock live & eff & t>=t_lock:                      # persistent lock holds
        with prob r the pod removes it (free next turn); else it keeps holding
        continue                                          # bought this turn
    else: with prob (1−D) the pod combos -> LOSE          # one-shot answer, as before
undecided at horizon -> LOSE
```

**Key property — it reduces to the standing gauntlet.** With an empty package (`t_lock=∞`,
`τ=0`) every turn falls through to the existing `if rand < 1−D` branch — *identical* to
`simulate()`. So the 14 lock-less decks are provably unchanged (they move only within
Monte-Carlo noise, ±0–1pp at 20k). The model **only** moves real packages.

**Parameters (judgment, sourced, swept — the `delay_lab` convention):**
- `e` = P(a live lock stops THIS pod's line). Tuned per-piece to the pod's shells (3/4 win
  via *activated* abilities, Kairi via spells — so Cursed Totem/Linvala hit creature-
  activations, Rule of Law hits spell-combos, Drannith hits *commander*-casts). 
- `r` = P(pod removes our lock each of their turns). Baseline **0.25** (~4 turns to clear a
  2-mana artifact in a focused 4c pod); swept `0.0–0.6`.
- `g` = pod mana growth for `τ→Δ`. **1.4**/turn (Ur-Dragon ramp shell). Only bites mana-tax,
  which the roster doesn't run.

---

## 3. Results — the active roster (DECAP clock, a=0.30, r=0.25)

`python scripts/pod_gauntlet.py --lock` (20k; +Kefka build-candidate, lab clock):

```
deck                       e    τ   cur  lock   Δ     (drawn-only availability)
Kefka (Forced Liq.)     0.50  0.0   41%   44%  +3     ← tutored: 41% → 50% (+9)
Lightning War           0.40  0.0   37%   40%  +3
Esper-Sentinel decks    0.00  0.3    =     =   +0     (τ0.3 → Δ0, negligible)
every empty-package deck 0.00 0.0    =     =   ±0     (provably unchanged)
The Calamity Tax        0.00  0.0    4%    4%  ±0     ← NOT rescued
```

**Three findings:**

1. **Calamity's "Favoured" verdict is confirmed-not-overturned.** It has no static package;
   the lock model gives it **nothing** (4% → 4%). Its anti-pod plan is one-shot answers behind
   a T13 clock — leaky disruption + a kill too slow to convert. The Pod Gauntlet's open
   question (*"does Calamity beat the pod, or just not-lose for a long time?"*) is answered:
   **on this model it does not beat the pod, and no tax model rescues it** — because it
   doesn't tax.

2. **Kefka is the one deck the model illuminates.** Cursed Totem vs this activation-combo pod
   lifts P(win) **+3pp drawn / +9pp tutored** (41% → 50%). Realistically ~**+5pp** (tutoring
   the Totem competes with tutoring the kill). This *quantifies* Kefka's anti-pod case beyond
   its Abolisher-proof clock — and it's the no-approval build. The lift **erodes with pod
   removal** (52% @ r=0 → 46% @ r=0.6): a lock answered on sight buys little.

3. **Lightning War +3** from Opposition Agent — a real but soft persistent tutor-lock.

---

## 4. What-if (prescriptive): what would adding a lock buy?

`python scripts/pod_gauntlet.py --add "<slug>=<piece>"` injects a catalog static, measures its
availability *in that shell*, and races the lift (8k, r-swept):

| Deck + add | e | avail T6 (drawn/tut) | P(win) cur → lock @r=0.25 | @r=0 (tut) |
|---|---|---|---|---|
| **Dark Lord + Drannith Magistrate** | 0.60 | 11% / 22% | 26% → **31%** | 35% |
| Diminishing Returns + Rule of Law | 0.55 | 11% / 11% | 25% → 28% | 30% |
| Calamity + Cursed Totem | 0.50 | 11% / 21% | 5% → 6% | 10% |
| Grand Design + Cursed Totem | 0.50 | 11% / 11% | 25% → 27% | 29% |

**The best lock to add vs this pod is Drannith Magistrate into a black tutor shell** — a
*commander*-cast lock (e0.60) is the right tech against a *commander*-combo pod, and the
tutors raise its availability. But even the best case is **+5–9pp**, and it is **triple-gated**:

> A lock helps only if it is **AVAILABLE** (a single copy is ~13% drawn by T6 — the dominant
> throttle in a singleton format), **EFFECTIVE** (`e` — it must hit *this* pod's lines), and
> **STICKS** (low `r` — the pod can't just remove it). A persistent lock is **not a silver
> bullet** here; adding one to the slow grind decks barely moves the needle.

This vindicates the gauntlet's original skepticism under a *generous* lock model: the reason
locks don't appear in the roster is that, as singletons against a removal-rich pod, they
aren't worth a slot for most decks. The exception is a deck whose **identity** already wants
the piece (Kefka's Cursed Totem is free against its own spell/trigger kill).

---

## 5. Limitations (load-bearing)

1. **Availability is a drawn floor + a generic-tutor ceiling.** Creature-tutor fetch of
   *creature* locks (GSZ/Chord/Eladamri's → Linvala/Drannith) is **not** modelled, so those
   availabilities are **floors** — Drannith/Linvala into green/white tutor shells are
   *under*-credited. The drawn-vs-tutored spread is the honest band.
2. **A live lock ≠ effective (`e`) ≠ un-removed (`r`).** `r` is the pod's removal of *our*
   lock at a flat swept rate, not a per-pod-deck count. `e` is judgment per the shell mix.
3. **One mana-tax piece (Esper Sentinel) is scored negligible**, correctly — but if the
   roster ever adds real Spheres, the `τ→Δ` path is built and waiting (`g` swept).
4. **Still a heuristic race model, not a rules engine.** decap (remove the archenemy), not
   table, is the headline; the pod's own blockers/backup lines aren't modelled.

---

## 6. Run it

```bash
python scripts/lock_lab.py                          # availability per deck -> JSON
python scripts/lock_lab.py --mode whatif            # injected-piece availability table
python scripts/pod_gauntlet.py --lock               # lock-aware race (drawn floor)
python scripts/pod_gauntlet.py --lock --use-lock-tutors   # tutored ceiling (Kefka 41→50%)
python scripts/pod_gauntlet.py --lock --r 0.5       # a pod that removes our lock faster
python scripts/pod_gauntlet.py --add "dark_lords_army=Drannith Magistrate"   # what-if lift
```

**Bottom line.** Limitation #1 is **closed**: the opponent-clock tax is real, but on this
roster it lives as *persistent locks*, not mana-tax — and the roster barely runs them.
Calamity's skeptical verdict **stands**; Kefka's Cursed Totem is the one lock that earns its
slot (~+5pp, more if it sticks); and if you ever want to *buy* clock-tax vs this pod, the
model says **Drannith Magistrate in a black tutor deck**, not a Sphere.
