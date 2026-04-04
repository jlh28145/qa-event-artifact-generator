# QA Event Artifact Generator

A Python CLI tool that converts long test recordings into event-based video clips with structured metadata for faster debugging and QA workflows.

## Phase 0 Status
This repository is currently bootstrapped on the `dev` branch and includes the initial package layout, CLI entrypoint, tests, and documentation for development.

## Features
- CLI application scaffold using standard library `argparse`
- project packaging with `pyproject.toml`
- editable install via `pip install -e .`
- basic validation for input paths and output directory creation
- dry-run mode for input validation without generating artifacts

## Requirements
- Python 3.10+
- `ffmpeg` installed and available on `PATH`

## Install
```bash
python -m pip install -e .
```

## Usage
```bash
qa-event-artifact-generator --video path/to/video.mp4 --events path/to/events.manual.json --output output/
```

To validate inputs without generating output:
```bash
qa-event-artifact-generator --video path/to/video.mp4 --events path/to/events.manual.json --output output/ --dry-run
```

## Development
Run tests with:
```bash
pytest
```

## Notes
This project is structured for iterative development on the `dev` branch. Phase 0 focuses on repository setup, packaging, CLI scaffolding, and development tooling.
