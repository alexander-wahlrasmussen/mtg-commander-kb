# Proposal: "Planned Obsolescence" — Urza, Lord High Artificer (Mono-Blue Artifact Stax-Combo)

Status: **proposal — not built.** Drafted 2026-06-11 as the THIRD clean-sheet candidate
(vs `PROP_Yuriko_Insider_Trading.md` and `PROP_Godo_Hostile_Takeover.md` — user picks one).
Same brief: beats the pod combo deck, bracket-4 in spirit, 3-GC cap; protected donors
Lightning War / Calamity Tax / Grand Design / Genome Project / Zero Sum Game.

Texts verified via `card_lookup.py` 2026-06-11: Urza, Winter Orb (incl. the asymmetry
ruling), Static Orb, Trinisphere, Basalt Monolith, Rings of Brighthearth, Isochron
Scepter, Dramatic Reversal, Brain Freeze. GC statuses vs `REF_Game_Changers_List.md`.

---

## The third axis

Insider Trading races on two clocks; Hostile Takeover races on one. **Planned Obsolescence
doesn't race — it moves the finish line.** Static tax/untap locks push the pod's T6–7
combo window to T9+ while Urza's engine ignores the locks entirely, then a 2-card
infinite kills at leisure. This is the only candidate that attacks *their* clock instead
of just optimizing ours — and per the opponent-profile memory, statics are exactly the
axis Grand Abolisher cannot protect (they're not spells or activations aimed at the
combo player; they just sit there).

## Commander

**Urza, Lord High Artificer** — `{2}{U}{U}`, 1/4. *(verified)*

> When Urza enters, create a 0/0 Construct token with "This token gets +1/+1 for each
> artifact you control."
> Tap an untapped artifact you control: Add {U}.
> {5}: Shuffle your library, then exile the top card. Until end of turn, you may play
> that card without paying its mana cost.

**Delisted from the GC list 2025-10-21** (same purge as Yuriko/Winota/Kinnan) — a card
WotC rated GC-grade, now 0 of 3 slots. **Owned ×1 — deployed in Crystal Sickness.** The
pull is THE donor decision of this proposal (see Roster fit).

## How the lock is one-sided (rules-verified)

- **Winter Orb** ruling, verbatim: *"If Winter Orb is tapped as your untap step begins,
  your lands will all untap."* Urza taps the Orb for {U} on the last opponent's end
  step → we untap everything, all three opponents untap one land. Same trick suspends
  **Static Orb**, **Tangle Wire**, and friends on our turn only.
- **Trinisphere / Sphere of Resistance** tax every cheap spell — the pod's tutor-ritual-
  combo chains pay triple; our mana comes from rocks that tap for {U} under Urza and got
  deployed before the locks landed.
- Every stax piece is itself a mana source under Urza. There are no dead lock cards.

## Kill lines (all on our own turn — Abolisher-irrelevant)

1. **Isochron Scepter + Dramatic Reversal** *(2-card, both buys ~€5 total)*: imprint
   Reversal; with Urza out every artifact taps for {U}, so each loop nets mana →
   infinite blue. Outlet: **Brain Freeze (owned, free)** — also imprintable (MV-2
   instant) — mills all three opponents out at instant speed; or Urza's {5} plays the
   whole deck.
2. **Basalt Monolith (×2 owned, free) + Rings of Brighthearth** *(buy ~€5)*: tap for
   {C}{C}{C}, pay {3} to untap, {2} to Rings-copy the untap → +1 per cycle, infinite
   colorless → Urza converts to blue / activates {5} through the library.
3. **Backup beats:** Urza's Construct + token friends grow with the artifact count
   (10–15 artifacts by mid-game = lethal Constructs); Karn, Scion of Urza optional.

## Game Changer plan (3/3 — all owned, free, idle; zero GC buys)

**Mana Vault + Grim Monolith + Chrome Mox.** This is the deck where the fast-mana suite
is *systemically* right, not just fast: the spheres tax us too, and pre-deployed rocks
break that parity — then Urza turns every one of them into a blue dork. (The DR/ZSG
"tutors > fast mana" verdict applied to combo-assembly decks; here the rocks are the
engine itself.) Lab A/B: swap Chrome Mox → Mystical Tutor (owned free, contested with
the Yuriko proposal — only one deck gets built).

## Shell from the collection

Rocks/substrate owned in surplus: Thought Vessel ×6, Mind Stone ×6, Everflowing Chalice,
Foundry Inspector ×2, Basalt ×2, Sol Ring/Signets, Buried Ruin ×2, Tribute Mage (free —
tutors Scepter/Winter Orb/Rings at MV exactly... Scepter+Orb are MV2 ✓), Brain Freeze,
Counterspell/Mana Drain ×2/Swan Song/Force of Negation spares, Pongify, 139 Islands,
Needleverge— (skip, colorless-irrelevant), Mystic Sanctuary, ~30 lands mostly Islands +
artifact lands (cheap buys).

**Buy list (prices unverified):** stax suite — Winter Orb ~€8, Static Orb ~€6,
Trinisphere ~€10, Tangle Wire ~€4, Sphere of Resistance ~€8, Torpor Orb ~€3 (pod ETB
tech); combo — Scepter ~€4, Reversal ~€1, Rings ~€5; tutors — Whir of Invention ~€4,
Reshape ~€1, Fabricate ~€2, Trophy Mage ~€1; misc artifacts/lands ~€10.
**Total ~€55–75.**

## Roster fit — the honest asterisk

- **Crystal Sickness collision.** Urza himself must be pulled from Crystal's 99 (its
  commander is Golbez; Crystal stays Elite but loses a good engine card). Crystal also
  holds the natural substrate (Mox Opal, Sai, Etherium Sculptor, Mystic Forge, Academy
  Ruins proxy, artifact lands). Recommendation: pull **only Urza**, buy/proxy the cheap
  substrate dupes — don't gut a 17/20 deck. Mechanical distinctiveness: stax-combo vs
  Crystal's artifact *reanimator* — different play pattern, defensible, but this is the
  closest-neighbour candidate of the three. User call.
- **Politics, two layers:** the 2-card infinite needs pod approval (either line), AND
  stax has table-feel costs the other candidates don't — Winter Orb hits the two
  non-combo players too. Mitigation: the lock suite is modular; the lab + first games
  can tune how mean it gets.

## Clock — *(unverified — lab gates the build)*

Two metrics, both for `urz_clock_lab.py`: (a) our goldfish kill, target **median T6–8**
(combo is 4–7 mana total across two cards with tutor support — between Godo and Yuriko);
(b) **pod delay under taxes** — model their T6–7 curve paying +1–3 per spell; even crude,
this quantifies the candidate's actual thesis. If the combined spread (our kill vs their
delayed kill) isn't decisively favourable, the premise is falsified.

## Open questions

1. Pod approval (2-card infinite) + stax table-feel conversation.
2. Urza pull from Crystal Sickness — the one mandatory donor hit.
3. `urz_clock_lab.py` with the tax-delay model.
4. 3rd-GC A/B (Chrome Mox vs Mystical Tutor).
5. Lock-suite depth (Orb count vs combo density) — lab sweep.
