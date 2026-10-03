from dataclasses import dataclass, field
from typing import Any

from .messages import Message


@dataclass
class RunResult:
    text: str
    messages: list[Message] = field(default_factory=list)
    status: str = "completed"
    tool_calls: list[dict[str, Any]] = field(default_factory=list)
