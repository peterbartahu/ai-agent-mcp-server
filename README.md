# AI Agent MCP Server

This project is a Python-based MCP-style AI agent backend,
focused on clean architecture, tool-based execution,
and testable agent logic.

At the moment, the agent is deterministic and does not use a real LLM.
This is intentional: the focus is on architecture, not prompt engineering.
## Goals
- Agent-based reasoning
- MCP-inspired tool execution
- Clean / Hexagonal Architecture
- Fully testable core logic
- Future FastAPI and LLM integration

source venv/bin/activate

## Running the application
```bash
python -m app.main
```

## Running tests
```bash
pytest
```