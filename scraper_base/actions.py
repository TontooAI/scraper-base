"""Häufige Aktionen (Login-Flows, Cookie-Banner, Scroll)."""

from __future__ import annotations

import logging
import time

logger = logging.getLogger(__name__)

COOKIE_SELECTORS = [
    "button#onetrust-accept-btn-handler",
    "button[aria-label*='Accept']",
    "button[aria-label*='Akzeptieren']",
    "button:has-text('Accept all')",
    "button:has-text('Alle akzeptieren')",
    "button:has-text('I agree')",
]


def accept_cookies(page) -> bool:
    for sel in COOKIE_SELECTORS:
        try:
            btn = page.query_selector(sel)
            if btn:
                btn.click()
                time.sleep(0.5)
                logger.info("Cookie-Banner akzeptiert via %s", sel)
                return True
        except Exception:
            continue
    return False


def human_delay(min_ms: int = 200, max_ms: int = 800) -> None:
    import random
    time.sleep(random.uniform(min_ms, max_ms) / 1000.0)


def wait_for_network_idle(page, timeout: int = 10000) -> None:
    try:
        page.wait_for_load_state("networkidle", timeout=timeout)
    except Exception:
        pass
