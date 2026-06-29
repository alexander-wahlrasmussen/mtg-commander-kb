# REF — Multiplayer Card Evaluation

Two fast card-reading heuristics for a four-player format, lifted from the "I've
built 500 decks" Commander video (YouTube `gjS2jb5j_Xs`, 2026-05-27) and
reconciled with this repo's labbed findings. Both are **screening filters** — they
tell you which way a card's power *scales* before you commit a slot. They do **not**
override a clock/pod lab for our specific pod; where they disagree with a sim, the
sim wins (ground-truth hierarchy + memory: `feedback_lab_before_proposing`).

Operationalised by `deck_doctor.py --fragility` (the durability ladder below).

---

## 1. The multiplayer-scaling filter

Commander has four players and four turns per cycle instead of two. That single
fact re-weights every card. Read a card's trigger/cost language and ask which
column it falls in.

### Scales UP in multiplayer (lean in)

Effects that key off *other people* or *the whole table* fire ~3–4× as often as in
1v1:

- **Whenever an Opponent** … / **A Player** … / **Whenever a Player** …
- **Each Opponent** / **Each Player**
- **Each Upkeep** / **Each End Step** (every player's, not just yours)
- **Triggered abilities that do *not* include "you"/"your"** (symmetric triggers —
  e.g. Soul Warden "whenever *any* creature enters", Authority of the Consoles)
- **Until your next turn** (covers three opponents' turns, not one)
- **Once per turn** abilities you can use on *each* player's turn
- **Each / total on the battlefield** (counts the whole board)

Canonical payoffs that are near-unplayable in 1v1 and dominant here: Rhystic Study,
Smothering Tithe, Soul Warden / Authority of the Consoles, Phyrexian Arena-style
per-upkeep engines. Authority of the Consoles actually scales *harder* than Soul
Warden going 2→4 players (3× vs 2×), because it only ever triggered off opponents.

### Scales DOWN in multiplayer (discount, don't ban)

Effects gated to *you* or *your turn* get one trigger per four-turn cycle:

- **Your upkeep** / **your end step** (yours only)
- **Only on your turn** / **Sorcery speed**
- **When ~ attacks** / **Whenever ~ deals combat damage** (one combat per cycle)
- **Tap** (the permanent is tapped out three opponents' turns out of four)
- **Under your control** (your board only)
- **Target** (one target in a four-target world)

Discount, not delete: Sol Ring is on the "scales down" side of this filter and is
still arguably the best card in the format. The filter ranks a card's *upside vs.
its rate*, not its raw power.

---

## 2. The permanent-type durability ladder

When the engine matters, *which permanent type* it lives on decides how easily a
board wipe or spot-removal dismantles it. As Commander has sped up, board wipes
have become more common, so this exposure matters more, not less.

**Easiest → hardest to remove:**

| Rank | Type | Why |
|---|---|---|
| 0 | **Planeswalkers** | attacked down by the whole table; cheap PW removal |
| 1 | **Creatures** | every board wipe + the deepest removal pool |
| 2 | **Artifacts** | narrower removal; dodge creature wipes |
| 3 | **Enchantments** | narrower still; dodge creature + artifact wipes |
| 4 | **Battles** | rarely-answered permanent type |
| 5 | **Non-basic lands** | almost nobody runs land destruction in casual pods |
| 6 | **Basic lands** | effectively unremovable (and house-banned MLD aside) |

**Reading rule:** a card is as fragile as its *most removable* type. An artifact
creature dies to creature removal, so it reads as a creature (rank 1), not an
artifact. A Vehicle that is not currently a creature stays an artifact (rank 2) and
dodges creature wipes — the Ratchet, Field Medic point from the video.

**Build implication (video lesson 2 — resilience):** prefer to host your *engine*
on durable types; if it must sit on creatures, pay for it with the other two
resilience sub-levers — protection, and fast rebuild (full hand, low-CMC pieces,
recursion). A pure go-wide/aggro deck accepts a fragile base on purpose because it
wins before the wipe lands.

`deck_doctor.py --fragility` reports the % of a deck's nonland permanents on the
two most-removable tiers and flags any `win_line` engine piece on a fragile type.
It is type-only and INFO-only — it can't see *our* pod's actual answer density,
which lives in `delay_lab.py` / interaction-meta modelling.

---

## How this fits our framework

These are screening heuristics that feed the spine metric (video lesson 8,
"value-to-turn ratio" = our decap/table **clock**). The multiplayer filter is a
*card-selection* lens; the durability ladder is a *resilience* lens
([[reference_trinketmage_win_any_game]], `deck_doctor --interaction`). Neither
replaces a sim: for our pod, route resilience questions to `pod_gauntlet.py` /
`delay_lab.py` and speed questions to the `*_clock_lab.py`.
