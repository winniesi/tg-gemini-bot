from .auth import is_authorized
from .context import ChatManager, ImageChatManger
from .telegram import Update, send_message

chat_manager = ChatManager()


def handle_message(update_data):
    update = Update(update_data)
    authorized = is_authorized(update.from_id, update.user_name)
    if not authorized:
        send_message(update.from_id, "😫 You are not allowed to use this bot.")
        return
    if update.type == "text":
        chat = chat_manager.get_chat(update.from_id)
        anwser = chat.send_message(update.text)
        extra_text = (
            "\n\nType /new to kick off a new chat." if chat.history_length >= 2 else ""
        )
        response_text = f"{anwser}{extra_text}"
        send_message(update.from_id, response_text)
    elif update.type == "photo":
        chat = ImageChatManger(update.photo_caption, update.file_id)
        response_text = chat.send_image()
        send_message(update.from_id, response_text)
    else:
        send_message(update.from_id, "GEMINI can currently handle only text and image.")
