# Proposal: Winota, Joiner of Forces — "dismantle 3, build 1"

*Status: PIPELINE (un-built candidate). Raised 2026-06-18, lab-verified 2026-06-19.*
*Decklist: `decks/considering/winota-joiner-of-forces-20260618.txt` (100, parses clean, 3/3 GC).*
*Lab: `scripts/winota_clock_lab.py`.*

This is the answer to "dismantle 3 decks to build 1 strong deck (not a proposal)." The
build is honest-first: the clock lab **does not confirm** the fast-racer framing it was
pitched on. Read the verdict before committing.

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

## Clock lab — the verdict (this is the important part)

`scripts/winota_clock_lab.py`, 40k goldfish, decap (one opp @40) vs table (all three),
bracketed by the deck's haste package (no-haste floor ↔ all-haste ceiling):

| | decap median | table median | never-table in 14 |
|---|--:|--:|--:|
| **floor** (no haste) | **T9** | T14 | 43% |
| **ceiling** (all haste) | **T8** | T13 | 26% |

**Clock: T8–9 decap / T13–14 table (lab 2026-06-19).**

**This falsifies the "fast racer / pre-empt the combo" pitch.** Two findings:

1. **Decap is mid-pack, not fast.** T8–9 sits with Earthbend/Lorehold/Scarab (T8), *behind*
   the real racers (Genome/Radiation/Replication decap T7). The pod's combos assemble ~T6–7
   behind Abolisher — Winota is a turn or two too slow to pre-empt them.
2. **The table clock is the real, structural weakness.** Focus-fire combat through 120 life
   across three seats is slow, and going wider doesn't fix it (you can't split enough power).
   26–43% of games never table inside 14 turns. **It decaps one player but doesn't reliably
   close the game** — the same "can't close" bucket much of the roster already lives in.

**Model honesty (cuts both ways):** OPTIMISTIC — unblocked, no removal/wraths (a real cost
for a go-wide deck that walks into blockers + sweepers; this is a ceiling). CONSERVATIVE —
flooded-Human power fixed at 2, and the combat amplifiers (Théoden double strike, Iroas,
Odric keyword-share, Adriana melee, hardcast-Human Erkenbrand pumps) are **omitted**, so the
true decap is plausibly ~1 turn faster (≈T7–8). Even crediting that, the table clock stays
slow — that's structural, not a modelling artifact.

---

## Honest bottom line

As built, Winota is a **solid mid-speed go-wide deck, not a pod-solving racer.** It is
Abolisher-proof and offensive (fits the B4-in-spirit taste), but it neither out-races the
combo pod nor closes the table — so it would not clearly beat the Radiation/Genome/Replication
decks already on the roster. The "race the Abolisher pod" thesis is **not supported** by the lab.

**Open directions (user's call):**
- **(A) Iterate toward a real alpha-strike** — the current list is top-heavy (five 5-drops,
  midrange value Humans). A leaner curve + more haste/evasion (Rogue's Passage already in) +
  an actual overrun finisher could pull both clocks in; re-lab to test. *Most promising.*
- **(B) Accept it as a mid-speed deck** and rank it honestly (likely B-tier), not as a racer.
- **(C) Reconsider the commander** — if the goal is a *racer*, a tighter combo/aggro shell
  may serve better than go-wide combat.

The Human (366) / Wizard (136) collection depth that motivated this still stands; the
question is whether Winota's go-wide combat is the right way to spend it.
