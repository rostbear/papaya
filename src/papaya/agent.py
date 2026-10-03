from typing import Sequence

from .messages import (
    AssistantMessage,
    SystemMessage,
    ToolResultMessage,
    UserMessage,
)
from .models.base import BaseModel
from .result import RunResult
from .session import Session
from .tools import Tool


class Agent:
    def __init__(
        self,
        model: BaseModel,
        instructions: str,
        tools: Sequence[Tool] | None = None,
        max_steps: int = 5,
    ):
        self.model = model
        self.instructions = instructions
        self.tools = {t.name: t for t in (tools or [])}
        self.max_steps = max_steps
        self.session = Session()

    def run(self, user_input: str) -> RunResult:
        if not self.session.messages:
            self.session.add(SystemMessage(content=self.instructions))
        
        self.session.add(UserMessage(content=user_input))

        steps = 0
        tool_calls_record = []

        while steps < self.max_steps:
            response = self.model.generate(
                messages=self.session.messages,
                tools=list(self.tools.values())
            )
            self.session.add(response)

            if not isinstance(response, AssistantMessage):
                break

            if not response.tool_calls:
                return RunResult(
                    text=response.content or "",
                    messages=self.session.messages,
                    status="completed",
                    tool_calls=tool_calls_record
                )

            for tcall in response.tool_calls:
                tool_calls_record.append({
                    "id": tcall.id, 
                    "name": tcall.name, 
                    "arguments": tcall.arguments
                })
                
                tool_instance = self.tools.get(tcall.name)
                if not tool_instance:
                    result_msg = ToolResultMessage(
                        tool_call_id=tcall.id,
                        name=tcall.name,
                        content=f"Error: Tool '{tcall.name}' not found"
                    )
                else:
                    try:
                        res = tool_instance(**tcall.arguments)
                        result_msg = ToolResultMessage(
                            tool_call_id=tcall.id,
                            name=tcall.name,
                            content=str(res)
                        )
                    except Exception as e:
                        result_msg = ToolResultMessage(
                            tool_call_id=tcall.id,
                            name=tcall.name,
                            content=f"Error: {e}"
                        )
                
                self.session.add(result_msg)

            steps += 1

        return RunResult(
            text="Max steps reached",
            messages=self.session.messages,
            status="max_steps_reached",
            tool_calls=tool_calls_record
        )
