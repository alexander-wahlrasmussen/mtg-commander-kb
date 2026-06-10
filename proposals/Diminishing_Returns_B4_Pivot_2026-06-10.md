# Diminishing Returns — Bracket-4-in-Spirit Pivot (2026-06-10)

**Deck:** Diminishing Returns (Teysa Karlov) · 17/20 · Clock: T9 decap / T12+ table (lab 2026-06-10)
**Lab:** `scripts/dr_clock_lab.py --mode b4` (12,000 trials, seed 12345)
**Context:** Follow-up to `proposals/Diminishing_Returns_Clock_Lab_2026-06-10.md`. User
direction: push toward Bracket-4-in-spirit (offensive, kill-reliable) while keeping the
3-GC cap; identity change away from Disrupt approved.
**Question:** Is the path more drain infinites, or faster mana?

---

## Verdict

1. **Combos, not mana — and it's not close.** The fast-mana package tested
   *below* baseline (table 26% vs 30% by T12). Mana was never the gate, and
   the cuts cost bodies — in this deck even goldfish-dead protection creatures
   contribute corpses, so non-creature adds must clear a higher bar.
2. **Compact 2-card kills are the real B4 axis, with bounded gains.** The
   6-swap combo core lifts table kills 30→37% by T12 and cuts never-kill
   70→63%; with the GC-slot reallocation (tutor GCs in, defensive GCs out)
   it reaches **41% / 59%, with 21% of games ending via combo (T8–12)**.
3. **It does NOT become a racer.** Decap stays T9 in every variant; the table
   median stays outside T12. Against the pod's T6–7 combo decks this build
   still doesn't win the race — what it gains is a credible "I can just win
   now" channel layered on the attrition game.
4. **Bracket consequence:** Leonin Relic-Warder + Animate Dead is an
   early-capable 2-card infinite — this formally breaks the B3 letter and
   **requires pod approval** (the 5th per-deck 2-card request; the standing
   note about documenting an exception in `REF_Bracket_3_House_Rules.md`
   applies here too).

## 1. The combo packages (all oracle-verified 2026-06-10, GC-screened clean)

| Combo | New cards | Why it fits |
|---|---|---|
| **Leonin Relic-Warder + Animate Dead/Necromancy** | 1 (LRW) | Auras already in deck. Loop: aura reanimates LRW → LRW ETB exiles the aura → aura leaves → LRW dies (sacrificed to the aura's leave-trigger) → LRW's leave-trigger returns the aura → re-reanimates LRW. Infinite ETB/death loop, zero mana once started — every loop death drains through Teysa-doubled payoffs. **Recruiter of the Guard tutors LRW (toughness 2); Razaketh finds all of it.** |
| **Nim Deathmantle + Grave Titan (+ Ashnod's Altar, in deck)** | 2 — **both owned, undeployed ($0)** | Sac Titan (+{C}{C}), pay {4} to Mantle, Titan returns with 2 Zombies; sac the Zombies (+{C}{C}{C}{C}) → mana-positive infinite nontoken deaths. Both pieces have standalone value (6/6 fodder engine; Mantle = wrath insurance). |
| **Exquisite Blood + Vito / Sanguine Bond** | 2–3 | Closed gain→lose→gain loop. In THIS deck any Zulaport-class death starts it automatically. Vito is also a standalone payoff: every gain becomes single-target drain (Teysa-doubled Kokusho death = gain 30 → 30 to a face). |

Screened and rejected: Mikaeus+Triskelion (Mikaeus deployed in Curse of the
Scarab, Trisk unowned, redundant with the above), Karmic Guide+Reveillark
(all 3 Guides and both Larks deployed), Burnt Offering (BR identity — not
Orzhov-legal).

## 2. Lab results (12k trials; cuts from the protection/removal shell)

| Variant | T8 table | T10 table | T12 table | never-12 | decap med |
|---|---|---|---|---|---|
| BASE | 1 | 10 | 30 | 70% | T9 |
| b4-combo6 (LRW, Vito, ExqBlood, Titan, Mantle, Grim Tutor) | 3 | 15 | **37** | **63%** | T9 |
| b4-mana4 (Cabal Rit, Culling, Jet Medallion, Crypt Ghast) | 1 | 9 | 26 | 74% | T9 |
| b4-tutor3 (Grim, Wishclaw, Final Parting — no new combos) | 1 | 10 | 33 | 67% | T9 |
| b4-full10 (combo6 + Wishclaw/Sanguine/CabalRit/Culling) | 3 | 14 | 34 | 66% | T9 |
| **b4-gcswap (full10 − Smothering Tithe − Farewell + Demonic + Vampiric)** | **5** | **18** | **41** | **59%** | T9 |

Cuts: combo6/full10 from Mother of Runes, Giver of Runes, Skrelv, Selfless
Spirit, Generous Gift, Swiftfoot Boots (+ Cathar Commando, Morbid
Opportunist, Wayfarer's Bauble, Vindictive Lich at 10).

**Readings:**
- **Tutors without combos are dead weight** (tutor3 ≈ base): there's nothing
  compact to find in the current list. Combos invert that — in gcswap the
  same tutors are the difference between 34% and 41%.
- **full10 ≤ combo6**: the 7th–10th swaps cost real bodies (Morbid, Lich)
  for marginal pieces. The efficient core is 6 swaps.
- **Combo fire rate in gcswap: 21% of games (T8–12 spread).** That, not the
  median, is the B4 payoff: roughly one game in five ends on the spot.

## 3. Recommended path (staged, pod approval first)

**Stage 0 — ask the pod.** LRW+aura is an early-capable 2-card infinite;
Deathmantle and Exquisite lines are 3-piece but tutored. This is
behaviour-B4 by the matrix taxonomy.

**Stage 1 — $0 (owned, undeployed):** + Nim Deathmantle, + Grave Titan,
+ Grim Tutor, + Jet Medallion (optional 4th) − Mother of Runes − Skrelv
− Giver of Runes (− Swiftfoot Boots).

**Stage 2 — ~€1–5 *(prices unverified)*:** + Leonin Relic-Warder — the
single most efficient combo card in the package (1 card, 2 in-deck
partners, 2 in-deck tutors that find it). + Wishclaw Talisman if wanted.

**Stage 3 — ~€30 *(Cardmarket checked 2026-06-10: Exquisite Blood €20–23,
Vito ~€9–13)*:** + Exquisite Blood + Vito. Defensible to skip — it's the
most expensive line and the least tutored-into in the sims.

**Stage 4 — GC reallocation (the measured best, but the costly one):**
− Smothering Tithe − Farewell, + Demonic Tutor + Vampiric Tutor (GC count
stays 3/3 with Teferi's Protection). All owned copies are deployed
(Demonic ×3: Scarab/Sauron/Calamity; Vampiric: Mothman) — this stage means
buying *(prices unverified, both premium)* or negotiating a steal from
another deck. Worth +7pp table and the deepest never-kill cut.

**Not recommended:** the fast-mana axis in any form (tested below base);
Final Parting for this deck (contested — claimed by the Calamity Tax
reanimator lean, and tutor3 showed it adds nothing here without combos).

## 4. What this does to the deck's profile

- Kill Reliability rises (a 21% on-the-spot channel + unchanged drain
  grind); Interaction falls (the protection shell pays for it — Teysa
  goes from 5 protectors to Greaves/Boots + Teferi's). Score impact if
  applied: likely 17/20 → 17–18/20 with the axis mix shifting offensive.
- The matrix entry should move from pure Disrupt toward Disrupt/Combo
  hybrid. It still should NOT be the pod-race answer — that remains the
  Witherbloom/Kefka class of proposals.
- Decklist NOT modified; no purchase made. Pending: pod approval, then
  stage selection.
