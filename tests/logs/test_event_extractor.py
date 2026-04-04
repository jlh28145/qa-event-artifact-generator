from qa_event_artifact_generator.logs.event_extractor import extract_events_from_log
from qa_event_artifact_generator.logs.log_parser import LogLine


def test_extract_events_from_log_matches_rules():
    rules = {
        "default_pre_buffer": "00:01",
        "default_post_buffer": "00:02",
        "rules": [
            {"pattern": "ERROR", "label": "ERROR", "tags": ["error"], "type": "point"}
        ],
    }
    lines = [LogLine(timestamp=1.0, message="ERROR failed", raw="ERROR failed")]
    events, warnings = extract_events_from_log(lines, rules)
    assert len(events) == 1
    assert events[0].label == "ERROR"
    assert not warnings


def test_extract_events_from_log_warns_when_no_rule_matches():
    rules = {"rules": []}
    lines = [LogLine(timestamp=1.0, message="INFO ok", raw="INFO ok")]
    events, warnings = extract_events_from_log(lines, rules)
    assert not events
    assert warnings
