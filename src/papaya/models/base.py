from abc import ABC, abstractmethod
from typing import Sequence

from ..messages import Message
from ..tools import Tool


class BaseModel(ABC):
    @abstractmethod
    def generate(self, messages: list[Message], tools: Sequence[Tool] | None = None) -> Message:
        pass
