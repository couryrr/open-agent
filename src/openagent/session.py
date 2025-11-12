from pydantic import BaseModel

from .provider import OpenAgentProvider


class OpenAgentSession(BaseModel):
    id: str
    name: str
    provider: OpenAgentProvider
    # context: List[OpenAgentContext]


