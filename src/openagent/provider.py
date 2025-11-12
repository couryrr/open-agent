from typing import Optional, Set
from pydantic import BaseModel


class OpenAgentProvider(BaseModel):
    name: str
    models: Set[str] = set([])
    auth: Optional[str] = None
    url: Optional[str] = None
    port: Optional[str] = None

    def add_model(self, model: str):
        self.models.add(model)

    def remove_model(self, model: str):
        self.models = set([m for m in self.models if m != model])


