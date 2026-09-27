from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl

app = FastAPI(title="AI Shorts Studio API", version="0.1.0")


class CreateVideoRequest(BaseModel):
    source_url: HttpUrl


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/api/v1/videos", status_code=202)
async def create_video(request: CreateVideoRequest):
    # Workflow integration is added in the next slice.
    return {
        "status": "queued",
        "source_url": str(request.source_url),
        "message": "Video job accepted"
    }
