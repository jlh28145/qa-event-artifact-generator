# QA Event Artifact Generator TODO

## Project Goal
Build a Python-based QA tooling project that converts long test recordings into structured, event-level artifacts.

The tool should:
- segment long screen recordings into event-based video clips
- generate structured metadata per clip
- start with manually defined JSON events
- later support generating events automatically from logs
- improve debugging, review, and bug-report artifact quality

---

## Scope Guardrails
- no UI for MVP
- no ML or computer vision in early phases
- no OCR in MVP
- no over-engineering
- prioritize a working CLI pipeline first
- keep the project generic and not tied to one company or product

---

## MVP Definition
Input:
- video file
- manually authored `events.manual.json`

Output:
- segmented video clips
- `metadata.json`

Success criteria:
- one command can process a sample video and event file
- clips are generated correctly
- metadata is valid and readable
- validation errors are clear and actionable

---

## Phase 0: Project Setup
- [x] Create repo
- [x] Add package-style folder structure
- [x] Add `pyproject.toml`
- [x] Add `requirements.txt`
- [x] Add `.gitignore`
- [x] Add `README.md` skeleton
- [x] Add `Makefile`
- [x] Add initial test suite structure
- [x] Confirm `ffmpeg` is installed and callable
- [x] Add `todo.md`
- [x] Add basic dev setup instructions
- [x] Add sample command examples to README
- [x] Decide whether to use `argparse` or `typer` for CLI
- [x] Decide minimal supported Python version

---

## Phase 1: Manual Event-Based Segmentation MVP
### CLI
- [x] Create CLI entrypoint
- [x] Add `--video` argument
- [x] Add `--events` argument
- [x] Add `--output` argument
- [x] Add terminal summary output
- [x] Add non-zero exit codes for failures

### Validation
- [x] Validate video path
- [x] Validate events JSON path
- [x] Validate event schema
- [x] Validate allowed time fields
- [x] Validate start < end for duration events
- [x] Validate timestamp formatting
- [x] Validate events do not exceed video length when possible
- [x] Validate safe clip names
- [x] Warn on overlapping events

### Event Support
- [x] Support duration-based events
- [x] Support point-in-time events with buffers
- [x] Support optional notes field
- [x] Support optional tags field
- [x] Support default pre/post buffers
- [x] Support event-level pre/post buffer overrides

### Segmentation
- [x] Implement ffmpeg wrapper
- [x] Build and validate ffmpeg command generation
- [x] Generate single clip
- [x] Generate multiple clips
- [x] Sanitize filenames
- [x] Handle ffmpeg execution errors cleanly
- [x] Skip or fail gracefully for invalid event ranges

### Metadata
- [x] Write `metadata.json`
- [x] Include source video path
- [x] Include clip file path
- [x] Include event label
- [x] Include timing info
- [x] Include notes and tags when present
- [x] Include duration per clip
- [x] Include generation timestamp
- [x] Include warnings for skipped or adjusted events

### Testing
- [x] Add unit tests for validators
- [x] Add unit tests for event loader
- [x] Add unit tests for filename sanitization
- [x] Add unit tests for ffmpeg command generation
- [x] Add smoke test for end-to-end flow

### README
- [x] Add project overview
- [x] Add install steps
- [x] Add ffmpeg dependency note
- [x] Add manual JSON example
- [x] Add CLI usage example
- [x] Add sample output example

---

## Phase 1.5: Input JSON Generation
### Schema and Authoring
- [x] Define official `events.manual.json` schema
- [x] Document required vs optional fields
- [x] Add JSON example templates
- [x] Document duration-event vs point-event rules
- [x] Add schema examples in `docs/event-schema.md`

### JSON Generation Helpers
- [x] Create `scripts/generate_manual_events_json.py`
- [ ] Allow generating starter JSON from a video path
- [x] Auto-fill source video path in template
- [x] Add support for creating numbered placeholder events
- [x] Add support for generating empty notes/tags fields
- [x] Add support for global default buffers in template

### Validation UX
- [x] Add `--dry-run` validation mode
- [x] Print clear validation errors
- [x] Warn on overlapping events
- [x] Fail clearly on out-of-range timestamps
- [x] Warn on duplicate labels
- [x] Warn on filenames that would collide after sanitizing

### Possible Future Input Helpers
- [ ] Consider CSV-to-JSON helper
- [ ] Consider converting simple timestamp text files into JSON
- [ ] Consider scaffold command like `init-events`

---

## Phase 2: Log-Driven Event Generation
### Log Input
- [x] Add `--log` argument
- [x] Add `--recording-start` argument
- [x] Add `--event-rules` argument
- [x] Support text log input format first
- [x] Document supported log format assumptions

### Parsing
- [x] Implement raw log reader
- [x] Parse timestamped log lines
- [x] Normalize timestamps into internal model
- [x] Support malformed-line handling
- [x] Add parser warnings for unreadable lines

### Event Extraction
- [x] Define event extraction rules
- [x] Create `config/event_rules.json`
- [x] Support regex-based event extraction
- [x] Support severity-based events like ERROR and WARNING
- [x] Support domain-specific markers like START and END
- [x] Generate normalized event list from logs

### Time Correlation
- [x] Convert log timestamps to video offsets
- [x] Support configurable default buffers around point events
- [x] Warn on negative offsets
- [x] Warn on offsets beyond video duration
- [x] Document time-alignment assumptions

### Outputs
- [x] Generate `generated_events.json`
- [x] Feed generated events into segmentation flow
- [x] Include correlation details in `metadata.json`
- [x] Add source-log reference to metadata

### Testing
- [x] Add tests for event extraction
- [x] Add tests for time sync
- [x] Add malformed-log handling tests
- [x] Add end-to-end test for log -> events -> clips flow

---

## Phase 3: Test Data and Fixture Generation

### Goal
Create deterministic, reusable test assets so the project can be tested and demonstrated without relying on real recordings or logs.

---

### Sample Video Generation
- [x] Define fixed timeline for sample video (35 seconds total)
- [x] Create segment plan:
  - [x] SESSION_START (0–4s)
  - [x] LOGIN_SCREEN (5–9s)
  - [x] DASHBOARD (10–14s)
  - [x] NAVIGATION (15–19s)
  - [x] ERROR_POPUP (20–24s)
  - [x] RECOVERY (25–29s)
  - [x] SESSION_END (30–34s)
- [x] Implement `scripts/generate_sample_video.py`
- [x] Generate video using ffmpeg
- [x] Overlay segment labels on screen
- [x] Overlay timestamp on video
- [x] Output to `input/fixtures/short_session_video.mp4`
- [x] Ensure deterministic output (same every run)

---

### Sample Log Generation
- [x] Implement `scripts/generate_sample_log.py`
- [x] Define base timestamp for logs
- [x] Generate happy-path log (no errors)
- [x] Generate error-path log (includes ERROR event at ~20s)
- [x] Generate mixed/noisy log (DEBUG, malformed lines, duplicates)
- [x] Align log timestamps with sample video timeline
- [x] Output logs to:
  - [x] `input/fixtures/happy_path_log.txt`
  - [x] `input/fixtures/error_path_log.txt`
  - [x] `input/fixtures/mixed_path_log.txt`

---

### Manual Event JSON Fixtures
- [x] Create canonical `input/events.manual.json` aligned to sample video
- [x] Create minimal valid JSON fixture
- [x] Create duration-event example
- [x] Create point-event example
- [x] Create mixed-event example

---

### Invalid JSON Fixtures (Validation Testing)
- [x] Missing label
- [x] Invalid time format
- [x] End before start
- [x] Overlapping events
- [x] Timestamp outside video duration
- [x] Duplicate labels
- [x] Filename collision scenario

---

### Fixture Quality Goals
- [x] All fixtures are deterministic
- [x] No sensitive or real-world data
- [x] Easy to visually verify correctness
- [x] Small enough for local testing
- [x] Representative of real QA scenarios

---

### Why This Matters (Document This)
- [x] Add explanation in README:
  - [x] Enables reproducible testing
  - [x] Avoids dependency on real recordings
  - [x] Improves CI reliability
  - [x] Demonstrates engineering discipline

## Phase 4: Reporting and Usability
- [x] Add terminal summary report
- [x] Add processing statistics
- [x] Add warning summary for skipped events
- [x] Add optional HTML summary report
- [x] Add summary of clip creation success/failure
- [x] Add counts by event type
- [x] Add clear output directory summary

---

## Phase 5: Portfolio Polish
### Positioning
- [x] Clean README for QA/SDET audience
- [x] Keep project framed as QA workflow tooling, not just video splitting
- [x] Emphasize debugging and defect-report artifact generation
- [x] Keep language generic, not employer-specific

### Presentation
- [x] Add architecture diagram
- [x] Add workflow explanation
- [x] Add "Why this matters for QA" section
- [x] Add future roadmap
- [x] Add resume-ready bullet
- [x] Add before/after workflow example
- [x] Add example CLI commands section

### Resume / Interview Support
- [x] Prepare concise project summary for resume
- [x] Prepare STAR-style interview explanation
- [x] Prepare tradeoff explanation for why MVP starts with manual JSON before logs
- [x] Prepare explanation of how synthetic test data improved testability

---

## Future Enhancements
- [x] CSV-to-JSON conversion
- [x] Configurable clipping profiles by event type
- [Deferred] HTML dashboard/report
- [Deferred] Traceability links for test case / bug report integration
- [x] More advanced log correlation
- [x] Semi-automated event capture workflow
- [x] Optional packaging / PyPI readiness
- [x] GitHub Actions CI pipeline

---

## Notes
### Recommended Repo Name
`qa-event-artifact-generator`

### Recommended Repo Description
Python CLI tool that converts long test recordings into event-based video clips with structured metadata for faster debugging and QA workflows.

### Positioning Summary
This project should read as:
- a QA workflow acceleration tool
- a structured artifact generator
- a practical automation utility
- a portfolio piece that demonstrates systems thinking, tooling design, validation, and reproducibility

Not as:
- a random video cutting script
- a drone-only internal tool
- an ML project in disguise