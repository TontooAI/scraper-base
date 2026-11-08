"""Browser-Management: Playwright Chromium headless mit sinnvollen Defaults."""

from __future__ import annotations

import logging
from contextlib import contextmanager
from typing import Optional

from playwright.sync_api import sync_playwright, Browser as PwBrowser, Page, BrowserContext

logger = logging.getLogger(__name__)

DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)


class Browser:
    """Wrapper um Playwright Chromium. Nutzbar als Context-Manager."""

    def __init__(
        self,
        headless: bool = True,
        user_agent: str = DEFAULT_USER_AGENT,
        viewport: tuple[int, int] = (1366, 768),
        locale: str = "de-DE",
        timezone: str = "Europe/Berlin",
        extra_args: Optional[list[str]] = None,
    ):
        self.headless = headless
        self.user_agent = user_agent
        self.viewport = {"width": viewport[0], "height": viewport[1]}
        self.locale = locale
        self.timezone = timezone
        self.extra_args = extra_args or []
        self._pw = None
        self._browser: Optional[PwBrowser] = None
        self._context: Optional[BrowserContext] = None

    def __enter__(self) -> "Browser":
        self.start()
        return self

    def __exit__(self, *exc):
        self.close()

    def start(self) -> None:
        self._pw = sync_playwright().start()
        args = ["--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu"] + self.extra_args
        self._browser = self._pw.chromium.launch(headless=self.headless, args=args)
        self._context = self._browser.new_context(
            user_agent=self.user_agent,
            viewport=self.viewport,
            locale=self.locale,
            timezone_id=self.timezone,
        )
        logger.info("Browser gestartet (headless=%s)", self.headless)

    def new_page(self) -> Page:
        if self._context is None:
            raise RuntimeError("Browser nicht gestartet. Erst start() aufrufen.")
        page = self._context.new_page()
        page.set_default_timeout(30000)
        return page

    def close(self) -> None:
        try:
            if self._context:
                self._context.close()
            if self._browser:
                self._browser.close()
            if self._pw:
                self._pw.stop()
        except Exception as e:
            logger.warning("Fehler beim Schließen: %s", e)
        finally:
            self._context = None
            self._browser = None
            self._pw = None

    @contextmanager
    def page(self, url: Optional[str] = None):
        p = self.new_page()
        try:
            if url:
                p.goto(url, wait_until="domcontentloaded")
            yield p
        finally:
            p.close()
