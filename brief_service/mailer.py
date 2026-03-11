from __future__ import annotations

import logging
import smtplib
from email.message import EmailMessage

from .config import Settings

logger = logging.getLogger(__name__)


def send_email(settings: Settings, subject: str, html_body: str, text_body: str) -> None:
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = f"{settings.smtp_sender_name} <{settings.smtp_username}>"
    msg["To"] = settings.smtp_recipient
    msg.set_content(text_body)
    msg.add_alternative(html_body, subtype="html")

    logger.info("Sending email to %s via %s:%s", settings.smtp_recipient, settings.smtp_host, settings.smtp_port)

    with smtplib.SMTP(settings.smtp_host, settings.smtp_port, timeout=30) as server:
        server.starttls()
        server.login(settings.smtp_username, settings.smtp_password)
        server.send_message(msg)

    logger.info("Email sent successfully")
