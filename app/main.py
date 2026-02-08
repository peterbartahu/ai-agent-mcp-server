from fastapi import FastAPI

from app.api.agent import router as agent_router

app = FastAPI(title="AI Agent MCP Server")

app.include_router(agent_router)