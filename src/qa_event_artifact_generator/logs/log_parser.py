from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path
from typing import List

LOG_LINE_PATTERN = re.compile(r"^\s*\[?(?P<timestamp>[^\]]+?)\]?\s+(?P<message>.*)$")


class LogLine:
    def __init__(self, timestamp: datetime | float, message: str, raw: str) -> None:
        self.timestamp = timestamp
        self.message = message
        self.raw = raw


def parse_timestamp(value: str) -> datetime | float:
    value = value.strip()
    date_formats = [
        "%Y-%m-%dT%H:%M:%S.%f",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%d %H:%M:%S.%f",
        "%Y-%m-%d %H:%M:%S",
        "%H:%M:%S",
    ]
    for fmt in date_formats:
        try:
            if fmt == "%H:%M:%S":
                parts = value.split(":")
                return float(parts[0]) * 3600 + float(parts[1]) * 60 + float(parts[2])
            return datetime.strptime(value, fmt)
        except ValueError:
            continue

    raise ValueError(f"Unrecognized timestamp format: {value}")


def parse_log_line(line: str) -> LogLine:
    match = LOG_LINE_PATTERN.match(line)
    if not match:
        raise ValueError("Unable to parse log line")
    timestamp_value = match.group("timestamp").strip()
    try:
        timestamp = parse_timestamp(timestamp_value)
    except ValueError as exc:
        raise ValueError(f"Invalid timestamp '{timestamp_value}': {exc}") from exc
    return LogLine(
        timestamp=timestamp,
        message=match.group("message").strip(),
        raw=line.rstrip("\n"),
    )


def load_log_lines(path: Path) -> tuple[List[LogLine], List[str]]:
    lines: List[LogLine] = []
    warnings: List[str] = []
    for line_number, raw_line in enumerate(
        path.read_text(encoding="utf-8").splitlines(), start=1
    ):
        if not raw_line.strip():
            continue
        try:
            lines.append(parse_log_line(raw_line))
        except ValueError as exc:
            warnings.append(f"Line {line_number}: {exc}")
    return lines, warnings
