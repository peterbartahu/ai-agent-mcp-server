from app.domain.study_material import StudyMaterial

class Agent:
    def __init__(self, planner, tools: dict, knowledge_base=None):
        self.planner = planner
        self.tools = tools
        self.knowledge_base = knowledge_base

    def handle_task(self, topic: str) -> StudyMaterial:
        context = {"topic": topic}

        if self.knowledge_base:
            context["context_docs"] = self.knowledge_base.retrieve(topic)

        for step in self.planner.plan():
            tool = self.tools[step]
            result = tool.run(context)
            context.update(result)

        return StudyMaterial(
            topic=topic,
            summary=context["summary"],
            key_points=context["key_points"],
            questions=context["questions"],
            answers=context["answers"]
        )