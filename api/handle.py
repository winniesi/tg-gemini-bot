"""
All the chat that comes through the Telegram bot gets passed to the
handle_message function. This function checks out if the user has the
green light to chat with the bot. Once that's sorted, it figures out if
the user sent words or an image and deals with it accordingly.

For text messages, it fires up the ChatManager class that keeps track of
the back-and-forth with that user.

As for images, in Gemini pro, they're context-free, so you can handle
them pretty straight-up without much fuss.
"""

from .auth import is_authorized
from .command import excute_command
from .context import ChatManager, ImageChatManger
from .telegram import Update, send_message
from .printLog import send_log, send_image_log
from .config import *

chat_manager = ChatManager()


def handle_message(update_data):

    if "message" not in update_data:
        print(f"Ignoring non-message update: {list(update_data.keys())}")
        return

    update = Update(update_data)
    log = f"{event_received}\n@{update.user_name} id:`{update.from_id}`\n{the_content_sent_is}\n{update.text}\n```json\n{update_data}```"
    send_log(log)

    if not is_authorized(update.from_id, update.user_name):
        send_message(update.from_id, f"{user_no_permission_info}\nID:`{update.from_id}`")
        send_log(f"@{update.user_name} id:`{update.from_id}`{no_rights_to_use},{the_content_sent_is}\n{update.text}")
        return

    if update.type == "command":
        response_text = excute_command(update.from_id, update.text, update.chat_id)
        if response_text != "":
            send_message(update.chat_id, response_text)
            send_log(f"@{update.user_name} id:`{update.from_id}`{the_content_sent_is}\n{update.text}\n{the_reply_content_is}\n{response_text}")

    elif update.type == "text":
        chat = chat_manager.get_chat(update.chat_id)
        anwser = chat.send_message(update.text)
        extra_text = f"\n\n{prompt_new_info}" if chat.history_length >= prompt_new_threshold * 2 else ""
        response_text = f"{anwser}{extra_text}"
        send_message(update.chat_id, response_text)
        dialogueLogarithm = int(chat.history_length / 2)
        send_log(f"@{update.user_name} id:`{update.from_id}`{the_content_sent_is}\n{update.text}\n{the_reply_content_is}\n{response_text}\n{the_logarithm_of_historical_conversations_is}{dialogueLogarithm}")

    elif update.type == "photo":
        chat = ImageChatManger(update.photo_caption, update.file_id)
        response_text = chat.send_image()
        send_message(update.chat_id, response_text, reply_to_message_id=update.message_id)
        photo_url = chat.tel_photo_url()
        imageID = update.file_id
        send_log(f"@{update.user_name} id:`{update.from_id}`[photo]({photo_url}),{the_accompanying_message_is}\n{update.photo_caption}\n{the_reply_content_is}\n{response_text}")
        send_image_log("", imageID)

    else:
        send_message(update.chat_id, f"{unable_to_recognize_content_sent}\n\n/help")
        send_log(f"@{update.user_name} id:`{update.from_id}`{send_unrecognized_content}")
