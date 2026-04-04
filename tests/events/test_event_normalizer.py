from pathlib import Path

from qa_event_artifact_generator.events.event_normalizer import normalize_event
from qa_event_artifact_generator.models import DurationEvent, PointEvent


def test_normalize_duration_event():
    event = DurationEvent(label="demo", start=1.0, end=5.0, notes="note", tags=["a"], pre_buffer=1.0, post_buffer=2.0)
    normalized = normalize_event(event)
    assert normalized["label"] == "demo"
    assert normalized["start"] == 1.0
    assert normalized["end"] == 5.0
    assert normalized["pre_buffer"] == 1.0
    assert normalized["post_buffer"] == 2.0


def test_normalize_point_event():
    event = PointEvent(label="point", timestamp=10.0, notes="note", tags=["x"], pre_buffer=0.5, post_buffer=0.5)
    normalized = normalize_event(event)
    assert normalized["timestamp"] == 10.0
    assert normalized["label"] == "point"
