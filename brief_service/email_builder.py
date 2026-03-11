from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Tuple

from jinja2 import Environment, FileSystemLoader, select_autoescape

from .news import NewsItem
from .weather import WeatherBrief

TEMPLATES_DIR = Path(__file__).resolve().parents[1] / "templates"

_env = Environment(
    loader=FileSystemLoader(str(TEMPLATES_DIR)),
    autoescape=select_autoescape(["html", "xml"]),
    trim_blocks=True,
    lstrip_blocks=True,
)


@dataclass
class EmailContent:
    subject: str
    html: str
    text: str


def render_email(date: datetime, news_items: List[NewsItem], weather: WeatherBrief) -> EmailContent:
    template = _env.get_template("email.html.j2")

    context = {
        "date": date,
        "news_items": news_items,
        "weather": weather,
    }

    html_body = template.render(**context)

    lines = [
        f"AIRMAN'S Daily Brief — {date.strftime('%Y-%m-%d')}",
        "",
        "World Events:",
    ]

    if news_items:
        for idx, item in enumerate(news_items, start=1):
            lines.append(f"{idx}. {item.title} ({item.link})")
            if item.summary:
                lines.append(f"   {item.summary}")
    else:
        lines.append("- No stories available today.")

    lines.extend([
        "",
        "Shanghai Weather:",
        f"Current: {weather.temperature_c:.1f}°C, {weather.weather_description}",
        f"High/Low: {weather.high_c:.1f}°C / {weather.low_c:.1f}°C",
    ])
    if weather.precip_chance is not None:
        lines.append(f"Precipitation chance: {weather.precip_chance}%")

    text_body = "\n".join(lines)

    subject = f"AIRMAN'S Daily Brief – {date.strftime('%Y-%m-%d')}"

    return EmailContent(subject=subject, html=html_body, text=text_body)
