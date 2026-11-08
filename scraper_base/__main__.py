"""CLI: python -m scraper_base <url> [--screenshot path] [--js '...']"""

from __future__ import annotations

import argparse
import json
import sys

from .browser import Browser
from .scraper import Scraper


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("--selector", default="h1", help="CSS selector to extract text")
    ap.add_argument("--js", default=None, help="JavaScript to evaluate")
    ap.add_argument("--screenshot", default=None, help="Screenshot path")
    ap.add_argument("--headless", action="store_true", default=True)
    args = ap.parse_args()

    with Browser(headless=args.headless) as b:
        page = b.new_page()
        s = Scraper(page)
        s.goto(args.url)
        out = {"url": s.url(), "title": s.title()}
        out["texts"] = s.texts(args.selector)
        if args.js:
            out["js_result"] = s.evaluate(args.js)
        if args.screenshot:
            out["screenshot"] = s.screenshot(args.screenshot, full_page=True)
        print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
