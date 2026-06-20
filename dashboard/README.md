# The Pod Gauntlet — control room

A fun, visual, interactive front-end for the gauntlet/lab/championship stack.
Run the pod gauntlet, overlay the clock labs, and crown a champion from a browser
with sliders instead of CLI flags.

## Launch

```bash
python scripts/dashboard_server.py
# then open http://127.0.0.1:8765
```

No build step, no dependencies — `dashboard_server.py` is stdlib `http.server`.
(Charts and webfonts load from CDNs; offline, the charts degrade and the UI falls
back to the system font stack.)

## What it does

Four tabs, each driving the **existing** sim engine — nothing is reimplemented:

| Tab | Engine | Knobs (= CLI flags) |
|---|---|---|
| ⚔️ **Gauntlet** | `pod_gauntlet.run_default` | Abolisher P(out) `--a`, pod speed `--pod-fast/slow`, decap↔table `--strict`, trials |
| ⏱️ **Clocks / Labs** | harvested CDFs (`pod_gauntlet.merged_clocks`) | curve decap↔table, deck overlay chips |
| 🔒 **Locks** | `pod_gauntlet.lock_sweep_rows` (`--lock-sweep`) | Abolisher `--a`, lock-removal `--r`, decap↔table, pod speed, trials |
| 🏆 **Championship** | `pod_championship.main` | playoff trials, season trials, `--t-grind`, `--swapped` |

Gauntlet and Clocks re-run live as you move a control; Locks and Championship are
explicit **Run** (heavy compute — Locks loads the oracle data and measures every
deck × lock).

## Architecture

```
browser (dashboard/*)  ──HTTP/JSON──►  scripts/dashboard_server.py
                                          │ importlib (house pattern)
                                          ▼
                       pod_championship → self_meta_lab → pod_gauntlet + delay_lab
```

The server is a **fourth consumer** of the same imported functions
`pod_championship` and `self_meta_lab` already chain — it calls
`merged_clocks() / build_cdf() / pure_race() / simulate() / disruption()` and the
championship's `seed_field() / snake_groups() / pod_shares()` directly, so the
browser charts the same numbers the writeups cite. A fixed RNG seed per request
makes the curves move smoothly when you nudge a slider.

## Files

- `index.html` — markup + the only two CDN includes (Plotly, webfonts)
- `style.css` — **all** the look lives in `:root` design tokens (type scale,
  spacing, color, depth, motion). Re-skin the whole app by editing tokens; the
  charts read the same tokens via `cssvar()` in `app.js`.
- `app.js` — three independent modules (Gauntlet / Clocks / Championship) + shared
  Plotly theming. Swap `PALETTE` or `baseLayout()` to experiment with chart style.

## Endpoints (if you want to script against it)

- `GET /api/clocks`
- `GET /api/gauntlet?a=&pod=fast|base|slow&strict=0|1&trials=`
- `GET /api/lock_sweep?a=&r=&pod=fast|base|slow&strict=0|1&trials=`
- `GET /api/championship?trials=&season_trials=&t_grind=&swapped=0|1`

## Discipline

Inherited from the lab stack and shown in the UI footer: clock curves are
unblocked goldfish ceilings; disruption is *availability*, not effectiveness; the
durability tiebreak and `T_grind` are judgment. **Read the ranking and the gaps,
not the second decimal.** This is a viewer for the labs, not a new model.
