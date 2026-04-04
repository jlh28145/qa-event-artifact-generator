import argparse
import sys
from pathlib import Path

from qa_event_artifact_generator.events.event_json_writer import write_events_json
from qa_event_artifact_generator.events.manual_event_loader import (
    EventLoadingError,
    load_manual_events,
)
from qa_event_artifact_generator.logs.event_extractor import (
    LogExtractionError,
    extract_events_from_log,
    load_event_rules,
)
from qa_event_artifact_generator.logs.log_parser import load_log_lines
from qa_event_artifact_generator.logs.time_sync import correlate_log_events
from qa_event_artifact_generator.reporting.summary import (
    detailed_summary,
    generate_html_report,
    summary_message,
)
from qa_event_artifact_generator.segmentation.ffmpeg_wrapper import (
    FFmpegError,
    FFmpegWrapper,
)
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
        help="Path to the manual events JSON file.",
    )
    parser.add_argument(
        "--log",
        help="Path to the source log file for automated event extraction.",
    )
    parser.add_argument(
        "--recording-start",
        help="Recording start time for log correlation. Use datetime (YYYY-MM-DDTHH:MM:SS) or HH:MM:SS for relative logs.",
    )
    parser.add_argument(
        "--event-rules",
        default="config/event_rules.json",
        help="Path to event extraction rules JSON.",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Directory where clips and metadata will be written.",
    )
    parser.add_argument(
        "--generate-events",
        help="Optional path to write generated events JSON when using log input.",
    )
    parser.add_argument(
        "--html-report",
        help="Optional path to write an HTML summary report.",
    )
    parser.add_argument(
        "--suggest-events",
        action="store_true",
        help="Analyze log file and suggest events without generating clips.",
    )
    return parser.parse_args(argv)


def validate_path(path: Path, must_exist: bool = True) -> Path:
    if must_exist and not path.exists():
        raise FileNotFoundError(f"Path does not exist: {path}")
    return path


def load_events(args, video_duration: float | None):
    if args.events and args.log:
        raise ValueError("Please provide either --events or --log, not both.")
    if args.events:
        events = load_manual_events(validate_path(Path(args.events)))
        return events, args.events, None, []
    if args.log:
        if not args.recording_start and not args.suggest_events:
            raise ValueError(
                "--recording-start is required when using --log (unless --suggest-events)."
            )
        log_path = validate_path(Path(args.log))
        rules_path = validate_path(Path(args.event_rules))
        lines, parse_warnings = load_log_lines(log_path)
        rules = load_event_rules(rules_path)
        extracted_events, extract_warnings = extract_events_from_log(lines, rules)
        if args.suggest_events:
            # For suggestions, return extracted events without correlation
            return extracted_events, args.log, None, parse_warnings + extract_warnings
        synced_events, sync_warnings = correlate_log_events(
            extracted_events, args.recording_start, video_duration=video_duration
        )
        return (
            synced_events,
            args.log,
            Path(args.generate_events) if args.generate_events else None,
            parse_warnings + extract_warnings + sync_warnings,
        )
    raise ValueError("Either --events or --log must be provided.")


def main(argv=None) -> int:
    args = parse_args(argv)
    try:
        video_path = validate_path(Path(args.video))
        output_path = Path(args.output)
        if output_path.exists() and not output_path.is_dir():
            raise NotADirectoryError(
                f"Output path exists and is not a directory: {output_path}"
            )
        output_path.mkdir(parents=True, exist_ok=True)

        ffmpeg = FFmpegWrapper()
        video_duration = ffmpeg.get_video_duration(video_path)

        events, source_path, generated_events_path, event_warnings = load_events(
            args, video_duration
        )
        errors, validation_warnings = validate_events(
            events, video_duration=video_duration
        )

        print(
            summary_message(
                video_path,
                Path(args.events) if args.events else Path(args.log),
                output_path,
                len(events),
                video_duration,
            )
        )
        for warning in event_warnings + validation_warnings:
            print(f"WARNING: {warning}")
        if errors:
            for error in errors:
                print(f"ERROR: {error}", file=sys.stderr)
            return 1

        if args.suggest_events:
            print("\nSuggested Events:")
            for event in events:
                if hasattr(event, "timestamp"):
                    print(f"  {event.label}: {event.timestamp}")
                else:
                    print(
                        f"  {event.label}: {getattr(event, 'start', 'N/A')} - {getattr(event, 'end', 'N/A')}"
                    )
            return 0

        if args.generate_events and args.log:
            write_events_json(
                events,
                generated_events_path,
                defaults={
                    "source_log": str(source_path),
                    "recording_start": args.recording_start,
                },
            )

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
        write_metadata(
            metadata_path,
            video_path,
            clip_records,
            source_log=Path(args.log) if args.log else None,
            generated_events_path=generated_events_path,
        )
        print(f"Generated {len(clip_records)} clip(s) and metadata to {output_path}")
        print(
            detailed_summary(
                events,
                clip_records,
                event_warnings,
                validation_warnings,
                segment_warnings,
                output_path,
            )
        )

        if args.html_report:
            html_path = Path(args.html_report)
            generate_html_report(
                video_path,
                Path(source_path),
                output_path,
                events,
                clip_records,
                event_warnings,
                validation_warnings,
                segment_warnings,
                html_path,
            )
            print(f"HTML report written to {html_path}")

        return 0
    except (
        FileNotFoundError,
        NotADirectoryError,
        EventLoadingError,
        FFmpegError,
        ValueError,
        LogExtractionError,
    ) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
