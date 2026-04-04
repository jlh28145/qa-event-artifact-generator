from qa_event_artifact_generator.models import DurationEvent, PointEvent, parse_time


def test_parse_time_seconds_only():
    assert parse_time("30") == 30.0


def test_parse_time_with_minutes():
    assert parse_time("01:30") == 90.0


def test_parse_time_with_hours():
    assert parse_time("01:00:00") == 3600.0


def test_duration_event_clip_range():
    event = DurationEvent(label="demo", start=10.0, end=20.0, pre_buffer=2.0, post_buffer=3.0)
    assert event.clip_start_end() == (8.0, 23.0)


def test_point_event_clip_range():
    event = PointEvent(label="demo", timestamp=15.0, pre_buffer=2.0, post_buffer=3.0)
    assert event.clip_start_end() == (13.0, 18.0)
