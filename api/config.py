import os
from re import split

""" Required """

BOT_TOKEN = os.environ.get("BOT_TOKEN")
GOOGLE_API_KEY = split(r'[,;，；]+', os.environ.get("GOOGLE_API_KEY"))

""" Optional """

ALLOWED_USERS = split(r'[ ,;，；]+', os.getenv("ALLOWED_USERS", '').replace("@", "").lower())
ALLOWED_GROUPS = [g.strip() for g in split(r'[,;，；]+', os.getenv("ALLOWED_GROUPS", '')) if g.strip()]

SYSTEM_INSTRUCTION = os.getenv("SYSTEM_INSTRUCTION", "")
DEFAULT_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

# After setting up 3 rounds of dialogue, prompt the user to start a new dialogue
prompt_new_threshold = int(3)

# The default prompt when the photo has no accompanying text
default_photo_caption = "describe this picture"
# The default prompt for video messages
default_video_caption = "describe what is happening in this video"
# The default prompt for audio/voice messages
default_audio_caption = "transcribe this audio"

""" Below is some text related to the user """
help_text = "You can send me text or pictures. When sending pictures, please include the text in the same message."
command_list = (
    "/new — Start a new chat\n"
    "/get_model — Show current model\n"
    "/set_model — Switch Gemini model\n"
    "/list_models — List available models\n"
    "/get_my_info — Get your Telegram ID\n"
    "/help — Get help"
)
command_format_error_info = "Command format error"
command_invalid_error_info = "Invalid command, use /help for help"
user_no_permission_info = "You are not allowed to use this bot."
gemini_err_info = "Something went wrong! Please try again later."
new_chat_info = "We're having a fresh chat."
prompt_new_info = "Type /new to kick off a new chat."
unable_to_recognize_content_sent = "The content you sent is not recognized!"
group_not_allowed = "This group is not authorized. Please add the following group ID to ALLOWED_GROUPS environment variable and redeploy:"
bot_joined_group = "Hello! Please add the following group ID to ALLOWED_GROUPS environment variable and redeploy to enable this bot:"

""" Below is some text related to the log """
send_message_log = "Send a message. The content returned is:"
send_photo_log = "Send a photo. The content returned is:"
unnamed_user = "UnnamedUser"
event_received = "event received"
the_content_sent_is = "The content sent is:"
the_reply_content_is = "The reply content is:"
the_accompanying_message_is = "The accompanying message is:"
the_logarithm_of_historical_conversations_is = "The logarithm of historical conversations is:"
no_rights_to_use = "No rights to use"
send_unrecognized_content = "Send unrecognized content"


""" read https://ai.google.dev/api/rest/v1/GenerationConfig """
generation_config = {
    "max_output_tokens": 8192,
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
