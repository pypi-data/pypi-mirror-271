# aigents

Adapters for Large Language Models and Generative Pre-trained Transformers APIs

## Installation

### Using pip

```bash
python -m pip install aigents
```

## Usage

The `aigents` package intention is to tackle the issue of out there having a wide variety of different AI models APIs, even though most of them keep similar standards, it might be confusing or challeging for developers to merge, scale and write conssitent solutions that englobes them.

### Chat

The main classes for completions or chat have _Chatters_ on their name. For instance, `aigents.GoogleChatter` uses Google's AI completion models to generate chat responses. The method for calling responses is `answer`.

The constructors for _Chatters_ differs a little, but on thing in common on them is the `setup` (`str`) argument: a text instructing the AI model to play some role. For example:

``` python
from aigents import GoogleChatter

setup = "You are a very experienced and successful fantasy novel writer. "
## generate your API key: https://makersuite.google.com/app/apikey
api_key = "YOUR_GOOGLE_AI_API_KEY"
temperature = 0.5  # for creativity
chatter = GoogleChatter(setup=setup, api_key=api_key)

response = chatter.answer(
    "What are the difference between soft magic system "
    "and hard magic system?"
)
```

The returned value is a string corresponding on the first [candidate response from Gemini API](https://ai.google.dev/api/python/google/generativeai/GenerativeModel#generate_content), which you can access using the attribute `chatter.last_response`.

For `OpenAI` and `Google` chatters you can the the API key using `.env` file. Use the `.sample.env`: paste your API keys and save it as `.env`

#### Conversation

By default, `chatter.answer` has `conversation=True` for every _Chatter_. This means that the object keeps a record of the messages (conversation), which you can access using the attribute `chatter.messages`.

If the messages exceeds the token window allowed for the corresponding model, the instance will try to reduce the size of the messages. If the default values of `use_agent=True` is set for `chatter.answer`, the _Chatter_  will use another instance to summarize messages, in order to preserve most of the history and meaning of the conversation. Otherwise it will remove the oldest (but the `chatter.setup`, if provided) messages.

This section provides a brief overview of the classes in `core.py` and their usage.

#### Async version:

Every chatter have an async version. For instance, the previous code can be written using async version of the OpenAI's chatter:

``` python
from aigents import AsyncOpenAIChatter

setup = "You are a very experienced and successful fantasy novel writer. "
## generate your API key: https://platform.openai.com/api-keys
api_key = "YOUR_OPEN_AI_API_KEY"
temperature = 0.5  # for creativity
chatter = AsyncOpenAIChatter(setup=setup, api_key=api_key)

response = await chatter.answer(
    "What are the difference between soft magic system "
    "and hard magic system?"
)
```

#### Other Chatters:

* **AsyncGoogleChatter**: async version of `GoogleChatter`;
* **GoogleVision**: agent for image chat (<span style="color: #b04e27;">Important</span>: gemini-pro-vision does not generate images as for this date);
* **AsyncGoogleVision**: async version of `GoogleVision`
* **OpenAIChatter**: chatter that uses OpenAI's API;
* **BingChatter**: uses the uses [g4f](https://github.com/xtekky/gpt4free/tree/main) adpter, with `Bing` provider;
* **AsyncBingChatter**: async version of `BingChatter`.

#### Models

You can check different AI models used by `aigents` in module `constants`. For instance, for changing OpenAI chatter's model from `gpt-3.5-turbo-0125` to `gpt-4-0125-preview`:

```python
from aigents import OpenAIChatter
from aigents.constants import MODELS

api_key = "YOUR_OPEN_AI_API_KEY"
chatter = OpenAIChatter(setup=setup, api_key=api_key)
chatter.change_model(MODELS[3])
# always checked if it is the intended model
print(chatter.model)
```

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

This project is licensed under [GNU_GPL_v3.0](https://github.com/xtekky/gpt4free/blob/main/LICENSE)

## Credits

`aigents` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
