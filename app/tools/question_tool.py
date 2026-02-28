from app.tools.base import Tool

class QuestionTool(Tool):
    name = "questions"
    description = "Generates study questions"

    def __init__(self, llm):
        self.llm = llm

    def run(self, input_data: dict) -> dict:
        topic = input_data["topic"]
        return {
            "questions": self.llm.generate_questions(topic)
        }