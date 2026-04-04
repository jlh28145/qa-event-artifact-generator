import argparse
import sys
from pathlib import Path

from qa_event_artifact_generator.events.manual_event_loader import EventLoadingError, load_manual_events
from qa_event_artifact_generator.reporting.summary import summary_message
from qa_event_artifact_generator.segmentation.ffmpeg_wrapper import FFmpegError, FFmpegWrapper
from qa_event_artifact_generator.segmentation.metadata_writer import write_metadata
from qa_event_artifact_generator.segmentation.segmenter import Segmenter
from qa_event_artifact_generator.validators import validate_events


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        prog="qa-event-artifact-generator",
        description=(
            "Convert long test recordings into event-based video clips "
            "and structured metadata."
        ),
    )
    parser.add_argument(
        "--video",
        required=True,
        help="Path to the source video file.",
    )
    parser.add_argument(
        "--events",
        required=True,
        help="Path to the manual events JSON file.",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Directory where clips and metadata will be written.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate inputs without generating clips or metadata.",
    )
    return parser.parse_args(argv)


def validate_path(path: Path, must_exist: bool = True) -> Path:
    if must_exist and not path.exists():
        raise FileNotFoundError(f"Path does not exist: {path}")
    return path


def main(argv=None) -> int:
    args = parse_args(argv)
    try:
        video_path = validate_path(Path(args.video))
        events_path = validate_path(Path(args.events))
        output_path = Path(args.output)
        if output_path.exists() and not output_path.is_dir():
            raise NotADirectoryError(
                f"Output path exists and is not a directory: {output_path}"
            )
        output_path.mkdir(parents=True, exist_ok=True)

        events = load_manual_events(events_path)
        ffmpeg = FFmpegWrapper()
        video_duration = ffmpeg.get_video_duration(video_path)
        errors, warnings = validate_events(events, video_duration=video_duration)

        print(summary_message(video_path, events_path, output_path, len(events), video_duration))
        for warning in warnings:
            print(f"WARNING: {warning}")
        if errors:
            for error in errors:
                print(f"ERROR: {error}", file=sys.stderr)
            return 1

        if args.dry_run:
            print("Dry run complete. Inputs are valid.")
            return 0

        segmenter = Segmenter(ffmpeg)
        clip_records, segment_warnings = segmenter.segment_events(
            video_path, events, output_path, dry_run=False
        )
        for warning in segment_warnings:
            print(f"WARNING: {warning}")

        metadata_path = output_path / "metadata.json"
        write_metadata(metadata_path, video_path, clip_records)
        print(f"Generated {len(clip_records)} clip(s) and metadata to {output_path}")
        return 0
    except (FileNotFoundError, NotADirectoryError, EventLoadingError, FFmpegError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
