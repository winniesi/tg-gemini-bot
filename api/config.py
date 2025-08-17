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
defaut_photo_caption = "描述这张图片"

""" Below is some text related to the user """
help_text = "You can send me text or pictures. When sending pictures, please include the text in the same message.\nTo use the group please @bot or reply to any message sent by the bot\n\n你可以向我发送文字或图片，发送图片请在同一条消息内携带文字\n群组使用请@机器人或回复机器人发送的任意消息"
command_list = "/new Start a new chat\n/get_my_info Get personal information\n/get_group_info Get group information (group only)\n/get_allowed_users Get the list of users that are allowed to use the bot (admin only)\n/get_allowed_groups Get the list of groups that are allowed to use the bot (admin only)\n/list_models list_models (admin only)\n/get_api_key Get the list of gemini's apikeys. It is currently useless. Multiple keys may be added to automatically switch in the future.(admin only)\n/help Get help\n/5g_test :)\n\n/new 开始新的聊天\n/get_my_info 获取个人信息\n/get_group_info 获取群组信息（仅群组可用）\n/get_allowed_users 获取允许使用机器人的用户列表（仅管理员可用）\n/get_allowed_groups 获取允许使用机器人的群组列表\n/list_models 列出模型（仅管理员可用）\n/get_api_key 获取gemini的apikey的列表，目前没有用，以后可能会添加多个key自动切换（仅管理员可用）\n/help 获取帮助\n/5g_test :)"
admin_auch_info = "You are not the administrator or your administrator ID is set incorrectly!!!\n你不是管理员或你的管理员id设置错误！！！"
debug_mode_info = "Debug mode is not enabled!"
command_format_error_info = "Command format error\n命令格式错误"
command_invalid_error_info = "Invalid command, use /help for help\n无效的指令，使用/help来获取帮助"
user_no_permission_info = "You are not allowed to use this bot.\n您无权使用此机器人。"
group_no_permission_info = "This group does not have permission to use this robot.\n此群无权使用此机器人。"
gemini_err_info = f"Something went wrong!\nThe content you entered may be inappropriate, please modify it and try again\n您输入的内容可能不合适，请修改后重试"
new_chat_info = "We're having a fresh chat.\n我们正在进行新的聊天。"
prompt_new_info = "Type /new to kick off a new chat.\n输入 /new 开始新的聊天。"
unable_to_recognize_content_sent = "The content you sent is not recognized!\n无法识别您发送的内容!"

""" Below is some text related to the log """
send_message_log = "发送消息 返回的内容为:"
send_photo_log = "发送图片 返回的内容为:"
unnamed_user = "未命名用户"
unnamed_group = "未命名群组"
event_received = "收到事件"
group = "群group"
the_content_sent_is = "发送的内容为:"
the_reply_content_is = "回复的内容为:"
the_accompanying_message_is = "附带的消息为:"
the_logarithm_of_historical_conversations_is = "历史对话对数为:"
no_rights_to_use = "无权使用"
send_unrecognized_content = "发送无法识别的内容"



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
