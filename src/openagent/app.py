from typing import Any, Dict, List, Optional, Set
import datetime
import uuid


class OpenAgentContext():
    def __init__(self):
        self.role: str
        self.text: str
        self.fn: List[Dict[str, Any]]
        self.extra: Dict[str, Any]
        self.create_at: datetime.datetime


class OpenAgentProvider():
    def __init__(self, name: str) -> None:
        self.name = name
        self.models: Set[str] = set([])
        self.auth: Optional[str]
        self.url: Optional[str]
        self.port: Optional[int]

    def add_model(self, model: str):
        self.models.add(model)

    def remove_model(self, model: str):
        self.models = set([m for m in self.models if m != model])


class OpenAgentSession():
    def __init__(self, id: str, name: str, provider: OpenAgentProvider) -> None:
        self.id = id
        self.name = name
        self.provider = provider
        self.context: List[OpenAgentContext] = []


class OpenAgent():
    def __init__(self) -> None:
        self.sessions: Dict[str, OpenAgentSession] = {}
        self.providers: Dict[str, OpenAgentProvider] = {}

    def create_session(self, name: Optional[str], provider: OpenAgentProvider):
        if not name:
            name = "something strange"
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = OpenAgentSession(
            id=session_id, name=name, provider=provider)

    def add_provider(self, provider: OpenAgentProvider):
        self.providers[provider.name] = provider

    def remove_provider(self, name: str) -> None:
        self.providers.pop(name)

    def add_provider_model(self, name: str, model: str) -> None:
        provider = self.providers.get(name, None)
        if not provider:
            raise Exception(f"Provider {id} not found")
        provider.add_model(model)

    def remove_provider_model(self, name: str, model: str) -> None:
        provider = self.providers.get(name, None)
        if not provider:
            raise Exception(f"Provider {id} not found")
        provider.remove_model(model)
