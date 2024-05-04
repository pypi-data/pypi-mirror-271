import asyncio
import logging
from pathlib import Path
from typing import Dict

import tiktoken

from .constants import TOKENIZER

logger = logging.getLogger('standard')

def code_to_str(path: str | Path, comments: str = '#{}'):
    filepath = Path(path)
    code = comments.format(filepath.name) + '\n'
    with open(path, 'r', encoding='utf-8') as file_:
        code += file_.read()
    return code

def codes_to_str(path: str | Path,
                 suffix: str = '.py',
                 comments: str = '#',
                 exclude: list[str] = None) -> str:
    code = ''
    
    for item in sorted(Path(path).glob(f"*{suffix}")):
        if exclude and item.name in exclude:
            continue
        name = item.name
        with open(item, 'r', encoding='utf-8') as file_:
            code += f"{comments} {name}\n{file_.read()}\n"
    
    return code

def python_codes_to_str(path: str | Path, exclude: list[str] = None) -> str:
    return codes_to_str(path, exclude=exclude)

def json_to_html(json_data: Dict) -> str:
    def parse_content(content):
        if isinstance(content, list):
            return "".join([parse_content(item) for item in content])
        if isinstance(content, dict):
            tag_type, tag_content = next(iter(content.items()))
            return parse_tag(tag_type, tag_content)
        return content

    def parse_tag(tag_type, tag_content):
        if isinstance(tag_content, list):
            content_str = parse_content(tag_content)
        elif isinstance(tag_content, dict):
            content_str = parse_content([tag_content])
        else:
            content_str = tag_content

        if tag_type == "p":
            return f"<p>{content_str}</p>"
        if tag_type == "em":
            return f"<em>{content_str}</em>"
        if tag_type == "strong":
            return f"<strong>{content_str}</strong>"
        if tag_type == "blockquote":
            return f"<blockquote>{content_str}</blockquote>"
        if tag_type == "ol":
            return f"<ol>{content_str}</ol>"
        if tag_type == "ul":
            return f"<ul>{content_str}</ul>"
        if tag_type == "li":
            return f"<li>{content_str}</li>"
        if tag_type == "code":
            return f"<code>{content_str}</code>"
        return ""

    return parse_content(json_data)

def get_encoding(model: str = None):
    try:
        if model:
            return tiktoken.encoding_for_model(model)
        return tiktoken.get_encoding(TOKENIZER[0])
    except KeyError:
        return tiktoken.get_encoding(TOKENIZER[0])

def number_of_tokens(messages: str | list[str], model: str = TOKENIZER[0]):
    """
    Returns the number of tokens used by a list of messages.

    Parameters
    ----------
    messages : str or list of str
        A single message or a list of messages to be processed. Each message
        can be a string.
    model : str, optional
        The name of the model used for token encoding (default is MODELS[0]).

    Returns
    -------
    int
        The total number of tokens used by the provided messages.

    Raises
    ------
    NotImplementedError
        If the function is not presently implemented for the given model.

    Notes
    -----
    The function calculates the number of tokens used by messages. The number
    of tokens
    is derived from the encoding of the messages according to the specified
    model.
    If the model is not found in the pre-defined MODELS list, the function will
    fall back
    to using the "cl100k_base" model for token encoding.

    Each message is expected to be in the form of a dictionary with 'role' and
    'content' keys,
    representing the sender role and the content of the message, respectively.
    The function
    calculates the token count considering the special tokens used for message
    encoding,
    such as <im_start> and <im_end>. For future models, token counts may vary,
    so this
    behavior is subject to change.

    The function raises a NotImplementedError if the provided model is not
    supported. Users can refer to the provided link for information on how
    messages are converted to tokens for each specific model.

    Examples
    --------
    >>> messages = [
    ...     {
    ...         'role': 'user',
    ...         'content': "Hello, how are you?"
    ...     },
    ...     {
    ...         'role': 'assistant',
    ...         'content': "I'm doing great! How can I assist you?"
    ...     }
    ... ]
    >>> num_tokens = number_of_tokens(messages)
    >>> print(num_tokens)
    23

    >>> single_message = "This is a test message."
    >>> num_tokens = number_of_tokens(single_message, model="my_custom_model")
    >>> print(num_tokens)
    8
    """
    encoding = get_encoding(model)
    if isinstance(messages, str):
        messages = [
            {
                'role': 'user',
                'content': messages
            }
        ]
    if True:  # note: future models may deviate from this
        num_tokens = 0
        for message in messages:
            # every message follows
            # <im_start>{role/name}\n{content}<im_end>\n
            num_tokens += 4
            for key, value in message.items():
                num_tokens += len(encoding.encode(value))
                if key == "name":  # if True, the role is omitted
                    num_tokens += -1  # role is always required and 1 token
        num_tokens += 2  # every reply is primed with <im_start>assistant
        return num_tokens
    raise NotImplementedError(  # TODO choose another error
        f"number_of_tokens() is not presently implemented for model {model}. "
        "See https://github.com/openai/openai-python/blob/main/chatml.md for "
        "information on how messages are converted to tokens."
        ""
    )

def run_async(coro, *args, **kwargs):
    task = None
    try:
        loop = asyncio.get_running_loop()
        task = loop.create_task(coro(*args, **kwargs))
    except RuntimeError:
        task = coro(*args, **kwargs)
    try:
        asyncio.run(task)
    except RuntimeError:
        try:
            # NOTE: this allows running in jupyter without using 'await'
            import nest_asyncio  # pylint --disable=import-outside-toplevel
            nest_asyncio.apply()
            asyncio.run(task)
        except (ImportError, ModuleNotFoundError) as err:
            logger.error(err)
            logger.warning("Must install nest_asyncio for running in Jupyter")
            raise err
    return task.result()

class Message:
    def __init__(self, content: str = None) -> None:
        self.content: str = content

class Choices:
    def __init__(self, ) -> None:
        self.message = Message()

class LastResponse:
    def __init__(self) -> None:
        self.choices = [Choices()]
