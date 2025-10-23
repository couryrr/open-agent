from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional, Protocol, TypeVar

from ollama import ChatResponse
import ollama


SYSTEM_PROMPT = """
You are an LLM that answers questions directly and accurately.

Guidelines:
- Answer questions you know confidently
- If uncertain, use available tools to find the answer
- Call tools without announcing it - the system handles user communication
- If no tools can help and you're uncertain, respond: "That cannot be answered with confidence.
- Do not make up information
- Do not explain your reasoning process unless asked
- Provide facts, not speculation

Format requirements:
- Use well-structured markdown for all responses
- Never end responses with questions
- Do not ask follow-up questions or offer additional help
- Provide the answer and stop
"""


@dataclass
class SystemMessage():
    role: str
    # type: Literal["system", "user", "assistant", "tool"]
    message: Optional[str]
    fn: Optional[Dict[str, Dict[str, str]]]
    create_at: datetime


@dataclass
class SystemState():
    messages: List[SystemMessage]


T = TypeVar('T')


class LLMProvider[T](Protocol):
    def map_from(self, msg: T) -> SystemMessage:
        ...

    def map_to(self, msg: SystemMessage) -> T:
        ...

    def chat(self, msg: str):
        pass


class OllamaProvider:
    def __init__(self) -> None:
        pass

    def chat(self, system_messages: List[SystemMessage]) -> SystemMessage:
        messages = [{"role": system_message.role, "content": system_message.message}
                    for system_message in system_messages]
        response: ChatResponse = ollama.chat(model='mistral-nemo:latest',
                                             messages=messages)

        return SystemMessage(role=response.message.role,
                             message=response.message.content,
                             fn=None,
                             create_at=datetime.now())


def subtract_two_numbers(a: int, b: int) -> int:
    """
    Subtract two numbers
    """
    return int(a) - int(b)


# Tools can still be manually defined and passed into chat
subtract_two_numbers_tool = {
    'type': 'function',
    'function': {
        'name': 'subtract_two_numbers',
        'description': 'Subtract two numbers',
        'parameters': {
            'type': 'object',
            'required': ['a', 'b'],
            'properties': {
                'a': {'type': 'integer', 'description': 'The first number'},
                'b': {'type': 'integer', 'description': 'The second number'},
            },
        },
    },
}

available_functions = {'subtract_two_numbers': subtract_two_numbers}
