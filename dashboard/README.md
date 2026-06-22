# The Pod Gauntlet — control room

A visual, interactive front-end for the gauntlet / lab / championship stack. Run the pod
gauntlet, overlay the clock labs, and crown a champion from a browser with sliders instead
of CLI flags.

The front-end is the **React app in `../ui/`** (newsprint design system). This `dashboard/`
folder now only holds the **baked JSON** (`data/`, written by `scripts/dashboard_export.py`
and mirrored into `../ui/public/data`). The old hand-rolled vanilla front-end has been retired.

There are two ways to run it — both use the same React UI:

## 1. Compute mode (live backend)

The Python server (`scripts/dashboard_server.py`) serves the **built** React app plus the
live `/api/*` endpoints, so every control re-runs the real sim engine.

```bash
cd ui && npm ci && npm run build      # build the React front-end (once, or after UI changes)
python scripts/dashboard_server.py    # serves ui/dist + /api  → http://127.0.0.1:8765
```

The page probes `/api/clocks`, finds the backend, and runs in **live mode**: the Championship
**Re-draw** button reshuffles the pods with a fresh random draw each press.

For UI development with hot-reload, run Vite directly and let it proxy `/api` to the server:
`cd ui && npm run dev` (see `ui/vite.config.ts`).

### View on your phone (same Wi-Fi)

```bash
python scripts/dashboard_server.py --host 0.0.0.0
```

The banner prints a `phone:` URL. Then, **once**, allow the port through Windows Firewall in an
**elevated** PowerShell:

```powershell
New-NetFirewallRule -DisplayName "Pod Gauntlet 8765" -Direction Inbound -Action Allow `
  -Protocol TCP -LocalPort 8765 -Profile Private,Public -RemoteAddress LocalSubnet
```

No auth — anyone on the LAN can reach it; remove the rule with
`Remove-NetFirewallRule -DisplayName "Pod Gauntlet 8765"` when done.

## 2. Precomputed mode (static, no backend)

Bake a grid of scenarios to JSON, then host the static React build anywhere — no Python.

```bash
python scripts/dashboard_export.py    # writes dashboard/data/*.json, mirrored to ui/public/data
cd ui && npm run build && npm run preview   # or deploy ui/dist to any static host
```

The page auto-detects the baked `data/manifest.json` and switches to **static mode**: sliders
snap to the baked scenarios, the precision knobs (trials) lock, and Championship **Re-draw**
cycles the *N* baked sample draws (`CHAMP_DRAWS` in `dashboard_export.py`). Force the live API
instead with `?live=1`; force static with `?static=1`.

**GitHub Pages (this repo):** `.github/workflows/dashboard-pages.yml` builds `ui/` and deploys
`ui/dist` on push to `master`. Re-bake (`dashboard_export.py`) and commit the refreshed
`ui/public/data/*.json` to update the data. **A Pages site is public** even from a private repo —
the baked JSON holds deck names, win-probabilities, and the per-deck decklists (an external pilot
reference), but **not** the collection / ownership data.

## Tabs

| Tab | Engine | Knobs (= CLI flags) |
|---|---|---|
| **Gauntlet** | `pod_gauntlet.run_default` | Abolisher P(out) `--a`, pod speed `--pod-fast/slow`, decap↔table `--strict`, trials |
| **Clocks** | harvested CDFs (`pod_gauntlet.merged_clocks`) | curve decap↔table, deck overlay |
| **Locks** | `pod_gauntlet.lock_sweep_rows` | Abolisher `--a`, lock-removal `--r`, decap↔table, pod speed, trials |
| **Championship** | `pod_championship` | playoff trials, season trials, `--t-grind`, `--swapped`, **🎲 Re-draw** |
| Decks / Collection / Wishlist | `kb_content` (KB markdown / CSV / Scryfall) | — |

### The championship draw

The group stage is a **pot-based random draw**: the regular season (P(win | random 4-seat pod))
seeds the 16 decks, they split into 4 pots (1-4 / 5-8 / 9-12 / 13-16), and one deck is drawn from
each pot into each pod — balanced like the old snake bracket, but freshly shuffled. The CLI
exposes `--snake` (force the old deterministic 1-8-9-16 bracket) and `--draw-seed N` (reproduce a
specific draw); `python scripts/pod_championship.py` prints the draw seed it used.

## Architecture

```
React ui/dist  ──HTTP/JSON──►  scripts/dashboard_server.py
   │ (live: /api/*)               │ importlib (house pattern)
   │ (static: data/*.json)        ▼
   └───────────────►  pod_championship → self_meta_lab → pod_gauntlet + delay_lab
```

The server is a **consumer** of the same imported functions the labs already chain — it calls
`merged_clocks() / build_cdf() / pure_race() / simulate() / disruption()` and the championship's
`seed_field() / draw_groups() / pod_shares()` directly, so the browser charts the same numbers the
writeups cite. The season seeding uses a fixed RNG (stable seeds); the group draw uses a fresh RNG
(random brackets).

## Discipline

Inherited from the lab stack and shown in the UI footer: clock curves are unblocked goldfish
ceilings; disruption is *availability*, not effectiveness; the durability tiebreak and `T_grind`
are judgment. **Read the ranking and the gaps, not the second decimal.** This is a viewer for the
labs, not a new model.
