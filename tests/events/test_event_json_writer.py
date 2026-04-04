import json
from pathlib import Path

from qa_event_artifact_generator.events.event_json_writer import write_events_json
from qa_event_artifact_generator.models import DurationEvent


def test_write_events_json(tmp_path):
    path = tmp_path / "generated_events.json"
    events = [DurationEvent(label="a", start=1.0, end=3.0)]
    write_events_json(events, path, defaults={"default_pre_buffer": "00:01"})

    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["default_pre_buffer"] == "00:01"
    assert payload["events"][0]["label"] == "a"
    assert payload["events"][0]["start"] == 1.0
