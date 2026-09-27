from app.services.highlights import analyze_transcript


def test_analyze_transcript_returns_ranked_candidates():
    segments = [
        {"start": 0, "end": 5, "text": "hello"},
        {"start": 5, "end": 10, "text": "this is interesting"},
        {"start": 10, "end": 15, "text": "and this is funny"},
        {"start": 20, "end": 25, "text": "another point"},
    ]

    candidates = analyze_transcript(segments)

    assert candidates
    assert candidates[0]["score"] >= candidates[-1]["score"]
