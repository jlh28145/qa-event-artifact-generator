from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable

from qa_event_artifact_generator.events.event_normalizer import normalize_event
from qa_event_artifact_generator.models import Event


def write_events_json(
    events: Iterable[Event], path: Path, defaults: dict[str, Any] | None = None
) -> None:
    payload: dict[str, Any] = defaults.copy() if defaults is not None else {}
    payload["events"] = [normalize_event(event) for event in events]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
