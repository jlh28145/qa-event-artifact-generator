from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

from qa_event_artifact_generator.models import DurationEvent, Event, PointEvent, parse_time


class EventLoadingError(ValueError):
    pass


def _parse_buffer(value: Any) -> float:
    if value is None:
        return 0.0
    return parse_time(value)


def _load_event(data: Dict[str, Any], defaults: Dict[str, float]) -> Event:
    label = data.get("label")
    if not label or not isinstance(label, str):
        raise EventLoadingError("Each event requires a non-empty label.")

    notes = data.get("notes")
    tags = data.get("tags") or []
    if tags is None:
        tags = []
    if not isinstance(tags, list):
        raise EventLoadingError("Event tags must be a list if provided.")

    pre_buffer = _parse_buffer(data.get("pre_buffer", defaults.get("pre_buffer", 0.0)))
    post_buffer = _parse_buffer(data.get("post_buffer", defaults.get("post_buffer", 0.0)))

    if "start" in data or "end" in data:
        if "start" not in data or "end" not in data:
            raise EventLoadingError("Duration events must include both start and end.")
        start = parse_time(data["start"])
        end = parse_time(data["end"])
        return DurationEvent(
            label=label,
            start=start,
            end=end,
            notes=notes,
            tags=tags,
            pre_buffer=pre_buffer,
            post_buffer=post_buffer,
            raw=data,
        )

    if "timestamp" in data:
        timestamp = parse_time(data["timestamp"])
        return PointEvent(
            label=label,
            timestamp=timestamp,
            notes=notes,
            tags=tags,
            pre_buffer=pre_buffer,
            post_buffer=post_buffer,
            raw=data,
        )

    raise EventLoadingError(
        "Event must include either a start/end range or a timestamp."
    )


def load_manual_events(path: Path) -> List[Event]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, dict):
        defaults: Dict[str, float] = {
            "pre_buffer": _parse_buffer(payload.get("default_pre_buffer", 0.0)),
            "post_buffer": _parse_buffer(payload.get("default_post_buffer", 0.0)),
        }
        event_data = payload.get("events")
        if event_data is None:
            raise EventLoadingError("Top-level JSON object must contain an 'events' list.")
    elif isinstance(payload, list):
        defaults = {"pre_buffer": 0.0, "post_buffer": 0.0}
        event_data = payload
    else:
        raise EventLoadingError("Event JSON must be a list or an object containing an 'events' list.")

    if not isinstance(event_data, list):
        raise EventLoadingError("The 'events' field must be a list of event objects.")

    events: List[Event] = []
    for event_index, item in enumerate(event_data, start=1):
        if not isinstance(item, dict):
            raise EventLoadingError(f"Event at index {event_index} must be an object.")
        events.append(_load_event(item, defaults))

    return events
