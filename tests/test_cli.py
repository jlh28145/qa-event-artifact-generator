import json
from pathlib import Path

from qa_event_artifact_generator.cli import FFmpegWrapper, main, parse_args


def test_parse_args():
    args = parse_args([
        "--video",
        "video.mp4",
        "--events",
        "events.json",
        "--output",
        "output",
    ])
    assert args.video == "video.mp4"
    assert args.events == "events.json"
    assert args.output == "output"
    assert not args.dry_run


def test_main_returns_nonzero_for_missing_files(tmp_path):
    result = main(
        [
            "--video",
            str(tmp_path / "missing.mp4"),
            "--events",
            str(tmp_path / "missing.json"),
            "--output",
            str(tmp_path / "out"),
            "--dry-run",
        ]
    )
    assert result == 1


def test_main_validates_paths_and_creates_output_directory(tmp_path, monkeypatch):
    video = tmp_path / "video.mp4"
    events = tmp_path / "events.json"
    video.write_text("dummy video")
    events.write_text(json.dumps([]), encoding="utf-8")

    class DummyFFmpeg:
        def __init__(self):
            pass

        def get_video_duration(self, _):
            return 10.0

    monkeypatch.setattr("qa_event_artifact_generator.cli.FFmpegWrapper", DummyFFmpeg)

    output_dir = tmp_path / "output"
    result = main(
        [
            "--video",
            str(video),
            "--events",
            str(events),
            "--output",
            str(output_dir),
            "--dry-run",
        ]
    )

    assert result == 0
    assert output_dir.exists()
    assert output_dir.is_dir()
