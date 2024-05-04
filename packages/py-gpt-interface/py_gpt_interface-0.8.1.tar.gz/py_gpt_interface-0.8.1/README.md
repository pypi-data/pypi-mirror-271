A simple interface for using the GPT API.

## API Key

To use gpt_interface, you need an OpenAI API key (https://platform.openai.com/docs/api-reference/authentication).

I recommend creating a .env file and adding it to your .gitignore file. The file would contain the following:

```
OPENAI_API_KEY=sk-exampleKey
```

You can then load the key into your Python code, and use it to initialize GptInterface.

```python
from dotenv import load_dotenv
import os

from gpt_interface import GptInterface


if __name__ == "__main__":
    load_dotenv()  # load the OpenAI API key from a .env file
    interface = GptInterface(  # create interface
        api_key=os.getenv("OPENAI_API_KEY"),
        model="gpt-3.5-turbo",
    )
```

## Simple Usage

Use interface.say() to talk to GPT. The conversation log is stored in memory.

```python
from dotenv import load_dotenv
import os

from gpt_interface import GptInterface


if __name__ == "__main__":
    load_dotenv()
    interface = GptInterface(
        api_key=os.getenv("OPENAI_API_KEY"),
        model="gpt-3.5-turbo",
    )
    interface.say("Hi! My name is Matt")  # talk to GPT
    response = interface.say("What's my name?")  # conversation log is stored in memory
    assert "Matt" in response
```

You can also save and load the conversation log.

```python
    print(interface.log)
    interface.log.save("my_log.json")
    interface.log.load("my_log.json")
```

The log from the example above would look something like this:

```json
[
    {
        "role": "user",
        "content": "Hi! My name is Matt"
    },
    {
        "role": "assistant",
        "content": "Hello Matt! How can I assist you today?"
    },
    {
        "role": "user",
        "content": "What's my name?"
    },
    {
        "role": "assistant",
        "content": "Your name is Matt!"
    }
]
```

## Different Server

You can point the URL to any server that exposes an OpenAI-like API, including a local server.

```python
from dotenv import load_dotenv
import os

from gpt_interface import GptInterface


if __name__ == "__main__":
    load_dotenv()
    interface = GptInterface(
        base_url="http://localhost:8000",
        api_key=os.getenv("OPENAI_API_KEY"),
        model="gpt-3.5-turbo",
    )
    interface.say("Hi! My name is Matt")  # talk to GPT
    response = interface.say("What's my name?")  # conversation log is stored in memory
    assert "Matt" in response
```

## Manual Editing of Chat Log

You can manually overwrite the chat log in GptInterface, and continue the chat with it.

```python
from dotenv import load_dotenv
import os
from typing import cast

from gpt_interface import GptInterface
from gpt_interface.log import Message


def change_name():
    interface = GptInterface(
        api_key=cast(str, os.getenv("OPENAI_API_KEY")),
        model="gpt-4",
    )
    interface.say("Hi there!")
    interface.say("My first name is Bob.")
    interface.say("My last name is Smith.")
    messages = interface.log.messages[:-2]  # remove last user message and GPT reply
    interface.log.set_messages(messages)
    interface.say("My last name is Jones.")
    print(interface.log)


def force_response():
    interface = GptInterface(
        api_key=cast(str, os.getenv("OPENAI_API_KEY")),
        model="gpt-4",
    )
    messages = [
        Message(
            role="user",
            content="What's the square root of 4?",
        ),
        Message(
            role="assistant",
            content="I believe the square root of 4 is 3.",
        ),
    ]
    interface.log.set_messages(messages)
    interface.say("Is that correct?")
    print(interface.log)


if __name__ == "__main__":
    load_dotenv()  # load the OpenAI API key from a .env file
    change_name()
    print()
    force_response()
```

## System Message

Set a system message with the GptInterface.set_system_message() function. A few examples are below.

```python
from dotenv import load_dotenv
import os
from typing import cast

from gpt_interface import GptInterface


def be_pirate():
    interface = GptInterface(
        api_key=cast(str, os.getenv("OPENAI_API_KEY")),
        model="gpt-3.5-turbo",
    )
    interface.set_system_message(
        "You will respond as a 19th century pirate. You only speak in the form of lyrics from sea shanties.",
        message_at_end=False,  # message at start or end of log sent to GPT
    )
    interface.say("What's your job?")
    interface.say("What year is it?")
    print(interface.log)


def be_space_trucker():
    interface = GptInterface(
        api_key=cast(str, os.getenv("OPENAI_API_KEY")),
        model="gpt-3.5-turbo",
    )
    interface.set_system_message(
        "You will respond as a 23rd century space trucker. You talk like a hard-boiled detective. Keep your responses short.",
    )  # message_at_end=True by default
    interface.say("What's your job?")
    interface.say("What year is it?")
    print(interface.log)


def be_normal():
    interface = GptInterface(
        api_key=cast(str, os.getenv("OPENAI_API_KEY")),
        model="gpt-3.5-turbo",
    )
    interface.set_system_message(
        use_system_message=False,
    )
    interface.say("What's your job?")
    interface.say("What year is it?")
    print(interface.log)


if __name__ == "__main__":
    load_dotenv()  # load the OpenAI API key from a .env file
    be_pirate()
    print()
    be_space_trucker()
    print()
    be_normal()
```

## JSON Mode Output

Force output to be in JSON format.

```python
from dotenv import load_dotenv
import os
from typing import cast

from gpt_interface import GptInterface


def json_response():
    interface = GptInterface(
        api_key=cast(str, os.getenv("OPENAI_API_KEY")),
        model="gpt-4",
        json_mode=True,
    )
    interface.set_system_message(
        "Reply in the form {'query': [user query], 'answer': [your response]}.",
    )
    interface.say("Hello.")
    interface.set_json_mode(False)
    interface.set_system_message(
        use_system_message=False,
    )
    interface.say("Say hello normally.")
    print(interface.log)


if __name__ == "__main__":
    load_dotenv()  # load the OpenAI API key from a .env file
    json_response()
```

## Function Calling

Use GptInterface.set_tools() with a list of function objects to give GPT the ability to call functions.

```python
from dotenv import load_dotenv
import os
from print_columns import print_columns
from typing import cast, Literal

from gpt_interface import GptInterface
from gpt_interface.tools import make_annotated_function


def get_function_call_with_optional_params() -> None:
    def convert_day_to_int(day: Literal["M", "T", "W", "Th", "F", "Sa", "Su"], one_index: bool = False) -> int:
        return ["M", "T", "W", "Th", "F", "Sa", "Su"].index(day) + one_index

    interface = GptInterface(
        api_key=cast(str, os.getenv("OPENAI_API_KEY")),
        model="gpt-3.5-turbo",
    )
    interface.set_tools(
        [
            make_annotated_function(
                convert_day_to_int,
                description="Convert a day of the week to an integer",
                param_descriptions={
                    "day": "The day of the week",
                    "one_index": "Whether to start counting at 1 instead of 0",
                },
                param_types={
                    "day": "string",
                    "one_index": "boolean",
                },
                param_allowed_values={
                    "day": ["M", "T", "W", "Th", "F", "Sa", "Su"],
                },
            ),
        ]
    )
    response = interface.say("Convert Monday to an integer")
    print(response)
    response = interface.say("Convert Tuesday to an integer, starting from Monday=1")
    print(response)


if __name__ == "__main__":
    load_dotenv()  # load the OpenAI API key from a .env file
    get_function_call_with_optional_params()
```

These functions can be imported from external packages as well.

```python
from dotenv import load_dotenv
import os
from print_columns import print_columns
from typing import cast, Literal

from gpt_interface import GptInterface
from gpt_interface.tools import make_annotated_function


def call_external_function() -> None:
    interface = GptInterface(
        api_key=cast(str, os.getenv("OPENAI_API_KEY")),
        model="gpt-4",
    )
    interface.set_tools(
        [
            make_annotated_function(
                print_columns,
                description="Divide the terminal output into columns and print one wrapped string in each column. The strings, column_widths, and colors parameters should all be lists of the same length. This function does not return anything, but you can assume it completes correctly once called, and can let the user know so.",
                param_descriptions={
                    "strings": "The strings to print, one for each column",
                    "column_widths": "The width of each column",
                    "colors": "The text color of each column",
                    "divider": "The divider between columns",
                },
                param_types={
                    "strings": "array[string]",
                    "column_widths": "array[integer]",
                    "colors": "array[string]",
                    "divider": "string",
                },
            ),
        ]
    )
    response = interface.say("Print lorem ipsum in three columns, with widths of 30, 20, and 50. The colors should be red, blue, and green.")
    print(response)


if __name__ == "__main__":
    load_dotenv()  # load the OpenAI API key from a .env file
    get_function_call_with_optional_params()
    call_external_function()
```

## Retrying a Call

If a call to GPT fails, or gives an undesired response, you can regenerate a new response with GptInterface.retry().

```python
from dotenv import load_dotenv
import os
from typing import cast

from gpt_interface import GptInterface


if __name__ == "__main__":
    load_dotenv()  # load the OpenAI API key from a .env file
    interface = GptInterface(
        api_key=cast(str, os.getenv("OPENAI_API_KEY")),
        model="gpt-3.5-turbo",
    )
    response = interface.say("Give me a random number from 1-1000.")
    print(response)
    response = interface.retry()
    print(response)
    print(interface.log)
```

## Passing Images

You can add an image to your chat in two ways. You can either pass the filepath of an image on your local computer, or the URL of an image online.

```python
from dotenv import load_dotenv
import os
from typing import cast

from gpt_interface import GptInterface


def ask_about_image_from_filepath():
    interface = GptInterface(
        api_key=cast(str, os.getenv("OPENAI_API_KEY")),
        model="gpt-4-vision-preview",
    )
    interface.append_image_to_log_from_filepath("tests/elephant.webp")
    response = interface.say("What animal is this?")
    print(response)


def ask_about_image_from_url():
    interface = GptInterface(
        api_key=cast(str, os.getenv("OPENAI_API_KEY")),
        model="gpt-4-vision-preview",
    )
    interface.append_image_to_log_from_url("https://en.wikipedia.org/static/images/icons/wikipedia.png")
    response = interface.say("What logo is this?")
    print(response)


if __name__ == "__main__":
    load_dotenv()  # load the OpenAI API key from a .env file
    ask_about_image_from_filepath()
    ask_about_image_from_url()
```

## Thinking Time

Though I haven't done a study on this, I've found that adding additional spaces to the end of a query seems to give better answers. Adding a thinking_time parameter just appends spaces to the end of your query.

```python
from dotenv import load_dotenv
import os
from typing import cast

from gpt_interface import GptInterface


def dont_think(question: str):
    interface = GptInterface(
        api_key=cast(str, os.getenv("OPENAI_API_KEY")),
        model="gpt-3.5-turbo",
        json_mode=True,
    )
    interface.say(question)
    print(interface.log)


def think(question: str):
    interface = GptInterface(
        api_key=cast(str, os.getenv("OPENAI_API_KEY")),
        model="gpt-3.5-turbo",
        json_mode=True,
    )
    interface.say(question, thinking_time=300)
    print(interface.log)


if __name__ == "__main__":
    load_dotenv()  # load the OpenAI API key from a .env file
    question = """
A farmer is looking to divide his land among his three children. The land is a rectangle, 600 meters long and 400 meters wide. The eldest child wants a piece of land that is exactly twice the size of the land given to the youngest. The middle child is happy with any size of land. How should the farmer divide his land so that each child gets a fair share, with the eldest getting twice as much as the youngest, and the middle child getting an equal share?
    """
    dont_think(question)
    think(question)
```
