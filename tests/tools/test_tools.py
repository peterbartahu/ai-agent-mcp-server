from app.agent.llm_fake import FakeLLM
from app.tools.summary_tool import SummaryTool
from app.tools.question_tool import QuestionTool
from app.tools.answer_tool import AnswerTool


def test_summary_tool():

    llm = FakeLLM()
    tool = SummaryTool(llm)

    result = tool.run({"topic": "Machine Learning"})

    assert "summary" in result
    assert "key_points" in result
    assert isinstance(result["key_points"], list)


def test_question_tool():

    llm = FakeLLM()
    tool = QuestionTool(llm)

    result = tool.run({"topic": "Python"})

    assert "questions" in result
    assert len(result["questions"]) > 0


def test_answer_tool():

    llm = FakeLLM()
    tool = AnswerTool(llm)

    result = tool.run({
        "questions": ["What is Python?"]
    })

    assert "answers" in result
    assert len(result["answers"]) == 1