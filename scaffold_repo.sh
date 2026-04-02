#!/usr/bin/env bash

set -euo pipefail

echo "Scaffolding qa-event-artifact-generator structure in: $(pwd)"

# Top-level files
touch README.md
touch requirements.txt
touch pyproject.toml
touch .gitignore
touch Makefile

# Directories
mkdir -p input/fixtures
mkdir -p output/clips
mkdir -p output/reports
mkdir -p config
mkdir -p scripts
mkdir -p src/qa_event_artifact_generator/segmentation
mkdir -p src/qa_event_artifact_generator/events
mkdir -p src/qa_event_artifact_generator/logs
mkdir -p src/qa_event_artifact_generator/reporting
mkdir -p tests/segmentation
mkdir -p tests/events
mkdir -p tests/logs
mkdir -p tests/fixtures/events
mkdir -p tests/fixtures/logs
mkdir -p docs

# Input files
touch input/sample_video.mp4
touch input/sample_log.txt
touch input/events.manual.json
touch input/fixtures/short_session_video.mp4
touch input/fixtures/happy_path_log.txt
touch input/fixtures/error_path_log.txt
touch input/fixtures/generated_events_example.json

# Output files
touch output/metadata.json

# Config files
touch config/event_rules.json
touch config/clip_defaults.json

# Script files
touch scripts/generate_sample_video.py
touch scripts/generate_sample_log.py
touch scripts/generate_manual_events_json.py

# Source package files
touch src/qa_event_artifact_generator/__init__.py
touch src/qa_event_artifact_generator/cli.py
touch src/qa_event_artifact_generator/models.py
touch src/qa_event_artifact_generator/validators.py
touch src/qa_event_artifact_generator/utils.py

# Segmentation module
touch src/qa_event_artifact_generator/segmentation/__init__.py
touch src/qa_event_artifact_generator/segmentation/segmenter.py
touch src/qa_event_artifact_generator/segmentation/ffmpeg_wrapper.py
touch src/qa_event_artifact_generator/segmentation/metadata_writer.py

# Events module
touch src/qa_event_artifact_generator/events/__init__.py
touch src/qa_event_artifact_generator/events/manual_event_loader.py
touch src/qa_event_artifact_generator/events/event_normalizer.py
touch src/qa_event_artifact_generator/events/event_json_writer.py

# Logs module
touch src/qa_event_artifact_generator/logs/__init__.py
touch src/qa_event_artifact_generator/logs/log_parser.py
touch src/qa_event_artifact_generator/logs/event_extractor.py
touch src/qa_event_artifact_generator/logs/time_sync.py

# Reporting module
touch src/qa_event_artifact_generator/reporting/__init__.py
touch src/qa_event_artifact_generator/reporting/summary.py

# Test files
touch tests/conftest.py
touch tests/test_cli.py
touch tests/test_validators.py
touch tests/test_models.py

# Segmentation tests
touch tests/segmentation/test_segmenter.py
touch tests/segmentation/test_ffmpeg_wrapper.py
touch tests/segmentation/test_metadata_writer.py

# Event tests
touch tests/events/test_manual_event_loader.py
touch tests/events/test_event_normalizer.py
touch tests/events/test_event_json_writer.py

# Log tests
touch tests/logs/test_log_parser.py
touch tests/logs/test_event_extractor.py
touch tests/logs/test_time_sync.py

# Fixture files
touch tests/fixtures/events/valid_events.json
touch tests/fixtures/events/invalid_missing_label.json
touch tests/fixtures/events/invalid_bad_time.json
touch tests/fixtures/events/point_event_example.json

touch tests/fixtures/logs/sample_log_simple.txt
touch tests/fixtures/logs/sample_log_errors.txt
touch tests/fixtures/logs/sample_log_mixed.txt

# Docs
touch docs/architecture.md
touch docs/event-schema.md
touch docs/cli-usage.md
touch docs/roadmap.md

echo "Scaffold complete."