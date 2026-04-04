from __future__ import annotations

from typing import Any, Dict

from qa_event_artifact_generator.models import DurationEvent, Event, PointEvent


def normalize_event(event: Event) -> Dict[str, Any]:
    base: Dict[str, Any] = {
        "label": event.label,
        "notes": event.notes,
        "tags": event.tags,
        "pre_buffer": event.pre_buffer,
        "post_buffer": event.post_buffer,
    }
    if isinstance(event, DurationEvent):
        base["start"] = event.start
        base["end"] = event.end
    elif isinstance(event, PointEvent):
        base["timestamp"] = event.timestamp
    return {k: v for k, v in base.items() if v is not None and v != []}
