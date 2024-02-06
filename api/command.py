from time import sleep

import google.generativeai as genai

from .auth import is_admin
from .config import ALLOWED_USERS,IS_DEBUG_MODE,GOOGLE_API_KEY
from .printLog import send_log
from .telegram import send_message

admin_auch_info = "You are not the administrator or your administrator ID is set incorrectly!!!"
debug_mode_info = "Debug mode is not enabled!"

def help():
    help_text = "You can send me text or pictures. When sending pictures, please include the text in the same message."
    command_list = "/new Start a new chat\n/get_my_info Get personal information\n/get_allowed_users Get the list of users allowed to use robots (available only to admin)\n/list_models list_models (available only to admin)\n/get_api_key (available only to admin)"
    result = f"{help_text}\n\n{command_list}"
    return result

def list_models():
    for m in genai.list_models():
        send_log(str(m))
        if 'generateContent' in m.supported_generation_methods:
            send_log(str(m.name))
    return ""

def get_allowed_users():
    send_log(f"```json\n{ALLOWED_USERS}```")
    return ""


def get_API_key():
    send_log(f"```json\n{GOOGLE_API_KEY}```")
    return ""

def speed_test(id):
    send_message(id, "开始测速")
    sleep(5)
    return "测试完成，您的5G速度为：\n**114514B/s**"

def send_message_test(id, command):
    if not is_admin(id):
        return admin_auch_info
    a = command.find(" ")
    b = command.find(" ", a + 1)
    if a == -1 or b == -1:
        return "Command format error"
    to_id = command[a+1:b]
    text = command[b+1:]
    try:
        send_message(to_id, text)
    except Exception as e:
        send_log(f"err:\n{e}")
        return
    send_log("success")
    return ""

def excute_command(from_id, command):
    if command == "start" or command == "help":
        return help()

    elif command == "get_my_info":
        result = f"your telegram id is: `{from_id}`"
        return result

    elif command == "5g_test":
        return speed_test(from_id)

    elif command.startswith("send_message"):
        return send_message_test(from_id, command)

    elif command in ["get_allowed_users", "get_api_key", "list_models"]:
        if not is_admin(from_id):
            return admin_auch_info
        if IS_DEBUG_MODE == "0":
            return debug_mode_info

        if command == "get_allowed_users":
            return get_allowed_users()
        elif command == "get_api_key":
            return get_API_key()
        elif command == "list_models":
            return list_models()

    else:
        result = "Invalid command, use /help for help"
        return result
