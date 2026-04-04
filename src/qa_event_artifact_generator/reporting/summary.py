from pathlib import Path
from typing import List

from qa_event_artifact_generator.models import Event


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


def detailed_summary(
    events: List[Event],
    clip_records: List[dict],
    event_warnings: List[str],
    validation_warnings: List[str],
    segment_warnings: List[str],
    output_path: Path,
) -> str:
    total_events = len(events)
    duration_events = sum(1 for e in events if e.start is not None and e.end is not None)
    point_events = total_events - duration_events
    successful_clips = len(clip_records)
    failed_clips = total_events - successful_clips
    total_warnings = len(event_warnings) + len(validation_warnings) + len(segment_warnings)

    summary = [
        "\nProcessing Summary:",
        f"  Total events: {total_events}",
        f"  Duration events: {duration_events}",
        f"  Point events: {point_events}",
        f"  Successful clips: {successful_clips}",
        f"  Failed/skipped clips: {failed_clips}",
        f"  Total warnings: {total_warnings}",
        f"  Output directory: {output_path}",
    ]

    if event_warnings:
        summary.append(f"  Event warnings: {len(event_warnings)}")
    if validation_warnings:
        summary.append(f"  Validation warnings: {len(validation_warnings)}")
    if segment_warnings:
        summary.append(f"  Segmentation warnings: {len(segment_warnings)}")

    return "\n".join(summary)


def generate_html_report(
    video_path: Path,
    events_path: Path,
    output_path: Path,
    events: List[Event],
    clip_records: List[dict],
    event_warnings: List[str],
    validation_warnings: List[str],
    segment_warnings: List[str],
    html_path: Path,
) -> None:
    html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>QA Event Artifact Generator Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        h1 {{ color: #333; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
        .warning {{ color: orange; }}
        .error {{ color: red; }}
    </style>
</head>
<body>
    <h1>QA Event Artifact Generator Report</h1>
    <p><strong>Video:</strong> {video_path}</p>
    <p><strong>Events:</strong> {events_path}</p>
    <p><strong>Output:</strong> {output_path}</p>
    <p><strong>Total Events:</strong> {len(events)}</p>
    <p><strong>Successful Clips:</strong> {len(clip_records)}</p>

    <h2>Clips Generated</h2>
    <table>
        <tr><th>Label</th><th>Start</th><th>End</th><th>Duration</th><th>Clip Path</th></tr>
        {"".join(f"<tr><td>{r['label']}</td><td>{r['start']:.2f}</td><td>{r['end']:.2f}</td><td>{r['duration']:.2f}</td><td>{r['clip_path']}</td></tr>" for r in clip_records)}
    </table>

    <h2>Warnings</h2>
    <ul>
        {"".join(f"<li class='warning'>{w}</li>" for w in event_warnings + validation_warnings + segment_warnings)}
    </ul>
</body>
</html>
"""
    html_path.write_text(html_content, encoding='utf-8')
