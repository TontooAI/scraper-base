"""scraper_base - wiederverwendbare Basis für Headless-Chromium-Scraping.

Verwendung:
    from scraper_base import Browser, Scraper

    with Browser() as b:
        page = b.new_page()
        s = Scraper(page)
        s.goto("https://example.com")
        print(s.title())
        print(s.text("h1"))
"""

from .browser import Browser
from .scraper import Scraper

__version__ = "0.1.0"
__all__ = ["Browser", "Scraper"]
