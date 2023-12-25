import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
ALLOWED_USERS = os.getenv("ALLOWED_USERS", "").replace("@", "").split(",")
