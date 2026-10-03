from dataclasses import dataclass, field
from typing import Any, Literal


@dataclass
class ToolCall:
    id: str
    name: str
    arguments: dict[str, Any]


@dataclass
class Message:
    role: Literal["system", "user", "assistant", "tool"]
    content: str | None = None


@dataclass
class SystemMessage(Message):
    role: Literal["system"] = "system"


@dataclass
class UserMessage(Message):
    role: Literal["user"] = "user"


@dataclass
class AssistantMessage(Message):
    role: Literal["assistant"] = "assistant"
    tool_calls: list[ToolCall] = field(default_factory=list)


@dataclass
class ToolResultMessage(Message):
    role: Literal["tool"] = "tool"
    tool_call_id: str = ""
    name: str = ""
