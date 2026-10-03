import json
import os
from typing import Sequence

from openai import OpenAI

from .base import BaseModel
from ..messages import AssistantMessage, Message, ToolCall
from ..tools import Tool


class OpenAIModel(BaseModel):
    def __init__(self, api_key: str | None = None, model_name: str = "gpt-4o-mini"):
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        self.model_name = model_name

    def generate(self, messages: list[Message], tools: Sequence[Tool] | None = None) -> Message:
        formatted_messages = self._format_messages(messages)
        
        kwargs = {
            "model": self.model_name,
            "messages": formatted_messages,
        }
        
        if tools:
            kwargs["tools"] = [t.schema for t in tools]
            kwargs["tool_choice"] = "auto"
            
        response = self.client.chat.completions.create(**kwargs)
        choice = response.choices[0].message
        
        tool_calls = []
        if choice.tool_calls:
            for tc in choice.tool_calls:
                args = json.loads(tc.function.arguments)
                tool_calls.append(
                    ToolCall(
                        id=tc.id,
                        name=tc.function.name,
                        arguments=args
                    )
                )
                
        return AssistantMessage(
            content=choice.content,
            tool_calls=tool_calls
        )

    def _format_messages(self, messages: list[Message]) -> list[dict]:
        formatted = []
        for msg in messages:
            if msg.role in ["system", "user"]:
                formatted.append({"role": msg.role, "content": msg.content})
            elif msg.role == "assistant":
                d = {"role": "assistant", "content": msg.content}
                if getattr(msg, "tool_calls", None):
                    d["tool_calls"] = [
                        {
                            "id": tc.id,
                            "type": "function",
                            "function": {
                                "name": tc.name,
                                "arguments": json.dumps(tc.arguments)
                            }
                        }
                        for tc in msg.tool_calls
                    ]
                formatted.append(d)
            elif msg.role == "tool":
                formatted.append({
                    "role": "tool",
                    "tool_call_id": getattr(msg, "tool_call_id", ""),
                    "content": str(msg.content)
                })
        return formatted
