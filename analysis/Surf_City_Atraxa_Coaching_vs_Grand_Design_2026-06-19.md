# Surf City TCG — Atraxa Grand Unifier coaching (#12) vs. our Grand Design (2026-06-19)

Cross-archetype study: the **second Atraxa, Grand Unifier deck** that Surf City TCG (Matt) coaches in
[youtu.be/-JUtk8yKzSc](https://youtu.be/-JUtk8yKzSc) ("Atraxa, Grand Unifier EDH Coaching #12"),
read against **our** Atraxa deck *The Grand Design* (`decks/The_Grand_Design_Summary.md`) and the
general advice we've banked from Draftsim, Maldhound and BDD.

> **Sourcing:** the **full transcript is now in hand** (user-pasted) — so this doc reflects what the
> coach actually says, not inference. All video-deck card text was verified via `card_lookup.py`
> against the local Scryfall snapshot. (Earlier drafts of this doc could not access the audio and
> guessed at the bracket framing; that guess is **corrected** below.)

---

## 1. What the coached deck is (confirmed by the coach)

**Intentional Bracket "3.9"** — the owner *downgraded it from Bracket 4 to Bracket 3* for his
playgroup, and the channel specializes in **no-infinite-combo, top-of-Bracket-3** decks. Archetype:
**4-colour (WUBG) lands-ramp value-CONTROL built on inevitability.** Atraxa is a card-advantage
payoff + finisher you ramp into — **not** the engine; the deck is commander-independent.

The coach's thesis, near-verbatim:

- **"The plan of this deck is ramp a ton and not die, and then you're going to probably win."**
- **Ramp is the best Bracket-3 win plan** specifically because B3 *bans mass land denial* (so ramp
  can't be punished) and *nothing combos before ~T7* — so the ramping player just out-resources the
  table. "The player who spends the most mana over the course of a game is by far the most likely to
  win."
- **Engine = Cabal Coffers + Urborg** ("get Coffers out ASAP" — he calls it broken and is baffled
  it's not a Game Changer), plus **Field of the Dead**, **~40 lands**, heavy land-ramp, and landfall
  card-advantage (**Lotus Cobra** — "one of the scariest cards in the format, kill on sight";
  **Nissa, Resurgent Animist** — "probably the best opening play in the deck"; Aesi, Tatyova, Oracle
  of Mul Daya, Icetill Explorer, Blossoming Tortoise, Exploration).
- **Win-cons are deliberately MINIMAL** — *"with a control deck the win-con is the least important
  part of the deck."* He **cut** the previous list's Tooth and Nail / Craterhoof / Avenger / Scute
  Swarm. You win via **Field of the Dead** zombies (+ **Meathook Massacre** to burn the table off the
  zombies), **Exsanguinate** (X-drain off Coffers/Nyxbloom — the deck's named kill), **Hullbreaker
  Horror** soft-lock, or just Atraxa beats / "whatever's lying around once you can't lose."
- **Lands are the win axis** because in B3 they're nearly un-interactable ("there's no legal way to
  deal with them" without MLD). He cites his own deck (below) as proof.
- **Control shell:** ~5 board wipes (W/B sweepers + Toxic Deluge, Meathook, Vanquish the Horde,
  Culling Ritual — which doubles as ramp), counters (**Mana Drain, Pact of Negation, An Offer You
  Can't Refuse, Permission Denied**), soft locks (**Tidal Barracuda**, **Collective Restraint** =
  "double propaganda"), plus Oko and Jace.

---

## 2. Bracket — the corrected finding

Final **3 Game Changers = Crop Rotation, Field of the Dead, The One Ring** (coach-recommended; the
player agreed, *dropping Smothering Tithe, Rhystic Study, and Cyclonic Rift* from his old B4 list).
The pasted decklist already reflects these cuts — it **is** the post-coaching version (Jace kept as
an acknowledged "pet card / not optimal").

**The real insight (correctly framed this time):** this is a **maxed-out, fully-legal Bracket 3.** Its
power is loaded through **non-GC** cards — fast mana (Dark Ritual, Lotus Petal, Elvish Spirit Guide,
Gemstone Caverns), free counters (Mana Drain, Pact of Negation), premium walkers (Oko, Jace) — none
of which are on the Game Changers list. So a 3-GC deck can be a "3.9" monster *without breaking the
cap*. **This is precisely the user's own stated preference** — "Bracket 4 in spirit, Bracket 3 by GC
count" ([[feedback-bracket-4-in-spirit]]) — executed by a coach who claims a 90%+ win rate with the
template. The video is a worked example of how to spend the bracket's headroom.

The coach's GC reasoning is itself a lesson:
- **Cut Smothering Tithe & Rhystic Study** — not because they're weak, but because they make you the
  early **arch-enemy** and break the "fly under the radar, win on inevitability" plan ("even after
  they answer it, there's *pissed-off retention* — they still have an axe to grind").
- **Cut Cyclonic Rift** — its **7 mana competes with casting Atraxa**, and W/B sweepers + Hullbreaker
  cover the reset; also "telling the table you don't run Rift makes them lower their guard."
- **Preferred** Crop Rotation (a 1-mana **instant** that puts Cabal Coffers straight into play — "I
  was shocked they made it a GC, it absolutely deserves it"), Field of the Dead, The One Ring (extra
  value as the deck's *artifact* type for Atraxa's pile — see piloting note 4).

---

## 3. The "Garb" deck is the external "strong glarb" we already have on file

**Correction (per the user):** the coach's own **Glarb deck ("Garb")** that he holds up as the
template *is* the **"strong glarb" external list already in our repo** —
`decks/considering/glarb-strong-ext-20260613.txt`, one of the five external Glarb lists evaluated in
`proposals/Calamity_Tax_Direction_Glarb_Lists_2026-06-13.md`. The two are unmistakably the same
author/template: Cabal Coffers + Urborg + Field of the Dead + Crop Rotation + the same landfall draw
(Lotus Cobra / Icetill Explorer / Blossoming Tortoise) + Tidal Barracuda + Talon Gates + "We Want…
A SHRUBBERY!". The Atraxa video deck is literally **"strong glarb + white + Atraxa."**

So this is **not a new discovery** — it's *attribution and empirical backing*. The coach's claimed
**">90% win rate over ~50 games"** is the win-rate evidence behind that specific external list, and
the video is ~110 minutes of its author explaining how the archetype wins (ramp → Coffers → Field →
inevitability, win-cons minimal). It sharpens — but does not overturn — our existing Calamity-
direction work ([[project_calamity_tax_rebuild_direction]]). **NB:** this is a *different* list from
the budget "Yd Freehold" Glarb in `analysis/External_Glarb_vs_Calamity_Tax_2026-06-16.md` — don't
conflate the two.

---

## 4. How it stacks vs. our Grand Design (both Atraxa, both Bracket 3)

| Axis | **Surf City (coached)** | **Our Grand Design** |
|---|---|---|
| Archetype | Lands-ramp value-**control**, inevitability | **Reanimator / flicker / Birthing-Pod** creature toolbox |
| Atraxa's role | A great card *in* the deck (payoff + finisher) | The **engine hub** — abuse her ETB via flicker/reanimate |
| Commander-dependence | Low — wins without her | **High by design** |
| Core resource | **Lands** (Coffers/Urborg/Field + landfall draw) | **Creatures** (tutor/reanimate/flicker chain) |
| Win-cons | **Deliberately few** ("least important part of control") | **Maximised** — 8 kill lines, Kill Reliability 5/5 |
| Interaction | Premium free counters + Oko/Jace + 5 wipes | 20 pieces, but can't *tutor* noncreature interaction |
| Bracket | **Intentional B3 "3.9"**, no infinites | **B3, strict** (Conversion Check 19/20) |

**Same commander, same bracket, opposite philosophies — and one is a direct challenge to our build:**
the coach insists **win-cons are the least important part of a control deck**; our Grand Design is
engineered the *opposite* way (eight kill lines, a 5/5 Kill-Reliability score, a commander-centric
engine). Neither is "wrong" — his is pure ramp-control inevitability, ours is a midrange engine/combo
toolbox — but it's a sharp prompt: **is GD over-invested in redundant kill lines at the expense of
ramp + inevitability?** Our own labs already point the same way (Finale fires ~9%/T11; 96% of decaps
are incremental combat; the deck *out-grinds* but was slow to close), which is why the pending upgrade
adds ramp. The video says the quiet part out loud: for a B3 Atraxa, **ramp + not-dying is the win;
the kill is an afterthought.**

In a head-to-head grind, theirs is favoured (more interaction, faster mana, deeper card advantage,
the Coffers engine). Ours has the higher *ceiling* (Defense-of-the-Heart auto-win, Razaketh chains,
flicker-doubled Atraxa) and is tuned for our specific pod (Elesh Norn ETB-lock vs Acererak). Both are
legal at our table; this is an **idea donor**, not a build to copy.

---

## 5. What we can learn — DECKBUILDING (now validated by the transcript)

1. **Land ramp + Coffers/Urborg/Field of the Dead as the B3 win axis.** Validated empirically (his
   90% Glarb). For **Grand Design** the ramp half is already in flight
   (`archive/proposals/Grand_Design_Upgrade_2026-06-13.md`, decap T10→T9); the *full* Coffers/Field package
   is a better fit for **Calamity Tax** (§3) than for GD's creature-engine identity — don't bolt a
   lands sub-theme onto a flicker deck (BDD's "don't run a 4th half-plan").
2. **Tidal Barracuda — now strongly validated.** The coach calls it *"the card that will win you more
   games than maybe any other,"* via an **end-step Chord/Court of Calling for it** → opponents can't
   cast on your turn → you win. It's a **Grand-Abolisher effect on a creature**, **not a GC**, and is
   tutorable/flickerable — a real port candidate for GD's Grand-Abolisher slot (the upgrade was
   already cutting it) and a natural Calamity include. Directly answers our pod's Abolisher problem
   ([[feedback-grand-abolisher-blocks-counters]], [[project_pod_combo_opponent]]).
3. **Cheap "super-surveil" cantrips (Ponder/Preordain).** He loves them for *sculpting* hands ("every
   hand is that much more perfect"). Validates the smoothing idea for GD; cantrips aren't GCs.
4. **Spread card *types* for Atraxa.** The One Ring earns points partly for being an *artifact* — so
   Atraxa's "one of each type from the top 10" pile more often hands you what you need (don't
   over-concentrate in instants). A GD-specific deckbuilding nuance.
5. **Win-con minimalism in control** — a lens to re-examine GD's eight kill lines (§4).

## 6. What we can learn — PILOTING (the layer only the video carries)

It's a *"how to play"* coaching episode, so the richest content is piloting — and it generalises to
**all** our decks, not just Atraxa:

1. **Read opponents' commanders *before* looking at your hand** — decide your role ("Who's the
   Beatdown?"). Creature-heavy pod → lean on wipes; control pod → don't slam Atraxa with no backup.
2. **Ask the table for threat assessment.** You can't know every card; most opponents will help.
3. **Mulligan aggressively.** *"You should have a play on turn two."* A hand whose first action is
   turn 4 + reactive cards (e.g. lone Oko) is a mulligan **even on the first seven** — "I'd rather go
   to six." The deck runs **40 lands**, so flooding the smoother is fine.
4. **Tempo over value — "use your potions."** The player's biggest leak was hoarding (saving Finale
   for a big X, fetching surveil-lands to "dig" instead of ramping). Coach: **ramp a 2-drop into a
   4-drop** — play Finale / Green Sun for **X=0 → Dryad Arbor** or **X=2 → Lotus Cobra** for tempo.
   *But* know when to hold for value: keep a fetch (Marsh Flats) to combo with **Nissa's double
   landfall**, or grab a **surveil land to sculpt** when you have no other T1 play.
5. **Slow down; break your default line.** Complex decks have many lines and your brain shortcuts to
   one — **goldfish at home** to build the pattern recognition, then shortcut under pressure.
6. **Types & Tags categorisation (Moxfield)** — the coach's single biggest "get better" tip: tag
   every card by function; it sharpens both deckbuilding and mulligan decisions.
7. **Politics / optics.** Don't telegraph power: a T1 Green Sun-for-0 screams "kill me," a T3
   Smothering Tithe makes you arch-enemy. A control deck wants to stay under the radar.
8. **Rules reps worth internalising:** errataed OG dual lands (Bayou) *do* carry basic land types, so
   fetchlands grab them; **every fetchland can get all five colours** (treat any fetch as any colour);
   **Gemstone Caverns** only taps for any colour if it entered via its **pregame** action (i.e. when
   you're *not* on the play).

---

## 7. Lab results — the two levers, measured (`gd_clock_lab.py --mode video`, 40k, seed 12345)

Extended the GD clock lab with a new `video` mode for the two GC-free ideas above. Both tested on the
deployed list; numbers are the goldfish's, so trust the shape/delta, not the decimal.

**(A) Cantrip smootheners (−Dovin's Veto −Swan Song +Ponder +Preordain, with a top-3 dig):**

| build | T8 | T9 | T10 | T12 | median | never-12 |
|---|:--:|:--:|:--:|:--:|:--:|:--:|
| baseline GD | 22 | 46 | 68 | 90 | **T10** | **10%** |
| + Ponder + Preordain | 23 | 48 | 71 | 92 | **T10** | **8%** |

**Read: cantrips don't move the clock, they trim the variance.** Median stays T10 — confirming again
that GD is **mana-gated, not finding-gated** ([[feedback-selection-vs-mana-gated]]) — but never-in-12
drops **10%→8%** and the late cumulative lifts ~2–3pp. Smootheners buy **consistency, not speed.**
Caveat the goldfish can't see: the test cut two counters to make room, so this is the *pure* dig
upside; in a real game you also lose two pieces of interaction.

**(B) Tidal Barracuda — your-turn-lock availability by the decap turn:**

| lock suite | by decap | by T12 | median avail |
|---|:--:|:--:|:--:|
| current (Grand Abolisher + Teferi) = 2 locks | 52% | 65% | T8 |
| **SWAP** GA → Barracuda (+ Teferi) = 2 locks | 53% | 65% | T8 |
| **ADD** + Barracuda (GA + Teferi + Barra) = 3 locks | **62%** | **73%** | T7 |

**Read: the swap is availability-neutral; the lever vs the Abolisher pod is lock COUNT, not which
lock.** At 2 locks **GD has a your-turn lock in hand only ~half the time (52%) by its kill turn** —
exactly why the pod's Grand Abolisher hurts. GA→Barracuda is a *quality* change (Barracuda also stops
creature spells / flash-ins and enables the end-step-Chord line, but costs 4 vs GA's 2 on a tight turn
— none of which the goldfish scores). **Adding** Barracuda as a 3rd lock is what lifts availability
(**+10pp by decap**). The qualitative edge belongs in `delay_lab` / an interaction model, not the
kill goldfish.

## 8. Follow-ups (none applied)

- **GD upgrade already covers ramp + a tutorable finisher** — this corroborates it; no change forced.
- **The two levers are now measured (§7):** cantrips = a small consistency gain (not speed);
  Barracuda-as-swap = neutral on availability (a quality play); raising lock *count* to 3 is the real
  protection lever vs the Abolisher pod — route the quality/cost question to `delay_lab`.
- **Calamity Tax (§3):** revisit the lands-matter / Coffers-Field direction against our current list
  and `analysis/External_Glarb_vs_Calamity_Tax_2026-06-16.md` — the coach's 90%-WR Glarb is a strong
  external data point for that archetype.
- **Reskin alias:** "We Want… A SHRUBBERY!" (Monty Python Secret Lair) = a reskin of **Three Visits**
  ({1}{G}, Forest to battlefield), **not in our Scryfall snapshot** — add to `REF_Reskin_Aliases.md`
  so it can't trip a future "unowned" misfire. (Flagged, not yet added.)
- **General piloting (§6)** applies across the roster — candidate content for a `WF_` how-to-pilot doc
  if we want it reusable.

---

## Sources

- [Surf City TCG — "Atraxa, Grand Unifier EDH Coaching #12"](https://youtu.be/-JUtk8yKzSc) (full transcript, user-supplied)
- [Draftsim — Atraxa, Grand Unifier Commander Deck Guide](https://draftsim.com/atraxa-grand-unifier-edh-deck/)
- Our corpus: `decks/The_Grand_Design_Summary.md`, `analysis/Grand_Design_Speed_Curve_Analysis.md`,
  `archive/proposals/Grand_Design_Upgrade_2026-06-13.md`, `analysis/External_Glarb_vs_Calamity_Tax_2026-06-16.md`;
  memory `reference-maldhound-azula-review`, `reference-bdd-azula-b4-combo`, `feedback-bracket-4-in-spirit`.
- All video-deck card text verified via `scripts/card_lookup.py`.
