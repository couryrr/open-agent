import os
import uuid
from typing import List, Optional

from pydantic import BaseModel

from .tooling import OpenRunnerTooling
from .provider import OpenRunnerProvider
from .session import OpenRunnerSession
from .state import OpenRunnerState


class OpenRunner(BaseModel):
    state: OpenRunnerState = OpenRunnerState()

    def save(self):
        if self.state.data_dir:
            with open(os.path.join(self.state.data_dir, "data.json"), "w") as file:
                file.write(self.model_dump_json())

    def create_session(
        self, provider: OpenRunnerProvider, name: Optional[str] = None
    ) -> None:
        if not name:
            name = "something strange"
        session_id = str(uuid.uuid4())
        self.state.sessions[name] = OpenRunnerSession(
            id=session_id, name=name, provider=provider
        )

    def list_sessions(self):
        return list(self.state.sessions.values())

    def add_provider(self, provider: OpenRunnerProvider) -> None:
        if self.state.providers.get(provider.name):
            raise Exception(f"Provider {provider.name} already exists")
        self.state.providers[provider.name] = provider

    def list_providers(self) -> List[OpenRunnerProvider]:
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

    def tool_create_provider_script(self, name: str) -> None:
        tooling = OpenRunnerTooling()
        if self.state.data_dir:
            tooling.create_provider_script(directory=self.state.data_dir, file_name=name)

    def tool_smoke_test_provider(self, name: str) -> None:
        tooling = OpenRunnerTooling()
        if self.state.data_dir:
            tooling.smoke_test(directory=self.state.data_dir, file_name=name)

