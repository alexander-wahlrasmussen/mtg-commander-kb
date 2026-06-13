# The Exile's Return — Speed-Curve Analysis: Is the T6–8 Kill Window True, and Can We Buy Speed?

**What this is:** the same rigor applied to Lightning War, Calamity Tax, Grand Design and Replication Crisis, turned on **Fire Lord Zuko (The Exile's Return)** to answer two questions the user asked directly: **(1) is the Summary's "Goldfish: T6–8" kill window true, and (2) are there cards we should add to speed it up further?**

**Date:** 2026-06-09
**Card text verified** against local Scryfall data (`card_lookup.py`) for Fire Lord Zuko, Hellkite Charger, Sozin's Comet, Aggravated Assault, Enlightened Tutor, Imperial Recruiter, Recruiter of the Guard, Diabolic Intent, Laelia, Prosper, Norin, Teleportation Circle, Airbender Ascension, Appa, The Legend of Roku, Zuko (Exiled Prince), Fire Nation Palace, Panharmonicon, Cathars' Crusade, Combat Celebrant, Sarkhan's Triumph, Moraug, Port Razer, Scourge of the Throne, Wrenn's Resolve, Lotus Petal, Outpost Siege, Kiki-Jiki, Felidar Guardian, and the flicker suite — not pattern-matched.
**Deck measured:** `decks/the-exiles-return-20260417-194010.txt` (current 99) plus the pending-swap variant (+Kiki-Jiki −Night's Whisper, +Drannith Magistrate −Light Up the Stage; `The_Exiles_Return_Swaps_2026-06-01.md`, not applied).
**Lab:** `scripts/er_speed_lab.py` (40k trials, seed 12345), built on `deck_sim.py`'s engine. Goldfish combat model: +1/+1-counter accrual from cast-from-exile and enters-from-exile events (Panharmonicon doubling only the latter, per its printed text), firebending mana income, Hellkite Charger's in-combat untap loop, the commander-damage axis (21 from Zuko), and ten one-card levers swapped through a fixed flex slot.

> **Bottom line up front:**
> 1. **"Goldfish T6–8" is one turn optimistic at the front edge.** At the zero-blocker ceiling the deck decapitates one focused opponent with median **T8** (70% by T8) — but **T6 is only 9%**, and the **table** dies at median **T10**. The honest window is **T7–8 decap / T10 table**. This is *not* an RC-style god-draw artifact (RC's "T5" was 2%); it's an edge-of-distribution claim rounded in the deck's favour.
> 2. **No single card speeds it up.** Ten levers tested — extra-combat enablers, a Dragon tutor pointed at Hellkite, fast mana, impulse velocity, a second counters-engine — every one lands within +1–4 percentage points and **no lever moves any median**. The clock is broad-based counter compounding, not a missing-piece problem; one card in 99 is ~14% seen by T7.
> 3. **The pending Kiki swap *slows* the goldfish** (decap T7 39→33%, T8 70→62%; table median T10→T11) because it cuts the deck's two cheapest velocity spells. Its own stated rationale — resilience + Drannith disruption — survives; the swaps doc's "kill window compresses to T5–7" claim is **falsified**.
> 4. Two Summary text errors found and corrected: **Enlightened Tutor cannot find Sozin's Comet** (it fetches artifact/enchantment; the Comet is a **sorcery**), and the foretell costs were inverted (pay **{2}** to set face-down, cast later for **{2}{R}** — not the reverse).

---

## The question

The Pod Matchup Matrix marks The Exile's Return **Favoured** vs the combo opponent (T6–7 kill behind Grand Abolisher), with a ✅ in the Clock column on the strength of the Summary's "Goldfish: T6–8." That ✅ was never measured. Meanwhile the swaps doc (pending pod approval) claims +Kiki compresses the window to T5–7. Both claims are testable; the lab tests them.

---

## 1. Kill-package availability — the marquee line is rare, and the tutors mostly can't reach it

`er_speed_lab.py --mode avail`. Tutor map is the text-verified one, not the Summary's:

- **Diabolic Intent** → anything (the only card that reaches either L1 piece).
- **Enlightened Tutor** → artifact/enchantment **only**. Sozin's Comet is a **sorcery** — the Summary listed it as an ET target twice; corrected.
- **Imperial Recruiter** (power ≤2) and **Recruiter of the Guard** (toughness ≤2) → both miss the 5/5 Hellkite Charger.

| P(package reachable ≤ T), % | T4 | T5 | **T6** | T7 | T8 | T10 | T12 |
|---|---|---|---|---|---|---|---|
| **L1** Hellkite + Sozin (drawn only) | 1 | 1 | **1** | 2 | 2 | 2 | 3 |
| **L1** Hellkite + Sozin (+tutors = DI) | 2 | 3 | **3** | 4 | 5 | 6 | 8 |
| ≥2 exile engines seen | 13 | 16 | **19** | 21 | 24 | 30 | 36 |
| *lever:* +Sarkhan's Triumph (Dragon → Hellkite) | 4 | 4 | **5** | 6 | 7 | 9 | 12 |
| *pending swap:* Kiki + Felidar (drawn) | 1 | 1 | **1** | 1 | 2 | 2 | 3 |
| *pending swap:* Kiki + Felidar (+tutors: Imperial finds BOTH, RotG finds Kiki, DI any) | 6 | 7 | **9** | 11 | 12 | 16 | 20 |

The named L1 kill is a **3% by-T6 event**. The deck does not need it — the clock below is carried by the counter-stack swarm — but it means the Summary's "T6 goldfish kill via Hellkite + Sozin" describes the rare branch, not the deck. Contrast Lightning War: ≥1 table-finisher **47%** by T6 with tutors, because its kill is 1-of-4 cards with three tutors pointed at them.

---

## 2. The clock — what the goldfish actually kills, and when

`er_speed_lab.py --mode clock`. Mana-aware, greedy board development, 3 opponents at 40, focus-fire on one (the combo player), **every creature unblocked** — a ceiling. Zuko's 21 commander damage also kills.

| P(dead ≤ T), % | T5 | **T6** | **T7** | **T8** | T10 | T12 |
|---|---|---|---|---|---|---|
| **Combo player dead (decap)** | 1 | **9** | **39** | **70** | 94 | 99 |
| **Table dead** | 0 | **1** | **6** | **15** | 54 | 83 |
| — of which via Hellkite untap loop | 0 | 1 | 5 | 11 | 21 | 25 |
| — decap via 21 commander damage | 0 | 0 | 1 | 3 | 4 | 5 |

**Read:**

1. **Median decap T8; median table T10.** "T6–8" captures the back edge of the decap distribution (70% by T8) but sells the front edge: T6 is 9% even unblocked. Verdict on the Summary's claim: **optimistic by ~1 turn; corrected to T7–8 decap / T10 table.**
2. **Against the pod's T6–7 combo win, the pure race is ~9–39%** at a zero-blocker ceiling. The deck's actual pod plan is — and was always documented as — disruption-led: its own Grand Abolisher protects the kill turn, 9 spot-removal pieces point at theirs. The matrix verdict survives; the Clock ✅ does not.
3. **The Hellkite untap loop is real but a quarter-of-games line** (25% of games ever reach it by T12; 11% by T8). Mechanically verified: Hellkite's {5}{R}{R} is paid from firebending income *inside* combat (attack triggers), so income ≥7 per combat sustains it — Sozin's Comet (5 per attacker), Zuko himself at power ≥7, Avatar Roku (4), Fire Nation Palace's grant (4). It ends when blockers eat attackers, which is why it is bracket-safe and also why the unblocked number is its ceiling.
4. **Commander damage is the through-interaction line, not the goldfish line** (3% of decaps by T8): in goldfish the 40-damage swarm always arrives first. On a blocked board the maths invert — that nuance belongs in the Summary and stays there.

**Rules catch worth recording** (it constrains future "speed up the combat" ideas): **Aggravated Assault can never go infinite in this deck.** AA activates "only as a sorcery" — in a main phase — and firebending mana dies at end of combat, so the burst income can't carry across to pay AA. Without Sword of Feast and Famine (Lightning War/RC's enabler), AA here is one extra combat per 5 *real* mana. Hellkite's trigger fires *during* combat, which is exactly why it works and AA doesn't.

---

## 3. The lever test — ten candidates, none move the needle

`er_speed_lab.py --mode levers`. Each lever swapped through the same flex slot (−Imp's Mischief, goldfish-dead), same model, same seed. Decap / table shown at the decision turns:

| Lever (1-for-1) | decap T7 | decap T8 | table T8 | table T10 | medians | ownership |
|---|---|---|---|---|---|---|
| **BASELINE** | 39 | 70 | 15 | 54 | T8 / T10 | — |
| + Cathars' Crusade | 41 | 72 | 15 | 58 | T8 / T10 | **owned — in this deck's own SB** (3 copies total) |
| + Combat Celebrant | 42 | 72 | 16 | 60 | T8 / T10 | 1 owned, **deployed in Replication Crisis** |
| + Aggravated Assault | 38 | 69 | 14 | 56 | T8 / T10 | 2 owned, 1 free (other in RC) |
| + Sarkhan's Triumph | 39 | 71 | **19** | 60 | T8 / T10 | unowned (price unverified) |
| + Port Razer | 42 | 72 | 16 | 59 | T8 / T10 | unowned |
| + Moraug, Fury of Akoum | 42 | 72 | 15 | 58 | T8 / T10 | 2 owned, 1 free (other in Earthbend) |
| + Scourge of the Throne | 41 | 71 | 15 | 58 | T8 / T10 | 2 owned, both free |
| + Lotus Petal | 40 | 70 | 14 | 55 | T8 / T10 | 2 owned, both deployed |
| + Wrenn's Resolve | 41 | 72 | 15 | 57 | T8 / T10 | unowned |
| + Outpost Siege | 41 | 72 | 15 | 57 | T8 / T10 | owned — in this deck's own SB |

No GC conflicts (none of these is on the current GC list; deck sits at 3/3 regardless).

**Why so flat — the same §5 conjunction maths as Lightning War, plus one new reason.** A 1-of is ~14% seen by T7; even a card that doubles that turn's damage when present moves the aggregate curve low single digits. The new reason: **this deck's clock is already incremental.** Lightning War's lesson was "incremental clock dominates one-shot adds" — Exile's Return *is* the incremental clock. Counters compound across every creature from every exile event; there is no single bottleneck card whose redundancy unlocks a turn. The front edge is gated by **engine assembly + mana before T5** (≥2 engines seen by T6 is only 19%), and no 1-of fixes that.

**What *would* speed it up** is a multi-slot re-curve: trading ~4–5 interaction/protection slots for more sub-3-mana exile engines and velocity. **Recommended against.** The interaction suite (own Abolisher, 9 spot removal, the protection package) is precisely why the matrix marks this deck Favoured vs the combo pod — sacrificing the disruption axis to chase a clock that tops out T7 would be rebuilding the deck into a worse Lightning War (the matrix rec-#3 anti-pattern, same verdict the RC analysis reached for Satya).

If a slot ever opens for free, the marginal picks in order: **Cathars' Crusade** ($0, already in this deck's sideboard, the best table-kill lever among owned cards and a second counters engine that survives Zuko removal), then **Scourge of the Throne** ($0, undeployed, Sarkhan-findable Dragon). **Sarkhan's Triumph** is the best *table* lever overall (+4 at T8: 15→19) but is an unowned buy for a marginal effect.

---

## 4. The pending Kiki swap is a (mild) speed regression — and that's fine, but the doc's claim isn't

The −Night's Whisper +Kiki / −Light Up the Stage +Drannith package, measured:

- **Goldfish decap:** T7 39→33%, T8 70→62%. **Table:** median T10→T11. Cutting the two cheapest velocity spells costs real speed; the goldfish misses them every game while Kiki+Felidar is online only **2% T6 / 4% T7 / 6% T8** mana-aware — even with Imperial Recruiter finding both halves, RotG finding Kiki and Diabolic Intent finding anything.
- **The swaps doc's "T6–8 → T5–7" compression claim is falsified.** What survives — and is genuinely strong — is everything else in that doc: the combo is the deck's only blocker-independent, wipe-resilient win; tutorability (9% T6 / 12% T8 *reachable* with tutors) is resilience through interaction, exactly like RC's Kiki verdict; and **Drannith Magistrate is the best anti-pod card in the package** (a static hatebear that works under their Abolisher — the matrix's rec #1).
- **Net recommendation unchanged:** the swap should be pitched to the pod on disruption + resilience grounds, not speed. If it's applied, the Summary's kill window stays T7–8/T10 (slightly soft at T7–8).

---

## 5. Verdict vs the pod — and the matrix row

| | Exile's Return | Lightning War (for contrast) |
|---|---|---|
| Kill delivery | combat swarm, counters compound over 3–5 turns | one cast in Azula's combat, ignores blockers |
| Marquee-line availability T6 | 3% (Hellkite+Sozin, +tutors) | 47% (any of 4 finishers, +tutors) |
| Honest goldfish | **T7–8 decap / T10 table** | T6–7 table |
| Vs their Abolisher | ✅ own Abolisher + 9 spot removal + (pending) Drannith | races; Banefire uncounterable |
| Vs their blockers | bad-to-moderate (swarm is blockable; Hellkite/Appa fly) | irrelevant |

**Matrix consequence:** Clock cell corrected from "T6–8 ✅" to **"T7–8 decap · T10 table (lab)"** with the Clock flag downgraded to ⚠ — the deck does not reliably outrace a T6–7 combo win. **Verdict stays Favoured**, because the verdict never actually rested on the race: this is the roster's best *disruption-led* matchup (own Grand Abolisher protecting your turn + the largest removal suite pointed at theirs), and the pending Drannith swap strengthens exactly that axis.

**Answer to the user's two questions:** (1) T6–8 is one turn optimistic — real window T7–8 for one player, T10 for the table, at an unblocked ceiling. (2) No — there is no card the deck "needs" for speed; every tested add is noise, the $0 sideboard options (Cathars' Crusade, Outpost Siege) are the only ones worth considering at all, and the right pod play is the disruption package already pending, not a faster goldfish.

---

## Method caveats

- `er_speed_lab.py` is a **heuristic goldfish**, not a rules engine. Nothing blocks, nobody interacts, Zuko never dies, focus-fire is perfect. All of it favours the deck — real numbers are worse.
- Engine events are modelled deterministically (~1 event/engine/turn; Prosper's exiled card always playable) — mildly generous. Pan doubles only enters-from-exile events caused by creature/artifact entering (cast-from-exile triggers are not ETBs — verified). Counters land pre-combat only for pre-combat events; Norin/Circle/end-step loops pay off the *next* turn.
- Not modelled (small, conservative): Monk Gyatso, Windbrisk Heights, Dualcaster copying Sozin's Comet, Reconnaissance banking, Strionic-style second triggers, Karmic Guide/Sun Titan recursion (no deaths in goldfish), all removal/protection (pure dilution). Black Market Connections = flat +1 card/turn; Appa = 1 Ally per cast-from-exile event.
- Eldrazi Displacer's {2}{C} assumed payable (generous — the deck's colorless sources are thin).
- Reproduce: `python scripts/er_speed_lab.py --trials 40000` (seed fixed at 12345).

---

Related: `The_Exiles_Return_Summary.md` · `The_Exiles_Return_Swaps_2026-06-01.md` · `Pod_Matchup_Matrix.md` · `Lightning_War_Speed_Curve_Analysis.md` · `Replication_Crisis_Speed_Curve_Analysis.md` · [[project_exiles_return_bracket4_swaps]] · [[project_pod_combo_opponent]]
