from typing import Dict

import requests
from md2tgmd import escape

from .config import BOT_TOKEN, defaut_photo_caption, send_message_log, send_photo_log, unnamed_user, unnamed_group
from .printLog import send_log

TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"


def send_message(chat_id, text, **kwargs):
    """send text message"""
    payload = {
        "chat_id": chat_id,
        "text": escape(text),
        "parse_mode": "MarkdownV2",
        **kwargs,
    }
    r = requests.post(f"{TELEGRAM_API}/sendMessage", data=payload)
    print(f"Sent message: {text} to {chat_id}")
    send_log(f"{send_message_log}\n```json\n{str(r)}```")
    return r


def send_imageMessage(chat_id, text, imageID):
    """send image message"""
    payload = {
        "chat_id": chat_id,
        "caption": escape(text),
        "parse_mode": "MarkdownV2",
        "photo": imageID
    }
    r = requests.post(f"{TELEGRAM_API}/sendPhoto", data=payload)
    print(f"Sent imageMessage: {text} to {chat_id}")
    send_log(f"{send_photo_log}\n```json\n{str(r)}```")
    return r


class Update:
    def __init__(self, update: Dict) -> None:
        self.update = update
        self.from_id = update["message"]["from"]["id"]
        self.chat_id = update["message"]["chat"]["id"]
        self.from_type = update["message"]["chat"]["type"]
        self.is_group: bool = self._is_group()
        self.type = self._type()
        self.text = self._text()
        self.photo_caption = self._photo_caption()
        self.file_id = self._file_id()
        #self.user_name = update["message"]["from"]["username"]
        self.user_name = update["message"]["from"].get("username", f" [{unnamed_user}](tg://openmessage?user_id={self.from_id})")
        self.group_name = update["message"]["chat"].get("username", f" [{unnamed_group}](tg://openmessage?chat_id={str(self.chat_id)[4:]})")
        self.message_id: int = update["message"]["message_id"]

    def _is_group(self):
        if self.from_type == "supergroup":
            return True
        return False

    def _type(self):
        if "text" in self.update["message"]:
            text = self.update["message"]["text"]
            if text.startswith("/") and not text.startswith("/new"):
                return "command"
            return "text"
        elif "photo" in self.update["message"]:
            return "photo"
        else:
            return ""

    def _photo_caption(self):
        if self.type == "photo":
            return self.update["message"].get("caption", defaut_photo_caption)
        return ""

    def _text(self):
        if self.type == "text":
            return self.update["message"]["text"]
        elif self.type == "command":
            text = self.update["message"]["text"]
            command = text[1:]
            return command
        return ""

    def _file_id(self):
        if self.type == "photo":
            return self.update["message"]["photo"][-1]["file_id"]
        return ""
