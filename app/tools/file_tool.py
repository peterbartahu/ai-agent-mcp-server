from .base import Tool


class FileTool(Tool):
    name = "file_tool"
    description = "Handles file-related tasks"

    def run(self, input_data: str) -> str:
        return f"FileTool received: {input_data}"
