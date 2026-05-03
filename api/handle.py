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

from .auth import is_authorized, is_group_allowed
from .command import excute_command
from .context import ChatManager, MediaChatManager
from .telegram import Update, send_message, send_typing, _get_bot_username
from .printLog import send_log
from .config import *

chat_manager = ChatManager()


def _strip_bot_mention(text):
    bot_username = _get_bot_username()
    if bot_username and text.lower().startswith(f"@{bot_username}".lower()):
        text = text[len(f"@{bot_username}"):].lstrip()
    return text


def handle_message(update_data):

    if "message" not in update_data:
        print(f"Ignoring non-message update: {list(update_data.keys())}")
        return

    msg = update_data["message"]

    # Handle bot joining a group
    if "new_chat_members" in msg:
        for member in msg["new_chat_members"]:
            if member.get("is_bot") and member.get("username") == _get_bot_username():
                chat_id = msg["chat"]["id"]
                send_message(chat_id, f"{bot_joined_group}\n\n`{chat_id}`")
                send_log(f"Bot joined group {chat_id}")
        return

    update = Update(update_data)

    # Group chat logic
    if update.is_group:
        # Only respond when @mentioned or replying to bot
        if not update.is_mentioned() and not update.replied_to_bot():
            return

        # Check if group is authorized
        if not is_group_allowed(update.chat_id):
            send_message(update.chat_id, f"{group_not_allowed}\n\n`{update.chat_id}`")
            send_log(f"Unauthorized group {update.chat_id}, user @{update.user_name}")
            return

        # Strip @mention from text before processing
        if update.type == "text":
            update.text = _strip_bot_mention(update.text)
        elif update.type == "command":
            update.text = _strip_bot_mention(update.text)
            if not update.text.startswith("/"):
                update.text = "/" + update.text

    # Private chat: check user authorization
    elif not is_authorized(update.from_id, update.user_name):
        send_message(update.from_id, f"{user_no_permission_info}\nID:`{update.from_id}`")
        send_log(f"@{update.user_name} id:`{update.from_id}`{no_rights_to_use},{the_content_sent_is}\n{update.text}")
        return

    # Check if this is a reply to a media message
    is_reply = "reply_to_message" in msg
    target_update = None
    target_update_media = False

    if is_reply:
        target_update = Update({"message": msg["reply_to_message"]})
        target_update_media = update.type == "text" and target_update.media_type is not None

    log = f"{event_received}\n@{update.user_name} id:`{update.from_id}`\n{the_content_sent_is}\n{update.text}\n```json\n{update_data}```"
    send_log(log)

    if update.type == "command":
        response_text = excute_command(update.from_id, update.text, update.chat_id, is_group=update.is_group)
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
