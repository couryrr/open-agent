import os
from typing import List, Optional
import uuid
from .state import OpenAgentState
from .session import OpenAgentSession
from .provider import OpenAgentProvider
from pydantic import BaseModel


class OpenAgent(BaseModel):
    state: OpenAgentState = OpenAgentState()

    def save(self):
        if self.state.data_dir:
            with open(os.path.join(self.state.data_dir, "data.json"), "w") as file:
                file.write(self.model_dump_json())

    def create_session(self, provider: OpenAgentProvider, name: Optional[str] = None) -> None:
        if not name:
            name = "something strange"
        session_id = str(uuid.uuid4())
        self.state.sessions[name] = OpenAgentSession(
            id=session_id, name=name, provider=provider)

    def list_sessions(self):
        return list(self.state.sessions.values())

    def add_provider(self, provider: OpenAgentProvider) -> None:
        if self.state.providers.get(provider.name):
            raise Exception(f"Provider {provider.name} already exists")
        self.state.providers[provider.name] = provider

    def list_providers(self) -> List[OpenAgentProvider]:
        return list(self.state.providers.values())

    def remove_provider(self, name: str) -> None:
        self.state.providers.pop(name)

    def add_provider_model(self, name: str, model: str) -> None:
        provider = self.state.providers.get(name, None)
        if not provider:
            raise Exception(f"Provider {name} not found")
        provider.add_model(model)

    def remove_provider_model(self, name: str, model: str) -> None:
        provider = self.state.providers.get(name, None)
        if not provider:
            raise Exception(f"Provider {name} not found")
        provider.remove_model(model)
