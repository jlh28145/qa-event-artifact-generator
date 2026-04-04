import json

from qa_event_artifact_generator.events.manual_event_loader import load_manual_events
from qa_event_artifact_generator.models import DurationEvent, PointEvent


def test_load_manual_events_from_list(tmp_path):
    data = [
        {"label": "first", "start": "00:01", "end": "00:03"},
        {"label": "point", "timestamp": "00:05", "pre_buffer": "00:01", "post_buffer": "00:01"},
    ]
    path = tmp_path / "events.json"
    path.write_text(json.dumps(data), encoding="utf-8")

    events = load_manual_events(path)
    assert len(events) == 2
    assert isinstance(events[0], DurationEvent)
    assert isinstance(events[1], PointEvent)
