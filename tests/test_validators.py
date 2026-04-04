from qa_event_artifact_generator.models import DurationEvent
from qa_event_artifact_generator.validators import validate_events


def test_validate_events_detects_invalid_duration():
    event = DurationEvent(label="bad", start=10.0, end=5.0)
    errors, warnings = validate_events([event])
    assert errors
    assert "start must be less than end" in errors[0]
    assert not warnings


def test_validate_events_warns_overlap():
    event_a = DurationEvent(label="first", start=0.0, end=10.0)
    event_b = DurationEvent(label="second", start=5.0, end=15.0)
    errors, warnings = validate_events([event_a, event_b])
    assert not errors
    assert any("overlaps" in warning for warning in warnings)


def test_validate_events_warns_out_of_range():
    event = DurationEvent(label="out", start=60.0, end=70.0)
    errors, warnings = validate_events([event], video_duration=30.0)
    assert not errors
    assert warnings
