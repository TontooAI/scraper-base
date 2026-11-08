"""Häufige Extraktoren (Meta, Tabellen, Listen)."""

from __future__ import annotations

from typing import Any


def meta(page_or_scraper) -> dict[str, str]:
    page = getattr(page_or_scraper, "page", page_or_scraper)
    out = {}
    for el in page.query_selector_all("meta"):
        name = el.get_attribute("name") or el.get_attribute("property")
        content = el.get_attribute("content")
        if name and content:
            out[name] = content
    return out


def tables(page_or_scraper) -> list[list[list[str]]]:
    page = getattr(page_or_scraper, "page", page_or_scraper)
    result = []
    for t in page.query_selector_all("table"):
        rows = []
        for tr in t.query_selector_all("tr"):
            cells = [c.inner_text().strip() for c in tr.query_selector_all("th, td")]
            if cells:
                rows.append(cells)
        result.append(rows)
    return result


def images(page_or_scraper, min_width: int = 0) -> list[dict[str, str]]:
    page = getattr(page_or_scraper, "page", page_or_scraper)
    out = []
    for img in page.query_selector_all("img"):
        src = img.get_attribute("src") or img.get_attribute("data-src") or ""
        alt = img.get_attribute("alt") or ""
        w = img.get_attribute("width") or "0"
        try:
            wi = int(w)
        except ValueError:
            wi = 0
        if wi >= min_width or min_width == 0:
            out.append({"src": src, "alt": alt, "width": w})
    return out


def to_dict_list(rows: list[list[str]], header: bool = True) -> list[dict[str, str]]:
    if not rows:
        return []
    if header:
        keys = rows[0]
        return [dict(zip(keys, r)) for r in rows[1:]]
    return [dict(enumerate(r)) for r in rows]  # type: ignore
