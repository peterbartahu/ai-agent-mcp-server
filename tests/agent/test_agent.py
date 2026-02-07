from app.agent.agent import Agent
from app.tools.base import Tool


class DummyTool(Tool):
    name = "dummy"
    description = "Dummy tool for testing"

    def run(self, input_data: str) -> str:
        return "dummy-result"


def test_agent_executes_matching_tool():
    agent = Agent(tools=[DummyTool()])

    result = agent.handle_task("please use dummy tool")

    assert result == "dummy-result"

def test_agent_returns_message_when_no_tool_matches():
    agent = Agent(tools=[DummyTool()])

    result = agent.handle_task("do something else")

    assert result == "No suitable tool found for task"
