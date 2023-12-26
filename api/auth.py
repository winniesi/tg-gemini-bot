from .config import ALLOWED_USERS


def is_authorized(from_id: int, user_name: str) -> bool:
    if str(user_name) in ALLOWED_USERS:
        return True
    return False
