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

from .gemini import ChatConversation, generate_text_with_image, generate_text_with_file
from .telegram import get_file_content, get_file_url


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

    def photo_bytes(self) -> BytesIO:
        """get photo bytes"""
        photo_url = get_file_url(self.file_id)
        response = requests.get(photo_url)
        photo_bytes = BytesIO(response.content)
        return photo_bytes

    def send_image(self) -> str:
        response = generate_text_with_image(self.prompt, self.photo_bytes())
        return response


class MediaChatManager:
    def __init__(self, media_type, mime_type, file_id, prompt):
        self.media_type = media_type
        self.mime_type = mime_type
        self.file_id = file_id
        self.prompt = prompt
        self.file_url = get_file_url(self.file_id)

    def send_media(self):
        file_bytes = get_file_content(self.file_url)

        response = generate_text_with_file(self.prompt, file_bytes, self.mime_type)
        return response
