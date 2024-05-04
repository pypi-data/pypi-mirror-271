import os
import logging

from typing import Dict, List, Union
from abc import ABC, abstractmethod
from functools import wraps

from dotenv import load_dotenv

# APIs
# ----
from openai import OpenAI
from openai import AsyncOpenAI

import google.generativeai as genai
from google.generativeai.types.content_types import ContentType

from g4f.client import Client as ClientG4F
from g4f.Provider import Bing
# ----

from .constants import MODELS, MAX_TOKENS, ROLES
from .utils import number_of_tokens
from .errors import MessageError, AgentError, AgentRuntimeError
from .settings import DEBUG

logger = logging.getLogger('standard')


class BaseChatter(ABC):
    """
        Sync version of base class for chatter
    """
    
    def __init__(self,
                 *args,
                 setup: str = None,
                 api_key: str = None,
                 temperature: float = 0.0,
                 model: str = None,
                 **kwargs):
        """
        Base class for all agents main attribute: a chatter.

        Parameters
        ----------
        setup : str, optional
            Text for setting up a model's or assistant's role.

            This text should be a clear statement of how the model should
            respond the user's queries. Try to make it so that the model or
            assistant get rid of any coercion or user's attempt to diverge from
            the purpose and intention of the designed agent.
        api_key : str
            Most models, if not all, requires an API key to make queries.
        temperature: float
            The sampling temperature, between 0 and 1.
            Higher values like 0.8 will make the output more random,
            while lower values like 0.2 will make it more focused and
            deterministic.
        model: str
            Model string identification. See .constants.MODELS.
        Returns
        -------
        None
        """
        temperature = max(temperature, 0.0)
        temperature = min(temperature, 1.0)

        # settings and attributes
        self.setup = setup
        self.model = model  # model's name (see corresponding API's docs)
        self.temperature = temperature
        self.max_tokens = None  # query's token window
        self.messages: List[Dict] = []
        self.messages_backup: List[Dict] = []
        self.messages_summary: List[Dict] = []
        self.last_response = None
        self.api_key = None
        self.organization = None
        # ~self.client~
        # this is the main API's object for sending
        # user's queries. For example, OpenAI's client is openai.OpenAI or
        # openai.AsyncOpenAI;
        # while for Google's it is genai.GenerativeModel
        self.client: Union[
            OpenAI, AsyncOpenAI, genai.GenerativeModel, ClientG4F
        ] = self._configure(
            *args, api_key=api_key, **kwargs
        )

    @abstractmethod
    def _configure(self, *args, api_key, **kwargs):
        """
        With this method you should configure the agent by:
            - set API keys;
            - set self.max_tokens according to the model;
            - initialize the self.client object;
            - initialize self.messages in case of self.setup is not None;

        Parameters
        ----------
            *args: Any
                Positional arguments to construct the self.client object
            **kwargs: Any
                Keywords arguments to construct the self.client object
        Returns
        -------
            client:
                Main API's caller object for text generation.
                See the corresponding documentation:
                    - Google: https://ai.google.dev/tutorials/python_quickstart
                    - Openai: https://platform.openai.com/docs/introduction
        """
        return self.client
    
    @abstractmethod
    def answer(self,
               prompt: str,
               use_agent: bool = True,
               conversation: bool = True,
               **kwargs) -> str:
        """
        Generate a response to the given prompt.

        This method MUST call self.__update twice: once at the start and
        one more time after self.client's query response.

        Parameters:
            prompt (str): The prompt message for generating a response.

        Returns:
            str: The generated response content.
        """
        pass

    @abstractmethod
    def _update(self,
                *args,
                role: str,
                content: str,
                use_agent: bool = True,
                agent=None,
                **kwargs):

        """
        Update the conversation with a new message.

        Parameters:
        ----------
            role (str):
                The role of the message (e.g., 'system', 'user', 'assistant',
                'model'). See constants.
            content (str):
                The content of the message.
            use_agent (bool):
                Whether or not use a agent to summarize messages
            agent (Agent):
                Any agent instance that has 'answer' method implemented.
        """
    
    @abstractmethod
    def _reduce_number_of_tokens_if_needed(self, *args, **kwargs):
        """
        Reduce messages if they exceed self.max_tokens

        Parameters:
        ----------
            **kwargs:
                arguments for self.client's method for querying
                summary message.
        """


class OpenAIChatterMixin:

    def _is_async_client(self,):
        if isinstance(self.client, AsyncOpenAI):
            return True
        return False

    def _configure(self,
                   *args,
                   api_key: str = None,
                   organization: str = None,
                   async_client: bool = False,
                   **kwargs):
        
        self._load_credentials(api_key=api_key, organization=organization)
        
        self.max_tokens = dict(MAX_TOKENS)[self.model]

        if self.setup:
            self.messages.append(
                {
                    'role': ROLES[0],
                    'content': self.setup
                }
            )
        return self._set_client(async_client=async_client, **kwargs)

    def _load_credentials(self, api_key: str, organization: str = None):

        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.organization = organization or os.getenv(
            "OPENAI_API_ORGANIZATION"
        )

        if not self.api_key:
            load_dotenv()
            self.api_key = os.getenv("OPENAI_API_KEY")
            if not self.api_key:
                raise AgentRuntimeError(
                    "Environment variable OPENAI_API_KEY not set"
                )

    def _set_client(self, async_client=False, **kwargs):
        
        if async_client:
            return AsyncOpenAI(
                api_key=self.api_key,
                organization=self.organization,
                **kwargs
            )

        return OpenAI(
            api_key=self.api_key,
            organization=self.organization,
            **kwargs
        )

    def _update(self,
                *args,
                role: str,
                content: str,
                use_agent=True,
                agent=None):

        """
        Update the conversation with a new message.
        
        Parameters:
            role (str): The role of the message (e.g.,
                'system', 'user', 'assistant').
            content (str): The content of the message.
        """
        if role not in ROLES:
            raise KeyError(f"`role` must be one of: {ROLES}")

        if not isinstance(content, str):
            raise TypeError('`content` must be a string')

        message = {
            'role': role,
            'content': content
        }
        self.messages.append(message)
        self.messages_backup.append(message)
        self._reduce_number_of_tokens_if_needed(
            use_agent=use_agent, agent=agent
        )

    def _reduce_number_of_tokens_if_needed(
            self,
            *args,
            use_agent=True,
            agent=None,
            **kwargs
    ) -> None:
        """
        Reduces the number of tokens in the conversation if it exceeds the
        maximum allowed. It tries to summarize the conversation first and
        removes the oldest messages if necessary.

        Parameters:
        -----------
            use_agent (bool): whether use a separate GPT chat to summarize
                large messages
            agent (Agent):
                Any agent instance that has 'answer' method implemented.
        Returns:
            None
        """
        n_tokens = number_of_tokens(self.messages, self.model)
        while n_tokens > self.max_tokens:
            if use_agent and len(self.messages) > 2:
                # Attempt to summarize the conversation
                summary_prompt = (
                    "Please summarize the following conversation: "
                    "(IMPORTANT: keep the user's language):\n"
                )
                if self.setup:
                    summary_prompt += "\n".join(
                        message['content'] for message in self.messages[1:-1]
                    )
                else:
                    summary_prompt += "\n".join(
                        message['content'] for message in self.messages[:-1]
                    )
                if agent is None:
                    raise ValueError(
                        "For use_agent=True, you must provide and `agent`"
                    )
                summary_content = agent.answer(
                    prompt=summary_prompt,
                    use_agent=False,
                    conversation=False
                )

                # Replace the conversation with the summary and the
                # last message
                if self.setup:
                    self.messages = [
                        self.messages[0],
                        {'role': ROLES[1], 'content': summary_content},
                        self.messages[-1]
                    ]
                else:
                    self.messages = [
                        {'role': ROLES[1], 'content': summary_content},
                        self.messages[-1]
                    ]

                if DEBUG:
                    logger.info(
                        'Conversation summarized: %s', summary_content
                    )
            else:
                # Remove the oldest message if summarization is not possible
                # or did not help
                if self.setup:
                    removed_message = self.messages.pop(1)
                else:
                    removed_message = self.messages.pop(0)
                if DEBUG:
                    logger.warning(
                        'Oldest removed message: %s',
                        removed_message['content']
                    )

            # Recalculate the number of tokens after modification
            n_tokens = number_of_tokens(self.messages, self.model)

            if n_tokens <= self.max_tokens:
                break  # Exit the loop if we are within the token limit

            if len(self.messages) <= 2:
                # If we cannot reduce further, raise an error
                if self.setup or len(self.messages) == 1:
                    raise MessageError(
                        'Conversation exceeds maximum number of '
                        'tokens and cannot be reduced further.'
                    )

    def change_model(self, model: str | int):
        """
        Change the model used by the chatter.

        Parameters
        ----------
        model : Union[str, int]
            The model to switch to. Can be a string representing the model name
            or an integer index.

        Returns
        -------
        None
        """
        if isinstance(model, str):
            if model not in MODELS:
                raise ValueError(f"`model` must be one of {', '.join(MODELS)}")
            self.model = model
            self.max_tokens = dict(MAX_TOKENS)[model]
        elif isinstance(model, int):
            if model >= len(MODELS) or model < 0:
                models = '\n'.join(
                    [f"{idx+1}. {model}" for idx, model in enumerate(MODELS)]
                )
                raise ValueError(
                    f"`model` must be: {models}"
                )
            self.model = MODELS[model]
            self.max_tokens = MAX_TOKENS[model][1]


class GoogleChatterMixin:

    def _configure(self,
                   *args,
                   api_key: str = None,
                   **kwargs):
        if self.model is None:
            self.model = MODELS[6]
        if self.model not in MODELS[6:]:
            raise AgentError(f"Google models are: {', '.join(MODELS[6:])}")
        self.max_tokens = dict(MAX_TOKENS)[self.model]
        self.__load_credentials(api_key=api_key)
        
        self.max_tokens = dict(MAX_TOKENS)[self.model]

        if self.setup:
            self.messages.extend(
                [
                    {
                        'role': ROLES[1],
                        'parts': [self.setup,],
                    },
                    {
                        'role': ROLES[-1],
                        'parts': ['Understood',],
                    }
                ]
            )
        return self._set_client(**kwargs)

    def __load_credentials(self, api_key: str):
        
        self.api_key = api_key or os.getenv('GOOGLE_AI_API_KEY')

        if self.api_key is None:
            load_dotenv()
            self.api_key = os.getenv('GOOGLE_AI_API_KEY')
            if not self.api_key:
                raise AgentRuntimeError(
                    "Environment variable GOOGLE_AI_API_KEY not set"
                )

    def _set_client(self, **kwargs):
        genai.configure(api_key=self.api_key)
        return genai.GenerativeModel(model_name=self.model, **kwargs)

    def _update(self, role: str, content: ContentType, use_agent=True, agent=None):

        """
        Update the conversation with a new message.
        
        Parameters:
            role (str): The role of the message (e.g.,
                'system', 'user', 'assistant').
            content (str): The content of the message.
        """
        if role not in [ROLES[1], ROLES[-1]]:
            raise KeyError(f"`role` must be {ROLES[1]} or {ROLES[-1]}")

        # TODO: handle content type check
        # if not isinstance(content, ContentType):
        #     raise TypeError('`content` must be a ContentType')

        message = {
            'parts': [content],
            'role': role
        }
        self.messages.append(message)
        self.messages_backup.append(message)
        self._reduce_number_of_tokens_if_needed(use_agent, agent)

    def _reduce_number_of_tokens_if_needed(
            self,
            *args,
            use_agent=True,
            agent=None,
            **kwargs
    ):
        """
        Reduces the number of tokens in the conversation if it exceeds the
        maximum allowed. It tries to summarize the conversation first and
        removes the oldest messages if necessary.

        Parameters:
        -----------
            use_agent (bool): whether use a separate GPT chat to summarize
                large messages
            agent (Agent):
                Any agent instance that has 'answer' method implemented.

        Returns:
            None
        """
        n_tokens = self.client.count_tokens(self.messages)
        while n_tokens.total_tokens > self.max_tokens:
            if use_agent and len(self.messages) > 2:
                # Attempt to summarize the conversation
                summary_prompt = (
                    "Please summarize the following conversation "
                    "(IMPORTANT: keep the user's language):\n"
                )
                if self.set_up:
                    summary_prompt += "\n".join(
                        message['parts'] for message in self.messages[1:-1]
                    )
                else:
                    summary_prompt += "\n".join(
                        message['parts'] for message in self.messages[:-1]
                    )

                summary_content = agent.answer(
                    prompt=summary_prompt,
                    use_agent=False,
                    conversation=False
                )

                # Replace the conversation with the summary and the
                # last message
                if self.set_up:
                    self.messages = [
                        self.messages[0],
                        {'role': ROLES[1], 'parts': [summary_content]},
                        self.messages[-1]
                    ]
                else:
                    self.messages = [
                        {'role': ROLES[1], 'parts': [summary_content]},
                        self.messages[-1]
                    ]

                if DEBUG:
                    logger.info(
                        'Conversation summarized: %s', summary_content
                    )
            else:
                # Remove the oldest message if summarization is not possible
                # or did not help
                if self.set_up:
                    removed_message = self.messages.pop(1)
                else:
                    removed_message = self.messages.pop(0)
                if DEBUG:
                    logger.warning(
                        'Oldest removed message: %s',
                        removed_message['parts']
                    )

            # Recalculate the number of tokens after modification
            n_tokens = self.client.count_tokens(self.messages)

            if n_tokens.total_tokens <= self.max_tokens:
                break  # Exit the loop if we are within the token limit

            if len(self.messages) <= 2:
                # If we cannot reduce further, raise an error
                if self.set_up or len(self.messages) == 1:
                    raise MessageError(
                        'Conversation exceeds maximum number of '
                        'tokens and cannot be reduced further.'
                    )


class BingChatterMixin(OpenAIChatterMixin):

    def _configure(self,
                   *args,
                   api_key: str = None,
                   **kwargs):
        try:
            self._load_credentials(api_key=api_key)
        except AgentRuntimeError as err:
            logger.warning(
                "%s. Agent won't use callback in case of call error.", err
            )
        # TODO: find out what is the max tokens for bing provider
        self.max_tokens = dict(MAX_TOKENS)[self.model]
        if self.setup:
            self.messages.append(
                {
                    'role': ROLES[0],
                    'content': self.setup
                }
            )
        return self._set_client(**kwargs)
    
    def _set_client(self, **kwargs):
        return ClientG4F(provider=Bing, **kwargs)

    def change_model(self, model: str | int):
        """Bing provider only uses gtp-4"""
        logger.warning("Bing provider only uses gtp-4")
        return super().change_model(model=self.model)
