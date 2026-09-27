from pathlib import Path


async def transcribe_video(path: str) -> dict:
    """
    Transcribe media with faster-whisper.

    The model is loaded lazily so the API/worker can start without GPU
    dependencies being initialized.
    """
    from faster_whisper import WhisperModel

    model = WhisperModel("small", device="auto", compute_type="int8")
    segments, info = model.transcribe(
        str(Path(path)),
        word_timestamps=True,
        vad_filter=True,
    )

    result = []
    for segment in segments:
        result.append({
            "start": segment.start,
            "end": segment.end,
            "text": segment.text.strip(),
            "words": [
                {
                    "word": word.word,
                    "start": word.start,
                    "end": word.end,
                }
                for word in (segment.words or [])
            ],
        })

    return {
        "language": info.language,
        "duration": info.duration,
        "segments": result,
    }
