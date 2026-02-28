from app.tools.question_tool import QuestionTool

def test_question_tool_generates_questions(fake_llm):
    tool = QuestionTool(fake_llm)

    result = tool.run({"topic": "AWS S3"})

    assert "questions" in result
    assert len(result["questions"]) > 0