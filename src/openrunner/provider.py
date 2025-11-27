from typing import Set

from pydantic import BaseModel


class OpenRunnerProvider(BaseModel):
    name: str
    models: Set[str] = set([])
    auth: str | None = None
    url: str | None = None
    port: str | None = None

    def add_model(self, model: str):
        self.models.add(model)

    def remove_model(self, model: str):
        self.models = set([m for m in self.models if m != model])


