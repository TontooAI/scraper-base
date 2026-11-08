"""Scraper-Basis: Aktionen + Datenextraktion auf einer Page."""

from __future__ import annotations

import logging
import time
from typing import Any, Optional

from playwright.sync_api import Page, TimeoutError as PwTimeout

logger = logging.getLogger(__name__)


class Scraper:
    def __init__(self, page: Page):
        self.page = page

    # ---------- Navigation ----------
    def goto(self, url: str, wait_until: str = "domcontentloaded", timeout: int = 30000) -> None:
        logger.info("goto %s", url)
        self.page.goto(url, wait_until=wait_until, timeout=timeout)

    def wait_for_selector(self, selector: str, timeout: int = 15000, state: str = "visible") -> None:
        self.page.wait_for_selector(selector, timeout=timeout, state=state)

    def wait(self, ms: int = 1000) -> None:
        time.sleep(ms / 1000.0)

    # ---------- Infos ----------
    def title(self) -> str:
        return self.page.title()

    def url(self) -> str:
        return self.page.url

    def html(self) -> str:
        return self.page.content()

    # ---------- Extraktion ----------
    def text(self, selector: str, first: bool = True) -> Optional[str]:
        try:
            el = self.page.query_selector(selector)
            if el is None:
                return None
            return el.inner_text().strip()
        except Exception as e:
            logger.warning("text(%s) fehlgeschlagen: %s", selector, e)
            return None

    def texts(self, selector: str) -> list[str]:
        out = []
        for el in self.page.query_selector_all(selector):
            try:
                out.append(el.inner_text().strip())
            except Exception:
                pass
        return out

    def attr(self, selector: str, name: str) -> Optional[str]:
        el = self.page.query_selector(selector)
        if el is None:
            return None
        return el.get_attribute(name)

    def attrs(self, selector: str, name: str) -> list[Optional[str]]:
        return [el.get_attribute(name) for el in self.page.query_selector_all(selector)]

    def links(self, selector: str = "a") -> list[dict[str, str]]:
        out = []
        for el in self.page.query_selector_all(selector):
            try:
                out.append({"text": (el.inner_text() or "").strip(), "href": el.get_attribute("href") or ""})
            except Exception:
                pass
        return out

    def evaluate(self, js: str, *args: Any) -> Any:
        """Führt JavaScript im Seitenkontext aus."""
        return self.page.evaluate(js, *args)

    # ---------- Aktionen ----------
    def click(self, selector: str, timeout: int = 10000) -> None:
        self.page.click(selector, timeout=timeout)

    def fill(self, selector: str, value: str, timeout: int = 10000) -> None:
        self.page.fill(selector, value, timeout=timeout)

    def type_text(self, selector: str, text: str, delay: int = 50) -> None:
        self.page.type(selector, text, delay=delay)

    def press(self, selector: str, key: str) -> None:
        self.page.press(selector, key)

    def select_option(self, selector: str, value: str) -> None:
        self.page.select_option(selector, value)

    def scroll_to_bottom(self, steps: int = 5, delay_ms: int = 500) -> None:
        for _ in range(steps):
            self.page.evaluate("window.scrollBy(0, window.innerHeight)")
            time.sleep(delay_ms / 1000.0)

    def screenshot(self, path: str, full_page: bool = False, timeout: int = 60000) -> str:
        self.page.screenshot(path=path, full_page=full_page, timeout=timeout, animations="disabled")
        return path

    # ---------- Helpers ----------
    def exists(self, selector: str) -> bool:
        return self.page.query_selector(selector) is not None

    def count(self, selector: str) -> int:
        return len(self.page.query_selector_all(selector))

    def safe(self, fn, default=None):
        try:
            return fn()
        except Exception as e:
            logger.warning("safe() caught: %s", e)
            return default
