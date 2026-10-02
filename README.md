# Papaya 🥭

A small Python framework for building AI agents.

Papaya will handle the loop between a language model and the tools it can use. The idea is to let you define an agent in a few lines of Python, while keeping the code underneath small enough to read and understand.

The project is in early development. This README outlines the structure I plan to build; the API will likely change as the first examples come together.

## The idea

An agent needs instructions, a model, and a set of tools. Papaya will bring those pieces together and manage the execution: sending messages to the model, handling tool calls, and returning a result.

The first version will focus on a single agent completing a task. I'll start with one model provider and a few working examples before adding more integrations.

## What using it should look like

This is the API I'm working toward, not a working example yet:

```python
from papaya import Agent, tool


@tool
def count_words(text: str) -> int:
    """Count the words in a piece of text."""
    return len(text.split())


# `model` will be a configured provider adapter.
agent = Agent(
    model=model,
    instructions="Help users analyze text.",
    tools=[count_words],
    max_steps=5,
)

result = agent.run("How many words are in 'hello from papaya'?")
print(result.text)
```

The `@tool` decorator will use the function's type hints and docstring to describe it to the model. Papaya will validate the arguments before calling the function and pass its output back into the conversation.

## Project structure

The initial layout will look like this:

```text
papaya/
├── src/
│   └── papaya/
│       ├── __init__.py
│       ├── agent.py
│       ├── tools.py
│       ├── messages.py
│       ├── session.py
│       ├── result.py
│       └── models/
│           ├── __init__.py
│           └── base.py
├── examples/
│   └── text_assistant.py
├── tests/
│   ├── test_agent.py
│   └── test_tools.py
├── pyproject.toml
└── README.md
```

`agent.py` will contain the execution loop. It will request a response from the model, dispatch tool calls, and stop when the task is complete or a limit is reached.

`tools.py` will handle function registration, argument schemas, and validation. Tools will remain ordinary Python functions so they can also be called and tested on their own.

`messages.py` will define the message types shared by the agent and model adapters. Provider-specific formats will stay inside `models/`.

`session.py` will hold conversation history in memory. Saving sessions between runs can come later.

`result.py` will define the output of a run: the response, its status, and a record of tool calls and errors.

## Execution flow

For each task, Papaya will:

1. Build the conversation from the agent's instructions and the user's input.
2. Send it to the model along with the available tool definitions.
3. Return the answer if the model finishes, or validate and execute any requested tools.
4. Add the tool results to the conversation and ask the model for the next step.
5. Stop on completion, failure, or the configured execution limit.

Reaching a limit should return an explicit status and the work completed so far. Tool errors should also remain visible in the run result.

## Building the first version

I'll build the core loop against a fake model first. That will make it possible to test tool calls, failures, and stopping conditions without relying on an external API.

The next step will be a real model adapter and a small example that runs from start to finish.

- [ ] Define messages and the model interface
- [ ] Implement tool registration and argument validation
- [ ] Build the agent loop
- [ ] Add step limits and error handling
- [ ] Record tool calls and run results
- [ ] Connect the first model provider
- [ ] Write a runnable example
- [ ] Add installation and usage documentation

After that, I'll look at streaming, async execution, and a second provider to check whether the model interface holds up.

## Scope

For now, Papaya will focus on text-based agents with explicitly registered tools and in-memory conversation history.
