from typing import Dict

import requests
from md2tgmd import escape

from .config import BOT_TOKEN

TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"


def send_message(chat_id, text):
    """send text message"""
    payload = {
        "chat_id": chat_id,
        "text": escape(text),
        "parse_mode": "MarkdownV2",
    }
    r = requests.post(f"{TELEGRAM_API}/sendMessage", data=payload)
    print(f"Sent message: {text} to {chat_id}")
    return r


class Update:
    def __init__(self, update: Dict) -> None:
        self.update = update
        self.from_id = update["message"]["from"]["id"]
        self.type = self._type()
        self.text = self._text()
        self.photo_caption = self._photo_caption()
        self.file_id = self._file_id()
        self.user_name = update["message"]["from"]["username"]

    def _type(self):
        if "text" in self.update["message"]:
            return "text"
        elif "photo" in self.update["message"]:
            return "photo"
        else:
            return ""

    def _photo_caption(self):
        if self.type == "photo":
            return self.update["message"].get("caption", "describe the photo")
        return ""

    def _text(self):
        if self.type == "text":
            return self.update["message"]["text"]
        return ""

    def _file_id(self):
        if self.type == "photo":
            return self.update["message"]["photo"][0]["file_id"]
        return ""
