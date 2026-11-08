"""Beispiel-Scraper: Google-Suche (nur zu Demozwecken)."""

from __future__ import annotations

import logging
import urllib.parse
from typing import Optional

from .browser import Browser
from .scraper import Scraper
from .actions import accept_cookies

logger = logging.getLogger(__name__)


class GoogleScraper:
    def __init__(self, headless: bool = True):
        self.browser = Browser(headless=headless)
        self.browser.start()

    def search(self, query: str, num: int = 10) -> list[dict[str, str]]:
        page = self.browser.new_page()
        s = Scraper(page)
        url = "https://www.google.com/search?q=" + urllib.parse.quote(query) + f"&num={num}"
        s.goto(url)
        accept_cookies(page)
        s.wait(1000)
        results = []
        for el in page.query_selector_all("div.g, div.tF2Cxc"):
            try:
                a = el.query_selector("a")
                h3 = el.query_selector("h3")
                snippet = el.query_selector("div.VwiC3b, span.aCOpRe")
                if a and h3:
                    results.append({
                        "title": h3.inner_text().strip(),
                        "url": a.get_attribute("href") or "",
                        "snippet": (snippet.inner_text().strip() if snippet else ""),
                    })
            except Exception:
                continue
        page.close()
        return results

    def close(self) -> None:
        self.browser.close()

    def __enter__(self) -> "GoogleScraper":
        return self

    def __exit__(self, *exc):
        self.close()


if __name__ == "__main__":
    import json, sys
    q = sys.argv[1] if len(sys.argv) > 1 else "headless chromium python"
    with GoogleScraper() as g:
        res = g.search(q, num=5)
        print(json.dumps(res, ensure_ascii=False, indent=2))
