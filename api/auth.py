from .config import ALLOWED_USERS


def is_authorized(from_id: int, user_name: str) -> bool:
    if str(from_id) in ALLOWED_USERS:
        return True
    return False
