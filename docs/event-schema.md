# Event Schema

The manual event JSON file supports duration events and point events. A top-level object may provide default buffer values that apply to all events unless overridden.

## Supported event fields

- `label` (required): event name used for clip metadata and filename generation
- `notes` (optional): description or context
- `tags` (optional): list of strings
- `pre_buffer` / `post_buffer` (optional): time strings to extend the clip before/after the event

Duration event fields:

- `start` (required): event start time
- `end` (required): event end time

Point event fields:

- `timestamp` (required): event time for point-in-time captures

## Time formats

Supported time formats:
- `SS`
- `MM:SS`
- `HH:MM:SS`
- numeric seconds

## Top-level defaults

A top-level object can include these defaults:

- `default_pre_buffer`
- `default_post_buffer`
- `events`

Example:

```json
{
  "default_pre_buffer": "00:01",
  "default_post_buffer": "00:02",
  "events": [
    {
      "label": "SESSION_START",
      "timestamp": "00:00"
    },
    {
      "label": "LOGIN_SCREEN",
      "start": "00:05",
      "end": "00:10"
    }
  ]
}
```
