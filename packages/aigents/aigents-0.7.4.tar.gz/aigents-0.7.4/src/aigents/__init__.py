import logging
from logging import NullHandler
from logging.config import dictConfig

from .core import OpenAIChatter
from .core import AsyncOpenAIChatter
from .core import GoogleChatter
from .core import AsyncGoogleChatter
from .core import AsyncGoogleVision
from .core import BingChatter
from .core import AsyncBingChatter
from .context.core import Context
from . import base
from . import constants
from . import prompts

from .settings import CONFIG_LOG

dictConfig(CONFIG_LOG)
# Set default logging handler to avoid \"No handler found\" warnings.
logging.getLogger(__name__).addHandler(NullHandler())


__all__ = [
    'OpenAIChatter',
    'AsyncOpenAIChatter',
    'GoogleChatter',
    'AsyncGoogleChatter',
    'AsyncGoogleVision',
    'BingChatter',
    'AsyncBingChatter',
    'Context',
    'base',
    'constants',
    'prompts',
]
