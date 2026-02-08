from typing import List, Optional
from app.agent.planner import Planner
from app.tools.base import Tool

class Agent:
    def __init__(self, planner: Optional[Planner] = None, tools: Optional[List[Tool]] = None):
        self.planner = planner if planner else Planner()
        self.tools = tools if tools else []

    def handle_task(self, task: str):
        steps = self.planner.plan(task)
        results = []

        for step in steps:
            tool = self.tools[0] if self.tools else None
            if tool:
                results.append(tool.run(step))
            else:
                results.append(f"Executed: {step}")
        return results
