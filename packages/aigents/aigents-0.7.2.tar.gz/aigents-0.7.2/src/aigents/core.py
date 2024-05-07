import os
import logging
import asyncio
from pathlib import Path
from typing import Union

from dotenv import load_dotenv
from PIL import Image

import google.generativeai as genai
from g4f.Provider.Bing import Tones

from .base import BaseChatter
from .base import OpenAIChatterMixin
from .base import GoogleChatterMixin
from .base import BingChatterMixin

from .utils import LastResponse
from .errors import AgentError
from .constants import MODELS, ROLES
from .settings import DEBUG

logger = logging.getLogger('standard')


class OpenAIChatter(OpenAIChatterMixin, BaseChatter):
    def __init__(self,
                 *args,
                 setup: str = None,
                 api_key: str = None,
                 organization: str = None,
                 temperature: float = 0.0,
                 model: str = MODELS[0],
                 **kwargs):
        """
        Initialize an Openai based Chatter instance.

        Parameters
        ----------
        *args:
            Arguments for the __configure method.
        setup : str, optional
            Text for setting up a model's or assistant's role.

            This text should be a clear statement of how the model should
            respond the user's queries. Try to make it so that the model or
            assistant get rid of any coercion or user's attempt to diverge from
            the purpose and intention of the designed agent.
        api_key : str
            OpenAI API key for authentication (see
            https://platform.openai.com/account/api-keys)
            You can provide API key in a .env file
        organization: str
            Unique identifier for your organization which can be used in
            Openai's API requests.
        temperature: float
            The sampling temperature, between 0 and 1.
            Higher values like 0.8 will make the output more random,
            while lower values like 0.2 will make it more focused and
            deterministic.
        model: str
            Model string identification. See .constants.MODELS.
        **kwargs:
            Keyword arguments for the __configure method.
        Returns
        -------
        None
        """
        super().__init__(*args,
                         setup=setup,
                         api_key=api_key,
                         temperature=temperature,
                         model=model,
                         organization=organization,
                         **kwargs)

    def answer(self,
               prompt,
               use_agent=True,
               conversation=True,
               agent=None,
               **kwargs):
        """
        Generate a response to the given prompt.

        Parameters:
        -----------
            prompt (str): The prompt message for generating a response.
            use_agent (bool): whether use a separate GPT chat to summarize
                large messages
            conversation (bool): whether stream messages in a single
                conversation
            agent (Agent):
                Any agent instance that has 'answer' method implemented.

        Returns:
            str: The generated response content.
        """
        if use_agent and agent is None:
            setup = (
                "You are a very skilled writer that can summarize any text "
                "while preserving the whole meaning of its content."
            )
            agent = OpenAIChatter(
                setup=setup,
                model=MODELS[0],
                api_key=self.api_key,
                organization=self.organization
            )
            agent.max_tokens = self.max_tokens // 4  # Limit summary length
        if agent and asyncio.iscoroutinefunction(agent.answer):
            raise AgentError('Summarizer agent must be synchronous')
        self._update(
            role=ROLES[1], content=prompt, use_agent=use_agent, agent=agent
        )
        if self.setup:
            messages = self.messages if conversation else [
                self.messages[0], self.messages[-1]
            ]
        else:
            messages = self.messages if conversation else self.messages[-2:]

        self.last_response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            **kwargs
        )

        response_content = self.last_response.choices[0].message.content
        self._update(
            role=ROLES[1],
            content=response_content,
            use_agent=use_agent,
            agent=agent
        )

        return response_content


class AsyncOpenAIChatter(OpenAIChatterMixin, BaseChatter):
    def __init__(self,
                 *args,
                 setup: str = None,
                 api_key: str = None,
                 organization: str = None,
                 temperature: float = 0.0,
                 model: str = MODELS[0],
                 **kwargs):
        """
        Initialize an Async Openai based Chatter instance.

        Parameters
        ----------
        *args:
            Arguments for the __configure method.
        setup : str, optional
            Text for setting up a model's or assistant's role.

            This text should be a clear statement of how the model should
            respond the user's queries. Try to make it so that the model or
            assistant get rid of any coercion or user's attempt to diverge from
            the purpose and intention of the designed agent.
        api_key : str
            OpenAI API key for authentication (see
            https://platform.openai.com/account/api-keys)
        organization: str
            Unique identifier for your organization which can be used in
            Openai's API requests.
        temperature: float
            The sampling temperature, between 0 and 1.
            Higher values like 0.8 will make the output more random,
            while lower values like 0.2 will make it more focused and
            deterministic.
        model: str
            Model string identification. See .constants.MODELS.
        **kwargs:
            Keyword arguments for the __configure method.
        Returns
        -------
        None
        """
        super().__init__(*args,
                         setup=setup,
                         api_key=api_key,
                         temperature=temperature,
                         model=model,
                         organization=organization,
                         async_client=True,
                         **kwargs)

    async def answer(self,
                     prompt,
                     use_agent=True,
                     conversation=True,
                     agent=None,
                     **kwargs):
        """
        Generate a response to the given prompt.

        Parameters:
        -----------
            prompt (str): The prompt message for generating a response.
            use_agent (bool): whether use a separate GPT chat to summarize
                large messages
            conversation (bool): whether stream messages in a single
                conversation
            agent (Agent):
                Any agent instance that has 'answer' method implemented.

        Returns:
            coroutine:
                coroutine that when awaited, return the
                generated response content.
        """
        if use_agent and agent is None:
            setup = (
                "You are a very skilled writer that can summarize any text "
                "while preserving the whole meaning of its content."
            )
            agent = OpenAIChatter(
                setup=setup,
                model=MODELS[0],
                api_key=self.api_key,
                organization=self.organization
            )
            agent.max_tokens = self.max_tokens // 4  # Limit summary length
        if agent and asyncio.iscoroutinefunction(agent.answer):
            raise AgentError('Summarizer agent must be synchronous')
        self._update(
            role=ROLES[1], content=prompt, use_agent=use_agent, agent=agent
        )
        if self.setup:
            messages = self.messages if conversation else [
                self.messages[0], self.messages[-1]
            ]
        else:
            messages = self.messages if conversation else self.messages[-2:]

        self.last_response = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            **kwargs
        )

        response_content = self.last_response.choices[0].message.content
        self._update(
            role=ROLES[1],
            content=response_content,
            use_agent=use_agent,
            agent=agent
        )

        return response_content


class GoogleChatter(GoogleChatterMixin, BaseChatter):
    def __init__(self,
                 *args,
                 setup: str = None,
                 api_key: str = None,
                 temperature: float = 0.0,
                 **kwargs):
        """
        Initialize a Google based Chatter instance.

        Parameters
        ----------
        *args:
            Arguments for the __configure method.
        setup : str, optional
            Text for setting up a model's or assistant's role.

            This text should be a clear statement of how the model should
            respond the user's queries. Try to make it so that the model or
            assistant get rid of any coercion or user's attempt to diverge from
            the purpose and intention of the designed agent.
        api_key : str
            Google AI API key for authentication (see
            https://makersuite.google.com/app/apikey)
        temperature: float
            The sampling temperature, between 0 and 1.
            Higher values like 0.8 will make the output more random,
            while lower values like 0.2 will make it more focused and
            deterministic.
        model: str
            Model string identification. See .constants.MODELS.
        **kwargs:
            Keyword arguments for the __configure method.
        Returns
        -------
        None
        """
        super().__init__(*args,
                         setup=setup,
                         api_key=api_key,
                         temperature=temperature,
                         model=MODELS[6],
                         **kwargs)

    def answer(self,
               prompt,
               use_agent=True,
               conversation=True,
               agent=None,
               **kwargs):
        if use_agent and agent is None:
            setup = (
                "You are a very skilled writer that can summarize any text "
                "while preserving the whole meaning of its content."
            )
            agent = GoogleChatter(setup=setup, api_key=self.api_key)
            agent.max_tokens = self.max_tokens // 4  # Limit summary length
        messages = None
        
        self._update(ROLES[1], prompt, use_agent=use_agent, agent=agent)
        
        if self.setup:
            messages = self.messages if conversation else [
                *self.messages[:2], self.messages[-1]
            ]
        else:
            messages = self.messages if conversation else self.messages[-2:]

        config = genai.types.GenerationConfig(temperature=self.temperature)

        response = self.client.generate_content(
            messages, generation_config=config
        )
        self.last_response = response
        try:
            self._update(
                ROLES[-1],
                response.text,
                use_agent=use_agent,
                agent=agent
            )
            return response.text
        except ValueError:
            text = '\n'.join(
                [part.text for part in response.candidates[0].content.parts]
            )
            self._update(
                ROLES[-1],
                text,
                use_agent=use_agent,
                agent=agent
            )
            return text


class AsyncGoogleChatter(GoogleChatter):
    def __init__(self,
                 *args,
                 setup: str = None,
                 api_key: str = None,
                 temperature: float = 0.0,
                 **kwargs):
        """
        Initialize am async Google based Chatter instance.

        Parameters
        ----------
        *args:
            Arguments for the __configure method.
        setup : str, optional
            Text for setting up a model's or assistant's role.

            This text should be a clear statement of how the model should
            respond the user's queries. Try to make it so that the model or
            assistant get rid of any coercion or user's attempt to diverge from
            the purpose and intention of the designed agent.
        api_key : str
            OpenAI API key for authentication (see
            https://platform.openai.com/account/api-keys)
        temperature: float
            The sampling temperature, between 0 and 1.
            Higher values like 0.8 will make the output more random,
            while lower values like 0.2 will make it more focused and
            deterministic.
        model: str
            Model string identification. See .constants.MODELS.
        **kwargs:
            Keyword arguments for the __configure method.
        Returns
        -------
        None
        """
        super().__init__(*args,
                         setup=setup,
                         api_key=api_key,
                         temperature=temperature,
                         **kwargs)

    async def answer(self,
                     prompt,
                     use_agent=True,
                     conversation=True,
                     agent=None,
                     **kwargs):
        if use_agent and agent is None:
            setup = (
                "You are a very skilled writer that can summarize any text "
                "while preserving the whole meaning of its content."
            )
            agent = GoogleChatter(setup=setup, api_key=self.api_key)
            agent.max_tokens = self.max_tokens // 4  # Limit summary length
        messages = None
        
        self._update(ROLES[1], prompt, use_agent=use_agent, agent=agent)
        
        if self.setup:
            messages = self.messages if conversation else [
                *self.messages[:2], self.messages[-1]
            ]
        else:
            messages = self.messages if conversation else self.messages[-2:]
        
        config = genai.types.GenerationConfig(temperature=self.temperature)
        response = await self.client.generate_content_async(
            messages, generation_config=config
        )

        try:
            self._update(
                ROLES[-1], response.text, use_agent=use_agent, agent=agent
            )
            return response.text
        except ValueError:
            text = '\n'.join(
                [part.text for part in response.candidates[0].content.parts]
            )
            self._update(
                ROLES[-1],
                text,
                use_agent=use_agent,
                agent=agent
            )
            return text


class GoogleVision(GoogleChatterMixin, BaseChatter):
    def __init__(self,
                 *args,
                 setup: str = None,
                 api_key: str = None,
                 temperature: float = 0.0,
                 **kwargs):
        """
        Initialize a Google based Chatter instance.

        Parameters
        ----------
        *args:
            Arguments for the __configure method.
        setup : str, optional
            Text for setting up a model's or assistant's role.

            This text should be a clear statement of how the model should
            respond the user's queries. Try to make it so that the model or
            assistant get rid of any coercion or user's attempt to diverge from
            the purpose and intention of the designed agent.
        api_key : str
            Google AI API key for authentication (see
            https://makersuite.google.com/app/apikey)
        temperature: float
            The sampling temperature, between 0 and 1.
            Higher values like 0.8 will make the output more random,
            while lower values like 0.2 will make it more focused and
            deterministic.
        **kwargs:
            Keyword arguments for the __configure method.
        Returns
        -------
        None
        """
        super().__init__(*args,
                         setup=setup,
                         api_key=api_key,
                         temperature=temperature,
                         model=MODELS[7],
                         **kwargs)

    def answer(self,
               img: Union[str, Path, Image.Image],
               prompt: str = None,
               **kwargs):
        """
        Generate a response based on the given image and optional prompt.

        Parameters
        ----------
        img : str, Image.Image or Path
            The image to analyze. Can be a file path as a string or an Image.Image object.
        prompt : str, optional
            An optional prompt to guide the response. Default is None.
        **kwargs : dict, optional
            Additional keyword arguments for the method.

        Returns
        -------
        str
            The generated response content based on the image and prompt.

        Examples
        --------
        >>> vision = GoogleVision(api_key='your_api_key')
        >>> response = vision.answer('path/to/image.jpg', 'Describe the image.')
        >>> print(response)
        'The image shows a beautiful landscape with mountains and a river.'

        Notes
        -----
        This method generates a response based on the provided image and optional prompt.
        """
        # TODO: add messages system
        if isinstance(img, (str, Path)):
            img = Image.open(img)
        message = img
        if prompt:
            message = [prompt, img]
        response = self.client.generate_content(
            message
        )
        try:
            return response.text
        except ValueError:
            if len(response.candidates) == 0:
                logger.error(
                    "Prompt was blocked: %s.\nPrompt: %s",
                    response.prompt_feedback,
                    prompt
                )
                return '{"error": try another prompt}'
            text = '\n'.join(
                [part.text for part in response.candidates[0].content.parts]
            )
            return text


class AsyncGoogleVision(GoogleChatterMixin, BaseChatter):
    def __init__(self,
                 *args,
                 setup: str = None,
                 api_key: str = None,
                 temperature: float = 0.0,
                 **kwargs):
        """
        Initialize a Google based Chatter instance.

        Parameters
        ----------
        *args:
            Arguments for the __configure method.
        setup : str, optional
            Text for setting up a model's or assistant's role.

            This text should be a clear statement of how the model should
            respond the user's queries. Try to make it so that the model or
            assistant get rid of any coercion or user's attempt to diverge from
            the purpose and intention of the designed agent.
        api_key : str
            Google AI API key for authentication (see
            https://makersuite.google.com/app/apikey)
        temperature: float
            The sampling temperature, between 0 and 1.
            Higher values like 0.8 will make the output more random,
            while lower values like 0.2 will make it more focused and
            deterministic.
        **kwargs:
            Keyword arguments for the __configure method.
        Returns
        -------
        None
        """
        super().__init__(*args,
                         setup=setup,
                         api_key=api_key,
                         temperature=temperature,
                         model=MODELS[7],
                         **kwargs)

    async def answer(self,
                     img: Union[str, Path, Image.Image],
                     prompt: str = None,
                     **kwargs):
        """
        Generate a response based on the given image and optional prompt.

        Parameters
        ----------
        img : str, Image.Image or Path
            The image to analyze. Can be a file path as a string or an Image.Image object.
        prompt : str, optional
            An optional prompt to guide the response. Default is None.
        **kwargs : dict, optional
            Additional keyword arguments for the method.

        Returns
        -------
        str
            The generated response content based on the image and prompt.

        Examples
        --------
        >>> vision = AsyncGoogleVision(api_key='your_api_key')
        >>> response = await vision.answer('path/to/image.jpg', 'Describe the image.')
        >>> print(response)
        'The image shows a beautiful landscape with mountains and a river.'

        Notes
        -----
        This method generates a response based on the provided image and optional prompt.
        """
        # TODO: add messages system
        if isinstance(img, (str, Path)):
            img = Image.open(img)
        message = img
        if prompt:
            message = [prompt, img]
        response = await self.client.generate_content_async(
            message
        )
        try:
            return response.text
        except ValueError:
            if len(response.candidates) == 0:
                logger.error(
                    "Prompt was blocked: %s.\nPrompt: %s",
                    response.prompt_feedback,
                    prompt
                )
                return '{"error": try another prompt}'
            text = '\n'.join(
                [part.text for part in response.candidates[0].content.parts]
            )
            return text


class BingChatter(BingChatterMixin, BaseChatter):
    def __init__(self,
                 *args,
                 setup: str = None,
                 api_key: str = None,
                 **kwargs):
        """
        Initialize an Openai based Chatter instance.

        Parameters
        ----------
        *args:
            Arguments for the __configure method.
        setup : str, optional
            Text for setting up a model's or assistant's role.

            This text should be a clear statement of how the model should
            respond the user's queries. Try to make it so that the model or
            assistant get rid of any coercion or user's attempt to diverge from
            the purpose and intention of the designed agent.
        api_key : str
            OpenAI API key for authentication (see
            https://platform.openai.com/account/api-keys)
            You can provide API key in a .env file

            NOTE: in future version, this class will use
            OpenAIChatter as callback, using gpt-4-turbo
        organization: str
            Unique identifier for your organization which can be used in
            Openai's API requests.
        temperature: float
            The sampling temperature, between 0 and 1.
            Higher values like 0.8 will make the output more random,
            while lower values like 0.2 will make it more focused and
            deterministic.
        model: str
            Model string identification. See .constants.MODELS.
        **kwargs:
            Keyword arguments for the __configure method.
        Returns
        -------
        None
        """
        super().__init__(*args,
                         setup=setup,
                         api_key=api_key,
                         temperature=0.0,
                         model=MODELS[2],
                         organization=None,
                         **kwargs)
    def answer(self,
               prompt,
               use_agent=True,
               conversation=True,
               agent=None,
               tone: str = Tones.precise,
               web_search: bool = False,
               **kwargs):
        """
        Generate a response to the given prompt.

        Parameters:
        -----------
            prompt (str): The prompt message for generating a response.
            use_agent (bool): whether use a separate GPT chat to summarize
                large messages
            conversation (bool): whether stream messages in a single
                conversation
            agent (Agent):
                Any agent instance that has 'answer' method implemented.
            tone (str):
                Expected tone of the message: Balanced, Creative or Precise
            web_search (bool):
                Flag to enable or disable web search.

        Returns:
            str: The generated response content.
        """
        if use_agent and agent is None:
            setup = (
                "You are a very skilled writer that can summarize any text "
                "while preserving the whole meaning of its content."
            )
            agent = BingChatter(
                setup=setup,
                model=self.model,
                api_key=self.api_key,
            )
            agent.max_tokens = self.max_tokens // 4  # Limit summary length
        if agent and asyncio.iscoroutinefunction(agent.answer):
            raise AgentError('Summarizer agent must be synchronous')
        self._update(
            role=ROLES[1], content=prompt, use_agent=use_agent, agent=agent
        )
        if self.setup:
            messages = self.messages if conversation else [
                self.messages[0], self.messages[-1]
            ]
        else:
            messages = self.messages if conversation else self.messages[-2:]

        response_content = self.client.chat.completions.provider.create(
            model=self.model,
            messages=messages,
            tone=tone,
            web_search=web_search,
            **kwargs
        )
        
        self.last_response = LastResponse()
        self.last_response.choices[0].message.content = response_content
        
        self._update(
            role=ROLES[1],
            content=response_content,
            use_agent=use_agent,
            agent=agent
        )

        return response_content


class AsyncBingChatter(BingChatterMixin, BaseChatter):
    def __init__(self,
                 *args,
                 setup: str = None,
                 api_key: str = None,
                 **kwargs):
        """
        Initialize an Openai based Chatter instance.

        Parameters
        ----------
        *args:
            Arguments for the __configure method.
        setup : str, optional
            Text for setting up a model's or assistant's role.

            This text should be a clear statement of how the model should
            respond the user's queries. Try to make it so that the model or
            assistant get rid of any coercion or user's attempt to diverge from
            the purpose and intention of the designed agent.
        api_key : str
            OpenAI API key for authentication (see
            https://platform.openai.com/account/api-keys)
            You can provide API key in a .env file

            NOTE: in future version, this class will use
            OpenAIChatter as callback, using gpt-4-turbo
        organization: str
            Unique identifier for your organization which can be used in
            Openai's API requests.
        temperature: float
            The sampling temperature, between 0 and 1.
            Higher values like 0.8 will make the output more random,
            while lower values like 0.2 will make it more focused and
            deterministic.
        model: str
            Model string identification. See .constants.MODELS.
        **kwargs:
            Keyword arguments for the __configure method.
        Returns
        -------
        None
        """
        super().__init__(*args,
                         setup=setup,
                         api_key=api_key,
                         temperature=0.0,
                         model=MODELS[2],
                         organization=None,
                         **kwargs)
    async def answer(self,
                     prompt,
                     use_agent=True,
                     conversation=True,
                     agent=None,
                     tone: str = Tones.precise,
                     web_search: bool = False,
                     **kwargs):
        """
        Generate a response to the given prompt.

        Parameters:
        -----------
            prompt (str): The prompt message for generating a response.
            use_agent (bool): whether use a separate GPT chat to summarize
                large messages
            conversation (bool): whether stream messages in a single
                conversation
            agent (Agent):
                Any agent instance that has 'answer' method implemented.
            tone (str):
                Expected tone of the message: Balanced, Creative or Precise
            web_search (bool):
                Flag to enable or disable web search.

        Returns:
            str: The generated response content.
        """
        if use_agent and agent is None:
            setup = (
                "You are a very skilled writer that can summarize any text "
                "while preserving the whole meaning of its content."
            )
            agent = BingChatter(
                setup=setup,
                api_key=self.api_key,
            )
            agent.max_tokens = self.max_tokens // 4  # Limit summary length
        if agent and asyncio.iscoroutinefunction(agent.answer):
            raise AgentError('Summarizer agent must be synchronous')
        self._update(
            role=ROLES[1], content=prompt, use_agent=use_agent, agent=agent
        )
        if self.setup:
            messages = self.messages if conversation else [
                self.messages[0], self.messages[-1]
            ]
        else:
            messages = self.messages if conversation else self.messages[-2:]
        
        create_async = self.client.chat.completions.provider.create_async
        response_content = await create_async(
            model=self.model,
            messages=messages,
            tone=tone,
            web_search=web_search,
            **kwargs
        )
        
        self.last_response = LastResponse()
        self.last_response.choices[0].message.content = response_content
        
        self._update(
            role=ROLES[1],
            content=response_content,
            use_agent=use_agent,
            agent=agent
        )

        return response_content

