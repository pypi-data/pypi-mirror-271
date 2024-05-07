"""
    context_chat.agents.constants

Constants for module agents. Some are used in other modules.
Most constants comes from OpenAI documentation. See:
https://platform.openai.com/docs/models
"""

MODELS = (
    'gpt-3.5-turbo-0125',
    'gpt-3.5-turbo-1106',
    'gpt-4-turbo-preview',
    'gpt-4-0125-preview',  # 3
    'gpt-4-1106-preview',
    'gpt-4-vision-preview',
    'gemini-pro',  # Google # 6
    'gemini-pro-vision'
)

MAX_TOKENS = (
    (MODELS[0], 16385),
    (MODELS[1], 16385),
    (MODELS[2], 8192),
    (MODELS[3], 128000),
    (MODELS[4], 128000),
    (MODELS[5], 128000),
    (MODELS[6], 30720),
    (MODELS[7], 12288),
)

ROLES = (  # roles for messages objects
    'system',
    'user',
    'assistant',
    'model'  # Google gemini
)  # see https://platform.openai.com/docs/guides/gpt/chat-completions-api

"""Constants for embeddings operations"""

MODELS_EMBEDDING = (
    'text-embedding-3-small',
    'text-embedding-3-large',
    'text-embedding-ada-002',
    'models/embedding-001',
    'models/text-embedding-004',
)

TOKENIZER = (
    'cl100k_base',
)

EMBEDDINGS_COLUMNS = ('chunks', 'n_tokens', 'embeddings',)
