from pathlib import Path
import subprocess


def render_vertical_clip(
    source: str,
    output: str,
    start: float,
    end: float,
    subtitles: str | None = None,
) -> str:
    Path(output).parent.mkdir(parents=True, exist_ok=True)

    vf = "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920"
    if subtitles:
        vf += f",subtitles={subtitles}"

    command = [
        "ffmpeg", "-y",
        "-ss", str(start),
        "-to", str(end),
        "-i", source,
        "-vf", vf,
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "20",
        "-c:a", "aac",
        "-b:a", "192k",
        "-movflags", "+faststart",
        output,
    ]
    subprocess.run(command, check=True)
    return output
