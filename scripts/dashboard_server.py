#!/usr/bin/env python3
"""dashboard_server.py — a fun, visual, interactive front-end for the gauntlet stack.

A zero-dependency local web app (stdlib http.server) that drives the EXISTING sim
engine. It is a thin fourth consumer of the same functions pod_championship and
self_meta_lab already import — it does NOT reimplement any sim. It calls
pod_gauntlet / self_meta_lab / pod_championship functions directly and returns
their numbers as JSON, so the browser charts the same curves the writeups cite.

  GET /                     -> ui/dist/index.html (the React SPA; run `npm run build` in ui/)
  GET /api/clocks           -> harvested decap/table CDFs per deck (for the Labs tab)
  GET /api/gauntlet?...     -> P(beat the T6-7 pod) per deck (run_default, parameterised)
  GET /api/championship?... -> the roster bracket (pod_championship, parameterised)
  GET /api/tierlist?...      -> the Definitive Tier List v2 composite (tier_list, parameterised)

Content endpoints (kb_content — KB markdown / CSV / Scryfall, not the sim):
  GET /api/roster           -> active roster (Deck_Index ⋈ registry ⋈ clocks ⋈ GC)
  GET /api/home             -> dashboard hub (roster KPIs + a default gauntlet/championship)
  GET /api/wishlist         -> Build & Swap Tracker (builds / swaps / cheap unlocks)
  GET /api/collection       -> owned cards (Moxfield CSV ⋈ Scryfall) + facet counts
  GET /api/deck?slug=       -> one deck's Tale-of-the-Tape page payload

Knobs map 1:1 to the CLI flags:
  gauntlet:     a (Abolisher P-out), pod (fast|base|slow), strict (decap|table), trials
  championship: trials, season_trials, t_grind, swapped

DISCIPLINE (inherited, surfaced in the UI footer): clock curves are UNBLOCKED
goldfish ceilings; disruption availability != effectiveness; the durability
tiebreak and T_grind are judgment. Trust the RANKING and the shapes, not the
second decimal. This is a viewer for the lab stack, not a new model.

Launch:  cd ui && npm run build        (once, to build the React front-end)
         python scripts/dashboard_server.py   (then open http://127.0.0.1:8765)
"""
import argparse
import importlib.util
import json
import random
import socket
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from types import SimpleNamespace
from urllib.parse import urlparse, parse_qs

ROOT = Path(__file__).resolve().parent.parent
DASHBOARD_DIR = ROOT / "ui" / "dist"     # the built React app (run `npm run build` in ui/)
DEFAULT_HOST, DEFAULT_PORT = "127.0.0.1", 8765

for _s in (sys.stdout, sys.stderr):
    if hasattr(_s, "reconfigure"):
        try:
            _s.reconfigure(encoding="utf-8", errors="replace")
        except (ValueError, OSError):
            pass


def _load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# Load the championship LAST so we reuse its already-loaded sm/pg instances — one
# module graph, identical to how the CLI tools chain (championship -> self_meta -> gauntlet).
pc = _load("pod_championship")
sm = pc.sm                                   # self_meta_lab
pg = pc.pg                                   # pod_gauntlet  (clocks, build_cdf, simulate, ...)
kb = _load("kb_content")                     # KB content (roster / decks / collection / wishlist)
tl = _load("tier_list")                       # the v2 tier-list composite (reuses pg/sm/im)

CONTENT_TYPES = {
    ".html": "text/html; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".js": "application/javascript; charset=utf-8",
    ".mjs": "application/javascript; charset=utf-8",
    ".json": "application/json; charset=utf-8",
    ".svg": "image/svg+xml",
    ".png": "image/png",
    ".ico": "image/x-icon",
    ".woff": "font/woff",
    ".woff2": "font/woff2",
    ".ttf": "font/ttf",
    ".webmanifest": "application/manifest+json",
    ".map": "application/json",
}


# --- engine wrappers (return plain JSON-able dicts) -------------------------
def compute_clocks():
    """The harvested decap/table CDFs per deck — the raw material the Labs tab overlays."""
    C = pg.merged_clocks()
    decks = [dict(slug=s, name=c["name"], score=c.get("score"),
                  grid=c["grid"], decap=c["decap"], table=c["table"],
                  med=c["med"], never=c["never"], src=c.get("src", ""))
             for s, c in C.items()]
    return dict(horizon=pg.HORIZON, decks=decks)


def compute_gauntlet(a, pod, strict, trials, seed):
    """Mirror of pod_gauntlet.run_default, parameterised for the slider UI."""
    rng = random.Random(seed)
    kargs = SimpleNamespace(pod_fast=(pod == "fast"), pod_slow=(pod == "slow"))
    kdist = pg.pod_kdist(kargs)
    which = "table" if strict else "decap"
    C = pg.merged_clocks()
    rows = []
    for slug, c in C.items():
        F = pg.build_cdf(c["grid"], c[which])
        pr = pg.pure_race(F, kdist)
        win, _lose, grind = pg.simulate(slug, F, a, kdist, trials, rng)
        Db = pg.disruption(slug, a, 7)
        band = [pg.simulate(slug, F, aa, kdist, max(1, trials // 2), rng)[0]
                for aa in pg.A_SWEEP]
        rows.append(dict(slug=slug, name=c["name"], score=c.get("score"),
                         decap_med=c["med"][0], table_med=c["med"][1],
                         pure=pr, disruption=Db, win=win, grind=grind,
                         band=band, measured=(slug in pg.MEASURED)))
    rows.sort(key=lambda r: -r["win"])
    return dict(
        params=dict(a=a, pod=pod, strict=strict, trials=trials,
                    which=which,
                    kdist={str(k): v for k, v in sorted(kdist.items())},
                    a_sweep=pg.A_SWEEP),
        rows=rows)


def compute_lock_sweep(a, r, strict, trials, pod, seed):
    """Deck × lock P(win)-lift matrix via pod_gauntlet.lock_sweep_rows (shared with the CLI)."""
    rows, meta = pg.lock_sweep_rows(a, r, strict, trials, seed,
                                    pod_fast=(pod == "fast"), pod_slow=(pod == "slow"))
    return dict(
        params=dict(a=a, r=r, strict=strict, trials=meta["trials"], pod=pod, which=meta["which"]),
        locks=meta["locks"], abbr=meta["abbr"], rows=rows)


def _champ_draw(seeds, seedmap, names, tcdf, dura, t_grind, trials, changed, draw_seed):
    """One pot-based random draw + playoffs -> a single bracket dict. Reproducible from
    `draw_seed` (the draw rng also drives the playoff sims so a draw is self-contained)."""
    rng = random.Random(draw_seed)
    groups = pc.draw_groups(seeds, rng)

    group_out, winners = [], []
    for gi, pod in enumerate(groups):
        pod = sorted(pod, key=lambda s: seedmap[s])
        shares = pc.pod_shares(pod, tcdf, dura, t_grind, trials, rng)
        ranked = sorted(pod, key=lambda s: -shares[s])
        winners.append(ranked[0])
        group_out.append(dict(pod=chr(65 + gi), seats=[
            dict(slug=s, name=names[s], seed=seedmap[s], share=shares[s],
                 advances=(s == ranked[0])) for s in ranked]))

    final = sorted(winners, key=lambda s: seedmap[s])
    fshares = pc.pod_shares(final, tcdf, dura, t_grind, trials, rng)
    franked = sorted(final, key=lambda s: -fshares[s])
    champ = franked[0]
    medals = ["gold", "silver", "bronze", ""]
    final_out = [dict(slug=s, name=names[s], seed=seedmap[s],
                      share=fshares[s], medal=medals[i])
                 for i, s in enumerate(franked)]

    runner = franked[1]
    cinderella = max(winners, key=lambda s: seedmap[s])
    return dict(
        draw_seed=draw_seed, groups=group_out, final=final_out,
        champion=dict(slug=champ, name=names[champ], seed=seedmap[champ]),
        notes=dict(
            runner_up=dict(slug=runner, name=names[runner], seed=seedmap[runner]),
            upset=(seedmap[champ] > 1),
            cinderella=(dict(slug=cinderella, name=names[cinderella],
                             seed=seedmap[cinderella]) if seedmap[cinderella] >= 9 else None),
            changed=[names[s] for s in changed]))


def compute_championship(trials, season_trials, t_grind, swapped, seed,
                         draw_seed=None, n_draws=1):
    """Mirror of pod_championship.main as structured JSON. The regular season (seeded by
    `seed`) is deterministic and computed once; the group stage is a pot-based RANDOM draw,
    so this returns `n_draws` independent draws sharing that season. `draw_seed` pins the
    first draw (subsequent draws derive from it); omit it for a fresh random bracket."""
    season_rng = random.Random(seed)
    C = pg.merged_clocks()
    slugs = [s for s in sm.dl.ROSTER if s in C]
    names = {s: C[s]["name"] for s in slugs}
    defense = sm.defense_counts()
    tcdf, dura, disp, changed = pc.swapped_clocks(slugs, C, defense, swapped)

    seeds, pwin = pc.seed_field(slugs, tcdf, dura, t_grind, season_trials, season_rng)
    seedmap = {s: i + 1 for i, s in enumerate(seeds)}

    season = [dict(seed=i + 1, slug=s, name=names[s], table_med=disp[s][0],
                   never=disp[s][1], dura=round(dura[s], 3), pwin=pwin[s],
                   swap=(s in changed))
              for i, s in enumerate(seeds)]

    base = draw_seed if draw_seed is not None else random.randrange(1 << 30)
    draws = [_champ_draw(seeds, seedmap, names, tcdf, dura, t_grind, trials, changed,
                         base + i)
             for i in range(max(1, n_draws))]

    return dict(
        params=dict(trials=trials, season_trials=season_trials,
                    t_grind=t_grind, swapped=swapped),
        season=season, draws=draws)


# --- content wrappers (KB markdown / CSV / Scryfall, not the sim) ----------
def compute_roster():
    """Active roster for the Decks page (Deck_Index ⋈ registry ⋈ clocks ⋈ GC)."""
    return dict(decks=kb.roster())


def compute_deck(slug):
    """Full Tale-of-the-Tape payload for one deck."""
    return kb.deck(slug)


def compute_collection():
    """Owned cards (Moxfield CSV ⋈ Scryfall) + colour/role/rarity facets."""
    return kb.collection()


def compute_wishlist():
    """Build & Swap Tracker — builds, recommended swaps, cheap unlocks."""
    return kb.wishlist()


def compute_tierlist(trials, t_grind, tax, seed, legacy):
    """The Definitive Tier List v2 (or v1) as JSON — mirrors tier_list.compute_rows, rounding the
    axis values for transport. A 4th-consumer wrapper: the composite logic lives in tier_list."""
    p = tl.compute_rows(trials, t_grind, tax, seed, legacy)
    def ri(v):
        return None if v is None else round(v)
    rows = [dict(slug=x["slug"], name=x["name"], tier=x["tier"], comp=round(x["comp"]),
                 anti=round(x["anti"]), inter=ri(x["inter"]),
                 self=round(x["self"]), cc=x["cc"], decap=x["decap"], table=x["table"])
            for x in p["rows"]]
    return dict(version=p["version"], weights=p["weights"], tiers=p["tiers"],
                tax=p["tax"], t_grind=p["t_grind"], trials=p["trials"], rows=rows)


def compute_home(seed):
    """Dashboard hub — roster KPIs + a default gauntlet & championship result."""
    g = compute_gauntlet(a=pg.A_BASE, pod="base", strict=False, trials=8000, seed=seed)
    c = compute_championship(trials=8000, season_trials=20000,
                             t_grind=sm.T_GRIND, swapped=False, seed=sm.SEED,
                             draw_seed=0, n_draws=1)
    # kb.home reads champ["champion"]/["notes"]; flatten the first (fixed) draw up a level.
    champ_flat = {**c, **c["draws"][0]}
    return kb.home(g, champ_flat)


# --- HTTP plumbing ---------------------------------------------------------
def _qint(qs, key, default):
    try:
        return int(qs.get(key, [default])[0])
    except (ValueError, TypeError):
        return default


def _qfloat(qs, key, default):
    try:
        return float(qs.get(key, [default])[0])
    except (ValueError, TypeError):
        return default


def _qbool(qs, key):
    return qs.get(key, ["0"])[0] in ("1", "true", "True", "on")


class Handler(BaseHTTPRequestHandler):
    server_version = "GauntletDashboard/1.0"

    def log_message(self, fmt, *args):       # quieter console
        sys.stderr.write("  %s - %s\n" % (self.address_string(), fmt % args))

    def _send(self, body, ctype, code=200):
        if isinstance(body, str):
            body = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _json(self, obj, code=200):
        self._send(json.dumps(obj), CONTENT_TYPES[".json"], code)

    def do_GET(self):
        u = urlparse(self.path)
        path, qs = u.path, parse_qs(u.query)
        try:
            if path == "/api/clocks":
                return self._json(compute_clocks())
            if path == "/api/gauntlet":
                return self._json(compute_gauntlet(
                    a=_qfloat(qs, "a", pg.A_BASE),
                    pod=qs.get("pod", ["base"])[0],
                    strict=_qbool(qs, "strict"),
                    trials=max(200, min(80000, _qint(qs, "trials", 12000))),
                    seed=_qint(qs, "seed", 20260614)))
            if path == "/api/lock_sweep":
                return self._json(compute_lock_sweep(
                    a=_qfloat(qs, "a", pg.A_BASE),
                    r=_qfloat(qs, "r", pg.R_BASE),
                    strict=_qbool(qs, "strict"),
                    trials=max(200, min(8000, _qint(qs, "trials", 2000))),
                    pod=qs.get("pod", ["base"])[0],
                    seed=_qint(qs, "seed", 20260614)))
            if path == "/api/championship":
                # No draw_seed -> a fresh random bracket each request (so "Re-draw" reshuffles).
                draw_seed = _qint(qs, "draw_seed", -1)
                return self._json(compute_championship(
                    trials=max(500, min(120000, _qint(qs, "trials", 15000))),
                    season_trials=max(2000, min(300000, _qint(qs, "season_trials", 40000))),
                    t_grind=_qint(qs, "t_grind", sm.T_GRIND),
                    swapped=_qbool(qs, "swapped"),
                    seed=_qint(qs, "seed", sm.SEED),
                    draw_seed=(draw_seed if draw_seed >= 0 else None),
                    n_draws=max(1, min(16, _qint(qs, "draws", 1)))))
            if path == "/api/tierlist":
                return self._json(compute_tierlist(
                    trials=max(2000, min(120000, _qint(qs, "trials", 40000))),
                    t_grind=_qint(qs, "t_grind", sm.T_GRIND),
                    tax=_qfloat(qs, "tax", tl.im.TAX),
                    seed=_qint(qs, "seed", sm.SEED),
                    legacy=_qbool(qs, "legacy")))
            if path == "/api/roster":
                return self._json(compute_roster())
            if path == "/api/home":
                return self._json(compute_home(seed=_qint(qs, "seed", 20260614)))
            if path == "/api/wishlist":
                return self._json(compute_wishlist())
            if path == "/api/collection":
                return self._json(compute_collection())
            if path == "/api/deck":
                return self._json(compute_deck(qs.get("slug", [""])[0]))
        except Exception as e:                # surface engine errors to the UI, don't 500 silently
            import traceback
            traceback.print_exc()
            return self._json(dict(error=str(e)), code=500)

        return self._serve_static(path)

    def _serve_static(self, path):
        if not (DASHBOARD_DIR / "index.html").is_file():
            return self._send(
                f"<h1>React build not found</h1><p>Expected <code>{DASHBOARD_DIR}</code>. "
                f"Build the UI first:</p><pre>cd ui && npm ci && npm run build</pre>"
                f"<p>Then reload. (The <code>/api/*</code> endpoints work without a build.)</p>",
                CONTENT_TYPES[".html"], code=503)
        rel = "index.html" if path in ("/", "") else path.lstrip("/")
        target = (DASHBOARD_DIR / rel).resolve()
        if DASHBOARD_DIR not in target.parents and target != DASHBOARD_DIR:
            return self._send("forbidden", "text/plain", 403)
        if not target.is_file():
            return self._send("not found", "text/plain", 404)
        ctype = CONTENT_TYPES.get(target.suffix, "application/octet-stream")
        self._send(target.read_bytes(), ctype)


def lan_ip():
    """Best-guess LAN IPv4 (no traffic sent; just resolves the outbound interface)."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except OSError:
        return None
    finally:
        s.close()


def main():
    ap = argparse.ArgumentParser(description="Gauntlet dashboard server")
    ap.add_argument("--host", default=DEFAULT_HOST,
                    help="bind address; use 0.0.0.0 to allow your phone / other LAN devices")
    ap.add_argument("--port", type=int, default=DEFAULT_PORT)
    args = ap.parse_args()

    httpd = ThreadingHTTPServer((args.host, args.port), Handler)
    print(f"\n  🏟️  Gauntlet dashboard serving the lab stack")
    print(f"      engine: pod_gauntlet + self_meta_lab + pod_championship (imported, not shelled)")
    print(f"      front:  {DASHBOARD_DIR.relative_to(ROOT)} (React build)"
          + ("" if (DASHBOARD_DIR / 'index.html').is_file()
             else "  ⚠ MISSING — run `cd ui && npm run build`"))
    print(f"      local:  http://127.0.0.1:{args.port}")
    if args.host == "0.0.0.0":
        ip = lan_ip()
        if ip:
            print(f"      phone:  http://{ip}:{args.port}   (same Wi-Fi; needs a firewall allow on TCP {args.port})")
    else:
        print(f"      (localhost only — relaunch with --host 0.0.0.0 to reach it from your phone)")
    print(f"      stop:   Ctrl-C\n")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n  bye.\n")
        httpd.shutdown()


if __name__ == "__main__":
    main()
