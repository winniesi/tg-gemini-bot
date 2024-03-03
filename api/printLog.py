import requests
from md2tgmd import escape

from .config import IS_DEBUG_MODE, ADMIN_ID, BOT_TOKEN

admin_id = ADMIN_ID
is_debug_mode =IS_DEBUG_MODE

TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"

def send_log(text):
    if is_debug_mode == "1":
            payload = {
            "chat_id": admin_id,
            "text": escape(text),
            "parse_mode": "MarkdownV2",
        }
            requests.post(f"{TELEGRAM_API}/sendMessage", data=payload)


def send_image_log(text,imageID):
    if is_debug_mode == "1":
        payload = {
        "chat_id": admin_id,
        "caption": escape(text),
        "parse_mode": "MarkdownV2",
        "photo": imageID
    }
        requests.post(f"{TELEGRAM_API}/sendPhoto", data=payload)

