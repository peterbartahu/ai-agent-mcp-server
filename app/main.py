from app.agent.agent import Agent
from app.tools.file_tool import FileTool
from app.tools.math_tool import MathTool


def main():
    agent = Agent(
        tools=[
            FileTool(),
            MathTool()
        ]
    )

    result = agent.handle_task("use math_tool to calculate something")
    print(result)


if __name__ == "__main__":
    main()
