from flask import Flask, render_template, request
import requests as http_requests
import os

from .handle import handle_message
from .config import BOT_TOKEN

app = Flask(__name__)

def set_webhook():
    """Set Telegram webhook on cold start."""
    webhook_url = os.environ.get("VERCEL_URL", "")
    if not webhook_url:
        # Try to detect from request context later
        return
    if not webhook_url.startswith("https://"):
        webhook_url = f"https://{webhook_url}"
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
                json={"url": webhook_url},
                timeout=5
            )
            print(f"Webhook set to {webhook_url}")
        else:
            print(f"Webhook already set to {current_url}")
    except Exception as e:
        print(f"Failed to set webhook: {e}")

# Set webhook on module load (cold start)
set_webhook()


@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        update = request.json
        handle_message(update)
        return "ok"
    return render_template("status.html")
