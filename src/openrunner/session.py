from pydantic import BaseModel

from .provider import OpenRunnerProvider


class OpenRunnerSession(BaseModel):
    id: str
    name: str
    provider: OpenRunnerProvider
    # context: List[OpenRunnerContext]


