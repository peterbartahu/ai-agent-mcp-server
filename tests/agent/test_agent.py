from app.agent.agent import Agent
from app.agent.planner import Planner
from app.agent.llm_fake import FakeLLM

from app.tools.summary_tool import SummaryTool
from app.tools.question_tool import QuestionTool
from app.tools.answer_tool import AnswerTool


def test_agent_pipeline():

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

    result = agent.handle_task("Python")

    assert result.topic == "Python"
    assert isinstance(result.summary, str)
    assert len(result.key_points) > 0
    assert len(result.questions) > 0
    assert len(result.answers) > 0