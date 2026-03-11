from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional
from zoneinfo import ZoneInfo

from dotenv import load_dotenv


@dataclass
class Settings:
    smtp_host: str
    smtp_port: int
    smtp_username: str
    smtp_password: str
    smtp_sender_name: str
    smtp_recipient: str

    nyt_api_key: str
    nyt_endpoint: str
    openmeteo_lat: float
    openmeteo_lon: float
    timezone: ZoneInfo

    news_limit: int = 3


def load_settings(dotenv_override: Optional[Path] = None) -> Settings:
    project_root = Path(__file__).resolve().parents[1]
    dotenv_path = dotenv_override or project_root / ".env"
    if dotenv_path.exists():
        load_dotenv(dotenv_path)

    smtp_password = os.getenv("SMTP_PASSWORD")
    if not smtp_password:
        raise ValueError("SMTP_PASSWORD must be set in the environment or .env file")

    nyt_api_key = os.getenv("NYT_API_KEY")
    if not nyt_api_key:
        raise ValueError("NYT_API_KEY must be set for NYTimes Most Popular API")

    tz_name = os.getenv("TIMEZONE", "Asia/Shanghai")

    return Settings(
        smtp_host=os.getenv("SMTP_HOST", "smtp.gmail.com"),
        smtp_port=int(os.getenv("SMTP_PORT", "587")),
        smtp_username=os.getenv("SMTP_USERNAME", "airmanthehan@gmail.com"),
        smtp_password=smtp_password,
        smtp_sender_name=os.getenv("SMTP_SENDER_NAME", "AIRMAN'S Daily Brief"),
        smtp_recipient=os.getenv("SMTP_RECIPIENT", "hiairman@outlook.com"),
        nyt_api_key=nyt_api_key,
        nyt_endpoint=os.getenv(
            "NYT_ENDPOINT",
            "https://api.nytimes.com/svc/mostpopular/v2/shared/1/facebook.json",
        ),
        openmeteo_lat=float(os.getenv("OPENMETEO_LAT", "31.2304")),
        openmeteo_lon=float(os.getenv("OPENMETEO_LON", "121.4737")),
        timezone=ZoneInfo(tz_name),
    )
