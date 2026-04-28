from flask import Flask, render_template, request
import requests as http_requests
import os
import threading

from .handle import handle_message
from .config import BOT_TOKEN

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
        handle_message(update)
        return "ok"
    return render_template("status.html")
