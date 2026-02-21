from abc import ABC, abstractmethod

class LLM(ABC):

    @abstractmethod
    def generate_summary(self, topic: str) -> str:
        pass

    @abstractmethod
    def generate_key_points(self, topic: str) -> list[str]:
        pass

    @abstractmethod
    def generate_questions(self, topic: str) -> list[str]:
        pass

    @abstractmethod
    def generate_answers(self, questions: list[str]) -> list[str]:
        pass