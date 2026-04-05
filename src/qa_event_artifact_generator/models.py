from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


def parse_time(value: Any) -> float:
    if isinstance(value, (int, float)):
        return float(value)
    if not isinstance(value, str):
        raise ValueError(f"Unsupported time value: {value!r}")

    value = value.strip()
    if not value:
        raise ValueError("Empty time string")

    parts = value.split(":")
    if len(parts) == 1:
        return float(parts[0])
    if len(parts) == 2:
        minutes, seconds = parts
        return float(minutes) * 60 + float(seconds)
    if len(parts) == 3:
        hours, minutes, seconds = parts
        return float(hours) * 3600 + float(minutes) * 60 + float(seconds)

    raise ValueError(f"Invalid time string: {value}")


def format_time(seconds: float) -> str:
    seconds = max(0.0, float(seconds))
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    remainder = seconds - hours * 3600 - minutes * 60
    if hours:
        return f"{hours:02d}:{minutes:02d}:{remainder:06.3f}".replace(".000", "")
    return f"{minutes:02d}:{remainder:06.3f}".replace(".000", "")


@dataclass
class Event:
    label: str
    notes: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    pre_buffer: float = 0.0
    post_buffer: float = 0.0
    raw: Dict[str, Any] = field(default_factory=dict)

    def metadata(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {
            "label": self.label,
            "notes": self.notes,
            "tags": self.tags,
        }
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class DurationEvent(Event):
    start: float = 0.0
    end: float = 0.0

    def clip_start_end(
        self, video_duration: float | None = None
    ) -> tuple[float, float]:
        start = max(0.0, self.start - self.pre_buffer)
        end = self.end + self.post_buffer
        if video_duration is not None:
            end = min(end, video_duration)
        return start, end

    def is_valid(self) -> bool:
        return self.start < self.end

    def original_range(self) -> tuple[float, float]:
        return self.start, self.end


@dataclass
class PointEvent(Event):
    timestamp: float = 0.0

    def clip_start_end(
        self, video_duration: float | None = None
    ) -> tuple[float, float]:
        start = max(0.0, self.timestamp - self.pre_buffer)
        end = self.timestamp + self.post_buffer
        if video_duration is not None:
            end = min(end, video_duration)
        return start, end

    def is_valid(self) -> bool:
        return self.post_buffer >= 0 and self.pre_buffer >= 0

    def original_range(self) -> tuple[float, float]:
        return self.timestamp, self.timestamp
