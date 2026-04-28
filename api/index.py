from flask import Flask, render_template, request
import requests as http_requests
import os
import threading

from .handle import handle_message
from .config import BOT_TOKEN

app = Flask(__name__)

_webhook_set = False
_webhook_lock = threading.Lock()

def _get_bot_commands():
    return [
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

_commands_set = False

def ensure_commands():
    """Register bot command menu with Telegram."""
    global _commands_set
    if _commands_set:
        return
    try:
        resp = http_requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/setMyCommands",
            json={"commands": _get_bot_commands()},
            timeout=10
        )
        result = resp.json()
        if result.get("ok"):
            print("Bot command menu set successfully")
            _commands_set = True
        else:
            print(f"setMyCommands failed: {result}")
    except Exception as e:
        print(f"Failed to set commands: {e}")


def ensure_webhook():
    """Set Telegram webhook if not already set."""
    global _webhook_set
    if _webhook_set:
        return
    with _webhook_lock:
        if _webhook_set:
            return
        # Prefer WEBHOOK_URL env var (stable alias), fallback to VERCEL_URL
        webhook_url = os.environ.get("WEBHOOK_URL", "").strip()
        if not webhook_url:
            webhook_url = os.environ.get("VERCEL_URL", "").strip()
        if not webhook_url:
            return
        if not webhook_url.startswith("https://"):
            webhook_url = f"https://{webhook_url}"
        # Ensure trailing slash for consistent comparison
        if not webhook_url.endswith("/"):
            webhook_url += "/"
        try:
            r = http_requests.get(
                f"https://api.telegram.org/bot{BOT_TOKEN}/getWebhookInfo",
                timeout=5
            )
            info = r.json().get("result", {})
            current_url = info.get("url", "")
            # Only set webhook if not already configured (empty)
            if not current_url:
                http_requests.post(
                    f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook",
                    json={"url": webhook_url, "allowed_updates": ["message", "callback_query"]},
                    timeout=5
                )
                print(f"Webhook set to {webhook_url}")
            else:
                print(f"Webhook already set to {current_url}")
            _webhook_set = True
        except Exception as e:
            print(f"Failed to check/set webhook: {e}")
    # Register commands outside webhook lock
    ensure_commands()


@app.route("/", methods=["POST", "GET"])
def home():
    ensure_webhook()
    if request.method == "POST":
        update = request.json
        handle_message(update)
        return "ok"
    return render_template("status.html")

