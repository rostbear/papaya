import inspect
from typing import Any, Callable


class Tool:
    def __init__(self, func: Callable[..., Any]):
        self.func = func
        self.name = func.__name__
        self.description = inspect.getdoc(func) or ""
        self.signature = inspect.signature(func)

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        return self.func(*args, **kwargs)

    @property
    def schema(self) -> dict[str, Any]:
        parameters = {}
        required = []

        for name, param in self.signature.parameters.items():
            parameters[name] = {"type": "string"}
            if param.default == inspect.Parameter.empty:
                required.append(name)
        
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": parameters,
                    "required": required
                }
            }
        }


def tool(func: Callable[..., Any]) -> Tool:
    return Tool(func)
