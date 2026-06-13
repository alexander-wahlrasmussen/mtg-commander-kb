# Proposal: "Hostile Takeover" — Godo, Bandit Warlord (Mono-Red Equipment Turbo)

Status: **proposal — not built.** Drafted 2026-06-11 as the second clean-sheet candidate for
the reliable-T6–7 brief (alongside `PROP_Yuriko_Insider_Trading.md` — user picks one).
Same constraints: beats the pod combo deck, bracket-4 in spirit, 3-GC cap, donors free
except Lightning War / Calamity Tax / Grand Design / Genome Project / Zero Sum Game.

All texts below verified via `card_lookup.py` 2026-06-11 (Godo, Helm of the Host, Hammer
of Nazahn, Gamble, Neheb the Eternal, Scourge of the Throne). GC statuses checked against
`REF_Game_Changers_List.md` (Feb 2026).

---

## The package

**Godo, Bandit Warlord** — `{5}{R}`, 3/3. *(buy, ~€5–10 unverified)*

> When Godo enters, you may search your library for an Equipment card, put it onto the
> battlefield, then shuffle.
> Whenever Godo attacks for the first time each turn, untap it and all Samurai you
> control. After this phase, there is an additional combat phase.

**Helm of the Host** — `{4}`, Equip {5}. *(buy, ~€15)*

> At the beginning of combat on your turn, create a token that's a copy of equipped
> creature, except the token isn't legendary. That token gains haste.

**The loop (rules-verified):** Godo equipped with Helm → each combat's beginning-of-combat
step makes a hasty nonlegendary Godo token → that token's own "attacks for the first time
each turn" trigger grants another combat → every combat adds a body and another combat.
The army grows each phase and kills all three opponents **in one turn — decap = table
converge by construction.**

**Hammer of Nazahn** — `{4}`, the keystone support buy *(~€8)*:

> Whenever Hammer of Nazahn or another Equipment you control enters, you may attach that
> Equipment to target creature you control. Equipped creature gets +2/+0 and has
> indestructible.

With Hammer down, Godo's ETB fetches Helm onto the battlefield and Hammer **attaches it
immediately, free** — no equip-5 turn — and Godo is **indestructible**, blanking the
wrath/removal answer that is normally this archetype's loss condition. Godo can also just
fetch Hammer first if Helm is already in hand.

---

## Why it answers the brief

1. **It's a one-card combo from the command zone.** Godo tutors the kill piece himself.
   No assembly variance: the question is only "what turn does Godo land, and does he get
   one swing." Compare ZSG (2-card + igniter, median T9) and Yuriko's Clock B (2-card).
2. **The 3 GC slots are all owned, free, and idle:** **Mana Vault** (2 free), **Grim
   Monolith** (free), **Gamble** (1 free — red's Demonic Tutor, finds Helm/Hammer/haste).
   Zero GC buys; this is the only candidate that uses the dormant fast-mana GCs, and in a
   deck whose kill is genuinely mana-gated (6-mana commander) — the configuration the DR/
   ZSG labs say fast mana is actually FOR (their verdict "tutors > fast mana" applied to
   cheap-combo assembly decks; here the gate is one big cast).
3. **Grand Abolisher is irrelevant on every axis.** ETB tutor (trigger), free attach
   (trigger), extra combats (triggers), all on our turn. Nothing is cast or activated
   into the lock.
4. **Goldfish profile (UNVERIFIED — lab gates the build):** lands + Sol Ring + Vault +
   Monolith + rituals (Seething Song, Pyretic Ritual ×2 owned) put Godo down T3–4 in
   good hands, T4–5 normal; with Hammer pre-placed or a haste source the table dies the
   same turn, else the next. Structural target: **median table kill T5–6, the fastest
   profile of the three candidates.** `godo_clock_lab.py` on the harness BEFORE building;
   the lab must also sweep haste density and Hammer's delta.

## The honest weaknesses

- **Glassiest candidate.** Mono-red: zero counterspells. Godo is a counterable creature
  spell, and exile/bounce removal (not destroy — Hammer covers that) between landing and
  swinging costs a full cycle plus commander tax. The pod's decks per the opponent
  profile are combo-not-counters, which is exactly the matchup this deck wants — but a
  counter-heavy table beats it.
- **Telegraphed.** Everyone scoops to Godo once; after that he eats every answer. The
  build leans on redundancy: **Scourge of the Throne ×2 (owned free)**, **Neheb, the
  Eternal (1 free — post-combat {R} burst pays equip mid-turn)**, Port Razer / Combat
  Celebrant (cheap buys), Moraug (proxy in Earthbend, donor call), Aggravated Assault
  (proxy in Replication Crisis, donor call) as secondary extra-combat engines that win
  without Godo.
- **Pod approval still required** — infinite combats. Precedent is favourable: the pod
  approved Kiki combat-infinites twice (Exile's Return, Replication Crisis pending), and
  combat is the most interactable win type (blockers, fogs, removal all answer it).

---

## Shell from the collection (owned-free unless noted)

- **Fast mana / ramp:** Mana Vault, Grim Monolith, Chrome Mox (bench/4th-GC-NO — stays
  out), Sol Ring, Arcane Signet, Ruby Medallion, Seething Song, Pyretic Ritual ×2,
  Treasonous Ogre, Generator Servant (buy ~€0.5 — haste rider!)
- **Tutors/draw:** Gamble (GC), Inventors' Fair (1 free — tutors Helm/Hammer), Faithless
  Looting (8 owned), Imperial Recruiter (in Exile's Return — donor call; finds Celebrant/
  Inciter), Light Up the Stage (1 — ER swap pending makes it free), wheels skipped (€€)
- **Haste:** Swiftfoot Boots ×3 spares (hexproof still allows our own equips — never
  Lightning Greaves on Godo: shroud blocks attaching Helm), Anger (in Lorehold Spirits,
  donor call — discard to Looting), Fervor / Ogre Battledriver / Bloodlust Inciter /
  Hall of the Bandit Lord (cheap buys, lab decides count)
- **Protection/utility:** Defense Grid (buy ~€3 — taxes counter-walls without affecting
  us), Mountains from 109 owned, Forgotten Cave, ~30–31 lands total

**Buy list (prices unverified):** Godo ~€8, Helm ~€15, Hammer ~€8, Port Razer ~€3, Combat
Celebrant ~€1, haste package ~€5, Defense Grid ~€3, misc ~€5 → **~€45–60 total. Cheapest
of the candidates** (Yuriko ~€140–170; ZSG was ~55–70 before the full-buy call).

---

## Roster fit

- **Distinctiveness:** first mono-colored deck and first equipment deck in the roster;
  no overlap with any active archetype. Clean pass.
- **Donor impact:** near zero from binder spares; optional pulls (Imperial Recruiter from
  ER, Anger from Lorehold, Moraug/AA proxies) are all flagged user calls, none load-bearing.
- **Politics:** infinite-combat approval request; Kiki precedent ×2.

## Open questions

1. Pod approval (infinite combats).
2. `godo_clock_lab.py` — kill-turn distribution, Hammer delta, haste-count sweep,
   GC A/B (does Gamble beat Chrome Mox as the 3rd slot?).
3. Wheel package (Wheel of Fortune €€) — likely skip; Looting/Stage suffice for a deck
   that wins off 8 cards.
4. Imperial Recruiter / Anger donor calls.
