from app.tools.base import Tool

class AnswerTool(Tool):
    name = "answers"
    description = "Provides answers for questions"

    def __init__(self, llm):
        self.llm = llm

    def run(self, input_data: dict) -> dict:
        questions = input_data["questions"]
        return {
            "answers": self.llm.generate_answers(questions)
        }