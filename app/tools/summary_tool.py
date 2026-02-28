from app.tools.base import Tool

class SummaryTool(Tool):
    name = "summary"
    description = "Generates summary and key points"

    def __init__(self, llm):
        self.llm = llm

    def run(self, input_data: dict) -> dict:
        topic = input_data["topic"]
        return {
            "summary": self.llm.generate_summary(topic),
            "key_points": self.llm.generate_key_points(topic)
        }