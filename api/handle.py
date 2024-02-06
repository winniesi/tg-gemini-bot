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
from .printLog import send_log,send_image_log

chat_manager = ChatManager()


def handle_message(update_data):
    update = Update(update_data)
    authorized = is_authorized(update.from_id, update.user_name)
    send_log(f"event received\n@{update.user_name} id:`{update.from_id}`\nThe content sent is:\n{update.text}\n```json\n{update_data}```")

    if update.type == "command":
        response_text = excute_command(update.from_id, update.text)
        if response_text!= "":
            send_message(update.from_id, response_text)
            log = f"@{update.user_name} id:`{update.from_id}`The command sent is:\n{update.text}\nThe reply content is:\n{response_text}"
            send_log(log)


    elif not authorized:
        send_message(
            update.from_id, f"You are not allowed to use this bot.\nID:`{update.from_id}`")

        log = f"@{update.user_name} id:`{update.from_id}`No rights to use,The content sent is:\n{update.text}"

        send_log(log)
        return

    elif update.type == "text":
        chat = chat_manager.get_chat(update.from_id)
        anwser = chat.send_message(update.text)
        extra_text = (
            "\n\nType /new to kick off a new chat." if chat.history_length > 5 else ""
        )
        response_text = f"{anwser}{extra_text}"
        send_message(update.from_id, response_text)

        dialogueLogarithm = int(chat.history_length/2)
        log = f"@{update.user_name} id:`{update.from_id}`The content sent is:\n{update.text}\nThe reply content is:\n{response_text}\nThe logarithm of historical conversations is:{dialogueLogarithm}"
        send_log(log)

    elif update.type == "photo":
        chat = ImageChatManger(update.photo_caption, update.file_id)
        response_text = chat.send_image()
        print(f"update.message_id {update.message_id}")
        # Use the reply_to_message_id parameter to let the bot reply to
        # a specific image.
        send_message(
            update.from_id, response_text, reply_to_message_id=update.message_id
        )

        photo_url = chat.tel_photo_url()
        imageID = update.file_id
        log = f"@{update.user_name} id:`{update.from_id}`[photo]({photo_url}),The accompanying message is:\n{update.photo_caption}\nThe reply content is:\n{response_text}"
        send_image_log("", imageID)
        send_log(log)

    else:
        send_message(
            update.from_id, "The content you sent is not recognized\n\n/help")

        log = f"@{update.user_name} id:`{update.from_id}`Send unrecognized content"

        send_log(log)
