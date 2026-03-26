from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List

from app.agent.agent import Agent
from app.agent.planner import Planner
from app.main import create_llm
from app.tools.summary_tool import SummaryTool
from app.tools.question_tool import QuestionTool
from app.tools.answer_tool import AnswerTool
from app.storage.mongodb_store import (
    save_interaction,
    get_interaction,
    list_interactions as _list_interactions,
    search_interactions as _search_interactions,
)

router = APIRouter()


class StudyRequest(BaseModel):
    topic: str


class StudyResponse(BaseModel):
    summary: str
    key_points: List[str]
    questions: List[str]
    answers: List[str]


class InteractionSummary(BaseModel):
    id: str
    topic: str
    created_at: str


@router.post("/study", response_model=StudyResponse)
def study_topic(request: StudyRequest):
    """Generate study material and save to MongoDB."""
    if not request.topic.strip():
        raise HTTPException(status_code=400, detail="Topic cannot be empty")

    llm = create_llm()

    agent = Agent(
        planner=Planner(),
        tools={
            "summary": SummaryTool(llm),
            "questions": QuestionTool(llm),
            "answers": AnswerTool(llm),
        }
    )

    result = agent.handle_task(request.topic)

    # Convert to dict for storage
    response_dict = {
        "summary": result.summary,
        "key_points": result.key_points,
        "questions": result.questions,
        "answers": result.answers,
    }
    
    # Save to MongoDB
    save_interaction(request.topic, response_dict)

    return response_dict


@router.get("/interactions/search", response_model=List[InteractionSummary])
async def search_interactions(q: str = Query(..., min_length=1), limit: int = Query(100, ge=1, le=1000)):
    """Search study materials by topic."""
    items = _search_interactions(q, limit=limit)
    return items


@router.get("/interactions", response_model=List[InteractionSummary])
async def get_interactions(limit: int = Query(100, ge=1, le=1000)):
    """List all stored study interactions."""
    items = _list_interactions(limit=limit)
    return items


@router.get("/interactions/{topic}", response_model=StudyResponse)
async def get_study_interaction(topic: str):
    """Retrieve a stored study material by topic."""
    item = get_interaction(topic)
    if item is None:
        raise HTTPException(status_code=404, detail="Study material not found")
    return item["response"]