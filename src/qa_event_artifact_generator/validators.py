from __future__ import annotations

from typing import Iterable, List, Tuple

from qa_event_artifact_generator.models import DurationEvent, Event, PointEvent
from qa_event_artifact_generator.utils import safe_filename


def validate_event_label(label: str) -> Tuple[bool, str]:
    sanitized = safe_filename(label)
    if sanitized != label.strip():
        return False, sanitized
    return True, sanitized


def validate_events(events: Iterable[Event], video_duration: float | None = None) -> Tuple[List[str], List[str]]:
    errors: List[str] = []
    warnings: List[str] = []
    intervals: List[tuple[float, float, str]] = []

    for index, event in enumerate(events, start=1):
        if not event.label.strip():
            errors.append(f"Event {index} has an empty label.")

        if isinstance(event, DurationEvent):
            if not event.is_valid():
                errors.append(
                    f"Event {index} '{event.label}' has invalid duration: start must be less than end."
                )
        elif isinstance(event, PointEvent):
            if not event.is_valid():
                errors.append(
                    f"Event {index} '{event.label}' has invalid point event buffers."
                )

        start, end = event.original_range()
        intervals.append((start, end, event.label))

        if video_duration is not None:
            if start < 0 or end < 0:
                errors.append(f"Event {index} '{event.label}' contains negative time values.")
            if start > video_duration or end > video_duration:
                warnings.append(
                    f"Event {index} '{event.label}' falls outside video duration ({video_duration:.2f}s)."
                )

        valid_label, sanitized = validate_event_label(event.label)
        if not valid_label:
            warnings.append(
                f"Event {index} label '{event.label}' will be sanitized to '{sanitized}'."
            )

    for i in range(len(intervals)):
        for j in range(i + 1, len(intervals)):
            start_a, end_a, label_a = intervals[i]
            start_b, end_b, label_b = intervals[j]
            if start_b < end_a and start_a < end_b:
                warnings.append(
                    f"Event '{label_a}' overlaps with '{label_b}'."
                )

    return errors, warnings
