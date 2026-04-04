# QA Event Artifact Generator

A Python CLI tool that converts long test recordings into event-based video clips with structured metadata for faster debugging and QA workflows.

## Phase 0-1 Completed, Phase 1.5 and Phase 2 In Progress
This repository is currently developed on the `dev` branch. Phase 1 supports manual event segmentation, while Phase 1.5 adds event schema tooling and Phase 2 adds log-driven event generation.

## Requirements
- Python 3.10+
- `ffmpeg` installed and available on `PATH`

## Install
```bash
python -m pip install -e .
```

## Event JSON
The manual event file supports duration and point-in-time events.

Duration event example:
```json
{
  "label": "LOGIN_SCREEN",
  "start": "00:05",
  "end": "00:10",
  "notes": "User logged in",
  "tags": ["login", "ui"]
}
```

Point event example:
```json
{
  "label": "ERROR_POPUP",
  "timestamp": "00:20",
  "pre_buffer": "00:02",
  "post_buffer": "00:03",
  "notes": "Capture error dialog"
}
```

Top-level defaults can be provided using an object with `events`, `default_pre_buffer`, and `default_post_buffer`.

## Usage
```bash
qa-event-artifact-generator --video path/to/video.mp4 --events path/to/events.manual.json --output output/ --dry-run
```

To generate clips and metadata:
```bash
qa-event-artifact-generator --video path/to/video.mp4 --events path/to/events.manual.json --output output/
```

To generate clips from a log file with automatic event extraction:
```bash
qa-event-artifact-generator \
  --video path/to/video.mp4 \
  --log path/to/events.log \
  --recording-start 2026-04-04T12:00:00 \
  --event-rules config/event_rules.json \
  --generate-events output/generated_events.json \
  --output output/
```

## Sample Output
After a successful run, the output directory contains generated clip files and `metadata.json`.
Example metadata structure:
```json
{
  "source_video": "path/to/video.mp4",
  "generated_at": "2026-04-04T12:34:56Z",
  "clips": [
    {
      "label": "LOGIN_SCREEN",
      "clip_path": "output/01-LOGIN_SCREEN.mp4",
      "start": 5.0,
      "end": 10.0,
      "duration": 5.0,
      "notes": "User logged in",
      "tags": ["login", "ui"]
    },
    {
      "label": "ERROR_POPUP",
      "clip_path": "output/02-ERROR_POPUP.mp4",
      "start": 18.0,
      "end": 23.0,
      "duration": 5.0,
      "notes": "Capture error dialog"
    }
  ]
}
```

## Development
Run tests with:
```bash
pytest
```
