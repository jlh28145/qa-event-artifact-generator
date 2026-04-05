from datetime import datetime

from qa_event_artifact_generator.logs.event_extractor import ExtractedLogEvent
from qa_event_artifact_generator.logs.time_sync import correlate_log_events


def test_correlate_log_events_relative_time():
    extracted = [
        ExtractedLogEvent(
            label="ERROR", timestamp=10.0, pre_buffer=1.0, post_buffer=2.0
        )
    ]
    synced, warnings = correlate_log_events(extracted, "00:00:00", video_duration=20.0)
    assert synced[0].timestamp == 10.0
    assert not warnings


def test_correlate_log_events_absolute_time():
    extracted = [
        ExtractedLogEvent(
            label="START",
            timestamp=datetime(2026, 4, 4, 12, 0, 5),
            pre_buffer=1.0,
            post_buffer=1.0,
        )
    ]
    synced, warnings = correlate_log_events(
        extracted, "2026-04-04T12:00:00", video_duration=10.0
    )
    assert synced[0].timestamp == 5.0
    assert not warnings
