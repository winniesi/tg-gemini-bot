from io import BytesIO

import google.generativeai as genai
import PIL.Image

from .config import GOOGLE_API_KEY, safety_settings

genai.configure(api_key=GOOGLE_API_KEY)
model_usual = genai.GenerativeModel("gemini-pro")
model_vision = genai.GenerativeModel("gemini-pro-vision")


def list_models() -> None:
    """list all models"""
    for m in genai.list_models():
        print(m)
        if "generateContent" in m.supported_generation_methods:
            print(m.name)


def generate_content(prompt: str) -> str:
    """generate text from prompt"""
    try:
        response = model_usual.generate_content(prompt, safety_settings=safety_settings)
        result = response.text
    except Exception as e:
        result = f"🤖 {e}"
    return result


def generate_text_with_image(prompt: str, image_bytes: BytesIO) -> str:
    """generate text from prompt and image"""
    img = PIL.Image.open(image_bytes)
    try:
        response = model_vision.generate_content(
            [prompt, img], safety_settings=safety_settings
        )
        result = response.text
    except Exception as e:
        result = f"🤖 {e}\n\n🤷‍♀️ This is most likely due to Gemini's restrictions on image content safety."
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
            result = "🍺 We're having a fresh chat."
        else:
            try:
                response = self.chat.send_message(
                    prompt, safety_settings=safety_settings
                )
                result = response.text
            except Exception as e:
                result = f"🤖 {e}\n\n🤷‍♀️ This is most likely due to Gemini's restrictions on content safety"
        return result

    @property
    def history(self):
        return self.chat.history

    @property
    def history_length(self):
        return len(self.chat.history)


if __name__ == "__main__":
    print(list_models())
