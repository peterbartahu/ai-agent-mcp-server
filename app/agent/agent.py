from app.agent.planner import Planner


class Agent:
    def __init__(self):
        self.planner = Planner()

    def execute(self, task: str) -> dict:
        steps = self.planner.plan(task)

        results = []
        for step in steps:
            results.append(f"Executed: {step}")

        return {
            "result": results,
            "steps": steps,
        }
