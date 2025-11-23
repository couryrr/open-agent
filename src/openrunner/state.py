from typing import Dict, Optional

from pydantic import BaseModel

from .provider import OpenRunnerProvider
from .session import OpenRunnerSession


class OpenRunnerState(BaseModel):
    sessions: Dict[str, OpenRunnerSession] = {}
    providers: Dict[str, OpenRunnerProvider] = {}
    data_dir: Optional[str] = None

