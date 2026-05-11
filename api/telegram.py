import textwrap
import time
from typing import Dict, Literal

import requests
from md2tgmd import escape

from .config import BOT_TOKEN, default_photo_caption, default_video_caption, default_audio_caption, send_message_log, send_photo_log, unnamed_user
from .printLog import send_log

TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"

SEND_MESSAGE_MAX_LENGTH = int(4096 * 0.95)

_bot_username = None


def _split_by_words(text: str) -> list[str]:
    # textwrap.wrap automatically breaks the string at spaces
    # so words aren't cut in half.
    return textwrap.wrap(text, width=SEND_MESSAGE_MAX_LENGTH)


def _escape_text(text: str) -> str:
    try:
        return escape(text)
    except Exception:
        return text


def _get_bot_username():
    global _bot_username
    if _bot_username is None:
        try:
            r = requests.get(f"{TELEGRAM_API}/getMe", timeout=5)
            _bot_username = r.json().get("result", {}).get("username", "")
        except Exception:
            _bot_username = ""
    return _bot_username


def send_typing(chat_id):
    """Send typing action to show bot is processing."""
    try:
        requests.post(f"{TELEGRAM_API}/sendChatAction", data={"chat_id": chat_id, "action": "typing"}, timeout=2)
    except Exception:
        pass


def _send_message_api(chat_id, text, **kwargs):
    """send text message"""
    payload = {
        "chat_id": chat_id,
        "text": _escape_text(text),
        "parse_mode": "MarkdownV2",
        **kwargs,
    }
    r = requests.post(f"{TELEGRAM_API}/sendMessage", data=payload)
    print(f"Sent message: {text} to {chat_id}")
    send_log(f"{send_message_log}\n```json\n{str(r)}```")
    return r


def send_message(chat_id, text, **kwargs):
    """send text message"""
    results = []
    current_delay = 0.5
    chunks = _split_by_words(text)

    for chunk in chunks:
        result = _send_message_api(chat_id, chunk, **kwargs)
        results.append(result)
        # Short sleep to prevent hitting Telegram's burst rate limit
        if len(chunks) > 1:
            send_log(f"Sleeping for {current_delay:.1f}s...")
            time.sleep(current_delay)
            current_delay = min(current_delay + 0.1, 1)

    return results


def send_image_message(chat_id, text, imageID):
    """send image message"""
    payload = {
        "chat_id": chat_id,
        "caption": _escape_text(text),
        "parse_mode": "MarkdownV2",
        "photo": imageID,
    }
    r = requests.post(f"{TELEGRAM_API}/sendPhoto", data=payload)
    print(f"Sent imageMessage: {text} to {chat_id}")
    send_log(f"{send_photo_log}\n```json\n{str(r)}```")
    return r


def get_file_url(file_id: str) -> str:
    """Get Telegram file download URL."""
    r = requests.get(f"{TELEGRAM_API}/getFile?file_id={file_id}")
    file_path = r.json().get("result", {}).get("file_path")
    download_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"
    print(f"Found download link for {file_id}: {download_url}")
    return download_url


def get_file_content(file_url: str) -> bytes:
    """Download file content from URL."""
    response = requests.get(file_url)
    print(f"Content downloaded [{len(response.content)} bytes] from {file_url}")
    return response.content


UpdateType = Literal["command", "text", "voice", "video_note", "video", "audio", "photo", ""]


class Update:
    def __init__(self, update: Dict) -> None:
        self.update = update
        self.from_id = update["message"]["from"]["id"]
        self.chat_id = update["message"]["chat"]["id"]
        self.from_type = update["message"]["chat"]["type"]
        self.type: UpdateType = self._type()
        self.media_type = self._media_type()
        self.mime_type = self._mime_type()
        self.text = self._text()
        self.caption = self._caption()
        self.file_id = self._file_id()
        self.user_name = update["message"]["from"].get("username", f" [{unnamed_user}](tg://openmessage?user_id={self.from_id})")
        self.message_id: int = update["message"]["message_id"]
        self.chat_type = self.from_type
        self.is_group = self.chat_type in ("group", "supergroup")

    def is_mentioned(self) -> bool:
        bot_username = _get_bot_username()
        if not bot_username:
            return False
        msg = self.update["message"]
        entities = msg.get("entities") or msg.get("caption_entities") or []
        for entity in entities:
            if entity.get("type") == "mention":
                offset = entity["offset"]
                length = entity["length"]
                mention = msg.get("text", "")[offset:offset + length]
                if mention.lower() == f"@{bot_username}".lower():
                    return True
        text = msg.get("text", "")
        if text.lower().startswith(f"@{bot_username}".lower()):
            return True
        return False

    def replied_to_bot(self) -> bool:
        msg = self.update["message"]
        reply = msg.get("reply_to_message")
        if not reply:
            return False
        return reply.get("from", {}).get("is_bot", False)

    def _type(self) -> UpdateType:
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
        """Return media type if message contains media, else None."""
        if self.type in ("voice", "video_note", "video", "audio", "photo"):
            return self.type
        return None

    def _mime_type(self) -> str:
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
            return "image/jpeg"
        return "application/octet-stream"

    def _caption(self) -> str:
        """Get caption for media messages."""
        if self.media_type is not None:
            caption = self.update["message"].get("caption")
            if caption:
                return caption
            elif self.media_type == "photo":
                return default_photo_caption
            elif self.media_type in ("video", "video_note"):
                return default_video_caption
            else:
                return default_audio_caption
        return ""

    def _text(self) -> str:
        if self.type == "text":
            return self.update["message"]["text"]
        elif self.type == "command":
            text = self.update["message"]["text"]
            command = text[1:]
            return command
        return ""

    def _file_id(self) -> str:
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
