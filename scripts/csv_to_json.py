#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert CSV file to events JSON format."
    )
    parser.add_argument("--csv", required=True, help="Path to input CSV file.")
    parser.add_argument("--output", required=True, help="Path to output JSON file.")
    parser.add_argument(
        "--label-column", default="label", help="Column name for event label."
    )
    parser.add_argument(
        "--start-column", default="start", help="Column name for start time."
    )
    parser.add_argument(
        "--end-column", help="Column name for end time (optional for point events)."
    )
    parser.add_argument(
        "--timestamp-column", help="Column name for timestamp (for point events)."
    )
    parser.add_argument("--notes-column", help="Column name for notes.")
    parser.add_argument("--tags-column", help="Column name for tags (comma-separated).")
    return parser.parse_args()


def csv_to_events(csv_path: Path, args) -> list[dict]:
    events = []
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            event = {}
            if args.label_column in row:
                event["label"] = row[args.label_column].strip()
            if args.start_column in row and args.end_column in row:
                event["start"] = row[args.start_column].strip()
                event["end"] = row[args.end_column].strip()
            elif args.timestamp_column in row:
                event["timestamp"] = row[args.timestamp_column].strip()
            if args.notes_column in row and row[args.notes_column].strip():
                event["notes"] = row[args.notes_column].strip()
            if args.tags_column in row and row[args.tags_column].strip():
                event["tags"] = [
                    tag.strip() for tag in row[args.tags_column].split(",")
                ]
            if event:
                events.append(event)
    return events


def main() -> int:
    args = parse_args()
    csv_path = Path(args.csv)
    output_path = Path(args.output)

    if not csv_path.exists():
        print(f"ERROR: CSV file does not exist: {csv_path}", file=sys.stderr)
        return 1

    events = csv_to_events(csv_path, args)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps({"events": events}, indent=2), encoding="utf-8")
    print(f"Converted {len(events)} events to {output_path}")
    return 0


if __name__ == "__main__":
    import sys

    raise SystemExit(main())
