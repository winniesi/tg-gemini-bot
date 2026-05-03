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
                    json={"url": webhook_url, "allowed_updates": ["message", "callback_query", "chat_member"]},
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
