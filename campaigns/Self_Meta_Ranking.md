# Self-Meta Ranking — which deck wins if the roster *is* the field

**The question.** `Pod_Matchup_Matrix.md` answers "which of my decks beats **the
archenemy** (a T6–7 combo behind Grand Abolisher)." This doc answers the inverse:
**if a pod were drawn from my own decks, which deck has the highest win probability?**
"Best deck in my own metagame," not "best answer to one external threat."

**Method & confidence.** Grounded in the lab-measured decap/table clocks
(`Kill_Window_Lab_Sweep_2026-06-13.md`) and the documented interaction/resilience
profiles (the Summaries + `Pod_Matchup_Matrix.md`). **The clocks are lab-verified;
the win-probability ordering is reasoned judgment** — there is no multiplayer
rules-engine sim (politics, interaction, and 4-body combat math are out of reach of
the goldfish labs), and I won't fake one. Tiers are confident; fine order within a
tier is soft.

---

## Why this ranking differs from the anti-pod matrix

The threat model flips, and so do the traits that win:

| | Anti-pod (`Pod_Matchup_Matrix`) | Self-meta (this doc) |
|---|---|---|
| Threat | one **T6–7 combo** behind Abolisher | a **slow, grindy, interactive field** (table clocks T8–T13) |
| Win condition | **race to ~T7 OR disrupt the combo turn** (Abolisher-proof) | **close all three seats, and outlast** |
| Rewards | own-Abolisher fortresses, static stax, burn reach | **converge / hit-all** kills, durability/inevitability, **engines fed by opponent activity** |
| Punishes | counter-reliance (dead under Abolisher), slow clocks | **focus-fire combat** (clearing 3 seats one at a time is slow), glass cannons |

Three mechanical facts drive the difference:

1. **Nobody in the field races.** Only Genome/Radiation/Replication even *decap* by
   T7, and all three still **table** at T8–T10+. So a self-meta pod is a **grind**,
   not a race — inevitability and durability matter more than a fast decap.
2. **Converge beats focus-fire in a pod.** A drain/ping that hits **all** opponents
   (`hit_all`) closes a 3-player table far faster than combat that kills **one** at a
   time (`hit_focus`) — roughly a 3× difference to clear the table. The **table**
   clock, not the decap clock, is the self-meta win metric.
3. **Opponent-fed engines scale up.** A field of spell-dense decks is the *most
   active pod possible*, which supercharges any engine that triggers off opponents'
   spells/draws.

---

## The ranking

**Tier 1 — meta-warpers**

1. **The Dark Lord's Army** (19/20). The standout, and the sharpest inversion: its
   engine is **opponent-driven** — Sauron amasses on opponents' spells; Sheoldred /
   Underworld Dreams / Bowmasters drain on their draws; Wound Reflection doubles their
   loss — and the lab measured it **kills *faster* against active pods** (decap T8 /
   table T11 at high tempo vs T9/T12 typical). A pod of your own decks maximises that
   tempo. Its anti-pod weakness ("too slow to race one combo") *is* its self-meta
   strength, on top of 19/20 durability. **Most likely to win the field.**
2. **Radiation Sickness** (18/20). Rad/toxic + proliferate is a **converge** attrition
   engine that taxes the whole table at once and shrugs off counters (triggers, not
   casts); durable enough to reach its T10 table. The cleanest "grind everyone down"
   plan in the roster.

**Tier 2 — fast table-closers / inevitability**

3. **The Genome Project** (15/20). The **fastest table in the roster (T8)** — its pings
   hit all opponents, so decap = table (converge). Highest raw ceiling. The catch is a
   15/20 glass, combo-reliant body; in a slow field it usually gets the time to
   assemble, but as the visible "pinging everyone" threat it draws the removal and the
   focus. High ceiling, medium floor.
4. **Lightning War** (19/20). Pingers (Firebrand Archer / Thermo-Alchemist) chip every
   seat on each spell + X-spell reach to finish; 19/20 durability lets it out-attrition
   a grind.
5. **Zero-Sum Game** (unaudited). T9 converge lifeloop with a **board-independent**
   ~3-mana kill that resolves on your turn — would be Tier 1 if audited; held here
   only because it's unproven (cards on order).

**Tier 3 — durable but slow / mixed converge**

6. **The Grand Design** (19/20) and 7. **The Calamity Tax** (18/20) — win by
   **inevitability** *if* they survive, but they're slow to actually clear three seats
   (combat 96% / mana-gated X-drain). In a slow field their durability buys the time;
   their problem is closing, not surviving.
8. **Lorehold Spirits** (18/20) — Purphoros ping + the Goblin Bombardment `kill_all`
   combo give it a real table-close at T10, better than a pure combat deck.
9. **Diminishing Returns** (17/20) — aristocrat drain is converge, but slow (table T12+).
10. **Curse of the Scarab** (17/20) — Scarab + Gray Merchant table-drain (T11), behind a
    combat decap.

**Tier 4 — focus-fire in a peer field** (decent decap, but killing three grindy
opponents one at a time is too slow, and counter-reliance loses value mirror-wide):
11. **The Exile's Return** (17/20) · 12. **Earthbend the Meta** (17/20) ·
13. **The Replication Crisis** (17/20) · 14. **Eldrazi Stampede Chaos** (14/20) ·
15. **Ms. Bumbleflower** (15/20) · 16. **Crystal Sickness** (17/20, table T13 — slowest closer).

---

## The headline — the rankings invert at the edges

- **Dark Lord's Army:** anti-pod Tier 2 underdog → **self-meta #1.** The slow,
  opponent-fed grind that can't race a combo is exactly what dominates a slow active field.
- **Grand Design / Exile's Return:** anti-pod **Favoured** → self-meta Tier 3–4. Their
  edge is *disrupting one combo*; against a peer field their focus-fire is slow to close
  three seats.
- **Genome / Radiation:** strong in **both**, because they **converge** — they close
  tables fast regardless of the threat model. These are the roster's most
  threat-model-agnostic decks.

This is the framework's "**score ⊥ clock at the top**" thesis made concrete: the
Conversion-Check fortresses win the **grind** (self-meta), the converge/fast decks win
the **race** (anti-pod), and almost nothing wins both. See the closing note in
`Kill_Window_Lab_Sweep_2026-06-13.md`.

---

## Related

- `../Pod_Matchup_Matrix.md` — the anti-pod (vs archenemy) companion ranking, now
  **lab-`P(win)`-ordered** (`Pod_Gauntlet_2026-06-14.md`). That side is quantified;
  **this self-meta side stays reasoned judgment** (no 4-body sim — see Method above).
- `Pod_Gauntlet_2026-06-14.md` — the anti-pod win-probability model the matrix orders by.
- `Kill_Window_Lab_Sweep_2026-06-13.md` — the lab-measured decap/table clocks this rests on.
- memory `project_pod_combo_opponent` — the archenemy this contrasts against.
