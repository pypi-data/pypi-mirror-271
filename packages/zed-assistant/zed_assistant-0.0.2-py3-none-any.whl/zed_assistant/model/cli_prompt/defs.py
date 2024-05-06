from dataclasses import dataclass
from enum import Enum
from typing import List, Optional


class CliCommandType(str, Enum):
    COMMAND = "COMMAND"
    CONFIRM = "CONFIRM"
    ANSWER = "ANSWER"


@dataclass
class CliPromptInput:
    query: str


@dataclass
class CliPromptOutput:
    answer: Optional[str] = None
    command: Optional[str] = None
    needs_confirmation: bool = True


@dataclass
class CliPromptExchange:
    query: str
    response: str
    was_confirmed: bool


@dataclass
class CliPromptContext:
    history: List[CliPromptExchange]
    user: str
    path: str
    files_in_path: List[str]
