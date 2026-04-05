from __future__ import annotations

import re


def safe_filename(value: str) -> str:
    sanitized = re.sub(r"[^A-Za-z0-9._+-]+", "_", value.strip())
    sanitized = sanitized.strip("._- ")
    return sanitized or "clip"
