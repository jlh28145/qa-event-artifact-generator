#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a starter manual events JSON file."
    )
    parser.add_argument("--output", required=True, help="Path to write the JSON file.")
    parser.add_argument(
        "--count", type=int, default=3, help="Number of placeholder events."
    )
    parser.add_argument(
        "--default-pre-buffer",
        default="00:01",
        help="Default pre-buffer for generated events.",
    )
    parser.add_argument(
        "--default-post-buffer",
        default="00:02",
        help="Default post-buffer for generated events.",
    )
    return parser.parse_args()


def build_template(count: int, pre_buffer: str, post_buffer: str) -> dict[str, Any]:
    return {
        "default_pre_buffer": pre_buffer,
        "default_post_buffer": post_buffer,
        "events": [
            {
                "label": f"EVENT_{index + 1}",
                "timestamp": f"00:{index * 5:02d}",
                "notes": "Replace this placeholder with a real event.",
                "tags": [],
            }
            for index in range(count)
        ],
    }


def main() -> int:
    args = parse_args()
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(
            build_template(
                args.count, args.default_pre_buffer, args.default_post_buffer
            ),
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"Wrote manual event template to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
