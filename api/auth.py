from .config import ALLOWED_USERS,ADMIN_ID,AUCH_ENABLE



def is_authorized(from_id: int, user_name: str) -> bool:
    if AUCH_ENABLE == "0":
        return True
    if str(user_name).lower() in ALLOWED_USERS or str(from_id) in ALLOWED_USERS:
        return True
    return False


def is_admin(from_id: int) -> bool:
    if str(from_id) == ADMIN_ID:
        return True
    return False
