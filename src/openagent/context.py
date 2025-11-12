from typing import Any, Dict, List
import datetime
from pydantic import BaseModel


class OpenAgentContext(BaseModel):
    role: str
    text: str
    fn: List[Dict[str, Any]]
    extra: Dict[str, Any]
    create_at: datetime.datetime


