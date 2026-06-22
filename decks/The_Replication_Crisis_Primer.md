# The Replication Crisis — Pilot Primer

**Commander:** Satya, Aetherflux Genius (Jeskai / URW)
**Archetype:** ETB / token copy engine · infinite-combat closer · **Bracket:** 3
**Full detail:** see `The_Replication_Crisis_Summary.md`. This page is for piloting at the table.

---

## The pitch

When Satya **attacks**, she makes a free tapped-and-attacking copy of one of your nontoken creatures and hands you 2 energy. Stack the deck with strong ETB creatures, copy the best one every combat, and multiply the value with ETB doublers and token doublers. Close with **infinite combats** — your fastest-to-find line is **Satya + Lightning Runner** (commander + 1 card) — or a **Brudiclad alpha strike.**

## How you win

- **Satya + Lightning Runner (infinite, 2 cards = commander + 1) — PRIMARY:** both attack; each makes 2 energy; Satya copies the Runner. Pay 8{E} on the real Runner → untap all + extra combat. Next combat the token Runner is untapped and **attacks for real**, so it makes energy too. Energy per combat = 2 × (Satya + every Runner); at 3 Runners it's self-sustaining → infinite combats. You only need ~6 banked energy to start (4 with Anointed Procession). Copy **Inferno Titan** for infinite pings, or just swing the growing double-strike pile.
- **Sword of F&F + Aggravated Assault (infinite, 3 cards incl. commander) — backup:** equip Sword to Satya; her combat damage untaps all lands → re-cast AA post-combat → repeat. Each loop also nets a token + 2 energy.
- **Brudiclad token conversion:** the combat *after* Satya copies an Inferno Titan (or similar), Brudiclad turns your whole token pile into copies of it — and **converted tokens shed Satya's end-step sacrifice clause**, so they stick.
- **Adeline + Anointed Procession flood:** a real attack with Adeline makes ~3 humans per opponent, doubled by Procession — a 3–4 card alpha with no infinite required.
- **Value grind:** Inferno Titan copies (3 dmg), Cloudblazer copies (draw 2), Skyclave copies (exile a permanent) each combat — most pods can't out-resource it.

## Mulligan — what to keep

Looking for: **lands + ramp + a path to Satya on T4**, plus at least one ETB creature to start copying.

- **Keep:** ramp + Satya + an ETB creature; or ramp + interaction with Satya findable.
- **Toss:** no-land hands; hands with Satya but zero ETB creatures to copy; all-payoff/no-mana.
- You **don't** need the combo in your opener — the deck grinds ETB value and assembles it.

## Turn-by-turn

1. **T1–3:** ramp (Sol Ring, signets, talismans); hold interaction.
2. **T4:** cast Satya (or wait one turn for a protected swing — she must survive combat).
3. **T5+:** attack every turn — copy the best ETB creature, bank energy, snowball. Keep counters up on opponents' turns.
4. **Closing turn:** with Lightning Runner out, just attack with both it and Satya and pay 8{E} once you can — the loop builds its own energy. Otherwise equip Sword of F&F + activate Aggravated Assault, or set up a Brudiclad conversion for a lethal alpha.

## Don't-miss rulings

- **Tokens entering "tapped and attacking" do NOT trigger "whenever ~ attacks" abilities** *the combat they're made* — but they **CAN attack normally in a later combat** (once untapped + declared), and *then* they trigger. Satya copies of Adeline, Phelia, Bident-bearers, etc. don't fire attack triggers on entry, but their **ETB triggers DO**. This is the whole engine of the Lightning Runner combo: the token Runner makes no energy the combat Satya creates it, but it untaps with the others and **does** make energy when it attacks in the next combat. (It's also why the old Combat Celebrant "infinite" was fake — exert is a one-time, can't-untap thing.)
- **The copy must target a *nontoken* creature** — Brudiclad-converted tokens are not legal Satya targets.
- **Energy is gained free; tokens are kept by paying their mana value in {E} at end step.** An Inferno Titan token costs 6{E} to keep — three attacks bank enough for one. Unkept tokens are sacrificed.
- **Brudiclad-converted tokens shed Satya's end-of-turn sacrifice clause** (it's a delayed trigger stuck to the original token) — the cleanest way to keep tokens without paying energy.
- **The Sword + AA loop relies on Satya herself connecting**, not the tokens. Menace + haste + 5 toughness makes it reliable, but **two blockers stop menace.**
- **Panharmonicon / Elesh Norn double the *ETBs* of every Satya copy**; Strionic Resonator copies Satya's attack trigger for a second token. Phelia and Restoration Angel are the flicker engines (Phelia only flickers when *she* attacks).

## Threats & timing

- **Commander-dependent.** Every kill line needs Satya attacking as a 3/5 — instant-speed removal in response to the combat trigger blanks the turn. Repeated Satya removal is the best counterplay against you. Goldfish: decap ~T7, table T10–12 — a reliable closer, **not** a T6–7 racer (`rc_speed_lab.py`).
- **Protect the swing.** Lightning Greaves / Swiftfoot Boots, Slip Out the Back, Clever Concealment, Akroma's Will; Sword grants pro-black/green. Hold a free counter (Fierce Guardianship, Deflecting Swat) for the combo turn.
- **Weak to stax / pillowfort.** Ghostly Prison & Propaganda tax your attacks; Torpor Orb & Hushbringer shut off the ETBs entirely. Enchantment removal is thin (Loran, Generous Gift).
- **Two mass answers: Cyclonic Rift + Winds of Abandon** (overload = one-sided creature exile — doesn't touch your board). Plus Sublime Epiphany as a flexible modal counter/bounce/copy. 16 ETB creatures give deep redundancy, so you recover fast off any single creature.

## Reskins (for borrowers)

No reskinned cards — everything runs under its printed Magic name (Satya is a standard *Aetherdrift* legend, not an FF/ATLA reskin). The deck is a straightforward ETB/token engine; the only thing to internalize is the **tapped-and-attacking token ruling** under Don't-miss rulings above.
