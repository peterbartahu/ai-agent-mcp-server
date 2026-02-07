from typing import Dict
from app.tools.base import Tool


class Agent:
    def __init__(self, tools: list[Tool]):
        self.tools: Dict[str, Tool] = {
            tool.name: tool for tool in tools
        }

    def handle_task(self, task: str) -> str:
        """
        Very simple routing logic:
        - if task contains tool name -> execute it
        """
        for tool_name, tool in self.tools.items():
            if tool_name in task:
                return tool.run(task)

        return "No suitable tool found for task"
