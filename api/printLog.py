from .config import IS_DEBUG_MODE,ADMIN_ID
from .telegram import send_message,send_imageMessage

admin_id = ADMIN_ID
is_debug_mode =IS_DEBUG_MODE

def send_log(text):
    if is_debug_mode == "1":
        send_message(admin_id,text)

def send_image_log(text,imageID):
    if is_debug_mode == "1":
        send_imageMessage(admin_id,text,imageID)
