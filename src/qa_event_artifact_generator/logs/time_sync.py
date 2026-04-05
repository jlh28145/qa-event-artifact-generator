from __future__ import annotations

from datetime import datetime
from typing import List

from qa_event_artifact_generator.logs.event_extractor import ExtractedLogEvent
from qa_event_artifact_generator.models import PointEvent, parse_time


def parse_recording_start(value: str) -> datetime | float:
    value = value.strip()
    for fmt in (
        "%Y-%m-%dT%H:%M:%S.%f",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%d %H:%M:%S",
        "%H:%M:%S",
    ):
        try:
            if fmt == "%H:%M:%S":
                return parse_time(value)
            return datetime.strptime(value, fmt)
        except ValueError:
            continue
    raise ValueError(f"Invalid recording start format: {value}")


def correlate_log_events(
    extracted_events: List[ExtractedLogEvent],
    recording_start: str,
    video_duration: float | None = None,
) -> tuple[List[PointEvent], List[str]]:
    start_value = parse_recording_start(recording_start)
    synced: List[PointEvent] = []
    warnings: List[str] = []
    for index, event in enumerate(extracted_events, start=1):
        if isinstance(start_value, float):
            if not isinstance(event.timestamp, float):
                warnings.append(
                    f"Event '{event.label}' has a non-relative timestamp for relative recording start."
                )
                continue
            offset = event.timestamp - start_value
        else:
            if not isinstance(event.timestamp, datetime):
                warnings.append(
                    f"Event '{event.label}' has a non-datetime timestamp for absolute recording start."
                )
                continue
            offset = (event.timestamp - start_value).total_seconds()

        if offset < 0:
            warnings.append(
                f"Event '{event.label}' occurs before recording start ({offset:.2f}s)."
            )
        if video_duration is not None and offset > video_duration:
            warnings.append(
                f"Event '{event.label}' is beyond video duration ({offset:.2f}s > {video_duration:.2f}s)."
            )

        synced.append(
            PointEvent(
                label=event.label,
                timestamp=offset,
                notes=event.notes,
                tags=event.tags or [],
                pre_buffer=event.pre_buffer,
                post_buffer=event.post_buffer,
                raw=event.raw or {},
            )
        )
    return synced, warnings
