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
        response = client.models.generate_content(
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
        response = client.models.generate_content(
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
                response = self.chat.send_message(prompt)
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
