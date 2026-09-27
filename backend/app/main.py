import os
import uuid

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
from temporalio.client import Client

from .workflows.video import VideoJobInput, VideoProcessingWorkflow

app = FastAPI(title="AI Shorts Studio API", version="0.1.0")


class CreateVideoRequest(BaseModel):
    source_url: HttpUrl


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/api/v1/videos", status_code=202)
async def create_video(request: CreateVideoRequest):
    video_id = str(uuid.uuid4())

    try:
        client = await Client.connect(os.getenv("TEMPORAL_ADDRESS", "localhost:7233"))
        handle = await client.start_workflow(
            VideoProcessingWorkflow.run,
            VideoJobInput(video_id=video_id, source_url=str(request.source_url)),
            id=f"video-{video_id}",
            task_queue="video-processing",
        )
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"Temporal is unavailable: {exc}") from exc

    return {
        "video_id": video_id,
        "workflow_id": handle.id,
        "status": "queued",
    }
