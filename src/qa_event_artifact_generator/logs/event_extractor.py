from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, List

from qa_event_artifact_generator.logs.log_parser import LogLine
from qa_event_artifact_generator.models import parse_time


@dataclass
class ExtractedLogEvent:
    label: str
    timestamp: Any
    pre_buffer: float = 0.0
    post_buffer: float = 0.0
    notes: str | None = None
    tags: list[str] = None
    raw: dict[str, Any] = None


class LogExtractionError(ValueError):
    pass


def load_event_rules(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if "rules" not in payload or not isinstance(payload["rules"], list):
        raise LogExtractionError("Event rules JSON must contain a 'rules' list.")
    return payload


def _parse_buffer(value: Any) -> float:
    if value is None:
        return 0.0
    return parse_time(value)


def extract_events_from_log(lines: Iterable[LogLine], rules_config: dict[str, Any]) -> tuple[List[ExtractedLogEvent], List[str]]:
    events: List[ExtractedLogEvent] = []
    warnings: List[str] = []
    default_pre_buffer = _parse_buffer(rules_config.get("default_pre_buffer", 0.0))
    default_post_buffer = _parse_buffer(rules_config.get("default_post_buffer", 0.0))
    for line in lines:
        matched = False
        for rule in rules_config["rules"]:
            pattern = rule.get("pattern")
            if not pattern:
                continue
            if re.search(pattern, line.message, re.IGNORECASE):
                matched = True
                events.append(
                    ExtractedLogEvent(
                        label=rule.get("label", "UNNAMED_EVENT"),
                        timestamp=line.timestamp,
                        pre_buffer=_parse_buffer(rule.get("pre_buffer", default_pre_buffer)),
                        post_buffer=_parse_buffer(rule.get("post_buffer", default_post_buffer)),
                        notes=rule.get("notes"),
                        tags=rule.get("tags", []),
                        raw={"message": line.message, "raw": line.raw},
                    )
                )
                break
        if not matched:
            warnings.append(f"No extraction rule matched log line: {line.raw}")
    return events, warnings
