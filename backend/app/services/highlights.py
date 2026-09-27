from typing import Any


def rank_candidates(candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """
    Deterministic baseline scorer. Replace/augment this with an LLM provider.

    The provider interface intentionally works on transcript candidates rather
    than the entire video, keeping inference cost and context size bounded.
    """
    for candidate in candidates:
        candidate["score"] = round(
            0.30 * candidate.get("hook", 0)
            + 0.25 * candidate.get("humor", 0)
            + 0.20 * candidate.get("importance", 0)
            + 0.15 * candidate.get("standalone", 0)
            + 0.10 * candidate.get("emotion", 0),
            2,
        )
    return sorted(candidates, key=lambda item: item["score"], reverse=True)


def analyze_transcript(segments: list[dict[str, Any]]) -> list[dict[str, Any]]:
    # Initial heuristic: use short groups of transcript segments as candidates.
    candidates = []
    for index in range(0, len(segments), 3):
        group = segments[index:index + 3]
        if not group:
            continue
        candidates.append({
            "start": group[0]["start"],
            "end": group[-1]["end"],
            "text": " ".join(x["text"] for x in group),
            "title": "AI-generated short candidate",
            "hook": 5.0,
            "humor": 5.0,
            "importance": 5.0,
            "standalone": 5.0,
            "emotion": 5.0,
        })
    return rank_candidates(candidates)
