from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from app.api.study import router as study_router

app = FastAPI(title="AI Study Agent")

app.include_router(study_router)

# Serve static files (HTML, CSS, JS)
static_dir = Path(__file__).parent.parent / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=static_dir), name="static")
    
    # Serve index.html at root
    from fastapi.responses import FileResponse
    
    @app.get("/")
    async def root():
        return FileResponse(static_dir / "index.html")