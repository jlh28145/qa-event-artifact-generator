from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List


def write_metadata(metadata_path: Path, source_video: Path, clip_records: List[Dict[str, Any]]) -> None:
    payload: Dict[str, Any] = {
        "source_video": str(source_video),
        "generated_at": datetime.utcnow().replace(microsecond=0).isoformat() + "Z",
        "clips": clip_records,
    }
    metadata_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
