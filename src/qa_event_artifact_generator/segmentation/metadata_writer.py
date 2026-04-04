from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List


def write_metadata(
    metadata_path: Path,
    source_video: Path,
    clip_records: List[Dict[str, Any]],
    source_log: Path | None = None,
    generated_events_path: Path | None = None,
) -> None:
    payload: Dict[str, Any] = {
        "source_video": str(source_video),
        "generated_at": datetime.utcnow().replace(microsecond=0).isoformat() + "Z",
        "clips": clip_records,
    }
    if source_log is not None:
        payload["source_log"] = str(source_log)
    if generated_events_path is not None:
        payload["generated_events"] = str(generated_events_path)
    metadata_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
