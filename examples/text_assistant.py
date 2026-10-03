import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from papaya import Agent, tool
from papaya.models.fake import FakeModel
from papaya.messages import AssistantMessage, ToolCall


@tool
def count_words(text: str) -> int:
    """Count the words in a piece of text."""
    return len(text.split())


mock_responses = [
    AssistantMessage(
        tool_calls=[ToolCall(id="call_1", name="count_words", arguments={"text": "hello from papaya"})]
    ),
    AssistantMessage(content="There are 3 words in 'hello from papaya'.")
]


def main():
    agent = Agent(
        model=FakeModel(responses=mock_responses),
        instructions="Help users analyze text.",
        tools=[count_words],
        max_steps=5,
    )

    result = agent.run("How many words are in 'hello from papaya'?")
    
    print(f"Status: {result.status}")
    print(f"Answer: {result.text}")
    print(f"Tools Used: {[tc['name'] for tc in result.tool_calls]}")


if __name__ == "__main__":
    main()
