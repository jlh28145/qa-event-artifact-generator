from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path
from typing import List


class FFmpegError(RuntimeError):
    pass


class FFmpegWrapper:
    def __init__(self, ffmpeg_path: str | None = None, ffprobe_path: str | None = None):
        self.ffmpeg_path = ffmpeg_path or shutil.which("ffmpeg")
        self.ffprobe_path = ffprobe_path or shutil.which("ffprobe")
        if self.ffmpeg_path is None:
            raise FFmpegError("ffmpeg executable not found on PATH")
        if self.ffprobe_path is None:
            raise FFmpegError("ffprobe executable not found on PATH")

    def get_video_duration(self, video_path: Path) -> float:
        command = [
            self.ffprobe_path,
            "-v",
            "error",
            "-select_streams",
            "v:0",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(video_path),
        ]
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            raise FFmpegError(result.stderr.strip() or "Unable to read video duration")
        try:
            return float(result.stdout.strip())
        except ValueError as exc:
            raise FFmpegError("Unable to parse video duration") from exc

    def build_segment_command(
        self,
        source_video: Path,
        output_clip: Path,
        start: float,
        end: float,
    ) -> List[str]:
        duration = max(0.0, end - start)
        return [
            self.ffmpeg_path,
            "-y",
            "-ss",
            f"{start:.3f}",
            "-i",
            str(source_video),
            "-t",
            f"{duration:.3f}",
            "-c",
            "copy",
            str(output_clip),
        ]

    def execute(self, command: List[str]) -> None:
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            raise FFmpegError(result.stderr.strip() or "ffmpeg failed")
