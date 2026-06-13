# Proposal: "Mergers & Acquisitions" — Thrasios + Tymna (WUBG Draw-Go Combo, cEDH Throttled to Bracket 3)

Status: **proposal — not built.** Drafted 2026-06-12 as the SIXTH clean-sheet candidate for the
reliable-T6–7 brief (alongside Yuriko / Godo / Urza / Kinnan / Korvold — user picks one). Same
constraints: beats the pod combo deck, bracket-4 in spirit, **hard 3-GC cap**; protected donors
Lightning War / Calamity Tax / Grand Design / Genome Project / Zero Sum Game.

All texts below verified via `card_lookup.py` 2026-06-12 (Thrasios, Tymna, Isochron Scepter,
Dramatic Reversal, Thassa's Oracle, Demonic Consultation, Drannith Magistrate, Opposition Agent).
GC statuses checked against `REF_Game_Changers_List.md`.

---

## Read this first — what makes this candidate different

The other five candidates are **natively bracket-3 power**: delisted commanders (Yuriko, Urza,
Kinnan) or a non-GC commander (Godo, Korvold) built around a focused combo, where the 3-GC cap
costs them almost nothing because they were never going to run 15 Game Changers.

**Thrasios + Tymna is the opposite — it is a genuine cEDH commander pair deliberately throttled to
a 3-GC cap.** A real Witch-Maw list runs 15–25 Game Changers (Force of Will, Fierce Guardianship,
Rhystic Study, Mystic Remora, Ad Nauseam, Necropotence, the full tutor and fast-mana suites). The
cap deletes the part of the deck that makes Thrasios actually broken: **the free-counter suite that
interacts on opponents' turns**, most fast mana, and the resource engines.

So the honest question this candidate exists to answer is: **does a 3-GC Thrasios still beat the
pod, or does the cap neuter exactly the cEDH advantages?** That is the central tension, and the
`thr_clock_lab.py` run is built to quantify it. This is the highest-ceiling, highest-variance,
most-buy-heavy, and most politically-loaded of the six. Going in with eyes open.

---

## Commanders (both verified)

**Thrasios, Triton Hero** — `{G}{U}`, 1/3 Merfolk Wizard, **Partner. Owned, free.**

> {4}: Scry 1, then reveal the top card of your library. If it's a land card, put it onto the
> battlefield tapped. Otherwise, draw a card.

Ruling: *"No player may take another action while you're resolving the activated ability."* This is
the engine — with infinite mana, Thrasios draws your **entire library uninterrupted**, no card
needed beyond the mana.

**Tymna the Weaver** — `{1}{W}{B}`, 2/2 lifelink, **Partner. Buy (~€20–30 unverified).**

> At the beginning of each of your postcombat main phases, you may pay X life, where X is the number
> of opponents that were dealt combat damage this turn. If you do, draw X cards.

Together = **WUBG** (no red). Tymna's white+black is load-bearing: it's what lets the deck run the
black Consultation finish *and* white protection/hate — a Temur partner (Kraum) cannot. Neither
commander is a Game Changer, so both are **0 GC slots**.

## Win lines (all on our own turn — Abolisher-irrelevant)

1. **Thassa's Oracle + Demonic Consultation** *(both buys)* — 3 total mana, win on resolution.
   Consultation has no targets and "no way to make it affect your opponent"; Thoracle with an empty
   library wins even at zero blue devotion. **This is the same line as Yuriko's Clock B — overlap
   acknowledged; only one of the six is built.**
2. **Isochron Scepter + Dramatic Reversal → infinite mana → Thrasios decks you → Thoracle.**
   Imprint Reversal (`{1}{U}` instant, MV 2 ✓); with ≥`{3}` of nonland mana from rocks, each Scepter
   activation (`{2}`) untaps all rocks for net-positive mana = unbounded. Sink it into Thrasios
   `{4}` repeatedly to draw your whole library (uninterruptible per the ruling), cast Thoracle
   before the final draw → win. **Thrasios is the built-in outlet** — the combo needs no extra
   wincard. Both Scepter and Reversal are buys (~€5 the pair).
3. **Grind plan / standalone:** Tymna draws on combat damage, Thrasios ramps-or-draws every turn —
   a card-advantage backbone that out-resources the pod if the combo is answered.

## Game Changer plan (3/3 — the binding constraint)

Pick the three highest-impact GCs and accept that this is where the deck bleeds power vs. real cEDH:

| Slot | Card | Status |
|---|---|---|
| 1 | **Thassa's Oracle** | GC (Win Conditions). **Buy ~€12.** The wincon — non-negotiable |
| 2 | **Mystical Tutor** | GC (Tutors). **Owned, free.** Instant-speed find for Consult / Reversal / interaction |
| 3 | **Drannith Magistrate** | GC (Stax). **Owned, free.** "Opponents can't cast from anywhere but hand" — hoses the pod's exile/graveyard/command-zone combo casts and shuts off commander recasts; a static on *our* board, so it survives Grand Abolisher |

- **Lab A/B for slot 3:** Drannith vs. **Opposition Agent** (owned but in protected Lightning War →
  buy; flashes in to steal their tutor mid-combo) vs. a second tutor (**Demonic Tutor**, buy). All
  three are pod-targeted; Drannith is the owned-free proactive pick.
- **Deliberately OUT (the throttle):** Force of Will, Fierce Guardianship, Rhystic Study,
  Necropotence, Ad Nauseam, Underworld Breach, fast-mana beyond one slot — all legal Witch-Maw
  staples, all cut by the cap. Several are owned but locked in protected decks (Opp Agent → LW,
  Rhystic → GD, Necro + Breach → Genome), so they'd be buys anyway.

## Shell from the collection (owned-free unless noted)

- **Combo core (buys):** Thassa's Oracle ~€12 · Demonic Consultation ~€8 · Tainted Pact ~€20
  (redundant exiler — demands a near-singleton manabase, same rule as the Yuriko build) · Isochron
  Scepter ~€4 · Dramatic Reversal ~€1
- **Interaction (WUBG's edge under the cap):** Swords to Plowshares, Swan Song, An Offer You Can't
  Refuse, Veil of Summer, Teferi's Protection-class (some owned spares) — note the *cheap* counters
  stay, the *free* ones (FoW/FG) are the cap casualties
- **Hate / proactive (beats the pod):** Drannith Magistrate (GC, free), Opposition Agent (buy 2nd or
  bench), Aven Mindcensor / Cursed Totem-class (cheap buys; see `feedback-grand-abolisher-blocks-counters`)
- **Tutors / dig:** Mystical Tutor (GC, free), Worldly Tutor (free), Survival of the Fittest (free),
  Vampiric/Demonic (buys), Thrasios + Tymna drawing
- **Ramp:** Mana Vault ×3 (free), Sol Ring, Signets, dorks; mana rocks double as Scepter-combo fuel
- **Lands:** ~30 WUBG, fetches/duals/shocks; near-singleton basics for the Tainted Pact line

**Buy list (prices unverified):** Tymna ~€20–30 · Thoracle ~€12 · Consultation ~€8 · Tainted Pact
~€20 · Scepter+Reversal ~€5 · Demonic Tutor ~€25 · interaction + hate ~€20 · WUBG manabase ~€30 →
**~€140–180. The most expensive candidate** — the deck owns almost none of its core (one commander,
Drannith, Mystical Tutor, Mana Vault) and buys the rest, including a second copy of every cEDH
staple already locked in a protected deck.

## Roster fit — the honest asterisks

- **Distinctiveness:** no 4-color partner deck and no dedicated draw-go combo-control pile exists on
  the roster — the *archetype* is clean. But the **colors collide with The Grand Design (Atraxa,
  also WUBG)**, the protected 19/20 elite. Different play pattern (GD = midrange disruption-led
  value per its clock lab; this = cEDH-lite combo), so it passes the mechanical-distinctiveness
  filter — but the two decks compete for the same WUBG staple pool, and GD is a protected donor, so
  this build buys around it.
- **Donor impact:** the contested cEDH pieces (Opp Agent, Rhystic, Necro, Breach) all sit in
  protected decks — zero pulls, all buys. The free contribution is thin: Thrasios, Drannith,
  Mystical Tutor, Mana Vault.
- **Politics — the highest bar of the six.** This is transparently a cEDH commander pair, and the
  3-GC cap is its only fig leaf. Expect a "that's just cEDH, not bracket 4" reaction from the pod
  even at 3 GCs. The Thoracle+Consult request is the same as Yuriko's, but here it sits on a deck
  with no fair face to point at. If the pod is going to decline any candidate, it's this one — so
  this proposal lives or dies on the bracket conversation, not the build.

## Clock — *(unverified — lab gates the build)*

Structural estimate, NOT a citation: the combo itself is cheap (Thoracle+Consult = 3 mana; the
Scepter line is mid), so the *ceiling* is the fastest of the six (cEDH Witch-Maw goldfishes T3–4).
But the **3-GC throttle removes the free interaction and resource engines that hold that speed up
under pressure**, so the *median* should regress meaningfully — estimate **median T5–7**, with the
spread (ceiling vs. throttled median) being the whole point of the lab. `thr_clock_lab.py` on
`speed_lab_core.py` must model BOTH (a) our kill curve at 3 GCs and (b) explicitly, the **delta vs.
an unthrottled 15-GC list** — that delta is the number that tells us whether the cap is a fig leaf
or a real handicap. If the throttled median lands T7+, this candidate is just a worse Yuriko with
spicier politics, and we say so.

## Open questions for the build session

1. **Pod approval — the make-or-break.** Lead with the bracket conversation, not the decklist;
   `pod-combo-opponent` memory says the table tolerates combo, but this is the most cEDH-coded ask.
2. `thr_clock_lab.py` — kill curve at 3 GCs **and** the throttle-delta vs. a real cEDH list.
3. **Partner choice:** Thrasios + **Tymna** (WUBG, white hate + black Consult) vs. **Vial Smasher**
   (GUBR — cheaper ~€3, red rituals/Jeska's Will, keeps the black finish, loses white hate). Tymna
   is the card-engine pick; the lab/budget can argue Vial Smasher.
4. **GC slot 3** — Drannith vs. Opposition Agent vs. a second tutor.
5. **Near-singleton manabase audit** for the Tainted Pact line (same automation as the Yuriko build).
