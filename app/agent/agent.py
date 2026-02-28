class Agent:
    def __init__(self, planner, tools: dict):
        self.planner = planner
        self.tools = tools

    def handle_task(self, topic: str) -> dict:
        context = {"topic": topic}

        for step in self.planner.plan():
            tool = self.tools[step]
            result = tool.run(context)
            context.update(result)

        return context