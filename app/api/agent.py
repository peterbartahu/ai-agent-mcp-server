from fastapi import APIRouter, Depends

from app.agent.agent import Agent
from app.models.agent import AgentExecuteRequest, AgentExecuteResponse

router = APIRouter(prefix="/agent", tags=["agent"])


def get_agent() -> Agent:
    # később: config, LLM, planner injection
    return Agent()


@router.post("/execute", response_model=AgentExecuteResponse)
def execute_agent(
    request: AgentExecuteRequest,
    agent: Agent = Depends(get_agent),
):
    result = agent.execute(request.task)

    return AgentExecuteResponse(
        result=result["result"],
        steps=result["steps"],
    )
