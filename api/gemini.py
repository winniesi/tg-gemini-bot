import time
from io import BytesIO

from google import genai
from google.genai import types
import PIL.Image

from .config import (
    GOOGLE_API_KEY, generation_config, safety_settings,
    gemini_err_info, new_chat_info, SYSTEM_INSTRUCTION, DEFAULT_MODEL,
)

client = genai.Client(api_key=GOOGLE_API_KEY[0])

current_model = DEFAULT_MODEL

# Transient error codes that are safe to retry
_RETRY_CODES = {429, 500, 503}
_MAX_RETRIES = 3
_RETRY_DELAYS = [2, 4, 8]  # exponential backoff in seconds


def _is_retryable(exc: Exception) -> bool:
    """Check if exception is a transient Gemini API error."""
    s = str(exc)
    for code in _RETRY_CODES:
        if str(code) in s:
            return True
    return False


def _call_with_retry(fn, *args, **kwargs):
    """Call a Gemini API function with retry on transient errors."""
    last_exc = None
    for attempt in range(_MAX_RETRIES):
        try:
            return fn(*args, **kwargs)
        except Exception as e:
            last_exc = e
            if _is_retryable(e) and attempt < _MAX_RETRIES - 1:
                time.sleep(_RETRY_DELAYS[attempt])
                continue
            raise
    raise last_exc


def get_current_model():
    return current_model


def set_model(model_name: str):
    global current_model
    current_model = model_name


def _build_gen_config():
    """Build GenerateContentConfig from config settings."""
    return types.GenerateContentConfig(
        max_output_tokens=generation_config.get("max_output_tokens", 1024),
        safety_settings=[
            types.SafetySetting(
                category=s["category"],
                threshold=s["threshold"],
            )
            for s in safety_settings
        ],
        system_instruction=SYSTEM_INSTRUCTION if SYSTEM_INSTRUCTION else None,
    )


def list_models():
    """list all models"""
    return client.models.list()


def generate_content(prompt: str) -> str:
    """generate text from prompt"""
    try:
        response = _call_with_retry(
            client.models.generate_content,
            model=current_model,
            contents=prompt,
            config=_build_gen_config(),
        )
        result = response.text
    except Exception as e:
        result = f"{gemini_err_info}\n{repr(e)}"
    return result


def generate_text_with_image(prompt: str, image_bytes: BytesIO) -> str:
    """generate text from prompt and image"""
    img = PIL.Image.open(image_bytes)
    try:
        response = _call_with_retry(
            client.models.generate_content,
            model=current_model,
            contents=[prompt, img],
            config=_build_gen_config(),
        )
        result = response.text
    except Exception as e:
        result = f"{gemini_err_info}\n{repr(e)}"
    return result


class ChatConversation:
    """
    Kicks off an ongoing chat. If the input is /new,
    it triggers the start of a fresh conversation.
    """

    def __init__(self) -> None:
        self.chat = client.chats.create(
            model=current_model,
            config=_build_gen_config(),
        )

    def send_message(self, prompt: str) -> str:
        """send message"""
        prompt = prompt.removeprefix("/gemini")
        prompt = prompt.removeprefix("/Gemini")
        prompt = prompt.removeprefix("/ai")
        prompt = prompt.removeprefix("/AI")
        if prompt.startswith("/new"):
            self.__init__()
            result = new_chat_info
        else:
            try:
                response = _call_with_retry(self.chat.send_message, prompt)
                result = response.text
            except Exception as e:
                result = f"{gemini_err_info}\n{repr(e)}"
        return result

    @property
    def history(self):
        return self.chat.get_history()

    @property
    def history_length(self):
        return len(self.history)


if __name__ == "__main__":
    print(list_models())
