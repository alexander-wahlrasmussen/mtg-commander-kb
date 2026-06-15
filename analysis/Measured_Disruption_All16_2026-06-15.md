# Measured Disruption for all 16 — closing pod_gauntlet limitation #2

**2026-06-15.** `pod_gauntlet.py`'s limitation #2: the disruption term `D` (P(we stop the
pod's combo turn through Abolisher)) was **delay_lab-measured** for only 3 decks (Grand
Design / Calamity / Lightning War) and **class-bucketed** for the other 13 — a soft 2-value
guess (`warn`=(0.50,0.14), `none`=(0.20,0.02)) read off the matrix's "Through Abolisher?"
column. This iteration replaces the bucket with **measurement for all 16**.

> Same discipline as every lab: `D` is answer **availability**, not effectiveness; it's a
> ceiling; trust the ranking and the corrections, not the second decimal.

Tools: `delay_lab.py` (13 new answer-suite configs + `--emit-json`) →
`analysis/delay_disruption.json` → `pod_gauntlet.py` reads it for all 16. The
lab→JSON→gauntlet pattern mirrors the clocks pipeline.

---

## 1. Method

Each deck's pod-disruption suite was inventoried (grep of the list for interaction +
**oracle verification** of every candidate, 2026-06-15) and classified into delay_lab's
engine: **C** counters, **R** instant removal, **P** preempt-only (sorcery removal /
sweepers / edicts, which help only via the kill-Abolisher-then-react chain), **S** statics.
The Abolisher-aware composition (scenarios A / B1 / B2 over a swept `a` = P(Abolisher out))
and the judgment weights (`W_static .75 / removal .90 / counter .50`) are delay_lab's,
unchanged. Per-deck calls, all oracle-cited in the configs:

- **Excluded** (established rules): redirects (Deflecting Swat, Imp's Mischief), protect-own
  (Veil of Summer — anti-counter + hexproof, not a combo stop), Snapcaster (yard-dependent
  value, deliberately unmodelled → understates).
- **Free-if-commander-out** (Fierce Guardianship / Deadly Rollick) priced 0 only behind a
  cheap, reliably-cast commander: free for Genome/Kuja-4, Replication/Satya-4, Exile's/Zuko-3,
  Crystal/Golbez-2; full cost for Curse/Scarab-5, Dark Lord/Sauron-6, Zero-Sum/Witherbloom-8
  (matching how delay_lab already prices GD's Atraxa-7).
- **Maindeck is ground truth:** the emit filters each config to cards actually in the parsed
  99 (correctly dropped sideboard counters in Replication / Dark Lord / Curse / Diminishing).

**Validation:** the three decks delay_lab already measured reproduce their hardcoded gauntlet
arrays **exactly** through the new pipeline (LW T6 `[77,63,50,37,23]`, Calamity `[52,41,30,19,8]`,
GD `[67,55,42,30,17]`) — so the configs and the emit are consistent with the prior hand-entered
values, and the only thing that changed for the roster is the 13 newly-measured decks.

---

## 2. The bucket was wrong in both directions

`D@a=0.30` (the realistic Abolisher band), measured vs the old class bucket:

| Deck | old bucket | measured | Δ | read |
|---|---|---|---|---|
| **The Replication Crisis** | none 15% | **50%** | **+35** | deep blue suite (5 counters + 5 removal); was mis-classed "none" |
| Earthbend the Meta | none 15% | 38% | +23 | removal + REB/Pyroblast; mis-classed "none" |
| Lorehold Spirits | none 15% | 21% | +6 | 3 white removal |
| Zero-Sum Game | none 15% | 20% | +5 | Golgari removal + Deed |
| Radiation Sickness | warn 39% | 42% | +3 | ✓ bucket ~right |
| Ms. Bumbleflower | warn 39% | 40% | +1 | ✓ |
| Curse of the Scarab | warn 39% | 38% | −1 | ✓ |
| The Exile's Return | warn 39% | 38% | −1 | ✓ |
| The Dark Lord's Army | warn 39% | 37% | −2 | ✓ |
| Eldrazi Stampede | none 15% | 14% | −1 | ✓ genuinely thin (2 answers) |
| **Diminishing Returns** | warn 39% | **22%** | **−17** | removal + edicts, **no counters** — bucket too generous |
| **Crystal Sickness** | warn 39% | **15%** | **−24** | lean 4-answer suite; bucket too generous |
| **The Genome Project** | warn 39% | **16%** | **−23** | thin 3-answer suite; bucket too generous |

The `warn`/`none` buckets were a coin-flip: right for the six honest control/midrange decks,
badly wrong for the rest. **"none" hid two real answer suites** (Replication, Earthbend);
**"warn" over-credited three thin ones** (Genome, Crystal, Diminishing).

---

## 3. The re-ranked board (decap, a=0.30)

`P(win)` old (bucketed) → new (measured):

```
deck                    old → new           what moved
Radiation Sickness      68 → 69    #1   ✓ (was #2)
The Genome Project      74 → 66    #2   −8  disruption over-credited; rides PURE RACE 63%
The Replication Crisis  47 → 60    #3   +13 biggest mover; real anti-pod contender now
Ms. Bumbleflower        49 → 48    #4   ✓
The Exile's Return      45 → 44    #5   ✓
Lorehold Spirits        41 → 42    #6   ✓
Earthbend the Meta      34 → 42    #7   +8  under-credited
Curse of the Scarab     40 → 38    #8   ✓
Lightning War           37 → 38    #9   (already measured)
Zero-Sum Game           35 → 36    #10  ✓
Eldrazi Stampede        28 → 28    #11  ✓
The Dark Lord's Army    25 → 24    #12  ✓
The Grand Design        25 → 24    #13  (already measured)
Diminishing Returns     26 → 18    #14  −8  over-credited
Crystal Sickness        14 →  9    #15  −5  over-credited
The Calamity Tax         4 →  4    #16  (already measured)
```

**Verdict shifts worth propagating to the matrix:**
- **Replication Crisis is a genuine anti-pod deck, not just a fragile racer.** The matrix
  rated its Through-Abolisher ❌ "counter-reliant, dead under Abolisher"; the measurement says
  its *removal* (Path/Swords/Pongify/Abrade/Generous Gift — proactive, survive Abolisher) plus
  a Satya-free FG carries 50% disruption at the realistic band. It's #3, not mid-pack.
- **Genome's top rank is now honestly a *race* rank**, not a disruption one (D 39→16). Its
  case rests entirely on PURE RACE 63% — and that's the goldfish-ceiling caveat, so its real
  standing is softer than the headline.
- **Diminishing / Crystal drop** — their reactive-light suites can't stop the combo turn as
  often as `warn` assumed.

---

## 4. Limitations

1. **Availability ≠ effectiveness** (delay_lab's standing caveat): a live answer doesn't model
   the pod's backup line or second protection piece.
2. **Inventory is broad but not exhaustive** — a missed answer *understates* a deck. The
   thin-suite decks (Genome 3, Eldrazi 2, Lorehold 3) are plausibly genuinely thin (combo /
   big-mana / aggro identities), but a deck-specific oddball could be missed.
3. **Drawn-only feeds the gauntlet** (its existing convention) — the with-tutors ceiling isn't
   used, so tutor-heavy decks are, if anything, *under*-credited here.
4. **Pyroblast/REB credited at face** though blue-conditional (the pod is partly blue);
   **edicts are dodgeable**; both lean optimistic, partly offset by the class weights.
5. Still a heuristic race model; decap (remove the archenemy), not table, is the headline.

---

## 5. Run it

```bash
python scripts/delay_lab.py --emit-json     # measure all 16 -> analysis/delay_disruption.json
python scripts/pod_gauntlet.py              # gauntlet now reads measured D for all 16
python scripts/pod_gauntlet.py --matrix     # regenerate the matrix quantitative rows
```

**Bottom line.** Limitation #2 is **closed**: disruption is measured for all 16, the soft
bucket is gone (fallback only for off-roster builds). The headline correction is **Replication
Crisis +13 (now #3)**; the cautionary one is **Genome −8** (its rank is a race ceiling, not
disruption). Calamity/GD/LW are unchanged (already measured) — and Calamity still sits last at
4%, now for the third independent reason this week (slow clock, no lock, and a *measured* — not
bucketed — leaky one-shot suite).
