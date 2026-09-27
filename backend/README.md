# Backend

Install dependencies:

    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt

Run API:

    uvicorn app.main:app --reload --port 8000

Run Temporal worker:

    python -m app.workers.main

FFmpeg must be installed for rendering. A GPU is recommended for faster transcription.
