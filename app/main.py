from app.agent.agent import Agent
from app.agent.planner import Planner
from app.tools.file_tool import FileTool
from app.tools.math_tool import MathTool


def main():
    agent = Agent(
        tools=[FileTool(), MathTool()],
        planner=Planner()
    )

    task = "use file_tool to read data then use math_tool to process numbers"
    results = agent.handle_task(task)

    for result in results:
        print(result)


if __name__ == "__main__":
    main()
