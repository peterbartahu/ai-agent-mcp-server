from fastapi import FastAPI
from app.api.study import router as study_router

app = FastAPI(title="AI Study Agent")

app.include_router(study_router)