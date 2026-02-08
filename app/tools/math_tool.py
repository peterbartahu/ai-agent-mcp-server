from .base import Tool


class MathTool(Tool):
    name = "math_tool"
    description = "Handles basic math operations"

    def run(self, input_data: str) -> str:
        return f"MathTool received: {input_data}"
