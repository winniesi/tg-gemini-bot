from .config import ALLOWED_USERS, ALLOWED_GROUPS


def is_authorized(from_id: int, user_name: str) -> bool:
    if str(from_id) in ALLOWED_USERS:
        return True
    return False


def is_group_allowed(chat_id: int) -> bool:
    return str(chat_id) in ALLOWED_GROUPS
