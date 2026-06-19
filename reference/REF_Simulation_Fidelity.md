# REF_Simulation_Fidelity — the fidelity ladder & the rules-engine decision

What the simulation stack in `scripts/` **is** and **is not**, ranked by trust — and the standing
decision (evaluated 2026-06-17) **not** to bridge it to a real Magic rules engine.

**Status:** reference + decision record. The engine question was scoped, Forge was checked, and the
idea was **declined.** §3 is the durable reason; reopen only against §4. The fidelity ladder (§2)
stands on its own regardless of that decision.

> **TL;DR.** Every tool in `scripts/` is a *model*, not a game of Magic. We evaluated bridging to a
> real engine (Forge) to get a **pilot-decoupled** read on decks — the one thing real game logs can't
> give a learning builder. **Verdict: don't.** Forge's card coverage turned out fine (Commander 99.8%,
> Universes Beyond included), but its AI is heuristic and **only pilots fair/board decks competently —
> not the combo/control decks that are this roster's core and that you most need help judging.** The
> instrument is competent exactly where you *don't* need it; for the decks you do, our hand-scripted
> goldfish labs already beat it. Reality (`game_log.py` → `calibrate.py`) plus the existing labs remain
> the tools. An engine doesn't import the judgment the goldfish lacks — it imports a *weaker* one.

---

## 1. Why this doc exists

The disclaimer *"This is NOT a rules engine. It does not play games of Magic"* recurs across the script
headers (`deck_sim.py`, the `*_clock_lab.py` suite) and the analysis writeups. The Framework Bake-Off
(`analysis/Framework_Bakeoff_2026-06-16.md`) diagnosed the deepest leak — every oracle is a **solitaire
goldfish**, so Interaction and Durability (half the Conversion Check) score zero — and named the fix it
would *not* build: *"a real multiplayer interaction model … the rules engine the project deliberately
never built."* Backlog #6 built the tractable substitute (`interaction_meta_lab.py`, an overlay).

This doc (a) collects that scattered boundary into one place — point the disclaimers here — and (b)
records that the engine itself was evaluated and declined, so it isn't re-litigated from scratch.

## 2. The fidelity ladder

Layers ordered by trust *for "what happened in a game."* When two disagree on that, the lower row wins
(this extends `CLAUDE.md`'s ground-truth hierarchy from *files* to *models*).

| # | Layer | Tools | Models | Cannot model | Trust |
|---|---|---|---|---|---|
| **L0** | Composition stats | `deck_sim.py` | Keepable hands, lands/mana by turn, colour sources, combo-piece *availability* | Anything text-dependent; mana cost of the kill; the stack | Floor — "is the deck physically capable" |
| **L1a** | Hand-coded goldfish | `*_clock_lab.py`, `speed_lab_core.py` | Per-deck **kill checks** → decap & table clock curves (text interpreted, by hand) | Opponents, blocking, interaction — **solitaire**; optimism-prone | Per-deck clock claims (w/ citation) |
| **L1b** | Parametric pod overlays | `pod_gauntlet.py`, `self_meta_lab.py`, `interaction_meta_lab.py`, `delay_lab.py`, `lock_lab.py` | P(beat the pod), table races, interaction as a **swept `TAX`** | Real priority/targeting/sequencing — interaction *assumed*, not *played* | Cross-deck ranking, matchup shape |
| **LX** | *(evaluated, declined — §3)* synthetic rules engine | — none — | The full game *played* by an AI pilot — **but only as well as that AI plays** | Real human play; bounded by AI competence (which is the dealbreaker, §3) | Would sit above L1, below L2 — *if the AI could pilot the deck* |
| **L2** | Real game logs | `game_log.py` → `game_results.jsonl` → *`calibrate.py` (named, unbuilt)* | Actual pod outcomes: win/decap turn, win type, disruption that mattered | The pilot-skill confound — can't separate deck quality from your skill | Ceiling for "what happened" — overrides all above |

The one thing missing from this ladder is a **pilot-decoupled** read on a deck (strength / play-difficulty
independent of who's driving). L2 can't give it (results blend deck + pilot); a fixed-AI engine could — in
principle. §3 is why "in principle" didn't survive contact with a real engine.

## 3. The decision: evaluated, verified, declined (2026-06-17)

We took the reframe seriously: a learning builder's real games confound *"is the deck good?"* with *"am I
playing it well yet?"*, so an engine that holds the pilot fixed could decouple them — and answer *how
strong*, *how hard to pilot*, and *which cards help*. We checked **Forge** (the realistic substrate: `sim`
runs headless multiplayer AI-vs-AI, `-f Commander -p 4`). It doesn't pay off **here**:

- **Coverage is *not* the blocker we feared.** Forge implements Standard/Modern/Historic 100% and
  Commander **99.8%** (only 46 *Unfinity* stickers missing); **Universes Beyond is in** (Final Fantasy
  Jun 2025, LOTR, etc.) and new sets land within weeks. The card pool would mostly just work.
- **The AI is the wall, and it's archetype-shaped.** Forge's AI is heuristic and *untrained* — competent
  at aggro/midrange, **weak at combo *and* control.** That's a *piloting* failure, not a coverage one:
  the cards resolve fine, the AI just plays them badly.
- **So the tool is competent only where you don't need it.** This roster's core is combo (Genome,
  Replication, Diminishing Returns, the Thoracle builds) and grind/control (Grand Design, Lightning War,
  Dark Lord, Calamity) — exactly what the AI *can't* pilot, and exactly what a learning builder can't yet
  eyeball. The fair/board decks Forge *can* measure are the ones you can already judge by hand.
- **For the hard decks, the goldfish already wins.** A hand-scripted `*_clock_lab.py` kill check encodes
  a competent pilot *by hand*; Forge's AI would fail the line. So for combo/control, our crude solitaire
  labs are a **better** deck-quality proxy than the "real" engine.
- **The only salvage was too narrow to justify.** Forge's stock AI is a fair proxy for a *beginner*, so a
  "forgiveness / floor meter" on fair decks ("how I'll do today; does this card make the deck more
  beginner-proof") would have been honest — but it's a small slice (fair decks only, a question largely
  answerable by hand), not worth a Forge integration plus a per-deck audit.

**Net:** an engine doesn't import the judgment the goldfish lacks; it imports a *weaker* judgment. The hard
part was never the rules — it was the piloting — and that's the part you can't buy off the shelf. This is
the same wall the bake-off and the interaction overlay hit: every fidelity upgrade keeps revealing that
modelling *judgment* is the frontier, and a heuristic AI isn't it.

## 4. If this is ever reopened

Don't restart from scratch — start from the verified baseline:

- **Coverage is solved.** Recheck only the last ~1–2 months of sets (which can lag a Forge release).
- **The blocker to beat is AI piloting competence on combo/control — not cards.** A reopening is only
  worth it with a *materially stronger pilot* (a better engine AI, a search/MCTS layer, or hand-scripted
  combo lines fed to the engine). Absent that, the verdict in §3 stands.
- **Discipline still binds.** Any number an engine ever produces must clear the lab-citation bar in
  `reference/REF_The_Conversion_Check.md` before it's cited, and combo/control results stay quarantined
  until the AI demonstrably pilots them.

---

## See also

- `scripts/deck_sim.py` · the L0 disclaimer this doc generalises
- `analysis/Framework_Bakeoff_2026-06-16.md` · the solitaire-goldfish leak that named the frontier
- `analysis/Interaction_Oracle_2026-06-16.md` · Backlog #6 — the overlay built *instead of* an engine
- `scripts/game_log.py` · the L2 capture end; `calibrate.py` is the unbuilt validator
- `reference/REF_The_Conversion_Check.md` · the lab-citation bar any engine number would have to clear
- `CLAUDE.md` · card-text rule + kill-window/lab-citation rule

### Sources — Forge capability check (2026-06-17)

- Forge AI behaviour + `sim` flags — [Card-Forge/forge Wiki: AI](https://github.com/Card-Forge/forge/wiki/AI)
- Card-pool coverage (Commander 99.8%, only 46 Unfinity stickers missing) — [Wiki: Missing Cards in Forge](https://github.com/Card-Forge/forge/wiki/Missing-Cards-in-Forge)
- UB / set cadence incl. Final Fantasy (forge-2.0.04, Jun 2025) — [GitHub Releases](https://github.com/Card-Forge/forge/releases)
