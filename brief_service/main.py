from __future__ import annotations

import argparse
import logging
from datetime import datetime

from .config import load_settings
from .email_builder import render_email
from .mailer import send_email
from .news import fetch_top_news
from .weather import fetch_weather

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger(__name__)


def run(dry_run: bool = False) -> None:
    settings = load_settings()

    now = datetime.now(tz=settings.timezone)
    logger.info("Generating brief for %s", now.date())

    news_items = fetch_top_news(settings.nyt_endpoint, settings.nyt_api_key, settings.news_limit)
    if not news_items:
        logger.warning("No news items retrieved from Reuters feed")

    weather = fetch_weather(settings.openmeteo_lat, settings.openmeteo_lon, settings.timezone.key)

    email_content = render_email(now, news_items, weather)

    if dry_run:
        logger.info("Dry-run mode: printing email instead of sending")
        print("Subject:", email_content.subject)
        print("\n--- TEXT VERSION ---\n")
        print(email_content.text)
        print("\n--- HTML VERSION ---\n")
        print(email_content.html)
    else:
        send_email(settings, email_content.subject, email_content.html, email_content.text)


def main() -> None:
    parser = argparse.ArgumentParser(description="Send AIRMAN'S daily brief")
    parser.add_argument("--dry-run", action="store_true", help="Print email content without sending")
    args = parser.parse_args()

    run(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
