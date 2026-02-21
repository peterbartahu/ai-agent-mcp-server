import os

from app.agent.agent import Agent
from app.agent.planner import Planner
from app.agent.llm_fake import FakeLLM
from app.agent.llm_openai import OpenAILLM

from app.tools.summary_tool import SummaryTool
from app.tools.question_tool import QuestionTool
from app.tools.answer_tool import AnswerTool

from dotenv import load_dotenv

#.env variables -- for openai usage
load_dotenv()

def create_llm():
    """
    Factory method for selecting the LLM implementation.
    Defaults to FakeLLM for local development and tests.
    """
    use_openai = os.getenv("USE_OPENAI", "false").lower() == "true"

    if use_openai:
        return OpenAILLM()

    return FakeLLM()


def main():
    topic = input("Enter study topic: ").strip()

    if not topic:
        print("Topic cannot be empty.")
        return

    llm = create_llm()

    tools = {
        "summary": SummaryTool(llm),
        "questions": QuestionTool(llm),
        "answers": AnswerTool(llm),
    }

    agent = Agent(
        planner=Planner(),
        tools=tools
    )

    result = agent.handle_task(topic)

    print("\n=== SUMMARY ===")
    print(result["summary"])

    print("\n=== KEY POINTS ===")
    for kp in result["key_points"]:
        print(f"- {kp}")

    print("\n=== QUESTIONS & ANSWERS ===")
    for q, a in zip(result["questions"], result["answers"]):
        print(f"\nQ: {q}")
        print(f"A: {a}")


if __name__ == "__main__":
    main()