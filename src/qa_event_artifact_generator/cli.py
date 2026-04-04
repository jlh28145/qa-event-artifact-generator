import argparse
import sys
from pathlib import Path


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
        help="Validate inputs and paths without generating artifacts.",
    )
    return parser.parse_args(argv)


def validate_path(path: str, *, must_exist: bool = True) -> Path:
    resolved_path = Path(path)
    if must_exist and not resolved_path.exists():
        raise FileNotFoundError(f"Path does not exist: {resolved_path}")
    return resolved_path


def main(argv=None) -> int:
    args = parse_args(argv)
    try:
        video_path = validate_path(args.video)
        events_path = validate_path(args.events)
        output_path = Path(args.output)
        if output_path.exists() and not output_path.is_dir():
            raise NotADirectoryError(
                f"Output path exists and is not a directory: {output_path}"
            )
        output_path.mkdir(parents=True, exist_ok=True)
    except (FileNotFoundError, NotADirectoryError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print("QA Event Artifact Generator")
    print(f"  video: {video_path}")
    print(f"  events: {events_path}")
    print(f"  output: {output_path}")
    if args.dry_run:
        print("Dry run complete. Inputs are valid.")
        return 0

    print("Ready to generate event artifacts.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
