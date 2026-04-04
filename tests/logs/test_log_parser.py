from qa_event_artifact_generator.logs.log_parser import load_log_lines


def test_load_log_lines_parses_iso_timestamp(tmp_path):
    path = tmp_path / "log.txt"
    path.write_text("2026-04-04T12:00:00 INFO started\n", encoding="utf-8")
    lines, warnings = load_log_lines(path)
    assert len(lines) == 1
    assert not warnings
    assert lines[0].message == "INFO started"


def test_load_log_lines_skips_invalid_lines(tmp_path):
    path = tmp_path / "log.txt"
    path.write_text("bad line\n", encoding="utf-8")
    lines, warnings = load_log_lines(path)
    assert not lines
    assert warnings
