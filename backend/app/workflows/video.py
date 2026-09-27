from dataclasses import dataclass
from temporalio import workflow


@dataclass
class VideoJobInput:
    video_id: str
    source_url: str


@workflow.defn
class VideoProcessingWorkflow:
    @workflow.run
    async def run(self, data: VideoJobInput) -> dict:
        return {
            "video_id": data.video_id,
            "source_url": data.source_url,
            "status": "accepted",
        }
