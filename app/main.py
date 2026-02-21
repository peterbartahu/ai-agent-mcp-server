from app.agent.agent import Agent
from app.agent.planner import Planner
from app.agent.llm import FakeLLM
from app.tools.summary_tool import SummaryTool
from app.tools.question_tool import QuestionTool
from app.tools.answer_tool import AnswerTool

def main():
    topic = input("Enter study topic: ")

    llm = FakeLLM()

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
        print("-", kp)

    print("\n=== QUESTIONS & ANSWERS ===")
    for q, a in zip(result["questions"], result["answers"]):
        print(f"Q: {q}")
        print(f"A: {a}\n")

if __name__ == "__main__":
    main()