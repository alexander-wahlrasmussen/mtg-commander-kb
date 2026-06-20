#!/usr/bin/env python3
"""ui_screenshot.py — render the React rebuild (ui/) with Playwright and shoot each tab.

Point it at a running Vite preview/dev server. Use ?static=1 to read the baked data
with no Python backend.

Usage:
    python scripts/ui_screenshot.py [--url URL] [--out DIR]
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
        page = browser.new_page(viewport={"width": 1500, "height": 1000}, device_scale_factor=2)
        page.goto(url, wait_until="networkidle")

        # Gauntlet (default) — wait for the bar chart svg
        page.wait_for_selector("main svg", timeout=20000)
        page.wait_for_timeout(800)
        f = out / "01_gauntlet.png"; page.screenshot(path=str(f), full_page=True); shots.append(f)

        # Clocks (emoji selectors — "Locks" is a substring of "Clocks")
        page.click("button:has-text('⏱️')")
        page.wait_for_selector("main svg", timeout=20000)
        page.wait_for_timeout(700)
        f = out / "02_clocks.png"; page.screenshot(path=str(f), full_page=True); shots.append(f)

        # Locks -> run
        page.click("button:has-text('🔒')")
        page.wait_for_timeout(300)
        page.click("button:has-text('Run lock sweep')")
        page.wait_for_selector("main svg", timeout=30000)
        page.wait_for_timeout(700)
        f = out / "03_locks.png"; page.screenshot(path=str(f), full_page=True); shots.append(f)

        # Championship -> run
        page.click("button:has-text('🏆')")
        page.wait_for_timeout(300)
        page.click("button:has-text('Run the tournament')")
        page.wait_for_selector("text=Champion", timeout=30000)
        page.wait_for_timeout(700)
        f = out / "04_championship.png"; page.screenshot(path=str(f), full_page=True); shots.append(f)

        browser.close()
    return shots


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", default="http://127.0.0.1:5180/?static=1")
    ap.add_argument("--out", default=str(Path(__file__).resolve().parent.parent / ".dashboard_shots" / "react"))
    args = ap.parse_args()
    try:
        for s in shoot(args.url, args.out):
            print(s)
    except Exception as e:
        print(f"ERROR: {e}\n(is the preview server running at {args.url}?)", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
