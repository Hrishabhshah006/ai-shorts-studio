from dataclasses import dataclass
from datetime import timedelta

from temporalio import activity, workflow


@dataclass
class VideoJobInput:
    video_id: str
    source_url: str


@activity.defn
async def mark_processing(video_id: str) -> str:
    return f"{video_id}:processing"


@activity.defn
async def analyze_source(source_url: str) -> dict:
    return {
        "source_url": source_url,
        "status": "accepted",
        "candidates": [],
        "next_stage": "source-acquisition",
    }


@activity.defn
async def finalize(video_id: str, result: dict) -> dict:
    return {"video_id": video_id, "status": "completed", **result}


@workflow.defn
class VideoProcessingWorkflow:
    @workflow.run
    async def run(self, data: VideoJobInput) -> dict:
        await workflow.execute_activity(
            mark_processing,
            data.video_id,
            start_to_close_timeout=timedelta(seconds=30),
        )
        result = await workflow.execute_activity(
            analyze_source,
            data.source_url,
            start_to_close_timeout=timedelta(minutes=5),
        )
        return await workflow.execute_activity(
            finalize,
            args=[data.video_id, result],
            start_to_close_timeout=timedelta(seconds=30),
        )
