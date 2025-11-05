from typing import List


class OpenAgentMessage():
    pass


class OpenAgentProvider():
    pass


class OpenAgent():
    def __init__(self) -> None:
        self._state: List[OpenAgentMessage] = []
        self._providers: List[OpenAgentProvider] = []

    def get_providers(self):
        return self._providers

    def add_provider(self, provider: OpenAgentProvider):
        self._providers.append(provider)

    def get_messages(self):
        return self._state

    def add_message(self, message: OpenAgentMessage):
        self._state.append(message)
