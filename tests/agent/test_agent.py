from app.agent.agent import Agent
from app.agent.planner import Planner
from app.agent.llm import FakeLLM
from app.tools.summary_tool import SummaryTool
from app.tools.question_tool import QuestionTool
from app.tools.answer_tool import AnswerTool

def test_agent_runs_full_flow():
    llm = FakeLLM()

    tools = {
        "summary": SummaryTool(llm),
        "questions": QuestionTool(llm),
        "answers": AnswerTool(llm),
    }

    agent = Agent(
        planner=Planner(),
        tools=tools
    )

    result = agent.handle_task("AWS S3")

    assert "summary" in result
    assert "key_points" in result
    assert "questions" in result
    assert "answers" in result