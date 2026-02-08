from typing import Dict
from app.tools.base import Tool
from app.agent.planner import Planner


class Agent:
    def __init__(self, tools: list[Tool], planner: Planner):
        self.tools: Dict[str, Tool] = {
            tool.name: tool for tool in tools
        }
        self.planner = planner

    def handle_task(self, task: str) -> list[str]:
        """
        Handles a task by:
        1. Planning steps
        2. Executing each step via tools
        """
        steps = self.planner.plan(task)
        results: list[str] = []

        for step in steps:
            executed = False
            for tool_name, tool in self.tools.items():
                if tool_name in step:
                    results.append(tool.run(step))
                    executed = True
                    break

            if not executed:
                results.append(f"No suitable tool found for step: {step}")

        return results
