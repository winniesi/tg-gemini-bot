from .config import ALLOWED_USERS
from .telegram import send_message


def is_authorized(from_id: int, user_name: str) -> bool:
    if str(user_name) in ALLOWED_USERS:
        return True
    send_message(from_id, "😫 You are not allowed to use this bot.")
    return False
