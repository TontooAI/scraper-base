# scraper_base

Wiederverwendbare Python-Basis für Headless-Chromium-Scraping (Playwright).

## Features
- `Browser` Context-Manager (Chromium headless, sinnvolle Defaults, User-Agent, Viewport, Locale/TZ)
- `Scraper` mit Navigation, Aktionen (click/fill/type/press/scroll), Extraktion (text/texts/attr/links), JS-evaluate, Screenshots
- `actions`: Cookie-Banner akzeptieren, Human-Delays, Network-Idle
- `extractors`: Meta-Tags, Tabellen, Bilder
- Beispiel: `GoogleScraper`
- CLI: `python -m scraper_base <url>`

## Installation
```bash
pip install -r requirements.txt
playwright install chromium
```

## Schnellstart
```python
from scraper_base import Browser, Scraper

with Browser() as b:
    page = b.new_page()
    s = Scraper(page)
    s.goto("https://example.com")
    print(s.title())
    print(s.text("h1"))
    s.screenshot("/tmp/shot.png", full_page=True)
```

## JS ausführen
```python
print(s.evaluate("() => document.querySelectorAll('a').length"))
```

## Google-Beispiel
```bash
python -m scraper_base.google_scraper "python playwright"
```

## Hinweise
- Headless Chromium läuft mit `--no-sandbox` (Container). Für Produktion ggf. anpassen.
- Respektiere robots.txt / ToS der Ziel-Seiten.
- Keine destruktiven Aktionen ohne Freigabe.
PY