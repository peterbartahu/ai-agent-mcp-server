from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.agent.agent import Agent
from app.agent.planner import Planner
from app.main import create_llm
from app.tools.summary_tool import SummaryTool
from app.tools.question_tool import QuestionTool
from app.tools.answer_tool import AnswerTool

router = APIRouter()


class StudyRequest(BaseModel):
    topic: str


class StudyResponse(BaseModel):
    summary: str
    key_points: list[str]
    questions: list[str]
    answers: list[str]


@router.post("/study", response_model=StudyResponse)
def study_topic(request: StudyRequest):

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

    return result