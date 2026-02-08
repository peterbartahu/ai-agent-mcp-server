from app.agent.agent import Agent
from app.agent.planner import Planner
from app.tools.base import Tool


class DummyTool(Tool):
    name = "dummy"
    description = "Dummy tool"

    def run(self, input_data: str) -> str:
        return f"executed: {input_data}"


def test_agent_executes_multiple_steps():
    agent = Agent(
        tools=[DummyTool()],
        planner=Planner()
    )

    task = "use dummy then use dummy again"
    results = agent.handle_task(task)

    assert results == [
        "executed: use dummy",
        "executed: use dummy again"
    ]
