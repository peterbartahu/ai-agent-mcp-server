from app.agent.llm_base import LLM

class FakeLLM(LLM):

    def generate_summary(self, topic: str) -> str:
        return f"{topic} is an important concept used in many systems."

    def generate_key_points(self, topic: str) -> list[str]:
        return [
            f"{topic} key concept 1",
            f"{topic} key concept 2",
            f"{topic} key concept 3",
        ]

    def generate_questions(self, topic: str) -> list[str]:
        return [
            f"What is {topic}?",
            f"When should you use {topic}?",
            f"What are common pitfalls of {topic}?"
        ]

    def generate_answers(self, questions: list[str]) -> list[str]:
        return [f"This is a sample answer for: {q}" for q in questions]