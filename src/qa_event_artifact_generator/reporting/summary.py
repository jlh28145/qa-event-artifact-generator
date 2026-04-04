from pathlib import Path


def summary_message(
    video_path: Path,
    events_path: Path,
    output_path: Path,
    event_count: int,
    video_duration: float,
) -> str:
    return (
        "QA Event Artifact Generator\n"
        f"  video: {video_path}\n"
        f"  events: {events_path}\n"
        f"  output: {output_path}\n"
        f"  event count: {event_count}\n"
        f"  video duration: {video_duration:.2f}s"
    )
