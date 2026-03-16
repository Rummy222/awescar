"""
Scrape 98th Academy Awards winners from Wikipedia and update the database.

Run standalone:   python scraper.py
Called from app:  from scraper import sync_winners

Wikipedia marks winner rows with background-color #FAEB86 (gold).
Falls back to bold text in the first data row if no background is found.
"""
import re
import unicodedata

import requests
from bs4 import BeautifulSoup

WIKIPEDIA_URL = "https://en.wikipedia.org/wiki/98th_Academy_Awards"
HEADERS = {"User-Agent": "Awescar/1.0 (Oscar prediction pool)"}

# Maps normalized Wikipedia heading → our DB category name.
# Wikipedia sometimes omits "Film" from the end, so both forms are listed.
CATEGORY_MAP = {
    "best picture": "Best Picture",
    "best director": "Best Director",
    "best actor": "Best Actor",
    "best actress": "Best Actress",
    "best supporting actor": "Best Supporting Actor",
    "best supporting actress": "Best Supporting Actress",
    "best animated feature film": "Best Animated Feature Film",
    "best animated feature": "Best Animated Feature Film",
    "best documentary feature film": "Best Documentary Feature Film",
    "best documentary feature": "Best Documentary Feature Film",
    "best documentary short film": "Best Documentary Short Film",
    "best documentary short": "Best Documentary Short Film",
    "best international feature film": "Best International Feature Film",
    "best international feature": "Best International Feature Film",
    "best live action short film": "Best Live Action Short Film",
    "best live action short": "Best Live Action Short Film",
    "best animated short film": "Best Animated Short Film",
    "best animated short": "Best Animated Short Film",
    "best original screenplay": "Best Original Screenplay",
    "best adapted screenplay": "Best Adapted Screenplay",
    "best cinematography": "Best Cinematography",
    "best film editing": "Best Film Editing",
    "best original score": "Best Original Score",
    "best original song": "Best Original Song",
    "best sound": "Best Sound",
    "best visual effects": "Best Visual Effects",
    "best costume design": "Best Costume Design",
    "best makeup and hairstyling": "Best Makeup and Hairstyling",
    "best production design": "Best Production Design",
    "best casting": "Best Casting",
}


def _normalize(text):
    """Lowercase, strip diacritics, collapse whitespace, strip punctuation."""
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    text = text.lower()
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _map_heading(heading_text):
    """Return our DB category name for a Wikipedia section heading, or None."""
    # Strip "[edit]" and similar markup Wikipedia injects
    clean = re.sub(r"\[.*?\]", "", heading_text).strip()
    return CATEGORY_MAP.get(_normalize(clean))


def _winner_names_from_table(table):
    """
    Return list of winner name strings from a wikitable.
    Strategy:
      1. Rows with background-color #FAEB86 (Wikipedia gold highlight) are winners.
      2. If none found, fall back to the first data row that has bold text.
    """
    winner_names = []

    def _has_gold_bg(tag):
        style = (tag.get("style") or "").lower()
        bgcolor = (tag.get("bgcolor") or "").lower()
        return "faeb86" in style or "faeb86" in bgcolor

    for row in table.find_all("tr"):
        cells = row.find_all("td")
        if not cells:
            continue  # header row

        # Check row background or first-cell background
        if _has_gold_bg(row) or _has_gold_bg(cells[0]):
            name = cells[0].get_text(" ", strip=True)
            if name:
                winner_names.append(name)

    # Fallback: first data row that contains bold text
    if not winner_names:
        for row in table.find_all("tr"):
            cells = row.find_all("td")
            if not cells:
                continue
            bold = cells[0].find(["b", "strong"])
            if bold:
                name = bold.get_text(" ", strip=True)
                if name:
                    winner_names.append(name)
                break  # only the first bolded row

    return winner_names


def scrape_winners():
    """
    Fetch Wikipedia and return {db_category_name: [winner_name, ...]}.
    Raises requests.HTTPError on network failure.
    """
    resp = requests.get(WIKIPEDIA_URL, headers=HEADERS, timeout=15)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    results = {}
    content = soup.find(id="mw-content-text")
    if not content:
        return results

    current_category = None
    for elem in content.find_all(["h2", "h3", "h4", "table"]):
        if elem.name in ("h2", "h3", "h4"):
            current_category = _map_heading(elem.get_text())
        elif elem.name == "table" and "wikitable" in (elem.get("class") or []):
            if current_category:
                names = _winner_names_from_table(elem)
                if names:
                    results[current_category] = names
                current_category = None  # consumed by this table

    return results


def _nominee_matches(nominee, winner_name):
    """True if nominee.name fuzzy-matches the scraped winner name."""
    n = _normalize(nominee.name)
    w = _normalize(winner_name)
    # Exact match, or one contains the other (handles "Film Title" vs "Film Title — detail")
    return n == w or n in w or w in n


def sync_winners(dry_run=False):
    """
    Scrape Wikipedia and set is_winner on matching nominees.
    Only SETS winners — never clears them (use admin panel to clear).
    Returns (updated_count, log_lines).
    """
    from models import Category, db  # imported here to avoid circular import at module load

    log = []
    updated = 0

    try:
        scraped = scrape_winners()
    except Exception as exc:
        return 0, [f"ERROR fetching Wikipedia: {exc}"]

    if not scraped:
        return 0, ["No winners detected on Wikipedia page (page may not be updated yet)."]

    for db_cat_name, winner_names in scraped.items():
        cat = Category.query.filter_by(name=db_cat_name).first()
        if not cat:
            log.append(f"SKIP (no DB match): {db_cat_name}")
            continue

        for winner_name in winner_names:
            matched = next(
                (n for n in cat.nominees if _nominee_matches(n, winner_name)),
                None,
            )
            if not matched:
                log.append(f"NO MATCH: [{db_cat_name}] '{winner_name}'")
                continue

            if matched.is_winner:
                log.append(f"already set : [{db_cat_name}] {matched.name}")
            else:
                log.append(f"SET WINNER  : [{db_cat_name}] {matched.name}")
                updated += 1
                if not dry_run:
                    matched.is_winner = True

    if not dry_run and updated > 0:
        db.session.commit()

    return updated, log


if __name__ == "__main__":
    from app import app  # noqa: E402

    with app.app_context():
        count, lines = sync_winners()
        for line in lines:
            print(line)
        print(f"\nUpdated {count} winner(s).")
