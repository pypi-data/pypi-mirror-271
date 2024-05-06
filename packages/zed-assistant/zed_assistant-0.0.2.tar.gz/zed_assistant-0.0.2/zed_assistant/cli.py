import asyncio
import logging
import os
import sys
from argparse import ArgumentParser
from typing import get_args

from zed_assistant import __version__, zed
from zed_assistant.constants import DEFAULT_MODEL, OAI_KEY_ENV_VARIABLE, OpenAiModel

logging.basicConfig(stream=sys.stdout)
log = logging.getLogger(__name__)

zed_ascii = rf"""
     ______ ___________
    |___  /|  ___|  _  \
       / / | |__ | | | |
      / /  |  __|| | | |
    ./ /___| |___| |/ /
    \_____/\____/|___/  v{__version__}
"""


def main():
    parser = ArgumentParser(
        description="zed is a LLM-based CLI assistant built with python and Chat GPT",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    parser.add_argument(
        "--debug",
        default=False,
        action="store_true",
        help="Enables print debug logs.",
    )
    parser.add_argument(
        "--model",
        type=str,
        choices=get_args(OpenAiModel),
        default=DEFAULT_MODEL,
        help=f"The specific Open AI model to be used. Default is '{DEFAULT_MODEL}'.",
    )
    parser.add_argument(
        "--open-ai-key",
        type=str,
        required=False,
        help=f"The Open AI API key. You can also set the environment variable {OAI_KEY_ENV_VARIABLE}.",
    )
    parsed, user_query = parser.parse_known_args()

    is_debug: bool = parsed.debug
    model: OpenAiModel = parsed.model
    oai_key = parsed.open_ai_key or os.environ.get(OAI_KEY_ENV_VARIABLE)

    log.setLevel(logging.DEBUG if is_debug else logging.WARNING)
    log.debug(f"arguments: {is_debug = }, {model =}, {user_query}")

    if not oai_key:
        log.error(
            f" Open AI key is missing. Please set the '{OAI_KEY_ENV_VARIABLE}' "
            "environment variable, or as a command parameter."
        )
        sys.exit(-1)
    if not user_query:
        log.debug(" No question or comment provided to zed.")
        print(zed_ascii)
        parser.print_help()
        sys.exit(0)

    success = asyncio.run(
        zed.run(
            log=log,
            oai_key=oai_key,
            model=model,
            user_query=" ".join(user_query),
        )
    )
    sys.exit(0 if success else -1)


if __name__ == "__main__":
    main()
