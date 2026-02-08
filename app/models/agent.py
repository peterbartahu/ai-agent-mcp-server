from pydantic import BaseModel
from typing import Any, List


class AgentExecuteRequest(BaseModel):
    task: str


class AgentExecuteResponse(BaseModel):
    result: Any
    steps: List[str]