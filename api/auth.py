from .config import ALLOWED_USERS, ADMIN_ID, AUCH_ENABLE, ALLOWED_GROUPS



def is_authorized(is_group, from_id: int, user_name: str, chat_id, group_name) -> bool:
    if AUCH_ENABLE == "0":
        return True
    if is_group:
        if str(group_name).lower() in ALLOWED_GROUPS or str(chat_id) in ALLOWED_GROUPS:
            return True
    else:
        if str(user_name).lower() in ALLOWED_USERS or str(from_id) in ALLOWED_USERS:
            return True
    return False


def is_admin(from_id: int) -> bool:
    if str(from_id) == ADMIN_ID:
        return True
    return False
