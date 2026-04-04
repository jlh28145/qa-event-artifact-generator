import json
from pathlib import Path

from qa_event_artifact_generator.cli import main


def test_phase1_smoke_end_to_end(tmp_path, monkeypatch):
    video = tmp_path / "video.mp4"
    events = tmp_path / "events.json"
    output_dir = tmp_path / "output"

    video.write_text("dummy video content", encoding="utf-8")
    events.write_text(
        json.dumps(
            [
                {"label": "LOGIN_SCREEN", "start": "00:00", "end": "00:05"},
                {
                    "label": "ERROR_POPUP",
                    "timestamp": "00:10",
                    "pre_buffer": "00:01",
                    "post_buffer": "00:02",
                },
            ]
        ),
        encoding="utf-8",
    )

    class DummyFFmpeg:
        def __init__(self, ffmpeg_path=None, ffprobe_path=None):
            pass

        def get_video_duration(self, video_path: Path) -> float:
            assert video_path == video
            return 15.0

        def build_segment_command(
            self, source_video: Path, output_clip: Path, start: float, end: float
        ):
            assert source_video == video
            assert output_clip.parent == output_dir
            assert start >= 0
            assert end > start
            return ["echo", "dummy"]

        def execute(self, command):
            assert command == ["echo", "dummy"]
            return None

    monkeypatch.setattr("qa_event_artifact_generator.cli.FFmpegWrapper", DummyFFmpeg)

    result = main(
        [
            "--video",
            str(video),
            "--events",
            str(events),
            "--output",
            str(output_dir),
        ]
    )

    assert result == 0
    metadata_path = output_dir / "metadata.json"
    assert metadata_path.exists()
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    assert metadata["source_video"] == str(video)
    assert len(metadata["clips"]) == 2
