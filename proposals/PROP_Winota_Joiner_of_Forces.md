# Proposal: Winota, Joiner of Forces — "dismantle 3, build 1"

*Status: PIPELINE (un-built candidate). Raised 2026-06-18; clock RE-VERIFIED 2026-06-29
after a lab-bug fix (see the correction note below) — the original 2026-06-19 verdict was wrong.*
*Decklist: `decks/considering/winota-joiner-of-forces-20260618.txt` (100, parses clean, 3/3 GC).*
*Lab: `scripts/winota_clock_lab.py`.*

This is the answer to "dismantle 3 decks to build 1 strong deck (not a proposal)."

> **2026-06-29 CORRECTION.** The original verdict below — mid-speed, "structurally can't
> close the table" — was an artifact of a lab bug. `winota_clock_lab` set `self.winota=True`
> only when it found her *in hand*, but she is the commander and never appears there, so it
> clocked a Winota deck **without Winota's flood engine** (the engine fired in 0/3000 trials).
> With the command-zone deploy fixed, she is a **genuine racer**: decap **T6–7**, table
> **T9–10**, ~1% never-table. The "fast racer" pitch is now *supported*, not falsified.
> The corrected lab verdict and bottom line are below; the teardown/funding/engine sections
> were never affected by the bug and stand as written.

---

## The teardown (which 3, by RESULTS not score)

Per `analysis/Definitive_Tier_List_2026-06-15.md`, the three worst decks by the
results-weighted composite — the whole **D-tier** — are the cut:

| Deck | Colors | Anti-pod | Self% | COMP | Why |
|---|---|--:|--:|--:|---|
| Eldrazi Stampede Chaos | Temur | 26% | 11% | 16 | lowest on every axis; "clearest next project" |
| Crystal Sickness | Dimir | **9%** | 12% | 20 | worst anti-pod on the roster; dev-gated |
| Diminishing Returns | Orzhov | 17% | 4% | 22 | >T14 table, 70% never-close |

**Genome Project is NOT cut** — it is S-tier (the pod-championship winner, decap T8 =
table). The first draft of this analysis wrongly flagged Genome on its 15/20 Conversion
score; that is the exact `score ⊥ results` trap the lab stack exists to catch.

**Funding:** Diminishing Returns donates the white half (23 W cards incl. Mother of
Runes, Esper Sentinel, Recruiter of the Guard, **Grand Abolisher**, **Smothering Tithe**);
Eldrazi Stampede the red half + **Ancient Tomb**; Crystal Sickness ~33 colorless staples.
Two of the deck's three GCs (Ancient Tomb, Smothering Tithe) are literally freed by the
teardown.

---

## Commander & engine

**Winota, Joiner of Forces** `{2}{R}{W}`, Legendary Creature — Human Warrior, 4/4 (RW).
*Not a Game Changer* (removed from the GC list 2025-10-21 — verified in
`REF_Game_Changers_List.md` "Cards Removed").

> *card_lookup verified 2026-06-18:* "Whenever a **non-Human** creature you control attacks,
> look at the top six cards of your library. You may put a **Human** creature card from among
> them onto the battlefield tapped and attacking. It gains indestructible until end of turn."

The clock = (# non-human attackers each combat) → that many digs → flood Humans in
**attacking**. So the deck pairs a bank of cheap **non-human triggers** (Ornithopter/Memnite
0-drops, Ragavan, Myr dorks, Siege/Spawn-Gang token banks, Goldspan, Oketra's 4/4s) with a
dense **Human payoff** suite (ETB value + the Human-ETB lords Erkenbrand/Théoden/Lossarnach
+ Adeline). **It closes on YOUR turn through combat — Grand Abolisher does nothing to it**,
which is why it was floated as the answer to the Abolisher-combo archenemy.

GC package (3/3): **Ancient Tomb · Smothering Tithe · Drannith Magistrate** (the last is
anti-combo hate *and* a floodable Human). Wrath insurance is non-GC: Flawless Maneuver,
Selfless Spirit, Guardian of Faith, Clever Concealment, Boros Charm.

---

## Clock lab — the verdict (corrected 2026-06-29)

`scripts/winota_clock_lab.py`, 40k goldfish, decap (one opp @40) vs table (all three),
bracketed by the deck's haste package (no-haste floor ↔ all-haste ceiling). **The flood
engine is now live** — the lab deploys Winota from the command zone (the fix; see the
correction note up top):

| | decap median | table median | never-table in 14 |
|---|--:|--:|--:|
| **floor** (no haste) | **T7** | T10 | 1% |
| **ceiling** (all haste) | **T6** | T9 | 1% |

**Clock: T6–7 decap / T9–10 table (lab 2026-06-29).**

**This SUPPORTS the "fast racer / pre-empt the combo" pitch** — both original findings
reverse once the engine fires:

1. **Decap is at the racer tier.** T6–7 sits with Genome/Radiation/Replication (decap T7),
   not "mid-pack behind the racers" as the engine-less lab reported. That is fast enough to
   pre-empt the pod's ~T6–7 combos, and because it closes through **combat on your own turn,
   Grand Abolisher does nothing to it** — the original reason it was floated against the
   Abolisher-combo archenemy.
2. **The table does close.** Once the triggers snowball the board (Erkenbrand pumps +
   flooded Humans + Adeline bodies), the excess power spills across seats: table **T9–10**,
   and only **~1% of games never table** in 14 turns — not the 26–43% the broken lab showed.
   The "structurally can't close" claim was an artifact of clocking a small, non-snowballing
   board; the real engine goes wide enough to spill.

**Model honesty (caveats unchanged):** OPTIMISTIC — unblocked, no removal/wraths. For a
go-wide deck that walks into blockers + sweepers this is a real ceiling — but it is **the
same ceiling every racer's goldfish clock is measured at**, so the racer-tier comparison is
apples-to-apples. CONSERVATIVE — flooded-Human power fixed at 2, and the combat amplifiers
(Théoden double strike, Iroas, Odric keyword-share, Adriana melee, hardcast-Human Erkenbrand
pumps) are **omitted**, so the true clock is, if anything, a touch faster than stated.

---

## Honest bottom line

As built, Winota is a **genuine pod-racer**: decap T6–7 (racer tier) and a table that
reliably closes T9–10 (~1% never), all on your own turn through combat — so **Grand
Abolisher and the counterspell-combo archenemy do nothing to it**. The "race the Abolisher
pod" thesis the deck was pitched on is **supported** by the lab (once the engine-deploy bug
was fixed). It fits the B4-in-spirit / offensive taste and is Abolisher-proof by construction.

The standard go-wide caveat holds: it walks into blockers and sweepers, so the wrath
insurance (Flawless Maneuver, Selfless Spirit, Guardian of Faith, Clever Concealment, Boros
Charm) is load-bearing, not flex. But the speed is real and at the front of the roster.

**The open question is now a roster decision, not a build-quality one.** Winota's decap
*matches* the existing T6–7 racers (Genome/Radiation/Replication) with a table a turn or two
behind a drain-combo racer's — a peer of them, not a clear upgrade. So "dismantle 3 to build
Winota" trades three D-tier decks for a *fourth* top-tier racer plus an Abolisher-proof angle:
strong if you want redundancy in the race plan, less compelling if the goal is to diversify
*away* from racing. User's call — but the deck is no longer the disappointment the old verdict made it.

The Human (366) / Wizard (136) collection depth that motivated this stands, and the go-wide
combat plan now looks like the right way to spend it.
