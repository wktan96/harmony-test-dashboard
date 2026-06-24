import os
import logging
import httpx
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

logger = logging.getLogger("app.notifier")

async def send_telegram_notification(message: str):
    """Sends a markdown-formatted message to the configured Telegram chat."""
    if not TOKEN or not CHAT_ID:
        logger.warning("Telegram notification skipped: TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID missing in .env")
        return

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, timeout=5.0)
            if response.status_code != 200:
                logger.error(f"Telegram API responded with error: {response.text}")
    except Exception as e:
        logger.error(f"Failed to send Telegram notification: {e}")