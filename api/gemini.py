from io import BytesIO

from google import genai
import PIL.Image

from .config import GOOGLE_API_KEY, generation_config, safety_settings, gemini_err_info, new_chat_info

client = genai.Client(api_key=GOOGLE_API_KEY[0])

_MODEL_VERSION = 'gemini-flash-latest'


def list_models():
    """list all models"""
    return client.models.list()

""" This function is deprecated """
def generate_content(prompt: str) -> str:
    """generate text from prompt"""
    try:
        response = client.models.generate_content(model=_MODEL_VERSION, contents=prompt)
        result = response.text
    except Exception as e:
        result = f"{gemini_err_info}\n{repr(e)}"
    return result


def generate_text_with_image(prompt: str, image_bytes: BytesIO) -> str:
    """generate text from prompt and image"""
    img = PIL.Image.open(image_bytes)
    try:
        response = client.models.generate_content(model=_MODEL_VERSION, contents=[prompt, img])
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
        self.chat = client.chats.create(model=_MODEL_VERSION)

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
