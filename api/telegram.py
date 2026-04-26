from typing import Dict, Literal

import requests
from md2tgmd import escape

from .config import (
    BOT_TOKEN,
    default_photo_caption,
    default_media_caption,
    send_message_log,
    send_photo_log,
    unnamed_user,
    unnamed_group,
)
from .printLog import send_log

TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"


def send_message(chat_id, text, **kwargs):
    """send text message"""
    print(f"Sending message: {text} to {chat_id}")
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
        "photo": imageID,
    }
    r = requests.post(f"{TELEGRAM_API}/sendPhoto", data=payload)
    print(f"Sent imageMessage: {text} to {chat_id}")
    send_log(f"{send_photo_log}\n```json\n{str(r)}```")
    return r


def send_reaction(chat_id, message_id, emoji="👍"):
    url = f"{TELEGRAM_API}/setMessageReaction"
    payload = {
        "chat_id": chat_id,
        "message_id": message_id,
        "reaction": [{"type": "emoji", "emoji": emoji}],
        "is_big": False,
    }
    return requests.post(url, json=payload)


def get_file_url(file_id) -> str:
    """process telegram photo url"""
    r_file_id = requests.get(f"{TELEGRAM_API}/getFile?file_id={file_id}")
    file_path = r_file_id.json().get("result").get("file_path")
    download_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"
    print(f"Found download link for {file_id}: {download_url}")
    return download_url


def get_file_content(file_url):
    file_res = requests.get(file_url)
    print(f"Content downloaded [{len(file_res.content)}] from {file_url}")
    print(f"Content: {file_res.content}")
    return file_res.content


UpdateType = Literal[
    "command", "text", "voice", "video_note", "video", "audio", "photo", ""
]


class Update:
    def __init__(self, update: Dict) -> None:
        self.update = update
        self.from_id = update["message"]["from"]["id"]
        self.chat_id = update["message"]["chat"]["id"]
        self.from_type = update["message"]["chat"]["type"]
        self.is_group: bool = self._is_group()
        self.type: UpdateType = self._type()
        self.media_type = self._media_type()
        self.mime_type = self._mime_type()
        self.text = self._text()
        self.caption = self._caption()
        self.file_id = self._file_id()
        # self.user_name = update["message"]["from"]["username"]
        self.user_name = update["message"]["from"].get(
            "username", f" [{unnamed_user}](tg://openmessage?user_id={self.from_id})"
        )
        self.group_name = update["message"]["chat"].get(
            "username",
            f" [{unnamed_group}](tg://openmessage?chat_id={str(self.chat_id)[4:]})",
        )
        self.message_id: int = update["message"]["message_id"]

    def _is_group(self):
        if self.from_type == "supergroup":
            return True
        return False

    def _type(self):
        msg = self.update["message"]
        if "text" in msg:
            text = msg["text"]
            if text.startswith("/") and not text.startswith("/new"):
                return "command"
            return "text"
        elif "voice" in msg:
            return "voice"
        elif "video_note" in msg:
            return "video_note"
        elif "video" in msg:
            return "video"
        elif "audio" in msg:
            return "audio"
        elif "photo" in msg:
            return "photo"
        else:
            return ""

    def _media_type(self):
        return self.type if self.type != "text" and self.type != "command" else None

    def _caption(self):
        if self.media_type is not None:
            caption = self.update["message"].get("caption")
            if caption is not None and caption != "":
                return caption
            elif self.media_type == "photo":
                return default_photo_caption
            else:
                return default_media_caption
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
        msg = self.update["message"]
        if self.type == "voice":
            return msg["voice"]["file_id"]
        elif self.type == "video_note":
            return msg["video_note"]["file_id"]
        elif self.type == "video":
            return msg["video"]["file_id"]
        elif self.type == "audio":
            return msg["audio"]["file_id"]
        elif self.type == "photo":
            return msg["photo"][-1]["file_id"]
        return ""

    def _mime_type(self):
        msg = self.update["message"]
        if self.type == "voice":
            return msg["voice"].get("mime_type", "audio/ogg")
        elif self.type == "video_note":
            return msg["video_note"].get("mime_type", "video/mp4")
        elif self.type == "video":
            return msg["video"].get("mime_type", "video/mp4")
        elif self.type == "audio":
            return msg["audio"].get("mime_type", "audio/mpeg")
        elif self.type == "photo":
            return msg["photo"][-1].get("mime_type", "image/jpeg")
        return "application/octet-stream"
