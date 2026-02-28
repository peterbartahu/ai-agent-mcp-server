from app.tools.summary_tool import SummaryTool

def test_summary_tool_returns_summary_and_key_points(fake_llm):
    tool = SummaryTool(fake_llm)

    result = tool.run({"topic": "AWS S3"})

    assert "summary" in result
    assert "key_points" in result
    assert len(result["key_points"]) > 0