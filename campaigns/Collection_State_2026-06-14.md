# Collection State — snapshot, 2026-06-14

A point-in-time read of where the collection stands, produced by running the full
tool stack built this week against the live files. Not a new analysis — a synthesis
of what the tools already say, with the loose ends named. Every number below is
reproducible by re-running the cited command.

Regenerate this picture:

```
python scripts/validate.py            # legality + structural lint
python scripts/clock_check.py --strict # do Summary clocks still match the labs?
python scripts/pod_gauntlet.py        # P(beat the T6-7 combo pod)
python scripts/unlock_optimizer.py    # over-committed cards + one-purchase unlocks
python scripts/kill_tree.py --all     # the win-line decision trees
```

---

## 1. Health — is the repo internally consistent?

| Check | Result | Source |
|---|---|---|
| Decklist legality / 100-count / GC≤3 / filename uniqueness | **1 error, 11 warn** | `validate.py` |
| Summary kill-window clocks vs the labs | **16/16 match · 0 drift** | `clock_check.py --strict` |

**The one error** is the only red mark in the collection: the *active* Radiation
Sickness list `radiation-sickness-20260513-phaseC.txt` runs **4 Game Changers**
(Cyclonic Rift, Seedborn Muse, Survival of the Fittest, Vampiric Tutor) — Survival
is the uncounted 4th. The fix list `radiation-sickness-gcfix-20260614.txt` already
exists and validates clean (GC 3/3); it just hasn't been promoted to the active
slot. This is a $0, mandatory swap — see §4.

The 11 warnings are benign: unresolved card names inside `decks/considering/`
external lists (UB/FF reskins the alias table doesn't cover yet) and the retired
Loam summary's uncited turn-window line. None block anything.

**The clock ledger is spotless.** Every active Summary's `Kill Window / Clock:`
line is within ≤2 turns of its lab's measured decap/table median. The verify-loop
(`clock_check`) is doing its job — the systematic-optimism gap that started the
whole lab campaign (`Framework_Clock_Gap_2026-06-09.md`) is closed and staying
closed.

## 2. Anti-pod standing — who actually beats the T6-7 combo pod?

From `pod_gauntlet.py` (decap clock, Abolisher P(out)=0.3, 40k trials). `PURE RACE`
= P(decap ≤ opponent's combo turn), disruption ignored; `P(WIN)` folds disruption
back in. The gap between them = how much a deck leans on interaction vs raw speed.

| Tier | Decks | Read |
|---|---|---|
| **Race leaders** | Genome Project (P(WIN) 73%), Radiation Sickness (68%) | Goldfish ceilings — they out-run the pod on raw clock (decap T7, 57-63% pure race). The two strongest anti-pod decks, and both now have kill-trees (§3). |
| **Mid — race + light disruption** | Replication Crisis (47%), Bumbleflower (49%), Exile's Return (45%), Lorehold (41%), Scarab (40%) | Real decap clocks (T7-8) but thinner margins; win rate sits near the pure-race line. |
| **Disruption-led** | Lightning War (37% — but 56% if Abolisher stays home), Grand Design (24%/36%), Calamity Tax (4%) | These *don't* race — `PURE RACE` is 1-12%. Their win rate is bought almost entirely with measured disruption (`delay_lab`), so they swing hardest on P(Abolisher out). |

**The standout finding still holds:** Calamity Tax scores 18/20 on the Conversion
Check but lands **dead last** on P(beat pod) at 4% — its decap clock is T13. High
audit score and a fast clock are nearly orthogonal at the top of the roster; the
fortress decks score well precisely because they grind rather than race.

## 3. Win-line legibility — kill-trees

`kill_tree.py` now draws **4 decks**, rendered in `analysis/kill_trees/` (validated
via the Mermaid Chart tool, dark-theme-safe styling):

- **Genome Project** & **Replication Crisis** — the two race leaders, added today.
  Genome's tree shows the *converging* clock (pings hit every opponent, decap≈table);
  Replication's shows the *diverging* one (decap T7 / table T10+) and surfaces its
  defining fragility — every line is gated on a 3/5 commander connecting in combat.
- **Radiation Sickness** & **Diminishing Returns** — the grind/disrupt pair.

Coverage gap: the disruption-led decks (Lightning War, Grand Design, Calamity Tax)
aren't drawn yet — their "kill" is mostly a tax/delay clock, which the ladder format
fits less cleanly. Candidate next encodes if the tool gets revisited.

## 4. Buy pressure — what unlocks the live builds?

From `unlock_optimizer.py` (16 active decks + the two live builds: Kefka
forced-liquidation + Hashaton Thoracle; owned **+ proxy** netted out).

**Over-committed owned staples** (real demand exceeds physical copies):
- **Ponder, Preordain** — short 2 each (0 proxy backfill).
- **Demonic Tutor, Vampiric Tutor** — short 2 each, and both are **Game Changers** —
  contention here is GC-budget contention, not just copies.
- Phyrexian Tower, Arcane Denial, Go for the Throat, Razaketh — short 2.

**Shared one-purchase unlocks** (serve *both* live builds, own 0 real):
Go for the Throat, Drown in the Loch, Echo of Eons, Windfall. Buy these first —
each clears a slot in two builds at once.

## 5. Loose ends / open decisions

1. **RS GC-fix swap — pending, $0, mandatory.** Promote
   `radiation-sickness-gcfix-20260614.txt` to the active slot, archive the phaseC
   list. Clears the only error in the repo. *Note:* it changes physical deck state
   (pull Survival of the Fittest), so it's the user's call to execute.
2. **Hashaton vs Calamity redundancy — still flagged OPEN.** Memory flags Hashaton
   (Thoracle) and the Calamity build as redundant Thoracle decks, but Calamity was
   rebuilt toward a grind fortress (Thoracle dropped). Whether that de-conflicts
   them or they still overlap needs a look at the two live `.txt` files before
   committing buys to both.
3. **Loam summary** carries a turn-window line with no lab citation — but Loam is
   being dismantled, so this is cosmetic.

## 6. What shipped this week (context)

All four `Backlog.md` tooling ideas are live, plus the lab harness underneath:
`validate.py`, the clock-lab harness (`speed_lab_core.py` + 16 `*_clock_lab.py`),
`pod_gauntlet.py`, `clock_check.py`, `unlock_optimizer.py`, `kill_tree.py`. The
collection now has a closed loop: estimate a clock → lab it → cite it in the Summary
→ lint that the citation stays true → race the cited clocks into a pod win-rate →
draw the win lines. The remaining gap is real-pod data — every clock here is an
unblocked goldfish ceiling; no game-result feedback has been folded in yet.

---

*Snapshot only — regenerate the numbers, don't cite this doc as the source. The
tools are the source.*
