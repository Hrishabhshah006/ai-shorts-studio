import asyncio
import os

from temporalio.client import Client
from temporalio.worker import Worker

from app.workflows.video import (
    VideoProcessingWorkflow,
    analyze_source,
    finalize,
    mark_processing,
)


async def main():
    client = await Client.connect(os.getenv("TEMPORAL_ADDRESS", "localhost:7233"))
    worker = Worker(
        client,
        task_queue="video-processing",
        workflows=[VideoProcessingWorkflow],
        activities=[mark_processing, analyze_source, finalize],
    )
    print("video worker listening on video-processing")
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
