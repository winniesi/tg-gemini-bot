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
from .context import ChatManager, MediaChatManager
from .telegram import Update, send_message, send_reaction
from .printLog import send_log
from .config import *

chat_manager = ChatManager()


def handle_message(update_data):

    #try:
    #    update = update_data["message"]["from"]["id"]
    #except  Exception as e:
    #    strupdate_data = str(update_data)
    #    start = strupdate_data.find("\'id\': ")
    #    from_id = strupdate_data[start+6:start+16]
    #    send_message(from_id, f"You have sent an unknown event. Please send the following information to the bot administrator.\n您发送了一个未知事件，请把下面信息发送至bot管理员。\n\n{update_data}\n{e}")
    #    send_message(admin_id, f"收到了一个未知事件，原文为：\n{update_data}\n错误为：\n{e}")

    update = Update(update_data)

    is_reply = "reply_to_message" in update_data["message"]
    target_update = (
        Update({"message": update_data["message"]["reply_to_message"]})
        if is_reply
        else None
    )
    target_update_media = (
        update.type == "text" and is_reply and target_update.media_type is not None
    )

    if update.is_group:
        log = f"{event_received}\n@{update.user_name} id:`{update.from_id}` {group} @{update.group_name} id:`{update.chat_id}`\n{the_content_sent_is}\n{update.text}\n```json\n{update_data}```"
    else:
        log = f"{event_received}\n@{update.user_name} id:`{update.from_id}`\n{the_content_sent_is}\n{update.text}\n```json\n{update_data}```"
    send_log(log)
    authorized = is_authorized(
        update.is_group,
        update.from_id,
        update.user_name,
        update.chat_id,
        update.group_name,
    )

    send_reaction(update.chat_id, update.message_id, "👍")

    if update.type == "command":
        response_text = excute_command(update.from_id, update.text, update.from_type, update.chat_id)
        if response_text!= "":
            send_message(update.chat_id, response_text)
            if update.is_group :
                log = f"@{update.user_name} id:`{update.from_id}` {group} @{update.group_name} id:`{update.chat_id}`{the_content_sent_is}\n{update.text}\n{the_reply_content_is}\n{response_text}"
            else:
                log = f"@{update.user_name} id:`{update.from_id}`{the_content_sent_is}\n{update.text}\n{the_reply_content_is}\n{response_text}"
            send_log(log)

    elif not authorized:
        if update.is_group:
            send_message(update.chat_id, f"{group_no_permission_info}\nID:`{update.chat_id}`")
            log = f"@{update.user_name} id:`{update.from_id}` {group} @{update.group_name} id:`{update.chat_id}`{no_rights_to_use},{the_content_sent_is}\n{update.text}"
        else:
            send_message(
            update.from_id, f"{user_no_permission_info}\nID:`{update.from_id}`")
            log = f"@{update.user_name} id:`{update.from_id}`{no_rights_to_use},{the_content_sent_is}\n{update.text}"
        send_log(log)
        return

    elif target_update_media or update.media_type is not None:
        media_update = target_update if target_update_media else update
        prompt = (
            update.text
            if is_reply
            else (media_update.caption or "Transcribe or describe this.")
        )
        chat = MediaChatManager(
            media_update.media_type,
            media_update.mime_type,
            media_update.file_id,
            prompt,
        )
        response_text = chat.send_media()
        print(f"update.message_id {update.message_id}")
        # Use the reply_to_message_id parameter to let the bot reply to
        # a specific image.
        send_message(
            update.chat_id, response_text, reply_to_message_id=update.message_id
        )

        file_url = chat.file_url
        if update.is_group:
            log = f"@{update.user_name} id:`{update.from_id}` {group} @{update.group_name} id:`{update.chat_id}`[file]({file_url}),{the_accompanying_message_is}\n{prompt}\n{the_reply_content_is}\n{response_text}"
        else:
            log = f"@{update.user_name} id:`{update.from_id}`[file]({file_url}),{the_accompanying_message_is}\n{prompt}\n{the_reply_content_is}\n{response_text}"
        send_log(log)

    elif update.type == "text":
        if update.is_group and GROUP_MODE == "2":
            history_id = update.from_id
        else:
            history_id = update.chat_id
        chat = chat_manager.get_chat(history_id)
        anwser = chat.send_message(update.text)
        extra_text = (
            f"\n\n{prompt_new_info}" if chat.history_length >= prompt_new_threshold*2 else ""
        )
        response_text = f"{anwser}{extra_text}"
        send_message(update.chat_id, response_text)
        dialogueLogarithm = int(chat.history_length/2)
        if update.is_group:
            log = f"@{update.user_name} id:`{update.from_id}` {group} @{update.group_name} id:`{update.chat_id}`{the_content_sent_is}\n{update.text}\n{the_reply_content_is}\n{response_text}\n{the_logarithm_of_historical_conversations_is}{dialogueLogarithm}"
        else:
            log = f"@{update.user_name} id:`{update.from_id}`{the_content_sent_is}\n{update.text}\n{the_reply_content_is}\n{response_text}\n{the_logarithm_of_historical_conversations_is}{dialogueLogarithm}"
        send_log(log)

    else:
        send_message(
            update.chat_id, f"{unable_to_recognize_content_sent}\n\n/help")
        if update.is_group:
            log = f"@{update.user_name} id:`{update.from_id}` {group} @{update.group_name} id:`{update.chat_id}`{send_unrecognized_content}"
        else:
            log = f"@{update.user_name} id:`{update.from_id}`{send_unrecognized_content}"
        send_log(log)
