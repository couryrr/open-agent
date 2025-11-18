import datetime
from typing import Any, Dict, List

from pydantic import BaseModel


class OpenAgentContext(BaseModel):
    role: str
    text: str
    fn: List[Dict[str, Any]]
    extra: Dict[str, Any]
    create_at: datetime.datetime


