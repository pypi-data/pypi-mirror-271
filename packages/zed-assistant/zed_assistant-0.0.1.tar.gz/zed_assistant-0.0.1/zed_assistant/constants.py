from typing import Literal

OAI_KEY_ENV_VARIABLE = "ZED_OAI_KEY"

OpenAiModel = Literal["gpt-4", "gpt-4-turbo", "gpt-3.5-turbo"]

DEFAULT_MODEL = "gpt-4-turbo"
"""
The default OpenAI model used by Zed.
"""
