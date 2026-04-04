from pathlib import Path

from qa_event_artifact_generator.models import DurationEvent
from qa_event_artifact_generator.segmentation.ffmpeg_wrapper import FFmpegWrapper
from qa_event_artifact_generator.segmentation.segmenter import Segmenter


def test_build_segment_command(tmp_path, monkeypatch):
    video = tmp_path / "video.mp4"
    video.write_text("binary", encoding="utf-8")

    wrapper = FFmpegWrapper(ffmpeg_path="ffmpeg", ffprobe_path="ffprobe")
    command = wrapper.build_segment_command(video, tmp_path / "clip.mp4", 1.5, 6.5)
    assert command[:4] == ["ffmpeg", "-y", "-ss", "1.500"]
    assert "-t" in command

    segmenter = Segmenter(ffmpeg_wrapper=wrapper)
    assert segmenter.ffmpeg is wrapper
