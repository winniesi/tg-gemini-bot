from time import sleep
import requests as http_requests

from .auth import is_admin
from .config import *
from .printLog import send_log
from .telegram import send_message
from .gemini import client, set_model, get_current_model

def help():
    result = f"{help_text}\n\n{command_list}"
    return result

def list_models():
    models = []
    for m in client.models.list():
        if hasattr(m, 'name'):
            models.append(m.name)
    if models:
        return "Available models:\n" + "\n".join(models)
    return "No models found"


def get_model():
    return f"Current model: `{get_current_model()}`"


def setup_menu():
    """Register bot command menu with Telegram."""
    commands = [
        {"command": "new", "description": "Start a new chat"},
        {"command": "get_model", "description": "Show current Gemini model"},
        {"command": "set_model", "description": "Switch Gemini model (admin)"},
        {"command": "list_models", "description": "List available models (admin)"},
        {"command": "get_my_info", "description": "Get your account info"},
        {"command": "get_group_info", "description": "Get group info (group only)"},
        {"command": "get_allowed_users", "description": "Show allowed users (admin)"},
        {"command": "get_allowed_groups", "description": "Show allowed groups (admin)"},
        {"command": "get_api_key", "description": "Show API keys (admin)"},
    ]
    try:
        resp = http_requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/setMyCommands",
            json={"commands": commands},
            timeout=10
        )
        result = resp.json()
        if result.get("ok"):
            return "✅ Command menu registered! Type / in the chat to see it."
        return f"❌ Failed: {result}"
    except Exception as e:
        return f"❌ Error: {e}"


def set_model_cmd(command):
    parts = command.strip().split(maxsplit=1)
    if len(parts) < 2:
        return "Usage: /set_model <model_name>\nExample: /set_model gemini-2.5-pro\n\nUse /list_models to see available models."
    model_name = parts[1].strip()
    set_model(model_name)
    return f"Model switched to: `{model_name}`\nNote: existing conversations will use the old model. Send /new to start fresh."

def get_my_info(id):
    return f"your telegram id is: `{id}`"

def get_group_info(type, chat_id):
    if type == "supergroup":
        return f"this group id is: `{chat_id}`"
    return "Please use this command in a group"

def get_allowed_users():
    send_log(f"```json\n{ALLOWED_USERS}```")
    return ""

def get_allowed_groups():
    send_log(f"```json\n{ALLOWED_GROUPS}```")
    return ""

def get_API_key():
    send_log(f"```json\n{GOOGLE_API_KEY}```")
    return ""

def speed_test(id):
    """ This command seems useless, but it must be included in every robot I make. """
    send_message(id, "开始测速")
    sleep(5)
    return "测试完成，您的5G速度为：\n**114514B/s**"

def send_message_test(id, command):
    if not is_admin(id):
        return admin_auch_info
    a = command.find(" ")
    b = command.find(" ", a + 1)
    if a == -1 or b == -1:
        return command_format_error_info
    to_id = command[a+1:b]
    text = command[b+1:]
    try:
        send_message(to_id, text)
    except Exception as e:
        send_log(f"err:\n{e}")
        return
    send_log("success")
    return ""

def excute_command(from_id, command, from_type, chat_id):
    if command.startswith("start") or command.startswith("help"):
        return help()

    elif command.startswith("get_my_info"):
        return get_my_info(from_id)

    elif command.startswith("get_group_info"):
        return get_group_info(from_type, chat_id)

    elif command.startswith("5g_test"):
        return speed_test(chat_id)

    elif command.startswith("send_message"):
        return send_message_test(from_id, command)

    elif command in ["get_allowed_users", "get_allowed_groups", "get_api_key", "list_models"]:
        if not is_admin(from_id):
            return admin_auch_info
        if IS_DEBUG_MODE == "0":
            return debug_mode_info

        if command == "get_allowed_users":
            return get_allowed_users()
        elif command == "get_allowed_groups":
            return get_allowed_groups()
        elif command == "get_api_key":
            return get_API_key()
        elif command == "list_models":
            return list_models()

    elif command.startswith("set_model"):
        if not is_admin(from_id):
            return admin_auch_info
        return set_model_cmd(command)

    elif command.startswith("get_model"):
        return get_model()

    elif command == "setup_menu":
        if not is_admin(from_id):
            return admin_auch_info
        return setup_menu()

    else:
        return command_format_error_info
