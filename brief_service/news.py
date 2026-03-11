from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

import requests

logger = logging.getLogger(__name__)


@dataclass
class NewsItem:
    title: str
    summary: str
    link: str
    published: Optional[datetime]


def fetch_top_news(endpoint: str, api_key: str, limit: int = 3) -> List[NewsItem]:
    logger.info("Fetching NYTimes most popular feed: %s", endpoint)

    try:
        resp = requests.get(
            endpoint,
            params={"api-key": api_key},
            timeout=20,
        )
        resp.raise_for_status()
        payload = resp.json()
    except Exception as exc:
        logger.error("Failed to fetch NYTimes feed: %s", exc)
        return []

    results = payload.get("results", [])
    items: List[NewsItem] = []

    for entry in results[:limit]:
        title = entry.get("title") or "(Untitled)"
        summary = entry.get("abstract") or (entry.get("adx_keywords") or "")
        url = entry.get("url") or ""
        published = None
        if entry.get("published_date"):
            try:
                published = datetime.fromisoformat(entry["published_date"])
            except ValueError:
                published = None

        items.append(
            NewsItem(
                title=title.strip(),
                summary=summary.strip(),
                link=url.strip(),
                published=published,
            )
        )

    return items
