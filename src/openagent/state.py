from typing import Dict, Optional
from pydantic import BaseModel
from .session import OpenAgentSession
from .provider import OpenAgentProvider


class OpenAgentState(BaseModel):
    sessions: Dict[str, OpenAgentSession] = {}
    providers: Dict[str, OpenAgentProvider] = {}
    data_dir: Optional[str] = None

