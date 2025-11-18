from typing import Dict, Optional

from pydantic import BaseModel

from .provider import OpenAgentProvider
from .session import OpenAgentSession


class OpenAgentState(BaseModel):
    sessions: Dict[str, OpenAgentSession] = {}
    providers: Dict[str, OpenAgentProvider] = {}
    data_dir: Optional[str] = None

