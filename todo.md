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
- [ ] Define official `events.manual.json` schema
- [ ] Document required vs optional fields
- [ ] Add JSON example templates
- [ ] Document duration-event vs point-event rules
- [ ] Add schema examples in `docs/event-schema.md`

### JSON Generation Helpers
- [ ] Create `scripts/generate_manual_events_json.py`
- [ ] Allow generating starter JSON from a video path
- [ ] Auto-fill source video path in template
- [ ] Add support for creating numbered placeholder events
- [ ] Add support for generating empty notes/tags fields
- [ ] Add support for global default buffers in template

### Validation UX
- [ ] Add `--dry-run` validation mode
- [ ] Print clear validation errors
- [ ] Warn on overlapping events
- [ ] Fail clearly on out-of-range timestamps
- [ ] Warn on duplicate labels
- [ ] Warn on filenames that would collide after sanitizing

### Possible Future Input Helpers
- [ ] Consider CSV-to-JSON helper
- [ ] Consider converting simple timestamp text files into JSON
- [ ] Consider scaffold command like `init-events`

---

## Phase 2: Log-Driven Event Generation
### Log Input
- [ ] Add `--log` argument
- [ ] Add `--recording-start` argument
- [ ] Add `--event-rules` argument
- [ ] Support text log input format first
- [ ] Document supported log format assumptions

### Parsing
- [ ] Implement raw log reader
- [ ] Parse timestamped log lines
- [ ] Normalize timestamps into internal model
- [ ] Support malformed-line handling
- [ ] Add parser warnings for unreadable lines

### Event Extraction
- [ ] Define event extraction rules
- [ ] Create `config/event_rules.json`
- [ ] Support regex-based event extraction
- [ ] Support severity-based events like ERROR and WARNING
- [ ] Support domain-specific markers like START and END
- [ ] Generate normalized event list from logs

### Time Correlation
- [ ] Convert log timestamps to video offsets
- [ ] Support configurable default buffers around point events
- [ ] Warn on negative offsets
- [ ] Warn on offsets beyond video duration
- [ ] Document time-alignment assumptions

### Outputs
- [ ] Generate `generated_events.json`
- [ ] Feed generated events into segmentation flow
- [ ] Include correlation details in `metadata.json`
- [ ] Add source-log reference to metadata

### Testing
- [ ] Add tests for event extraction
- [ ] Add tests for time sync
- [ ] Add malformed-log handling tests
- [ ] Add end-to-end test for log -> events -> clips flow

---

## Phase 3: Test Data and Fixture Generation

### Goal
Create deterministic, reusable test assets so the project can be tested and demonstrated without relying on real recordings or logs.

---

### Sample Video Generation
- [ ] Define fixed timeline for sample video (35 seconds total)
- [ ] Create segment plan:
  - [ ] SESSION_START (0–4s)
  - [ ] LOGIN_SCREEN (5–9s)
  - [ ] DASHBOARD (10–14s)
  - [ ] NAVIGATION (15–19s)
  - [ ] ERROR_POPUP (20–24s)
  - [ ] RECOVERY (25–29s)
  - [ ] SESSION_END (30–34s)
- [ ] Implement `scripts/generate_sample_video.py`
- [ ] Generate video using ffmpeg
- [ ] Overlay segment labels on screen
- [ ] Overlay timestamp on video
- [ ] Output to `input/fixtures/short_session_video.mp4`
- [ ] Ensure deterministic output (same every run)

---

### Sample Log Generation
- [ ] Implement `scripts/generate_sample_log.py`
- [ ] Define base timestamp for logs
- [ ] Generate happy-path log (no errors)
- [ ] Generate error-path log (includes ERROR event at ~20s)
- [ ] Generate mixed/noisy log (DEBUG, malformed lines, duplicates)
- [ ] Align log timestamps with sample video timeline
- [ ] Output logs to:
  - [ ] `input/fixtures/happy_path_log.txt`
  - [ ] `input/fixtures/error_path_log.txt`

---

### Manual Event JSON Fixtures
- [ ] Create canonical `input/events.manual.json` aligned to sample video
- [ ] Create minimal valid JSON fixture
- [ ] Create duration-event example
- [ ] Create point-event example
- [ ] Create mixed-event example

---

### Invalid JSON Fixtures (Validation Testing)
- [ ] Missing label
- [ ] Invalid time format
- [ ] End before start
- [ ] Overlapping events
- [ ] Timestamp outside video duration
- [ ] Duplicate labels
- [ ] Filename collision scenario

---

### Fixture Quality Goals
- [ ] All fixtures are deterministic
- [ ] No sensitive or real-world data
- [ ] Easy to visually verify correctness
- [ ] Small enough for local testing
- [ ] Representative of real QA scenarios

---

### Why This Matters (Document This)
- [ ] Add explanation in README:
  - [ ] Enables reproducible testing
  - [ ] Avoids dependency on real recordings
  - [ ] Improves CI reliability
  - [ ] Demonstrates engineering discipline

## Phase 4: Reporting and Usability
- [ ] Add terminal summary report
- [ ] Add processing statistics
- [ ] Add warning summary for skipped events
- [ ] Add optional HTML summary report
- [ ] Add summary of clip creation success/failure
- [ ] Add counts by event type
- [ ] Add clear output directory summary

---

## Phase 5: Portfolio Polish
### Positioning
- [ ] Clean README for QA/SDET audience
- [ ] Keep project framed as QA workflow tooling, not just video splitting
- [ ] Emphasize debugging and defect-report artifact generation
- [ ] Keep language generic, not employer-specific

### Presentation
- [ ] Add architecture diagram
- [ ] Add demo screenshots or GIF
- [ ] Add workflow explanation
- [ ] Add “Why this matters for QA” section
- [ ] Add future roadmap
- [ ] Add resume-ready bullet
- [ ] Add before/after workflow example
- [ ] Add example CLI commands section
- [ ] Pin repo on GitHub if polished enough

### Resume / Interview Support
- [ ] Prepare concise project summary for resume
- [ ] Prepare STAR-style interview explanation
- [ ] Prepare tradeoff explanation for why MVP starts with manual JSON before logs
- [ ] Prepare explanation of how synthetic test data improved testability

---

## Future Enhancements
- [ ] CSV-to-JSON conversion
- [ ] Configurable clipping profiles by event type
- [ ] HTML dashboard/report
- [ ] Traceability links for test case / bug report integration
- [ ] More advanced log correlation
- [ ] Semi-automated event capture workflow
- [ ] Optional packaging / PyPI readiness
- [ ] GitHub Actions CI pipeline

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