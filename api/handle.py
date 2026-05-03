"""
All the chat that comes through the Telegram bot gets passed to the
handle_message function. This function checks out if the user has the
green light to chat with the bot. Once that's sorted, it figures out if
the user sent words or an image and deals with it accordingly.

For text messages, it fires up the ChatManager class that keeps track of
the back-and-forth with that user.

For media (photos, videos, audio), it uses MediaChatManager to process
the file through Gemini API.

Users can also reply to previously sent media with a custom prompt.
"""

from .auth import is_authorized
from .command import excute_command
from .context import ChatManager, MediaChatManager
from .telegram import Update, send_message, send_typing
from .printLog import send_log
from .config import *

chat_manager = ChatManager()


def handle_message(update_data):

    if "message" not in update_data:
        print(f"Ignoring non-message update: {list(update_data.keys())}")
        return

    update = Update(update_data)

    # Check if this is a reply to a media message
    is_reply = "reply_to_message" in update_data["message"]
    target_update = None
    target_update_media = False

    if is_reply:
        target_update = Update({"message": update_data["message"]["reply_to_message"]})
        target_update_media = update.type == "text" and target_update.media_type is not None

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

    # Handle media messages (photo, video, audio, voice, video_note)
    # OR text replies to media messages
    elif target_update_media or update.media_type is not None:
        send_typing(update.chat_id)
        media_update = target_update if target_update_media else update
        prompt = update.text if target_update_media else media_update.caption

        chat = MediaChatManager(
            media_update.media_type,
            media_update.mime_type,
            media_update.file_id,
            prompt,
        )
        response_text = chat.send_media()
        send_message(update.chat_id, response_text, reply_to_message_id=update.message_id)

        file_url = chat.file_url
        send_log(f"@{update.user_name} id:`{update.from_id}`[file]({file_url}),{the_accompanying_message_is}\n{prompt}\n{the_reply_content_is}\n{response_text}")

    elif update.type == "text":
        send_typing(update.chat_id)
        chat = chat_manager.get_chat(update.chat_id)
        anwser = chat.send_message(update.text)
        extra_text = f"\n\n{prompt_new_info}" if chat.history_length >= prompt_new_threshold * 2 else ""
        response_text = f"{anwser}{extra_text}"
        send_message(update.chat_id, response_text)
        dialogueLogarithm = int(chat.history_length / 2)
        send_log(f"@{update.user_name} id:`{update.from_id}`{the_content_sent_is}\n{update.text}\n{the_reply_content_is}\n{response_text}\n{the_logarithm_of_historical_conversations_is}{dialogueLogarithm}")

    else:
        send_message(update.chat_id, f"{unable_to_recognize_content_sent}\n\n/help")
        send_log(f"@{update.user_name} id:`{update.from_id}`{send_unrecognized_content}")
