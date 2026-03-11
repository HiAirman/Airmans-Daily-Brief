# AIRMAN'S Daily Brief Service

A Python service that sends a daily HTML email at 07:00 Beijing time with:

- Top three world events sourced from the New York Times "Most Popular" API (`/svc/mostpopular/v2/shared/1/facebook.json`)
- A Shanghai-focused weather snapshot (current conditions + remainder of the day) sourced from Open-Meteo
- Delivery via Gmail SMTP (TLS) using the sender alias **AIRMAN'S Daily Brief**

## Project layout

```
airman-daily-brief/
├── README.md
├── requirements.txt
├── sample.env
├── brief_service/
│   ├── __init__.py
│   ├── config.py
│   ├── news.py
│   ├── weather.py
│   ├── email_builder.py
│   ├── mailer.py
│   └── main.py
├── templates/
│   └── email.html.j2
└── systemd/
    ├── airman-daily-brief.service
    └── airman-daily-brief.timer
```

## Setup

1. **Python environment**
   ```bash
   cd ~/Desktop/airman-daily-brief
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Configuration**
   - Copy `sample.env` to `.env` and fill in/adjust the Gmail SMTP credentials plus any overrides.
   - The defaults already target 07:00 Asia/Shanghai, send from `airmanthehan@gmail.com` to `hiairman@outlook.com`, and use NYTimes/Open-Meteo as sources.

3. **Dry run**
   ```bash
   source .venv/bin/activate
   python -m brief_service.main --dry-run
   ```
   Dry-run prints the composed email to stdout instead of sending.

4. **Actual run**
   ```bash
   python -m brief_service.main
   ```

5. **Schedule with systemd (recommended)**
   ```bash
   sudo cp systemd/airman-daily-brief.service /etc/systemd/system/
   sudo cp systemd/airman-daily-brief.timer /etc/systemd/system/
   sudo systemctl daemon-reload
   sudo systemctl enable --now airman-daily-brief.timer
   ```

The systemd timer is configured to trigger daily at 07:00 local Asia/Shanghai time and runs the service user-level script via the virtual environment.

## Logging

- Runtime logs via the Python `logging` module print to stdout/stderr (captured by systemd if used)
- For quick inspection when running manually, logs appear in the terminal

## Configuration details

Environment variables (see `sample.env`):

| Variable | Description |
| --- | --- |
| `SMTP_HOST` | Gmail SMTP host (default `smtp.gmail.com`) |
| `SMTP_PORT` | TLS port (default `587`) |
| `SMTP_USERNAME` | Sender mail username |
| `SMTP_PASSWORD` | **Required.** app password for SMTP (2FA-enabled) |
| `SMTP_SENDER_NAME` | Display name (default `AIRMAN'S Daily Brief`) |
| `SMTP_RECIPIENT` | Recipient email |
| `NYT_API_KEY` | **Required.** NYTimes API key (Most Popular API) |
| `NYT_ENDPOINT` | NYTimes Most Popular endpoint (default shared-on-facebook feed) |
| `OPENMETEO_LAT` / `OPENMETEO_LON` | Shanghai coordinates |
| `TIMEZONE` | IANA timezone string (default `Asia/Shanghai`) |

## Notes
- NYTimes API key is required from developers.nytimes.com.
- Open-Meteo requires no API key but expects reasonable request volumes.
- SMTP credentials are kept outside the repository in `.env` (referenced by the service). For Gmail, ensure you create an App Password (requires 2FA) and use it as `SMTP_PASSWORD`.
