from app.tools.answer_tool import AnswerTool

def test_answer_tool_generates_answers(fake_llm):
    tool = AnswerTool(fake_llm)

    questions = ["What is S3?"]
    result = tool.run({"questions": questions})

    assert "answers" in result
    assert len(result["answers"]) == len(questions)