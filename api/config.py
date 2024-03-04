import os
from re import split

""" Required """

BOT_TOKEN = os.environ.get("BOT_TOKEN")
GOOGLE_API_KEY = split(r'[ ,;，；]+', os.environ.get("GOOGLE_API_KEY"))

""" Optional """

ALLOWED_USERS = split(r'[ ,;，；]+', os.getenv("ALLOWED_USERS", '').replace("@", "").lower())
ALLOWED_GROUPS = split(r'[ ,;，；]+', os.getenv("ALLOWED_GROUPS", '').replace("@", "").lower())

#Whether to push logs and enable some admin commands
IS_DEBUG_MODE = os.getenv("IS_DEBUG_MODE", '0')
#The target account that can execute administrator instructions and log push can use /get_my_info to obtain the ID.
ADMIN_ID = os.getenv("ADMIN_ID", "1234567890")

#Determines whether to verify identity. If 0, anyone can use the bot. It is enabled by default.
AUCH_ENABLE = os.getenv("AUCH_ENABLE", "1")

#"1"to use the same chat history in the group, "2"to record chat history individually for each person
GROUP_MODE = os.getenv("GROUP_MODE=", "1")

#After setting up 3 rounds of dialogue, prompt the user to start a new dialogue
prompt_new_threshold = int(3)

#The default prompt when the photo has no accompanying text
defaut_photo_caption = "describe this picture"

""" Below is some text related to the user """
help_text = "You can send me text or pictures. When sending pictures, please include the text in the same message.\nTo use the group please @bot or reply to any message sent by the bot"
command_list = "/new Start a new chat\n/get_my_info Get personal information\n/get_group_info Get group information (group only)\n/get_allowed_users Get the list of users that are allowed to use the bot (admin only)\n/get_allowed_groups Get the list of groups that are allowed to use the bot (admin only)\n/list_models list_models (admin only)\n/get_api_key Get the list of gemini's apikeys. It is currently useless. Multiple keys may be added to automatically switch in the future.(admin only)\n/help Get help\n/5g_test :)"
admin_auch_info = "You are not the administrator or your administrator ID is set incorrectly!!!"
debug_mode_info = "Debug mode is not enabled!"
command_format_error_info = "Command format error"
command_invalid_error_info = "Invalid command, use /help for help"
user_no_permission_info = "You are not allowed to use this bot."
group_no_permission_info = "This group does not have permission to use this robot."
gemini_err_info = f"Something went wrong!\nThe content you entered may be inappropriate, please modify it and try again"
new_chat_info = "We're having a fresh chat."
prompt_new_info = "Type /new to kick off a new chat."
unable_to_recognize_content_sent = "The content you sent is not recognized!"

""" Below is some text related to the log """
send_message_log = "Send a message. The content returned is:"
send_photo_log = "Send a photo. The content returned is:"
unnamed_user = "UnnamedUser"
unnamed_group = "UnnamedGroup"
event_received = "event received"
group = "group"
the_content_sent_is = "The content sent is:"
the_reply_content_is = "The reply content is:"
the_accompanying_message_is = "The accompanying message is:"
the_logarithm_of_historical_conversations_is = "The logarithm of historical conversations is:"
no_rights_to_use = "No rights to use"
send_unrecognized_content = "Send unrecognized content"


""" read https://ai.google.dev/api/rest/v1/GenerationConfig """
generation_config = {
    "max_output_tokens": 1024,
}

""" read https://ai.google.dev/api/rest/v1/HarmCategory """
safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE"
    },
]
