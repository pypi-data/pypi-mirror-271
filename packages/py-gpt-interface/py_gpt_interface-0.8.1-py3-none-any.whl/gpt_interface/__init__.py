import base64
from openai import OpenAI

from gpt_interface.calls.call_gpt import call_gpt
from gpt_interface.calls.rate_limiter import RateLimiter
from gpt_interface.log import Log
from gpt_interface.options.models import Model, known_models
from gpt_interface.options.system_message import SystemMessageOptions
from gpt_interface.tools import Tool

def encode_image_in_base64(image_filepath: str):
    with open(image_filepath, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


class GptInterface:
    def __init__(
        self,
        api_key: str,
        model: str,
        json_mode: bool = False,
        temperature: float = 1.0,
        base_url: str | None = None,
        openai_api_key: str | None = None,  # deprecated
    ) -> None:
        self.set_model(model)
        self.set_json_mode(json_mode)
        self.temperature = temperature
        if openai_api_key:
            print("Warning: openai_api_key is deprecated. Use api_key instead.")
            api_key = openai_api_key
        self.interface = (
            OpenAI(base_url=base_url, api_key=api_key)
            if base_url
            else OpenAI(api_key=api_key)
        )
        self.log = Log()
        self.rate_limiter = RateLimiter()
        self.system_message_options = SystemMessageOptions(
            use_system_message=False,
            system_message="",
            message_at_end=True,
        )
        self.tools: list[Tool] = []

    def set_model(self, model: str) -> None:
        self.model = model
        if model not in [m.name for m in known_models]:
            print(f"Warning: unrecognized model {model}. Known models list may be out of date.")

    def append_image_to_log_from_filepath(self, image_url: str) -> None:
        self.append_image_to_log_from_url(
            f"data:image/jpeg;base64,{encode_image_in_base64(image_url)}"
        )

    def append_image_to_log_from_url(self, image_url: str) -> None:
        matching_model: Model = [m for m in known_models if m.name==self.model][0]
        if not matching_model.vision_enabled:
            print("Warning: Vision API is not enabled for this model. Image not attached.")
        else:
            self.log.append("user", [
                {
                    "type": "image_url",
                    "image_url": {"url": image_url},
                },
            ])

    def set_json_mode(self, json_mode: bool) -> None:
        self.json_mode = json_mode

    def set_system_message(
        self,
        system_message: str = "",
        use_system_message: bool = True,
        message_at_end: bool = True,
    ) -> None:
        self.system_message_options = SystemMessageOptions(
            use_system_message=use_system_message,
            system_message=system_message,
            message_at_end=message_at_end,
        )

    def set_tools(self, tools: list[Tool]) -> None:
        self.tools = tools

    def say(self, user_message: str, thinking_time: int = 0) -> str:
        self.log.append("user", user_message)
        return self.get_assistant_message(thinking_time=thinking_time)

    def retry(self, thinking_time: int = 0) -> str:
        self.log.messages = self.log.messages[:-1]
        return self.get_assistant_message(thinking_time=thinking_time)

    def get_assistant_message(self, thinking_time: int) -> str:
        assistant_message = call_gpt(
            interface=self.interface,
            model=self.model,
            log=self.log,
            system_message_options=self.system_message_options,
            temperature=self.temperature,
            json_mode=self.json_mode,
            tools=self.tools,
            call_again_fn=self.get_assistant_message,
            thinking_time=thinking_time,
        )
        self.rate_limiter.wait()
        self.log.append("assistant", assistant_message)
        return assistant_message
