import os
from openai import OpenAI
from app.agent.llm_base import LLM

class OpenAILLM(LLM):

    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY is not set")

        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.client = OpenAI(api_key=api_key)

    def _prompt(self, system: str, user: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            temperature=0.3,
        )
        return response.choices[0].message.content

    def generate_summary(self, topic: str) -> str:
        return self._prompt(
            "You are a study assistant.",
            f"Give a concise summary of the topic: {topic}"
        )

    def generate_key_points(self, topic: str) -> list[str]:
        text = self._prompt(
            "You are a study assistant.",
            f"List the most important key points about {topic}."
        )
        return [line.strip("- ") for line in text.splitlines() if line.strip()]

    def generate_questions(self, topic: str) -> list[str]:
        text = self._prompt(
            "You are an exam preparation assistant.",
            f"Generate 5 exam-style questions about {topic}."
        )
        return [line.strip("- ") for line in text.splitlines() if line.strip()]

    def generate_answers(self, questions: list[str]) -> list[str]:
        answers = []
        for q in questions:
            answers.append(
                self._prompt(
                    "You are an expert instructor.",
                    f"Provide a clear and concise answer to: {q}"
                )
            )
        return answers