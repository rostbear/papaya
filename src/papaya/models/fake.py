from typing import Sequence

from .base import BaseModel
from ..messages import AssistantMessage, Message
from ..tools import Tool


class FakeModel(BaseModel):
    def __init__(self, responses: Sequence[Message]):
        self.responses = list(responses)
        self._call_count = 0

    def generate(self, messages: list[Message], tools: Sequence[Tool] | None = None) -> Message:
        if self._call_count < len(self.responses):
            response = self.responses[self._call_count]
            self._call_count += 1
            return response
        
        return AssistantMessage(content="Out of responses")
