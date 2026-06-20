#!/usr/bin/env python3
"""dashboard_screenshot.py — render the live dashboard with Playwright and shoot
each tab to PNG, for visual verification after style changes.

Requires: pip install playwright; python -m playwright install chromium
The dashboard server must be running (python scripts/dashboard_server.py).

Usage:
    python scripts/dashboard_screenshot.py [--url URL] [--out DIR]
"""
import argparse
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright


def shoot(url, out):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    shots = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1500, "height": 1000},
                                device_scale_factor=2)
        page.goto(url, wait_until="networkidle")

        # Gauntlet (default tab) — the status badge flips to .ok when the run lands
        page.wait_for_selector("#gauntletStatus.ok", timeout=20000)
        page.wait_for_selector("#gauntletBars svg", state="attached", timeout=20000)
        page.wait_for_timeout(900)
        f = out / "01_gauntlet.png"; page.screenshot(path=str(f), full_page=True); shots.append(f)

        # Clocks tab
        page.click('button[data-tab="clocks"]')
        page.wait_for_selector("#clockPlot svg", state="attached", timeout=20000)
        page.wait_for_timeout(900)
        f = out / "02_clocks.png"; page.screenshot(path=str(f), full_page=True); shots.append(f)

        # Locks tab -> run the sweep (heavy)
        page.click('button[data-tab="locks"]')
        page.wait_for_timeout(300)
        page.click("#runLocks")
        page.wait_for_selector("#lockCard:not(.hidden)", timeout=60000)
        page.wait_for_selector("#lockHeatmap svg", state="attached", timeout=60000)
        page.wait_for_timeout(900)
        f = out / "05_locks.png"; page.screenshot(path=str(f), full_page=True); shots.append(f)

        # Championship tab -> run the tournament
        page.click('button[data-tab="championship"]')
        page.wait_for_timeout(300)
        f = out / "03_championship_empty.png"; page.screenshot(path=str(f), full_page=True); shots.append(f)
        page.click("#runChamp")
        page.wait_for_selector("#champBanner:not(.hidden)", timeout=30000)
        page.wait_for_timeout(700)
        f = out / "04_championship.png"; page.screenshot(path=str(f), full_page=True); shots.append(f)

        browser.close()
    return shots


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", default="http://127.0.0.1:8765")
    ap.add_argument("--out", default=str(Path(__file__).resolve().parent.parent / ".dashboard_shots"))
    args = ap.parse_args()
    try:
        shots = shoot(args.url, args.out)
    except Exception as e:
        print(f"ERROR: {e}\n(is the server running at {args.url}?)", file=sys.stderr)
        sys.exit(1)
    for s in shots:
        print(s)


if __name__ == "__main__":
    main()
