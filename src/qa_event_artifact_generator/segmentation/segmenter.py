from __future__ import annotations

from pathlib import Path
from typing import List

from qa_event_artifact_generator.models import Event
from qa_event_artifact_generator.segmentation.ffmpeg_wrapper import FFmpegWrapper
from qa_event_artifact_generator.utils import safe_filename


class Segmenter:
    def __init__(self, ffmpeg_wrapper: FFmpegWrapper | None = None):
        self.ffmpeg = ffmpeg_wrapper or FFmpegWrapper()

    def segment_events(
        self,
        video_path: Path,
        events: List[Event],
        output_dir: Path,
        dry_run: bool = False,
    ) -> tuple[List[dict], List[str]]:
        video_duration = self.ffmpeg.get_video_duration(video_path)
        output_dir.mkdir(parents=True, exist_ok=True)

        clip_metadata: List[dict] = []
        warnings: List[str] = []

        for index, event in enumerate(events, start=1):
            start, end = event.clip_start_end(video_duration=video_duration)
            if start >= end:
                warnings.append(
                    f"Skipping '{event.label}' because adjusted clip range is invalid."
                )
                continue

            clip_name = f"{index:02d}-{safe_filename(event.label)}.mp4"
            clip_path = output_dir / clip_name
            command = self.ffmpeg.build_segment_command(
                video_path, clip_path, start, end
            )

            if dry_run:
                warnings.append(f"Dry-run command: {' '.join(command)}")
            else:
                self.ffmpeg.execute(command)

            record = {
                "label": event.label,
                "clip_path": str(clip_path),
                "start": start,
                "end": end,
                "duration": end - start,
                **event.metadata(),
            }
            clip_metadata.append(record)

        return clip_metadata, warnings
