from io import BytesIO

import google.generativeai as genai
import PIL.Image

from .config import GOOGLE_API_KEY, generation_config, safety_settings, gemini_err_info, new_chat_info

genai.configure(api_key=GOOGLE_API_KEY[0])

model_usual = genai.GenerativeModel(
    model_name="gemini-pro",
    generation_config=generation_config,
    safety_settings=safety_settings)

model_vision = genai.GenerativeModel(
    model_name="gemini-pro-vision",
    generation_config=generation_config,
    safety_settings=safety_settings)


def list_models() -> None:
    """list all models"""
    for m in genai.list_models():
        print(m)
        if "generateContent" in m.supported_generation_methods:
            print(m.name)

""" This function is deprecated """
def generate_content(prompt: str) -> str:
    """generate text from prompt"""
    try:
        response = model_usual.generate_content(prompt)
        result = response.text
    except Exception as e:
        result = f"{gemini_err_info}\n{repr(e)}"
    return result


def generate_text_with_image(prompt: str, image_bytes: BytesIO) -> str:
    """generate text from prompt and image"""
    img = PIL.Image.open(image_bytes)
    try:
        response = model_vision.generate_content([prompt, img])
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
        self.chat = model_usual.start_chat(history=[])

    def send_message(self, prompt: str) -> str:
        """send message"""
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
        return self.chat.history

    @property
    def history_length(self):
        return len(self.chat.history)


if __name__ == "__main__":
    print(list_models())
