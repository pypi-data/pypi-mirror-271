from dataclasses import asdict, dataclass
from typing import Dict, Literal


@dataclass
class Settings:
    model: str
    max_tokens: int
    temperature: float
    stream: float

    def to_dict(self):
        return asdict(self)


class OpenAIMessage(Dict):
    role: Literal["assistant", "user"]
    content: str
