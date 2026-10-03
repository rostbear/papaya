from dataclasses import dataclass, field
from .messages import Message


@dataclass
class Session:
    messages: list[Message] = field(default_factory=list)

    def add(self, message: Message) -> None:
        self.messages.append(message)
