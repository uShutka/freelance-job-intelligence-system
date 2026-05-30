import logging
import os

import pandas as pd

logger = logging.getLogger(__name__)


def build_job_alert(job: pd.Series | dict[str, object]) -> str:
    data = job.to_dict() if hasattr(job, "to_dict") else job
    skills = ", ".join(data.get("skills", []))
    return (
        "Job market intelligence alert\n"
        f"{data['title']}\n"
        f"Score: {data['score']}/100 | Rate: ${data.get('hourly_rate') or 'n/a'}/h | Level: {data['level']}\n"
        f"Skills: {skills}\n"
        f"Source: {data['source']} | {data.get('url', '')}"
    )


def send_telegram_alert(message: str) -> bool:
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        logger.info("Telegram credentials are not configured; alert was logged only")
        return False
    logger.info("Telegram alert prepared", extra={"chat_id": chat_id, "message_size": len(message)})
    return True
