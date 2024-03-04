"""
The class ChatManager manages all users and their conversations in the
form of a dictionary.

Each user has a ChatConversation instance, which may include multiple
previous conversations of the user (provided by the Google Gemini API).

The class ImageChatManager is rather simple, as the images in Gemini Pro
do not have a contextual environment. This class performs some tasks
such as obtaining photos to addresses and so on.
"""
from io import BytesIO
from typing import Dict

import requests

from .config import BOT_TOKEN
from .gemini import ChatConversation, generate_text_with_image


class ChatManager:
    """setting up a basic conversation storage manager"""

    def __init__(self):
        self.chats: Dict[int, ChatConversation] = {}

    def _new_chat(self, history_id: int) -> ChatConversation:
        chat = ChatConversation()
        self.chats[history_id] = chat
        return chat

    def get_chat(self, history_id: int) -> ChatConversation:
        if self.chats.get(history_id) is None:
            return self._new_chat(history_id)
        return self.chats[history_id]


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
