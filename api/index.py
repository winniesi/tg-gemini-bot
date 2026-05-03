from flask import Flask, render_template, request
import requests as http_requests
import os
import threading
import traceback

from .handle import handle_message
from .config import BOT_TOKEN, ALLOWED_USERS, ALLOWED_GROUPS, DEFAULT_MODEL

app = Flask(__name__)

_webhook_set = False
_webhook_lock = threading.Lock()


def ensure_webhook():
    """Verify and set Telegram webhook if needed."""
    global _webhook_set
    if _webhook_set:
        return
    with _webhook_lock:
        if _webhook_set:
            return
        webhook_url = os.environ.get("WEBHOOK_URL", "").strip()
        if not webhook_url:
            webhook_url = os.environ.get("VERCEL_URL", "").strip()
        if not webhook_url:
            print("No WEBHOOK_URL or VERCEL_URL set, skipping webhook setup")
            return
        if not webhook_url.startswith("https://"):
            webhook_url = f"https://{webhook_url}"
        if not webhook_url.endswith("/"):
            webhook_url += "/"
        try:
            r = http_requests.get(
                f"https://api.telegram.org/bot{BOT_TOKEN}/getWebhookInfo",
                timeout=5
            )
            info = r.json().get("result", {})
            current_url = info.get("url", "")
            if current_url != webhook_url:
                http_requests.post(
                    f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook",
                    json={"url": webhook_url, "allowed_updates": ["message", "callback_query"]},
                    timeout=5
                )
                print(f"Webhook set to {webhook_url} (was: {current_url or 'empty'})")
            else:
                print(f"Webhook OK: {current_url}")
            _webhook_set = True
        except Exception as e:
            print(f"Failed to check/set webhook: {e}")


@app.route("/", methods=["POST", "GET"])
def home():
    ensure_webhook()
    if request.method == "POST":
        update = request.json
        try:
            handle_message(update)
        except Exception as e:
            err = traceback.format_exc()
            print(f"ERROR handling message: {err}")
            # Try to notify user of the error
            try:
                msg = update.get("message", {})
                chat_id = msg.get("chat", {}).get("id")
                if chat_id:
                    http_requests.post(
                        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                        json={"chat_id": chat_id, "text": f"⚠️ Error: {e}"},
                        timeout=5
                    )
            except:
                pass
        return "ok"
    return render_template("status.html")


@app.route("/debug", methods=["GET"])
def debug():
    """Debug endpoint to check config state."""
    token_preview = (BOT_TOKEN[:6] + "...") if BOT_TOKEN else "NOT SET"
    return {
        "bot_token": token_preview,
        "allowed_users": ALLOWED_USERS,
        "allowed_groups": ALLOWED_GROUPS,
        "default_model": DEFAULT_MODEL,
        "webhook_url_env": os.environ.get("WEBHOOK_URL", "not set"),
        "vercel_url": os.environ.get("VERCEL_URL", "not set"),
    }


@app.route("/test_group", methods=["GET"])
def test_group():
    """Test group message processing with a simulated @mention."""
    from .telegram import Update, _get_bot_username, send_message
    from .auth import is_group_allowed

    test_update = {
        "update_id": 999999999,
        "message": {
            "message_id": 999,
            "from": {"id": 6702231827, "is_bot": False, "first_name": "Test", "username": "ohmorningsir"},
            "chat": {"id": -5280543061, "type": "group", "title": "test"},
            "date": 1700000000,
            "text": "@tg_ai_test_bot say hello",
            "entities": [{"type": "mention", "offset": 0, "length": 16}]
        }
    }

    steps = []
    try:
        bot_username = _get_bot_username()
        steps.append(f"bot_username: {bot_username}")

        update = Update(test_update)
        steps.append(f"is_group: {update.is_group}")
        steps.append(f"is_mentioned: {update.is_mentioned()}")
        steps.append(f"replied_to_bot: {update.replied_to_bot()}")
        steps.append(f"type: {update.type}")
        steps.append(f"text: {update.text}")
        steps.append(f"chat_id: {update.chat_id}")
        steps.append(f"is_group_allowed: {is_group_allowed(update.chat_id)}")

        # Try sending a test message
        r = send_message(-5280543061, "🧪 Test from /test_group endpoint")
        steps.append(f"send_message status: {r.status_code}")
    except Exception as e:
        steps.append(f"ERROR: {traceback.format_exc()}")

    return {"steps": steps}
