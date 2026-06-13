# The Calamity Tax — Kill-Turn Clock Lab + Version Bake-off (2026-06-13)

Deck 8 of the Kill-Window Lab Sweep (`campaigns/Kill_Window_Lab_Sweep_2026-06-13.md`), the
last of the two PARTIAL rows. Lab: `scripts/ct_speed_lab.py` (despite the name, a
kill-turn decap/table Monte Carlo — written 2026-06-10 but never run: it crashed on a
Windows cp1252 `◐` print, so the writeup it references never existed and the deck stayed
PARTIAL. Fixed the glyph, added the missing V3 variant + Witherbloom affinity, ran it).
40 000 trials, seed 12345. Commander: Glarb, Calamity's Augur (Sultai). Score: **18/20**.

**Outcome: clock measured + 4 versions compared; no version applied — the deck stays on
the committed V1 list. The user's call (2026-06-13): none of the swap-versions is up to
par; a different improvement direction is needed (not these swaps).**

---

## Claim vs measured — the biggest falsification in the sweep

| | Claim (Summary) | Measured (V1 committed, strict mana-floor goldfish) |
|---|---|---|
| Goldfish | T7–9 | **decap median T13 / table rarely resolves in 14** (47% of trials kill the table in 14T) |

The Summary's "T7–9" is fantasy on a strict goldfish. The deck is **hard mana-gated**: the
X-drain kill (Torment/Exsanguinate) wants ~16 mana for a lethal X, and assembling that
(Cabal Coffers + Urborg, or brute land count) without Seedborn lands ~T12–13. The
reanimator pivot's "fast line ~T5–6" is **also falsified** — it's a god-hand (T6 ≈ 1%).

**Important caveat (why T13 is a conservative floor, like Lightning War's strict goldfish):**
the lab deliberately omits **Seedborn Muse** — the deck's actual mana multiplier (untaps all
lands on every opponent's untap → ~4× land taps per cycle) — and all flash/instant-speed
casting, because the model is sorcery-speed. The *real* deck is faster than T13 once Seedborn
is online. But it is decisively **not T7–9**, and it cannot out-race the T6–7 Abolisher pod
(`project_pod_combo_opponent`). Direction of the correction is certain; the absolute T13 is a
floor.

## Kill shape — CONVERGE (mana-gated drain)

The kill is overwhelmingly hit-all drain (Torment/Exsanguinate hit every opponent; Gray/Kokusho
death-drains hit all) → decap ≈ table by construction. The combat/Archon focus-fire is a minor
chip. So the gap between decap and table is small; both are gated on the same mana threshold.
There is no "race one player" axis — this is an inevitability deck, not a tempo deck.

## Version bake-off (40k, seed 12345) — the swaps barely move the *turn*

| Version | decap | table | killed in 14T | line that carries | buildable? |
|---|---|---|---|---|---|
| **V1 committed** (current `.txt`) | T13 | never | 47% | xdrain 51% / copy 42% | deployed ($0) |
| **V2 31-May oppression** | T12 | never | 49% | xdrain 53% | ~$15–25 buys |
| **V3 06-01 Witherbloom/Dellian** | T12 | T14 | 50% | xdrain 55% | **impractical** (see ownership) |
| **V4 reanimator lean** | T12 | T14 | **56%** | copy 52% | ~$15–30 (mostly Loam-freed) |

**Read:** the swaps move the **kill rate** (47% → 56%) far more than the **kill turn** (all
T12–13). V4 is the best measured performer — its cheaper-mana copy/reanimator axis (Final
Parting tutor + Rite/Reanimate) fires more often than grinding to a 16-mana X-drain, and it's
the only version whose table reliably resolves (T14). V3's Witherbloom affinity nudges the
X-drain cheaper (kills shift to xdrain 55%, table resolves) but the gain over V2 is marginal —
a control deck rarely has the creature count for big affinity, so the 06-01 doc's "Torment
lethal 14→4 mana" was optimistic. None of the swaps addresses the structural problem (mana-gate
+ Seedborn-dependence), and **none out-races the T6–7 pod**.

## Ownership reality (the decisive constraint — `moxfield_haves_2026-06-07`)

The collection holds **exactly one copy of every relevant card**; the prior proposals' "owned
spare / 2nd copy" claims are all **stale** (this is the flagged "Calamity Sheoldred stale claim").

- **V3 is off the table.** Witherbloom (the only copy, a $190 foil) is now the **commander of
  Zero-Sum Game** (built 2026-06-11), and Dellian Fel is in that deck too. V3 would require
  buying a 2nd Witherbloom + 2nd Dellian — the 06-01 proposal predates the Zero-Sum build.
- **V4 is *mostly* free, not $0:** Final Parting / Jarad / Lord of Extinction are freed by the
  Loam teardown (owned, unallocated). But **The Scarab God is the Curse-of-the-Scarab commander
  (locked)**, Exsanguinate is in Genome, and Victimize is over-subscribed across 3 decklists on
  one physical copy → ~$15–30 of buys/pulls, and the package loses its resilience anchor (Scarab)
  unless bought.
- **V2** needs Sheoldred (Dark Lord's), Bloom Tender (Rad/GD), Mystic Remora (Replication),
  Exsanguinate (Genome) — all single copies deployed elsewhere → ~$15–25 buys/pulls.

## Decision (2026-06-13)

**Stay on V1 (committed `.txt`). No version applied.** Presented with the clock + the
ownership reality, the user concluded none of the swap-versions is up to par — all are
T12-gated, none races the documented pod, and the two that improve the kill rate most (V4) or
the feel (V3) carry real cost / a locked-commander conflict. The deck needs a **different
improvement direction**, not these swaps — to be figured out in a later session (open thread).

What a future direction would have to beat: the structural mana-gate + Seedborn-dependence.
Candidate angles to explore later (NOT proposed here): a genuinely lower-mana / board-independent
kill that doesn't need 16 mana or the yard; or leaning the deck into the Seedborn/flash
instant-speed plan the goldfish can't model (which may mean the deck is better than its floor and
the fix is pilot technique, not cards). Left for a fresh look.

## Card text

`ct_speed_lab.py`'s kill lines were card-text-verified 2026-06-10 (per its docstring). This
session's additions — Witherbloom affinity (generic-cost relief on I/S spells, modelled as a
creature-count discount on the X-drain + Rite/Doppel) and Dellian Fel (0: draw) — match the
oracle text verified in `The_Calamity_Tax_Swaps_2026-06-01.md`. No new card-text errors.

### Summary Kill Window field → replace with

**`Clock (strict mana-floor goldfish, Seedborn/flash excluded): T13 decap / table rarely in 14 (lab 2026-06-13, ct_speed_lab.py) — hard mana-gated; "T7–9" falsified. Real clock faster with Seedborn online but not T7–9, and does not out-race the pod. Version bake-off: see analysis/Calamity_Tax_Kill_Turn_Lab_2026-06-13.md`**
