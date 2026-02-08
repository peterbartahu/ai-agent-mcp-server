class Planner:
    """
    Very simple planner.
    Splits a task into sequential steps.
    """

    def plan(self, task: str) -> list[str]:
        """
        For now:
        - split by 'then'
        - return ordered steps
        """
        steps = [step.strip() for step in task.split("then")]
        return steps