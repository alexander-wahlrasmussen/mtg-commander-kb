# Mass Production (Baylen) — Kill-Turn Clock Lab (2026-07-11)

New-deck build (`workflows/WF_New_Deck.md` Stage 2 → `WF_Kill_Window_Lab.md`).
Lab: `scripts/mp_clock_lab.py` (20k trials, seed 20260711), built on `speed_lab_core.py`.
Deck: `decks/mass-production-20260711.txt` · Summary: `decks/Mass_Production_Summary.md`.
This is a **candidate** (not on the roster), so it is not wired into `pod_gauntlet.py`/
`deck_registry.py` yet — the clock stands on this lab alone until/unless it's promoted.

## Claim vs. measured

| | Claim (hand-estimate) | Measured (lab, 20k) |
|---|---|---|
| Goldfish decap | ~T8 | median **T7** (T6 ≈ 29%) |
| Goldfish table | ~T10 | median **T10** |
| Never-in-14 | — | decap 0% / **table 5%** |

```
  P(kill <= turn T) %                          5     6     7     8     9    10    12    14
  decap (one opponent, 40)                     8    29    59    80    90    95    99   100
  table (all three)                            1     3    12    26    45    63    86    95

  first-kill mixture: combat 82%  burn 9%  combat-infect 7%  combo 1%
```

## Direction: table confirmed, decap one turn FASTER than estimate (the atypical case)

The **table clock T10 is confirmed** exactly. The **decap clock came in a turn faster
than my hand estimate** (T7 vs ~T8) — the *opposite* of the framework's usual "hand
estimate is optimistic" pattern. Two reasons it front-loads on a goldfish:

1. **The doublers do the work the estimate under-weighted.** A single mass-token spell
   (Hop to It, Forth Eorlingas!, Awaken, Decree) under one doubler is 2× the bodies, and
   the Craterhoof/Finale alpha's swing scales with the *square* of the board (X per
   attacker). Once the board is wide, one focused swing decaps well before the estimate.
2. **Naya ramp is deep** (Sol Ring + 6 dorks + 3 land-ramp + Baylen's token-mana), so the
   8-mana Craterhoof / X=8 Finale threshold arrives ~T6–7 in a healthy fraction of hands.

**This decap is a goldfish CEILING** (unblocked, no interaction), and the primary kill is
`board` — go-wide combat is the *most* answerable kill shape (a fog, a chump, a wrath, or
instant removal on the turn all buy time; the pod runs flying blockers our ground tokens
must get through). So the *real* decap through interaction is later than T7, and the table
(T10) is board-vulnerable for 2–3 turns behind it. Read T7/T10 as the unblocked ceiling.

## The headline finding: the combo is resilience, not speed

Disabling the Broodscale infinite (`--mode nocombo`) gives an **identical clock — decap T7
/ table T10** — and the combo is only **1%** of first-kills. The deck goldfishes on its
fair go-wide plan (combat 82% / ETB-burn 9% / infect 7%); the Broodscale + Rosie/Cathars'
loop almost never *beats* that plan to the kill. Its value is **through interaction**: after
a board wipe blanks the combat line, the 2-card infinite is a compact, board-light way to
close that the goldfish (no wipes) doesn't reward. Don't sell this deck as a fast combo deck
— it's a fast go-wide deck with combo insurance.

## Kill-shape prediction (pre-registered) — held

Stage-1 priors: combat go-wide → decap-fast/table-via-trample (diverge); ETB-burn → converge;
combo → decap=table. Confirmed: combat is 82% of kills with a decap T7 / table T10 divergence
(~3 turns, the classic go-wide spread); burn/infect converge; combo (when it fires) is
`kill_all`. Kill-shape lens holds again.

## Card text (card_lookup.py 2026-07-11 — no new errors)

- **Craterhoof Behemoth** has haste; its +X/+X + trample counts this-turn deploys, so the
  alpha is a true same-turn distributed swing when the board is wide.
- **Finale of Devastation** *puts* a creature onto the battlefield — X=8 ({X}{G}{G} = 10
  mana) tutors Craterhoof into play for the same alpha, so Finale is a second copy of the
  overrun, not just a pump.
- **Purphoros** triggers on every *other* creature ETB regardless of devotion (pings while a
  non-creature); **Twinflame Tyrant** doubles it (and combat) to opponents.
- **Basking Broodscale + Rosie / + Cathars'** is a genuine 2-card infinite (counter→Spawn→
  counter); modelled as `kill_all` only when a pinger (Purphoros/Impact) is also out.

## Modeling caveats (heuristic, not a rules engine — all documented optimism)

- Mana = lands + rocks/dorks + land-ramp floor **plus a capped Baylen bump** (`min(3, tokens/2)`
  mana/turn once Baylen + a board are out) and a Baylen card/turn. Baylen's tapped tokens
  *can't attack*, but the model assumes token surplus and **does not dock attackers** — a
  real optimism on tight boards, negligible on wide ones.
- **Token multiplier** M = 2^doublers × (3 if Ojer Taq), applied to every token batch and
  thus to the Purphoros/Impact pings. **Capped M ≤ 12 and tokens/turn ≤ 50** so a triple-
  doubler god-hand can't print a fictional T3. Omitting doublers would bias slow (the WF's
  named failure); capping them bounds the tail, not the median.
- X-token spells (Awaken/Decree/Forth) scale with mana left after base cost; Forth's tokens
  have haste (attack the turn cast). Battle Screech's flashback and Adeline/Suki growth are
  under-counted (slow bias).
- **Damage unblocked** (goldfish convention). Go-wide ground tokens are the kill shape most
  flattered by "no blockers," so the real table clock is *slower* than T10 against the pod.
- Combo modelled as `kill_all` only with a pinger online; the infinite-tokens→Craterhoof and
  infinite-mana→Finale outlets are not separately credited (slow bias on the combo line,
  which is already only 1%).

## Verdict for the Summary

Replace `~T8 decap / ~T10 table (unverified)` with:
**`Clock: T7 decap / T10 table (board) (lab 2026-07-11, mp_clock_lab.py) · Through interaction: slower (unverified — goldfish, no blockers/disruption)`**

Pod-bar read (decap T≤7): the deck reaches a lethal-ish decap board ~59% of games by T7 **on
the unblocked ceiling** — but the kill is `board` (widest answer window) and the *table* clock
is T10, so it is a strong **table-presence / mid-speed** deck, not a T6–7 combo racer. That
matches the 15/20 (B) self-assessment: Core Loop carries it; Durability/Interaction (wipes,
no stack answers) are the ceiling, exactly where a go-wide deck is expected to sit.

---

## Owned / no-contention variant (`decks/mass-production-owned-20260711.txt`)

The primary list contends with the roster on ~25 cards (the premium top-end: Craterhoof,
Finale, Purphoros ×2, Moonshaker, Impact Tremors, Basking Broodscale, Adeline, Selvala, …).
The **fully-owned, zero-contention** rebuild keeps the go-wide engine (4 free doublers +
Ojer Taq + the free token-makers) and swaps the deployed premium cards for the best *free*
replacements: **Legion Loyalty** (myriad → table-wide), **Blossoming Bogbeast** (repeatable
Overrun-lite), **Salvation Colossus / Jazal Goldmane** (team pumps), **Elesh Norn** (anthem +
strips blockers), **Colossus of the Blood Age** (one-shot 3-to-each pinger), plus free ramp/
removal/draw/lands. The lab models both lists (run `--deck mass-production-owned-20260711`).

| | Primary (premium) | Owned (no-contention) |
|---|---|---|
| Decap median | **T7** | **T7** |
| Table median | **T10** | **T10** |
| never-in-14 table | 4% | 3% |
| First-kill mixture | combat 83 / burn 9 / infect 7 / combo 1 | **combat 99** / burn 0 |

**The goldfish clock is identical (T7 / T10).** The go-wide *engine* drives the clock, not the
specific finishers — a wide token board plus any Overrun/anthem/Twinflame gets there on the
same turn. The owned list is **99% combat** (vs 82%): it loses the ETB-burn axis and the
Broodscale combo as *first-kill* routes. The premium cards buy alternate axes + raw top-end,
not a faster median. If the pilot wants the premium list, the cheapest path is proxying the ~6
cards the roster double-books (proxies are used throughout the collection), not a teardown.

## Durability — wipe-recovery (measured, `--mode wipe`)

A first draft of this doc *asserted* the premium list was "more resilient" and the owned list
"the most wipe-vulnerable posture." **That was an unmeasured hand-wave; the wipe lab falsifies
it.** A creature board-wipe resolves on turn W (enchantment/artifact doublers, anthems, Impact
Tremors, and the indestructible Purphoros survive; every creature dies); the table-clock SLIP
vs no-wipe is the recovery cost.

| Wipe | Premium table (slip) · never-table | Owned table (slip) · never-table |
|---|---|---|
| none | T10 · 4% | T10 · 3% |
| @ T6 | T12 (**+2**) · 20% | T12 (**+2**) · **13%** |
| @ T8 | T13 (**+3**) · 29% | T13 (**+3**) · **22%** |
| @ T6 & T9 | T14 (**+4**) · 49% | T14 (**+4**) · **45%** |

**The median recovery is identical (+2 / +3 / +4), and the owned list is *marginally more
reliable* in the tail.** Why the premium "alternate axes" don't buy durability: (1) the burn is
board-*dependent* too — Purphoros survives the wrath but only pings on the tokens you rebuild,
so it stays ~9% and doesn't close a rebuilt small board any faster; (2) **Basking Broodscale is
a creature — it dies to the wrath**, so the combo is not wrath-resilient (it stays 0–1% post-
wipe). Meanwhile the owned list spent those slots on *more* token-makers, so it rebuilds a wide
board slightly more reliably (lower never-table). Net: **the two lists are within noise on
wipe-recovery; neither has a durability edge over the other.**

Scope caveat: this models a **creature wrath** (the common case). A Cyclonic Rift (bounce all
nonland) removes the surviving doublers/pingers from *both* lists, erasing even the premium
list's small burn edge — so under Rift the two are, if anything, *more* equal. The premium
list's real advantage is **top-end ceiling and answer diversity through combat interaction**
(fogs/blocks/spot removal), which this wrath model does not capture — not wipe-recovery, where
they tie. The combo's genuine resilience is against **go-wide combat hate and spot removal** (a
board-light 2-card close), *not* against wraths.

## Pod-overlay resilience — the owned list run through the roster labs (measured)

The wipe mode above is decklist-local. The roster's through-interaction oracles
(`self_meta_lab`, `interaction_meta_lab`) put a deck's Durability + Interaction into a
4-seat pod race. They iterate `delay_lab.ROSTER ∩ pod_gauntlet.CLOCKS ∩ MEASURED`, so the
owned list was **temporarily wired as a 17th seat** (an authored `delay_lab` answer spec —
6 instant-removal, 0 counters, 0 statics — + a `pod_gauntlet.CLOCKS` entry from its 20k
clock), the labs run, then the wiring **reverted** (the roster is canonically 16; permanent
promotion needs a freed seat). Reproduce by re-applying that spec/clock.

Baylen owned disruption (delay_lab, drawn, P(disrupt their T7)): **48% with no Abolisher →
5% under Abolisher** — good open, near-zero under the lock (no proactive statics; all-removal
suite). Honest profile for a Naya go-wide deck.

| Oracle | Result for Mass Production (owned) |
|---|---|
| **self_meta_lab** (P win, own-decks pod) | **#5 of 17** · CLOSE 30% / WIN 31% · table T10 · never-table 3% · **durability 0.79** |
| **interaction_meta_lab** (interaction-taxed) | **#5 of 17** · WIN(sm) 31% → INTER 29% · **Δ −2** · int 48% · prot 0% |

**This settles the resilience question in the owned list's favour.** On both roster oracles it
ranks **upper-third (#5/17)** — ahead of Radiation Sickness, The Exile's Return, Lorehold
Spirits, and The Replication Crisis. The interaction overlay barely moves it (**−2**, vs −6/−7
for genuine glass cannons): its own removal suite (int 48%) taxes opponents back and its
durability (0.79 — driven by a 3% never-table and 7 defensive answers) absorbs the field's
answers. The "99% combat-dependent glass cannon" my first draft implied is **falsified** — the
board kill is answerable, but the deck around it is measured as durable and interaction-robust.
Caveat: `prot` defaulted to 0 (I did not author a PROTECT index; a combat/counter-immune kill
arguably merits ~0.10, which would nudge INTER *up*, not down) — so this is the conservative read.

---

## Lever test — Walking Ballista ping axis (`--mode ballista`) — FLAT, drop for speed

Proposal under test: Baylen's tap-tokens mana battery + the counter-doublers (Doubling Season /
Branching Evolution / The Earth Crystal) + Cathars'/Rosie counter-feeds → **Walking Ballista**
as a board-independent, any-target ping payoff and a 3rd Broodscale outlet.
**Pre-registered prior:** clock unchanged (combat already carries T7/T10); ping shows up as
mixture + outlet redundancy; wipe recovery NOT improved (Ballista is a creature — dies to the
wrath). A/B: `-Harmonize +Ballista` (premium) / `-Battle Menu +Ballista` (owned), 20k each.

| | baseline | +Ballista | baseline wipe@T6 | +Ballista wipe@T6 |
|---|---|---|---|---|
| Premium | T7/T10 · nt 4% | T7/T10 · nt 4% · ping 1% | T9/T12 · nt 20% | T9/T12 · nt **18%** · ping 1% |
| Owned | T7/T10 · nt 3% | T7/T10 · nt 3% · ping 1% | T9/T12 · nt 13% | T9/T12 · nt **11%** · ping 1% |

**Prior held on every axis: the lever is FLAT.** Medians identical with and without the wrath;
ping leads only 1% of first-kills; the sole movement is ~2pp off the never-table tail post-wipe.
`find_combos` on the variant: **no new combos** — the Broodscale pairings already print infinite
colorless mana, so Ballista is outlet *redundancy* (a 3rd damage outlet), not a new line.
Per the lab-before-proposing rule (flat → resilience case or drop):

- **Owned list: DROP.** Ballista is contended (free 0) — adding it breaks zero-contention for a
  measurably flat delta. Battle Menu keeps its slot.
- **Premium list: optional flex, not a recommendation.** `-Harmonize +Ballista` trades a draw
  spell for outlet redundancy + unblockable spread. The one thing the goldfish cannot price is
  **blockers/fogs** (goldfish combat is unblocked, so the combat axis is flattered and the ping
  axis under-credited) — that residual case is *(unverified, judgment)* and is the only reason
  to run it. Do not buy/proxy Ballista for speed; the lab says it buys none.

---

## Keeper decision (2026-07-11): the OWNED list

With clock, wipe-recovery, and pod overlays all tied or favouring it, the owned list is the
deck. Premium draft archived (`archive/old_decklists/mass-production-20260711.txt`, still
runnable via `--deck <path>`); `mp_clock_lab.py` DECK repointed to the owned list;
`mass-production` → `deck_registry.EXTRA_COMMANDERS` (candidate, not a roster seat; quick
pytest gate green).

## Blockers — vs the Ur-Dragon fair board (vs_dragon_roster_lab, temporary wiring)

The goldfish's biggest flattery for this deck is "damage unblocked" — a ground-token swarm is
the kill shape most taxed by real blockers. The repo's blocking-board instrument is the
Ur-Dragon lab (fair flying wall, no combo turn; combat kills only connect at p≈0.22 through
the wall). Wired `mass_production` in temporarily (lock_lab DECKS/NAMES + KILL entry
`axis=combat, cdf=decap` + clocks-JSON curves), ran @20k, reverted all four files.

**P(win) = 50% — the BEST of the roster's nine combat-axis decks** (Replication 49%, Exile's
42%, Lorehold 39%, Bumbleflower 37%, Scarab 33%, Eldrazi 28%, Grand Design 20%), though far
behind the over-the-top drain decks (Genome 99% … Crystal 57%). Sweep-stable: 34% vs a fast
go-live, 67% vs slow; ranking position holds at every sweep point. Why best-of-combat: the
fastest measured decap CDF among them (T7) races the dragon's T6–9 go-live window, plus 4
spot-removal toolkit hits. Caveats: its only "wrath" credit is **Elesh Norn** (−2/−2 clears
their *tokens*, not 4/4+ dragons — mildly generous), and `axis=combat` is honest (Legion
Loyalty's myriad copies are blockable; only Angel/Herald fly). Read: ~coin-flip against a
blocking wall — race it early, don't grind into it.

## Smoothness — deck_sim --flow (20k trials)

| metric | Mass Production (owned) | context |
|---|---|---|
| keepable opening hand | **99.2%** | Lorehold 99.3% |
| has a play T2 / T3 / T4 | 79% / 96% / 99% | — |
| all colors (lands only) T3 / T5 | 72% / 87% | 3-colour floor; Birds/Fellwar not counted |
| **mean dead turns T1–10** | **1.88** | Lorehold 1.49 · Eldrazi Stampede 3.28 |
| dead-starved T2 → T6 | 30% → 9% | front-loaded, fades fast |
| hellbent (≤1 card) T8 / T10 | 30% / 41% | deploy-all upper bound; **Baylen's tap-3 draw is NOT in this model**, so real hellbent is lower |

Read: a smooth deck — near-universal keeps, a play in ≥96% of turns from T3, dead turns
closer to the roster's smooth end than its clunky end. The one flow risk is late-game hand
exhaustion, which is exactly what Baylen's tap-3-tokens draw (unmodelled by deck_sim's
generic flow pass) exists to patch — treat the 30–41% hellbent numbers as a worst case.

-----

## ADDENDUM 2026-07-17 — Akroma swap re-run (`mass-production-owned-20260717.txt`)

Physical assembly caught **4 phantom Moxfield copies** — Angel of Invention, Avenger of
Zendikar, Birds of Paradise, Skyclave Apparition all read "1 free" in the CSV while every
real copy is sleeved in another deck. Swapped for **Akroma's Will** (Angel's slot),
**Akroma's Memorial** (Avenger's 7-cmc slot), **Ilysian Caryatid** (Birds' slot),
**Stroke of Midnight** (Skyclave's slot). All four free-verified (`free_pool.py --check`,
self-exclusion bug fixed same day); GC stays 2/3.

Re-run @20k, seed 20260711, same grid:

| list | decap CDF T5–14 | table CDF T5–14 | med | never-table |
|---|---|---|---|---|
| 20260711 (pre-swap) | 8 / 30 / 62 / 83 / 92 / 96 / 99 / 100 | 0 / 1 / 8 / 24 / 49 / 71 / 91 / 97 | T7 / T10 | 3% |
| **20260717 (Akroma)** | 6 / 25 / 56 / 78 / 89 / 94 / 99 / 100 | 0 / 1 / 6 / 20 / 42 / 63 / 87 / 96 | **T7 / T10** | 4% |

**Medians HOLD.** Tails thin ~4–8pp (two token producers left the engine). Wipe mode:
never-table worsens (12→17% @T6, 21→29% @T8, 44→52% double-wrath) — **but the model's
wraths always resolve; it cannot hold Akroma's Will**, whose indestructible+protection
mode blanks a creature wrath outright. The lab also credits nothing for Memorial's team
haste (tokens attack the turn they enter) or Will's double-strike alpha. Treat the modelled
wipe worsening as the floor and the protection upside as real but unmodelled — the swap is
clock-neutral on medians with a qualitative resilience trade (engine tails ↓, wrath
counterplay ↑). Pod-overlay oracles (gauntlet 57%, self-meta, delay_lab) NOT re-harvested.
