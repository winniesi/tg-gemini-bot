import requests as http_requests

from .config import (
    BOT_TOKEN, help_text, command_list,
    command_format_error_info,
)
from .printLog import send_log
from .gemini import client, set_model, get_current_model


def help():
    return f"{help_text}\n\n{command_list}"


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
        {"command": "set_model", "description": "Switch Gemini model"},
        {"command": "list_models", "description": "List available models"},
        {"command": "get_my_info", "description": "Get your Telegram ID"},
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


def get_my_info(id, is_group=False, chat_id=None):
    if is_group:
        return f"Group ID: `{chat_id}`\nYour user ID: `{id}`"
    return f"your telegram id is: `{id}`"


def excute_command(from_id, command, chat_id, is_group=False):
    if command.startswith("/"):
        command = command[1:]
    if command.startswith("start") or command.startswith("help"):
        return help()
    elif command.startswith("new"):
        return ""  # handled by caller
    elif command.startswith("get_my_info"):
        return get_my_info(from_id, is_group=is_group, chat_id=chat_id)
    elif command.startswith("get_model"):
        return get_model()
    elif command.startswith("set_model"):
        return set_model_cmd(command)
    elif command.startswith("list_models"):
        return list_models()
    elif command.startswith("setup_menu"):
        return setup_menu()
    else:
        return command_format_error_info
