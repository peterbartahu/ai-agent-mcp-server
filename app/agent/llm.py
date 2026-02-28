class FakeLLM:
    def generate_summary(self, topic: str) -> str:
        return f"{topic} is a core concept. This is a short summary for study purposes."

    def generate_key_points(self, topic: str) -> list[str]:
        return [
            f"{topic} key point 1",
            f"{topic} key point 2",
            f"{topic} key point 3",
        ]

    def generate_questions(self, topic: str) -> list[str]:
        return [
            f"What is {topic}?",
            f"When should you use {topic}?",
            f"What are common pitfalls of {topic}?"
        ]

    def generate_answers(self, questions: list[str]) -> list[str]:
        return [f"Answer to: {q}" for q in questions]