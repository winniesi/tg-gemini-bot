from io import BytesIO
from typing import Dict

import requests

from .config import BOT_TOKEN
from .gemini import ChatConversation, generate_text_with_image


class ChatManager:
    """setting up a basic conversation storage manager"""

    def __init__(self):
        self.chats: Dict[str, ChatConversation] = {}

    def _new_chat(self, username: str) -> ChatConversation:
        chat = ChatConversation()
        self.chats[username] = chat
        return chat

    def get_chat(self, username: str) -> ChatConversation:
        if self.chats.get(username) is None:
            return self._new_chat(username)
        return self.chats[username]


class ImageChatManger:
    def __init__(self, prompt, file_id: str) -> None:
        self.prompt = prompt
        self.file_id = file_id

    def tel_photo_url(self) -> str:
        """process telegram photo url"""
        r_file_id = requests.get(
            f"https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id={self.file_id}"
        )
        file_path = r_file_id.json().get("result").get("file_path")
        download_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"
        return download_url

    def photo_bytes(self) -> BytesIO:
        """get photo bytes"""
        photo_url = self.tel_photo_url()
        response = requests.get(photo_url)
        photo_bytes = BytesIO(response.content)
        return photo_bytes

    def send_image(self) -> str:
        response = generate_text_with_image(self.prompt, self.photo_bytes())
        return response
