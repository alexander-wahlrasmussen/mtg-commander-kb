#!/usr/bin/env python3
"""ramp_audit.py — does each deck's RAMP match its plan? (BDD "You're Probably Ramping Wrong")

Two questions, from reference_bdd_ramp_framework (youtube.com/watch?v=upqHyQqN3WU):

  (a) BAND — count mana sources against the fair-deck band: ~12 ramp + ~36-38 lands ~= ~48-50
      mana sources. Flags the two failure modes BDD names: UNDER-resourced ("32 lands + a
      handful of ramp -> land screw every second game") and OVER-ramped (his Pantlaza case:
      ~20 ramp sources, no room for payoffs). The 12 is calibrated to FAIR B2-B3 decks; our
      combo decks correctly run more burst/free mana, so the band is a sanity check, not a law.

  (b) TYPE vs ROLE — BDD's core lesson is that ramp TYPE must match the game plan:
      one-explosive-turn combo decks want BURST (rituals, treasures: "a treasure is as good as
      a land"); decks that deploy a threat every turn want REPEATABLE (rocks/dorks/land-ramp),
      not one-shot rituals. We already classify decks by kill SHAPE via the clock labs
      (analysis/pod_gauntlet_clocks.json): a one-shot combo closes the table ~at once (small
      decap->table gap); a deploy-each-turn deck focus-kills then grinds (large gap). So we read
      each deck's burst/repeatable split against its measured clock shape and flag mismatches.

This is a COMPOSITION audit, not a rules engine and not a kill-turn claim. Every classification
is derived from oracle text + type_line + produced_mana (collection/oracle-cards.json) — no card
NAME pattern-matching (CLAUDE.md hard rule). Run with --cards to dump the per-card calls so the
classifier itself can be eyeballed against the oracle text it read.

Reuses deck_sim for decklist parsing / reskin-alias / commander resolution (one source of truth),
but builds its own ORACLE-TEXT index because deck_sim's record drops oracle_text.

Usage:
    python scripts/ramp_audit.py                 # roster table + flags
    python scripts/ramp_audit.py --cards         # + per-deck classified ramp cards (verify here)
    python scripts/ramp_audit.py --deck eldrazi  # one deck (fuzzy)
    python scripts/ramp_audit.py --considering   # also the candidate/considering builds
    python scripts/ramp_audit.py --json out.json
"""
import argparse
import importlib.util as _il
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ORACLE = ROOT / "collection" / "oracle-cards.json"
CLOCKS = ROOT / "analysis" / "pod_gauntlet_clocks.json"


def _load(name):
    spec = _il.spec_from_file_location(name, Path(__file__).parent / f"{name}.py")
    mod = _il.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


deck_sim = _load("deck_sim")          # parse_deck / is_land / is_pure_land / load_reskin_aliases
registry = _load("deck_registry")     # the roster (active) + EXTRA (considering)

# ---- the fair-deck band (BDD), as constants so the thresholds are one place -------------
# BDD's target is ~12 ramp + ~36-38 lands ~= ~48-50 mana sources. We flag the SOURCE total
# (the band that catches both his failure modes); ramp count itself is reported, not flagged,
# because our combo decks correctly run more than 12 (he exempts high-power/fringe-cEDH).
SRC_LO, SRC_HI = 44, 52              # ~48-50 mana sources (lands + mana-ramp)
TOPEND_CMC = 6                       # "ramp toward what?" — count of heavy payoffs (cmc>=this)

# ---- role from clock shape (judgment, documented) ----------------------------------------
# COMBO    = one-shot kill, closes the table ~at once (small decap->table gap, fast) -> burst OK
# GRIND    = slow/never table close                                                  -> repeatable
# INCREMENTAL = focus-kill then grind (large gap)                                     -> repeatable
COMBO_TABLE_MAX, COMBO_GAP_MAX = 8, 1
GRIND_TABLE_MIN, GRIND_NEVER_MIN = 11, 25
INCR_GAP_MIN = 2


# ---------------------------------------------------------------------------
# Oracle index WITH oracle text (deck_sim's index drops it)
# ---------------------------------------------------------------------------
def load_rich_index():
    if not ORACLE.exists():
        sys.exit(f"ERROR: {ORACLE} not found — run scripts/update_scryfall_data.py first "
                 f"(it is gitignored; in a worktree, link the main repo's copy).")
    print("Loading card data (large file, a few seconds)...", file=sys.stderr)
    cards = json.loads(ORACLE.read_text(encoding="utf-8"))
    index = {}
    for c in cards:
        faces = c.get("card_faces", [])
        face_types = [f.get("type_line", "") for f in faces] or [c.get("type_line", "")]
        text = c.get("oracle_text", "")
        if not text and faces:
            text = " // ".join(f.get("oracle_text", "") for f in faces)
        # produced_mana can live per-face; union them too (Scryfall often only sets the top level)
        prod = set(c.get("produced_mana", []) or [])
        for f in faces:
            prod.update(f.get("produced_mana", []) or [])
        record = {
            "name": c.get("name", ""),
            "cmc": c.get("cmc", 0.0),
            "type_line": c.get("type_line", ""),
            "face_types": face_types,
            "oracle_text": text,
            "produced_mana": tuple(prod),
            "color_identity": tuple(c.get("color_identity", [])),
        }
        names = [c.get("name", "")] + [f["name"] for f in faces if f.get("name")]
        junk = c.get("layout", "normal") in {"art_series", "double_faced_token", "token"}
        for n in names:
            key = n.lower()
            if key and (key not in index or not junk):
                index[key] = record
    return index


# ---------------------------------------------------------------------------
# Classification — reads the card (oracle text), never the name
# ---------------------------------------------------------------------------
_MANA_ADD = re.compile(r"add\b[^.]*?(\{[wubrgcsx0-9]|mana\b)", re.I)
BASIC_WORDS = ("forest", "island", "swamp", "mountain", "plains", "basic land", "gate", "land")


def _lines(text):
    """Ability lines, lowercased — split on reminder-stripped newlines and face separators."""
    text = re.sub(r"\([^)]*\)", "", text)              # drop reminder text
    parts = re.split(r"\n|//", text)
    return [p.strip().lower() for p in parts if p.strip()]


def _adds_mana(line):
    return bool(_MANA_ADD.search(line))


def is_permanent(rec):
    t = rec["type_line"].lower()
    return any(w in t for w in ("artifact", "creature", "enchantment", "planeswalker")) and "land" not in t


def is_instant_sorcery(rec):
    t = rec["type_line"].lower()
    return "instant" in t or "sorcery" in t


def makes_treasure(text):
    t = text.lower()
    return ("create" in t and ("treasure" in t or "gold token" in t))


def is_land_ramp(rec):
    """Searches/puts LANDS into play, or grants extra land drops (repeatable land acceleration)."""
    t = rec["oracle_text"].lower()
    if "play an additional land" in t:
        return True
    if "put a land card from your hand onto the battlefield" in t:
        return True
    if "search your library" in t and "onto the battlefield" in t and any(w in t for w in BASIC_WORDS):
        return True
    return False


def is_cost_reducer(rec):
    t = rec["oracle_text"].lower()
    if "this spell costs" in t:          # self-reducer = a cheap payoff (Ghalta), not ramp
        return False
    return "less to cast" in t            # reduces OTHER spells (Urza's Incubator / Electromancer)


def classify(rec):
    """Return (category, bucket) or (None, None). Categories: treasure/ritual/land_ramp/rock/
    dork/cost_reducer. Buckets: burst (one-shot) / repeatable / enabler."""
    if rec.get("type_line", "").upper() == "UNKNOWN":
        return None, None
    if deck_sim.is_land(rec):
        return None, None
    text = rec["oracle_text"]

    # 1) Treasure / token mana. Spell or one-shot ETB = burst; ongoing trigger engine = repeatable.
    if makes_treasure(text):
        if is_instant_sorcery(rec):
            return "treasure", "burst"
        t = text.lower()
        ongoing = "whenever" in t or "at the beginning" in t   # Tireless/Smothering vs ETB Dockside
        return "treasure", ("repeatable" if ongoing else "burst")

    # 2) Land ramp (Cultivate / Three Visits / Exploration / Burgeoning) — repeatable acceleration.
    if is_land_ramp(rec):
        return "land_ramp", "repeatable"

    # 3) Ritual — instant/sorcery that adds mana (one-shot burst). A counterspell that happens to
    #    refund mana (Mana Drain) is interaction, not ramp — exclude it.
    if is_instant_sorcery(rec):
        t = text.lower()
        if "counter target" in t or "counter that spell" in t:
            return None, None
        if any(_adds_mana(ln) for ln in _lines(text)):
            return "ritual", "burst"
        return None, None

    # 4) Mana permanent — rock (artifact) / dork (creature). Sac-to-add = burst (Lotus Petal class);
    #    a non-sac {T}: Add line = repeatable. produced_mana is the structured backstop.
    if is_permanent(rec):
        is_creature = "creature" in rec["type_line"].lower()
        tap_repeat = sac_burst = False
        for ln in _lines(text):
            if not _adds_mana(ln):
                continue
            if "sacrifice this" in ln and "{t}" in ln:
                sac_burst = True
            elif "{t}" in ln or "creatures you control" in ln or "lands you control" in ln:
                tap_repeat = True
        if tap_repeat:
            return ("dork" if is_creature else "rock"), "repeatable"
        if sac_burst:
            return ("dork" if is_creature else "rock"), "burst"
        # structured backstop: produces mana but the text heuristics missed how
        if rec["produced_mana"] and any(_adds_mana(ln) for ln in _lines(text)):
            return ("dork" if is_creature else "rock"), "repeatable"

    # 5) Cost reducer — ramp-adjacent (BDD counts Urza's Incubator). Static enabler, not a source.
    if is_cost_reducer(rec):
        return "cost_reducer", "enabler"

    return None, None


# ---------------------------------------------------------------------------
# Clock shape (role) from the harvested lab clocks
# ---------------------------------------------------------------------------
def _t(s):
    m = re.search(r"\d+", s or "")
    return int(m.group()) if m else None


def load_roles():
    if not CLOCKS.exists():
        return {}
    data = json.loads(CLOCKS.read_text(encoding="utf-8"))
    roles = {}
    for slug, d in data.items():
        decap, table = _t(d["med"][0]), _t(d["med"][1])
        never_t = d["never"][1]
        gap = (table - decap) if (decap is not None and table is not None) else None
        if table is not None and table <= COMBO_TABLE_MAX and (gap is not None and gap <= COMBO_GAP_MAX):
            role = "COMBO"
        elif (table is not None and table >= GRIND_TABLE_MIN) or never_t >= GRIND_NEVER_MIN:
            role = "GRIND"
        elif gap is not None and gap >= INCR_GAP_MIN:
            role = "INCR"
        else:
            role = "MID"
        roles[slug] = {"role": role, "decap": decap, "table": table, "gap": gap, "never": never_t}
    return roles


# ---------------------------------------------------------------------------
# Per-deck audit
# ---------------------------------------------------------------------------
def resolve_any(stem):
    """Newest decklist for a stem, looking in decks/ then decks/considering/ (registry.resolve_deck
    only globs the top level, where the active roster lives; candidate builds sit in considering/)."""
    for d in (ROOT / "decks", ROOT / "decks" / "considering"):
        hits = sorted(d.glob(f"{stem}-*.txt"))
        if hits:
            return hits[-1]
    return None


def audit_deck(stem, index, aliases):
    path = resolve_any(stem)
    if path is None:
        return None
    library, commander, diag = deck_sim.parse_deck(path, index, aliases)

    pure_lands = flex_lands = 0
    cats = {k: 0 for k in ("rock", "dork", "land_ramp", "ritual", "treasure", "cost_reducer")}
    burst = repeat = 0
    topend = 0
    nonland_cmcs = []
    cards = []          # (name, cmc, category, bucket) for --cards
    for name, rec in library:
        if deck_sim.is_land(rec):
            if deck_sim.is_pure_land(rec):
                pure_lands += 1
            else:
                flex_lands += 1
            continue
        cmc = rec.get("cmc", 0.0)
        nonland_cmcs.append(cmc)
        if cmc >= TOPEND_CMC:
            topend += 1
        cat, bucket = classify(rec)
        if cat:
            cats[cat] += 1
            if bucket == "burst":
                burst += 1
            elif bucket == "repeatable":
                repeat += 1
            cards.append((name, cmc, cat, bucket))

    n_ramp = sum(cats.values())
    n_ramp_mana = n_ramp - cats["cost_reducer"]            # cost reducers aren't mana sources
    # MDFC flex lands ARE mana sources (playable as a land), so they count toward the total and
    # the land band — excluding them falsely under-counts flex-heavy decks (e.g. Lightning War).
    n_lands = pure_lands + flex_lands
    n_sources = n_lands + n_ramp_mana
    avg_cmc = sum(nonland_cmcs) / len(nonland_cmcs) if nonland_cmcs else 0.0
    return {
        "stem": stem, "name": deck_sim.DISPLAY.get(diag["deck_key"], path.stem),
        "deck_key": diag["deck_key"], "commander": commander, "file": path.name,
        "pure_lands": pure_lands, "flex_lands": flex_lands, "n_lands": n_lands,
        "cats": cats, "n_ramp": n_ramp, "burst": burst, "repeat": repeat,
        "n_sources": n_sources, "avg_cmc": round(avg_cmc, 2), "topend": topend,
        "cmdr_cmc": index.get((commander or "").lower(), {}).get("cmc"),
        "unresolved": diag["unresolved"], "cards": sorted(cards, key=lambda c: (-c[1], c[0])),
    }


def flags_for(a, role):
    """High-confidence mechanical flags (source band + type/role mismatch). The 'ramp toward
    what' question (topend payoffs) is a DATA column, not an auto-flag — the cmc>=6 proxy can't
    see a combo/X-spell/engine target, so it cried wolf on storm decks; interpret it by hand."""
    out = []
    if a["n_sources"] < SRC_LO:
        out.append(f"UNDER-resourced: {a['n_sources']} mana sources (<{SRC_LO}) — BDD land-screw risk")
    if a["n_sources"] > SRC_HI:
        out.append(f"OVER-resourced: {a['n_sources']} mana sources (>{SRC_HI}) — verify the payoff "
                   f"profile justifies it ({a['topend']} payoffs cmc>={TOPEND_CMC}, avg {a['avg_cmc']})")
    r = role.get("role") if role else None
    # BDD's core rule: ramp TYPE must match the kill shape. Mismatches (high-confidence):
    if r in ("GRIND", "INCR") and a["n_ramp"] >= 6 and a["burst"] > a["repeat"]:
        out.append(f"TYPE/ROLE: {r} deck (deploys each turn) but ramp is mostly BURST "
                   f"({a['burst']} burst vs {a['repeat']} repeatable) — BDD: prefer repeatable")
    if r == "COMBO" and a["n_ramp"] >= 8 and a["burst"] == 0:
        out.append("TYPE/ROLE: one-shot COMBO clock but ZERO burst ramp — BDD: a treasure is as "
                   "good as a land for a one-turn kill; consider rituals/treasure")
    return out


# ---------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--deck", help="Fuzzy stem filter")
    ap.add_argument("--cards", action="store_true", help="Dump classified ramp cards per deck")
    ap.add_argument("--considering", action="store_true", help="Also audit EXTRA (candidate) builds")
    ap.add_argument("--summary", action="store_true",
                    help="Emit a paste-ready one-line ramp descriptor per deck (for the Summaries)")
    ap.add_argument("--json", metavar="PATH")
    args = ap.parse_args()

    index = load_rich_index()
    aliases = deck_sim.load_reskin_aliases()
    roles = load_roles()

    stems = [(s, d["stem"]) for s, d in registry.DECKS.items()]
    if args.considering:
        stems += [(st, st) for st in registry.EXTRA_COMMANDERS]
    if args.deck:
        stems = [(s, st) for s, st in stems if args.deck.lower() in st.lower()]
        if not stems:
            sys.exit(f"No deck stem matches '{args.deck}'")

    audits = []
    for slug, stem in stems:
        a = audit_deck(stem, index, aliases)
        if a:
            a["slug"] = slug
            audits.append(a)

    # --- paste-ready Summary line (the clock-annotation analog) ---
    if args.summary:
        for a in audits:
            band = ("in band" if SRC_LO <= a["n_sources"] <= SRC_HI else
                    f"over band, {a['topend']} payoffs cmc>={TOPEND_CMC}" if a["n_sources"] > SRC_HI
                    else "under band")
            print(f"{a['name']}\tRamp: {a['n_ramp']} sources ({a['burst']} burst / {a['repeat']} "
                  f"repeatable) · {a['n_sources']} mana sources, {a['n_lands']} land · {band} "
                  f"(`ramp_audit.py` 2026-06-21)")
        return

    # --- table ---
    print(f"\n{'='*118}")
    print("RAMP AUDIT — band: ~12 ramp / ~36-38 lands / ~48-50 sources (BDD, fair-deck calibration)")
    print(f"{'='*118}")
    print(f"  {'deck':22}{'role':>5}{'lnd':>4}{'flx':>4}{'rock':>5}{'dork':>5}{'lrmp':>5}"
          f"{'rit':>4}{'tre':>4}{'cr':>3}{'RAMP':>5}{'b/r':>7}{'src':>5}{'top':>4}{'avgC':>6}")
    for a in audits:
        c = a["cats"]
        role = roles.get(a["slug"], {})
        rl = role.get("role", "—")
        print(f"  {a['name'][:21]:22}{rl:>5}{a['pure_lands']:>4}{a['flex_lands']:>4}"
              f"{c['rock']:>5}{c['dork']:>5}{c['land_ramp']:>5}{c['ritual']:>4}{c['treasure']:>4}"
              f"{c['cost_reducer']:>3}{a['n_ramp']:>5}{(str(a['burst'])+'/'+str(a['repeat'])):>7}"
              f"{a['n_sources']:>5}{a['topend']:>4}{a['avg_cmc']:>6}")
    print("\n  role: COMBO=one-shot table (burst OK) · GRIND/INCR=deploy each turn (repeatable) · "
          "MID=mixed.  b/r = burst/repeatable.  top = nonland payoffs cmc>=6.")

    # --- flags ---
    print(f"\n{'-'*118}\nFLAGS\n{'-'*118}")
    any_flag = False
    for a in audits:
        fl = flags_for(a, roles.get(a["slug"], {}))
        if a["unresolved"]:
            fl.append(f"{len(a['unresolved'])} unresolved card(s): {', '.join(a['unresolved'][:4])}")
        if fl:
            any_flag = True
            print(f"\n  {a['name']}  [{roles.get(a['slug'], {}).get('role', '—')}]")
            for f in fl:
                print(f"     • {f}")
    if not any_flag:
        print("  (none)")

    # --- per-card dump (verify the classifier here) ---
    if args.cards:
        print(f"\n{'='*118}\nCLASSIFIED RAMP CARDS (verify against oracle text)\n{'='*118}")
        for a in audits:
            print(f"\n  {a['name']}  ({a['n_ramp']} ramp · {a['burst']} burst / {a['repeat']} repeatable)")
            for name, cmc, cat, bucket in a["cards"]:
                print(f"     {cmc:>4.0f}  {cat:<12}{bucket:<11}{name}")

    if args.json:
        Path(args.json).write_text(json.dumps(
            [{**a, "role": roles.get(a["slug"], {})} for a in audits], indent=2), encoding="utf-8")
        print(f"\nWrote {args.json}", file=sys.stderr)


if __name__ == "__main__":
    main()
