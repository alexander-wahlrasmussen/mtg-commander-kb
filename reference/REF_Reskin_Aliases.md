# Universes Beyond Reskin Aliases

Reskin cards are mechanically identical to an existing MTG card but printed under a different name. For deckbuilding, collection tracking, and GC verification, treat them as the same card.

---

## Rules

- **Collection demand:** merge reskins and originals into one pool under the original MTG name.
- **GC verification:** look up the *original* name. A reskin of a GC is still a GC.
- **Recommendations:** if a card appears unowned, check this list *before* declaring it missing.
- **In summaries and discussion:** name the reskin first, then the original in parentheses. "Aang's Shelter (Teferi's Protection)".

---

## Confirmed aliases

### Avatar: The Last Airbender

| Reskin name | Original MTG card |
|---|---|
| Aang's Shelter | Teferi's Protection |
| The Banyan Tree | The Great Henge |
| Lifelong Friendship | Eladamri's Call |
| Castle Shimura | Eiganjo Castle |
| Wild Rose Rebellion | Counterspell |
| Joo Dee, Public Servant | Sakashima of a Thousand Faces |
| Dawn Warriors' Legacy | Mizzix's Mastery |

### Final Fantasy

| Reskin name | Original MTG card |
|---|---|
| Paradise Chocobo | Birds of Paradise |
| Newfound Adventure | Farseek |

### Lord of the Rings

| Reskin name | Original MTG card |
|---|---|
| Morgul-Knife | Shadowspear |
| Fangorn Forest | Yavimaya, Cradle of Growth |

### Secret Lair alternate-name printings

| Reskin name | Original MTG card |
|---|---|
| Master Emerald Shrine | Command Tower |
| La abuela, siempre generosa | Tireless Provisioner |

> The four 2026-07-04 additions (Newfound Adventure, Fangorn Forest, Master Emerald
> Shrine, La abuela siempre generosa) are *official* alternate-name printings indexed
> by Scryfall itself (`fca` / `ltc` / `sld` sets) — not user-applied custom names.
> Confirmed via Scryfall API 2026-07-04 (Hearthhull external list evaluation).

> ⚠️ **Name collision:** a *real, different* card is named **Morgul-Knife Wound** (`{1}{B}`
> Enchantment — Aura, color identity **B**). A `card_lookup.py` search for "Morgul-Knife"
> fuzzy-matches that black aura, **not** Shadowspear. In a mono-red list the black card is illegal,
> so always resolve "Morgul-Knife" via this alias → Shadowspear (colorless). Confirmed 2026-06-12.

### Other / mechanical analogues

| Name | Mechanical analogue | Notes |
|---|---|---|
| Bayo, Irritable Instructor | Electro, Assaulting Battery | User-applied custom name. Printed card is `Electro, Assaulting Battery` (Marvel set), a mono-R legendary creature. Confirmed 2026-06-01. |
| Ellie's Rage | Dictate of Erebos | Set TBC |
| Merata, Neuron Hacker | Lady Octopus, Inspired Inventor | User-applied custom name (cyber theme); printed card is from Marvel set. Confirmed 2026-05-06. |
| Green Dragon Inn | Homeward Path | User-applied custom name (Tolkien tavern theme); printed card is `Homeward Path` (C16). Confirmed 2026-05-08. |
| Storm's Will | Jeska's Will | User-applied custom name. **Jeska's Will is a Game Changer** — a reskin of a GC is still a GC. Confirmed 2026-06-12 (Clive external list). |
| Helm's Deep | Shinka, the Bloodsoaked Keep | User-applied custom name (Tolkien theme); printed card is the red legendary land. Confirmed 2026-06-12 (Clive external list). |
| Wakandan Skyscraper | Karn's Bastion | User-applied custom name (Marvel theme); printed card is the colorless proliferate land. Confirmed 2026-06-12 (Clive external list). |
| Calliope's Song | Seething Song | User-applied custom name; printed card is the red ritual (add {R}{R}{R}{R}{R} — oracle-verified 2026-06-12, current printing is an instant). Confirmed 2026-06-12 (Clive external list). |

---

## Protocol when encountering an unfamiliar UB card

1. **Check this file** for a listed alias.
2. **If not listed:** web-search the card's Oracle text on Scryfall.
3. **If the Oracle text reads as identical** to a known MTG card, propose the alias, confirm with Alex, and append to this file.
4. **Never declare a card unowned** without completing step 1.

---

## Why this matters

UB sets (ATLA, Final Fantasy, LotR) print mechanically identical cards under thematic names. A deck built for one of these sets may list "Wild Rose Rebellion" — which is Counterspell — and the collection search will return no match if the alias isn't resolved first.

This has caused false "missing card" reports in the past. The check is cheap; the error is expensive.
