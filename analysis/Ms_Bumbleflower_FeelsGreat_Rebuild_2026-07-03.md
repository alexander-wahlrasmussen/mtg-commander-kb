# Ms. Bumbleflower — the "Feels Great to Play" rebuild (2026-07-03)

**The challenge (user, 2026-07-03):** *"create a new deck or modify an existing deck into one
that feels great to play"* — defined as: (1) always a play to make on your own turn, (2) a tight
game plan that **isn't** always tutoring the same combo to finish, (3) not an immediate
archenemy, (4) not obvious to the table how it wins. "One of those decks you just play when you
want to enjoy a game of magic."

**Result:** the 2026-07-03 **"quiet exits" package** for Ms. Bumbleflower — a 3-card swap,
2-card buy (≈ €6 indicative), measured before/after on every axis of the brief. New list:
`decks/this-bunny-goes-to-market-20260703.txt`. Score 15→**16/20** (Kill Reliability 3→4).

---

## 1. The brief, turned into measurements

Each "feel" criterion maps onto an instrument this repo already has:

| Criterion | Instrument | Metric |
|---|---|---|
| always a play on your turn | `deck_sim.simulate_flow` (paced, draw-aware) | mean dead turns T1–10; hellbent@T8 |
| tight plan, not one tutored combo | `bmf_clock_lab` all-lines goldfish | **close-mixture** — which line actually tables each game |
| not an immediate archenemy | `deck_doctor` GC / salience review | GC count; no Rhystic/Tithe-class hate magnets |
| non-obvious win | kill-line inspection + footprint | exits assemble from value cards; fp% low |
| …and still wins | clock lab + pod context | decap/table medians + front edge |

## 2. Why modify Bumbleflower (and not rebuild Eldrazi or build new)

The 2026-07-03 smoothness sweep + tier list v2 frame the roster choice:

- **Ms. Bumbleflower** was already the 2nd-smoothest deck on the roster (0.61 dead turns
  T1–10; only Crystal Sickness is smoother), the only 0-GC deck, instant-speed control texture,
  low early threat profile — criteria 1, 3, 4 essentially native. Its **one** documented defect
  (Summary, clock lab, tier list all agree) was criterion 2's flip side: *"stalls between
  dominating and finishing"* — a slow, combat-only close (decap T8 ceiling / table T11, 3-turn
  gap, all three lines combat).
- **Eldrazi Stampede** (the tier list's "clearest next project") fails 3 of 4 criteria natively
  (3.15 dead turns — worst on the roster by 2×; big-stompy is obvious and archenemy-visible).
  A rebuild there is a *power* project, not a *feel* project.
- **A new build** would fight the mechanical-distinctiveness filter (the remaining candidate
  ideas — Hinata, Krark+Sakashima — overlap the existing spellslinger/copy decks) and buys ~100
  cards to reach a feel Bumbleflower already has at 97/100 owned.

## 3. The design: three quiet exits, found via `find_combos`

Per [[feedback_verify_kill_shape_before_labbing]], the kill shape came from the combo-adjacency
map, not from vibes: `find_combos.py this-bunny --almost-max 1` showed the deck **one card away**
from several closes that assemble from cards it already runs. Three were chosen for
low salience + zero tutor-dependence; every card oracle-verified via `card_lookup.py` first:

| Out | In | Slot logic |
|---|---|---|
| Misleading Signpost ({2}{U} rock + one-shot trick) | **Intruder Alarm** ({2}{U}) | weakest ramp slot → the loop engine |
| Sin, Unending Cataclysm ({5}{G}{U} slow finisher) | **Approach of the Second Sun** ({6}{W}) | 7-drop finisher → 7-drop alt-win |
| Rewind ({2}{U}{U}, clunkiest of 7 counters) | **Wizard Class** ({U}, staged) | curve down, gas up |

- **Approach**: second cast from hand = win. Ruling-verified: the win checks the first copy was
  **cast, not resolved** — so **Reprieve** (already in deck) bouncing your *own* first cast back
  to hand banks the cast and sets up a 9-then-7-mana win, protected by the counter suite.
  Combat-free, wipe-proof, and the deck's draw engine (2–4 cards/turn) re-finds the natural
  7th-from-top copy in ~2 turns anyway.
- **Intruder Alarm**: with Shrieking Drake / Whitemane Lion (both already in) + any repeatable
  dork, each self-bounce recast is mana-neutral (Alarm untaps all creatures on every ETB) and a
  Bumbleflower trigger → "target opponent draws," iterated → **the table draws out**. Lion makes
  it instant-speed. Per-iteration resource delta traced per
  [[feedback_trace_combo_loop_not_just_cards]]: Drake {U} in, Chocobo 1-any out = net 0; Druid
  with a Bumbleflower counter taps for 3 alone.
- **Wizard Class**: lvl 3 + Fathom Mage (already in) = draw the library at will ("may" draw —
  stop anywhere). An enabler, not a kill: feeds Jolrael X and finds whichever exit is live.
  Levels 1–2 are honest standalone value.

Gates all passed: none of the three is a Game Changer (deck stays **0/3**); no reskin aliases
involved; Intruder Alarm's only other appearance is the *shelved* Berta candidate list (not
deployed); house rules OK (infinites pod-accepted 2026-06-19; no MLD; no extra turns); colour
identity W/U/U ⊆ GWU; all Commander-legal.

## 4. Measured before → after (same instruments, same seeds)

**Clock** (`bmf_clock_lab.py`, extended to the all-lines model — min over correlated draws on
ONE game, the Backlog #11 discipline; baseline verified to reproduce the committed 2026-06-13
curve before comparing):

| | baseline (20260404 list) | quiet-exits (20260703 list) |
|---|---|---|
| decap median | T8 (T7 39%) | T8 (T7 36%) — small honest cost of reserving combo pieces |
| table median | T11 | T11 |
| **P(table ≤ T9 / T10)** | 3% / 17% | **15% / 35%** |
| never-in-14 (table) | 2% | 2% |
| **close-mixture** | combat 100% | **combat 59% · Approach 32% · Alarm 9%** |

*(@40k, seed 20260613. The front edge — not the median — is where the "stall" lived: the odds
of actually finishing by T10 doubled.)*

**Flow** (paired A/B, plan keep + draw on, 8k):

| | baseline | quiet-exits |
|---|---|---|
| mean dead turns T1–10 | 0.609 | **0.566** |
| hellbent@T8 | 18.2% | **16.4%** |

The deck got *smoother* while gaining exits (Wizard Class for Rewind does the work).

**Doctor** (`deck_doctor this-bunny --deep`): PASS 0 errors / 0 warnings. 0/3 GCs. Own 98/100;
buy = Intruder Alarm €2.84 + Approach €2.79 ≈ **€6** *(indicative, Scryfall 2026-07-03)*.
Footprint 16% (low — the exits are value cards, not dead combo slots). Bracket estimate ~4
(infinite present), pod-accepted.

## 5. The verdict against the brief

1. **Always a play** — ✓ improved: 0.566 dead turns (2nd-best on the roster), 16.4% hellbent@T8.
2. **Tight but not one tutored combo** — ✓ by construction *and* measurement: zero tutors; the
   measured close-mixture is 60/32/8 across three mechanically different endings (+ Willbreaker
   theft, goldfish-invisible, in real pods).
3. **Not an archenemy** — ✓ unchanged: 0 GCs, no Rhystic/Tithe-class salience, a 1/5 Rabbit
   giving people cards. The exits don't exist on board until the turn they happen.
4. **Non-obvious win** — ✓: a gift-bunny that wins via a white sorcery cast twice, a Stronghold
   enchantment loop, or a Cat lord's X/X pump. Nothing on the battlefield telegraphs which.

## 6. Caveats (inherited + new)

- Goldfish ceiling caveat carries over: the velocity model dumps interaction proactively.
  Note the Approach/Alarm exits are precisely the lines that *don't* need the dump — they
  monetise mana + 1–2 held cards, which is how the real control deck plays anyway.
- The Alarm loop model requires the bouncer **in hand** and ≥1 loop dork deployed; Alarm's
  symmetric untap static is ignored in the mana floor (flagged OPTIMISTIC in the lab header).
- Close-mixture percentages are goldfish shares, not pod-adjusted: counter-dense tables tax
  Approach cast #2 (sorcery, your turn — Abolisher-style locks *don't* tax it, notably), and
  graveyard hate touches none of the exits.
- CC re-score 15→16 (KR 3→4) is a judgment, as all CC scores are; the lab evidence is above.
- Layer C still open: no logged real games yet. `game_log.py quick` the first pod outings —
  the close-mixture is the most fun thing to grade against reality.
