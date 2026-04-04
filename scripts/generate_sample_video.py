#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path

SEGMENTS = [
    ("SESSION_START", 4),
    ("LOGIN_SCREEN", 4),
    ("DASHBOARD", 4),
    ("NAVIGATION", 4),
    ("ERROR_POPUP", 5),
    ("RECOVERY", 4),
    ("SESSION_END", 4),
]

COLORS = [
    "black",
    "navy",
    "darkgreen",
    "maroon",
    "purple",
    "darkorange",
    "darkslategray",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a deterministic sample video using ffmpeg."
    )
    parser.add_argument(
        "--output",
        default="input/fixtures/short_session_video.mp4",
        help="Output video path.",
    )
    parser.add_argument("--width", type=int, default=1280, help="Video width.")
    parser.add_argument("--height", type=int, default=720, help="Video height.")
    parser.add_argument("--fps", type=int, default=30, help="Video frame rate.")
    return parser.parse_args()


def build_ffmpeg_command(output: Path, width: int, height: int, fps: int) -> list[str]:
    ffmpeg = shutil.which("ffmpeg")
    if ffmpeg is None:
        raise RuntimeError("ffmpeg executable not found on PATH")

    inputs = []
    filters = []
    concat_inputs = []
    for index, (label, duration) in enumerate(SEGMENTS):
        color = COLORS[index % len(COLORS)]
        inputs.extend(
            [
                "-f",
                "lavfi",
                "-i",
                f"color=c={color}:s={width}x{height}:d={duration}:r={fps}",
            ]
        )
        text = label.replace("_", " ")
        filters.append(
            f"[{index}:v]drawtext=text='{text}':fontcolor=white:fontsize=42:x=(w-text_w)/2:y=(h-text_h)/2:box=1:boxcolor=black@0.5,drawtext=text='%{{pts\\:hms}}':fontcolor=white:fontsize=24:x=10:y=10:box=1:boxcolor=black@0.5[v{index}]"
        )
        concat_inputs.append(f"[v{index}]")

    filter_complex = (
        ";".join(filters)
        + ";"
        + "".join(concat_inputs)
        + f"concat=n={len(SEGMENTS)}:v=1:a=0[outv]"
    )
    return [
        ffmpeg,
        "-y",
        *inputs,
        "-filter_complex",
        filter_complex,
        "-map",
        "[outv]",
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        str(output),
    ]


def main() -> int:
    args = parse_args()
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    command = build_ffmpeg_command(output_path, args.width, args.height, args.fps)
    print("Running:", " ".join(command))
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr or "ffmpeg failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
