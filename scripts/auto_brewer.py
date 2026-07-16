#!/usr/bin/env python3
"""Auto-Brewer -- search the owned pool for the best UNBUILT commander decks.

The pipeline every deck in this repo went through by hand -- notice a
commander, check what the collection gives it, draft a 99, judge the
consistency -- run as an instrument over the whole owned pool:

  census : every owned card that can legally helm a deck (Legendary Creature
           front face, or "can be your commander" text), with its in-identity
           owned-pool size and roster status (ROSTER / KNOWN / NEW).
  combos : owned Commander Spellbook combos the commander anchors (variants
           endpoint, front-face matched, reskin-resolved, response cached
           under analysis/autobrew/ -- the repo's first CSB cache).
  brew   : a template 99 from the owned pool -- combo package first, then
           function-tag quotas (ramp 12 / draw 8 / removal 5 / wipes 2 /
           tutors 3), then theme fill scored from the commander's own oracle
           text, then a manabase with pip-weighted basics.
  score  : deck_sim screening -- keepable%, flow (dead turns / hellbent),
           ramp/draw counts, colour consistency, and a combo-assembly
           availability curve (speed_lab_core.simulate_groups).
  sweep  : census -> combos -> brew -> score for every candidate; ranked
           leaderboard to analysis/autobrew/leaderboard.json.

DISCIPLINE -- this is a SCREENING instrument:
  * Every number is SCREEN-grade (consistency / availability). The assembly
    curve is P(pieces SEEN by turn T) -- no mana costs, no opposition, no
    kill resolution. It is NEVER a kill-window claim. A winner here
    graduates to a hand-written proposal + a real *_clock_lab run, per the
    cite-the-lab rule (REF_The_Conversion_Check.md).
  * Output lives under analysis/autobrew/, NEVER decks/ -- deck_doctor --all
    (the CI legality gate) and speed_lab_core.resolve_deck_arg both sweep
    decks/**, and an auto-brewed rough 100 must not reach either.
  * Proxies count as owned (house rule). Reskins resolve through
    deck_sim.load_reskin_aliases. Availability contention (a card physically
    deployed in an active deck) is NOT enforced here -- run
    availability_check.py before physically building anything proposed.
  * House rules enforced during the brew: max 3 Game Changers (commander
    counted), mass land denial excluded outright, at most one extra-turn
    card, no combo whose CSB "produces" mentions turns.

Usage:
  python scripts/auto_brewer.py census [--min-pool N] [--all-statuses]
  python scripts/auto_brewer.py brew "Commander Name" [--no-combos] [--write]
  python scripts/auto_brewer.py sweep [--min-pool N] [--limit N] [--top N]
                                      [--trials N] [--no-combos]
                                      [--include-known] [--refresh-combos]

Run with PYTHONIOENCODING=utf-8 on Windows (card names carry non-ASCII).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from collections import namedtuple
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

OUT_DIR = ROOT / "analysis" / "autobrew"
LISTS_DIR = OUT_DIR / "lists"
CACHE_FILE = OUT_DIR / "csb_variants_cache.json"
LEADERBOARD = OUT_DIR / "leaderboard.json"
TAGS_FILE = ROOT / "collection" / "oracle-tags.json"

CSB_VARIANTS = "https://backend.commanderspellbook.com/variants/"

# --- brew template ----------------------------------------------------------
LANDS_TARGET = 37
GC_CAP = 3            # validate.MAX_GC; kept literal so the pure core stays I/O-free
XTURN_CAP = 1         # house allowance: 0-1 extra-turn cards, no chains
BIG_CMC = 6           # curve guard threshold ...
BIG_CAP = 9           # ... and how many >=BIG_CMC cards a brew may run
COMBO_PIECE_CAP = 18  # distinct non-commander combo pieces seeded at most

QUOTAS = [
    # (label, target, otag names that satisfy it) -- vocabulary is the fixed
    # 39-tag taxonomy of update_tag_index.py (no 'boardwipe': use mass-removal).
    ("ramp",    12, frozenset({"ramp", "mana-rock", "mana-dork"})),
    ("draw",     8, frozenset({"draw", "cantrip", "wheel"})),
    ("removal",  5, frozenset({"spot-removal", "counterspell"})),
    ("wipes",    2, frozenset({"mass-removal"})),
    ("tutors",   3, frozenset({"tutor"})),
]

BASIC_FOR = {"W": "Plains", "U": "Island", "B": "Swamp", "R": "Mountain",
             "G": "Forest"}
NONBASIC_CAP = {0: 6, 1: 8, 2: 14, 3: 18, 4: 22, 5: 26}  # by colour count

TYPE_DASH = "—"

# One owned, commander-legal oracle card, everything the pure brew core needs.
# All flags precomputed at load time so brew_deck / score_card stay hermetic.
PoolCard = namedtuple(
    "PoolCard",
    "disp oid ci cmc type_line text tags produced pips "
    "is_land is_cmdr is_gc is_mld is_xturn")

Brew = namedtuple(
    "Brew",
    "commander ci deck spells lands basics quota_report themes tribes "
    "combo_package combos_seeded notes gc_hits")


# ---------------------------------------------------------------------------
# small pure helpers
# ---------------------------------------------------------------------------

def front(name):
    """Front face of a DFC/split full name ('A // B' -> 'A')."""
    return name.split("//")[0].strip()


def _the_variants(name):
    """Lowercase name variants for registry/CSB matching ('Wise Mothman' vs
    'The Wise Mothman')."""
    low = front(name).lower()
    other = low[4:] if low.startswith("the ") else "the " + low
    return {low, other}


def slugify(name):
    s = re.sub(r"[^a-z0-9]+", "-", front(name).lower()).strip("-")
    return s or "unnamed"


def curve_median(curve, thresh=50.0):
    """First turn whose cumulative pct >= thresh, else None."""
    for t in sorted(curve):
        if curve[t] >= thresh:
            return t
    return None


def clamp01(x):
    return max(0.0, min(1.0, x))


# ---------------------------------------------------------------------------
# commander predicate + theme profile (pure -- hermetically tested)
# ---------------------------------------------------------------------------

def can_be_commander(rec):
    """Legendary Creature on the FRONT face, or the card's own text grants it
    ("can be your commander" -- planeswalkers etc.). Banned cards excluded.
    Partners/Backgrounds are NOT paired (v1 limitation: single commander)."""
    if rec.get("legalities", {}).get("commander") != "legal":
        return False
    faces = rec.get("card_faces") or []
    front_tl = (faces[0].get("type_line", "") if faces else
                rec.get("type_line", "")).split("//")[0].lower()
    if "legendary" in front_tl and "creature" in front_tl:
        return True
    parts = [rec.get("oracle_text", "") or ""]
    for f in faces:
        parts.append(f.get("oracle_text", "") or "")
    return "can be your commander" in " ".join(parts).lower()


Theme = namedtuple("Theme", "label trigger tags card_rx type_hook")


def _t(label, trigger, tags=(), card=None, type_hook=None):
    return Theme(label, re.compile(trigger), frozenset(tags),
                 re.compile(card) if card else None, type_hook)


# trigger: matched against the COMMANDER's oracle text (lowercased).
# tags / card_rx / type_hook: what a POOL card scores synergy points for.
# NOTE current Scryfall wording: "enters" (not "enters the battlefield").
THEMES = [
    _t("aristocrats", r"\bsacrifice\b|whenever .{0,40} dies",
       ("sacrifice-outlet", "recursion"),
       r"\bsacrifice\b|whenever .{0,40} dies"),
    _t("graveyard", r"graveyard", ("reanimate", "recursion", "mill"),
       r"from (your|a) graveyard"),
    _t("tokens", r"creates? .{0,60}token", ("anthem",),
       r"creates? .{0,60}token"),
    _t("spellslinger",
       r"instant or sorcery|noncreature spell|copy .{0,20}spell",
       ("cantrip", "copy"), r"instant or sorcery|copy target (instant|sorcery)"),
    _t("counters", r"\+1/\+1 counter|proliferate", (),
       r"\+1/\+1 counter|proliferate"),
    _t("lifegain", r"gains? (\d+ |x )?life|lifelink", ("lifegain",),
       r"gains? (\d+ |x )?life|lifelink"),
    _t("draw-matters", r"whenever you draw|draws? (a|two|three) cards?",
       ("draw", "cantrip", "wheel"), r"draws? (a|two|three|that many) cards?"),
    _t("discard", r"discards?\b", ("discard", "wheel"), r"discards?\b"),
    _t("mill", r"\bmills?\b", ("mill",), r"\bmills?\b"),
    _t("landfall", r"landfall|land enters|play .{0,30}lands?",
       ("landfall", "lands-matter", "ramp"), r"landfall|land enters"),
    _t("artifacts", r"artifact", ("mana-rock",), r"artifact", "artifact"),
    _t("enchantments", r"enchantment", (), r"enchantment", "enchantment"),
    _t("drain", r"loses? (\d+ |x )?life", ("pinger", "lifegain"),
       r"loses? (\d+ |x )?life|each opponent"),
    _t("combat", r"attacks?\b|combat damage|extra combat",
       ("extra-combat", "evasion"),
       r"attacks?\b|double strike|extra combat"),
    _t("etb", r"when .{0,40} enters", ("flicker",),
       r"when .{0,40} enters"),
    _t("theft", r"gain control", ("theft",), r"gain control"),
    _t("wide", r"creatures you control", ("anthem",),
       r"creatures you control"),
]


def theme_profile(cmdr):
    """(active_themes, tribes) from the commander's own text/type line.
    A creature subtype counts as a tribe only when the commander's TEXT
    mentions it (e.g. 'other Zombies you control') -- being a Wizard is not
    Wizard tribal."""
    text = cmdr.text
    active = [th for th in THEMES if th.trigger.search(text)]
    tribes = []
    front_tl = cmdr.type_line.split("//")[0]
    if TYPE_DASH in front_tl:
        for sub in front_tl.split(TYPE_DASH)[1].split():
            if re.search(r"\b" + re.escape(sub.lower()) + r"s?\b", text):
                tribes.append(sub)
    return active, tribes


def score_card(pc, themes, tribes):
    """Synergy screen score for one pool card vs an active theme profile."""
    s = 0.0
    tl = pc.type_line.lower()
    tags = frozenset(pc.tags)
    for th in themes:
        hit = False
        if tags & th.tags:
            s += 8.0
            hit = True
        if th.card_rx and th.card_rx.search(pc.text):
            s += 4.0 if hit else 6.0
        if th.type_hook and th.type_hook in tl and not pc.is_land:
            s += 5.0
    for t in tribes:
        tp = re.escape(t.lower())
        if re.search(r"\b" + tp + r"\b", tl):
            s += 10.0
        elif re.search(r"\b" + tp + r"s?\b", pc.text):
            s += 5.0
    s += min(len(pc.tags), 3) * 1.0
    s -= max(0.0, pc.cmc - 4.0) * 1.5
    return s


# ---------------------------------------------------------------------------
# the brew core (pure -- hermetically tested)
# ---------------------------------------------------------------------------

def _combo_is_house_legal(row):
    """House rule: no combo whose product mentions turns (repeatable extra
    turns are banned; 'Infinite turns' etc.)."""
    return not any("turn" in p.lower() for p in row.get("produces", []))


def brew_deck(cmdr, pool, combos, lands_target=LANDS_TARGET):
    """Assemble a screening 99 for `cmdr` (a PoolCard) from `pool` (PoolCards
    already CI-filtered, commander excluded). `combos` = complete-combo rows
    [{'pieces': [names], 'produces': [features], 'popularity': int}].
    Deterministic: no randomness, all ties broken by name."""
    spell_target = 99 - lands_target
    by_oid = {}
    for pc in pool:
        by_oid.setdefault(pc.oid, pc)
    nonlands = [pc for pc in by_oid.values() if not pc.is_land and not pc.is_mld]
    lands = [pc for pc in by_oid.values() if pc.is_land and not pc.is_mld]

    themes, tribes = theme_profile(cmdr)
    sc = {pc.oid: score_card(pc, themes, tribes) for pc in nonlands}

    chosen = {}
    notes = []
    state = {"gc": 1 if cmdr.is_gc else 0, "xturn": 0, "big": 0}
    if cmdr.is_gc:
        notes.append("commander is a Game Changer (counts toward the cap)")

    def addable(pc):
        if pc.oid in chosen or len(chosen) >= spell_target:
            return False
        if pc.is_gc and state["gc"] >= GC_CAP:
            return False
        if pc.is_xturn and state["xturn"] >= XTURN_CAP:
            return False
        return True

    def add(pc):
        if not addable(pc):
            return False
        chosen[pc.oid] = pc
        state["gc"] += 1 if pc.is_gc else 0
        state["xturn"] += 1 if pc.is_xturn else 0
        state["big"] += 1 if pc.cmc >= BIG_CMC else 0
        return True

    # 1. combo package -- smallest complete combos first, popularity breaks ties.
    name_ix = {}
    for pc in nonlands:
        name_ix.setdefault(pc.disp.lower(), pc)
        name_ix.setdefault(front(pc.disp).lower(), pc)
    package, combos_seeded = [], 0
    ordered = sorted(combos,
                     key=lambda r: (len(r["pieces"]), -r.get("popularity", 0),
                                    tuple(sorted(r["pieces"]))))
    for row in ordered:
        if not _combo_is_house_legal(row):
            notes.append("skipped combo (produces turns, house-banned): "
                         + " + ".join(row["pieces"]))
            continue
        pcs = [name_ix.get(front(p).lower()) or name_ix.get(p.lower())
               for p in row["pieces"]]
        if any(p is None for p in pcs):
            continue  # a piece is off-CI / a land / unresolved -> not brewable
        fresh = [p for p in pcs if p.oid not in chosen]
        if len(package) + len(fresh) > COMBO_PIECE_CAP:
            continue
        if not all(p.oid in chosen or addable(p) for p in pcs):
            continue  # would break GC/extra-turn caps
        for p in fresh:
            add(p)
            package.append(p.disp)
        combos_seeded += 1

    # 2. function-tag quotas (cards already in count toward each quota).
    quota_report = {}
    for label, target, tagset in QUOTAS:
        have = sum(1 for pc in chosen.values() if frozenset(pc.tags) & tagset)
        cands = sorted(
            (pc for pc in nonlands
             if pc.oid not in chosen and frozenset(pc.tags) & tagset),
            key=lambda pc: (-sc[pc.oid], pc.cmc, pc.disp))
        for pc in cands:
            if have >= target:
                break
            if add(pc):
                have += 1
        quota_report[label] = (have, target)

    # 3. synergy fill, curve-guarded.
    for pc in sorted((p for p in nonlands if p.oid not in chosen),
                     key=lambda p: (-sc[p.oid], p.cmc, p.disp)):
        if len(chosen) >= spell_target:
            break
        if pc.cmc >= BIG_CMC and state["big"] >= BIG_CAP:
            continue
        add(pc)
    if len(chosen) < spell_target:
        notes.append(f"pool thin: {len(chosen)} spells for {spell_target} "
                     "slots -- padding with basics")

    # 4. manabase: owned in-identity nonbasics, then pip-weighted basics.
    ci = set(cmdr.ci)

    def land_ok(pc):
        if "basic" in pc.type_line.lower():
            return False  # basics are assumed owned; counted separately
        if not ci:
            return bool(pc.produced)
        return bool(set(pc.produced) & ci) or "search your library" in pc.text

    def land_score(pc):
        s = len(set(pc.produced) & ci) * 3.0
        if not pc.produced and "search your library" in pc.text:
            s += 4.0  # fetch
        if any(th.label == "landfall" for th in themes) and \
                frozenset(pc.tags) & {"landfall", "lands-matter"}:
            s += 2.0
        return s

    good = sorted((pc for pc in lands if land_ok(pc)),
                  key=lambda pc: (-land_score(pc), pc.disp))
    nb_cap = NONBASIC_CAP.get(len(ci), 26)
    picked = good[:min(len(good), nb_cap, lands_target - 8)]

    basics_n = 99 - len(chosen) - len(picked)
    pips = {c: 0 for c in ci}
    for pc in chosen.values():
        for c, n in pc.pips.items():
            if c in pips:
                pips[c] += n
    basics = {}
    if not ci:
        basics["Wastes"] = basics_n
    else:
        total_pips = sum(pips.values()) or len(ci)
        order = sorted(ci, key=lambda c: (-pips.get(c, 0), c))
        left = basics_n
        for i, c in enumerate(order):
            share = pips.get(c, 0) / total_pips if total_pips else 1 / len(ci)
            n = max(1, round(share * basics_n)) if basics_n >= len(ci) else 0
            if i == len(order) - 1:
                n = left
            n = min(n, left)
            basics[BASIC_FOR[c]] = n
            left -= n
        if left > 0:
            basics[BASIC_FOR[order[0]]] += left
    basics = {k: v for k, v in basics.items() if v > 0}

    deck = ([(pc.disp, 1) for pc in
             sorted(chosen.values(), key=lambda p: (p.cmc, p.disp))]
            + [(pc.disp, 1) for pc in picked]
            + sorted(basics.items()))
    gc_hits = sorted(pc.disp for pc in chosen.values() if pc.is_gc)
    return Brew(commander=cmdr.disp, ci="".join(sorted(ci)) or "C",
                deck=deck, spells=len(chosen), lands=len(picked),
                basics=basics, quota_report=quota_report,
                themes=[th.label for th in themes], tribes=tribes,
                combo_package=package, combos_seeded=combos_seeded,
                notes=notes, gc_hits=gc_hits)


def composite(metrics):
    """SCREEN score 0-100 from the metric dict. Weights are documented, not
    calibrated -- combo axis (35) is deliberately heavy: this pod's bar is a
    proven kill package, not value (kill-shape lens)."""
    m = metrics
    pts = {
        "keepable": clamp01((m["keepable_pct"] - 55.0) / 35.0) * 20.0,
        "flow": clamp01((2.8 - m["mean_dead_turns"]) / 2.8) * 15.0,
        "colors": clamp01(m["colors_t4"] / 100.0) * 10.0,
        "ramp": clamp01(m["ramp_n"] / 12.0) * 10.0,
        "draw": clamp01(m["draw_n"] / 8.0) * 10.0,
    }
    if m.get("combos_seeded"):
        # Continuous: P(pieces SEEN by T10). A 50%-median cutoff is dead for
        # every deck (a specific 2-card combo is only ~4% seen-by-T13 without
        # dig -- 2026-07-15 sweep) -- 30%+ seen-by-T10 = full marks.
        pts["assembly"] = clamp01((m.get("assembly_t10") or 0.0) / 30.0) * 25.0
        pts["combo_depth"] = min(m.get("combos_owned", 0), 5) / 5.0 * 10.0
    else:
        pts["assembly"] = 0.0
        pts["combo_depth"] = 0.0
    return round(sum(pts.values()), 1), {k: round(v, 1) for k, v in pts.items()}


# ---------------------------------------------------------------------------
# heavy context (bulk + CSV + tags) -- everything I/O lives below this line
# ---------------------------------------------------------------------------

Ctx = namedtuple("Ctx", "pool owned_keys roster known aliases")


def _pips_of(rec):
    pips = {}
    costs = [rec.get("mana_cost") or ""]
    for f in rec.get("card_faces") or []:
        costs.append(f.get("mana_cost") or "")
    for sym in re.findall(r"\{([^}]+)\}", " ".join(costs)):
        for ch in sym.split("/"):
            if ch in "WUBRG":
                pips[ch] = pips.get(ch, 0) + 1
    return pips


def load_context():
    """Owned pool as PoolCards (proxies count as owned; reskin-resolved;
    commander-legal only; flags precomputed). One bulk parse via
    deck_doctor.load_full_index (lru_cached)."""
    from deck_sim import load_reskin_aliases
    from unlock_optimizer import load_owned, latest_csv
    from deck_doctor import (load_full_index, lookup, _all_text, is_mld,
                             is_extra_turn, _commander_legal, SKIP_LAYOUTS)
    from validate import load_game_changers
    import deck_registry as reg

    full = load_full_index()
    aliases = load_reskin_aliases()
    owned, proxy = load_owned(latest_csv(), aliases)
    counts = {}
    for k in set(owned) | set(proxy):
        n = owned.get(k, 0) + proxy.get(k, 0)
        if n > 0:
            counts[k] = n
    if not TAGS_FILE.exists():
        sys.exit(f"ERROR: {TAGS_FILE} not found -- run scripts/update_tag_index.py")
    tags_by_oid = json.loads(TAGS_FILE.read_text(encoding="utf-8")) \
        .get("by_oracle_id", {})
    gc_names = load_game_changers()

    pool = {}
    for key in counts:
        rec = lookup(full, aliases, key)
        if rec is None or rec.get("layout") in SKIP_LAYOUTS:
            continue
        if not _commander_legal(rec):
            continue
        oid = rec.get("oracle_id")
        if not oid or oid in pool:
            continue
        disp = rec.get("name", "")
        faces = rec.get("card_faces") or []
        front_tl = (faces[0].get("type_line", "") if faces else
                    rec.get("type_line", "")).split("//")[0].strip()
        low = disp.lower()
        pool[oid] = PoolCard(
            disp=disp, oid=oid, ci=frozenset(rec.get("color_identity", [])),
            cmc=float(rec.get("cmc", 0.0)), type_line=front_tl,
            text=_all_text(rec), tags=tuple(tags_by_oid.get(oid, ())),
            produced=tuple(rec.get("produced_mana") or ()),
            pips=_pips_of(rec), is_land="land" in front_tl.lower(),
            is_cmdr=can_be_commander(rec),
            is_gc=(low in gc_names or front(disp).lower() in gc_names),
            is_mld=is_mld(low, rec), is_xturn=is_extra_turn(rec))

    roster, known = set(), set()
    for name in reg.active_commanders().values():
        if name:
            roster |= _the_variants(name)
    for name in reg.EXTRA_COMMANDERS.values():
        if name:
            known |= _the_variants(name)
    return Ctx(pool=pool, owned_keys=set(counts), roster=roster, known=known,
               aliases=aliases)


def status_of(ctx, pc):
    v = _the_variants(pc.disp)
    if v & ctx.roster:
        return "ROSTER"
    if v & ctx.known:
        return "KNOWN"
    return "NEW"


def census(ctx):
    """[(PoolCard, status, pool_size)] for every owned commander candidate,
    pool_size = distinct owned commander-legal cards inside its identity."""
    out = []
    cards = list(ctx.pool.values())
    for pc in cards:
        if not pc.is_cmdr:
            continue
        n = sum(1 for q in cards if q.ci <= pc.ci) - 1
        out.append((pc, status_of(ctx, pc), n))
    out.sort(key=lambda r: (-r[2], r[0].disp))
    return out


def ci_pool(ctx, cmdr):
    return [pc for pc in ctx.pool.values()
            if pc.ci <= cmdr.ci and pc.oid != cmdr.oid]


# ---------------------------------------------------------------------------
# Commander Spellbook (network, cached)
# ---------------------------------------------------------------------------

def load_cache():
    if CACHE_FILE.exists():
        return json.loads(CACHE_FILE.read_text(encoding="utf-8"))
    return {}


def save_cache(cache):
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    CACHE_FILE.write_text(json.dumps(cache, indent=0, sort_keys=True),
                          encoding="utf-8")


_LAST_REQ = [0.0]
FETCH_GAP = 0.8  # min seconds between any two CSB requests (429s otherwise)


def _csb_get(url, tries=4):
    """Paced GET with Retry-After/backoff on 429 -- a 391-commander sweep
    rate-limited 310 fetches without this (2026-07-15)."""
    import urllib.error
    import urllib.request
    for attempt in range(tries):
        wait = _LAST_REQ[0] + FETCH_GAP - time.monotonic()
        if wait > 0:
            time.sleep(wait)
        req = urllib.request.Request(
            url, headers={"User-Agent": "mtg-commander-kb/auto_brewer"})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                data = json.load(r)
            _LAST_REQ[0] = time.monotonic()
            return data
        except urllib.error.HTTPError as e:
            _LAST_REQ[0] = time.monotonic()
            if e.code == 429 and attempt < tries - 1:
                retry = e.headers.get("Retry-After") or ""
                delay = int(retry) if retry.isdigit() else 20 * (attempt + 1)
                time.sleep(min(delay, 120))
                continue
            raise


def fetch_variants(card_name):
    """All CSB variants using `card_name` (paginated GET), trimmed for the
    cache: uses-names, produces-features, popularity, commander legality."""
    import urllib.parse
    url = (CSB_VARIANTS + "?q=" + urllib.parse.quote(f'card:"{card_name}"')
           + "&limit=100")
    out = []
    while url:
        data = _csb_get(url)
        for v in data.get("results", []):
            out.append({
                "uses": [u.get("card", {}).get("name", "")
                         for u in v.get("uses", [])],
                # Template requirements ("Persist Creature", "Free Sacrifice
                # Outlet"...) — a variant with these is NOT complete from its
                # named cards alone. Dropping this field made Gev's 8
                # persist-gated variants read as owned 2-card combos
                # (2026-07-15 correction).
                "requires": [t.get("template", {}).get("name", "")
                             for t in v.get("requires", [])],
                "produces": [p.get("feature", {}).get("name", "")
                             for p in v.get("produces", [])],
                "popularity": v.get("popularity") or 0,
                "legal": v.get("legalities", {}).get("commander", True),
            })
        url = data.get("next")
    return out


def _owned_has(owned_keys, name):
    low = front(name).lower()
    if low in owned_keys:
        return True
    other = low[4:] if low.startswith("the ") else "the " + low
    return other in owned_keys


def combos_for(ctx, cmdr, cache, refresh=False, network=True):
    """{'complete': rows, 'one_away': rows} for combos the commander is IN.
    rows: {'pieces': other-cards, 'missing': unowned, 'produces', 'popularity'}.
    Pieces are checked against ownership only here -- brew_deck later enforces
    CI by resolving pieces against the CI-filtered pool."""
    key = front(cmdr.disp)
    empty = {"complete": [], "one_away": [], "template_gated": [],
             "fetched": False}
    if refresh or key not in cache:
        if not network:
            return empty
        try:
            cache[key] = fetch_variants(cmdr.disp)
        except Exception as e:  # noqa: BLE001 -- a dead API must not kill a sweep
            print(f"  [csb] {key}: fetch failed ({e}) -- skipping combos",
                  file=sys.stderr)
            return empty
    fronts = _the_variants(cmdr.disp)
    complete, one_away, template_gated = [], [], []
    for v in cache[key]:
        if v.get("legal") is False:
            continue
        uses = [u for u in v["uses"] if u]
        if not any(front(u).lower() in fronts for u in uses):
            continue
        others = [u for u in uses if front(u).lower() not in fronts]
        missing = [u for u in others if not _owned_has(ctx.owned_keys, u)]
        requires = [t for t in v.get("requires", []) if t]
        row = {"pieces": others, "missing": missing, "requires": requires,
               "produces": v["produces"], "popularity": v["popularity"]}
        if requires:
            # A template slot may or may not be fillable from the pool —
            # resolving that honestly needs a template->cards engine, so the
            # screen treats these as NOT complete (strict; never optimistic).
            if not missing:
                template_gated.append(row)
        elif not missing:
            complete.append(row)
        elif len(missing) == 1:
            one_away.append(row)
    return {"complete": complete, "one_away": one_away,
            "template_gated": template_gated, "fetched": True}


# ---------------------------------------------------------------------------
# screening score (deck_sim + speed_lab_core)
# ---------------------------------------------------------------------------

def screen_score(brew, combos, trials=2000, seed=17):
    """SCREEN metrics for a brew. Consistency/availability only -- never a
    kill window."""
    import deck_sim as ds
    import speed_lab_core as slc

    index = ds.load_oracle_index()
    lib = []
    for nm, cnt in brew.deck:
        rec = index.get(nm.lower())
        if rec is None:
            continue
        lib.extend([(nm, rec)] * cnt)
    identity = set(brew.ci) - {"C"}

    cons = ds.simulate(lib, identity, turns=7, trials=trials,
                       rng=ds.deck_rng(seed, brew.commander))
    flow = ds.simulate_flow(lib, turns=8, trials=trials,
                            rng=ds.deck_rng(seed + 1, brew.commander),
                            draw_profiles=ds.draw_map(lib))
    lib_names = {nm.lower() for nm, _ in lib}
    ramp_n = len(ds.need_source_set(lib, "ramp") & lib_names)
    draw_n = len(ds.need_source_set(lib, "draw") & lib_names)

    assembly_median = None
    assembly_never = None
    assembly_t10 = None
    if brew.combo_package and combos:
        best = min((r for r in combos if r["pieces"] and not r["missing"]
                    and all(front(p).lower() in lib_names
                            or p.lower() in lib_names for p in r["pieces"])),
                   key=lambda r: (len(r["pieces"]), -r.get("popularity", 0)),
                   default=None)
        if best:
            groups = [{p} for p in best["pieces"]]
            tutor_set = _tutor_names_of(lib)
            tutor_names = {nm for nm, _ in lib if nm.lower() in tutor_set}
            _, with_t = slc.simulate_groups(
                lib, groups, tutor_names, trials=trials,
                rng=ds.deck_rng(seed + 2, brew.commander), turns=13)
            assembly_median = curve_median(with_t)
            assembly_t10 = round(with_t.get(10, 0.0), 1)
            assembly_never = round(100.0 - with_t[13], 1)

    metrics = {
        "keepable_pct": round(cons["keepable_pct"], 1),
        "colors_t4": round(cons["all_colors_by_turn"].get(4, 0.0), 1),
        "mean_dead_turns": round(flow["mean_dead_turns"], 2),
        "hellbent_t8": round(flow["hellbent_by_turn"].get(8, 0.0), 1),
        "ramp_n": ramp_n, "draw_n": draw_n,
        "assembly_median": assembly_median, "assembly_t10": assembly_t10,
        "assembly_never": assembly_never,
        "combos_seeded": brew.combos_seeded,
        "combos_owned": len(combos) if combos else 0,
    }
    metrics["screen_score"], metrics["axes"] = composite(metrics)
    return metrics


def _tutor_names_of(lib):
    import deck_sim as ds
    return ds.need_source_set(lib, "tutor")


# ---------------------------------------------------------------------------
# output
# ---------------------------------------------------------------------------

def write_list(brew, date_tag):
    """Write the brew as a .txt under analysis/autobrew/lists/ -- NEVER under
    decks/ (would enter deck_doctor --all + resolve_deck_arg's glob)."""
    LISTS_DIR.mkdir(parents=True, exist_ok=True)
    path = LISTS_DIR / f"{slugify(brew.commander)}-autobrew-{date_tag}.txt"
    lines = [
        f"# AUTO-BREWER SCREEN CANDIDATE -- not a deck. Generated {date_tag}.",
        f"# Commander: {brew.commander}  [{brew.ci}]",
        "# Screen-grade only: graduate via proposal + clock lab before building.",
        f"1 {brew.commander}",
    ]
    lines += [f"{n} {nm}" for nm, n in brew.deck]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def print_brew(brew, metrics=None):
    print(f"\n=== {brew.commander}  [{brew.ci}] "
          f"-- SCREEN brew, not a deck ===")
    print(f"  themes: {', '.join(brew.themes) or '(none)'}"
          + (f" | tribes: {', '.join(brew.tribes)}" if brew.tribes else ""))
    q = "  ".join(f"{k} {a}/{b}" for k, (a, b) in brew.quota_report.items())
    print(f"  quotas: {q}")
    print(f"  spells {brew.spells} + nonbasic lands {brew.lands} + basics "
          f"{sum(brew.basics.values())} = "
          f"{brew.spells + brew.lands + sum(brew.basics.values())} + commander")
    if brew.combo_package:
        print(f"  combo package ({brew.combos_seeded} combos): "
              + ", ".join(brew.combo_package))
    if brew.gc_hits:
        print(f"  game changers: {', '.join(brew.gc_hits)}")
    for n in brew.notes:
        print(f"  note: {n}")
    if metrics:
        m = metrics
        asm = ("none" if not m["combos_seeded"]
               else f"{m['assembly_t10']}% seen-by-T10")
        print(f"  SCREEN {m['screen_score']}: keep {m['keepable_pct']}% | "
              f"dead {m['mean_dead_turns']} | colors@T4 {m['colors_t4']}% | "
              f"ramp {m['ramp_n']} draw {m['draw_n']} | "
              f"assembly {asm} (pieces SEEN, NOT a kill turn)")


# ---------------------------------------------------------------------------
# dashboard leaderboard page (pure shaping over the two baked artifacts)
# ---------------------------------------------------------------------------

# GENERIC archetype names/glosses keyed by the THEMES labels above. The theme
# itself is already derived from the commander's OWN oracle text by
# theme_profile(); this only puts the pattern into prose, it never asserts what
# any single card does -- so it stays inside the CLAUDE.md "don't describe cards
# from name/memory" rule.
THEME_LABEL = {
    "aristocrats": "Aristocrats", "graveyard": "Graveyard", "tokens": "Tokens",
    "spellslinger": "Spellslinger", "counters": "+1/+1 Counters",
    "lifegain": "Lifegain", "draw-matters": "Draw-Matters", "discard": "Discard",
    "mill": "Mill", "landfall": "Landfall", "artifacts": "Artifacts",
    "enchantments": "Enchantments", "drain": "Drain", "combat": "Combat",
    "etb": "Blink / ETB", "theft": "Theft", "wide": "Go-Wide",
}
THEME_GLOSS = {
    "aristocrats": "sacrifices its own creatures for value and drain",
    "graveyard": "recurs and reanimates out of the graveyard",
    "tokens": "floods the board with tokens and pumps them",
    "spellslinger": "chains and copies instants and sorceries",
    "counters": "grows +1/+1 counters and proliferates",
    "lifegain": "turns lifegain into an engine",
    "draw-matters": "rewards every extra card drawn",
    "discard": "weaponises discard and wheels",
    "mill": "mills libraries as a resource",
    "landfall": "ramps extra lands for landfall payoffs",
    "artifacts": "assembles an artifact engine",
    "enchantments": "builds out an enchantment web",
    "drain": "drains each opponent's life total",
    "combat": "wins through repeated and extra combats",
    "etb": "loops enters-the-battlefield triggers with blink",
    "theft": "steals opponents' permanents",
    "wide": "goes wide and anthems the team",
}

# produced-features that must NOT headline a combo (a stalemate is not a win).
# Exact match, case-folded.
_COMBO_IGNORE = {"draw the game"}

# combo-type buckets, most-lethal first; the FIRST bucket whose needles hit a
# feature wins. CSB's `produces` strings are its own classification -- we only
# bucket them, never invent them.
_COMBO_CATS = [
    ("Instant win",     ("loses the game", "lose the game", "wins the game")),
    ("Infinite damage", ("damage", "burn")),
    ("Infinite drain",  ("lifeloss", "life loss", "loses life", "drain")),
    ("Infinite mill",   ("mill",)),
    ("Infinite tokens", ("creature token", "tokens", "creature")),
    ("Infinite mana",   ("mana",)),
    ("Infinite draw",   ("card draw",)),
]
_COMBO_PRIORITY = {label: i for i, (label, _) in enumerate(_COMBO_CATS)}
_COMBO_PRIORITY["Infinite loop"] = len(_COMBO_CATS)
_COMBO_PRIORITY["Combo engine"] = len(_COMBO_CATS) + 1
_WIN_NEEDLES = ("loses the game", "lose the game", "wins the game")


def _combo_category(features):
    """Bucket a list of CSB produced-features into a short kill-type label."""
    low = [f.lower() for f in features if f.lower() not in _COMBO_IGNORE]
    for label, needles in _COMBO_CATS:
        if any(any(n in f for n in needles) for f in low):
            return label
    if any("infinite" in f for f in low):
        return "Infinite loop"
    return "Combo engine"


def _seeded_combos(commander, package, cache):
    """The owned complete combos the brew actually seeded, reconstructed from
    the commander's CSB cache rows + the brewed combo package. A cache variant
    counts iff it uses the commander, has NO template requirement, and every
    other named piece is in the package -- exactly the seed rule brew_deck used.
    Returns [(other_pieces, produces, popularity)]."""
    fronts = _the_variants(commander)
    pkg = set(package)
    out = []
    for v in cache.get(front(commander), []):
        if v.get("legal") is False:
            continue
        if [t for t in v.get("requires", []) if t]:
            continue
        uses = [u for u in v.get("uses", []) if u]
        if not any(front(u).lower() in fronts for u in uses):
            continue
        others = [u for u in uses if front(u).lower() not in fronts]
        if not others or any(o not in pkg for o in others):
            continue
        produces = [p for p in v.get("produces", []) if p]
        out.append((others, produces, v.get("popularity", 0) or 0))
    return out


def _combo_summary(commander, package, cache):
    """The headline combo for a commander: the most-lethal seeded owned combo
    (Instant-win > damage > drain > ...), popularity then piece-count breaking
    ties. None when nothing reconstructs (e.g. the owned combo's piece was
    off-colour and never entered the package)."""
    seeded = _seeded_combos(commander, package, cache)
    if not seeded:
        return None

    def rank(item):
        others, produces, pop = item
        return (_COMBO_PRIORITY.get(_combo_category(produces), 99), -pop,
                len(others))

    others, produces, pop = min(seeded, key=rank)
    cat = _combo_category(produces)
    cat_needles = dict(_COMBO_CATS).get(cat, ())
    seen, feats = set(), []
    for f in produces:
        if f.lower() not in _COMBO_IGNORE and f not in seen:
            seen.add(f)
            feats.append(f)

    def relevance(f):
        fl = f.lower()
        if any(n in fl for n in _WIN_NEEDLES):
            return 0                       # the actual win, first
        if any(n in fl for n in cat_needles):
            return 1                       # the feature that named the type
        return 2
    feats.sort(key=relevance)
    return {"type": cat, "pieces": [commander] + others,
            "produces": feats[:6], "popularity": pop}


_COLOR_ORDER = "WUBRG"


def _color_pips(ci):
    """CI string ('BGRUW', 'RU', 'C') -> WUBRG-ordered pip letters for the UI."""
    if not ci or ci == "C":
        return ["C"]
    return [c for c in _COLOR_ORDER if c in ci]


def shape_leaderboard(lb, cache):
    """Pure transform: (leaderboard dict, CSB cache dict) -> the dashboard
    Auto-Brewer page payload. Each row gains a playstyle gloss (from the brew's
    themes) and a combo-type summary (from CSB produced-features). No I/O, no
    network -- hermetically testable. Every metric stays SCREEN-grade; assembly
    is P(pieces SEEN), never a kill turn (the note field carries the caveat)."""
    rows = []
    for i, r in enumerate(lb.get("results", []), 1):
        themes = r.get("themes", [])
        tribes = r.get("tribes", [])
        labels = ([f"{tribes[0]} tribal"] if tribes else []) + \
            [THEME_LABEL.get(t, t.title()) for t in themes]
        gloss = "; ".join(THEME_GLOSS[t] for t in themes[:2] if t in THEME_GLOSS)
        gloss = gloss[:1].upper() + gloss[1:] if gloss else ""
        combo = _combo_summary(r["commander"], r.get("combo_package", []), cache)
        rows.append({
            "rank": i,
            "commander": r["commander"],
            "ci": r.get("ci", "C"),
            "colors": _color_pips(r.get("ci", "C")),
            "status": r.get("status", ""),
            "pool": r.get("pool", 0),
            "score": r.get("screen_score"),
            "axes": r.get("axes", {}),
            "keepable": r.get("keepable_pct"),
            "deadTurns": r.get("mean_dead_turns"),
            "colorsT4": r.get("colors_t4"),
            "ramp": r.get("ramp_n"),
            "draw": r.get("draw_n"),
            "assemblyT10": r.get("assembly_t10"),
            "assemblyMedian": r.get("assembly_median"),
            "combosOwned": r.get("combos_owned", 0),
            "combosOneAway": r.get("combos_one_away", 0),
            "combosGated": r.get("combos_template_gated", 0),
            "themes": themes,
            "tribes": tribes,
            "playstyle": " · ".join(labels) if labels else "Midrange / goodstuff",
            "playstyleGloss": gloss,
            "gc": r.get("gc_hits", []),
            "comboType": combo["type"] if combo else None,
            "combo": combo,
            "package": r.get("combo_package", []),
        })

    def fdate(d):
        return f"{d[:4]}-{d[4:6]}-{d[6:]}" if d and len(d) == 8 else (d or "")

    return {
        "date": lb.get("date", ""),
        "generated": fdate(lb.get("date", "")),
        "trials": lb.get("trials"),
        "minPool": lb.get("min_pool"),
        "candidates": len(rows),
        "note": lb.get("note", ""),
        "rows": rows,
    }


def leaderboard_page(lb_path=LEADERBOARD, cache_path=CACHE_FILE):
    """Load the baked sweep + CSB cache and shape the Auto-Brewer page payload.
    Read-only over analysis/autobrew/ -- it NEVER re-runs a sweep (that needs
    the bulk + network). Raises FileNotFoundError with a hint if the sweep has
    not been run."""
    lb_path, cache_path = Path(lb_path), Path(cache_path)
    if not lb_path.exists():
        raise FileNotFoundError(
            f"{lb_path} not found -- run `python scripts/auto_brewer.py sweep`")
    lb = json.loads(lb_path.read_text(encoding="utf-8"))
    cache = (json.loads(cache_path.read_text(encoding="utf-8"))
             if cache_path.exists() else {})
    return shape_leaderboard(lb, cache)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def cmd_census(args):
    ctx = load_context()
    rows = census(ctx)
    cache = load_cache()
    shown = 0
    print(f"{'commander':<42} {'ci':<6} {'pool':>5} {'status':<7} combos(cached)")
    for pc, st, n in rows:
        if n < args.min_pool:
            continue
        if not args.all_statuses and st != "NEW":
            continue
        c = ""
        key = front(pc.disp)
        if key in cache:
            r = combos_for(ctx, pc, cache, network=False)
            c = f"{len(r['complete'])} owned / {len(r['one_away'])} 1-away"
        ci = "".join(sorted(pc.ci)) or "C"
        print(f"{pc.disp[:42]:<42} {ci:<6} {n:>5} {st:<7} {c}")
        shown += 1
    print(f"\n{shown} candidates shown "
          f"({len(rows)} owned commander candidates total; "
          f"--min-pool {args.min_pool}"
          + ("" if args.all_statuses else "; NEW only, --all-statuses to widen")
          + ")")


def _find_commander(ctx, name):
    want = _the_variants(name)
    for pc in ctx.pool.values():
        if pc.is_cmdr and (_the_variants(pc.disp) & want):
            return pc
    sys.exit(f"ERROR: '{name}' not found among owned commander candidates "
             "(check spelling / ownership; reskins resolve automatically)")


def cmd_brew(args):
    ctx = load_context()
    pc = _find_commander(ctx, args.commander)
    cache = load_cache()
    rows = ({"complete": [], "one_away": [], "template_gated": [],
             "fetched": False}
            if args.no_combos else
            combos_for(ctx, pc, cache, refresh=args.refresh_combos))
    if rows.get("fetched"):
        save_cache(cache)
    brew = brew_deck(pc, ci_pool(ctx, pc), rows["complete"])
    metrics = screen_score(brew, rows["complete"], trials=args.trials)
    print_brew(brew, metrics)
    if rows["template_gated"]:
        tg = sorted(rows["template_gated"],
                    key=lambda r: -r.get("popularity", 0))[:5]
        print(f"  template-gated ({len(rows['template_gated'])} -- pieces "
              "owned but a generic slot is unverified):")
        for r in tg:
            print(f"    needs [{' & '.join(r['requires'])}] with "
                  + (" + ".join(r["pieces"]) or "the commander alone"))
    if rows["one_away"]:
        best = sorted(rows["one_away"],
                      key=lambda r: -r.get("popularity", 0))[:5]
        print("  top 1-away upgrades (unowned piece):")
        for r in best:
            print(f"    buy {r['missing'][0]} -> "
                  + " + ".join(r["pieces"]))
    if args.write:
        p = write_list(brew, args.date)
        print(f"  wrote {p.relative_to(ROOT)}")


def cmd_sweep(args):
    ctx = load_context()
    rows = census(ctx)
    todo = [(pc, st, n) for pc, st, n in rows
            if n >= args.min_pool
            and (st == "NEW" or (args.include_known and st == "KNOWN"))]
    if args.limit:
        todo = todo[:args.limit]
    cache = load_cache()
    print(f"Sweeping {len(todo)} candidates "
          f"(min-pool {args.min_pool}, trials {args.trials}, "
          f"combos {'off' if args.no_combos else 'on'})", flush=True)
    results = []
    for i, (pc, st, n) in enumerate(todo, 1):
        rows_c = ({"complete": [], "one_away": [], "template_gated": [],
                   "fetched": False}
                  if args.no_combos else
                  combos_for(ctx, pc, cache, refresh=args.refresh_combos))
        brew = brew_deck(pc, ci_pool(ctx, pc), rows_c["complete"])
        metrics = screen_score(brew, rows_c["complete"], trials=args.trials)
        results.append({
            "commander": pc.disp, "ci": brew.ci, "status": st, "pool": n,
            "combos_owned": len(rows_c["complete"]),
            "combos_one_away": len(rows_c["one_away"]),
            "combos_template_gated": len(rows_c["template_gated"]),
            "themes": brew.themes, "tribes": brew.tribes,
            "quotas": {k: list(v) for k, v in brew.quota_report.items()},
            "combo_package": brew.combo_package, "gc_hits": brew.gc_hits,
            **{k: metrics[k] for k in
               ("screen_score", "axes", "keepable_pct", "mean_dead_turns",
                "colors_t4", "ramp_n", "draw_n", "assembly_median",
                "assembly_t10", "assembly_never", "combos_seeded")},
        })
        t10 = metrics["assembly_t10"]
        print(f"[{i}/{len(todo)}] {pc.disp[:38]:<38} "
              f"SCREEN {metrics['screen_score']:>5}  "
              f"combos {len(rows_c['complete']):>3}  "
              f"asm@T10 {(str(t10) + '%') if t10 is not None else '-':>6}",
              flush=True)
        if not args.no_combos and i % 10 == 0:
            save_cache(cache)  # crash-safe: the fetches are the slow part
    if not args.no_combos:
        save_cache(cache)

    results.sort(key=lambda r: -r["screen_score"])
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    LEADERBOARD.write_text(
        json.dumps({"date": args.date, "trials": args.trials,
                    "min_pool": args.min_pool,
                    "note": "SCREEN-grade consistency/availability metrics. "
                            "assembly_median = pieces SEEN by turn, not a "
                            "kill window. Winners graduate via proposal + "
                            "clock lab.",
                    "results": results}, indent=1),
        encoding="utf-8")
    print(f"\nwrote {LEADERBOARD.relative_to(ROOT)}")

    print(f"\n{'#':>3} {'commander':<40} {'ci':<6} {'SCREEN':>6} "
          f"{'combos':>6} {'asm@T10':>7} {'keep%':>5} {'dead':>5}")
    for i, r in enumerate(results[:args.top], 1):
        t10 = r["assembly_t10"]
        print(f"{i:>3} {r['commander'][:40]:<40} {r['ci']:<6} "
              f"{r['screen_score']:>6} {r['combos_owned']:>6} "
              f"{(str(t10) + '%') if t10 is not None else '-':>7} "
              f"{r['keepable_pct']:>5} {r['mean_dead_turns']:>5}")
    if args.write:
        for r in results[:args.top]:
            pc = _find_commander(ctx, r["commander"])
            rows_c = combos_for(ctx, pc, cache, network=False)
            brew = brew_deck(pc, ci_pool(ctx, pc), rows_c["complete"])
            p = write_list(brew, args.date)
            print(f"  wrote {p.relative_to(ROOT)}")


def main(argv=None):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # noqa: BLE001 -- non-console streams
        pass
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("census", help="owned commander candidates")
    p.add_argument("--min-pool", type=int, default=150)
    p.add_argument("--all-statuses", action="store_true")
    p.set_defaults(fn=cmd_census)

    p = sub.add_parser("brew", help="brew + score one commander")
    p.add_argument("commander")
    p.add_argument("--no-combos", action="store_true")
    p.add_argument("--refresh-combos", action="store_true")
    p.add_argument("--trials", type=int, default=4000)
    p.add_argument("--write", action="store_true")
    p.set_defaults(fn=cmd_brew)

    p = sub.add_parser("sweep", help="brew + score every candidate")
    p.add_argument("--min-pool", type=int, default=150)
    p.add_argument("--limit", type=int, default=0)
    p.add_argument("--top", type=int, default=12)
    p.add_argument("--trials", type=int, default=2000)
    p.add_argument("--no-combos", action="store_true")
    p.add_argument("--refresh-combos", action="store_true")
    p.add_argument("--include-known", action="store_true")
    p.add_argument("--write", action="store_true")
    p.set_defaults(fn=cmd_sweep)

    args = ap.parse_args(argv)
    import datetime as _dt
    args.date = _dt.date.today().strftime("%Y%m%d")
    args.fn(args)


if __name__ == "__main__":
    main()
