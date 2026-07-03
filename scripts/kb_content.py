#!/usr/bin/env python3
"""kb_content.py — parse the repo's KB sources into the JSON the dashboard's
content pages (Home / Decks / Collection / Wishlist / DeckPage) render.

This is the *content* sibling of dashboard_server's *sim* computes: where the sim
side runs pod_gauntlet / pod_championship, this side reads the static knowledge
base — Deck_Index.md, each deck's _Summary.md + dated .txt, the Moxfield CSV
(+ Scryfall oracle data), and Build_And_Swap_Tracker.md — and returns plain
JSON-serialisable dicts. dashboard_server exposes these as /api/*, and
dashboard_export bakes them for the static (no-backend) build.

Reuses the house tooling instead of re-deriving it:
  - deck_registry.DECKS            per-deck identity / cc / cc_axes / win_line / stem
  - deck_sim.load_reskin_aliases   UB reskin -> canonical name (CLAUDE.md hard rule)
  - validate.load_game_changers    the authoritative GC list (Full List section)
  - card_lookup.load_cards         Scryfall oracle data (colour / rarity / type / text)
  - analysis/pod_gauntlet_clocks.json   harvested decap/table CDFs + medians

Pure-ish: roster()/deck()/collection()/wishlist() read files only. home() is a
pure assembler over a gauntlet + championship result the caller already computed
(keeps this module free of the sim-stack import, no cycle with dashboard_server).

CLI smoke test (no sim stack needed):
    python scripts/kb_content.py            # roster + wishlist + collection sizes
    python scripts/kb_content.py deck genome_project
"""
import importlib.util as _il
import json
import re
import sys
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"

for _s in (sys.stdout, sys.stderr):
    if hasattr(_s, "reconfigure"):
        try:
            _s.reconfigure(encoding="utf-8", errors="replace")
        except (ValueError, OSError):
            pass


def _load(name):
    spec = _il.spec_from_file_location(name, SCRIPTS / f"{name}.py")
    mod = _il.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ---------------------------------------------------------------- house modules
deck_registry = _load("deck_registry")
DECKS = deck_registry.DECKS
# kill-tree specs keyed by registry slug (KILL_TREES is keyed by display-slug, carries reg_slug)
_KILL_TREES_BY_REG = {sp["reg_slug"]: sp for sp in deck_registry.KILL_TREES.values()}


@lru_cache(maxsize=1)
def _aliases():
    return _load("deck_sim").load_reskin_aliases()


@lru_cache(maxsize=1)
def _gc_names():
    return _load("validate").load_game_changers()


@lru_cache(maxsize=1)
def _clocks():
    p = ROOT / "analysis" / "pod_gauntlet_clocks.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}


@lru_cache(maxsize=1)
def _cards_index():
    """name(lower) -> Scryfall card record (front + face names indexed).

    Degrades to {} when collection/oracle-cards.json is absent (it's the ~140MB
    gitignored Scryfall bulk; run scripts/update_scryfall_data.py to fetch it).
    Without it, per-card colour/role/rarity enrichment is skipped — deck pips fall
    back to the Deck_Index colour label (see _label_pips)."""
    cl = _load("card_lookup")
    if not cl.DATA_FILE.exists():
        return {}
    cards = cl.load_cards()
    idx = {}
    for c in cards:
        if c.get("layout") in {"art_series", "double_faced_token", "token"}:
            continue
        names = {c.get("name", "").lower()}
        for f in c.get("card_faces", []):
            if f.get("name"):
                names.add(f["name"].lower())
        for n in names:
            idx.setdefault(n, c)
    return idx


# ----------------------------------------------------------------- small helpers
def _norm(s):
    """Fold curly apostrophes/dashes so KB names match across files."""
    return (s.replace("’", "'").replace("‘", "'")
            .replace("–", "-").replace("—", "-").strip())


def _strip_annot(s):
    """Card name with any trailing `*(annotation)*` / `(note)` removed, then normed.

    Summary decklists annotate cards inline (e.g. `The Banyan Tree *(reskin: The
    Great Henge)*`); the annotation must come off or the name won't match the .txt."""
    return _norm(re.sub(r"\s*\*?\([^)]*\)\*?\s*$", "", s))


@lru_cache(maxsize=1)
def _name_to_slug():
    return {_norm(d["name"]).lower(): s for s, d in DECKS.items()}


def _resolve(name):
    """Reskin alias -> canonical, then the Scryfall record (or None).

    Tolerates Moxfield's split/adventure 'A/B' spelling: Scryfall indexes those as
    'A // B' (and under each face), so the raw .txt 'Expansion/Explosion' would miss
    and fall into the by-type 'Other' group (and count as CMC 0 in the curve). Fold
    any '/'/'//' separator to ' // ', then fall back to the front face."""
    idx = _cards_index()
    canon = _aliases().get(name.lower(), name)
    rec = idx.get(canon.lower())
    if rec is None and "/" in canon:
        rec = (idx.get(re.sub(r"\s*/+\s*", " // ", canon).lower())
               or idx.get(canon.split("/")[0].strip().lower()))
    return rec


def _parse_decklist(path):
    """(count, name) per line of a `N Card Name` decklist; sideboard excluded.

    Moxfield exports the maindeck, then a blank-line-separated `SIDEBOARD:` block
    (our maybeboard), then the commander as a trailing block. The sideboard is NOT
    part of the deck. A marker opens a skip region; the next blank line closes it,
    so the trailing commander is still read. (Matching only a bare lowercase
    `sideboard` missed Moxfield's `SIDEBOARD:` colon — it counted the maybeboard,
    inflating both this list and the GC tallies built on it.)"""
    out, skip = [], False
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line:
            skip = False                      # blank line ends a section
            continue
        low = line.lower().rstrip(":")
        if low in ("sideboard", "maybeboard"):
            skip = True
            continue
        if skip or low in ("deck", "commander"):
            continue
        m = re.match(r"^(\d+)\s+(.+?)\s*$", line)
        if m:
            out.append((int(m.group(1)), _norm(m.group(2))))
    return out


def _newest_txt(stem):
    hits = sorted((ROOT / "decks").glob(f"{stem}-*.txt"))
    return hits[-1] if hits else None


def _gc_count(stem):
    """Game Changers in a deck's newest .txt (reskin-resolved ∩ GC list)."""
    path = _newest_txt(stem)
    if not path:
        return None
    gc = _gc_names()
    aliases = _aliases()
    hits = set()
    for _, name in _parse_decklist(path):
        canon = aliases.get(name.lower(), name).lower()
        if canon in gc:
            hits.add(canon)
    return len(hits)


_ORDER = {"W": 0, "U": 1, "B": 2, "R": 3, "G": 4}

# Guild / shard / wedge → WUBRG letters, so pips work without Scryfall (the
# Deck_Index "Colors" column is the fallback source when oracle data is absent).
_COLOR_LABELS = {
    "white": "W", "blue": "U", "black": "B", "red": "R", "green": "G",
    "azorius": "WU", "dimir": "UB", "rakdos": "BR", "gruul": "RG", "selesnya": "GW",
    "orzhov": "WB", "izzet": "UR", "golgari": "BG", "boros": "RW", "simic": "GU",
    "bant": "GWU", "esper": "WUB", "grixis": "UBR", "jund": "BRG", "naya": "RGW",
    "abzan": "WBG", "jeskai": "URW", "sultai": "BGU", "mardu": "RWB", "temur": "GUR",
    "5c": "WUBRG", "wubrg": "WUBRG",
}


def _sort_pips(letters):
    return sorted(set(letters), key=lambda c: _ORDER.get(c, 9))


def _label_pips(label):
    """WUBRG letters from a guild/shard name or a raw 'WUBG'-style colour string."""
    key = (label or "").strip().lower()
    if key in _COLOR_LABELS:
        return _sort_pips(_COLOR_LABELS[key])
    raw = [c for c in (label or "").upper() if c in _ORDER]
    return _sort_pips(raw)


def _commander_pips(commander, label=""):
    """Colour-identity letters (WUBRG order): Scryfall if present, else label."""
    rec = _resolve(commander)
    ci = rec.get("color_identity", []) if rec else []
    return _sort_pips(ci) if ci else _label_pips(label)


def _tier(score):
    if score is None:
        return "unscored"
    if score >= 17:
        return "elite"
    if score >= 13:
        return "solid"
    return "developing"


# ------------------------------------------------------------ Deck_Index parsing
_INDEX_HEADER = re.compile(r"^\|\s*Deck\s*\|", re.I)


@lru_cache(maxsize=1)
def _deck_index_rows():
    """Active-roster table rows from Deck_Index.md → {name: {...}} (pre-Retired)."""
    text = (ROOT / "Deck_Index.md").read_text(encoding="utf-8")
    rows = {}
    in_table = False
    for raw in text.splitlines():
        if raw.strip().lower().startswith("### retired"):
            break
        if _INDEX_HEADER.match(raw):
            in_table = True
            continue
        if in_table:
            if not raw.lstrip().startswith("|"):
                continue
            cells = [c.strip() for c in raw.strip().strip("|").split("|")]
            if len(cells) < 6 or set(cells[0]) <= set("-: "):
                continue  # separator / malformed
            name, commander, colors, score, archetype, status = cells[:6]
            m = re.search(r"(\d+)\s*/\s*20", score)
            rows[_norm(name).lower()] = dict(
                name=_norm(name), commander=_norm(commander), colors=colors,
                score=int(m.group(1)) if m else None,
                archetype=archetype, status=status.split("(")[0].strip(),
            )
    return rows


# ===================================================================== ROSTER ==
def roster():
    """Active roster for Decks/Home: identity + score + clock + GC, score-sorted."""
    idx = _deck_index_rows()
    clocks = _clocks()
    out = []
    for slug, d in DECKS.items():
        ix = idx.get(_norm(d["name"]).lower(), {})
        ck = clocks.get(slug, {})
        med = ck.get("med", [None, None])
        out.append(dict(
            slug=slug, name=d["name"], commander=d["commander"],
            colors=ix.get("colors", ""),
            pips=_commander_pips(d["commander"], ix.get("colors", "")),
            score=d["cc"], archetype=ix.get("archetype", ""),
            tier=_tier(d["cc"]), status=ix.get("status", ""),
            decap=med[0], table=med[1], gc=_gc_count(d["stem"]),
        ))
    out.sort(key=lambda r: (r["score"] is None, -(r["score"] or 0)))
    return out


# ==================================================================== COLLECTION
# Heuristic role tags (the template's 8 buckets) from type_line + oracle_text.
# Order = priority: first match wins. Approximate + editable, not authoritative.
_ROLE_RULES = [
    ("wipe", re.compile(r"destroy all|each player sacrifices|to all creatures|"
                        r"all creatures get -|exile all", re.I)),
    ("tutor", re.compile(r"search your library for (a|up to|two|that)", re.I)),
    ("ramp", re.compile(r"add \{[wubrgc0-9]|search your library for .*(land|basic)|"
                        r"adds? an additional|mana of any (one )?color", re.I)),
    ("removal", re.compile(r"destroy target|exile target|deals? \d+ damage to (target|any)|"
                           r"target creature gets -|fight target", re.I)),
    ("draw", re.compile(r"draw (a card|\w+ cards|cards equal)", re.I)),
    ("recur", re.compile(r"return target .*from (your |a )?graveyard|"
                         r"from your graveyard to (the battlefield|your hand)", re.I)),
    ("prot", re.compile(r"hexproof|indestructible|counter target|protection from|"
                        r"can't be countered|gains? shroud", re.I)),
    ("fin", re.compile(r"wins the game|loses the game|infect|double strike|"
                       r"creatures you control get \+|extra (turn|combat)", re.I)),
]


def classify_role(card):
    """One of ramp/draw/removal/wipe/prot/recur/tutor/fin, or '' — heuristic."""
    tl = card.get("type_line", "")
    txt = card.get("oracle_text", "") or " ".join(
        f.get("oracle_text", "") for f in card.get("card_faces", []))
    if "Land" in tl and "add" in txt.lower():
        return "ramp"
    for role, rx in _ROLE_RULES:
        if rx.search(txt):
            return role
    return ""


_PRIMARY = {"W": "W", "U": "U", "B": "B", "R": "R", "G": "G"}


def _card_color(card):
    ci = card.get("color_identity", [])
    if not ci:
        return "C"
    return ci[0] if len(ci) == 1 else "M"  # mono letter, else multicolor


def collection():
    """Owned cards (Moxfield CSV ⋈ Scryfall) + colour/role/rarity facet counts."""
    csvs = sorted((ROOT / "collection").glob("moxfield_haves_*.csv"))
    if not csvs:
        return dict(count=0, cards=[], facets=dict(color={}, role={}, rarity={}))
    import csv as _csv
    idx = _cards_index()
    aliases = _aliases()
    cards, seen = [], set()
    facet_color, facet_role, facet_rarity = {}, {}, {}
    with csvs[-1].open(encoding="utf-8", newline="") as f:
        for row in _csv.DictReader(f):
            name = _norm(row.get("Name", ""))
            if not name or name.lower() in seen:
                continue
            seen.add(name.lower())
            rec = idx.get(aliases.get(name.lower(), name).lower())
            color = _card_color(rec) if rec else "C"
            role = classify_role(rec) if rec else ""
            rarity = (rec.get("rarity", "") if rec else "").title()
            try:
                qty = int(row.get("Count") or 1)
            except ValueError:
                qty = 1
            cards.append(dict(
                name=name, set=(rec.get("set", "") if rec else "").upper(),
                color=color, cost=(rec.get("mana_cost", "") if rec else ""),
                cmc=(rec.get("cmc", 0) if rec else 0),
                rarity=rarity, role=role, qty=qty,
            ))
            for facet, key in ((facet_color, color), (facet_role, role or "—"),
                               (facet_rarity, rarity or "—")):
                facet[key] = facet.get(key, 0) + 1
    cards.sort(key=lambda c: c["name"])
    return dict(count=len(cards), cards=cards,
                facets=dict(color=facet_color, role=facet_role, rarity=facet_rarity))


# ====================================================================== DECKPAGE
def _summary_path(name):
    """Best-guess _Summary.md for a deck display name."""
    stem = re.sub(r"[^A-Za-z0-9]+", "_", _norm(name)).strip("_")
    for cand in (ROOT / "decks").glob("*_Summary.md"):
        key = cand.name[:-len("_Summary.md")]
        if key.lower().replace("_", "") in stem.lower().replace("_", "") or \
           stem.lower().replace("_", "") in key.lower().replace("_", ""):
            return cand
    return None


def _summary_sections(path):
    """{heading_lower: (heading, body)} for '## '/'### ' sections of a Summary.

    Keyed lowercase for matching; the original-case heading is kept for display
    (kill-line titles are proper nouns)."""
    if not path or not path.exists():
        return {}
    secs, cur, buf = {}, None, []
    for raw in path.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^#{2,3}\s+(.+?)\s*$", raw)
        if m:
            if cur is not None:
                secs[cur[0]] = (cur[1], "\n".join(buf).strip())
            head = m.group(1).strip()
            cur, buf = (head.lower(), head), []
        elif cur is not None:
            buf.append(raw)
    if cur is not None:
        secs[cur[0]] = (cur[1], "\n".join(buf).strip())
    return secs


def _first_para(text):
    for block in re.split(r"\n\s*\n", text):
        b = block.strip()
        if b and not b.startswith(("|", "-", "*", ">")):
            return re.sub(r"\s+", " ", b)
    return ""


def _composition(path):
    """Functional buckets from a Summary's '## Decklist' → '### Name (N)' headings."""
    if not path or not path.exists():
        return []
    out, in_list = [], False
    for raw in path.read_text(encoding="utf-8").splitlines():
        h2 = re.match(r"^##\s+(.+)", raw)
        if h2:
            in_list = "decklist" in h2.group(1).lower()
            continue
        if in_list:
            # tolerate trailing text in the count paren, e.g. "Lands (36, plus … total)"
            m = re.match(r"^###\s+(.+?)\s*\((\d+)[^)]*\)", raw.strip())
            # exact match: the command-zone card sits under '### Commander (1)'; don't
            # swallow real functional buckets like '### Commander Protection (5)'. Also
            # drop a '### Sideboard/Maybeboard (N)' — it's not part of the 99.
            if m and m.group(1).strip().lower() not in ("commander", "sideboard", "maybeboard"):
                out.append(dict(name=m.group(1).strip(), count=int(m.group(2))))
    return out


# Card-type grouping (the alternate decklist view) — priority order; a card with
# several types files under the first it matches, so 'Artifact Creature' → Creatures.
_TYPE_ORDER = ["Creature", "Planeswalker", "Instant", "Sorcery",
               "Artifact", "Enchantment", "Battle", "Land"]
_TYPE_PLURAL = {"Creature": "Creatures", "Planeswalker": "Planeswalkers",
                "Instant": "Instants", "Sorcery": "Sorceries", "Artifact": "Artifacts",
                "Enchantment": "Enchantments", "Battle": "Battles", "Land": "Lands",
                "Other": "Other"}


def _primary_type(rec):
    """Front-face card type for grouping (split/MDFC → the face before '//')."""
    tl = ((rec or {}).get("type_line") or "").split("//")[0]
    for t in _TYPE_ORDER:
        if t in tl:
            return t
    return "Other"


def _summary_buckets(path):
    """Ordered [(bucket, [card names])] from a Summary's '## Decklist' section.

    The labels (Mana Engines / Burn Finishers / …) are curation, not ground truth —
    the .txt owns the card set. Used only to GROUP the .txt cards (see _decklist).
    The Commander bucket is dropped; the commander is surfaced separately."""
    if not path or not path.exists():
        return []
    out, cur, in_list = [], None, False
    for raw in path.read_text(encoding="utf-8").splitlines():
        h2 = re.match(r"^##\s+(.+)", raw)
        if h2:
            in_list = "decklist" in h2.group(1).lower()
            cur = None
            continue
        if not in_list:
            continue
        h3 = re.match(r"^###\s+(.+)$", raw.strip())
        if h3:
            name = re.sub(r"\s*\(.*\)\s*$", "", h3.group(1)).strip()   # drop "(N)" / "(note)"
            # exact match only: keep '### Commander Protection' as a real bucket; the
            # command-zone card ('### Commander (1)') is surfaced separately by _decklist.
            # Sideboard/Maybeboard headings aren't deck cards (and aren't in the .txt main).
            cur = None if name.lower() in ("commander", "sideboard", "maybeboard") else [name, []]
            if cur:
                out.append(cur)
            continue
        if cur is not None:
            # card lines come in two Summary styles — numbered ("1 Card Name") and
            # bulleted ("- Card Name"); accept either lead-in (Lightning War et al. bullet
            # their decklist, so a numbered-only match filed every card under "Other").
            m = re.match(r"^(?:\d+|[-*])\s+(.+?)\s*$", raw.strip())
            if m:
                cur[1].append(_strip_annot(m.group(1)))
    return out


def _decklist(txt_path, summary_path, commander, gc_names, aliases):
    """The deck's 100 cards as a grouped, copy-pasteable, pilot-facing reference.

    Ground truth is the dated .txt (CLAUDE.md hierarchy). The Summary only LABELS:
    each .txt card is filed under the functional bucket the Summary assigns it (the
    same buckets as the composition bar); .txt cards the Summary doesn't mention fall
    to an 'Other' group rather than vanishing, so Summary drift is visible not silent.
    No Summary section → a flat alphabetical fallback. No Scryfall needed."""
    if not txt_path or not txt_path.exists():
        return None

    def _is_gc(name):
        return aliases.get(name.lower(), name).lower() in gc_names

    def _card(name):
        return dict(n=name, gc=_is_gc(name))

    def _key(name):  # alias-resolved, 'The'-insensitive identity for commander match
        a = aliases.get(name.lower(), name).lower()
        return re.sub(r"^the\s+", "", a).strip()

    # Pull the commander out of the maindeck pool. The registry may store a short
    # spelling ('Wise Mothman') while the .txt has the real card ('The Wise Mothman');
    # match alias-resolved + 'The'-insensitive, and display the deck's actual name.
    cmd_key, cmd_name, seen_cmd = _key(commander), commander, False
    entries = []
    for c, n in _parse_decklist(txt_path):
        if not seen_cmd and _key(n) == cmd_key:
            cmd_name, seen_cmd = n, True
            continue
        entries.append((c, n))
    counts = {}
    for c, n in entries:
        counts[n] = counts.get(n, 0) + c
    total = sum(counts.values()) + 1  # + commander

    # bucket name → file order, so we can place each .txt card under its Summary label
    buckets = _summary_buckets(summary_path)
    where = {}
    for bi, (_label, cards) in enumerate(buckets):
        for nm in cards:
            where.setdefault(nm.lower(), bi)

    grouped = bool(buckets)
    if grouped:
        bins = [[] for _ in buckets]
        other = []
        for n in sorted(counts):
            bi = where.get(n.lower())
            (bins[bi] if bi is not None else other).append(n)
        groups = []
        for (label, _cards), names in zip(buckets, bins):
            if names:
                groups.append(dict(name=label, count=sum(counts[n] for n in names),
                                   cards=[_card(n) for n in names]))
        if other:
            groups.append(dict(name="Other", count=sum(counts[n] for n in other),
                               cards=[_card(n) for n in other]))
    else:
        names = sorted(counts)
        groups = [dict(name="The 99", count=sum(counts.values()),
                       cards=[_card(n) for n in names])]

    # Alternate view + mana curve — Scryfall-derived (type_line / cmc), so both are
    # None when the oracle bulk is absent and the front-end hides the toggle/curve.
    groups_by_type, curve = None, None
    if _cards_index():
        by, curve_counts = {}, {}
        for n in sorted(counts):
            rec = _resolve(n)
            by.setdefault(_primary_type(rec), []).append(n)
            if "Land" not in ((rec or {}).get("type_line") or ""):  # curve = nonland spells
                cmc = int((rec or {}).get("cmc", 0) or 0)
                b = "7+" if cmc >= 7 else str(cmc)
                curve_counts[b] = curve_counts.get(b, 0) + counts[n]
        groups_by_type = [
            dict(name=_TYPE_PLURAL[t], count=sum(counts[x] for x in by[t]),
                 cards=[_card(x) for x in by[t]])
            for t in _TYPE_ORDER + ["Other"] if t in by
        ]
        curve = [dict(cmc=b, n=curve_counts.get(b, 0))
                 for b in ("0", "1", "2", "3", "4", "5", "6", "7+")]

    return dict(
        total=total, grouped=grouped,
        commander=dict(n=cmd_name, gc=_is_gc(cmd_name)),
        groups=groups, groupsByType=groups_by_type, curve=curve,
        text=txt_path.read_text(encoding="utf-8").strip(),
    )


def _image_url(rec):
    """Scryfall 'normal' JPEG for a card record; multi-face layouts (transform /
    modal_dfc) carry image_uris per face, so fall back to the front face."""
    if not rec:
        return None
    uris = rec.get("image_uris") or (rec.get("card_faces") or [{}])[0].get("image_uris") or {}
    return uris.get("normal")


def card_images(names):
    """name -> Scryfall CDN image URL for hover previews, keyed on the CALLER's
    spelling (.txt decklist / baked-hand names), alias- and split-card-resolved
    like everything else. {} when the oracle bulk is absent — the front-end then
    simply shows no previews (hotlinking scryfall.io images is permitted)."""
    if not _cards_index():
        return {}
    out = {}
    for n in names:
        url = _image_url(_resolve(n))
        if url:
            out[n] = url
    return out


def _deck_images(decklist):
    """The hover-preview map for one deck page: every decklist card + the
    commander. None (payload-omitted semantics) when there's nothing to map."""
    if not decklist:
        return None
    names = {c["n"] for g in decklist["groups"] for c in g["cards"]}
    names.add(decklist["commander"]["n"])
    return card_images(sorted(names)) or None


def _first_sentence(text):
    p = _first_para(text)
    return re.split(r"(?<=[.!])\s", p)[0] if p else ""


def _split_finisher(title_raw, note):
    """Title → {name, tag}: a trailing '(tag)' or ' — tag' becomes the tag."""
    title = title_raw.strip().rstrip(":.").strip()
    tag = ""
    pm = re.search(r"\(([^)]+)\)\s*$", title)            # trailing "(primary)"
    if pm:
        tag, title = pm.group(1).strip(), title[:pm.start()].strip()
    else:
        dm = re.split(r"\s+[—-]\s+", title, maxsplit=1)  # "Title — tag"
        if len(dm) > 1:
            title, tag = dm[0].strip(), dm[1].strip()
    note = re.split(r"(?<=[.!])\s", note.strip())[0] if note else ""
    return dict(name=title.rstrip(":.").strip(), tag=tag, note=note)


# Index may be a number (Line 1) or a letter (Line A — Zero-Sum's style).
_LINE_SUB = re.compile(r"(?i)^(?:kill\s+)?line\s*(?:\d+|[a-z])\s*[:—-]\s*(.+)")
_LINE_BOLD = re.compile(r"(?i)^\*\*\s*(?:kill\s+)?line\s*(?:\d+|[a-z])\s*[—:.-]\s*(.+?)\*\*[:.]?\s*(.*)$")
# Fallback list shape (Forced Liquidation): 'N. **Card Name** *(tag)* — note', where the
# bold lead IS the line's name rather than a 'Line N' label.
_LINE_NUM = re.compile(r"^(?:\d+[.)]|[-*])\s+\*\*(.+?)\*\*\s*(.*)$")


def _finisher_from_numbered(name, rest):
    """A '**Name** *(tag)* — note' list item → {name, tag, note} (the bold is the name; a
    leading italic *(tag)* and an em-dash note follow)."""
    rest = rest.strip()
    tag = ""
    tm = re.match(r"^\*\(?\s*([^*)]+?)\s*\)?\*\s*[—:.\-]*\s*(.*)$", rest)   # leading *italic* tag
    if tm:
        tag, rest = tm.group(1).strip(), tm.group(2)
    else:
        dm = re.match(r"^[—:.\-]+\s*(.*)$", rest)
        if dm:
            rest = dm.group(1)
    return dict(name=_demph(name).rstrip(":.").strip(), tag=_demph(tag),
                note=_first_sentence(rest))


def _kill_lines(sections):
    """Finishers from a Summary — tolerant of the heading/format variants across Summaries.

    A) '### Kill Line N: Title — tag' / '### Line N — Title (tag)' subheadings.
    B) under a '## Kill Lines' / '## Closing Lines' / 'How We End Games' section, in priority:
       B1) '**Line N — Title:** desc' (or 'Line A —' letter index) bold-lead items;
       B2) fallback 'N. **Name** *(tag)* — note' numbered/bulleted bold-lead items.
    Subheadings win; else B1; else B2."""
    out = []
    for low, (head, body) in sections.items():
        if _LINE_SUB.match(low):
            out.append(_split_finisher(_LINE_SUB.match(head).group(1), _first_sentence(body)))
    if out:
        return out[:8]
    body = ""
    for low, (_head, sec) in sections.items():
        if any(k in low for k in ("kill line", "closing line", "how we end games",
                                  "how you win", "how we win")):
            body = sec
            break
    lines = body.splitlines()
    for i, ln in enumerate(lines):
        m = _LINE_BOLD.match(ln.strip())
        if m:
            note = m.group(2).strip()
            if not note:                      # '**Line N — Title**' with the description on
                for nxt in lines[i + 1:]:     # the FOLLOWING line (5 Summaries' real shape —
                    s = nxt.strip()           # radiation/replication/earthbend/exiles/diminishing)
                    if not s:                 # blank line ends the one-paragraph note
                        break
                    if _LINE_BOLD.match(s) or _LINE_SUB.match(s) or s.startswith("#"):
                        break                 # next label/heading -> this line truly had no note
                    note = s                  # first continuation line (first sentence taken below)
                    break
            out.append(_split_finisher(m.group(1), note))
    if out:
        return out[:8]
    for ln in body.splitlines():                       # B2 — numbered bold-lead (FL style)
        m = _LINE_NUM.match(ln.strip())
        if m:
            out.append(_finisher_from_numbered(m.group(1), m.group(2)))
    return out[:8]


def _demph(s):
    """Strip markdown bold/italic markers for plain-text display."""
    return re.sub(r"\*+", "", s).strip()


def _rulings(sections):
    """Pilot 'don't-miss rulings' from a Summary — the card-text gotchas that lose
    games when missed (hidden types, trigger ordering, threshold counting, reskin
    behaviour). Parses bullets under a '## Don't-Miss Rulings' (or '… Key Rulings')
    section: a leading '**headline**' becomes the name, the rest the note; a plain
    bullet keeps its whole text as the note. This is the one piece of the retired
    pilot primers the Summary/deck-page didn't already carry."""
    # Prefer the deck-wide '## Don't-Miss Rulings'; only fall back to an incidental
    # single-card '### … Key Rulings' subsection if the deck-wide one is absent.
    body, best = "", 9
    for low, (_head, sec) in sections.items():
        tier = 0 if "miss ruling" in low else 1 if (low.endswith("key rulings") or low == "rulings") else 9
        if tier < best:
            body, best = sec, tier
            if tier == 0:
                break
    out = []
    for raw in body.splitlines():
        m = re.match(r"^[-*]\s+(.*\S)\s*$", raw.strip())
        if not m:
            continue
        item = m.group(1).strip()
        b = re.match(r"^\*\*(.+?)\*\*\s*[—:.,;\-]*\s*(.*)$", item)
        if b:
            out.append(dict(name=_demph(b.group(1)).rstrip(":"), note=_demph(b.group(2))))
        else:
            out.append(dict(name="", note=_demph(item)))
    return out[:12]


def _game_plan(secs, fallback):
    """The deck-page one-paragraph overview. Prefer a prose section with a SUBSTANTIVE first
    paragraph; skip empties so we never stop on a table ('Quick Reference' is a table, not
    prose). Match any '## What the Deck …' heading by prefix ('does' / 'is trying to do' both
    occur in the Summaries), then the other overview headings in priority; else the terse
    win-line. (Audit 2026-06-28: Eldrazi stalled on Quick Reference, LW on a heading variant.)"""
    keys = [low for low in secs if low.startswith("what the deck")]
    keys += [k for k in ("core loop", "overview", "how it wins", "the plan", "strategy")
             if k in secs]
    for low in keys:
        para = _first_para(secs[low][1])
        if len(para) >= 40:                         # a real sentence, not a list lead-in stub
            return para
    return fallback


# How-it-kills framing (the redesigned page flips the kill module by `mode`): a
# cheapest-first LADDER for combo decks, parallel VECTORS for grind/drain decks, a
# board-power BEATDOWN curve for ramp-aggro. Default ladder; this map names the
# non-ladder decks. `kind` (the registry's 5th line field) → a short chip tag.
_KILL_MODE = {
    "eldrazi_stampede": "beatdown",
    "dark_lords_army": "vectors",
    "diminishing_returns": "vectors",
    "radiation_sickness": "vectors",
    "curse_of_the_scarab": "vectors",
}
_KILL_TAG = {"combo": "combo", "table": "table", "combat": "decap", "enabler": "enabler"}
_KILL_MODE_CAPTION = {
    "ladder": "cheapest line first · fall to the next",
    "vectors": "parallel vectors — they stack, not rank",
    "beatdown": "a curve, not a tree — ramp the board, then alpha",
}


def _kill_tree(slug):
    """Structured kill module for the deck page (one per roster deck). The same cheapest-first
    specs kill_tree.py renders to Mermaid (deck_registry.KILL_TREES), served here to a hand-rolled
    React module that flips between ladder / vectors / beatdown by `mode`. Pure registry data — no
    Scryfall, no sim. Text fields keep their `<br/>` line breaks; the front-end splits on them.
    Each line carries a short `tag` (from its kind) and a `primary` flag (the headline line)."""
    sp = _KILL_TREES_BY_REG.get(slug)
    if not sp:
        return None
    bg = sp.get("background")
    mode = _KILL_MODE.get(slug, "ladder")
    return dict(
        title=sp["title"], root=sp["root"], stall=sp["stall"], src=sp["src"],
        mode=mode, caption=_KILL_MODE_CAPTION.get(mode, _KILL_MODE_CAPTION["ladder"]),
        stallLabel="When nothing’s up",
        background=(dict(need=bg[0], kill=bg[1], clock=bg[2], kind=bg[3],
                         tag=_KILL_TAG.get(bg[3], bg[3])) if bg else None),
        lines=[dict(id=l[0], need=l[1], kill=l[2], clock=l[3], kind=l[4],
                    tag=_KILL_TAG.get(l[4], l[4]), primary=(i == 0))
               for i, l in enumerate(sp["lines"])],
    )


# ---------------------------------------------------------- Brief/Full extras
# The redesigned scouting report (DeckPage.dc.html) adds a BRIEF returning-player
# mode on top of the existing FULL report. Most of its slots derive from data that
# is ALREADY card-checked and baked (kill lines, clock medians, keep model, Summary
# prose); only a few are editorial. We DERIVE every slot for all 17 decks from that
# ground truth, then let OVERRIDES (below) refine the worked-example decks with the
# design's authored copy. Nothing here invents a card interaction or a clock number.
_BOTTLENECK_KEEP = {
    "FINDING": "a route to a combo piece (you tutor or dig for the rest)",
    "MANA": "your mana coming online roughly on curve",
    "BOARD": "an early play that builds toward the commander",
}
_WIN_RX = re.compile(r"combo|finisher|payoff|drain|win\s?con|wincon|burn|"
                     r"infinite|closer|alpha|kill", re.I)


def _tnum(s):
    m = re.search(r"\d+", s or "")
    return int(m.group()) if m else None


def _strip_links(s):
    """Drop [[memory-link]] wiki markers, keeping the readable phrase."""
    return re.sub(r"\[\[([^\]]+)\]\]", lambda m: m.group(1).replace("_", " "), s or "")


def _flatbr(s):
    return re.sub(r"\s*<br\s*/?>\s*", " ", s or "").strip()


def _idea(game_plan):
    """One-line hero 'idea' — the game plan's first sentence, markdown/link-stripped."""
    return _demph(_strip_links(_first_sentence(game_plan) or game_plan or ""))


def _vitals(clock, gc):
    """Three derived vital signs (measured, not editorial): clock, decap, GC count."""
    decap, table = clock.get("decap"), clock.get("table")
    return [
        dict(label="Clock", value=(table or decap or "—"), accent=True,
             sub=(f"decap {decap}" if decap else "measured table kill")),
        dict(label="Decap", value=(decap or "—"), sub="one opponent"),
        dict(label="Game Changers", value=f"{len(gc)}/3", sub="bracket-3 cap"),
    ]


def _openings(axes, keep, clock):
    """'How it loses' bullets, derived from the same structured fields the FULL page used."""
    out = []
    if axes:
        low = min(axes, key=lambda a: a["score"])
        out.append(f"Weakest axis — {low['label']} ({low['score']}/5): the judges' soft spot.")
    mixed = (keep or {}).get("mixed")
    if mixed:
        out.append(mixed[0].upper() + mixed[1:].rstrip(".") + ".")
    never = clock.get("never") or []
    if never and never[0]:
        out.append(f"Decap never-closes in {never[0]}% of goldfish games — a grind risk.")
    if len(never) > 1 and never[1]:
        out.append(f"Tables (all three) never-close {never[1]}% of the time.")
    return out[:4]


def _clock_extras(clock):
    """Headline VS card + band-chart geometry, derived from the harvested medians/grid."""
    decap, table = clock.get("decap"), clock.get("table")
    grid = clock.get("grid") or []
    af = grid[0] if grid else 5
    at = grid[-1] if grid else 14
    bands = []
    for lab, val, kind in (("decap", _tnum(decap), "decap"), ("table", _tnum(table), "table")):
        if val is not None:
            bands.append({"label": lab, "from": val, "to": val, "kind": kind})
    ticks = [t for t in grid if (t - af) % 2 == 0] or list(range(af, at + 1, 2))
    return dict(
        sub="measured kill-clock",
        headline=[dict(label="Decap · one opp", value=(decap or "—"), sub="median kill", kind="decap"),
                  dict(label="Table · all three", value=(table or "—"), sub="median kill", kind="table")],
        bands=bands, ticks=ticks, axisFrom=af, axisTo=at,
        note="", noteLabel="",
        caption=(f"Decap (one opponent) lands around {decap}; the full table around {table}."
                 if decap and table else "Measured kill-clock from the deck's clock lab."),
    )


def _brief_kills(kill_tree, finishers):
    """The two kill lines that win, for BRIEF mode — the top kill-tree lines (or finishers)."""
    out = []
    if kill_tree and kill_tree.get("lines"):
        for i, l in enumerate(kill_tree["lines"][:2]):
            out.append(dict(idx=f"{i + 1:02d}", tag=l.get("tag", ""),
                            primary=l.get("primary", i == 0), clock=l.get("clock", ""),
                            line=f"{_flatbr(l['need'])} → {_flatbr(l['kill'])}"))
    else:
        for i, f in enumerate(finishers[:2]):
            line = f"{f['name']} — {f['note']}" if f.get("note") else f["name"]
            out.append(dict(idx=f"{i + 1:02d}", tag=f.get("tag", ""),
                            primary=(i == 0), clock="", line=line))
    return out


def _mark_win(composition):
    """Flag the single wincon bucket (first name matching the win lexicon) for the comp bar."""
    out, flagged = [], False
    for b in composition:
        win = (not flagged) and bool(_WIN_RX.search(b["name"]))
        flagged = flagged or win
        out.append(dict(name=b["name"], count=b["count"], win=win))
    return out


def _mull_strategy(keep):
    """The BRIEF keep heuristic, from the deck's keep model (bottleneck axis + land band)."""
    bn = (keep or {}).get("bottleneck")
    lo, hi = (keep or {}).get("minLands"), (keep or {}).get("maxLands")
    band = f"{lo}–{hi}" if lo is not None and hi is not None else "2–4"
    s = f"Keep {band} lands with {_BOTTLENECK_KEEP.get(bn, 'a workable opener toward the game plan')}."
    mixed = (keep or {}).get("mixed")
    if mixed:
        s += f" {mixed[0].upper()}{mixed[1:].rstrip('.')}."
    return s


_MULL_LABEL_RE = re.compile(r"\*\*Mulligan[.:]?\*\*[.:]?\s*", re.I)


def _mull_from_summary(sections):
    """The Summary's own mulligan paragraph — Piloting Notes' '**Mulligan.**' lead — so
    the deck page shows the audited per-deck keep guidance (mulligan audit 2026-07-03)
    instead of the derived band heuristic. The Summary is the single source of truth;
    None (no section / no paragraph) falls back to _mull_strategy."""
    for low, (_head, body) in sections.items():
        if not low.startswith("piloting notes"):
            continue
        for para in re.split(r"\n\s*\n", body):
            p = para.strip()
            if _MULL_LABEL_RE.match(p):
                return _strip_md(_MULL_LABEL_RE.sub("", p, count=1))
    return None


def _apply_override(payload, ov):
    """Field-by-field override merge; clock/killTree/mull merge into the derived dicts."""
    for k, v in ov.items():
        if k in ("clock", "killTree", "mull") and isinstance(payload.get(k), dict) and isinstance(v, dict):
            payload[k].update(v)
        else:
            payload[k] = v


# Authored copy for the design's three worked examples (verbatim from the Pod Gauntlet
# design system's DeckPage template). Every other deck renders the derived copy above.
# These refine editorial slots only — kill-tree lines, clock medians, decklist and
# rulings stay sourced from the registry / Summary / clock labs (the ground truth).
OVERRIDES = {
    "lightning_war": {
        "kicker": "In the Grixis corner", "corner": "Bracket 3 · Grixis",
        "tagline": "You set the clock — close on your turn, where Abolisher can’t act",
        "colorLine": "Grixis · UBR",
        "idea": "When Fire Lord Azula attacks, every spell you cast that combat happens three "
                "times. The whole deck bends toward the one swing where that multiplier turns "
                "lethal — and races to get there first.",
        "vitals": [
            {"label": "Clock", "value": "~T9", "accent": True, "sub": "combo is the clock · decap T8"},
            {"label": "Win on", "value": "Your turn", "sub": "Abolisher can’t act"},
            {"label": "Plan B", "value": "Burn race", "sub": "copy-X · 45 each"},
        ],
        "briefKillsCaption": "the two that win",
        "openings": [
            "Weakest axis — Durability (4/5): graveyard-hate exposure on the recursion / storm backup.",
            "Tables never-close in 17% of goldfish games — a grindy, disrupted pod stretches the clock.",
            "Tutor-gated combo: stack interaction at the 8 tutors and the kill slips a turn.",
            "Creature-light — go-wide aggro can pressure or race you; you answer, you don’t block.",
        ],
        # mull: sourced from the Summary's Piloting Notes (mulligan audit 2026-07-03)
        "clock": {"sub": "measured kill-clock", "note": "", "noteLabel": "",
                  "caption": "The combo (~T9) is the fastest table kill — infinite mana into Torment "
                             "ends the table in one cast; the race alone tables much later."},
        "killTree": {"stallLabel": "When nothing’s up"},
    },
    "dark_lords_army": {
        "kicker": "In the Grixis corner", "corner": "Bracket 3 · Grixis",
        "tagline": "Durability is the point — recover from wipes trivially and let the drain do the work",
        "colorLine": "Grixis · UBR",
        "idea": "Sauron punishes opponents for playing the game: every spell they cast amasses your "
                "Army, every card they draw bleeds them. There is no explosive turn — you assemble a "
                "tax-and-drain web and grind the table out over several cycles.",
        "vitals": [
            {"label": "Clock", "value": "T9–12", "accent": True, "sub": "opponent-driven · faster vs active pods"},
            {"label": "Win by", "value": "Attrition", "sub": "drain on their draws"},
            {"label": "Watch", "value": "Ganged up", "sub": "slowest clock · yard hate"},
        ],
        "briefKillsCaption": "two ways life totals hit zero",
        "openings": [
            "Weakest axis — Kill Reliability (4/5): no single-turn finish; you win on accumulated advantage over 2–4 turns.",
            "Fast combo can race the grind — the counter suite is the answer, not the clock.",
            "Graveyard hate clamps the reset backup; the primary drain survives it.",
            "Threat perception: the slowest clock in the sweep invites being ganged up before drain matters.",
        ],
        # mull: sourced from the Summary's Piloting Notes (mulligan audit 2026-07-03)
        "clock": {"sub": "opponent-driven clock", "noteLabel": "opp-driven",
                  "note": "The engine is opponent-driven — it kills FASTER against active pods, because "
                          "amass and drain feed on opponents’ spells and draws.",
                  "caption": "No single explosive finish — drain accumulates over 2–4 turns, the slowest "
                             "clock in the sweep. Manage threat perception so you aren’t ganged up before it matters."},
        "killTree": {"stallLabel": "The long game"},
    },
    "eldrazi_stampede": {
        "kicker": "In the Temur corner", "corner": "Bracket 3 · Temur",
        "tagline": "Build the curve, then swing — Craterhoof turns a wide board into a one-turn table kill",
        "colorLine": "Temur · GUR",
        "idea": "Ramp hard, cheat huge creatures into play with haste, and turn the board sideways. "
                "There is no combo to assemble — you build a damage curve and, once the board is wide "
                "enough, one alpha strike ends the table.",
        "vitals": [
            {"label": "Clock", "value": "T8–12", "accent": True, "sub": "decap T8 · table T12"},
            {"label": "Win by", "value": "Alpha strike", "sub": "Craterhoof / wide swing"},
            {"label": "Watch", "value": "Wraths & combo", "sub": "no counters · Rift resets you"},
        ],
        "briefKillsCaption": "ramp, then one big swing",
        "openings": [
            "No hard counterspells despite blue — combo decks that go off T4–6 pre-empt your T6–8 window.",
            "Cyclonic Rift / Farewell are devastating — thin recursion, a 3–4 turn rebuild.",
            "Politically loud — Annihilator and 12/12 Eldrazi draw the table’s fire; expect to be the early target.",
            "Weakest axes — Durability & Interaction (3/3): the deck dominates the board but answers little.",
        ],
        # mull: sourced from the Summary's Piloting Notes (mulligan audit 2026-07-03)
        "clock": {"sub": "measured kill-clock", "noteLabel": "slow build",
                  "note": "Does not race the pod — a T≤7 decap lands only ~26% of games; the table kill "
                          "needs Craterhoof, 8 mana, and a wide board at once.",
                  "caption": "The Craterhoof alpha is the real table kill — trample + X/X across a wide "
                             "board ends three opponents at once. The Wanderer cascades are the fast decap."},
        "killTree": {"stallLabel": "When you stall",
                     "curve": [{"t": 3, "p": 5}, {"t": 4, "p": 11}, {"t": 5, "p": 19},
                               {"t": 6, "p": 30}, {"t": 7, "p": 44}, {"t": 8, "p": 60}],
                     "lethalAt": 40, "lethalLabel": "wide alpha = lethal"},
    },
}


def deck(slug):
    """Full Tale-of-the-Tape payload for one deck — structured spine + Summary prose."""
    d = DECKS.get(slug)
    if not d:
        raise ValueError(f"unknown deck slug: {slug!r}")
    ix = _deck_index_rows().get(_norm(d["name"]).lower(), {})
    ck = _clocks().get(slug, {})
    sp = _summary_path(d["name"])
    secs = _summary_sections(sp)

    # GC list (canonical names) from the newest .txt
    gc_used, gc_names, aliases = [], _gc_names(), _aliases()
    txt = _newest_txt(d["stem"])
    if txt:
        for _, name in _parse_decklist(txt):
            canon = aliases.get(name.lower(), name).lower()
            if canon in gc_names and gc_names[canon] not in gc_used:
                gc_used.append(gc_names[canon])

    axes_labels = ["Core loop", "Kill reliability", "Durability", "Interaction"]
    axes = ([dict(label=lab, score=sc) for lab, sc in zip(axes_labels, d["cc_axes"])]
            if d.get("cc_axes") else [])

    game_plan = _game_plan(secs, (d.get("win_line") or {}).get("line", ""))

    colors = ix.get("colors", "")
    pips = _commander_pips(d["commander"], colors)
    score = d["cc"]
    clock = dict(
        decap=(ck.get("med") or [None, None])[0],
        table=(ck.get("med") or [None, None])[1],
        grid=ck.get("grid", []), decapCurve=ck.get("decap", []),
        tableCurve=ck.get("table", []), never=ck.get("never", []),
        src=ck.get("src", ""),
    )
    clock.update(_clock_extras(clock))
    kill_tree = _kill_tree(slug)
    finishers = _kill_lines(secs)
    composition = _mark_win(_composition(sp))
    dl = _decklist(txt, sp, d["commander"], gc_names, aliases)
    keep = dict(
        bottleneck=d.get("bottleneck"), minLands=d.get("min_lands"),
        maxLands=d.get("max_lands"), mixed=d.get("mixed"),
    )

    payload = dict(
        slug=slug, name=d["name"], commander=d["commander"],
        colors=colors, pips=pips,
        archetype=ix.get("archetype", ""), status=ix.get("status", ""),
        bracket=3, score=score, axes=axes, axesTotal=(f"{score}/20" if score is not None else "—/20"),
        gc=gc_used,
        # ---- redesigned scouting report: hero / brief identity (derived, OVERRIDES refine) ----
        kicker=(f"In the {colors} corner" if colors else (ix.get("archetype", "") or "")),
        corner=(f"Bracket 3 · {colors}" if colors else "Bracket 3"),
        tagline=(d.get("win_line") or {}).get("line", ""),
        colorLine=(f"{colors} · {''.join(pips)}" if colors else "".join(pips)),
        idea=_idea(game_plan),
        vitals=_vitals(clock, gc_used),
        briefKillsCaption="the lines that win",
        briefKills=_brief_kills(kill_tree, finishers),
        openings=_openings(axes, keep, clock),
        clock=clock,
        gamePlan=game_plan,
        winLine=(d.get("win_line") or {}).get("line", ""),
        finishers=finishers,
        rulings=_rulings(secs),
        composition=composition,
        decklist=dl,
        images=_deck_images(dl),
        keep=keep,
        mull=dict(strategy=_mull_from_summary(secs) or _mull_strategy(keep)),
        killTree=kill_tree,
    )
    ov = OVERRIDES.get(slug)
    if ov:
        _apply_override(payload, ov)
    return payload


# ====================================================================== WISHLIST
_COST = {"\U0001F7E2": "free", "\U0001F7E1": "small", "\U0001F534": "major"}
_GATE = "\U0001F512"


def _cost_of(cell):
    for emoji, tag in _COST.items():
        if emoji in cell:
            return tag
    return "free"


def _strip_md(s):
    s = re.sub(r"\*\*?|`|~~", "", s)
    return re.sub(r"\s+", " ", s).strip()


def wishlist():
    """Build & Swap Tracker → builds (§1), recommended swaps (§2 table), buys (§3)."""
    text = (ROOT / "Build_And_Swap_Tracker.md").read_text(encoding="utf-8")
    lines = text.splitlines()

    # --- §1 builds ---
    builds = []
    i = 0
    while i < len(lines):
        m = re.match(r"^###\s+1[a-z]\.\s+(.+)", lines[i])
        if m:
            head = m.group(1)
            gate = _GATE in head
            tm = re.search(r"\*(.+?)\*", head)
            theme = _strip_md(tm.group(1)) if tm else ""
            name = _strip_md(re.split(r"\s+[—-]\s+", head)[0])
            clock = gc = ""
            acquire = None
            for j in range(i + 1, min(i + 10, len(lines))):
                ln = lines[j]
                if ln.startswith("### ") or ln.startswith("## "):
                    break
                cm = re.search(r"Clock:\*\*\s*([^·|]+?)\s*(?:·|\||$)", ln)
                if cm:
                    clock = _strip_md(cm.group(1))
                gm = re.search(r"GCs?:\*\*\s*([0-9]/[0-9])", ln)
                if gm:
                    gc = gm.group(1)
                am = re.search(r"(\d+)\s+unowned", ln)
                if am:
                    acquire = int(am.group(1))
            builds.append(dict(name=name, theme=theme, clock=clock, gc=gc,
                               acquire=acquire, cost="major", gate=gate))
        i += 1

    # --- §2 recommended swaps (markdown table) ---
    swaps = []
    in_tbl = False
    for raw in lines:
        if re.match(r"^\|\s*Deck\s*\|\s*Out\b", raw, re.I):
            in_tbl = True
            continue
        if in_tbl:
            if not raw.lstrip().startswith("|"):
                if swaps:
                    in_tbl = False
                continue
            cells = [c.strip() for c in raw.strip().strip("|").split("|")]
            if len(cells) < 6 or set(cells[0]) <= set("-: "):
                continue
            deck_name, change, _src, cost, gate, status = cells[:6]
            applied = "applied" in status.lower() or "✅" in deck_name
            chg = _strip_md(change)
            out_in = re.split(r"\s*[→]\s*", chg, maxsplit=1)  # → if present
            swaps.append(dict(
                deck=_strip_md(deck_name), change=chg,
                out=out_in[0] if len(out_in) > 1 else "",
                into=out_in[1] if len(out_in) > 1 else chg,
                cost=_cost_of(cost), gate=(_GATE in gate or "approval" in gate.lower()),
                applied=applied,
            ))

    # --- §3 cheap unlocks (bullets: "- Card ×N → Deck (~€…)") ---
    buys, in_buys = [], False
    for raw in lines:
        h = re.match(r"^##\s+3\.", raw)
        if h:
            in_buys = True
            continue
        if in_buys:
            if raw.startswith("## "):
                break
            m = re.match(r"^-\s+(.+?)\s+[×x](\d+)\s*→\s*(.+?)\s*(?:\(([^)]*)\))?\s*$",
                         raw.strip())
            if m:
                buys.append(dict(card=_strip_md(m.group(1)), qty="×" + m.group(2),
                                 unlocks=_strip_md(m.group(3)), note=_strip_md(m.group(4) or "")))

    k_free = sum(1 for s in swaps if s["cost"] == "free" and not s["applied"])
    k_small = sum(1 for s in swaps if s["cost"] == "small") + len(buys)
    k_gates = sum(1 for s in swaps if s["gate"]) + sum(1 for b in builds if b["gate"])
    return dict(builds=builds, swaps=swaps, buys=buys,
                counts=dict(free=k_free, small=k_small, builds=len(builds), gates=k_gates))


# ========================================================================== HOME
def home(gauntlet=None, champ=None):
    """Dashboard hub — pure assembler over roster + a gauntlet + championship result.

    `gauntlet` is a compute_gauntlet() dict ({params, rows:[{slug,name,win,...}]});
    `champ` is a compute_championship() dict. Both optional — the page degrades to
    roster-only KPIs when the sim outputs aren't supplied.
    """
    rs = roster()
    clocks = _clocks()
    by_slug = {r["slug"]: r for r in rs}
    tiers = {}
    for r in rs:
        tiers[r["tier"]] = tiers.get(r["tier"], 0) + 1

    g_rows = sorted((gauntlet or {}).get("rows", []), key=lambda x: -x.get("win", 0))
    champion = (champ or {}).get("champion", {})
    runner = ((champ or {}).get("notes", {}) or {}).get("runner_up", {})

    top_score = max((r["score"] for r in rs if r["score"] is not None), default=None)
    best = g_rows[0] if g_rows else None

    champ_name = champion.get("name", "") if champion else ""
    kpis = [
        dict(label="Decks", value=str(len(rs)),
             sub=f"{tiers.get('elite', 0)} Elite · {tiers.get('solid', 0)} Solid"),
        dict(label="Champion", value=(re.sub(r"^The\s+", "", champ_name) or "—"),
             sub="Pod Championship"),
        dict(label="Best vs pod", value=(f"{best['win']*100:.0f}%" if best else "—"),
             sub=(best["name"] if best else "")),
        dict(label="Top score", value=(f"{top_score}/20" if top_score else "—"),
             sub=f"{sum(1 for r in rs if r['score'] == top_score)} decks" if top_score else ""),
    ]

    # clock overlay: top racers by gauntlet win that have a curve (else top-score)
    overlay_slugs = [r["slug"] for r in g_rows[:4]] or [r["slug"] for r in rs[:4]]
    clock_series = []
    for slug in overlay_slugs:
        ck = clocks.get(slug)
        if ck:
            clock_series.append(dict(
                name=ck["name"], grid=ck["grid"], decap=ck["decap"]))

    pod_rows = [dict(name=r.get("name"), pct=round(r.get("win", 0) * 100))
                for r in g_rows[:3]]

    awards = []
    if champion:
        awards.append(dict(label="MVP · Champion", winner=champion.get("name", ""),
                           note="Won the Pod Championship bracket"))
    if best:
        awards.append(dict(label="Bring vs the pod", winner=best["name"],
                           note=f"{best['win']*100:.0f}% to beat the pod"))
    if top_score:
        top_deck = next((r for r in rs if r["score"] == top_score), None)
        if top_deck:
            awards.append(dict(label="Top judges' score", winner=top_deck["name"],
                               note=f"{top_score}/20 Conversion Check"))
    open_deck = next((r for r in rs if r["gc"] == 0), None)
    if open_deck:
        awards.append(dict(label="Open upgrade path", winner=open_deck["name"],
                           note="0 Game Changers — room for 3"))

    return dict(
        kpis=kpis,
        champion=dict(name=champion.get("name", ""), seed=champion.get("seed", 1),
                      note=(f"Pod Championship winner."
                            + (f" Runner-up: {runner.get('name')} (#{runner.get('seed')})."
                               if runner else ""))),
        clockSeries=clock_series,
        roster=[dict(name=r["name"], commander=r["commander"], score=r["score"],
                     slug=r["slug"], decap=r["decap"], table=r["table"], tier=r["tier"])
                for r in rs[:6]],
        pod=pod_rows, awards=awards,
    )


# ============================================================================ CLI
if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] == "deck":
        print(json.dumps(deck(args[1]), indent=2, ensure_ascii=False))
    elif args and args[0] in ("roster", "wishlist", "collection", "home"):
        print(json.dumps(globals()[args[0]](), indent=2, ensure_ascii=False)[:4000])
    else:
        r = roster()
        print(f"roster: {len(r)} decks; top = {r[0]['name']} ({r[0]['score']}/20, "
              f"GC {r[0]['gc']}, clock {r[0]['decap']}/{r[0]['table']})")
        w = wishlist()
        print(f"wishlist: {len(w['builds'])} builds, {len(w['swaps'])} swaps, "
              f"{len(w['buys'])} buys; counts={w['counts']}")
        c = collection()
        print(f"collection: {c['count']} cards; colors={c['facets']['color']}")
